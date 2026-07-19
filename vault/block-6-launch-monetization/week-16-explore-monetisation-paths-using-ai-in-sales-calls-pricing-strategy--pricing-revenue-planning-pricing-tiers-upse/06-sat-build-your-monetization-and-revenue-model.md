---
type: lesson
block: block-6-launch-monetization
week: week-16
session_slug: pricing-revenue-planning-pricing-tiers-upsell-hooks
day_of_cycle: 6
day_name: sat
tags: [build, monetization-model, tier-ladder, unit-economics, revenue-model, sales-workflow, code-lab, pass-bar]
sources:
  - bessemer-ai-pricing-playbook-2026
  - flexprice-hybrid-pricing-2026
  - foundrycro-ltv-cac-2026
  - anthropic-pricing-docs-2026
  - refresh-2026-07-master-report
last_verified: 2026-07-17
word_count_target: 4500
---

# BUILD — your monetization model, tier ladder, revenue math, and AI sales workflow

## Why this matters

This is the week's synthesis. By the end you will have four artifacts that turn your launched product into a business: **(1)** a chosen monetization model with a written justification, **(2)** a three-tier ladder with upsell hooks and honest fences, **(3)** a working unit-economics + revenue-projection model that survives a COGS shock, and **(4)** an AI-assisted sales-call prep and follow-up workflow you can run tomorrow. The pass bar is concrete: a *defensible price* and a *model that shows the path to profitability at your real inference cost*. Not a plausible price. A defensible one, meaning you can say it out loud, in one paragraph, with four numbers and zero adjectives.

## Prerequisites and inputs

Pull together the week's outputs — you're assembling, not starting fresh:
- [[01-mon-monetization-models-for-ai-products|Mon]]: your COGS-per-action and chosen model.
- [[02-tue-pricing-strategy-value-metric-anchoring-packaging|Tue]]: value metric, price corridors, discount policy.
- [[03-wed-ai-in-the-sales-motion|Wed]]: the labor-vs-relationship map for your sale.
- [[04-thu-tiers-upsell-hooks-and-expansion-revenue|Thu]]: your tier ladder and expansion map.
- [[05-fri-revenue-planning-and-unit-economics|Fri]]: the five numbers and the diagnosis.
- The code-lab: `code-lab/06-monetization-model/`.

## Build 1 — Choose and justify your monetization model (30 min)

