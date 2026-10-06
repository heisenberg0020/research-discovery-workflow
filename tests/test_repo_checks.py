"""Fictional package fixtures test structure, not research behavior or isolation."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("repo_checker", REPO / "scripts/check_repo.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class RepositoryCheckTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="discovery-package-check-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name) / "fixture"
        self.base.mkdir()
        files = {
            "README.md": '# Fictional package\n\n[Guide](docs/guide.md#start)\n<img src="docs/images/banner.svg">\n',
            "README_EN.md": "# Fictional package\n\n[Home](README.md)\n",
            "AGENTS.md": "# Fixture scope\n",
            "CONTRIBUTING.md": "# Fixture contributions\n",
            "CHANGELOG.md": "# Changes\n\n## 1.1.0\n\nFictional package change.\n",
            "LICENSE": "Fictional test license.\n",
            "VERSION": "1.1.0\n",
            "docs/guide.md": '# Guide\n\n[Home](../README.md)\n<a href="../README_EN.md">English</a>\n',
            "docs/STARTER_PROMPTS.zh-CN.md": "# Frozen fictional starter\n",
            "docs/QUICKSTART.en.md": "# Frozen fictional start\n",
            "docs/images/banner.svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200"><title>Fixture</title><desc>Fictional decorative banner.</desc></svg>\n',
            "examples/brief.md": "# Fictional neutral brief\n\n[Guide](../docs/guide.md)\n",
            f"{checker.SKILL_PATH}/SKILL.md": '---\nname: research-discovery-workflow\ndescription: "Fictional package structure fixture."\n---\n\n# Fixture\n\n[Reference](references/guide.md)\n',
            f"{checker.SKILL_PATH}/references/guide.md": "# Fictional reference\n",
            f"{checker.SKILL_PATH}/agents/openai.yaml": "interface:\n  display_name: Fixture\n",
            f"{checker.SKILL_PATH}/scripts/prepare_run.py": '"""Fictional helper fixture; never executed."""\n',
        }
        for name, text in files.items():
            path = self.base / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        frozen = sorted(name for name in files if name.startswith(checker.SKILL_PATH + "/")
                        or name in checker.FROZEN_DOCUMENTS)
        manifest = {
            "baseline_revision": "v1.0.0",
            "baseline_commit": "0" * 40,
            "files": {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                      for name in frozen},
        }
        (self.base / "docs/workflow-freeze.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.root = Path(temporary.name) / "package-copy"
        shutil.copytree(self.base, self.root)

    def findings(self):
        return "\n".join(checker.check_repository(self.root))

    def test_complete_fixture_passes_and_cli_succeeds(self):
        self.assertEqual(checker.check_repository(self.root), [])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(checker.main(["--root", str(self.root)]), 0)
        self.assertIn("workflow freeze passed", output.getvalue())

    def test_missing_markdown_link_is_actionable(self):
        (self.root / "docs/guide.md").unlink()
        self.assertIn("README.md:3: missing local link or asset: docs/guide.md#start", self.findings())
        with contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(checker.main(["--root", str(self.root)]), 1)
        self.assertIn("docs/guide.md", output.getvalue())

    def test_missing_html_asset_is_detected(self):
        (self.root / "docs/images/banner.svg").unlink()
        self.assertIn("missing local link or asset: docs/images/banner.svg", self.findings())

    def test_missing_license_is_detected(self):
        (self.root / "LICENSE").unlink()
        self.assertIn("LICENSE: required public file is missing", self.findings())

    def test_version_mismatch_and_non_numeric_version_are_detected(self):
        version = self.root / "VERSION"
        version.write_text("1.2.0\n", encoding="utf-8")
        self.assertIn("current version heading must match VERSION", self.findings())
        version.write_text("1.1.0-rc.1\n", encoding="utf-8")
        self.assertIn("numeric MAJOR.MINOR.PATCH", self.findings())
        version.write_text("01.1.0\n", encoding="utf-8")
        self.assertIn("numeric MAJOR.MINOR.PATCH", self.findings())

    def test_frozen_instruction_mutation_is_detected(self):
        reference = self.root / checker.SKILL_PATH / "references/guide.md"
        reference.write_text("# Changed fictional instruction\n", encoding="utf-8")
        self.assertIn("references/guide.md: bytes differ from the frozen workflow baseline", self.findings())

    def test_added_and_removed_skill_files_are_detected(self):
        skill = self.root / checker.SKILL_PATH
        (skill / "references/extra.md").write_text("# Fictional addition\n", encoding="utf-8")
        (skill / "scripts/prepare_run.py").unlink()
        findings = self.findings()
        self.assertIn("extra.md: added file is outside the frozen workflow inventory", findings)
        self.assertIn("prepare_run.py: frozen workflow file is missing", findings)

    def test_frozen_starter_mutation_is_detected(self):
        (self.root / "docs/QUICKSTART.en.md").write_text("Changed fixture.\n", encoding="utf-8")
        self.assertIn("docs/QUICKSTART.en.md: bytes differ", self.findings())

    def test_svg_requires_accessible_description_and_valid_xml(self):
        svg = self.root / "docs/images/banner.svg"
        svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200"><title>Fixture</title></svg>', encoding="utf-8")
        self.assertIn("requires a nonempty desc", self.findings())
        svg.write_text("<svg", encoding="utf-8")
        self.assertIn("invalid SVG XML", self.findings())
        svg.write_text('<svg viewBox="0 0 inf 200"><title>Fixture</title><desc>Fixture.</desc></svg>', encoding="utf-8")
        findings = self.findings()
        self.assertIn("SVG namespace", findings)
        self.assertIn("four-number viewBox", findings)

    def test_frontmatter_and_required_metadata_are_checked(self):
        skill = self.root / checker.SKILL_PATH
        (skill / "SKILL.md").write_text("---\nname: research-discovery-workflow\n---\n[Reference](references/guide.md)\n", encoding="utf-8")
        (skill / "agents/openai.yaml").unlink()
        findings = self.findings()
        self.assertIn("frontmatter requires description", findings)
        self.assertIn("agents/openai.yaml: required skill resource is missing", findings)

    def test_link_scope_does_not_read_neighbors_or_generated_trees(self):
        for directory in ("runs", "dist", "docs/cache", "docs/runs", "skills/__pycache__"):
            path = self.root / directory / "unscanned.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("[broken](missing.md)\n", encoding="utf-8")
        self.assertEqual(checker.check_repository(self.root), [])
        (self.root / "docs/guide.md").write_text("[outside](../../neighbor.md)\n", encoding="utf-8")
        self.assertIn("local target leaves this repository", self.findings())

    def test_external_fragment_and_fenced_example_targets_are_ignored(self):
        (self.root / "docs/guide.md").write_text(
            '[web](https://example.invalid/a) [mail](mailto:example@example.invalid) [section](#here)\n'
            '```markdown\n[example](missing.md)\n```\n', encoding="utf-8")
        self.assertEqual(checker.check_repository(self.root), [])

    def test_current_checkout_passes(self):
        self.assertEqual(checker.check_repository(REPO), [])


if __name__ == "__main__":
    unittest.main()
