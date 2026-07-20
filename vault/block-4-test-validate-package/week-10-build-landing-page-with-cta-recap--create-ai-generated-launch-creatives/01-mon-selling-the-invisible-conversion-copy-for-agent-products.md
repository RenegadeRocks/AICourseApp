---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 1
day_name: mon
session_slug: build-landing-page-with-cta-recap
date_due: 2026-07-20
tags: [agent-products, conversion-copy, trust-gap, proof-hierarchy, eval-as-marketing, outcome-based-pricing, per-resolution-pricing, ftc-substantiation, security-objections, hallucination-objection]
sources:
  - okta-enterprise-buyer-ai-agent-security-survey
  - infuse-voice-of-the-buyer-2026
  - trustradius-2026-buying-disconnect
  - fin-ai-pricing-benchmarks
  - zendesk-outcome-based-pricing
  - deloitte-dart-outcome-pricing-agentic-2026-06
  - clonedesk-fin-limitations
  - ftc-operation-ai-comply-2024
  - benesch-operation-ai-comply-one-year
  - drata-trust-center
  - vanta-trust-center-landscape
  - growthspree-demo-benchmarks-2026
last_verified: 2026-07-17
word_count_target: 5200
---

# Selling the invisible — conversion copy for agent products, or how to make a probabilistic system feel safe to buy

## Why this matters

This week ends with your Week 9 package behind a live landing page. Today decides what that page *says*, and the stakes are specific: you are not selling software that does the same thing every time. You are selling a system that is right most of the time, wrong occasionally, and expensive to embarrass yourself with. Your buyer knows this. By mid-2026 the median B2B buyer has personally caught an AI tool being confidently wrong, has read a security post-mortem about an over-permissioned agent, and has sat through a vendor demo that they correctly suspected was the best run out of forty. Copy that worked for deterministic SaaS ("Automate your support. Save 40%.") now reads as either naive or dishonest, and both readings kill conversion.

The skill you install today is writing conversion copy whose every claim survives the question "prove it." That is not a compliance chore; it is the positioning. In a market drowning in AI claims, **substantiation is differentiation**. The operator who can put a scoped, measured, honestly-caveated promise on a page will beat the one with the better adjectives, because the buyer's default state is disbelief. You will leave today with a rewritten hero, a proof stack ordered by evidential weight, a pricing-page pattern chosen from the 2026 menu, and an objection map that Tuesday assembles into a full page.

One boundary, stated up front: the mechanics of landing pages (anatomy, benchmark conversion rates, attention ratio, reading level, sample-size math) are canonical in [[01-mon-landing-page-as-conversion-machine|Block 2 Week 3 Monday]] and are not re-taught here. Tuesday carries a one-table recap. Today is entirely about what changes when the product is an agent.

## Prerequisites

