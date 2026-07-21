#!/usr/bin/env python3
"""Verify that an operating-first token is visibly bound to the prototype."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def banned_literals(value: str) -> list[str]:
    """Extract display terms from a token note without treating its explanation as UI."""
    head = re.split(r"[（(]", value, maxsplit=1)[0].strip()
    candidates = re.split(r"\s*/\s*|\s*、\s*|\s*,\s*", head)
    return [candidate.strip() for candidate in candidates if len(candidate.strip()) > 1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("token_json", type=Path)
    parser.add_argument("prototype_html", type=Path)
    args = parser.parse_args()
    try:
        token = json.loads(args.token_json.read_text(encoding="utf-8"))
        html = args.prototype_html.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
        return 2
    errors: list[str] = []
    operating = token.get("operatingModel", {})
    for job in operating.get("dailyJobs", []):
        job_id = job.get("id")
        if isinstance(job_id, str) and f'data-operating-job="{job_id}"' not in html and f"data-operating-job='{job_id}'" not in html:
            errors.append(f"daily job '{job_id}' is not marked in HTML with data-operating-job")
    journey = token.get("experienceContract", {}).get("primaryJourney", {})
    action_id = journey.get("actionId")
    if isinstance(action_id, str) and f'data-operating-action="{action_id}"' not in html and f"data-operating-action='{action_id}'" not in html:
        errors.append("primary journey action is not marked with data-operating-action")
    if 'data-home-primary="daily-work"' not in html and "data-home-primary='daily-work'" not in html:
        errors.append("first workbench surface must be marked data-home-primary=\"daily-work\"")
    for term in token.get("evidenceIntegrity", {}).get("uiBannedTerms", []):
        if not isinstance(term, str) or "replace" in term.lower():
            continue
        for literal in banned_literals(term):
            if literal.casefold() in html.casefold():
                errors.append(f"UI contains banned unsupported term: {literal}")
    if not re.search(r"data-operating-outcome\s*=", html):
        errors.append("HTML must mark at least one visible result/state region with data-operating-outcome")
    if errors:
        print("Token implementation checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: operating token implementation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
