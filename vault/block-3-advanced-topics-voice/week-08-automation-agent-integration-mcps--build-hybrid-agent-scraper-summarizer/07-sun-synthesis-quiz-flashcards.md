---
type: synthesis
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 7
day_name: sun
title: 'Week 8 Synthesis — Unattended automation as engineered trust'
study_date: 2026-07-12
date_due: 2026-07-12
tags: [synthesis, quiz, flashcards, automation, mcp, scraping, hybrid-agent, reliability, evals, unattended-agents, block-3-capstone]
last_verified: 2026-07-17
word_count_target: 4000
---

# Week 8 Synthesis — Unattended automation as engineered trust

## The one-sentence thesis of this week

The six lessons — the automation spectrum, MCP integration for headless agents, the scraping stack, hybrid agent design, reliability engineering, and the build — are six answers to one question: *what does it take to trust an agent's output when no human sees it before it ships?* Everything this week is the engineering of that trust, and the answer is never "a better model" — it's determinism where you can get it, contracts where you can't, evals that gate every change, and a human at exactly the irreversible steps and nowhere else.

---

## The unifying frame: automation is trust, decomposed

Block 2 taught you to build AI workers you supervised. Block 3 Week 8 removes the supervision, and every lesson is a different facet of what has to replace it:

- **Mon — the automation spectrum.** The decision is not "n8n or agents" but *which runtime lets me engineer reliability at all*, chosen per workload by determinism-vs-judgment, priced honestly at July-2026 rates.
- **Tue — MCP integration.** The decision is not "use MCP" but *how do I wire an agent to real systems without a human at the consent screen* — service identities, least privilege, idempotency, and the stateless-core RC that makes serverless MCP natural.
- **Wed — the scraping stack.** *How do I build a data supply that's clean legally and technically* against a web that now meters AI access by default (Cloudflare's Sept 15 block) and courts that turned robots.txt into evidence.
- **Thu — hybrid design.** *Where do the deterministic stages end and the judgment islands begin*, with checkpoints, retries, contracts, and budgets as the plumbing between them.
- **Fri — reliability engineering.** *How do I know it keeps working unwatched* — golden-set gates, canaries, drift metrics, hallucination containment, kill switches, and the human at the irreversible actions only.
- **Sat — the build.** All five, made real: a scheduled, monitored, evaluated scraper→summarizer you'd put your name on.

Frame it this way and the week is one system: **trust is not a property of the model; it's a property of the machinery you build around it.**

---

## Where each day's content goes forward

| This week's lesson | Underwrites later |
|---|---|
| Mon — automation spectrum | Every client automation decision; Block 4 packaging; Block 6 monetization (managed-service pricing) |
| Tue — MCP integration | Every headless integration; Block 4 productization; enterprise engagements needing service identities |
| Wed — scraping stack | Any data-supply-dependent product; Block 6 offers built on monitored data; the legal posture for client work |
| Thu — hybrid design | Every multi-stage automation; the spine-and-islands shape recurs in every unattended product |
| Fri — reliability engineering | Every unattended deployment; Block 4 validation; the eval discipline that separates a service from a demo |
| Sat — the build | The portfolio piece and the template you resell across niches |

---

