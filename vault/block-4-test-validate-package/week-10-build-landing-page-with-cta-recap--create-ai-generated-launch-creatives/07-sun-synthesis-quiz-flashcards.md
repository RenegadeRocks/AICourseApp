---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 7
day_name: sun
session_slug: create-ai-generated-launch-creatives
date_due: 2026-07-26
tags: [synthesis, quiz, flashcards, week-10, launch-kit, agent-conversion, creative-stack, instrumentation]
sources: []
last_verified: 2026-07-17
---

# Week 10 synthesis — the launch surface, consolidated

## The one-sentence thesis of this week

A landing page for an agent product is an eval report wearing a suit: the trust gap is the conversion bottleneck, AI production is for volume while human judgment gates everything that ships, and a launch is an experiment whose pass bars were written before the traffic arrived.

## The unifying frame: proof, produced and measured

Every day this week was the same discipline applied to a different surface:

- **Monday** applied it to *claims*: scoped promises, a proof hierarchy ordered by buyer-verifiability, published evals with methodology, pricing models that answer the risk objection, and the FTC's substantiation standard as the legal floor under all of it.
- **Tuesday** applied it to *structure*: the demo asset chosen by measured p90 rather than ambition, the CTA chosen from an ACV × time-to-evidence grid, objection blocks written to be forwarded, and social proof that scales down to N=3 without lying.
- **Wednesday** applied it to *tools*: a creative stack chosen on capability, commercial terms, and perception, in a market where the slop backlash punishes visible laziness and the Sora shutdown punished building on subsidized ground.
- **Thursday** applied it to *production*: brief-first pipelines, batch-and-select, the storyboard with a guardrail beat, platform disclosure rules, and a QA gate whose mechanical half a script can run.
- **Friday** applied it to *measurement*: qualified-action rate over vanity counts, hybrid attribution over UTM theology, and pre-registered kill/continue/scale bands with a calendar-blocked decision date.
- **Saturday** assembled all five under a milestone clock, with exit-code-0 as the definition of done and a ship log as the record.

The through-line backward: Monday's claims file came from [[06-sat-rag-evaluation|Block 2 Week 4]]'s eval harness; Tuesday's statistics and Friday's decision rules are [[06-sat-validation-instrumentation|Block 2 Week 3 Saturday]]'s canon applied to a launch; the QA gate is the validator pattern from your agent builds pointed at marketing assets. The through-line forward: Friday's decision memo and interview pool are the raw material for Week 11's validation discipline, where launch numbers meet actual humans and "continue" gets decomposed into what to validate next.

## Where each day's content goes forward

| Day | Artifact produced | Where it goes next |
|---|---|---|
| Mon | Hero, objection map, eval section, claims file | Claims file becomes `claims.json`, the build's CI gate; objection map seeds Week 11 interview script |
| Tue | Page spec, CTA decision, demo-rung decision | Saturday's build input; the sandbox isolation answers become a security-review asset |
| Wed | Stack selection, terms notes, brand spec, stance | Every future creative task; terms notes re-verified quarterly |
| Thu | Four QA-passed assets, pipeline habit | Reused for every campaign; the gate log tells you when briefs drift |
| Fri | Instrumentation plan, pre-registered memo, war-room protocol | The T+14d decision memo, Week 11's primary input |
| Sat | The shipped kit + ship log | The launch itself; the template for launch two |

## The week's key moves — the mental-move table

