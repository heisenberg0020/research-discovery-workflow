#!/usr/bin/env python3
"""Check public package structure; this proves neither isolation nor research quality.

Only named root documents and the docs/examples/skills trees are inspected.
Network links, research runs, caches, distribution output, and neighbors are not
scanned. The workflow manifest checks unchanged bytes, not scientific correctness.
SVG checks concern XML and descriptive structure, not content safety.
"""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT_DOCUMENTS = (
    "README.md", "README_EN.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md",
)
PUBLIC_TREES = ("docs", "examples", "skills")
SKILL_PATH = "skills/research-discovery-workflow"
FROZEN_DOCUMENTS = {"docs/STARTER_PROMPTS.zh-CN.md", "docs/QUICKSTART.en.md"}
IGNORED_DIRECTORIES = {
    ".git", ".venv", "venv", "env", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".cache", "cache", "caches", "runs",
    "dist", "build", "node_modules",
}
SEMVER = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
MARKDOWN_LINK = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)"
    r"(?:\s+['\"][^\n]*?['\"])?\s*\)"
)
REFERENCE_LINK = re.compile(
    r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE
)
SVG_NAMESPACE = "http://www.w3.org/2000/svg"


def _files_in_tree(directory: Path):
    """Walk this tree only, excluding generated directories and following no links."""
    if not directory.is_dir() or directory.is_symlink():
        return
    for current, directories, names in os.walk(directory, followlinks=False):
        for name in sorted(directories):
            path = Path(current) / name
            if name not in IGNORED_DIRECTORIES and path.is_symlink():
                yield path
        directories[:] = sorted(
            name for name in directories
            if name not in IGNORED_DIRECTORIES
            and not (Path(current) / name).is_symlink()
        )
        for name in sorted(names):
            if name != ".DS_Store" and not name.endswith((".pyc", ".pyo")):
                yield Path(current) / name


def _read_text(path: Path, root: Path, issues: list[str]) -> str | None:
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        issues.append(f"{relative}: symbolic link is not inspected; use a package file")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        issues.append(f"{relative}: cannot read UTF-8 file ({exc})")
        return None


def _without_fences(text: str) -> str:
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return "\n".join(lines)


class _HTMLTargets(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.targets: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attributes):
        for name, value in attributes:
            if name.lower() in {"href", "src"} and value:
                self.targets.append((self.getpos()[0], value))

    handle_startendtag = handle_starttag


def _document_targets(text: str) -> list[tuple[int, str]]:
    visible = _without_fences(text)
    targets = []
    for expression in (MARKDOWN_LINK, REFERENCE_LINK):
        for match in expression.finditer(visible):
            targets.append((visible.count("\n", 0, match.start()) + 1,
                            match.group(1).strip("<>")))
    parser = _HTMLTargets()
    parser.feed(visible)
    return targets + parser.targets


def _local_target(source: Path, link: str, root: Path) -> Path | None:
    parsed = urlsplit(link.strip())
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = Path(unquote(parsed.path))
    target = (source.parent / path).resolve()
    if path.is_absolute() or not target.is_relative_to(root):
        raise ValueError("local target leaves this repository")
    return target


def _check_skill(root: Path, issues: list[str]) -> None:
    skill = root / SKILL_PATH
    entry = skill / "SKILL.md"
    text = _read_text(entry, root, issues)
    for relative in ("agents/openai.yaml", "scripts/prepare_run.py"):
        if not (skill / relative).is_file():
            issues.append(f"{SKILL_PATH}/{relative}: required skill resource is missing")
    if text is None:
        return
    lines = text.splitlines()
    if len(lines) >= 500:
        issues.append(f"{SKILL_PATH}/SKILL.md: entrypoint must stay below 500 lines")
    if re.search(r"\[\s*TODO\b|^\s*(?:TODO|TBD)\s*[:：]", text,
                 re.IGNORECASE | re.MULTILINE):
        issues.append(f"{SKILL_PATH}/SKILL.md: unfinished scaffold marker")
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        issues.append(f"{SKILL_PATH}/SKILL.md: missing or unclosed YAML frontmatter")
    else:
        header = "\n".join(lines[1:lines.index("---", 1)])
        for field in ("name", "description"):
            match = re.search(rf"^{field}:\s*(.+)$", header, re.MULTILINE)
            if not match or not match.group(1).strip("\"' "):
                issues.append(f"{SKILL_PATH}/SKILL.md: frontmatter requires {field}")
        name = re.search(r"^name:\s*([^\n]+)$", header, re.MULTILINE)
        if name and name.group(1).strip("\"' ") != skill.name:
            issues.append(f"{SKILL_PATH}/SKILL.md: frontmatter name differs from directory")
    references = sorted((skill / "references").glob("*.md"))
    if not references:
        issues.append(f"{SKILL_PATH}/references: required reference documents are missing")
    direct_targets = set()
    for _, link in _document_targets(text):
        try:
            target = _local_target(entry, link, root)
        except ValueError:
            continue
        if target is not None:
            direct_targets.add(target)
    for reference in references:
        if reference.resolve() not in direct_targets:
            issues.append(f"{reference.relative_to(root).as_posix()}: not directly indexed by SKILL.md")


