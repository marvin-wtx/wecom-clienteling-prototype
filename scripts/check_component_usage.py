#!/usr/bin/env python3
"""Verify executable UI-kit integrity and full-page component recipes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SHA256 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDER = re.compile(r"replace_with|todo|tbd|待补|待确认", re.I)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_class(source: str, name: str) -> bool:
    return bool(re.search(rf"(?:class\s*=\s*['\"][^'\"]*|className\s*=\s*['\"][^'\"]*)\b{re.escape(name)}\b", source))


def has_component(source: str, name: str) -> bool:
    return bool(re.search(rf"data-ux-component\s*=\s*['\"]{re.escape(name)}['\"]", source))


def meaningful(value: Any, minimum: int = 4) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum and not PLACEHOLDER.search(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    skill = Path(__file__).resolve().parents[1]
    docs = case / "docs"
    prototype = case / "prototype"
    paths = {
        "manifest": docs / "component-usage.json",
        "intake": docs / "design-intake.json",
        "pageContract": docs / "page-state-contract.json",
        "html": prototype / "index.html",
        "css": prototype / "workbench-visual-primitives.css",
        "runtime": prototype / "shell-runtime.js",
        "layoutAudit": prototype / "layout-audit.js",
        "contracts": skill / "assets" / "design-foundation" / "component-ux-contracts.json",
        "recipes": skill / "assets" / "design-foundation" / "page-composition-recipes.json",
    }
    missing = [f"{name}: {path}" for name, path in paths.items() if not path.is_file()]
    if missing:
        print("Component usage check failed:", *[f"- missing {item}" for item in missing], sep="\n", file=sys.stderr)
        return 1
    try:
        manifest = load(paths["manifest"])
        intake = load(paths["intake"])
        page_contract = load(paths["pageContract"])
        contracts = load(paths["contracts"])
        recipes = load(paths["recipes"])
        source = paths["html"].read_text(encoding="utf-8") + "\n" + paths["runtime"].read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Component usage check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if manifest.get("skillVersion") != "4.0":
        errors.append('skillVersion must remain "4.0"')
    build_hash = manifest.get("buildHash")
    if not isinstance(build_hash, str) or not SHA256.fullmatch(build_hash) or build_hash != digest(paths["html"]):
        errors.append("component usage buildHash must match prototype/index.html")
    kit = manifest.get("uiKit") if isinstance(manifest.get("uiKit"), dict) else {}
    expected_refs = {
        "css": "prototype/workbench-visual-primitives.css",
        "runtime": "prototype/shell-runtime.js",
        "layoutAudit": "prototype/layout-audit.js",
    }
    if any(kit.get(key) != value for key, value in expected_refs.items()) or kit.get("copiedUnchanged") is not True:
        errors.append("uiKit must reference the three protected runtime files and declare copiedUnchanged=true")
    source_map = {
        "css": skill / "assets" / "prototype-shell" / "workbench-visual-primitives.css",
        "runtime": skill / "assets" / "prototype-shell" / "shell-runtime.js",
        "layoutAudit": skill / "assets" / "prototype-shell" / "layout-audit.js",
    }
    for key, source_path in source_map.items():
        if digest(source_path) != digest(paths[key]):
            errors.append(f"protected UI-kit file differs from the skill source: {expected_refs[key]}")

    pages = manifest.get("pages") if isinstance(manifest.get("pages"), list) else []
    representative_ids = set(intake.get("representativePages", []))
    manifest_representatives = set(manifest.get("representativePageIds", []))
    if manifest_representatives != representative_ids:
        errors.append("representativePageIds must exactly match design-intake representativePages")
    contracted_ids = {item.get("id") for item in page_contract.get("pages", []) if isinstance(item, dict) and item.get("id")}
    page_ids = {item.get("pageId") for item in pages if isinstance(item, dict)}
    if page_ids != contracted_ids or len(pages) != len(contracted_ids):
        missing_pages = sorted(contracted_ids - page_ids)
        extra_pages = sorted(page_ids - contracted_ids)
        errors.append(
            "component usage pages must cover every selected page from page-state-contract"
            + (f"; missing: {', '.join(missing_pages)}" if missing_pages else "")
            + (f"; extra: {', '.join(extra_pages)}" if extra_pages else "")
        )
    known_components = contracts.get("components") if isinstance(contracts.get("components"), dict) else {}
    known_recipes = recipes.get("recipes") if isinstance(recipes.get("recipes"), dict) else {}
    for page in pages:
        if not isinstance(page, dict):
            errors.append("every component usage page must be an object")
            continue
        page_id = page.get("pageId")
        recipe_id = page.get("recipe")
        recipe = known_recipes.get(recipe_id)
        if not isinstance(recipe, dict):
            errors.append(f"{page_id} uses an unknown composition recipe")
            continue
        if page.get("protectedStructureChanged") is not False:
            errors.append(f"{page_id} must keep protectedStructureChanged=false")
        for field in ("informationHero", "primaryAction", "compositionRationale"):
            if not meaningful(page.get(field), 4 if field != "compositionRationale" else 24):
                errors.append(f"{page_id} must declare a meaningful {field}")
        states = page.get("stateCoverage")
        if not isinstance(states, list) or not states or not all(isinstance(item, str) and item for item in states):
            errors.append(f"{page_id} must declare stateCoverage")
        items = page.get("components") if isinstance(page.get("components"), list) else []
        used_ids = {item.get("id") for item in items if isinstance(item, dict)}
        required_ids = set(recipe.get("requiredComponents", []))
        if not required_ids.issubset(used_ids):
            errors.append(f"{page_id} is missing recipe components: {', '.join(sorted(required_ids - used_ids))}")
        for item in items:
            component_id = item.get("id") if isinstance(item, dict) else None
            selector = item.get("selector") if isinstance(item, dict) else None
            if component_id not in known_components or not isinstance(selector, str) or len(selector) < 3:
                errors.append(f"{page_id} contains an invalid component entry")
                continue
            if component_id and not has_component(source, component_id):
                errors.append(f"{page_id} component marker is not implemented: {component_id}")
            for class_name in known_components[component_id].get("requiredClasses", []):
                if not has_class(source, class_name):
                    errors.append(f"{page_id} component {component_id} is missing executable class {class_name}")
        overrides = page.get("brandOverrides")
        if not isinstance(overrides, list) or not all(isinstance(item, str) and item for item in overrides):
            errors.append(f"{page_id} must list explicit brandOverrides")

    if errors:
        print("Component usage check failed:", *[f"- {item}" for item in errors[:100]], sep="\n", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... {len(errors) - 100} additional errors", file=sys.stderr)
        return 1
    print("OK: every selected page declares an executable recipe and component mapping")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
