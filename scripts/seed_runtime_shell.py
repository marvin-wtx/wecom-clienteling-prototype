#!/usr/bin/env python3
"""Seed only the V4.0 protected shell after scope and page contracts pass."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "assets" / "prototype-shell"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path, help="new case directory")
    args = parser.parse_args()
    case_dir = args.case_dir.resolve()
    prototype = case_dir / "prototype"
    runtime_files = ("index.html", "shell-runtime.js", "layout-audit.js", "workbench-visual-primitives.css")
    targets = [prototype / name for name in runtime_files]
    if any(path.exists() for path in targets):
        print("refusing to overwrite an existing runtime shell", file=sys.stderr)
        return 1
    prototype.mkdir(parents=True, exist_ok=True)
    for name in runtime_files:
        shutil.copy2(SHELL / name, prototype / name)
    print(f"Seeded V4.0 runtime shell (not a deliverable): {prototype}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
