# Research Discovery Workflow

<p align="center">
  <img src="docs/images/banner.svg" alt="Research Discovery Workflow: understanding, proposals, and discriminating plans" width="100%" />
</p>

<p align="center">
  <strong>Turn understanding of a field into concrete proposals and plans that distinguish competing answers.</strong>
</p>

<p align="center">
  <a href="README.md">中文</a> · <a href="README_EN.md">English</a><br />
  <a href="https://github.com/heisenberg0020/research-discovery-workflow/releases/latest"><img src="https://img.shields.io/github/v/release/heisenberg0020/research-discovery-workflow" alt="Latest release" /></a>
  <a href="https://github.com/heisenberg0020/research-discovery-workflow/actions/workflows/ci.yml"><img src="https://github.com/heisenberg0020/research-discovery-workflow/actions/workflows/ci.yml/badge.svg" alt="Repository checks" /></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776ab" alt="Python 3.10 or newer" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2f6f8f" alt="MIT license" /></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#workflow">Workflow</a> ·
  <a href="#examples">Examples</a> ·
  <a href="#validation">Validation</a> ·
  <a href="#docs">Docs</a>
</p>

This portable Skill supports open-ended topic selection, literature-to-idea synthesis, explanations of phenomena, and method proposals across research fields. It develops the research object, its mechanism, the nearest existing answers, and a comparison that could change a research decision.

It is a planning Skill, not an experiment execution harness. Its default work is literature, theory, and static code understanding. Planning does not authorize implementation, training, or experiments.

Repository **v1.4.0** improves installation, startup navigation and evidence handling alongside public use cases. The scientific workflow remains the byte-frozen **v1.0.0** workflow; see the [freeze boundary](docs/FROZEN_WORKFLOW.md) and [changelog](CHANGELOG.md). Earlier releases remain available.

## Quick start

Use Python 3.10 or newer. The package helpers use the Python standard library.

```bash
git clone https://github.com/heisenberg0020/research-discovery-workflow.git
cd research-discovery-workflow
RDW_PYTHON=python3
"$RDW_PYTHON" -c 'import sys; print(sys.executable, sys.version); raise SystemExit(0 if sys.version_info >= (3, 10) else "Python 3.10+ required")'
```

These are POSIX-shell commands, suitable for macOS/Linux. `python3` is a candidate, not a guaranteed version. If it is missing or older, select `python` or the full path of an installed Python 3.10+ executable, then repeat the check. **Only after it succeeds**, continue in the same terminal:

```sh
"$RDW_PYTHON" scripts/install.py --dry-run
"$RDW_PYTHON" scripts/install.py
```

The installer defaults to `.agents/skills` in the current user's home directory (`$HOME/.agents/skills` in POSIX notation), matching the USER location in the [official Skill loading table](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). `CODEX_HOME` does not change this helper's default. Use `--dest` for a legacy or custom location; the installer does not automatically migrate, delete, or overwrite existing copies. Preview writes nothing.

