---
type: review
phase: 2
week: week-07
reviewer: multi-persona 13-lens (Karpathy / Chip Huyen / Jerry Liu / Hamel Husain / Simon Willison / Seibel / Boris Cherny / cohort peer / Mira Murati / swyx / Ethan Mollick / Lilian Weng / Jeremy Howard)
spec: .claude/block-3-briefs/_generator-base.md
date: 2026-07-17
---

# Week 7 — Phase 2 Multi-Persona Review

Reviewed cold (reviewer did not generate the content). Checks run: all 8 markdown files + `code-lab/6/` read in full; `py_compile` on all 6 Python files (PASS); both JSON configs parsed (PASS); wikilink targets resolved against the vault; cross-file number sweep; anti-slop counts; 2 WebSearch spot-checks (Realtime-2.1 pricing; WA Oct-1 service-message change) — both corroborated, one sub-discrepancy logged below. WebFetch egress-blocked, so citation liveness remains Phase 4's job; every fast-moving citation already carries the correct `search-verified / liveness pending` hedge tag.

Scoring 1–10. Weights: Karpathy / Hamel / Simon = 1.0 each; the other ten = 0.8 (total 11.0).

---

## Per-file scores

### 01-mon — The 2026 voice stack — **8.0**

| Persona | Score | One-liner |
|---|---|---|
| Karpathy (1.0) | 8 | Ordinal-not-cardinal caveat on vendor latency tables is exactly right and stated in-lesson; still, millisecond-precision tables invite over-trust. |
| Hamel (1.0) | 7 | Worksheet is a real artifact but has no pass/fail gates; "flag every number you copied" is a habit, not an eval. |
| Simon (1.0) | 8 | Source-criticism modeled well (Gradium overclaim discounted explicitly); no security angle needed Monday. |
| Chip 9 · Jerry 8 · Seibel 8 · Boris 8 · peer 9 · Mira 7 · swyx 9 · Mollick 8 · Lilian 7 · Howard 8 (0.8 each) | | Config A/B/C economics with a named migration trigger is the strongest decision artifact; swyx lens (platforms absorb parts) is genuinely predictive. |

### 02-tue — Conversation engineering — **8.3**

