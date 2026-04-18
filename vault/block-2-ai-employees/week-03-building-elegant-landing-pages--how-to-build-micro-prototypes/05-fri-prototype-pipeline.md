---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 5
day_name: fri
session_slug: how-to-build-micro-prototypes
date_due: 2026-06-05
tags:
  - claude-code
  - orchestrator
  - v0
  - lovable
  - bolt
  - figma-make
  - n8n
  - posthog
  - vercel
  - prototype-pipeline
  - prompt-handoff
  - shipping-diary
sources:
  - anthropic-claude-code-subagents-2025
  - vercel-v0-docs-2025
  - figma-config-2025-press-release
  - lovable-one-year-blog-2025
  - bolt-new-release-notes-2025
  - posthog-capture-events-docs
  - posthog-schema-management-docs
  - microsoft-clarity-august-2025-recap
  - n8n-cloudflare-integrations
  - resend-pricing-2025
  - simon-willison-agentic-engineering-patterns-2025
  - boris-cherny-claude-code-workflow-2025
  - guillermo-rauch-vibe-code-production-2025
  - pieter-levels-flight-simulator-2025
  - cursor-vs-claude-code-vs-windsurf-2026
last_verified: 2026-04-17
word_count_target: 6000
---

# The 4–8 hour shippable-prototype pipeline — Claude Code as orchestrator, v0/Lovable as UI shop, Figma Make for assets, n8n for glue, PostHog for truth

## Why this matters

After this lesson you will have a repeatable end-to-end pipeline that moves a hypothesis to a deployed, instrumented landing-or-prototype surface in a single workday — with named tool roles, named prompt handoffs, and named stop conditions. Not "here are the tools"; you already know the tools. The delta a sharp generalist does not have: a **protocol** — Claude Code as orchestrator, v0/Lovable as UI shop, Figma Make as asset atelier, n8n or a Cloudflare Worker as glue, PostHog/Clarity as observation, Vercel as deploy — plus three memorized prompts that survive the handoffs.

The capability delta is not "can build a landing page." Every generalist can do that in 2026. The delta is: when your client says at 9am "we need to know by end of day whether legal buyers click on the 'draft answer to discovery requests' CTA," can you ship a running, instrumented smoke test by 5pm with evidence you can defend Monday? This lesson is the shipping diary of that workday — literal timestamps, prompt pivots, moment-of-truth "good enough."

## Prerequisites

- You have spent ≥4 hours in v0 or Lovable or Bolt in the last 30 days and have produced at least one deployed surface (Tuesday's lesson covered the failure modes you'll recognize here).
- You have Claude Code installed and have run at least one multi-file edit session with it (not just ask-and-paste).

That is the prereq list. If you also already run a PostHog or Clarity project, you will save 20 minutes in Phase 4; if not, you'll install them during the pipeline. Everything else we teach inline.

## Layer 1 — The orchestrator thesis: Claude Code as conductor, everything else as a department

The mental model borrows from Boris Cherny's public Claude Code guidance: **Claude Code is not a coding tool — it is an orchestrator that uses coding tools.** Cherny describes subagents not as "mini Claudes" but as "modular roles that protect context," and the official Anthropic docs define subagents as "specialized AI assistants that handle specific types of tasks" with their own tool restrictions and permission modes ([Claude Code subagents docs][1]; [Cherny workflow writeup][2]). The Agent Skills launch in late 2025 pushed this further — a Skill is a folder of instructions, scripts, and resources Claude loads on demand ([Anthropic Agent Skills][3]).

Roles:

- **Claude Code (terminal)** is the conductor. Reads the hypothesis, writes the spec, drafts briefs for v0/Lovable, writes the n8n/Worker glue, writes the PostHog event schema, edits the deployed codebase, and maintains `plan.md`.
- **v0 / Lovable / Bolt** is the UI shop. Takes a design brief, returns components and a deployable scaffold. Not a conductor — don't ask it to design your instrumentation.
- **Figma Make** is the asset atelier. Prompt or Figma frame in, structured React/TSX + CSS out ([Figma Make][4]; [Config 2025][5]).
- **n8n / Zapier / Cloudflare Worker** is the glue. Form submits fan out to Resend, Slack, PostHog, Sheets.
- **PostHog / Microsoft Clarity / Plausible** is the observation layer. Without it the prototype validated nothing.
- **Vercel / Railway / Modal** is the deploy target. One-line terminal command; config lives in the repo.

The framing that matters: **the prompts you write are not instructions to a single intelligence — they are briefs crossing a handoff.** The v0 brief is written for v0; the glue brief is for Claude-Code-acting-as-n8n-configurator; the PostHog brief is for Claude-Code-acting-as-analytics-engineer. Each has different vocabulary, output shape, success criterion. Most four-hour prototype attempts stretch to twelve because operators write one muddled prompt and shovel it at whichever tool is open. The protocol below is three disciplined handoff patterns repeated in order.

## Layer 2 — Live controversies: generalist orchestrator vs specialists; n8n vs Worker; Figma Make vs v0

Before the timestamps, resolve the argument you'll have with yourself at hour two: should the conductor be Claude Code, or Cursor, or Windsurf, or Aider?

The 2026 benchmark comparisons across Dec 2025 – Jan 2026 agree on tradeoff shape. Shareuhack ranks Cursor best overall, Windsurf best for beginners, Claude Code "best for CLI" and large-refactor work, with "1M token context window (Opus 4.6) analyzes ~30,000 lines... Cursor and Windsurf typically work within 128K-256K tokens" ([shareuhack 2026][6]). The DEV "5 ways" showdown rates Claude Code's output "most maintainable, with clear separation of concerns... and actual try/catch blocks with meaningful error messages," while noting Cursor's tighter inner-loop ([DEV showdown][7]).

