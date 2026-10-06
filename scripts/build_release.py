#!/usr/bin/env python3
"""Build and check a reproducible local release from a clean, public Git HEAD."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile


REPOSITORY = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "research-discovery-workflow"
ROOT_FILES = {
    "README.md", "README_EN.md", "AGENTS.md", "CONTRIBUTING.md", "LICENSE",
    "CHANGELOG.md", "VERSION", ".gitignore",
}
PUBLIC_DIRECTORIES = {"docs", "scripts", "examples", "tests", "skills", ".github"}
REQUIRED_FILES = ROOT_FILES | {
    "scripts/install.py", "scripts/build_release.py",
    "skills/research-discovery-workflow/SKILL.md",
    "skills/research-discovery-workflow/agents/openai.yaml",
    "skills/research-discovery-workflow/scripts/prepare_run.py",
}
CACHE_NAMES = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache",
    ".git", ".DS_Store", ".venv",
}
VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
HASH_PATTERN = re.compile(r"[0-9a-f]{64}")
COMMIT_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _git(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments], cwd=repository, check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"Local Git command failed: {message}")
    return result.stdout


def _safe_path(name: str) -> None:
    path = PurePosixPath(name)
    if (
        not name or path.is_absolute() or "\\" in name
        or any(character in name for character in ("\n", "\r", "\x00"))
        or any(part in ("", ".", "..") for part in name.split("/"))
        or ":" in path.parts[0]
    ):
        raise ValueError(f"Unsupported package path: {name!r}")


def _public_path(name: str) -> None:
    _safe_path(name)
    parts = PurePosixPath(name).parts
    if name not in ROOT_FILES and (len(parts) < 2 or parts[0] not in PUBLIC_DIRECTORIES):
        raise ValueError(f"Tracked file is outside the public package allowlist: {name}")
    if any(part in CACHE_NAMES for part in parts) or name.endswith((".pyc", ".pyo")):
        raise ValueError(f"Caches must not be tracked in a release: {name}")


def _validate_inventory(names: set[str]) -> None:
    for name in sorted(names):
        _public_path(name)
    missing = REQUIRED_FILES - names
    if missing:
        raise ValueError("Required package files are missing: " + ", ".join(sorted(missing)))
    reference_prefix = "skills/research-discovery-workflow/references/"
    if not any(name.startswith(reference_prefix) for name in names):
        raise ValueError("At least one skill reference file is required")


def _version(data: bytes) -> str:
    version = data.decode("utf-8").strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("VERSION must contain a three-part numeric version, such as 1.1.0")
    return version


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _new_output(output: Path) -> Path:
    output = Path(output).expanduser().absolute()
    if os.path.lexists(output):
        raise FileExistsError(f"Refusing to overwrite an existing output path: {output}")
    output = output.resolve()
    if os.path.lexists(output):
        raise FileExistsError(f"Refusing to overwrite an existing output path: {output}")
    if not output.parent.is_dir():
        raise ValueError("The output parent directory must already exist")
    return output


def _clean_head(repository: Path) -> str:
    if _git(repository, "status", "--porcelain=v1", "--untracked-files=all"):
        raise ValueError("Release builds require a clean tree, including nonignored untracked files")
    commit = _git(repository, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    if not COMMIT_PATTERN.fullmatch(commit):
        raise ValueError("Unexpected Git commit identifier")
    return commit


def build_release(output: Path, *, repository: Path | None = None) -> Path:
    """Build only committed public bytes; refuse preexisting output paths."""
    output = _new_output(output)
    repository = Path(REPOSITORY if repository is None else repository).resolve()
    git_root = Path(_git(repository, "rev-parse", "--show-toplevel").decode("utf-8").strip())
    if git_root.resolve() != repository:
        raise ValueError("The source must be the root of its own Git repository")
    commit = _clean_head(repository)
    files: dict[str, bytes] = {}
    modes: dict[str, int] = {}
    tree = _git(repository, "ls-tree", "-r", "-z", "--full-tree", commit)
    for record in tree.split(b"\x00"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        name = encoded_path.decode("utf-8")
        _public_path(name)
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError(f"Only regular tracked files may be released: {name}")
        files[name] = _git(repository, "cat-file", "blob", object_id)
        modes[name] = int(mode, 8)
    _validate_inventory(set(files))
    version = _version(files["VERSION"])
    if _clean_head(repository) != commit:
        raise ValueError("Git HEAD changed while reading the release source; retry from a clean tree")

    manifest = {
        "format_version": 1,
        "version": version,
        "commit": commit,
        "files": {name: _hash(files[name]) for name in sorted(files)},
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    release_name = f"{PACKAGE_NAME}-{version}"
    archive_path = output / f"{release_name}.zip"

    # The output directory is created exclusively, only after all source checks.
    # Unexpected I/O errors leave this newly created directory for inspection.
    output.mkdir()
    archive_files = {**files, "manifest.json": manifest_bytes}
    with zipfile.ZipFile(archive_path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(archive_files):
            entry = zipfile.ZipInfo(f"{release_name}/{name}", FIXED_TIMESTAMP)
            entry.create_system = 3
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = modes.get(name, 0o100644) << 16
            archive.writestr(entry, archive_files[name], compresslevel=9)
    (output / "manifest.json").write_bytes(manifest_bytes)
    (output / "SHA256SUMS").write_text(
        f"{_file_hash(archive_path)}  {archive_path.name}\n"
        f"{_hash(manifest_bytes)}  manifest.json\n",
        encoding="utf-8",
    )
    return archive_path


def _regular_file(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Expected a regular, non-link release file: {path}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate manifest key: {key}")
        result[key] = value
    return result


def _read_checksums(path: Path, archive_name: str) -> dict[str, str]:
    _regular_file(path)
    checksums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\]+)", line)
        if not match or match.group(2) in checksums:
            raise ValueError("SHA256SUMS contains an invalid or duplicate entry")
        checksums[match.group(2)] = match.group(1)
    if set(checksums) != {archive_name, "manifest.json"}:
        raise ValueError("SHA256SUMS must list exactly this archive and manifest.json")
    return checksums


def verify_release(archive_path: Path) -> dict[str, object]:
    """Check inventory and local checksums without extraction or installation."""
    archive_path = Path(archive_path).expanduser().absolute()
    _regular_file(archive_path)
    checksums = _read_checksums(archive_path.parent / "SHA256SUMS", archive_path.name)
    if _file_hash(archive_path) != checksums[archive_path.name]:
        raise ValueError("Archive SHA256 does not match SHA256SUMS")
    external_manifest = archive_path.parent / "manifest.json"
    _regular_file(external_manifest)
    manifest_bytes = external_manifest.read_bytes()
    if _hash(manifest_bytes) != checksums["manifest.json"]:
        raise ValueError("Manifest SHA256 does not match SHA256SUMS")
    manifest = json.loads(manifest_bytes, object_pairs_hook=_unique_object)
    if not isinstance(manifest, dict) or set(manifest) != {"format_version", "version", "commit", "files"}:
        raise ValueError("Unsupported manifest structure")
    if type(manifest["format_version"]) is not int or manifest["format_version"] != 1:
        raise ValueError("Unsupported manifest format_version")
    version = manifest["version"]
    commit = manifest["commit"]
    files = manifest["files"]
    if not isinstance(version, str) or not VERSION_PATTERN.fullmatch(version):
        raise ValueError("Invalid manifest version")
    if not isinstance(commit, str) or not COMMIT_PATTERN.fullmatch(commit):
        raise ValueError("Invalid manifest commit")
    if not isinstance(files, dict) or not all(
        isinstance(name, str) and isinstance(digest, str) and HASH_PATTERN.fullmatch(digest)
        for name, digest in files.items()
    ):
        raise ValueError("Invalid manifest file hashes")
    _validate_inventory(set(files))
    release_name = f"{PACKAGE_NAME}-{version}"
    if archive_path.name != f"{release_name}.zip":
        raise ValueError("Archive filename must match the manifest version")
    prefix = release_name + "/"
    expected = {prefix + name for name in files} | {prefix + "manifest.json"}
    with zipfile.ZipFile(archive_path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(set(names)):
            raise ValueError("Archive contains duplicate paths")
        for entry in entries:
            _safe_path(entry.filename)
            if entry.is_dir() or stat.S_IFMT(entry.external_attr >> 16) != stat.S_IFREG:
                raise ValueError(f"Archive entry is not a regular file: {entry.filename}")
            if entry.flag_bits & 1:
                raise ValueError("Encrypted archive entries are unsupported")
        if set(names) != expected:
            raise ValueError("Archive inventory does not exactly match the manifest")
        if archive.read(prefix + "manifest.json") != manifest_bytes:
            raise ValueError("Archived and external manifests differ")
        for name, digest in files.items():
            if _hash(archive.read(prefix + name)) != digest:
                raise ValueError(f"Archived file SHA256 does not match the manifest: {name}")
        if _version(archive.read(prefix + "VERSION")) != version:
            raise ValueError("Archived VERSION differs from the manifest version")
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a clean tracked Git HEAD, or verify local release checksums. "
            "Checksums check consistency; they are not signatures or a security review."
        ),
        allow_abbrev=False,
    )
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--output", type=Path, help="New output directory with an existing parent")
    actions.add_argument("--verify", type=Path, metavar="ARCHIVE", help="Check ZIP and sibling release files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.verify is not None:
            manifest = verify_release(args.verify)
            print(f"Verified: {args.verify}")
            print(f"Version: {manifest['version']}; commit: {manifest['commit']}")
        else:
            archive = build_release(args.output)
            print(f"Built: {archive}")
            print(f"Manifest: {archive.parent / 'manifest.json'}")
            print(f"Checksums: {archive.parent / 'SHA256SUMS'}")
            print(f"SHA256: {_file_hash(archive)}")
    except (OSError, UnicodeError, ValueError, zipfile.BadZipFile, RuntimeError) as error:
        print(f"Release operation failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
