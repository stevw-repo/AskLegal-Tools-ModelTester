#!/usr/bin/env python3
"""List Azure environment-variable names without printing their values."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = REPO_ROOT / ".env.azure.local"
VALID_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
SENSITIVE_NAME = re.compile(
    r"(?:API[_-]?KEY|(?:^|[_-])KEY$|SECRET|PASSWORD|PASSWD|PRIVATE[_-]?KEY|"
    r"CONNECTION[_-]?STRING|CONNSTR|CREDENTIAL|CERTIFICATE|DATABASE[_-]?URL|"
    r"(?:ACCESS|AUTH|BEARER|REFRESH)[_-]?TOKEN|SAS(?:$|[_-]))",
    re.IGNORECASE,
)


def names_from_json(data: Any) -> list[str]:
    if isinstance(data, list):
        names = [item.get("name") for item in data if isinstance(item, dict)]
    elif isinstance(data, dict):
        properties = data.get("properties")
        names = list(properties) if isinstance(properties, dict) else list(data)
    else:
        raise ValueError("Azure JSON must be an object or array.")

    return validate_names(names)


def names_from_dotenv(text: str) -> list[str]:
    names: list[str] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        name, separator, _value = line.partition("=")
        if not separator:
            raise ValueError(f"Line {line_number} is not NAME=VALUE format.")
        names.append(name.strip())
    return validate_names(names)


def validate_names(names: list[Any]) -> list[str]:
    clean: list[str] = []
    for name in names:
        if not isinstance(name, str) or not VALID_NAME.fullmatch(name):
            raise ValueError(f"Invalid environment-variable name: {name!r}")
        clean.append(name)
    return sorted(set(clean), key=str.casefold)


def load_names(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if not stripped or all(not line.strip() or line.lstrip().startswith("#") for line in text.splitlines()):
        return []
    if stripped.startswith("[") or stripped.startswith("{"):
        return names_from_json(json.loads(text))
    return names_from_dotenv(text)


def is_likely_secret(name: str) -> bool:
    return bool(SENSITIVE_NAME.search(name))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List Azure setting names without displaying their values."
    )
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        names = load_names(args.path)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not names:
        print("No variables found.")
        return 0

    configuration = [name for name in names if not is_likely_secret(name)]
    secrets = [name for name in names if is_likely_secret(name)]

    print("Configuration candidates (names only):")
    for name in configuration:
        print(f"- {name}")
    print("\nLikely secrets (names only; do not copy into experiments):")
    for name in secrets:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
