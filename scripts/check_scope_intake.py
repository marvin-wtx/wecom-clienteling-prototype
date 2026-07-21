#!/usr/bin/env python3
"""Validate the confirmed V4.0 scope intake before any prototype build."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MODES = {"framework-default", "module-scoped-demo", "source-grounded"}
CATEGORIES = ("home", "clients", "tasks", "appointments", "performance_tools")
RECOMMENDED = {
    "home": {"workbench", "today-list"},
    "clients": {"list-search-filter", "profile-basic", "membership", "transactions", "interactions"},
    "tasks": {"list", "detail", "prepare-outreach", "native-send-result"},
    "appointments": {"calendar-list", "detail", "create-confirm"},
    "performance_tools": {"personal-performance", "task-performance", "asset-library"},
}
PLACEHOLDER = re.compile(r"replace_with|\btodo\b|\btbd\b|待补|待确认", re.I)


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    path = args.case_dir.resolve() / "docs" / "scope-intake.json"
    if not path.is_file():
        print("Scope intake check failed:\n- missing docs/scope-intake.json", file=sys.stderr)
        return 1
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Scope intake check failed:\n- cannot read scope: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if data.get("skillVersion") != "4.0":
        errors.append('skillVersion must remain "4.0"')
    if data.get("mode") not in MODES:
        errors.append("mode must be framework-default, module-scoped-demo, or source-grounded")
    if data.get("confirmed") is not True:
        errors.append("scope intake must be confirmed before files are built")
    if not isinstance(data.get("brand"), str) or not data["brand"].strip():
        errors.append("brand is required")
    roles = data.get("roles")
    if not isinstance(roles, list) or not roles or not all(isinstance(item, str) and item for item in roles):
        errors.append("roles must contain at least one selected role")
    selections = data.get("selections")
    if not isinstance(selections, dict):
        errors.append("selections must be an object covering the five scope groups")
        selections = {}
    for category in CATEGORIES:
        values = selections.get(category)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            errors.append(f"selections.{category} must be a list")
    if not any(selections.get(category) for category in CATEGORIES):
        errors.append("at least one second-level page must be selected")
    extensions = data.get("extensions")
    if not isinstance(extensions, list):
        errors.append("extensions must be a list")
        extensions = []
    extension_ids: set[str] = set()
    for extension in extensions:
        if not isinstance(extension, dict):
            errors.append("every extension must be an object")
            continue
        extension_id = extension.get("id")
        pages = extension.get("secondLevelPages")
        if not isinstance(extension_id, str) or not extension_id.strip() or extension_id in extension_ids:
            errors.append("extensions need unique non-empty ids")
        else:
            extension_ids.add(extension_id)
        if extension.get("source") != "user-request":
            errors.append(f"extension {extension_id} must come from user-request")
        if not isinstance(pages, list) or not pages or not all(isinstance(item, str) and item.strip() for item in pages):
            errors.append(f"extension {extension_id} needs confirmed secondLevelPages")
    if data.get("mode") == "framework-default":
        for category, required in RECOMMENDED.items():
            if not required.issubset(set(selections.get(category, []))):
                errors.append(f"framework-default is missing recommended {category} pages")
    if data.get("mode") == "source-grounded" and not data.get("sourceMaterials"):
        errors.append("source-grounded mode requires sourceMaterials")
    authorization = data.get("demoDataAuthorization") if isinstance(data.get("demoDataAuthorization"), dict) else {}
    allowed_mock = authorization.get("allowedBrandLikeMock")
    if not isinstance(allowed_mock, list) or not all(isinstance(item, str) and item.strip() for item in allowed_mock):
        errors.append("demoDataAuthorization.allowedBrandLikeMock must be a list")
    required_forbidden = {"internal-membership-rule", "task-source-rule", "kpi-definition", "appointment-resource", "crm-writeback", "permission-model"}
    if not required_forbidden.issubset(set(authorization.get("forbiddenInferences", []))):
        errors.append("demo data policy must forbid unsupported brand operating rules")
    if not isinstance(authorization.get("visibleDisclosure"), str) or len(authorization["visibleDisclosure"].strip()) < 2:
        errors.append("demo data policy needs a visible disclosure label")
    depth = data.get("pageDepth") if isinstance(data.get("pageDepth"), dict) else {}
    if depth.get("primaryJourney") != "complete-loop":
        errors.append("pageDepth.primaryJourney must be complete-loop")
    if depth.get("otherSelectedPages") not in {"clickable-structure", "complete-loop"}:
        errors.append("otherSelectedPages must be clickable-structure or complete-loop")
    if not isinstance(data.get("primaryJourney"), str) or not data["primaryJourney"].strip():
        errors.append("one primaryJourney is required")
    playback = data.get("confirmationPlayback") if isinstance(data.get("confirmationPlayback"), dict) else {}
    if playback.get("shownToUser") is not True:
        errors.append("confirmationPlayback must show the exact selected second-level pages to the user")
    if playback.get("selectedSecondLevelPages") != selections:
        errors.append("confirmationPlayback.selectedSecondLevelPages must exactly match selections")
    if playback.get("primaryJourney") != data.get("primaryJourney"):
        errors.append("confirmationPlayback.primaryJourney must match the confirmed Journey")
    if playback.get("otherSelectedPagesDepth") != depth.get("otherSelectedPages"):
        errors.append("confirmationPlayback must state the confirmed depth for other pages")
    expected_count = sum(len(selections.get(category, [])) for category in CATEGORIES)
    expected_count += sum(len(item.get("secondLevelPages", [])) for item in extensions if isinstance(item, dict))
    if playback.get("estimatedPageCount") != expected_count:
        errors.append(f"confirmationPlayback.estimatedPageCount must equal the exact selected page count ({expected_count})")
    if depth.get("otherSelectedPages") == "complete-loop" and expected_count > 12 and playback.get("expansionConfirmed") is not True:
        errors.append("more than 12 complete-loop pages require explicit expansion confirmation after the exact page list is shown")
    if not isinstance(data.get("briefPlayback"), str) or len(data["briefPlayback"].strip()) < 24:
        errors.append("briefPlayback must record the confirmed product frame")
    if PLACEHOLDER.search(json.dumps(data, ensure_ascii=False)):
        errors.append("scope intake still contains placeholders")
    if errors:
        print("Scope intake check failed:", file=sys.stderr)
        print(*[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: confirmed V4.0 scope intake passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
