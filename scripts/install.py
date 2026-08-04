#!/usr/bin/env python3
"""Install this repository's skills by creating user-level symlinks."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (REPO_ROOT / "skills", REPO_ROOT / "synced")


def discover_skills() -> list[Path]:
    skills: list[Path] = []
    for root in SKILL_ROOTS:
        if not root.exists():
            continue
        skills.extend(
            path.parent
            for path in root.glob("jl-*/SKILL.md")
            if path.is_file()
        )
    return sorted(skills, key=lambda path: path.name)


def default_destination() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return base / "skills"


def install(destination: Path, dry_run: bool) -> int:
    skills = discover_skills()
    if not skills:
        print("No jl-* skills found.", file=sys.stderr)
        return 1

    conflicts: list[tuple[Path, Path]] = []
    actions: list[tuple[Path, Path]] = []
    for source in skills:
        target = destination / source.name
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            conflicts.append((target, source))
            continue
        actions.append((target, source))

    if conflicts:
        print("Refusing to overwrite existing skill paths:", file=sys.stderr)
        for target, source in conflicts:
            print(f"  {target} (wanted {source})", file=sys.stderr)
        return 2

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for target, source in actions:
            target.symlink_to(source.resolve(), target_is_directory=True)

    verb = "Would link" if dry_run else "Linked"
    for target, source in actions:
        print(f"{verb} {target} -> {source.resolve()}")
    print(f"Available JL skills: {len(skills)}; new links: {len(actions)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Symlink all owned and synced JL skills into Codex."
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=default_destination(),
        help="Skill directory (default: CODEX_HOME/skills or ~/.codex/skills)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return install(args.destination.expanduser().resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
