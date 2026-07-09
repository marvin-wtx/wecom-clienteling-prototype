#!/usr/bin/env python3
"""Validate that the visual token's structural differentiation promises are actually implemented in the HTML.

v2.4 Implementation Contract:
- `data-nav-model="<id>"` on the rendered bottom navigation (matches implementationContract.navigationId)
- `data-page-architecture="<id>"` on home, C360, task detail, and appointment detail roots
- `data-signature-interaction="<id>"` on the functional signature interaction

The visual token must carry the same IDs. Navigation labels in the token must match the implemented tab labels and order.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def collect_token_contracts(token: dict) -> dict:
    """Extract the IDs the token declares under implementationContract."""
    contract = token.get("implementationContract", {})
    if not isinstance(contract, dict):
        return {}
    return contract


def collect_navigation_labels(token: dict) -> list[str]:
    """Extract navigation labels from the token's structuralDifferentiation.navigationModel."""
    sd = token.get("structuralDifferentiation", {})
    nav = sd.get("navigationModel", {}) if isinstance(sd, dict) else {}
    items = nav.get("topLevelItems", []) if isinstance(nav, dict) else []
    return [str(x) for x in items] if isinstance(items, list) else []


def collect_html_evidence(source: str) -> dict:
    """Find every data-* marker the HTML actually uses."""
    markers = {
        "nav_model": set(),
        "page_architecture": set(),
        "signature_interaction": set(),
    }
    for m in re.finditer(r'data-nav-model=["\']([^"\']+)["\']', source):
        markers["nav_model"].add(m.group(1))
    for m in re.finditer(r'data-page-architecture=["\']([^"\']+)["\']', source):
        markers["page_architecture"].add(m.group(1))
    for m in re.finditer(r'data-signature-interaction=["\']([^"\']+)["\']', source):
        markers["signature_interaction"].add(m.group(1))
    mapping = re.search(r"const\s+pageArchitectureByTitle\s*=\s*\{(.*?)\};", source, re.DOTALL)
    if mapping:
        markers["page_architecture"].update(
            re.findall(r':\s*["\']([^"\']+)["\']', mapping.group(1))
        )
    return markers


def collect_html_navigation_labels(source: str) -> list[str]:
    """Find the rendered bottom navigation label order from the prototype.

    Targets the actual <footer class="tabbar"> or <nav class="wx-tabbar"> block, not the stage-controls.
    """
    # Match the actual tabbar block (not the stage-controls nav)
    m = re.search(r'<(?:footer|nav)\s+class="(?:tabbar|wx-tabbar|nav-bar)"[^>]*>(.*?)</(?:footer|nav)>', source, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    block = m.group(1)
    labels = re.findall(r'<span[^>]*class=["\']?(?:tab-label|tab-text|nav-label)["\']?[^>]*>([^<]+)</span>|<span[^>]*>([一-龥\w\s]+)</span>', block)
    flat = []
    for tup in labels:
        for s in tup:
            s = s.strip()
            if s and len(s) < 20:
                flat.append(s)
    return flat


def collect_errors(token_path: Path, html_path: Path) -> list[str]:
    errors: list[str] = []
    token = json.loads(token_path.read_text(encoding="utf-8"))
    source = html_path.read_text(encoding="utf-8")

    contract = collect_token_contracts(token)
    if not contract:
        errors.append("visual token has no implementationContract block; v2.4 requires it for every branded prototype")
        return errors

    html_markers = collect_html_evidence(source)

    nav_id = contract.get("navigationId")
    if not nav_id:
        errors.append("implementationContract.navigationId is missing")
    elif nav_id not in html_markers["nav_model"]:
        errors.append(
            f"navigationId '{nav_id}' is declared in the token but no `data-nav-model=\"{nav_id}\"` attribute appears on the rendered bottom navigation in the HTML"
        )

    page_arch_map = {
        "homeArchitectureId": "home",
        "customerArchitectureId": "customer",
        "taskArchitectureId": "task",
        "appointmentArchitectureId": "appointment",
    }
    declared_archs = {k: contract.get(k) for k in page_arch_map}
    for k, v in declared_archs.items():
        if not v:
            errors.append(f"implementationContract.{k} is missing")
            continue
        if v not in html_markers["page_architecture"]:
            errors.append(
                f"{k} '{v}' is declared in the token but no `data-page-architecture=\"{v}\"` attribute appears on the {page_arch_map[k]} page root in the HTML"
            )

    sig_id = contract.get("signatureInteractionId")
    if not sig_id:
        errors.append("implementationContract.signatureInteractionId is missing")
    elif sig_id not in html_markers["signature_interaction"]:
        errors.append(
            f"signatureInteractionId '{sig_id}' is declared in the token but no `data-signature-interaction=\"{sig_id}\"` attribute appears on the functional signature interaction in the HTML"
        )

    token_labels = collect_navigation_labels(token)
    if token_labels:
        html_labels = collect_html_navigation_labels(source)
        if html_labels and html_labels != token_labels:
            errors.append(
                f"navigation labels in the token {token_labels} do not match the rendered tab order {html_labels}"
            )

    evidence = token.get("evidenceIntegrity", {})
    if isinstance(evidence, dict):
        source_lower = source.lower()
        for key in ("assumptionTerms", "disallowedCarryoverTerms"):
            terms = evidence.get(key, [])
            if not isinstance(terms, list):
                continue
            for term in terms:
                normalized = str(term).strip().lower()
                if len(normalized) >= 3 and normalized in source_lower:
                    errors.append(f"{key} term appears in delivered HTML: {term!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that the visual token's structural differentiation promises are actually implemented in the HTML."
    )
    parser.add_argument("token", type=Path, help="Path to visual-token.json")
    parser.add_argument("html", type=Path, help="Path to prototype index.html")
    args = parser.parse_args()

    if not args.token.exists():
        print(f"ERROR: file not found: {args.token}", file=sys.stderr)
        return 2
    if not args.html.exists():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    errors = collect_errors(args.token, args.html)
    if errors:
        print("Token implementation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: token implementation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
