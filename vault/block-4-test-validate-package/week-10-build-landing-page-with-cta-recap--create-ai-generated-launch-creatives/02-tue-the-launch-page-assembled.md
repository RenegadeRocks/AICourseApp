---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 2
day_name: tue
session_slug: build-landing-page-with-cta-recap
date_due: 2026-07-21
tags: [launch-page, demo-embedding, interactive-demo, live-sandbox, cta-design, demo-vs-trial, waitlist, security-faq, social-proof, navattic, arcade, storylane]
sources:
  - arcade-best-interactive-demo-2026
  - storylane-vs-navattic-2026
  - demosmith-navattic-storylane-arcade
  - navattic-state-of-interactive-demo-2026
  - growthspree-demo-benchmarks-2026
  - growthspree-trial-benchmarks-2026
  - chartmogul-saas-conversion-report
  - growleads-trials-vs-demos
  - ftc-fake-reviews-rule
  - okta-enterprise-buyer-ai-agent-security-survey
last_verified: 2026-07-17
word_count_target: 5000
---

# The launch page, assembled — demo embedding, CTA choice, objection sections, and honest proof at three customers

## Why this matters

Yesterday you wrote the argument. Today you build the machine that delivers it: the actual page, section by section, with the three decisions that determine most of its conversion before a single word of polish. Which demo asset to embed (live sandbox, interactive tour, or video) is a risk decision disguised as a design decision. Which CTA to run (book a demo, start a trial, join a waitlist) is a sales-strategy decision disguised as a button label. And what to do about social proof when you have three customers is an honesty decision disguised as a layout problem. Operators get these three wrong more often than they get copy wrong, and the errors are quieter: a mis-calibrated CTA doesn't look broken, it just converts a third of what it should.

By tonight you will have a complete page skeleton for your Week 9 package: sections ordered, demo asset chosen with a fallback, CTA selected from a decision framework backed by 2026 benchmark data, and a proof plan that survives the fact that you are small. Saturday turns the skeleton into a shipped page.

## Prerequisites

- Monday's outputs: hero, objection map, eval section draft, pricing model. Today assumes them.
- [[05-fri-prototype-pipeline|Block 2 Week 3 Friday]]'s build pipeline: you can go from spec to deployed page with Claude Code plus your codegen tool of choice. We do not re-teach the tooling.
- The security mental model from [[03-wed-mcp-security|Block 0 Week 2 Wednesday]] (prompt injection, lethal trifecta). It returns today in an unexpected place: your marketing page.

## Layer 1 — The Week 3 recap, in one table (and only one table)

The session title says "Recap," so here it is, compressed to its operational minimums. Everything in this table is taught properly in [[01-mon-landing-page-as-conversion-machine|Block 2 Week 3]] and its siblings; if any row feels unfamiliar, that lesson is your remedial reading tonight, not this one.

| Discipline | The one-line version | Canonical home |
|---|---|---|
| Anatomy | Shapiro's seven modules; hero carries the page; header must pass the one-read test | [[01-mon-landing-page-as-conversion-machine]] |
| Conversion math | Lift value = visitors × Δconversion × revenue per conversion; know your number before optimizing | [[01-mon-landing-page-as-conversion-machine]] |
| Diagnosis | Laja's clarity → relevance → value → differentiation; find the broken layer, don't redesign blindly | [[01-mon-landing-page-as-conversion-machine]] |
| Attention ratio | One page, one goal; count tappable elements; AI codegen defaults to homepage-shaped clutter | [[01-mon-landing-page-as-conversion-machine]] |
| Design system | Seven variables (type, color, spacing, density, motion, imagery, voice); pick a reference aesthetic and hold it | [[03-wed-design-system-literacy]] |
| Statistics | Small-N is noise; Wilson intervals; pre-registered decision rules; no peeking | [[06-sat-validation-instrumentation]] |
| Cheap validation | The pretotyping ladder; waitlists and fake doors are experiments with ethics attached | [[04-thu-micro-prototype-ladder]] |

That is the whole recap. The rest of today is what Week 3 could not teach, because it is specific to selling an agent.

## Layer 2 — The demo embedding decision: video, interactive tour, or live sandbox

Monday's proof hierarchy put live product contact at the top. Today's question is whether you can afford the top, and the answer is a genuine 2026 controversy.

