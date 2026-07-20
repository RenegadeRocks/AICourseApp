---
type: review
phase: 2
week: week-21
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 21 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-8-briefs/_generator-base.md` (anti-slop + finale-fluff vigilance + ≥3-wikilink integration mandate + amended verification protocol), and `week-21-briefs.md`. This is a SYNTHESIS week: judged on integration-by-wikilink and *no re-teaching*, not on new-topic depth.

**Mechanical checks run this session (Python 3.11):** `py_compile planner.py system_map.py content_engine.py` — **clean**. `python planner.py system system.example.json` → renders the three-subsystem loop (Demand→Delivery→Money→Demand) and prints **`PASS — no orphan subsystems`** (all three boxes `[x]`), exactly as Saturday and the README claim. `python planner.py engine engine.example.json` → 20-row biweekly calendar (pillar + 4 derivatives × 4 cycles), 4×4 repurposing matrix, and engine-health **`STATUS: HEALTHY`** with open_rate 0.4200 (inside the 0.35–0.50 band the lessons cite), weekly_growth 0.0312, click_reply 0.0350, downstream_conversion 0.0060 — every metric passes its threshold, matching the "engine reports HEALTHY" line in Saturday's Priya example. The orphan-check and engine-health outputs the prose promises both reproduce.

**Internal consistency:** the recurring Priya law-firm case is coherent across Mon (leaks: unbilled expansion, missing referral loop, no money owner), Tue (agency vs SaaS vs ladder build-out), Thu ("The Retrieval Gate" newsletter), Sat (map passes after assigning money owner + case-study handoff). Substack 10% fee → ~$24k/yr at $20k/mo reproduces in Thu, Sat, and Sun A9 (10% × $20k × 12). Three-subsystem metrics (leads/wk; TTFV+retention; NRR+runway), four returns on authority, four engine-health metrics + weekly/monthly cadence, and the AI-assisted-vs-authored line are identical wherever they recur (dailies ↔ Sat ↔ Sun quiz ↔ 28 flashcards). Quiz answer key traces: A9 fee math, A6 82%/77% (Wed [^5]), A12 metric cadence all check.

**Anti-slop (extra finale vigilance):** em-dash density 6.4–11.1/1k across the eight files — all under the ~12 ceiling (Sat highest at 11.1). Contrast-scaffold tics ≤2/file (grep of "not X, it is/but Y" forms returns ≤1 per file). House tics ("load-bearing", "operator", "would push back") in budget. **No motivational padding or hollow closers** — the finale grandiosity trap is resisted: Sun's "close the week" is three concrete actions ("Did you publish?"), not a graduation speech; "My take" blocks argue against the text rather than inflate it. Passes finale-fluff vigilance.

**No re-teaching / integration density:** every prior is one-line-recapped and wikilinked, never re-taught — B0W01/02/03, B1W01/02, B2W04, B3W06, B4W09/11, B5W12/13/14, B6W15/16/17, B7W18/19/20. **All wikilinks resolve** (script-checked against the vault): 00-overview 8, Mon 28, Tue 5, Wed 9, Thu 9, Fri 5, Sat 12, Sun 3 — every lesson clears the ≥3 mandate, **zero unresolved, zero `(pending)`**. Forward link to Week 22 resolves.

**DATE NORMALIZATION (required, applied):** the generator left 23 `search-verified 2026-07-19` tags across Mon(1)/Tue(4)/Wed(6)/Thu(6)/Fri(4)/Sat(2). **All 23 normalized to 2026-07-17 this session.** Zero `2026-07-19` remain. All frontmatter/footer `_last_verified` were already 2026-07-17.

**NAME-VERIFICATION (≥2 corroborations each):**

- **Rob Walling — stair-step approach (MicroConf/TinySeed)** — real; corroborated by microconf.com + robwalling.com/essays. **Verified.**
- **Jason Fried & DHH — 37signals/Basecamp built from a web-design agency** — real; 37signals began as a web design firm (1999), Basecamp built internally, product ate the agency by 2005. Corroborated by basecamp.com/about + en.wikipedia.org/wiki/37signals. **Verified.**
- **Andrew Chen — "Law of Shitty Clickthroughs" (a16z)** — real a16z partner; corroborated by andrewchen.com + news.ycombinator.com. **Verified.**
- **Marty Cagan — *Inspired*/*Empowered* (SVPG)** — real SVPG founder; corroborated by svpg.com + amazon. **Verified.**
- **Michael Gerber — *E-Myth Revisited* ("work on, not in, the business")** — real; corroborated by goodreads + rosenbergassoc.com. **Verified.**
- **Kevin Kelly — "1,000 True Fans"** — real (Wired founder); kk.org/thetechnium + already verified in the Week-20 review. **Verified.**
- **Atul Gawande — *The Checklist Manifesto*** — real surgeon/author; atulgawande.com + NIH PMC4953332 (verified Week-20). **Verified.**

No hallucinated authorities (the "Max Freiberg" failure mode is absent). **Note:** "Kit (formerly ConvertKit)" appears only as a platform name — Nathan Barry is *not* attributed, so no misattribution risk.

**Citation sanity:** all fast-moving facts (Substack 10% / beehiiv 0% / Kit ~3.5% pricing, 35–50% open bands, email ~8% vs social ~3%, LinkedIn ~30%/55% demotion, X ~25% / LinkedIn ~41% AI-authored, vertical-SaaS 130%+ NRR, bootstrapped 3×/¼-CAC/35–40% survival) carry two-domain corroboration + `search-verified … fetch egress-blocked — liveness pass pending` stamps per the amended protocol. Newsletter-platform pricing is explicitly hedged ("confirm current numbers before you commit, because this layer moves").

---

## Per-file weighted scores

| File | Weighted avg | Note |
|---|---|---|
| 00-overview | 8.0 | Two-builds framing + week pass bar stated plainly; day table maps day→artifact. |
| 01-mon — complete system | 8.2 | Pipeline↔three-subsystem↔handoff cuts are genuine models; Priya audit exposes named leaks. Seibel/Chip/Mira lenses argue against the text. |
| 02-tue — agency vs SaaS | 8.1 | Five-rung ladder + timing rule resolves the controversy without hand-waving; Walling/37signals anchor it. swyx "which layer do you defend" lens is sharp. |
| 03-wed — thought-leadership thesis | 8.1 | POV Level-0→3 ladder is the strongest teaching device in the week; anti-slop premium quantified. Mollick survivorship + Simon specificity lenses land. |
| 04-thu — newsletter & engine | 8.1 | Platform table hedged and search-verified; idea→draft→edit→distribute pipeline concrete. Chip (opens inflated by MPP) + Jeremy (editing slop ≠ writing) lenses genuine. |
| 05-fri — content ops & the line | 8.0 | AI-assisted vs AI-authored drawn precisely; quality bar operationalized as a content eval. Hamel/Mollick/Karpathy lenses converge on "insight before the model." |
| 06-sat — BUILD | 8.2 | Five build steps map 1:1 to the two lab tools; pass bar literal and tool-checked. Boris "make the check stricter" lens feeds a real extension. |
| 07-sun — synthesis + quiz + flashcards | 8.0 | 12-Q quiz + 28 cards trace to the dailies; four controversies resolved crisply; no capstone inflation. |
| code-lab/1 | 8.4 | Zero-dependency stdlib; compiles clean; both tools reproduce the lessons' PASS + HEALTHY outputs exactly. Orphan/handoff validator fails loudly on missing fields. |

---

## Overall Week 21: **8.1 / 10**

Strongest: Monday, Saturday, and the code-lab — the three-subsystem/handoff model that debugs a real business, a build day whose pass bar is literally tool-enforced, and a lab that compiles clean and reproduces every claimed output (PASS — no orphans; STATUS: HEALTHY). The reviewer lenses genuinely push back (Chip on open-rate inflation and one-number dashboards as triggers-not-truth, Boris on making the schema check stricter, Mollick on authority's survivorship bias, swyx on defending your layer as AI eats the one below). Integration is the job here and it is done: every prior block wikilinked with a one-line recap, nothing re-taught, all links resolve. Finale-fluff vigilance passes — no motivational padding, no hollow closers.

---

## Surgical fixes applied this session (Phase 3, done)

1. **Date normalization (required):** all 23 `search-verified 2026-07-19` tags → `2026-07-17` across Mon, Tue, Wed, Thu, Fri, Sat. Zero `2026-07-19` remain.

No other edits needed — anti-slop, wikilinks (all resolve, none pending), and internal consistency were clean on arrival. No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Egress-blocked liveness pass pending.** All 2026 fast-moving facts carry `fetch egress-blocked — liveness pass pending` stamps. A Phase-4 pass should re-hit live URLs for the newsletter-platform pricing (Substack 10% / beehiiv 0% / Kit ~3.5% — thatmarketingbuddy, beehiiv), the open-rate and email-vs-social bands (clickminded, monday.com, heistbrain), the LinkedIn demotion figures (zoomsphere, rewarx), and the beehiiv State-of-Newsletters growth stats ($8M→$19M, 15%→30%).
2. **Several 2026 sources are secondary/SEO-tier** (wellows, entrepreneurloop, startupa.ge, workflows.io, gtmdelta, zoomsphere, thatmarketingbuddy). Each load-bearing figure is corroborated across two domains and hedged; the strongest claims lean on primaries (Gawande + NIH PMC, andrewchen, kk.org, svpg, hamel.dev). Phase-4 could hunt firmer primaries for the bootstrapped-survival and vertical-NRR bands.
3. **The Register [^1] (Wed) and the ~25%/~41% AI-authored figures** are the single most striking stats in the week; the article was not fetch-verified this session (egress-blocked). Corroborated by adweek/newsguard secondary; confirm the exact percentages resolve before they carry more weight.

---

_Review + surgical polish produced 2026-07-17. Files edited: 01-mon, 02-tue, 03-wed, 04-thu, 05-fri, 06-sat (date-tag normalization only). No git commits made._
