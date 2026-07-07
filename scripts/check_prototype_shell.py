#!/usr/bin/env python3
"""Static guardrail checks for generated WeCom clienteling HTML prototypes."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


REQUIRED_TOKENS = [
    "--phone-w: 390px",
    "--phone-h: 844px",
    "--status-h: 38px",
    "PROJECT.frontlineTerm",
    "status-network",
    ".wx-nav",
    ".wx-capsule",
    ".wx-capsule-dot",
    ".wx-capsule-circle",
    ".tabbar",
    "body.mobile",
    "100dvh",
    "detectViewportMode",
    "fitDesktopPhone",
    "appShell",
    "has-actions",
    "journey-hud",
    "管理看板",
    "staffPerformance",
    "staffPerformanceRows",
    "managerPeriodPills",
    "按\" + term + \"表现",
    "native-send-wrap",
    "native-brand-tile",
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
    "heavy decorative phone border is not allowed in the reusable shell": re.compile(
        r"border\s*:\s*(?:1[0-9]|[2-9][0-9])px\s+solid",
        re.IGNORECASE,
    ),
    "frontline terminology must not be exposed as a runtime selector": re.compile(
        r"(termSelect|SA\s+通用|FA\s+Fashion|BA\s+美妆|value=[\"']fa[\"']|value=[\"']ba[\"']|<select[^>]+aria-label=[\"'][^\"']*称呼)",
        re.IGNORECASE,
    ),
    "WeCom capsule must not use a home icon as the right-side control": re.compile(
        r"wx-capsule[\s\S]{0,500}(data-icon=[\"']home[\"']|icon\([\"']home[\"']\))",
        re.IGNORECASE,
    ),
    "quick tool panel must not duplicate primary tabs or page-local filters": re.compile(
        r"toolCell\([\"'](?:tasks|appointment|filter)[\"']",
        re.IGNORECASE,
    ),
    "status bar must not use fake signal-dot placeholders": re.compile(
        r"status-dots",
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

    if not re.search(
        r"svg\s*\{[^}]*width\s*:\s*1em[^}]*height\s*:\s*1em[^}]*fill\s*:\s*none",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("shell icons need a global svg size and fill guardrail")

    if not re.search(
        r"\.sticky-actions\s*\{[^}]*position\s*:\s*absolute[^}]*bottom\s*:\s*0",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("secondary-page CTA bars must be absolutely pinned to the shell bottom")

    if not re.search(
        r"(?m)^\s*\.phone::before\s*\{[^}]*content\s*:\s*[\"'][\"'][^}]*background\s*:",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("desktop phone frame must render an iPhone-style notch")

    if not re.search(
        r"(?m)^\s*\.wx-nav-title\s*\{[^}]*top\s*:\s*var\(--status-h\)[^}]*height\s*:\s*calc\(var\(--top-h\)\s*-\s*var\(--status-h\)\)",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("mini-program nav title must be centered in the nav row below the status bar")

    if not re.search(
        r"(?m)^\s*\.wx-nav\s*>\s*\.wx-capsule\s*\{[^}]*top\s*:\s*calc\(var\(--status-h\)\s*\+\s*\(var\(--top-h\)\s*-\s*var\(--status-h\)\)\s*/\s*2\)",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("WeCom capsule must be vertically centered in the nav row below the status bar")

    if not re.search(
        r"body\.mobile\s+\.phone::before[\s\S]{0,160}display\s*:\s*none",
        source,
        re.IGNORECASE,
    ):
        errors.append("mobile full-screen mode must hide the decorative phone notch")

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
