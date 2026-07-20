---
type: review
phase: 2
week: week-16
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 16 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-6-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-16-briefs.md`.

## Mechanical checks run this session

- **Code-lab:** `python -m py_compile rate_card.py unit_economics.py config_example.py` → clean. `python unit_economics.py` runs. **Both reported failure modes reproduce exactly:** the `THREE_STRIKES_SCENARIO` prints negative per-tier margins (−61.2% / −66.3%), an **un-payable CAC** (`payback = inf`, LTV −$714, LTV:CAC −0.5:1), and **exactly four audit warnings** (two margin-floor, one 1.7× ladder-step, one identical-fences). The `HEALTHY_SCENARIO` survives every shock down to Fable 5 (margin 20.2%, LTV:CAC 3.2:1) — matching the README claim verbatim.
- **Rate card vs July refresh:** Sonnet 5 $2/$10 intro → $3/$15 on 2026-09-01, Opus 4.8 $5/$25, Fable 5 $10/$50, Haiku 4.5 $1/$5, ~+30% tokenizer — all match `_refresh-2026-07-master-report.md` cross-cutting theme #1. Monday's per-brief math ($0.156/run, $3.43/niche/mo) reproduces.
- **Wikilinks:** all 17 distinct cross-week targets resolve to real vault files (script-verified). Canonical homes wikilinked, not re-taught: b4w09 (packaging/value-metric), b2w04 (sales-agent tech + RAG + deliverability), b3w07 (consent law), b5w14 (retention/NRR), b5w13 (magic/tasteful prompts), b2w03 (small-N). Confirmed by inspection.
- **Quiz/flashcards trace:** A2 LTV = (199×0.55)/0.03 = **$3,648** matches Friday line 56; Q7 code-completion `gross_per_month * horizon` matches `unit_economics.py:148` exactly; A5/A6/A8/A10 trace to Wed/Thu; flashcard 32 rate card matches. All trace.
- **Name-verification:** no non-core-roster growth guru was named as a reviewer voice (the "Max Freiberg" trap is avoided). Named third parties — **Peter van Westendorp** (Dutch economist, PSM 1976), **Bret Taylor** (Sierra, canonically sourced in b4w09) — are real and correctly attributed; both are established/historical, no fabrication risk.
- **Anti-slop:** "load-bearing" ~3–4×/week (sparing, OK); contrast-scaffold and em-dash density within budget; house tics restrained.

## CRITICAL — margin-math cross-lesson inconsistency (unresolved, flagged not fixed)

The **same named example (Niche Radar) carries two different blended margins**:

- **Friday** worked example (line 92): "blended ARPA ~$180/month (mostly Pro), gross margin **58%**" → LTV $2,610, LTV:CAC 11.9:1, payback 2.1mo. Internally self-consistent.
- **Saturday** worked example (line 104) + the shipped `HEALTHY_SCENARIO` + calculator output: ARPA **$141**, blended margin **76%**, LTV $2,684, LTV:CAC 12.2:1, payback 2.0mo.

Friday says "Saturday's code-lab **mechanizes this**"; Saturday says it assembles Friday. But the config is mostly Starter (22 of 40 customers), not "mostly Pro," so it yields ARPA $141 / 76%, not $180 / 58%. A reader who runs the calculator gets numbers ~18 margin-points off Friday's prose. Root cause: the config's support/hosting COGS are light and per-tier margins land 63–79%, which **also sits above the week's own headline "AI margins are 50–60%" thesis** (Mon/Overview/Sun). Not a surgical fix — reconciling requires either restructuring the config (cascades into Saturday's "76%" line + README's Fable-5 numbers) or rewriting Friday's worked example (undercuts the margin-compression pedagogy). Editorial decision needed. The *cascade arithmetic* in both lessons is correct; only the shared example's inputs diverge.

---

## Per-file scores (weighted average of 13 lenses)

| File | Weighted score | Note |
|---|---|---|
| 00-overview | **8.1** | Sells the machine in four parts; margin-under-COGS framed as the one number. |
| 01-mon — monetization models | **8.0** | Full menu + honest hybrid default; COGS-shock reasoning strong. Origin of the 58%-vs-calculator gap. |
| 02-tue — pricing strategy | **8.2** | Van Westendorp with its limits engaged; tiny-N/Wilson discipline; "price is a hypothesis, sales calls are the experiment." |
| 03-wed — AI in the sales motion | **8.2** | Labor-vs-relationship cut is the load-bearing frame; consent law (12 states, bot≠consent, live litigation) precise and current. |
| 04-thu — tiers & expansion | **8.0** | NRR benchmarks flagged directional; the AI-specific "expand margin, not just revenue" trap surfaced. |
| 05-fri — unit economics | **7.7** | Cascade math is clean and always-true; docked for the worked-example numbers not reconciling with the calculator it points to. |
| 06-sat — BUILD | **8.1** | Four concrete artifacts, structural follow-up gate, rate-card-update ritual; correctly reports calc output (which exposes the Fri gap). |
| 07-sun — synthesis/quiz | **8.1** | 13 Q + 32 cards, all trace; A12 "too-high LTV:CAC is a growth signal" is the right nuance. |
| code-lab | **8.0** | Compiles, runs, fails loudly on the stress case; date-stamped rate card is the right design. Config margins exceed the week's own 50–60% claim. |

Representative persona table (05-fri, the lowest file):

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Cascade (margin → LTV/LTV:CAC/payback) is real mechanism; COGS-shock-on-the-business-model is the right generalization. |
| Chip Huyen | 7 | Benchmarks honestly labeled directional, but the worked example's 58%/$180 diverges from the calculator's 76%/$141 it claims to mechanize. |
| Jerry Liu | 7 | AI-COGS thread is correct; the shipped example undercuts it by landing at 76%. |
| Hamel Husain | 7 | Pass bar is measured, but references a calculator that returns different numbers than the prose. |
| Simon Willison | 8 | No overclaim; formulas stated without hand-waving. |
| Seibel | 9 | His "LTV:CAC from 12 customers is astrology" is in the text and conceded via stage-appropriate metrics. |
| Boris Cherny | 7 | Date-stamped-rate-card point is right; the Fri/Sat number mismatch is exactly the "quietly lies" failure he warns about. |
| Cohort peer | 8 | The diagnosis-not-numbers framing is genuinely useful. |
| Mira Murati | 8 | Commercial reality without hype. |
| swyx | 8 | Three-levers-in-order is a clean operator heuristic. |
| Ethan Mollick | 7 | Benchmark ranges quoted are vendor-sourced; lesson concedes it. |
| Lilian Weng | 8 | Definitions internally consistent with Sunday's cards. |
| Jeremy Howard | 8 | Prereq wikilinks carry the b5w14/Thu/Mon load. |

**Weighted average: 7.7**

---

## Surgical fixes applied this session

1. **03-wed line 37** — upgraded the stale `(pending)` week-15 link (`[week-15 folder](...)`) to a resolving wikilink `[[04-thu-cold-outreach-post-ai-slop|b6w15 Thursday — cold outreach after the AI-slop era]]`, since week-15 now exists. No other `(pending)` lesson markers remain (all remaining "pending" strings are the citation-protocol "liveness pass pending" tag).

## Unresolved concerns (for the generator / an editorial pass)

1. **Fri↔Sat↔calculator margin reconciliation (CRITICAL, above).** Pick one canonical Niche Radar input set and make Friday's prose, Saturday's worked example, and `config_example.py` agree. Simplest honest path: raise the config's support/hosting COGS (or shift the customer mix toward Pro) so the blended margin lands ~58%, matching the week's 50–60% thesis and Friday's narrative — then update Saturday's "76%" line and the README's shock-row numbers to match.
2. **Calculator undercuts the week thesis.** As shipped, every healthy-scenario tier margin (63–79%) is above the "AI margins are 50–60%" claim the whole week rests on. Even after reconciling #1, consider a config whose blended margin actually demonstrates the compression the lessons teach.
3. **Citations are search-verified only** (fetch egress-blocked); every source carries the "liveness pass pending" tag per protocol. A liveness pass on the ~30 external URLs is still owed before the live session.
