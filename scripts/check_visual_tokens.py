#!/usr/bin/env python3
"""Validate the lean V4.0 operating-first visual token."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
PLACEHOLDER_RE = re.compile(r"\b(replace with|todo|tbd|lorem ipsum|待补|待确认)\b", re.I)
REQUIRED_PALETTE = {"primary", "primaryStrong", "accent", "background", "surface", "surfaceSoft", "text", "muted", "line", "danger", "onPrimary"}
REQUIRED_JOB_FIELDS = {"id", "label", "trigger", "object", "nextAction", "outcome", "evidenceRef"}


def text(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER_RE.search(value)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(data.get("version")) != "4.0":
        errors.append("version must be 4.0")
    brief_mode = data.get("briefMode")
    if brief_mode not in {"framework-default", "module-scoped-demo", "source-grounded"}:
        errors.append("briefMode must match the confirmed V4.0 scope mode")
    if data.get("designIntakeRef") != "docs/design-intake.json":
        errors.append("visual token must reference docs/design-intake.json")
    foundation = data.get("componentFoundation") if isinstance(data.get("componentFoundation"), dict) else {}
    if foundation.get("contract") != "assets/design-foundation/component-ux-contracts.json" or foundation.get("visualReference") != "assets/design-foundation/component-reference.html":
        errors.append("visual token must use the V4.0 local component foundation")
    if not isinstance(foundation.get("protected"), list) or len(foundation["protected"]) < 5:
        errors.append("componentFoundation.protected must preserve UX structure, states, touch and transitions")
    if not isinstance(foundation.get("adaptable"), list) or len(foundation["adaptable"]) < 4:
        errors.append("componentFoundation.adaptable must define the brand-expression surface")
    brand = data.get("brand")
    if not isinstance(brand, dict) or not all(text(brand.get(key), 2) for key in ("name", "industry", "targetFidelity", "frontlineTerm")):
        errors.append("brand must include non-placeholder name, industry, targetFidelity, and frontlineTerm")
    sources = data.get("referenceSources")
    if not isinstance(sources, list) or not sources:
        errors.append("referenceSources must contain at least one source or generic-baseline record")

    integrity = data.get("evidenceIntegrity")
    if not isinstance(integrity, dict):
        errors.append("evidenceIntegrity must be an object")
        integrity = {}
    claims = integrity.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("evidenceIntegrity.claims must contain at least one claim")
        claim_ids: set[str] = set()
    else:
        claim_ids = set()
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"evidenceIntegrity.claims[{index}] must be an object")
                continue
            claim_id = claim.get("id")
            if not text(claim_id, 2):
                errors.append(f"evidenceIntegrity.claims[{index}].id must be concrete")
            else:
                claim_ids.add(claim_id)
            if claim.get("status") not in {"user-confirmed", "official-public", "generic-default", "assumption"}:
                errors.append(f"evidenceIntegrity.claims[{index}].status is invalid")
            if claim.get("sourceKind") not in {"user-artifact", "user-statement", "official-public", "design-reference", "generic-baseline", "inference"}:
                errors.append(f"evidenceIntegrity.claims[{index}].sourceKind is invalid")
            if not isinstance(claim.get("allowedInUI"), bool):
                errors.append(f"evidenceIntegrity.claims[{index}].allowedInUI must be boolean")
            if claim.get("status") in {"assumption"} and claim.get("allowedInUI") is True:
                errors.append(f"evidenceIntegrity.claims[{index}] assumptions cannot be allowed in UI")

    operating = data.get("operatingModel")
    if not isinstance(operating, dict):
        errors.append("operatingModel must be an object")
        operating = {}
    mode = operating.get("mode")
    if mode not in {"framework-default", "module-scoped-demo", "source-grounded"}:
        errors.append("operatingModel.mode must match a V4.0 scope mode")
    if not text(operating.get("role"), 3):
        errors.append("operatingModel.role must be concrete")
    jobs = operating.get("dailyJobs")
    if not isinstance(jobs, list) or not 1 <= len(jobs) <= 4:
        errors.append("operatingModel.dailyJobs must contain one to four confirmed jobs")
        jobs = []
    else:
        job_ids: set[str] = set()
        for index, job in enumerate(jobs):
            if not isinstance(job, dict) or not REQUIRED_JOB_FIELDS.issubset(job):
                errors.append(f"operatingModel.dailyJobs[{index}] misses a required field")
                continue
            for key in REQUIRED_JOB_FIELDS:
                if not text(job.get(key), 3):
                    errors.append(f"operatingModel.dailyJobs[{index}].{key} must be concrete")
            job_id = job.get("id")
            if isinstance(job_id, str):
                if job_id in job_ids:
                    errors.append("operatingModel.dailyJobs IDs must be unique")
                job_ids.add(job_id)
            if job.get("evidenceRef") not in claim_ids:
                errors.append(f"operatingModel.dailyJobs[{index}].evidenceRef must name an evidence claim")
    language = data.get("operatingLanguage")
    checks = language.get("selfCheck") if isinstance(language, dict) else None
    if not isinstance(checks, list) or len(checks) < 3:
        errors.append("operatingLanguage.selfCheck must contain three semantic checks")
    elif any(not isinstance(item, dict) or not text(item.get("uiText"), 2) or not all(text(item.get(key), 3) for key in ("workMoment", "decisionOrAction")) for item in checks):
        errors.append("each operating-language check needs uiText, workMoment, and decisionOrAction")
    rejected = language.get("rejectedPhrases") if isinstance(language, dict) else None
    if not isinstance(rejected, list) or len(rejected) < 2:
        errors.append("operatingLanguage.rejectedPhrases must name two rejected phrases")

    experience = data.get("experienceContract")
    if not isinstance(experience, dict) or not text(experience.get("firstViewport"), 12):
        errors.append("experienceContract.firstViewport must be concrete")
    else:
        journey = experience.get("primaryJourney")
        if not isinstance(journey, dict) or not all(text(journey.get(key), 3) for key in ("entryJobId", "actionId", "stateChange")):
            errors.append("experienceContract.primaryJourney must name entryJobId, actionId, and stateChange")

    palette = data.get("palette")
    if not isinstance(palette, dict) or not REQUIRED_PALETTE.issubset(palette):
        errors.append("palette misses required colors")
    elif any(not isinstance(palette[key], str) or not HEX_RE.fullmatch(palette[key]) for key in REQUIRED_PALETTE):
        errors.append("palette colors must use #RRGGBB")
    for key in ("visualDirection", "implementationContract"):
        if not isinstance(data.get(key), dict):
            errors.append(f"{key} must be an object")
    plan = data.get("workbenchVisualPlan")
    if not isinstance(plan, dict) or not all(text(plan.get(key), 12) for key in ("priorityTreatment", "queuePattern", "resultTreatment", "brandMaterial")):
        errors.append("workbenchVisualPlan must define priority, queue, result, and brand treatments")
    elif not isinstance(plan.get("avoid"), list) or len(plan["avoid"]) < 2:
        errors.append("workbenchVisualPlan.avoid must name two visual anti-patterns")
    if data.get("visualRecipe") not in {"precise", "boutique", "vivid"}:
        errors.append("visualRecipe must be precise, boutique, or vivid")
    if not isinstance(data.get("assumptions"), list):
        errors.append("assumptions must be a list")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check V4.0 visual token JSON.")
    parser.add_argument("token_json", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.token_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read token: {exc}", file=sys.stderr)
        return 2
    errors = validate(data) if isinstance(data, dict) else ["token root must be an object"]
    if errors:
        print("Visual token checks failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: V4.0 visual token checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
