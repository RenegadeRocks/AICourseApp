---
type: lesson
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 5
day_name: fri
session_slug: build-hybrid-agent-scraper-summarizer
date_due: 2026-07-10
tags: [reliability, evals, golden-set, regression, canary, drift, hallucination-containment, kill-switch, incident-postmortem, human-in-the-loop, human-on-the-loop, unattended-agents]
sources:
  - hamel-evals-error-analysis-2026
  - hamel-shreya-evals-faq-2026
  - anthropic-building-effective-agents-2024-12
  - owasp-agentic-top10-2026
  - mit-tr-humans-in-loop-illusion-2026-04
  - nist-ai-agent-standards-2026-02
  - ai-agent-adoption-2026-stats
  - eu-ai-act-tdm-2026
  - refresh-2026-07-master-report
last_verified: 2026-07-17
word_count_target: 5300
---

# Reliability engineering for unattended agents — the discipline that makes it safe to walk away

## Why this matters

Tomorrow you ship an agent whose output nobody reviews before it reaches a reader. That single fact is the whole reason this lesson exists and the whole reason 88% of agent pilots never reach production — with evaluation gaps named the top blocker by 64% of leaders and non-deterministic output the number-one production-readiness barrier by 70%.[^7] The pipeline you designed Thursday can be architecturally perfect and still be unshippable, because "perfect architecture" says nothing about whether the *output* is good, stays good, and fails safe when it isn't.

Reliability engineering for unattended agents is the set of practices that let you sleep: a golden-set regression that gates every change, canary runs that catch trouble on a small blast radius, drift metrics that make silent degradation loud, hallucination containment for the case where nobody's checking, a kill switch you can actually reach, and a clear-eyed answer to the question the whole field is fighting over — *when do you refuse to remove the human at all?* By tonight you'll have the eval harness spec that turns Thursday's architecture into something you'd put your name on.

## Prerequisites

- [[04-thu-hybrid-agent-design-pipeline-plus-judgment]] — the staged pipeline, contracts, and drift detectors this lesson gates and monitors.
- [[06-sat-rag-evaluation]] — the Block 2 eval lesson: eval decomposition, LLM-as-judge and its biases, Hamel's eval-driven-development discipline, binary-over-scores. This lesson applies that discipline to *unattended* operation; the eval-threshold convention lives there and is wikilinked, not re-taught.
- [[02-tue-when-ai-fits-a-problem]] — when a human belongs in the loop is a scoping decision, revisited here at the action level.

## Layer 1 — The golden set: your regression gate

The single highest-leverage reliability practice is a **golden set**: a fixed collection of representative inputs with known-good expected outputs (or known-good acceptance criteria), that you re-run on *every* change to prompt, model, schema, or source-handling — before the change ships. This is Hamel Husain and Shreya Shankar's core discipline, ported to automation: **your evaluation strategy should emerge from observed failure patterns via error analysis, not from predetermined categories, and binary pass/fail beats arbitrary quality scores.**[^1][^2]

For the scraper→summarizer, the golden set is concrete:

- **Relevance-judge golden set**: ~30–50 real items you've hand-labeled keep/drop. The judge must reproduce your labels above a threshold you set (the eval-threshold discipline from [[06-sat-rag-evaluation]] — pick it deliberately, e.g. ≥90% agreement, and treat regressions below it as ship-blockers).
- **Synthesis golden set**: ~10–15 sets of kept-items with a rubric per set — every claim cited to a provided source, no fabricated sources, required sections present, length in bounds, no duplicated items. Binary per criterion, per Hamel.[^1]
- **End-to-end golden set**: a few frozen full-source snapshots (raw bytes checkpointed from real runs) that must produce an acceptable brief start to finish. This catches integration failures the stage-level sets miss.

