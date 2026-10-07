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
from unittest import mock


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
            '```markdown\n[example](missing.md)\n```\n'
            '~~~text\n[example](also-missing.md)\n~~~\n'
            '`[inline](missing.md)` ``[inline](another-missing.md)``\n\n'
            '    [indented](missing.md)\n\t[tabbed](missing.md)\n', encoding="utf-8")
        self.assertEqual(checker.check_repository(self.root), [])

    def test_balanced_link_filenames_and_bad_prose_targets_keep_their_line_numbers(self):
        (self.root / "docs/report(1).md").write_text("Fictional result.\n", encoding="utf-8")
        text = (
            '```text\n[code](not-a-file.md)\n```\n'
            '[balanced](report(1).md) [escaped](report\\(1\\).md)\n'
            '`[inline](not-a-file.md)`\n[bad prose](missing(2).md)\n'
        )
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [
            (4, "report(1).md"), (4, "report(1).md"), (6, "missing(2).md"),
        ])
        findings = self.findings()
        self.assertIn("docs/guide.md:6: missing local link or asset: missing(2).md", findings)
        self.assertNotIn("report(1).md", findings)
        self.assertNotIn("not-a-file.md", findings)

    def test_list_continuation_links_are_checked_but_list_code_remains_literal(self):
        (self.root / "docs/report(1).md").write_text("Fictional result.\n", encoding="utf-8")
        text = (
            '1. Parent item\n\n'
            '    [report](report(1).md)\n\n'
            '        [code](not-a-file.md)\n\n'
            '    [bad](missing.md)\n\n'
            '    ```text\n    [fenced code](another-missing.md)\n    ```\n'
        )
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [(3, "report(1).md"), (7, "missing.md")])
        findings = self.findings()
        self.assertIn("docs/guide.md:7: missing local link or asset: missing.md", findings)
        self.assertNotIn("not-a-file.md", findings)
        self.assertNotIn("another-missing.md", findings)

    def test_link_label_code_is_not_html_but_rendered_label_assets_are_checked(self):
        text = (
            '[Literal `<img src="missing.svg">`](guide.md)\n'
            '[Real <img src="images/banner.svg">](guide.md "<img src=title-only.svg>")\n'
        )
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [
            (1, "guide.md"), (2, "guide.md"), (2, "images/banner.svg"),
        ])
        self.assertEqual(checker.check_repository(self.root), [])

    def test_empty_image_labels_still_check_the_asset(self):
        text = '![](missing.svg) [](missing.md)\n'
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [(1, "missing.svg"), (1, "missing.md")])
        self.assertIn("missing local link or asset: missing.svg", self.findings())

    def test_indented_paragraph_continuation_is_not_a_code_block(self):
        text = 'Paragraph\n    [visible](missing.md)\n\n    [literal](not-a-file.md)\n'
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [(2, "missing.md")])
        self.assertIn("docs/guide.md:2: missing local link or asset: missing.md", self.findings())
        self.assertNotIn("not-a-file.md", self.findings())

    def test_brackets_inside_label_code_spans_do_not_unbalance_links(self):
        text = '[Literal `[`](missing.md) [Literal ``]`[``](other.md)\n'
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [(1, "missing.md"), (1, "other.md")])
        self.assertIn("missing local link or asset: missing.md", self.findings())

    def test_angle_destinations_can_contain_unbalanced_parentheses(self):
        text = '[paper](<https://example.invalid/paper)>) [local](<missing(.md>)\n'
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [
            (1, "https://example.invalid/paper)"), (1, "missing(.md"),
        ])
        self.assertIn("missing local link or asset: missing(.md", self.findings())
        self.assertNotIn("example.invalid", self.findings())

    def test_quoted_titles_have_separate_delimiters_from_destinations(self):
        text = '[report](missing.md "A( title") [report](other.md \'A) title\')\n'
        (self.root / "docs/guide.md").write_text(text, encoding="utf-8")
        self.assertEqual(checker._document_targets(text), [(1, "missing.md"), (1, "other.md")])
        self.assertIn("missing local link or asset: other.md", self.findings())

    def evidence_fixture(self):
        case = self.root / "docs/validation-runs/fictional-run/evidence/CASE"
        case.mkdir(parents=True)
        files = {"final.md": b"Fictional scientific limitation.\n", "output/result.txt": b"Fictional estimate.\n"}
        for name, data in files.items():
            path = case / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        manifest = {"format_version": 1, "public_files": {
            name: hashlib.sha256(data).hexdigest() for name, data in files.items()
        }}
        path = case / "export.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return case, path, manifest

    def test_public_evidence_hashes_detect_changed_and_missing_declared_files(self):
        case, _path, _manifest = self.evidence_fixture()
        self.assertEqual(checker.check_repository(self.root), [])
        (case / "final.md").write_bytes(b"Changed fictional scientific limitation.\n")
        (case / "output/result.txt").unlink()
        findings = self.findings()
        self.assertIn("public evidence SHA256 mismatch: final.md", findings)
        self.assertIn("declared public evidence file is missing: output/result.txt", findings)

    def test_evidence_summary_itself_is_excluded_and_invalid_summaries_are_actionable(self):
        _case, path, manifest = self.evidence_fixture()
        manifest["public_files"]["export.json"] = "0" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertIn("public_files must exclude the summary itself", self.findings())
        for malformed in ("{invalid", "[]", '{"format_version":1,"public_files":{}}'):
            with self.subTest(malformed=malformed):
                path.write_text(malformed, encoding="utf-8")
                self.assertIn("export.json:", self.findings())

    def test_evidence_invalid_paths_and_hashes_do_not_read_outside_case(self):
        _case, path, _manifest = self.evidence_fixture()
        original_read = Path.read_bytes

        def scoped_read(candidate):
            if not candidate.resolve().is_relative_to(self.root.resolve()):
                raise AssertionError("Checker read outside the fictional package")
            return original_read(candidate)

        for name, digest in (("../../outside.txt", "0" * 64), ("/private/fixture.txt", "0" * 64),
                             (".", "0" * 64), ("runs/raw.jsonl", "0" * 64), ("final.md", "invalid-hash")):
            with self.subTest(name=name):
                path.write_text(json.dumps({"format_version": 1, "public_files": {name: digest}}), encoding="utf-8")
                with mock.patch.object(Path, "read_bytes", new=scoped_read):
                    self.assertIn("invalid public evidence", self.findings())

    def test_evidence_symlinks_are_rejected_without_following_them(self):
        case, path, manifest = self.evidence_fixture()
        (case / "linked.txt").symlink_to(self.root / "LICENSE")
        manifest["public_files"]["linked.txt"] = "0" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertIn("public evidence must be a local regular file: linked.txt", self.findings())

    def test_evidence_rejects_drive_and_stream_syntax_in_every_component(self):
        _case, path, _manifest = self.evidence_fixture()
        for name in ("output/D:/outside.txt", "output/D:outside.txt", "output/file.txt:stream"):
            with self.subTest(name=name):
                path.write_text(json.dumps({"format_version": 1, "public_files": {name: "0" * 64}}), encoding="utf-8")
                self.assertIn("invalid public evidence path", self.findings())

    def test_evidence_surrogate_filename_is_an_issue_not_an_uncaught_error(self):
        _case, path, _manifest = self.evidence_fixture()
        path.write_text(json.dumps({"format_version": 1, "public_files": {"\ud800": "0" * 64}}), encoding="utf-8")
        self.assertIn("invalid public evidence path", self.findings())

    def test_evidence_checks_ignore_raw_and_non_evidence_export_files(self):
        for name in ("runs/private/export.json", "docs/validation-runs/fictional-run/fixtures/export.json"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{not a public evidence summary", encoding="utf-8")
        self.assertEqual(checker.check_repository(self.root), [])

    def test_current_checkout_passes(self):
        self.assertEqual(checker.check_repository(REPO), [])


if __name__ == "__main__":
    unittest.main()
