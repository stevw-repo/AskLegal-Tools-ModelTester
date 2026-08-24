#!/usr/bin/env python3
"""Run Ask.Legal prompt test suites and save Markdown responses."""

from __future__ import annotations

import argparse
import base64
import json
import os
import ssl
import sys
import time
import uuid
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib import error, request


DEFAULT_BASE_URL = "https://dev.ask.legal"
DEFAULT_JURISDICTION = "singapore"
DEFAULT_SUITE = Path("testing/suites/singapore/sg-contract-tort-v1.json")
DEFAULT_OUTPUT_DIR = Path("testing/results")
DEFAULT_API_KEY_FILE = Path("api.txt")
DEFAULT_PARALLEL = 4
ASSISTANT_GREETING = "Hello! I'm the Ask.Legal AI Assistant. How can I help you today?"

StreamResult = namedtuple("StreamResult", ["conversation_id", "content", "raw_chunks"])
QueryResult = namedtuple("QueryResult", ["id", "query", "conversation_id", "content", "error"])


def load_suite(path: Path) -> list[dict[str, str]]:
    """Load a query suite whose entries contain exactly id and query."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError("Suite must be a JSON array.")

    seen_ids = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Suite item {index} must be an object.")
        if set(item.keys()) != {"id", "query"}:
            raise ValueError(f"Suite item {index} must contain exactly 'id' and 'query'.")
        if not isinstance(item["id"], str) or not item["id"].strip():
            raise ValueError(f"Suite item {index} has an invalid id.")
        if not isinstance(item["query"], str) or not item["query"].strip():
            raise ValueError(f"Suite item {index} has an invalid query.")
        if item["id"] in seen_ids:
            raise ValueError(f"Duplicate query id: {item['id']}")
        seen_ids.add(item["id"])

    return data


def assemble_stream_response(body: bytes) -> StreamResult:
    """Assemble Ask.Legal's NDJSON content deltas.

    HAR exports store the octet-stream body as base64. Live HTTP responses are
    expected to be raw NDJSON bytes. This function accepts either form.
    """
    decoded = _decode_body(body)
    conversation_id = ""
    parts: list[str] = []
    chunks: list[dict] = []

    for raw_line in decoded.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        chunk = json.loads(line.decode("utf-8"))
        chunks.append(chunk)
        if chunk.get("conversationId"):
            conversation_id = chunk["conversationId"]
        parts.append(chunk.get("content") or "")

    return StreamResult(conversation_id=conversation_id, content="".join(parts), raw_chunks=chunks)


def _decode_body(body: bytes) -> bytes:
    stripped = body.strip()
    if not stripped:
        return b""
    if stripped.startswith(b"{"):
        return stripped
    try:
        return base64.b64decode(stripped, validate=True)
    except Exception:
        return stripped


def build_ssl_context(ca_bundle: Path | None, insecure: bool) -> ssl.SSLContext:
    """Build the TLS context used for all Ask.Legal API requests."""
    if insecure:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    return ssl.create_default_context(cafile=str(ca_bundle) if ca_bundle else None)


def load_api_key(api_key: str | None, api_key_file: Path | None) -> str:
    """Load the API key without exposing it in command output or result files."""
    if api_key:
        return api_key.strip()

    env_key = os.environ.get("ASKLEGAL_API_KEY", "").strip()
    if env_key:
        return env_key

    if api_key_file and api_key_file.exists():
        raw = api_key_file.read_text(encoding="utf-8").strip()
        if "=" in raw and "\n" not in raw:
            return raw.split("=", 1)[1].strip().strip('"').strip("'")
        return raw

    return ""


def auth_headers(api_key: str) -> dict[str, str]:
    """Return common Ask.Legal auth headers for the same API endpoint."""
    if not api_key:
        return {}
    bearer_value = api_key if api_key.lower().startswith("bearer ") else f"Bearer {api_key}"
    return {
        "Authorization": bearer_value,
        "X-API-Key": api_key,
        "x-access-token": api_key,
    }


def run_query(
    base_url: str,
    jurisdiction: str,
    query: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
) -> StreamResult:
    payload = {
        "conversationId": "null",
        "messages": json.dumps(
            [
                {"role": "assistant", "content": ASSISTANT_GREETING},
                {"role": "user", "content": query},
            ],
            ensure_ascii=False,
        ),
        "jurisdiction": jurisdiction,
    }
    body, content_type = encode_multipart_form(payload)
    endpoint = f"{base_url.rstrip('/')}/api/ai/embedChat"
    req = request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": content_type,
            "Accept": "*/*",
            "Origin": base_url.rstrip("/"),
            "Referer": f"{base_url.rstrip('/')}/en/chatbot",
            "User-Agent": "AskLegalPromptTester/1.0",
            **auth_headers(api_key),
        },
    )

    with request.urlopen(req, timeout=timeout, context=ssl_context) as response:
        stream_result = assemble_stream_response(response.read())

    if stream_result.content.strip():
        return stream_result

    if stream_result.conversation_id:
        retrieved = retrieve_chat(base_url, stream_result.conversation_id, timeout, ssl_context, api_key)
        if retrieved:
            return StreamResult(stream_result.conversation_id, retrieved, stream_result.raw_chunks)

    return stream_result


def encode_multipart_form(fields: dict[str, str]) -> tuple[bytes, str]:
    boundary = f"----AskLegalPromptTester{uuid.uuid4().hex}"
    lines: list[bytes] = []
    for name, value in fields.items():
        lines.extend(
            [
                f"--{boundary}".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"),
                b"",
                value.encode("utf-8"),
            ]
        )
    lines.append(f"--{boundary}--".encode("utf-8"))
    lines.append(b"")
    return b"\r\n".join(lines), f"multipart/form-data; boundary={boundary}"


def retrieve_chat(
    base_url: str,
    conversation_id: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
) -> str:
    endpoint = f"{base_url.rstrip('/')}/api/ai/retrieveChat/{conversation_id}"
    req = request.Request(
        endpoint,
        method="GET",
        headers={"Accept": "application/json", **auth_headers(api_key)},
    )
    try:
        with request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError):
        return ""

    if not isinstance(data, list):
        return ""
    for message in reversed(data):
        if isinstance(message, dict) and message.get("role") == "assistant":
            return message.get("content") or ""
    return ""


def execute_query(
    item: dict[str, str],
    base_url: str,
    jurisdiction: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
) -> QueryResult:
    try:
        stream_result = run_query(
            base_url,
            jurisdiction,
            item["query"],
            timeout,
            ssl_context,
            api_key,
        )
        return QueryResult(
            id=item["id"],
            query=item["query"],
            conversation_id=stream_result.conversation_id,
            content=stream_result.content,
            error="",
        )
    except Exception as exc:
        return QueryResult(
            id=item["id"],
            query=item["query"],
            conversation_id="",
            content="",
            error=f"{type(exc).__name__}: {exc}",
        )


def run_suite(
    suite: list[dict[str, str]],
    base_url: str,
    jurisdiction: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
    delay: float,
    parallel: int,
) -> list[QueryResult]:
    if parallel <= 1:
        results: list[QueryResult] = []
        for index, item in enumerate(suite, start=1):
            print(f"[{index}/{len(suite)}] Sending {item['id']}...", flush=True)
            results.append(execute_query(item, base_url, jurisdiction, timeout, ssl_context, api_key))
            if index < len(suite) and delay > 0:
                time.sleep(delay)
        return results

    results_by_index: dict[int, QueryResult] = {}
    max_workers = min(parallel, len(suite))
    print(f"Running {len(suite)} queries with {max_workers} parallel workers.", flush=True)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(execute_query, item, base_url, jurisdiction, timeout, ssl_context, api_key): index
            for index, item in enumerate(suite)
        }
        for completed_count, future in enumerate(as_completed(futures), start=1):
            index = futures[future]
            result = future.result()
            results_by_index[index] = result
            status = "error" if result.error else "ok"
            print(f"[{completed_count}/{len(suite)}] Finished {result.id} ({status})", flush=True)

    return [results_by_index[index] for index in range(len(suite))]


def render_markdown(
    prompt_version: str,
    jurisdiction: str,
    suite_path: Path,
    base_url: str,
    tls_mode: str,
    results: Iterable[QueryResult],
) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"# Ask.Legal Test Results - {prompt_version}",
        "",
        f"- Jurisdiction: `{jurisdiction}`",
        f"- Suite: `{suite_path}`",
        f"- API base URL: `{base_url}`",
        f"- TLS verification: {tls_mode}",
        f"- Generated at: `{timestamp}`",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"## {result.id}",
                "",
                "**Query**",
                "",
                result.query,
                "",
                "**Conversation ID**",
                "",
                f"`{result.conversation_id or 'n/a'}`",
                "",
                "**Response**",
                "",
            ]
        )
        if result.error:
            lines.extend([f"ERROR: {result.error}", ""])
        else:
            lines.extend([result.content.strip() or "_No response content captured._", ""])

    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Ask.Legal API prompt tests.")
    parser.add_argument("--prompt-version", required=True, help="Prompt label for the output file.")
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE, help="Path to the query suite JSON.")
    parser.add_argument("--jurisdiction", default=DEFAULT_JURISDICTION, help="Ask.Legal jurisdiction value.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Ask.Legal API base URL.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Base output directory.")
    parser.add_argument("--timeout", type=int, default=180, help="Per-query timeout in seconds.")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between queries in seconds.")
    parser.add_argument(
        "--parallel",
        type=int,
        default=DEFAULT_PARALLEL,
        help="Number of queries to send concurrently. Use 1 for sequential execution.",
    )
    parser.add_argument(
        "--api-key",
        help="Ask.Legal API key. Prefer ASKLEGAL_API_KEY or --api-key-file to avoid shell history.",
    )
    parser.add_argument(
        "--api-key-file",
        type=Path,
        default=DEFAULT_API_KEY_FILE,
        help="Path to a local file containing the Ask.Legal API key.",
    )
    tls_group = parser.add_mutually_exclusive_group()
    tls_group.add_argument(
        "--ca-bundle",
        type=Path,
        help="PEM CA bundle to trust instead of the system certificate store.",
    )
    tls_group.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for development testing only.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and list the suite without API calls.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.parallel < 1:
        raise ValueError("--parallel must be at least 1.")

    suite = load_suite(args.suite)

    if args.dry_run:
        for item in suite:
            print(f"{item['id']}: {item['query']}")
        return 0

    ssl_context = build_ssl_context(args.ca_bundle, args.insecure)
    api_key = load_api_key(args.api_key, args.api_key_file)
    if args.insecure:
        tls_mode = "disabled (`--insecure`)"
        print("WARNING: TLS certificate verification is disabled.", file=sys.stderr, flush=True)
    elif args.ca_bundle:
        tls_mode = f"enabled with custom CA bundle `{args.ca_bundle}`"
    else:
        tls_mode = "enabled (system trust store)"

    results = run_suite(
        suite,
        args.base_url,
        args.jurisdiction,
        args.timeout,
        ssl_context,
        api_key,
        args.delay,
        args.parallel,
    )

    output_dir = args.output_dir / args.jurisdiction
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.prompt_version}.md"
    output_path.write_text(
        render_markdown(
            args.prompt_version,
            args.jurisdiction,
            args.suite,
            args.base_url,
            tls_mode,
            results,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
