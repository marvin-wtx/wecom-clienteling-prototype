#!/usr/bin/env python3
"""Validate the manual screenshot evidence required for V3.5 visual QA."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|lorem ipsum|待补|待确认)\b", re.I)
RECIPES = {"precise", "boutique", "vivid"}


def meaningful(value: Any, minimum: int = 24) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def image_exists(root: Path, value: Any) -> bool:
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
    evidence = data.get("visualQualityEvidence")
    if not isinstance(evidence, dict):
        return ["visualQualityEvidence must be an object"]
    if evidence.get("recipe") not in RECIPES:
        errors.append("visualQualityEvidence.recipe must be precise, boutique, or vivid")
    for key in ("desktopFirstViewportScreenshotPath", "mobileFirstViewportScreenshotPath"):
        if not image_exists(root, evidence.get(key)):
            errors.append(f"visualQualityEvidence.{key} must reference an existing screenshot")
    for key in ("normalPhoneScale", "completeShellVisible", "priorityActionDiscoverable", "queueVisuallySubordinate", "honestInitialResult", "noDuplicatePrimaryNavigation", "notEqualWeightCardStack"):
        if evidence.get(key) is not True:
            errors.append(f"visualQualityEvidence.{key} must be true")
    if not meaningful(evidence.get("observedEvidence"), 42):
        errors.append("visualQualityEvidence.observedEvidence must describe the visible hierarchy")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evaluation_json", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.evaluation_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read evaluation: {exc}", file=sys.stderr)
        return 2
    errors = validate(data, args.evaluation_json.parent) if isinstance(data, dict) else ["evaluation root must be an object"]
    if errors:
        print("Visual delivery evidence checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: visual delivery evidence checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
