---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 2
day_name: tue
session_slug: building-elegant-landing-pages
date_due: 2026-06-02
tags: [ai-code-gen, v0, lovable, bolt, replit, webcontainer, shadcn-ui, generative-ui, design-taste, prompt-engineering, tool-failure-modes, agentic-engineering]
sources:
  - vercel-introducing-new-v0-2026
  - vercel-ship-2026-recap
  - vercel-v0-pricing-2026
  - vercel-ai-sdk-3-generative-ui-2024
  - stackblitz-bolt-new-github-repo
  - lennys-inside-bolt-eric-simons-2025
  - evilmartians-bolt-new-stackblitz-2025
  - posthog-how-bolt-works-2025
  - bolt-release-notes-2026
  - lovable-prompting-handbook-2025
  - techcrunch-lovable-13b-talks-2026
  - ycombinator-masad-coding-agents-2025
  - replit-agent-3-announcement-2025
  - techcrunch-replit-9b-valuation-2026
  - growthunhinged-replit-100m-arr-2025
  - shadcn-ui-tailwind-v4-changelog-2025
  - karpathy-sequoia-ascent-2026
  - willison-ai-assisted-programming-tag
  - cherny-claude-code-lennys-2025
  - venturebeat-vercel-v0-90-percent-problem
  - vercel-agentic-infrastructure-2026
  - anthropic-claude-design-2026
  - anthropic-fable-5-mythos-5-2026
  - anthropic-sonnet-5-2026
  - figma-make-model-selection-2026
  - venturebeat-43pct-ai-code-debugging
  - ieee-spectrum-ai-coding-silent-failures
  - coderabbit-ai-vs-human-code-report
  - devouring-details-rauno-freiberg
last_verified: 2026-07-17
word_count_target: 6000
---

# Under the hood of v0, Lovable, Bolt, and Replit — the prompt-to-UI pipeline, failure taxonomy, and the taste layer

## Why this matters

Yesterday's lesson stripped a landing page to its measurable anatomy. Today is the mechanics of the machine that assembles that anatomy at 4 AM when a hypothesis is still warm.

In February 2026 Vercel published the numbers that describe the new substrate: **over 30% of deployments on Vercel are now initiated by coding agents, up 1000% in six months, with Claude Code at ~75% of agent deployments, Lovable and v0 at ~6% each, Cursor at ~1.5%.**[^1] Since launch, more than 4 million people have used v0 to turn prompts into apps.[^2] Lovable hit $10M ARR in 60 days with 15 people and raised $16M in February 2025.[^3] Replit's ARR went from ~$10M at end of 2024 to a Sacra-estimated $150M annualized by September 2025 — roughly 15x in nine months, driven by Replit Agent on Anthropic's Claude.[^4] Bolt.new went from near-death to ~$40M ARR in five months.[^5]

The capability delta after internalizing this lesson is not "you can use v0" — a sharp generalist could figure that out in a weekend. It is that you can **pick the right tool for a specific job, write prompts that collapse the distance between default-Vercel-template output and a deliberate aesthetic, predict where each tool will fail before it fails, and treat the stack selection as an engineering decision with named tradeoffs** — cost per prompt, lock-in surface, quality ceiling, iteration cycle, handoff cost to Claude Code for the last mile.

This lesson teaches the pipeline, the failure taxonomy, and the taste layer. It does not teach the chat UIs — those are surface layers that change monthly, and vendor docs cover them better than any lesson would.

## Prerequisites

- Yesterday's lesson on conversion anatomy (hero / proof / objection / pricing / CTA modular structure, Julian Shapiro's hook-promise-proof-action, Unbounce Conversion Benchmark reference points). Today assumes you can already look at a generated hero and say what is wrong with it at the module level, not just the pixel level. If that muscle is not there, this lesson will produce taste-free tool comparison.
- A working Claude Code install and at least one of {v0, Lovable, Bolt, Replit} account with billing attached. The runnable experiment requires four tools in parallel; if you can only access three, swap the fourth for a second Claude Code run with a different system prompt.

## Layer 1 — Four distinct architectures, not four flavors of the same thing

Industry press describes v0, Lovable, Bolt, and Replit Agent as "the AI app builders" and that framing produces the wrong mental model. They are four architectural bets with different physics. Treating them interchangeably is how operators pay 5x cost for a landing page a better-matched tool would have shipped in a quarter the time.

### v0 (Vercel) — generative UI as a React Server Components discipline

**Public facts, verified:** v0.dev launched October 2023 and went generally available in 2024. In May 2025 Vercel shipped `v0-1.0-md`, a model accessible through an OpenAI-compatible API, making generative UI a `curl` call from Cursor, Claude Code, or any other agent.[^2] In February 2026 Vercel rebuilt v0 around a sandbox-based runtime that directly imports GitHub repositories, automatically pulls environment variables and configurations from Vercel, and emits production-ready code that "already understands the company's infrastructure."[^1][^6] The underlying component substrate is Next.js + Tailwind + shadcn/ui + React Server Components (RSC).[^7]

**Architectural claim:** v0's differentiator is not the model — multiple vendors use the same frontier models — it is the **component vocabulary and the RSC streaming primitive** Vercel open-sourced with AI SDK 3.0 in March 2024.[^7] The generative-UI abstraction lets an LLM response stream React components, not text chunks, and v0 is the canonical implementation against the shadcn/ui vocabulary. Behaviorally: v0 produces components *typed* against shadcn primitives (Button, Card, Dialog, with data-slot attributes after the Tailwind v4 migration in February 2025[^8]), which integrate cleanly into projects that have shadcn installed, and break noisily in projects that do not.

**Where it wins:** single-page, component-dense landing pages where the target aesthetic is within one standard deviation of Vercel Geist, deployment is on Vercel, and generated components paste into an existing Next.js + shadcn codebase. The 70% case for AI-services landing pages.

**Where it fails:** multi-page routing with complex state — v0 generates plausible server components that do not compile against the consumer's actual route tree. Custom design systems deviating from shadcn's tokens require override CSS v0's defaults do not account for. Non-React frameworks are out of scope.

### Lovable — generate → verify → refine as a managed product assembly environment

