---
name: research-discovery-workflow
description: "Discovers worthwhile research questions and builds concrete, evidence-grounded proposals and conditional plans through isolated exploration, domain-down and method-up discovery, critical reading, mechanism construction, independent retrospective repair, and optional prior-result reconciliation. Use for open-ended research topic selection, literature-to-idea synthesis, explaining a phenomenon or a method's value, designing a better method, or fresh two-pass exploration in any research field. Not for a simple paper summary, implementing an already fixed method, or resuming a frozen experiment."
---

# Research Discovery Workflow

Turn understanding of a field into a concrete research proposal, not merely a list of gaps or a completed set of documents. Work in the user's language. Default to literature, theory, and static code understanding; a planning request does not by itself launch experiments.

## Essential behavior

1. **Explore before inheriting answers.** Use a fresh context and a clean, scoped workspace where possible. Keep previous candidates, architectures, rankings, and results out until Q6. State actual isolation limits; a new directory or a “forget the history” prompt does not clear context or memory.
2. **Understand and create together.** Keep domain-down and method-up discovery distinct before synthesis. A credible opportunity from either route can survive. Allow explicit hypotheses and new operations without requiring prior empirical success.
3. **Judge claims, not labels.** Separate relevance, competitive strength, and sufficient solution. Related work can supply a better baseline or design principle, not just a rejection. Connect the specific remaining opportunity to a meaningful consequence.
4. **Deliver the mechanism.** Expand the actual explanation, intervention, algorithm, or theoretical object. Preserve its defining relationships and operations in the main proposal. File completion, caution, and novelty searches do not substitute for a proposal.
5. **Review before merging; explain after deciding.** Save Q5 unchanged, perform mandatory Q5-R review and separate repairs, then conditionally reconcile old results. Q7 ends with an insight-rich explanation in the conversation as well as saved planning artifacts.

## Start or resume

For a new run, read [isolation](references/isolation.md) and [discovery](references/discovery.md) completely before starting. Establish the topic, goal, common neutral brief, output root, evidence scope, stop point, and whether one or two passes are requested. Unknown resources may become planning conditions; they need not block public discovery.

For a resume, inspect the run's state and actual current proposals. Verify what was substantively completed, what evidence was read, whether T/U have already exchanged judgments, and whether old results have been seen. Do not infer completion from filenames or re-label a merged context independent. Resume the earliest unresolved dependency within the existing authorization; do not restart to obtain nicer ideas.

Record lightweight state in `RUN.md`: scope and pass number; actual isolation; current phase; T/U first-pass exposure; evidence/idea/validation status; previous-material availability and authorized scope; output index and next action. This is an index, not a mandatory database or proof of quality.

## Ordered stages

| Stage | Entry and work | Exit |
|---|---|---|
| Setup | New-run intent; implement the five isolation steps as supported | Neutral inputs and actual boundaries established, limits disclosed |
| Q0 | Clarify topic, research goal, negotiable boundaries, evidence cutoff and resources | A usable research contract, not a preselected answer |
| Q1-T / Q1-U | Same neutral contract; separately explore field needs and working mechanisms | Each first judgment saved before exchanging candidate judgments |
| Q1-S | First-pass findings available | Substantive comparison, changes in understanding, and concrete onward questions; missing routes labeled |
| Q2 | Evidence sufficient to discuss an opportunity, including conditional hypotheses | Distinct opportunity sketches linked to mechanisms and consequences |
| Q3 | Sketches exist | Concrete mechanisms, claim-specific close-neighbor analysis, support/challenge and distinguishable predictions |
| Q4 | Candidate-changing evidence or logic exists | Substantive revision, technical comparison or reasoned reselection, not merely extra caveats |
| Q5 | Independent work ready for bounded synthesis | Independent proposal/plan saved unchanged; actual completeness stated |
| **Q5-R** | Q5 original preserved; no previous research results read | Independent retrospective, specific paper-only repairs and research-core clarification saved separately; unresolved issues stated |
| Q6 | Q5-R done; previous results, if any, have an authorized handoff | Scoped reconciliation, explicit `not_applicable`/`skipped`, or honest `pending_handoff` |
| Q6-P | Q6 completed or skipped | Optional pilot proposal, justified skip, or authorized result; never a positive-result gate |
| Q7-A | Repaired proposals and applicable reconciliation available | Per-direction executable comparison design and resource assessment: four questions answered before comprehensive reporting |
| Q7-B | Q7-A substantively completed, with actual readiness/conditions stated | Final proposals, conditional plan, and detailed in-chat insight report; then stop |

