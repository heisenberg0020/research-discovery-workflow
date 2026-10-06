# Value of information before a deadline

This is an **authored, annotated, theory-only teaching reconstruction** of Q0–Q7. It includes intentionally erroneous originals, separate repairs, and scripted two-pass handoff. No two independent runs, independent review, experiment, simulation, model API, private-artifact use, or workflow-effectiveness validation took place. Stage labels describe the lesson's logical sequence, not an execution history.

The substantive lesson is that failure to receive a purchased signal by the deadline can itself be an observation. A timely-arrival probability times ordinary VOI is valid under an explicit sufficient condition such as independent erasure. The complete Bayesian decision is the established strongest comparator, not a new method here.

Start with the [English neutral brief](neutral-brief.en.md). Read [source scope and primary links](sources.md), then the path below. The Chinese artifacts are optional detailed derivations; this page gives the complete explanatory route. The [Chinese walkthrough](README.md) contains fuller annotations.

## Q0–Q7 in one route

**Q0.** The objective is theoretical from the beginning: establish the shortcut's conditions and separate status from content value. Real latency data are unqualified; this is not a late switch from an empirical objective. The author sees all files, and a directory neither clears history nor enforces access. There are no real prior results for pass 1.

**Q1-T / Q1-U.** The domain route asks what the decision maker can observe at the deadline and why buying information might change an action. The mechanism route compares choosing an action before observations with maximizing separately after each observation. They supply different questions before the scripted synthesis; two authored sections do not constitute unexposed workers.

**Q1-S.** Their bridge is the observation partition: “not arrived” can change beliefs, and the timely subset can have a different signal distribution. This changes the next question from estimating a marginal arrival rate to specifying the joint model. [Q0–Q4 artifact](pass-1/discovery.md).

**Q2–Q3.** Construct two objects: A, the shortcut's validity boundary; B, a status/content decomposition. Let state `θ`, action `a`, and signal `Y` be binary, utility be `1[a=θ]`, acquisition cost be fixed `c`, and arrival status be `R=1[L≤d]`. After purchase, at the deadline observe `Z=⊥` if late and `Z=(1,Y)` if timely. No purchase gives no observation of `R`. The prior and joint model are known; extra timestamps and metadata are excluded. The serious comparator is the best policy over this same `Z`.

**Q4.** Keep the classical answer and the explanatory task. Calling a rule new does not change its operations. The first shortcut's mistake remains visible for the Q5-R lesson; an actual run should repair an already-known mistake immediately.

**Q5.** Preserve the [intentionally wrong original](pass-1/q5-original.md): it claims `p(VY−V0)−c` for every arrival mechanism, falls back to the prior when late, and uses the ordinary posterior when timely. These claims are objects of review, not advice.

**Q5-R.** The [review](pass-1/q5-review.md) identifies the three consequential interfaces. With `w_{θyr}=P(θ,Y=y,R=r)`, the [repaired policy](pass-1/q5-repaired.md) has

`V0=max_θ Σ_{y,r}w_{θyr}`,

`VY=Σ_y max_θ Σ_r w_{θyr}`,

`VZ=max_θ Σ_y w_{θy0}+Σ_y max_θ w_{θy1}`.

Buy if `VZ−V0>c`; equality permits either choice. The late action uses `P(θ|R=0)` and the timely action uses `P(θ|R=1,Y)`. Zero-mass observations can take any action. If `R` is independent of the pair `(θ,Y)`, substitution yields `VZ−V0=p(VY−V0)`. Independence is sufficient, not necessary; independence from `θ` alone is insufficient.

For a transparent counterexample, take prior `1/2`, signal correctness `3/4`, and `R=1` exactly when `Y=1`. The nonzero masses `(θ,Y,R)` are `(0,0,0):3/8`, `(0,1,1):1/8`, `(1,0,0):1/8`, `(1,1,1):3/8`. Both arrival outcomes reveal `Y`, so `VZ=3/4` and gross gain is `1/4`; the shortcut gives `1/8`. At cost `3/16`, it rejects while the optimal rule buys. These are exact stipulated probabilities, not synthetic performance measurements.

To separate sources, let `VR=Σ_r max_θ Σ_y w_{θyr}`. Status value is `VR−V0`, and content value after status is `VZ−VR`; they sum to gross value and cost is subtracted once. In the counterexample, status accounts for the entire `1/4`, with no extra content value. In the control `R=1[Y=θ]`, status is independent of `θ` and has zero value, but timely content is perfectly correct: gross value is `3/8` rather than the shortcut's `3/16`. A pure-arrival control uses an independent fair `Y` and `R=1[θ=1]`: all value `1/2` comes from status. These controls fix the model and suppress content; they do not assume status can be purchased for free.

**Q6 / Q6-P.** Pass 1 marks reconciliation `not_applicable` and pilot `skipped`. The [scripted two-pass demonstration](two-pass.md) supplies a second original that mistakes conditional timely-content value for total acquisition value. It repairs that omission before showing an explicit three-file pass-1 package. This withholding is illustrative, not enforced. Reconciliation retains the stronger complete pass-1 expression; no second-pass victory or independent confirmation is inferred.

**Q7-A.** The [four-question plan](pass-1/final.md) identifies the classical comparator, the exact claims distinguished by derivation/controls, eligible formal resources, and result-to-decision branches. Its resources are the eight joint masses and finite policy sets. Holding the prior and signal fixed, four arrival probabilities each in `{0,1/2,1}` give 81 kernels. Exhaustively checking 8 full-observation policies, 4 status policies, 4 ordinary-signal policies, and 2 constant policies entails `81×(8×8+4×8+4×4+2×2)=9,396` weighted payoff contributions. This is a derived, unexecuted workload, not a timing or cost benchmark. The grid checks only that grid; the algebraic proof covers the stated general relationship. No empirical resource is certified.

**Q7-B.** The actionable synthesis is to price the actual observation, use the shortcut when its assumptions apply, and explain gains with the nested information sets `none → R → Z`. Any scheme under the same true model and information cannot exceed the full Bayesian optimum. The work delivered is a teaching derivation, analytic counterexample, and concrete formal plan; grid execution, real-world benefit, novelty, independent runs, and workflow effectiveness remain unclaimed. A future application must establish whether non-arrival is observable and whether its joint model can be identified.

## Artifact map

[Neutral brief](neutral-brief.en.md) → [source notes](sources.md) → [scripted discovery](pass-1/discovery.md) → [Q5 original](pass-1/q5-original.md) → [review](pass-1/q5-review.md) → [repair](pass-1/q5-repaired.md) → [comparison plan and explanatory report](pass-1/final.md) → [two-pass handoff](two-pass.md).

No stage asks the reader to infer missing operations from file names. These files are teaching artifacts, not prepared-run or isolation certificates.
