# block-2 / week-03 (landing pages + micro-prototypes) — Refresh Review Findings (2026-07-17)

Reviewed files: `00-overview.md`, `01-mon`, `02-tue`, `03-wed`, `04-thu`, `05-fri`, `06-sat`, `07-sun` in
`/home/user/AICourseApp/vault/block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/`.
All web claims below were checked via WebSearch on 2026-07-17. **Environment note:** direct WebFetch/curl to arbitrary
hosts is blocked by this session's egress policy (403 from proxy), so URL-resolution checks were done via
search-index existence, not direct fetch. Dead-link detection is therefore incomplete — the fix phase should re-run a
link check from an unrestricted session. Session web-search budget was exhausted after 16 rounds; items marked
**[NOT RE-VERIFIED]** below were not confirmed either way.

## Verdict

This week is a tale of two halves. The evergreen mechanics — Shapiro/Laja anatomy, seven-variable taste briefs,
Savoia/Torres rung selection, Wilson-interval discipline, Mom-Test-hardened interviews, session-replay compliance —
have aged well; Saturday in particular survives July 2026 nearly untouched. But the week's differentiating promise
("the specific failure modes of v0 vs Lovable vs Bolt vs Replit… that is this week") is exactly where it has rotted:
every one of the four tools has re-priced, re-platformed, or re-modeled since April; the frontier model story
(Sonnet 4.5 as coding flagship) is two generations behind Claude Fable 5; Anthropic shipped Claude Design, partially
resolving Tuesday's central open question; Bolt has a hard August 3, 2026 legacy-project cutoff a reader needs to know
about *now*; and Unbounce published a mid-year report that moves the week's most-repeated benchmark (6.6% → 8.1%).
There are also two internal math defects the April review flagged and the polish pass never fixed.

Currency grades: **00-overview C · 01-mon B− · 02-tue D+ · 03-wed B− · 04-thu B · 05-fri C · 06-sat A− · 07-sun C+.**
Week overall: **C+** — structurally sound, factually expired where it matters most.

---

## CRITICAL (untrue today / dead-wrong landscape / broken decision rules)

1. **[02-tue: "Why this matters" + [^1]; echoed in 00-overview §L3-depth-4] "over 30% of deployments on Vercel are
   now initiated by coding agents… Claude Code at ~75%"** — accurate for the Feb 2026 post it cites, but superseded:
   per Vercel Ship 2026 coverage and Rauch's own posts, agents now drive **more than half** of Vercel deployments
   (from under 3% six months prior). The lesson's flagship stat is ~2x stale.
   Current truth: https://www.digitalapplied.com/blog/vercel-ship-2026-agents-half-of-deployments-enterprise-stack ;
   original still live at https://vercel.com/blog/agentic-infrastructure (its 30%/1000%/75%/6%/1.5% figures verified
   as written — so it's a dating problem, not a fabrication problem).

2. **[02-tue: Layer 2, "Claude Sonnet 4.5 (September 2025) is Anthropic's coding flagship" [^21]; also Fri's
   "Opus 4.6 1M context" via shareuhack, Mon's "Claude Sonnet 4.6" aside, Fri reviewer-lens "Sonnet 4.4/4.6"]** —
   dead-wrong model landscape in July 2026. **Claude Fable 5 + Claude Mythos 5 launched June 9, 2026** (Fable 5 =
   publicly available Mythos-class model; SOTA on software engineering; $10/$50 per Mtok; export-control suspension
   June 12–30, generally available again from July 1 on Claude Platform/Claude.ai/Claude Code/Cowork). Opus 4.7
   shipped earlier in 2026 (powers Claude Design). Every model-name and "coding flagship" claim in the week needs a
   sweep. Sources: https://www.anthropic.com/news/claude-fable-5-mythos-5 ;
   https://techcrunch.com/2026/06/09/anthropics-claude-fable-5-is-a-version-of-mythos-the-public-can-access-today/ ;
   https://www.anthropic.com/news/redeploying-fable-5

3. **[02-tue: Replit section + Case study 2 + four-way table]** Replit story ends at "$150M annualized by Sept 2025,
   effort-based pricing with $0.06 floor" and **never mentions Replit Agent 3 — which launched September 2025, seven
   months before this lesson was written** (a truth defect even in April, not just staleness). Current truth:
   **50M users and ~$525M annualized revenue by April 2026 (up 1,775% YoY); $400M raised at $9B (March 2026);
   pricing is now credit-based tiers** (Starter free / Core $20-25 incl. ~$25 credits / Pro ~$95-100 incl. ~$100
   credits), not per-run effort pricing. The "checkpoint-diff-commit, $0.06–multi-dollar" description and the
   pricing-strategy "transfer" lesson built on it are obsolete.
   Sources: https://espressio.ai/blog/replit-guide-2026/ ; https://replit.com/pricing ;
   https://serenitiesai.com/articles/replit-agent-2026-features-pricing-review

4. **[02-tue: Bolt section [^16]; Fri optional reading [26]]** "Sonnet as historical default; June 2025 Sonnet 4
   partnership" presented as the current Bolt model story. Current truth: Bolt now exposes **two agents (Standard /
   Max) instead of model selection**; **v1 Agent (legacy) unselectable for new projects since April 13, 2026, and v1
   projects/sites become inaccessible after August 3, 2026** — an urgent, actionable fact for any reader who built
   Bolt projects while following this course in the spring. Also since April: MCP-server connections, in-chat AI
   image generation, Microsoft Azure/M365 partnership (May 2026). Source: https://support.bolt.new/release-notes