### The three options, with current tooling

**Recorded video of real runs.** Cheapest, safest, weakest. Production tooling is Thursday's topic; the decision-relevant fact is that a real-run video costs you an afternoon and risks nothing at runtime.

**Interactive demo / guided tour.** The middle rung has become a proper product category. The three leaders as of mid-2026, verified pricing: Arcade (Growth moved to a flat ~$297.50/month including 5 seats, from per-seat pricing), Storylane (free tier; Starter $40/seat/month; Growth $500/month), and Navattic (enterprise-oriented HTML capture, from ~$500/month).[^1][^2] All three now ship AI-assisted production (auto-generated voiceover, translation), and the category's own data is worth knowing: Navattic's 2026 State of the Interactive Product Demo analyzed 40,000+ demos built on its platform (up 43 percent year over year), with top-percentile demos reaching click-through rates around 70 percent.[^3] Treat vendor-published engagement numbers as directional, but the mechanism is real: an interactive tour lets the buyer *do* something, and doing converts better than watching.

Two developments matter specifically for agent products. First, Navattic launched Agent Demos (in beta as of 2026): autonomous walkthroughs where an AI drives the demo, which is philosophically odd (an AI performing a scripted version of your AI) but useful for personalization at scale.[^3] Second, and more important: an interactive tour of an *agent* is a curated replay. It shows the happy path with perfect reliability precisely because it is not running your agent. That is both its safety and its epistemic limit, and sophisticated buyers know the difference.

**Live sandbox.** The buyer types real input; your actual agent runs. Highest proof value on the page, and four distinct ways to hurt yourself:

1. **The worst-run problem.** Your landing page now performs your tail latencies and tail failures in public, to your least-committed audience, with no human present to contextualize. A buyer who gets a bad completion on their first anonymous visit does not file it as variance; they file it as truth and leave.
2. **Prompt injection and abuse.** A public text box wired to an agent is an attack surface. The lethal-trifecta logic from [[03-wed-mcp-security|Block 0 Week 2]] applies directly: if your demo agent touches any private data or tool and renders attacker-supplied input, you have built the vulnerability on purpose and put it on your homepage. Demo agents must run isolated: synthetic data, no tools with side effects, no shared context with production.
3. **Cost abuse.** Anonymous inference is a faucet. Rate-limit by IP and session, cap generation length, and put a circuit breaker on daily spend. This is Friday's instrumentation discipline applied defensively.
4. **Signal pollution.** Sandbox traffic contaminates your launch metrics unless events are tagged apart from real usage. Friday covers the taxonomy.

### The decision rule

Run the live sandbox only if all four are true: your agent demonstrates value on *visitor-supplied or visitor-selected* input in under two minutes; its p90 quality on that scoped demo task is boringly good (you know this from evals, not vibes); the demo environment is fully isolated from production data and tools; and you have rate limits plus spend alarms. Fail any one and drop to an interactive tour of real runs. Fail the budget for tour tooling and ship a lightly-edited real-run video with visible timestamps. Every rung is respectable if it is honest; the only wrong choice is faking a higher rung, like a "live" demo that is secretly canned, which buyers eventually discover, and which converts your entire page into a lie retroactively.

A useful middle pattern for agent products: **the curated-input sandbox.** Live agent, real inference, but the visitor picks from six prepared inputs (real tickets, real contracts, whatever your domain is) instead of free-typing. You keep the "this is actually running" proof while bounding the input distribution to the region your evals cover. It also neutralizes most injection and abuse risk in one move. Many operators land here and should.

## Layer 3 — CTA choice for high-consideration products

Agent products are high-consideration almost by definition: they touch customer-facing surfaces, they need integration, and the buyer's trust gap (Monday, Layer 1) demands evidence that takes time to deliver. The CTA must match the consideration level, and the 2026 benchmark data gives the framework real numbers.

**The three candidate CTAs, with the evidence:**

