---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 6
day_name: sat
session_slug: market-user-validation-interview-or-poll-potential-users
date_due: 2026-08-01
tags: [build-day, validation-sprint, evidence-ledger-tool, note-synthesizer, for-against-tagging, claude-cli, pre-registration, build-pivot-kill, sprint-planning]
sources:
  - fitzpatrick-mom-test
  - bland-testing-business-ideas
  - husain-field-guide-2025
  - gv-design-sprint
  - park-generative-agents-1000
  - lost-in-simulation-2026
  - waitlister-statistics
  - nyu-shipping-not-asking-2026
last_verified: 2026-07-17
word_count_target: 5000
---

# BUILD — run the validation sprint: five days, one defensible decision

## Why this matters

Build days in this course have meant shipping agents. Today you ship a *decision system*: a five-day validation sprint for your own idea, powered by two tools you will assemble and run from `code-lab/6/`. The sprint's deliverables are the week's artifacts assembled into motion: a frozen assumption map, a desk dossier with verified sources, five interviews scheduled with a piloted guide, one live smoke test, and an evidence ledger that returns BUILD, PIVOT, or KILL under the rule you registered before evidence existed. The tooling matters beyond this week for a commercial reason Friday's reviewer lens already spotted: an evidence ledger with provenance, for/against tagging, and an auditable verdict is a *sellable research artifact*. The consultant who shows up to a discovery engagement ([[03-wed-discovery-calls-and-qualification|Block 1 Week 1 Wed]]) with this pipeline is charging for evidence discipline, not opinions. Today's version is aimed at the client you are least honest with: yourself.

## Prerequisites

- Monday's `validation/00-bet.md` (frozen, committed). The sprint imports its assumptions verbatim.
- Wednesday's interview guide and ≥1 real transcript; Thursday's synthetic boundary memo; Friday's pre-registered smoke-test read.
- Python 3.10+ and optionally the `claude` CLI on PATH. The code-lab is stdlib-only; everything runs without an API key ([`code-lab/6/README.md`](code-lab/6/README.md) has the exact commands).
- 2–3 focused hours today for setup; the sprint itself spans the coming week alongside your other work.

## Layer 1 — Sprint architecture: why five days, and what each day must produce

The shape borrows deliberately from the GV Design Sprint (Knapp et al.): a time-boxed week, artifacts due daily, a decision at the end, and, crucially, the *decision criteria fixed before the week begins*.[^1] The GV sprint validates a solution prototype; yours validates a bet. Same skeleton, different payload:

| Day | Produce | Evidence class unlocked |
|---|---|---|
| 1 | Ledger initialized; assumptions + kill criteria registered; decision rule committed | none (pre-registration) |
| 2 | Desk dossier finalized; atoms imported; guide piloted (synthetic, weight 0) | `desk`, `synthetic` (design only) |
| 3–4 | Interviews 2–5 completed and synthesized; smoke test live | `stated` |
| 4–5 | Smoke-test window runs; pilot offers made to warmest prospects | `behavioral`, `paid` |
| 5 | Ledger verdict; decision memo written and shared | the verdict |

Three structural rules keep the sprint honest:

1. **Evidence classes unlock in cost order.** Cheap evidence early (it shapes instruments), expensive evidence late (it decides). Bland's experiment-sequencing logic, compressed.[^2]
2. **Nothing re-registers after Day 1.** New assumptions discovered mid-sprint (they will be; interview Movement 4 generates them) enter the ledger flagged as late additions with reasons, which the tool records as overrides. They can be *tested*; they cannot quietly replace the assumptions that were failing.
3. **The verdict is scheduled.** Day 5's ledger run happens at a calendar time you set today, whatever state the evidence is in. "We'll decide when we know more" is how validation becomes a lifestyle. An incomplete-evidence verdict of "extend: collect n more atoms of class X by date Y" is a legitimate output; an unscheduled verdict is not.

## Layer 2 — The toolchain: what you are running and why it is shaped this way

`code-lab/6/` ships two stdlib-only Python tools; the README's quickstart runs the full loop on bundled sample data in five minutes. Architecture notes worth internalizing before you run them:

