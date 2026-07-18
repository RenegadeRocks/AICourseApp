---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 7
day_name: sun
session_slug: market-user-validation-interview-or-poll-potential-users
date_due: 2026-08-02
tags: [synthesis, quiz, flashcards, block-4-capstone, ship-with-evidence, build-pivot-kill]
sources:
  - fitzpatrick-mom-test
  - gui-toubia-causal-inference
  - park-generative-agents-1000
  - nng-synthetic-users
  - nosek-preregistration-pnas
  - gascoigne-buffer-idea-to-customers
last_verified: 2026-07-17
word_count_target: 4600
---

# Synthesis — the week in one system, the block in one loop

## The week's argument, reconstructed

Week 11 built one machine with five interlocking parts, and the machine's purpose is stated most honestly in the negative: it exists to stop you from believing what you want to believe about your own idea.

**Monday** made the idea falsifiable: problem/customer/wedge pinned to a page, a bet sentence with numbers in its brackets, assumptions ranked by (probability wrong × cost if wrong), and, before any evidence existed, kill criteria and a decision rule, committed with a timestamp. The 2026 calibration that reorders everything downstream: for agent products, feasibility is rarely the binding risk; desirability usually is, with viability close behind, because you can build almost anything and so can everyone else.

**Tuesday** gathered the cheapest evidence class and installed the paranoia to match: deep-research agents for speed, bottom-up sizing only, alternatives mapped down to "paste it into ChatGPT," demand mined from communities in the customer's own words, and a standing verification protocol (two tools, date fences, citation walks, an error log), because AI desk research fails in five characteristic ways: it is stale, it inherits SEO slop, it flatters your framing, it launders fake specifics, and it hands your competitors the same homogenized "insights" it hands you.

**Wednesday** collected the only evidence that cannot be simulated: humans describing what they actually did. Mom Test discipline (their life, the past, your silence), the currency test (time, reputation, money; compliments score zero), consent-clean recording under 2026's live notetaker litigation, and synthesis as atomization: every claim tagged for/against/neutral per assumption, with a disconfirmation quota per interview.

**Thursday** faced the week's centerpiece controversy and drew the boundary: LLM-simulated users are real research artifacts (Park et al.'s interview-grounded agents hit 85% of human test-retest consistency on the GSS) *and* systematically unreliable where validation needs them most: too agreeable,[^7] ~50% on treatment effects, tails sanded off. The protocol that survives both literatures: simulate to design studies, humans to decide; synthetic evidence carries weight zero in the ledger, forever, with an audit trail when you are tempted otherwise.

**Friday** climbed the cost ladder of quantitative evidence (waitlist → fake door → pre-order → paid pilot), re-aimed the Week 10 page as an instrument, read every count as a Wilson interval rather than a point, and assembled the evidence ledger: class-weighted, direction-tagged, pre-registered thresholds, mechanical verdict. For agent products it added the metric that outranks all others: delegation depth, not signups.

**Saturday** made it run: the five-day sprint, two stdlib tools (`evidence_ledger.py`, `note_synthesizer.py`), per-interview synthesis with blind audits, a scheduled verdict, and a witnessed decision memo.

The single sentence, if you keep only one: **decide how you will decide before you collect anything, price evidence by what it cost the source, and let no simulated yes stand in for a human one.**

## Block 4 capstone recap — package, launch, validate: one loop

Block 4's three weeks compose into the course's commercial engine, and the composition matters more than any week alone.

**Week 9** ([[../week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/_week|lessons]] (pending)) turned a build into a *package*: a named offer with a scope, a price, and a deliverable shape a stranger can buy without buying you. **Week 10** ([[../week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/_week|lessons]] (pending)) gave the package a *launch surface*: the landing page, the CTA, the AI-generated creative pipeline. **Week 11** supplied the *verdict layer*: the evidence that says whether the package deserves the launch, and the instrumentation that turns the launch surface itself into a measuring device.

Run in course order, the block reads package → launch → validate. Run in *life* order, for every idea after this one, the loop inverts and closes:

