# Capabilities, compatibility, and validation limits

[中文](compatibility.md) · [Installation](installation.en.md)

This is an Agent-guiding Skill. The [frozen entry](../skills/research-discovery-workflow/SKILL.md) and its references are authoritative. Repository helpers and this guide are optional usage aids; they add no research stage, model, or search service. Distribution versions retain the byte-frozen Workflow v1.0.0.

| Component | Actual scope | What this does not establish |
| --- | --- | --- |
| Skill text | Self-contained `SKILL.md` and local references, readable as a complete package | Automatic discovery or compliance in every host |
| Codex metadata | Includes `agents/openai.yaml` | Installer-driven host restart or registration changes |
| Python helpers | Python 3.10+ standard library for installation, checks, preparation, and packaging | A model, search service, or experiment runner |
| Isolation | Fresh context, clean workspace, and limited inputs as supported by the host | Memory clearing or file-access restrictions from directory preparation |
| Search | Tools actually available in the host; seven optional upstream capabilities | Bundled third-party scripts, accounts, or paid services |
| Pilots | An optional frozen-workflow step, executed only within actual authorization | Training or evaluation authorization from installation or a planning request |

<a id="loading-check"></a>

## Host responsibilities

The host must be able to read the entry and its relative references. Automatic discovery, `$research-discovery-workflow` invocation, custom destinations, and Skill-list refresh depend on host support. A successful file copy establishes installer completion, not host loading.

The [official Skill loading table](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) distinguishes USER `$HOME/.agents/skills` from project-level `.agents/skills`. This repository's installer chooses the former default; that choice is not a new host-loading test.

Fresh chats, memory controls, file-access boundaries, and search tools also come from the host. State unavailable capabilities honestly. A new directory is not a sandbox, and an existing context is not a blank one. The [optional reading-only prompt](installation.en.md#4-optional-check-reading-only) can check the actual path, references, and host limits; it starts no research and adds no workflow stage.

## Explicit-read fallback

If automatic discovery is unavailable but the host can read local files, keep the entire `skills/research-discovery-workflow/` directory and specify its entry directly. Do not copy only `SKILL.md`: its package includes `references/`, `scripts/`, and `agents/`. Repository examples and this guide do not replace those references.

Replace the path with the real absolute entry path for a reading-only check:

```text
Read /absolute/path/to/research-discovery-workflow/SKILL.md directly.
Treat it as the authoritative research workflow. Resolve and read its local references from the same intact Skill directory as instructed; do not replace them with this guide's summary.
For this request, report only the actual entry path, references read or missing, and the host's actual search, file-access, fresh-context, and memory-control capabilities and limits.
Do not start research, create a workspace, run the preparation helper, search for papers, generate candidates, or execute Q0–Q7. Wait for my separate start request.
```

To start research, use the [frozen English starter](QUICKSTART.en.md#one-run) in a fresh, non-forked chat. Replace its Skill invocation line with these two lines, and supply your actual neutral brief and scoped output workspace:

```text
Read /absolute/path/to/research-discovery-workflow/SKILL.md directly and use it as the authoritative workflow for this research and planning request.
Resolve and read its local references from the same intact Skill directory as instructed, then follow the start request I provide.
```

The default installed entry is `$HOME/.agents/skills/research-discovery-workflow/SKILL.md`; `CODEX_HOME` does not change the installer's default. Use `--dest` explicitly for legacy `.codex/skills`, `CODEX_HOME/skills`, or other locations. No automatic migration, deletion, or overwrite occurs, and this does not establish that legacy host loading is unsupported. Custom installations, clones, and extracted packages use their actual paths. Provide the resolved path rather than assuming a prompt expands shell variables. Explicit reading still does not establish compliance or isolation.

## What has been checked

v1.0.0 had standard-library file tests, metadata checks, and a few Agent walkthroughs with fictional materials. The [original validation record](VALIDATION.md) preserves failures, repairs, and limitations. Those checks do not prove topic quality, research success rates, or superiority of two passes.

Repository checks concern unchanged frozen files, document and asset links, temporary installation, refusal to overwrite, and release hashes. Recorded v1.1.0 results are in its [release notes](releases/v1.1.0.md); later distribution changes are in the [changelog](../CHANGELOG.md). Remote CI results require actual [Actions](https://github.com/heisenberg0020/research-discovery-workflow/actions) receipts.

CI tests repository code only on its configured Python and operating-system combinations. It does not verify every host's Skill loading, full research, or isolation. Local Windows symlink tests may require permission; a check that was not run cannot be reported as passing.

v1.3.0 adds an [actual Codex CLI receipt](validation-runs/2026-10-06-codex-cli/README.md#english-summary) on macOS / CLI 0.160.0. A name-only invocation resolved and read the intact local `.agents/skills` package; fictional cases exercised first use, delayed handoff, main-resource incompleteness and final conversation reporting. Internal registry behavior, observable child creation/isolation, implicit memory and arbitrary file-read denial remain unverified. This is not full-platform certification; see [reproduction boundaries](validation-runs/2026-10-06-codex-cli/REPRODUCE.md).

That receipt covers a project-level path, not the new default USER installation. No real installation into the personal default Skill directory or host discovery/loading check of that path was performed here; file-tool tests cannot supply that missing client evidence.

The v1.4.0 [native public-topic case](use-cases/forecast-uncertainty-2026-10-06/README.md#english-summary) encountered actual history exposure: a fresh worker's agent-status request returned substantive results from completed workers. It stopped before research rather than claiming an independent pass 2. The user retained the partial case without restarting. A status surface can carry research history even when only capacity information was requested; this observation is neither general isolation certification nor a new scientific stage.

## Other hosts

Use the import mechanism your host supports or the explicit-read fallback above. Claude Code, Cursor, and other hosts do not have complete compatibility certification here. Codex metadata cannot establish their permissions, memory behavior, or automatic loading paths.

<a id="resume-run"></a>

## Continue the same pass, without restarting

If this pass was only interrupted or is waiting for material, specify its existing workspace, `RUN.md`, and actual current proposals, including any preserved Q5 original and separate repairs. Follow the frozen entry's [Start or resume](../skills/research-discovery-workflow/SKILL.md#start-or-resume): check substantive work, evidence read, T/U exposure, and prior-result exposure, then continue the earliest unresolved dependency within the existing authorization. Do not infer completion from filenames or reroll for nicer answers.

A changed chat or executor does not relabel an informed context independent; state actual context and access changes. Do not prepare the existing directory again. For a missing authorized prior package, use the [`pending_handoff` entry](../README_EN.md#pending-handoff); use [pass-2 start](../README_EN.md#second-pass) only when another pass is actually intended. This only links existing resume rules; it adds no stage or record template.

## Common questions

**Does installation start research?** No. Installation copies files, preparation makes an empty workspace, and the reading check only inspects files and host capabilities. Starting requires a neutral brief and an explicit request in an appropriate new chat.

**Are the seven upstream Skills required?** No. They are [optional capability mappings](../skills/research-discovery-workflow/references/upstream-capabilities.md). Existing host tools can supply the capabilities.

**What if I have no previous results?** The frozen workflow allows Q6 `not_applicable` and continuation. Do not invent prior results.

**Can I report while Q7-A resources are unresolved?** Report actual partial progress and gaps, without claiming complete Q7-B. The frozen instructions define completion.

**Is pass 2 necessarily better?** No. Reconciliation can retain a better pass-1 idea. Repeated sources are not independent replication.
