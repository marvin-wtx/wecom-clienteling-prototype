#!/usr/bin/env python3
"""Validate screenshot-backed quality evidence for a branded prototype case."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ARCHETYPES = {
    "priority-queue",
    "appointment-atelier",
    "product-interest-studio",
    "lifecycle-radar",
    "service-recovery-desk",
    "event-attendance-cockpit",
    "content-conversation-engine",
    "manager-exception-review",
}
QUALITY_DIMENSIONS = {
    "brandExpression",
    "workbenchClarity",
    "informationDepth",
    "structuralDistinctness",
    "demoCoherence",
}
ARCHITECTURE_DIMENSIONS = {
    "businessAxis",
    "navigationModel",
    "homeNarrative",
    "detailArchitecture",
    "taskModel",
    "signatureInteraction",
}
CORE_SURFACES = {"home", "c360", "task-detail"}
OPTIONAL_SURFACES = {"appointment-detail"}
PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|lorem ipsum|待补|待确认后补)\b", re.I)


def meaningful(value: Any, minimum: int = 18) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def screenshot_exists(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    raw = Path(value)
    if raw.is_absolute():
        return False
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    if not candidate.is_file() or candidate.stat().st_size == 0:
        return False
    header = candidate.read_bytes()[:16]
    return (
        header.startswith(b"\x89PNG\r\n\x1a\n")
        or header.startswith(b"\xff\xd8\xff")
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    )


def validate(data: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    case_id = data.get("caseId")
    if not meaningful(case_id, 6):
        errors.append("caseId must be a concrete identifier")

    mode = data.get("portfolioMode")
    if mode not in {"first-case", "compare"}:
        errors.append("portfolioMode must be first-case or compare")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
        scope = {}
    included = scope.get("includedSurfaces")
    if not isinstance(included, list) or not CORE_SURFACES.issubset(set(included)):
        errors.append("scope.includedSurfaces must include home, c360, and task-detail")
        included = []
    out_of_scope = scope.get("outOfScopeSurfaces")
    if not isinstance(out_of_scope, list):
        errors.append("scope.outOfScopeSurfaces must be a list")
        out_of_scope = []
    out_of_scope_ids = {
        item.get("surface") for item in out_of_scope if isinstance(item, dict) and isinstance(item.get("surface"), str)
    }
    if "appointment-detail" not in included and "appointment-detail" not in out_of_scope_ids:
        errors.append("appointment-detail must be included or explicitly out of scope")
    for index, item in enumerate(out_of_scope):
        if not isinstance(item, dict) or item.get("surface") not in OPTIONAL_SURFACES or not meaningful(item.get("reason"), 20):
            errors.append(f"scope.outOfScopeSurfaces[{index}] must name an optional surface and a concrete reason")

    architecture = data.get("caseArchitecture")
    if not isinstance(architecture, dict):
        errors.append("caseArchitecture must be an object")
        architecture = {}
    primary = architecture.get("primaryArchetypeId")
    if primary not in ARCHETYPES:
        errors.append(f"caseArchitecture.primaryArchetypeId must be one of {sorted(ARCHETYPES)}")
    candidates = architecture.get("candidateArchetypeIds")
    if not isinstance(candidates, list) or len(candidates) < 3:
        errors.append("caseArchitecture.candidateArchetypeIds must include at least three archetypes")
    else:
        if len(set(candidates)) != len(candidates) or any(item not in ARCHETYPES for item in candidates):
            errors.append("caseArchitecture.candidateArchetypeIds must be unique valid archetype IDs")
        if primary not in candidates:
            errors.append("caseArchitecture.candidateArchetypeIds must include primaryArchetypeId")
    for key, minimum in (
        ("operationalTension", 28),
        ("selectionRationale", 36),
        ("antiConvergenceCommitment", 32),
    ):
        if not meaningful(architecture.get(key), minimum):
            errors.append(f"caseArchitecture.{key} must be concrete")
    rejected = architecture.get("rejectedArchetypes")
    if not isinstance(rejected, list) or len(rejected) < 2:
        errors.append("caseArchitecture.rejectedArchetypes must include at least two rejected candidates")
    else:
        rejected_ids: set[str] = set()
        for index, item in enumerate(rejected):
            if not isinstance(item, dict) or item.get("id") not in ARCHETYPES or not meaningful(item.get("reason"), 24):
                errors.append(f"caseArchitecture.rejectedArchetypes[{index}] must include a valid ID and concrete reason")
                continue
            rejected_ids.add(str(item["id"]))
        if primary in rejected_ids:
            errors.append("primaryArchetypeId cannot appear in rejectedArchetypes")
        if isinstance(candidates, list) and not rejected_ids.issubset(set(candidates)):
            errors.append("rejectedArchetypes must be drawn from candidateArchetypeIds")
    architecture_evidence = architecture.get("architectureEvidence")
    if not isinstance(architecture_evidence, dict):
        errors.append("caseArchitecture.architectureEvidence must be an object")
    else:
        for key in ARCHITECTURE_DIMENSIONS:
            if not meaningful(architecture_evidence.get(key), 12):
                errors.append(f"caseArchitecture.architectureEvidence.{key} must be concrete")

    rendered = data.get("renderedEvidence")
    if not isinstance(rendered, list):
        errors.append("renderedEvidence must be a list")
        rendered = []
    seen_surfaces: set[str] = set()
    for index, item in enumerate(rendered):
        if not isinstance(item, dict):
            errors.append(f"renderedEvidence[{index}] must be an object")
            continue
        surface = item.get("surface")
        if surface not in CORE_SURFACES | OPTIONAL_SURFACES:
            errors.append(f"renderedEvidence[{index}].surface is not supported")
        else:
            seen_surfaces.add(surface)
        if not screenshot_exists(root, item.get("screenshotPath")):
            errors.append(f"renderedEvidence[{index}].screenshotPath must be an existing non-empty relative file")
        if item.get("verdict") != "pass":
            errors.append(f"renderedEvidence[{index}].verdict must be pass before release")
        if not meaningful(item.get("observedEvidence"), 36):
            errors.append(f"renderedEvidence[{index}].observedEvidence must describe a visible result")
    required_surfaces = CORE_SURFACES | (OPTIONAL_SURFACES if "appointment-detail" in included else set())
    missing_surfaces = required_surfaces - seen_surfaces
    if missing_surfaces:
        errors.append(f"renderedEvidence missing required surfaces: {sorted(missing_surfaces)}")

    interactions = data.get("interactionEvidence")
    if not isinstance(interactions, list) or len(interactions) < 3:
        errors.append("interactionEvidence must include at least three observed state-changing interactions")
    else:
        for index, item in enumerate(interactions):
            if not isinstance(item, dict):
                errors.append(f"interactionEvidence[{index}] must be an object")
                continue
            for key, minimum in (("entry", 8), ("action", 18), ("expectedResult", 18), ("observedResult", 18)):
                if not meaningful(item.get(key), minimum):
                    errors.append(f"interactionEvidence[{index}].{key} must be concrete")
            if item.get("verdict") != "pass":
                errors.append(f"interactionEvidence[{index}].verdict must be pass before release")

    quality = data.get("humanQuality")
    if not isinstance(quality, dict):
        errors.append("humanQuality must be an object")
    else:
        for key in QUALITY_DIMENSIONS:
            item = quality.get(key)
            if not isinstance(item, dict):
                errors.append(f"humanQuality.{key} must be an object")
                continue
            score = item.get("score")
            if not isinstance(score, int) or not 4 <= score <= 5:
                errors.append(f"humanQuality.{key}.score must be an integer from 4 to 5")
            if not meaningful(item.get("evidence"), 32):
                errors.append(f"humanQuality.{key}.evidence must cite visible evidence")

    comparison = data.get("portfolioComparison")
    if not isinstance(comparison, dict):
        errors.append("portfolioComparison must be an object")
    else:
        references = comparison.get("referenceCases")
        if not isinstance(references, list):
            errors.append("portfolioComparison.referenceCases must be a list")
        elif mode == "first-case" and references:
            errors.append("first-case evaluations must not list reference cases")
        elif mode == "compare" and not references:
            errors.append("compare evaluations must list at least one reference case")
        if not meaningful(comparison.get("residualSimilarityRisk"), 28):
            errors.append("portfolioComparison.residualSimilarityRisk must be concrete")

    release = data.get("releaseDecision")
    if not isinstance(release, dict):
        errors.append("releaseDecision must be an object")
    else:
        if release.get("result") != "pass":
            errors.append("releaseDecision.result must be pass before delivery")
        if release.get("blockers") != []:
            errors.append("releaseDecision.blockers must be an empty list before delivery")
        if not meaningful(release.get("notes"), 24):
            errors.append("releaseDecision.notes must explain the release decision")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check screenshot-backed branded prototype case evidence.")
    parser.add_argument("evaluation_json", type=Path, help="Path to prototype-case-evaluation.json")
    args = parser.parse_args()
    try:
        data = json.loads(args.evaluation_json.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.evaluation_json}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("ERROR: evaluation root must be an object", file=sys.stderr)
        return 1
    errors = validate(data, args.evaluation_json.parent)
    if errors:
        print("Prototype case evaluation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OK: prototype case evaluation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