1. **Validate** (W11): bet sentence, assumption map, kill criteria; desk → interviews → smoke test; ledger verdict.
2. **Package** (W9): only what survived gets a name, a scope, and a price, and the price is anchored in atoms (what the workaround cost, what the pilot paid), not in hope.
3. **Launch** (W10): the page and creatives ship what the interviews phrased, in the customer's verbatim language, instrumented from birth because W11 taught you pages are instruments.
4. **Loop**: launch data (behavioral atoms, at scale) feeds the next ledger; delegation-depth metrics from pilots feed the next package revision. The wheel turns; the ledger schema never changes.

That loop, running quarterly on your own products and rentable to clients as a validation engagement, is Block 4's real deliverable. The block's through-test still applies to every turn: Seibel's "would a customer actually pay?" gates entry to packaging; Hamel's "is that claim measured?" gates everything that claims to be evidence.[^8]

What Block 5 inherits: a decision (BUILD, or a pre-named PIVOT already in motion, or a clean KILL with salvage), a working evidence pipeline, and, whatever the verdict, ten humans in your niche who now know you do research before you sell. That last asset compounds longest.

## Quiz — take it cold

Answer before scrolling to the key. Mix of recall, application, and judgment.

**Q1.** Monday's bet sentence requires a "specific behavioral commitment" in its final bracket. Give two examples that qualify and two stated responses that do not, and name the principle that separates them.

**Q2.** For agent products in 2026, which of Cagan/Bland's risk categories is *usually* the binding one, and what are the three named exception classes where feasibility stays on top?

**Q3.** Your research agent returns: "The AI meeting-assistant market is $4.2B growing 38% CAGR (source: industry report)." List three distinct reasons this claim, as evidence for *your* wedge, should score at or near zero in the ledger even if the number is accurate.

**Q4.** What killed GummySearch, and what standing lesson does it teach about demand-signal tooling and about product ideas generally?

**Q5.** Rewrite this interview question to be Mom-Test-compliant: "Would you pay $200 a month for an agent that updates your CRM after every client call?" Then state what evidence class the *original* question's answer would have produced, and its strength score under the week's rubric.

**Q6.** An interviewee says: "This sounds amazing, I'd definitely use it. I'm slammed this month, but circle back anytime." Tag this as atoms: direction(s), strength(s), and the rule(s) applied.

**Q7.** State the two headline findings that anchor the FOR and AGAINST cases on synthetic users: one from Park et al. (2024), one from Gui & Toubia. Include the numbers.

**Q8.** Why does the week's protocol permit synthetic panels for interview-guide piloting but forbid them as desirability evidence? Answer in terms of what property the output needs downstream, not in terms of accuracy percentages.

**Q9.** Name the mechanism by which RLHF-style post-training corrupts simulated-customer research specifically, and the documented direction of the resulting error in agentic evaluations.

**Q10.** Order the smoke-test ladder by evidence strength and state what makes each rung stronger than the one below it. At which rung does a B2B agent product's *viability* usually become decidable, and why not earlier?

**Q11.** Your fake-door test: 6 signups from 90 warm visitors against a pre-registered 4% floor. The Wilson 95% interval is approximately [3.1%, 13.7%]. What is the verdict under Friday's read rule, and what are your two legitimate next moves?

**Q12.** In the ledger's default weighting, why is `desk` 0.5 rather than 0? And why is `synthetic` 0 rather than 0.5? The asymmetry is the answer.

**Q13.** The sprint requires the Day 5 verdict to run at a scheduled time regardless of evidence completeness. What failure mode does this rule target, and what legitimate output exists for incomplete evidence?

**Q14.** Your ledger returns KILL and you feel a strong pull to override. Under the week's system, what must an override produce, and which two artifacts exist specifically to make the override expensive?

**Q15 (block capstone).** Trace one concrete data path by which Week 11's outputs should change a Week 9 package and a Week 10 page, one each.

### Answer key

**A1.** Qualify: scheduling a paid pilot with a date; making an intro to a colleague; a pre-order/deposit; a scheduled workflow walkthrough with real data. Don't qualify: "I'd definitely use that," "great idea," survey enthusiasm, a hypothetical price acceptance. Principle: commitments cost the giver currency (time, reputation, money); words cost nothing, and evidence is priced by what it cost the source.

