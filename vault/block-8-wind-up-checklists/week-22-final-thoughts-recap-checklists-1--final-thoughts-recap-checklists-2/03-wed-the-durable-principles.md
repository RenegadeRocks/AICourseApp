---
type: lesson
block: block-8-wind-up-checklists
week: week-22
session_slug: final-thoughts-recap-checklists-1
day_of_cycle: 3
day_name: wed
date_due: 2026-10-14
tags:
  - capstone
  - principles
  - first-principles
  - durability
sources:
  - willison-lethal-trifecta
  - anthropic-building-effective-agents
  - chip-huyen-ai-engineering
  - karpathy-agents-timeline
  - anthropic-pricing-2026
last_verified: 2026-07-17
---

# The durable principles: what outlasts the tools

## Why this matters (operator framing)

The July 2026 refresh of this course rewrote model names, prices, benchmarks,
tool comparisons, and API surfaces — and touched almost none of the reasoning.[^1]
That is the empirical proof of today's thesis: a small set of principles carried
the whole course, and they did not decay while the field molted. If you internalize
these, you can lose every tool you learned and rebuild the business, because you
will know what you are looking for. This lesson names the durable core, ties each
principle to where the course earned it, and then argues honestly about which
"best practices" are durable and which are fashion.

## Prerequisites

[[01-mon-the-whole-map|Monday's map]] and [[02-tue-the-master-build-checklist|Tuesday's checklist]]. Today extracts the invariants under both.

## How to tell a principle from a fashion

A useful test before we list anything. A principle is durable if it would still
be true under a 10× cheaper model, a different vendor, and a tool you have never
heard of. A fashion is a practice that is really an artifact of today's prices,
context limits, or platform rules. "Keep prompts short to save tokens" is a
fashion — it is downstream of pricing that changes monthly. "Control what the
model sees" is a principle — it is true at any price. Hold each item below up to
that test as you read.

## The durable core (14 principles)

**1. Decide whether AI fits before you build.** The most valuable skill in the
course is saying no to AI for a problem it does not suit. This is durable because
better models widen the fit envelope but never eliminate the judgment. →
[[block-0-basecamp/week-03-decoding-real-business-problems-with-ai-i--decoding-real-business-problems-with-ai-ii/02-tue-when-ai-fits-a-problem|when AI fits a problem]]

**2. Evidence over vibes.** Route every consequential decision through evidence
you could show someone. Validation, evals, and honest growth measurement are the
same instinct at different stages. → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/05-fri-polls-smoke-tests-evidence-ledger|the evidence ledger]]

**3. Compute margin under real COGS.** Always know your gross margin, computed on
current token prices and the current tokenizer. This principle is durable
precisely because the inputs are not. The refresh caught cost math that was 3×
off because prices moved; the discipline of recomputing is the durable part.[^2]
→ [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/05-fri-revenue-planning-and-unit-economics|unit economics]]

**4. Price on value, not cost.** Anchor to the value metric the customer feels,
not the tokens you spend. Cost sets your floor; value sets your price. →
[[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/02-tue-pricing-strategy-value-metric-anchoring-packaging|value-metric pricing]]

**5. Retention before growth.** Growth compounds only on top of retention;
retention compounds only on top of a product people would be upset to lose.
Pouring acquisition into a leaky product is the most common expensive mistake in
the course. → [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/05-fri-the-growth-system-and-honest-measurement|retention-first growth]]

**6. Loops beat funnels.** A funnel you refill by hand is labor; a loop that
feeds itself is an asset. Durable because it is a structural claim about
compounding, independent of any channel. → [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/03-wed-growth-loops-vs-funnels|loops vs funnels]]

**7. Control what the model sees.** Context engineering is the successor to prompt
engineering, and it is durable: no matter how large the window gets, deciding what
enters it is the lever. → [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/01-mon-context-engineering-the-successor-discipline|context engineering]]

**8. Eval-gate everything.** Define the pass bar before you build, then measure.
Anthropic's agent guidance and Hamel Husain's evals argument converge here: you
cannot improve what you cannot measure, and you cannot ship what you have not
measured.[^3] → [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|evaluation as a gate]]

