---
type: review
phase: 2-multi-persona
week: week-03
reviewers: [cagan, lenny, huyen, husain, skeptical-cfo, cohort-peer]
date: 2026-04-15
---

# Week 3 multi-persona review

## Per-lesson ratings (0–10)

### 01-mon-problem-discovery-frameworks
- Cagan 9 — Christensen/Ulwick/Moesta seam analysis is discovery rigor at its best; Cagan's own *Transformed* cited correctly.
- Lenny 8.5 — switch-interview protocol is operational; Moesta-Lenny podcast cited as primary.
- Huyen 7.5 — strong on JTBD, lighter on production-eval hooks, which is fine for a Mon framing day.
- Husain 7 — kill criterion appears in checklist item 7 but isn't operationalized with eval numbers.
- CFO 8 — McKinsey/BCG critique names integration-cost omission explicitly; Humane/Rabbit $-numbers grounded.
- Peer 9 — 3 domains (legal, coding, consumer) in case work; sharable across fields.
- **Weighted avg: 8.2**

### 02-tue-when-ai-fits-a-problem
- Cagan 8.5 — 4-test reference; lesson correctly notes Cagan "under-specifies the eval problem."
- Lenny 8 — RICE-with-C_eval is a genuine PM artifact; decision tree terminates.
- Huyen 9 — *Prediction Machines* framing applied to 2026 with Moffatt-v-Air-Canada + Klarna; compound-reliability math.
- Husain 9 — eval-first protocol (20-50 labels → score → categorize) summarized faithfully with citation.
- CFO 8.5 — queue-ops cost denial named; 0.9^5=0.59 reliability math.
- Peer 8.5 — lending-workflow partition lands for any domain.
- **Weighted avg: 8.6**

### 03-wed-scoping-ai-projects
- Cagan 7.5 — discovery thread present but Cagan less central.
- Lenny 8 — walking-skeleton + cadence discipline operational.
- Huyen 8.5 — retrieval precision@k at chunk level, tool-call success math, criteria-drift citation to Shankar UIST 2024.
- Husain 10 — this lesson is Husain-doctrine executed: error analysis → judge calibration (κ≥0.7) → kill criteria with metric/threshold/decision.
- CFO 8 — 5 cost surfaces including eval-run cost ($9k/12wk) and fallback-to-human.
- Peer 8 — insurance-claims + legal-memo war stories translate across fields.
- **Weighted avg: 8.3**

### 04-thu-pricing-ai-services
- Cagan 7.5 — viability test implicit throughout; not central.
- Lenny 9 — trilemma + hybrid synthesis ("sell outcomes, bill usage") is crisp PM-craft.
- Huyen 9 — COGS decomposition (tokens+infra+HITL+remediation), prompt-caching collapse of token cost, Bessemer Supernova/Shooting Star margin gap.
- Husain 7.5 — eval not primary here, but margin-of-safety discipline analogous.
- CFO 10 — sensitivity table across +30%/-50% model price, $4M mispricing war story, model-price adjustment-clause recommendation.
- Peer 9 — services-pricing section extends lesson to consultants/catalysts directly.
- **Weighted avg: 8.8** (strongest lesson)

### 05-fri-case-study-customer-support-agent
- Cagan 8 — four-shapes taxonomy is discovery-grade; architecture-predicts-pricing insight.
- Lenny 8.5 — Intercom Fin / Decagon / Sierra pricing mechanics worked through.
- Huyen 9 — honest unit-economics spreadsheet; Gartner 2030 crossover; non-English quality cliff.
- Husain 8 — eval rubric in teardown section; "held-out labeled test set vendor doesn't see."
- CFO 9 — $350-700k TCO build vs $29.9k/mo savings math explicit; "resolution" denominator fraud named.
- Peer 9 — teardown template directly reusable on any vendor.
- **Weighted avg: 8.6**

### 06-sat-case-study-coding-agent
- Cagan 8.5 — four-job decomposition (A/B/C/D) is discovery-grade.
- Lenny 8 — pricing-encodes-strategy read of Cursor/Claude Code/Copilot/Devin.
- Huyen 8.5 — METR 19% slowdown RCT + SWE-bench contamination + Pro gap cited with primary sources.
- Husain 9 — Pushback 2 *is* Husain doctrine, and lesson self-applies it (binary pass/fail, N≥20).
- CFO 8 — unit economics of Cursor's $20 credit pool; no equivalent $-war-story to Thu's $4M.
- Peer 8 — experiment is directed-through-Claude-Code, matches medium spec; Problem 5 (reviewer-lens email) is reusable.
- **Weighted avg: 8.4**

## Overall
- **Week average: 8.5 / 10** — above Week 1's 8.2 baseline.
- **Weakest lesson: 01-mon (8.2)** — strong on JTBD but lighter on eval/production specifics. (Still above quality gate.)
- Strongest: 04-thu (8.8).

## Bounded polish targets (≤2 lines each)

