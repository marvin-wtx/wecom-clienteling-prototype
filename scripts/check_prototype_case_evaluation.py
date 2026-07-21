#!/usr/bin/env python3
"""Validate visible, before-and-after evidence for a V3.5 prototype."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from check_visual_delivery_evidence import validate as validate_visual_evidence

PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|lorem ipsum|待补|待确认)\b", re.I)
CORE_SURFACES = {"home", "c360", "task-detail"}


def meaningful(value: Any, minimum: int = 18) -> bool:
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
    if not meaningful(data.get("caseId"), 6):
        errors.append("caseId must be concrete")
    scope = data.get("scope")
    included = scope.get("includedSurfaces") if isinstance(scope, dict) else []
    if not isinstance(included, list) or not CORE_SURFACES.issubset(set(included)):
        errors.append("scope.includedSurfaces must include home, c360, and task-detail")
    operating = data.get("operatingEvidence")
    if not isinstance(operating, dict) or not meaningful(operating.get("role"), 3):
        errors.append("operatingEvidence.role must be visible and concrete")
    elif not isinstance(operating.get("dailyJobsObserved"), list) or len(operating["dailyJobsObserved"]) < 2:
        errors.append("operatingEvidence.dailyJobsObserved must name two jobs")
    elif operating.get("firstViewportVerdict") != "pass" or not meaningful(operating.get("firstViewportEvidence"), 28):
        errors.append("operatingEvidence must record a passing, concrete first-viewport result")
    desktop = data.get("desktopReviewEvidence")
    if not isinstance(desktop, dict):
        errors.append("desktopReviewEvidence must be an object")
    else:
        if not image_exists(root, desktop.get("screenshotPath")):
            errors.append("desktopReviewEvidence.screenshotPath must reference an existing desktop screenshot")
        if desktop.get("fullPhoneVisible") is not True:
            errors.append("desktopReviewEvidence.fullPhoneVisible must be true")
        if desktop.get("controlsOutsidePhone") is not True:
            errors.append("desktopReviewEvidence.controlsOutsidePhone must be true")
        if not meaningful(desktop.get("observedEvidence"), 32):
            errors.append("desktopReviewEvidence.observedEvidence must describe the complete desktop frame")
    rendered = data.get("renderedEvidence")
    seen: set[str] = set()
    if not isinstance(rendered, list):
        errors.append("renderedEvidence must be a list")
    else:
        for index, item in enumerate(rendered):
            if not isinstance(item, dict):
                errors.append(f"renderedEvidence[{index}] must be an object")
                continue
            if item.get("surface") in CORE_SURFACES:
                seen.add(item["surface"])
            if not image_exists(root, item.get("screenshotPath")):
                errors.append(f"renderedEvidence[{index}] must reference an existing screenshot")
            if item.get("verdict") != "pass" or not meaningful(item.get("observedEvidence"), 28):
                errors.append(f"renderedEvidence[{index}] needs a passing concrete observation")
    if CORE_SURFACES - seen:
        errors.append(f"renderedEvidence misses core surfaces: {sorted(CORE_SURFACES - seen)}")
    interactions = data.get("interactionEvidence")
    if not isinstance(interactions, list) or len(interactions) < 3:
        errors.append("interactionEvidence must include three observed interactions")
    else:
        for index, item in enumerate(interactions):
            if not isinstance(item, dict):
                errors.append(f"interactionEvidence[{index}] must be an object")
                continue
            for key in ("entry", "action", "expectedResult", "observedResult"):
                if not meaningful(item.get(key), 14):
                    errors.append(f"interactionEvidence[{index}].{key} must be concrete")
            for key in ("beforeScreenshotPath", "afterScreenshotPath"):
                if not image_exists(root, item.get(key)):
                    errors.append(f"interactionEvidence[{index}].{key} must reference an existing screenshot")
            if item.get("verdict") != "pass":
                errors.append(f"interactionEvidence[{index}].verdict must pass")
    fresh = data.get("freshStateEvidence")
    if not isinstance(fresh, dict):
        errors.append("freshStateEvidence must prove an open item became a named home-workbench result")
    else:
        if fresh.get("initialState") != "open":
            errors.append("freshStateEvidence.initialState must be open")
        if not meaningful(fresh.get("action"), 14) or not meaningful(fresh.get("homeOutcome"), 24):
            errors.append("freshStateEvidence needs a concrete action and homeOutcome")
        for key in ("beforeScreenshotPath", "afterScreenshotPath"):
            if not image_exists(root, fresh.get(key)):
                errors.append(f"freshStateEvidence.{key} must reference an existing screenshot")
    quality = data.get("humanQuality")
    for key in ("operatingClarity", "interactionReliability", "brandExpression", "presentationReadiness"):
        item = quality.get(key) if isinstance(quality, dict) else None
        if not isinstance(item, dict) or not isinstance(item.get("score"), int) or not 4 <= item["score"] <= 5 or not meaningful(item.get("evidence"), 24):
            errors.append(f"humanQuality.{key} must score 4–5 with visible evidence")
    release = data.get("releaseDecision")
    if not isinstance(release, dict) or release.get("result") != "pass" or release.get("blockers") != [] or not meaningful(release.get("notes"), 20):
        errors.append("releaseDecision must pass with no blockers and concrete notes")
    errors.extend(validate_visual_evidence(data, root))
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
        print("Prototype case evaluation checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: prototype case evaluation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
