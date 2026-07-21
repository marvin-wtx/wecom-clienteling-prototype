#!/usr/bin/env python3
"""Validate the staged V4.0 business, product, visual, and browser delivery."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = {
    "prototype HTML": Path("prototype/index.html"),
    "protected shell runtime": Path("prototype/shell-runtime.js"),
    "protected layout audit": Path("prototype/layout-audit.js"),
    "protected visual primitives": Path("prototype/workbench-visual-primitives.css"),
    "confirmed scope intake": Path("docs/scope-intake.json"),
    "business blueprint": Path("docs/business-blueprint.json"),
    "page-state contract": Path("docs/page-state-contract.json"),
    "confirmed design intake": Path("docs/design-intake.json"),
    "component usage manifest": Path("docs/component-usage.json"),
    "representative layout review": Path("docs/representative-layout-review.json"),
    "representative design acceptance": Path("docs/design-acceptance.json"),
    "visual token": Path("docs/visual-token.json"),
    "delivery review": Path("docs/prototype-delivery-review.json"),
}


def run_check(script_dir: Path, arguments: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(script_dir / arguments[0]), *arguments[1:]],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a complete WeCom Clienteling prototype delivery directory."
    )
    parser.add_argument("case_dir", type=Path, help="Directory containing prototype/ and docs/")
    args = parser.parse_args()

    case_dir = args.case_dir.resolve()
    if not case_dir.is_dir():
        print(f"ERROR: delivery directory not found: {case_dir}", file=sys.stderr)
        return 2

    missing = [label for label, relative in REQUIRED_FILES.items() if not (case_dir / relative).is_file()]
    if missing:
        print("Prototype delivery bundle failed:", file=sys.stderr)
        for label in missing:
            print(f"- missing required {label}: {REQUIRED_FILES[label]}", file=sys.stderr)
        return 1

    prototype = case_dir / REQUIRED_FILES["prototype HTML"]
    token = case_dir / REQUIRED_FILES["visual token"]
    review = case_dir / REQUIRED_FILES["delivery review"]
    source = prototype.read_text(encoding="utf-8")
    try:
        review_data = json.loads(review.read_text(encoding="utf-8"))
        page_contract = json.loads((case_dir / "docs" / "page-state-contract.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Prototype delivery bundle failed:\n- cannot read staged review inputs: {exc}", file=sys.stderr)
        return 1
    actual_hash = hashlib.sha256(prototype.read_bytes()).hexdigest()
    if review_data.get("buildHash") != actual_hash:
        print("Prototype delivery bundle failed:\n- delivery review buildHash does not match prototype/index.html", file=sys.stderr)
        return 1
    expected_pages = {item.get("id") for item in page_contract.get("pages", []) if isinstance(item, dict) and item.get("id")}
    checked_pages = set(review_data.get("selectedPagesChecked", []))
    if checked_pages != expected_pages:
        print("Prototype delivery bundle failed:\n- selectedPagesChecked must exactly match the page-state contract", file=sys.stderr)
        return 1
    incomplete_pattern = re.compile(r"replace(?:\s+with|-with)|\btodo\b|\btbd\b|待补|待确认后补", re.I)
    incomplete_artifacts = [
        label
        for label, relative in REQUIRED_FILES.items()
        if label != "prototype HTML" and incomplete_pattern.search((case_dir / relative).read_text(encoding="utf-8"))
    ]
    if incomplete_artifacts:
        print("Prototype delivery bundle failed:", file=sys.stderr)
        print(
            "- evidence artifacts still contain template placeholders: " + ", ".join(incomplete_artifacts),
            file=sys.stderr,
        )
        return 1
    starter_markers = (
        "renderKitPreview",
        "PROJECT CANVAS",
        "Start with the operating model.",
        "data-starter-demo=",
    )
    found_markers = [marker for marker in starter_markers if marker in source]
    if found_markers:
        print("Prototype delivery bundle failed:", file=sys.stderr)
        print(
            "- prototype still contains shell-kit or starter-demo content: "
            + ", ".join(found_markers),
            file=sys.stderr,
        )
        return 1

    script_dir = Path(__file__).resolve().parent
    checks = [
        ["check_scope_intake.py", str(case_dir)],
        ["check_business_blueprint.py", str(case_dir)],
        ["check_page_state_contract.py", str(case_dir)],
        ["check_blueprint_implementation.py", str(case_dir)],
        ["check_design_intake.py", str(case_dir)],
        ["check_design_foundation_implementation.py", str(case_dir)],
        ["check_component_usage.py", str(case_dir)],
        ["check_representative_layout_review.py", str(case_dir)],
        ["check_design_acceptance.py", str(case_dir)],
        ["check_visual_tokens.py", str(token)],
        ["check_delivery_review.py", str(review)],
        ["check_prototype_shell.py", str(prototype)],
        ["check_review_interaction_wiring.py", str(prototype)],
        ["check_token_implementation.py", str(token), str(prototype)],
        ["check_operating_language.py", str(token), str(prototype)],
    ]
    if "native-broadcast-frozen:start" in source or "新建群发" in source:
        checks.append(["check_native_wecom_broadcast.py", str(case_dir), "--required"])

    failures: list[str] = []
    for check in checks:
        passed, output = run_check(script_dir, check)
        if not passed:
            failures.append(f"{check[0]}\n{output}")

    if failures:
        print("Prototype delivery bundle failed:", file=sys.stderr)
        for failure in failures:
            print(f"\n{failure}", file=sys.stderr)
        return 1

    print("OK: complete prototype delivery bundle passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