5. **[02-tue: four-way table, v0 row "Backend default: None (frontend-only by default)"; also "Where it fails" and
   the Phase-2 bake-off framing]** — no longer true. v0's Feb 2026 platform update added **database connectivity,
   Supabase CRUD, full Next.js apps incl. API routes and Server Actions, a VS Code-style editor, and agentic
   workflows**; pricing moved to **token-metered credits** (Free w/ $5 credits, Premium $20, Team $30/user, Business
   $100/user) with a ~3x price cut on v0 Max Fast in June 2026 and a new **Vercel Agent BETA SKU (July 2026)**.
   The lesson's v0-vs-Lovable division of labor ("Lovable if you need persistence, v0 returns a static UI and a todo
   item") is now partially false. Sources: https://www.nxcode.io/resources/news/v0-by-vercel-complete-guide-2026 ;
   https://uibakery.io/blog/vercel-v0-pricing-explained-what-you-get-and-how-it-compares ;
   https://vercel.com/blog/updated-v0-pricing ; https://www.usagepricing.com/blueprint/vercel

6. **[02-tue + 05-fri: Lovable numbers]** Fri's "Lovable went $100M → $200M ARR between July and November 2025 and
   raised a $330M Series B at $6.6B" is two cycles behind: **Series B closed December 2025 at $6.6B; ~$400M ARR by
   March 2026, $500M annualized announced June 2026; in talks (July 2026) to raise ~$300M at a $13.2B valuation
   (Menlo Ventures expected lead)**. Sources:
   https://techcrunch.com/2026/07/08/lovable-reportedly-in-talks-to-double-its-valuation-to-13-2b/ ;
   https://www.forbes.com/sites/rashishrivastava/2026/06/05/ai-coding-startup-lovable-in-talks-to-raise-funding-at-a-12-billion-valuation/ ;
   https://lovable.dev/blog/series-b

7. **[01-mon: Layer 1 [^1]–[^3]; 07-sun: quiz Q1–Q3, flashcards 1–6, mental-move row 2]** The week's most-repeated
   benchmark — "Unbounce median 6.6% across 41,000 pages" — is superseded. Unbounce's **mid-year CRO Intelligence
   Report (68,000 pages, 89M conversions) puts the global median at 8.1%**, described as the largest single-year
   benchmark jump, attributed to AI-assisted A/B testing adoption; it also adds directly-relevant new data
   (single-CTA pages 13.5% vs 10.5% multi-CTA — which *strengthens* Mon's attention-ratio argument and should be
   cited). Mon's own open question #2 said "watch the 2026 CBR" — it arrived, and the lesson doesn't know.
   Sources: https://unbounce.com/conversion-benchmark-report/ ;
   https://foundrycro.com/blog/landing-page-conversion-rate-benchmarks-2026/ ;
   https://searchlab.nl/en/statistics/conversion-optimization-statistics-2026 (secondary corroboration — fix phase
   should confirm the 8.1% figure against the Unbounce primary, which was not directly fetchable from this session).

