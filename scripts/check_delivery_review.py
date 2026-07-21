#!/usr/bin/env python3
"""Validate one concise, visible-browser acceptance record for V4.0."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"replace_with|todo|tbd|待补|待确认", re.I)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def meaningful(value: Any, minimum: int = 12) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def valid_screenshot(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
        return False
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    if not path.is_file() or path.stat().st_size == 0:
        return False
    header = path.read_bytes()[:16]
    return header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(b"\xff\xd8\xff") or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")


def validate(data: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if data.get("skillVersion") != "4.0":
        errors.append('skillVersion must remain "4.0"')
    if data.get("browser") != "Google Chrome":
        errors.append("browser must record Google Chrome visible-browser acceptance")
    if not meaningful(data.get("testedUrl"), 8) or not meaningful(data.get("checkedAt"), 10):
        errors.append("testedUrl and checkedAt must be recorded")
    if not isinstance(data.get("buildHash"), str) or not SHA256_RE.fullmatch(data["buildHash"]):
        errors.append("buildHash must be the SHA-256 of the tested prototype HTML")
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    for key in ("mobileFirstViewportComplete", "tabbarTouchesBottom", "longPageScrolls", "journeyValuesPersist", "allVisibleInteractionsWork"):
        if checks.get(key) is not True:
            errors.append(f"checks.{key} must be true")
    for key in ("consoleErrors", "brokenImages"):
        if checks.get(key) != 0:
            errors.append(f"checks.{key} must be 0")
    if not meaningful(data.get("primaryJourneyId"), 4):
        errors.append("primaryJourneyId must identify the confirmed Journey")
    journey = data.get("journey") if isinstance(data.get("journey"), list) else []
    if len(journey) < 4 or not all(isinstance(item, str) and len(item.strip()) >= 2 for item in journey):
        errors.append("journey must record at least four observed steps")
    pages = data.get("selectedPagesChecked") if isinstance(data.get("selectedPagesChecked"), list) else []
    if not pages or len(pages) != len(set(pages)) or not all(isinstance(item, str) and item.strip() for item in pages):
        errors.append("selectedPagesChecked must list each checked selected page once")
    shots = data.get("screenshots") if isinstance(data.get("screenshots"), list) else []
    if not 1 <= len(shots) <= 6 or not all(valid_screenshot(root, item) for item in shots):
        errors.append("screenshots must contain one to six existing relative image paths")
    if not meaningful(data.get("observation"), 24):
        errors.append("observation must briefly describe what was actually seen")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_json", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.review_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read review: {exc}", file=sys.stderr)
        return 2
    errors = validate(data, args.review_json.parent) if isinstance(data, dict) else ["review root must be an object"]
    if errors:
        print("Browser acceptance checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: concise visible-browser acceptance record passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
