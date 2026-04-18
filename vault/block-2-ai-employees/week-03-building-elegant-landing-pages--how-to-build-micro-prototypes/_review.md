# Week 3 Review — Multi-Persona Reviewer Panel

**Reviewers rotated across lessons:** Guillermo Rauch (Vercel), Max Freiberg (Lovable), Adam Wathan (Tailwind), shadcn (shadcn/ui), Julian Shapiro (landing-page copy), Teresa Torres (continuous discovery), Jeff Gothelf (lean UX), plus secondary voices already named in-lesson (Laja, Gardner, Rauno Freiberg, Willison, Cherny, Kohavi, Fitzpatrick, Cagan).

**Criteria (1–10):** (1) L3 technical depth · (2) Citation quality · (3) Reviewer-lens sharpness · (4) Operator war stories · (5) Controversy engagement · (6) Cross-domain applicability · (7) Runnable experiment quality · (8) Problem set rigor · (9) Block 2 thesis fit · (10) Overall L3 quality

Word-count deliberately NOT penalized. Tight long content is treated as a feature.

---

## Summary — per-lesson score table

| Lesson | 1 Depth | 2 Cites | 3 Rev | 4 War | 5 Ctrl | 6 Cross | 7 Exp | 8 PSet | 9 Thesis | 10 Ovr | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-mon — landing page as conversion machine | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | **8.9** |
| 02-tue — how AI code-gen tools work | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 8 | 9 | 9 | **8.7** |
| 03-wed — design-system literacy | 9 | 8 | 9 | 7 | 8 | 8 | 9 | 8 | 9 | 8 | **8.3** |
| 04-thu — micro-prototype ladder | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | **9.0** |
| 05-fri — 4–8 hour prototype pipeline | 9 | 9 | 9 | 9 | 8 | 8 | 9 | 8 | 9 | 9 | **8.7** |
| 06-sat — validation instrumentation | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | **9.0** |
| 07-sun — synthesis / quiz / flashcards | 8 | 8 | 8 | 7 | 8 | 8 | 9 | 8 | 9 | 8 | **8.1** |

**Week average: 8.67** — well above the 8.0 target.

---

## 01-mon — Landing page as conversion machine

**Reviewer lens rotation:** Julian Shapiro (primary), Peep Laja (Wynter), Oli Gardner (Unbounce), Rob Hope (One Page Love), April Dunford.

**Strongest:**
- Conversion math is operationally load-bearing — the three-scenario "0.5-point lift" table (solo $8.6K, mid-market $3.6M, course $107K) forces the reader to match iteration budget to ceiling. This is the single sharpest move in the lesson and is exactly what separates L3 from L2.
- Shapiro's *Purchase Rate = Desire − (Labor + Confusion)* is quoted verbatim with correct attribution and operationalized via the seven-element anatomy AND Laja's four-layer hierarchy, with the synthesis ("Shapiro = skeleton, Laja = diagnostic") clearly articulated.
- TruckersReport 79.3% case study, NeuroMD 55.3%, Ensighten +35%/-20%, Basecamp 2014 counter-case all carry named operators + numbers + URLs.
- Binomial power table (0.5pt lift = 9,500 per variant) is diagnostic, not decorative.