8. **[04-thu: Rung 3, [^2], Problem 2; 06-sat inherits via CPPA references]** "civil penalties of up to $2,500 per
   violation and $7,500 for willful violations" — stale. CCPA penalty caps are CPI-adjusted: **2026 maxima are
   $2,663 (unintentional) and $7,988 (intentional/minor-related)**. The April `_review.md` explicitly ordered this
   verification ("verify $2,500/$7,500 is still current") and the polish pass never did it.
   Sources: https://www.clym.io/blog/ccpa-penalties-and-fines-what-businesses-need-to-know ;
   https://privacylawmap.com/blog/state-privacy-law-penalties-fines-guide ;
   advisory itself still live: https://cppa.ca.gov/announcements/2024/20240904.html

9. **[02-tue: Open question 1 [^30]; 05-fri Layer 2 + open questions; 04-thu controversy 3]** "Anthropic ships its
   own app-builder — leaks suggest it is coming" is no longer a rumor-grade bear case: **Anthropic shipped Claude
   Design (April 17, 2026, Anthropic Labs; prompt-to-prototype/design, powered by Claude Opus 4.7, for all paid
   tiers)** and **Claude Cowork went GA April 9, 2026** with Managed Agents in public beta; a further full-stack
   app-builder leak surfaced April 12, 2026. Tuesday's central controversy ("envelope vs model") now has its
   predicted disruptor partially on the field, and Fri's "Figma Make vs v0" duel is a three-way fight (the
   "Claude Design vs Figma Make" comparison is already its own content genre). The kingy.ai citation should be
   replaced with primary sources. Sources: https://www.anthropic.com/news/claude-design-anthropic-labs ;
   https://www.magicpatterns.com/blog/claude-design-vs-figma-make ;
   https://piunikaweb.com/2026/04/14/anthropic-claude-app-builder-leak/

10. **[05-fri: Layer 1/[4][5]; 02-tue open question 2 [^31]] "Figma Make, built on Claude 3.7"** — stale twice over:
    Figma Make is GA (out of beta) and offers **selectable Claude models including Opus 4.7** via Figma AI credits;
    and Figma Config 2026 has happened (Fri/Sun both say "watch Config 2026 / Q4 2026" as if future). Sources:
    https://www.figma.com/blog/figma-make-general-availability/ ;
    https://help.figma.com/hc/en-us/articles/36400680326551-Select-an-AI-model-to-use-in-Figma-Make ;
    https://help.figma.com/hc/en-us/articles/39582753756695-What-s-new-from-Config-2026

11. **[04-thu: "Sample-size math box"] Wrong Wilson-interval decision rule (math error, taught as a rule).**
    The box claims "observing ≤2/50 (≤4% observed) gives you an upper CI bound below 11% — kill." Recomputing:
    the Wilson 95% upper bound for 2/50 is **≈13.5%**, which does *not* exclude a 10% true rate — by the lesson's own
    logic 2/50 is still ambiguous, and the kill line as stated only holds at ≤1/50 (upper ≈10.5%, which the lesson's
    own table shows). Minor companion error: the 6/50 interval is [5.6%, 23.8%], not "24.2%" (Sat repeats 24.2 and a
    width of 18.6pp; true width ≈18.2pp; Sat also gives 60/500 upper as 15.2% where Thu says 15.1% — 15.1% is right).
    This is a pre-registration decision rule readers are told to write into their go/no-go memos; it must be fixed.

12. **[07-sun: flashcard 32 + mental-move row 11 vs 04-thu/06-sat] Internal contradiction on the week's core math.**
    Sun teaches "6/50 ≈ 4.7%–24.8%, 12/100 ≈ 6.4%–20.2%, 60/500 ≈ 9.3%–15.2%" while Thu/Sat teach Wilson
    [5.6, 23.8-24.2] / [7.0, 19.8] / [9.4, 15.1] **for the same inputs**. Sun's numbers match no interval Thu/Sat
    name (closest to Clopper-Pearson, unlabeled). A student drilling the flashcards memorizes different numbers than
    the lesson worked examples. The April review's #2 polish priority ("cross-check every numeric flashcard against
    the source lesson") was never executed. Fix: recompute all three as Wilson and label the method on the card.