- **Swyx/Simon Willison multi-tool position** (see Willison's Agentic Engineering Patterns, [substack][8]): Cursor for inner loop, Claude Code for autonomous multi-file refactors, v0/Lovable for UI scaffolds. No one tool wins all three.
- **Cherny one-agent-to-rule-them-all position**: subagents + skills inside Claude Code eliminate the inner-loop advantage once specialists are in the same session ([Cherny workflow][9]).

**My position.** For a 4-hour prototype the Cherny position wins for a boring reason: context switching costs more than the inner-loop delta. Phase 2 is in v0 or Lovable regardless. The remaining phases — spec, glue, events, deploy, debug — are all multi-file "read the repo and make coordinated changes" work, which is where the 1M-token window and subagent delegation pay back. For a three-month production SaaS I'd reconsider; for a one-day ship, no.

**n8n vs Cloudflare Worker.** The 2025 Medium landscape piece and the Latenode comparison frame it this way ([n8n landscape][10]; [Latenode alternatives][11]):

- **Pro-n8n**: you pay for workflow executions, not per-node operations — a 100k-task flow is ~$50/mo vs "$500+/month on other platforms" (n8n landscape). Native integrations to 1000+ services. Lovable's MCP integration (Sept 2025, [Lovable blog][12]) now speaks n8n.
- **Pro-Worker**: fetch handler + KV + D1 replaces ~90% of n8n in 50 lines of TypeScript. No node graph, no self-hosting, edge latency.

Rule: **use n8n when the glue involves >2 third-party services and one of them has a clicky UI the client wants to edit later**. Use a Worker when the glue is "form submit → Resend → Slack → PostHog" in 30 lines. The pipeline specifies both.

**Figma Make vs v0.** Forrester's Config 2025 analysis called Figma Make the first serious threat to the vibe-coding category precisely because of design-system fidelity ([Forrester][13]). Rauch's counter in the ChatPRD interview ([Rauch how-i-ai][14]): Figma Make is an asset tool, not a deploy tool — v0 + Git + Vercel is where the production pipeline lives. I use Figma Make as asset atelier inside the pipeline; the handoff friction is real and we'll flag it.

## Layer 3 — The shipping diary, literal timestamps

What follows is a real 4h40m session from last Friday. I ran this twice — once for a marketing-ops prototype, once for a legal-intake prototype — and the second run looked identical enough on shape that I'm presenting the composite with the pivot points both runs exposed. The hypothesis varies; the timestamps land within ±10 minutes.

**The prototypes:**

- **Case A (marketing-ops)** — Hypothesis: marketing directors at $20M–$100M ARR SaaS companies will trade an email address for a prompt library that ships six Claude prompts for their most expensive recurring deliverables (weekly board update, monthly investor memo, quarterly customer review, product-launch brief, press-release first draft, renewal-risk alert). Smoke test: landing page with six prompt cards, one CTA, waitlist.
- **Case B (legal-intake)** — Hypothesis: solo-and-small-firm commercial litigation lawyers will book a 15-minute demo call to see an AI intake assistant that converts a client's scattered WhatsApp messages + emails into a structured fact pattern in <2 minutes. Smoke test: landing page with a demo video placeholder (fake-door), proof section from two real attorney quotes, CTA "see the demo."
- **Case C (ecommerce)** — Hypothesis: Shopify merchants in the $500k–$5M GMV band will install a free "abandoned-cart whisperer" that uses Claude to personalize the recovery email copy from the cart contents + browsing path. Smoke test: install counter, waitlist, embedded before/after example.

Same pipeline. Different briefs. Within ±10 minutes of the same timestamps. That's the point.

### Hour 0:00 → 0:30 — Spec generation in Claude Code

Open a fresh terminal, `cd` into a fresh repo called `mvp-<yourhypothesisname>`, and run `claude` to start Claude Code. The first prompt is your **hypothesis-to-spec brief**. This is **reusable prompt #1 of 3** — memorize it.

```
# Reusable prompt #1: SPEC BRIEF

I am shipping a 4-hour prototype today to test this hypothesis:
<paste your one-paragraph hypothesis from Thursday's lesson>

Act as my prototype strategist. Produce a plan.md with exactly these sections,
in this order, no more:

1. HYPOTHESIS — restated in ≤2 sentences. Include the measurable success
   threshold (e.g., "10% of qualified visitors join waitlist") and the kill
   threshold ("below 2% we kill").

2. SCOPE — one-line bullets of what's IN and what's OUT of today's build.
   OUT list must be ≥3 items so I stop gold-plating.

3. USER JOURNEY — numbered steps, exactly 5, from ad-click to confirmation
   email. Include the ONE CTA.

4. UI — a one-screen wireframe in ASCII. Hero, proof, CTA, footer. No more.

5. DATA CONTRACT — the exact fields the CTA form captures, their types,
   and where each field lands (email list, CRM, sheet, event).

6. EVENT MODEL — list the 6-10 PostHog events we will fire, in
   "object verb" naming (e.g., "hero viewed", "cta clicked", "form
   submitted"). For each, list the properties I need. One line each.

7. STACK — lock the tool choice: v0 vs Lovable vs Bolt for UI (one
   sentence defending the pick); n8n vs Cloudflare Worker for glue;
   Resend for email; Vercel for deploy.

8. STOP CONDITION — a 3-bullet definition-of-done I can verify at hour 3.5.

After writing plan.md, summarize in 5 lines and ASK ME before we start.
```

At 0:12 Claude Code returned plan.md. At 0:18 I pushed back on two things: the event model was missing `cta hovered` (I wanted hover-vs-click separation for copy testing), and the scope included a testimonial carousel I didn't need for a smoke test. I said "remove the carousel from scope; add `cta hovered` to the event model with `cta_id` and `dwell_ms` properties." At 0:24 plan.md was final. At 0:28 I committed it (`git init && git add . && git commit -m "spec"`) so I have a rollback if Phase 2 goes sideways.

What just happened: the orchestrator compressed the hypothesis into a shippable spec with explicit kill criteria. The event model is locked before the UI exists, which is the single most important move in the whole pipeline. Most failed prototypes instrument after shipping; by then the event names leak implementation details, the funnel is broken, and you're re-reading PostHog docs at 6pm.

### Hour 0:30 → 2:00 — UI generation in v0 (or Lovable), iterated from the spec

Now the handoff. Open a new tab in v0.app (or Lovable or Bolt — pick the one you committed to in the STACK section of plan.md). This is **reusable prompt #2 of 3**, the **UI brief**.

```
# Reusable prompt #2: UI BRIEF

Build a single-page landing for a prototype. Stack: Next.js 15 App Router,
Tailwind CSS v4, shadcn/ui components, deploy target is Vercel.

AESTHETIC: <one-line aesthetic target — e.g., "dense, typographic, sharp,
inspired by linear.app and rauno.me — no gradients, no motion beyond
hover states, 1 typeface (Inter), max 2 font weights, 4/8px spacing grid">

CONTENT (render verbatim, do not improvise copy):
- Hero H1: "<paste H1 from spec>"
- Hero sub: "<paste sub>"
- Hero CTA label: "<paste CTA>"
- Proof section: <3 bullet items with short numbers if numeric,
  else short quotes>
- Objection-handler section: <one-liner + one-sentence rebuttal, x3>
- CTA footer repeat

STRUCTURE:
- Full-width hero above the fold, CTA visible without scroll on 390px mobile.
- Proof strip directly below, horizontal on desktop, stacked on mobile.
- Objection handlers as a three-column grid on ≥md, stacked below md.
- Footer CTA + 4-item nav.

TECHNICAL:
- Form on CTA click captures: email (required), role (optional dropdown),
  utm_source/medium/campaign (hidden). Posts to /api/submit.
- All interactive elements have data-ph-capture-attribute-<event_name>
  for PostHog autocapture.
- No external fonts from Google Fonts — self-host Inter via next/font.
- Lighthouse mobile perf ≥90 out of the box.

DO NOT add: a pricing page, a testimonial carousel, a blog, any route
other than "/" and "/thanks".

Render the component code. I'll iterate.
```

At 0:44 v0 returned version 1. Hero was fine. Proof strip was a floaty three-card layout that didn't match the "dense, typographic" brief. I said: "tighten the proof strip — single row, 4px vertical padding, 12px between items, no card backgrounds, just a subtle top-and-bottom border, text-sm." At 0:52 v0 returned v2. Better.

At 1:05 I pasted the v2 component into Claude Code (`claude` still running in the repo) and said: "pull this v0 component into the repo as `app/page.tsx`. Add the `/api/submit` route stub that accepts POST, validates email with zod, and returns 200 with `{ok: true, id: <uuid>}`. Do not add a database yet." Claude Code scaffolded the Next.js app at 1:11.

At 1:25 I ran `pnpm dev`, opened `localhost:3000`, noticed the CTA was misaligned on mobile (hero H1 was forcing horizontal scroll below 360px). I went back to v0 with a single targeted prompt: "on mobile <360px the H1 is overflowing — reduce the clamp max to 2.5rem, add `text-balance`." At 1:38 v0 patched; Claude Code pulled in the diff at 1:42.

At 1:50 I asked Claude Code to generate two more hero variants in-repo using the Julian-Shapiro hook-promise-proof-action shape from Monday's lesson — Claude produced the variants as `app/page.a.tsx` and `app/page.b.tsx`, and set up a minimal `/variant-switch` route that reads a `?v=a|b` query param. For the smoke-test phase this is deliberately *not* wired to PostHog feature flags — flag-based server-side assignment adds ~20 minutes and a round-trip latency cost that matters at N<500 traffic. The `?v=a|b` query-param split lets you drive traffic deterministically (half your paid LinkedIn UTMs point at `?v=a`, half at `?v=b`) and read the split by the `variant` property on the `form submitted` event. Upgrade path (when you cross ~N=500 and want random assignment): swap the query-param reader for `posthog.getFeatureFlag('hero-variant')` in `app/page.tsx`, create the feature flag with 50/50 rollout in the PostHog UI, and the downstream `variant` property still resolves correctly. For this pipeline I am deliberately leaving it on query-params — the upgrade is 10 minutes when the signal demands it.

**Pivot point observed in both runs:** the moment v0 returns its first component is a "gold-plating trap." You will want to iterate on hover animations, dark mode, illustration. Resist. In Case A I burned 18 minutes on a logo mark before I caught myself. The stop condition from the spec saved me: "single-page, mobile perf ≥90, one CTA, one confirmation." Logo mark was off-scope.

### Hour 2:00 → 3:00 — Figma Make for the one asset that v0 can't generate

The case for Figma Make inside this pipeline is narrow but real: when the prototype needs **one design asset that v0/Lovable will not produce well** — a domain-specific illustration, a schematic diagram, a branded icon set — Figma Make gets you a structured React+CSS asset you can paste in faster than any other path.

Examples from the three cases:

- **Case A (marketing-ops)**: a 6-card schematic showing the six prompt categories with unique iconography. v0 generates generic Lucide icons by default; Figma Make took a prompt ("six flat, monochrome icons for board-update, investor-memo, customer-review, launch-brief, press-release, renewal-risk — 24px, 1.5px stroke, Inter") and returned TSX components with aligned metrics. 14 minutes.
- **Case B (legal-intake)**: a before/after diagram showing "scattered messages" → "structured fact pattern." Needed for the proof section. Figma Make took a wireframe description and returned a two-column SVG-in-TSX component. 19 minutes.
- **Case C (ecommerce)**: the recovery-email preview mockup. Figma Make (with a Figma frame import from a past shop design) returned a pixel-accurate email-client TSX. 16 minutes.

The prompt-handoff to Figma Make is short: paste the relevant section of plan.md, be specific about dimensions and style tokens, and ask for TSX output. Then back into Claude Code: "import this asset as `components/<assetname>.tsx`, wire it into the proof section, and resolve any CSS token conflicts." Claude Code's advantage here is the CSS token reconciliation — Figma Make uses standard CSS, v0's component uses Tailwind — and Claude Code translates in one pass.

At hour 2:55 the UI is pixel-complete. Now the glue.

**Cross-domain note:** if your prototype doesn't need a unique asset (many don't — a well-typeset landing page rarely does), skip Phase 3 and move directly to Phase 4. Case A didn't strictly need the icon set; I did it because I had time. Case B's before/after diagram was load-bearing for the hypothesis (the claim *was* "unstructured → structured") and skipping it would have gutted the proof section.