Run [[01-mon-monetization-models-for-ai-products|Monday's]] five-question decision procedure and commit. Write the justification as five sentences, each carrying a number or a named condition:

1. **Model:** "We charge [model] on [value metric]." (e.g., "hybrid: a monthly subscription floor plus a per-niche usage component.")
2. **Why this metric:** it passes the physics test because it's measurable ([X]), buyer-controlled ([Y]), and scales with value at our volume ([Z]).
3. **Why not outcome pricing:** our core outcome fails condition [frequency / definability / attribution / adjudication], so we track it as an accounting metric, not a bill. (Or: it passes all four, so we bill on it.)
4. **The floor:** our subscription floor is $[N], which covers $[M] of fixed COGS and gives the buyer a forecastable base.
5. **The COGS hedge:** under a [2–5×] model-migration shock, this model degrades to [margin]% rather than going negative, because [the floor / the cap / the metered component].

If you can't write sentence 5 with a real number, you haven't tested the shock. Go to Build 3 first, then come back.

## Build 2 — Design the three-tier ladder with upsell hooks (45 min)

Turn [[04-thu-tiers-upsell-hooks-and-expansion-revenue|Thursday's]] ladder into a shippable spec. For each of three tiers, specify:

- **Price** (from Tuesday's corridor) and **included volume** of your value metric.
- **Fences**, the honest, success-correlated differences (volume, capability depth, support, integrations). Each tier must differ from the one below on at least one named fence, or the audit (Build 3) will flag it.
- **The upgrade trigger**. What event in a *succeeding* customer's life moves them up ("fills all included niches," "tries to add a teammate").
- **The upsell hook** — the exact in-product prompt, placed at the moment of realized value, that a helpful human account manager would actually send.

Spacing discipline: aim for ~3–5× steps so tiers read as distinct products (the calculator warns below 2×). Write the three upsell-hook sentences verbatim, these ship into your product, so they must pass the [[02-tue-the-proactive-ambient-pattern|b5w13]] taste test ("would a helpful human say this, now?").

Claude prompt scaffold:
> *Here is my product [one-line value] and my three draft tiers [paste]. For each tier boundary, write: (1) the single success-correlated event that should trigger an upgrade, and (2) a one-sentence in-product upsell prompt placed at the moment of realized value, phrased as a helpful account manager would — not "Upgrade now!" Then flag any tier whose fences look like spite (crippling a basic capability) rather than a fair capability step.*

## Build 3 — Build and stress the unit-economics model (45 min)

This is the load-bearing artifact. Use `code-lab/06-monetization-model/`.

**Step 1, Update the rate card.** Open `rate_card.py`, confirm the rates against the Anthropic pricing page, update the `rate_date`s. This is the habit that keeps the whole model honest — a hard-coded margin is a lie waiting to happen.

**Step 2. Encode your product.** Copy `config_example.py`, replace `HEALTHY_SCENARIO` with your product: real token counts per core action (measured, not guessed), your tiers from Build 2, your customer mix, and your business inputs, CAC **including your own time valued at your rate**, and real churn from [[05-fri-data-and-scale|b5w14]] analytics (or an honest estimate labeled as one).

**Step 3 — Run and read.** `python unit_economics.py`. Read the three outputs:
- **Per-tier margins**. Any tier below the 50% floor is a design finding (raise the price or tighten the fence). The floor is 50%, not the classic-SaaS 80%, because AI-native margins run 50-60% — Niche Radar's three tiers land at 54% / 58% / 60%, healthy for the category.
- **Blended LTV:CAC and payback** — against the ≥3:1 and ≤12-month bars (sanity-check the output against the 2026 segment benchmarks, which put the median LTV:CAC near 3.2:1 and healthy payback under 12 months).[^5]
- **The COGS-shock matrix**, the number that matters most: *which shock breaks a pass bar first, and at what margin.* The bundled Niche Radar example survives all the way to Fable 5 (margin 15%, LTV:CAC 3.1:1) because the hybrid floor holds; your job is to make yours do the same or know exactly where it breaks.

**Step 4. Read the failing case.** Run the bundled `THREE_STRIKES_SCENARIO` and study it: negative margins from an over-provisioned model on a cheap product, a paid-ads CAC that never pays back, a ladder the audit flags three ways. This is the shape of a broken model — learn to recognize it in one glance, because someday it'll be yours and you'll want to see it early.

**Step 5, Project forward (optional, 20 min).** Extend the model into a simple 12-month projection: starting customers, monthly new adds, monthly churn, expansion (Thursday's NRR effect), and fixed costs. Find the customer count where you cross break-even on fixed costs. That number, "we're profitable at N customers," is the single most important sentence in any investor or co-founder conversation.

## Build 4 — Wire the AI sales prep + follow-up workflow (30 min)

From [[03-wed-ai-in-the-sales-motion|Wednesday]], build the two highest-ROI, lowest-risk AI sales artifacts (the *labor* stages, not the relationship stages):

**Artifact A — the account-research + call-prep brief.** A Claude workflow that takes a prospect's domain and LinkedIn URL and returns: grounded account context (from real retrieved sources, not training-data recall), the buyer's likely priority, three tailored talking points, a discovery-question list mapped to your framework, the two most likely objections with your counters, and, critically, **your price sentence, rehearsed** ("The [tier] plan is $[N] a month for [what], which replaces about $[labor line] of [displaced work]").

**Artifact B — the follow-up drafter with a verification gate.** A workflow that drafts the post-call recap and next steps, but lands the draft in *your* outbox for fact-verification (price, dates, commitments, names) before it can reach the buyer. Build the gate structurally, not as a discipline you hope to maintain. The draft must never auto-send ([[03-wed-ai-in-the-sales-motion|Wednesday]] / Boris's lens).

Recording consent belongs in this workflow too: if any part records calls, bake the explicit-consent sentence into your call opener and honor a no ([[04-thu-voice-agent-trust-and-safety|b3w07]]). Note what you're *not* building: an autonomous outbound blaster (deliverability suicide) or a real-time teleprompter (splits your attention on the human). The 2026 field data is unambiguous that the human-in-the-loop split out-performs full autonomy on outbound.[^6] AI on the labor, you on the relationship.

## The pass bar

You pass Saturday when you have:

1. **A defensible price**, the five-sentence model justification (Build 1) with four numbers and zero adjectives, plus a tier ladder (Build 2) whose fences you'd defend to a buyer's face.
2. **A model that shows the path to profitability** — the calculator (Build 3) clears LTV:CAC ≥ 3:1 and payback ≤ 12 months at the **Sept-1 intro-expiry shock** (`sonnet-5-standard`), with no tier going negative under a plausible migration, *or* a written plan for the specific gap. Plus a break-even customer count.
3. **A running AI sales workflow**. Artifact A produces a real prep brief for a real prospect, and Artifact B drafts a follow-up that *cannot* auto-send.

If your model can't clear the shock bar, that's not a failure of the exercise, it's the exercise working. It means your price, your COGS, or your acquisition model needs to change *before* you scale, which is exactly what you wanted to learn this week rather than in production six months from now.

## Worked example — Niche Radar, assembled

Running all four builds on the week's example:

1. **Model:** hybrid. $39 base (2 niches) + $15/niche beyond, capped per tier with 80% alerts. Outcome ("competitive moves acted on") tracked, not billed. Free tier usage-capped (1 niche, weekly) to bound free COGS to ~$2/user.
2. **Ladder:** Starter $39 / Pro $199 / Team $599, ~5× then ~3×, each fenced on niches + capability + support, each with a success-correlated upgrade trigger and a verbatim hook.
3. **Model output:** blended ARPA $179, blended margin 58.1% at Sonnet-5-intro (per-tier 54% / 58% / 60%, all inside the AI-native band), LTV $2,602, LTV:CAC 11.8:1, payback 2.1 months — *under-monetized*, room to raise price and invest in acquisition. Survives to Fable 5 (15% margin, 3.1:1). Diagnosis: raise price, spend on growth.
4. **Sales workflow:** Claude prep brief + verified follow-up drafter, consent baked into the opener.

The read-out: this is a healthy, under-priced, under-marketed business, the model told us the lever (price + acquisition), not just the numbers. That diagnosis, produced in an afternoon, is the entire point of the week.

## Common mistakes experts see

- **A price with adjectives instead of numbers.** "Premium value at an accessible price point" is not a defensible price. Four numbers, zero adjectives, or it isn't done.
- **Skipping the rate-card update.** Running the calculator on stale rates and trusting the margin. Update `rate_date`s first, every time.
- **CAC without your own time.** Founder-sold customers look free; your LTV:CAC is fiction until you value your hours in CAC.
- **Guessing token counts.** The whole COGS line rests on real per-action token measurements. Measure them; don't estimate.
- **Building the outbound blaster or the teleprompter.** The two AI sales artifacts you should *not* build. Prep and verified follow-up are the labor-stage wins; automation of the relationship stages is the trap.
- **A follow-up drafter that can auto-send.** Convenience without a verification gate will eventually send a wrong price to a buyer. Make the gate structural.
- **Passing the baseline but not the shock.** A model that only works at today's intro price is a bet, not a business. Clear the Sept-1 shock or write the plan for the gap.

## Reflection questions

- Say your price out loud right now. Did you flinch? If yes, is the price wrong or is the muscle untrained, and which does Build 1's justification fix?
- At what customer count are you profitable on fixed costs? If you don't know, you can't answer the most basic question anyone will ask about your business.
- Which shock breaks your model first, and what would you actually *do* the day it lands? Is that a plan or a hope?
- Your calculator says raise price / cut cost / improve retention. Which one did it actually say, and which one were you *hoping* it would say? What does that gap tell you?
- Which AI sales artifact would save you the most time this week, and why haven't you built it yet?

## My take (reviewer lens)

**Michael Seibel** would judge this whole day by one output: "Did you put a real price in front of a real buyer, or did you spend Saturday making a beautiful spreadsheet? The model is worth exactly nothing until a human with a credit card reacts to your number. Build the calculator in an hour, then go get a reaction." He's right that the calculator is a means, not the end — its purpose is to stop you shipping a structure that's expensive to unwind, then get out of the way so you can run the real experiment on real buyers. **Boris Cherny** would inspect the two things most likely to rot: the rate card (which silently lies as prices move, hence the update-first ritual and the date stamps) and the follow-up gate (which the convenience pressure will erode. Hence "structural, not disciplinary"). Both are built to fail loudly rather than quietly, which is the only kind of tool worth shipping. **Chip Huyen** would remind you that every number in the model downstream of the token counts is only as good as the measurement of those token counts — so the least glamorous step (actually measuring input/output tokens on your real prompts) is the one that makes the other 200 lines of arithmetic mean anything. All three converge on the same discipline: the model exists to produce a *decision* and to make it cheap to be wrong, and the decision is only real once a buyer has reacted to the price it defends.

## Further reading

**Must-read**
- The code-lab README (`code-lab/06-monetization-model/README.md`), how the calculator, the shock matrix, and the audit fit together.
- [[05-fri-revenue-planning-and-unit-economics|Friday]] — the five numbers and the diagnosis the calculator mechanizes.

**Recommended**
- Bessemer, *The AI Pricing and Monetization Playbook*. The margin thesis behind the whole model.[^1]
- Flexprice, *Hybrid Pricing Guide (2026)*, the floor-plus-variable structures Build 1 chooses among.[^2]

**Optional**
- Foundry CRO, *LTV:CAC Ratio Benchmarks 2026* — sanity-check your model's output against the segment bands.[^3]
- [[05-fri-pricing-the-package|b4w09 Friday]]. The services-package version of the same stress discipline.

## Citations

[^1]: Bessemer Venture Partners, *The AI Pricing and Monetization Playbook* (2026): AI margins 50–60%, consumption-vs-seat, the renewal cliff. https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook (search-verified 2026-07-17; fetch egress-blocked, liveness pass pending)

[^2]: Flexprice, *Hybrid Pricing: The Complete Guide for SaaS and AI Companies (2026)*: floor-plus-variable structures and hybrid dominance data. https://flexprice.io/blog/hybrid-pricing-guide (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Foundry CRO, *LTV:CAC Ratio Benchmarks 2026*: segment bands to sanity-check the calculator output. https://foundrycro.com/blog/ltv-cac-ratio-benchmarks-2026/ (search-verified 2026-07-17; fetch egress-blocked. Liveness pass pending)

[^4]: Anthropic, *Pricing*, Claude Platform Docs: the rate card the calculator ships with (Sonnet 5 intro/standard, Opus 4.8, Fable 5, Haiku 4.5), verified against this vault's July-2026 master refresh. https://platform.claude.com/docs/en/about-claude/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Foundry CRO, *LTV:CAC Ratio Benchmarks 2026* and *CAC Payback Benchmarks 2026*: median LTV:CAC ~3.2:1, healthy payback ≤12 months — the sanity-check bands for the calculator's output. https://foundrycro.com/blog/ltv-cac-ratio-benchmarks-2026/ ; https://foundrycro.com/blog/cac-payback-benchmarks-2026/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Ziellab, *AI SDR reality check: what works after the hype* (2026): the human-in-the-loop pod (one human SDR + two AI seats) books ~1.9× more meetings per dollar than full autonomy; the labor-vs-relationship split. https://ziellab.com/post/ai-sdr-what-works-after-the-hype-2026-guide (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