**A2.** Desirability is usually binding (with viability adjacent), because building capability is abundant and cheap in 2026 while attention and behavior change are not. Exceptions where feasibility leads: reliability-threshold workflows (zero-error tolerance), data-access-dependent products, and latency/cost-envelope products.

**A3.** (1) Top-down category size says nothing about your wedge's reachable buyers (bottom-up rule); (2) unverified provenance: analyst headline numbers routinely launder through citation chains (Tuesday's verification protocol); (3) category tailwinds are the weakest admissible class (`desk`, 0.5×) and touch no specific assumption; a growing category is fully compatible with zero demand for your wedge. (Also acceptable: homogenization means every competitor holds the same claim.)

**A4.** It failed to secure a commercial license under Reddit's Data API terms (commercial access ~$0.24/1,000 calls) and shut down. Lessons: method over tool (search operators and thread-reading survive any tool's death), and platform dependence is a first-class viability assumption for any product built on someone else's data faucet.

**A5.** Compliant version, e.g.: "Walk me through what happened after your last client call: what got updated where, by whom, and how long did it take?" (past, specific, no idea exposure, no price hypothetical). The original produces stated-class hypothetical enthusiasm: strength 0 by the compliment/hypothetical rule.

**A6.** Two atoms: the compliment ("sounds amazing, definitely use it") is NEUTRAL, strength 0 (compliments score zero by rule); the deferral ("circle back anytime") without a scheduled date is NEUTRAL/soft-AGAINST on commitment, strength 0–1: an invitation that cost nothing. No FOR atom exists in this quote. Rules: currency test; prefer AGAINST/NEUTRAL when ambiguous.

**A7.** FOR: Park et al., interview-grounded generative agents of 1,052 real people replicated their GSS answers at 85% of the participants' own two-week test-retest consistency (requiring ~2 hours of real interview per agent). AGAINST: Gui & Toubia, LLM simulations replicated only ~50% of aggregate treatment effects across 11 behavioral-economics experiments, due to prompt-induced confounding.

**A8.** Guide piloting needs outputs that are *design feedback*: a confusing question is confusing regardless of whether the simulated respondent resembles any human, and the flaw gets verified by the instrument's later human use. Desirability evidence needs outputs that are *costly signals from the population under study*, which simulation cannot supply: nothing was at stake for the sayer, so the yes carries no information. The downstream check exists in the first case and is absent in the second.

**A9.** Post-training optimizes for helpful, agreeable responses to the prompter; the persona mask does not remove that disposition, so simulated customers drift accommodating. Documented direction: simulated users are systematically more cooperative and inflate success rates (with structured miscalibration by task difficulty) in agentic-evaluation studies.

**A10.** Waitlist < fake door < pre-order/deposit < paid pilot. Each rung raises the cost of the visitor's action (email → click-through-past-a-price believing it real → money down → money plus real workload plus reputation). B2B agent viability usually becomes decidable only at paid pilot, because seat-price willingness, delegation trust, and workflow fit are revealed only when real work and real money move; everything below measures curiosity.

**A11.** 6/90 ≈ 6.7%, but the interval [3.1%, 13.7%] contains the 4% floor, so the pre-registered read is "threshold inside interval → collect more n," not pass. Legitimate moves: extend the window/traffic to the pre-registered larger n, or escalate a rung (e.g., pilot offers) if the decision rule's EXTEND clause allows substitution. Illegitimate: declaring 6.7% > 4% a pass.

**A12.** Desk evidence is weak but *human-generated*: it summarizes real behavior (job postings, paid workarounds, community complaints), so it carries small non-zero weight. Synthetic output is generated by a model with no stakes and a documented agreeable drift, and its errors correlate with the founder's hopes; any non-zero weight invites substitution creep. The asymmetry: weak real signal versus confident non-signal.

**A13.** It targets indefinite deferral: "we'll decide when we know more" converting validation into a permanent lifestyle (the research-museum failure). The legitimate incomplete-evidence output is EXTEND: a named evidence class, a specific additional n, and a new verdict date, i.e., a decision *about the deciding*, on schedule.