**`evidence_ledger.py`** is pre-registration as software, Nosek's prediction-vs-postdiction distinction compiled into a file format.[^8] `init` writes the class weights (`paid` 5.0, `behavioral` 3.0, `stated` 1.0, `desk` 0.5, `synthetic` 0.0) and a default decision rule into `ledger.json`; you edit them once, then commit, and the commit hash is your receipt. `add-assumption` refuses silent late additions once evidence exists (they require `--reason`, which lands in an override log the verdict prints back to you). `verdict` evaluates the registered predicates and always displays the *strongest single AGAINST atom* per assumption, because Friday taught you that averages hide the quote that should be haunting you. `wilson` is a one-liner port of the [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]] interval discipline (E. B. Wilson's 1927 score interval[^6]) for reading smoke-test counts.

**`note_synthesizer.py`** is Wednesday's atomization protocol, automated. Claude mode shells out to the `claude` CLI (`claude -p`, the same pattern as this course's app), with a prompt whose two non-obvious design choices come straight from the week's research: it instructs the model to tag *ambiguous statements AGAINST or NEUTRAL, never FOR* (countering the documented sycophantic drift of LLM judgment[^3]), and it refuses FOR atoms without verbatim quotes (making every optimistic tag auditable against source text). The `--offline` mode is a deliberately crude keyword tagger; run it once on your real transcripts and compare with Claude mode's output, and you will viscerally understand why labeling quality, not pipeline plumbing, is where synthesis lives or dies (Hamel Husain's field-guide thesis, enacted[^4]). The `--audit N` command samples FOR atoms for blind re-tagging, the inter-annotator check Wednesday's reviewer lens demanded; the underlying principle (machine judgment is trustworthy only after its alignment with human judgment is measured) is Shankar et al.'s validator-validation result, ported from LLM evals to evidence tagging.[^7]

The boundary rule from Thursday is enforced mechanically: atoms ingested with `--source-class synthetic` carry weight 0.0, never satisfy any predicate, and the tools print the reminder every time you touch them. You *can* defeat this by editing JSON in a text editor. The tool's job is to make self-deception explicit, not impossible; nothing can make it impossible.

## Layer 3 — Day 1 in full: registration (do this today)

Work through this now; it is today's build. Commands are abbreviated; the README carries full flags.

**Step 1 — Initialize and register (30 min).**

```bash
cd code-lab/6
python evidence_ledger.py init --ledger ledger.json
# One add-assumption per Monday assumption, verbatim text, quantified kill criteria:
python evidence_ledger.py add-assumption --ledger ledger.json \
  --id A1 --category desirability \
  --text "<your assumption, with its number in it>" \
  --kill "<your kill criterion, quantified>"
```

Then open `ledger.json` once: adjust class weights only if you have a written reason (put the reason in a comment file next to it), replace the default BUILD thresholds with numbers matched to *your* sprint scale (the default `min_for_mass_desirability` of 12.0 assumes roughly five stated atoms of strength 3–4 or one paid atom plus change; scale to your planned n), and rewrite the PIVOT clause to name your axis in advance ("if A1 passes and A3 fails, pivot the wedge to the plumbing use case; customer unchanged"). Commit.

**Step 2 — Backfill the week (30 min).** Everything this week already produced becomes atoms: dossier findings (`--source-class desk`), your first interview (run the synthesizer on `validation/interviews/`), the smoke-test pre-registration (a placeholder atom noting thresholds, replaced by real counts when the window closes). Run `verdict` once now. It should return NOT build-grade with mostly-empty checks. That baseline printout is worth keeping: it is what an evidence-free conviction looks like, formatted honestly.

**Step 3 — Schedule the sprint (15 min).** Calendar entries, now, with real times: the five interview slots (from Wednesday's recruiting), the smoke-test window open/close, the Day 5 verdict run, and a 30-minute "decision memo" block after it. The sprint exists once these are on the calendar and not before.

**Step 4 — Pilot the guide, synthetically, correctly (30 min).** Thursday's divergence audit doubles as guide QA. Run your five-persona panel, feed the transcripts through the synthesizer with `--source-class synthetic`, and read the output *only* for instrument defects: questions that produced compliments (rewrite them), questions all personas answered identically (probably leading), assumptions no question touches (coverage gap). The atoms themselves go nowhere; the guide edits are the product. This is "simulate to design" as a concrete workflow rather than a slogan.

## Layer 4 — Days 2–5: execution patterns and their failure points

**The interview cadence (Days 3–4).** Two interviews per day maximum with a 15-minute synthesis slot immediately after each (run the synthesizer, read every atom against its quote, fix mis-tags by hand in the JSON; the model proposes, you dispose). Batch-synthesizing five interviews on Day 5 is the classic failure: memory has already smoothed the disconfirming material by then, and your correction rate on the model's tags drops to near zero because rereading five transcripts is a chore. Fifteen minutes while it is fresh, every time.

**The smoke-test window (Days 4–5).** Open the taps per Friday's pre-registration. Mid-window peeking is allowed for *operational* faults only (broken form, tracking gap); acting on mid-window conversion numbers is the moving-threshold sin with extra steps. When the window closes, counts go in as `behavioral` atoms with the Wilson interval in the quote field, e.g. `"4/74 warm → [2.1%, 13.1%] vs pre-registered 3% floor"`.

**The pilot offers (Day 4–5).** The two warmest interviewees get the Movement 5 ask in writing, with a price. Acceptances are `paid` FOR atoms of strength 5. Refusals with reasons are atoms too, direction per the reason, and asking "what would have made this a yes?" is mandatory. Silence after 72 hours is a NEUTRAL atom; log it rather than re-sending hope.

**The decision memo (Day 5).** One page, four sections: the verdict as printed (paste it, overrides and all); the three strongest atoms each way, quoted; the decision (BUILD / PIVOT-with-named-axis / KILL / EXTEND-with-specific-n-and-date); and, if you overrode the tool, the override paragraph, written knowing that Sunday-you and Week-12-you will reread it. Share the memo with one human who will ask you a hard question: a cohort peer, or the office-hours thread. Private decisions about your own idea revert to vibes within a fortnight; witnessed decisions hold.

## Worked example — the follow-up agent's sprint, compressed

The running example, end to end. Day 1: A1 (desirability: admin bundle pain), A2 (viability: 2/10 paid pilots at $200/mo), A3 (wedge: drafting is the valued piece), A4 (feasibility: field-accuracy ≥90% on a 20-call golden set) registered; PIVOT clause pre-names the plumbing wedge; verdict baseline: empty. Day 2: dossier atoms land (Upwork budget receipts FOR A1 at desk weight; flat Trends line NEUTRAL); synthetic pilot flags two leading questions in Movement 4; guide v2. Days 3–4: interviews P2–P6; the synthesizer's per-interview runs accumulate 31 stated atoms; the A3 row turns unambiguous (five AGAINST atoms, three at strength 4, all quoting variants of "the drafting is mine, the plumbing rots"); A1 accumulates FOR mass with two strength-5 currency atoms (intros made). Day 4: pivoted smoke test goes live at $200/mo fake-door pricing; two pilot offers sent *for the plumbing wedge*. Day 5: smoke window closes 4/74 warm ([2.1%, 13.1%] against a 3% floor: interval straddles, EXTEND clause fires for cold traffic n≥150); one pilot acceptance arrives, one "not now, ask me in Q4 when we switch CRMs" (logged AGAINST A2 at strength 3, with a date). Verdict printout: A1 BUILD-grade; A3 killed by its own criterion; A2 one paid atom short with the EXTEND path specified. Decision memo: PIVOT to the plumbing wedge (pre-named, so it is a rule-following act, not a rescue), EXTEND viability evidence via the cold window and one more pilot offer, feasibility golden-set build scheduled into Week 12. Total out-of-pocket: about $90 of traffic and $60 of coffee. Compare that to the fully-loaded cost of the wrong build.

## Runnable experiment — today's session, with milestones and a pass bar

Timed, like every build day. 2.5–3 hours.

- **T+0:00 — Quickstart on sample data (20 min).** Run the README quickstart end to end (init → sample assumptions → offline synthesis of `sample_interviews/P3.md` → import → verdict → `wilson 4 74` → report). You are verifying the toolchain and meeting the sample output before your own data raises the stakes.
- **T+0:20 — Registration (45 min).** Layer 3, steps 1–2, on your real bet. Commit `ledger.json`.
- **T+1:05 — Claude-mode synthesis of your real transcript(s) (30 min).** Run without `--offline` if the CLI is available; then run `--offline` on the same file and diff the two atom sets. Write three sentences in your notes on what the diff teaches about labeling quality. Run `--audit 5` on the Claude-mode output and blind re-tag.
- **T+1:35 — Sprint scheduling (20 min).** Layer 3 step 3. Calendar or it isn't real.
- **T+1:55 — Synthetic guide pilot (30 min).** Layer 3 step 4. Guide v2 saved.
- **T+2:25 — Baseline verdict + memo skeleton (20 min).** Run `verdict`; save the printout into a `validation/04-decision-memo.md` skeleton with the four section headers and the Day 5 date at the top.

**Pass bar:** (a) quickstart reproduced (verdict prints, wilson matches `[2.1%, 13.1%]` for 4/74); (b) your ledger registered and committed with ≥3 assumptions, each carrying a quantified kill criterion, and a PIVOT clause that names its axis; (c) real transcript synthesized in both modes with the diff noted and the blind audit done (≤1 direction disagreement in 5, else re-run with a corrected prompt); (d) five interview slots, the smoke window, and the Day 5 verdict on the calendar; (e) the sprint's decision memo skeleton exists with the verdict-day date written in. The sprint's own pass bar, evaluated on Day 5: **a build/pivot/kill/extend decision you can defend, out loud, to a skeptic, from atoms with quotes.**

## Common mistakes experts see

1. **Tool-polishing as sprint avoidance.** The ledger CLI is a means. Every hour extending it before the sprint runs is an hour the interviews did not happen. (Extend it in Week 12 if it earned its keep.)
2. **Registering mushy kill criteria.** "Weak interest" trips nothing. If the criterion has no number, the tool cannot referee and you will not either.
3. **Batch synthesis on Day 5.** Memory-smoothed, correction-starved, and always flattering. Fifteen minutes per interview, same day, no exceptions.
4. **Trusting the model's tags.** The synthesizer proposes; the audit disposes. An unaudited FOR atom is an opinion with a JSON schema.
5. **Editing thresholds mid-sprint.** The override log will show it, which is the point, but the deeper cost is that your Day 5 verdict stops meaning anything even to you.
6. **Letting synthetic atoms leak upward.** They are in the file, weight 0.0, and the temptation is to cite them in the memo's prose ("our panel also showed..."). The memo quotes human atoms only.
7. **Running the sprint on zero scheduled interviews.** If Wednesday's recruiting hasn't produced five slots, today's correct build is more recruiting messages, not more tooling. The sprint waits a week; the discipline doesn't change.
8. **Deciding privately.** Unwitnessed verdicts decay. Share the memo with someone licensed to say "that reads like a rescue."

## Open questions — what's not settled

**1. How much of validation can be agentized before it stops working?** The temptation after today is obvious: wire the whole sprint into an agent (recruiting outreach, scheduling, AI-moderated interviews, auto-synthesis, auto-verdict) and validate ten ideas a quarter. Some links agentize cleanly (scheduling, transcription, atomization-with-audit); one does not, and the week's research says why: the evidence-bearing step is a human incurring cost in a relationship with you, and automating your side of that relationship visibly (AI outreach, absent founders) changes what the human gives, usually toward polite noise. Where exactly the automation frontier sits, and whether AI-moderated interviewing shifts it (Wednesday's open question 1), is the live design problem for anyone productizing this pipeline.

**2. Does decision apparatus actually improve founder decisions?** Uncomfortable admission: the pre-registration-for-founders thesis is mechanism-plausible and imported from a field (metascience) where it demonstrably works, but no controlled study shows founders with evidence ledgers outperforming founders with spreadsheets and honesty. The confounds are brutal (founders who adopt decision hygiene differ in everything else too), so the evidence may never be clean. This course teaches the apparatus anyway, on the argument that its costs are twenty minutes and its failure mode is mild (you decided consciously); but intellectual honesty requires labeling it a reasoned bet, not a proven intervention, and Seibel's spreadsheet remains a respectable null hypothesis.

**3. When does the CLI deserve to become a product?** Friday's Jerry Liu observation and today's reflection question 6 both point at the same fork: this toolchain, pointed at clients, is a service offering; generalized, it is a SaaS wedge in a space (evidence-based product decisions) with established incumbents on the research-repository side and none on the pre-registered-verdict side. Whether the verdict layer is a product or a feature is precisely the kind of question the toolchain itself should answer. If you feel the pull, you know the protocol: bet sentence Monday, and this time the recruiting is easier, because your prospects are the cohort.

## Reflection questions

1. The tool makes self-deception *visible* rather than impossible. Where, specifically, would you cheat if you were going to, and what one additional check would catch that exact move?
2. Your Claude-mode vs offline-mode diff: which mis-tags did the crude mode make that the model avoided, and which did *both* make? What does the overlap tell you about where human audit is non-optional?
3. The default weights say one paid atom outweighs five stated ones. For your idea's price point and sales motion, defend or revise that ratio in writing, today, before Day 5 gives you a reason to want it different.
4. The sprint schedules the verdict regardless of evidence completeness. What is the strongest argument *against* that rule for your specific situation, and does the EXTEND output already answer it?
5. If Day 5 returns KILL, write now, in two sentences, what the sprint's assets are worth to you anyway. (Sunday's capstone will ask what W9–W11 compose into; a killed idea with a working validation pipeline is a better position than most builders ever reach.)
6. What would this exact toolchain look like pointed at a *client's* product decision, and what would you charge for the week? (Friday's Jerry Liu lens planted this; answer it concretely.)

