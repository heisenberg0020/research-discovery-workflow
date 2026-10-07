#!/usr/bin/env python3
"""Copy an explicitly trusted, reviewed local skill package; start no research."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys


REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_NAME = "research-discovery-workflow"
SKILL_DIR = REPOSITORY / "skills" / SKILL_NAME
LICENSE_PATH = REPOSITORY / "LICENSE"
PACKAGE_DIRS = ("references", "scripts", "agents")
CACHE_NAMES = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache",
    ".git", ".DS_Store", ".venv",
}


def _ignored(name: str) -> bool:
    return name in CACHE_NAMES or name.endswith((".pyc", ".pyo"))


def _copy_ignore(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if _ignored(name)]


def _regular_file(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Expected a regular, non-link file: {path}")


def _validate_source(skill: Path, license_path: Path) -> None:
    if not stat.S_ISDIR(skill.lstat().st_mode):
        raise ValueError(f"Expected a non-link skill directory: {skill}")
    _regular_file(skill / "SKILL.md")
    _regular_file(license_path)
    for name in PACKAGE_DIRS:
        directory = skill / name
        if not stat.S_ISDIR(directory.lstat().st_mode):
            raise ValueError(f"Expected a non-link payload directory: {directory}")
        for current, directories, files in os.walk(directory, followlinks=False):
            directories[:] = sorted(entry for entry in directories if not _ignored(entry))
            for entry in directories:
                path = Path(current) / entry
                if not stat.S_ISDIR(path.lstat().st_mode):
                    raise ValueError(f"Unsupported payload directory: {path}")
            for entry in files:
                if not _ignored(entry):
                    _regular_file(Path(current) / entry)


def default_destination() -> Path:
    """Use Codex's documented user-skill root; custom roots stay explicit."""
    return Path.home() / ".agents" / "skills"


def install_skill(destination: Path | None = None, *, dry_run: bool = False) -> Path:
    """Validate, then copy a new skill directory without replacing any target."""
    destination = Path(default_destination() if destination is None else destination)
    destination = destination.expanduser().absolute()
    target = destination / SKILL_NAME
    if os.path.lexists(target):
        raise FileExistsError(f"Refusing to overwrite an existing target: {target}")
    ancestor = destination
    while not os.path.lexists(ancestor):
        ancestor = ancestor.parent
    if not ancestor.is_dir():
        raise ValueError(f"Destination and its existing ancestors must be directories: {ancestor}")
    destination = destination.resolve()
    target = destination / SKILL_NAME
    if os.path.lexists(target):
        raise FileExistsError(f"Refusing to overwrite an existing target: {target}")

    skill = Path(SKILL_DIR).absolute()
    license_path = Path(LICENSE_PATH).absolute()
    _validate_source(skill, license_path)
    skill = skill.resolve()
    if destination == skill or skill in destination.parents:
        raise ValueError("Destination must be outside the source skill directory")
    if dry_run:
        return target

    destination.mkdir(parents=True, exist_ok=True)
    # Exclusive mkdir is the overwrite boundary. A later I/O failure leaves the
    # newly created target for inspection; existing user files are never removed.
    target.mkdir()
    shutil.copy2(skill / "SKILL.md", target / "SKILL.md")
    shutil.copy2(license_path, target / "LICENSE")
    for name in PACKAGE_DIRS:
        shutil.copytree(skill / name, target / name, ignore=_copy_ignore)
    return target


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install only an explicitly trusted, reviewed local package. "
            "This copies files and does not start research or model calls."
        ),
        allow_abbrev=False,
    )
    parser.add_argument(
        "--dest", type=Path,
        help="Skills directory (default: ~/.agents/skills; use --dest for custom or legacy locations)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and report; write nothing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        target = install_skill(args.dest, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 2
    if args.dry_run:
        print(f"Dry run: would install to {target}")
        print("Validation passed; no files or directories were written.")
    else:
        print(f"Installed: {target}")
        print("Skill instructions were copied unchanged; the repository LICENSE was included.")
    print("No research, experiments, model calls, or global configuration changes were started.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