**Mon:**
1. Layer 5 step 6 ("check for outcome metrics") — add one concrete outcome-example from a non-sales domain (finance or ops) so the 3-domain coverage target is hit inside the protocol, not only in case studies.
2. Reviewer lens bullet 2 on ODI overkill — add one sentence naming the $50k–$500k estimate's source or marking it as operator estimate.
3. Checklist item 7 (kill criteria) — add a specific-numerical exemplar ("e.g., <40% switch-interview struggle-confirmation by week 4") matching the Wed kill-criterion rigor.

**Tue:**
1. Layer 1 Axis 2 "medium volume, medium value" — the partition example is abstract; add one named-company instance (e.g., Zendesk's 2025 triage pattern) with a citation.
2. Layer 5 agent-compatibility axis — the 0.9^5=0.59 number could specify a real agent where compound reliability was measured, not just the arithmetic.
3. Reviewer lens bullet 5 — "overstates how much of the 'agentic' category is actually agentic" would land harder with one named vendor where the mismatch is documented.

**Wed:**
1. Part 3 *Retrieval precision@k* thresholds (P@5≥0.8, Recall@20≥0.95) — add one citation or operator source; currently presented as authoritative without attribution.
2. Part 5 "80% RAG failure rate" — the figure is cited as "dominated by teams who never gated on retrieval quality"; tighten with the MIT NANDA source inline rather than only in footnote 10.
3. Part 7 insurance-claims war story marked as "I advised in Q4 2025" — label as composite/illustrative per Thu's pattern to avoid implying fabricated operator claim.

**Thu:**
1. Layer 2 Bessemer Supernova/Shooting Star split — add the primary URL inline on first use (currently only in footnote), since the 25%/60% GM claim is load-bearing for the whole lesson.
2. Operator war story already labeled "composite"; consider same label on the Wed insurance story for consistency.
3. Layer 5 Harvey seat-minimum arithmetic — spell out that the $24/conversation @ 50/mo figure is derived assumption, not Harvey-published.

**Fri:**
1. Klarna $40M and $60M figures — one of the sources (CX Dive) is secondary; add the Klarna IR/press-release primary URL where possible.
2. "Decagon $50K platform floor plus ~$0.99/conversation" — cite which industry reporting source this comes from (not just Stripe case study).
3. Unit-economics "$5-$8 per interaction NA in-house" — Teneo 2025 citation exists; pull the specific page number/section into footnote for auditability.

**Sat:**
1. Experiment's "Claude Code + sympy/sympy issue" — note that the agent may refuse to pick open GitHub issues without web access; add fallback instruction (paste an issue text if no browsing).
2. Claude Code "$13/active-dev/day, $150–250/month" figures — cite specific Anthropic public source (blog post, earnings commentary) not just costs docs page.
3. Problem 2's option (f) "heaviest 5 users" — add one sentence on how to identify those 5 in practice (usage logs from the vendor dashboard).

## Citation-verify suspects (up to 3 per lesson)

- **Mon:** [^12] getlatka + Spearhead for Cursor $1B/50K customers — verify against TechCrunch/Anysphere primary. [^22] TechResearchOnline Humane $700 lesson — secondary; prefer Engadget or HP press release for the $116M figure. [^24] DigitalApplied "AI Product Failures 2026" — dated 2026, verify publication is actually live.
- **Tue:** [^8] Marily Nika RICE-A substack — confirm framework is actually dated 2024 as claimed. [^13] METR 4-months doubling claim — verify METR paper says this explicitly (not a secondary interpretation).
- **Wed:** [^10] MIT NANDA 95% figure — verify Beam.ai link still resolves and correctly cites the MIT report. [^8] Gartner 40% cancellation via RCR Wireless — confirm Gartner primary press release exists. [^14] Anthropic Applied AI "no single canonical post" — confirm this is still true April 2026.
- **Thu:** [^4] a16z LLMflation framework via Monetizely/Tanay Jaipuria — confirm the "10x annual decline" phrasing is a16z's own, not secondary paraphrase. [^8] ksred.com 10B-tokens case study — blog-level source for load-bearing claim; cross-check with Anthropic's own Claude Code cost docs. [^16] Artificial Lawyer Harvey+LexisNexis projection of $3k/seat — verify date and figure.
- **Fri:** [^7] S&P Global Klarna 26% revenue reference dated Nov 2025 — date should be checked against actual IPO S-1. [^15] TechCrunch Sierra $100M ARR Nov 2025 — verify date (recent, should be robust). [^22] Gartner $3+ 2030 projection via CX Today — find Gartner primary.
- **Sat:** [^6] Meridiem / Yahoo Finance $19B Anthropic ARR claim — double-check; Yahoo Finance is syndication, find origin. [^8] Microsoft 15M paid seats via creati.ai dated 2026-02-10 — very recent secondary, verify primary. [^11] METR arXiv 2507.09089 — verify arXiv ID resolves.

## Summary report
- **Overall: 8.5/10** (week strong; publishable)
- **Weakest: Mon (8.2)**
- **Polish targets: 18** (3 per lesson × 6)
- **Citation-verify suspects: 17** across 6 lessons