## My take (reviewer lens)

**Boris Cherny** would look at the toolchain and ask why the atoms flow through hand-run CLI steps at all: his current fleet-management practice would wire the synthesizer as a hook on the transcript directory, run the audit sample automatically, and have the verdict post itself to the decision memo, because every manual step in a pipeline is a step that stops happening under load; he would be right for Week 12, and deliberately resisted for this week, where *feeling* each step is the pedagogy. He would also, fairly, flag the offline tagger's first-assumption default as the kind of silent data-quality hazard that should fail loudly instead. **Michael Seibel** would read the whole apparatus and deliver the shortest review in this vault: "You have five interviews and a landing page. You could have done this with a spreadsheet and honesty." True, and worth saying out loud; the tooling's honest defense is that the spreadsheet-and-honesty regime has a documented failure mode (the honesty degrades under attachment), and twenty minutes of pre-registration plumbing is cheap insurance against it. But his implicit warning stands: if the ratio of tool time to human-contact time in your sprint exceeds 1:3, you have built a very sophisticated way to avoid the phone. **Hamel Husain** would endorse the audit loop and push it one step further: the sprint generates exactly the artifact needed to *measure* the synthesizer (human-corrected tags = labels; model tags = predictions; agreement rate = your pipeline's real accuracy), and a reader who computes that number and writes it in the decision memo has understood this entire course's eval thesis at a level no quiz can check.

## Further reading

**Must-read**

- `code-lab/6/README.md` — the runbook you will actually use this week.
- Jake Knapp, John Zeratsky, Braden Kowitz, *Sprint* (2016), Day 5 ("Test") chapters, for the original time-boxed-decision architecture.[^1]

**Recommended**

- Hamel Husain, "A Field Guide to Rapidly Improving AI Products" (2025), reread with today's synthesizer in mind: the look-at-your-data discipline is the same muscle.[^4]
- David Bland & Alexander Osterwalder, *Testing Business Ideas* (2019), the experiment-sequencing chapters.[^2]

**Optional**

- "Lost in Simulation" (arXiv 2601.17087), for why the synthesizer's anti-sycophancy prompt clause exists.[^3]
- Rob Fitzpatrick, *The Mom Test*, ch. 7 on note-taking symbols, a manual ancestor of the atom schema.[^5]

## Citations

[^1]: Jake Knapp, John Zeratsky, Braden Kowitz, *Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days* (Simon & Schuster, 2016); methodology reference at https://www.gv.com/sprint/ — time-boxed week, daily artifacts, decision criteria fixed up front.

[^2]: David J. Bland & Alexander Osterwalder, *Testing Business Ideas* (Wiley, 2019) — experiment sequencing by evidence strength and cost; assumption mapping.

[^3]: "Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations," arXiv 2601.17087 (2026). https://arxiv.org/html/2601.17087v1 — systematic cooperativeness/inflation in LLM-simulated judgment; the empirical basis for the synthesizer's prefer-AGAINST-when-ambiguous prompt rule (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Hamel Husain, "A Field Guide to Rapidly Improving AI Products," March 2025. https://hamel.dev/blog/posts/field-guide/ — error analysis on real traces; labeling quality over pipeline sophistication; the audit-loop discipline ported here.

[^5]: Rob Fitzpatrick, *The Mom Test* (2013). https://www.momtestbook.com/ — ch. 7's note-taking symbol system as the manual precursor to atom tagging.

[^6]: Edwin B. Wilson, "Probable Inference, the Law of Succession, and Statistical Inference," *Journal of the American Statistical Association* 22(158), 1927, pp. 209–212. https://www.tandfonline.com/doi/abs/10.1080/01621459.1927.10502953 — the score interval implemented by the `wilson` subcommand; applied treatment canonical in [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]].

[^7]: Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya G. Parameswaran, Eugene Wu, "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences," UIST 2024. https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.pdf — machine judgments require measured human alignment; the basis for the `--audit` loop.

[^8]: Brian A. Nosek et al., "The preregistration revolution," *PNAS* 115(11), 2018. https://www.pnas.org/doi/10.1073/pnas.1708274114 — commit-before-data as the guard against postdiction; the ledger's `init`-then-commit flow is its founder-scale port.

_last_verified: 2026-07-17_