File installation is not host discovery. Existing actual receipts cover the project-level `.agents/skills` path, not a real installation/loading test of the new user-level default. Read [English installation and updates](docs/installation.en.md) for destination choices, Windows command notes, and release checksums before extraction. Use the optional [loading-only check](docs/compatibility.en.md#loading-check) to inspect your host; it starts no research.

Copy [the English neutral brief](examples/neutral-brief.en.md) to a personal file and edit it with your actual topic, research goal, evidence scope, constraints, and resources. Keep previous proposals, rankings, architectures, and results out of this first-pass input.

Start a **fresh, non-forked chat** with that brief and a clean, scoped workspace for this pass. Replace both paths below with actual values. If you choose the [optional preparation helper](docs/installation.en.md#5-start-in-a-fresh-context), prepare first and use its printed `Prepared` root as this pass's workspace. Invoke the installed Skill using this planning-only request:

```text
Use $research-discovery-workflow for research discovery and proposal planning.

Neutral brief: /absolute/path/to/my-neutral-brief.md
Output workspace for this pass: /absolute/path/to/new-discovery-workspace

Follow the frozen Q0–Q7 workflow. Keep Q1-T domain-down and Q1-U
method-up first judgments separate before Q1-S synthesis. Develop
concrete mechanisms and preserve the original Q5 proposal unchanged.

Complete mandatory Q5-R retrospective and separate repairs before
reading previous research results. Q6 is conditional on an authorized
handoff; with no prior material, mark it not_applicable. Propose or
skip optional Q6-P without running a pilot.

Complete Q7-A's four-question comparison design and resource assessment
before Q7-B. Finish with a substantive in-chat insight report as well
as saved planning artifacts, stating actual readiness and conditions.

Describe the actual context, memory, and file-access isolation limits.
Do not implement the proposal, run experiments, train models, or resume
previous experiments. Stop after the planning deliverable.
```

A prepared directory does not create a fresh conversation, clear memory, or restrict file access. Use the [English compatibility guide](docs/compatibility.en.md) to understand what your host supports, including an explicit-read fallback. Repository helpers and onboarding documents are optional wrappers around the frozen workflow.

If this pass already has work and was only interrupted or is waiting for material, use the [same-run resume entry](docs/compatibility.en.md#resume-run) rather than restarting as a new independent exploration.

## Workflow

The two discovery routes begin with the same neutral contract. Each saves its first judgment before exchanging candidate judgments. Their synthesis feeds mechanism construction and revision.

```mermaid
flowchart TD
    Q0["Q0: neutral research contract"] --> T["Q1-T: domain-down discovery"]
    Q0 --> U["Q1-U: method-up discovery"]
    T --> S["Q1-S: compare and synthesize"]
    U --> S
    S --> Q2["Q2: opportunity sketches"]
    Q2 --> Q3["Q3: mechanisms and close neighbors"]
    Q3 --> Q4["Q4: substantive revision"]
    Q4 --> Q5["Q5: preserve independent proposal"]
    Q5 --> R["Q5-R: mandatory retrospective and repair"]
    R --> Q6["Q6: conditional reconciliation or skip"]
    Q6 --> P["Q6-P: optional pilot proposal or skip"]
    P --> A["Q7-A: comparison and resource assessment"]
    A --> B["Q7-B: final proposals and in-chat insights"]
```

Q5-R preserves the independent proposal and saves repairs separately. Q6 reconciles only authorized previous material after that review. First use can mark Q6 `not_applicable`; an explicitly skipped comparison can use `skipped`. A required but missing handoff remains `pending_handoff`.

Before the comprehensive Q7-B report, Q7-A answers four questions for each retained developed direction:

1. Where does the nearest work's answer actually stop?
2. What exact difference do we still want to answer?
3. Which real resources can answer it?
4. What decision would the result change?

Q7-A states the plan's actual readiness: executable within specified conditions, conditional, or incomplete. An unresolved main mechanism or resource gap is partial progress, not a completed Q7-B report. Filled headings and saved files do not establish completion or research quality.

<a id="second-pass"></a>

**Start pass 2:** complete pass 1 through Q7, then use a fresh context and workspace with the same neutral brief only. Follow the [frozen two-run guidance](docs/QUICKSTART.en.md#two-runs); the user/coordinator keeps pass-1 outputs outside pass-2 inputs and workspace through pass-2 Q5-R. An informed revisit must be described honestly; repeated sources do not provide independent confirmation.

<a id="pending-handoff"></a>

**When `pending_handoff` is reported:** check that pass-2's original Q5 and separate Q5-R repairs are preserved, then supply the authorized pass-1 package with its exact readable file scope, following the [frozen handoff guidance](docs/QUICKSTART.en.md#two-runs). Do not copy the whole prior project tree. Continue this pass through Q6 and later planning rather than restarting independent discovery.

## Examples

Read the [complete annotated case in English](examples/deadline-information/README_EN.md): public source understanding, concrete construction, separate Q5 original and repairs, formal comparisons, and an insight-rich final explanation. Its [two-pass handoff demonstration](examples/deadline-information/two-pass.md) shows the authorized packet and its delayed delivery, with English notes.

This is an **authored educational reconstruction, not a record of two actual independent runs**. Sources are real; candidate versions and the discovery storyline are teaching constructs. It includes no empirical performance, novelty claim, or evidence that the Workflow improves research quality. The original [short illustrative fragment](examples/README.md) remains available in Chinese.

The [actual public-topic case](docs/use-cases/forecast-uncertainty-2026-10-06/README.md#english-summary) retains public-source discovery, a concrete proposal, substantive paper repairs and comparison planning. Pass 1 remained incomplete on its main resources; pass 2 stopped before research because a host status tool exposed prior results. The user chose to retain this partial case without a replacement run. It is **not a completed two-pass exploration or efficacy validation**; see its [substantive assessment](docs/use-cases/forecast-uncertainty-2026-10-06/ASSESSMENT.md).

A run normally leaves a lightweight `RUN.md` index, independent proposals, separate retrospective and repair records, applicable reconciliation, comparison plans, and a final explanation. Actual scientific content and unresolved dependencies matter more than a file inventory.

Host support and the distinction between preparation and isolation are documented in [English compatibility](docs/compatibility.en.md). Optional integrations are described by the Skill; they are not required to use the workflow.

## Validation

From the repository root:

```bash
"$RDW_PYTHON" scripts/check_repo.py
"$RDW_PYTHON" -m unittest discover -s tests -v
```

These checks cover public repository contracts and behavior represented by fictional fixtures. They require no experiments, external model calls, or live topic research. Passing them does not prove proposal novelty, scientific validity, or experiment success. See [validation scope](docs/VALIDATION.md) for the checks and their limits.

If this is a new terminal, select and check `RDW_PYTHON` again before running these commands.

The [actual Codex CLI receipt](docs/validation-runs/2026-10-06-codex-cli/README.md#english-summary) retains six one-attempt fictional runs, sanitized output/artifacts and reported usage. These demonstrate the listed local reading and behavior paths, not internal auto-registration, child isolation or research quality. GUI and other hosts remain untested. Live capture is opt-in and consumes account quota; unit tests and CI never launch it.

For v1.4.0, **105 standard-library tests passed**; [installation calibration and outer checks](docs/validation-runs/2026-10-06-installation/README.md) retain their exact scope. The [native public-topic artifacts](docs/validation-runs/2026-10-06-public-topic/README.md) are not CLI events: full event capture and closed token costs remain unknown, and the failure and partial completion are preserved.

## Docs

| Read this | For |
| --- | --- |
| [English installation](docs/installation.en.md) | Install, inspect destinations, and update without overwriting |
| [Architecture](docs/architecture.md) | Repository layout and the roles of Skill, helpers, and documentation |
| [English compatibility](docs/compatibility.en.md) | Host capabilities, fresh-context limits, and optional integrations |
| [Annotated English case](examples/deadline-information/README_EN.md) | Understand concrete proposals, repairs and delayed handoff |
| [English neutral brief](examples/neutral-brief.en.md) | Editable optional starting input |
| [Frozen workflow](docs/FROZEN_WORKFLOW.md) | The scientific v1.0.0 boundary retained by repository v1.4.0 |
| [English quickstart](docs/QUICKSTART.en.md) | The original workflow usage guide |
| [中文启动提示](docs/STARTER_PROMPTS.zh-CN.md) | Chinese starter prompts |
| [Validation](docs/VALIDATION.md) | Package checks, fictional fixtures, and claims they cannot establish |
| [Provenance](docs/PROVENANCE.md) | Origins and attribution of the generalized workflow |
| [Contributing](CONTRIBUTING.md) | Public feedback and repository contributions |
| [Changelog](CHANGELOG.md) | Distribution changes and retained releases |

The package is distributed under the [MIT license](LICENSE). The installer includes the repository license in its installed payload outside the frozen scientific instructions.
