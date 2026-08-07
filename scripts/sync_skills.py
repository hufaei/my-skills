#!/usr/bin/env python3
"""Check and regenerate upstream-managed skills declared in sources.yaml."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "sources.yaml"


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict[str, Any]) -> None:
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=REPO_ROOT, delete=False
    ) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, MANIFEST_PATH)


def synced_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [entry for entry in manifest["skills"] if entry["kind"] == "synced"]


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
        digest.update(b"x" if os.access(path, os.X_OK) else b"-")
    return digest.hexdigest()


def latest_commit(entry: dict[str, Any]) -> str:
    output = run("git", "ls-remote", entry["repo"], entry.get("ref", "HEAD"))
    if not output:
        raise RuntimeError(f"No upstream ref for {entry['name']}")
    return output.splitlines()[0].split()[0]


def check(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    latest_by_source: dict[tuple[str, str], str] = {}
    results: list[dict[str, Any]] = []
    for entry in synced_entries(manifest):
        key = (entry["repo"], entry.get("ref", "HEAD"))
        if key not in latest_by_source:
            latest_by_source[key] = latest_commit(entry)
        destination = REPO_ROOT / entry["destination"]
        recorded_hash = entry.get("content_sha256", "")
        actual_hash = tree_hash(destination) if destination.exists() else ""
        results.append(
            {
                "name": entry["name"],
                "repo": entry["repo"],
                "source_path": entry["source_path"],
                "recorded_commit": entry.get("commit", ""),
                "latest_commit": latest_by_source[key],
                "upstream_changed": entry.get("commit", "") != latest_by_source[key],
                "destination": entry["destination"],
                "missing": not destination.exists(),
                "local_modified": bool(recorded_hash and actual_hash != recorded_hash),
            }
        )
    return results


def render_openai_yaml(entry: dict[str, Any]) -> str:
    def quoted(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    return "\n".join(
        [
            "interface:",
            f"  display_name: {quoted(entry['display_name'])}",
            f"  short_description: {quoted(entry['short_description'])}",
            f"  default_prompt: {quoted(entry['default_prompt'])}",
            "policy:",
            "  allow_implicit_invocation: false",
            "",
        ]
    )


def transform_text(text: str, entry: dict[str, Any], source_names: list[str]) -> str:
    source_name = entry["source_name"]
    if entry.get("is_skill_file"):
        text = re.sub(
            rf"(?m)^name:\s*['\"]?{re.escape(source_name)}['\"]?\s*$",
            f"name: {entry['name']}",
            text,
            count=1,
        )

    for old, new in entry.get("replacements", []):
        text = text.replace(old, new)

    for dependency in source_names:
        local = f"jl-{dependency}"
        text = text.replace(f"superpowers:{dependency}", local)
        text = text.replace(f"../{dependency}/", f"../{local}/")
        text = text.replace(f"${dependency}", f"${local}")
        text = text.replace(f"`{dependency}`", f"`{local}`")
        text = re.sub(
            rf"(?<![\w-]){re.escape(dependency)} skill\b",
            f"{local} skill",
            text,
        )
    return text


def transform_tree(root: Path, entry: dict[str, Any], source_names: list[str]) -> None:
    skill_file = root / "SKILL.md"
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        data = path.read_bytes()
        if b"\x00" in data:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        local_entry = dict(entry)
        local_entry["is_skill_file"] = path == skill_file
        transformed = transform_text(text, local_entry, source_names)
        if transformed != text:
            path.write_text(transformed, encoding="utf-8")

    agents = root / "agents"
    agents.mkdir(exist_ok=True)
    (agents / "openai.yaml").write_text(render_openai_yaml(entry), encoding="utf-8")


def replace_directory(staged: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = destination.parent / f".{destination.name}.sync-backup"
    if backup.exists():
        raise RuntimeError(f"Stale sync backup exists: {backup}")
    if destination.exists():
        os.replace(destination, backup)
    try:
        os.replace(staged, destination)
    except Exception:
        if backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def copy_source(source: Path, staged: Path, entry: dict[str, Any]) -> None:
    include_paths = entry.get("include_paths")
    if not include_paths:
        # A Skill may live at the upstream repository root. Git's own
        # metadata is never part of the distributable Skill package.
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns(".git"))
        return

    staged.mkdir()
    for item in include_paths:
        relative = Path(item)
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Invalid include path for {entry['name']}: {item}")
        source_item = source / relative
        destination_item = staged / relative
        if source_item.is_dir():
            shutil.copytree(
                source_item,
                destination_item,
                ignore=shutil.ignore_patterns(".git"),
            )
        elif source_item.is_file():
            destination_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_item, destination_item)
        else:
            raise RuntimeError(f"Missing include path for {entry['name']}: {item}")


def apply(manifest: dict[str, Any], requested: set[str]) -> None:
    entries = synced_entries(manifest)
    known = {entry["name"] for entry in entries}
    unknown = requested - known
    if unknown:
        raise RuntimeError(f"Unknown synced skills: {', '.join(sorted(unknown))}")
    selected = [entry for entry in entries if entry["name"] in requested]
    source_names = [entry["source_name"] for entry in entries]

    for entry in selected:
        destination = REPO_ROOT / entry["destination"]
        recorded_hash = entry.get("content_sha256", "")
        if destination.exists() and recorded_hash:
            actual_hash = tree_hash(destination)
            if actual_hash != recorded_hash:
                raise RuntimeError(
                    f"Refusing to overwrite manually changed synced skill: {entry['name']}"
                )

    with tempfile.TemporaryDirectory(prefix="jl-skill-sync-") as temporary:
        temp_root = Path(temporary)
        clones: dict[str, Path] = {}
        commits: dict[str, str] = {}
        for entry in selected:
            repo = entry["repo"]
            if repo in clones:
                continue
            clone = temp_root / f"source-{len(clones)}"
            run("git", "clone", "--depth", "1", repo, str(clone))
            clones[repo] = clone
            commits[repo] = run("git", "rev-parse", "HEAD", cwd=clone)

        for entry in selected:
            source = clones[entry["repo"]] / entry["source_path"]
            if not (source / "SKILL.md").is_file():
                raise RuntimeError(f"Missing upstream skill: {source}")
            destination = REPO_ROOT / entry["destination"]
            with tempfile.TemporaryDirectory(
                prefix=f".{entry['name']}.stage-", dir=destination.parent
            ) as stage_parent_text:
                stage_parent = Path(stage_parent_text)
                staged = stage_parent / entry["name"]
                copy_source(source, staged, entry)
                transform_tree(staged, entry, source_names)
                generated_hash = tree_hash(staged)
                replace_directory(staged, destination)
            entry["commit"] = commits[entry["repo"]]
            entry["content_sha256"] = generated_hash
            print(f"Synced {entry['name']} @ {entry['commit'][:12]}")

    write_manifest(manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--json", action="store_true")

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("skills", nargs="*")
    apply_parser.add_argument("--all", action="store_true")

    args = parser.parse_args()
    manifest = load_manifest()
    if args.command == "check":
        results = check(manifest)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for item in results:
                flags = [
                    flag
                    for flag in ("upstream_changed", "missing", "local_modified")
                    if item[flag]
                ]
                print(f"{item['name']}: {', '.join(flags) if flags else 'current'}")
        return 0

    requested = {entry["name"] for entry in synced_entries(manifest)} if args.all else set(args.skills)
    if not requested:
        parser.error("apply requires one or more skill names, or --all")
    apply(manifest, requested)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError, OSError, ValueError) as error:
        print(f"sync error: {error}", file=sys.stderr)
        raise SystemExit(1)
