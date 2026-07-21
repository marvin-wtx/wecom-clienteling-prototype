#!/usr/bin/env python3
"""Require the protected V4.0 workbench focus and result primitives."""
from __future__ import annotations
import argparse
import hashlib
import re
import sys
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prototype_html", type=Path)
    args = parser.parse_args()
    source = args.prototype_html.read_text(encoding="utf-8")
    sparse = 'data-brief-mode="sparse"' in source or "data-brief-mode='sparse'" in source
    required = ("data-workbench-priority", "data-workbench-result") if sparse else ("data-workbench-priority", "data-workbench-queue", "data-workbench-result")
    missing = [marker for marker in required if marker not in source]
    required_classes = ("wb-priority", "wb-result") if sparse else ("wb-priority", "wb-queue", "wb-result")
    missing_classes = [name for name in required_classes if name not in source]
    if not re.search(r'data-workbench-style=["\'](?:precise|boutique|vivid)["\']', source):
        missing.append('a data-workbench-style recipe (precise, boutique, or vivid)')
    if not re.search(r'<link[^>]+href=["\']\.?/workbench-visual-primitives\.css["\']', source, re.I):
        missing.append('a local workbench-visual-primitives.css stylesheet link')
    primitives = args.prototype_html.parent / "workbench-visual-primitives.css"
    canonical = Path(__file__).resolve().parent.parent / "assets" / "prototype-shell" / "workbench-visual-primitives.css"
    if not primitives.is_file():
        missing.append("protected workbench-visual-primitives.css beside index.html")
    elif canonical.is_file() and hashlib.sha256(primitives.read_bytes()).digest() != hashlib.sha256(canonical.read_bytes()).digest():
        missing.append("unchanged protected workbench-visual-primitives.css")
    missing.extend(f"a {name} primitive class" for name in missing_classes)
    if missing:
        print("Workbench composition checks failed:", file=sys.stderr)
        print(*[f"- missing {marker}" for marker in missing], sep="\n", file=sys.stderr)
        return 1
    print("OK: workbench composition checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