| Situation | The move | Source |
|---|---|---|
| Writing any product claim | Scope it, then check: what artifact substantiates this? | Mon L2–L3 |
| Buyer objection surfaces | Map it to a proof asset at the highest affordable rung | Mon L2 |
| Tempted to hide the escalation path | Film it instead; the guardrail beat differentiates | Mon L1, Thu L3 |
| Choosing demo asset | Four sandbox criteria; fail any → drop a rung; never fake a rung | Tue L2 |
| Choosing CTA | ACV × time-to-credible-evidence grid; one primary action | Tue L3 |
| N=3 social proof | Depth over density: one quantified case, real counters, design-partner framing | Tue L5 |
| Picking a creative tool | Capability, then commercial terms read this month, then perception | Wed L1–L2 |
| Any generated asset | Batch ≥ 12, select against brief, never negotiate with mediocrity | Thu L1 |
| Before anything ships | Mechanical gate (script) + judgment gate (human), no open failures | Thu L6, Sat M3 |
| Launch morning | Reply fast T+0–6h; four scheduled looks; bands decide, not moods | Fri L4 |
| Attribution question | Hybrid: UTM where mechanical, free-text HDYHAU where human | Fri L3 |
| Two weeks post-launch | Decision memo against pre-registered bands; hand to Week 11 | Fri L4–L5 |

## 15 quiz questions

1. Name the three above-the-fold objections specific to agent products, and state why they precede value claims in the page's order.
2. Order these proof assets by buyer-verifiability, strongest first: logo wall, published eval with methodology, live sandbox, quantified named case study, interactive tour.
3. What are the four criteria that must all hold before a live sandbox goes on the page, and what is the standard middle pattern when free-typing is too risky?
4. Intercom's Fin markets fleet-level resolution rates while an independent teardown argues production B2B rates land 20+ points lower. What page-design practice does this gap argue for, and why does it *not* argue for hiding your numbers?
5. Give the per-resolution prices for Fin and Zendesk's outcome-based tier, and explain in one sentence why outcome pricing functions as an objection handler.
6. Your package: $20K ACV, evidence deliverable in a 30-minute pilot run. Which CTA does the grid select, and what role does the sandbox play?
7. State the two benchmark medians for opt-in vs opt-out trial-to-paid conversion, and explain why an agent package usually wants a "scoped trial" instead of either.
8. Which US legal instrument sets the substantiation standard for AI capability claims, and what is the standard's phrasing?
9. Midjourney and ElevenLabs each hide a commercial-terms trap for operators. Name both.
10. Why is a raw AI-generated hero image probably unprotectable by copyright, what *is* protectable, and what duty applies at registration?
11. What killed Sora, per reported figures, and what two operator habits does the shutdown justify?
12. Meta, YouTube, LinkedIn: one sentence each on their mid-2026 posture toward AI-generated content.
13. Define qualified-action rate and the property a qualified action must have; explain why launch week specifically punishes cheap-action metrics.
14. What does dark social do to UTM-based attribution, and what is the hybrid fix with its known bias?
15. Your T+14d numbers: 1,100 visitors, QAR 1.9% against bands of kill <0.5% / scale >3%. Two booked calls showed; one was a bad fit. What band is called, what happens next per the memo, and what Week 11 activity consumes the result?

## Answers