Full exploration/planning authorization covers ordinary stage progression and public rereading; do not ask again at every stage. Honor narrower requested stop points. If the user requires reconciliation but its handoff is missing, report the pending portion without falsely claiming it completed. No prior material on first use is normal: explicitly mark Q6 `not_applicable` and finish Q7.

## Read at the relevant stage

- [Discovery](references/discovery.md): Q0, Q1-T/U/S, Q2; dual-route reasoning and opportunity formation.
- [Evidence and mechanisms](references/evidence-and-mechanisms.md): Q2–Q4 and later revisions; primary-source reading, close neighbors, concrete research objects, bounded iteration.
- [Independent review and repair](references/independent-review-and-repair.md): Q5 and mandatory Q5-R; preserve originals, inspect scientific content, repair, clarify the research core.
- [Reconciliation and planning](references/reconciliation-and-planning.md): Q6/Q6-P/Q7; first-use branches, two-pass operation, claim-scoped comparison, conditional validation.
- [Comparison plan](references/comparison-plan.md): mandatory Q7-A **before** the comprehensive insight report; nearest answer, two competing accounts and distinguishing observations, real resource qualifications/estimates, result-to-decision branches.
- [Insight reporting](references/insight-reporting.md): Q7's saved report and **conversation** report; explain what was learned and why these proposals emerged.
- [Upstream capabilities](references/upstream-capabilities.md): optional integration with seven Phase 0 skills. The workflow is self-contained; do not install them or activate paid services just to check a usage box.

Read each selected instruction file fully yourself before acting on it. Delegation may perform source reading and proposal work, not replace reading the workflow instructions. Give fresh workers the same neutral scope and batch work by question cluster rather than one worker per paper. Recheck original passages that drive decisive scientific judgments.

## Two-pass usage

When the user requests two passes, complete pass 1 through Q7 (normally without old material). Run pass 2 in a fresh context with the same neutral brief and workflow, withholding pass-1 results through pass-2 Q5-R. Only then stage the approved pass-1 package for Q6. The pass-2 Q7 deliverable is the practical synthesis, but it may preserve a stronger pass-1 idea or retain competing branches. Repeated sources are not independent confirmation; a second run is not automatically better.

If starting in a context already exposed to pass 1, do not claim a clean second pass. Use a fresh main conversation or a genuinely fresh worker with only the neutral packet when supported; otherwise label an informed revisit and explain the limit.

## Optional workspace helper

`scripts/prepare_run.py --root NEW_DIRECTORY --brief NEUTRAL_BRIEF --pass-number 1` (or `2`) creates a non-overwriting workspace with a copy of this skill and the supplied brief. It does **not** create a conversation, clear memory, restrict tools, enforce file access, assess the brief's neutrality, or start research. Read the isolation instructions before treating the directory as an execution environment.

## Completion check

Before closing, verify Q7-A's actual comparison design and resource assessment for the retained main question, not merely a completed subproblem, then compare final prose against the repaired mechanisms: no defining relationship or operation should have been lost during compression. Explain the existing answer, the proposed addition, and the difference that would make the research meaningful. Separate **work closed**, **proposal formed**, **evidence sufficient for stated claims**, **comparison-plan readiness**, and **validation completed**. An unresolved mechanism or main-plan resource gap can be honestly delivered as partial progress, not disguised as a mature plan or completed Q7-B. End with the substantial in-chat synthesis after Q7-A, not a file inventory. Do not automatically begin another run or experiment.
