"""Structural tests using explicitly fictional research-discovery fixtures."""

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "research-discovery-workflow"
    / "scripts"
    / "prepare_run.py"
)


class PrepareRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "fictional_prepare_run_under_test", SCRIPT_PATH
        )
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.module
        with contextlib.ExitStack() as stack:
            for target in (
                "socket.socket",
                "socket.create_connection",
                "subprocess.run",
                "subprocess.Popen",
            ):
                stack.enter_context(
                    mock.patch(target, side_effect=AssertionError("Unexpected external work"))
                )
            spec.loader.exec_module(cls.module)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fictional-prepare-run-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "prepared-run"
        self.source_repository = self.base / "fictional-source-repository"
        self.skill = self.source_repository / "skills" / "research-discovery-workflow"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "# Explicitly fictional fixture skill\n", encoding="utf-8"
        )
        for directory in ("references", "scripts", "agents"):
            (self.skill / directory).mkdir()
        (self.skill / "references" / "nested").mkdir()
        (self.skill / "references" / "nested" / "protocol.md").write_text(
            "Fictional protocol fixture: Q5-R is mandatory.\n", encoding="utf-8"
        )
        (self.skill / "scripts" / "fictional_helper.py").write_text(
            '"""Fictional fixture; no experiments or external calls."""\n',
            encoding="utf-8",
        )
        (self.skill / "agents" / "openai.yaml").write_text(
            "display_name: Fictional fixture\n", encoding="utf-8"
        )
        self.brief = self.base / "fictional-brief.md"
        self.brief_bytes = (
            "# Explicitly fictional research brief\r\n"
            "研究主题：虚构材料的可证伪机制。\r\n"
        ).encode("utf-8")
        self.brief.write_bytes(self.brief_bytes)
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(self.module, "SKILL_DIR", self.skill).start()
        for target in (
            "socket.socket",
            "socket.create_connection",
            "subprocess.run",
            "subprocess.Popen",
        ):
            mock.patch(
                target, side_effect=AssertionError("Unexpected external work")
            ).start()

    def prepare(self, *, root=None, brief=None, pass_number=1):
        return self.module.prepare_run(
            self.root if root is None else root,
            self.brief if brief is None else brief,
            pass_number,
        )

    def assert_rejected_without_root(self, *, brief=None, pass_number=1):
        with self.assertRaises((ValueError, OSError)):
            self.prepare(brief=brief, pass_number=pass_number)
        self.assertFalse(self.root.exists())
        self.assertFalse(self.root.is_symlink())

    def test_creates_required_layout_and_preserves_brief_bytes(self):
        original_stat = self.brief.stat()
        result = self.prepare()
        self.assertEqual(result, self.root)
        self.assertEqual(
            {entry.name for entry in self.root.iterdir()},
            {"BRIEF.md", ".agents", "output", "tmp", "AGENTS.md", "RUN.md"},
        )
        self.assertEqual((self.root / "BRIEF.md").read_bytes(), self.brief_bytes)
        self.assertEqual(self.brief.read_bytes(), self.brief_bytes)
        self.assertEqual(self.brief.stat().st_mtime_ns, original_stat.st_mtime_ns)
        self.assertTrue((self.root / ".agents" / "skills" / self.skill.name).is_dir())
        self.assertTrue((self.root / "tmp").is_dir())
        self.assertTrue((self.root / "AGENTS.md").read_text(encoding="utf-8").strip())
        self.assert_output_is_empty()

    def assert_output_is_empty(self):
        output = self.root / "output"
        self.assertEqual(
            {entry.name for entry in output.iterdir()},
            {"q5-original", "q5-repaired", "final"},
        )
        for name in ("q5-original", "q5-repaired", "final"):
            with self.subTest(output_directory=name):
                directory = output / name
                self.assertTrue(directory.is_dir())
                self.assertEqual(list(directory.iterdir()), [])

    def test_copies_only_skill_payload_and_ignores_recursive_caches(self):
        for parent in (self.source_repository, self.skill):
            (parent / "README.md").write_text(
                "Explicitly fictional repository material; do not copy.\n",
                encoding="utf-8",
            )
            for name in ("tests", "output", "cache"):
                (parent / name).mkdir()
                (parent / name / "fictional-private-marker.txt").write_text(
                    "Explicitly fictional non-skill fixture.\n", encoding="utf-8"
                )
        cache_directories = (
            "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", ".git"
        )
        for payload_name in ("references", "scripts", "agents"):
            payload = self.skill / payload_name
            for cache_name in cache_directories:
                cache = payload / cache_name
                cache.mkdir()
                (cache / "cached.txt").write_text("Fictional cache.\n", encoding="utf-8")
            for cache_name in (".DS_Store", "fixture.pyc", "fixture.pyo"):
                (payload / cache_name).write_bytes(b"fictional cache")
        self.prepare()
        copied = self.root / ".agents" / "skills" / self.skill.name
        self.assertEqual(
            {entry.name for entry in copied.iterdir()},
            {"SKILL.md", "references", "scripts", "agents"},
        )
        expected_files = {
            "SKILL.md",
            "references/nested/protocol.md",
            "scripts/fictional_helper.py",
            "agents/openai.yaml",
        }
        self.assertEqual(
            {entry.relative_to(copied).as_posix() for entry in copied.rglob("*") if entry.is_file()},
            expected_files,
        )
        for name in expected_files:
            self.assertEqual((copied / name).read_bytes(), (self.skill / name).read_bytes())

    def test_run_record_states_prepared_status_and_protocol_limits(self):
        self.prepare()
        run = (self.root / "RUN.md").read_text(encoding="utf-8")
        self.assertIn("prepared-not-started", run)
        self.assertRegex(run, r"pass[-_]number\s*[:=]\s*1")
        self.assertIn("Q5-R", run)
        self.assertIn("Q6", run)
        self.assertRegex(run.lower(), r"mandatory|required|强制|必须")
        self.assertRegex(run.lower(), r"skip|跳过")
        self.assertRegex(run.lower(), r"not (?:a )?sandbox|不是.*沙箱|非沙箱")
        self.assertRegex(
            run.lower(), r"research has not started|no research.*have started|未启动|尚未启动"
        )

    def test_second_pass_remains_prepared_with_empty_outputs(self):
        self.prepare(pass_number=2)
        self.assert_output_is_empty()
        self.assertEqual(list((self.root / "tmp").iterdir()), [])
        run = (self.root / "RUN.md").read_text(encoding="utf-8")
        self.assertIn("prepared-not-started", run)
        self.assertRegex(run, r"pass[-_]number\s*[:=]\s*2")

    def test_existing_directory_is_rejected_and_unchanged(self):
        self.root.mkdir()
        (self.root / "sentinel.txt").write_bytes(b"fictional existing run\n")
        (self.root / "nested").mkdir()
        (self.root / "nested" / "data.txt").write_bytes(b"keep this fixture\n")
        before = {
            path.relative_to(self.root): path.read_bytes() if path.is_file() else None
            for path in self.root.rglob("*")
        }
        with self.assertRaises((ValueError, OSError)):
            self.prepare()
        after = {
            path.relative_to(self.root): path.read_bytes() if path.is_file() else None
            for path in self.root.rglob("*")
        }
        self.assertEqual(after, before)

    def test_existing_file_is_rejected_and_unchanged(self):
        self.root.write_bytes(b"fictional existing file\n")
        with self.assertRaises((ValueError, OSError)):
            self.prepare()
        self.assertEqual(self.root.read_bytes(), b"fictional existing file\n")

    def test_existing_and_dangling_root_symlinks_are_rejected(self):
        for target_name in ("existing-target", "missing-target"):
            with self.subTest(target=target_name):
                target = self.base / target_name
                if target_name == "existing-target":
                    target.mkdir()
                    (target / "sentinel.txt").write_bytes(b"preserve fictional target")
                root = self.base / (target_name + "-link")
                root.symlink_to(target, target_is_directory=True)
                with self.assertRaises((ValueError, OSError)):
                    self.prepare(root=root)
                self.assertTrue(root.is_symlink())
                if target.exists():
                    self.assertEqual(
                        (target / "sentinel.txt").read_bytes(), b"preserve fictional target"
                    )

    def test_invalid_utf8_brief_is_rejected_without_creating_root(self):
        self.brief.write_bytes(b"explicitly fictional invalid UTF-8: \xff\n")
        self.assert_rejected_without_root()
        self.assertEqual(
            self.brief.read_bytes(), b"explicitly fictional invalid UTF-8: \xff\n"
        )

    def test_missing_and_directory_briefs_are_rejected_without_root(self):
        directory = self.base / "fictional-brief-directory"
        directory.mkdir()
        for invalid_brief in (self.base / "missing-brief.md", directory):
            with self.subTest(brief=invalid_brief.name):
                self.assert_rejected_without_root(brief=invalid_brief)

    def test_symlink_brief_is_rejected_without_creating_root(self):
        linked_brief = self.base / "linked-fictional-brief.md"
        linked_brief.symlink_to(self.brief)
        self.assert_rejected_without_root(brief=linked_brief)
        self.assertEqual(self.brief.read_bytes(), self.brief_bytes)

    def test_symlink_skill_root_is_rejected_without_creating_root(self):
        linked_skill = self.base / "linked-fictional-skill"
        linked_skill.symlink_to(self.skill, target_is_directory=True)
        with mock.patch.object(self.module, "SKILL_DIR", linked_skill):
            self.assert_rejected_without_root()

    def test_symlink_payload_files_are_rejected_without_creating_root(self):
        for relative in ("SKILL.md", "references/nested/protocol.md", "scripts/fictional_helper.py"):
            with self.subTest(payload=relative):
                path = self.skill / relative
                original = path.read_bytes()
                outside = self.base / (path.name + ".external")
                outside.write_bytes(original)
                path.unlink()
                path.symlink_to(outside)
                try:
                    self.assert_rejected_without_root()
                finally:
                    path.unlink()
                    path.write_bytes(original)

    def test_symlink_payload_directory_is_rejected_without_creating_root(self):
        references = self.skill / "references"
        external = self.base / "external-fictional-references"
        references.rename(external)
        references.symlink_to(external, target_is_directory=True)
        self.assert_rejected_without_root()

    def test_nested_symlink_directory_is_rejected_without_creating_root(self):
        nested = self.skill / "references" / "nested"
        external = self.base / "external-fictional-nested"
        nested.rename(external)
        nested.symlink_to(external, target_is_directory=True)
        self.assert_rejected_without_root()

    def test_missing_required_skill_payload_is_rejected_without_root(self):
        for name in ("SKILL.md", "references", "scripts", "agents"):
            with self.subTest(payload=name):
                path = self.skill / name
                backup = self.base / (name + ".fixture-backup")
                path.rename(backup)
                try:
                    self.assert_rejected_without_root()
                finally:
                    backup.rename(path)

    def test_invalid_pass_numbers_are_rejected_without_creating_root(self):
        for pass_number in (-1, 0, 3, True, 1.0, "1", None):
            with self.subTest(pass_number=pass_number):
                self.assert_rejected_without_root(pass_number=pass_number)

    def test_root_with_missing_parent_is_rejected_without_creating_parent(self):
        parent = self.base / "missing-fictional-parent"
        with self.assertRaises((ValueError, OSError)):
            self.prepare(root=parent / "prepared-run")
        self.assertFalse(parent.exists())

    def test_root_inside_source_skill_is_rejected_without_changing_payload(self):
        root = self.skill / "prepared-run"
        before = {path.relative_to(self.skill) for path in self.skill.rglob("*")}
        with self.assertRaises((ValueError, OSError)):
            self.prepare(root=root)
        self.assertFalse(root.exists())
        self.assertEqual(
            {path.relative_to(self.skill) for path in self.skill.rglob("*")}, before
        )

    def test_parser_accepts_only_supported_pass_numbers(self):
        for pass_number in (1, 2):
            with self.subTest(pass_number=pass_number):
                args = self.module.parse_args(
                    ["--root", str(self.root), "--brief", str(self.brief),
                     "--pass-number", str(pass_number)]
                )
                self.assertEqual(Path(args.root), self.root)
                self.assertEqual(Path(args.brief), self.brief)
                self.assertEqual(args.pass_number, pass_number)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                self.module.parse_args(
                    ["--root", str(self.root), "--brief", str(self.brief),
                     "--pass-number", "3"]
                )
        self.assertEqual(error.exception.code, 2)

    def test_history_option_is_rejected_and_does_not_create_root(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                self.module.parse_args(
                    ["--root", str(self.root), "--brief", str(self.brief),
                     "--pass-number", "2", "--history", "fictional-history.md"]
                )
        self.assertEqual(error.exception.code, 2)
        self.assertFalse(self.root.exists())

    def test_main_prepares_without_network_or_subprocess_calls(self):
        with contextlib.redirect_stdout(io.StringIO()):
            status = self.module.main(
                ["--root", str(self.root), "--brief", str(self.brief),
                 "--pass-number", "1"]
            )
        self.assertEqual(status, 0)
        self.assert_output_is_empty()
        self.assertEqual(self.brief.read_bytes(), self.brief_bytes)


if __name__ == "__main__":
    unittest.main()