- **Book a demo / book a pilot call.** The default for ACV above roughly $10–15K. Demo-request pages average 1.5–4 percent conversion with top quartiles at 8–15 percent, per Growthspree's 2026 benchmark compilation, with expected rates *falling* as ACV rises (their $75K+ band targets 1.5–3 percent) because qualification is doing more of the work.[^4] For enterprise-sized deals, demo-sourced pipeline closes dramatically better than trial-sourced: one 2026 analysis puts demo-path close rates at 55–75 percent versus 10–15 percent for trials at $50K+ ACV, single-publisher data but directionally consistent with every PLG-vs-sales-led writeup of the period.[^5] For your agent package, "book a demo" has a hidden advantage: the call is where you run Monday's verify-it-yourself eval offer, which is your strongest close.
- **Self-serve trial.** Right when time-to-first-value is genuinely short and the product can be safely used without you. The 2026 conversion benchmarks: opt-in trials (no credit card) convert to paid at a median around 14 percent (range 8–22), while opt-out trials (card required) convert around 44 percent (range 35–55) at the cost of far fewer trial starts.[^6] ChartMogul's long-running conversion report adds the sobering distribution: a fifth of B2B free-trial products convert below 2.5 percent.[^7] For most Week 9 packages (which need onboarding, integration, or data connection) a naked trial is wrong, but a **scoped trial** can work: the curated-input sandbox from Layer 2 extended into "upload 50 of your own tickets, see your resolution report." That is a trial of the *evidence*, not the product, and it fits agent economics.
- **Waitlist.** Correct only when you are genuinely capacity-constrained or genuinely pre-product. As demand *validation*, the waitlist belongs to the pretotyping ladder ([[04-thu-micro-prototype-ladder]], including its ethics discussion); as a *launch* CTA for a product you can actually deliver, a waitlist is friction cosplaying as exclusivity, and sophisticated buyers read it as weakness. If you can serve customers, ask for customers.

**The decision framework, as a two-axis grid.** Axis one: ACV. Axis two: time-to-credible-evidence (how long until the buyer sees proof on their own data). Low ACV + fast evidence → self-serve (scoped trial). High ACV + fast evidence → demo call, with the sandbox doing pre-call warming; this is the sweet spot for most agent packages, because the demo call converts extraordinarily well when the buyer arrives already half-convinced. High ACV + slow evidence → demo call only, and invest in the eval-during-pilot offer. Low ACV + slow evidence → fix your product's evidence economics before launching; that quadrant is where agent products go to churn.

One CTA per page, per the attention-ratio recap. If you must serve two intents (self-serve SMB and sales-led enterprise), the honest pattern is one primary CTA and a quiet text link ("Running support for 50+ agents? Talk to us instead"), not two competing buttons.

## Layer 4 — Objection sections as conversion assets

Monday mapped the objections; today they become sections. The design principle: **each disqualifier objection gets its own scannable block, findable in one scroll, written to be forwarded.** The buyer who has the objection is often not the person who can resolve it; your security block will be pasted into a Slack thread with the security lead. Write for that reader.

- **The security and data block.** One diagram (where data flows, what is stored, for how long), one table (credentials held, scopes, what the agent can and cannot write to), one honest compliance line, one link to a fuller document. Remember the Okta numbers from Monday: 83 percent of leaders name data leakage as a top barrier;[^8] this section is not legal hygiene, it is your second-most-load-bearing conversion asset after the hero.
- **The "when it's wrong" block.** State the failure modes, the escalation path, the SLA for human handoff, and what the buyer sees when it happens. This is the hallucination objection converted into an operations answer. Pattern the diagram after your actual architecture from [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8 Friday]]; if your marketing diagram and your real escalation logic diverge, the sales call will find out.
- **The integration block.** What it connects to, what setup actually takes ("2 hours with your API key, not a quarter"), what you need from them. Under-claimed setup times are a churn factory; state the honest number.
- **The FAQ.** Six to ten real questions from real calls, including at least two uncomfortable ones. An FAQ with no uncomfortable questions is a brochure.

## Layer 5 — Social proof when you have three customers

The temptation at N=3 is to fake density: a "trusted by" wall padded with logos of companies that once replied to an email, review-site badges from incentivized reviews, or vague plural claims ("teams love us"). Beyond being corrosive, some of it is now straightforwardly illegal: the FTC's rule on fake reviews and testimonials (effective October 2024) prohibits fabricated or materially misrepresented testimonials and undisclosed incentivized reviews, with per-violation penalties.[^9] The honest patterns convert better anyway, because at small N the *depth* of proof can be extraordinary:

