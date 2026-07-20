---
type: lesson
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 6
day_name: sat
session_slug: build-hybrid-agent-scraper-summarizer
date_due: 2026-07-11
tags: [build, scraper, summarizer, hybrid-agent, pipeline, eval-harness, scheduling, delivery, checkpointing, golden-set, claude-code, code-lab]
sources:
  - anthropic-building-effective-agents-2024-12
  - anthropic-structured-outputs-docs
  - claude-code-scheduled-tasks-docs
  - claude-code-routines-docs
  - firecrawl-v25-2026
  - hamel-shreya-evals-faq-2026
  - anthropic-sonnet-5-2026-06
  - cloudflare-content-independence-2026-07
last_verified: 2026-07-17
word_count_target: 5200
---

# Build the hybrid scraper + summarizer — a scheduled, monitored, evaluated agent, end to end

## Why this matters

Today you build the thing the whole week pointed at: a monitored, scheduled agent that scrapes 3–5 sources in your niche (respecting robots.txt and ToS), extracts structured items, dedups, judges relevance, synthesizes a cited daily brief, delivers it, and (the part that separates this from every "I built an AI agent" LinkedIn post) **runs a golden-set eval and alerts on failure, so you can trust it unwatched.** This is a portfolio piece and a sellable template at once: "I'll build you a monitored daily intelligence brief for your niche" is a real offer with real buyers, and you'll have built it end to end.

The build is orchestrated through Claude Code, with the durable pipeline and eval harness in `code-lab/06-hybrid-agent/`. Everything you designed Thursday and specced Friday, you implement today. Budget 3+ focused hours. Walk in with Thursday's stage table and Friday's eval spec done — this lesson assumes them.

## Prerequisites

- [[04-thu-hybrid-agent-design-pipeline-plus-judgment]]: the architecture (stages, checkpoints, contracts, budgets, drift).
- [[05-fri-reliability-engineering-for-unattended-agents]]: the eval harness, heartbeat/alerts, kill switch.
- [[03-wed-the-scraping-stack-legally-and-technically]]: your per-source access policy; the build honors it.
- [[06-sat-build-the-weekly-report-generator]]: the Block 2 build with the same spine-plus-gates discipline; this is its web-fed, unattended sibling. If you shipped that, today is faster.

## Layer 1 — The architecture decision, resolved

Monday's spectrum, Thursday's stages, collapsed into one concrete choice for *this* build:

- **Runtime:** code-first (lane 2), because reliability engineering needs somewhere to live and Saturday's whole point is the eval harness. Python pipeline, Claude Code as the builder and orchestrator.
- **Scheduling:** local cron (or a `$5` VPS + systemd timer) for development, with a clean path to a durable option. Routines are tempting but their network allowlist and no-local-files posture ([[01-mon-the-automation-spectrum-in-2026]]) fight a scraper that hits arbitrary sites and writes local checkpoints, so local scheduling wins here. If your sources are all connector-reachable (Slack, RSS-via-connector), Routines becomes viable; for the general case, cron.
- **Model tiering:** Sonnet 5 ($2/$10 intro through 2026-08-31) for synthesis; a Haiku-class tier for relevance judging. Date-stamped, per [[04-thu-hybrid-agent-design-pipeline-plus-judgment]].
- **Extraction:** feeds/APIs first, typed selectors for stable HTML, structured-output LLM extraction only for irregular prose (the [[03-wed-the-scraping-stack-legally-and-technically]] ladder). Firecrawl is an optional drop-in for sources where its change-tracking earns its credits.
- **MCP:** optional, and deliberately *not* on the critical path today. The judgment stages read from the local checkpoint store directly. You *may* wrap the finished pipeline as an MCP server (Tuesday's Pattern C) so you can query briefs conversationally: a great stretch goal, not a requirement.

## Layer 2 — The pipeline spine, stage by stage

The eight stages from Thursday, now as a build order. Build the spine first end-to-end with one source and no armor, confirm a brief comes out, *then* add the gates. (Seibel's sequence from Friday: happy path first, armor where failures earn it.)

**Stage 1: Fetch.** Per-source access honoring your Wednesday policy: RSS/API where available, polite HTTP with a truthful User-Agent + contact URL otherwise, conditional requests (`If-None-Match`/`If-Modified-Since`) to avoid the re-fetch waste Cloudflare measured at >50% of AI crawl traffic.[^8] Checkpoint raw responses (bytes + status + etag + timing) to `runs/<date>/01-fetch.json`. Classify fetch failures TRANSIENT (5xx/timeout/429 → backoff) vs PERMANENT (403/paywall/ToS block → skip source, alert, degrade).

**Stage 2: Extract.** Every source populates the *same* `Item` schema (title, url, source, published_at, summary, topics[]) via `output_format` structured outputs where prose extraction is needed, typed selectors where HTML is stable.[^2] Checkpoint `Item[]` to `02-items.json`. A source yielding zero items where it usually yields ten is a drift alert (Stage 8), not a valid empty.

**Stage 3: Dedup.** Content-hash `sha256(url + normalized_title)` for exact dupes; a similarity threshold for near-dupes (same story, two outlets). Keep the highest-quality instance, record dropped-duplicate provenance. Mostly deterministic; the near-dup adjudication is the whisker of judgment.

**Stage 4: Relevance judge (judgment island #1).** Cheap tier, structured output `{keep: bool, score: 0-1, reason: str}` per item. Checkpoint to `04-judged.json`. On resume, reuse the checkpoint; do not re-judge (non-idempotent; Thursday). This stage is gated by the relevance golden set (Friday).

**Stage 5: Synthesize (judgment island #2).** Sonnet 5, given *only* the kept items, instructed to summarize those and cite each claim to a source URL in the set: no outside knowledge (hallucination containment, Friday Layer 4). Prose-with-citations, because strict JSON conflicts with citation blocks.[^2] Checkpoint `05-brief.md` + structured metadata.

**Stage 6: Validate contract (deterministic gate).** Every claim cites a URL in the kept set; no fabricated sources; sections + length in bounds; no duplicated items. A faithfulness pass (validated cheap judge) scores each cited claim against its source. Failure is PERMANENT: alert, don't ship. **Only validated briefs proceed.**

**Stage 7: Deliver.** Deterministic code holding the only write credential: email (SMTP), a file drop, or WhatsApp/Slack. Idempotent, keyed by brief date/ID so a retry can't double-send ([[02-tue-mcp-integration-patterns-for-unattended-agents]]).

**Stage 8: Record + alert.** Heartbeat, per-source volume, keep-rate, per-run cost, contract-failure rate to `run.log`; a monitor that alerts on missing heartbeat, zero-from-productive-source, keep-rate/cost anomalies, and contract failures (Friday Layer 3).

## Layer 3 — The eval harness that earns unattended operation

This is what makes the build *shippable* rather than *demoable*, and it's the deliverable that distinguishes your work. From Friday, implemented in `code-lab/06-hybrid-agent/eval/`:

- **Relevance golden set** (`golden_relevance.jsonl`): 30–50 hand-labeled keep/drop items; the judge must clear your threshold (e.g. ≥90% agreement) or changes don't ship.
- **Synthesis rubric** (`rubric.py`): binary per criterion (Hamel's discipline[^6]): cited claims, no fabrication, sections, length, no dupes, plus a faithfulness judge validated against your own labels.
- **End-to-end golden snapshots**: a few frozen raw-fetch checkpoints that must produce acceptable briefs start to finish.
- **The gate**: `python -m eval.run --gate` returns non-zero if any golden set fails at threshold. Wire it so no prompt/model change ships without a green gate. This is your model-drift defense: the thing that catches Anthropic's next default-model change before your readers do.

Run order that matters: **error-analysis first.** Your day-one golden set is a hypothesis. After a week of shadow runs (Friday's staged rollout), rebuild it from the failures you actually observed: Hamel's "error analysis is all you need," sequenced honestly for a build with no production history yet.[^6][^7]

## Layer 4 — The build session, timed

Open Claude Code in a fresh directory. Give it the whole design up front (paste Thursday's stage table and Friday's eval spec), then work in milestones. Concrete prompts:

**Milestone 0 (10 min): scaffold.** *"Scaffold `code-lab/06-hybrid-agent/`: a Python package with modules `fetch.py`, `extract.py`, `dedup.py`, `judge.py`, `synthesize.py`, `validate.py`, `deliver.py`, `monitor.py`, a `pipeline.py` orchestrator that runs stages with checkpoint/resume, an `eval/` package, `config.example.yaml` for sources + schedule + budget, `requirements.txt` (pinned), and a README with run commands and the env-var table. Use structured outputs (`output_format`) for extraction and judging. No secrets in code."*

**Milestone 1 (40 min): happy path, one source.** *"Implement fetch→extract→synthesize→deliver for ONE source [my RSS feed], no armor yet. Deliver the brief to a local file. Show me a real brief."* Confirm output. This is your proof of life.

**Milestone 2 (40 min): full spine, all sources, checkpoints.** *"Add my other sources honoring [paste Wednesday policy]. Add checkpoint/resume: stages write `runs/<date>/NN-*.json`, a re-run skips stages whose valid output exists. Content-hash items. Add dedup and the relevance judge with structured output. Demonstrate a resume after a simulated stage-4 crash that doesn't re-fetch or re-extract."*

**Milestone 3 (40 min): contracts, budget, retries.** *"Add the brief validator (cited-claims, no fabrication, sections, length, faithfulness pass) as a PERMANENT gate. Add TRANSIENT/PERMANENT classification with capped backoff+jitter to every fallible stage. Add per-stage token caps and a per-run dollar ceiling with a controlled stop. Show the validator rejecting a brief with a fabricated source URL."*

**Milestone 4 (40 min): eval harness + monitoring.** *"Build `eval/`: relevance golden set runner with a ship-blocking threshold, synthesis rubric + validated faithfulness judge, and `eval.run --gate`. Add `monitor.py`: heartbeat, volume/keep-rate/cost/contract-failure metrics to `run.log`, and alerts (start with a log-and-notify stub; wire to email/Slack). Add a `PIPELINE_ENABLED` kill switch checked at run start."*

**Milestone 5 (20 min): schedule + chaos test.** *"Add a cron/systemd-timer setup (documented in README, not committed as a live crontab). Then chaos-test: (a) a source returns empty → which alert fires? (b) no run happened → does absence-of-heartbeat catch it? (c) synthesis fabricates a URL → validator rejects? (d) a cited claim misrepresents its source → faithfulness catches? (e) runaway input → cost ceiling stops cleanly? Show each guard firing."* Every guard that doesn't fire correctly is your punch list before you schedule it live.

## Layer 5 — Delivery, scheduling, and going live safely

**Delivery format.** A brief a human wants to read: a dated title, 3–7 synthesized items grouped by theme, each with a one-line takeaway and a source link, and an honest footer ("5 sources checked, 1 unavailable today, N items after dedup"). The footer is Friday's uncertainty-labeling made concrete: it builds trust precisely by admitting gaps.

**Scheduling, staged.** Do not point cron at real recipients on day one. Follow Friday's rollout: **shadow** (delivers only to you) for several days, reading every brief every morning and logging what's wrong (you are the eval harness in week one); **canary** (you + a couple of tolerant users); **full** only after clean days and a golden set rebuilt from real failures. The kill switch is documented and reachable before the first scheduled run.

**Cost, real numbers.** At Sonnet 5 intro pricing, a 5-source / ~40-item daily run lands around $0.45 (~$0.68 after August 31), ~$14–20/month, plus ~$5 infra ([[01-mon-the-automation-spectrum-in-2026]]).[^5] Measure your *actual* token counts from stage checkpoints and put them in the README's cost table; that table is what you show a client, at post-August prices, not intro ones.

**The sellable framing.** What you built is a template: swap the source list and the niche prompt, and it's a new client's daily intelligence brief. The eval harness and monitoring are the parts a client can't get from a no-code demo, and they're the parts that justify a retainer: "monitored, evaluated, with failure alerting" is the difference between a $200 setup and a $2,000/month managed service.

## Common mistakes experts see

- **Building all eight stages before proving one brief comes out.** Ship the one-source happy path first; you'll learn the real problems there.
- **Pointing cron at real recipients on day one.** Shadow first. The first week of briefs will embarrass you; let them embarrass only you.
- **Skipping the eval harness "to save time."** It *is* the deliverable. Without it you built a demo that will drift into wrongness unwatched.
- **Re-judging and re-synthesizing on resume.** Non-idempotent; checkpoint judgment outputs and reuse them.
- **Committing a live crontab or secrets.** Document the schedule; store keys in env/secret store; `.gitignore` `runs/` and any `.env`.
- **No honest footer.** A brief that hides a dead source is a brief that lies. Label what was checked and what failed.
- **Ignoring your Wednesday policy under time pressure.** The build honors robots.txt and ToS even when it's inconvenient; a fast brief built on a bad-faith scrape is a liability with your name on it.

## Reflection questions

1. Your one-source happy path shipped a brief in 40 minutes. Which of the seven remaining stages did building the happy path reveal you actually need *first* — and which did you assume you'd need but didn't?
2. On resume after a stage-5 crash, your pipeline reuses the stage-4 relevance checkpoint. Construct the one scenario where that reuse produces a subtly wrong brief, and the guard that would catch it.
3. Your validator rejects fabricated source URLs with certainty and misrepresentations with a faithfulness judge at ~85% agreement. For a brief nobody reviews, is 85% good enough? What raises it, and what does raising it cost per run?
4. You shadow-ran for a week and the briefs were fine — but "fine" was your judgment, unlogged. What did you fail to capture that Hamel would insist on, and how does that change your golden set?
5. A client wants this for their niche but their two best sources have no RSS and sit behind Cloudflare. Walk the Wednesday decision tree: what do you tell them, and does it change your quote?
6. Your cost table shows $0.45/run at intro pricing. It's August 30. Write the sentence you send the client about what changes tomorrow — before they find out from their invoice.

## My take (reviewer lens)

**Michael Seibel** would love the milestone structure and hate anyone who spends the full 3 hours before delivering a single brief to themselves. His whole thesis is Milestone 1: get one real brief in your inbox today, feel whether it's actually useful, and let that feeling (not the architecture diagram) drive what you build next. The lesson's sequencing honors this, and the honest reinforcement is: **if you only get through Milestone 2 today, you still shipped something real; Milestones 3–4 are what turn it from "works when I watch" into "works when I don't," and you earn them by wanting them.**

**Boris Cherny**, from fleet-scale agent management, would push on the scheduling hand-wave. "Local cron for development" is fine; the lesson should be louder that local cron is *not* where this lives in production: machine sleeps, laptop closes, the job silently stops, and only the heartbeat's absence tells you. The graduation path (durable scheduler: VPS+systemd, Routines for connector-reachable sources, or a managed cron) isn't optional polish; it's the difference between a toy and a service. Fair, and the README makes the durable path explicit, because "it worked on my laptop until I closed it" is the single most common way these die.

**Hamel Husain** would inspect the eval harness first and everything else second, and he'd catch the same thing as Friday: the golden set built today is speculative. His mandate: ship, shadow-run, *read the outputs*, categorize the failures, and let the golden set emerge from real error analysis in week two. The build's day-one harness is scaffolding for a harness you don't yet have the data to fill correctly, which is fine, as long as you know that and schedule the rebuild. The lesson says so; the discipline is doing it.

## Further reading

**Must-read**

- The companion code-lab: `code-lab/06-hybrid-agent/README.md`.
- Anthropic, "Building Effective Agents" (the spine-and-islands discipline, one more time).[^1]
- Hamel & Shreya, Evals FAQ (error-analysis-first, before you trust today's golden set).[^6]

**Recommended**

- Anthropic, Structured outputs docs (the extraction/judge enforcement).[^2]
- Claude Code, Routines and scheduled-tasks docs (the durable-scheduling graduation path).[^3][^4]
- Firecrawl, change-tracking (fetch only what changed).[^9]

**Optional**

- Cloudflare, "Your site, your rules" (why polite, conditional, identified fetching is the durable path).[^8]

## Citations

[^1]: Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents — Dec 19, 2024.

[^2]: Anthropic. Structured outputs — Claude Platform docs. https://platform.claude.com/docs/en/build-with-claude/structured-outputs — `output_format` grammar-constrained JSON; citation-block conflict with strict schema. Corroborated by Thomas Wiegold https://thomas-wiegold.com/blog/claude-api-structured-output/ (search-verified 2026-07-17; direct fetch egress-blocked — liveness pass pending).

[^3]: Claude Code docs. "Automate work with routines." https://code.claude.com/docs/en/routines — fetched live 2026-07-17. Durable cloud scheduling; network allowlist and no-local-files constraints that make local scheduling the right call for a general scraper.

[^4]: Claude Code docs. "Run prompts on a schedule." https://code.claude.com/docs/en/scheduled-tasks — fetched live 2026-07-17. Session-scoped `/loop`; `CLAUDE_CODE_DISABLE_CRON=1` kill-switch shape; jitter.

[^5]: Anthropic. "Claude Sonnet 5." https://www.anthropic.com/news/claude-sonnet-5 — June 30, 2026; intro $2/$10 per Mtok through 2026-08-31 then $3/$15. Verified in master refresh (two-source) and landscape delta §1.

[^6]: Hamel Husain & Shreya Shankar. "LLM Evals: Everything You Need to Know." https://hamel.dev/blog/posts/evals-faq/ — error-analysis-first; binary rubrics; judge validation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Hamel Husain. "Evals, error analysis, and better prompts." Lenny's Newsletter. https://www.lennysnewsletter.com/p/evals-error-analysis-and-better-prompts (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Cloudflare blog. "Your site, your rules." https://blog.cloudflare.com/content-independence-day-ai-options/ — >50% of AI crawl traffic re-fetches unchanged pages; Search/Agent/Training taxonomy; Sept 15 defaults. Corroborated by TechCrunch https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Firecrawl. Change Tracking docs. https://docs.firecrawl.dev/features/change-tracking (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