## The week's key moves — the mental-move table

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Choose the runtime by workload (determinism-vs-judgment per step), never by team identity | Wrong-lane deployments overfit nondeterminism onto deterministic tasks — the dominant published failure mode | Any automation scoping | Never; this is always the first move |
| 2 | Let the agent decide *inside* runs; never let it decide *whether* runs happen | Schedules, triggers, kill switches must be reasoning-free infrastructure you trust at 3 a.m. | Every unattended system | — |
| 3 | Price at post-intro rates and stamp the date | Sonnet 5's $2/$10 ends 2026-08-31; the current tokenizer runs ~30% heavier — intro-priced quotes are margin bombs | Any client cost table | — |
| 4 | Run automations on service identities with per-automation scopes, not your personal account | Blast radius: an automation acting as *you* means revoking it breaks you, and its writes are yours | Any client or shared automation | A throwaway personal digest (proportionality) |
| 5 | Separate privilege: the content-reading model holds no write tools or secrets; deterministic code delivers | Breaks the lethal trifecta by construction — untrusted content and exfiltration capability live in different processes | Any agent that reads untrusted web content | Fully local, no-egress, no-secret scripts |
| 6 | Make every write idempotent; checkpoint judgment outputs and reuse on resume | Everything eventually runs twice (redelivery, cron overlap, post-timeout retry); LLM stages are non-idempotent | Every unattended pipeline | — |
| 7 | Classify failures TRANSIENT (retry+jitter, capped) vs PERMANENT (skip/alert, never retry) | Retrying a 403 gets you blocked; retrying a schema violation burns tokens on an input that can't conform | Every fallible stage | — |
| 8 | Honor robots.txt/ToS/TDM signals and identify truthfully — treat clean access as a moat | Cloudflare blocks mixed-use crawlers by default (Sept 15); EU makes TDM opt-outs copyright-relevant; courts read evasion as bad faith | All scraping | — |
| 9 | Prefer the front door: RSS/API/sitemap before rendering; conditional requests before blind re-fetch | >50% of AI crawl traffic is wasteful re-fetches; front-door access is cheaper, cleaner, and survives the new regime | Every fetch | A source with genuinely no front door and a real licensing basis |
| 10 | Extract against a uniform schema (structured outputs), never regex against HTML | Grammar-constrained JSON eliminates almost-JSON failures; one schema keeps dedup/judge/synth source-agnostic | Every extraction | Feeds/APIs already structured (parse, don't extract) |
| 11 | Enforce the citation contract in deterministic code: every claim cites a kept source, or the brief doesn't ship | The whole point of unattended operation is nobody checks — so code checks. Primary hallucination containment | Any unreviewed summarizer | — |
| 12 | Gate every prompt/model change on a golden set at threshold | Model drift is invisible per-output and global; only a fixed reference catches it before readers do | Every change to an unattended pipeline | — |
| 13 | Automate the reversible, gate the irreversible, measure everything | Blanket human-in-the-loop is rubber-stamping (approval fatigue); targeted HITL on rare irreversible actions actually works | Every autonomy decision | — |

---

## Block 3 capstone recap — how weeks 6, 7, 8 compose

Block 3 made you technically elite across three surfaces, and Week 8 is where they compose into one production practice:

- **Week 6 (context engineering, advanced RAG)** gave you the retrieval and context discipline that the summarizer's synthesis stage silently assumes — grounding the brief in kept items *is* context engineering, and the schemas-not-regex extraction is the same discipline one layer upstream.
- **Week 7 (voice agents → WA chatbot)** gave you the latency-sensitive, streaming deployment surface and the delivery channels (WhatsApp/chat) that Week 8's brief can ship into. A monitored daily brief delivered over the Week 7 WA channel is a single product.
- **Week 8 (unattended automation)** is the integration layer: it takes retrieval-grade synthesis (W6) and multi-channel delivery (W7) and makes them run unwatched, reliably, on a schedule — the thing a client actually pays a retainer for.

The Block 3 capstone thesis: *elite technique is table stakes; the differentiator is shipping it as something that runs without you and doesn't break silently.* That's the whole block, and Week 8 is its proof.

---

## 15 quiz questions

**Q1 (MCQ).** You're automating: "nightly, pull yesterday's Stripe transactions, flag anomalies vs a 90-day baseline, Slack a summary." Which runtime lane fits best and why?
- A) Free-roaming agent, for flexibility
- B) Visual workflow platform with an LLM island for the anomaly judgment
- C) Pure deterministic script, no LLM anywhere
- D) Claude Code Routines, because it's newest

**Q2 (short answer).** State the determinism-vs-judgment test in one sentence, and explain why it's asked per *step* rather than per *project*.

**Q3 (MCQ).** Claude Code Routines run with which default network posture?
- A) Full internet access
- B) No network access at all
- C) An allowlist ("Trusted") — package registries and common dev domains, everything else `403`
- D) Whatever the prompt requests

