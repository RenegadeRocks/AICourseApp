---
type: overview
block: block-5-product-building-principles
week: week-14
title: 'Week 14 — Analytics & Iteration + Scale Infra (Auth, DB, UI Polish)'
last_verified: 2026-07-17
---

# Week 14 — Measure it honestly, then make it survive real users

You have a product. Week 12 gave it a frontend and a backend. Week 13 gave it
magic. This week you find out whether any of it works, and you turn the
prototype into something a stranger can log into without breaking it or
stealing someone else's data.

Two jobs, one week. The first half is **measurement and iteration**: what to
count, how to instrument it without lying to yourself, and how to turn numbers
into product changes when you have forty users instead of forty thousand. The
second half is **hardening**: real auth, a real database schema with
migrations, observability you can actually read, and a UI-polish pass. Saturday
you take the Week 12/13 product and make it production-ready. Sunday closes
Block 5 with the capstone recap and the quiz.

This is the pivot most indie builders skip, and it is why their products die
quietly in month three. The build was the easy part.

## The through-line

Block 4 taught you to instrument a **launch** — the spike, the creatives, the
conversion funnel on day one ([[block-4-test-validate-package/week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/05-fri-launch-day-instrumentation|launch-day instrumentation]]).
This week is **steady state**: the boring, compounding weeks after the spike,
where retention is the only metric that tells the truth. We build on the
[[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/06-sat-validation-instrumentation|Wilson-interval discipline]]
from Block 2 (small-sample statistics), the
[[block-0-basecamp/week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/03-wed-mcp-security|security posture]]
from Basecamp, and [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/03-wed-retrieval-beyond-naive-rag|retrieval at scale]]
from Block 3. We do not re-teach those. We link and extend.

## The seven days

| Day | Session | What you leave with |
|---|---|---|
| **Mon** | Product analytics for AI products | A north-star metric and the 6 AI-specific numbers that predict churn |
| **Tue** | Instrumentation & the analytics stack | An event taxonomy + a product/LLM-observability stack chosen on evidence |
| **Wed** | The iteration loop | A hypothesis→measure→decide cadence that works at 40 users |
| **Thu** | Auth & security for real users | An auth decision (build vs buy) and a multi-tenant isolation model |
| **Fri** | Data & scale | A Postgres-first data plan and honest thresholds for when to worry |
| **Sat** | BUILD: harden the product | Real auth + schema/migrations + observability + a live metric, shipped |
| **Sun** | Synthesis + capstone recap + quiz | Block 5 assembled; 12 quiz Qs; 30 flashcards |

## The live controversies you will be able to argue

- **Premature scaling vs build-for-scale-from-day-1.** Startup Genome says 70%
  of failed startups died of premature scaling. So why does everyone reach for
  Kubernetes on day one?
- **Build vs buy your auth.** Clerk's speed-to-ship against Better Auth's
  zero-marginal-cost. Where does the line actually sit in 2026?
- **Session replay ethics.** You can watch every user's screen. Should you?
  What does GDPR let you keep?
- **How much observability an indie product actually needs.** The eval-in-prod
  tax, and when paying it is procrastination dressed as rigor.

## Pass bar for the week

By Sunday you can (1) name your north-star metric and defend it, (2) read your
own retention curve, (3) point to one product change you shipped because of a
number, and (4) hand a hostile stranger a login URL and watch, in your
dashboard, exactly what they did — without them being able to reach anyone
else's data.

_Estimated reading time: ~3 hours 40 minutes across the week (excluding the
Saturday build)._

_last_verified: 2026-07-17_