Karpathy 9 (three-schools framing + "no turn-taking ImageNet" honesty is the lesson's best epistemics) · Hamel 8 (five metrics with defensible targets; interruption-direction ratio as diagnosis is operational) · Simon 8 · Chip 9 · Jerry 8 · Seibel 8 · Boris 8 · peer 9 (the "I'm on Retell, I control nothing" reframe is the most useful paragraph for the median reader) · Mira 8 · swyx 8 · Mollick 8 · Lilian 9 (interruption recovery correctly framed as working-memory) · Howard 8.

### 03-wed — The voice agent squad — **8.2**

Karpathy 9 (prompt-length-as-TTFT-variable is a real mechanism insight) · Hamel 7 (squad metrics named but targets left to the reader) · Simon 8 · Chip 8 · Jerry 9 (tool/posture matrix as the design input, not the org chart) · Seibel 9 (his objection is steel-manned and answered) · Boris 9 (config-as-code) · peer 8 · Mira 8 · swyx 8 · Mollick 7 · Lilian 9 (handoff-payload-as-lossy-compression critique lands and Saturday operationalizes it) · Howard 8. The Cognition-critique resolution — router squad = single-threaded writes = the pattern Cognition itself conceded — is the sharpest controversy handling in the week.

### 04-thu — Trust & safety — **8.3**

Karpathy 8 · Hamel 8 (Chip-lens converts checklist into monitoring — right) · Simon 10 (his beat; capability-confinement framing correct, handoff-payload-as-trust-boundary is the catch most content misses) · Chip 9 · Jerry 7 · Seibel 7 · Boris 8 · peer 9 · Mira 9 · swyx 8 · Mollick 9 (disclosure non-monotonicity engaged, not hand-waved) · Lilian 8 · Howard 8. Legal dates (Art. 50 Aug 2; omnibus Dec 2 grace; FCC Feb 2024; SB 243 Jan 2026; DPDP Nov 2025 → May 2027) are internally consistent and correctly future-framed per the master-report rules.

### 05-fri — WhatsApp extension — **7.9**

Karpathy 7 (weakest sourcing tier in the week: India stats and open rates lean on marketing-adjacent aggregators, hedged but thin) · Hamel 7 (per-channel eval slices named in reviewer lens, not in the body) · Simon 8 (voice-note injection carried through) · Chip 9 · Jerry 8 · Seibel 9 · Boris 7 · peer 9 · Mira 7 · swyx 9 (aggregator-taxing-complements read on the Oct-1 exemption) · Mollick 8 · Lilian 7 · Howard 8. Oct-1 change and Meta-agent exemption corroborated by WebSearch this session.

### 06-sat — BUILD — **8.0**

Karpathy 8 · Hamel 8 (failure-generation-first framing is his protocol verbatim; capped by the stubbed re-ask metric, below) · Simon 8 (gateway + dead-writes-by-default is the right shape) · Chip 8 · Jerry 8 · Seibel 9 (timed phases) · Boris 9 · peer 9 · Mira 7 · swyx 7 · Mollick 7 · Lilian 8 · Howard 8. All code compiles; SETUP smoke-test payload matches `voice_tools`' normalization; `.env` hygiene correct; $0-to-complete claim holds.

### 07-sun — Synthesis + quiz + flashcards — **8.1**

Karpathy 8 · Hamel 8 · Simon 8 · Chip 8 · Jerry 8 · Seibel 8 · Boris 7 · peer 9 · Mira 8 · swyx 8 · Mollick 9 · Lilian 8 · Howard 9 (mental-move table with apply/do-NOT-apply columns is the best retention artifact in the block so far). Quiz: 12 questions, all answerable from the week's files; answer key spot-checked accurate (A1–A12 traced to source layers). Flashcards now 25 (one added in polish).

**Overall Week 7: 8.1 / 10** (8.0, 8.3, 8.2, 8.3, 7.9, 8.0, 8.1). Weakest: Fri (sourcing tier). Strongest: Tue and Thu.

---

## Hard-check results

- **Code lab:** `py_compile` PASS on all 6 `.py`; both JSON configs valid; requirements pinned; README run command matches SETUP; smoke-test curl payload matches the webhook's field fallbacks; CRM phone `+919000000001` consistent across SETUP, lesson, and `crm.py`.
- **Internal consistency:** all repeated numbers identical across files after one fix (Realtime $32/$64 + mini $10/$20; Flux $0.0065/$0.0078; Retell $0.07 / Vapi $0.05 base, $0.13–0.31 all-in; ~600 ms; Aura-2 $0.030/1k vs 313 ms independent; Art. 50 Aug 2 + Dec 2 grace; Oct 1 WA change; ~41/52/29% containment; 3-second clone; ₹/India rates in Fri = Sun A8).
- **No re-teaching:** verified against b0w02 Thu — Week 7 cites its 800 ms table, 85/97 LiveKit numbers, 100–200 ms cancellation, and 40%+ abandonment by wikilink and explicitly says "take as read"; canonical homes (trifecta → b0w02 Wed; eval discipline → b2w04 Sat) are wikilinked one-line recaps, as required.
- **Wikilinks:** all targets exist; two ambiguous-basename links and one stale "(pending)" link fixed (below).
- **Anti-slop:** contrast-scaffold tic ≤1/file (PASS); "would push back" 0 (PASS); "load-bearing" ≤1/file (PASS); **em-dash density FAIL** — 18–27 per 1k words body-text vs the ≤~12 cap, in every file (see concerns).

## Surgical fixes applied (9)

1. **Mon "Why this matters":** "$65/month" floor contradicted the lesson's own Config C ($0.077/min → $770 at 10k min); fixed to "$770/month" with the derivation named.
2. **Wed Layer 1:** stale `[[…week-06/_week|Week 6 (pending)]]` → `[[01-mon-context-engineering-the-successor-discipline|Week 6 Mon]]` (Week 6 is generated).
3. **Tue Layer 4** and 4. **Sat Layer 4:** `[[07-sun-synthesis-quiz-flashcards|Week 3]]` was ambiguous (5 files share that basename; nearest-match resolves to *this week's* synthesis) → `[[05-fri-case-study-customer-support-agent|Week 3]]`, the actual deflection-skepticism lesson.
5. **Sat Phase 4:** "four server-side numbers" listed five → "five".
6. **Fri Layer 2:** "Meta Business Agent is exempt" qualified — exempt from per-message service billing but metered on its own token basis from Aug 1 (corroborated: Meta non-template-pricing doc + Zernio, this session).
7. **Sun flashcards:** 24 → 25 (added a containment-benchmarks card; base spec floor is 25).
8. **code-lab README:** eval output comment claimed first-audio p50/p95 and interruption split, which `eval.py` does not compute → corrected to the actual five outputs + paste-from-dashboard note.
9. (Header count "## 24 flashcards" updated with fix 7.)

## Unresolved concerns → Phase 3 / Phase 4

1. **Em-dash density (Phase 3, systemic):** 18–27/1k across all eight files vs the ≤~12 cap. Needs a dedicated de-dashing pass (convert to periods/commas/colons); too pervasive for surgical edits without a rewrite-scale diff.
2. **Length vs frontmatter (Phase 3):** bodies run ~2,300–3,800 words against `word_count_target: 5500` and the 5,000–6,500 L3 soft target. The prose is dense, not lazy, and the spec says density over length — but either the frontmatter targets should be lowered to what was delivered or the deepest lessons (Mon, Thu) deserve one more layer each.
3. **`reask` is hardcoded `False` in `brain/app.py`** — the "re-ask rate (target 0)" metric is a constant, not a measurement. Either compute it (detect sacred-field re-prompts in specialist output) or label it hand-graded like the barge-in check. Hamel-lens: this is the lab's one "eval theater" spot.
4. **`window_open()` in `channels/whatsapp.py` is never called** by `app.py`, while lesson + docstring claim the adapter "checks before EVERY send." Wire it into the send path or soften the claim.
5. **Mini cached-audio price conflict (Phase 4):** one source this session says gpt-realtime-2.1-mini cached input is $0.06/1M vs the lesson's $0.30/1M. Resolve on OpenAI's pricing page when fetch is available; the number appears in Mon Layer 1 and the Layer 3 table.
6. **Phase 4 liveness list (highest-stakes URLs):** Mon [^1][^2] (Realtime-2.1 pricing/dates), Mon [^3] (Flux Multilingual GA 2026-04-29), Fri [^4] (Meta non-template pricing page + Oct-1 waves), Fri [^5] (Calling API pricing + excluded countries), Thu [^2] (Sidley omnibus Dec-2 grace), Thu [^11] (DPDP PIB PDF + phase dates), Tue [^5] / Thu [^8][^9] (arXiv IDs 2606.19595, 2604.14604, 2505.19598 — unverifiable this session, must confirm they exist).
7. **Fri sourcing tier:** India-market stats (91%, 78%, 98% open rate) rest on marketing-adjacent aggregators; hedged in [^9], but a Kantar/Meta primary would upgrade the weakest citation block in the week.

---

_Review produced 2026-07-17. Nine surgical fixes applied as listed; no other content edited. No git commit made._
