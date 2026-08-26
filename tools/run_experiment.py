#!/usr/bin/env python3
"""Run one manually deployed Ask.Legal experiment arm and save its artifacts."""

from __future__ import annotations

import argparse
import base64
import math
import json
import os
import re
import ssl
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from http import client as http_client
from pathlib import Path
from typing import Any
from urllib import error, request

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on the local environment
    raise SystemExit("PyYAML 6.x is required: install the 'PyYAML' package.") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = REPO_ROOT / ".env"
DEFAULT_PARALLEL = 5
DEFAULT_RETRIES = 2
DEFAULT_RETRY_DELAY = 2.0
ASSISTANT_GREETING = "Hello! I'm the Ask.Legal AI Assistant. How can I help you today?"
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SENSITIVE_CONFIGURATION_KEY = re.compile(
    r"(?:^|_)(?:api_?key|key|secret|password|passwd|private_?key|"
    r"connection_?string|credential|(?:access|auth|bearer|refresh)_?token|sas)"
    r"(?:$|_)",
    re.IGNORECASE,
)
EXPERIMENT_FIELDS = {
    "format_version",
    "name",
    "jurisdiction",
    "api",
    "suite",
    "expectations",
    "rubric",
    "arms",
}
API_FIELDS = {"base_url", "jurisdiction"}
ARM_FIELDS = {"label", "configuration"}
EXPECTATION_FIELDS = {
    "id",
    "must_cover",
    "must_not_claim",
    "critical_failures",
    "gold_answer",
}


@dataclass(frozen=True)
class StreamResult:
    conversation_id: str
    content: str
    raw_body: bytes


@dataclass(frozen=True)
class QueryResult:
    id: str
    query: str
    conversation_id: str
    response: str
    error: str
    duration_ms: int
    raw_body: bytes
    attempts: int = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def reject_unknown_fields(
    value: dict[Any, Any], allowed: set[str], description: str
) -> None:
    unknown = [key for key in value if not isinstance(key, str) or key not in allowed]
    if unknown:
        names = ", ".join(sorted(repr(key) for key in unknown))
        raise ValueError(f"{description} has unsupported fields: {names}")


def load_experiment(path: Path) -> dict[str, Any]:
    """Load and validate a simple experiment YAML file."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError("Experiment must be a YAML object.")
    if data.get("format_version") != 1:
        raise ValueError("Experiment format_version must be 1.")
    reject_unknown_fields(data, EXPERIMENT_FIELDS, "Experiment")

    for field in ("name", "jurisdiction", "suite", "rubric"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"Experiment field '{field}' must be a non-empty string.")

    api = data.get("api")
    if not isinstance(api, dict):
        raise ValueError("Experiment field 'api' must be an object.")
    reject_unknown_fields(api, API_FIELDS, "Experiment api")
    for field in ("base_url", "jurisdiction"):
        if not isinstance(api.get(field), str) or not api[field].strip():
            raise ValueError(f"Experiment api.{field} must be a non-empty string.")

    expectations = data.get("expectations")
    if expectations is not None and (
        not isinstance(expectations, str) or not expectations.strip()
    ):
        raise ValueError("Experiment field 'expectations' must be a non-empty path when used.")

    arms = data.get("arms")
    if not isinstance(arms, dict) or len(arms) < 2:
        raise ValueError("Experiment must define at least two arms.")
    for arm_name, arm in arms.items():
        if not isinstance(arm_name, str) or not SAFE_ID.fullmatch(arm_name):
            raise ValueError(f"Invalid arm name: {arm_name!r}")
        if not isinstance(arm, dict):
            raise ValueError(f"Arm '{arm_name}' must be an object.")
        reject_unknown_fields(arm, ARM_FIELDS, f"Arm '{arm_name}'")
        label = arm.get("label")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Arm '{arm_name}' must have a non-empty label.")
        configuration = arm.get("configuration")
        if not isinstance(configuration, dict) or not configuration:
            raise ValueError(f"Arm '{arm_name}' must have a non-empty configuration object.")
        validate_configuration(configuration, arm_name)
        try:
            json.dumps(configuration)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Arm '{arm_name}' configuration must contain JSON-compatible values. "
                "Quote values such as ISO dates in YAML."
            ) from exc

    return data


def validate_configuration(value: Any, arm_name: str, path: str = "configuration") -> None:
    """Reject non-string or secret-looking keys from a recorded configuration."""
    if isinstance(value, dict):
        for key, nested in value.items():
            if not isinstance(key, str) or not key:
                raise ValueError(
                    f"Arm '{arm_name}' {path} keys must be non-empty strings."
                )
            if SENSITIVE_CONFIGURATION_KEY.search(key):
                raise ValueError(
                    f"Arm '{arm_name}' {path} contains prohibited secret field: {key}"
                )
            validate_configuration(nested, arm_name, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            validate_configuration(nested, arm_name, f"{path}[{index}]")


def load_questions(path: Path) -> list[dict[str, str]]:
    """Load questions whose entries contain exactly id and query."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list) or not data:
        raise ValueError("Questions must be a non-empty JSON array.")

    seen_ids: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} must be an object.")
        if set(item) != {"id", "query"}:
            raise ValueError(f"Question {index} must contain exactly 'id' and 'query'.")
        if not isinstance(item["id"], str) or not SAFE_ID.fullmatch(item["id"]):
            raise ValueError(f"Question {index} has an invalid id.")
        if not isinstance(item["query"], str) or not item["query"].strip():
            raise ValueError(f"Question {index} has an invalid query.")
        if item["id"] in seen_ids:
            raise ValueError(f"Duplicate question id: {item['id']}")
        seen_ids.add(item["id"])

    return data


