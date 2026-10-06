"""Consumer command-path tests, not client loading or scientific validation.

Copy the public package to a temporary Git fixture, create release assets, then
exercise the ZIP-only path without a source checkout or a global installation.
No model, search service, or scientific experiment is called.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_NAME = "research-discovery-workflow"
PUBLIC_ROOTS = (
    "README.md", "README_EN.md", "AGENTS.md", "CONTRIBUTING.md", "LICENSE",
    "CHANGELOG.md", "VERSION", ".gitignore", "docs", "scripts", "examples",
    "tests", "skills", ".github",
)


def run(*arguments, cwd):
    return subprocess.run(
        list(arguments), cwd=cwd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, check=False,
    )


class ReleaseDownloadOnboardingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="public-onboarding-fixture-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name).resolve()
        cls.source = cls.root / "source"
        cls.source.mkdir()
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")
        for name in PUBLIC_ROOTS:
            origin = REPOSITORY / name
            if origin.is_dir():
                shutil.copytree(origin, cls.source / name, ignore=ignore)
            else:
                shutil.copyfile(origin, cls.source / name)
        commands = (
            ("git", "init", "-q"),
            ("git", "add", "--all"),
            ("git", "-c", "user.name=Public Package Fixture",
             "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
             "commit", "-qm", "Temporary onboarding fixture, not scientific results"),
            (sys.executable, "scripts/build_release.py", "--output", str(cls.root / "download")),
        )
        for command in commands:
            result = run(*command, cwd=cls.source)
            if result.returncode:
                raise AssertionError(result.stdout + result.stderr)
        cls.download = cls.root / "download"
        cls.version = (cls.source / "VERSION").read_text(encoding="utf-8").strip()
        cls.archive_name = f"{SKILL_NAME}-{cls.version}.zip"
        cls.archive = cls.download / cls.archive_name

    def test_python_version_selection_command(self):
        check = (
            'import sys; print(sys.executable, sys.version); '
            'raise SystemExit(0 if sys.version_info >= (3, 10) '
            'else "Python 3.10+ required")'
        )
        result = run(
            sys.executable, "-c", check,
            cwd=self.root,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(sys.executable, result.stdout)
        # Simulate the unsupported version value under optimization. An assert
        # would disappear under -O and incorrectly allow this command to pass.
        unsupported = run(
            sys.executable, "-O", "-c",
            'import sys; sys.version_info = (3, 9); ' + check,
            cwd=self.root,
        )
        self.assertNotEqual(unsupported.returncode, 0)
        self.assertIn("Python 3.10+ required", unsupported.stderr)

    def test_checksums_before_extraction_with_platform_command(self):
        # This test needs only the three downloaded assets, not the verifier.
        checker = shutil.which("shasum") or shutil.which("sha256sum")
        if checker is None:
            self.skipTest("No documented POSIX checksum command available on this host")
        flags = ("-a", "256", "-c", "SHA256SUMS") if Path(checker).name == "shasum" else ("-c", "SHA256SUMS")
        result = run(checker, *flags, cwd=self.download)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(self.archive_name + ": OK", result.stdout)
        self.assertIn("manifest.json: OK", result.stdout)
        self.assertEqual(
            set(path.name for path in self.download.iterdir()),
            {self.archive_name, "manifest.json", "SHA256SUMS"},
        )

    def test_standard_library_asset_hashes_match_published_format(self):
        checksums = (self.download / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(checksums), 2)
        for line in checksums:
            expected, filename = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((self.download / filename).read_bytes()).hexdigest(), expected)
        manifest = json.loads((self.download / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], self.version)

    def test_extracted_package_verifies_installs_and_prepares_without_git(self):
        extract_root = self.root / "extracted"
        extract_root.mkdir()
        # This is a trusted locally built regular-file-only fixture, not an
        # arbitrary downloaded archive. Test methods need no execution order.
        with zipfile.ZipFile(self.archive) as archive:
            archive.extractall(extract_root)
        package = extract_root / f"{SKILL_NAME}-{self.version}"
        self.assertFalse((package / ".git").exists())
        verify = run(sys.executable, "scripts/build_release.py", "--verify", str(self.archive), cwd=package)
        self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
        self.assertIn("Verified:", verify.stdout)
        destination = self.root / "local-skills"
        preview = run(sys.executable, "scripts/install.py", "--dest", str(destination), "--dry-run", cwd=package)
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertFalse(destination.exists())
        install = run(sys.executable, "scripts/install.py", "--dest", str(destination), cwd=package)
        self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
        installed = destination / SKILL_NAME
        for source in (package / "skills" / SKILL_NAME).rglob("*"):
            if source.is_file():
                self.assertEqual((installed / source.relative_to(package / "skills" / SKILL_NAME)).read_bytes(), source.read_bytes())
        self.assertEqual((installed / "LICENSE").read_bytes(), (package / "LICENSE").read_bytes())
        runs = self.root / "runs"
        runs.mkdir()
        brief = package / "examples/neutral-brief.en.md"
        prepared = run(
            sys.executable, str(installed / "scripts/prepare_run.py"),
            "--root", str(runs / "pass-1"), "--brief", str(brief), "--pass-number", "1", cwd=package,
        )
        self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
        index = (runs / "pass-1/RUN.md").read_text(encoding="utf-8")
        self.assertIn("prepared-not-started", index)
        for relative in ("output/q5-original", "output/q5-repaired", "output/final", "tmp"):
            self.assertFalse(any((runs / "pass-1" / relative).iterdir()))


if __name__ == "__main__":
    unittest.main()
