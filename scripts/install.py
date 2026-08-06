#!/usr/bin/env python3
"""Install or update this repository's skills as independent local copies."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (REPO_ROOT / "skills", REPO_ROOT / "synced")
MANIFEST_PATH = REPO_ROOT / "sources.yaml"
SOURCE_ID = "https://github.com/hufaei/my-skills"
MARKER_NAME = ".jl-install.json"


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


def discover_replacements(skills: list[Path]) -> dict[str, str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    available = {path.name for path in skills}
    replacements: dict[str, str] = {}
    for entry in manifest.get("skills", []):
        replacement = entry.get("name")
        for retired in entry.get("replaces", []):
            if replacement not in available:
                raise ValueError(f"replacement skill is unavailable: {replacement}")
            if not isinstance(retired, str) or not retired.startswith("jl-"):
                raise ValueError(f"invalid retired skill name: {retired!r}")
            if retired in available:
                raise ValueError(f"retired skill is still available: {retired}")
            if retired in replacements:
                raise ValueError(f"duplicate retired skill name: {retired}")
            replacements[retired] = replacement
    return replacements


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if relative == MARKER_NAME:
            continue
        if path.is_symlink():
            digest.update(b"L\0")
            digest.update(relative.encode())
            digest.update(b"\0")
            digest.update(os.readlink(path).encode())
        elif path.is_dir():
            digest.update(b"D\0")
            digest.update(relative.encode())
        elif path.is_file():
            digest.update(b"F\0")
            digest.update(relative.encode())
            digest.update(b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def read_marker(target: Path) -> dict[str, object] | None:
    marker_path = target / MARKER_NAME
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    if not isinstance(marker, dict):
        return None
    return marker


def classify_target(target: Path, source_digest: str) -> tuple[str, str | None]:
    if not target.exists() and not target.is_symlink():
        return "install", None

    if target.is_symlink():
        try:
            resolved = target.resolve(strict=True)
        except OSError:
            return "conflict", "existing link is broken"
        if resolved.is_dir() and tree_digest(resolved) == source_digest:
            return "migrate", None
        return "conflict", "existing link does not match this repository"

    if not target.is_dir():
        return "conflict", "existing path is not a skill directory"

    installed_digest = tree_digest(target)
    marker = read_marker(target)
    if installed_digest == source_digest:
        if (
            marker is not None
            and marker.get("repository") == SOURCE_ID
            and marker.get("skill") == target.name
            and marker.get("content_sha256") == installed_digest
        ):
            return "unchanged", None
        return "adopt", None

    if (
        marker is not None
        and marker.get("repository") == SOURCE_ID
        and marker.get("skill") == target.name
        and marker.get("content_sha256") == installed_digest
    ):
        return "update", None

    return "conflict", "installed copy has unmanaged or local changes"


def classify_retired_target(target: Path) -> tuple[str, str | None]:
    if not target.exists() and not target.is_symlink():
        return "absent", None
    if target.is_symlink() or not target.is_dir():
        return "conflict", "retired path is not a managed skill directory"

    installed_digest = tree_digest(target)
    marker = read_marker(target)
    if (
        marker is not None
        and marker.get("repository") == SOURCE_ID
        and marker.get("skill") == target.name
        and marker.get("content_sha256") == installed_digest
    ):
        return "retire", None
    return "conflict", "retired skill has unmanaged or local changes"


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def replace_with_copy(source: Path, target: Path, source_digest: str) -> None:
    stage_root = Path(tempfile.mkdtemp(prefix=f".{source.name}.stage-", dir=target.parent))
    staged = stage_root / source.name
    backup = target.parent / f".{source.name}.backup-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        shutil.copytree(source, staged, symlinks=True)
        marker = {
            "schema": 1,
            "repository": SOURCE_ID,
            "skill": source.name,
            "content_sha256": source_digest,
        }
        (staged / MARKER_NAME).write_text(
            json.dumps(marker, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if tree_digest(staged) != source_digest:
            raise RuntimeError(f"staged copy verification failed for {source.name}")

        if target.exists() or target.is_symlink():
            target.rename(backup)
            moved_existing = True
        staged.rename(target)
        if moved_existing:
            remove_path(backup)
    except Exception:
        if not target.exists() and not target.is_symlink() and moved_existing and backup.exists():
            backup.rename(target)
        raise
    finally:
        if backup.exists() or backup.is_symlink():
            remove_path(backup)
        if stage_root.exists():
            shutil.rmtree(stage_root)


def install(destination: Path, dry_run: bool) -> int:
    skills = discover_skills()
    if not skills:
        print("No jl-* skills found.", file=sys.stderr)
        return 1

    replacements = discover_replacements(skills)
    plan: list[tuple[str, Path, Path, str]] = []
    retirement_plan: list[tuple[Path, str]] = []
    conflicts: list[tuple[Path, str]] = []
    for source in skills:
        source_digest = tree_digest(source)
        target = destination / source.name
        action, reason = classify_target(target, source_digest)
        if action == "conflict":
            conflicts.append((target, reason or "unknown conflict"))
        else:
            plan.append((action, source, target, source_digest))

    for retired, replacement in replacements.items():
        target = destination / retired
        action, reason = classify_retired_target(target)
        if action == "conflict":
            conflicts.append((target, reason or "unknown conflict"))
        elif action == "retire":
            retirement_plan.append((target, replacement))

    if conflicts:
        print("Refusing to overwrite conflicting skill paths:", file=sys.stderr)
        for target, reason in conflicts:
            print(f"  {target}: {reason}", file=sys.stderr)
        return 2

    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
        for action, source, target, source_digest in plan:
            if action != "unchanged":
                replace_with_copy(source, target, source_digest)
        for target, _ in retirement_plan:
            remove_path(target)

    changed = 0
    for action, source, target, _ in plan:
        if action == "unchanged":
            continue
        changed += 1
        verb = "Would install" if dry_run else "Installed"
        if action in {"migrate", "update", "adopt"}:
            verb = "Would update" if dry_run else "Updated"
        print(f"{verb} {target} from {source}")

    for target, replacement in retirement_plan:
        verb = "Would remove" if dry_run else "Removed"
        print(f"{verb} retired {target}; replaced by {replacement}")

    unchanged = len(plan) - changed
    print(
        f"Available JL skills: {len(skills)}; "
        f"changed: {changed}; unchanged: {unchanged}; "
        f"retired: {len(retirement_plan)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy all owned and synced JL skills into Codex."
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