def load_expectations(path: Path, question_ids: set[str]) -> list[dict[str, Any]]:
    """Load optional evaluation expectations and match them to suite IDs."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError("Expectations must be a JSON array.")

    seen_ids: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Expectation {index} must be an object.")
        reject_unknown_fields(item, EXPECTATION_FIELDS, f"Expectation {index}")
        item_id = item.get("id")
        if not isinstance(item_id, str) or item_id not in question_ids:
            raise ValueError(f"Expectation {index} does not match a question id.")
        if item_id in seen_ids:
            raise ValueError(f"Duplicate expectation id: {item_id}")
        seen_ids.add(item_id)

        for field in ("must_cover", "must_not_claim", "critical_failures"):
            value = item.get(field)
            if value is not None and (
                not isinstance(value, list)
                or any(not isinstance(entry, str) or not entry.strip() for entry in value)
            ):
                raise ValueError(f"Expectation {item_id} field '{field}' must be a string array.")
        gold_answer = item.get("gold_answer")
        if gold_answer is not None and (
            not isinstance(gold_answer, str) or not gold_answer.strip()
        ):
            raise ValueError(
                f"Expectation {item_id} field 'gold_answer' must be a non-empty string or null."
            )

    return data


def resolve_repo_path(value: str, description: str) -> Path:
    """Resolve a repository-relative path without allowing it to escape the repo."""
    candidate = (REPO_ROOT / value).resolve()
    try:
        candidate.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError(f"{description} must stay inside the repository: {value}") from exc
    if not candidate.is_file():
        raise FileNotFoundError(f"{description} does not exist: {value}")
    return candidate


def relative_repo_path(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def collect_prompt_files(configuration: dict[str, Any]) -> list[Path]:
    """Collect existing repository prompt paths mentioned in a configuration."""
    values: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)
        elif isinstance(value, str) and value.startswith("prompts/"):
            values.append(value)

    walk(configuration)
    return sorted(
        {resolve_repo_path(value, "Prompt") for value in values},
        key=lambda path: path.as_posix(),
    )


def load_api_key(env_file: Path = DEFAULT_ENV_FILE) -> str:
    """Load ASKLEGAL_API_KEY from the environment or ignored root .env file."""
    env_key = os.environ.get("ASKLEGAL_API_KEY", "").strip()
    if env_key:
        return env_key

    if env_file.exists():
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line.removeprefix("export ").strip()
            name, separator, value = line.partition("=")
            if separator and name.strip() == "ASKLEGAL_API_KEY":
                return value.strip().strip('"').strip("'")

    return ""


def auth_headers(api_key: str) -> dict[str, str]:
    token = re.sub(r"^bearer\s+", "", api_key.strip(), flags=re.IGNORECASE).strip()
    if not token:
        return {}
    return {
        "Authorization": f"Bearer {token}",
        "X-API-Key": token,
        "x-access-token": token,
    }


def build_ssl_context(ca_bundle: Path | None, insecure: bool) -> ssl.SSLContext:
    if insecure:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    return ssl.create_default_context(cafile=str(ca_bundle) if ca_bundle else None)


def encode_multipart_form(fields: dict[str, str]) -> tuple[bytes, str]:
    boundary = f"----AskLegalModelTester{uuid.uuid4().hex}"
    lines: list[bytes] = []
    for name, value in fields.items():
        lines.extend(
            [
                f"--{boundary}".encode(),
                f'Content-Disposition: form-data; name="{name}"'.encode(),
                b"",
                value.encode("utf-8"),
            ]
        )
    lines.extend([f"--{boundary}--".encode(), b""])
    return b"\r\n".join(lines), f"multipart/form-data; boundary={boundary}"


def decode_stream_body(body: bytes) -> bytes:
    stripped = body.strip()
    if not stripped or stripped.startswith(b"{"):
        return stripped
    try:
        return base64.b64decode(stripped, validate=True)
    except Exception:
        return stripped


def assemble_stream_response(body: bytes) -> tuple[str, str]:
    """Assemble Ask.Legal NDJSON content deltas from raw or base64 bytes."""
    decoded = decode_stream_body(body)
    conversation_id = ""
    parts: list[str] = []

    for raw_line in decoded.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        chunk = json.loads(line.decode("utf-8"))
        if chunk.get("conversationId"):
            conversation_id = chunk["conversationId"]
        parts.append(chunk.get("content") or "")

    return conversation_id, "".join(parts)


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
            "User-Agent": "AskLegalModelTester/2.0",
            **auth_headers(api_key),
        },
    )

    with request.urlopen(req, timeout=timeout, context=ssl_context) as response:
        raw_body = response.read()

    conversation_id, content = assemble_stream_response(raw_body)
    if not content.strip() and conversation_id:
        content = retrieve_chat(base_url, conversation_id, timeout, ssl_context, api_key)

    return StreamResult(conversation_id, content, raw_body)


def execute_question(
    item: dict[str, str],
    base_url: str,
    jurisdiction: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
    retries: int = DEFAULT_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> QueryResult:
    started = time.perf_counter()
    max_attempts = retries + 1

    for attempt in range(1, max_attempts + 1):
        raw_body = b""
        retryable = False
        try:
            stream = run_query(
                base_url, jurisdiction, item["query"], timeout, ssl_context, api_key
            )
            raw_body = stream.raw_body
            if stream.content.strip():
                return QueryResult(
                    id=item["id"],
                    query=item["query"],
                    conversation_id=stream.conversation_id,
                    response=stream.content,
                    error="",
                    duration_ms=round((time.perf_counter() - started) * 1000),
                    raw_body=stream.raw_body,
                    attempts=attempt,
                )
            error_text = "ValueError: Ask.Legal returned an empty response."
            retryable = True
        except error.HTTPError as exc:
            raw_body = exc.read()
            error_text = f"HTTPError {exc.code}: {exc.reason}"
            pool_timeout = (
                exc.code == 401
                and b"timed out fetching a new connection from the connection pool"
                in raw_body.lower()
            )
            retryable = exc.code == 429 or 500 <= exc.code <= 599 or pool_timeout
        except (
            error.URLError,
            TimeoutError,
            ConnectionError,
            ssl.SSLError,
            http_client.HTTPException,
        ) as exc:
            error_text = f"{type(exc).__name__}: {exc}"
            retryable = True
        except Exception as exc:  # Keep a failed question in the run artifact.
            error_text = f"{type(exc).__name__}: {exc}"

        if retryable and attempt < max_attempts:
            wait_seconds = retry_delay * attempt
            print(
                f"Retrying {item['id']} after attempt {attempt}/{max_attempts} "
                f"({error_text})...",
                flush=True,
            )
            if wait_seconds > 0:
                time.sleep(wait_seconds)
            continue

        return QueryResult(
            id=item["id"],
            query=item["query"],
            conversation_id="",
            response="",
            error=error_text,
            duration_ms=round((time.perf_counter() - started) * 1000),
            raw_body=raw_body,
            attempts=attempt,
        )

    raise AssertionError("Retry loop ended without a result.")


def run_suite(
    questions: list[dict[str, str]],
    base_url: str,
    jurisdiction: str,
    timeout: int,
    ssl_context: ssl.SSLContext,
    api_key: str,
    delay: float,
    parallel: int,
    retries: int = DEFAULT_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> list[QueryResult]:
    if parallel <= 1:
        results: list[QueryResult] = []
        for index, item in enumerate(questions, start=1):
            print(f"[{index}/{len(questions)}] Sending {item['id']}...", flush=True)
            results.append(
                execute_question(
                    item,
                    base_url,
                    jurisdiction,
                    timeout,
                    ssl_context,
                    api_key,
                    retries,
                    retry_delay,
                )
            )
            if index < len(questions) and delay > 0:
                time.sleep(delay)
        return results

    results_by_index: dict[int, QueryResult] = {}
    workers = min(parallel, len(questions))
    print(f"Running {len(questions)} questions with {workers} workers.", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for index, item in enumerate(questions):
            future = executor.submit(
                execute_question,
                item,
                base_url,
                jurisdiction,
                timeout,
                ssl_context,
                api_key,
                retries,
                retry_delay,
            )
            futures[future] = index
            if index < len(questions) - 1 and delay > 0:
                time.sleep(delay)
        for completed, future in enumerate(as_completed(futures), start=1):
            index = futures[future]
            result = future.result()
            results_by_index[index] = result
            status = "error" if result.error else "ok"
            print(f"[{completed}/{len(questions)}] Finished {result.id} ({status})", flush=True)

    return [results_by_index[index] for index in range(len(questions))]


def ensure_run_available(run_dir: Path) -> None:
    if run_dir.exists():
        raise FileExistsError(
            f"Run already exists for this arm: {relative_repo_path(run_dir)}. "
            "Create a new experiment instead of overwriting it."
        )


def write_run(
    run_dir: Path,
    experiment_path: Path,
    experiment: dict[str, Any],
    arm_name: str,
    suite_path: Path,
    expectations_path: Path | None,
    rubric_path: Path,
    prompt_paths: list[Path],
    results: list[QueryResult],
    started_at: str,
    parallel: int,
    timeout: int,
    delay: float,
    tls_mode: str,
    retries: int = DEFAULT_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=False)
    raw_dir = run_dir / "raw"
    response_records: list[dict[str, Any]] = []

    for result in results:
        raw_file: str | None = None
        if result.raw_body:
            raw_dir.mkdir(exist_ok=True)
            raw_path = raw_dir / f"{result.id}.ndjson"
            raw_path.write_bytes(result.raw_body)
            raw_file = raw_path.relative_to(run_dir).as_posix()

        response_records.append(
            {
                "id": result.id,
                "query": result.query,
                "conversation_id": result.conversation_id or None,
                "response": result.response,
                "error": result.error or None,
                "duration_ms": result.duration_ms,
                "attempts": result.attempts,
                "raw_file": raw_file,
            }
        )

    responses_path = run_dir / "responses.jsonl"
    responses_path.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in response_records),
        encoding="utf-8",
    )

    input_files = {
        "experiment": relative_repo_path(experiment_path),
        "suite": relative_repo_path(suite_path),
        "rubric": relative_repo_path(rubric_path),
        "prompts": [relative_repo_path(path) for path in prompt_paths],
    }
    if expectations_path:
        input_files["expectations"] = relative_repo_path(expectations_path)

    arm = experiment["arms"][arm_name]
    errors = sum(bool(result.error) for result in results)
    run_record = {
        "format_version": 1,
        "experiment": experiment["name"],
        "arm": arm_name,
        "label": arm["label"],
        "jurisdiction": experiment["jurisdiction"],
        "api": experiment["api"],
        "configuration": arm["configuration"],
        "started_at": started_at,
        "completed_at": utc_now(),
        "execution": {
            "parallel": parallel,
            "timeout_seconds": timeout,
            "delay_seconds": delay,
            "retries": retries,
            "retry_delay_seconds": retry_delay,
            "tls_verification": tls_mode,
        },
        "inputs": input_files,
        "summary": {
            "questions": len(results),
            "succeeded": len(results) - errors,
            "failed": errors,
        },
    }
    (run_dir / "run.json").write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one manually deployed Ask.Legal experiment arm."
    )
    parser.add_argument("experiment", type=Path, help="Path to experiment.yaml.")
    parser.add_argument("--arm", required=True, help="Arm name from the experiment file.")
    parser.add_argument(
        "--parallel",
        type=int,
        default=DEFAULT_PARALLEL,
        help="Number of concurrent questions (default: 5).",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Seconds between sequential requests or parallel submissions.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help="Retries per question after the initial attempt (default: 2).",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=DEFAULT_RETRY_DELAY,
        help="Base retry delay in seconds; the second retry waits twice as long (default: 2).",
    )
    tls_group = parser.add_mutually_exclusive_group()
    tls_group.add_argument("--ca-bundle", type=Path)
    tls_group.add_argument("--insecure", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--confirm-deployed",
        action="store_true",
        help="Confirm that this arm's configuration has been manually deployed.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.parallel < 1:
            raise ValueError("--parallel must be at least 1.")
        if args.timeout < 1:
            raise ValueError("--timeout must be at least 1 second.")
        if args.delay < 0:
            raise ValueError("--delay cannot be negative.")
        if args.retries < 0:
            raise ValueError("--retries cannot be negative.")
        if not math.isfinite(args.retry_delay):
            raise ValueError("--retry-delay must be finite.")
        if args.retry_delay < 0:
            raise ValueError("--retry-delay cannot be negative.")

        experiment_path = args.experiment.resolve()
        try:
            experiment_path.relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ValueError("Experiment file must be inside the repository.") from exc

        experiment = load_experiment(experiment_path)
        if args.arm not in experiment["arms"]:
            choices = ", ".join(experiment["arms"])
            raise ValueError(f"Unknown arm '{args.arm}'. Available arms: {choices}")

        suite_path = resolve_repo_path(experiment["suite"], "Suite")
        questions = load_questions(suite_path)
        expectations_path = None
        if experiment.get("expectations"):
            expectations_path = resolve_repo_path(experiment["expectations"], "Expectations")
            load_expectations(expectations_path, {item["id"] for item in questions})
        rubric_path = resolve_repo_path(experiment["rubric"], "Rubric")
        arm = experiment["arms"][args.arm]
        prompt_paths = collect_prompt_files(arm["configuration"])

        run_dir = experiment_path.parent / "runs" / args.arm

        print(f"Experiment: {experiment['name']}")
        print(f"Arm: {args.arm} ({arm['label']})")
        print(f"Suite: {relative_repo_path(suite_path)} ({len(questions)} questions)")
        print("Configuration:")
        print(yaml.safe_dump(arm["configuration"], sort_keys=False).rstrip())
        print(f"Output: {relative_repo_path(run_dir)}")

        if args.dry_run:
            print("Dry run complete; no API requests or files were created.")
            return 0
        ensure_run_available(run_dir)
        if not args.confirm_deployed:
            raise ValueError(
                "Live runs require --confirm-deployed after manually deploying this arm."
            )

        api_key = load_api_key()
        if not api_key:
            raise ValueError(
                "No API key found. Set ASKLEGAL_API_KEY in the environment or root .env file."
            )

        ssl_context = build_ssl_context(args.ca_bundle, args.insecure)
        if args.insecure:
            tls_mode = "disabled"
            print("WARNING: TLS certificate verification is disabled.", file=sys.stderr)
        elif args.ca_bundle:
            tls_mode = f"custom CA bundle: {args.ca_bundle}"
        else:
            tls_mode = "enabled"

        started_at = utc_now()
        results = run_suite(
            questions=questions,
            base_url=experiment["api"]["base_url"],
            jurisdiction=experiment["api"]["jurisdiction"],
            timeout=args.timeout,
            ssl_context=ssl_context,
            api_key=api_key,
            delay=args.delay,
            parallel=args.parallel,
            retries=args.retries,
            retry_delay=args.retry_delay,
        )
        write_run(
            run_dir=run_dir,
            experiment_path=experiment_path,
            experiment=experiment,
            arm_name=args.arm,
            suite_path=suite_path,
            expectations_path=expectations_path,
            rubric_path=rubric_path,
            prompt_paths=prompt_paths,
            results=results,
            started_at=started_at,
            parallel=args.parallel,
            timeout=args.timeout,
            delay=args.delay,
            tls_mode=tls_mode,
            retries=args.retries,
            retry_delay=args.retry_delay,
        )
        print(f"Wrote {relative_repo_path(run_dir)}")
        return 1 if any(result.error for result in results) else 0
    except (FileNotFoundError, FileExistsError, OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
