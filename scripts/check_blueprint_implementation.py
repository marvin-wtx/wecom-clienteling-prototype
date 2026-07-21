#!/usr/bin/env python3
"""Verify that confirmed V4.0 pages and common fields exist in the mobile build."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} root must be an object")
    return data


def marker(source: str, name: str, value: str) -> bool:
    return bool(re.search(rf"\b{re.escape(name)}\s*=\s*['\"]{re.escape(value)}['\"]", source))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    prototype = case / "prototype" / "index.html"
    scope_path = case / "docs" / "scope-intake.json"
    contract_path = case / "docs" / "page-state-contract.json"
    module_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / "common-retail-module-contracts.json"
    paths = (prototype, scope_path, contract_path, module_path)
    if any(not path.is_file() for path in paths):
        print("Blueprint implementation check failed:", file=sys.stderr)
        print(*[f"- missing {path}" for path in paths if not path.is_file()], sep="\n", file=sys.stderr)
        return 1
    try:
        source = prototype.read_text(encoding="utf-8")
        scope, contract, modules = load(scope_path), load(contract_path), load(module_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Blueprint implementation check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if not marker(source, "data-demo-data", "true"):
        errors.append("mobile product must declare data-demo-data=true once")
    pages = contract.get("pages") if isinstance(contract.get("pages"), list) else []
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_id = str(page.get("id", ""))
        for name, value in (
            ("data-page-id", page_id),
            ("data-module", str(page.get("module", ""))),
            ("data-selection", str(page.get("selection", ""))),
            ("data-page-depth", str(page.get("depth", ""))),
        ):
            if value and not marker(source, name, value):
                errors.append(f"page {page_id} missing {name}={value}")
    selected = scope.get("selections") if isinstance(scope.get("selections"), dict) else {}
    known = modules.get("modules") if isinstance(modules.get("modules"), dict) else {}
    for category, selections in selected.items():
        for selection in selections:
            for field in known.get(category, {}).get(selection, []):
                if not marker(source, "data-common-field", field):
                    errors.append(f"selected common field is not implemented: {category}.{selection}.{field}")
    journey = contract.get("primaryJourney") if isinstance(contract.get("primaryJourney"), dict) else {}
    for page_id in journey.get("pageOrder", []):
        page = next((item for item in pages if item.get("id") == page_id), {})
        if page.get("depth") != "complete-loop":
            errors.append(f"primary Journey page is not complete-loop: {page_id}")
    if "native-broadcast" in journey.get("pageOrder", []):
        if not marker(source, "data-native-mount", "direct"):
            errors.append("native page must expose data-native-mount=direct")
        if not marker(source, "data-result-source", "runtime-receipt"):
            errors.append("send result must expose data-result-source=runtime-receipt")
    if errors:
        print("Blueprint implementation check failed:", file=sys.stderr)
        print(*[f"- {item}" for item in errors[:80]], sep="\n", file=sys.stderr)
        if len(errors) > 80:
            print(f"- ... {len(errors) - 80} additional errors", file=sys.stderr)
        return 1
    print("OK: confirmed blueprint is implemented in the mobile product")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
