#!/usr/bin/env python3
"""Heuristic checks for metric semantics and detail-page information depth."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_C360_CAPABILITIES = {
    "identity",
    "relationship",
    "value",
    "recency",
    "operating-context",
    "customer-knowledge",
    "history",
    "actions",
}
REQUIRED_TASK_CAPABILITIES = {
    "definition",
    "progress",
    "audience",
    "guidance",
    "assets",
    "result-capture",
    "execution",
}
REQUIRED_APPOINTMENT_CAPABILITIES = {
    "schedule",
    "people-place",
    "service-resource",
    "customer-context",
    "preparation-communication",
    "outcome-follow-up",
    "actions-exceptions",
}


def function_segment(source: str, names: tuple[str, ...]) -> str:
    for name in names:
        match = re.search(rf"function\s+{re.escape(name)}\s*\(", source)
        if not match:
            continue
        start = match.start()
        next_match = re.search(r"\n\s*function\s+\w+\s*\(", source[match.end() :])
        if not next_match:
            return source[start:]
        return source[start : match.end() + next_match.start()]
    return ""


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE | re.DOTALL))


def count_groups(text: str, groups: list[tuple[str, str]]) -> int:
    return sum(1 for _label, pattern in groups if has(pattern, text))


def capability_names(text: str) -> set[str]:
    capabilities: set[str] = set()
    for value in re.findall(r"data-info-capability=[\"']([^\"']+)", text, re.IGNORECASE):
        capabilities.update(token.strip().lower() for token in value.split() if token.strip())
    return capabilities


def extract_css_vars(source: str) -> dict[str, str]:
    variables: dict[str, str] = {}
    for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;}{]+)", source):
        variables[name.lower()] = value.strip().lower()
    return variables


def resolve_css_value(value: str, variables: dict[str, str]) -> str:
    seen: set[str] = set()
    current = value.strip().lower()
    while True:
        match = re.fullmatch(r"var\((--[\w-]+)\)", current)
        if not match or match.group(1) in seen:
            return re.sub(r"\s+", "", current)
        seen.add(match.group(1))
        current = variables.get(match.group(1), current)


def css_rule(source: str, selector: str) -> str:
    matches = re.findall(rf"{selector}\s*\{{([^}}]+)\}}", source, re.IGNORECASE | re.DOTALL)
    for body in reversed(matches):
        if re.search(r"background|color", body, re.IGNORECASE):
            return body
    return matches[-1] if matches else ""


def nav_title_errors(source: str) -> list[str]:
    errors: list[str] = []
    for title in re.findall(
        r"appShell\s*\(\s*\{\s*title\s*:\s*[\"']([^\"']+)[\"']",
        source,
        re.IGNORECASE,
    ):
        if re.fullmatch(r"[\x00-\x7f]+", title) and len(title.strip()) > 8:
            errors.append(
                f'mini-program nav title "{title}" is too long; keep ASCII titles to 8 characters or fewer'
            )
    return errors


def expressive_region_count(text: str) -> int:
    count = 0
    for class_value in re.findall(
        r"<(?:section|div)[^>]*class=[\"']([^\"']+)[\"']",
        text,
        re.IGNORECASE,
    ):
        tokens = class_value.lower().split()
        if any(
            token == "hero"
            or token.endswith("-hero")
            or any(
                marker in token
                for marker in ("campaign", "editorial", "drop-block", "lookbook", "countdown")
            )
            for token in tokens
        ):
            count += 1
    return count


def collect_errors(source: str) -> list[str]:
    errors: list[str] = []
    home = function_segment(source, ("homePage", "renderHome", "homeView"))
    c360 = function_segment(source, ("c360Page", "customerDetailPage", "clientDetailPage"))
    task = function_segment(source, ("taskDetailPage", "taskDetail", "renderTaskDetail"))
    appointment = function_segment(
        source, ("appointmentDetailPage", "bookingDetailPage", "serviceDetailPage")
    )

    if home:
        has_metrics = has(r"metric|stat|kpi|指标|任务|预约|客户|销售|业绩", home)
        metric_count = len(re.findall(r"\bdata-home-kpi\b", home, re.IGNORECASE))
        label_count = len(re.findall(r"data-metric-label(?:=[\"'][^\"']*[\"'])?", home, re.I))
        if has_metrics and (metric_count < 1 or label_count < metric_count):
            errors.append(
                "home KPI rendering must use data-home-kpi containers with visible data-metric-label elements"
            )

        operational_count = len(re.findall(r"\bdata-home-operational\b", home, re.IGNORECASE))
        if operational_count < 2:
            errors.append("home first viewport must include at least two data-home-operational regions")

        first_operational = re.search(r"\bdata-home-operational\b", home, re.IGNORECASE)
        before_operational = home[: first_operational.start()] if first_operational else home
        expressive_regions = expressive_region_count(before_operational)
        if expressive_regions > 1:
            errors.append(
                "home may show at most one campaign/editorial brand region before the first operational region"
            )

    if c360:
        c360_groups = [
            ("identity/relationship", r"客户详情|客户身份|负责人|owner|门店|企微|注册|会员|生命周期"),
            ("value/recency", r"消费|交易|贡献|客单|最近购买|最近互动|recency|value"),
            ("operating context", r"当前待办|任务|预约|下一步|截止|机会|原因|优先"),
            ("customer knowledge", r"偏好|尺码|兴趣|心愿|wishlist|备注|标签|画像"),
            ("history", r"互动记录|历史|timeline|交易记录|服务记录|任务记录|预约记录"),
            ("actions", r"企微沟通|新建任务|新建预约|分享内容|添加备注|转移|邀请注册"),
        ]
        if count_groups(c360, c360_groups) < 4:
            errors.append("A-level C360 must expose at least four distinct information regions")
        c360_capabilities = capability_names(c360)
        required_core = {"identity", "operating-context", "actions"}
        if not required_core.issubset(c360_capabilities):
            errors.append(
                "A-level C360 must cover identity, operating-context, and actions capabilities"
            )
        if len(c360_capabilities & REQUIRED_C360_CAPABILITIES) < 6:
            errors.append("A-level C360 must cover at least six required information capabilities")
        unknown = c360_capabilities - REQUIRED_C360_CAPABILITIES
        if unknown:
            errors.append(
                "C360 uses unknown data-info-capability values: " + ", ".join(sorted(unknown))
            )

    if task:
        task_groups = [
            ("definition", r"任务目标|目标颗粒度|来源|类型|优先级|负责人|截止|成功指标"),
            ("progress", r"进度|已完成|待处理|跳过|失败|异常|\d+\s*/\s*\d+"),
            ("audience", r"目标客户|目标人群|名单|联系人状态|逐客户|客户状态"),
            ("guidance/assets", r"话术|素材|内容资产|预览|有效期|就绪|使用范围|编辑"),
            ("result capture", r"结果|回复|无响应|拒绝|跟进日期|回填|写回|跳过原因"),
            ("execution", r"进入企微|发送|发布|记录完成|创建预约|执行|不可执行|恢复"),
        ]
        if count_groups(task, task_groups) < 5:
            errors.append("A-level task detail must expose at least five distinct information regions")
        task_capabilities = capability_names(task)
        missing_task_capabilities = REQUIRED_TASK_CAPABILITIES - task_capabilities
        if missing_task_capabilities:
            errors.append(
                "A-level task detail is missing capabilities: "
                + ", ".join(sorted(missing_task_capabilities))
            )
        unknown = task_capabilities - REQUIRED_TASK_CAPABILITIES
        if unknown:
            errors.append(
                "task detail uses unknown data-info-capability values: "
                + ", ".join(sorted(unknown))
            )
        if has(r"根据客户状态生成", task) and not has(r"预览|编辑|有效期|来源|使用范围", task):
            errors.append("task guidance must show actionable preview/metadata, not generic generated-copy filler")
        hardcoded_counts = {
            int(value) for value in re.findall(r"(?<![\w$])(\d+)\s*位客户", task)
        }
        if len(hardcoded_counts) > 1:
            errors.append(
                "task detail contains conflicting hard-coded customer counts; derive counts from shared task data"
            )
        elif hardcoded_counts and has(r"targetIds|targets|target_ids", task):
            errors.append(
                "task detail hard-codes a customer count while also using shared targets; derive all displayed counts from the same data"
            )

    if appointment:
        appointment_groups = [
            ("schedule", r"日期|时间|开始|结束|时段|状态|确认"),
            ("people/place", r"客户|负责人|协同|门店|地点|顾问"),
            ("service/resource", r"服务|资源|试衣间|房间|产品|尺码|冲突"),
            ("customer context", r"偏好|目的|关联任务|来源活动|最近互动|联系限制"),
            ("preparation/communication", r"准备|清单|备注|确认方式|确认时间|企微"),
            ("outcome/follow-up", r"到店|完成|未到店|取消|结果|贡献|转化|下一步|跟进"),
            ("actions/exceptions", r"发送确认|改期|取消|联系客户|签到|回填|记录结果|冲突|无权限"),
        ]
        if count_groups(appointment, appointment_groups) < 5:
            errors.append(
                "A-level appointment detail must expose at least five distinct information regions"
            )
        appointment_capabilities = capability_names(appointment)
        mandatory = {
            "schedule",
            "people-place",
            "service-resource",
            "preparation-communication",
            "actions-exceptions",
        }
        missing_mandatory = mandatory - appointment_capabilities
        if missing_mandatory:
            errors.append(
                "A-level appointment detail is missing mandatory capabilities: "
                + ", ".join(sorted(missing_mandatory))
            )
        if not appointment_capabilities.intersection({"customer-context", "outcome-follow-up"}):
            errors.append(
                "A-level appointment detail must cover customer-context or outcome-follow-up"
            )
        unknown = appointment_capabilities - REQUIRED_APPOINTMENT_CAPABILITIES
        if unknown:
            errors.append(
                "appointment detail uses unknown data-info-capability values: "
                + ", ".join(sorted(unknown))
            )

    if has(
        r"BRAND\s*[·:]\s*EXPRESSIVE|WORKBENCH\s*[·:]\s*DENSE|ACCENT\s*[·:]\s*\d+\s*/\s*\d+|balance-badge",
        source,
    ):
        errors.append("product UI must not expose brand/workbench/accent QA or debug labels")

    variables = extract_css_vars(source)
    secondary = css_rule(source, r"\.secondary")
    background_match = re.search(r"background(?:-color)?\s*:\s*([^;]+)", secondary, re.I)
    color_match = re.search(r"(?<!-)color\s*:\s*([^;]+)", secondary, re.I)
    if background_match and color_match:
        background = resolve_css_value(background_match.group(1), variables)
        foreground = resolve_css_value(color_match.group(1), variables)
        if background == foreground:
            errors.append("secondary button foreground and background resolve to the same color")

    errors.extend(nav_title_errors(source))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check metric semantics and A-level detail-page information depth."
    )
    parser.add_argument("html", type=Path, help="Path to generated index.html")
    args = parser.parse_args()

    if not args.html.exists():
        print(f"ERROR: file not found: {args.html}", file=sys.stderr)
        return 2

    errors = collect_errors(args.html.read_text(encoding="utf-8"))
    if errors:
        print("Page information checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: page information checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
