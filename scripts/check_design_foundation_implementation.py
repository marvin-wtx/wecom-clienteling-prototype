#!/usr/bin/env python3
"""Verify that the confirmed component UX foundation is visible in the prototype."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def has_marker(source: str, name: str, value: str) -> bool:
    return bool(re.search(rf"\b{re.escape(name)}\s*=\s*['\"]{re.escape(value)}['\"]", source))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    html_path = case / "prototype" / "index.html"
    css_path = case / "prototype" / "workbench-visual-primitives.css"
    intake_path = case / "docs" / "design-intake.json"
    if not html_path.is_file() or not css_path.is_file() or not intake_path.is_file():
        print("Design foundation implementation check failed:\n- missing prototype HTML, visual primitives, or design intake", file=sys.stderr)
        return 1
    try:
        source = html_path.read_text(encoding="utf-8")
        style_source = css_path.read_text(encoding="utf-8")
        intake = load(intake_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Design foundation implementation check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    for component in intake.get("foundationComponents", []):
        if not has_marker(source, "data-ux-component", component):
            errors.append(f"confirmed UX component is not marked in HTML: {component}")
    for state in intake.get("requiredStates", []):
        if not has_marker(source, "data-ux-state", state):
            errors.append(f"confirmed UX state is not visibly represented: {state}")
    combined = source + "\n" + style_source
    if not re.search(r"--ux-touch-min\s*:\s*44px", combined):
        errors.append("project CSS must declare --ux-touch-min: 44px")
    if not re.search(r"min-height\s*:\s*var\(--ux-touch-min\)", combined):
        errors.append("interactive project CSS must use the 44px touch-target token")
    if errors:
        print("Design foundation implementation check failed:", *[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: confirmed component UX foundation is implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
