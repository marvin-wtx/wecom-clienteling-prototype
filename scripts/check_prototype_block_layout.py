#!/usr/bin/env python3
"""Validate brand-agnostic structure DNA against a rendered prototype."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


LAYOUT_MODES = {"reference-led", "evidence-derived", "open-generative"}
NAV_TYPES = {
    "frequency-first",
    "lifecycle-first",
    "object-first",
    "role-first",
    "journey-first",
    "hub-and-action",
}
REQUIRED_GRAMMARS = {"home", "customers", "c360", "tasks", "appointments", "dashboard"}
SCORE_KEYS = {
    "operationalFit",
    "evidenceFit",
    "informationDepth",
    "interactionUsefulness",
    "similarityRisk",
}


def nonempty(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def marker_values(source: str, marker: str) -> set[str]:
    pattern = rf'data-{re.escape(marker)}=["\']([^"\']+)["\']'
    values = {match.group(1).strip() for match in re.finditer(pattern, source)}
    mapping_names = {
        "module-grammar": "moduleGrammarByTitle",
        "page-architecture": "pageArchitectureByTitle",
    }
    mapping_name = mapping_names.get(marker)
    if mapping_name:
        mapping = re.search(
            rf"const\s+{mapping_name}\s*=\s*\{{(.*?)\}};",
            source,
            re.DOTALL,
        )
        if mapping:
            values.update(re.findall(r':\s*["\']([^"\']+)["\']', mapping.group(1)))
    return values


def collect_errors(token_path: Path, html_path: Path) -> list[str]:
    token = json.loads(token_path.read_text(encoding="utf-8"))
    source = html_path.read_text(encoding="utf-8")
    errors: list[str] = []

    generation = token.get("structureGeneration")
    if not isinstance(generation, dict):
        return ["visual token must include structureGeneration"]

    mode = generation.get("layoutAuthority")
    if mode not in LAYOUT_MODES:
        errors.append(f"structureGeneration.layoutAuthority must be one of {sorted(LAYOUT_MODES)}")

    authority_sources = generation.get("authoritySources")
    if mode == "reference-led" and (not isinstance(authority_sources, list) or not authority_sources):
        errors.append("reference-led mode requires at least one authoritySources entry")

    variation_seed = generation.get("variationSeed")
    if not isinstance(variation_seed, str) or len(variation_seed.strip()) < 12:
        errors.append("structureGeneration.variationSeed must be a descriptive phrase")

    business_axis = generation.get("businessAxis")
    axis_id = business_axis.get("id") if isinstance(business_axis, dict) else None
    if not isinstance(business_axis, dict) or not nonempty(axis_id) or not nonempty(business_axis.get("rationale")):
        errors.append("structureGeneration.businessAxis requires id and rationale")

    navigation = generation.get("navigationLogic")
    if not isinstance(navigation, dict):
        errors.append("structureGeneration.navigationLogic must be an object")
    else:
        if navigation.get("type") not in NAV_TYPES:
            errors.append(f"structureGeneration.navigationLogic.type must be one of {sorted(NAV_TYPES)}")
        if not nonempty(navigation.get("rationale")):
            errors.append("structureGeneration.navigationLogic.rationale is required")

    home = generation.get("homeNarrative")
    if not isinstance(home, dict):
        errors.append("structureGeneration.homeNarrative must be an object")
    else:
        block_order = home.get("blockOrder")
        if not nonempty(home.get("type")) or not nonempty(home.get("rationale")):
            errors.append("structureGeneration.homeNarrative requires type and rationale")
        if not isinstance(block_order, list) or len(block_order) < 3:
            errors.append("structureGeneration.homeNarrative.blockOrder must contain at least three blocks")
        elif len({str(item).strip().lower() for item in block_order}) != len(block_order):
            errors.append("structureGeneration.homeNarrative.blockOrder entries must be unique")

    grammars = generation.get("moduleGrammars")
    if not isinstance(grammars, dict):
        errors.append("structureGeneration.moduleGrammars must be an object")
        grammars = {}
    else:
        missing = REQUIRED_GRAMMARS - set(grammars)
        if missing:
            errors.append(f"structureGeneration.moduleGrammars missing: {sorted(missing)}")
        values = [str(grammars.get(key, "")).strip().lower() for key in REQUIRED_GRAMMARS]
        if len({value for value in values if value}) < 4:
            errors.append("moduleGrammars must use at least four distinct grammars across required modules")

    signature = generation.get("signatureInteraction")
    signature_id = signature.get("id") if isinstance(signature, dict) else None
    if not isinstance(signature, dict) or not all(
        nonempty(signature.get(key)) for key in ("id", "stateChange", "rationale")
    ):
        errors.append("structureGeneration.signatureInteraction requires id, stateChange, and rationale")

    if mode == "open-generative":
        candidates = generation.get("candidateDirections")
        if not isinstance(candidates, list) or len(candidates) < 3:
            errors.append("open-generative mode requires at least three candidateDirections")
            candidates = []
        candidate_ids: set[str] = set()
        summaries: set[str] = set()
        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, dict):
                errors.append(f"candidateDirections[{index}] must be an object")
                continue
            candidate_id = str(candidate.get("id", "")).strip()
            summary = str(candidate.get("summary", "")).strip().lower()
            if not candidate_id or candidate_id in candidate_ids:
                errors.append(f"candidateDirections[{index}].id must be non-empty and unique")
            candidate_ids.add(candidate_id)
            if not summary or summary in summaries:
                errors.append(f"candidateDirections[{index}].summary must be non-empty and unique")
            summaries.add(summary)
            scores = candidate.get("scores")
            if not isinstance(scores, dict) or set(scores) != SCORE_KEYS:
                errors.append(f"candidateDirections[{index}].scores must contain exactly {sorted(SCORE_KEYS)}")
            elif any(not isinstance(value, int) or not 1 <= value <= 5 for value in scores.values()):
                errors.append(f"candidateDirections[{index}].scores values must be integers from 1 to 5")

        selected = generation.get("selectedDirectionId")
        if selected not in candidate_ids:
            errors.append("selectedDirectionId must match a candidateDirections id")
        if not nonempty(generation.get("selectionRationale")):
            errors.append("open-generative mode requires selectionRationale")
        rejected = generation.get("rejectedDirections")
        if not isinstance(rejected, list) or len(rejected) < 2:
            errors.append("open-generative mode requires at least two rejectedDirections")
        else:
            rejected_ids = {item.get("id") for item in rejected if isinstance(item, dict)}
            if selected in rejected_ids:
                errors.append("selectedDirectionId cannot appear in rejectedDirections")
            for index, item in enumerate(rejected):
                if not isinstance(item, dict) or not nonempty(item.get("id")) or not nonempty(item.get("reason")):
                    errors.append(f"rejectedDirections[{index}] requires id and reason")

    html_modes = marker_values(source, "layout-mode")
    if mode and mode not in html_modes:
        errors.append(f"HTML must implement data-layout-mode=\"{mode}\"")
    html_axes = marker_values(source, "business-axis")
    if axis_id and axis_id not in html_axes:
        errors.append(f"HTML must implement data-business-axis=\"{axis_id}\"")

    html_grammars = marker_values(source, "module-grammar")
    expected_grammars = {str(value) for value in grammars.values() if nonempty(value)}
    missing_grammars = expected_grammars - html_grammars
    if missing_grammars:
        errors.append(f"HTML is missing declared data-module-grammar values: {sorted(missing_grammars)}")

    html_signatures = marker_values(source, "signature-interaction")
    if signature_id and signature_id not in html_signatures:
        errors.append(f"HTML must implement data-signature-interaction=\"{signature_id}\"")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate brand-agnostic structure DNA and its rendered implementation."
    )
    parser.add_argument("token", type=Path, help="Path to visual-token.json")
    parser.add_argument("html", type=Path, help="Path to prototype index.html")
    args = parser.parse_args()

    for path in (args.token, args.html):
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2

    errors = collect_errors(args.token, args.html)
    if errors:
        print("Prototype block layout checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OK: brand-agnostic prototype block layout checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
