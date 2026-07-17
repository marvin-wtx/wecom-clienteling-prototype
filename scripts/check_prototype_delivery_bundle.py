#!/usr/bin/env python3
"""Validate that a branded WeCom prototype is delivered as a complete evidence bundle."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = {
    "prototype HTML": Path("prototype/index.html"),
    "visual token": Path("docs/visual-token.json"),
    "delivery review": Path("docs/prototype-delivery-review.json"),
    "case evaluation": Path("docs/prototype-case-evaluation.json"),
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
    evaluation = case_dir / REQUIRED_FILES["case evaluation"]
    source = prototype.read_text(encoding="utf-8")
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
    skill_root = script_dir.parent
    starter_demo = skill_root / "assets/prototype-shell-demo/index.html"
    checks = [
        ["check_visual_tokens.py", str(token)],
        ["check_creative_divergence.py", str(token)],
        ["check_delivery_review.py", str(review)],
        ["check_prototype_shell.py", str(prototype)],
        ["check_workbench_implementation.py", str(prototype)],
        ["check_page_information.py", str(prototype)],
        ["check_token_implementation.py", str(token), str(prototype)],
        ["check_prototype_block_layout.py", str(token), str(prototype)],
        ["check_prototype_case_evaluation.py", str(evaluation)],
        [
            "check_structural_similarity.py",
            str(prototype),
            "--token",
            str(token),
            "--reference",
            str(starter_demo),
        ],
    ]

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