**Weakest:**
- Problem 1's "3 AI-services operator landing pages" is slightly underspecified — a peer could satisfy it with generic SaaS pages rather than AI-services specifically. Fix: name 3 canonical pages (e.g., Vellum, Copy.ai, Jasper, or actual AI agency sites) as a starter corpus.
- Controversy 3 ("Book a demo vs try it now") is the weakest of the three — the position feels consensus rather than contested. Sharpen by naming a specific operator who publicly reversed on this (e.g., Gong's 2024 demo-first doubling-down after a trial experiment).

**Line-level fix targets:**
- Line ~113 ("self-serve-first pages in the $10K–$50K ACV range generally out-convert demo-only pages") — add a specific citation or soften to "anecdotally"; current phrasing implies a public benchmark that is not in the citation list.
- Line ~250 (mobile-first section (e)) — add the actual device-emulation-vs-real-phone failure mode with a named case.

**Rollup: 8.9 / 10.** A standard-setter for the week.

---

## 02-tue — How v0/Lovable/Bolt/Replit actually work

**Reviewer lens rotation:** Guillermo Rauch, Max Freiberg (Lovable), Swyx, Karpathy, Simon Willison, Anton Osika, Rauno Freiberg.

**Strongest:**
- The "four architectural bets, not four flavors of the same thing" frame is the load-bearing operator move and it is executed precisely — v0 = RSC streaming + shadcn vocabulary; Lovable = Supabase scaffolding pass; Bolt = WebContainer primitive; Replit = persistent workspace.
- The commodity-vs-envelope axis cleanly separates "what commodifies" (the model) from "what doesn't" (the envelope). This is the sharpest live-controversy treatment in the week.
- Numbers are everywhere and verifiable: 30%+ Vercel deploys from agents, Claude Code 75% share, Lovable $10M in 60 days with 15 people, Replit $2.8M→$150M in 9 months, Bolt $40M in 5 months, 43% AI-code redebug rate, CodeRabbit 1.7× issues.
- Rauch/Swyx/Karpathy/Willison/Osika/Rauno reviewer lens is the most diverse and specific in the week; each named critic disagrees with a specific lesson claim.

**Weakest:**
- Runnable experiment requires accounts on 4 paid tools — the graceful-degradation clause is good but buried. Move the "swap the fourth for a second Claude Code run" line into the phase header, not the prerequisites.
- Cross-domain applicability is slightly SaaS-biased — add one non-SaaS example (e.g., a legal-tech or healthcare operator who evaluated tool choice).

**Line-level fix targets:**
- Line ~133 ("Klinger-aligned... Rauch-aligned") — this is a good debate but neither position is given a hyperlinked source. Add Klinger's specific post URL and Rauch's specific counter post.
- Line ~297 expected-vs-observed bake-off results — these should be clearly marked as "author-observed across 2 runs" not as a published benchmark.

**Rollup: 8.7 / 10.**

---

## 03-wed — Design-system literacy

**Reviewer lens rotation:** Adam Wathan (primary), Steve Schoger, shadcn, Brian Lovin, Rauno Freiberg.

**Strongest:**
- The seven-variable framework is genuinely reusable — each variable gets a paste-ready override prompt that survives cross-tool handoff. This is the operator artifact with the highest transfer value in the week.
- OKLCH migration is treated as a first-class operator concern, not a designer curiosity. The hex-code briefing failure mode is sharp.
- Reading target aesthetics as seven-row tables (Linear, Raycast, Geist) is the specific move that collapses "make it like Linear" from vibe into brief.
- Wathan and Schoger push back on their own framework (scale ratio is less important than weight contrast; ship correct color *choices* before OKLCH technicals) — this is the right reviewer voice for the lesson.

**Weakest:**
- **Operator war stories is the weakest dimension at 7/10.** The three stories (shadcn Tailwind v4 migration, Rauno Devouring Details launch, Linear redesign) are named but thin on specific numbers. The migration story is the strongest; the other two would benefit from specific before/after data.
- Controversy engagement could sharpen — the shadcn wholesale-vs-plunder debate is well-framed but the motion-as-medium vs motion-as-tax reconciliation is slightly too diplomatic. Pick a side more forcefully, let Rauno's reviewer lens push back.
- Citation quality is good but not week-best — some secondary citations (LogRocket, Medium aggregators) where a primary source exists.

**Line-level fix targets:**
- Line ~228 (Story 1 operator lesson) — "retune hover states, not just base values" is good but needs a specific OKLCH example ("oklch(0.58 0.18 264) hover at 0.50 felt correct in HSL but reads muddy in OKLCH — moved to 0.52").
- Line ~232 (Story 3 Linear redesign) — add at least one quantified outcome (e.g., specific page-level metric Linear publicly disclosed post-redesign, or honest "Linear hasn't disclosed quantitative post-redesign metrics" note).
- Problem 5 ("two generated pages agreeing on ≥5 of 7 variables") — add a rubric for how to score "agreement" at the value level, otherwise this is unfalsifiable.

**Rollup: 8.3 / 10.** Lowest lesson in the week but still well above floor. Polish Phase 3 priority: war-story quantification.

---

## 04-thu — Micro-prototype ladder

**Reviewer lens rotation:** Alberto Savoia, Teresa Torres, Marty Cagan, Rob Fitzpatrick, Lenny Rachitsky, Andrew Chen.

**Strongest:**
- Torres × Savoia synthesis ("Torres picks the rung; Savoia instantiates the experiment") is the sharpest framework synthesis in the week.
- Three operator case studies are exceptional: Buffer two-page (rung 2, specific 4-day-to-paying-customer signal), Gmail Priority Inbox (rung 3, honest about limited public disclosure), Superhuman concierge (rung 4, specific "dozens of full-time onboarding specialists, ~2 hours per session, tens of thousands of customers"). Named + numbered + URLed.
- The Wilson-interval math box with the 6/50, 3/50, 12/100, 60/500 table is the most useful small-N operator artifact in the week. Second occurrence in Saturday's lesson is legitimate reinforcement, not duplication.
- The 2026 fake-door ethics position (CPPA Advisory 2024-02, $2,500/$7,500 penalties) is both current and operationally actionable.
- Cagan-vs-Savoia controversy 2 is the best-engaged controversy in the week — the synthesis ("ladder + Cagan bar are complementary") is earned, not hand-waved.

**Weakest:**
- Almost nothing. If forced to pick: Controversy 3 (concierge-in-Claude-Code-era) is labeled "partially unresolved" and could use one more specific operator example.

**Line-level fix targets:**
- Line ~194 (the CPPA penalty number) — verify $2,500/$7,500 is still current in the April 2026 enforcement calendar; the advisory was Sep 2024 and penalty amounts occasionally update.

**Rollup: 9.0 / 10.** Co-highest lesson in the week. No polish needed beyond minor verification.

---

## 05-fri — 4–8 hour prototype pipeline

**Reviewer lens rotation:** Boris Cherny, Erik Schluntz, Swyx, Simon Willison, Amjad Masad, Guillermo Rauch, Justin Welsh.

**Strongest:**
- The literal-timestamp shipping diary (0:00→4:40) is the most operationally teachable device in the week. The "gold-plating trap at hour 2" with specific 18-minute logo-mark failure is a war-story-within-a-war-story.
- Three reusable prompts (SPEC BRIEF, UI BRIEF, GLUE+INSTRUMENTATION BRIEF) are verbatim-pasteable, which is exactly the artifact a practitioner needs.
- Three parallel case runs (marketing-ops, legal-intake, ecommerce) do the cross-domain work inline rather than as afterthought.
- Reviewer lens is strong — Cherny pushing back on "1M context" as insufficient (subagents matter more), Schluntz pushing back on "Claude Code for full pipeline" (scope fluidity matters), Willison on prompt staleness, Masad on Replit-vs-Vercel deploy.

**Weakest:**
- Controversy engagement is slightly weaker than Tue/Thu/Sat — the n8n vs Worker and Figma Make vs v0 debates are live but the position-taking is softer than other lessons.
- The composite-run framing ("ran this twice — once for marketing-ops, once for legal-intake") is honest but slightly blurs the empirical base — a cleaner version would table the two runs' actual timings side-by-side so the ±10-min claim is visible.
- Resend rate-limit (3,000/mo, 100/day) is called out as a failure mode but not integrated into the actual pipeline cost math — add a "if you drive >100 visits in an hour, upgrade plan or queue" into the sanity-traffic phase.

**Line-level fix targets:**
- Line ~200 (hour 1:50 two-variant A/B) — wiring A/B to PostHog feature flags is deferred to Phase 4, but Phase 4 (instrumentation tightening) doesn't actually add the feature-flag wiring. Either add it or remove the forward reference.
- Problem 3 (write your three reusable prompts) — asks for ≥120/150/180 word minimums; these floors will push readers toward padding. Consider removing word floors and replacing with a behavioral test ("paste each into a fresh session tomorrow and confirm output lands on-spec in ≤2 rounds").

**Rollup: 8.7 / 10.**

---

## 06-sat — Validation instrumentation

**Reviewer lens rotation:** Teresa Torres, Rob Fitzpatrick, Ronny Kohavi, James Hawkins (PostHog), Aaron Cannon (Outset), Carl Pearson.

**Strongest:**
- Four-domain event model (B2B SaaS leadgen, ecommerce, creator waitlist, consulting leadgen) is the single cleanest cross-domain artifact in the week — same skeleton, four instantiations, each properly industry-specific.
- The Wilson-interval treatment is the clearest in the vault — three "all-12%" observations (6/50, 12/100, 60/500) worked in full with CI widths (18.6pp, 12.8pp, 5.8pp) and decision implications for each.
- Session-replay legal treatment is current and specific: WilmerHale 2024 review, Loeb & Loeb July 2025 advisory, Clarity Oct 31 2025 EEA enforcement, CPPA scroll-as-consent dark-pattern flag. Five-item compliance checklist is operator-ready.
- AI-moderated-interview treatment is the best controversy engagement in the week: Outset $51M + Nestlé "10×/2× depth" disclosure vs NN/g 2024 + Pearson May 2025 methodological critique. The resolution ("reach on structured; depth on generative") is earned.
- Mom-Test-hardened AI script with seven-question template is immediately reusable.
- Pre-registered decision rule at Layer 5 closes the loop with the Thursday ladder lesson cleanly.

**Weakest:**
- Almost nothing. Minor: the Wilson-interval repetition with Thursday could be explicitly framed as "reinforcement at a different point in the pipeline" rather than letting the reader wonder if it's duplication.

**Line-level fix targets:**
- Line ~152 (Outset customer list) — verify HubSpot and Uber as customers; the GlobeNewswire press release is primary but the 2026-04-17 re-verification is worth a quick re-check in Phase 4 citation pass.
- Line ~218 (Kohavi 55%→0.73% replication example) — the claim is load-bearing; make sure the *specific paper* being replicated is cited, not just the neweconomies.co secondary.

**Rollup: 9.0 / 10.** Co-highest lesson in the week.

---

## 07-sun — Synthesis / quiz / flashcards

**Reviewer lens rotation:** Peep Laja, Rauno Freiberg, Simon Willison, Ronny Kohavi, patio11.

**Strongest:**
- The four-collapse-mode frame (copy / tool / taste / rung) is a clean unifying device for the week.
- The 13-move mental-move table is the single most transferable artifact for flashcard-style recall.
- 20-question quiz mixes recall/apply/prompt-completion/controversy-defense proportions sensibly; answers are full-text, not one-liners.
- Reviewer-lens section ("where you'd still lose points") is unusually honest for a synthesis — the patio11 "4 hours is aspirational for engagement #1; honest for engagement #5" line is an important expectation reset.

**Weakest:**
- War stories dimension is low (7) because the synthesis reuses week examples rather than introducing new ones — this is appropriate for a synthesis, but it means the dimension should either be reframed or not scored as harshly. Scoring it 7 is fair against the rubric but functionally this is by-design.
- Some numbers are lightly paraphrased from source lessons without re-verification (e.g., Q7 PostHog free-tier "1M events"; Saturday's lesson cites "1M events and 5,000 session replays" — same, good). No actual error found, but a dedicated citation pass in Phase 4 polish should re-verify each flashcard number against the source lesson.
- Flashcard #32 (binomial CI shape) uses slightly different interval bounds than Sat's Layer 4 (5.9%–25.2% vs 5.6%–24.2% for 6/47 vs 6/50 — the input differs, so OK, but cross-reference clarity could improve).

**Line-level fix targets:**
- Q10 sample answer — "WCAG 2.2 contrast ≥ 7:1" is AAA for body text; standard AA is 4.5:1. Clarify which bar is being specified.
- Flashcard 26 ("+90.2% on internal research evals") — this is an Anthropic-published number but the specific eval is not named. Either name the eval or soften to "internal research-task evals."
- Flashcard 38–39 (88% POC kill rate, MIT NANDA 95%) — these are explicitly "reference, not re-taught" but the source-week citation should be named.

**Rollup: 8.1 / 10.** Strong synthesis; highest-value polish is citation-number re-verification.

---

## Week-level notes

### Thesis arc coherence

The six lessons compose cleanly into the week thesis ("hypothesis → anatomy → tool pick → taste brief → rung choice → 4-hour ship → instrumentation → go/no-go"). Each lesson genuinely sets up the next:

- Mon's Shapiro anatomy is what Fri's UI BRIEF templates reference.
- Tue's tool-pick tradeoffs are what Fri's STACK section of the SPEC BRIEF operationalizes.
- Wed's seven variables are what Fri's AESTHETIC target line compresses.
- Thu's rung ladder is what Sat's pre-registered thresholds assume.
- Sat's Wilson intervals are what Thu's sample-size math boxes introduced.
- Sun's synthesis correctly names the feedback loops, not just the forward chain.

No lesson feels like filler; no lesson over-reaches into the next week's territory (sales-agent, RAG, document-understanding are all referenced as Week 4–6 material without being taught).

### Duplication across days

Three legitimate reinforcements, zero actual duplication:

1. **Wilson/binomial CI math** appears Thu (Layer on small-N) and Sat (Layer 4 full treatment). This is legitimate — Thu introduces the concept for rung-selection, Sat deepens it for go/no-go decisioning. Could be flagged explicitly with "Sat will deepen this" at Thu's math box.
2. **Shapiro anatomy** appears Mon (full treatment) and Fri (invoked in the UI BRIEF). This is legitimate reuse.
3. **Mom Test** appears Thu (Fitzpatrick reviewer lens) and Sat (full seven-question script). Legitimate — Sat is the operational instantiation.

### Phase 3 polish priorities

In rank order:

1. **Wed war-story quantification** — the lesson's weakest dimension is the war-stories at 7/10. Add specific before/after numbers to the Rauno Devouring Details launch story and the Linear redesign story. **Highest ROI polish target.**
2. **Sun flashcard number re-verification** — cross-check every numeric flashcard against the source-lesson citation to prevent drift.
3. **Mon Controversy 3 sharpening** — name a specific operator who publicly reversed on demo-vs-trial to raise the controversy tension.
4. **Fri forward-reference cleanup** — the Phase 4 A/B-feature-flag reference (hour 1:50) should either be fulfilled or removed.
5. **Line-level fixes flagged per-lesson above** — all minor.

### Flagged-for-polish count

**3 lessons flagged:** Wed (priority 1 — war-stories dimension), Sun (priority 2 — flashcard verification), plus minor touches on Mon and Fri.

4 lessons ship as-is from a scoring perspective (Tue, Thu, Sat all above 8.5 average; Thu and Sat at 9.0 are week standard-setters).

### Overall

Week average **8.67** against an 8.0 target. This is the strongest week-opening scores the vault has seen on first-pass review. No lesson is below 8.0. The instrumentation discipline (Sat) and the rung ladder (Thu) are the standout lessons and could serve as reference exemplars for Week 4+ Phase 1 drafts.

---

_Reviewed 2026-04-17 — multi-persona panel, Phase 2 of 4-phase week-generation workflow._
