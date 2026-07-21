#!/usr/bin/env python3
"""Check that prototype UI is phrased as daily work, not implementation or QA."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


FORBIDDEN_UI_PHRASES = ("最近回写结果", "今日尚未回写", "回写结果", "系统 1v1", "最高优先·今日open", "open事项", "QA", "token rationale")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check frontline operating language.")
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
    language = token.get("operatingLanguage")
    checks = language.get("selfCheck") if isinstance(language, dict) else None
    if not isinstance(checks, list) or len(checks) < 3:
        errors.append("token needs three operatingLanguage.selfCheck entries")
    else:
        for entry in checks:
            if not isinstance(entry, dict) or not isinstance(entry.get("uiText"), str) or len(entry["uiText"].strip()) < 2 or any(not isinstance(entry.get(key), str) or len(entry[key].strip()) < 4 for key in ("workMoment", "decisionOrAction")):
                errors.append("each language self-check needs uiText, workMoment, and decisionOrAction")
                break
    rejected = language.get("rejectedPhrases") if isinstance(language, dict) else None
    if not isinstance(rejected, list) or len(rejected) < 2:
        errors.append("token needs at least two rejected implementation/QA phrases")
    found = [phrase for phrase in FORBIDDEN_UI_PHRASES if phrase in html]
    if found:
        errors.append("implementation/QA language leaked into product UI: " + ", ".join(found))
    if errors:
        print("Operating language checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: operating language checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