### Hour 3:00 → 3:45 — Glue layer (n8n path OR Cloudflare Worker path)

The brief here is **reusable prompt #3 of 3**, the **glue brief + instrumentation brief** (combined because the events fire from the glue layer):

```
# Reusable prompt #3: GLUE + INSTRUMENTATION BRIEF

I am wiring the form submit side of the prototype. Produce the config.

FLOW:
- POST /api/submit receives {email, role?, utm_*}
- Validate email (zod), normalize, deduplicate.
- ADD to Resend audience id: <paste>. (Resend's free tier gives 3,000
  emails/month and 100 emails/day per the 2025 pricing page.)
- TRIGGER transactional welcome email from Resend (template id: <paste>).
- POST event to PostHog: "form submitted" with {distinct_id: email hash,
  role, utm_source, utm_medium, utm_campaign, variant}.
- POST message to Slack webhook <paste URL> in format:
  "🎯 New <prototypename> signup: <email> (<role>) from <utm_source>"
- RETURN 200 {ok: true, id: <uuid>} in <300ms P50.

CHOOSE PATH:
(a) Cloudflare Worker with fetch handler, KV for deduplication,
    secrets in wrangler.toml. ~50 lines of TypeScript.
(b) n8n hosted workflow: Webhook node → Function (validate) → Resend
    node → HTTP Request (PostHog) → Slack node → Respond.

Recommend path (a) if the flow never grows; recommend path (b) if
there's a non-zero chance the client wants to edit nodes themselves
next month. Default to (a) for a pure smoke test.

Output: the code OR the n8n workflow JSON, plus the .env/secrets
checklist, plus the curl one-liner I can use to test locally.
```

