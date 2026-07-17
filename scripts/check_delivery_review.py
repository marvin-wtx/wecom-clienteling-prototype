#!/usr/bin/env python3
"""Validate prototype delivery review JSON for branded WeCom prototypes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_STAGES = [
    "evidence",
    "structure",
    "productLogic",
    "dataModel",
    "pageContracts",
    "prototype",
    "qa",
]

REQUIRED_SCORES = [
    "brandFit",
    "workbenchUsability",
    "businessCredibility",
    "structuralOriginality",
    "evidenceIntegrity",
    "demoReadiness",
]

REQUIRED_SELF_CRITIQUE = [
    "starterShellDifference",
    "priorCaseDifference",
    "brandClientelingModule",
    "thinPageRisk",
    "evidenceBackedTerms",
    "assumptionsKeptOut",
    "debrandedDistinctiveness",
]

REQUIRED_CREATIVE_REVIEW = [
    "operatingMetaphor",
    "transposedMechanisms",
    "highImpactLeversUsed",
    "whyThisIsNotJustSkin",
    "creativeRiskControl",
]

ANTI_GENERIC_FLAGS = [
    "starterNavigationCopied",
    "homeUsesDefaultOrder",
    "detailPagesAreThin",
    "styleOnlyDifferentiation",
    "unconfirmedInternalTermsVisible",
    "campaignHeroDisplacesWorkbench",
    "singleCardGrammarEverywhere",
    "debrandedPrototypeStillGeneric",
]

PLACEHOLDER_REJECTS = ("replace with", "todo", "tbd", "待补", "待确认后补")


def nonempty_text(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip()
    if len(text) < 12:
        return False
    return not any(marker in text.lower() for marker in PLACEHOLDER_REJECTS)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    positioning = data.get("deliveryPositioning")
    if not isinstance(positioning, str) or "WeCom Clienteling" not in positioning:
        errors.append("deliveryPositioning must identify the deliverable as a WeCom Clienteling prototype")

    stages = data.get("deliveryStages")
    if not isinstance(stages, dict):
        errors.append("deliveryStages must be an object")
    else:
        for stage in REQUIRED_STAGES:
            entry = stages.get(stage)
            if not isinstance(entry, dict):
                errors.append(f"deliveryStages.{stage} must be an object")
                continue
            if entry.get("status") != "complete":
                errors.append(f"deliveryStages.{stage}.status must be complete")
            if not nonempty_text(entry.get("notes")):
                errors.append(f"deliveryStages.{stage}.notes must explain the completed stage")

    scores = data.get("qualityScores")
    if not isinstance(scores, dict):
        errors.append("qualityScores must be an object")
    else:
        for key in REQUIRED_SCORES:
            value = scores.get(key)
            if not isinstance(value, int) or not 1 <= value <= 5:
                errors.append(f"qualityScores.{key} must be an integer from 1 to 5")
            elif value < 4:
                errors.append(f"qualityScores.{key} must be at least 4 for delivery")

    critique = data.get("selfCritique")
    if not isinstance(critique, dict):
        errors.append("selfCritique must be an object")
    else:
        for key in REQUIRED_SELF_CRITIQUE:
            if not nonempty_text(critique.get(key)):
                errors.append(f"selfCritique.{key} must contain a non-placeholder answer")

    creative = data.get("creativeDivergenceReview")
    if not isinstance(creative, dict):
        errors.append("creativeDivergenceReview must be an object")
    else:
        for key in REQUIRED_CREATIVE_REVIEW:
            value = creative.get(key)
            if key in {"transposedMechanisms", "highImpactLeversUsed"}:
                if not isinstance(value, list) or len(value) < 2:
                    errors.append(f"creativeDivergenceReview.{key} must include at least two items")
            elif not nonempty_text(value):
                errors.append(f"creativeDivergenceReview.{key} must contain a non-placeholder answer")
        levers = creative.get("highImpactLeversUsed")
        if isinstance(levers, list) and len(set(str(item) for item in levers)) < 4:
            errors.append("creativeDivergenceReview.highImpactLeversUsed must include at least four distinct levers")

    anti_generic = data.get("antiGenericReview")
    if not isinstance(anti_generic, dict):
        errors.append("antiGenericReview must be an object")
    else:
        for flag in ANTI_GENERIC_FLAGS:
            if anti_generic.get(flag) is not False:
                errors.append(f"antiGenericReview.{flag} must be false before delivery")

    automated = data.get("automatedChecks")
    if not isinstance(automated, list) or len(automated) < 6:
        errors.append("automatedChecks must list the completed automated checks")
    else:
        for required in (
            "check_visual_tokens.py",
            "check_prototype_block_layout.py",
            "check_prototype_case_evaluation.py",
            "check_delivery_review.py",
        ):
            if required not in automated:
                errors.append(f"automatedChecks must include {required}")

    rendered = data.get("renderedChecks")
    if not isinstance(rendered, list) or len(rendered) < 4:
        errors.append("renderedChecks must list key browser-inspected surfaces")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check prototype delivery review JSON.")
    parser.add_argument("review_json", type=Path, help="Path to prototype-delivery-review JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.review_json.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.review_json}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("ERROR: delivery review root must be an object", file=sys.stderr)
        return 1

    errors = validate(data)
    if errors:
        print("Delivery review checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: delivery review checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
