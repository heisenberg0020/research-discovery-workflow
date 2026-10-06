"""Opt-in local evidence capture for this fixed smoke test, not a research harness.

Only an explicit invocation starts one existing-login Codex call. Unit tests/CI
must never run this script. Raw records stay outside the public evidence tree.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--sandbox", choices=("read-only", "workspace-write"), required=True)
    args = parser.parse_args()
    workspace, prompt, record = (p.resolve() for p in (args.workspace, args.prompt, args.record))
    if not workspace.is_dir() or not prompt.is_file() or record.exists():
        parser.error("Existing workspace/prompt and a new record directory are required")
    if not record.parent.is_dir() or record.is_relative_to(workspace):
        parser.error("Record parent must exist and records must stay outside executor workspace")
    env = dict(os.environ)
    for key in ("OPENAI_API_KEY", "CODEX_API_KEY"):
        env.pop(key, None)
    auth = subprocess.run(["codex", "login", "status"], env=env, capture_output=True, text=True)
    if auth.returncode or "Logged in using ChatGPT" not in auth.stdout + auth.stderr:
        parser.error("Existing ChatGPT login required; no API-key fallback is allowed")
    record.mkdir()
    command = [
        "codex", "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral",
        "--skip-git-repo-check", "--sandbox", args.sandbox, "--json", "--color", "never",
        "--cd", str(workspace), "--output-last-message", str(record / "final.md"), "-",
    ]
    started = datetime.now(timezone.utc).isoformat()
    metadata = {"command": command, "started_at": started, "timeout_seconds": 900,
                "auth_mode": "existing ChatGPT login", "model_override": None}
    (record / "invocation.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (record / "prompt.md").write_bytes(prompt.read_bytes())
    clock = time.monotonic()
    timed_out = False
    with prompt.open("rb") as source, (record / "events.jsonl").open("wb") as events, \
            (record / "stderr.log").open("wb") as errors:
        process = subprocess.Popen(command, stdin=source, stdout=events, stderr=errors,
                                   env=env, start_new_session=True)
        print(json.dumps({"pid": process.pid, "record": str(record)}), flush=True)
        try:
            returncode = process.wait(timeout=900)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                returncode = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                returncode = process.wait()
    result = {"returncode": returncode, "timed_out": timed_out,
              "elapsed_seconds": round(time.monotonic() - clock, 3)}
    (record / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    raise SystemExit(returncode if not timed_out else 124)


if __name__ == "__main__":
    main()