**9. Simplicity first; earn complexity.** Start with the simplest thing that
could work (a single call, a workflow) and add agentic complexity only when it
measurably improves the outcome. This is Anthropic's explicit recommendation and
it survives every model generation.[^3] → [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/02-tue-agent-architectures|agent architectures]]

**10. Human-in-the-loop where the cost of error is high.** Automate the reversible
and the cheap; keep a human on the irreversible and the expensive. The line moves
as models improve, but the principle of drawing the line by cost-of-error does
not. → [[block-3-advanced-topics-voice/week-07-voice-agent-squad--voice-agent-extened-to-a-chatbot-on-wa/04-thu-voice-agent-trust-and-safety|trust and safety]]

**11. Assume the security posture, do not bolt it on.** Simon Willison's lethal
trifecta — an agent with access to private data, exposure to untrusted content,
and the ability to exfiltrate — is a durable threat model, not a passing CVE.[^4]
Any agent that reads email, web pages, or user input inherits it. →
[[block-0-basecamp/week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/03-wed-mcp-security|MCP security]]

**12. Reliability is engineering, not prompting.** The gap between a demo and a
system is retries, idempotency, monitoring, and graceful failure. No model
release closes it for you. → [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/05-fri-reliability-engineering-for-unattended-agents|reliability engineering]]

**13. Systematize into canonical homes.** Every price, procedure, and spec lives
in exactly one authoritative place and is referenced everywhere. This is what lets
a business scale past your personal memory, and it is the same discipline as an
SOP library and a clean codebase. → [[block-7-onboarding-tracking/week-20-sops-for-onbaording-delivery-growth--build-community-paid-inner-circle/01-mon-sops-the-operating-system-of-a-scaling-business|SOPs as an operating system]]

**14. Distribution is a first-class problem.** A great product with no
distribution loses to a mediocre one with a channel. Owned audience, community,
and a lead engine are durable assets because they survive product pivots. →
[[block-7-onboarding-tracking/week-20-sops-for-onbaording-delivery-growth--build-community-paid-inner-circle/04-thu-building-community-the-compounding-moat|community as a moat]]

Fourteen. If you can restate each in one sentence and name where the course
proved it, you own the course. The rest was scaffolding to teach these.

## The controversy: which "best practices" are durable, and which are fashion

This is where honest people disagree, and where naming positions matters more
than pretending there is consensus.

**Agency versus product as the better 2026 path.** One camp, loud on X and in
YC-adjacent circles, argues AI-native services agencies are the wealth wave of
the decade, with a market potential framed as far larger than SaaS, because
agencies monetize immediately and productize later.[^5] The counter-position:
services are a job with extra steps unless you systematize toward a product, and
the durable asset is the productized IP, not the client roster. My read: this is
partly a fashion. The durable principle underneath is **start where cash is
fastest, migrate toward where margin is highest** — services at 70–80% margin to
learn the problem, product at 90%+ once the workflow repeats.[^5] The "agency vs
product" framing is a false binary; the sequence is the real answer, and it is
taught across [[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/01-mon-from-build-to-package-the-productization-spectrum|the productization spectrum]] and [[block-7-onboarding-tracking/week-19-build-async-client-dashboard-or-project-tracking-for-agency--productizing-your-service-community-market-research/03-wed-productizing-your-service|productizing your service]].

**Which current practices age fastest.** Chip Huyen's framing of AI engineering
as a discipline distinct from model building is durable; the specific stack she
or anyone names is not.[^6] Karpathy has repeatedly cautioned against over-reading
the current agent hype curve — his public position is that useful agents are a
decade-long build-out, not a solved 2026 product, which means today's
agent-framework orthodoxy is more fashion than principle.[^7] Concretely: model
names, prices, context limits, specific tool comparisons, framework choice, and
prompt-golfing tricks age in months. Threat models, eval discipline, unit
economics, and retention math do not. When you cannot tell which category a
"best practice" is in, apply the test from the top of this lesson.

**Prompt engineering is dead / not dead.** A fashionable claim says context
engineering killed prompt engineering. The durable reading: the *label* changed,
the *skill* generalized. Wording still matters; it is now one input among many
you control. Do not throw out the prompting fundamentals from [[block-0-basecamp/week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding/01-mon-prompting-first-principles|prompting first principles]] because a newer word arrived.

