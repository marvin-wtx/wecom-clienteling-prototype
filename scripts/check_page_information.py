#!/usr/bin/env python3
"""Heuristic checks for metric semantics and detail-page information depth."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


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
        metric_count = len(
            re.findall(
                r"class=[\"'][^\"']*(?:stat(?!-)|metric-card|kpi(?:-card)?)\b",
                home,
                re.I,
            )
        )
        label_count = len(re.findall(r"data-metric-label(?:=[\"'][^\"']*[\"'])?", home, re.I))
        if has_metrics and (label_count == 0 or (metric_count and label_count < metric_count)):
            errors.append(
                "home metrics must pair every metric with a visible data-metric-label element"
            )

        if has(r"class=[\"'][^\"']*(stat|metric|kpi)", home):
            if has(
                r"\.(stat|metric|kpi)[^{]*(span|label)[^{]*\{[^}]*(display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0|font-size\s*:\s*0)",
                source,
            ):
                errors.append("home metric label CSS must not hide labels")

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
        if len(set(re.findall(r"data-info-region=[\"']([^\"']+)", c360, re.I))) < 4:
            errors.append("A-level C360 must mark at least four truthful data-info-region sections")

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
        if len(set(re.findall(r"data-info-region=[\"']([^\"']+)", task, re.I))) < 5:
            errors.append("A-level task detail must mark at least five truthful data-info-region sections")
        if has(r"根据客户状态生成", task) and not has(r"预览|编辑|有效期|来源|使用范围", task):
            errors.append("task guidance must show actionable preview/metadata, not generic generated-copy filler")

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
        if len(set(re.findall(r"data-info-region=[\"']([^\"']+)", appointment, re.I))) < 5:
            errors.append(
                "A-level appointment detail must mark at least five truthful data-info-region sections"
            )

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
