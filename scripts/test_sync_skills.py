#!/usr/bin/env python3
"""Compatibility and sync contracts; run with python3 scripts/test_sync_skills.py."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync_skills as sync


def skill_entry(**overrides):
    entry = {
        "kind": "synced",
        "name": "jl-ponytail",
        "source_name": "ponytail",
        "source_path": ".",
        "destination": "synced/jl-ponytail",
        "display_name": "Ponytail",
        "short_description": "Keep the solution small.",
        "default_prompt": "Use $jl-ponytail.",
        "allow_implicit_invocation": False,
    }
    entry.update(overrides)
    return entry


def read_openai_yaml(path):
    """Read the generated two-section mapping without a YAML dependency."""
    result = {}
    for line in path.read_text().splitlines():
        if not line.startswith(" "):
            section = line.removesuffix(":")
            result[section] = {}
        else:
            key, value = line.removeprefix("  ").split(": ", 1)
            result[section][key] = json.loads(value)
    return result


class FrontmatterTests(unittest.TestCase):
    def test_unsupported_fields_are_removed_regardless_of_value_or_policy(self):
        fields = [
            'argument-hint: "[lite|full|ultra]"\n',
            'argument-hint: "[lite|full|ultra|off]"\n',
            "argument-hint: '[lite|full|ultra|off]'\n",
            "argument-hint: lite or off\n",
            "argument-hint: >-\n  lite or\n  off\n\n",
            "'argument-hint': |\n  [lite|full|ultra|off]\n",
            "disable-model-invocation: true\n",
            "disable-model-invocation: false\n",
            '"disable-model-invocation": "false"\n',
            "disable-model-invocation: null\n",
            "disable-model-invocation:\n  nested: value\n",
        ]
        for field in fields:
            for implicit in (False, True):
                with self.subTest(field=field, implicit=implicit):
                    text = "---\nname: ponytail\n" + field + "license: MIT\n---\n"
                    actual = sync.transform_text(
                        text,
                        skill_entry(is_skill_file=True, allow_implicit_invocation=implicit),
                        ["ponytail"],
                    )
                    self.assertEqual(actual, "---\nname: jl-ponytail\nlicense: MIT\n---\n")

    def test_only_first_frontmatter_top_level_fields_are_normalized(self):
        body = (
            "\n```yaml\nname: ponytail\nargument-hint: example\n"
            "disable-model-invocation: true\n```\n"
            "---\nname: ponytail\nargument-hint: later document\n---\n"
        )
        retained = (
            "description: >\n  name: ponytail\n"
            "metadata:\n  argument-hint: nested\n  disable-model-invocation: true\n"
            "unknown-field: preserved\n"
        )
        actual = sync.transform_text(
            "---\nname: 'ponytail' # upstream\n" + retained
            + "argument-hint: |\n  removed\n# license follows\nlicense: MIT\n---\n" + body,
            skill_entry(is_skill_file=True),
            ["ponytail"],
        )
        self.assertEqual(
            actual,
            "---\nname: jl-ponytail # upstream\n" + retained
            + "# license follows\nlicense: MIT\n---\n" + body,
        )
        for text in (
            "name: ponytail\nargument-hint: body\n---\n",
            "---\nname: ponytail\nargument-hint: unclosed\n",
        ):
            with self.subTest(text=text):
                self.assertEqual(
                    sync.transform_text(text, skill_entry(is_skill_file=True), ["ponytail"]),
                    text,
                )
        crlf = '---\r\nname: "ponytail"\r\nargument-hint: off\r\n---\r\nbody\r\n'
        self.assertEqual(
            sync.transform_text(crlf, skill_entry(is_skill_file=True), ["ponytail"]),
            "---\r\nname: jl-ponytail\r\n---\r\nbody\r\n",
        )

    def test_tree_generation_preserves_references_and_manifest_invocation_policy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reference = "---\nname: ponytail\nargument-hint: example\n---\n"
            for implicit in (False, True):
                with self.subTest(implicit=implicit):
                    (root / "SKILL.md").write_text(
                        "---\nname: ponytail\nargument-hint: off\n"
                        "disable-model-invocation: true\n---\n"
                        "$dependency superpowers:dependency ../dependency/ `dependency` "
                        "dependency skill /ponytail\n"
                    )
                    (root / "references").mkdir(exist_ok=True)
                    (root / "references" / "SKILL.md").write_text(reference)
                    (root / "examples.md").write_text(reference)
                    (root / "image.bin").write_bytes(b"\x00$dependency")
                    (root / "agents").mkdir(exist_ok=True)
                    (root / "agents" / "openai.yaml").write_text("upstream metadata\n")
                    entry = skill_entry(
                        allow_implicit_invocation=implicit,
                        replacements=[["/ponytail", "$jl-ponytail"]],
                    )
                    sync.transform_tree(root, entry, ["ponytail", "dependency"])
                    self.assertEqual(
                        (root / "SKILL.md").read_text(),
                        "---\nname: jl-ponytail\n---\n"
                        "$jl-dependency jl-dependency ../jl-dependency/ `jl-dependency` "
                        "jl-dependency skill $jl-ponytail\n",
                    )
                    self.assertEqual((root / "references" / "SKILL.md").read_text(), reference)
                    self.assertEqual((root / "examples.md").read_text(), reference)
                    self.assertEqual((root / "image.bin").read_bytes(), b"\x00$dependency")
                    self.assertEqual(
                        read_openai_yaml(root / "agents" / "openai.yaml"),
                        {
                            "interface": {key: entry[key] for key in (
                                "display_name", "short_description", "default_prompt"
                            )},
                            "policy": {"allow_implicit_invocation": implicit},
                        },
                    )


class ApplyTests(unittest.TestCase):
    def test_apply_tracks_source_and_protects_local_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            upstream = root / "upstream"
            upstream.mkdir()
            sync.run("git", "init", "--initial-branch=main", cwd=upstream)
            skill = upstream / "SKILL.md"
            skill.write_text("---\nname: ponytail\n---\nold\n")
            sync.run("git", "add", ".", cwd=upstream)
            commit_args = ("git", "-c", "user.name=Sync Test", "-c",
                           "user.email=sync-test@example.invalid", "commit", "-m")
            sync.run(*commit_args, "initial", cwd=upstream)
            old_commit = sync.run("git", "rev-parse", "HEAD", cwd=upstream)
            skill.write_text(
                "---\nname: ponytail\nargument-hint: off\n"
                "disable-model-invocation: true\n---\nnew\n"
            )
            sync.run("git", "add", ".", cwd=upstream)
            sync.run(*commit_args, "updated", cwd=upstream)
            tip = sync.run("git", "rev-parse", "HEAD", cwd=upstream)

            project = root / "project"
            destination = project / "synced" / "jl-ponytail"
            destination.mkdir(parents=True)
            (destination / "SKILL.md").write_text("old generated content\n")
            untouched = project / "synced" / "jl-other"
            untouched.mkdir()
            (untouched / "SKILL.md").write_text("untouched\n")
            (untouched / "asset.bin").write_bytes(b"\x00unchanged")
            selected = skill_entry(repo=upstream.as_uri(), commit=old_commit)
            selected["content_sha256"] = sync.tree_hash(destination)
            unselected = skill_entry(
                name="jl-other", source_name="other", destination="synced/jl-other",
                repo=upstream.as_uri(), commit=old_commit,
                content_sha256=sync.tree_hash(untouched),
            )
            original_unselected = copy.deepcopy(unselected)
            untouched_files = {path.name: path.read_bytes() for path in untouched.iterdir()}
            manifest = {"skills": [selected, unselected]}
            manifest_path = project / "sources.yaml"
            manifest_path.write_text(json.dumps(manifest))

            with patch.object(sync, "REPO_ROOT", project), patch.object(
                sync, "MANIFEST_PATH", manifest_path
            ), contextlib.redirect_stdout(io.StringIO()):
                sync.apply(manifest, {"jl-ponytail"})
                self.assertEqual(selected["commit"], tip)
                self.assertNotEqual(selected["commit"], old_commit)
                self.assertEqual(selected["content_sha256"], sync.tree_hash(destination))
                self.assertEqual(
                    (destination / "SKILL.md").read_text(),
                    "---\nname: jl-ponytail\n---\nnew\n",
                )
                self.assertFalse((destination / ".git").exists())
                self.assertEqual(
                    read_openai_yaml(destination / "agents" / "openai.yaml")["policy"],
                    {"allow_implicit_invocation": False},
                )
                self.assertEqual(json.loads(manifest_path.read_text()), manifest)
                self.assertEqual(unselected, original_unselected)
                self.assertEqual(
                    {path.name: path.read_bytes() for path in untouched.iterdir()}, untouched_files
                )

                saved_manifest = manifest_path.read_bytes()
                (destination / "SKILL.md").write_text("manual change\n")
                with self.assertRaises(RuntimeError):
                    sync.apply(manifest, {"jl-ponytail"})
                self.assertEqual((destination / "SKILL.md").read_text(), "manual change\n")
                self.assertEqual(manifest_path.read_bytes(), saved_manifest)
                self.assertEqual(unselected, original_unselected)
                self.assertEqual(
                    {path.name: path.read_bytes() for path in untouched.iterdir()}, untouched_files
                )


if __name__ == "__main__":
    unittest.main()
