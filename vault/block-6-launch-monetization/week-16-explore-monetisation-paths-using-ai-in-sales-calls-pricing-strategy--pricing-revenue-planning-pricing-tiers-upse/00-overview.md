---
type: week-overview
block: block-6-launch-monetization
week: week-16
title: 'Week 16, Monetization paths, AI in sales calls, pricing tiers & revenue planning'
live_sessions:
  - '2026-09-05 — Explore monetisation paths: Using AI in Sales Calls & Pricing Strategy'
  - '2026-09-06. Pricing & Revenue Planning: Pricing tiers & upsell hooks'
study_window: 2026-08-31 to 2026-09-06
last_verified: 2026-07-17
---

# Week 16 — Turning a launched product into durable revenue

## The thesis of this week

Last week you launched. People are arriving. This week decides whether their arrival compounds into a business or evaporates into a graph that spikes and dies. The launch is an event; monetization is a machine, and the machine has four moving parts: the **model** by which you charge, the **price** you attach to it, the **motion** by which you sell (increasingly AI-assisted), and the **revenue architecture**, tiers, upsell hooks, expansion — that turns one customer into a growing account. Get the machine right and every future launch pours into a structure that keeps money. Get it wrong and you spend Block 7 papering over a monetization model that was mispriced at birth.

The hard constraint that makes 2026 different from every prior SaaS era: **your cost of goods sold moves.** A traditional SaaS company shipped bits at ~85% gross margin and never thought about COGS again. You run inference on every action, your token bill is a real line item, your model's price changed twice this quarter, and the tokenizer under it inflated by ~30%. Bessemer's own 2026 data puts AI-native gross margins at 50–60%, not 80–90%.[^1] Every pricing decision this week is grounded in that reality. We do the margin math with the actual July-2026 rate card, so the numbers you leave with are real, not aspirational.

## What this week is NOT re-teaching

[[05-fri-pricing-the-package|Week 9 (b4w09)]] already taught value-metric selection, the labor-line anchor, the usage-based backlash, and the outcome-pricing controversy for a *services package*. This week is the product-company version and goes deeper on **monetization-model selection, AI-assisted selling, and revenue architecture** — it wikilinks the fundamentals rather than repeating them. [[02-tue-agent-architectures|Week 4 (b2w04)]] built the sales-agent *technology*; here we take the *seller's* angle. [[04-thu-voice-agent-trust-and-safety|Week 7 (b3w07)]] is the canonical home for call-recording consent law. [[05-fri-data-and-scale|Week 14 (b5w14)]] owns retention metrics; we build the expansion layer on top of it.

## Shape of the week

| Day | Topic | Output |
|-----|-------|--------|
| Mon | Monetization models for AI products in 2026: the full menu, how token COGS reshapes viability, the usage-vs-subscription debate resolved | A chosen model with margin math |
| Tue | Pricing strategy: value metric, anchoring, good-better-best, price testing with tiny N, discounting discipline | Draft price points + test plan |
| Wed | AI in the sales motion: research, drafting, call prep, real-time assist, follow-up, CRM hygiene, where AI helps and where it erodes trust | An AI-assisted sales workflow |
| Thu | Tiers, upsell hooks, and expansion revenue: the tier ladder, in-product upgrade prompts, gating without crippling, NRR as the compounding metric | A 3-tier ladder + expansion map |
| Fri | Revenue planning & unit economics: CAC, LTV, payback, gross margin under AI COGS, churn's compounding damage, the raise-price-vs-cut-cost-vs-retain decision | A maintainable revenue model |
| Sat | BUILD: choose your model, design the tier ladder, build the unit-economics + revenue-projection calculator, wire an AI sales-prep + follow-up workflow | `code-lab/06-monetization-model/` |
| Sun | Synthesis + quiz (13 Q) + flashcards (32) | Marked complete |

## The four controversies you'll be able to argue by Sunday

1. **Outcome-based pricing**: endgame of AI monetization, or a special case that only works for high-frequency, cleanly-attributable outcomes like support resolutions? (Mon/Thu)
2. **Freemium vs free-trial vs paid-only** for an AI product whose free tier burns real GPU money. (Mon)
3. **AI in a human sale**: force multiplier, or trust-eroding tell that gets your domain blacklisted? The AI-SDR churn data is brutal. (Wed)
4. **NRR / expansion as the real growth engine** vs the founder instinct to obsess over new logos. (Thu)

## The one number to carry all week

**Gross margin under real token COGS.** Every model, price, and tier gets stress-tested against it. A price that shows a path to profitability at your actual inference cost is the pass bar for Saturday. A price that only works if the model gets cheaper is a bet, not a business — though in 2026, betting on cheaper inference is the least crazy bet on the board.

## Prerequisites

- [[05-fri-pricing-the-package|b4w09 Friday. Pricing the package]] (value metric, labor-line anchor, COGS discipline)
- [[02-tue-agent-architectures|b2w04 — the sales-agent build]]
- [[05-fri-data-and-scale|b5w14 Friday, retention metrics]]
- Your launched product's real numbers: token cost per core action, current visitor→signup→paid funnel (from [[05-fri-launch-day-instrumentation|b4w10]] instrumentation).

_last_verified: 2026-07-17_

[^1]: Bessemer Venture Partners, *The AI Pricing and Monetization Playbook* (2026): AI-native gross margins of 50–60% vs 80–90% for traditional SaaS; "per-user products are for humans, consumption products are for agents." https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook ; PDF: https://www.bvp.com/assets/uploads/2026/02/The_AI_pricing_playbook_for_founders_Bessemer_Venture_Partners_2026.pdf ; corroborated by SaaS Mag, *The AI COGS Problem: SaaS Gross Margin Compression 2026*, https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
