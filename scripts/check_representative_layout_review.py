#!/usr/bin/env python3
"""Validate Chrome-generated geometry reports before asking for visual acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDER = re.compile(r"replace_with|todo|tbd|待补|待确认", re.I)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def valid_image(root: Path, value: object) -> bool:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return False
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    if not path.is_file() or path.stat().st_size == 0:
        return False
    head = path.read_bytes()[:16]
    return head.startswith(b"\x89PNG\r\n\x1a\n") or head.startswith(b"\xff\xd8\xff") or (head.startswith(b"RIFF") and head[8:12] == b"WEBP")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    report_path = case / "docs" / "representative-layout-review.json"
    intake_path = case / "docs" / "design-intake.json"
    prototype = case / "prototype" / "index.html"
    if any(not path.is_file() for path in (report_path, intake_path, prototype)):
        print("Representative layout review failed:\n- missing layout report, design intake, or prototype", file=sys.stderr)
        return 1
    try:
        report, intake = load(report_path), load(intake_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Representative layout review failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if report.get("skillVersion") != "4.0" or report.get("browser") != "Google Chrome":
        errors.append("layout review must remain V4.0 and use visible Google Chrome")
    if report.get("source") != "window.__wecomLayoutReport":
        errors.append("layout review must come from the runtime geometry probe")
    build_hash = report.get("buildHash")
    actual_hash = hashlib.sha256(prototype.read_bytes()).hexdigest()
    if not isinstance(build_hash, str) or not SHA256.fullmatch(build_hash) or build_hash != actual_hash:
        errors.append("layout review buildHash must match prototype/index.html")
    if not isinstance(report.get("testedAt"), str) or len(report["testedAt"].strip()) < 10:
        errors.append("testedAt must record the visible Chrome run")
    pages = report.get("pages") if isinstance(report.get("pages"), list) else []
    expected = set(intake.get("representativePages", []))
    actual = {item.get("pageId") for item in pages if isinstance(item, dict)}
    if actual != expected or len(pages) != len(expected):
        errors.append("layout review pages must exactly cover representativePages")
    for item in pages:
        if not isinstance(item, dict):
            errors.append("every layout review page must be an object")
            continue
        viewport = item.get("viewport") if isinstance(item.get("viewport"), dict) else {}
        if viewport.get("width") != 390 or viewport.get("height") != 844:
            errors.append(f"{item.get('pageId')} must be checked at 390 × 844")
        if item.get("status") != "pass" or item.get("failures") != []:
            errors.append(f"{item.get('pageId')} has unresolved layout failures")
        metrics = item.get("metrics") if isinstance(item.get("metrics"), dict) else {}
        for key in ("bodyClientHeight", "bodyScrollHeight", "visibleControls", "brokenImages"):
            if not isinstance(metrics.get(key), int) or metrics[key] < 0:
                errors.append(f"{item.get('pageId')} has invalid metric {key}")
        if metrics.get("brokenImages") != 0:
            errors.append(f"{item.get('pageId')} has broken images")
        if not valid_image(report_path.parent, item.get("screenshot")):
            errors.append(f"{item.get('pageId')} needs an existing visible Chrome screenshot")
    checks = report.get("observedChecks") if isinstance(report.get("observedChecks"), dict) else {}
    for key in ("lastContentClearsStickyAction", "stickyActionClearsBottomNavigation", "touchTargetsAtLeast44", "noHorizontalOverflow", "realAssetsLoaded", "boundCountersMatch"):
        if checks.get(key) is not True:
            errors.append(f"observedChecks.{key} must be true")
    observation = report.get("observation")
    if not isinstance(observation, str) or len(observation.strip()) < 24 or PLACEHOLDER.search(observation):
        errors.append("observation must record what was actually seen in Chrome")
    if errors:
        print("Representative layout review failed:", *[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: representative screens passed the Chrome geometry probe before user acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