**Public facts, verified:** Lovable (formerly GPT Engineer) generates React + TypeScript + Supabase code with native Supabase integration for database and auth, GitHub sync, and a conversational chat interface.[^9][^10] In January 2025 Anton Osika (CEO, co-founder) published *The Lovable Prompting Handbook*, and Lovable's product documentation formalised the two execution modes — **Plan Mode** (think through the approach and queue implementation steps before touching code) and **Agent Mode** (autonomous execution of the plan against the codebase) — alongside **Visual Edits**, a direct-UI-manipulation surface for non-code changes, and a Chat-for-debugging pattern in which you investigate failures conversationally before letting Agent Mode re-run.[^11] Osika's public posts describe the architectural shift from single-shot generation to a **generate → verify → refine loop**, explicitly framed as the move from a "generator" to a "managed product assembly environment."[^11][^12]

**Architectural claim:** Lovable's differentiator is not the UI library — it uses the same Tailwind + shadcn substrate as v0 — it is the **full-stack scaffolding pass that treats Supabase as a first-class dependency.** A Lovable prompt mentioning "users, authentication, save their preferences" produces the Supabase schema, RLS policies aligned to Supabase Auth, the React hook, and the component wiring in one pass. The same prompt to v0 returns a static UI and a todo item.

**Where it wins:** prototypes that need a real backend by EOD — waitlist pages with persisted email lists and auth-gated previews, concierge intake forms with persistent state, small CRUD tools. The hidden win: the generated Supabase schema is usable beyond the prototype.

**Where it fails:** nuanced design taste. Output lands closer to "Supabase template" than "Linear page," and closing that gap takes more override iteration than v0 or hand-built shadcn.

### Bolt.new — WebContainer as the unique primitive

**Public facts, verified:** Bolt.new launched circa October 2024 from StackBlitz, the company that spent over four years building WebContainer — a WebAssembly-based operating system that boots a Node.js environment inside a browser tab in roughly 100 milliseconds.[^5][^13] The repository is open-sourced at `github.com/stackblitz/bolt.new` (along with the community `bolt.diy` fork at `github.com/stackblitz-labs/bolt.diy`).[^14][^15] Bolt's middleware routes prompts through Anthropic models (Sonnet as the historical default; in June 2025 Bolt announced a partnership with Anthropic to bring Claude Sonnet 4 to all Bolt users[^16]), tracks file changes, handles package installations via WebContainer, and orchestrates third-party integrations.[^13][^17]

**Architectural claim:** Bolt's differentiator is not the model or UI library — it is **the WebContainer primitive itself.** Submit a prompt; the browser spins up a full Node environment locally; `npm install` runs; a dev server boots on a localhost URL served back into the same tab; every file edit hot-reloads. No remote VM. WebContainer executes the entire stack in-browser rather than in a remote worker.[^13] Eric Simons has described it as a four-year bet that browser coding needed an OS-level substrate, not a syntax-highlighting layer.[^5]

**Where it wins:** zero-setup iteration, demos where reader should see code *and* running app in the same tab, full-stack landing pages where the glue (form → API → database) must work end-to-end. No "works on my machine" asymmetry.

**Where it fails:** context bleed at scale. Bolt's context management produces a pattern reported across teardowns where the agent starts forgetting earlier decisions around file 30–50 and overwrites components that were correct.[^18] For landing-page scope, rarely bites; for multi-feature prototypes, routinely does.

### Replit Agent — the checkpoint-diff-commit model for teams that will keep the project

**Public facts, verified:** Replit Agent launched early access in September 2024, built on Anthropic's Claude.[^19] Replit's ARR trajectory — ~$10M at end of 2024 to $150M annualized by September 2025 — is the clearest commercial evidence that the Agent landed.[^4][^20] In 2025 Replit shifted pricing from a flat $0.25-per-checkpoint model to effort-based pricing, with simple agent runs costing as little as $0.06 and complex work running into multiple dollars per run.[^20]

**Architectural claim:** Replit's differentiator is not the model — it is **the persistent, shared workspace with built-in deploy, database, and auth.** Every project is a long-lived environment with its own PostgreSQL, object storage, and deployment target; the Agent works inside that environment, not in a disposable session. The checkpoint-diff-commit cycle means the Agent proposes a diff, you approve or reject it, accepted diffs commit to the workspace history.

**Where it wins:** prototypes you intend to keep and iterate with a team, deliverables where you want a single URL to share that contains both the running app and the editable environment, hand-offs to less-technical collaborators who need a dashboard rather than a git clone.

**Where it fails:** bespoke design systems. Replit Agent consistently produces the most "template-default" output of the four tools. For a landing page whose taste is the product, Replit is the wrong default.

### The four-way summary that matters

| Tool | Architectural primitive | UI substrate | Backend default | Best-case job |
|---|---|---|---|---|
| v0 | React Server Components streaming | Next.js + shadcn/ui + Tailwind | None (frontend-only by default) | Component-dense hero on Vercel stack |
| Lovable | Generate→verify→refine plan-mode loop | React + shadcn + Tailwind | Supabase (first-class) | Concierge prototype with auth + DB by EOD |
| Bolt.new | WebContainer (in-browser Node OS) | Framework-agnostic; Vite default | In-browser (ephemeral) or user-configured | Full-stack demo where env = runtime |
| Replit Agent | Persistent cloud workspace | Any (React default) | Postgres + object store (managed) | Team-kept prototype with shared URL |

The operator mistake is framing these as "which is best." The right question is **which primitive does my job actually need?** Hero on Vercel for Thursday's outbound → v0. Waitlist page with real signup storage by EOD → Lovable. Demo to a non-technical stakeholder who clicks around the live app → Bolt. Prototype for handoff to an engineering team → Replit, or Claude Code for the last-mile polish.

## Layer 2 — Why the "commodity race" framing is half-right

The controversy — "is v0/Lovable/Bolt/Replit a commodity race-to-zero, or is there genuine moat in taste-corpus and fine-tuning?" — gets wrong answers in most operator threads because it conflates two independent axes.

### The axis that is commodifying: the model

All four tools use Anthropic's Claude family as primary code-gen. Bolt's June 2025 announcement made this explicit; Lovable's architecture diagrams do the same; Replit Agent committed to Claude earliest.[^16][^19][^10] v0's `v0-1.0-md` is Vercel-fine-tuned but sits within the same frontier-model family. Claude Sonnet 4.5 (September 2025) is Anthropic's coding flagship, and Claude Code alone drives 75% of Vercel agent traffic.[^21][^1]