1. **One quantified case study, told properly.** Named customer, real baseline, real number, real quote from a real human with a title. "Acme Property Group: 61% of maintenance requests resolved without staff touch across 2,300 requests, March–June 2026" outperforms any logo wall you could assemble. If the customer will do a 20-minute joint webinar or a quote with their face on it, that is your launch's centerpiece asset.
2. **Design-partner framing.** "Built with three property-management teams over six months" turns small N into a story about depth and fit. It also implicitly explains why you are not covered in logos, which is the actual anxiety the logo wall was covering.
3. **Aggregate usage numbers.** "3 customers, 11,400 requests processed, 4 months in production" is small and real, and small-and-real is the brand (see Wednesday, where the same logic governs creative). Update the number weekly; a counter that grows is itself proof.
4. **Founder credibility as proof.** At N=3 the buyer is partly buying you. Your public build record from [[03-wed-building-in-public|Block 1 Week 2]] (the eval threads, the honest post-mortems) is a proof asset; link it. This is where the personal-brand investment pays its dividend.
5. **The published eval as proof-of-rigor.** Monday's eval section does double duty here: at small customer counts, methodology is your substitute for volume.

What all five share: they are verifiable, they are specific, and they scale *down* gracefully. Proof strategies that require pretending to be bigger than you are all fail the same way: the sales call reveals the truth, and the deal dies of the gap, not of the smallness. Nobody expects a launch-week product to have 200 logos. They expect it not to lie.

## Worked example — one package, one page, every decision shown

A composite (labeled as such: assembled from real patterns across 2025–2026 agent launches, not one company): **"Dispatch," a maintenance-request agent for mid-size property managers**, packaged in Week 9 at $1,200/month base + $0.40 per resolved request, targeting firms with 500–3,000 units. ACV ≈ $18–25K. Time-to-credible-evidence: fast; the agent can triage a real maintenance email in seconds.

**Grid position:** high-ish ACV, fast evidence → demo call as primary CTA, sandbox as pre-call warmer. The button says "Book a 20-minute pilot scoping call"; the quiet text link below it says "Just exploring? Run it on a sample request first," pointing at the demo block. One primary action, one deliberately subordinate path.

**Demo asset:** curated-input sandbox. Six real (anonymized, design-partner-approved) maintenance emails as selectable inputs: a burst pipe, an ambiguous "something smells weird," a lease question misfiled as maintenance, an angry duplicate, a routine filter swap, a legal-threat edge case. The agent runs live on whichever the visitor picks. Two of the six *deliberately trigger escalation*, and the escalation render is styled as a feature card: "This one goes to a human, in 12 seconds, with this summary attached." The sandbox answers the four criteria: sub-two-minute value (yes, ~20 seconds per run), known p90 on these input classes (the six inputs mirror the golden-set categories from the eval harness), full isolation (static demo tenant, no write tools), rate limits (10 runs/IP/hour, $25/day circuit breaker). Fallback standby: a 90-second real-run video, already rendered, swappable by flipping one flag.