**Q4 (short answer).** A webhook sender POSTs to your handler, times out at 10 seconds, and redelivers. Your handler runs the agent inline for 90 seconds. Describe the failure and the two defenses (one from Tuesday's wiring patterns, one from idempotency).

**Q5 (MCQ).** Under the MCP 2026-07-28 release candidate, which is TRUE?
- A) It removes the Tasks feature entirely
- B) It makes the protocol stateless — no handshake, no session id, any request can hit any instance
- C) It's already the current stable spec as of this lesson
- D) It breaks all 2025-11-25 servers on day one

**Q6 (short answer).** Why is the client-credentials (M2M) OAuth flow the correct shape for a scheduled automation, and what identity should the token represent?

**Q7 (MCQ).** Starting September 15, 2026, Cloudflare's default settings will:
- A) Charge every crawler a flat fee
- B) Block all crawlers on all pages
- C) Block mixed-use AI crawlers by default on pages that host ads
- D) Require a login for all scraping

**Q8 (short answer).** hiQ v. LinkedIn is cited as "scraping public data is legal." Explain what the case actually held and what it did *not* protect against — the part the memes ignore.

**Q9 (code completion).** Complete the failure classification: an HTTP `429` is `______` (retry with backoff); an HTTP `403` from a source's block page is `______` (skip source, alert, don't retry); a schema-validation failure on model output is `______`.

**Q10 (MCQ).** Why must you checkpoint LLM-stage *outputs* and reuse them on resume, rather than re-running the stage?
- A) To save disk space
- B) Because LLM stages are non-idempotent — re-running changes the output and re-pays
- C) Because the spec requires it
- D) Because retries are always faster

**Q11 (short answer).** Name the primary (deterministic) hallucination-containment check for the summarizer's output, and the one class of hallucination it does NOT catch. What second check covers that class?

**Q12 (MCQ).** Which is the strongest defense against *model drift* (a new default model silently changing your judge/synthesizer)?
- A) A better prompt
- B) A golden-set regression that gates every model change at threshold
- C) A higher temperature
- D) More retries

**Q13 (short answer).** Why is "the run finished green" not evidence that the task succeeded, per the Routines docs — and what actually measures task-level success?

**Q14 (short answer).** State the course's autonomy rule for unattended agents in one sentence, and apply it: for a daily brief to twelve people vs a brief published under a client's brand to thousands, where does the human belong in each?

**Q15 (MCQ).** The current Anthropic tokenizer runs ~30% heavier than the 2025 generation. The operational consequence for your cost budgets is:
- A) Nothing — tokens are tokens
- B) Budgets ported from older intuition *undercount*, so measure real tokens from checkpoints
- C) You should switch to word-count budgeting
- D) It only affects output tokens

---

## Answers

