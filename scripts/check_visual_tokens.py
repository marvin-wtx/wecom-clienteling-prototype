#!/usr/bin/env python3
"""Validate brand visual token JSON for WeCom clienteling prototypes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "brand",
    "referenceSources",
    "evidenceIntegrity",
    "structureGeneration",
    "creativeDivergence",
    "palette",
    "typography",
    "componentStyle",
    "structuralDifferentiation",
    "implementationContract",
    "deliveryDiscipline",
    "workbenchBalance",
    "imageryRules",
    "layoutRhythm",
    "shellBoundary",
    "moduleAdaptation",
    "avoid",
    "assumptions",
]

REQUIRED_PALETTE = [
    "primary",
    "primaryStrong",
    "accent",
    "background",
    "surface",
    "surfaceSoft",
    "text",
    "muted",
    "line",
    "danger",
    "onPrimary",
]

REQUIRED_BRAND = ["name", "industry", "targetFidelity", "frontlineTerm"]
REQUIRED_SHELL_BOUNDARY = ["protectedShell", "adaptablePageLayer", "nativeReplicaTreatment"]
REQUIRED_MODULES = [
    "home",
    "customers",
    "c360",
    "tasks",
    "appointments",
    "content",
    "dashboard",
    "transfer",
    "extensions",
]

REQUIRED_TYPOGRAPHY_LEVELS = ["display", "h1", "h2", "num", "eyebrow"]
REQUIRED_TYPOGRAPHY_LEVEL_FIELDS = {
    "display": ["size", "weight", "transform", "useCases"],
    "h1": ["size", "weight", "useCases"],
    "h2": ["size", "weight", "useCases"],
    "num": ["size", "weight", "feature", "useCases"],
    "eyebrow": ["size", "weight", "tracking", "transform", "useCases"],
}
REQUIRED_COMPONENT_GEOMETRY = ["controlRadius", "cardRadius", "useClipPath", "clipCorner", "description"]
REQUIRED_ACCENT_RULE = ["useCases", "avoid", "description"]
REQUIRED_ANCHOR = ["primaryAnchor", "secondaryAnchor", "fullWidthSection", "numDisplay", "description"]
REQUIRED_STRUCTURAL_DIFFERENTIATION = [
    "navigationModel",
    "homeComposition",
    "customerArchitecture",
    "taskArchitecture",
    "appointmentArchitecture",
    "dashboardArchitecture",
    "signatureInteraction",
    "antiTemplateCheck",
]
REQUIRED_NAVIGATION_MODEL = [
    "topLevelItems",
    "orderRationale",
    "centerAction",
    "activeTreatment",
    "roleVariation",
]
REQUIRED_WORKBENCH_BALANCE = [
    "brandIntensity",
    "heroPolicy",
    "operationalPriority",
    "accentBudget",
    "moduleDifferentiation",
    "pageLayerOnly",
    "readabilityRules",
    "pageContracts",
]
REQUIRED_PAGE_CONTRACTS = ["home", "customers", "tasks", "appointments", "dashboard", "nativeWeCom"]
REQUIRED_DELIVERY_STAGES = [
    "evidence",
    "structure",
    "productLogic",
    "dataModel",
    "pageContracts",
    "prototype",
    "qa",
]
REQUIRED_QUALITY_SCORES = [
    "brandFit",
    "workbenchUsability",
    "businessCredibility",
    "structuralOriginality",
    "evidenceIntegrity",
    "demoReadiness",
]

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
EVIDENCE_STATUSES = {"user-confirmed", "official-public", "generic-default", "assumption"}
EVIDENCE_SOURCE_KINDS = {
    "user-artifact",
    "user-statement",
    "official-public",
    "design-reference",
    "generic-baseline",
    "inference",
}
INTERNAL_CATEGORIES = {"business", "terminology", "interaction"}
ARCHETYPE_IDS = {
    "priority-queue",
    "appointment-atelier",
    "product-interest-studio",
    "lifecycle-radar",
    "service-recovery-desk",
    "event-attendance-cockpit",
    "content-conversation-engine",
    "manager-exception-review",
}
VAGUE_SOURCE_RE = re.compile(
    r"\b(industry standard|common|public program|another prototype|comparison)\b",
    re.IGNORECASE,
)


def is_nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def rel_luminance(hex_color: str) -> float:
    def channel(v: int) -> float:
        x = v / 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    high = max(rel_luminance(a), rel_luminance(b))
    low = min(rel_luminance(a), rel_luminance(b))
    return (high + 0.05) / (low + 0.05)


def require_keys(data: dict[str, Any], keys: list[str], label: str, errors: list[str]) -> None:
    for key in keys:
        if key not in data:
            errors.append(f"missing {label} key: {key}")
        elif not is_nonempty(data[key]):
            errors.append(f"empty {label} key: {key}")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require_keys(data, REQUIRED_TOP_LEVEL, "top-level", errors)

    brand = data.get("brand", {})
    if isinstance(brand, dict):
        require_keys(brand, REQUIRED_BRAND, "brand", errors)
    else:
        errors.append("brand must be an object")

    sources = data.get("referenceSources", [])
    if not isinstance(sources, list) or not sources:
        errors.append("referenceSources must be a non-empty list")

    evidence = data.get("evidenceIntegrity")
    if not isinstance(evidence, dict):
        errors.append("evidenceIntegrity must be an object")
    else:
        claims = evidence.get("claims")
        if not isinstance(claims, list) or not claims:
            errors.append("evidenceIntegrity.claims must be a non-empty list")
        else:
            claim_ids: set[str] = set()
            for index, claim in enumerate(claims):
                label = f"evidenceIntegrity.claims[{index}]"
                if not isinstance(claim, dict):
                    errors.append(f"{label} must be an object")
                    continue
                require_keys(
                    claim,
                    ["id", "claim", "category", "status", "sourceKind", "sourceRef", "allowedInUI", "neutralFallback"],
                    label,
                    errors,
                )
                claim_id = str(claim.get("id", "")).strip()
                if claim_id in claim_ids:
                    errors.append(f"{label}.id must be unique")
                claim_ids.add(claim_id)
                status = claim.get("status")
                source_kind = claim.get("sourceKind")
                category = claim.get("category")
                source_ref = str(claim.get("sourceRef", ""))
                if status not in EVIDENCE_STATUSES:
                    errors.append(f"{label}.status must be one of {sorted(EVIDENCE_STATUSES)}")
                if source_kind not in EVIDENCE_SOURCE_KINDS:
                    errors.append(f"{label}.sourceKind must be one of {sorted(EVIDENCE_SOURCE_KINDS)}")
                if status == "user-confirmed" and source_kind not in {"user-artifact", "user-statement"}:
                    errors.append(f"{label}: user-confirmed requires user-artifact or user-statement sourceKind")
                if status == "assumption" and claim.get("allowedInUI") is not False:
                    errors.append(f"{label}: assumption claims must set allowedInUI to false")
                if category in INTERNAL_CATEGORIES and status == "official-public":
                    errors.append(f"{label}: official-public cannot prove internal {category} claims")
                if VAGUE_SOURCE_RE.search(source_ref) and status == "user-confirmed":
                    errors.append(f"{label}: vague research or comparison text cannot support user-confirmed status")

        for key in ("assumptionTerms", "disallowedCarryoverTerms", "sourcePriority"):
            value = evidence.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"evidenceIntegrity.{key} must be a non-empty list")

    palette = data.get("palette", {})
    if isinstance(palette, dict):
        require_keys(palette, REQUIRED_PALETTE, "palette", errors)
        for key in REQUIRED_PALETTE:
            value = palette.get(key)
            if isinstance(value, str) and not HEX_RE.match(value):
                errors.append(f"palette.{key} must be a six-digit hex color")
        if all(isinstance(palette.get(k), str) and HEX_RE.match(palette[k]) for k in ("text", "background")):
            if contrast_ratio(palette["text"], palette["background"]) < 4.5:
                errors.append("palette.text and palette.background contrast is below 4.5")
        if all(isinstance(palette.get(k), str) and HEX_RE.match(palette[k]) for k in ("text", "surface")):
            if contrast_ratio(palette["text"], palette["surface"]) < 4.5:
                errors.append("palette.text and palette.surface contrast is below 4.5")
        if all(isinstance(palette.get(k), str) and HEX_RE.match(palette[k]) for k in ("onPrimary", "primary")):
            if contrast_ratio(palette["onPrimary"], palette["primary"]) < 3:
                errors.append("palette.onPrimary and palette.primary contrast is below 3")
    else:
        errors.append("palette must be an object")

    shell = data.get("shellBoundary", {})
    if isinstance(shell, dict):
        require_keys(shell, REQUIRED_SHELL_BOUNDARY, "shellBoundary", errors)
        protected = " ".join(shell.get("protectedShell", [])) if isinstance(shell.get("protectedShell"), list) else ""
        for token in ("status bar", "capsule", "bottom navigation", "native WeCom"):
            if token not in protected:
                errors.append(f"shellBoundary.protectedShell should include {token}")
    else:
        errors.append("shellBoundary must be an object")

    modules = data.get("moduleAdaptation", {})
    if isinstance(modules, dict):
        require_keys(modules, REQUIRED_MODULES, "moduleAdaptation", errors)
    else:
        errors.append("moduleAdaptation must be an object")

    avoid = data.get("avoid", [])
    if not isinstance(avoid, list) or not avoid:
        errors.append("avoid must be a non-empty list")

    typography = data.get("typography", {})
    if isinstance(typography, dict):
        for level in REQUIRED_TYPOGRAPHY_LEVELS:
            if level not in typography:
                errors.append(f"typography.{level} is required (brand depth check)")
                continue
            level_data = typography[level]
            if not isinstance(level_data, dict):
                errors.append(f"typography.{level} must be an object (brand depth check)")
                continue
            for field in REQUIRED_TYPOGRAPHY_LEVEL_FIELDS.get(level, []):
                if field not in level_data or not is_nonempty(level_data[field]):
                    errors.append(f"typography.{level}.{field} is required (brand depth check)")
    else:
        errors.append("typography must be an object (brand depth check)")

    component_style = data.get("componentStyle", {})
    if isinstance(component_style, dict):
        geometry = component_style.get("geometry")
        if not isinstance(geometry, dict):
            errors.append("componentStyle.geometry is required (brand depth check)")
        else:
            for field in REQUIRED_COMPONENT_GEOMETRY:
                if field not in geometry or not is_nonempty(geometry[field]):
                    errors.append(f"componentStyle.geometry.{field} is required (brand depth check)")

        accent = component_style.get("accentRule")
        if not isinstance(accent, dict):
            errors.append("componentStyle.accentRule is required (brand depth check)")
        else:
            for field in REQUIRED_ACCENT_RULE:
                if field not in accent or not is_nonempty(accent[field]):
                    errors.append(f"componentStyle.accentRule.{field} is required (brand depth check)")
            if isinstance(accent.get("useCases"), list) and len(accent["useCases"]) < 2:
                errors.append("componentStyle.accentRule.useCases should include at least two concrete use cases")
            if isinstance(accent.get("avoid"), list) and len(accent["avoid"]) < 2:
                errors.append("componentStyle.accentRule.avoid should include at least two concrete avoid cases")

        anchor = component_style.get("anchor")
        if not isinstance(anchor, dict):
            errors.append("componentStyle.anchor is required (brand depth check)")
        else:
            for field in REQUIRED_ANCHOR:
                if field not in anchor or not is_nonempty(anchor[field]):
                    errors.append(f"componentStyle.anchor.{field} is required (brand depth check)")
    else:
        errors.append("componentStyle must be an object (brand depth check)")

    structural = data.get("structuralDifferentiation", {})
    if isinstance(structural, dict):
        require_keys(
            structural,
            REQUIRED_STRUCTURAL_DIFFERENTIATION,
            "structuralDifferentiation",
            errors,
        )
        navigation = structural.get("navigationModel")
        if not isinstance(navigation, dict):
            errors.append("structuralDifferentiation.navigationModel must be an object")
        else:
            require_keys(
                navigation,
                REQUIRED_NAVIGATION_MODEL,
                "structuralDifferentiation.navigationModel",
                errors,
            )
            top_level_items = navigation.get("topLevelItems")
            if not isinstance(top_level_items, list) or not 3 <= len(top_level_items) <= 5:
                errors.append(
                    "structuralDifferentiation.navigationModel.topLevelItems must contain 3-5 items"
                )
            elif len({str(item).strip().lower() for item in top_level_items}) != len(top_level_items):
                errors.append(
                    "structuralDifferentiation.navigationModel.topLevelItems must be unique"
                )

        anti_template = structural.get("antiTemplateCheck")
        if not isinstance(anti_template, list) or len(anti_template) < 3:
            errors.append(
                "structuralDifferentiation.antiTemplateCheck should include at least three concrete checks"
            )

        architecture_keys = [
            "homeComposition",
            "customerArchitecture",
            "taskArchitecture",
            "appointmentArchitecture",
            "dashboardArchitecture",
        ]
        architecture_values = [
            re.sub(r"\s+", " ", str(structural.get(key, "")).strip().lower())
            for key in architecture_keys
        ]
        if len({value for value in architecture_values if value}) < 4:
            errors.append(
                "structuralDifferentiation should define at least four distinct page architecture decisions"
            )
    else:
        errors.append("structuralDifferentiation must be an object")

    generation = data.get("structureGeneration")
    if not isinstance(generation, dict):
        errors.append("structureGeneration must be an object")
    else:
        require_keys(
            generation,
            [
                "layoutAuthority",
                "variationSeed",
                "businessAxis",
                "navigationLogic",
                "homeNarrative",
                "informationDensity",
                "moduleGrammars",
                "visualAnchor",
                "signatureInteraction",
            ],
            "structureGeneration",
            errors,
        )
        mode = generation.get("layoutAuthority")
        if mode not in {"reference-led", "evidence-derived", "open-generative"}:
            errors.append("structureGeneration.layoutAuthority is invalid")
        if mode == "reference-led" and not generation.get("authoritySources"):
            errors.append("reference-led structureGeneration requires authoritySources")
        if mode == "open-generative":
            candidates = generation.get("candidateDirections")
            rejected = generation.get("rejectedDirections")
            if not isinstance(candidates, list) or len(candidates) < 3:
                errors.append("open-generative structureGeneration requires at least three candidateDirections")
            if not isinstance(rejected, list) or len(rejected) < 2:
                errors.append("open-generative structureGeneration requires at least two rejectedDirections")
            if not is_nonempty(generation.get("selectedDirectionId")):
                errors.append("open-generative structureGeneration requires selectedDirectionId")
            if not is_nonempty(generation.get("selectionRationale")):
                errors.append("open-generative structureGeneration requires selectionRationale")

        if mode in {"open-generative", "evidence-derived"}:
            archetype = data.get("archetypeSelection")
            if not isinstance(archetype, dict):
                errors.append("open-generative/evidence-derived work requires archetypeSelection")
            else:
                primary = archetype.get("primaryArchetypeId")
                if primary not in ARCHETYPE_IDS:
                    errors.append(f"archetypeSelection.primaryArchetypeId must be one of {sorted(ARCHETYPE_IDS)}")
                candidates = archetype.get("candidateArchetypeIds")
                if not isinstance(candidates, list) or len(candidates) < 3:
                    errors.append("archetypeSelection.candidateArchetypeIds must include at least three candidates")
                else:
                    if len(set(candidates)) != len(candidates) or any(item not in ARCHETYPE_IDS for item in candidates):
                        errors.append("archetypeSelection.candidateArchetypeIds must be unique valid archetype IDs")
                    if primary not in candidates:
                        errors.append("archetypeSelection.candidateArchetypeIds must include primaryArchetypeId")
                for key, minimum in (
                    ("operationalTension", 28),
                    ("selectionRationale", 36),
                    ("antiConvergenceCommitment", 32),
                ):
                    value = archetype.get(key)
                    if not isinstance(value, str) or len(value.strip()) < minimum:
                        errors.append(f"archetypeSelection.{key} must be concrete")
                rejected = archetype.get("rejectedArchetypes")
                if not isinstance(rejected, list) or len(rejected) < 2:
                    errors.append("archetypeSelection.rejectedArchetypes must include at least two rejected candidates")
                else:
                    rejected_ids: set[str] = set()
                    for index, item in enumerate(rejected):
                        if not isinstance(item, dict) or item.get("id") not in ARCHETYPE_IDS:
                            errors.append(f"archetypeSelection.rejectedArchetypes[{index}].id must be valid")
                            continue
                        reason = item.get("reason")
                        if not isinstance(reason, str) or len(reason.strip()) < 24:
                            errors.append(f"archetypeSelection.rejectedArchetypes[{index}].reason must be concrete")
                        rejected_ids.add(str(item["id"]))
                    if primary in rejected_ids:
                        errors.append("archetypeSelection.primaryArchetypeId cannot be rejected")
                    if isinstance(candidates, list) and not rejected_ids.issubset(set(candidates)):
                        errors.append("archetypeSelection.rejectedArchetypes must come from candidateArchetypeIds")
                if primary == "priority-queue":
                    justification = archetype.get("priorityQueueJustification")
                    weak_reason = isinstance(justification, str) and re.search(
                        r"sparse|no evidence|no data|starter shell|default", justification, re.I
                    )
                    if not isinstance(justification, str) or len(justification.strip()) < 40 or weak_reason:
                        errors.append(
                            "priority-queue requires a positive priorityQueueJustification, not a sparse-brief or starter-shell fallback"
                        )

    contract = data.get("implementationContract")
    if not isinstance(contract, dict):
        errors.append("implementationContract must be an object")
    else:
        require_keys(
            contract,
            [
                "navigationId",
                "homeArchitectureId",
                "customerArchitectureId",
                "taskArchitectureId",
                "appointmentArchitectureId",
                "signatureInteractionId",
            ],
            "implementationContract",
            errors,
        )

    delivery = data.get("deliveryDiscipline")
    if not isinstance(delivery, dict):
        errors.append("deliveryDiscipline must be an object")
    else:
        require_keys(
            delivery,
            [
                "positioning",
                "recipeStages",
                "minimumQualityBar",
                "selfCritiquePrompts",
                "antiGenericFlags",
            ],
            "deliveryDiscipline",
            errors,
        )
        positioning = str(delivery.get("positioning", ""))
        if "WeCom Clienteling" not in positioning:
            errors.append("deliveryDiscipline.positioning must identify a WeCom Clienteling deliverable")
        stages = delivery.get("recipeStages")
        if not isinstance(stages, list):
            errors.append("deliveryDiscipline.recipeStages must be a list")
        else:
            missing_stages = [stage for stage in REQUIRED_DELIVERY_STAGES if stage not in stages]
            if missing_stages:
                errors.append(f"deliveryDiscipline.recipeStages missing: {missing_stages}")
        quality = delivery.get("minimumQualityBar")
        if not isinstance(quality, dict):
            errors.append("deliveryDiscipline.minimumQualityBar must be an object")
        else:
            for key in REQUIRED_QUALITY_SCORES:
                value = quality.get(key)
                if not isinstance(value, int) or value < 4:
                    errors.append(f"deliveryDiscipline.minimumQualityBar.{key} must be an integer >= 4")
        prompts = delivery.get("selfCritiquePrompts")
        if not isinstance(prompts, list) or len(prompts) < 5:
            errors.append("deliveryDiscipline.selfCritiquePrompts must include at least five prompts")
        flags = delivery.get("antiGenericFlags")
        if not isinstance(flags, list) or len(flags) < 6:
            errors.append("deliveryDiscipline.antiGenericFlags must include at least six failure modes")

    workbench = data.get("workbenchBalance", {})
    if isinstance(workbench, dict):
        require_keys(workbench, REQUIRED_WORKBENCH_BALANCE, "workbenchBalance", errors)
        intensity = workbench.get("brandIntensity")
        if isinstance(intensity, str) and intensity.strip().lower() not in {"restrained", "balanced", "expressive"}:
            errors.append("workbenchBalance.brandIntensity should be restrained, balanced, or expressive")
        for key in ("operationalPriority", "readabilityRules"):
            value = workbench.get(key)
            if not isinstance(value, list) or len(value) < 2:
                errors.append(f"workbenchBalance.{key} should include at least two concrete rules")
        page_contracts = workbench.get("pageContracts")
        if not isinstance(page_contracts, dict):
            errors.append("workbenchBalance.pageContracts must be an object (workbench balance check)")
        else:
            for page in REQUIRED_PAGE_CONTRACTS:
                value = page_contracts.get(page)
                if not isinstance(value, list) or len(value) < 2:
                    errors.append(f"workbenchBalance.pageContracts.{page} should include at least two implementation rules")
    else:
        errors.append("workbenchBalance must be an object (workbench balance check)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a brand visual token JSON file.")
    parser.add_argument("json_file", type=Path, help="Path to visual-token JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.json_file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("ERROR: visual token root must be an object", file=sys.stderr)
        return 1

    errors = validate(data)
    if errors:
        print("Visual token checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: visual token checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
