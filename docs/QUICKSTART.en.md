# English quick start

This agent skill turns field understanding into concrete research proposals and conditional plans. It supports method/value studies, phenomenon/explanation studies, better-method design, and other research contributions. It does not impose a domain, agent architecture, paper quota, idea score, positive pilot result or promise of novelty.

## Install

Import `skills/research-discovery-workflow/` into your agent's supported skill directory, without overwriting an existing copy. In Codex, the usual user skills location is `$HOME/.codex/skills/`. The package has a portable `SKILL.md` entrypoint and optional Codex UI metadata. Other hosts may need explicit loading; compatibility is not certified for every host.

## One run

Start a fresh, non-forked conversation in a clean workspace. Supply a neutral brief describing the field, scientific interests, negotiable boundaries and resource facts. Do not supply previous candidate reports at startup.

```text
Use $research-discovery-workflow for a complete research-discovery and planning pass.
Use only my attached neutral brief, the workflow, this run's outputs, and newly acquired public evidence. Implement the five isolation steps where supported and state actual limits.
Execute Q0–Q5, preserve the original independent proposal, then perform mandatory Q5-R retrospective and paper-only repair. There are no previous results, so mark Q6 not_applicable and continue.
Do not execute experiments; propose or skip optional pilots. Before the comprehensive report, complete Q7-A per direction: nearest answer at mechanism/condition/comparison level, two competing accounts and distinguishing observations, qualified real resources/splits and estimates, and result-to-decision branches. Then finish Q7-B with concrete mechanisms, conditional plans, and a substantial in-chat explanation of field insights, candidate origins, remaining-opportunity value, strong alternatives and next questions. Do not end with file links alone.
```

The five setup steps address fresh context, clean workspace, memory/inherited instructions, context-source scope, and normal-path verification. The skill cannot itself enforce host isolation. The optional `prepare_run.py` creates files only; it does not start a chat, clear memory, restrict tools or begin research.

## Two runs

1. Complete the first run through Q7, normally without previous-result reconciliation.
2. Start another fresh context with **the same neutral brief and skill only**. Keep first-run reports outside its inputs and workspace until the second run finishes Q5-R.
3. Then hand off the authorized first-run proposal/mechanism/source package for second-run Q6. Include relevant counterevidence; do not copy unrelated history.
4. Use the second run's final Q7 reconciliation as the practical output. It can retain a better first-run proposal or unresolved competing branches; a second pass is not intrinsically superior or empirical replication.

If the handoff is required but missing, report `pending_handoff`. With no old results, use `not_applicable`; an intentionally omitted comparison is `skipped`. Optional pilots can remain proposals, and a small negative result never mechanically kills an entire direction.

## Prepare a workspace (optional)

Create a neutral UTF-8 brief file and an existing parent directory, then run:

```sh
python3 skills/research-discovery-workflow/scripts/prepare_run.py \
  --root ./runs/pass-1 --brief ./neutral-brief.md --pass-number 1
```

The target must not already exist. Pass `2` for another equally blank workspace. The caller checks that the brief is truly neutral and configures any host-level boundaries separately.

## What completion means

Separate closed work, formed proposals, evidence adequate for particular claims, and completed validation. Keep the actual mechanism in the main proposal and chat explanation. A list of gaps is not a finished method; an articulated untested hypothesis can be a finished proposal. Stop after reporting unless the user asks for more.