**Section order:** hero (scoped promise: "Every maintenance request answered in 60 seconds. The 1 in 5 that needs a human gets one, with context") → sandbox → eval block (Monday's four-part form: 62% end-to-end resolution on a 500-request golden set, methodology stated, failure classes named) → "when it's wrong" diagram → security/data block (data-flow diagram; the agent holds a scoped mailbox credential and a read-only unit database key; nothing else) → one quantified case study ("Ridgeline PM: 58% of 1,900 requests resolved without staff, April–June") → pricing with worked math at 1,000 requests/month → FAQ with two uncomfortable questions ("What happens if it promises a repair date we can't meet?" answered with the actual guardrail: the agent cannot commit dates, only humans can) → repeat CTA.

**Proof plan:** patterns 1 (Ridgeline case study) and 3 (aggregate counter: "3 firms, 6,100 requests, 14 weeks in production"). No logo wall; the two customers who declined public naming appear nowhere.

Total build spec: one markdown file, 70 lines. That is the artifact your Saturday build consumes, and the level of decision-explicitness the experiment below demands from you.

## Runnable experiment — assemble the skeleton

**Task.** Produce the complete page specification for your Week 9 package, as a markdown document Claude Code will build from on Saturday: (a) section order, each with a one-line content note; (b) demo asset decision via the Layer 2 rule, with your answers to all four sandbox criteria written down, plus the fallback asset; (c) CTA choice via the Layer 3 grid, with your ACV and time-to-credible-evidence estimates stated; (d) the four objection blocks drafted in bullet form; (e) social-proof plan choosing at least two of the five honest patterns, with the specific artifacts named (which customer, which number, which eval).

**Method.** Write the spec yourself; then run two red-team passes with Claude: first as the security lead ("what's missing from the data block?"), then as a conversion reviewer ("count the CTAs and tappable elements; flag attention-ratio violations"). Do not let Claude write the spec; the decisions are the exercise.

**Pass bar.** (1) Exactly one primary CTA, and you can state in one sentence why it matches your grid position. (2) The sandbox decision cites your own eval numbers or explicitly says "no evals yet, so video," which is the honest branch. (3) Every objection block contains at least one sentence a lawyer would wince at (i.e., a real commitment: an SLA, a retention period, a named failure mode). (4) Zero proof elements you could not defend on a sales call. Time budget: 90 minutes.

## Common mistakes experts see

1. **Choosing the demo asset by ambition instead of eval coverage.** The sandbox goes up because it is impressive, not because p90 on the demo task is known-good; the page then performs your variance to strangers.
2. **Two CTAs because "we don't want to lose either segment."** You lose both; the attention-ratio recap exists for a reason.
3. **A "live demo" that is secretly canned.** The single most expensive lie available at this stage. When discovered (and technical buyers probe), it invalidates every other claim on the page.
4. **Security block written by the marketing voice.** "Bank-grade encryption" instead of a data-flow table. The security lead forwarding your page cannot verify vibes.
5. **Waitlist-as-aesthetic.** Gating a product you could deliver, for launch-theater reasons; you pay in lost revenue and read as fragile.
6. **Logo inflation at N=3.** Now an FTC exposure, not just a taste failure.[^9]
7. **Skipping the fallback plan.** The sandbox falls over on launch day (it happens; Friday's instrumentation will tell you) and there is no video to swap in. Always ship the rung below as a standby.

## Reflection questions

1. For your specific package: what is the two-minute visitor-supplied input that would prove value live? If you cannot name one, is that a demo problem or a product-scoping problem?
2. The curated-input sandbox bounds inputs to your eval distribution. A skeptical buyer says "so it only works on the six examples you chose." Write your actual reply. Does it hold?
3. Your grid position says "demo call" but you personally hate sales calls. What breaks first: the CTA, your calendar, or your close rate? What would you have to productize to move one quadrant left?
4. Which single artifact would move you from pattern 2 (design-partner framing) to pattern 1 (quantified named case study)? What would it cost, in weeks and in favors, to get it before launch?
5. An interactive tour shows a curated replay; your Monday copy promises honesty about failure. Should the tour include a failure-and-escalation step? What does showing the escalation *on the happy path* do to trust, and to conversion?
6. If Navattic's Agent Demos pattern matures (an AI walking each visitor through a personalized demo), what happens to the evidential weight of interactive tours? Does personalization increase proof or dilute it?

## My take (reviewer lens)

**Simon Willison** would zero in on Layer 2 and say the lesson still undersells the risk: a public text box in front of an agent is an invitation to every drive-by prompt injector on the internet, and "synthetic data, no tools" is a design constraint that one hurried Saturday integration quietly violates; he would want the sandbox isolation *verified by an adversarial test*, not asserted in a spec document. He is right, and the Saturday checklist includes exactly that probe. **swyx** would push the other direction: the AI-engineering zeitgeist rewards founders who demo live and eat the risk, because "we demo live" is itself a credibility signal the tour-builders cannot buy; he would argue the curated-input compromise, while sensible, sacrifices the exact moment of danger that makes live demos convert. Both are right, which is why the decision rule is written in terms of measured p90 rather than courage. **Chip Huyen** would question the benchmark numbers in Layer 3: single-publisher conversion benchmarks with round-number bands are marketing content, and building a decision framework on them risks false precision. Fair; the framework's axes (ACV, time-to-evidence) are the durable part, and the numbers are labeled directional for exactly this reason. Use the grid, hold the percentages loosely, and replace them with your own funnel data the moment Friday's instrumentation produces any.

## Further reading

**Must-read**

- Navattic, "Interactive Demo Platforms and Best Practices" + the 2026 State of the Interactive Product Demo — the category's mechanics and its own engagement data (vendor-published; read critically).[^3]
- FTC, final rule on fake reviews and testimonials — the legal floor under social proof; short, and every operator should have read it once.[^9]

**Recommended**

- Growthspree's 2026 benchmark pair (demo-request and trial-to-paid) — directional numbers for the CTA grid.[^4][^6]
- Arcade, "Best Interactive Demo Software in 2026" — competitor-written but a fast map of the tooling.[^1]

**Optional**

- ChartMogul SaaS Conversion Report — the free-to-paid distribution that keeps trial expectations honest.[^7]
- GrowLeads, "Why Enterprise SaaS Trials Convert at 10%" — the sales-led counterargument in its strongest form.[^5]

## Citations

[^1]: Arcade. "Best Interactive Demo Software in 2026: 7 Tools Compared." https://www.arcade.software/post/best-interactive-demo-software-2026 — category map; Arcade Growth plan at ~$297.50/mo flat with 5 included seats (moved from $42.50/user/mo) corroborated by Demosmith, "Navattic vs Storylane vs Arcade," https://demosmith.ai/blog/navattic-vs-storylane-vs-arcade (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Storylane. "Storylane vs Navattic: 2026 Feature, Pricing, and AI Comparison." https://www.storylane.io/blog/storylane-vs-navattic — Storylane Free $0 / Starter $40/seat/mo / Growth $500/mo / Premium $1,200/mo; Navattic from ~$500/mo, enterprise HTML capture. Corroborated by Naoma, "Navattic vs Storylane: Which Demo Platform Wins in 2026?" https://www.naoma.ai/articles/navattic-vs-storylane-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). Vendor-written comparisons; pricing cross-checked across both sides' pages.

[^3]: Navattic. "Interactive Demo Platforms and Best Practices for 2026." https://www.navattic.com/blog/interactive-demos — 2026 State of the Interactive Product Demo: 40,000+ demos analyzed, +43% YoY; top-percentile demos ~70% CTR; Agent Demos beta. Corroborated by Naoma (above) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; engagement figures are vendor-published).

[^4]: Growthspree. "B2B SaaS Demo Request Conversion Rate Benchmarks 2026 by ACV and Traffic Source." https://www.growthspreeofficial.com/blogs/b2b-saas-demo-request-conversion-rate-benchmarks-2026 — 1.5–4% average, 8–15% top quartile, ACV-banded targets (search-verified 2026-07-17; single benchmark publisher — treated as directional).

[^5]: GrowLeads. "Why Enterprise SaaS Trials Convert at 10% in 2026 (Demos Close 55–75%)." https://growleads.io/blog/b2b-saas-trials-vs-demo-sales-conversion/ — demo-path 55–75% close vs trial-path 10–15% at $50K+ ACV; churn asymmetry 3.5% vs 7.5% (search-verified 2026-07-17; single-source — flagged, used directionally).

[^6]: Growthspree. "B2B SaaS Trial-to-Paid Conversion Rate Benchmarks 2026." https://www.growthspreeofficial.com/blogs/b2b-saas-trial-to-paid-conversion-rate-benchmarks-2026-by-trial-type-acv-length-credit-card — opt-in median ~14% (8–22%), opt-out median ~44% (35–55%). Directionally corroborated by Userpilot, "SaaS Average Free Trial Conversion Rate," https://userpilot.com/blog/saas-average-conversion-rate/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: ChartMogul. "The SaaS Conversion Report." https://chartmogul.com/reports/saas-conversion-report/ — free-to-paid distribution, including the bottom-quintile-below-2.5% finding (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Okta Newsroom. "Survey: AI agent security is now a priority for enterprise buyers." https://www.okta.com/newsroom/articles/enterprise-buyer-survey-ai-agent-security/ — 83% data leakage / 80% over-privileged access as top barriers (see Monday [^1] for full corroboration).

[^9]: Federal Trade Commission. Rule on the Use of Consumer Reviews and Testimonials (final rule announced August 2024, effective October 2024). https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials — prohibits fake/AI-generated testimonials, materially misrepresented endorsements, and undisclosed incentivized reviews; civil penalties per violation. See also the Rytr action under Operation AI Comply (Monday [^6]).

_last_verified: 2026-07-17_
