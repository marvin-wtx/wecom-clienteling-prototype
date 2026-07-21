#!/usr/bin/env python3
"""Validate explicit user acceptance of representative branded screens."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")
CRITERIA = {
    "workAndPrimaryActionClear",
    "brandExpressionTraceable",
    "componentStatesDistinct",
    "componentConsistency",
    "mobileReadableAt390x844",
    "protectedUxPreserved",
}


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
    header = path.read_bytes()[:16]
    return header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(b"\xff\xd8\xff") or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    intake_path = case / "docs" / "design-intake.json"
    acceptance_path = case / "docs" / "design-acceptance.json"
    if not intake_path.is_file() or not acceptance_path.is_file():
        print("Design acceptance check failed:\n- missing docs/design-intake.json or docs/design-acceptance.json", file=sys.stderr)
        return 1
    try:
        intake, acceptance = load(intake_path), load(acceptance_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Design acceptance check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if acceptance.get("skillVersion") != "4.0" or acceptance.get("designIntakeRef") != "docs/design-intake.json":
        errors.append("design acceptance must reference the V4.0 design intake")
    if acceptance.get("componentUsageRef") != "docs/component-usage.json":
        errors.append("design acceptance must reference executable component usage")
    if acceptance.get("layoutReviewRef") != "docs/representative-layout-review.json":
        errors.append("design acceptance must reference the pre-acceptance Chrome layout review")
    if acceptance.get("accepted") is not True or acceptance.get("acceptedBy") != "user":
        errors.append("representative screens require explicit user acceptance; the agent may not self-approve")
    if not isinstance(acceptance.get("acceptedBuildHash"), str) or not SHA256.fullmatch(acceptance["acceptedBuildHash"]):
        errors.append("acceptedBuildHash must bind acceptance to the representative build")
    screens = acceptance.get("representativeScreens") if isinstance(acceptance.get("representativeScreens"), list) else []
    accepted_ids = {item.get("pageId") for item in screens if isinstance(item, dict)}
    expected_ids = set(intake.get("representativePages", []))
    if accepted_ids != expected_ids or len(screens) != len(expected_ids):
        errors.append("representativeScreens must exactly cover the design-intake representativePages")
    for item in screens:
        if not isinstance(item, dict) or not valid_image(acceptance_path.parent, item.get("screenshot")):
            errors.append("every representative screen needs an existing relative PNG, JPEG, or WebP screenshot")
            break
    criteria = acceptance.get("criteria") if isinstance(acceptance.get("criteria"), dict) else {}
    if any(criteria.get(key) is not True for key in CRITERIA):
        errors.append("all visual acceptance criteria must be true")
    if acceptance.get("structureRegression") is not False:
        errors.append("structureRegression must remain false")
    if acceptance.get("feedbackApplied") is not True or acceptance.get("remainingPagesMayBeStyled") is not True:
        errors.append("feedback must be applied before remaining pages may be styled")
    observation = acceptance.get("observation")
    if not isinstance(observation, str) or len(observation.strip()) < 24 or re.search(r"replace_with|todo|tbd|待补|待确认", observation, re.I):
        errors.append("observation must record the user decision and visible-browser result")
    if errors:
        print("Design acceptance check failed:", *[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: representative branded screens have explicit user acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
