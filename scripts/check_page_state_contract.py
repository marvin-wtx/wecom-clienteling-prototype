#!/usr/bin/env python3
"""Validate selected pages, page depth, and the primary Journey state contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
    paths = [case / "docs" / name for name in ("scope-intake.json", "business-blueprint.json", "page-state-contract.json")]
    if any(not path.is_file() for path in paths):
        print("Page-state contract check failed:", file=sys.stderr)
        print(*[f"- missing {path.relative_to(case)}" for path in paths if not path.is_file()], sep="\n", file=sys.stderr)
        return 1
    try:
        scope, blueprint, contract = (load(path) for path in paths)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Page-state contract check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if contract.get("skillVersion") != "4.0" or contract.get("mode") != scope.get("mode"):
        errors.append("contract version and mode must match V4.0 scope")
    pages = contract.get("pages") if isinstance(contract.get("pages"), list) else []
    ids = [page.get("id") for page in pages if isinstance(page, dict)]
    if not ids or len(ids) != len(set(ids)):
        errors.append("pages need unique non-empty ids")
    selected_pairs = {
        (category, selection)
        for category, values in (scope.get("selections") or {}).items()
        for selection in values
    }
    for extension in scope.get("extensions", []):
        if isinstance(extension, dict):
            selected_pairs.update(
                (f"extension:{extension.get('id')}", page)
                for page in extension.get("secondLevelPages", [])
            )
    page_pairs: set[tuple[str, str]] = set()
    for page in pages:
        if not isinstance(page, dict):
            errors.append("every page must be an object")
            continue
        pair = (page.get("module"), page.get("selection"))
        page_pairs.add(pair)
        if pair not in selected_pairs:
            errors.append(f"page {page.get('id')} belongs to an unselected module/page")
        if page.get("depth") not in {"complete-loop", "clickable-structure"}:
            errors.append(f"page {page.get('id')} needs an approved depth")
        if not page.get("purpose") or not page.get("primaryAction"):
            errors.append(f"page {page.get('id')} needs purpose and primaryAction")
    missing_pairs = selected_pairs - page_pairs
    if missing_pairs:
        errors.append("selected pages missing from contract: " + ", ".join(f"{a}.{b}" for a, b in sorted(missing_pairs)))
    if blueprint.get("selectedModules") != scope.get("selections"):
        errors.append("blueprint selections no longer match scope")
    journey = contract.get("primaryJourney") if isinstance(contract.get("primaryJourney"), dict) else {}
    if journey.get("id") != scope.get("primaryJourney"):
        errors.append("primary Journey id must match scope")
    order = journey.get("pageOrder") if isinstance(journey.get("pageOrder"), list) else []
    if not order or any(page_id not in ids for page_id in order):
        errors.append("primary Journey pageOrder must reference declared pages")
    if any(next((page for page in pages if page.get("id") == page_id), {}).get("depth") != "complete-loop" for page_id in order):
        errors.append("every primary Journey page must be complete-loop")
    if "native-broadcast" in order:
        native = next((page for page in pages if page.get("id") == "native-broadcast"), {})
        result = next((page for page in pages if page.get("id") == "send-result"), {})
        if native.get("mount") != "direct":
            errors.append("native-broadcast must mount directly")
        if result.get("resultSource") != "runtime-receipt":
            errors.append("send-result must use runtime-receipt")
        required_result = {"status", "recipientCount", "messageSnapshot", "materialSnapshot", "sentAt"}
        if not required_result.issubset(set(journey.get("resultFields", []))):
            errors.append("native Journey resultFields are incomplete")
    console = contract.get("reviewConsole") if isinstance(contract.get("reviewConsole"), dict) else {}
    if console.get("insidePhone") is not False or console.get("allowedAfterMobileAcceptance") is not True:
        errors.append("review console must stay outside the phone and follow mobile acceptance")
    if errors:
        print("Page-state contract check failed:", file=sys.stderr)
        print(*[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: V4.0 page-state contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
