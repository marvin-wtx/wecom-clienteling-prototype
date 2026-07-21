#!/usr/bin/env python3
"""Validate the frozen native group-send frame and its project-layer draft bindings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "native-wecom-broadcast-generic"
CSS = ASSET / "native-broadcast-frozen.css"
JS = ASSET / "native-broadcast-frozen.js"


def marked_block(page: str, start: str, end: str) -> tuple[str | None, str]:
    try:
        left = page.index(start) + len(start)
        right = page.index(end, left)
    except ValueError:
        return None, page
    return page[left:right].strip() + "\n", page[: left - len(start)] + page[right + len(end) :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--required", action="store_true", help="fail when the native route is absent")
    args = parser.parse_args()
    page_path = args.case_dir.resolve() / "prototype" / "index.html"
    if not page_path.is_file():
        print("Native broadcast check failed: missing prototype/index.html", file=sys.stderr)
        return 1
    page = page_path.read_text(encoding="utf-8")
    actual_css, outside_css = marked_block(page, "/* native-broadcast-frozen:start */", "/* native-broadcast-frozen:end */")
    actual_js, outside_js = marked_block(page, "// native-broadcast-frozen:start", "// native-broadcast-frozen:end")
    if actual_css is None and actual_js is None and not args.required:
        print("OK: native group-send route is not in scope")
        return 0
    errors: list[str] = []
    frozen_css = CSS.read_text(encoding="utf-8")
    if actual_css != frozen_css:
        errors.append("protected native broadcast CSS differs from frozen component")
    if actual_js != JS.read_text(encoding="utf-8"):
        errors.append("protected native broadcast JavaScript differs from frozen component")
    project_layer = outside_css + outside_js
    for hook in (
        "window.getNativeBroadcastDraft",
        "window.getNativeBroadcastContext",
        "window.openNativeBroadcastMaterialPicker",
        "window.closeNativeBroadcast",
        "window.commitNativeBroadcast",
    ):
        if hook not in project_layer:
            errors.append(f"native group-send route lacks project-layer binding: {hook}")
    if "wxNav('新建群发'" in page:
        errors.append("native group-send route must not add a second mini-program header")
    if re.search(r"(?:WeComShell\.)?nativeSendFrame\s*\(", page):
        errors.append("native group-send route must not use a parent nativeSendFrame navigation wrapper")
    if re.search(r"(?:WeComShell\.)?appShell\s*\(\s*\{[^}]*\bbody\s*:\s*renderWecomExecute\s*\(", page):
        errors.append("renderWecomExecute must not be nested inside appShell")
    direct_mount = re.search(
        r"(?:innerHTML\s*=\s*|return\s+)renderWecomExecute\s*\(\)",
        project_layer,
    )
    if not direct_mount:
        errors.append("native group-send route must mount or return renderWecomExecute() directly")
    if re.search(r"native[-_ ]?(?:task|broadcast)[\s\S]{0,500}?class=[\"'][^\"']*wx-nav", project_layer, re.I):
        errors.append("native group-send route must not inject .wx-nav or an originating task title")
    if "height:calc(74px + var(--status-h))" not in frozen_css or "padding:var(--status-h) 16px 0" not in frozen_css:
        errors.append("frozen native header must reserve the shared status-bar safe area")
    if errors:
        print("Native broadcast check failed:", *[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: native group-send frame is frozen and binds a project broadcast draft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
