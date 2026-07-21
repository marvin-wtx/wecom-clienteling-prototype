#!/usr/bin/env python3
"""Reject an incomplete, generic-looking, or clone-shaped V4.0 project configuration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLACEHOLDER = re.compile(r"REPLACE_WITH|\bTODO\b|\bTBD\b|待补|待确认", re.I)
FORBIDDEN = re.compile(r"golden[- ]baseline|wecom-clienteling-v4-sanitized|mode\s*[:=]\s*['\"]?exact|FSN\s+WeCom|Generic Baseline", re.I)
BAD_PRODUCT_LANGUAGE = re.compile(r"最近回写结果|今日尚未回写|\bQA\b|\bimplementation\b|\bopen事项\b", re.I)
SPARSE_INTERNAL_FACTS = re.compile(
    r"门店|总部|\bCRM\b|消费(?:史|记录)?|购买(?:史|记录)?|生日|会员等级|客户等级|偏好|预约|私享|礼遇|店长|顾问今早|系统下发|待回执|排队任务|\bKPI\b|具体产品推荐",
    re.I,
)
SPARSE_UI_STRUCTURES = re.compile(
    r"class=[\"'][^\"']*(?:\bmetric-strip\b|\bmetric\b|\bsearch\b|\bfilter-btn\b)|总部任务|今日概览|运营故事",
    re.I,
)
SPARSE_STAGES = ["today", "select", "native-broadcast", "result"]


def text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    config_path = case / "docs" / "project-config.json"
    prototype_path = case / "prototype" / "index.html"
    errors: list[str] = []
    if not config_path.is_file():
        errors.append("missing docs/project-config.json")
    if not prototype_path.is_file():
        errors.append("missing prototype/index.html")
    if errors:
        print("Project configuration check failed:", *[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Project configuration check failed:\n- invalid JSON: {exc}", file=sys.stderr)
        return 1
    if config.get("skillVersion") != "4.0":
        errors.append('project config must declare "skillVersion": "4.0"')
    project = config.get("project") if isinstance(config.get("project"), dict) else {}
    loop = config.get("operatingLoop") if isinstance(config.get("operatingLoop"), dict) else {}
    for key in ("name", "brandTreatment", "briefMode"):
        if not text(project.get(key)):
            errors.append(f"project.{key} is required")
    for key in ("role", "trigger", "object", "decision", "action", "visibleResult"):
        if not text(loop.get(key)):
            errors.append(f"operatingLoop.{key} is required")
    brief_mode = text(project.get("briefMode"))
    if brief_mode not in {"sparse", "source-grounded"}:
        errors.append("project.briefMode must be sparse or source-grounded")
    source_facts = project.get("sourceBoundFacts") if isinstance(project.get("sourceBoundFacts"), list) else []
    if brief_mode == "sparse" and any(text(item) for item in source_facts):
        errors.append("sparse mode must not claim source-bound internal facts")
    if brief_mode == "source-grounded" and not any(text(item) for item in source_facts):
        errors.append("source-grounded mode requires at least one explicit source-bound fact")

    routes = config.get("routes") if isinstance(config.get("routes"), list) else []
    route_ids = {text(item.get("id")) for item in routes if isinstance(item, dict) and text(item.get("id"))}
    if len(route_ids) < 3:
        errors.append("at least three project-specific routes are required")
    if any(not text(item.get("purpose")) for item in routes if isinstance(item, dict)):
        errors.append("every route needs a concrete purpose")
    navigation = config.get("navigation") if isinstance(config.get("navigation"), list) else []
    nav_ids = [text(item.get("id")) for item in navigation if isinstance(item, dict)]
    nav_range = range(1, 3) if brief_mode == "sparse" else range(3, 6)
    if len(nav_ids) not in nav_range or len(set(nav_ids)) != len(nav_ids):
        errors.append("sparse navigation needs one or two unique routes; source-grounded navigation needs three to five")
    if any(route not in route_ids for route in nav_ids):
        errors.append("each navigation item must reference a declared route")
    journey = config.get("primaryJourney") if isinstance(config.get("primaryJourney"), list) else []
    if not 3 <= len(journey) <= 7:
        errors.append("primaryJourney needs three to seven connected steps")
    for step in journey:
        if not isinstance(step, dict) or text(step.get("route")) not in route_ids or not text(step.get("moment")) or not text(step.get("expectedResult")):
            errors.append("every primaryJourney step needs a declared route, moment, and expected result")
            break
    if brief_mode == "sparse":
        stages = [text(step.get("stage")) for step in journey if isinstance(step, dict)]
        if stages != SPARSE_STAGES:
            errors.append("sparse primaryJourney must be exactly today → select → native-broadcast → result")
        if any(text(item) for item in config.get("assumptions", []) if isinstance(item, str)):
            errors.append("sparse mode must not add operating assumptions")
    native = config.get("nativeBroadcast") if isinstance(config.get("nativeBroadcast"), dict) else {}
    if native.get("enabled") and any(not text(native.get(key)) for key in ("entryRoute", "draftSource", "completionResult")):
        errors.append("enabled nativeBroadcast needs entryRoute, draftSource, and completionResult")
    serialized = json.dumps(config, ensure_ascii=False)
    if PLACEHOLDER.search(serialized):
        errors.append("project configuration still contains template placeholders")
    if BAD_PRODUCT_LANGUAGE.search(serialized):
        errors.append("project configuration contains review or fake-CRM language")
    source = prototype_path.read_text(encoding="utf-8")
    if brief_mode == "sparse":
        if 'data-brief-mode="sparse"' not in source and "data-brief-mode='sparse'" not in source:
            errors.append("sparse prototype must expose data-brief-mode=sparse")
        if SPARSE_INTERNAL_FACTS.search(serialized) or SPARSE_INTERNAL_FACTS.search(source):
            errors.append("sparse prototype contains unsupported internal customer, store, CRM, or operating facts")
        if SPARSE_UI_STRUCTURES.search(source):
            errors.append("sparse first delivery must not include KPI, search, filter, or operating-story UI")
        if not native.get("enabled"):
            errors.append("sparse default journey must enable nativeBroadcast")
    if FORBIDDEN.search(source) or FORBIDDEN.search(serialized):
        errors.append("retired Golden Baseline or former-project marker detected")
    if any(marker in source for marker in ("renderKitPreview", "PROJECT CANVAS", "WeCom Clienteling Shell Kit", "Protected frame and page primitives")):
        errors.append("shell kit preview or review-stage copy remains in the delivered prototype")
    if text(project.get("name")) not in source:
        errors.append("prototype does not visibly bind the project name from its configuration")
    if text(loop.get("action")) not in source and text(loop.get("trigger")) not in source:
        errors.append("prototype does not visibly bind the configured operating loop")
    if native.get("enabled") and "native-broadcast-frozen:start" not in source:
        errors.append("enabled nativeBroadcast must include the frozen native group-send route")
    if errors:
        print("Project configuration check failed:", *[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: project configuration defines a non-cloned V4.0 operating prototype")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
