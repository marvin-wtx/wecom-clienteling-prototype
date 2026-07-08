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
    "palette",
    "typography",
    "componentStyle",
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
REQUIRED_WORKBENCH_BALANCE = [
    "brandIntensity",
    "heroPolicy",
    "operationalPriority",
    "accentBudget",
    "moduleDifferentiation",
    "pageLayerOnly",
    "readabilityRules",
]

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


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
        for token in ("status bar", "capsule", "bottom tabbar", "native WeCom"):
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
