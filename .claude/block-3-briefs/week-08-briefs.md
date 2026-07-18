# Week 8 briefs — Automation + Agent Integration (MCPs) + Build: Hybrid Agent (Scraper + Summarizer)

Curriculum sessions: "Automation + Agent Integration (MCPs)" + "Build: Hybrid
Agent (Scraper + Summarizer)". July-2026 interpretation: unattended automation
— agents that run on schedules/triggers without a human in the loop, the
reliability engineering that demands, MCP as the integration fabric (b0w02 is
canonical for MCP itself — wikilink, don't re-teach), and a production
scraper→summarizer hybrid as the capstone.

Day plan:

- **01-mon — The automation spectrum in 2026.** n8n 2.x / Make / Zapier
  agents vs code-first (Claude Code + Agent SDK, scheduled workflows, cron
  agents) vs platform-native (Claude dynamic workflows — verify current state).
  Decision framework: determinism vs judgment at each step; when a workflow
  tool beats an agent and vice versa. Total-cost math with current pricing.
- **02-tue — Integration patterns with MCP.** MCP servers as the integration
  layer in automations; auth in headless contexts (OAuth in the 2025-11-25
  spec; service accounts; secrets handling), rate limits, idempotency,
  webhook-in / MCP-out patterns; the 2026-07-28 stateless-core RC's relevance
  for serverless automations (frame as scheduled). Security posture for
  unattended agents — trifecta wikilink; least-privilege by default.
- **03-wed — The scraping stack, legally and technically.** 2026 stack:
  Playwright/Browserbase, Firecrawl, Claude computer-use-class browsing
  (verify current tools/pricing); anti-bot reality (Cloudflare's 2025-26 AI
  crawler tolls / pay-per-crawl — verify), robots.txt + ToS + case law
  (hiQ lineage, EU TDM opt-outs, AI-crawler lawsuits — verify current),
  ethical scraping rules this course endorses; structured extraction
  (schemas, not regex).
- **04-thu — Hybrid agent design: pipeline + judgment.** The scraper→
  summarizer as the canonical hybrid: deterministic fetch/extract stages,
  LLM judgment stages (dedup, relevance, synthesis), checkpointing, retries
  with TRANSIENT/PERMANENT semantics (b0w02 tue taught the convention —
  wikilink), cost budgeting per run, output contracts (structured outputs GA
  API). Scheduling + monitoring: heartbeats, failure alerting, drift
  detection when sources change layout.
- **05-fri — Reliability engineering for unattended agents.** The eval
  discipline for automations: golden-set regression on every prompt/model
  change (b2w04 sat wikilink), canary runs, output-quality drift metrics,
  hallucination containment when nobody reviews the output, kill-switch
  design, incident postmortems. When to keep a human in the loop anyway.
- **06-sat — BUILD: the hybrid scraper + summarizer.** A monitored, scheduled
  agent: scrape 3–5 sources in the reader's niche (respecting robots/ToS),
  extract structured items, dedup, synthesize a daily brief with citations,
  deliver (email/WA/file), with golden-set eval + failure alerting.
  Claude Code orchestrated; code-lab for the pipeline + eval harness.
- **07-sun — Synthesis + quiz + flashcards.** Also: Block 3 capstone recap —
  how weeks 6/7/8 compose into one production-grade practice.

Controversies (verify current state): AI scraping legality/ethics post-
Cloudflare-tolls and the publisher lawsuits; workflow tools vs agent frameworks
("n8n is training wheels" vs "agents are unreliable automations"); how much
autonomy unattended agents should get (name positions).
