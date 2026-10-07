#!/usr/bin/env python3
"""Opt-in sanitized evidence export for the fixed CLI smoke cases; no client calls.

This reads only the named record files and the explicit scientific artifact root.
Public copies require independent review. Path masking is not a secret detector.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys


REPOSITORY = Path(__file__).resolve().parents[4]
# Reuse the repository's small Markdown parser; importing it performs no checks.
_MARKDOWN_SPEC = importlib.util.spec_from_file_location(
    "evidence_markdown", REPOSITORY / "scripts/check_repo.py"
)
_MARKDOWN = importlib.util.module_from_spec(_MARKDOWN_SPEC)
_MARKDOWN_SPEC.loader.exec_module(_MARKDOWN)
RECORD_FILES = ("invocation.json", "prompt.md", "events.jsonl", "final.md", "result.json")
USAGE_FIELDS = (
    "input_tokens", "cached_input_tokens", "output_tokens",
    "cache_write_input_tokens", "reasoning_output_tokens",
)
ITEM_FIELDS = {
    "agent_message": ("id", "type", "text"),
    "command_execution": ("id", "type", "command", "aggregated_output", "exit_code", "status"),
    "file_change": ("id", "type", "changes", "patch", "diff", "status"),
    "collab_tool_call": (
        "id", "type", "tool", "sender_thread_id", "receiver_thread_ids",
        "prompt", "agents_states", "status",
    ),
    "error": ("id", "type", "message", "error"),
}
IDENTIFIER_FIELDS = {
    "thread_id", "threadId", "sender_thread_id", "receiver_thread_id",
    "receiver_thread_ids", "session_id", "sessionId", "conversation_id",
}
HISTORY_FIELDS = {"reasoning", "reasoning_content", "encrypted_content", "history", "tool_state_history"}
UUID = re.compile(r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b")
THREAD_TOKEN = re.compile(r"\bthread_[A-Za-z0-9_-]{8,}\b")
LABELED_IDENTIFIER = re.compile(
    r"(?i)(\b(?:thread|session|conversation)[_ -]?id\s*[:=]\s*[\"']?)([^\s\"',;<>]+)"
)
PRIVATE_PATH = re.compile(
    r"(?<![\w/:.<>])(?:"
    r"/(?:Users|home|private|tmp|var/folders|var/tmp|mnt|media|Volumes)/"
    r"[^\s\"'`<>()[\]{},;]+"
    r"|[A-Za-z]:[\\/]Users[\\/][^\s\"'`<>()[\]{},;]+"
    r"|\\\\[^\\\s\"'`<>()[\]{},;]+\\[^\s\"'`<>()[\]{},;]+"
    r")"
)
FILE_URI = re.compile(r"file://(/[^\s\"'`<>()[\]{},;]+)")
PUBLIC_SYSTEM_PREFIXES = ("/usr/", "/bin/", "/sbin/", "/dev/", "/etc/", "/System/", "/Library/")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def regular_file(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Expected a regular, non-link input file: {path}")


def directory(path: Path) -> Path:
    path = Path(path).expanduser().absolute()
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise ValueError(f"Expected a non-link input directory: {path}")
    return path.resolve()


class Redactor:
    """Mechanical replacement labels, with stable IDs across one export."""

    def __init__(self, workspace: Path, record: Path, repository: Path, home: Path):
        self.prefixes = sorted(
            [(str(workspace), "<WORKSPACE>"), (str(record), "<RECORD>"),
             (str(repository), "<REPOSITORY>"), (str(home), "<HOME>")],
            key=lambda pair: -len(pair[0]),
        )
        self.identifiers: dict[str, str] = {}
        self.counts = {
            "workspace_paths": 0, "record_paths": 0, "repository_paths": 0,
            "home_paths": 0, "other_absolute_paths": 0, "identifier_occurrences": 0,
            "omitted_history_fields": 0, "markdown_local_links": 0, "final_local_markdown_links": 0,
        }

    def identifier(self, value: str) -> str:
        key = value.lower() if UUID.fullmatch(value) else value
        if key not in self.identifiers:
            self.identifiers[key] = f"<ID-{len(self.identifiers) + 1}>"
        self.counts["identifier_occurrences"] += 1
        return self.identifiers[key]

    def text(self, value: str) -> str:
        for prefix, label in self.prefixes:
            logical_exclusion = (
                r"(?!/(?:domain|method|reviewer)(?:$|[/\s\"'`<>()[\]{},;:]))"
                if label == "<HOME>" and prefix == "/root" else ""
            )
            pattern = re.compile(re.escape(prefix) + logical_exclusion + r"(?=$|[/\\\s\"'`<>()[\]{},;:])")
            value, count = pattern.subn(lambda _match: label, value)
            key = {"<WORKSPACE>": "workspace_paths", "<RECORD>": "record_paths",
                   "<REPOSITORY>": "repository_paths", "<HOME>": "home_paths"}[label]
            self.counts[key] += count

        def other_path(path: str) -> str:
            if path.startswith(PUBLIC_SYSTEM_PREFIXES):
                return path
            normalized = path.replace("\\", "/")
            parts = normalized.strip("/").split("/")
            self.counts["other_absolute_paths"] += 1
            if len(parts) >= 2 and parts[0] in ("Users", "home"):
                return "<HOME>" + ("/" + "/".join(parts[2:]) if len(parts) > 2 else "")
            if len(parts) >= 3 and re.fullmatch(r"[A-Za-z]:", parts[0]) and parts[1] == "Users":
                return "<HOME>" + ("/" + "/".join(parts[3:]) if len(parts) > 3 else "")
            return "<HOME>/" + parts[-1]

        value = FILE_URI.sub(lambda match: "file://" + other_path(match.group(1)), value)
        value = PRIVATE_PATH.sub(lambda match: other_path(match.group()), value)
        value = UUID.sub(lambda match: self.identifier(match.group()), value)
        value = THREAD_TOKEN.sub(lambda match: self.identifier(match.group()), value)
        return LABELED_IDENTIFIER.sub(
            lambda match: match.group(1) + self.identifier(match.group(2)), value
        )

    def value(self, value: object, *, field: str | None = None) -> object:
        if isinstance(value, str):
            return self.identifier(value) if field in IDENTIFIER_FIELDS else self.text(value)
        if isinstance(value, list):
            return [self.value(entry, field=field) for entry in value]
        if isinstance(value, dict):
            result = {}
            for key, entry in value.items():
                if key in HISTORY_FIELDS:
                    self.counts["omitted_history_fields"] += 1
                    continue
                public_key = self.identifier(key) if field == "agents_states" else self.text(key)
                if public_key in result:
                    raise ValueError("Redaction produced duplicate object keys")
                result[public_key] = self.value(entry, field=key)
            return result
        return value

    def markdown_text(self, value: str, *, final: bool = False) -> str:
        def local_link(label: str, target: str, original: str, _start: int) -> str:
            destination = _MARKDOWN._link_destination(target)
            if destination.startswith(("#", "//")) or (
                re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", destination) and not destination.startswith("file:")
            ):
                return original
            self.counts["markdown_local_links"] += 1
            if final:
                self.counts["final_local_markdown_links"] += 1
            fence = "`" * (max((len(run) for run in re.findall(r"`+", target)), default=0) + 1)
            return f"{label} ({fence}{target}{fence})"

        # Parse original destinations before replacing absolute roots with
        # angle-shaped placeholders such as <WORKSPACE>/output/report.md.
        return self.text("".join(
            chunk if code else _MARKDOWN.rewrite_prose_links(chunk, local_link)
            for chunk, code in _MARKDOWN.markdown_chunks(value)
        ))


def usage_fields(value: object) -> dict[str, int | None]:
    fields = value if isinstance(value, dict) else {}
    result = {}
    for key in USAGE_FIELDS:
        entry = fields.get(key)
        result[key] = entry if type(entry) is int and entry >= 0 else None
    input_tokens, output_tokens = result["input_tokens"], result["output_tokens"]
    result["recorded_input_plus_output_tokens"] = (
        input_tokens + output_tokens if input_tokens is not None and output_tokens is not None else None
    )
    return result


def parse_events(data: bytes, redactor: Redactor) -> tuple[list[dict], dict, dict]:
    selected = []
    turns = []
    uncovered_usage = []
    report = {
        "total_lines": 0, "blank_lines": 0, "malformed_events": 0,
        "unknown_events": 0, "incomplete_events": 0, "selected_events": 0,
        "omitted_reasoning_events": 0, "omitted_tool_state_events": 0,
        "omitted_other_events": 0, "omitted_item_fields": 0,
        "turn_completed_events": 0, "malformed_lines": [],
        "count_note": "incomplete_events is a schema diagnostic and can overlap unknown_events",
    }
    for line_number, raw in enumerate(data.splitlines(), 1):
        report["total_lines"] += 1
        if not raw.strip():
            report["blank_lines"] += 1
            continue
        try:
            event = json.loads(raw)
            if not isinstance(event, dict):
                raise ValueError("not_object")
        except (ValueError, UnicodeError):
            report["malformed_events"] += 1
            report["malformed_lines"].append({"line": line_number, "sha256": digest(raw)})
            continue
        kind = event.get("type")
        item = event.get("item")
        item_type = item.get("type") if isinstance(item, dict) else None
        public = None
        if item_type == "reasoning":
            report["omitted_reasoning_events"] += 1
        elif kind in ("item.started", "item.updated"):
            report["omitted_tool_state_events"] += 1
        elif kind == "item.completed" and isinstance(item_type, str) and item_type in ITEM_FIELDS:
            if item_type == "agent_message" and not isinstance(item.get("text"), str):
                report["incomplete_events"] += 1
            else:
                allowed = ITEM_FIELDS[item_type]
                report["omitted_item_fields"] += len(set(item) - set(allowed))
                public = {"type": kind, "item": redactor.value({key: item[key] for key in allowed if key in item})}
        elif kind == "turn.completed":
            report["turn_completed_events"] += 1
            reported_usage = event.get("usage")
            usage = usage_fields(reported_usage)
            if isinstance(reported_usage, dict):
                uncovered = sorted(set(reported_usage) - set(USAGE_FIELDS))
                if uncovered:
                    uncovered_usage.append({"line": line_number, "fields": redactor.value(uncovered)})
            turns.append({"line": line_number, **usage})
            public = {"type": kind, "usage": usage}
        elif kind in ("error", "turn.failed"):
            public = redactor.value({key: event[key] for key in ("type", "message", "error") if key in event})
            if "message" not in event and "error" not in event:
                report["incomplete_events"] += 1
        elif kind in ("thread.started", "turn.started"):
            report["omitted_other_events"] += 1
        else:
            report["unknown_events"] += 1
            if not isinstance(kind, str) or (kind == "item.completed" and not isinstance(item, dict)):
                report["incomplete_events"] += 1
        if public is not None:
            selected.append({"source_line": line_number, **public})
    report["selected_events"] = len(selected)
    call_usage = {key: turns[0][key] for key in usage_fields(None)} if len(turns) == 1 else usage_fields(None)
    usage = {
        "call_usage": call_usage,
        "reported_turns": turns,
        "uncovered_usage_fields": uncovered_usage,
        "call_usage_status": "one_reported_turn" if len(turns) == 1 else "missing_or_ambiguous",
        "cached_input_note": "cached_input_tokens is a subset of input_tokens; it is never added again",
        "auxiliary_usage_note": "cache_write_input_tokens and reasoning_output_tokens are retained as reported and are not added to recorded input plus output",
        "multiple_turn_note": "Multiple usage events are retained individually; no call total is inferred",
        "usage_scope": (
            "Fields are reported by this CLI main-session turn.completed event. "
            "Separate native subagent usage was not captured; whether it is included is unknown. "
            "Recorded input plus output across calls is not a closed total cost or bill. "
            "Unknown fields stay null and are never treated as zero."
        ),
    }
    return selected, report, usage


def read_artifacts(root: Path) -> list[tuple[str, bytes]]:
    if not os.path.lexists(root):
        return []
    root = directory(root)
    result = []
    for current, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        for name in directories:
            directory(Path(current) / name)
        for name in sorted(files):
            path = Path(current) / name
            regular_file(path)
            result.append((path.relative_to(root).as_posix(), path.read_bytes()))
    return result


def export_evidence(
    record: Path, workspace: Path, output: Path, *, artifacts: Path | None = None,
    repository: Path | None = None, home: Path | None = None,
) -> Path:
    """Create one new public case from explicit raw inputs without changing them."""
    record, workspace = directory(record), directory(workspace)
    output = Path(output).expanduser().absolute()
    if os.path.lexists(output):
        raise FileExistsError(f"Refusing an existing evidence path: {output}")
    output = output.resolve()
    if os.path.lexists(output):
        raise FileExistsError(f"Refusing an existing evidence path: {output}")
    repository = Path(REPOSITORY if repository is None else repository).resolve()
    artifact_root = (workspace / "output") if artifacts is None else directory(artifacts)
    if any(output == source or source in output.parents for source in (record, workspace, artifact_root)):
        raise ValueError("Evidence output must be outside raw records, workspace, and artifact root")
    redactor = Redactor(workspace, record, repository, Path.home() if home is None else Path(home).resolve())
    copies: dict[str, bytes] = {}
    raw_sources = []
    missing_files = []
    omitted_files = []
    raw_records = {}
    for name in RECORD_FILES:
        source = record / name
        if not os.path.lexists(source):
            missing_files.append(name)
            continue
        regular_file(source)
        data = source.read_bytes()
        raw_records[name] = data
        raw_sources.append({"kind": "record", "relative_path": name, "sha256": digest(data), "bytes": len(data)})
        if name == "events.jsonl":
            continue
        if name.endswith(".json"):
            try:
                value = json.loads(data)
            except (ValueError, UnicodeError):
                omitted_files.append({"relative_path": name, "reason": "invalid_json"})
                continue
            copies[name] = encoded_json(redactor.value(value))
        else:
            text = data.decode("utf-8")
            copies[name] = redactor.markdown_text(text, final=name == "final.md").encode("utf-8")
    selected, event_report, usage = parse_events(raw_records.get("events.jsonl", b""), redactor)
    copies["transcript.jsonl"] = b"".join(
        (json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8") for event in selected
    )
    copies["usage.json"] = encoded_json(usage)
    for name, data in read_artifacts(artifact_root):
        public_name = "output/" + redactor.text(name)
        raw_sources.append({"kind": "artifact", "relative_path": public_name, "sha256": digest(data), "bytes": len(data)})
        try:
            text = data.decode("utf-8")
            if "\x00" in text:
                raise ValueError("binary")
        except (UnicodeError, ValueError):
            omitted_files.append({"relative_path": public_name, "reason": "non_utf8_or_binary"})
            continue
        if public_name in copies:
            raise ValueError("Redaction produced duplicate artifact paths")
        public_text = redactor.markdown_text(text) if name.lower().endswith((".md", ".markdown")) else redactor.text(text)
        copies[public_name] = public_text.encode("utf-8")
    artifact_source = redactor.text(str(artifact_root))
    export_record = {
        "format_version": 1,
        "source_record": "<RECORD>", "source_workspace": "<WORKSPACE>",
        "artifact_source": artifact_source,
        "explicit_artifact_root": artifacts is not None,
        "artifact_source_is_workspace_output": artifact_root == workspace / "output",
        "artifact_source_note": "An explicit artifact root may be a retained snapshot; it is not the CLI workspace",
        "raw_sources": raw_sources,
        "missing_raw_files": missing_files, "omitted_files": omitted_files,
        "events": event_report, "redactions": redactor.counts,
        "masked_identifier_count": len(redactor.identifiers),
        "public_files": {name: digest(data) for name, data in sorted(copies.items())},
        "boundaries": [
            "Sanitized public copies, not raw transcripts or proof of research quality",
            "Only selected completed items, turn usage, and explicit errors are published",
            "No spawn, isolation, missing message, missing usage, or successful science is inferred",
            "Paths and identifiers are mechanically masked; independent public review is still required",
            "Only known source/home prefixes, recognized private filesystem roots, and file URIs are masked; other abstract paths and mathematical division are retained",
            "Local links in sanitized Markdown become label plus code path; URL links and scientific prose are retained",
        ],
    }
    copies["export.json"] = encoded_json(export_record)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    for name, data in sorted(copies.items()):
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--record", type=Path, required=True, help="One explicitly scoped raw record directory")
    parser.add_argument("--workspace", type=Path, required=True, help="Actual CLI case workspace, used for masking")
    parser.add_argument("--output", type=Path, required=True, help="New public case evidence directory; no overwrite")
    parser.add_argument("--artifacts", type=Path, help="Explicit output artifact root, including a retained snapshot")
    args = parser.parse_args(argv)
    try:
        output = export_evidence(args.record, args.workspace, args.output, artifacts=args.artifacts)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Evidence export failed: {error}", file=sys.stderr)
        return 2
    print(f"Exported sanitized evidence: {output}")
    print("Raw inputs were preserved. Review the public copies independently before publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
