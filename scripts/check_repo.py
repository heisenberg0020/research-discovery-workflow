#!/usr/bin/env python3
"""Check public package structure; this proves neither isolation nor research quality.

Only named root documents and the docs/examples/skills trees are inspected.
Network links, research runs, caches, distribution output, and neighbors are not
scanned. The workflow manifest checks unchanged bytes, not scientific correctness.
Published evidence summaries check their declared public-file hashes, without
reading original execution logs. SVG checks concern XML and descriptive structure,
not content safety.
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


def markdown_chunks(value: str):
    """Separate fenced/indented code while retaining text and newline bytes."""
    lines = []
    fence = None
    list_indents = []
    paragraph_open = False
    for line in value.splitlines(keepends=True):
        expanded = line.expandtabs(4)
        indent = len(expanded) - len(expanded.lstrip(" "))
        if fence is None and expanded.strip():
            while list_indents and indent < list_indents[-1]:
                list_indents.pop()
            item = re.match(r"^ *(?:[-+*]|[0-9]{1,9}[.)]) {1,4}(?=\S)", expanded)
            if item:
                list_indents.append(item.end())
        content_indent = list_indents[-1] if list_indents else 0
        # Four columns inside a list can be a rendered continuation paragraph,
        # not code. Interpret code indentation relative to the list content.
        fence_text = expanded[content_indent:] if indent >= content_indent else expanded
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", fence_text)
        if fence is None and marker:
            if lines:
                yield "".join(lines), False
            lines = [line]
            fence = marker.group(1)
            paragraph_open = False
        elif fence is not None:
            lines.append(line)
            if (marker and marker.group(1)[0] == fence[0]
                    and len(marker.group(1)) >= len(fence)
                    and not marker.group(2).strip()):
                yield "".join(lines), True
                lines, fence = [], None
        elif expanded.strip() and indent >= content_indent + 4 and not paragraph_open:
            if lines:
                yield "".join(lines), False
                lines = []
            yield line, True
        else:
            lines.append(line)
            visible = fence_text.lstrip()
            # Indented code cannot interrupt a paragraph. Blank lines, headings,
            # rules and reference definitions end the small helper's paragraph.
            paragraph_open = bool(visible.strip()) and not (
                re.match(r"#{1,6}(?:\s|$)", visible)
                or re.fullmatch(r"(?:=+|-+|(?:\*\s*){3,}|(?:_\s*){3,})\s*", visible)
                or REFERENCE_LINK.match(visible)
            )
    if lines:
        yield "".join(lines), fence is not None


def _code_span_end(value: str, start: int) -> int | None:
    opening = re.match(r"`+", value[start:]).group()
    closing = next((match for match in re.finditer(r"`+", value[start + len(opening):])
                    if len(match.group()) == len(opening)), None)
    return start + len(opening) + closing.end() if closing is not None else None


def inline_link(value: str, start: int) -> tuple[int, str, str] | None:
    """Read a direct link/image with escaped characters and balanced brackets."""
    opening = start + 1 if value[start] == "!" else start
    if value[opening:opening + 1] != "[":
        return None
    index, depth = opening + 1, 1
    while index < len(value) and value[index] != "\n":
        character = value[index]
        if character == "\\":
            index += 2
            continue
        if character == "`":
            end = _code_span_end(value, index)
            if end is not None:
                index = end
                continue
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                break
        index += 1
    if depth or value[index + 1:index + 2] != "(":
        return None
    label = value[opening + 1:index]
    target_start = index + 2
    index = target_start
    while index < len(value) and value[index] in " \t":
        index += 1
    if value[index:index + 1] == "<":
        index += 1
        while index < len(value) and value[index] not in ">\n\r<":
            index += 2 if value[index] == "\\" else 1
        if value[index:index + 1] != ">":
            return None
        index += 1
    else:
        depth = 0
        while index < len(value) and value[index] not in " \t\n\r":
            character = value[index]
            if character == "\\":
                index += 2
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                if not depth:
                    break
                depth -= 1
            elif character in "<>":
                return None
            index += 1
        if depth:
            return None
    destination_end = index
    while index < len(value) and value[index] in " \t":
        index += 1
    # Optional quoted/parenthesized titles are separate from the destination;
    # parentheses inside a quoted title do not change the link's depth.
    if index > destination_end and value[index:index + 1] in ('"', "'", "("):
        delimiter = ")" if value[index] == "(" else value[index]
        index += 1
        while index < len(value) and value[index] not in (delimiter, "\n", "\r"):
            index += 2 if value[index] == "\\" else 1
        if value[index:index + 1] != delimiter:
            return None
        index += 1
        while index < len(value) and value[index] in " \t":
            index += 1
    if value[index:index + 1] != ")":
        return None
    target = value[target_start:index].strip()
    return (index + 1, label, target) if target else None


def _mask_code(value: str) -> str:
    return re.sub(r"[^\n]", " ", value)


def rewrite_prose_links(value: str, replace, *, mask_code: bool = False) -> str:
    """Visit rendered direct links, preserving escapes and backtick code spans.

    The callback receives label, target, original markup and its character offset.
    The optional code mask retains line numbers for document-link inspection.
    This is a small package-text helper, not a complete Markdown renderer.
    """
    result = []
    index = 0
    while index < len(value):
        if value[index] == "\\":
            result.append(value[index:index + 2])
            index += 2
            continue
        if value[index] == "`":
            opening = re.match(r"`+", value[index:]).group()
            end = _code_span_end(value, index)
            if end is not None:
                result.append(_mask_code(value[index:end]) if mask_code else value[index:end])
                index = end
                continue
            result.append(opening)
            index += len(opening)
            continue
        if value[index] in ("[", "!"):
            link = inline_link(value, index)
            if link is not None:
                end, label, target = link
                result.append(replace(label, target, value[index:end], index))
                index = end
                continue
        result.append(value[index])
        index += 1
    return "".join(result)


def _link_destination(value: str) -> str:
    """Discard optional link titles and decode Markdown punctuation escapes."""
    if value.startswith("<") and ">" in value:
        target = value[1:value.index(">")]
    else:
        target = value.split(maxsplit=1)[0]
    return re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])", r"\1", target)


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
    targets = []
    chunks = []
    offset = 0
    for chunk, code in markdown_chunks(text):
        if code:
            chunks.append(_mask_code(chunk))
        else:
            def collect(_label, target, original, start):
                targets.append((text.count("\n", 0, offset + start) + 1,
                                _link_destination(target)))
                label_view = rewrite_prose_links(
                    _label, lambda _l, _t, markup, _s: markup, mask_code=True
                )
                prefix_length = 2 if original.startswith("![") else 1
                # The HTML view may inspect rendered label HTML, but not literal
                # label code, the Markdown destination, or an optional title.
                return (_mask_code(original[:prefix_length]) + label_view
                        + _mask_code(original[prefix_length + len(_label):]))

            chunks.append(rewrite_prose_links(chunk, collect, mask_code=True))
        offset += len(chunk)
    visible = "".join(chunks)
    for match in REFERENCE_LINK.finditer(visible):
        targets.append((visible.count("\n", 0, match.start()) + 1,
                        _link_destination(match.group(1))))
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


def _check_evidence_exports(root: Path, issues: list[str]) -> None:
    """Check existing case summaries only; original logs are outside this scope."""
    validation_root = root / "docs/validation-runs"
    for manifest_path in _files_in_tree(validation_root):
        parts = manifest_path.relative_to(validation_root).parts
        if len(parts) != 4 or parts[1] != "evidence" or parts[-1] != "export.json":
            continue
        location = manifest_path.relative_to(root).as_posix()
        text = _read_text(manifest_path, root, issues)
        if text is None:
            continue
        try:
            manifest = json.loads(text)
        except json.JSONDecodeError as exc:
            issues.append(f"{location}: invalid evidence JSON ({exc})")
            continue
        if (not isinstance(manifest, dict) or type(manifest.get("format_version")) is not int
                or manifest["format_version"] != 1
                or not isinstance(manifest.get("public_files"), dict)
                or not manifest["public_files"]):
            issues.append(f"{location}: expected format_version 1 and a nonempty public_files-to-SHA256 mapping")
            continue
        for name, digest in sorted(manifest["public_files"].items()):
            path = PurePosixPath(name)
            try:
                name.encode("utf-8")
            except UnicodeError:
                issues.append(f"{location}: invalid public evidence path {name!r}")
                continue
            if (not name or not path.parts or path.is_absolute() or ".." in path.parts
                    or "\\" in name or str(path) != name or any(":" in part for part in path.parts)
                    or any(character in name for character in ("\n", "\r", "\x00"))
                    or set(path.parts) & IGNORED_DIRECTORIES):
                issues.append(f"{location}: invalid public evidence path {name!r}")
                continue
            if name == manifest_path.name:
                issues.append(f"{location}: public_files must exclude the summary itself")
                continue
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                issues.append(f"{location}: invalid public evidence SHA256 for {name}")
                continue
            target = manifest_path.parent
            for part in path.parts:
                target = target / part
                if target.is_symlink():
                    issues.append(f"{location}: public evidence must be a local regular file: {name}")
                    break
            else:
                if not target.resolve().is_relative_to(manifest_path.parent.resolve()):
                    issues.append(f"{location}: public evidence must stay inside its case: {name}")
                    continue
                if not target.is_file():
                    issues.append(f"{location}: declared public evidence file is missing: {name}")
                    continue
                try:
                    current = hashlib.sha256(target.read_bytes()).hexdigest()
                except OSError as exc:
                    issues.append(f"{location}: cannot read public evidence {name} ({exc})")
                    continue
                if current != digest:
                    issues.append(f"{location}: public evidence SHA256 mismatch: {name}")


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
    _check_evidence_exports(root, issues)
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
    print("Public package links, resources, version, SVG structure, evidence summaries, and workflow freeze passed.")
    print("These checks do not establish client isolation or research quality.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
