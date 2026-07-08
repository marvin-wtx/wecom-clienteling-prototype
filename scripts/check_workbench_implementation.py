#!/usr/bin/env python3
"""Heuristic workbench-balance checks for branded WeCom clienteling prototypes."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def function_segment(source: str, function_name: str) -> str:
    match = re.search(rf"function\s+{re.escape(function_name)}\s*\(", source)
    if not match:
        return ""
    start = match.start()
    next_match = re.search(r"\n\s*function\s+\w+\s*\(", source[match.end() :])
    if not next_match:
        return source[start:]
    return source[start : match.end() + next_match.start()]


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE | re.DOTALL))


def count_groups(text: str, groups: list[tuple[str, str]]) -> int:
    return sum(1 for _label, pattern in groups if has(pattern, text))


def collect_errors(source: str) -> list[str]:
    errors: list[str] = []
    lower_source = source.lower()

    home = function_segment(source, "homePage") or source
    clients = function_segment(source, "clientsPage") or function_segment(source, "customerPage") or source
    tasks = (
        (function_segment(source, "tasksPage") or "")
        + (function_segment(source, "taskCard") or "")
        + (function_segment(source, "taskDetailPage") or "")
    ) or source
    appointments = (
        function_segment(source, "appointmentPage")
        or function_segment(source, "appointmentsPage")
        or function_segment(source, "appointmentRow")
        or source
    )

    home_workbench_groups = [
        ("priority clients", r"priority\s+clients|重点客户|优先客户|客户"),
        ("tasks", r"tasks?\b|任务|待办"),
        ("appointments", r"appointments?|bookings?|预约|到店|试衣|服务"),
        ("dashboard metric", r"kpi|dashboard|看板|达成|转化|销售|业绩"),
        ("campaign-to-task entry", r"data-route=[\"'](?:tasks|taskDetail|clients|appointment)|查看全部|进入任务|通知客户|发起邀约"),
    ]
    if count_groups(home, home_workbench_groups) < 2:
        errors.append(
            "home first-screen implementation should expose at least two workbench signals: clients, tasks, appointments, dashboard KPI, or campaign-to-task entry"
        )

    if has(r"hero|display|campaign|drop|limited|lookbook|editorial|full-bleed", home):
        if not has(r"priority\s+clients|tasks?\b|appointments?|bookings?|客户|任务|预约|到店|查看全部", home):
            errors.append("expressive home hero/campaign must not replace workbench summary and entries")

    if not has(r"placeholder=[\"'][^\"']*(搜索|search)|class=[\"'][^\"']*search|id=[\"'][^\"']*search", clients):
        errors.append("customer list must include a visible search input before or near customer rows")

    if not has(r"筛选|filter|filter-btn|scopePill|data-route=[\"']filter|全部[^<]{0,20}(待跟进|企微|客户)|tabs", clients):
        errors.append("customer list must include visible filter, segment, or scope controls")

    if not has(r"下一步|next action|待跟进|截止|due|优先|priority|原因|reason|状态|status", clients):
        errors.append("customer rows must expose next action, reason, due date, priority, or status signal")

    if not has(r"taskPill|tabs|全部任务|1v1|1vn|朋友圈|moments|native|群发|筛选|filter", tasks):
        errors.append("task list must include task type/status filters or tabs")

    task_groups = [
        ("source/type", r"source|总部|门店|系统|native|moments|1v1|1vn|群发|任务类型"),
        ("target grain", r"\d+\s*位|target|目标客户|客户|人群|名单"),
        ("due/progress", r"截止|due|progress|进度|已处理|今日|逾期"),
        ("primary action", r"进入企微|记录完成|发起|确认|通知|发送|data-route|primary"),
    ]
    if count_groups(tasks, task_groups) < 3:
        errors.append("task rows must show at least three of: source/type, target grain, due/progress, primary action")

    appointment_groups = [
        ("time", r"\b\d{1,2}:\d{2}\b|时间|time"),
        ("customer", r"客户|customer|王|陈|林|周|许|杜"),
        ("service/resource", r"服务|service|试衣|造型|到店|资源|resource|预约"),
        ("status", r"已确认|待确认|待回填|冲突|status|状态"),
        ("action", r"新建预约|确认|回填|follow|data-route|primary"),
    ]
    if count_groups(appointments, appointment_groups) < 4:
        errors.append("appointment page must expose time, customer, service/resource, status, and action clearly")

    if "nativebroadcast" in lower_source or "新建群发" in source or "群发" in source:
        if not has(r"recipient|收件人|客户数|frequency|频率|合规|发送|取消|返回|send", source):
            errors.append("native WeCom handoff must include recipient, frequency/compliance, send/cancel, and return-state cues")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check branded WeCom clienteling prototypes for workbench-balance implementation gaps."
    )
    parser.add_argument("html", type=Path, help="Path to generated index.html")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    source = args.html.read_text(encoding="utf-8")
    errors = collect_errors(source)
    if errors:
        print("Workbench implementation checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: workbench implementation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