The rule that makes it a *gate* and not a dashboard: **no prompt or model change ships until the golden set passes at threshold.** This is the only defense against model drift (Thursday's most dangerous failure), because model drift is invisible in a single output and only shows against a fixed reference. When Anthropic ships a new default mid-quarter, the golden set is what stands between the upgrade and your readers noticing before you do.

Validate your judge, too. If you use LLM-as-judge to score synthesis quality, you must confirm the judge agrees with *you* on a labeled sample before trusting it — Hamel's "validate your LLM judges" step, non-negotiable, because an unvalidated judge is just a second unreviewed model watching the first.[^1][^2]

## Layer 2 — Canary runs and staged rollout

Even a passing golden set can't cover everything (real inputs surprise you). So you stage exposure. **Canary runs**: before a changed pipeline delivers to real readers, run it in shadow — produce the brief, but deliver it only to *you*, alongside the current production brief, for a few days. Diff them. A change that passes the golden set but produces visibly worse briefs on live data gets caught on a blast radius of one (you), not your whole readership.

Staged rollout for automations, in order of increasing blast radius:

1. **Shadow** — new pipeline runs, output goes only to you, production unchanged.
2. **Canary** — new pipeline delivers to a small friendly subset (you + a couple of tolerant users).
3. **Full** — after N clean days, promote.

This is boring deployment discipline from software engineering, and it is exactly what agent teams skip because "it's just a prompt change." A prompt change *is* a deploy — arguably a riskier one than a code change, because its effects are diffuse and its blast radius is every output. Treat it like one.

## Layer 3 — Drift metrics and heartbeats: making silence loud

Thursday built the drift *detectors*; reliability engineering turns them into *monitored metrics with alerts*. The minimum instrumentation for a brief nobody reviews:

- **Heartbeat**: every run writes "I ran, here's when, here's the outcome." *Absence* of a heartbeat is itself an alert — the most common unattended failure is the run that silently stopped happening (cron died, token expired, machine slept), and only a heartbeat's absence catches "nothing happened." A brief that doesn't arrive is a failure you must be paged about, not one you notice a week later.
- **Volume metrics**: items per source per run, tracked over time; zero-from-a-usually-productive-source alerts (layout drift).
- **Keep-rate metrics**: relevance-judge keep-rate per source; sudden shifts flag content or model drift.
- **Cost metrics**: tokens and dollars per run, with both a per-run ceiling (Thursday) *and* a rolling weekly trend — because slow drift inflates cost across runs without any single run breaching its cap (Chip Huyen's point from Thursday, now operationalized).
- **Contract-failure rate**: how often the brief validator rejects synthesis output. A rising rate is an early warning that a source, the model, or a prompt is degrading before readers see it.

You don't need a full observability platform for one automation — a structured `run.log` plus a script that reads it and alerts is enough. But know the standard exists: OpenTelemetry's GenAI semantic conventions ([[04-thu-hybrid-agent-design-pipeline-plus-judgment]]) are where you graduate when you're watching more than one agent. The alerting channel matters as much as the metric: an alert that lands in a Slack channel nobody reads is not an alert. Route failure alerts somewhere you actually look — the same discipline that makes a smoke detector useful is a battery you can't ignore.

## Layer 4 — Hallucination containment when nobody reviews

The defining risk of a summarizer nobody proofreads is a confident, fluent, *wrong* brief. Containment is layered, cheapest-first:

1. **Ground everything in retrieved content.** The synthesis prompt gets only the kept items and is instructed to summarize *those* — not to add knowledge, context, or "helpful" background from its training. A summarizer that stays inside its provided sources can't hallucinate a source it wasn't given.
2. **Enforce citation-to-source as a deterministic contract** (Thursday's primary check): every claim cites a URL in the kept set; the validator rejects any that doesn't. This is code, not judgment, and it catches fabricated sources with certainty.
3. **Add a faithfulness check for the claims that *do* cite.** Citation-to-source catches invented URLs but not misrepresentation — a claim that cites a real kept source but distorts what it says. A second, cheap LLM-as-judge pass (validated per Layer 1) scores each claim against its cited source for faithfulness; below threshold, flag or drop. This is the check Thursday's reflection question pointed at.
4. **Prefer extraction and quotation over paraphrase for facts that matter.** Numbers, dates, names — pull them structurally where you can (structured outputs) rather than letting the model restate them, because restatement is where numeric hallucination lives.
5. **Label uncertainty in the output.** When the pipeline is unsure (low faithfulness, thin sources, a degraded run), the brief should *say so* — "1 source unavailable today" — rather than paper over it with confident prose. An honest brief that admits gaps is more trustworthy than a smooth one that hides them.

The uncomfortable truth, and this course states it plainly: **no containment stack makes an unreviewed summarizer perfectly safe.** It makes it *safe enough for the stakes* — and the stakes decision (Layer 6) is where judgment can't be automated away.

## Layer 5 — Kill switches and incident postmortems

**Kill switch.** Every unattended automation needs a way to stop it *now*, reachable by whoever's on call, that doesn't require redeploying. Minimum viable: an environment flag the pipeline checks at the top of every run (`PIPELINE_ENABLED=false` → log and exit) — the same shape as Claude Code's `CLAUDE_CODE_DISABLE_CRON=1`.[^5] Better: a documented one-command disable and a delivery-channel pause, so a bad brief can be stopped mid-flight before it fans out. The kill switch is worthless if nobody knows it exists; it goes in the README, and its location is the first line of the incident runbook.

**Incident postmortems.** When an unattended agent fails — ships a wrong brief, stops running, blows a budget, gets a source blocked — you run a blameless postmortem: what happened, what the pipeline saw at each checkpoint (this is why Thursday's checkpoints retain raw bytes), why the guards didn't catch it, and what golden-set case or metric would have. **The output of every postmortem is a new golden-set entry or a new alert.** That's the flywheel: production failures become regression tests, so the same failure can't ship twice. NIST's AI Agent Standards Initiative is codifying exactly this expectation — action logging and auditability so that "what was the agent allowed to do, what context did it receive, what did it decide, who approved or overrode it" is answerable after the fact.[^6]

## Layer 6 — The live controversy: how much autonomy, and when to keep the human

This is the debate the whole field is having in 2026, and it has real, named camps.

**Position A — "human-in-the-loop is increasingly an illusion; invest elsewhere."** MIT Technology Review's April 2026 piece argues the comfort of "a human in the loop" is a distraction: overseers can't verify what a black-box model is actually reasoning about, so approval becomes rubber-stamping.[^3] The operational echo, widely reported: HITL controls fail under approval fatigue, auto-approve habits, and "YOLO mode" bypasses — a human who approves 200 agent actions a day approves the 201st, the bad one, without reading it. On this view, effort spent on approval gates is better spent on evals, containment, and interpretability.

**Position B — graduated autonomy, oversight proportional to blast radius.** The emerging consensus (reflected in Singapore's graduated-autonomy framework and OWASP's "least-agency" principle): match oversight intensity to reversibility and impact.[^4] **Human-in-the-loop (HITL)** — a human approves *before* execution — for high-stakes, irreversible actions (money out, legal commitments, publishing under a real brand at scale). **Human-on-the-loop (HOTL)** — the agent acts, a human monitors and can intervene after — for medium-stakes reversible actions where speed matters. **Fully autonomous** only for low-stakes, reversible, well-evaluated actions. The EU AI Act makes a version of this legally binding for high-risk systems from August 2, 2026 (human-oversight requirements enforceable), and NIST is building the identity/logging/containment standards that make HOTL auditable.[^6][^8]

**Where this course lands** (opinion, labeled): both positions are correct about different things, and the synthesis is a rule you can apply Saturday. Position A is right that HITL as a *blanket* control is theater — approving every action doesn't scale and doesn't work. Position B is right that HITL *targeted at irreversible, high-blast-radius actions* is exactly where a human belongs, precisely because those are rare enough to actually review. So: **automate the reversible, gate the irreversible, and measure everything.** For the scraper→summarizer specifically — a reversible, low-stakes, well-evaluated daily brief to a small audience — HOTL is proportionate: it ships autonomously, you monitor via heartbeat and metrics, and you can kill it. The moment it publishes under a client's brand to thousands, or drives a decision with money attached, the irreversible-action gate snaps on and a human reviews before send. The stakes set the oversight; the oversight is never one-size-fits-all; and "how much autonomy" is answered per action, not per agent — the same move as Monday's determinism-per-step.

## Experiment — build the eval harness and break the pipeline

Direct Claude Code (60 min; this is the reliability layer of Saturday's build):

1. **Build the relevance golden set.** *"From these 40 real items [paste/point], help me hand-label keep/drop for my niche, then write a harness that runs the relevance judge against these labels and reports agreement %. Set a ship-blocking threshold and show what a failing run looks like."*
2. **Build the synthesis rubric + validator.** *"Write a binary rubric (per Hamel: pass/fail per criterion) for brief quality — every claim cited to a provided source, no fabricated sources, required sections, length bounds, no duplicated items — and a validator that scores a brief against it. Then add a faithfulness check: for each cited claim, a cheap LLM-as-judge pass scoring whether the claim matches its source. Validate the judge against 10 of my own labels first."*
3. **Add heartbeat + drift alerts.** *"Add to the run log: heartbeat, per-source volume, keep-rate, per-run cost, contract-failure rate. Write a monitor that reads the log and alerts on: no heartbeat (missed run), zero items from a usually-productive source, keep-rate shift, cost anomaly (per-run and rolling-weekly). Route alerts to a channel I actually check."*
4. **Chaos-test it.** *"Now break things and show each guard firing: (a) source 2 returns empty (layout drift) → which alert? (b) the cron didn't run at all → how does absence-of-heartbeat catch it? (c) synthesis fabricates a source URL → does the validator reject and alert? (d) a cited claim misrepresents its source → does the faithfulness check catch it? (e) a runaway input pushes cost past ceiling → controlled stop?"* Every one of these must produce a specific, correct alert. The ones that don't are your Saturday punch list.
5. **Write the kill switch and one postmortem template.** *"Add a `PIPELINE_ENABLED` kill switch checked at run start, document it in the README as line one of the incident runbook, and give me a blameless postmortem template whose output is always a new golden-set entry or a new alert."*

## Common mistakes experts see

- **No golden set, "we'll eyeball it."** Eyeballing doesn't scale past a few runs and catches zero silent drift. The gate is the golden set or there is no gate.
- **Shipping model/prompt changes without regression.** Model drift is invisible per-output and global in effect; only a fixed reference catches it.
- **Unvalidated LLM judge.** Trusting a judge you never checked against your own labels is adding a second unreviewed model, not adding oversight.
- **No heartbeat.** The silent-stopped-run is the most common unattended failure and the only one you can't see in the output — because there is no output.
- **Alerts nobody reads.** An alert in a dead channel is a log line. Route to where you look, and test that it actually pages.
- **Blanket human-in-the-loop.** Approving every action produces approval fatigue and rubber-stamping;[^3] reserve HITL for irreversible, high-blast-radius actions.
- **No kill switch, or one nobody can find.** When it's shipping bad briefs at 3 a.m., "redeploy to stop it" is not a plan.
- **Postmortems that don't produce regressions.** A postmortem whose output isn't a new golden case or alert is a feelings meeting; the same failure will ship again.

## Reflection questions

1. Your golden set passes at 92% (threshold 90%) after a model upgrade, but the two failing cases are your two most important sources. Does it ship? Defend a rule that isn't "it depends."
2. HITL fails via approval fatigue; full autonomy fails via unreviewed hallucination. For your specific brief and audience, where exactly is the line between an action you'd let ship autonomously and one you'd gate — and what makes an action cross it?
3. A heartbeat catches the run that didn't happen. What catches the run that happened, produced a brief, delivered it, and was *entirely wrong* — with no error anywhere? Name the specific guard and its blind spot.
4. You validate your faithfulness judge against 10 labels and it agrees 8/10. Do you trust it? What do you do about the 2 — and how many labels would you need before "80% judge agreement" is enough to gate on?
5. The MIT Tech Review "illusion" argument says oversight of black boxes is theater. Grant it fully for a moment: if a human genuinely can't verify the model's reasoning, what's left that's *worth* doing — and is any of it in your Saturday build?
6. Write the first three lines of your incident runbook for "the brief that shipped was wrong and it's already in readers' inboxes." What's line one? (If it isn't "here's the kill switch," rewrite it.)

## My take (reviewer lens)

**Hamel Husain** would approve of the golden-set spine and then immediately catch the lesson skipping the step he considers foundational: **error analysis comes before the golden set, not after.** You don't know what to put in the golden set until you've read a pile of real outputs and let the failure categories *emerge* — "error analysis is all you need," and a golden set assembled from imagined failures tests the wrong things. The lesson gestures at this ("emerge from observed failure patterns") but sequences it backward for a build week where you have no production outputs yet. The honest fix: your *first* golden set is a hypothesis; the real one is assembled after week one of shadow runs, from the failures you actually observe. Say that.

**Michael Seibel** would call the whole lesson a reason people never ship. Golden sets, canaries, faithfulness judges, postmortem templates — for a daily digest to twelve people. His line: the fastest way to learn what reliability your agent needs is to ship it to yourself, read the brief every morning for two weeks, and *notice what's wrong*. You'll build the golden set from real annoyance, not speculative rubrics, and you'll build only the guards that failures earned. He's right about sequence, and the lesson concedes it: **week one is you-as-the-eval-harness; the automated harness is what you build once your own reading has told you what to check.** The machinery is the destination.

**A safety-minded reviewer** (the OWASP/NIST position) would push the opposite way: the lesson's "automate the reversible, gate the irreversible" rule is correct but under-specifies *reversibility* — a daily brief feels reversible until it's an archived, indexed, shared artifact that shaped a decision nobody can un-make. "Reversible" is doing heavy, unexamined work. Fair. The sharper formulation: an action is reversible only if you can both *detect* the error and *undo its consequences* before they compound — and for a published summary, the consequence (a reader acted on a wrong claim) is often neither detectable nor undoable. Which is exactly why Layers 4 and 1 exist, and exactly why the irreversible-action gate snaps on the moment the audience or the stakes grow.

## Further reading

**Must-read**

- Hamel Husain (Lenny's Newsletter) — "Evals, error analysis, and better prompts."[^1]
- Hamel Husain & Shreya Shankar — "LLM Evals: Everything You Need to Know" (the FAQ).[^2]
- [[06-sat-rag-evaluation]] — the course's eval home; re-read Layers 3–4 before Saturday.

**Recommended**

- OWASP — Top 10 for Agentic Applications 2026 (least-agency; observability as mandatory control).[^4]
- MIT Technology Review — "Why having 'humans in the loop' in an AI war is an illusion" (April 2026) — read as the strongest steelman of Position A.[^3]
- NIST — AI Agent Standards Initiative (identity, logging, containment).[^6]

**Optional**

- Digital Applied — "AI Agent Adoption 2026" (the 88%/64%/70% failure decomposition).[^7]
- Anthropic — "Building Effective Agents" (the simplicity discipline that underwrites all of this).[^9]

## Citations

[^1]: Hamel Husain. "Evals, error analysis, and better prompts: A systematic approach to improving your AI products." Lenny's Newsletter. https://www.lennysnewsletter.com/p/evals-error-analysis-and-better-prompts — error analysis as the foundation; binary pass/fail over quality scores; validate your LLM judges. Corroborated by Product Growth "How to Master AI Evals" https://www.aakashg.com/ai-evals-masterclass-with-hamel-shreya/ (search-verified 2026-07-17; direct fetch egress-blocked — liveness pass pending).

[^2]: Hamel Husain & Shreya Shankar. "LLM Evals: Everything You Need to Know." https://hamel.dev/blog/posts/evals-faq/ — "error analysis is all you need"; evaluation strategy emerges from observed failures, not predetermined categories; judge validation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: MIT Technology Review. "Why having 'humans in the loop' in an AI war is an illusion." https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/ — April 16, 2026; overseers cannot verify black-box reasoning, so oversight risks becoming rubber-stamping. Approval-fatigue / auto-approve / YOLO-bypass framing corroborated by Waxell "Human-in-the-Loop vs Human-on-the-Loop" https://waxell.ai/blog/human-in-the-loop-vs-human-on-the-loop-ai-agents (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: OWASP Gen AI Security Project. "OWASP Top 10 for Agentic Applications for 2026." https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ — least-agency; graduated autonomy; logging/observability as mandatory. Graduated-autonomy (HITL/HOTL/autonomous by reversibility) corroborated by Waxell (above) and ideaforge "Human-in-the-Loop AI Agents Autonomy Playbook" https://ideaforgestudios.com/2026/07/17/human-in-the-loop-ai-agents-autonomy-playbook/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Claude Code docs. "Run prompts on a schedule." https://code.claude.com/docs/en/scheduled-tasks — `CLAUDE_CODE_DISABLE_CRON=1` disables the scheduler entirely (kill-switch shape) (fetched live 2026-07-17).

[^6]: NIST. "Announcing the 'AI Agent Standards Initiative.'" https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure — Feb 17, 2026; agent identity/authorization, action logging/auditability, containment. Corroborated by WorkOS https://workos.com/blog/nist-ai-agent-standards-initiative-explained (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Digital Applied. "AI Agent Adoption 2026: 120+ Enterprise Data Points." https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points — 88% of pilots never reach production; 64% name evaluation/observability the top blocker; 70% name non-deterministic outputs the #1 production-readiness barrier. Corroborated by CIO.com https://www.cio.com/article/3850763/88-of-ai-pilots-fail-to-reach-production-but-thats-not-all-on-it.html (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). Survey-grade figures.

[^8]: EU AI Act. High-risk human-oversight obligations enforceable from August 2, 2026 — per artificialintelligenceact.eu implementation timeline and landscape delta §8 (URL-verified 2026-07-17). https://artificialintelligenceact.eu/implementation-timeline/ .

[^9]: Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents — Dec 19, 2024; simplicity and measurement as the underwriting discipline.

_last_verified: 2026-07-17_