- Your Week 9 package definition: scope, deliverable, price, target buyer, from [[06-sat-build-your-first-sellable-agent-package|Week 9's package build]]; a Block 2–3 build with an invented price works as a stand-in.
- The eval discipline from [[06-sat-rag-evaluation|Block 2 Week 4 Saturday]]: you know what a golden set is and have run one. Today weaponizes it as marketing.
- Working recall of Shapiro's hero test and the "Desire − (Labor + Confusion)" frame from Block 2 Week 3. One line of recap: a landing page is a function from visitors to actions, and copy is its highest-leverage input.

## Layer 1 — The trust gap: why agent landing pages fail differently

Standard SaaS conversion theory assumes the buyer's core doubts are *value* doubts: is this worth the money, will my team use it, is switching painful. Agent products add a second stack of doubts that sit **above** the value doubts, because they are disqualifiers rather than negotiables. Survey evidence through 2025–2026 is unusually consistent about what they are.

Okta's 2026 enterprise-buyer research found that 69 percent of organizations report security concerns actively slowing their adoption of AI agents, with data leakage (cited by 83 percent of leaders) and over-privileged access (80 percent) as the top two named barriers.[^1] INFUSE's *Voice of the Buyer 2026* names the overall condition directly: a "Trust Gap" in which buyers have more vendor information than ever and less confidence in their decisions than ever, with 94 percent of AI-using buyers saying they fact-check AI outputs at least some of the time.[^2] TrustRadius's 2026 B2B Buying Disconnect reaches the same shape from the other side: AI has changed how buyers *research* (they increasingly ask assistants instead of reading vendor sites) but not what they *trust*, which remains peer evidence and verifiable claims over vendor marketing.[^3]

Translate that into page terms and you get the three objections that must be answered above the fold or in the first scroll, in the buyer's own voice:

1. **"Will it hallucinate in front of my customers?"** The accuracy objection. Not "is it good" but "what happens on the bad day." A page that never mentions failure modes is answering this question with silence, and silence reads as "yes, and we'd rather not discuss it."
2. **"What happens to my data?"** The security objection. For an agent this is sharper than for SaaS because agents *act*: they hold credentials, call tools, and write to systems. Your buyer's security team has read the same over-privileged-access statistics you just did.
3. **"How much babysitting does it need?"** The reliability objection, inherited from every pilot that died in production. The honest answer involves escalation paths and human review gates, which is why hiding them is a mistake (Layer 3).

The failure mode of most agent landing pages in 2026 is that they are written as if the buyer's doubt were value doubt. They lead with outcomes ("10x your pipeline") when the buyer is still stuck on disqualifiers. Conversion copy for agents therefore inverts the classic order: **establish "this won't hurt me" before "this will help me."** The trust gap is the bottleneck; desire without trust converts to nothing.

> My take: the trust gap is an asymmetric opportunity for small operators. Big vendors have marketing teams that legally cannot say "here is where our agent fails." You can. A solo operator publishing honest failure modes reads as more credible than a unicorn's compliance-approved vagueness, and credibility is the scarce good.

## Layer 2 — The proof hierarchy for probabilistic software

All proof is not equal, and for agent products the ordering is different from classic SaaS. Ranked from strongest to weakest by how directly the buyer can verify the claim themselves:

1. **Live product contact.** The buyer runs your agent on their input, now, without talking to you. Highest evidential weight because it is not mediated by you at all. Also the highest-risk asset on the page; Tuesday covers when a live sandbox is wise and when it is self-sabotage.
2. **Interactive demo / guided tour.** The buyer walks a real recorded flow at their own pace. Verifiable that the product exists and works on the happy path; not verifiable that the happy path is typical.
3. **Product video with real runs.** Weaker than interactive (passive, editable) but still shows the actual artifact. The 2026 norm-shift: buyers assume edited demos hide retries, so unedited or lightly-edited runs with visible timestamps carry more weight than cinematic cuts.
4. **Published eval numbers with methodology.** Your golden-set results, stated with scope: task distribution, sample size, pass criteria, failure examples. This is the eval-report-as-marketing move (Layer 3). For technical buyers it can outrank video.
5. **Quantified named case study.** "Acme cut first-response time from 4.1h to 22min over 6,400 tickets in Q2" with a named, quotable human. One of these beats ten logos.
6. **Logo walls and testimonials.** Legitimacy proof only. Answers "is this real," never "will it work for me."
7. **Adjectives and category claims.** "Enterprise-grade," "cutting-edge," "powered by advanced AI." Zero evidential weight in 2026; often negative, since buyers pattern-match unsubstantiated superlatives to the vendors that burned them.

Two operational rules fall out of this hierarchy. First, **spend your page's scarce attention on the highest rung you can afford to show.** If your agent can demonstrate value on visitor-supplied input in under two minutes, a live surface embarrasses every competitor's video. If it cannot, an honest eval section beats a faked interactivity. Second, **each proof asset should be scoped to the objection it answers.** Eval numbers answer the hallucination objection. A security/trust page answers the data objection. An escalation diagram answers the babysitting objection. A logo wall answers none of them, which is why pages built around logo walls under-convert for agents even when they worked fine for SaaS.

### The scoped-claim pattern

The sentence-level move that separates credible agent copy from slop is **scoping**. Compare:

- Unscoped: "Our AI answers your customers' questions accurately."
- Scoped: "Resolves order-status, returns, and warranty questions end-to-end. Everything else gets routed to your team with full context, in under 30 seconds."

The scoped version does three jobs at once: it makes a falsifiable promise (falsifiable promises read as confident), it pre-answers the failure-mode question (escalation is in the sentence), and it qualifies the buyer (if your ticket mix is 80 percent edge cases, we are not for you, and both of us just saved a sales call). Scoping shrinks the promise and grows the belief. Small-believed beats large-doubted at every price point.

## Layer 3 — The eval report as marketing

Here is the move most of your competitors will not make, and the reason this course made you build eval harnesses in [[06-sat-rag-evaluation|Block 2 Week 4]] before it let you sell anything: **publish your evals.**

The pattern already exists at the top of the market. Intercom's Fin, one of the most widely deployed support agents, runs a public benchmarks surface and reports aggregate resolution performance across its customer base, alongside per-customer reporting products (Monitors, custom scorecards) that let buyers verify performance on their own traffic.[^4] Whatever you think of the numbers, notice the *shape*: the marketing asset is a measurement artifact. The pricing page and the eval report have fused.

Notice also the failure mode, because it is instructive. Intercom's marketing cites resolution rates in the 65–76 percent range across its fleet; one independent 2026 teardown argues that production deployments in complex B2B settings land materially lower, at 45–53 percent, because vendor-reported cohorts skew toward high-volume, low-variance B2C ticket mixes.[^5] The critique may or may not be fair in magnitude. The lesson for you is precise either way: **the moment you publish numbers, the gap between your benchmark distribution and the buyer's real distribution becomes your credibility exposure.** The defense is not to hide the numbers; it is to publish the methodology with them. State the task mix. State what counts as success. Show failure examples. A published 71 percent with visible methodology and a "where we fail" section out-converts a published 92 percent with neither, because the buyer's prior is that unexplained numbers are cherry-picked.

There is also a legal floor under this, not just a taste argument. The FTC's Operation AI Comply, launched September 2024 and continued under the current administration, has brought more than a dozen actions against companies whose AI capability claims lacked substantiation, from DoNotPay's "robot lawyer" (which the FTC alleged was never tested against human-lawyer performance) to Rytr's fake-review generation.[^6] The agency's standard is the one you should write to anyway: claims about AI capabilities must be backed by competent and reliable evidence at the time you make them.[^7] "Our agent resolves 70 percent of tickets" on your landing page is an advertising claim. Your eval harness is your substantiation file. This is the cleanest possible alignment of good engineering, good marketing, and staying out of trouble: the same golden set serves all three.

Practical form for a solo operator's eval section, in one scroll block:

- **The claim, scoped.** "Resolves 68% of order-support tickets end-to-end without human touch."
- **The basis.** "Measured on a 400-ticket golden set drawn from three design partners' real traffic, March–June 2026. 'Resolved' = customer confirmed or no reopen within 72h."
- **The failure honesty.** "Where it fails: multi-order disputes, refunds above policy thresholds, angry-customer de-escalation. These route to your team automatically."
- **The verify-it-yourself.** "We run the same eval on your historical tickets during the pilot. You see your number before you pay full price."

That last bullet is the conversion weapon. It converts the eval from *our* evidence into *their* evidence, and it makes the pilot (which you were going to offer anyway, per your Week 9 package design) feel like science instead of sales.

## Layer 4 — Pricing pages for agents, July 2026

Your pricing page is copy too, and for agent products it carries an argument no SaaS pricing page had to make: *how the price relates to the risk*. The 2026 menu, verified against live vendors:

**Per-resolution / outcome-based.** Intercom's Fin charges $0.99 per resolved conversation; unresolved interactions are free.[^4][^8] Zendesk launched outcome-based agent pricing around $1.50 per automated resolution on committed volume and roughly $2.00 pay-as-you-go.[^8] Sierra built its positioning on outcome-based pricing without publishing rates.[^8] This model's marketing power is that the *pricing is the objection handler*: "what if it fails?" is answered with "then you don't pay." It is now mainstream enough that Deloitte published formal revenue-recognition guidance for outcome-based agentic-software pricing in June 2026, which tells you the model has crossed from experiment to expected pattern.[^9] Its costs: you inherit the burden of defining "resolution" contractually (expect disputes at the boundary), your revenue inherits your accuracy variance, and you need measurement infrastructure the buyer trusts, which loops back to Layer 3.

**Per-seat.** Still common, increasingly awkward for agents because agents replace seat-work; charging per human seat for a product whose pitch is "fewer humans needed" prices against your own value story. Useful mainly when the agent is a copilot amplifying named users.

**Usage/credits.** Simple to meter, hard to buy: buyers cannot forecast usage before adopting, so the pricing page must carry a calculator or worked scenarios or it becomes a bounce point.

**Flat platform fee + outcome kicker.** The hybrid pattern increasingly common for smaller vendors: a base fee that covers integration and floor costs, plus an outcome-metered component. For a solo operator selling a packaged agent, this is usually the right default. The base fee keeps you solvent through ramp-up; the outcome component makes the page's promise credible.

Two page-level rules regardless of model. First, **show the math on a worked example**: "1,000 tickets/month at your current mix ≈ $640/month, versus $2,900/month of agent time at your team's loaded cost." Buyers of agent products are almost always building an internal cost case; a pricing page that builds it for them gets forwarded to the CFO, and *forwardable* is what a high-consideration pricing page is for. Second, **price transparency is a trust signal in this category specifically.** "Contact us" pricing on an agent product stacks a second opacity on top of an already-opaque product. If you cannot publish exact numbers, publish the model and a realistic range. (Where the *services* version of your offer needs bespoke pricing, that is your [[05-fri-commercial-sow-for-ai-projects|Block 1 SOW discipline]]; the packaged product should aspire to a printed price.)

## Layer 5 — Assembling the argument: a hero-and-proof template for agent products

Pulling the layers together into a copy skeleton you will fill for your own package today and wire into a page tomorrow:

1. **Hero header: the scoped promise.** One sentence a buyer could repeat to their boss. Pattern: *[Outcome] on [scoped domain], [honesty clause]*. Example: "Answers your tenants' maintenance requests end to end. Escalates the 1 in 5 it shouldn't touch."
2. **Hero subheader: the mechanism plus the guarantee-shaped element.** "Trained on your playbook, measured on your tickets during a two-week pilot. You see the resolution number before you pay full price."
3. **First proof block: your highest affordable rung.** Live surface, interactive tour, or real-run video, per Layer 2.
4. **The eval section.** Claim, basis, failure honesty, verify-it-yourself, per Layer 3.
5. **The security block.** One scroll: data flow diagram, what is stored where, credential scoping, sub-processor list, compliance status stated honestly ("SOC 2 Type II in progress, report available under NDA" is fine; pretending is not). Trust-center tooling has made this table-stakes at the enterprise tier: Vanta alone reports 16,000+ customers and vendors ship public trust pages precisely because security review otherwise adds weeks of sales drag.[^10] At your scale, one honest page does the same job.
6. **The escalation diagram.** Where humans enter, how fast, with what context. This section converts the babysitting objection into a feature: "your team only sees the 20 percent that deserves them."
7. **Pricing with worked math.** Layer 4.
8. **CTA calibrated to consideration level.** Tomorrow's whole topic; today just note that agent products are high-consideration and the CTA must match.[^11]

What is deliberately absent: category self-praise, "AI-powered" as a feature (in 2026 it is a disclosure, not a differentiator), and any claim you could not defend from your eval file in an FTC inquiry or, more realistically, in a prospect's technical deep-dive call.

## Runnable experiment — rewrite your package's hero and proof stack

**Task.** Take your Week 9 package (or stand-in). Produce: (a) hero header + subheader in the scoped-promise pattern; (b) an objection map listing the top five objections *in the buyer's voice*, each paired with the proof asset that answers it and the asset's rung on the Layer 2 hierarchy; (c) a drafted eval section using the four-part form, with real numbers from your Block 2–3 eval runs, or the harness plan to get them this week; (d) a chosen pricing model with one worked example.

**Method.** Draft by hand first (20 minutes), then use Claude to red-team, not to write: paste your draft with the prompt "You are a skeptical VP of Support who has been burned by two AI vendors. List every claim on this page you don't believe and what evidence would change your mind." Revise. Iterate until the red-team pass produces no claim you cannot substantiate.

**Pass bar.** (1) The hero passes the one-read test: a stranger reading only the header knows what you sell and for whom. (2) Every quantitative claim on the page has a written substantiation note pointing at an artifact that exists (eval run, customer data, invoice). (3) At least one section explicitly names a failure mode. (4) The red-team prompt, run cold on the final draft, surfaces zero claims you cannot back. If you cannot hit (2), the finding is not "write vaguer copy," it is "run the eval first"; that is the correct order and the whole point of Block 4.

## Common mistakes experts see

1. **Leading with outcomes while the buyer is stuck on disqualifiers.** Trust before desire; the trust gap is the bottleneck, not the value story.
2. **Hiding the human in the loop.** Operators bury escalation paths thinking they weaken the automation pitch. Buyers in 2026 read "no humans anywhere" as either a lie or a liability.
3. **Publishing a number without a methodology.** An unexplained "94% accurate" is read as cherry-picked and invites the Fin-style teardown gap between your benchmark and their production reality.[^5]
4. **"Contact us" pricing on a product whose core objection is opacity.** Two black boxes stacked. Publish the model even if you cannot publish the number.
5. **Borrowing deterministic-SaaS guarantee language.** "99.9% uptime" is a promise you can keep; "99.9% accuracy" is a promise your own eval file contradicts. Never let template copy smuggle in determinism.
6. **Treating the FTC substantiation standard as a big-company problem.** Operation AI Comply's defendants included small operators; earnings-type claims ("save $40K/year") need the same evidence file as capability claims.[^6]
7. **Answering the security objection with a badge instead of an explanation.** A SOC 2 logo without a data-flow story fails the technical buyer who actually decides; the badge answers legitimacy, not "what do you do with my data."

## Reflection questions

1. Your agent's honest end-to-end resolution rate is 55 percent. Write the hero that makes 55 percent a selling point rather than a confession. What buyer is that hero *for*?
2. The verify-it-yourself pilot ("see your number before you pay") transfers eval cost to pre-sale. At what deal size does that stop being affordable for you, and what is the cheaper proof rung you would substitute below it?
3. Outcome-based pricing makes your revenue inherit your accuracy variance. Sketch the month your accuracy drops 15 points because a customer's upstream data changed. Which pricing model would you rather be on, and what does that imply about what you should sell *this quarter*?
4. Which of your current claims would survive an FTC-style "show me the competent and reliable evidence" request today? Which would survive it after one week of eval work? The delta is your real to-do list.
5. If a buyer's AI assistant, not the buyer, is the first "reader" of your landing page (the TrustRadius research direction), what changes about how you structure claims and evidence on the page?[^3]
6. Where is the line between an honest failure-modes section and self-sabotage? Write the failure sentence you are *not* willing to put on the page, and articulate why not. Is the reason evidence, or fear?

## My take (reviewer lens)

**Seibel** would push on sequencing: this lesson risks making you spend a week polishing copy for a product with three users. His version: put up the ugly page with an honest paragraph and a Calendly link today, and let the first ten sales calls write the copy for you; the objection map in the experiment is the part he would keep, because it is really a discovery-call script. Fair, and the synthesis is that the experiment's pass bar deliberately requires artifacts, not polish. **Hamel Husain** would sharpen Layer 3's knife: "publish your evals" is empty advice if the eval is weak, and a public golden set of 40 hand-picked examples is marketing slop wearing a lab coat; he would demand the published methodology include task-distribution provenance and would note that "verify on your data during the pilot" is the only eval claim that fully closes the gap. **A cohort peer** would raise the awkward one: this lesson assumes you have eval numbers worth publishing, and many Week 9 packages will not yet. The honest fallback is the one in the pass bar: scope the claims down to what you can substantiate, even if that makes the page quieter than the competition. Quiet and true compounds; loud and fragile gets one launch.

## Further reading

**Must-read**

- FTC, "Operation AI Comply" announcement and case list — the substantiation standard, with named defendants; read it as a copywriting checklist in the negative.[^6]
- Intercom Fin's public pricing and benchmarks surfaces — the fused eval/marketing artifact, live; study the shape, then read the CloneDesk critique for the gap risk.[^4][^5]

**Recommended**

- INFUSE, *Voice of the Buyer 2026* — the trust-gap framing from the buyer's side.[^2]
- Deloitte DART, "Accounting for Outcome-Based Pricing in an Agentic AI Software Product" (June 2026) — dry, but the strongest available evidence that outcome pricing is now standard enough to have accounting doctrine.[^9]

**Optional**

- TrustRadius 2026 B2B Buying Disconnect — how AI-mediated research changes page reading order.[^3]
- Drata / Vanta trust-center materials — vendor-written, but the sales-friction framing is useful for your one-page security story.[^10]

## Citations

[^1]: Okta Newsroom. "Survey: AI agent security is now a priority for enterprise buyers." https://www.okta.com/newsroom/articles/enterprise-buyer-survey-ai-agent-security/ — 69% report security concerns slowing AI-agent adoption; 83% cite data leakage and 80% over-privileged access as top barriers. Corroborated by Gravitee, "State of AI Agent Security Report," https://www.gravitee.io/state-of-ai-agent-security and AvePoint, "State of AI 2026," https://www.avepoint.com/blog/manage/state-of-ai-2026-report (74% inaccuracy / 72% cybersecurity as highly relevant risks) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: INFUSE. "Voice of the Buyer: AI Reality Check 2026." https://infuse.com/insight/voice-of-the-buyer-ai-research-reality-check-from-hype-to-proof/ — the "Trust Gap" as the defining condition of 2026 B2B buying; 94% of AI-using buyers fact-check AI responses at least some of the time (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: TrustRadius. "2026 B2B Buying Disconnect Report" via PR Newswire, https://www.prnewswire.com/news-releases/trustradius-2026-b2b-buying-disconnect-report-reveals-ai-has-changed-how-buyers-research-but-not-what-they-trust-302825792.html — AI changed how buyers research, not what they trust (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Intercom / Fin. Pricing and benchmarks surfaces: https://fin.ai/ and https://fin.ai/benchmarks ; per-resolution pricing $0.99/resolved conversation corroborated by Pickaxe, "AI Agent Pricing Models Explained (2026)," https://pickaxe.co/post/ai-agent-pricing-models and Quickchat, "AI Agent Pricing Models 2026," https://quickchat.ai/post/ai-agent-pricing-models ; per-customer verification products (Monitors, custom scorecards) per Intercom blog "Announcing Monitors," https://www.intercom.com/blog/announcing-monitors-opening-the-ai-black-box/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). Fleet-level resolution figures are vendor-reported; treat accordingly. Billing nuance, corroborated across independent pricing teardowns (Gleap, Macha, Aimdoc, search-verified 2026-07-17): the $0.99 unit is a qualifying *outcome* (confirmed or assumed resolution, procedure handoff, disqualification), with a monthly outcome minimum on the standalone plan — "unresolved is free" is the marketing framing, not the billing fine print.

[^5]: CloneDesk. "Intercom Fin Resolution Rate: 45–53% in Production — 3 Limitations Behind the Gap." https://clonedesk.ai/blog/intercom-fin-limitations — single-source competitive analysis arguing vendor-marketed 76% draws on favorable cohorts while B2B SaaS production lands 45–53%. Cited here as a named critique illustrating benchmark-vs-production gap risk, not as an audited number (search-verified 2026-07-17; single-source — flagged).

[^6]: Federal Trade Commission. "FTC Announces Crackdown on Deceptive AI Claims and Schemes." September 25, 2024. https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes — Operation AI Comply launch; DoNotPay and Rytr actions. Case-detail corroboration: Mintz, "FTC Launches Operation AI Comply," https://www.mintz.com/insights-center/viewpoints/54731/2024-10-03-ftc-launches-operation-ai-comply-five-enforcement .

[^7]: Benesch. "One Year In, FTC's 'Operation AI Comply' Continues Under New Administration." https://www.beneschlaw.com/insight/one-year-in-ftcs-operation-ai-comply-continues-under-new-administration-signaling-enduring-enforcement-focus/ — more than a dozen Section 5 actions; substantiation-by-competent-and-reliable-evidence standard; enforcement continuing through the current administration (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Outcome-based pricing landscape: Zendesk ~$1.50/automated resolution committed, ~$2.00 pay-as-you-go, and Sierra's unpublished per-outcome model per The Pricing Conundrum, "Outcome-based Pricing in Practice," https://thepricingconundrum.substack.com/p/outcome-based-pricing-in-practice corroborated by Quickchat (above) and Solvimon, "What is AI Agent Pricing?" https://www.solvimon.com/glossary/ai-agent-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Deloitte DART. "Technology Spotlight — Accounting for Outcome-Based Pricing in an Agentic AI Software Product." June 4, 2026. https://dart.deloitte.com/USDART/home/publications/deloitte/industry/technology/accounting-outcome-based-pricing-agentic-ai (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: Trust-center category and sales-friction claims: Drata, "What Is a Trust Center," https://drata.com/learn/assurance/what-is-a-trust-center (vendor-claimed: manual security review historically adds weeks of deal drag; SafeBase acquired by Drata) and Vanta, "4 best Trust Center products for 2026," https://www.vanta.com/resources/best-trust-center-software ; Vanta scale (~$300M ARR, 16,000+ customers, April 2026) per ClawNewbie comparison https://clawnewbie.com/compare/vanta-vs-drata-2026 and SOC2Auditors review https://soc2auditors.org/insights/vanta-review/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; ARR figure is press-derived, not audited).

[^11]: Growthspree. "B2B SaaS Demo Request Conversion Rate Benchmarks 2026." https://www.growthspreeofficial.com/blogs/b2b-saas-demo-request-conversion-rate-benchmarks-2026 — demo-request pages average 1.5–4%, top quartile 8–15%, with ACV-banded targets. Single benchmark publisher; used directionally in Tuesday's CTA framework (search-verified 2026-07-17; single-source — flagged, treated as directional).

_last_verified: 2026-07-17_
