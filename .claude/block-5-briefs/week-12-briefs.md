# Week 12 briefs — Frontend UI/UX Principles + MVP Backend Connected to AI Workflows

Curriculum sessions: "Frontend - Basic UI/UX Design Principles" + "Build MVP
backend & connect with AI workflows". July-2026 interpretation: the reader has
been shipping agents and landing pages; now they build the actual product
surface — a real frontend with taste, and an MVP backend that connects to the
AI workflows from Blocks 2–3. b2w03 taught design-system literacy and codegen
tools — wikilink, don't re-teach. This week is UX principles for AI products +
the backend that serves them.

Day plan (researcher may sharpen; keep the arc):

- **01-mon — UI/UX first principles for product builders.** Visual hierarchy,
  typography, spacing/grid, color/contrast + WCAG 2.2 accessibility (verify
  current standard), affordances, Fitts/Hick's laws, the difference between
  "looks designed" and "is usable." Taste as a learnable skill for engineers.
  Wikilink b2w03 design-system literacy; go beyond it into interaction design.
- **02-tue — UX patterns for AI-native products.** Designing for
  probabilistic/latent systems: loading/streaming states, optimistic UI,
  showing confidence/uncertainty, citations/sources UI, graceful failure &
  regeneration, empty states, onboarding to non-deterministic value, the
  "AI did something" transparency patterns. Verify current best practice
  (Anthropic/OpenAI/Vercel AI UX guidance 2026).
- **03-wed — Frontend build stack in 2026.** Next.js/React (verify current
  major versions), Tailwind, shadcn/ui-class component systems, the AI-codegen
  workflow (v0/Lovable/Bolt → export → own the code) as the realistic path;
  when to hand-code vs generate; component architecture that survives
  iteration. Cite current versions/pricing. Wikilink b2w03 codegen lesson.
- **04-thu — MVP backend architecture.** The 2026 pragmatic stack: BaaS
  (Supabase/Firebase/Neon — verify current state/pricing), serverless vs
  long-running for AI workloads (streaming, timeouts, background jobs),
  API design for AI endpoints, secrets/env, the "thin backend + AI workflow"
  pattern. Where the agent/automation work from Blocks 2–3 & 8 plugs in
  (wikilink, don't re-teach the agents themselves).
- **05-fri — Connecting frontend to AI workflows.** Streaming responses to the
  UI (SSE/streaming APIs), job queues for long agent runs, webhooks, state
  management for async AI, cost/rate-limit handling at the product layer,
  optimistic + eventual-consistency patterns, error surfaces. The full
  request→agent→stream→render loop.
- **06-sat — BUILD: ship the product skeleton.** A working thin-slice product:
  frontend (generated then owned) + MVP backend + one AI workflow from an
  earlier week wired end-to-end, deployed to a URL. code-lab: the backend +
  a streaming AI endpoint + minimal frontend, lint/type-checked, with a README
  deploy path. Pass bar: a stranger can hit the URL and get AI value.
- **07-sun — Synthesis + quiz + flashcards.**

Controversies (verify current): hand-code vs AI-generate-then-own the frontend;
BaaS lock-in vs roll-your-own; how much to show users about the AI's
uncertainty (transparency vs confidence).