When the same model powers all four, raw generation capability converges. What one tool generates this week, another generates next week given the same model upgrade. This is the commodity race-to-zero Swyx, Mckay Wrigley, and other commentators describe on Latent Space and X throughout 2025.[^22] A new tool reaches parity on pure generation in roughly one model release cycle.

### The axis that is not commodifying: the envelope

What does not commodify is what wraps the model. For each tool the envelope is a different set of architectural choices, each taking months or years:

- **v0's envelope:** RSC streaming primitive, shadcn-typed component vocabulary, Vercel infrastructure knowledge graph, GitHub/Vercel integration surface.
- **Lovable's envelope:** Supabase scaffolding pass, plan-mode 5-step queue, verify-refine loop, Dev Mode (2025).[^12]
- **Bolt's envelope:** four years of WebContainer. Anyone copies the chat UI; nobody copies the four-year WebContainer bet in a quarter.
- **Replit's envelope:** persistent shared workspace, managed Postgres, object storage, deploy target, multi-seat collaboration, a decade of online-IDE product learning.

Behaviorally, the envelope decides the job. Want in-browser full-stack execution? WebContainer is hard differentiation; no model upgrade at v0 replicates it. Want a persistent team workspace? Replit's infrastructure; no model upgrade at Lovable replicates it. The defensible operator position: **the model commodifies within a release cycle, the envelope does not, and 2026's tool winners are those whose envelope matches a job the model alone cannot do.**

### The 80% ceiling thesis, and where it breaks

The related controversy — does AI-code-gen plateau at 80% or 95% of a shippable landing page? — surfaces in Andreas Klinger's PROTOTYPE Capital threads versus the Swyx / Rauno / Rauch counter on shipped cases. Klinger-aligned: the last 20% (taste, last-mile overrides, responsive edges) is where the generalist tool becomes net drag; a human design engineer adds more value than iterating prompts. Rauch-aligned: 2025 shipped cases show production marketing surfaces going AI-generated → production via iteration, not replacement.

The honest operator answer is that the ceiling is **task-dependent and taste-dependent**, not tool-dependent:

- **Standard conversion-anatomy, Vercel-template aesthetic acceptable:** v0 + 30 minutes of prompt iteration → 95% shipped. The last 5% is copy and measurement, not design.
- **Deliberate aesthetic (Linear / Rauno / Raycast / custom):** all four tools default to ~70% of target; the remaining 30% requires an override pass. This is where Claude Code's full-codebase reading closes the gap faster than a specialist tool's chat UI.
- **Multi-page app with routing, state, auth:** specialist tools hit 60–70% and regress past ~2,000 LOC. The context-bleed failure mode, documented in Lenny's Newsletter (Simons 2025) and PostHog's Bolt breakdown.[^5][^18]

The ceiling moves with the job. The choice that optimizes Tuesday's hero is not the choice that optimizes Friday's end-to-end pipeline.

### Quality-metrics counter-evidence

In Lightrun's 2026 report (VentureBeat), **43% of AI-generated code changes require manual debugging in production even after passing QA and staging.**[^23] IEEE Spectrum's 2025 coverage documents silent-failure modes — code passing tests because the tests were generated with the same flawed logic, and generated code that "removes safety checks or creates fake output that matches the desired format."[^24] CodeRabbit's analysis of 470 open-source PRs found AI-generated code creates 1.7x more issues than human-written.[^25]

For a landing page these matter less than for a backend — a buggy hero is visible. For the glue layer (form → webhook → database) in a full-stack prototype they are structurally dangerous. The operator response, per Simon Willison's *ai-assisted-programming* tag, is that **reviewing, testing, and understanding AI-generated code is the difference between "using an LLM as a typing assistant" and vibe coding your way into production.**[^26] For a 4-hour prototype living one week, vibe coding is fine. For a prototype persisting a quarter, the discipline is not optional.

## Layer 3 — The taste layer, and how to push the default

The taste layer is orthogonal to conversion — a beautiful page that doesn't convert is worthless; a converting page with no taste signals commodity. Across the vault's audience, a marketing-ops landing page, a finance-SaaS dashboard, a legal-tech page, a healthcare-intake prototype, and a creative-production portfolio all need *different* taste envelopes even when the conversion anatomy is identical.

### The default-Vercel-template problem

All four tools default to what practitioners call "the Vercel template," the "shadcn default," or the "2024 SaaS gradient." The signature: subtle gradient background, centered H1 in sans-serif (Geist/Inter/system-ui), rounded-pill CTA, three feature cards, testimonial carousel, pricing table. It looks fine. It signals generic. Anyone who has seen three of these in a week stops reading.

This is not a bug — it is the maximum-likelihood output of the model given "build a landing page," averaged across training corpus. Brian Lovin's position on taste as competitive edge lands here: in an era when anyone can generate the default, taste is one of the few remaining moats.[^27]

The operator technique for pushing the default is a three-part prompt scaffold each of v0, Lovable, Bolt, and Claude Code responds to. Call it the **aesthetic brief**:

```
Aesthetic target: [named reference — Linear / Rauno Freiberg's rauno.io / Raycast /
  Vercel Geist / Stripe 2024 / a specific named site]

Load-bearing variables: [type, color, spacing, density, motion, imagery, voice]
  Type: [typeface + scale + line-height + measure]
  Color: [hue count, saturation ceiling, contrast ratio math, background strategy]
  Spacing: [4 or 8 px base, vertical rhythm multiplier]
  Density: [dense / moderate / airy, with a reference page]
  Motion: [static / subtle / expressive, with named reference interactions]
  Imagery: [illustration / photo / 3D / generated; allowed asset types]
  Voice: [copy register — technical, playful, authoritative]

Hard anti-patterns: [the default-Vercel-template signatures to avoid — e.g., no
  radial gradient hero, no gradient-text H1, no rounded-pill CTA if target is Linear]
```

Tested across the four tools in the experiment below, the aesthetic brief moves all four ~15–25 percentage points toward the target. None gets to 100%. The last mile — 5–15% between "obviously inspired by Linear" and "indistinguishable from Linear at a glance" — is where Rauno Freiberg's *Devouring Details* (September 2025, 23 chapters of interaction-design manual[^28]) lives, and where a generated page stops scaling without an explicit override pass.