**A14.** An override must produce a written reason, logged in the ledger's override record and reproduced in the decision memo, which is shared with a witness (peer/office hours). The two artifacts making it expensive: the pre-registration commit (proving what past-you said would count) and the printed override trail in every future verdict run.

**A15.** Examples (any faithful pair): W9 package: interview atoms revealed the valued piece is CRM/task plumbing, not drafting, so the package's named deliverable and price anchor (what the dead Zapier workaround cost, what the pilot paid) change accordingly. W10 page: headline rewritten into the customers' verbatim pain language from interview quotes, and the CTA moved up the smoke-test ladder (from waitlist capture to pilot-request with visible price), with events pre-registered as ledger instruments.

## Flashcards

Import into the app or Anki. Front → Back.

1. Bet sentence (Monday) → We believe [customer] experiences [problem] at [frequency], handles it with [alternative] at [cost], and enough will [behavioral commitment] for [wedge]. Every bracket falsifiable.
2. The 2026 risk ranking for agent products → Desirability usually binding; viability next; feasibility rarely (exceptions: reliability-threshold, data-access, latency/cost-envelope products).
3. Riskiest Assumption Test (RAT) → Don't build the smallest product; design the smallest test of the deadliest assumption (Higham).
4. Kill criteria timing rule → Written and committed BEFORE evidence gathering; the commit timestamp is the pre-registration receipt (Nosek: prediction vs postdiction).
5. Escape-hatch inventory → Pre-naming the excuses you'll reach for if evidence is bad; makes motivated reasoning observable in real time.
6. Vitamin / painkiller / fine-you're-fired → Nice-to-have / named recurring cost / consequence-bearing task with an accountable human. Agents adopt fastest at rung 3, which also carries the highest reliability bar.
7. The ChatGPT-default test → Your real competitor is a $20/month chat subscription plus paste; the wedge must name its delta: plumbing, reliability, accountability, or workflow position.
8. TAM theater → Top-down category sizing ("0.1% of $47B"); replaced by bottom-up: reachable buyers × plausible penetration × price.
9. Two-tool rule (desk research) → Same falsification-framed brief through two vendors' research agents; diff; only cross-corroborated claims promote. Contradictions are gold.
10. Five failure modes of AI desk research → Recency gaps, SEO-slop inputs, sycophantic synthesis, fabricated/laundered specifics, homogenized insight.
11. Citation spot-check scores → VERIFIED / LAUNDERED / FABRICATED / UNVERIFIABLE; assume any single citation wrong until walked to a primary source (CJR/Tow prior).
12. Homogenization evidence (one line) → Doshi & Hauser: AI-assisted work is individually better, collectively more similar; cross-model clustering replicates it; your AI "insights" are everyone's.
13. Mom Test, three rules → Their life, not your idea; specific past, not hypothetical future; talk less, listen more.
14. Currency of commitment → Time, reputation, or money. Compliments score zero by rule.
15. Workaround excavation (agent products) → "What have you tried?" then follow the AI attempt down: the failure story of the horizontal default maps your wedge.
16. Interview guide, five movements → Context → The last time (full story) → Workarounds & spend → Stack rank → Currency close (idea last, asks graduated).
17. All-party consent, 2026 → 12 US states require every participant's consent to record; affirmative spoken consent on tape; calendar-invite disclaimers insufficient; no autonomous notetaker bots (Otter wiretap suits, Fireflies BIPA).
18. Evidence atom → One claim, one source, one quote: tagged assumption + direction (for/against/neutral) + strength 0–5 + class + channel.
19. Disconfirmation quota → Extract ≥1 AGAINST/NEUTRAL atom per interview before any FOR atoms; a synthesis with none is measuring the synthesizer.
20. Synthetic users, three-way taxonomy → LLM-as-respondent (peril lives here) vs AI-moderated research on real humans (evidence is real) vs simulated users as system test harness (legitimate diagnostic).
21. Park et al. 2024, headline → 1,052 interview-grounded agents; 85% of humans' own GSS test-retest consistency; needed 2h of real interview each; beat demographic personas.
22. Gui & Toubia, headline → Prompt "treatments" violate unconfoundedness; only ~50% of aggregate treatment effects replicate across 11 experiments; simulated experiments ≈ observational studies.
23. NN/g verdict on synthetic users (Rosala & Moran) → Shallow, one-dimensional, sycophantic; marginal use for broad attitudes; "user research needs real users."
24. "Lost in Simulation" findings → Simulated users more cooperative, inflate success, miss demographic patterns, ±9pp across user-LLMs, miscalibrated by difficulty; salvage: system-defect diagnostics.
25. The synthetic-users protocol → Simulate to DESIGN (guides, copy variants, hypotheses, rehearsal); humans to DECIDE; synthetic weight 0.0 in the ledger; disclosure mandatory.
26. Why simulation fails (mechanisms) → Trained-in sycophancy; personas = training-distribution priors; no stakes = no information; staleness and demographic flattening.
27. Poll design, four rules → Behavior before attitude; no idea exposure first; one decision per survey; screen respondents, log channel. (Pew: wording moves answers double digits.)
28. Smoke-test ladder → Waitlist < fake door < pre-order/deposit < paid pilot; ordered by what the action costs the actor; start at the highest rung your assets allow.
29. Wilson-interval read rule → State k/n as its 95% interval; if the pre-registered threshold sits inside the interval, the verdict is "collect more n." Canonical math: Block 2 Week 3 Sat.
30. Ledger class weights (default) → paid 5.0 · behavioral 3.0 · stated 1.0 · desk 0.5 · synthetic 0.0; fixed before evidence; changes after = logged overrides.
31. Agent-product validation metrics → Delegation depth over signups: tasks/week routed through the agent, return-after-first-failure, escalation acceptance, renew-at-full-price.
32. Sprint structural rules → Evidence classes unlock in cost order; nothing re-registers silently after Day 1; the verdict is calendar-scheduled (EXTEND is legal, deferral is not).
33. Blind audit (synthesizer) → Random sample of FOR atoms re-tagged by a human without seeing stored tags; >1 in 5 direction disagreement = tagging run not decision-grade.
34. Block 4 loop → Validate (W11) → package what survived (W9) → launch instrumented (W10) → launch data feeds the next ledger. Gates: Seibel "would they pay?"; Hamel "is it measured?"