1. "Will it hallucinate in front of my customers" (accuracy), "what happens to my data" (security; agents hold credentials and act), "how much babysitting does it need" (reliability). They are disqualifiers: unresolved, they end evaluation regardless of value, so value copy converts nothing until they are answered. (Mon L1)
2. Live sandbox > interactive tour > published eval with methodology ≈ (for technical buyers) > quantified named case study > logo wall. Ordering principle: how directly the buyer can verify without your mediation. (Mon L2)
3. Sub-two-minute value on visitor-supplied/selected input; known-good p90 on the demo task from evals; full isolation from production data and tools; rate limits + spend breaker. Middle pattern: the curated-input sandbox (live agent, six prepared inputs). (Tue L2)
4. Publish methodology with numbers: task mix, sample size, success definition, failure examples, plus verify-on-your-data during pilot. The gap is credibility exposure only when numbers are unexplained; hiding numbers concedes the trust gap entirely. (Mon L3)
5. Fin $0.99 per resolved conversation; Zendesk ~$1.50 committed / ~$2.00 pay-as-you-go per automated resolution. Outcome pricing answers "what if it fails?" with "then you don't pay," embedding the risk answer in the price. (Mon L4)
6. Demo call as primary CTA (high-ish ACV, fast evidence = the sweet-spot quadrant), with the sandbox as pre-call warmer so buyers arrive half-convinced; quiet secondary link at most. (Tue L3)
7. Opt-in ~14% median (8–22), opt-out ~44% median (35–55). Agent packages usually need onboarding/integration, so a naked trial mismatches; the scoped trial trials the *evidence* (run your data, see your report) rather than the product. (Tue L3)
8. The FTC Act Section 5 as enforced through Operation AI Comply: AI capability claims must be substantiated by "competent and reliable evidence" at the time they are made. (Mon L3)
9. Midjourney: companies over $1M gross annual revenue must be on Pro/Mega for commercial use (and stealth mode starts at Pro). ElevenLabs: the free tier carries no commercial rights at all. (Wed L2)
10. The Copyright Office's Part 2 report (Jan 2025): human authorship required, prompts alone insufficient. Protectable: human selection, arrangement, substantial modification, and the composited page as a whole. Registration carries a duty to disclose more-than-de-minimis AI-generated material. (Wed L2)
11. Reported ~$1M/day operating cost against ~$2.1M lifetime in-app revenue and collapsing usage; two-stage shutdown (app April 2026, API September 2026) with data deletion. Habits: prefer tools with visible unit economics, and archive prompts/settings/outputs in your own repo on acceptance. (Wed L3)
12. Meta: disclosure required for AI-generated ad content (photorealistic triggers), auto-labeling plus detection enforcement. YouTube: creator disclosure required for realistic synthetic media that could mislead. LinkedIn: no disclosure regime but algorithmic demotion of generic AI text; hybrid human-edited content outperforms. (Thu L5)
13. QAR = qualified actions ÷ unique visitors, where the action must cost the visitor something (time, data, calendar, answered email). Launch traffic is maximally curious and minimally qualified, so costless-action metrics peak exactly when they are least predictive. (Fri L1)
14. Private-channel shares (Slack, DMs, forwards) arrive as "direct," so UTM systematically undercounts the highest-intent channel. Fix: hybrid attribution with a free-text "how did you hear about us" field; known bias: respondents report the most memorable touch, not the first or decisive one. (Fri L3)
15. Continue band (between 0.5 and 3). Per the memo: no kill, no scale; the channel ranking and verbatim HDYHAU answers plus the interview pool go to Week 11, whose validation interviews investigate *why* 1.9 and what would move it, before any further creative or channel spend. (Fri L4–L5)

## 28 flashcards

