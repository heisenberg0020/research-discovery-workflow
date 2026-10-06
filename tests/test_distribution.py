"""Local distribution checks with fictional fixtures; no scientific quality claim."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_NAME = "research-discovery-workflow"


def load_helper(filename, module_name):
    spec = importlib.util.spec_from_file_location(module_name, REPOSITORY / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(sys, "dont_write_bytecode", True))
        for target in ("socket.socket", "socket.create_connection", "subprocess.run", "subprocess.Popen"):
            stack.enter_context(mock.patch(target, side_effect=AssertionError("Unexpected external work")))
        spec.loader.exec_module(module)
    return module


INSTALL = load_helper("install.py", "fictional_install_under_test")
RELEASE = load_helper("build_release.py", "fictional_release_under_test")


def snapshot(directory):
    return {
        entry.relative_to(directory).as_posix(): (
            "link", os.readlink(entry)
        ) if entry.is_symlink() else (
            "file", entry.read_bytes(), entry.stat().st_mtime_ns
        ) if entry.is_file() else ("directory",)
        for entry in directory.rglob("*")
    }


class TemporaryFixtureTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fictional-distribution-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        for target in ("socket.socket", "socket.create_connection"):
            patch = mock.patch(target, side_effect=AssertionError("Unexpected network work"))
            patch.start()
            self.addCleanup(patch.stop)


class InstallerTests(TemporaryFixtureTests):
    def setUp(self):
        super().setUp()
        self.source = self.base / "fictional-source"
        self.skill = self.source / "skills" / SKILL_NAME
        self.skill.mkdir(parents=True)
        self.license_path = self.source / "LICENSE"
        self.license_path.write_bytes(b"Explicitly fictional license fixture.\n")
        (self.skill / "SKILL.md").write_bytes(b"# Explicitly fictional, frozen skill fixture\n")
        for directory in ("references", "scripts", "agents"):
            payload = self.skill / directory
            (payload / "nested").mkdir(parents=True)
            (payload / "nested" / "fictional.txt").write_bytes(b"Explicitly fictional payload.\n")
        self.destination = self.base / "new" / "skills"
        for name, value in (("SKILL_DIR", self.skill), ("LICENSE_PATH", self.license_path)):
            patch = mock.patch.object(INSTALL, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        for target in ("subprocess.run", "subprocess.Popen"):
            patch = mock.patch(target, side_effect=AssertionError("Unexpected external work"))
            patch.start()
            self.addCleanup(patch.stop)

    def test_cli_dry_run_creates_nothing_even_when_destination_parent_is_missing(self):
        before = snapshot(self.base)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            status = INSTALL.main(["--dest", str(self.destination), "--dry-run"])
        self.assertEqual(status, 0)
        self.assertIn("Dry run:", output.getvalue())
        self.assertIn("no files or directories were written", output.getvalue())
        self.assertEqual(snapshot(self.base), before)
        self.assertFalse(self.destination.parent.exists())

    def test_cli_installs_only_unchanged_skill_payload_and_repository_license(self):
        (self.source / "PRIVATE-FICTIONAL-MARKER.txt").write_bytes(b"Must not be copied.\n")
        (self.skill / "README.md").write_bytes(b"Not part of installation payload.\n")
        before = snapshot(self.source)
        with contextlib.redirect_stdout(io.StringIO()):
            status = INSTALL.main(["--dest", str(self.destination)])
        self.assertEqual(status, 0)
        target = self.destination / SKILL_NAME
        self.assertEqual(
            {path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_file()},
            {"SKILL.md", "LICENSE", "references/nested/fictional.txt", "scripts/nested/fictional.txt", "agents/nested/fictional.txt"},
        )
        self.assertEqual((target / "LICENSE").read_bytes(), self.license_path.read_bytes())
        for path in self.skill.rglob("*"):
            if path.is_file() and path.name != "README.md":
                self.assertEqual((target / path.relative_to(self.skill)).read_bytes(), path.read_bytes())
        self.assertEqual(snapshot(self.source), before)

    def test_recursive_cache_entries_are_excluded(self):
        for directory in ("references", "scripts", "agents"):
            payload = self.skill / directory / "nested"
            for name in ("__pycache__", ".cache", ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv"):
                (payload / name).mkdir()
                (payload / name / "cache.txt").write_bytes(b"Fictional rebuildable cache.\n")
            for name in (".DS_Store", "fictional.pyc", "fictional.pyo"):
                (payload / name).write_bytes(b"Fictional rebuildable cache.\n")
        target = INSTALL.install_skill(self.destination)
        self.assertEqual(
            {path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_file()},
            {"SKILL.md", "LICENSE", "references/nested/fictional.txt", "scripts/nested/fictional.txt", "agents/nested/fictional.txt"},
        )

    def test_existing_directory_file_and_broken_link_targets_are_preserved(self):
        for kind in ("directory", "file", "broken-link"):
            with self.subTest(kind=kind):
                destination = self.base / kind
                destination.mkdir()
                target = destination / SKILL_NAME
                if kind == "directory":
                    target.mkdir()
                    (target / "sentinel.txt").write_bytes(b"Preserve this fictional user file.\n")
                elif kind == "file":
                    target.write_bytes(b"Preserve this fictional user file.\n")
                else:
                    target.symlink_to(self.base / "missing-fictional-target")
                before = snapshot(destination)
                for dry_run in (False, True):
                    with self.assertRaises(FileExistsError):
                        INSTALL.install_skill(destination, dry_run=dry_run)
                    self.assertEqual(snapshot(destination), before)

    def test_default_destinations_stay_in_temporary_fixture(self):
        temporary_codex = self.base / "fictional-codex-home"
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(temporary_codex)}):
            target = INSTALL.install_skill(dry_run=True)
            self.assertEqual(target, temporary_codex / "skills" / SKILL_NAME)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(Path, "home", return_value=self.base):
            target = INSTALL.install_skill(dry_run=True)
            self.assertEqual(target, self.base / ".codex" / "skills" / SKILL_NAME)
        self.assertFalse(temporary_codex.exists())
        self.assertFalse((self.base / ".codex").exists())

    def test_missing_license_payload_and_source_links_fail_before_destination_creation(self):
        for path in (self.license_path, self.skill / "SKILL.md", self.skill / "references"):
            with self.subTest(path=path.name):
                backup = path.with_name(path.name + ".backup")
                path.rename(backup)
                try:
                    with self.assertRaises((OSError, ValueError)):
                        INSTALL.install_skill(self.destination)
                    self.assertFalse(self.destination.parent.exists())
                    path.symlink_to(backup, target_is_directory=backup.is_dir())
                    with self.assertRaises((OSError, ValueError)):
                        INSTALL.install_skill(self.destination)
                    self.assertFalse(self.destination.parent.exists())
                    path.unlink()
                finally:
                    backup.rename(path)

    def test_nested_payload_link_is_rejected_without_writes(self):
        linked = self.skill / "scripts" / "nested" / "linked.txt"
        linked.symlink_to(self.license_path)
        before = snapshot(self.base)
        with self.assertRaises(ValueError):
            INSTALL.install_skill(self.destination)
        self.assertEqual(snapshot(self.base), before)

    def test_destination_file_and_inside_source_are_rejected(self):
        destination_file = self.base / "fictional-destination-file"
        destination_file.write_bytes(b"Preserve this fixture.\n")
        for destination in (destination_file, destination_file / "skills"):
            for dry_run in (False, True):
                with self.assertRaises(ValueError):
                    INSTALL.install_skill(destination, dry_run=dry_run)
        self.assertEqual(destination_file.read_bytes(), b"Preserve this fixture.\n")
        with self.assertRaises(ValueError):
            INSTALL.install_skill(self.skill / "nested-destination")
        self.assertFalse((self.skill / "nested-destination").exists())


class ReleaseTests(TemporaryFixtureTests):
    def setUp(self):
        super().setUp()
        self.repo = self.base / "fictional-git-repository"
        self.repo.mkdir()
        original_run = subprocess.run

        def local_git_only(arguments, *args, **kwargs):
            if not isinstance(arguments, list) or arguments[0] != "git":
                raise AssertionError("Only local Git fixture operations are allowed")
            return original_run(arguments, *args, **kwargs)

        patch = mock.patch("subprocess.run", side_effect=local_git_only)
        patch.start()
        self.addCleanup(patch.stop)
        self.git("init", "-q")
        self.files = {
            name: b"# Explicitly fictional public release fixture\n"
            for name in (
                "README.md", "README_EN.md", "AGENTS.md", "CONTRIBUTING.md", "LICENSE", "CHANGELOG.md",
                "scripts/install.py", "scripts/build_release.py",
                "skills/research-discovery-workflow/SKILL.md",
                "skills/research-discovery-workflow/agents/openai.yaml",
                "skills/research-discovery-workflow/scripts/prepare_run.py",
                "skills/research-discovery-workflow/references/fictional.md",
                "docs/FICTIONAL.md", "tests/fictional.txt", "examples/fictional.txt", ".github/workflows/fictional.yml",
            )
        }
        self.files["VERSION"] = b"1.1.0\n"
        self.files[".gitignore"] = b"__pycache__/\n*.py[cod]\n.DS_Store\n.cache/\ndist/\n"
        for name, data in self.files.items():
            self.write(name, data)
        self.commit()
        self.output = self.base / "new-release"

    def git(self, *arguments):
        return subprocess.run(
            ["git", *arguments], cwd=self.repo, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout

    def write(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def commit(self):
        self.git("add", "--all")
        self.git(
            "-c", "user.name=Fictional Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-qm", "Explicitly fictional package fixture",
        )

    def build(self, output=None):
        return RELEASE.build_release(self.output if output is None else output, repository=self.repo)

    def rejected_build(self):
        with self.assertRaises((ValueError, OSError)):
            self.build()
        self.assertFalse(self.output.exists())

    def test_reproducible_build_uses_only_head_and_verifies_without_extraction(self):
        self.write("skills/research-discovery-workflow/scripts/__pycache__/fictional.pyc", b"Ignored fixture.")
        self.write(".DS_Store", b"Ignored fixture.")
        first = self.build()
        second = self.build(self.base / "second-release")
        for name in (first.name, "manifest.json", "SHA256SUMS"):
            self.assertEqual((first.parent / name).read_bytes(), (second.parent / name).read_bytes())
        before = snapshot(first.parent)
        manifest = RELEASE.verify_release(first)
        self.assertEqual(snapshot(first.parent), before)
        self.assertEqual(manifest["version"], "1.1.0")
        self.assertEqual(manifest["commit"], self.git("rev-parse", "HEAD").decode().strip())
        self.assertEqual(set(manifest["files"]), set(self.files))
        prefix = "research-discovery-workflow-1.1.0/"
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(archive.namelist(), sorted(archive.namelist()))
            self.assertEqual(set(archive.namelist()), {prefix + name for name in self.files} | {prefix + "manifest.json"})
            for entry in archive.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
            for name, data in self.files.items():
                self.assertEqual(archive.read(prefix + name), data)
                self.assertEqual(manifest["files"][name], hashlib.sha256(data).hexdigest())

    def test_cli_build_and_verify_print_paths_and_hash(self):
        with mock.patch.object(RELEASE, "REPOSITORY", self.repo), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(RELEASE.main(["--output", str(self.output)]), 0)
        self.assertIn("SHA256:", output.getvalue())
        archive = self.output / "research-discovery-workflow-1.1.0.zip"
        with contextlib.redirect_stdout(io.StringIO()) as verified:
            self.assertEqual(RELEASE.main(["--verify", str(archive)]), 0)
        self.assertIn("Verified:", verified.getvalue())

    def test_existing_outputs_including_broken_link_are_preserved(self):
        for kind in ("directory", "file", "broken-link"):
            with self.subTest(kind=kind):
                output = self.base / kind
                if kind == "directory":
                    output.mkdir()
                    (output / "sentinel.txt").write_bytes(b"Preserve fixture.\n")
                elif kind == "file":
                    output.write_bytes(b"Preserve fixture.\n")
                else:
                    output.symlink_to(self.base / "missing-fictional-output")
                before = snapshot(self.base)
                with self.assertRaises(FileExistsError):
                    self.build(output)
                self.assertEqual(snapshot(self.base), before)

    def test_missing_output_parent_is_not_created(self):
        parent = self.base / "missing-parent"
        with self.assertRaises(ValueError):
            self.build(parent / "release")
        self.assertFalse(parent.exists())

    def test_modified_staged_and_untracked_nonignored_files_are_rejected(self):
        self.write("README.md", b"Fictional uncommitted modification.\n")
        self.rejected_build()
        self.git("add", "README.md")
        self.rejected_build()
        self.commit()
        self.write("fictional-untracked.txt", b"Fictional nonignored fixture.\n")
        self.rejected_build()

    def test_tracked_nonpublic_files_and_caches_are_rejected(self):
        for name in ("FICTIONAL-NONPUBLIC.txt", "docs/__pycache__/fictional.pyc"):
            with self.subTest(name=name):
                self.write(name, b"Fictional excluded fixture.\n")
                self.git("add", "-f", name)
                self.commit()
                self.rejected_build()
                self.git("rm", "--", name)
                self.commit()

    def test_tracked_symlink_is_rejected(self):
        linked = self.repo / "docs" / "linked-fictional.txt"
        linked.symlink_to("FICTIONAL.md")
        self.commit()
        self.rejected_build()

    def test_missing_required_file_and_invalid_version_are_rejected(self):
        self.git("rm", "LICENSE")
        self.commit()
        self.rejected_build()
        self.write("LICENSE", self.files["LICENSE"])
        self.write("VERSION", b"1.1.0-beta\n")
        self.commit()
        self.rejected_build()

    def test_source_must_be_its_own_repository_root(self):
        with self.assertRaises(ValueError):
            RELEASE.build_release(self.output, repository=self.repo / "docs")
        self.assertFalse(self.output.exists())

    def rewrite_archive(self, archive_path, transform):
        with zipfile.ZipFile(archive_path) as archive:
            entries = [(entry, archive.read(entry)) for entry in archive.infolist()]
        replacement = archive_path.with_suffix(".fixture-tmp")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(replacement, "w") as archive:
                for entry, data in transform(entries):
                    archive.writestr(entry, data)
        replacement.replace(archive_path)
        self.refresh_checksums(archive_path)

    def refresh_checksums(self, archive_path):
        manifest = archive_path.parent / "manifest.json"
        (archive_path.parent / "SHA256SUMS").write_text(
            f"{hashlib.sha256(archive_path.read_bytes()).hexdigest()}  {archive_path.name}\n"
            f"{hashlib.sha256(manifest.read_bytes()).hexdigest()}  manifest.json\n",
            encoding="utf-8",
        )

    def test_corrupted_zip_is_detected_by_sibling_checksum(self):
        archive = self.build()
        archive.write_bytes(archive.read_bytes() + b"Explicitly fictional corruption.")
        with self.assertRaisesRegex(ValueError, "Archive SHA256"):
            RELEASE.verify_release(archive)

    def test_modified_file_is_detected_even_if_archive_checksum_is_updated(self):
        archive = self.build()
        self.rewrite_archive(archive, lambda entries: [
            (entry, b"Fictional altered payload.\n" if entry.filename.endswith("/README.md") else data)
            for entry, data in entries
        ])
        with self.assertRaisesRegex(ValueError, "file SHA256"):
            RELEASE.verify_release(archive)

    def test_duplicate_extra_traversal_and_symlink_entries_are_rejected(self):
        archive = self.build()
        original = archive.read_bytes()
        for kind in ("duplicate", "extra", "traversal", "symlink", "missing"):
            with self.subTest(kind=kind):
                archive.write_bytes(original)

                def transform(entries):
                    if kind == "duplicate":
                        return entries + [entries[0]]
                    if kind == "missing":
                        return entries[1:]
                    if kind == "symlink":
                        entries[0][0].external_attr = (stat.S_IFLNK | 0o777) << 16
                        return entries
                    name = "../fictional-escape.txt" if kind == "traversal" else "research-discovery-workflow-1.1.0/docs/extra-fictional.txt"
                    entry = zipfile.ZipInfo(name)
                    entry.external_attr = (stat.S_IFREG | 0o644) << 16
                    return entries + [(entry, b"Explicitly fictional extra payload.\n")]

                self.rewrite_archive(archive, transform)
                with self.assertRaises(ValueError):
                    RELEASE.verify_release(archive)
        self.assertFalse((self.base / "fictional-escape.txt").exists())

    def test_sibling_manifest_mismatch_and_invalid_checksum_list_are_rejected(self):
        archive = self.build()
        manifest_path = archive.parent / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["commit"] = "0" * 40
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.refresh_checksums(archive)
        with self.assertRaisesRegex(ValueError, "manifests differ"):
            RELEASE.verify_release(archive)
        checksums = archive.parent / "SHA256SUMS"
        checksums.write_text(checksums.read_text() * 2, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            RELEASE.verify_release(archive)


if __name__ == "__main__":
    unittest.main()
