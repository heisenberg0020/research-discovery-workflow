#!/usr/bin/env python3
"""Prepare an empty research run; do not start research or isolate the host."""

from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
import shutil
import stat
import sys


SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_NAME = "research-discovery-workflow"
PACKAGE_DIRS = ("references", "scripts", "agents")
IGNORED_NAMES = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache",
    ".git", ".DS_Store",
}


AGENTS_TEXT = """# Prepared research run

This directory is prepared, not started. Read BRIEF.md and the local skill at
.agents/skills/research-discovery-workflow/SKILL.md before doing research.
The pass number is a label, not permission to continue another pass or read its
results. Use the explicitly supplied neutral brief as the common input.

Keep research writing in output/ and scratch work in tmp/. This is a working
convention, not an enforced filesystem or network boundary.

Save domain-down Q1-T and method-up Q1-U first-pass judgments separately before
Q1-S comparison. Preserve their original judgments and distinguish common
sources from independent evidence. Deliver concrete relationships or operations,
not only topic names; distinguish proposal formation from scientific validation.

At Q5, preserve the original independent snapshot in output/q5-original/.
Q5-R is mandatory: conduct a paper retrospective, repair the mechanism and
sharpen the research core where warranted, and save the revised independent
version in output/q5-repaired/. Keep the original snapshot. Complete Q5-R before
reading any prior research material. This preparation includes no prior results.

Q6 is conditional on explicitly scoped, authorized prior material. If there is
no prior material, record Q6 as skipped/not-applicable and continue to final
delivery in output/final/. If reconciliation is explicitly requested but its
material is missing, record the specific pending handoff. Do not search another
run or external research directory to fill it. Keep any later reconciliation
distinct from the independent versions.

Before the comprehensive final report, complete Q7-A per developed direction:
the nearest answer's mechanism and conditions; two competing accounts and
distinguishing observations; qualified real resources, splits and estimates;
and what each result changes. Do not silently replace the research object with
an easier resource or automatically resume an old experiment. Then deliver
Q7-B's substantive insight report with actual plan readiness stated.

These directories may contain a few coherent documents with stage sections;
they do not require a file for every checklist item. Report substantive insights
and concrete proposals in the final conversation as well as linking documents.

Preparation grants no experimental execution or paid-service authority. Propose
verification as needed; execute only within the user's authorized actions and
resources. Do not automatically run experiments or start another exploration.

This directory is not a sandbox or a fresh conversation. The helper does not
disable memory, enforce host isolation, or create a chat. Use an appropriate
fresh context separately when the task calls for one, and describe actual
exposure accurately.
"""


def _ignored(name: str) -> bool:
    return name in IGNORED_NAMES or any(
        fnmatch.fnmatchcase(name, pattern) for pattern in ("*.pyc", "*.pyo")
    )


def _copy_ignore(_directory: str, names: list[str]) -> list[str]:
    return [name for name in names if _ignored(name)]


def _regular_file(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Expected a regular, non-symbolic-link file: {path}")


def _validate_package(skill_dir: Path) -> None:
    _regular_file(skill_dir / "SKILL.md")
    for name in PACKAGE_DIRS:
        directory = skill_dir / name
        if not stat.S_ISDIR(directory.lstat().st_mode):
            raise ValueError(f"Expected a non-symbolic-link skill directory: {directory}")
        for current, directories, files in os.walk(directory, followlinks=False):
            directories[:] = [entry for entry in directories if not _ignored(entry)]
            for entry in directories:
                path = Path(current) / entry
                if not stat.S_ISDIR(path.lstat().st_mode):
                    raise ValueError(f"Unsupported skill directory: {path}")
            for entry in files:
                if not _ignored(entry):
                    _regular_file(Path(current) / entry)


def prepare_run(root: Path, brief: Path, pass_number: int) -> Path:
    """Create a new blank run from one UTF-8 brief and this skill package."""
    if type(pass_number) is not int or pass_number not in (1, 2):
        raise ValueError("pass_number must be 1 or 2")
    root = Path(root).expanduser().absolute()
    if os.path.lexists(root):
        raise FileExistsError(f"Refusing to overwrite an existing path: {root}")
    root = root.resolve()
    if os.path.lexists(root):
        raise FileExistsError(f"Refusing to overwrite an existing path: {root}")
    skill_dir = Path(SKILL_DIR).absolute()
    if not stat.S_ISDIR(skill_dir.lstat().st_mode):
        raise ValueError(f"Expected a non-symbolic-link skill root: {skill_dir}")
    skill_dir = skill_dir.resolve()
    if root == skill_dir or skill_dir in root.parents:
        raise ValueError("The run root must be outside the source skill package")
    if not root.parent.is_dir():
        raise ValueError("The run root's parent directory must already exist")

    brief = Path(brief).expanduser().absolute()
    _regular_file(brief)
    brief_bytes = brief.read_bytes()
    brief_bytes.decode("utf-8")
    _validate_package(skill_dir)

    # Exclusive mkdir is the non-overwrite boundary; validate before creating it.
    # An unexpected later I/O failure leaves this new directory for inspection.
    root.mkdir()
    (root / "BRIEF.md").write_bytes(brief_bytes)
    target_skill = root / ".agents" / "skills" / SKILL_NAME
    target_skill.mkdir(parents=True)
    shutil.copy2(skill_dir / "SKILL.md", target_skill / "SKILL.md")
    for name in PACKAGE_DIRS:
        shutil.copytree(skill_dir / name, target_skill / name, ignore=_copy_ignore)
    for name in ("q5-original", "q5-repaired", "final"):
        (root / "output" / name).mkdir(parents=True)
    (root / "tmp").mkdir()
    (root / "AGENTS.md").write_text(AGENTS_TEXT, encoding="utf-8")
    (root / "RUN.md").write_text(
        "# Run preparation\n\n"
        "status: prepared-not-started\n"
        f"pass-number: {pass_number}\n"
        "current-stage: not-started\n"
        "input: BRIEF.md\n"
        "skill: .agents/skills/research-discovery-workflow/SKILL.md\n\n"
        "Q5 original snapshot: output/q5-original/\n"
        "Q5-R: mandatory paper retrospective and repair before prior material; "
        "save to output/q5-repaired/, preserve the original.\n"
        "Q6: conditional; skip as not-applicable when no prior material is supplied.\n"
        "Final delivery: output/final/; stage sections in coherent files are enough.\n\n"
        "No research, retrieval, experiments, or model calls have started. "
        "No earlier pass directory was read or copied. "
        "This is not a sandbox or a new chat; host access and global memory "
        "settings are unchanged.\n",
        encoding="utf-8",
    )
    return root


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a new blank run; no research or host isolation is started.",
        allow_abbrev=False,
    )
    parser.add_argument("--root", required=True, type=Path, help="New directory; must not exist")
    parser.add_argument("--brief", required=True, type=Path, help="One regular, non-link UTF-8 brief")
    parser.add_argument("--pass-number", required=True, type=int, choices=(1, 2))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = prepare_run(args.root, args.brief, args.pass_number)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Preparation failed: {error}", file=sys.stderr)
        return 2
    print(f"Prepared: {root}")
    print(f"Pass {args.pass_number}; status: prepared-not-started. Research has NOT started.")
    print("The host is NOT isolated: no sandbox, no new chat, and no memory-setting changes.")
    print("Only the supplied brief and this skill package were copied; no earlier-pass directory was loaded.")
    print("The caller is responsible for supplying a neutral brief; this helper does not assess its content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