| # | Q | A |
|---|---|---|
| 1 | The week's thesis in one line | An agent landing page is an eval report wearing a suit; trust gap first, human-gated AI production, pre-registered launch |
| 2 | Three agent-specific objections | Hallucination in front of customers; data security; babysitting/reliability |
| 3 | Proof hierarchy principle | Rank by how directly the buyer can verify without vendor mediation |
| 4 | Scoped-claim pattern | Falsifiable promise + escalation in the sentence + buyer qualification ("resolves X; routes Y with context") |
| 5 | Eval section, four parts | Claim (scoped) · basis (set, source, success definition) · failure honesty · verify-it-yourself pilot |
| 6 | FTC substantiation standard | AI capability claims need competent and reliable evidence when made (Operation AI Comply, 2024–) |
| 7 | Fin per-resolution price | $0.99 per resolved conversation; unresolved free |
| 8 | Zendesk outcome pricing | ~$1.50/resolution committed volume, ~$2.00 pay-as-you-go |
| 9 | Why outcome pricing converts | The price itself answers "what if it fails" (no outcome, no charge) |
| 10 | Outcome pricing's costs | Contractual "resolution" definition disputes; revenue inherits accuracy variance; needs trusted measurement |
| 11 | Sandbox go-criteria (4) | <2-min value on visitor input; known-good p90 from evals; full isolation; rate limits + spend breaker |
| 12 | Curated-input sandbox | Live agent, prepared inputs only: keeps "actually running" proof, bounds inputs to eval coverage |
| 13 | Interactive demo tools + prices (mid-2026) | Arcade ~$297.50/mo flat (5 seats); Storylane $40/seat Starter, $500/mo Growth; Navattic from ~$500/mo |
| 14 | CTA grid axes | ACV × time-to-credible-evidence; agent sweet spot = demo call warmed by sandbox |
| 15 | Trial benchmarks 2026 | Opt-in median ~14% (8–22); opt-out ~44% (35–55); demo pages avg 1.5–4%, top quartile 8–15% (directional) |
| 16 | Honest proof at N=3 (any three) | Quantified named case; design-partner framing; real usage counters; founder build-record; published eval |
| 17 | FTC fake-reviews rule | Effective Oct 2024: bans fabricated/AI testimonials and undisclosed incentivized reviews, per-violation penalties |
| 18 | Image-tool division of labor | Midjourney aesthetics; Ideogram in-image text; Recraft SVG + brand styles; frontier models for edits |
| 19 | Midjourney commercial trap | > $1M gross revenue requires Pro/Mega; stealth (private gens) Pro+ |
| 20 | ElevenLabs commercial floor | Free tier non-commercial; Starter $6/mo is the floor for shippable voiceover |
| 21 | Sora shutdown lesson | Subsidized consumer inference ends (~$1M/day vs $2.1M lifetime revenue); archive your prompts/outputs; judge the business, not the model |
| 22 | Copyright rule for gen assets | Purely generated = unprotectable; human selection/arrangement/modification protectable; disclose AI material at registration |
| 23 | Slop backlash mechanism | Consumers punish detectability + laziness, not assistance; execs overestimate consumer positivity (IAB, 2 yrs running) |
| 24 | Three positioning stances | Invisible assistance (default) · demonstrative assistance (builder audiences) · human-made premium (slop-fatigued audiences) |
| 25 | Pipeline six stages | Brief → generate (batch) → select (against brief) → polish → QA gate → archive & publish |
| 26 | Demo-video storyboard beats | Pain artifact · real run (timestamps) · guardrail/escalation beat · scoped claim + CTA |
| 27 | QAR definition + property | Qualified actions ÷ unique visitors; the action must cost the visitor something |
| 28 | Pre-registered launch memo | Three bands (kill/continue/scale) + 14-day window + consequences, written before launch; T+14d memo feeds Week 11 |

## Where you'd still lose points (reviewer lens)

Three residual weaknesses to carry consciously into Week 11. First, the week's benchmark numbers (demo-page conversion, trial medians, Product Hunt bands) are single-publisher or founder-analysis data used directionally; the honest posture is to replace every one of them with your own funnel's numbers as fast as Friday's instruments can produce them, and to notice which of your decisions would change if a benchmark were off by 2×. Second, the judgment half of the QA gate is unmeasured, and Hamel's critique stands: a gate that is not periodically checked against a labeled set drifts with your mood. Third, the entire week assumes your eval numbers deserve a landing page; if Monday's substantiation exercise came up thin and you scoped claims down to near-silence, the correct reading is not "marketing is hard" but "the package needs another eval cycle," and Week 11's validation work will say so louder.

## Further reading

**Must-read**

- The T+14d decision-memo skeleton you wrote Friday. Reading it cold today is the cheapest rehearsal of the discipline it encodes.
- US Copyright Office Part 2 report + FTC Operation AI Comply materials (Mon/Wed citations) — the two legal floors under everything this week shipped.

**Recommended**

- [[06-sat-validation-instrumentation]] and [[04-thu-micro-prototype-ladder]] — the Block 2 canon this week stood on; re-skim before Week 11 re-uses both.

**Optional**

- One competitor agent product's landing page, read with Monday's proof hierarchy as a scorecard. Twenty minutes, and you will never un-see the adjectives.

_last_verified: 2026-07-17_
