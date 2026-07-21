#!/usr/bin/env python3
"""Forward-test the V4.0 staged contracts with one positive and two negative cases."""

from __future__ import annotations

import copy
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
CHECKS = (
    "check_scope_intake.py",
    "check_business_blueprint.py",
    "check_page_state_contract.py",
    "check_blueprint_implementation.py",
    "check_design_intake.py",
    "check_design_foundation_implementation.py",
    "check_design_acceptance.py",
)


def read_template(name: str) -> dict:
    return json.loads((TEMPLATES / name).read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(check: str, case: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / check), str(case)],
        capture_output=True,
        text=True,
        check=False,
    )


def build_positive(case: Path) -> tuple[dict, dict, dict]:
    docs = case / "docs"
    prototype = case / "prototype"
    docs.mkdir(parents=True)
    prototype.mkdir(parents=True)
    scope = read_template("scope-intake-template.json")
    blueprint = read_template("business-blueprint-template.json")
    page_contract = read_template("page-state-contract-template.json")
    modules = read_template("common-retail-module-contracts.json")
    design_intake = read_template("design-intake-template.json")
    design_acceptance = read_template("design-acceptance-template.json")
    scope["brand"] = "测试品牌"
    scope["confirmed"] = True
    scope["extensions"] = [
        {
            "id": "campaigns",
            "label": "活动",
            "secondLevelPages": ["invitation-list", "invitation-detail"],
            "source": "user-request",
        }
    ]
    blueprint["brand"] = scope["brand"]
    blueprint["extensions"] = copy.deepcopy(scope["extensions"])
    page_contract["pages"].extend(
        [
            {
                "id": "campaign-invitations",
                "module": "extension:campaigns",
                "selection": "invitation-list",
                "depth": "clickable-structure",
                "purpose": "查看用户要求的活动邀约",
                "primaryAction": "open-invitation",
            },
            {
                "id": "campaign-invitation-detail",
                "module": "extension:campaigns",
                "selection": "invitation-detail",
                "depth": "clickable-structure",
                "purpose": "查看用户要求的活动邀约详情",
                "primaryAction": "return-to-invitations",
            },
        ]
    )
    write_json(docs / "scope-intake.json", scope)
    write_json(docs / "business-blueprint.json", blueprint)
    write_json(docs / "page-state-contract.json", page_contract)

    markers = ['<main data-demo-data="true">']
    for page in page_contract["pages"]:
        markers.append(
            '<section data-page-id="{id}" data-module="{module}" '
            'data-selection="{selection}" data-page-depth="{depth}"></section>'.format(**page)
        )
    for category, selections in scope["selections"].items():
        for selection in selections:
            for field in modules["modules"][category][selection]:
                markers.append(f'<span data-common-field="{field}"></span>')
    markers.extend(
        (
            '<style>:root{--ux-touch-min: 44px}.tap{min-height:var(--ux-touch-min)}</style>',
            '<div data-native-mount="direct"></div>',
            '<div data-result-source="runtime-receipt"></div>',
        )
    )
    for component in design_intake["foundationComponents"]:
        markers.append(f'<div class="tap" data-ux-component="{component}"></div>')
    for state in design_intake["requiredStates"]:
        markers.append(f'<div data-ux-state="{state}"></div>')
    markers.append("</main>")
    html_path = prototype / "index.html"
    html_path.write_text("\n".join(markers), encoding="utf-8")
    (prototype / "workbench-visual-primitives.css").write_text(
        ":root{--ux-touch-min:44px}.tap{min-height:var(--ux-touch-min)}",
        encoding="utf-8",
    )

    design_intake["confirmed"] = True
    design_intake["functionalBuildHash"] = hashlib.sha256(html_path.read_bytes()).hexdigest()
    write_json(docs / "design-intake.json", design_intake)
    screenshot_dir = docs / "qa"
    screenshot_dir.mkdir()
    png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    screens = []
    for page_id in design_intake["representativePages"]:
        relative = f"qa/{page_id}.png"
        (docs / relative).write_bytes(png)
        screens.append({"pageId": page_id, "screenshot": relative})
    design_acceptance.update(
        {
            "acceptedBuildHash": hashlib.sha256(html_path.read_bytes()).hexdigest(),
            "accepted": True,
            "acceptedBy": "user",
            "representativeScreens": screens,
            "criteria": {key: True for key in design_acceptance["criteria"]},
            "remainingPagesMayBeStyled": True,
            "observation": "用户在可见浏览器中确认代表页面的信息层级、组件状态和品牌方向，可以扩展到其余页面。",
        }
    )
    write_json(docs / "design-acceptance.json", design_acceptance)
    return scope, blueprint, page_contract


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="wecom-v4-contracts-") as raw:
        root = Path(raw)
        positive = root / "positive"
        _, blueprint, _ = build_positive(positive)
        for check in CHECKS:
            result = run(check, positive)
            if result.returncode:
                failures.append(f"positive case failed {check}: {(result.stdout + result.stderr).strip()}")

        unsupported = root / "unsupported-claim"
        build_positive(unsupported)
        invalid_blueprint = copy.deepcopy(blueprint)
        invalid_blueprint["unsupportedClaims"] = ["品牌使用某 CRM 自动回写"]
        write_json(unsupported / "docs" / "business-blueprint.json", invalid_blueprint)
        result = run("check_business_blueprint.py", unsupported)
        if result.returncode == 0 or "unsupportedClaims must be an empty list" not in result.stderr:
            failures.append("unsupported brand claim was not rejected")

        legacy = root / "legacy-brand-only-output"
        (legacy / "prototype").mkdir(parents=True)
        (legacy / "prototype" / "index.html").write_text("<main>brand-only build</main>", encoding="utf-8")
        result = run("check_scope_intake.py", legacy)
        if result.returncode == 0 or "missing docs/scope-intake.json" not in result.stderr:
            failures.append("legacy build without confirmed intake was not rejected")

        borrowed = root / "silent-brand-borrowing"
        build_positive(borrowed)
        borrowed_intake = json.loads((borrowed / "docs" / "design-intake.json").read_text(encoding="utf-8"))
        borrowed_intake["referenceStrategy"]["awesomeDesignMd"].update(
            {
                "used": True,
                "referenceMode": "user-selected-analogue",
                "designMdUrl": "https://getdesign.md/example/design-md",
                "userConfirmedAnalogue": False,
                "adoptedAspects": ["color-roles"],
            }
        )
        write_json(borrowed / "docs" / "design-intake.json", borrowed_intake)
        result = run("check_design_intake.py", borrowed)
        if result.returncode == 0 or "explicit user confirmation" not in result.stderr:
            failures.append("silent borrowing from another brand was not rejected")

        self_approved = root / "self-approved-design"
        build_positive(self_approved)
        self_acceptance = json.loads((self_approved / "docs" / "design-acceptance.json").read_text(encoding="utf-8"))
        self_acceptance["acceptedBy"] = "agent"
        write_json(self_approved / "docs" / "design-acceptance.json", self_acceptance)
        result = run("check_design_acceptance.py", self_approved)
        if result.returncode == 0 or "may not self-approve" not in result.stderr:
            failures.append("agent self-approval of representative screens was not rejected")

    if failures:
        print("Staged contract forward test failed:", file=sys.stderr)
        print(*[f"- {item}" for item in failures], sep="\n", file=sys.stderr)
        return 1
    print("OK: staged business/design contracts accept confirmed work and reject unsupported, legacy, borrowed, or self-approved builds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
