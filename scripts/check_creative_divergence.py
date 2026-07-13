#!/usr/bin/env python3
"""Validate creative divergence planning in a brand visual token."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "creativeThesis",
    "inspirationTranspositions",
    "divergenceLevers",
    "portfolioContrast",
    "coherenceProof",
]

HIGH_IMPACT_LEVERS = {
    "businessAxis",
    "navigationModel",
    "homeNarrative",
    "detailArchitecture",
    "taskModel",
    "dataStory",
    "signatureInteraction",
    "visualAnchor",
}

VAGUE_THESIS_RE = re.compile(r"\b(premium|modern|elegant|minimalist|luxury|young|gen z|beautiful)\b", re.I)
PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|待补|待确认后补)\b", re.I)


def meaningful_text(value: Any, minimum: int = 18) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    divergence = data.get("creativeDivergence")
    if not isinstance(divergence, dict):
        return ["creativeDivergence must be an object"]

    for key in REQUIRED_TOP_LEVEL:
        if key not in divergence:
            errors.append(f"creativeDivergence missing key: {key}")

    thesis = divergence.get("creativeThesis")
    if not meaningful_text(thesis, 40):
        errors.append("creativeDivergence.creativeThesis must be a concrete operating-thesis sentence")
    elif VAGUE_THESIS_RE.search(str(thesis)):
        errors.append("creativeThesis must use an operating metaphor, not vague style adjectives")

    transpositions = divergence.get("inspirationTranspositions")
    if not isinstance(transpositions, list) or len(transpositions) < 2:
        errors.append("creativeDivergence.inspirationTranspositions must include at least two mechanisms")
    else:
        for index, item in enumerate(transpositions):
            if not isinstance(item, dict):
                errors.append(f"inspirationTranspositions[{index}] must be an object")
                continue
            for key in ("referencePattern", "extractedMechanism", "clientelingTranslation", "rejectionBoundary"):
                if not meaningful_text(item.get(key), 12):
                    errors.append(f"inspirationTranspositions[{index}].{key} must be concrete")

    levers = divergence.get("divergenceLevers")
    if not isinstance(levers, list) or len(levers) < 4:
        errors.append("creativeDivergence.divergenceLevers must include at least four high-impact levers")
    else:
        seen: set[str] = set()
        for index, item in enumerate(levers):
            if not isinstance(item, dict):
                errors.append(f"divergenceLevers[{index}] must be an object")
                continue
            lever = item.get("lever")
            if lever not in HIGH_IMPACT_LEVERS:
                errors.append(f"divergenceLevers[{index}].lever must be one of {sorted(HIGH_IMPACT_LEVERS)}")
            elif lever in seen:
                errors.append(f"divergenceLevers[{index}].lever must be unique")
            seen.add(str(lever))
            if not meaningful_text(item.get("decision"), 12):
                errors.append(f"divergenceLevers[{index}].decision must be concrete")
            if not meaningful_text(item.get("rationale"), 18):
                errors.append(f"divergenceLevers[{index}].rationale must explain business or brand fit")

    contrast = divergence.get("portfolioContrast")
    if not isinstance(contrast, dict):
        errors.append("creativeDivergence.portfolioContrast must be an object")
    else:
        if not meaningful_text(contrast.get("comparisonTarget"), 10):
            errors.append("portfolioContrast.comparisonTarget must name a prior/likely comparison or state no prior case")
        dimensions = contrast.get("differentDimensions")
        if not isinstance(dimensions, list) or len(dimensions) < 3:
            errors.append("portfolioContrast.differentDimensions must include at least three dimensions")
        if not meaningful_text(contrast.get("debrandedDifference"), 24):
            errors.append("portfolioContrast.debrandedDifference must explain what remains distinct without brand styling")

    proof = divergence.get("coherenceProof")
    if not isinstance(proof, dict):
        errors.append("creativeDivergence.coherenceProof must be an object")
    else:
        for key in (
            "navigationFollowsAxis",
            "homeSupportsThesis",
            "detailArchitecturesFit",
            "signatureInteractionChangesWork",
            "workbenchStillScannable",
            "evidenceBoundaryRespected",
        ):
            if not meaningful_text(proof.get(key), 18):
                errors.append(f"coherenceProof.{key} must be concrete")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check creative divergence planning in a visual token.")
    parser.add_argument("json_file", type=Path, help="Path to visual-token JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.json_file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("ERROR: visual token root must be an object", file=sys.stderr)
        return 1

    errors = validate(data)
    if errors:
        print("Creative divergence checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: creative divergence checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