### The seven variables as debug surface

Wednesday's lesson will deep-dive the seven variables (type, color, spacing, density, motion, imagery, voice). For today, what matters is that **they are the fastest debug surface for a wrong-looking page.** When the hero is off, the failure localizes to one or two variables, and the fix is a targeted prompt addendum, not re-generation:

- Off on type → "Replace the default sans-serif with Inter at 14/-0.01em for body, and a 48px/1.05/-0.02em display size for H1. Measure the hero headline to 60 characters max."
- Off on color → "Remove the radial gradient background. Use `#0A0A0B` as the surface, `#F4F4F5` as text, single accent at `#3B82F6` for CTA only. Contrast ratio on all text ≥ 7:1."
- Off on spacing → "Apply an 8px base grid. Vertical rhythm between sections = 96px. Between elements within a section = 32px. Kill all the `py-12` and `py-16` defaults."
- Off on density → "Increase information density: three rows of proof below the hero instead of one centered testimonial."
- Off on motion → "Static page. No hover animations. No fade-in on scroll. No gradient shift."
- Off on imagery → "Replace the illustrated hero image with a single typographic hero. No stock photos, no 3D renders."
- Off on voice → "Rewrite H1 and sub in the voice of a senior operator explaining this to a peer — no marketing verbs, no 'transform your business', concrete numbers, second-person."

This is where Claude Code earns its 75% share of Vercel's agent deployments. When the taste gap localizes to one or two variables and the fix crosses component boundaries, Claude Code operating on the full codebase closes faster than the specialist tool's chat UI, which is confined to single-file edits.

## Operator case studies — three shipped examples with numbers

### Case study 1 — Bolt.new's trajectory as the canonical WebContainer case

Per Eric Simons' *Lenny's Newsletter* interview (March 2025), Bolt.new went from October 2024 launch to **~$40M ARR in five months**, among the fastest-growing software products documented.[^5] Simons' framing: the four-year WebContainer bet looked like a money-loser the entire time it was built, because "browser-based Node" sounded like a feature rather than a primitive. Once AI code generation emerged as the use case, WebContainer became the unique infrastructure, because AI-generated code that cannot be instantly executed has a 10x longer feedback loop.

**Operator move:** Bolt routes prompts through Claude and passes WebContainer's running state into the model's context every turn.[^13] The model sees stdout, build errors, file state; output is a diff WebContainer applies; the loop closes in seconds. PostHog's breakdown reports "under 2 seconds" as the typical cycle.[^18]

**Transfer:** if your critical feedback loop is "does this actually run," Bolt is the structural match. For "does this look right," v0's RSC streaming is the match. The tool follows the feedback loop.

### Case study 2 — Replit Agent and the $10M → $150M curve

Per *Growth Unhinged* and Sacra, Replit ended 2024 around $10M ARR, then crossed $100M in June 2025 and hit roughly $150M annualized by September 2025 — Sacra attributes the post-Agent acceleration to consumption-based pricing on AI agents and a subscriber base growing 45% month-over-month.[^4][^20] The inflection is Replit Agent (September 2024); the cause is that the pre-existing primitive — persistent workspaces with managed Postgres and deploy — was exactly the envelope the Claude-family model needed to become a product for non-developers.

**Operator move:** Replit shifted pricing in 2025 from flat $0.25-per-checkpoint to effort-based, with the floor at $0.06 and the ceiling at multiple dollars per complex run.[^20] Agent-run pricing only works when the envelope absorbs run-complexity variance; a flat-per-checkpoint price incentivizes the agent to hack "checkpoint completion" and starves the user of deep work.

**Transfer:** if you charge per project for AI services, your pricing model should reflect actual compute variance, not flat-rate theater.

### Case study 3 — Lovable at $10M ARR in 60 days with 15 people

Per Osika's 2025 deck, Lovable hit **$4M ARR in four weeks, $10M in two months with a 15-person team**, Europe's fastest-growing startup by that metric.[^3][^11] TechCrunch reported $16M raised in February 2025.[^10] Osika documents the shift from "single-shot generator" to "managed product assembly environment" — envelope, not model, is the product.[^12]

**Operator move:** Plan Mode. Before any code generation, Lovable's Plan Mode lets you think through the approach and queue implementation steps the user edits before Agent Mode touches files.[^11] This collapses the "Agent generates something surprising, I have to refine or restart" cycle.

**Transfer:** the plan-mode pattern is reproducible in Claude Code via system prompt: *"Before writing code, produce a 5-step plan. Wait for approval. Only then start on step 1."* Boris Cherny's public templates on `howborisusesclaudecode.com` implement variants.[^29]

## Runnable experiment — the four-tool bake-off

Run this end-to-end today. You will produce four landing-page hero outputs plus a comparative analysis.

**Target:** hero + proof + CTA for an AI-services offer aimed at marketing ops leads at mid-market SaaS. Working hypothesis from Monday: the offer converts better with specific-benefit / specific-proof / specific-ask structure than the generic-value-prop default.

### Phase 1 — the aesthetic brief

Draft once, use in all four tools. Linear-inspired target.

```
Target: marketing ops leads at mid-market SaaS companies (50-500 employees)
Offer: AI agent that audits their Salesforce pipeline hygiene weekly and
  produces a rep-level coaching brief, priced at $2,500/month.

Aesthetic target: Linear-adjacent — dense, typographic, sharp. NOT Vercel-template.

Load-bearing variables:
  Type: Inter, 14/-0.01em body, 48/1.05/-0.02em display. Max 60-char measure.
  Color: #0A0A0B background, #E4E4E7 body text, #3B82F6 accent for CTA only. No gradients.
  Spacing: 8px base. 96px between sections. 32px within sections.
  Density: Three proof rows (name + quantified result + logo) below hero. Not one testimonial.
  Motion: Static. No fade-in. No hover animation beyond CTA.
  Imagery: Typographic only. No illustrations, no stock photos.
  Voice: Operator-to-operator. Specific numbers. No 'transform your business.'

Anti-patterns to avoid: rounded-pill CTA, gradient H1, centered single testimonial,
  'Trusted by' logo carousel, feature-card trio below hero.

Content:
  H1: Weekly Salesforce pipeline hygiene coaching, generated by an AI agent.
  Sub: Your agent reviews 500+ opportunities per rep each week, flags the six
    that will likely slip, and produces a one-page coaching brief your managers
    actually read.
  CTA: See a sample brief
  Proof rows: three named (company, quantified result, month/year)
```