## Worked example: classify your own habits

List ten things you currently do in your build process. For each, apply the
durability test: would it still be true under a 10× cheaper model from a vendor
you have not heard of? Sort into "principle" and "fashion." Then check: are you
defending any fashions as if they were principles? Those are the beliefs that
will cost you when the field moves.

**Pass bar:** at least seven of your ten habits map cleanly to one of the 14
principles above; any that do not are either a genuine addition worth writing
down, or a fashion you were mistaking for a rule.

## Common mistakes experts see

- **Defending a fashion as a principle.** "We always use framework X" is a
  fashion. "We eval before we ship" is a principle. Confusing them makes you
  rigid where you should be flexible.
- **Treating a threat model as a fixed patch.** The lethal trifecta is not a bug
  that got fixed; it is a permanent property of agents with the wrong access.
- **Dropping a principle because its example aged.** The Opus-pricing example
  will be wrong within a year; principle 3 will not.
- **Over-indexing on the newest word.** Every quarter ships a rebrand of an old
  idea. Learn the idea, not the word.
- **Assuming consensus where there is a live fight.** Agency-vs-product is not
  settled. Anyone who tells you it is, is selling something.

## Reflection questions

1. Which of the 14 could you not restate from memory? That is your weakest link.
2. Name one fashion you have been defending as a principle.
3. On agency-vs-product, where are you on the sequence, and is your cash-speed
   matched to your margin ambition?
4. Which principle does your current business most violate?
5. If every tool you use vanished tonight, which principle would let you rebuild
   fastest?

## My take (reviewer lens)

**Chip Huyen** would push on principle 9. Her nuance: "simplicity first" can
become an excuse to never build the harder system a problem genuinely needs. The
principle is not "stay simple," it is "add complexity only when measured need
justifies it" — which requires you to actually measure, not to hide behind
minimalism.

**Karpathy** would want the durability test itself stress-tested. His likely
objection: some "fashions" (a specific model's behavior) compound into deep
intuition that is genuinely valuable, so the binary undersells accumulated
tool-specific taste. Fair — the test sorts *rules*, not *intuition*.

**Willison** would insist principle 11 is stated too gently. In his framing the
lethal trifecta is not a risk to manage but a configuration to avoid: if all
three legs are present, you have already lost, and the only durable fix is to
remove a leg. Take his version, not the softer one.

## Further reading

- **Must-read:** the July 2026 refresh master report in [[00-program/_refresh-2026-07-master-report|the program folder]] — the empirical case that skeleton survives and skin decays.
- **Recommended:** Simon Willison, "The lethal trifecta" — the durable agent
  threat model, stated plainly.[^4]
- **Optional:** Chip Huyen, *AI Engineering* (O'Reilly, 2024) — the discipline
  framing that outlasts any stack.[^6]

## Citations

[^1]: AI Pro-level Course, "July 2026 Content Refresh — Master Findings Report," internal, 2026-07-17 — frameworks and reasoning graded A-range while model names, prices, and tool features decayed; see [[00-program/_refresh-2026-07-master-report|the master report]].
[^2]: Anthropic, "Pricing," platform.claude.com/docs/en/about-claude/pricing — current per-Mtok rates and the updated tokenizer; the refresh caught prior cost math ~3× off after prices moved. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^3]: Anthropic, "Building effective agents," anthropic.com/research/building-effective-agents, Dec 2024 — start simple, add agentic complexity only when it measurably improves outcomes; measure workflows.
[^4]: Simon Willison, "The lethal trifecta for AI agents," simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — private data access + untrusted content + exfiltration ability; remove a leg to be safe.
[^5]: Y Combinator commentary and operator analysis on AI-native agencies vs SaaS, 2026, and margin framing (services ~70–80%, product ~90%+); reported across fluxio.dev and lootr.io, Jul 2026. Treat the "10× larger than SaaS" claim as a contested projection, not fact. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^6]: Chip Huyen, *AI Engineering* (O'Reilly, 2024), huyenchip.com/books — AI engineering as a discipline distinct from model building.
[^7]: Andrej Karpathy, public talks and interviews, 2025–2026 — caution against over-reading the agent hype curve; useful agents as a decade-long build-out. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
