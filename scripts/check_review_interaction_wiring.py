#!/usr/bin/env python3
"""Catch static signs of disconnected reviewer controls and staged completion."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prototype_html", type=Path)
    args = parser.parse_args()
    try:
        source = args.prototype_html.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read prototype: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    if re.search(r"\bentries\s*:\s*\[", source):
        if "wecom-review-change" not in source or not re.search(r"type\s*={2,3}\s*[\"']entry[\"']", source):
            errors.append("configured Review Entry controls are not wired to a wecom-review-change entry handler")
    if 'data-home-primary="daily-work"' not in source and "data-home-primary='daily-work'" not in source:
        errors.append("home must expose a daily-work marker")
    if "data-operating-outcome" not in source:
        errors.append("home must expose a visible operating outcome marker")
    if re.search(r"taskResultRecord\s*:\s*\{[\s\S]{0,320}?\bdone\s*:\s*[1-9]", source):
        errors.append("initial task state pre-seeds a completed result; start the validated loop from an open item")
    for match in re.finditer(r"<button\b([^>]*)>", source, re.I):
        attrs = match.group(1)
        if re.search(r"\bdisabled\b|\bonclick\s*=|\bdata-(?:back|route|operating-action|review-control|review-entry|stage-action)\s*=", attrs, re.I):
            continue
        errors.append("visible button lacks a click handler or routed data action")
        break
    if errors:
        print("Review interaction wiring checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: review interaction wiring checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