### Phase 2 — the four generations

Run the same brief through all four. Time each from first prompt to first shippable output. Record iterations.

- **v0:** single Next.js page with shadcn primitives. One iteration to fix color, one to kill the default gradient.
- **Lovable:** Supabase-backed waitlist page with the same hero. Use Plan Mode to queue the implementation steps; approve, let Agent Mode run.
- **Bolt.new:** static landing page in the WebContainer Vite environment; observe how hot-reload affects iteration speed.
- **Claude Code:** Next.js + shadcn page. Use `/init` or custom slash commands for shadcn setup. Handcrafted baseline.

### Phase 3 — comparative analysis in Claude.ai

Paste all four outputs (HTML + CSS, or screenshots). Prompt:

```
You are a senior design engineer who has shipped landing pages for Linear, Vercel,
and Stripe. I have four landing-page heroes generated by v0, Lovable, Bolt, and
Claude Code against the same aesthetic brief. For each, rate 1-10 on:

(a) Match to the Linear-adjacent aesthetic target.
(b) Code quality and component architecture.
(c) Estimated iterations to ship.
(d) Hidden costs (vendor lock, deploy friction, backend coupling).

Then show me the diff of the hero component between the two closest tools.
Identify the single prompt addendum that would close the taste gap fastest
for each tool. Be specific. Do not hedge.
```

### Phase 4 — iterate the weakest

Pick the lowest-scoring output. Apply the suggested prompt addendum. Run one more iteration. Document whether the gap closed, widened, or plateaued.

### Phase 5 — the write-up

**500 words** on: what each tool exposed about the underlying code-gen model, what each tool hid, and the one-line prompt change that moved the weakest output closest to target. Wednesday's design-system lesson assumes you have done this and can point at the specific variable where each tool defaulted.

### Expected vs observed