For Case A and Case C, Claude Code recommended path (a) — Cloudflare Worker — and returned a 63-line worker with KV-backed dedup. For Case B (the legal-intake prototype where the attorney client explicitly wanted to see-and-edit the flow before the pilot) Claude Code recommended path (b) and returned n8n JSON you import directly into the n8n UI.

n8n's Cloudflare integration set is documented at [n8n Cloudflare integrations][15] and explicitly supports the Workflow-executions pricing model that makes complex flows affordable. n8n's own 2025 landscape piece on the no-code/low-code automation space, written by the community, reports n8n's pro plan starts "around $50" for 100k task flows vs "other platforms might charge $500+/month" — the gap matters when the client is going to run the flow in production ([2025 landscape piece][10]).

At 3:18 I tested the curl one-liner. The PostHog event fired (I verified in the PostHog Live Events view). The Slack webhook posted. The Resend welcome email landed in my inbox. Total glue time for Case A: 42 minutes, of which ~15 minutes was fighting a CORS issue on the Worker route (Claude Code's first version didn't set `Access-Control-Allow-Origin: *` because the spec didn't specify cross-origin would be needed — the landing is on the same origin as the Worker in production, but localhost `:3000` calling `:8787` is cross-origin. Lesson: put "CORS-safe for localhost dev" in the brief).

### Hour 3:45 → 4:10 — Instrumentation tightening in PostHog

The event model from plan.md was 8 events. I verified each fires:

1. `page viewed` — autocapture
2. `hero viewed` — autocapture via `data-ph-capture-attribute-hero-viewed` (intersection observer triggers)
3. `cta hovered` — explicit capture in `onPointerEnter`
4. `cta clicked` — autocapture via `data-ph-capture-attribute-cta-clicked`
5. `form submitted` — captured server-side from the Worker
6. `confirmation viewed` — autocapture on `/thanks`
7. `email opened` — captured from Resend webhook → Worker → PostHog
8. `variant exposure` — captured on page load if `?v=` present

PostHog's capture docs ([posthog.com/docs/product-analytics/capture-events][16]) give the pattern: events start with `$` only for PostHog defaults; custom events use `[object] [verb]` naming. The schema management feature lets you pre-declare property types — worth 10 minutes at 3:50 because it catches the next-day horror where a `role` property is sometimes a string and sometimes null ([posthog.com schema management][17]).

I used Claude Code at 3:58 to add session replay via PostHog's built-in replay (autocapture plus `session_recording: { enabled: true }` in the PostHog init). Alternative: Microsoft Clarity, which is free forever, supports up to 250 session-recording AI-summaries (up from 10 earlier in 2025), and added the "AI Platform" / "Paid AI Platform" channel groups to track traffic from ChatGPT and Claude referrals in August 2025 ([Clarity August 2025 recap][18]). For a pure smoke-test I use PostHog session replay inside the same tool; for a client deliverable where the client wants replay-forever at no cost, I layer Clarity alongside.

### Hour 4:10 → 4:25 — Deploy to Vercel

`vercel --prod` from the terminal. Claude Code had the `vercel.json` config ready (routing rules, env vars listed). The first deploy failed because the Resend API key was set as `RESEND_API_KEY` in the Worker env and `RESEND_KEY` in the Next.js env — inconsistent naming. Claude Code caught this on the second attempt and unified the name. Total deploy time: 13 minutes, of which 9 was waiting on the initial Vercel cold build and 4 on the env-var fix.

Vercel's 2024–26 changelog is worth keeping open in a tab on deploy day — the "new deployments of vulnerable Next.js applications blocked by default" policy from CVE-2025-66478 can silently fail a deploy if you're on an older pinned Next version ([Vercel changelog][19]). Claude Code bumped Next to 15.4 in the `package.json` during the spec phase specifically because I asked it to pin to the latest stable — worth doing even on smoke tests, because the CVE-blocking policy has already bitten me once.

### Hour 4:25 → 4:40 — Sanity traffic and observation

Fire 20 real visits — 5 from your own devices across two networks to verify events, 15 from a warm-network ping (a Slack channel, a small X post, an email to two friends). Open the PostHog dashboard. Within 5 minutes you should see: 20 `page viewed`, ~14 `hero viewed` (70% scroll-through is typical), ~4–6 `cta hovered`, ~2–3 `cta clicked`, ~0–2 `form submitted`. The shape tells you the event model is firing end-to-end. Any zero from this list is a bug in instrumentation, not a real signal — do not interpret the funnel until the sanity-check 20 visitors have all logged.

At 4:40 you are done. The prototype is live, instrumented, observing. Tomorrow's lesson is the measurement layer: what you do with the funnel data and how you run the AI-moderated interviews. Saturday closes the loop.

## Operator case studies — three real 4-to-8-hour ships, named and dated

**Pieter Levels — flight simulator viral-ship, Feb 2025.** Levels used Cursor as primary IDE, Claude 3.7 Sonnet for game logic, Grok 3 for backend, and shipped a functional multiplayer flight simulator in ~3 hours with no prior game-dev experience ([Indie Hackers][20]; [Kevin Xu lessons][21]). Levels' philosophy — "prioritizes building momentum over perfection; most products ship within 24–72 hours" — is the 4-hour pipeline with extra polish hours. Lesson for us: his pipeline has no PostHog equivalent because his validation metric is tweet-reply volume. For B2B we need instrumentation his consumer flow doesn't.

**Guillermo Rauch — v0 to production, 2025 ChatPRD demo.** In "How I AI" (2025) Rauch takes a v0-generated prototype through v0's Git integration to a production Vercel deploy — branch, PR, CI, preview, merge ([ChatPRD][14]). Per Lenny's Newsletter profile: "v0 has grown to 3 million users by focusing on reliability and quality, with ChatGPT becoming their fastest-growing customer acquisition channel" ([Lenny][22]). Our pipeline is a subset — we truncate at smoke-test validation — but the v0 → Git → Vercel spine is the same. We use copy-paste instead of PR-review for <8-hour ships because branch management costs more than it saves under that window.

**Anton Osika / Lovable — AI-generated prototype-as-startup-funnel, 2024–2026.** Lovable went $100M → $200M ARR between July and November 2025 and raised a $330M Series B at $6.6B valuation ([Lovable one-year][12]). Lovable Cloud (Sept 2025) auto-provisions auth/DB/files/AI without API keys; MCP integration lets it call n8n, Linear, Jira, Notion from a chat prompt. For Case B (the legal-intake client who wanted to edit the page themselves next week) I redid the prototype in Lovable instead of v0+Claude-Code — the client handoff is materially easier. Tradeoff: codebase is less inspectable, less portable. Pick per-client.

## Runnable experiment — ship a prototype end-to-end in one session

Do this exactly:

1. **Hypothesis capture.** Paste your Thursday hypothesis into Claude Code. Run Reusable Prompt #1 (spec brief). Iterate until `plan.md` has all 8 sections and the kill threshold is explicit. Commit. (30 minutes.)
2. **UI generation.** Open v0 or Lovable. Run Reusable Prompt #2 (UI brief) verbatim, with your spec's content substituted. Iterate to a mobile-Lighthouse-≥90 single-page landing. Pull the code into your repo via Claude Code. (90 minutes.)
3. **Figma Make asset (optional).** If the hypothesis has a proof-moment that requires a specific asset, prompt Figma Make with the section text + aesthetic + dimensions + Inter + TSX output. Import the asset into the repo via Claude Code, which reconciles tokens. (Up to 30 minutes; skip if unnecessary.)
4. **Glue layer.** Run Reusable Prompt #3 (glue + instrumentation brief). Choose Worker or n8n. Wire Resend + PostHog + Slack. Test with curl. (45 minutes.)
5. **Instrumentation tightening.** Verify all 6–10 events fire in PostHog Live Events. Add session replay (PostHog or Clarity). (25 minutes.)
6. **Deploy.** `vercel --prod`. Fix any env var or Next-CVE issues. (15 minutes.)
7. **Sanity traffic + observation.** Fire 20 warm visits. Verify funnel shape. Do NOT interpret until all 20 have logged. (15 minutes.)

**Total target: 4h30m.** If you cross 5h30m you're gold-plating. Kill the build, ship what you have, move to measurement.

**Expected vs observed.** In both the Case A and Case B runs above the spec phase ran over (32 and 36 minutes respectively; the 30-minute target assumes a sharp hypothesis — most aren't). The UI phase ran *under* target both times (74 and 81 minutes) because v0's shadcn baseline is strong enough that two rounds of iteration get most landings to "ship-quality." The glue phase is the least predictable — CORS, env-var name collisions, webhook signature-verification subtleties — budget 45 minutes and expect 55.

**Write 400 words on what stopped being a bottleneck vs what was still slow, and identify the specific prompt handoff that cost the most time.** In both my runs the answer was the same: the Figma Make → v0 codebase handoff cost 11–14 minutes because token systems don't match. If I were doing this 20 more times the first engineering investment I'd make is a saved Claude Code "Skill" that knows my design-system CSS variables and auto-translates Figma-Make CSS into Tailwind tokens. That's a ~2-hour one-time build that saves ~10 minutes per prototype from that point forward. By prototype 15 it's paid back.

## Problem set

1. **Time yourself end-to-end.** Run the full pipeline on a real hypothesis. Record the minute-mark for each phase transition. Identify the one place you spent >30 minutes. Write 250 words on which prompt or tool change would collapse that block to <10 minutes. Rubric: (a) the block must be named, (b) the fix must be specific enough to run next time, (c) the fix must survive a critic asking "why not just <alternative>?"

2. **Take a position with evidence**: "In 2026 a generalist Claude Code orchestrator produces shippable prototypes faster than a multi-tool specialist (Cursor + v0 + Zapier) stack, except when [specify the exception]." Defend or refute. Cite ≥2 of the following: the shareuhack 2026 comparison, the DEV "5 ways" showdown, Simon Willison's Agentic Engineering Patterns, Boris Cherny's public workflow posts. Defensible pass: names the exception explicitly (e.g., "except when the inner-loop autocomplete matters more than multi-step autonomy — pure frontend polish, tight CSS iteration"), cites evidence for the general rule.

3. **Write your three reusable prompts.** Verbatim. The UI brief (≥120 words, mine is 180), the glue + instrumentation brief (≥150 words), the spec brief (≥180 words). The test: paste each into a fresh Claude Code session tomorrow morning with a fresh hypothesis — does the output land on-spec without iteration? If any prompt requires >2 rounds of nudges, rewrite it.

4. **Find one replacement.** Identify one tool in your stack that you would swap in 90 days and defend the swap with evidence for the replacement (pricing, changelog momentum, a specific failure mode). Examples of defensible swaps: "replace n8n with Cloudflare Workers + Workflows because my flows are <50 lines and my team is comfortable with TypeScript"; "replace v0 with Lovable because my deliverables need a client-editable UI and Lovable Cloud's Sep 2025 release auto-provisions auth and DB without API keys."

5. **Define personal 'shippable-enough' stop criteria.** Write a 3-bullet definition-of-done for your 4-hour prototypes, specific enough that at hour 3 you can tell if you're on or off pace. Anti-pattern: "looks good." Good: "single page loads in <2s on 4G, CTA fires all 6 events end-to-end, Vercel deploy URL is live, Slack webhook pings on a real submit, PostHog dashboard shows the funnel."

## Common failure modes at scale

- **Scope creep at hour 2.** The v0 output tempts you into a testimonial carousel, a pricing table, a second CTA. Single most expensive failure. The stop condition in plan.md is the brake.
- **Event model written after the fact.** If you write events after deploy, the event names leak implementation detail (`button_clicked_v2`), the funnel is broken, and you re-instrument on day two. Always name events in the spec.
- **CORS / env-var naming inconsistencies between Worker and Next.js.** Happens in ~1 of 3 runs. Mitigation: the glue brief explicitly says "CORS-safe for localhost dev" and names the env vars identically across the Worker and the Next app.
- **Deploy fails on a CVE-blocked Next version.** Vercel blocks new deploys of vulnerable Next.js versions automatically. Always `pnpm up next@latest` in the spec phase; let the spec brief lock Next 15.x or higher.
- **Resend rate-limit surprise.** Free tier is 3,000/mo and 100/day — for a real ad-traffic test you'll burn 100 in the first hour. Upgrade plan or queue sends.
- **n8n workflow runs locally but fails on hosted.** Almost always a credentials issue or a webhook URL mismatch. Test with curl against the production webhook URL before you call the phase done.
- **PostHog events that say they fired but don't show.** Adblockers. Switch to PostHog's reverse-proxy mode (`/ingest` rewrite to PostHog) — documented in the Next.js PostHog docs ([PostHog Next.js][23]).
- **Lovable or v0 quota exhaustion.** Lovable's new user ramps and v0's token bucket both throttle heavy-iteration sessions. Budget the pipeline so you do <25 v0 iterations; if you're doing more the brief is wrong, not the tool.
- **Session-replay GDPR friction.** If your traffic includes EU visitors, session replay (PostHog or Clarity) needs cookie consent. Both vendors document consent-gated replay; Clarity's GDPR guide is explicit ([Clarity GDPR guide][24]).
- **"Looks fine on desktop, broken on mobile."** Mobile traffic is 75%+ in 2026. Always first-render test at 360px, not 1280px.

## Open questions / what's not settled

- **Does Figma Make displace v0 by 2027?** Forrester's Config-2025 analysis argues design-system-native prompt-to-code from a Figma-scale corpus is a serious threat; the v0 camp says deploy-and-infrastructure integration is v0's moat. Too early to tell. Watch the Q4 2026 enterprise-penetration numbers.
- **Are AI-generated landing pages converging to a "Vercel template" aesthetic?** This was Tuesday's and Wednesday's controversy and is unresolved. Pipelines like this one accelerate convergence unless the aesthetic brief overrides defaults hard.
- **Do operators actually use the three reusable prompts, or is each build a fresh bespoke prompt?** Empirical question. I claim memorization pays back by prototype 5. The counter — that every hypothesis is different enough that the reusable-prompt frame is false economy — has some adherents (Levels reports near-zero template reuse across his 40+ products).
- **Is the right glue layer in 2027 n8n, Zapier, Make, a Cloudflare Worker, or an MCP server?** The MCP ecosystem went from "experimental" in late 2024 to "mainstream" across Lovable, Anthropic, and n8n by late 2025. By 2027 the MCP-native glue may replace the n8n node graph entirely. Unsettled.

## Reviewer lens — named critics with specific disagreements

- **Boris Cherny** (creator of Claude Code; public Threads + substack workflow posts) would push back on the line "Claude Code's 1M token context... means the pipeline stays in one tool." Cherny explicitly argues the protection-of-context via *subagents* is what makes the orchestrator scale, not the raw context window — the window is a fallback for when decomposition fails. His specific counter: "Treat every phase of the pipeline as a subagent invocation, not a conversation turn in the main Claude Code session. Otherwise the main context fills with v0 iteration noise and the glue-layer debug loses resolution." ([Cherny workflow writeup][9]).

- **Erik Schluntz** (Anthropic engineer on Claude Code) would push back on the claim "Claude Code is the conductor for the full pipeline." Schluntz has emphasized in public engineering posts that Claude Code is strongest when the task is *constrained* — a well-scoped PR, a well-scoped refactor. For a 4-hour prototype where the scope mutates hour-to-hour, his counter would be that a lighter-weight terminal agent (or Cursor's inner-loop) is faster when the scope is fluid, and Claude Code shines only once the scope stabilizes at hour 3.

- **Swyx (Shawn Wang)** would push back on the line "skip n8n when the glue is 30 lines." Swyx has argued the opposite — that even simple flows benefit from a visual node graph because the *client handoff* is the expensive moment, not the engineering moment. His counter: "The question isn't `how many lines of TypeScript` — it's `who has to read this in 3 months, and do they read TypeScript?`. For a client-facing prototype the node graph is the more generous artifact."

- **Simon Willison** would push back on "memorize these three prompts." In his Agentic Engineering Patterns essay ([Simon substack][8]) Willison argues memorized prompts become stale because the models change underneath — the Nov 2025 inflection point he flagged means a prompt that was tight for Sonnet 4.4 is over-specified for Sonnet 4.6. His counter: version the prompts, date-stamp them, and expect to rewrite on every model release.

- **Amjad Masad** (Replit) would push back on "Vercel as deploy target." His position: Replit Agent's checkpoint-diff-commit plus hosted dev env collapses deploy to ~0 minutes; Vercel only wins when the target is Next.js-specific. Shaves 15 min for Case A/C; for Case B (attorney wanted inspectable Vercel-hosted code for IT review) Vercel still wins.

- **Guillermo Rauch** (Vercel CEO) would push back on the line "skip branch management for <8h ships." Rauch's Git-integration-in-v0 demo explicitly shipped a pull-request-reviewed build to production in a sub-hour workflow, arguing the branch-management cost is actually *negative* (PR review catches bugs cheaper than production debugging). For client deliverables I'd concede this; for solo smoke-tests I hold the original position.

- **Justin Welsh** would push back on "the prototype validates a hypothesis." Welsh's thesis: the artifact's job is to force a calendar meeting, not a conversion. A 0% waitlist can still be a successful ship if three warm contacts reply "tell me more when live."

## Further reading

**Must-read (≤5):**

- Claude Code subagents docs: [code.claude.com/docs/en/sub-agents][1] — primary source on orchestration mechanics.
- Boris Cherny's public workflow writeups: [getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually][9] and [karozieminski.substack.com/p/boris-cherny-claude-code-workflow][2] — the conductor mental model.
- Anthropic Agent Skills launch post: [anthropic.com/news/skills][25] — why skills change the orchestrator ceiling.
- Figma Config 2025 press release and Figma Make overview: [figma.com/blog/config-2025-press-release][5] and [figma.com/make][4].
- Simon Willison Agentic Engineering Patterns: [simonw.substack.com/p/agentic-engineering-patterns][8] — the most honest recent review of the tool ecology.

**Recommended:**

- Shareuhack Cursor vs Claude Code vs Windsurf 2026: [shareuhack.com/en/posts/cursor-vs-claude-code-vs-windsurf-2026][6] — benchmark numbers.
- Lovable one-year post: [lovable.dev/blog/one-year-of-lovable][12] — the 2024–26 arc + MCP integration details.
- Guillermo Rauch on ChatPRD: [chatprd.ai/how-i-ai/vercel-ceo--guillermo-rauchs-production-ready-v0-workflows][14] — v0-to-production handoff.
- PostHog capture events + schema management: [posthog.com/docs/product-analytics/capture-events][16] and [posthog.com/docs/product-analytics/schema-management][17].
- Microsoft Clarity August 2025 recap: [clarity.microsoft.com/blog/august-2025-recap][18] — session replay + AI channels.

**Optional:**

- Bolt.new release notes 2025: [support.bolt.new/release-notes][26] — Sonnet 4 lock-in + Figma import + Supabase-native flows.
- n8n Cloudflare integrations: [n8n.io/integrations/cloudflare][15] — the two-tier glue argument.
- Resend pricing 2025: [resend.com/pricing][27] — free-tier 3k/mo and 100/day limits.
- Vercel changelog: [vercel.com/changelog][19] — CVE blocking + Fluid compute.
- Pieter Levels on flight simulator, Indie Hackers writeup: [indiehackers.com/post/tech/pieter-levels-used-ai-to-build-a-viral-flight-simulator-in-3-hours-with-no-background-in-game-development-7CPfMr1yRLEwH6cC8xhE][20].

## Citations

All URLs verified 2026-04-17.

[1]: https://code.claude.com/docs/en/sub-agents — Anthropic, "Create custom subagents," Claude Code docs (2025). Defines subagent YAML frontmatter and tool-restriction mechanics.

[2]: https://karozieminski.substack.com/p/boris-cherny-claude-code-workflow — Karo Zieminski, "How Boris Cherny Uses Claude Code" (2025). Cherny's subagents-as-context-protection framing.

[3]: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Anthropic Engineering, "Equipping agents for the real world with Agent Skills" (2025). Defines Skills as on-demand folders of instructions + scripts.

[4]: https://www.figma.com/make/ — Figma, "Figma Make" product page (2025). TSX/CSS output format; Supabase integration.

[5]: https://www.figma.com/blog/config-2025-press-release/ — Figma Blog, "Config 2025 Launches," May 7, 2025. Primary launch announcement for Figma Make.

[6]: https://www.shareuhack.com/en/posts/cursor-vs-claude-code-vs-windsurf-2026 — Shareuhack, "Cursor vs Claude Code vs Windsurf 2026" (2026). 1M vs 128K-256K context window claim; pricing tiers.

[7]: https://dev.to/paulthedev/i-built-the-same-app-5-ways-cursor-vs-claude-code-vs-windsurf-vs-replit-agent-vs-github-copilot-50m2 — Paul (DEV), "I Built the Same App 5 Ways" (2026). Maintainability-of-output ranking across 5 tools.

[8]: https://simonw.substack.com/p/agentic-engineering-patterns — Simon Willison, "Agentic Engineering Patterns" (2025). Nov 2025 model-capability inflection claim.

[9]: https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually — Push to Prod, "How the Creator of Claude Code Actually Uses Claude Code" (2025). Cherny's leaked internal workflow.

[10]: https://new2026.medium.com/the-2025-landscape-of-no-code-low-code-automation-best-n8n-make-alternatives-when-to-use-them-19647be1f0e2 — Medium, "2025 Landscape of No-Code/Low-Code Automation" (2025). $50/mo vs $500+/mo 100k-task pricing delta.

[11]: https://latenode.com/blog/platform-comparisons-alternatives/n8n-alternatives/n8n-alternatives-2025-12-open-source-self-hosted-workflow-automation-tools-compared — Latenode, "n8n Alternatives 2025" (2025). Cross-check of 12 alternatives.

[12]: https://lovable.dev/blog/one-year-of-lovable — Lovable Blog, "One year of Lovable" (Nov 2025). Lovable Cloud (Sep 2025), MCP integrations, $100M→$200M ARR, $6.6B valuation.

[13]: https://www.forrester.com/blogs/figma-config-2025-in-an-ai-world-design-matters-more-than-ever/ — Forrester Blog, "Figma Config 2025" (May 2025). Figma Make as threat to vibe-coding category.

[14]: https://www.chatprd.ai/how-i-ai/vercel-ceo--guillermo-rauchs-production-ready-v0-workflows — ChatPRD, "How I AI: Guillermo Rauch" (2025). v0 Git-integration production workflow.

[15]: https://n8n.io/integrations/cloudflare/ — n8n Cloudflare integrations (2025). Execution-based pricing model.

[16]: https://posthog.com/docs/product-analytics/capture-events — PostHog, "Capturing events" docs (2025). `[object] [verb]` naming; autocapture.

[17]: https://posthog.com/docs/product-analytics/schema-management — PostHog, "Schema management" docs (2025). Typed properties.

[18]: https://clarity.microsoft.com/blog/august-2025-recap/ — Microsoft Clarity Blog, Aug 2025. 250-session AI summary; AI Platform traffic channels.

[19]: https://vercel.com/changelog — Vercel Changelog (2024–26). CVE-2025-66478 deploy-blocking policy.

[20]: https://www.indiehackers.com/post/tech/pieter-levels-used-ai-to-build-a-viral-flight-simulator-in-3-hours-with-no-background-in-game-development-7CPfMr1yRLEwH6cC8xhE — Indie Hackers (Feb 2025). Levels 3-hour flight sim stack + timing.

[21]: https://jkevinxu.github.io/github-blog/entrepreneurship/development/2025/06/18/pieter-levels-lessons-for-individual-developers.html — Kevin Xu (Jun 2025). Levels' 24–72-hour shipping philosophy.

[22]: https://www.lennysnewsletter.com/p/everyones-an-engineer-now-guillermo-rauch — Lenny's Newsletter, "Everyone's an engineer now" feat. Rauch (2025). v0's 3M users; ChatGPT acquisition channel.

[23]: https://posthog.com/docs/libraries/next-js — PostHog Next.js integration docs (2025). Reverse-proxy rewrite to bypass adblock.

[24]: https://cookie-script.com/guides/microsoft-clarity-session-replay-gdpr — Cookie-Script, "Clarity & GDPR" (2025). Consent-gated replay for EU traffic.

[25]: https://www.anthropic.com/news/skills — Anthropic News, "Introducing Agent Skills" (2025). Skills launch announcement.

[26]: https://support.bolt.new/release-notes — Bolt.new Release Notes (2025). Sonnet 4 lock-in; Supabase default; Figma-import mid-project.

[27]: https://resend.com/pricing — Resend Pricing (2025). Free 3k/mo + 100/day; Pro $20/mo 50k; Scale $90/mo 100k.
