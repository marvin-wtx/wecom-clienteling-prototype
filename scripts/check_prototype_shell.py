#!/usr/bin/env python3
"""Static guardrail checks for generated WeCom clienteling HTML prototypes."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path


REQUIRED_TOKENS = [
    "--phone-w: 390px",
    "--phone-h: 844px",
    "--status-h: 38px",
    "--brand-primary",
    "--brand-primary-strong",
    "--brand-accent",
    "--brand-on-primary",
    ".stage",
    ".phone-wrap",
    ".phone",
    "#app { height: 100%; min-height: 0; }",
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
    "reviewModeEnabled",
    'get("review") === "1"',
    "body.review-mode",
]

V4_REVIEW_TOKENS = [
    "mountReviewControls",
    "wecom-review-change",
    "registerAction",
    "wecom-operating-action",
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
    "review guidance must never render inside the phone": re.compile(
        r"journey-hud|journeyHud",
        re.IGNORECASE,
    ),
    "native group-send must not use the retired parent navigation frame": re.compile(
        r"nativeSendFrame|native-send-wrap",
        re.IGNORECASE,
    ),
}


def load_external_blocklist() -> list[str]:
    raw = os.environ.get("WECOM_CLIENTELING_FORBIDDEN_TERMS", "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def collect_errors(source: str, path: Path) -> list[str]:
    errors: list[str] = []
    is_starter_demo = "data-starter-demo=" in source
    runtime_source = ""

    if not is_starter_demo:
        if 'data-wecom-shell-runtime="4.0"' not in source:
            errors.append("missing protected V4.0 shell-runtime marker")
        if not re.search(r'<script[^>]+src=["\']\./shell-runtime\.js["\'][^>]*>', source, re.IGNORECASE):
            errors.append("prototype must load the local protected shell-runtime.js")
        runtime_path = path.parent / "shell-runtime.js"
        if not runtime_path.is_file():
            errors.append("missing protected shell-runtime.js beside index.html")
        else:
            runtime_source = runtime_path.read_text(encoding="utf-8")
            canonical_runtime = Path(__file__).resolve().parent.parent / "assets" / "prototype-shell" / "shell-runtime.js"
            if canonical_runtime.is_file() and hashlib.sha256(runtime_path.read_bytes()).digest() != hashlib.sha256(canonical_runtime.read_bytes()).digest():
                errors.append("shell-runtime.js differs from the protected V4.0 runtime")
        if "WeComShell.afterRender" not in source:
            errors.append("project render path must call WeComShell.afterRender()")

    required_tokens = REQUIRED_TOKENS
    if not is_starter_demo:
        required_tokens = [*REQUIRED_TOKENS, *V4_REVIEW_TOKENS]

    combined_source = source + "\n" + runtime_source
    for token in required_tokens:
        if token not in combined_source:
            errors.append(f"missing required shell token: {token}")

    for message, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(combined_source):
            errors.append(message)

    if re.search(r"<option[^>]+value=[\"']mobile[\"']", source, re.IGNORECASE):
        errors.append("viewport mode must not be exposed as an in-app select option")

    if not re.search(
        r"\.stage-header\s*,\s*\.stage-controls\s*\{\s*display\s*:\s*none",
        source,
        re.IGNORECASE,
    ):
        errors.append("external review header and controls must be hidden outside ?review=1")

    if not re.search(
        r"body\.review-mode\s+\.stage-header\s*,\s*body\.review-mode\s+\.stage-controls\s*\{\s*display\s*:\s*flex",
        source,
        re.IGNORECASE,
    ):
        errors.append("external review controls must be enabled only by review mode")

    if not re.search(
        r"svg\s*\{[^}]*width\s*:\s*1em[^}]*height\s*:\s*1em[^}]*fill\s*:\s*none",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("shell icons need a global svg size and fill guardrail")

    if not re.search(
        r"(?m)^\s*#app\s*\{[^}]*height\s*:\s*100%[^}]*min-height\s*:\s*0",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("app mount must fill the phone screen so bottom navigation cannot float above blank space")

    if not re.search(
        r"(?m)^\s*\.body\s*\{[^}]*flex\s*:\s*1\s+1\s+auto[^}]*min-height\s*:\s*0[^}]*overflow-y\s*:\s*auto",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("page body must be the scroll container inside the fixed phone frame")

    if not re.search(
        r"(?m)^\s*\.tabbar\s*\{[^}]*position\s*:\s*absolute[^}]*bottom\s*:\s*0",
        source,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("bottom navigation must be absolutely pinned to the phone screen bottom")

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

    script_sources = re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", source, re.IGNORECASE)
    if any(script != "./shell-runtime.js" for script in script_sources):
        errors.append("prototype shell may load only the local protected shell-runtime.js")

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
