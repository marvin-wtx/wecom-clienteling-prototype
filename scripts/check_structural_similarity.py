#!/usr/bin/env python3
"""Compare branded prototypes with a brand-agnostic structural fingerprint."""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


def marker_values(source: str, marker: str) -> list[str]:
    pattern = rf'data-{re.escape(marker)}=["\']([^"\']+)["\']'
    return list(dict.fromkeys(match.group(1).strip() for match in re.finditer(pattern, source)))


def tabs(source: str) -> list[str]:
    match = re.search(r"const\s+tabs\s*=\s*\[(.*?)\];", source, re.DOTALL)
    if not match:
        return []
    return re.findall(r'\[\s*["\'][^"\']+["\']\s*,\s*["\']([^"\']+)', match.group(1))


def function_body(source: str, name: str) -> str:
    start = re.search(rf"function\s+{re.escape(name)}\s*\([^)]*\)\s*\{{", source)
    if not start:
        return ""
    next_function = re.search(r"\n\s*function\s+\w+\s*\(", source[start.end() :])
    end = start.end() + next_function.start() if next_function else len(source)
    return source[start.end() : end]


def dom_signature(source: str, function_name: str) -> list[str]:
    body = function_body(source, function_name)
    body = re.sub(r"\$\{.*?\}", "EXPR", body, flags=re.DOTALL)
    signature: list[str] = []
    for tag, attrs in re.findall(r"<([a-z][a-z0-9-]*)([^>]*)>", body, re.IGNORECASE):
        role = ""
        capability = re.search(r'data-info-capability=["\']([^"\']+)', attrs)
        grammar = re.search(r'data-module-grammar=["\']([^"\']+)', attrs)
        if capability:
            role += ":cap=" + re.sub(r"\s+", "+", capability.group(1).strip())
        if grammar:
            role += ":grammar=" + grammar.group(1).strip()
        signature.append(tag.lower() + role)
    return signature[:120]


def load_mode(token_path: Path | None) -> str:
    if not token_path or not token_path.exists():
        return ""
    token = json.loads(token_path.read_text(encoding="utf-8"))
    generation = token.get("structureGeneration", {})
    return generation.get("layoutAuthority", "") if isinstance(generation, dict) else ""


def fingerprint(html_path: Path) -> dict:
    source = html_path.read_text(encoding="utf-8")
    return {
        "tab_order": tabs(source),
        "business_axis": marker_values(source, "business-axis"),
        "home_architecture": marker_values(function_body(source, "homePage"), "page-architecture"),
        "module_grammars": marker_values(source, "module-grammar"),
        "page_architectures": marker_values(source, "page-architecture"),
        "signature_interactions": marker_values(source, "signature-interaction"),
        "home_dom": dom_signature(source, "homePage"),
        "detail_dom": {
            "customer": dom_signature(source, "c360Page"),
            "task": dom_signature(source, "taskDetailPage"),
            "appointment": dom_signature(source, "appointmentDetailPage"),
        },
    }


def sequence_ratio(left: object, right: object) -> float:
    return SequenceMatcher(None, json.dumps(left, sort_keys=True), json.dumps(right, sort_keys=True)).ratio()


def differences(left: dict, right: dict) -> tuple[list[str], dict[str, float]]:
    ratios = {key: sequence_ratio(left[key], right[key]) for key in left}
    changed = [key for key, ratio in ratios.items() if ratio < 0.72]
    return changed, ratios


def main() -> int:
    parser = argparse.ArgumentParser(description="Brand-agnostic structural similarity check.")
    parser.add_argument("target", type=Path)
    parser.add_argument("--token", type=Path)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--reference-token", type=Path)
    parser.add_argument("--min-differences", type=int, default=3)
    parser.add_argument("--show-fingerprint", action="store_true")
    args = parser.parse_args()

    for path in (args.target, args.reference):
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            return 2

    target_fp = fingerprint(args.target)
    if args.show_fingerprint:
        print(json.dumps(target_fp, ensure_ascii=False, indent=2))
        return 0

    if load_mode(args.token) == "reference-led":
        print("OK: similarity gate skipped for reference-led target; authoritative layout fidelity takes priority")
        return 0

    reference_fp = fingerprint(args.reference)
    changed, ratios = differences(target_fp, reference_fp)
    if len(changed) < args.min_differences:
        print("Structural similarity check failed:", file=sys.stderr)
        print(
            f"- only {len(changed)} structural dimensions differ; require at least {args.min_differences}",
            file=sys.stderr,
        )
        print(f"- changed: {changed}", file=sys.stderr)
        print(f"- similarity ratios: {json.dumps(ratios, ensure_ascii=False)}", file=sys.stderr)
        return 1

    print(f"OK: structural similarity check passed ({len(changed)} dimensions differ: {', '.join(changed)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
