#!/usr/bin/env python3
"""Validate material architecture differences across branded prototype cases."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


HIGH_IMPACT_DIMENSIONS = {
    "businessAxis",
    "navigationModel",
    "homeNarrative",
    "detailArchitecture",
    "taskModel",
    "signatureInteraction",
}
PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|lorem ipsum|待补|待确认后补)\b", re.I)


def meaningful(value: Any, minimum: int = 18) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def normalized(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("evaluation root must be an object")
    return data


def load_portfolio(path: Path) -> list[dict[str, Any]]:
    portfolio = load(path)
    cases = portfolio.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("portfolio cases must be a non-empty list")
    root = path.parent.resolve()
    loaded: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(cases):
        if not isinstance(item, dict):
            raise ValueError(f"portfolio cases[{index}] must be an object")
        case_id = str(item.get("caseId", "")).strip()
        evaluation_path = item.get("evaluationPath")
        if not case_id or not isinstance(evaluation_path, str) or not evaluation_path.strip():
            raise ValueError(f"portfolio cases[{index}] requires caseId and evaluationPath")
        if case_id in seen:
            raise ValueError(f"portfolio caseId must be unique: {case_id}")
        seen.add(case_id)
        raw = Path(evaluation_path)
        if raw.is_absolute():
            raise ValueError(f"portfolio evaluationPath must be relative: {evaluation_path}")
        resolved = (root / raw).resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"portfolio evaluationPath escapes the portfolio root: {evaluation_path}") from exc
        evaluation = load(resolved)
        if evaluation.get("caseId") != case_id:
            raise ValueError(f"portfolio caseId does not match evaluation caseId: {case_id}")
        loaded.append(evaluation)
    return loaded


def architecture(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    block = data.get("caseArchitecture", {})
    if not isinstance(block, dict):
        return "", {}
    evidence = block.get("architectureEvidence", {})
    return str(block.get("primaryArchetypeId", "")), evidence if isinstance(evidence, dict) else {}


def validate(candidate: dict[str, Any], references: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if candidate.get("portfolioMode") != "compare":
        return ["candidate portfolioMode must be compare when portfolio references are supplied"]
    candidate_id = str(candidate.get("caseId", ""))
    candidate_archetype, candidate_evidence = architecture(candidate)
    comparison = candidate.get("portfolioComparison", {})
    entries = comparison.get("referenceCases", []) if isinstance(comparison, dict) else []
    if not isinstance(entries, list):
        return ["candidate portfolioComparison.referenceCases must be a list"]
    by_id = {
        str(item.get("referenceCaseId", "")): item
        for item in entries
        if isinstance(item, dict) and str(item.get("referenceCaseId", ""))
    }

    for reference in references:
        reference_id = str(reference.get("caseId", ""))
        if not reference_id:
            errors.append("reference evaluation has no caseId")
            continue
        if reference_id == candidate_id:
            errors.append("candidate cannot compare itself as a reference case")
            continue
        entry = by_id.get(reference_id)
        if not isinstance(entry, dict):
            errors.append(f"candidate is missing a portfolio comparison for reference case {reference_id}")
            continue
        reference_archetype, reference_evidence = architecture(reference)
        declared = entry.get("materialDifferences")
        if not isinstance(declared, list):
            errors.append(f"comparison for {reference_id} must include materialDifferences")
            continue
        required_count = 4 if candidate_archetype == reference_archetype else 3
        seen: set[str] = set()
        for index, difference in enumerate(declared):
            if not isinstance(difference, dict):
                errors.append(f"comparison {reference_id} difference[{index}] must be an object")
                continue
            dimension = difference.get("dimension")
            if dimension not in HIGH_IMPACT_DIMENSIONS:
                errors.append(f"comparison {reference_id} difference[{index}].dimension must be high-impact")
                continue
            seen.add(str(dimension))
            candidate_value = candidate_evidence.get(str(dimension))
            reference_value = reference_evidence.get(str(dimension))
            if not candidate_value or not reference_value:
                errors.append(f"comparison {reference_id} cannot verify {dimension} against architecture evidence")
                continue
            if normalized(candidate_value) == normalized(reference_value):
                errors.append(f"comparison {reference_id} declares {dimension} but both cases use the same decision")
            if normalized(difference.get("candidateDecision")) != normalized(candidate_value):
                errors.append(f"comparison {reference_id} candidateDecision must match candidate {dimension}")
            if normalized(difference.get("referenceDecision")) != normalized(reference_value):
                errors.append(f"comparison {reference_id} referenceDecision must match reference {dimension}")
            if not meaningful(difference.get("whyMaterial"), 28):
                errors.append(f"comparison {reference_id} difference[{index}].whyMaterial must explain operational impact")
        if len(seen) < required_count:
            errors.append(
                f"comparison {reference_id} needs at least {required_count} unique high-impact differences"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check portfolio-level prototype architecture diversity.")
    parser.add_argument("candidate", type=Path, help="Candidate prototype-case-evaluation JSON")
    parser.add_argument("--reference", type=Path, action="append", default=[], help="Prior case evaluation JSON")
    parser.add_argument("--portfolio", type=Path, help="Portfolio index JSON containing every released case")
    args = parser.parse_args()
    if not args.reference and not args.portfolio:
        parser.error("provide at least one --reference or a --portfolio index")
    try:
        candidate = load(args.candidate)
        references = [load(path) for path in args.reference]
        if args.portfolio:
            portfolio_cases = load_portfolio(args.portfolio)
            candidate_id = str(candidate.get("caseId", ""))
            if candidate_id not in {str(item.get("caseId", "")) for item in portfolio_cases}:
                raise ValueError("candidate caseId must appear in the portfolio index")
            references.extend(item for item in portfolio_cases if item.get("caseId") != candidate_id)
            deduplicated: dict[str, dict[str, Any]] = {}
            for item in references:
                case_id = str(item.get("caseId", ""))
                if case_id:
                    deduplicated[case_id] = item
            references = list(deduplicated.values())
    except FileNotFoundError as exc:
        print(f"ERROR: file not found: {exc.filename}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: invalid evaluation JSON: {exc}", file=sys.stderr)
        return 1
    errors = validate(candidate, references)
    if errors:
        print("Portfolio diversity checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"OK: portfolio diversity checks passed against {len(references)} reference case(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
