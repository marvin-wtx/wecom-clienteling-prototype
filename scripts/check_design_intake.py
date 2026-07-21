#!/usr/bin/env python3
"""Validate the V4.0 design intake and representative-screen plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")
REFERENCE_MODES = {"exact-brand", "user-selected-analogue", "brand-source-only", "generic-foundation"}
ADOPTABLE = {"color-roles", "typography-rhythm", "atmosphere", "geometry", "depth", "imagery-treatment", "responsive-principles"}
REJECTED = {"marketing-ia", "desktop-navigation", "source-content", "business-rules", "identity-assets"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} root must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    intake_path = case / "docs" / "design-intake.json"
    page_path = case / "docs" / "page-state-contract.json"
    foundation_path = Path(__file__).resolve().parents[1] / "assets" / "design-foundation" / "component-ux-contracts.json"
    missing = [path for path in (intake_path, page_path, foundation_path) if not path.is_file()]
    if missing:
        print("Design intake check failed:", *[f"- missing {path}" for path in missing], sep="\n", file=sys.stderr)
        return 1
    try:
        intake, pages, foundation = load(intake_path), load(page_path), load(foundation_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Design intake check failed:\n- cannot read input: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    if intake.get("skillVersion") != "4.0" or intake.get("confirmed") is not True:
        errors.append("design intake must be confirmed and remain V4.0")
    if intake.get("interaction") != "one-grouped-design-intake":
        errors.append("design intake must use one grouped interaction")
    playback = intake.get("intakePlayback") if isinstance(intake.get("intakePlayback"), dict) else {}
    if playback.get("shownToUserBeforeRepresentativeBuild") is not True:
        errors.append("design intake must be shown and confirmed before representative screens are built")
    if not isinstance(playback.get("assetAvailability"), str) or len(playback["assetAvailability"].strip()) < 12:
        errors.append("design intake must state available or missing brand assets")
    if playback.get("recommendedDirectionShown") is not True:
        errors.append("design intake must recommend a direction instead of asking the user to design the UI")
    if not isinstance(intake.get("functionalBuildHash"), str) or not SHA256.fullmatch(intake["functionalBuildHash"]):
        errors.append("functionalBuildHash must identify the accepted functional build")
    direction = intake.get("direction") if isinstance(intake.get("direction"), dict) else {}
    for key in ("tone", "density", "imageryLevel", "fidelityTarget"):
        if not isinstance(direction.get(key), str) or len(direction[key].strip()) < 3:
            errors.append(f"direction.{key} must be concrete")
    if not isinstance(direction.get("dislikedPatterns"), list) or len(direction["dislikedPatterns"]) < 1:
        errors.append("direction.dislikedPatterns must record at least one boundary")
    plan = intake.get("visualApplicationPlan") if isinstance(intake.get("visualApplicationPlan"), dict) else {}
    for key in ("typography", "colorRoles", "surfaceAndGeometry", "imagery", "density"):
        if not isinstance(plan.get(key), str) or len(plan[key].strip()) < 12:
            errors.append(f"visualApplicationPlan.{key} must be concrete")
    for key in ("expressiveZones", "protectedZones"):
        if not isinstance(plan.get(key), list) or not plan[key] or not all(isinstance(item, str) and item for item in plan[key]):
            errors.append(f"visualApplicationPlan.{key} must be a non-empty list")
    if not {"page-shell", "scroll-body", "sticky-action-clearance", "bottom-navigation", "native-wecom"}.issubset(set(plan.get("protectedZones", []))):
        errors.append("visualApplicationPlan must protect shell, scroll, sticky clearance, bottom navigation, and native WeCom")
    strategy = intake.get("referenceStrategy") if isinstance(intake.get("referenceStrategy"), dict) else {}
    awesome = strategy.get("awesomeDesignMd") if isinstance(strategy.get("awesomeDesignMd"), dict) else {}
    mode = awesome.get("referenceMode")
    if mode not in REFERENCE_MODES:
        errors.append("awesomeDesignMd.referenceMode is invalid")
    if awesome.get("indexUrl") != "https://github.com/VoltAgent/awesome-design-md":
        errors.append("Awesome DESIGN.md index attribution is required")
    adopted = set(awesome.get("adoptedAspects", []))
    rejected = set(awesome.get("rejectedAspects", []))
    if not adopted.issubset(ADOPTABLE):
        errors.append("Awesome DESIGN.md adoptedAspects contains a forbidden transfer")
    if not REJECTED.issubset(rejected):
        errors.append("Awesome DESIGN.md must explicitly reject marketing IA, content, rules, navigation, and identity assets")
    if awesome.get("used") is True:
        if mode not in {"exact-brand", "user-selected-analogue"}:
            errors.append("a used Awesome DESIGN.md reference must be exact-brand or user-selected-analogue")
        if not isinstance(awesome.get("designMdUrl"), str) or not awesome["designMdUrl"].startswith("https://"):
            errors.append("a used Awesome DESIGN.md reference needs its exact HTTPS URL")
        if not adopted:
            errors.append("a used Awesome DESIGN.md reference needs adoptedAspects")
        if mode == "user-selected-analogue" and awesome.get("userConfirmedAnalogue") is not True:
            errors.append("another brand may be used only after explicit user confirmation")
    elif mode not in {"brand-source-only", "generic-foundation"}:
        errors.append("unused Awesome DESIGN.md must fall back to brand sources or generic foundation")
    known_components = set((foundation.get("components") or {}).keys())
    selected_components = intake.get("foundationComponents") if isinstance(intake.get("foundationComponents"), list) else []
    if not selected_components or len(selected_components) != len(set(selected_components)):
        errors.append("foundationComponents must contain unique selected components")
    unknown = set(selected_components) - known_components
    if unknown:
        errors.append("unknown foundation components: " + ", ".join(sorted(unknown)))
    required_states = set(intake.get("requiredStates", []))
    vocabulary = set((foundation.get("global") or {}).get("requiredStateVocabulary", []))
    if not required_states or not required_states.issubset(vocabulary):
        errors.append("requiredStates must use the foundation state vocabulary")
    page_items = pages.get("pages") if isinstance(pages.get("pages"), list) else []
    page_ids = {item.get("id") for item in page_items if isinstance(item, dict)}
    representatives = intake.get("representativePages") if isinstance(intake.get("representativePages"), list) else []
    if not 2 <= len(representatives) <= 4 or len(representatives) != len(set(representatives)):
        errors.append("representativePages must contain two to four unique pages")
    if not set(representatives).issubset(page_ids):
        errors.append("representativePages must exist in the page-state contract")
    recipe_path = Path(__file__).resolve().parents[1] / "assets" / "design-foundation" / "page-composition-recipes.json"
    try:
        recipe_data = load(recipe_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"cannot read page composition recipes: {exc}")
        recipe_data = {}
    known_recipes = set((recipe_data.get("recipes") or {}).keys())
    selected_recipes = intake.get("compositionRecipes") if isinstance(intake.get("compositionRecipes"), list) else []
    if not selected_recipes or not set(selected_recipes).issubset(known_recipes):
        errors.append("compositionRecipes must select known executable page recipes")
    if intake.get("componentUsageManifest") != "docs/component-usage.json":
        errors.append("design intake must require docs/component-usage.json")
    if intake.get("layoutReview") != "docs/representative-layout-review.json":
        errors.append("design intake must require the representative Chrome layout review")
    representative_modules = {item.get("module") for item in page_items if item.get("id") in representatives}
    selected_modules = {item.get("module") for item in page_items}
    if "home" in selected_modules and "home" not in representative_modules:
        errors.append("selected Home needs a representative screen")
    if "clients" in selected_modules and "clients" not in representative_modules:
        errors.append("selected Clients needs a representative screen")
    journey_pages = set((pages.get("primaryJourney") or {}).get("pageOrder", []))
    if not journey_pages.intersection(representatives):
        errors.append("representative screens need at least one primary-Journey page")
    if not isinstance(intake.get("briefPlayback"), str) or len(intake["briefPlayback"].strip()) < 24:
        errors.append("briefPlayback must record the confirmed design direction and review sequence")
    if errors:
        print("Design intake check failed:", *[f"- {item}" for item in errors], sep="\n", file=sys.stderr)
        return 1
    print("OK: confirmed V4.0 design intake passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
