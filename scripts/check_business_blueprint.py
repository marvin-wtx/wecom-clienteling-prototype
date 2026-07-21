#!/usr/bin/env python3
"""Validate selected modules, common contracts, and provenance in the V4.0 blueprint."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_PROVENANCE = {"user-source", "common-structure", "mock-value", "public-brand", "runtime"}


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} root must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    scope_path = case / "docs" / "scope-intake.json"
    blueprint_path = case / "docs" / "business-blueprint.json"
    contract_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "common-retail-module-contracts.json"
    missing = [str(path.relative_to(case)) if path.is_relative_to(case) else str(path) for path in (scope_path, blueprint_path, contract_path) if not path.is_file()]
    if missing:
        print("Business blueprint check failed:", *[f"- missing {item}" for item in missing], sep="\n", file=sys.stderr)
        return 1
    try:
        scope, blueprint, contracts = load(scope_path), load(blueprint_path), load(contract_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Business blueprint check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if blueprint.get("skillVersion") != "4.0":
        errors.append('skillVersion must remain "4.0"')
    if blueprint.get("mode") != scope.get("mode") or blueprint.get("brand") != scope.get("brand"):
        errors.append("blueprint mode and brand must match confirmed scope")
    if blueprint.get("selectedModules") != scope.get("selections"):
        errors.append("selectedModules must exactly match confirmed second-level selections")
    if blueprint.get("extensions") != scope.get("extensions"):
        errors.append("blueprint extensions must exactly match confirmed user-request extensions")
    known = contracts.get("modules") if isinstance(contracts.get("modules"), dict) else {}
    for category, selections in (blueprint.get("selectedModules") or {}).items():
        if category not in known or not isinstance(selections, list):
            errors.append(f"unknown module category: {category}")
            continue
        invalid = [item for item in selections if item not in known[category]]
        if invalid:
            errors.append(f"unknown {category} selections: {', '.join(invalid)}")
    roles = blueprint.get("roles") if isinstance(blueprint.get("roles"), list) else []
    if {item.get("id") for item in roles if isinstance(item, dict)} != set(scope.get("roles", [])):
        errors.append("blueprint roles must match scope roles")
    for collection in (roles, blueprint.get("objects", []), blueprint.get("brandSpecificClaims", [])):
        if not isinstance(collection, list):
            errors.append("roles, objects, and brandSpecificClaims must be lists")
            continue
        for item in collection:
            if not isinstance(item, dict) or item.get("provenance") not in ALLOWED_PROVENANCE:
                errors.append("every role, object, and brand claim needs allowed provenance")
                break
    for extension in blueprint.get("extensions", []):
        if not isinstance(extension, dict) or extension.get("source") != "user-request":
            errors.append("every extension must preserve user-request provenance")
            break
    unsupported = blueprint.get("unsupportedClaims")
    if not isinstance(unsupported, list) or unsupported:
        errors.append("unsupportedClaims must be an empty list")
    if scope.get("mode") != "source-grounded" and blueprint.get("brandSpecificClaims"):
        errors.append("demo modes must not contain brandSpecificClaims")
    journey = blueprint.get("primaryJourney") if isinstance(blueprint.get("primaryJourney"), dict) else {}
    if journey.get("id") != scope.get("primaryJourney"):
        errors.append("primaryJourney must match confirmed scope")
    selected_tasks = set((scope.get("selections") or {}).get("tasks", []))
    if "native-send-result" in selected_tasks:
        if journey.get("resultSource") != "runtime-receipt":
            errors.append("native send Journey resultSource must be runtime-receipt")
        stages = journey.get("stages") if isinstance(journey.get("stages"), list) else []
        if stages != ["task", "prepare", "native-broadcast", "result"]:
            errors.append("standard native Journey must be task → prepare → native-broadcast → result")
    if errors:
        print("Business blueprint check failed:", file=sys.stderr)
        print(*[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: V4.0 business blueprint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