**A1 — B.** The anomaly judgment is genuine judgment (can't pre-write "correct"); everything else (pull, baseline math, Slack post) is deterministic. Workflow-with-an-island fits. A over-agents a mostly-deterministic task; C can't do the anomaly judgment well; D fetishizes novelty (and Routines' constraints may not fit Stripe/Slack access cleanly).

**A2.** *Can I write down, in advance, exactly what correct behavior is for this step?* Yes → deterministic (code/node); no → judgment (LLM). It's per-step because real automations are mostly deterministic with a few judgment islands — asking per-project forces an all-or-nothing choice that over-agents deterministic work or under-serves judgment work.

**A3 — C.** The Default environment uses "Trusted" network access: an allowlist of package registries and common dev domains; other hosts fail with `403` / `x-deny-reason: host_not_allowed`. Least privilege as the default.

**A4.** The sender's retry spawns a *second* concurrent agent run (and a third, a fourth) while the first still runs — duplicated work and duplicated writes. Defense 1 (Tuesday Pattern A): the handler acks fast and enqueues, running the agent out-of-band so the sender never times out. Defense 2 (idempotency): dedup on the delivery/event ID so even concurrent runs can't double-send.

**A5 — B.** The RC's headline is a stateless core (SEP-2575 removes the handshake, SEP-2567 deletes session ids); capabilities travel in `_meta` per request. It's an RC until it publishes July 28 (not current stable), it moves Tasks to an *extension* (doesn't remove it), and it removes no features on day one (three deprecated with replacements).

**A6.** A scheduled automation isn't "you at midnight" — it's a service principal with its own identity, scopes, and audit trail. Client credentials authenticate the *application* (client ID + secret) and issue a token representing the application, not a person — the correct "no human in the loop" shape.

**A7 — C.** From September 15, 2026, default settings block "mixed-use" AI crawlers on ad-carrying pages, applying to new customers, new sites, and existing free-tier customers. Search-classified crawlers stay allowed by default.

**A8.** The Ninth Circuit held scraping *publicly available* data likely isn't a CFAA violation (public pages aren't "protected" in the anti-hacking sense). But the case *settled* with hiQ paying damages and destroying data after LinkedIn won on *contract* and unfair-competition theories. So: CFAA is weak against public-data scraping, but breach of ToS you assented to is live and winnable — public does not mean permissionless.

**A9.** `429` = **TRANSIENT**; `403` block page = **PERMANENT**; schema-validation failure = **PERMANENT**.

**A10 — B.** LLM stages produce different output for the same input, so re-running a stage on resume gives a *different* brief and pays for it twice. Checkpoint the output and reuse it.

**A11.** Primary: every claim in the brief must cite a URL present in the kept-items set; the validator rejects any that doesn't (catches fabricated sources with certainty, in deterministic code). It does NOT catch *misrepresentation* — a claim that cites a real kept source but distorts what it says. Second check: a validated cheap faithfulness judge scoring each cited claim against its source.

**A12 — B.** Model drift is invisible in any single output and affects every run globally; only a fixed reference set, re-run on every model change and gated at threshold, catches it before your readers do.

**A13.** A green run means the session started and exited without an *infrastructure* error — blocked network calls, missing connector tools, and task-level failures all surface only inside the transcript, not in the status. Task-level success is measured by evals (golden set, rubric, faithfulness), not by exit status.

**A14.** *Automate the reversible, gate the irreversible, measure everything* — oversight proportional to blast radius. Twelve-person brief: reversible, low-stakes, well-evaluated → human-on-the-loop (ships autonomously, you monitor and can kill it). Brand-published to thousands: the irreversible/high-blast-radius gate snaps on → human-in-the-loop review before send.

**A15 — B.** Heavier tokenization means the same content costs more tokens than older intuition assumed, so ported budgets undercount. Measure real token counts from stage checkpoints rather than estimating from word counts.

---

## 25 flashcards

1. **Q:** The determinism-vs-judgment test? **A:** Can I write down correct behavior in advance? Yes → deterministic (code/node); no → judgment (LLM). Asked per step.
2. **Q:** Who owns the schedule in an unattended agent? **A:** Infrastructure, never the model. Agents decide *inside* runs; they never decide *whether* runs happen.
3. **Q:** Three Claude Code scheduling tiers? **A:** `/loop` (in-session, session-scoped, 7-day expiry); Desktop scheduled tasks (local, durable); Routines (Anthropic cloud, machine-off, no permission prompts).
4. **Q:** Routines' default network posture? **A:** "Trusted" allowlist — package registries + common dev domains; other hosts `403`. Least privilege by default.
5. **Q:** Why do Routines wrap `/fire` payloads in `<routine-fire-payload>`? **A:** Labels trigger input as untrusted data; the agent won't follow instructions inside unless the saved prompt opts in. Prompt-injection mitigation baked into the trigger.
6. **Q:** Sonnet 5 pricing and its expiry? **A:** $2/$10 per Mtok intro through 2026-08-31, then $3/$15. Date-stamp every cost table.
7. **Q:** Client-credentials (M2M) OAuth flow — what does the token represent? **A:** The application (service principal), not a person. The correct shape for headless/scheduled automation.
8. **Q:** CIMD? **A:** Client ID Metadata Documents — a client identifies via an HTTPS URL it controls; default identity mechanism replacing Dynamic Client Registration in MCP 2025-11-25.
9. **Q:** The MCP 2026-07-28 headline change? **A:** Stateless core — no `initialize` handshake, no `Mcp-Session-Id`; any request can hit any server instance. Makes serverless MCP natural.
10. **Q:** Idempotency, one sentence? **A:** Every write must be safe to perform twice, because in an unattended system everything eventually runs twice.
11. **Q:** TRANSIENT vs PERMANENT? **A:** TRANSIENT (5xx/timeout/429) → retry with capped backoff+jitter. PERMANENT (4xx/auth/schema/ToS) → skip, alert, never retry the same input.
12. **Q:** Cloudflare's Sept 15, 2026 default? **A:** Block mixed-use AI crawlers on ad-carrying pages by default (new customers, new sites, existing free tier). Search/Agent/Training taxonomy.
13. **Q:** Share of crawler traffic that's AI, and how much is waste? **A:** AI = 52% of crawler requests (June 2026, up from 22%); >50% re-fetches unchanged pages.
14. **Q:** What did hiQ v. LinkedIn actually establish? **A:** Scraping public data likely isn't a CFAA violation — but it settled on *contract* grounds. Public ≠ permissionless.
15. **Q:** robots.txt legal status? **A:** Not binding/contract, but evidence of good faith (honoring) or willfulness (ignoring); in the EU a TDM opt-out in robots.txt can be copyright-relevant.
16. **Q:** The 2026 scraping stack, one line each? **A:** Playwright (open-source fetch+render); Browserbase+Stagehand (managed browsers for agents); Firecrawl (URL→clean structured data + change-tracking).
17. **Q:** "Schemas, not regex"? **A:** Extract every source into one uniform Item schema via structured outputs; grammar-constrained JSON eliminates almost-JSON failures and keeps downstream source-agnostic.
18. **Q:** Structured outputs caveat with citations? **A:** Strict JSON schema conflicts with Claude's interleaved citation blocks (400). Synthesize prose-with-citations, then validate the contract separately.
19. **Q:** Spine-and-islands architecture? **A:** Deterministic pipeline (fetch/extract/dedup/deliver) with LLM judgment islands (relevance, synthesis) between checkpoints.
20. **Q:** Why checkpoint judgment outputs and reuse on resume? **A:** LLM stages are non-idempotent — re-running changes output and re-pays. Reuse = correctness + cost.
21. **Q:** Primary hallucination containment for the summarizer? **A:** Deterministic contract: every claim cites a URL in the kept set, or the brief doesn't ship. Faithfulness judge catches misrepresentation of real sources.
22. **Q:** The golden set's job? **A:** Regression gate — re-run on every prompt/model change; below threshold blocks the ship. The only defense against invisible, global model drift.
23. **Q:** Why is a heartbeat's *absence* an alert? **A:** The most common unattended failure is the run that silently stopped (cron died, token expired, machine slept) — no output means no error to see; only missing-heartbeat catches it.
24. **Q:** The autonomy rule for unattended agents? **A:** Automate the reversible, gate the irreversible, measure everything — oversight proportional to blast radius (HITL for irreversible, HOTL for reversible).
25. **Q:** Why is "the run went green" not success? **A:** Green = session exited without infrastructure error; task-level success (right output) is measured only by evals, per Routines' own docs.

---

## Where you'd still lose points (reviewer lens)

- **Seibel:** you can recite the thirteen moves and still not have shipped a brief to yourself. The quiz tests knowledge; the week tests whether one real brief landed in your inbox and taught you which two of the eight stages actually needed armor. If Saturday's build is still a design doc, you skipped the week.
- **Hamel:** every eval answer here assumes a golden set built from imagined failures. The real one comes from a week of shadow runs and error analysis. If you can't yet name three failure categories from *your own* outputs, your golden set is a hypothesis wearing a gate's clothing.
- **A publisher-side reviewer:** the scraping answers stay a shade too comfortable with "route around the site politely." In the Pay-Per-Use world, for a handful of high-value sources the durable move may be to *license*, not scrape — and the strongest version of your practice knows when.

## Further reading

- Re-read this week's Must-reads before the live session, especially the Claude Code Routines docs and the Cloudflare "Your site, your rules" post — both fast-moving.
- The companion code-lab `code-lab/06-hybrid-agent/` is the week made runnable; if you did nothing else, run it in shadow mode.

_last_verified: 2026-07-17_
