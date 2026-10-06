# Repository development instructions

This repository packages a general research-discovery and proposal-planning skill.

- Develop only within this repository. Do not scan neighboring research projects for examples or copy private research artifacts, conversations, local configuration, credentials, or personal paths into the package.
- Preserve the scientific behaviors in the skill: fresh-context discovery; separate domain-down and method-up first passes; concrete mechanism proposals; mandatory Q5-R retrospective and repair before prior-work reconciliation; conditional Q6; insight-rich in-chat final reporting.
- A prepared directory is not a sandbox, a fresh chat, or disabled memory. Do not claim capabilities that helpers do not implement.
- Scripts use Python's standard library. Test changes with `python3 -m unittest discover -s tests -v`. No experiments, external model calls, or live topic research are needed for package tests.
- Keep the skill self-contained. Optional upstream skills are referenced, not vendored. Do not add mandatory APIs, fixed paper counts, numerical idea scores, or experiment-success gates.
- Use fictional, explicitly labeled fixtures for behavior tests. Distinguish structural validation and dry-run behavior testing from proof of research quality.
- Do not install over an existing user skill or modify global agent configuration as a development step.
