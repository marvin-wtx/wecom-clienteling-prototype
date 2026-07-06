#!/usr/bin/env python3
"""Static guardrail checks for generated WeCom clienteling HTML prototypes."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


REQUIRED_TOKENS = [
    ".wx-nav",
    ".wx-capsule",
    ".tabbar",
    "body.mobile",
    "100dvh",
    "detectViewportMode",
    "appShell",
    "journey-hud",
]

FORBIDDEN_PATTERNS = {
    "emoji characters are not allowed in app UI source": re.compile(
        "[\U0001F000-\U0001FAFF\u2600-\u27BF]"
    ),
    "visible viewport selectors are not allowed": re.compile(
        r"(移动全屏|桌面审核台|mobile\s+fullscreen|desktop\s+review|viewSelect)",
        re.IGNORECASE,
    ),
    "legacy mobile shell bug hides the phone frame": re.compile(
        r"body\.mobile(?:-[\w-]+)?\s+\.phone(?:-frame|-wrap)?\s*\{[^}]*display\s*:\s*none",
        re.IGNORECASE | re.DOTALL,
    ),
    "legacy selector-based viewport class is not allowed": re.compile(
        r"mobile-fullscreen|desktop-preview",
        re.IGNORECASE,
    ),
}


def load_external_blocklist() -> list[str]:
    raw = os.environ.get("WECOM_CLIENTELING_FORBIDDEN_TERMS", "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def collect_errors(source: str, path: Path) -> list[str]:
    errors: list[str] = []

    for token in REQUIRED_TOKENS:
        if token not in source:
            errors.append(f"missing required shell token: {token}")

    for message, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(source):
            errors.append(message)

    if re.search(r"<option[^>]+value=[\"']mobile[\"']", source, re.IGNORECASE):
        errors.append("viewport mode must not be exposed as an in-app select option")

    if re.search(r"<script[^>]+src=", source, re.IGNORECASE):
        errors.append("prototype shell must be portable and avoid external script dependencies")

    for term in load_external_blocklist():
        if term and term in source:
            errors.append(f"external blocklist term found: {term}")

    if path.name.lower() != "index.html":
        errors.append("prototype entry file should be named index.html")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a WeCom clienteling prototype HTML file for shell-contract violations."
    )
    parser.add_argument("html", type=Path, help="Path to the generated index.html file")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    source = args.html.read_text(encoding="utf-8")
    errors = collect_errors(source, args.html)

    if errors:
        print("Prototype shell checks failed:", file=sys.stderr)
        for error in errors:
          print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: prototype shell checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
