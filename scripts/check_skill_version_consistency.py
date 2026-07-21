#!/usr/bin/env python3
"""Require every user-facing skill title to match the canonical SKILL.md version."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TITLE_VERSION = re.compile(r"^#\s+.*?\bV(\d+(?:\.\d+)+)\b", re.MULTILINE)
REQUIRED = ("SKILL.md", "README.md", "VALIDATION-README.md")


def version_from_title(path: Path) -> str | None:
    match = TITLE_VERSION.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Check user-facing skill version titles.")
    parser.add_argument("skill_dir", type=Path, help="Skill directory containing SKILL.md")
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    errors: list[str] = []
    versions: dict[str, str] = {}
    for filename in REQUIRED:
        path = root / filename
        if not path.is_file():
            errors.append(f"missing required versioned file: {filename}")
            continue
        version = version_from_title(path)
        if version is None:
            errors.append(f"{filename} needs an H1 title containing Vx.y")
        else:
            versions[filename] = version
    canonical = versions.get("SKILL.md")
    if canonical:
        mismatched = [f"{filename}=V{version}" for filename, version in versions.items() if version != canonical]
        if mismatched:
            errors.append(f"titles must match SKILL.md V{canonical}: " + ", ".join(mismatched))
    if errors:
        print("Skill version consistency failed:", file=sys.stderr)
        print(*[f"- {error}" for error in errors], sep="\n", file=sys.stderr)
        return 1
    print(f"OK: all user-facing titles match V{canonical}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