## Sunday-night ritual

1. Ten minutes on the cards above.
2. Quiz cold; below 80% → `/deepen-lesson` on the weakest day Monday.
3. Fill the "what surprised me" card. (Likely candidate: how it felt to watch the synthetic panel be confidently wrong about your own idea.)
4. Write the three-line post-mortem in `_week.md`: what you'd tell the you from last Monday.
5. Check the sprint calendar: interviews scheduled, smoke window set, Day 5 verdict blocked out. The week's real exam happens there.

## Citations

[^1]: Rob Fitzpatrick, *The Mom Test* (2013). https://www.momtestbook.com/

[^2]: Joon Sung Park et al., "Generative Agent Simulations of 1,000 People," arXiv 2411.10109 (2024). https://arxiv.org/abs/2411.10109

[^3]: George Gui & Olivier Toubia, "The Challenge of Using LLMs to Simulate Human Behavior: A Causal Inference Perspective," arXiv 2312.15524. https://arxiv.org/abs/2312.15524

[^4]: Maria Rosala & Kate Moran (NN/g), "Synthetic Users: If, When, and How to Use AI-Generated 'Research'." https://www.nngroup.com/articles/synthetic-users/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Brian A. Nosek et al., "The preregistration revolution," *PNAS* 115(11), 2018. https://www.pnas.org/doi/10.1073/pnas.1708274114

[^6]: Joel Gascoigne, "Idea to Paying Customers in 7 Weeks," Buffer, 2011. https://buffer.com/resources/idea-to-paying-customers-in-7-weeks-how-we-did-it/

[^7]: "Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations," arXiv 2601.17087 (2026). https://arxiv.org/html/2601.17087v1 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Hamel Husain, "A Field Guide to Rapidly Improving AI Products," March 2025. https://hamel.dev/blog/posts/field-guide/ — the measurement gate that runs through Block 4.

_last_verified: 2026-07-17_
