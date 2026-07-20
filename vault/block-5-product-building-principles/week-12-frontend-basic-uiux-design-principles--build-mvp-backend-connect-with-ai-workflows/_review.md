---
type: review
phase: 2
week: week-12
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 12 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-5-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-12-briefs.md`.

Mechanical checks run this session: `npm install --no-audit --no-fund` on `code-lab/1` (122 pkgs, clean), then `npm run typecheck` (`tsc --noEmit`) and `npm run lint` (`eslint src`) — **both exit 0**. All 13 distinct lesson wikilink targets resolve to real vault files (script-verified; the earlier "MISS" noise was node_modules README fragments, not lesson links). No `(pending)` markers remain — Weeks 9/10/11 already exist and are linked directly. Em-dash density 5.1–8.2/1k across all eight files (under the ~12 bar). Contrast-scaffold tics: Tue and Fri were at 4 and 3 (over the ≤2 budget) — trimmed to 2 each this session. Internal-consistency audit (dailies vs Sunday vs code-lab): WCAG 4.5/3/3, Supabase 7-day pause + $25 Pro, Neon/Databricks ~$1B May 2025 + storage $0.35/GB, Vercel 5-min default + 30-min beta, Sonnet 5 $2/$10 (matches `server.ts` PRICE_IN/OUT), shadcn five styles + CLI-v4 presets, Next.js 16 / React 19.2 / Tailwind v4, the eight AI states, `useChat` + `UIMessage`/`ModelMessage` — all reproduce identically. Canonical homes checked against direct inspection of b2w03 Tue+Wed: the seven aesthetic variables, the codegen tool matrix, and the density-is-audience-indexed point (Brian Lovin, b2w03 [^30]) are recapped-plus-wikilinked, never re-taught. Monday states this explicitly ("This lesson does not re-teach them").

**NAME-VERIFICATION (required this week):** both design voices are real, correctly spelled, and correctly attributed — no repeat of the "Max Freiberg" hallucination.

- **Rauno Freiberg** — Staff Design Engineer at Vercel (prev. The Browser Company / Arc), author of the "Devouring Details" interaction-design course. Corroborated ≥2 independent domains (ui.land interview, LinkedIn/ee.linkedin.com, x.com/raunofreiberg, workspaces.xyz). Week 12's attribution (Vercel design engineer, interaction-detail/motion lens) matches, and is consistent with b2w03's existing [^16]/[^17]/[^30] usage. **Verified.**
- **Brian Lovin** — product designer at Notion, co-founder of Campsite, formerly GitHub Mobile / Spectrum. Corroborated ≥2 independent domains (github.com/brianlovin, brianlovin.com/about, designerfounders.substack.com, read.cv). Week 12 cites him for the "density is the most audience-indexed variable" point, which traces exactly to b2w03 [^30]. **Verified.**
- No other non-core-roster named person requiring verification (Norman, Fitts, Hick, Yablonski, Nielsen, Wathan/Schoger are historical/established citations).

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Thesis ("thin backend wrapped around an AI workflow") is the real mechanism, not a slogan; failure-chain framing is honest. |
| Chip Huyen | 8 | Day table maps to concrete artifacts and pass bars; dependency-order rationale is correct. |
| Jerry Liu | 8 | Correctly subordinates the frontend polish to the workflow being the product. |
| Hamel Husain | 8 | Every day carries an explicit pass bar; "run the experiment" prioritized over prose. |
| Simon Willison | 8 | Facts named with verification stamps, not hyped; server-side-key rule foregrounded. |
| Seibel | 9 | Sells the week in two paragraphs; "if you study one day, study Saturday" is right operating advice. |
| Boris Cherny | 8 | Points at the layer failure modes without teaching them; Claude-Code direction implied. |
| Cohort peer | 8 | "From selling agents to shipping software users log into" is the honest pivot. |
| Mira Murati | 8 | Commercial framing without hype. |
| swyx | 8 | The "versus dissolves once you ask which component" meta-move signals non-naivety. |
| Ethan Mollick | 8 | Study-order guidance is real behavior design. |
| Lilian Weng | 8 | Terminology (eight states, thin backend, generate-then-own) consistent with dailies. |
| Jeremy Howard | 8 | Prereq wikilinks carry the b2w03/b2w04/b3 load. |

**Weighted average: 8.1**

---

## 01-mon — UI/UX first principles for product builders

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | His own lens is in the text ("taste-is-learnable" signal is noisier/slower than code); anchors on the measurable subset (contrast, target size, choice count). |
| Chip Huyen | 8 | Contrast-as-constraint with OKLCH values and WCAG SC numbers; density-as-audience-decision correct. |
| Jerry Liu | 8 | Hierarchy-of-one framed as a spec line an agent executes. |
| Hamel Husain | 9 | Five-principle audit has a measured pass bar (numbers/counts, "no vibes"); aesthetic-usability effect named as the reason to distrust the eye. |
| Simon Willison | 8 | WCAG 2.2 vs 2.1 handled precisely (ratios unchanged, 2.2 adds 2.5.8 target-size); no overclaim. |
| Seibel | 9 | His pushback is the controversy's Position A and the reviewer lens, conceded then bounded ("floor is correctness, not polish"). |
| Boris Cherny | 8 | The `slate-400`/`slate-50` ≈ 3:1 tooling-trap is the concrete pitfall. |
| Cohort peer | 8 | Reference-library rep makes taste-building actionable for engineers. |
| Mira Murati | 7 | Little on how taste shifts across product maturity; defensible scope. |
| swyx | 8 | Jakob's-law "reserve originality for your differentiator" is the right 2026 posture. |
| Ethan Mollick | 8 | Three-phase experiment with a hard four-part pass bar. |
| Lilian Weng | 8 | Fitts/Hick/Jakob attributions accurate and internally consistent with Sunday's cards. |
| Jeremy Howard | 8 | b2w03 seven-variables recapped in one line, wikilinked, not re-taught — compliant. |

**Weighted average: 8.1**

---

## 02-tue — UX patterns for AI-native products

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | The three driving properties (latency/non-determinism/confident-wrong) are the real mechanism behind every pattern. |
| Chip Huyen | 8 | Eight-state table is a genuine design system; over-indication named as the failure mode. |
| Jerry Liu | 9 | Citation UI correctly linked back to agentic-retrieval grounding — front/back-of-house as one trust system. |
| Hamel Husain | 8 | State-audit experiment forces all eight states with concrete UI, not "TODO". |
| Simon Willison | 9 | His lens is in the text: a citation is worthless without grounding; shipping citation UI over ungrounded generation named a dark pattern. |
| Seibel | 8 | His "build the happy path" pushback conceded for the taste layer, bounded to streaming+input-preservation+examples on day one. |
| Boris Cherny | 8 | Optimistic-about-action-not-content is the correct, non-obvious wiring rule. |
| Cohort peer | 8 | "Information not apology" microcopy rule is directly copyable. |
| Mira Murati | 8 | Transparency-vs-confidence resolved on stakes+verifiability, not a global dial. |
| swyx | 8 | Vercel AI Elements placed as the code encoding these patterns. |
| Ethan Mollick | 8 | Reverse-engineer-a-competitor experiment is good behavior design. |
| Lilian Weng | 8 | Confidence-vocabulary (badge/source/color/language) consistent and calibrated. |
| Jeremy Howard | 8 | b2w03 codegen + Block 3 retrieval wikilinked, not re-taught — compliant. |

**Weighted average: 8.3**

Notes: contrast-tics were 4 (budget ≤2) — trimmed two this session (citation "compliance checkbox" line; Seibel-lens "not polish" line). The ~40%-perceived-load figure is flagged in-text as practitioner-source, not peer-reviewed — correct hedge.

---

## 03-wed — The frontend build stack in 2026

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | His "versions churn, the RSC-streaming model is the durable skill" pushback is the reviewer lens; versions carry date stamps. |
| Chip Huyen | 8 | Generate-structure/own-logic split stated as a decision rule with a security-boundary carve-out. |
| Jerry Liu | 8 | AI SDK v5/v6 (AI Elements, Workflows, Sandbox) placed accurately as the AI-UI layer. |
| Hamel Husain | 8 | Experiment must `tsc --noEmit` clean and demands you explain what the tool got wrong. |
| Simon Willison | 8 | 45% OWASP / 1.7x-issues cited for the review-generated-security-code discipline, not hyped. |
| Seibel | 8 | Cohort-peer lens carries "that's a lot of stack for an MVP," answered honestly. |
| Boris Cherny | 9 | His repo-native Claude-Code-orchestration pushback is the sharpest lens; tool-loop framed as legitimate on-ramp. |
| Cohort peer | 8 | The five-step generate-then-own loop is concrete and defensible. |
| Mira Murati | 7 | Version specifics over capability-frontier reasoning; bounded by the topic. |
| swyx | 8 | shadcn-as-design-system-platform (presets) is the current 2026 read. |
| Ethan Mollick | 8 | Hand-edit-the-last-mile drill ties taste to a concrete rep. |
| Lilian Weng | 8 | Component-architecture rules (presentational/container, RSC boundary, tokens) consistent. |
| Jeremy Howard | 8 | b2w03 tool-matrix + design-system wikilinked, not re-taught — compliant. |

**Weighted average: 8.1**

---

## 04-thu — MVP backend architecture

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Thin-backend/fat-workflow is the correct mechanism-level read; orchestrator-workers lifted to the product boundary. |
| Chip Huyen | 9 | His cost-model pushback (per-call → per-user unit economics) is the lens and wired into the pass bar. |
| Jerry Liu | 8 | Where-the-agents-plug-in section is placement, not re-teaching. |
| Hamel Husain | 8 | Pass bar demands no-key-to-browser + token/cost logging + a timeout decision with a number. |
| Simon Willison | 9 | His lens escalates prompt-injection correctly (lethal-trifecta once tools touch other systems); text admits it understates deliberately for MVP scope. |
| Seibel | 8 | His "premature abstraction" pushback on BaaS-isolation conceded, bounded to keeping AI-orchestration portable. |
| Boris Cherny | 8 | Secrets-per-environment + least-privilege keys is the operational discipline. |
| Cohort peer | 8 | Supabase/Neon/Firebase decision framed for a non-infra solo builder. |
| Mira Murati | 8 | BaaS-lock-in resolved on isolation discipline, not ideology. |
| swyx | 8 | Neon/Databricks "80% of DBs created by agents" is the correct 2026-native signal. |
| Ethan Mollick | 8 | Three-phase backend-design experiment with a concrete pass bar. |
| Lilian Weng | 8 | Serverless-vs-durable rule consistent with Friday and Sunday. |
| Jeremy Howard | 8 | Block 3 reliability + b2w04 architectures wikilinked, not re-taught — compliant. |

**Weighted average: 8.3**

---

## 05-fri — Connecting frontend to AI workflows

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | His "the hook hides the SSE bytes" pushback is the lens; the experiment makes you `curl` the raw stream and grep the bundle. |
| Chip Huyen | 8 | Cost-caps/model-routing tied to unit economics and forward to Block 4 pricing. |
| Jerry Liu | 9 | His event-driven pushback (streaming AND durable is the frontier) is the sharpest lens; binary kept deliberately for MVP pedagogy. |
| Hamel Husain | 8 | Pass bar: tokens visibly stream, key provably absent, failure preserves input, cost logged. |
| Simon Willison | 8 | Unsigned-webhook-endpoint named as an open door; signature validation as the boundary. |
| Seibel | 8 | Minimalist camp (SSE + status-column poll ships this week) is his instinct, resolved on core-workload shape. |
| Boris Cherny | 9 | His "cost control is the P&L, foreground it more" pushback is in the lens and the pass bar. |
| Cohort peer | 8 | Two-loop diagram (fast stream / slow queue) is a clean mental model. |
| Mira Murati | 8 | Model-routing-for-cost framed as strategy, not just plumbing. |
| swyx | 8 | Inngest/Trigger.dev/QStash/Vercel Workflows landscape current and correctly differentiated. |
| Ethan Mollick | 8 | Wire-it-end-to-end experiment with a forced-failure phase. |
| Lilian Weng | 8 | React 19 `useOptimistic`/`useActionState` described accurately and consistently. |
| Jeremy Howard | 8 | Block 3 reliability + Thursday wikilinked; useChat recapped, not re-taught — compliant. |

**Weighted average: 8.2**

Notes: contrast-tics were 3 (budget ≤2) — trimmed one ("rate limits...not just abuse prevention, they are"). SSE/`streamText`/`useChat` API surface matches Wednesday and the code-lab.

---

## 06-sat — BUILD: ship the product skeleton

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Thin-slice-vertical-not-horizontal is the right architecture; six phases map to the runnable code-lab. |
| Chip Huyen | 8 | Her "metering is necessary but insufficient (latency percentiles, failure rate)" pushback is the lens and the bridge to analytics. |
| Jerry Liu | 8 | Phase 3 wires exactly one earlier-block workflow, not five stubs. |
| Hamel Husain | 8 | Six-point pass bar is blunt and measurable ("a stranger hits your URL and gets AI value"). |
| Simon Willison | 8 | Backend-required-on-exposure resolved crisply; client-side-key-on-public-URL named the expensive mistake. |
| Seibel | 9 | His build-after-validate pushback is the lens, pointed back at the Block 4 validation week. |
| Boris Cherny | 8 | His "do it in one Claude Code session" note conceded, bounded to build-the-model-by-hand-once. |
| Cohort peer | 9 | "What you deliberately did not build" is the discipline most build-days skip. |
| Mira Murati | 7 | No model-choice stage; inherited from Wednesday, defensible. |
| swyx | 8 | Deploy-to-a-URL-a-stranger-can-reach is the correct ship bar. |
| Ethan Mollick | 8 | Phone-on-non-dev-network test is a real behavior check. |
| Lilian Weng | 8 | Cuts (queue, taste, analytics, auth) each justified, boundaries understood. |
| Jeremy Howard | 8 | Block 4 launch-instrumentation + validation wikilinked forward — compliant. |

**Weighted average: 8.1**

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Q3/Q6 reward applying the rule, not recall; the "versus dissolves on which-component" meta-lesson compresses the week. |
| Chip Huyen | 8 | Q12 forces the unbounded-per-user-cost business failure and its two controls. |
| Jerry Liu | 8 | Synthesis keeps the workflow primary, backend thin — matches the week. |
| Hamel Husain | 8 | Answer key precise; scoring bands direct rereads to the weakest days. |
| Simon Willison | 8 | Q7 rewards the server-side-key rule plus the exact `grep` verification. |
| Seibel | 8 | "Redo Saturday with the code-lab open" is the right remediation. |
| Boris Cherny | 8 | Q6 durable-workflow answer matches Thursday/Friday exactly. |
| Cohort peer | 9 | 12-question quiz + 28 cards calibrated; cold-quiz instruction is correct study protocol. |
| Mira Murati | 7 | Forward pointers commercial; no capability-frontier note. |
| swyx | 8 | Stack flashcard (Next 16/React 19.2/Tailwind v4/shadcn/AI SDK) current. |
| Ethan Mollick | 8 | "How this connects forward" converts content into scheduled next steps. |
| Lilian Weng | 8 | All 28 cards checked against weekday lessons; no contradictions found. |
| Jeremy Howard | 8 | No duplicate territory with earlier quizzes; builds on b2w03, doesn't repeat. |

**Weighted average: 8.0**

Consistency audit (Sunday vs weekdays vs code-lab, all identical): WCAG 4.5/3/3; eight states (idle/empty, submitted, generating, success, low-quality success, refusal, error/timeout, uncertain claim); `useChat` + `UIMessage`/`ModelMessage`; Supabase 7-day pause + $25 Pro; Neon/Databricks ~$1B May 2025 + 80%-agents + $0.35/GB; Vercel 5-min default; Next 16 / React 19.2 / Tailwind v4; shadcn Vega/Nova/Maia/Lyra/Mira + CLI-v4 presets; Inngest 50K/mo + QStash 500/day; Sonnet 5 $2/$10. Quiz (12Q + key) and flashcards (28) all trace to weekday lessons.

---

## code-lab/1 (README, package.json, tsconfig, eslint.config, src/server.ts, src/client.ts, public/index.html, .env.example)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-runtime-dependency `node:http` + native `fetch` in ~200 lines; every line of the SSE loop is readable, which is the point. |
| Chip Huyen | 8 | Per-call token+cost logging with date-stamped Sonnet-5 pricing; unit economics from day one. |
| Jerry Liu | 8 | Lesson→lab mapping table ties each file to Mon/Tue/Thu/Fri; Next.js+AI SDK port shown 1:1. |
| Hamel Husain | 9 | `typecheck` and `lint` both exit 0; README ships the four exact pass-bar commands incl. the `grep sk-ant` check. |
| Simon Willison | 9 | Server-side-only key, input length-capped and type-checked, rate-limit before spend; secrets-by-reference in `.env.example`. |
| Seibel | 8 | Deliberately framework-free teaching skeleton that says so; deploy path is real (Render/Railway/Fly + Vercel). |
| Boris Cherny | 8 | In-memory rate-limit honestly flagged as restart-resetting (use Redis/Upstash in prod); Node 20+ engines pinned. |
| Cohort peer | 8 | README runnable top to bottom; the client demonstrates preserve-input-plus-Retry concretely. |
| Mira Murati | 7 | Single-model call only; multi-model routing left to the prose. |
| swyx | 8 | The AI SDK `streamText`/`toUIMessageStreamResponse` + `useChat` port matches the current API. |
| Ethan Mollick | 8 | Pass-bar checks tie code output to Saturday's decision rule. |
| Lilian Weng | 8 | SSE frame parsing (message_start/content_block_delta/message_delta) matches Anthropic's stream shape. |
| Jeremy Howard | 8 | Small, deterministic, no network in the type/lint path; deps dev-only. |

**Weighted average: 8.3**

---

## Overall Week 12: **8.2 / 10**

(File averages: 8.1, 8.1, 8.3, 8.1, 8.3, 8.2, 8.1, 8.0, code-lab 8.3.) Strongest: Tuesday, Thursday, and the code-lab — reviewer lenses that genuinely argue against the text (Simon on citation-grounding and prompt-injection, Jerry on event-driven hybrids, Chip on cost models) and a lab that type/lint-checks clean and demonstrates the exact server-side-key discipline the lessons preach. Anti-slop: em-dash 5.1–8.2/1k (well under ~12); contrast-tics ≤2/file after trimming Tue and Fri; house tics inside budget. Canonical homes (b2w03 design-system + codegen, b2w04 architectures, b3w06 retrieval, b3w08 reliability, b4w09/10/11) all wikilinked with one-line recaps — no re-teaching found against direct inspection of b2w03 Tue+Wed. Both design-voice names (Rauno Freiberg, Brian Lovin) verified real and correctly attributed.

---

## Surgical fixes applied this session (Phase 3, done)

1. **02-tue Pattern 4:** "citations are not a compliance checkbox, they are the feature…" → "citations are the feature… well beyond any compliance checkbox" (contrast-tic trim; meaning preserved).
2. **02-tue Seibel lens:** "…are not polish, they are the difference between a demo and a product…" → "…are the difference between a demo and a product…, well short of polish" (contrast-tic trim).
3. **05-fri rate-limits section:** "Rate limits and cost caps are not just abuse prevention, they are what make your margins predictable" → "…do more than prevent abuse; they are what make your margins predictable" (contrast-tic trim).

No wikilink upgrades needed — all forward links (Weeks 9/10/11) already resolve to existing files; no `(pending)` markers present. No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Word counts run under the L3 4,500–6,500 soft target** on every daily (Mon 4.5K is closest; Tue 4.0K, Wed 3.5K, Thu 3.8K, Fri 3.5K; Sat 2.9K and Sun 2.5K have lower intrinsic targets). Density is genuinely high and the brief says density over length, so this is a soft miss, not a defect — but Wed and Fri could each absorb ~400 words (Boris's repo-native workflow on Wed; Jerry's streaming-AND-durable hybrid on Fri) without padding.
2. **Fast-moving facts carry `search-verified … fetch egress-blocked — liveness pass pending` stamps**, per the amended protocol. A Phase-4 liveness pass should re-hit the live URLs for: Next.js 16.2.x current line, AI SDK v5/v6 feature split, Supabase/Neon 2026 pricing, Vercel 30-min-function beta, shadcn CLI-v4 presets, Inngest/QStash free-tier limits.
3. **Several 2026 practitioner sources are secondary/SEO-tier** (wavespace, groovyweb, thefrontkit, reloadux, pkgpulse, vela.simplyblock). The ~40%-skeleton-load figure is correctly hedged in-text as practitioner-not-peer-reviewed; Phase 4 should hunt a stronger primary for the trust-pattern census or keep the directional framing.
4. **`code-lab/1` model id is `claude-sonnet-5`** with $2/$10 pricing hard-coded as constants — correct for July 2026 and commented "verify current before pricing a product," but it will date; the comment is the right mitigation.

---

_Review + surgical polish produced 2026-07-17. Files edited: 02-tue-ux-patterns-for-ai-native-products.md, 05-fri-connecting-frontend-to-ai-workflows.md. No git commits made._
