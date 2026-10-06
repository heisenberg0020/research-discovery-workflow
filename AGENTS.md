# Repository development instructions

This repository packages a general research-discovery and proposal-planning skill.

- Develop only within this repository. Do not scan neighboring research projects for examples or copy private research artifacts, conversations, local configuration, credentials, or personal paths into the package.
- Preserve the scientific behaviors in the skill: fresh-context discovery; separate domain-down and method-up first passes; concrete mechanism proposals; mandatory Q5-R retrospective and repair before prior-work reconciliation; conditional Q6; insight-rich in-chat final reporting.
- A prepared directory is not a sandbox, a fresh chat, or disabled memory. Do not claim capabilities that helpers do not implement.
- Scripts use Python's standard library. Test changes with `python3 -m unittest discover -s tests -v`. No experiments, external model calls, or live topic research are needed for package tests.
- Keep the skill self-contained. Optional upstream skills are referenced, not vendored. Do not add mandatory APIs, fixed paper counts, numerical idea scores, or experiment-success gates.
- Use fictional, explicitly labeled fixtures for behavior tests. Distinguish structural validation and dry-run behavior testing from proof of research quality.
- Do not install over an existing user skill or modify global agent configuration as a development step.

## Frozen workflow

- The user froze the workflow at `v1.0.0` / commit `894b429b51d2f3aeb35e5e4606260dbc91376e70`. Do not modify, add or remove files in `skills/research-discovery-workflow/`, or modify `docs/STARTER_PROMPTS.zh-CN.md` and `docs/QUICKSTART.en.md`, as part of repository construction.
- `docs/workflow-freeze.json` records the preserved file inventory and hashes. Do not change the baseline to make a failed check pass. A future workflow change requires an explicit user request distinct from repository improvement.
- New installation, packaging, presentation and contributor files belong outside the frozen Skill. These helpers do not add research stages, experiments or execution authority. Repository version changes are not workflow revisions.
