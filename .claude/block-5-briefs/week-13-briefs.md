# Week 13 briefs — Making Your Product Feel Magic with AI + Smart Features That Wow

Curriculum sessions: "Making Your Product Feel Magic with AI" + "How to add
Smart Features That Wow Users". July-2026 interpretation: the craft of AI-native
product features that feel magical rather than gimmicky — the difference between
bolting a chatbot on and weaving intelligence into the core loop. This is
product-taste + applied-AI, building on all the technical machinery from
Blocks 2–3 (wikilink; don't re-teach RAG/agents/context engineering).

Day plan:

- **01-mon — What "magic" actually is (and its opposite).** Anatomy of magical
  features: anticipation, invisible effort-collapse, appropriate agency,
  latency-as-feel; the anti-patterns (chatbot-bolt-on, feature-that-needs-a-
  manual, uncanny over-automation, AI-slop features). Case teardowns of
  products that nailed vs faked it (verify real 2026 examples). Reviewer:
  Mollick, Murati, Seibel.
- **02-tue — The proactive/ambient pattern.** Features that act without being
  asked: smart defaults, suggestions, autocomplete/ghost-text, background
  enrichment, "we did this for you" summaries. Designing trust for proactive
  AI (undo, transparency, the right amount of confidence), when proactivity
  becomes creepy or annoying. Latency masking (b3w07 conversation-engineering
  wikilink for perceived-latency craft).
- **03-wed — Generative & personalization features.** In-product generation
  (drafts, transforms, summaries), personalization from user data without
  contamination (b3w06 memory canonical — wikilink), structured outputs
  driving UI (b2w05 wikilink), the "editable AI output" pattern, keeping the
  human in the driver's seat. Cost/latency tradeoffs at feature granularity.
- **04-thu — Reliability of magic: when features fail in public.** Magic that
  breaks is worse than no magic. Confidence gating, fallback to non-AI paths,
  eval-gating features before ship (b2w04 eval discipline + b3w08 reliability —
  wikilink), guardrails, the "degrade gracefully" contract, measuring
  feature trust. Named positions on how much to ship-and-see vs gate.
- **05-fri — Prioritizing smart features: the wow-vs-cost frontier.** Which
  features earn their complexity: the value/effort/risk triage for AI features,
  retention-driving vs demo-driving features, the "sequence of magic" (what to
  ship first), avoiding the AI-feature graveyard. Tie to Block 4 validation
  (wikilink) — validate the feature, not just the product.
- **06-sat — BUILD: add one magical feature to your Week-12 product.** Take the
  Week-12 skeleton; design, eval-gate, and ship ONE genuinely magical feature
  end-to-end (proactive suggestion / in-product generation / personalization),
  with a fallback path and a feature-trust metric. code-lab: the feature
  service + eval harness + fallback, lint/type-checked. Pass bar: the feature
  measurably improves a task and degrades gracefully.
- **07-sun — Synthesis + quiz + flashcards.**

Controversies (verify current): proactive AI (helpful vs creepy — 2026
evidence); how much magic to ship before it's reliable; "AI features" as
retention driver vs churn-inducing gimmick (find real data).
