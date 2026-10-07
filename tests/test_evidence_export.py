"""Synthetic-only public evidence checks; no Codex invocation or live model calls."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "docs/validation-runs/2026-10-06-codex-cli/tools/export_evidence.py"
)
UUID_ONE = "12345678-1234-5678-1234-567812345678"
UUID_TWO = "87654321-4321-8765-4321-876543218765"


def source_snapshot(root):
    return {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*") if path.is_file() and not path.is_symlink()
    }


class EvidenceExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("fictional_evidence_export", SCRIPT)
        cls.exporter = importlib.util.module_from_spec(spec)
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(sys, "dont_write_bytecode", True))
            for target in ("socket.socket", "socket.create_connection", "subprocess.run", "subprocess.Popen"):
                stack.enter_context(mock.patch(target, side_effect=AssertionError("Unexpected external work")))
            spec.loader.exec_module(cls.exporter)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fictional-evidence-export-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.repo = self.base / "fictional-repository"
        self.workspace = self.repo / "runs/case-workspace"
        self.record = self.repo / "runs/case-record"
        self.artifacts = self.workspace / "output"
        self.output = self.repo / "docs/public-evidence/FICTIONAL"
        self.home = self.base / "fictional-home"
        self.workspace.mkdir(parents=True)
        self.record.mkdir()
        self.artifacts.mkdir()
        self.home.mkdir()
        for target in ("socket.socket", "socket.create_connection", "subprocess.run", "subprocess.Popen"):
            patch = mock.patch(target, side_effect=AssertionError("Unexpected external work"))
            patch.start()
            self.addCleanup(patch.stop)
        self.raw_json("invocation.json", {"command": ["fictional-client", "--cd", str(self.workspace)], "model_override": None})
        self.raw("prompt.md", b"# Explicitly fictional test prompt\n")
        self.raw("final.md", b"A fictional mechanism remains unvalidated.\n")
        self.raw_json("result.json", {"returncode": 0, "timed_out": False, "elapsed_seconds": 1.25})
        self.events([{"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3}}])

    def raw(self, name, value):
        (self.record / name).write_bytes(value)

    def raw_json(self, name, value):
        self.raw(name, (json.dumps(value) + "\n").encode())

    def events(self, values):
        self.raw("events.jsonl", b"".join((json.dumps(value) + "\n").encode() for value in values))

    def export(self, *, output=None, artifacts=None):
        return self.exporter.export_evidence(
            self.record, self.workspace, self.output if output is None else output,
            artifacts=artifacts, repository=self.repo, home=self.home,
        )

    def public_json(self, name):
        return json.loads((self.output / name).read_bytes())

    def transcript(self):
        return [json.loads(line) for line in (self.output / "transcript.jsonl").read_bytes().splitlines()]

    def test_deterministic_export_preserves_sources_complete_final_and_raw_hashes(self):
        final = "Fictional scientific claim and exact limitation.\n" * 2000
        self.raw("final.md", final.encode())
        artifact = self.artifacts / "q5-repaired/mechanism.md"
        artifact.parent.mkdir()
        artifact.write_bytes(b"Fictional repaired operation, not validation.\n")
        (self.artifacts / "table.csv").write_bytes(b"fictional,estimate\nA,unknown\n")
        (self.artifacts / "plot.bin").write_bytes(b"\x00\xffFICTIONAL")
        before = source_snapshot(self.repo)
        self.export()
        second = self.repo / "docs/public-evidence/SECOND"
        self.export(output=second)
        first_files = {path.relative_to(self.output).as_posix(): path.read_bytes() for path in self.output.rglob("*") if path.is_file()}
        second_files = {path.relative_to(second).as_posix(): path.read_bytes() for path in second.rglob("*") if path.is_file()}
        self.assertEqual(first_files, second_files)
        self.assertEqual((self.output / "final.md").read_text(), final)
        self.assertEqual((self.output / "output/q5-repaired/mechanism.md").read_bytes(), artifact.read_bytes())
        self.assertFalse((self.output / "output/plot.bin").exists())
        after = source_snapshot(self.repo)
        for name, value in before.items():
            self.assertEqual(after[name], value)
        manifest = self.public_json("export.json")
        self.assertEqual(manifest["omitted_files"], [{"relative_path": "output/plot.bin", "reason": "non_utf8_or_binary"}])
        references = {(entry["kind"], entry["relative_path"]): entry for entry in manifest["raw_sources"]}
        for name in self.exporter.RECORD_FILES:
            self.assertEqual(references[("record", name)]["sha256"], hashlib.sha256((self.record / name).read_bytes()).hexdigest())
        self.assertEqual(references[("artifact", "output/q5-repaired/mechanism.md")]["sha256"], hashlib.sha256(artifact.read_bytes()).hexdigest())
        for name, expected in manifest["public_files"].items():
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), expected)

    def test_paths_and_identifiers_are_masked_consistently_without_changing_urls(self):
        self.raw_json("invocation.json", {
            "workspace": str(self.workspace), "record": str(self.record), "repository": str(self.repo),
            "home": str(self.home / "notes.txt"), "thread_id": UUID_ONE,
        })
        text = (
            f"Read {self.workspace}/output/test.md and {self.record}/final.md.\n"
            f"Repository {self.repo}/README.md; home {self.home}/notes.txt.\n"
            "/Users/another-person/private.txt /home/another-person/note.md /private/var/folders/private.log\n"
            "file:///Users/another-person/local.md C:\\Users\\another-person\\windows.txt \\\\private-server\\private-share\\unc.txt\n"
            "https://example.invalid/Users/another-person/paper /usr/bin/python3\n"
            f"Thread id: {UUID_ONE}; partner {UUID_TWO}\n"
        )
        self.raw("final.md", text.encode())
        self.export()
        final = (self.output / "final.md").read_text()
        self.assertIn("<WORKSPACE>/output/test.md", final)
        self.assertIn("<RECORD>/final.md", final)
        self.assertIn("<REPOSITORY>/README.md", final)
        self.assertIn("<HOME>/notes.txt", final)
        self.assertIn("<HOME>/private.txt", final)
        self.assertIn("<HOME>/private.log", final)
        self.assertIn("file://<HOME>/local.md", final)
        self.assertIn("<HOME>/windows.txt", final)
        self.assertIn("<HOME>/unc.txt", final)
        self.assertIn("https://example.invalid/Users/another-person/paper", final)
        self.assertIn("/usr/bin/python3", final)
        self.assertNotIn(UUID_ONE, final)
        self.assertNotIn(UUID_TWO, final)
        self.assertNotIn(str(self.base), final)
        self.assertNotIn("another-person/private.txt", final)
        identity = self.public_json("invocation.json")["thread_id"]
        self.assertIn(identity, final)
        self.assertEqual(self.public_json("export.json")["masked_identifier_count"], 2)

    def test_reasoning_and_state_histories_are_omitted_but_completed_content_and_errors_remain(self):
        self.events([
            {"type": "thread.started", "thread_id": UUID_ONE},
            {"type": "item.completed", "item": {"type": "reasoning", "text": "HIDDEN_REASONING_MARKER"}},
            {"type": "item.started", "item": {"type": "command_execution", "command": "TOOL_HISTORY_MARKER"}},
            {"type": "item.updated", "item": {"type": "agent_message", "text": "TOOL_HISTORY_MARKER"}},
            {"type": "item.completed", "item": {"id": "item_1", "type": "agent_message", "text": "Fictional scientific failure retained.", "reasoning": "HIDDEN_REASONING_MARKER"}},
            {"type": "item.completed", "item": {"id": "item_2", "type": "command_execution", "command": f"read {self.workspace}/brief.md", "aggregated_output": "Fictional resource remains unqualified.\n", "exit_code": 1, "status": "failed"}},
            {"type": "error", "message": f"Explicit fictional error at {self.record}/events.jsonl"},
            {"type": "turn.failed", "error": {"message": "Fictional executor interruption."}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3}},
        ])
        self.export()
        transcript = self.transcript()
        self.assertEqual([event["type"] for event in transcript], ["item.completed", "item.completed", "error", "turn.failed", "turn.completed"])
        public = (self.output / "transcript.jsonl").read_text()
        self.assertNotIn("HIDDEN_REASONING_MARKER", public)
        self.assertNotIn("TOOL_HISTORY_MARKER", public)
        self.assertIn("Fictional scientific failure retained", public)
        self.assertIn("Fictional resource remains unqualified", public)
        self.assertIn("Fictional executor interruption", public)
        counts = self.public_json("export.json")["events"]
        self.assertEqual(counts["omitted_reasoning_events"], 1)
        self.assertEqual(counts["omitted_tool_state_events"], 2)
        self.assertEqual(counts["omitted_other_events"], 1)
        self.assertEqual(counts["omitted_item_fields"], 1)

    def test_completed_file_and_collaboration_events_preserve_observations_without_inferred_spawn(self):
        self.events([
            {"type": "item.completed", "item": {"id": "item_2", "type": "file_change", "changes": [{"path": str(self.workspace / "output/repaired.md"), "kind": "add"}], "status": "completed"}},
            {"type": "item.completed", "item": {"id": "item_3", "type": "collab_tool_call", "tool": "wait", "sender_thread_id": UUID_ONE, "receiver_thread_ids": [UUID_TWO], "prompt": None, "agents_states": {UUID_TWO: {"status": "completed", "message": "Fictional worker found a missing control.", "history": "HIDDEN_HISTORY_MARKER"}}, "status": "completed"}},
            {"type": "turn.completed", "usage": {"input_tokens": 5, "cached_input_tokens": 1, "output_tokens": 2}},
        ])
        self.export()
        transcript = self.transcript()
        file_item = transcript[0]["item"]
        collab = transcript[1]["item"]
        self.assertEqual(file_item["changes"], [{"path": "<WORKSPACE>/output/repaired.md", "kind": "add"}])
        receiver = collab["receiver_thread_ids"][0]
        self.assertIn(receiver, collab["agents_states"])
        self.assertNotEqual(collab["sender_thread_id"], receiver)
        self.assertEqual(collab["tool"], "wait")
        self.assertIsNone(collab["prompt"])
        self.assertEqual(collab["agents_states"][receiver]["message"], "Fictional worker found a missing control.")
        self.assertNotIn("HIDDEN_HISTORY_MARKER", (self.output / "transcript.jsonl").read_text())
        self.assertNotIn("spawn", [event.get("item", {}).get("tool") for event in transcript])

    def test_usage_keeps_cached_subset_and_unknown_fields_null(self):
        self.export()
        usage = self.public_json("usage.json")
        self.assertEqual(usage["call_usage"], {"input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3, "cache_write_input_tokens": None, "reasoning_output_tokens": None, "recorded_input_plus_output_tokens": 13})
        self.assertIn("subset", usage["cached_input_note"])
        self.assertIn("subagent usage was not captured", usage["usage_scope"])
        self.assertIn("not a closed total cost or bill", usage["usage_scope"])
        self.events([{"type": "turn.completed", "usage": {"input_tokens": None, "output_tokens": 4}}])
        second = self.repo / "docs/public-evidence/UNKNOWN"
        self.export(output=second)
        unknown = json.loads((second / "usage.json").read_bytes())["call_usage"]
        self.assertIsNone(unknown["input_tokens"])
        self.assertIsNone(unknown["cached_input_tokens"])
        self.assertEqual(unknown["output_tokens"], 4)
        self.assertIsNone(unknown["recorded_input_plus_output_tokens"])

    def test_reported_auxiliary_usage_is_retained_without_adding_or_inventing_unknown_fields(self):
        self.events([{"type": "turn.completed", "usage": {
            "input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3,
            "cache_write_input_tokens": 2, "reasoning_output_tokens": 1,
            "future_token_field": 99,
        }}])
        self.export()
        usage = self.public_json("usage.json")
        self.assertEqual(usage["call_usage"]["cache_write_input_tokens"], 2)
        self.assertEqual(usage["call_usage"]["reasoning_output_tokens"], 1)
        self.assertEqual(usage["call_usage"]["recorded_input_plus_output_tokens"], 13)
        self.assertNotIn("future_token_field", usage["call_usage"])
        self.assertEqual(usage["uncovered_usage_fields"], [{"line": 1, "fields": ["future_token_field"]}])
        self.assertEqual(self.transcript()[0]["usage"]["reasoning_output_tokens"], 1)

    def test_multiple_usage_events_remain_individual_without_guessed_call_total(self):
        self.events([
            {"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3}},
            {"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 7, "output_tokens": 3}},
        ])
        self.export()
        usage = self.public_json("usage.json")
        self.assertEqual(len(usage["reported_turns"]), 2)
        self.assertTrue(all(value is None for value in usage["call_usage"].values()))
        self.assertEqual(usage["call_usage_status"], "missing_or_ambiguous")

    def test_malformed_unknown_and_incomplete_events_do_not_become_invented_messages(self):
        self.raw("events.jsonl", (
            b"\nnot-json\n{\"type\":\"future.event\",\"text\":\"UNKNOWN_MARKER\"}\n"
            b"[]\n{\"type\":\"item.completed\"}\n"
            b"{\"type\":\"item.completed\",\"item\":{\"type\":[\"unknown\"]}}\n"
            b"{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\"}}\n"
            b"{\"type\":\"item.completed\",\"item\":{\"type\":\"reasoning\",\"text\":\"HIDDEN\"}}\n"
            b"{\"type\":\"turn.completed\""
        ))
        (self.record / "final.md").unlink()
        (self.record / "result.json").unlink()
        self.export()
        self.assertEqual(self.transcript(), [])
        report = self.public_json("export.json")
        self.assertEqual(report["events"]["malformed_events"], 3)
        self.assertEqual(report["events"]["unknown_events"], 3)
        self.assertEqual(report["events"]["incomplete_events"], 2)
        self.assertEqual(report["events"]["blank_lines"], 1)
        self.assertEqual(len(report["events"]["malformed_lines"]), 3)
        self.assertEqual(report["missing_raw_files"], ["final.md", "result.json"])
        self.assertFalse((self.output / "final.md").exists())
        self.assertTrue(all(value is None for value in self.public_json("usage.json")["call_usage"].values()))

    def test_markdown_local_links_become_code_paths_and_paper_urls_survive(self):
        self.raw("final.md", (
            f"Concrete fictional claim. [Report]({self.workspace}/output/report.md)\n"
            "[relative](output/report.md) [paper](https://example.invalid/paper) [section](#claim)\n"
        ).encode())
        (self.artifacts / "report.md").write_text("Fictional control. [data](table.csv) [paper](https://example.invalid/paper)\n")
        self.export()
        final = (self.output / "final.md").read_text()
        artifact = (self.output / "output/report.md").read_text()
        self.assertIn("Report (`<WORKSPACE>/output/report.md`)", final)
        self.assertIn("relative (`output/report.md`)", final)
        self.assertIn("[paper](https://example.invalid/paper)", final)
        self.assertIn("[section](#claim)", final)
        self.assertIn("data (`table.csv`)", artifact)
        self.assertIn("[paper](https://example.invalid/paper)", artifact)
        counts = self.public_json("export.json")["redactions"]
        self.assertEqual(counts["markdown_local_links"], 3)
        self.assertEqual(counts["final_local_markdown_links"], 2)

    def test_markdown_code_spans_and_fences_remain_literal_while_prose_links_convert(self):
        code = (
            '```python\nrule = "[q](x)"\n[example](output/not-a-rendered-link.md)\n```\n'
            "~~~markdown\n[tilde example](output/example.md)\n~~~\n"
            '    rule = "[indented](x)"\n\t[tab code](output/example.md)\n'
            "Inline `[q](x)` and ``[label](output/file.md) `literal` `` remain code.\n"
            "Multiline `code [label](output/file.md)\ncontinued` remains code.\n"
        )
        prose = "[actual report](output/report.md)\n"
        self.raw("final.md", (code + prose).encode())
        (self.artifacts / "report.md").write_text(code + prose)
        self.export()
        expected = code + "actual report (`output/report.md`)\n"
        self.assertEqual((self.output / "final.md").read_text(), expected)
        self.assertEqual((self.output / "output/report.md").read_text(), expected)
        self.assertEqual(self.public_json("export.json")["redactions"]["markdown_local_links"], 2)

    def test_balanced_parentheses_escaped_text_and_unclosed_links_are_preserved(self):
        text = (
            "[report](output/report(1).md) [nested](output/a(b(c)).md)\n"
            "![figure](output/figure(2).svg)\n"
            "[paper](https://example.invalid/paper(1))\n"
            r"\[literal](output/literal.md) [escaped](output/report\(1\).md)" + "\n"
            "[unclosed](output/report(1).md\n"
        )
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), (
            "report (`output/report(1).md`) nested (`output/a(b(c)).md`)\n"
            "figure (`output/figure(2).svg`)\n"
            "[paper](https://example.invalid/paper(1))\n"
            r"\[literal](output/literal.md) escaped (`output/report\(1\).md`)" + "\n"
            "[unclosed](output/report(1).md\n"
        ))

    def test_angle_external_targets_and_titles_keep_clickable_source_links(self):
        text = (
            '[paper](<https://example.invalid/paper(1)> "Source title")\n'
            '[mail](<mailto:source@example.invalid>) [section](<#here>)\n'
            '[network](<//example.invalid/source>)\n'
            '[local](<output/report(1).md> "Local title")\n'
        )
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), text.replace(
            '[local](<output/report(1).md> "Local title")',
            'local (`<output/report(1).md> "Local title"`)'
        ))
        self.assertEqual(self.public_json("export.json")["redactions"]["markdown_local_links"], 1)

    def test_list_continuation_prose_converts_while_nested_code_stays_literal(self):
        text = (
            '1. Parent item\n\n'
            '    [report](output/report(1).md)\n\n'
            '        rule = "[code](not-a-link.md)"\n\n'
            '    ```python\n    rule = "[fenced](not-a-link.md)"\n    ```\n'
        )
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), text.replace(
            '[report](output/report(1).md)', 'report (`output/report(1).md`)'
        ))
        self.assertEqual(self.public_json("export.json")["redactions"]["markdown_local_links"], 1)

    def test_empty_labels_and_literal_label_brackets_still_convert_local_links(self):
        text = '![](output/figure.svg) [Literal `[`](output/report.md)\n'
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(),
                         ' (`output/figure.svg`) Literal `[` (`output/report.md`)\n')
        self.assertEqual(self.public_json("export.json")["redactions"]["markdown_local_links"], 2)

    def test_indented_paragraph_links_convert_but_actual_code_remains_literal(self):
        text = 'Paragraph\n    [report](output/report.md)\n\n    [literal](output/example.md)\n'
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), text.replace(
            '[report](output/report.md)', 'report (`output/report.md`)'
        ))
        self.assertEqual(self.public_json("export.json")["redactions"]["markdown_local_links"], 1)

    def test_angle_sources_keep_unbalanced_parentheses_unchanged(self):
        text = '[paper](<https://example.invalid/paper)>) [local](<output/report(.md>)\n'
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), text.replace(
            '[local](<output/report(.md>)', 'local (`<output/report(.md>`)'
        ))

    def test_quoted_title_parentheses_are_not_link_delimiters(self):
        text = '[local](output/report.md "A( title") [paper](https://example.invalid/paper \'A) title\')\n'
        self.raw("final.md", text.encode())
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), text.replace(
            '[local](output/report.md "A( title")', 'local (`output/report.md "A( title"`)'
        ))

    def test_mathematical_division_tables_and_logical_agent_names_are_preserved(self):
        mathematical_text = (
            "q=(x−20)/5\na=(q+1)/2\n(1/3)/4\nx / y\n"
            "| quantity | formula | interpretation |\n"
            "| --- | --- | --- |\n"
            "| q | (x−20)/5 | retained scientific operation |\n"
            "| a | (q+1)/2 | retained control |\n"
            "| ratio | (1/3)/4 | exact fractional calculation |\n"
            "Logical agent /root/domain; abstract protocol /unknown/protocol/path.\n"
        )
        self.raw("final.md", mathematical_text.encode())
        (self.artifacts / "mathematics.md").write_text(mathematical_text)
        self.events([{"type": "item.completed", "item": {"type": "agent_message", "text": mathematical_text}}])
        self.export()
        self.assertEqual((self.output / "final.md").read_text(), mathematical_text)
        self.assertEqual((self.output / "output/mathematics.md").read_text(), mathematical_text)
        self.assertEqual(self.transcript()[0]["item"]["text"], mathematical_text)
        root_home_redactor = self.exporter.Redactor(self.workspace, self.record, self.repo, Path("/root"))
        self.assertEqual(root_home_redactor.text("Logical /root/domain and private /root/.codex/config"), "Logical /root/domain and private <HOME>/.codex/config")

    def test_explicit_artifact_snapshot_is_disclosed_and_actual_workspace_mask_is_retained(self):
        with self.assertRaises(OSError):
            self.export(artifacts=self.repo / "runs/missing-snapshot/output")
        self.assertFalse(self.output.exists())
        snapshot = self.repo / "runs/snapshots/FICTIONAL-pre/output"
        snapshot.mkdir(parents=True)
        (snapshot / "pre.md").write_text(f"Frozen fictional operation at {self.workspace}/output/pre.md.\n")
        (self.artifacts / "post.md").write_text("Fictional later handoff; do not export in the pre snapshot.\n")
        self.export(artifacts=snapshot)
        report = self.public_json("export.json")
        self.assertTrue(report["explicit_artifact_root"])
        self.assertFalse(report["artifact_source_is_workspace_output"])
        self.assertIn("snapshots/FICTIONAL-pre/output", report["artifact_source"])
        self.assertFalse((self.output / "output/post.md").exists())
        self.assertIn("<WORKSPACE>/output/pre.md", (self.output / "output/pre.md").read_text())

    def test_existing_target_and_symlink_inputs_are_rejected_without_source_changes(self):
        self.output.mkdir(parents=True)
        (self.output / "sentinel.txt").write_bytes(b"Preserve public evidence fixture.\n")
        before = source_snapshot(self.repo)
        with self.assertRaises(FileExistsError):
            self.export()
        self.assertEqual(source_snapshot(self.repo), before)
        broken = self.repo / "docs/public-evidence/BROKEN"
        broken.symlink_to(self.base / "missing-target")
        with self.assertRaises(FileExistsError):
            self.export(output=broken)
        linked = self.artifacts / "external.md"
        linked.symlink_to(self.record / "final.md")
        new_output = self.repo / "docs/public-evidence/REJECTED"
        with self.assertRaises(ValueError):
            self.export(output=new_output)
        self.assertFalse(new_output.exists())
        self.assertTrue(broken.is_symlink())

    def test_output_inside_source_is_rejected_and_cli_uses_only_explicit_synthetic_inputs(self):
        with self.assertRaises(ValueError):
            self.export(output=self.workspace / "public-copy")
        with mock.patch.object(self.exporter, "REPOSITORY", self.repo), mock.patch.object(Path, "home", return_value=self.home), contextlib.redirect_stdout(io.StringIO()) as stdout:
            result = self.exporter.main([
                "--record", str(self.record), "--workspace", str(self.workspace), "--output", str(self.output),
                "--artifacts", str(self.artifacts),
            ])
        self.assertEqual(result, 0)
        self.assertIn("Exported sanitized evidence", stdout.getvalue())
        self.assertTrue(self.public_json("export.json")["explicit_artifact_root"])


if __name__ == "__main__":
    unittest.main()
