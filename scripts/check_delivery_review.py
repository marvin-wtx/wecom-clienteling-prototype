#!/usr/bin/env python3
"""Validate one concise, visible-browser acceptance record for V4.0."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLACEHOLDER_RE = re.compile(r"replace_with|todo|tbd|待补|待确认", re.I)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def meaningful(value: Any, minimum: int = 12) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def valid_screenshot(root: Path, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
        return False
    path = (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    if not path.is_file() or path.stat().st_size == 0:
        return False
    header = path.read_bytes()[:16]
    return header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(b"\xff\xd8\xff") or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")


def status_pass(item: Any) -> bool:
    return isinstance(item, dict) and item.get("status") == "pass"


def validate(data: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if data.get("skillVersion") != "4.0":
        errors.append('skillVersion must remain "4.0"')
    if data.get("browser") != "Google Chrome":
        errors.append("browser must record Google Chrome visible-browser acceptance")
    if not meaningful(data.get("testedUrl"), 8) or not meaningful(data.get("checkedAt"), 10):
        errors.append("testedUrl and checkedAt must be recorded")
    if not isinstance(data.get("buildHash"), str) or not SHA256_RE.fullmatch(data["buildHash"]):
        errors.append("buildHash must be the SHA-256 of the tested prototype HTML")
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    for key in ("mobileFirstViewportComplete", "tabbarTouchesBottom", "longPageScrolls", "journeyValuesPersist", "allVisibleInteractionsWork"):
        if checks.get(key) is not True:
            errors.append(f"checks.{key} must be true")
    for key in ("consoleErrors", "brokenImages"):
        if checks.get(key) != 0:
            errors.append(f"checks.{key} must be 0")
    if not meaningful(data.get("primaryJourneyId"), 4):
        errors.append("primaryJourneyId must identify the confirmed Journey")
    journey = data.get("journey") if isinstance(data.get("journey"), list) else []
    if len(journey) < 4 or not all(isinstance(item, str) and len(item.strip()) >= 2 for item in journey):
        errors.append("journey must record at least four observed steps")
    pages = data.get("selectedPagesChecked") if isinstance(data.get("selectedPagesChecked"), list) else []
    if not pages or len(pages) != len(set(pages)) or not all(isinstance(item, str) and item.strip() for item in pages):
        errors.append("selectedPagesChecked must list each checked selected page once")
    page_shots = data.get("pageScreenshots") if isinstance(data.get("pageScreenshots"), dict) else {}
    if set(page_shots) != set(pages):
        errors.append("pageScreenshots must map every selectedPagesChecked page id to its visible Chrome screenshot")
    else:
        for page_id, shot in page_shots.items():
            if not valid_screenshot(root, shot):
                errors.append(f"pageScreenshots.{page_id} must be an existing relative PNG, JPEG, or WebP screenshot")
    runtime_pages = data.get("runtimePages") if isinstance(data.get("runtimePages"), list) else []
    runtime_by_id = {item.get("pageId"): item for item in runtime_pages if isinstance(item, dict)}
    if set(runtime_by_id) != set(pages):
        errors.append("runtimePages must include one visible #app assertion for every selected page")
    else:
        for page_id in pages:
            item = runtime_by_id[page_id]
            if item.get("actualPageId") != page_id or item.get("visibleInApp") is not True or item.get("renderedMarkersInApp") is not True:
                errors.append(f"runtimePages.{page_id} must prove #app rendered the expected page and markers")
            if not meaningful(item.get("routeEntry"), 2):
                errors.append(f"runtimePages.{page_id}.routeEntry must name the navigation path used in Chrome")
            if not valid_screenshot(root, item.get("screenshot")):
                errors.append(f"runtimePages.{page_id}.screenshot must be an existing relative image")
    tested = data.get("testedControlsByPage") if isinstance(data.get("testedControlsByPage"), dict) else {}
    if set(tested) != set(pages):
        errors.append("testedControlsByPage must list controls tested for every selected page")
    else:
        for page_id, controls in tested.items():
            if not isinstance(controls, list) or not controls or not all(isinstance(item, str) and item.strip() for item in controls):
                errors.append(f"testedControlsByPage.{page_id} must contain at least one tested visible control")
    controls = data.get("controlAssertions") if isinstance(data.get("controlAssertions"), list) else []
    if not controls or not all(status_pass(item) for item in controls):
        errors.append("controlAssertions must record passing before/action/after checks for visible controls")
    for item in controls:
        if not isinstance(item, dict):
            continue
        if item.get("pageId") not in pages:
            errors.append("controlAssertions may only reference selected pages")
        if not meaningful(item.get("control"), 2) or not meaningful(item.get("action"), 4) or not meaningful(item.get("after"), 4):
            errors.append("each control assertion must name the control, action, and observable after-state")
        if item.get("before") == item.get("after"):
            errors.append(f"controlAssertions.{item.get('control')} appears inert because before and after match")
    identities = data.get("objectIdentityAssertions") if isinstance(data.get("objectIdentityAssertions"), list) else []
    if not identities or not all(status_pass(item) for item in identities):
        errors.append("objectIdentityAssertions must prove clicked IDs are rendered on detail/result pages")
    for item in identities:
        if not isinstance(item, dict):
            continue
        if item.get("clickedId") != item.get("renderedId"):
            errors.append("objectIdentityAssertions clickedId must match renderedId")
    provenance = data.get("provenanceSamples") if isinstance(data.get("provenanceSamples"), list) else []
    if len(provenance) < 3 or not all(status_pass(item) for item in provenance):
        errors.append("provenanceSamples must include at least three passing visible structure/value provenance checks")
    for item in provenance:
        if not isinstance(item, dict):
            continue
        if item.get("structureProvenance") == item.get("valueProvenance") == "common-structure":
            errors.append("provenanceSamples must separate common field structure from mock visible values")
    if data.get("inertControls") not in ([], None):
        errors.append("inertControls must be empty")
    if data.get("wrongRouteControls") not in ([], None):
        errors.append("wrongRouteControls must be empty")
    shots = data.get("screenshots") if isinstance(data.get("screenshots"), list) else []
    if shots and not all(valid_screenshot(root, item) for item in shots):
        errors.append("screenshots, when present, must contain existing relative image paths")
    if not meaningful(data.get("observation"), 24):
        errors.append("observation must briefly describe what was actually seen")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review_json", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.review_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read review: {exc}", file=sys.stderr)
        return 2
    errors = validate(data, args.review_json.parent) if isinstance(data, dict) else ["review root must be an object"]
    if errors:
        print("Browser acceptance checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: concise visible-browser acceptance record passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