---

## MAJOR (stale, weakened, shifted controversy, missing must-have)

1. **[01-mon: Layer 4 sample-size table]** The binomial power numbers look materially understated. Standard two-sided
   80%/95% calculation (the Evan Miller-style formula the lesson itself points readers to in Problem 5) for a
   0.5-pt absolute lift on a 2.5% baseline gives **≈16,500–17,000 per variant**, not "≈9,500"; 1.0-pt on 3.0% gives
   ≈5,300 not "≈3,900"; 2.0-pt gives ≈1,500 not "≈1,100". The qualitative conclusion (solo operators can't A/B)
   survives — and actually strengthens — but the numbers as printed don't reproduce with the recommended tool.
   Recompute and state the formula/tool used. (Computed analytically this pass; fix phase should confirm against
   evanmiller.org/ab-testing/sample-size.html.)

2. **[03-wed: Layer 3 entire shadcn section]** A full platform cycle behind. Since the lesson's newest shadcn fact
   (Oct 2025 components): **`npx shadcn create` (Dec 2025) with five visual styles (Vega, Nova, …); a visual project
   builder (Feb 2026); shadcn/cli v4 (Mar 2026); `shadcn preset` commands (Apr 2026); a registry *platform* with an
   official directory of ~149 registries, GitHub-backed registries (v4.10), and May 2026 registry include/validate.**
   This materially weakens the lesson's anti-wholesale argument #3 ("aesthetic homogeneity… every shadcn page looks
   the same") — first-party styles/presets now exist precisely to break homogeneity — and changes Wed's operator
   guidance: a seven-variable taste brief can now be encoded as a shareable preset handed to coding agents, which is
   exactly the artifact this lesson teaches readers to build by hand. The "835+ open PRs / Issue #6417 / Radix-WorkOS
   risk" claims were **[NOT RE-VERIFIED]** this pass and should be re-checked before being repeated.
   Sources: https://ui.shadcn.com/docs/changelog/2025-12-shadcn-create ;
   https://ui.shadcn.com/docs/changelog/2026-04-preset-commands ; https://ui.shadcn.com/docs/changelog/2026-03-cli-v4 ;
   https://www.infoq.com/news/2026/02/shadcn-ui-builder/ ; https://ui.shadcn.com/docs/directory

3. **[02-tue: "The four-way summary that matters" table + Problem 1/5]** Beyond the v0 backend cell (CRITICAL #5),
   the whole comparison table needs a July 2026 pass: Bolt's "Framework-agnostic; Vite default" row says nothing of
   Standard/Max agents or MCP; Replit's row predates Agent 3; per-tool cost axes (Problem 5 asks for "cost per
   project… with specific numbers") now resolve against changed pricing on all four tools. The bake-off experiment's
   "Expected vs observed" percentages (v0 ~75% aesthetic match etc.) are author-observed under superseded model
   versions — should be re-run or re-dated.

4. **[05-fri: Layer 2 tool-comparison]** The shareuhack/DEV comparisons quote "1M token context (Opus 4.6)" vs
   "Cursor 128K-256K" — a pre-Fable-5 snapshot. Claude Code itself has moved (per July 2026 coverage: `/goal`
   command with autonomous completion conditions, agent teams, local↔web session teleport; Cherny's current public
   setup describes 5–10 parallel claude.ai/code sessions). The "my position" (one-orchestrator wins for 4-hour
   ships) probably still holds but its evidence base is dated. Sources:
   https://linas.substack.com/p/anthropic-claude-2026-every-launch-guide ; https://howborisusesclaudecode.com/

5. **[05-fri: citation [8] + Willison reviewer-lens]** *Agentic Engineering Patterns* is real but is dated "(2025)"
   — Willison announced the project **Feb 23, 2026** (simonwillison.net/2026/Feb/23/agentic-engineering-patterns/).
   The "Nov 2025 model-capability inflection he flagged" attribution is questionable: the publicly documented
   inflection claim of that shape is **Karpathy's, dated December 2025** (Sequoia Ascent 2026). Likely
   misattribution; verify or reassign. Sources: https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ ;
   https://karpathy.bearblog.dev/sequoia-ascent-2026/

6. **[02-tue: reviewer lens, Karpathy entry [^33][^34]]** Held up well — "agentic engineering" is now formalized
   (Sequoia Ascent 2026 framing: vibe coding raises the floor, agentic engineering raises the ceiling; spec design /
   diff review / eval design as core skills). The lesson's Karpathy paragraph should be upgraded from "his 2026
   evolution" to the concrete Ascent framework, which maps almost 1:1 onto the lesson's aesthetic-brief-vs-agent
   point. Source: https://karpathy.bearblog.dev/sequoia-ascent-2026/

7. **[00-overview: "What L3 depth means" + thesis]** The overview hard-codes the now-stale numbers (30%+ deploys,
   Lovable $10M-in-60-days as the current fact, Replit $2.8M→$150M, Bolt $40M) as the week's evidentiary spine.
   When Tue is fixed, the overview must be re-anchored in the same pass or the two will contradict.

8. **[01-mon: Controversy 3 + _review carryover]** April review asked for a named operator who publicly reversed on
   demo-vs-trial ("e.g., Gong") — never added; the controversy still reads consensus-grade. Also [^10] cites
   aggregators (Landingi, digitalapplied) for NeuroMD/Ensighten when primary sources exist and were located this
   pass: SplitBase's own NeuroMD case study (https://splitbase.com/case-studies/landing-pages-neuromd, "55.3%
   increase… against pages it was tested against") and ToTheWeb's Ensighten PDF
   (https://totheweb.com/wp-content/uploads/2021/08/totheweb-ensighten-ppc-landing-page-optimization-case-study.pdf,
   +35% conversion / −20% ad spend / +9% total conversions). Upgrade the citations; note the Ensighten case is a
   ~2021 study, so presenting it under "2024–2026" aggregator dates overstates freshness.

9. **[Cross-file inconsistency: mobile share]** Mon teaches "mobile is 82.9% of visit volume" [^1]; Fri and Sat both
   assert "mobile traffic is 75%+ in 2026." Both can't be the week's number. Pick one (and re-check against the 2026
   Unbounce mid-year data when re-anchoring CRITICAL #7).

10. **[02-tue vs 05-fri: v0 user count]** Tue: "more than 4 million people have used v0" [^2]; Fri (Lenny cite [22]):
    "v0 has grown to 3 million users." Same week, two numbers, no dates attached. Reconcile and date-stamp.

11. **[05-fri: deploy phase] "CVE-2025-66478" Next.js deploy-blocking claim** — **[NOT RE-VERIFIED]**; the CVE ID
    could not be checked this pass and Vercel's changelog was not fetchable. Given the reader is told to expect
    deploy failures from it, verify the CVE exists and is still the operative example (a 2026 CVE may have replaced
    it).

12. **[04-thu: Controversy 3 / Andrew Chen "new rung" claim]** The AI-in-the-loop concierge question has moved:
    with Claude Cowork GA and Managed Agents (April 2026), the founder-driving-Claude concierge now has a
    productized form. The "public data is thin" caveat is increasingly untrue; refresh with the April–June 2026
    releases. (Chen's position aging well is worth stating.)

13. **[05-fri: n8n pricing claims]** "$50/mo for 100k-task flows vs $500+/mo elsewhere" rests on a Medium landscape
    piece — **[NOT RE-VERIFIED]** this pass (budget). n8n changed pricing structure repeatedly in 2025; re-verify
    against n8n.io/pricing before repeating specific dollar figures.

14. **[06-sat]** Positive finding: the AI-moderated-interview category facts (Outset $30M Series B Dec 2025 / $51M
    total; Listen Labs $69M Ribbit-led at $500M+; Strella $14M Bessemer Oct 2025; Maze June 2024) and the
    compliance layer (Clarity Oct 31 2025 EEA consent enforcement — verified:
    https://www.cookiehub.com/blog/dont-lose-your-clarity-data ;
    https://clarity.microsoft.com/blog/clarity-cookie-consent-update/) **held up**. Funding figures themselves were
    not re-searched this pass (no contradiction surfaced anywhere); a light July-2026 sweep for Series C/acquisition
    news in this category is still advisable in the fix phase.

---

## CITATIONS (spot-check results)

**Verified real and accurate (via search-index):**
- [02-tue ^1] vercel.com/blog/agentic-infrastructure — exists; 30%/1000%/75%/6%/1.5% figures match the post
  (superseded by newer data, see CRITICAL #1).
- [01-mon ^12] Welsh X post status/1874418985271259339 — real; text matches "$4.15M+ … ~86% margins … 177K LinkedIn
  … 43K X" verbatim. (https://x.com/thejustinwelsh/status/1874418985271259339)
- [05-fri 8] simonw.substack.com/p/agentic-engineering-patterns — real; **mis-dated** (2026, not 2025) and the
  Nov-2025-inflection attribution is doubtful (see MAJOR #5).
- [02-tue ^29 / 05-fri must-read] howborisusesclaudecode.com — real ("121+ tips" site); content matches the
  orchestration-of-multiple-sessions claim.
- [05-fri 27] resend.com/pricing — free tier still 3,000/mo + 100/day (July 2026); the lesson's numbers are current.
- [06-sat ^5 / 07-sun Q7, flashcards 28–29] PostHog free tier — 1M events / 5k replays / 1M flag requests and
  $0.005/replay all still current mid-2026; one of the few numeric claims in the week that needed no change.
- [06-sat ^8] Clarity Oct 31 2025 EEA/UK/CH consent enforcement — verified real and correctly characterized.
- [04-thu ^2] cppa.ca.gov advisory — resolves; **penalty amounts in the lesson's summary are stale** (CRITICAL #8).
- [01-mon ^10] NeuroMD +55.3% and Ensighten +35%/−20% — both real, but cited to aggregators; primary sources found
  (see MAJOR #8), and Ensighten is a ~2021 case dressed in 2024–2026 aggregator clothing.
- [07-sun move-6 / flashcard 16] "Shadcn Create (late 2025)" — real (`npx shadcn create`, Dec 2025). Sun was ahead
  of Wed here; Wed doesn't mention it at all.

**Weak / replaceable:**
- [02-tue ^30] kingy.ai Anthropic-leak post — was already flagged "secondary" in April; now obsolete as the
  load-bearing source for the bear case since Claude Design shipped and better-sourced 2026 leak coverage exists.
- [05-fri 6, 7, 10, 11] shareuhack / DEV showdown / Medium n8n-landscape / Latenode — blog-tier sources carrying
  specific numeric claims (context windows, $/mo); all now dated or unverifiable. Replace or re-date.
- [02-tue ^4] Growth Unhinged "Inside Replit's path to $100M ARR — Jason Donahue" — Growth Unhinged is Kyle Poyar's
  newsletter; the "Jason Donahue" byline looks like a misattribution **[NOT RE-VERIFIED — check byline in fix phase]**.

**Not checked this pass (budget/egress):** VentureBeat 43%-redebug (Lightrun), IEEE Spectrum silent-failures,
CodeRabbit 1.7x, TruckersReport CXL, Kohavi 55%→0.73% replication (neweconomies.co — April review already asked for
the primary paper; still not added), Sacra Replit page, Lovable one-year blog, Outset/Listen/Strella press releases,
Vercel changelog CVE. None showed contradictions in adjacent search results, but per the brief's ≥8-per-lesson
sampling bar, the fix phase should finish this list from a session with fetch access.

**Hallucination watch:**
- **"Max Freiberg (Lovable)"** — named in `00-overview.md` (reviewer-lens roster, §L3-depth-5) and `_review.md`.
  No such Lovable figure is findable; Lovable's public faces are Anton Osika and Fabian Hedin, and "Freiberg" is
  Rauno Freiberg (Vercel). This looks like a conflated/hallucinated person. Remove or correct in 00-overview
  (content file). **[Could not be positively disproven with budget exhausted, but treat as guilty until verified.]**
- "Andreas Klinger… PROTOTYPE Capital threads" [02-tue Layer 2] — still cited with no URL, exactly as the April
  review complained. Either find the primary thread or drop the attribution.
- CVE-2025-66478 — see MAJOR #11.

---

## SLOP (per file)

**Contrast-scaffold tic ("not X — it's Y" and variants), counts per file — week total ≈ 30, far over budget:**
- 00-overview: 3 ("Not because it is small, but because…", "a brochure / a demo with no denominator" pairing,
  "mechanical ones" vs "vibes answers").
- 01-mon: **7** — "not a communication artifact. It is a function…"; "Reading level is not a stylistic choice. It is
  a conversion lever."; "entirely a measurement problem, not a design problem"; "It is not a framework; it is a
  three-column spreadsheet"; "a *default*, not an *outcome*" (this one earns its keep); "The lesson isn't 'always
  A/B test'; it's…"; "trust-depressors, not trust-builders".
- 02-tue: **6** — the four parallel "X's differentiator is not the model — it is Y" constructions (deliberate
  parallelism, but it is the tic four times in a row), plus "not four flavors of the same thing", "This is not a
  bug — it is the maximum-likelihood output".
- 03-wed: 3 — "Motion is signal, not decoration"; "That page is not bad. It is *generic*"; reviewer-lens "doesn't
  produce taste — it produces coherent boringness".
- 04-thu: 4 — "Rung 4 is a test, not a product"; "'cheap to build' is not the same as 'cheap to learn from'"; "not a
  signal; the interval is"; "demand signal… not yet user signal".
- 05-fri: 4 — "Claude Code is not a coding tool — it is an orchestrator"; "not instructions to a single intelligence
  — they are briefs"; "Not 'here are the tools'"; "The capability delta is not 'can build a landing page'".
- 06-sat: 3 — "the instrument, not the tool"; "a division of labor, not a hedge"; "validation rather than
  confirmation-bias with a dashboard". Lowest density in the week.
- 07-sun: **6** — "a signed contract with reality, not a demo" (used twice); "not a linear waterfall"; "a vibe…
  a brief"; "updating a prior, not measuring an effect" (twice more in flashcards); "a floor, not a ceiling";
  "a target, not a promise".

**Fluff:** low by vault standards — no "delve"/"game-changer"/empty intensifiers found. Residual padding pattern:
punchy one-sentence paragraph-closers used as applause lines ("That is the bar." "That discomfort is the education."
"That's the point." "This is the rung-selection muscle.") — ~8 instances across the week; trim half.

**Repetition within week:**
- Wilson/CI math taught **three** times (Thu, Sat, Sun) — the third instance introduces the contradictory numbers
  (CRITICAL #12). Two instances are legitimate reinforcement (April review agreed); Sun should reference, not
  re-state, the numbers.
- "Vercel template / default aesthetic" described afresh in Tue, Wed, Fri, and Sun with near-identical inventory
  (gradient hero, rounded-pill CTA, three feature cards…) — 4x; consolidate to one canonical description + links.
- Mobile-share stat appears three times with two different values (see MAJOR #9).
- Cross-week duplication candidates for the dedup agent: Shapiro anatomy (Mon ↔ Block 1 Week 1 references),
  IDC 88% / MIT NANDA 95% (Sun flashcards 38–39, correctly labeled as references), Mom Test (Thu/Sat ↔ any Block 3
  interview content).

**Length vs standard:** every lesson targets 6,000 words while `quality-standard.md` §6 says core lessons are
2,000–4,000 ("longer is padded") and CLAUDE.md says 5,000–6,500. The two standards conflict; the vault should
reconcile them, since "is this padded?" is unanswerable while the bar is ambiguous. (Not a Week-3-specific defect.)

---

## MISSING (what a July-2026 reader needs that isn't here)

1. **Claude Fable 5 / Claude 5 family (June 2026)** — the substrate under all four tools changed; Tue's
   "model commodifies within a release cycle" thesis just got its cleanest test case and the lesson can't name it.
   Include the June 12–30 export-control suspension as an operator lesson in platform risk.
2. **Claude Design (April 2026)** — belongs in Tue's landscape, Wed's taste layer (a first-party
   aesthetic-generation surface), and Fri's asset-atelier phase as a Figma Make alternative.
3. **Claude Cowork GA + Managed Agents + Claude Code `/goal` / agent teams** — Fri's orchestrator section teaches an
   April-2026 Claude Code; the pipeline's Phase 1/Phase 4 should at least name `/goal`-style completion conditions.
4. **Replit Agent 3** — required for Tue to be credible at all (it existed before the lesson was written).
5. **Bolt v1→v2 migration + August 3, 2026 legacy cutoff** — time-sensitive; readers with spring-built Bolt
   prototypes need an explicit migration warning.
6. **v0 token-based pricing, full-stack capability, Vercel Agent SKU** — reshapes Tue's table, Fri's stack lock, and
   Problem 5's cost math.
7. **shadcn create / presets / CLI v4 / registry platform** — Wed's controversy needs the 2026 state; teach "encode
   your taste brief as a preset" as the new operator move.
8. **Unbounce mid-year 2026 CRO Intelligence Report (8.1% median; single-vs-multi-CTA data)** — re-anchor Mon and
   all Sun artifacts; answers Mon's open question #2.
9. **Updated commodity-vs-envelope scoreboard** — Lovable $500M ARR/$13.2B talks, Replit $525M/$9B, Bolt's
   Azure/enterprise turn: the envelope thesis is winning and the lesson should say so with 2026 numbers.
10. **Figma Config 2026 outcomes** — both forward references ("watch Config 2026") are now backward references.
11. **CPI-adjusted CCPA penalties** ($2,663/$7,988) plus any 2026 CPPA enforcement actions against session
    replay/dark patterns (fix phase: check CPPA announcements for 2026 orders).

---

## PERSONA VERDICTS

- **Karpathy:** "Your Thursday math box tells people to kill at 2/50 with an upper bound you computed wrong — fix
  the arithmetic before the philosophy; and my 'agentic engineering' now has a concrete skills list you're
  paraphrasing from memory."
- **Chip Huyen:** "Every cost number a reader would put in a spreadsheet — Replit per-run, v0 credits, n8n $/mo,
  Bolt tokens — is from a pricing regime that no longer exists; the ops advice is fine, the unit economics are
  fiction."
- **Jerry Liu:** "The pipeline treats retrieval/glue as n8n-vs-Worker; by July 2026 MCP-native glue is the default
  question and your own open question predicted it — promote it from footnote to section."
- **Hamel Husain:** "The bake-off is a one-shot vibe eval — 'expected ~75% aesthetic match' with no rubric, N=2
  author runs, run on superseded models; swyx's own critique in your reviewer lens says to make it a repeatable
  harness, so do it."
- **Simon Willison:** "You cite my Patterns project with the wrong year and possibly someone else's inflection
  claim; also your CVE example is unverified — my whole point is you check these."
- **Michael Seibel:** "The one thing a builder must know this month — Bolt deletes v1 project access Aug 3 — isn't
  in the lesson; everything else is commentary."
- **Boris Cherny:** "The subagent framing aged fine, but Claude Code grew /goal, agent teams, and web teleport since
  April; my public setup you cite has moved too — re-read the source you named after me."
- **Cohort peer:** "Readable and genuinely useful, but I memorized flashcard 32 and then failed quiz-by-Saturday
  because the lesson's numbers disagree with the cards."
- **Mira Murati:** "The lesson's landscape says Anthropic *might* enter the builder market; it entered in April, the
  frontier model changed in June, and half of Vercel deploys are agent-initiated — the strategic picture is a
  quarter out of date, which in this market is a full generation."
- **swyx:** "The stack is still recognizable, but 2026 AI engineers pick between v0-full-stack, Lovable, Bolt v2,
  Replit Agent 3, and Claude Design with token-metered pricing everywhere — the tool chapter needs a rev, and my
  eval-layer moat point deserved a section, not a paragraph."
- **Ethan Mollick:** "The adoption claims that were verifiable held up (PostHog, Resend, Clarity, Welsh); the
  behavioral claim that 'AI-assisted A/B testing' just moved the global conversion median to 8.1% is exactly the
  kind of research-backed shift this lesson should be teaching, not missing."
- **Lilian Weng:** "The agent-pattern claims are secondhand (Cherny via substack summaries) and the
  AI-moderated-interview evidence is vendor-disclosed; the NN/g and Pearson critiques carried the rigor — keep that
  balance and update it with any 2026 follow-up studies."
- **Jeremy Howard:** "The seven-variable and rung-ladder teaching is real understanding, not ceremony; the ceremony
  is the thirty 'not X — it's Y' constructions and the applause-line paragraph closers — cut them and the week gets
  denser and better."
