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
    if re.search(rf"\b{re.escape(name)}\s*=\s*['\"]{re.escape(value)}['\"]", source):
        return True
    dataset_name = ''.join(part[:1].upper() + part[1:] for part in name.removeprefix('data-').split('-'))
    dataset_name = dataset_name[:1].lower() + dataset_name[1:]
    return bool(re.search(rf"\.dataset\.{re.escape(dataset_name)}\s*=\s*['\"]{re.escape(value)}['\"]", source))


def common_field_marker(source: str, value: str) -> bool:
    return marker(source, "data-common-field", value) or bool(re.search(rf"\bfield\(\s*['\"]{re.escape(value)}['\"]", source))


def visible_claim_marker(source: str, value: str) -> bool:
    return marker(source, "data-visible-claim", value) or value in source


def page_metadata_marker(source: str, page_id: str, name: str, value: str) -> bool:
    if name == "data-page-id":
        return rendered_page_container(source, page_id)
    if marker(source, name, value):
        return True
    if name in {"data-module", "data-selection", "data-page-depth"} and rendered_page_container(source, page_id):
        # Dynamic pageRoot/page functions may pass these values as variables; runtimePages evidence verifies actual DOM.
        return value in source
    return False


def strip_non_runtime_markup(source: str) -> str:
    source = re.sub(r"<template\b[\s\S]*?</template>", "", source, flags=re.I)
    source = re.sub(r"<!--([\s\S]*?)-->", "", source)
    return source


def marker_only_template_errors(source: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"<template\b[^>]*>([\s\S]*?)</template>", source, flags=re.I):
        body = match.group(1)
        if re.search(r"data-(?:page-id|common-field|ux-component|ux-state|visible-claim|content-provenance)", body):
            errors.append("marker-only templates are forbidden; runtime markers must render inside #app for the active route")
            break
    for match in re.finditer(r"<span\b([^>]*)>\s*</span>", source, flags=re.I):
        attrs = match.group(1)
        if re.search(r"data-(?:page-id|common-field|ux-component|ux-state)", attrs) and not re.search(r"class\s*=|aria-|role=", attrs):
            errors.append("zero-content marker-only spans are forbidden for page, field, component, or state validation")
            break
    return errors


def rendered_page_container(source: str, page_id: str) -> bool:
    if page_id == "native-broadcast":
        return marker(source, "data-native-mount", "direct") and (marker(source, "data-page-id", "native-broadcast") or "native-broadcast" in source)
    literal_container = re.search(rf"<(?:div|section|article|main)\b[^>]*\bdata-page-id\s*=\s*['\"]{re.escape(page_id)}['\"]", source)
    direct_page_root = re.search(rf"\bpageRoot\(\s*['\"]{re.escape(page_id)}['\"]", source)
    ternary_page_root = re.search(rf"\bpageRoot\(\s*[^,()]+\?\s*['\"]{re.escape(page_id)}['\"]\s*:", source) or re.search(rf"\bpageRoot\(\s*[^,()]+\?\s*[^,()]+:\s*['\"]{re.escape(page_id)}['\"]", source)
    page_root_call = direct_page_root or ternary_page_root
    array_mapped_page = re.search(rf"\[\s*['\"]{re.escape(page_id)}['\"]\s*,", source)
    return bool(literal_container or page_root_call or array_mapped_page)


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
        raw_source = prototype.read_text(encoding="utf-8")
        source = strip_non_runtime_markup(raw_source)
        scope, contract, modules = load(scope_path), load(contract_path), load(module_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Blueprint implementation check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = marker_only_template_errors(raw_source)
    if not marker(source, "data-demo-data", "true"):
        errors.append("mobile product must declare data-demo-data=true once")
    blueprint_path = case / "docs" / "business-blueprint.json"
    try:
        blueprint = load(blueprint_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"cannot read business blueprint for visible claim traceability: {exc}")
        blueprint = {}
    for claim in blueprint.get("visibleMockClaims", []):
        if not isinstance(claim, dict) or not claim.get("id"):
            continue
        claim_id = str(claim["id"])
        if not visible_claim_marker(source, claim_id):
            errors.append(f"visible mock claim is not traceable in the product: {claim_id}")
        if not marker(source, "data-content-provenance", str(claim.get("provenance", ""))):
            errors.append(f"visible mock claim lacks rendered provenance marker: {claim_id}")
    pages = contract.get("pages") if isinstance(contract.get("pages"), list) else []
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_id = str(page.get("id", ""))
        if page_id and not rendered_page_container(source, page_id):
            errors.append(f"page {page_id} must be implemented on a rendered page container, not only an inventory marker")
        for name, value in (
            ("data-page-id", page_id),
            ("data-module", str(page.get("module", ""))),
            ("data-selection", str(page.get("selection", ""))),
            ("data-page-depth", str(page.get("depth", ""))),
        ):
            if value and not page_metadata_marker(source, page_id, name, value):
                errors.append(f"page {page_id} missing {name}={value}")
    selected = scope.get("selections") if isinstance(scope.get("selections"), dict) else {}
    known = modules.get("modules") if isinstance(modules.get("modules"), dict) else {}
    for category, selections in selected.items():
        for selection in selections:
            for field in known.get(category, {}).get(selection, []):
                if not common_field_marker(source, field):
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
