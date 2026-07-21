#!/usr/bin/env python3
"""Reject prototypes whose operating model is only a speculative concept."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check daily-work grounding and implementation markers.")
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
    operating = token.get("operatingModel")
    if not isinstance(operating, dict):
        errors.append("missing V4.0 operatingModel; no grounded daily-work contract")
    else:
        jobs = operating.get("dailyJobs")
        if not isinstance(jobs, list) or len(jobs) < 1:
            errors.append("at least one daily job is required")
        else:
            for job in jobs:
                if not isinstance(job, dict):
                    errors.append("daily job must be an object")
                    continue
                missing = [key for key in ("trigger", "object", "nextAction", "outcome") if not isinstance(job.get(key), str) or len(job[key].strip()) < 8]
                if missing:
                    errors.append(f"daily job {job.get('id', '?')} lacks grounded fields: {', '.join(missing)}")
                job_id = job.get("id")
                if isinstance(job_id, str) and f'data-operating-job="{job_id}"' not in html and f"data-operating-job='{job_id}'" not in html:
                    errors.append(f"daily job {job_id} has no visible HTML marker")
        if operating.get("mode") == "evidence-qualified-specialization":
            refs = operating.get("specialization", {}).get("evidenceRefs", []) if isinstance(operating.get("specialization"), dict) else []
            if not isinstance(refs, list) or len(set(refs)) < 2:
                errors.append("specialised operating mode needs two qualifying evidence references")
    if 'data-home-primary="daily-work"' not in html and "data-home-primary='daily-work'" not in html:
        errors.append("home does not declare a daily-work first viewport")
    if 'data-operating-action=' not in html or 'data-operating-outcome=' not in html:
        errors.append("prototype must mark an executable action and its visible outcome")
    if errors:
        print("Operating grounding checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: operating grounding checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