def _check_freeze(root: Path, issues: list[str]) -> None:
    manifest_path = root / "docs/workflow-freeze.json"
    text = _read_text(manifest_path, root, issues)
    if text is None:
        return
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        issues.append(f"docs/workflow-freeze.json: invalid JSON ({exc})")
        return
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), dict):
        issues.append("docs/workflow-freeze.json: expected a files-to-SHA256 mapping")
        return
    if not manifest.get("baseline_revision") or not re.fullmatch(
            r"[0-9a-f]{40}", str(manifest.get("baseline_commit", ""))):
        issues.append("docs/workflow-freeze.json: baseline revision and full commit are required")
    expected = {}
    for name, digest in manifest["files"].items():
        path = PurePosixPath(name) if isinstance(name, str) else None
        if (path is None or path.is_absolute() or ".." in path.parts
                or str(path) != name
                or not (name.startswith(SKILL_PATH + "/") or name in FROZEN_DOCUMENTS)):
            issues.append(f"docs/workflow-freeze.json: invalid frozen path {name!r}")
            continue
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            issues.append(f"docs/workflow-freeze.json: invalid SHA256 for {name}")
            continue
        expected[name] = digest
    actual = {path.relative_to(root).as_posix()
              for path in _files_in_tree(root / SKILL_PATH)}
    frozen_skill = {name for name in expected if name.startswith(SKILL_PATH + "/")}
    for name in sorted(actual - frozen_skill):
        issues.append(f"{name}: added file is outside the frozen workflow inventory")
    for name in sorted(frozen_skill - actual):
        issues.append(f"{name}: frozen workflow file is missing")
    for name in sorted(FROZEN_DOCUMENTS - expected.keys()):
        issues.append(f"docs/workflow-freeze.json: missing frozen document {name}")
    for name, digest in sorted(expected.items()):
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            issues.append(f"{name}: frozen file must be a local regular package file")
            continue
        try:
            current = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            issues.append(f"{name}: cannot read frozen file ({exc})")
            continue
        if current != digest:
            issues.append(f"{name}: bytes differ from the frozen workflow baseline")


def check_repository(root: Path) -> list[str]:
    root = Path(root).resolve()
    if not root.is_dir():
        return [f"{root}: repository directory does not exist"]
    issues: list[str] = []
    for name in (*ROOT_DOCUMENTS, "LICENSE", "VERSION"):
        if not (root / name).is_file():
            issues.append(f"{name}: required public file is missing")
    version = _read_text(root / "VERSION", root, issues)
    if version is not None:
        version = version.strip()
        if not SEMVER.fullmatch(version):
            issues.append("VERSION: expected a numeric MAJOR.MINOR.PATCH version")
        changelog = _read_text(root / "CHANGELOG.md", root, issues)
        if changelog is not None:
            heading = re.search(r"^##\s+\[?v?([0-9]+\.[0-9]+\.[0-9]+)\]?\b",
                                changelog, re.MULTILINE)
            if heading is None or heading.group(1) != version:
                issues.append("CHANGELOG.md: current version heading must match VERSION")
    documents = [root / name for name in ROOT_DOCUMENTS if (root / name).is_file()]
    for tree in PUBLIC_TREES:
        documents.extend(path for path in _files_in_tree(root / tree)
                         if path.suffix.lower() == ".md")
    for document in sorted(set(documents)):
        text = _read_text(document, root, issues)
        if text is None:
            continue
        for line, link in _document_targets(text):
            location = f"{document.relative_to(root).as_posix()}:{line}"
            try:
                target = _local_target(document, link, root)
            except ValueError as exc:
                issues.append(f"{location}: {exc}: {link}")
                continue
            if target is not None and not target.exists():
                issues.append(f"{location}: missing local link or asset: {link}")
    _check_skill(root, issues)
    _check_freeze(root, issues)
    for svg in _files_in_tree(root / "docs/images"):
        if svg.suffix.lower() != ".svg":
            continue
        relative = svg.relative_to(root).as_posix()
        if svg.is_symlink():
            issues.append(f"{relative}: symbolic SVG is not inspected")
            continue
        try:
            element = ET.parse(svg).getroot()
        except (ET.ParseError, OSError) as exc:
            issues.append(f"{relative}: invalid SVG XML ({exc})")
            continue
        if element.tag != f"{{{SVG_NAMESPACE}}}svg":
            issues.append(f"{relative}: root must be an SVG element in the SVG namespace")
        try:
            bounds = [float(value) for value in re.split(r"[\s,]+", element.get("viewBox", "").strip())]
            valid_bounds = (len(bounds) == 4 and all(math.isfinite(value) for value in bounds)
                            and bounds[2] > 0 and bounds[3] > 0)
        except ValueError:
            valid_bounds = False
        if not valid_bounds:
            issues.append(f"{relative}: requires a four-number viewBox with positive dimensions")
        for tag in ("title", "desc"):
            child = element.find(f"{{{SVG_NAMESPACE}}}{tag}")
            if child is None or not "".join(child.itertext()).strip():
                issues.append(f"{relative}: requires a nonempty {tag} for its description")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="package root; defaults to this script's repository")
    args = parser.parse_args(argv)
    issues = check_repository(args.root)
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    print("Public package links, resources, version, SVG structure, and workflow freeze passed.")
    print("These checks do not establish client isolation or research quality.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
