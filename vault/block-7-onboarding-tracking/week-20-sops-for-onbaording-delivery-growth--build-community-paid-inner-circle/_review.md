---
type: review
phase: 2
week: week-20
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 20 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-7-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-20-briefs.md`.

Mechanical checks run this session (Python 3.11): `python3 -m py_compile sop_generator.py membership_model.py` — **clean**. `membership_model.py` reproduces the lessons' numbers exactly: 92 members, **MRR $6,400**, **ARPU $69.57**, 4% churn → **25-month** lifetime, **LTV $1,565**, **LTV:CAC 10.4:1**; churn doubled to 10% → **LTV $626 (40%)**. Ghost-town demo: healthy history → `HEALTHY`; dying history (active ratio 37%→17%) → `GHOST_TOWN_RISK` on exactly the **three grounds** Saturday claims (below 20% ratio floor, 20% first-week activation below the 30% floor, 3 consecutive declines). `sop_generator.py` renders checklist-form SOPs and the run-mode verdicts match the prose: "New client kickoff" (weekly/mixed/medium) → **AGENT-ASSIST**, "Produce one monthly report" (monthly/deterministic) → **AGENT-ASSIST**. **Hand-check:** Sunday Q6 (ARPU $80, 90% margin, 5% churn) → lifetime 1/0.05 = **20 months**, LTV (80×0.9)/0.05 = **$1,440** — matches the answer key. Friday scenario B LTV:CAC 626/150 = **4.2:1** ("~4:1", passing but doomed) — consistent.

**Internal consistency (dailies vs Sat vs Sun quiz/flashcards vs code-lab, all identical):** MRR $6,400, ARPU ~$70, 25-mo lifetime @4%, LTV ~$1,565, LTV:CAC ~10:1, 10%-churn LTV ~$626/40%, ghost-town 37%→17%, healthy churn <5% / danger >10%, hybrid retention >96% vs course 88-92%, TTFV 80%+ vs 35-50%, ~90% churn from no day-3 engagement, activation ~38% B2B SaaS / ~29% services, top-quartile TTFV <5min / <24h, 90-9-1 with 30%+ modern update, Skool $9/$99 (2.9% Pro / ~10% Hobby), Circle $89/$199 (2%/1%), Discord free — all reproduce identically wherever they appear.

**Anti-slop:** em-dash density 2.9–5.0/1k across all eight files (well under the ~12 ceiling; Sat 5.0 is the top). Contrast-scaffold tics: seven files at ≤2; **Thursday was at 5 — trimmed to 2 this session** (three inversions, meaning preserved). House tics ("load-bearing", "operator", "would push back") within budget.

**No re-teaching / canonical homes:** every required prior is one-line-recapped and wikilinked, not re-taught — b4w09 (delivery engineering, Mon), b7w19 (productized service / client dashboard, Mon-Tue), b2w04 ("we apply it, we do not re-teach it", Wed), b6w17 (growth loops, Wed-Thu), b5w13 (magic feature, Thu), b5w14 ("we build on it, we do not re-teach it", Tue/Fri), b6w16 (tiers, Fri/Sat), b3w08 (automation spectrum, Mon/Tue/Wed/Sat). All 18 distinct wikilink targets resolve to real vault files.

**Wikilink upgrades (required, applied):** the generator left five `(pending)` markers on forward/back links into Weeks 18 and 19, both of which now exist. **All five upgraded this session** (Mon L47 → w19; Tue L50 + L199 → w19; Sun L62 → w18, L65 → w19). Zero `(pending)` markers remain.

**NAME-VERIFICATION (required, ≥2 corroborations each):**

- **Atul Gawande — *The Checklist Manifesto*** (WHO surgical checklist, deaths cut >⅓). Real surgeon/author; corroborated by atulgawande.com + NIH PMC review (PMC4953332). **Verified.**
- **Michael Gerber — *The E-Myth Revisited*** ("work on, not in, the business"; franchise prototype). Real; corroborated by readingraphics + systemhub summaries. **Verified.**
- **David Spinks — *The Business of Belonging* / CMX.** Real 4x community founder, co-founded CMX (2014), Wiley book ISBN 9781119766124. Corroborated ≥2 independent domains (amazon, newbooksnetwork, goodreads, nityesh). Lesson says "founded CMX" — sources say co-founded; minor imprecision, widely titled "founder of CMX." **Verified.**
- **Kevin Kelly — "1,000 True Fans"** (kk.org/thetechnium). Real (Wired founder); corroborated by kk.org + a16z "1000 True Fans / try 100." **Verified.**
- **Jakob Nielsen — 90-9-1 participation inequality** (Nielsen Norman Group). Real; corroborated by nngroup.com + Higher Logic. **Verified.**
- **Sam Ovens — Skool** (Hormozi/Acquisition.com major stake 2024, ~50/50, $1B+; $9 Hobby/$99 Pro, 2.9% Pro / ~10% Hobby). Real; corroborated ≥2 domains (skoolprep, communipass, dealroom, kourses, schoolmaker). Pricing + ownership match Thursday exactly. **Verified.**

No hallucinated authorities — the "Max Freiberg" failure mode is absent.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "A business in your head is a job with extra steps" states the real mechanism up front. |
| Chip Huyen | 8 | Day table maps each day to a concrete artifact and outcome. |
| Jerry Liu | 8 | Subordinates the week to two compounding assets (SOP layer, community layer). |
| Hamel Husain | 8 | "A stranger could join / execute" is a measured, checkable bar. |
| Simon Willison | 8 | No hype; the through-line is stated plainly. |
| Seibel | 9 | Sells the week in two paragraphs; the systematize-vs-sell tension is honored. |
| Boris Cherny | 8 | Points at the SOP-as-agent-spec idea without over-claiming. |
| Cohort peer | 8 | "Make it run without you, then give it a home" lands for a solo operator. |
| Mira Murati | 7 | Commercial framing sound; light on capability frontier. |
| swyx | 8 | "Community is the one asset AI cannot clone overnight" is the right 2026 read. |
| Ethan Mollick | 8 | Behavior design: the week is framed as two artifacts, not concepts. |
| Lilian Weng | 8 | Terminology (SOP hierarchy, TTFV, MRR/churn/LTV) consistent with dailies. |
| Jeremy Howard | 8 | Prereq wikilinks (w16/w17, w14) carry the load. |

**Weighted average: 8.0**

---

## 01-mon — SOPs: the operating system

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "SOP as OS" (trigger=interrupt, checklist=program, DoD=test) is a genuine model, not a slogan. |
| Chip Huyen | 8 | The four-part SOP spec is checkable, not vibes. |
| Jerry Liu | 8 | SOP-to-agent framed as a spec problem, correctly. |
| Hamel Husain | 9 | "AI draft is a well-spoken junior; you supply 'good'" is the right eval-flavored caution. |
| Simon Willison | 8 | Vendor claims ("AI automates the majority") hedged as vendor copy. |
| Seibel | 9 | His "you have a not-enough-customers problem" pushback IS the reviewer lens and the when-not-to section. |
| Boris Cherny | 9 | His stricter-SOP-for-agents pushback is the sharpest lens and feeds Saturday's generator. |
| Cohort peer | 8 | The bus test and "frequency × pain" sequencing are directly usable. |
| Mira Murati | 7 | Light on frontier; defensible for an ops topic. |
| swyx | 8 | AI-writes-vs-AI-runs distinction is the current, non-naive read. |
| Ethan Mollick | 8 | His "adoption, not prose, is the bottleneck" caveat is named. |
| Lilian Weng | 8 | SOP hierarchy consistent with Sunday's cards. |
| Jeremy Howard | 8 | b4w09 + b3w08 recapped one-line, wikilinked, not re-taught. |

**Weighted average: 8.2**

---

## 02-tue — Onboarding SOPs

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Front-load value, back-load information" is the real mechanism, derived not asserted. |
| Chip Huyen | 9 | Her "instrument your own funnel; benchmarks are directional" pushback is the lens. |
| Jerry Liu | 8 | Leading-vs-lagging measurement framed as the design point. |
| Hamel Husain | 8 | Day-3 flag → human reach-out is a concrete, testable rule. |
| Simon Willison | 8 | TTFV/activation stats carry search-verified stamps, not hype. |
| Seibel | 8 | "Hand-onboard your first five" pushback bounded and honored. |
| Boris Cherny | 8 | Automate-plumbing / keep-human-moment split is the tooling discipline. |
| Cohort peer | 8 | The T+5min → T+30day worked SOP is copyable. |
| Mira Murati | 7 | Benchmark-heavy; light on frontier. |
| swyx | 8 | AI-native onboarding lift framed with the adoption caveat. |
| Ethan Mollick | 8 | His "the tool does not save an unengaged user" caveat is the lens. |
| Lilian Weng | 8 | Activation/TTFV/day-3 taxonomy consistent with Sunday. |
| Jeremy Howard | 8 | b5w14 recapped, explicitly not re-taught; w19 wikilinked. |

**Weighted average: 8.0**

---

## 03-wed — Delivery & growth SOPs

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Quality gate as "check, don't trust the process" is the right structural point. |
| Chip Huyen | 8 | Rubric-not-vibe gate with named failure modes is measurable. |
| Jerry Liu | 9 | His "AI fluency masks errors; sharpen the gate as production speeds up" is the sharpest lens. |
| Hamel Husain | 9 | His "treat the delivery rubric as a real eval set" pushback is the lens and load-bearing. |
| Simon Willison | 8 | Deterministic-checks-before-judgment mirrors layered eval, cited to b2w04. |
| Seibel | 8 | His "don't systematize an unproven growth channel" pushback bounded. |
| Boris Cherny | 8 | Under-specified-SOP-scales-mistakes point tied to the agent column. |
| Cohort peer | 8 | The silent-run-through delegation test is directly actionable. |
| Mira Murati | 7 | Ops-heavy; light on frontier. |
| swyx | 8 | SOP-to-agent selection rubric is the current 2026 framing. |
| Ethan Mollick | 8 | "Let the failure teach the SOP" is real behavior design. |
| Lilian Weng | 8 | Three growth SOPs + three axes consistent with Sunday's cards. |
| Jeremy Howard | 8 | b2w04 + b6w17 + b3w08 wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 04-thu — Building community: the compounding moat

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Temporal irreducibility" of a network is the real moat mechanism, not a buzzword. |
| Chip Huyen | 8 | Active-core-direction framed as the honest signal vs vanity totals. |
| Jerry Liu | 8 | Free-as-funnel / paid-as-product is a clean strategic decomposition. |
| Hamel Husain | 8 | Cold-start "engineer the first interaction" is concrete and testable. |
| Simon Willison | 8 | Platform pricing hedged and search-verified; a16z used for the moat claim. |
| Seibel | 8 | His "don't build a community as procrastination" pushback honored in free-first sequencing. |
| Boris Cherny | 8 | "Own the audience off-platform" tooling discipline present (via swyx lens). |
| Cohort peer | 8 | Narrow-beats-broad cold-start advice lands for a first community. |
| Mira Murati | 7 | Platform-tactical; light on frontier. |
| swyx | 9 | His "rented land / own the email list" pushback is the sharpest lens. |
| Ethan Mollick | 8 | His "moat is slow and behavioral; most quit before the flywheel" is the lens. |
| Lilian Weng | 8 | 90-9-1 + 30%-update consistent with Sunday's cards. |
| Jeremy Howard | 8 | b5w13 + b6w17 + b1w02 wikilinked, not re-taught. |

**Weighted average: 8.0** (after this session's 5→2 contrast-tic trim)

---

## 05-fri — The paid inner circle & membership economics

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "LTV divides by churn" is the real lever, stated as mechanism with the math. |
| Chip Huyen | 9 | Her "instrument the early-warning metric before launch; avoid vanity engagement" is the lens. |
| Jerry Liu | 8 | Access + content + belonging bundle framed as why chat-with-a-paywall churns. |
| Hamel Husain | 8 | Net-MRR-movement as the honest number, not headline MRR. |
| Simon Willison | 8 | Churn/retention bands hedged, search-verified; LTV formula sourced. |
| Seibel | 8 | His "go get ten members before over-modeling" pushback bounded. |
| Boris Cherny | 8 | Ghost-town flag framed as a leading-indicator instrument, not a dashboard. |
| Cohort peer | 8 | The two-scenario worked example (healthy vs bleak) is concrete and copyable. |
| Mira Murati | 7 | Economics-heavy; light on frontier. |
| swyx | 8 | Platform-dependence risk to LTV is the correct 2026 caveat. |
| Ethan Mollick | 8 | "Why am I still paying on the 28th?" is real behavior design. |
| Lilian Weng | 8 | MRR/churn/LTV/CAC taxonomy consistent with code-lab + Sunday. |
| Jeremy Howard | 8 | b6w16 + b5w14 wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 06-sat — BUILD: SOP library + community launch

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Five-part build maps 1:1 to the two code-lab tools; no gold-plating. |
| Chip Huyen | 8 | Pass bar (c) forces stated break lines and a watched threshold. |
| Jerry Liu | 8 | Two-column human/agent view is a spec, not a vibe. |
| Hamel Husain | 8 | "Say so with the numbers, don't launch a treadmill" is a measured bar. |
| Simon Willison | 9 | Both tools verified to run clean; the worked example reproduces the demo exactly. |
| Seibel | 9 | His "ship the ugly version, ten founding members" pushback is the lens. |
| Boris Cherny | 9 | His agent-candidate-is-not-a-safety-certificate pushback is the sharpest lens. |
| Cohort peer | 8 | Stranger-executability pass bar is the discipline most build-days skip. |
| Mira Murati | 7 | No model-choice stage; inherited, defensible. |
| swyx | 8 | Seed-nucleus + founder-as-engine plan is the correct launch shape. |
| Ethan Mollick | 8 | Chip's "instrument from member one" behavior check is present. |
| Lilian Weng | 8 | SOP + membership artifacts consistent with the whole week. |
| Jeremy Howard | 8 | b3w08 + b6w16 wikilinked forward and back. |

**Weighted average: 8.2**

---

## 07-sun — Synthesis + quiz + flashcards + capstone

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Compresses to "a business in your head is a job; written down + community is an asset." |
| Chip Huyen | 8 | Q6/Q12 force the LTV math and the leading-indicator reasoning, not recall. |
| Jerry Liu | 8 | Block-7 arc (capture → deliver → systematize) is a clean synthesis. |
| Hamel Husain | 8 | Answer key precise; Q6 LTV = $1,440 verified by hand. |
| Simon Willison | 8 | Q9 platform-pricing answer matches the verified figures. |
| Seibel | 8 | Close-the-week reflection converts the week into a next action. |
| Boris Cherny | 8 | Q4/Q11 agent-vs-human answers match Monday and the generator. |
| Cohort peer | 9 | 15-question quiz + 30 cards calibrated; cold-quiz instruction correct. |
| Mira Murati | 7 | Forward pointer to Block 8 commercial; no frontier note. |
| swyx | 8 | Platform + moat cards current. |
| Ethan Mollick | 8 | "The week in one arc" schedules the mental model. |
| Lilian Weng | 8 | All 30 cards checked against weekday lessons; no contradictions. |
| Jeremy Howard | 8 | Capstone recap builds on w18/w19 (now upgraded) without re-teaching. |

**Weighted average: 8.0**

---

## code-lab/1 (README, requirements, sop_generator.py, membership_model.py)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-dependency stdlib; every formula and gate readable; the simplicity is the point. |
| Chip Huyen | 8 | Ghost-town flag is a real leading indicator with tunable, documented thresholds. |
| Jerry Liu | 8 | SOP-to-agent verdicts map 1:1 to Wednesday's rubric. |
| Hamel Husain | 9 | `py_compile` clean; demos exercise both healthy and dying paths exactly as documented. |
| Simon Willison | 9 | Numbers reproduce the lessons to the dollar; ARPU $69.57 → LTV $1,565 verified. |
| Seibel | 8 | Tiny by design so estimates get replaced with real numbers post-launch. |
| Boris Cherny | 9 | Verdict function fails safe (judgment → HUMAN-RUN; high error cost → HUMAN-IN-THE-LOOP). |
| Cohort peer | 8 | README runnable top-to-bottom; pass bar concrete. |
| Mira Murati | 7 | No LLM backend wired; correctly left as a guarded extension. |
| swyx | 8 | Standard-library-only, offline, 3.10+ floor correctly pinned. |
| Ethan Mollick | 8 | Pass bar ties output to a human decision (state your churn break line). |
| Lilian Weng | 8 | EngagementSnapshot / Tier taxonomy consistent with the lessons. |
| Jeremy Howard | 9 | Small, deterministic, no network; compiles and runs clean. |

**Weighted average: 8.4**

---

## Overall Week 20: **8.1 / 10**

(File averages: 8.0, 8.2, 8.0, 8.1, 8.0, 8.1, 8.2, 8.0, code-lab 8.4.) Strongest: Monday, Saturday, and the code-lab — reviewer lenses that genuinely argue against the text (Boris on stricter-SOPs-for-agents and agent-candidate-is-not-a-safety-certificate, Hamel/Jerry on the delivery rubric as a real eval set and AI-fluency masking errors, Chip on instrumenting the leading indicator before launch, swyx on rented-land communities) and a lab that compiles clean and reproduces every lesson number to the dollar, including the three-ground ghost-town flag. Anti-slop after the Thursday trim: em-dash 2.9–5.0/1k, contrast-tics ≤2/file, house tics in budget. Canonical homes (b2w04, b3w08, b4w09, b5w13/14, b6w16/17, b7w19) all wikilinked with one-line recaps — no re-teaching. All six named authorities verified real and correctly attributed.

---

## Surgical fixes applied this session (Phase 3, done)

1. **Wikilink upgrades (required):** removed all five `(pending)` markers now that Weeks 18 and 19 exist — 01-mon L47 (w19), 02-tue L50 + L199 (w19), 07-sun L62 (w18) + L65 (w19). Zero `(pending)` remain; all 18 wikilink targets resolve.
2. **04-thu contrast-scaffold-tic trim (5 → 2):** three "X is not Y, it is Z" constructions inverted to "Z, not X" form, meaning preserved — the ghost-town-with-a-logo line, "Community is a multiplier … not a separate business line," and the Mollick lens "the hard part is the months of unglamorous daily showing-up … well beyond the strategy itself."

No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Fast-moving facts carry `search-verified 2026-07-17; fetch egress-blocked — liveness pass pending` stamps** per the amended protocol. A Phase-4 liveness pass should re-hit live URLs for: community-platform pricing (Skool $9/$99 + fees, Circle $89/$199 + 2%/1%, Discord free — Stickyhive/SchoolMaker/Communipass), the hybrid-retention >96% and course 88-92% figures (Kourses/Churnkey), the TTFV/activation benchmarks (Digital Applied/Userpilot/productgrowth.in/Artisan/Perspective), and the Skool $1B+ valuation / ~50/50 ownership (Communipass/Dealroom).
2. **Several 2026 sources are secondary/SEO-tier** (Stickyhive, SchoolMaker, Communipass, Kourses, Eightx, Artisan Growth Strategies, F7i, digitalapplied, productgrowth.in, AI Profit Boardroom). Each load-bearing figure is corroborated across two domains and hedged, and the strongest claims lean on primaries (Gawande + NIH PMC for the checklist evidence; the arXiv Agent-S paper for SOP-to-agent; Wiley + a16z + NN/G for the evergreen names). Phase-4 could hunt stronger primaries for the membership-retention and TTFV benchmark bands.
3. **arXiv 2503.15520 ("Agent-S … automate SOPs")** is cited four times as the SOP-to-agent evidence. The ID/title were not independently fetch-verified this session (egress-blocked); the claim it supports (structured SOPs improve agent controllability) is evergreen and mild, and it is corroborated by the v7labs secondary. Phase-4 should confirm the arXiv ID resolves and the paper's framing matches before it carries more weight. Note the roster also references "Agent-S / arXiv 2503.15520" whereas the Week-15 lineage used a different Agent-S id — worth a one-line liveness check that 2503.15520 is the intended paper.
4. **"founded CMX" (Thu) is a minor imprecision** — Spinks co-founded CMX (2014). Multiple sources title him "founder of CMX," so the point holds; left unfixed to avoid over-editing a correct attribution.

---

_Review + surgical polish produced 2026-07-17. Files edited: 01-mon, 02-tue, 04-thu, 07-sun. No git commits made._