Expected pattern from operator reports[^18][^22]: v0 scores highest on code quality and iteration count for the single-page case, ~75% on aesthetic match. Lovable scores highest on backend coupling when the brief includes "waitlist that persists," ~70% on aesthetic without override. Bolt scores highest on iteration speed per cycle (hot-reload beats v0's remote render), ~70% on aesthetic, shows context bleed if pushed past the hero. Claude Code scores highest on aesthetic match after override, lower on initial scaffold speed. If your results deviate significantly, the deviation is the valuable datum. Record it.

## Problem set

Five problems. Each has a measurable pass/fail or a defensible written position. No "think about how you might..." prompts.

### Problem 1 — tool-fit matrix

For each of v0, Lovable, Bolt, and Replit, write a **100-word "where it wins"** and a **100-word "where it breaks"** based on your experiment. Each claim must cite either a specific output from your experiment or a specific source from the citation list. **Pass criterion:** a peer reading your matrix can predict, for a novel landing-page brief, which tool you would pick and why.

### Problem 2 — defend or refute the moat thesis

In **≤500 words**, take a position on: *"In 2026 the AI-code-gen tool winners differentiate on envelope (infrastructure, component vocabulary, persistent workspace, WebContainer) rather than on model capability, and any tool whose only moat is the model will be commoditized within one Anthropic release cycle."* Use **≥3 public tool launches in the last 12 months** as evidence. Candidate evidence: Bolt's WebContainer, Lovable's Supabase scaffolding, Replit's pricing shift, v0's sandbox rebuild, Anthropic's own app-builder moves. **Pass criterion:** your position is falsifiable (name an observation that would disprove it) and engages the opposing view.

### Problem 3 — the reusable aesthetic brief

Design a **3–5 sentence prompt pattern** pasteable into any AI-code-gen tool to push output toward a specific design system. Must cover: typography, color, spacing, density, motion, imagery, voice, and ≥1 named anti-pattern. **Pass criterion:** paste into two tools with the same content payload; visual outputs are materially more similar to each other than the defaults. Rate similarity 1–10 before and after.

### Problem 4 — the named failure mode

Pick one tool. Identify **one reproducible failure mode** — a prompt type that produces consistently wrong output. Document prompt, expected output, observed output, reproduction rate at N≥3, and the fix (prompt change or handoff). **Pass criterion:** a peer reproduces the failure from your prompt with >50% probability. Reference failures to start from[^18][^23][^24]: v0's routing regression in multi-page apps; Lovable's RLS policies with joins across 3+ tables; Bolt's context bleed past ~50 files; Replit Agent's default-template visual signature without an aesthetic reference.

### Problem 5 — the default-tool recommendation

For a first AI-services engagement — $2,500–$10,000 one-page-landing-plus-waitlist due in under a week — **recommend a default tool and a fallback.** Defend on four axes with specific numbers: cost per project, speed to shippable, quality ceiling, lock-in surface. Engage the likely alternative choice and say why it loses. **Pass criterion:** a peer running a similar engagement agrees your recommendation is defensible, or disagrees with a specific counter-number.

## Common failure modes at scale

Operator-documented patterns that surface when these tools move past single-session / single-page scope.

**Context bleed past ~50 files.** Bolt and Lovable both exhibit a pattern where the agent loses track of earlier decisions and overwrites correct components. Reproducible: generate a hero, then prompt 20–30 iterations adding features. Observe where the agent first regenerates a component it already built.[^18] Mitigation: at the 30-component threshold, hand the codebase to Claude Code, which reads the full file tree in one context.[^1]

**Silent failure in the test layer.** Per IEEE Spectrum 2025: AI-generated code produces tests that pass by validating the code's actual behavior rather than intended behavior, creating false confidence while the logic error persists.[^24] For landing pages, rarely fatal; for the glue layer in a full-stack prototype, this shows up as "signup works in dev, silently drops submissions in production." Mitigation: write ≥1 end-to-end test by hand, or have Claude Code write it with an explicit "do not trust existing tests" prompt.

**The 43% redebug rate.** Lightrun's 2026 report of 43% of AI-generated changes requiring production debugging after QA and staging is, per operator response, test-coverage pathology, not model-quality pathology.[^23] Mitigation: treat the prototype as the eval set for the production code, not as the production code.

**CTA regression on mobile.** All four tools default to desktop-first heroes even when the prompt names mobile as 75% of traffic. The mobile layout looks "fine" but the CTA moves below the fold and conversion drops. Mitigation: every aesthetic brief should include "CTA above the fold at 375px viewport." None of the four tools enforces this by default.

**Vendor coupling via templated defaults.** v0's defaults assume Vercel + shadcn; Lovable assumes Supabase; Bolt assumes WebContainer; Replit assumes the workspace. Output is technically portable, but porting cost grows with prototype size. Mitigation: plan the deploy target before first generation.

**Cost explosion on agent-mode runs.** Replit's shift from flat $0.25 to $0.06–$5+ effort-based acknowledges that agent runs can cost a dollar+ per prompt at complexity.[^20] Thirty agent prompts on a taste-override loop can rack up $50+ that would have been $0 in Claude Code on Claude Max. Mitigation: for taste iteration, hand off to Claude Code. For structural scaffolding, accept the per-run cost because the envelope is worth it.

## Open questions — what is not settled

1. **Will the envelope-vs-model moat hold through 2026–2027?** Bear case: Anthropic ships its own app-builder (leaks suggest it is coming), bundles the model with an envelope that subsumes v0/Lovable/Bolt, and specialist tools compete on Anthropic's infrastructure.[^30] Bull case: v0/Lovable/Bolt/Replit envelopes are now opinionated enough that a horizontal Anthropic product cannot match any of them at a specific job. Resolution visible by late 2026 based on which envelope-tool's growth curve flattens first.

2. **Does Figma Make's multimodal pipeline beat text-to-code for design-heavy prototypes?** Figma Make, announced at Config 2025 on May 7, 2025, built on Claude 3.7, bets the native artifact of design is the file, not the prompt.[^31] Counter (Swyx camp): text is more compressible and versionable; multimodal gen introduces divergence that is harder to diff than text-prompt divergence. Unresolved.

3. **Where does Claude Code plateau on pure design-taste generation?** Claude Code leads at 75% of Vercel deployments, but its strength is reading and editing full codebases, not generating polished initial scaffolds. Whether the next model release closes the gap on specialist tools for the *generation* case, or the specialist envelope pulls ahead, is live. Boris Cherny's public position: Claude Code's strength is orchestration of multiple sessions, not competition with specialist tools on single-session generation.[^29][^32]

## Reviewer lens — named critics with specific disagreements

- **Guillermo Rauch (Vercel, public writing on v0 and agentic infrastructure)**[^6] would push back on the Layer 1 claim that "v0's differentiator is the RSC streaming primitive and the shadcn vocabulary." His 2026 positioning has shifted toward v0-the-platform-that-imports-any-repo; the February 2026 rebuild framed v0 around "the 90% problem" of connecting AI-generated code to existing production stacks, not scaffolding new ones. Counter: the moat is the Vercel infrastructure knowledge graph that injects deployment, env-var, and repo context into every prompt. The lesson's "Next.js + shadcn + Tailwind substrate" is 2024-accurate and 2026-incomplete.

- **Swyx (Shawn Wang, Latent Space)**[^22] would push back on the Layer 2 commodity-race framing. His position across 2025 Latent Space posts: the evaluation layer — internal eval harnesses that tell you which tool won a specific job on your actual prompts — is the real operator moat, not the model or the envelope. The lesson grants this partially but does not give the eval harness first-class treatment. The practitioner who internalizes the four-tool bake-off as a repeatable eval, not a one-time exercise, has pulled ahead of one who has merely read this lesson.

- **Andrej Karpathy (X posts on vibe coding / agentic engineering)**[^33][^34] would push back on the taste-override section. His February 2025 "vibe coding" post and his 2026 evolution to "agentic engineering" emphasize that the correct discipline is *not* to push generated output toward a pre-specified aesthetic through prompt engineering, but to *orchestrate multiple agents* each working on a subset of the taste problem. The aesthetic-brief pattern is one rung; the higher rung is an agent that reads the generated page, scores it against the aesthetic, and iterates without each addendum being hand-written. That agent is buildable today in Claude Code.

- **Simon Willison**[^26] would push back on the 43% redebug rate treatment. His position: the redebug rate is a test-coverage pathology, not a model-quality one. AI-generated code at 2026 quality is fine; AI-generated tests for AI-generated code are not. Counter to the mitigation "write at least one end-to-end test by hand": that is the bare minimum; the real discipline is treating every generated test as suspect until reviewed, which the lesson soft-pedals.

- **Anton Osika (Lovable)**[^11][^12] would push back on Case Study 3's framing of Lovable as "best when you need Supabase by EOD." His 2025 positioning (Dev Mode, Prompting Handbook) has shifted toward Lovable-as-managed-product-assembly-environment — the moat is the generate-verify-refine loop, not Supabase specifically. A developer evaluating Lovable on "does it scaffold auth fast" misses the loop discipline driving Lovable's 85% Day-30 retention.

- **Rauno Freiberg (Vercel, *Devouring Details*)**[^28] would push back on Layer 3. His teaching: interaction design begins in code, not in a design brief; the correct discipline for real taste is to prototype specific interactions (motion curves, hover states, scroll behaviors) inline and iterate against the running page. The aesthetic brief gets to 75% of target; the remaining 25% cannot be specified in text and must be demonstrated in code. The handoff-to-Claude-Code move is directionally right; stopping at "Claude Code applies the brief" is premature.

## Further reading

**Must-read (≤5)**
- Vercel Blog — *Introducing the new v0* (Feb 3, 2026). The primary source on v0's current architecture. https://vercel.com/blog/introducing-the-new-v0
- Lenny's Newsletter — *Inside Bolt: From near-death to ~$40M ARR* (Eric Simons interview, March 2025). The canonical operator account of WebContainer as a primitive. https://www.lennysnewsletter.com/p/inside-bolt-eric-simons
- Lovable Blog — *The Lovable Prompting Handbook* (Jan 16, 2025). Primary source on Lovable's four prompting levels and the Chat-for-debugging pattern; pair with the product docs at https://docs.lovable.dev/features/modes and https://docs.lovable.dev/features/visual-edit for Plan Mode, Agent Mode, and Visual Edits. https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook
- Simon Willison — *ai-assisted-programming* tag archive. Running operator-level commentary on AI code-gen failure modes. https://simonwillison.net/tags/ai-assisted-programming/
- RedMonk — *UI Component Libraries, shadcn/ui, and the Revenge of Copypasta* (Kate Holterhoff, April 22, 2025). The best single analysis of why the shadcn copy-paste model is AI-native. https://redmonk.com/kholterhoff/2025/04/22/ui-component-libraries-shadcn-ui-and-the-revenge-of-copypasta/

**Recommended**
- Vercel Blog — *Introducing AI SDK 3.0 with Generative UI support* (March 2024). Primary source on RSC streaming as the generative-UI primitive.
- Evil Martians — *bolt.new from StackBlitz: how they surfed the AI wave* (2025). Technical teardown of the WebContainer + LLM middleware layer.
- PostHog — *How bolt.new works* (Lior Neu-ner, 2025). Operator-facing breakdown of the prompt → WebContainer → diff cycle.
- Y Combinator — *Replit CEO Amjad Masad: Coding Agents, Autonomy, and the Future of Work* (2025 YC Library talk). Masad's own framing of the Agent architecture.
- VentureBeat — *Vercel rebuilt v0 to tackle the 90% problem* (Feb 2026). The rebuilt-v0 reframing and deployment numbers.
- Rauno Freiberg — *Devouring Details* (September 2025 opening, 23 chapters + downloadable React components). The canonical reference for interaction-design-in-code.

**Optional**
- shadcn/ui Changelog — *February 2025: Tailwind v4* — the release notes for the Tailwind v4 and React 19 migration.
- The New Stack — *Vibe coding is passé* (2026). Karpathy's evolution from vibe coding to agentic engineering.
- Contrary Research — *Bolt Business Breakdown* (2025). Business-layer analysis of StackBlitz / Bolt.
- CodeRabbit — *State of AI vs Human Code Generation Report* (2025). Quality-metrics data on AI-generated vs human-written PRs.

## Citations

[^1]: Vercel Blog. *Agentic Infrastructure.* February 2026. https://vercel.com/blog/agentic-infrastructure — supports the claim that 30%+ of Vercel deployments are initiated by coding agents, up 1000% in six months, with Claude Code at ~75% share, Lovable and v0 at ~6% each, Cursor at ~1.5%. Verified from Vercel's own infrastructure post.

[^2]: Vercel Blog. *Introducing the new v0.* February 3, 2026. https://vercel.com/blog/introducing-the-new-v0 — supports the 4M+ users figure since v0's GA in 2024, and the February 2026 sandbox-based-runtime + GitHub import + environment variable pulling architecture.

[^3]: Lovable. *Anton Osika — Building Lovable: $10M ARR in 60 days with 15 people* (video + deck). 2025. https://lovable.dev/video/building-lovable-10m-arr-in-60-days-with-15-people-anton-osika-ceo-and-co-founder — primary source on Lovable's $4M ARR in four weeks, $10M ARR in 60 days, 15-person team claim.

[^4]: Growth Unhinged. *Inside Replit's path to $100M ARR.* Jason Donahue, 2025. https://www.growthunhinged.com/p/replit-growth-journey — supports Replit reaching $10M ARR end-2024 and $100M ARR by June 2025, with 45% MoM subscriber growth since the Replit Agent launch; and Sacra. *Replit revenue, funding & news.* https://sacra.com/c/replit/ — supports ~$2.8M annualized revenue at the start of 2025 and $150M annualized by September 2025, on track for $1B run-rate by end of 2026.

[^5]: Lenny's Newsletter. *Inside Bolt: From near-death to ~$40m ARR in 5 months — one of the fastest-growing products in history | Eric Simons.* March 2025. https://www.lennysnewsletter.com/p/inside-bolt-eric-simons — supports the four-year WebContainer bet, the $40M ARR in five months, and Simons's architectural framing.

[^6]: VentureBeat. *Vercel rebuilt v0 to tackle the 90% problem: Connecting AI-generated code to existing production infrastructure, not prototypes.* February 2026. https://venturebeat.com/infrastructure/vercel-rebuilt-v0-to-tackle-the-90-problem-connecting-ai-generated-code-to — supports Rauch's rebuilt-v0 framing and the "90% problem" positioning.

[^7]: Vercel Blog. *Introducing AI SDK 3.0 with Generative UI support.* March 2024. https://vercel.com/blog/ai-sdk-3-generative-ui — primary source for React Server Components streaming as the generative-UI primitive and the open-sourcing of v0's generative-UI technology.

[^8]: shadcn/ui Changelog. *February 2025 — Tailwind v4.* https://ui.shadcn.com/docs/changelog/2025-02-tailwind-v4 — supports the Tailwind v4 migration, the data-slot attribute per primitive, the HSL→OKLCH color conversion, the deprecation of Toast in favor of Sonner, and the shift of default style to new-york.

[^9]: Lovable Docs. *Integrate a backend with Supabase.* https://docs.lovable.dev/integrations/supabase — primary source on Lovable's native Supabase integration for schema, RLS, and auth.

[^10]: TechCrunch. *Sweden's Lovable, an app-building AI platform, rakes in $15M after spectacular growth.* February 25, 2025. https://techcrunch.com/2025/02/25/swedens-lovable-an-app-building-ai-platform-rakes-in-16m-after-spectacular-growth/ — supports the $16M raise and the growth claims, with Lovable on Claude as the underlying model.

[^11]: Lovable product documentation — "Modes" (https://docs.lovable.dev/features/modes) and "Visual edits" (https://docs.lovable.dev/features/visual-edit), plus Lovable Blog, *The Lovable Prompting Bible / Prompting Handbook* (January 16, 2025, https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook). Primary sources for Lovable's two execution modes — Plan Mode (decision-making: think through the approach, explore options, queue implementation steps before touching code) and Agent Mode (autonomous execution: run the plan against the codebase) — the Visual Edits direct-UI-manipulation surface, and the four prompting levels (training-wheels, no-training-wheels, meta-prompting, reverse meta-prompting) plus the Chat-for-debugging pattern from the handbook.

[^12]: Anton Osika on X. *"lovable *dev mode* coming soon..."* 2025. https://x.com/antonosika/status/1897389383529193496 — supports the shift from "generator" to "managed product assembly environment" and the Dev Mode announcement.

[^13]: Evil Martians. *bolt.new from StackBlitz: how they surfed the AI wave—with no wipeouts.* 2025. https://evilmartians.com/chronicles/bolt-new-from-stackblitz-how-they-surfed-the-ai-wave-with-no-wipeouts — supports the technical description of WebContainer as a WebAssembly-based in-browser OS booting in ~100ms, and the prompt → LLM → middleware → file-change pipeline.

[^14]: GitHub. *stackblitz/bolt.new — Prompt, run, edit, and deploy full-stack web applications.* https://github.com/stackblitz/bolt.new — primary source confirming Bolt's open-source status and architecture.

[^15]: GitHub. *stackblitz-labs/bolt.diy — Prompt, run, edit, and deploy full-stack web applications using any LLM you want.* https://github.com/stackblitz-labs/bolt.diy — the community fork supporting any LLM.

[^16]: Bolt Blog. *We've partnered with Anthropic to bring Claude Sonnet 4 to all Bolt users.* June 2025. https://bolt.new/blog/we-ve-partnered-with-anthropic-to-bring-claude-sonnet-4-to-all-bolt-users — supports the Anthropic model relationship; rollout tied to the World's Largest Hackathon the week of June 2 2025.

[^17]: devclass. *StackBlitz Bolt.new blurs boundaries between web development and skilled use of AI prompts.* October 16, 2024. https://devclass.com/2024/10/16/stackblitz-bolt-new-blurs-boundaries-between-web-development-and-skilled-use-of-ai-prompts/ — early launch-period technical coverage of Bolt.new, including template-start options.

[^18]: PostHog Newsletter. *How bolt.new works* / *From 0 to $40M ARR inside the tech.* Lior Neu-ner, 2025. https://newsletter.posthog.com/p/from-0-to-40m-arr-inside-the-tech — supports the context-bleed failure mode and the under-2-second full prompt-to-running-app cycle.

[^19]: Wikipedia. *Replit* (cross-referenced against Y Combinator Library). https://en.wikipedia.org/wiki/Replit and https://www.ycombinator.com/library/Mi-replit-ceo-amjad-masad-coding-agents-autonomy-and-the-future-of-work — supports the September 2024 Replit Agent early-access launch date; Anthropic Claude is the widely reported underlying model for the Agent per multiple operator writeups in 2024–2025, consistent with Replit's broader integration story.

[^20]: Sacra. *Replit revenue, funding & news.* https://sacra.com/c/replit/ — supports the pricing shift from flat $0.25-per-checkpoint to effort-based $0.06–multi-dollar, and the $150M annualized estimate by September 2025.

[^21]: Anthropic. *Introducing Claude Sonnet 4.5.* September 2025. https://www.anthropic.com/news/claude-sonnet-4-5 — supports the Claude Sonnet 4.5 positioning as Anthropic's coding flagship.

[^22]: Latent.Space. *The Tiny Teams Playbook.* Shawn "swyx" Wang, 2025. https://www.latent.space/p/tiny — supports Swyx's position on internal evals, tiny-teams stack discipline, and the broader AI-engineer progression framing.

[^23]: VentureBeat. *43% of AI-generated code changes need debugging in production, survey finds.* 2026. https://venturebeat.com/technology/43-of-ai-generated-code-changes-need-debugging-in-production-survey-finds — supports the 43% redebug rate and the 88%-need-two-to-three-redeploy-cycles numbers from the Lightrun 2026 report.

[^24]: IEEE Spectrum. *AI Coding Degrades: Silent Failures Emerge.* 2025. https://spectrum.ieee.org/ai-coding-degrades — supports the silent-failure and fake-output failure-mode descriptions.

[^25]: CodeRabbit. *State of AI vs Human Code Generation Report.* 2025. https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report — supports the 1.7x more issues claim from the 470 open-source PR analysis.

[^26]: Simon Willison. *ai-assisted-programming* tag archive. Ongoing. https://simonwillison.net/tags/ai-assisted-programming/ — supports the "using an LLM as a typing assistant" vs "vibe coding" distinction and the review-test-understand discipline.

[^27]: Designer Founders. *Brian Lovin on why designers need to be less "nice" as founders.* https://designerfounders.substack.com/p/brian-lovin-notion-campsite — supports Lovin's position on taste as competitive edge in the AI era.

[^28]: Devouring Details (Rauno Freiberg). Interaction-design manual. September 2025. https://devouringdetails.com/ — supports the 23-chapter September 2025 opening and the interaction-design-in-code discipline.

[^29]: How Boris Uses Claude Code. Boris Cherny's public workflow. https://howborisusesclaudecode.com — supports the orchestration-of-multiple-sessions pattern and the slash-command-heavy Claude Code discipline.

[^30]: Kingy AI. *Anthropic Leak Hints at a Claude App Builder That Could Crush Lovable, Bolt, and v0.* 2025. https://kingy.ai/ai/anthropic-leak-hints-at-a-claude-app-builder-that-could-crush-lovable-bolt-and-v0/ — secondary reporting on rumored Anthropic app-builder. Secondary source, used only for the bear-case hypothesis in the open-questions section.

[^31]: Figma Blog. *Config 2025 Launches Deepen Figma's Design Capabilities As Its Platform Expands.* May 7, 2025. https://www.figma.com/blog/config-2025-press-release/ — supports Figma Make's Config 2025 announcement, Claude 3.7 foundation, and the text-and-image-to-code positioning.

[^32]: Lenny's Newsletter. *Head of Claude Code: What happens after coding is solved | Boris Cherny.* 2025. https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens — supports Cherny's orchestration framing and the $1B run-rate Claude Code revenue claim as of mid-2025.

[^33]: Andrej Karpathy on X. *"There's a new kind of coding I call 'vibe coding'..."* February 2, 2025. https://x.com/karpathy/status/1886192184808149383 — primary source on the coining of vibe coding.

[^34]: The New Stack. *Vibe coding is passé. Karpathy has a new name for the future of software.* 2026. https://thenewstack.io/vibe-coding-is-passe/ — supports Karpathy's evolution from vibe coding to "agentic engineering" as the preferred 2026 frame.
