---
type: lesson
block: block-8-wind-up-checklists
week: week-22
session_slug: final-thoughts-recap-checklists-2
day_of_cycle: 4
day_name: thu
date_due: 2026-10-15
tags:
  - capstone
  - re-verification
  - staying-current
  - meta-skill
  - epistemics
sources:
  - course-refresh-report-2026-07
  - reading-model-specs-critically
  - forte-para-pkm
  - anthropic-pricing-2026
  - eu-ai-act-2026
  - willison-blog
last_verified: 2026-07-17
---

# Staying current: the graduate's re-verification practice

## Why this matters (operator framing)

Here is the skill the course was quietly teaching under all the others: how to
keep expensive knowledge from silently going wrong. You now know that this course
itself was refreshed in July 2026 and that three-month-old content was already
incorrect in places — Opus mispriced 3×, a deprecated vulnerable server taught as
canonical, cost math that no longer computed after a tokenizer change.[^1] That is
not an indictment of the course. It is the demonstration. Everything you learned
decays, and the graduate who thrives is the one who runs a re-verification
practice instead of trusting a memory that is quietly rotting. This lesson hands
you that practice, using this course's own refresh as the worked example.

## Prerequisites

[[block-0-basecamp/week-00-ai-catalyst-program-onboarding/04-thu-reading-model-specs-critically|Reading model specs critically]] from Basecamp — the atomic version of today's skill — and [[03-wed-the-durable-principles|Wednesday's durable principles]], because the whole method rests on knowing which layer decays.

## The core insight: knowledge has a half-life, and it is short

Not all knowledge decays at the same rate. Wednesday's 14 principles have a
half-life measured in years or decades. The facts they rest on have a half-life
measured in weeks. The refresh report quantified exactly where the rot
concentrates: "The course's skeleton is sound; its skin is three months old in a
field that molts monthly."[^1] Frameworks, failure taxonomies, and eval discipline
graded A. The decay was concentrated in "exactly the layer a reader touches:
model names, prices, benchmarks, tool features, commands, and API surfaces."[^1]

That sentence is the whole method. Fast-decaying knowledge sits closest to what
you actually do each day, which is why it feels most concrete and gets trusted
most. The re-verification practice is a system for distrusting the concrete on a
schedule.

## What in THIS course will age fastest — a decay map

Read this as a model for how to audit any body of knowledge you rely on. Sort
what you learned by half-life.

**Weeks (trust nothing older than a quarter without re-checking):**

- **Model names, prices, and context limits.** As of the last verification: Opus
  4.8 at $5/$25, Sonnet 5 at a $2/$10 introductory rate moving to $3/$15, a new
  Mythos-class tier above Opus, plus a tokenizer that adds roughly 30% to token
  counts.[^2] Every one of these numbers is a landmine in old notes. The refresh
  found four separate weeks with model lineups one to three generations stale.[^1]
- **Tool features, commands, and pricing.** The coding-agent market restructured
  in a single quarter: Cursor acquired, Copilot moved to usage-based credits,
  Claude Code usage shifted to API-rate credit pools.[^1] Any teardown or command
  you memorized has a shelf life of one product cycle.
- **Platform rules.** LinkedIn now demotes AI-generated outreach; the X ranker
  changed; the EU AI Act became fully applicable on 2 August 2026.[^3] Advice that
  was compliant in spring can be counterproductive or non-compliant by autumn.

**Months to a year:**

- **Benchmarks and "best in class" claims.** True on the day written, stale by the
  next release.
- **Specific stack and framework recommendations.** The discipline is durable; the
  named library is not.

**Years to durable:**

- **The 14 principles, the failure taxonomies, the threat models, the eval
  discipline, the unit-economics reasoning.** These are what the refresh left
  almost untouched.[^1]

The rule that falls out of this map: **distrust anything fact-shaped that is older
than a quarter, and re-verify before you act on it.**

## The `_last_verified` habit

You saw it at the bottom of every lesson in this vault: `_last_verified:
2026-07-17`. That stamp is not decoration. It is the single highest-leverage habit
in this lesson, and you should adopt it for your own knowledge.

The habit: every claim you write down that could decay — a price, a model choice,
a platform rule, a competitor fact — gets a date next to it. Then a fact is never
just "true" or "false." It is "true as of a date," and its trustworthiness is a
function of how old that date is against the thing's half-life. A price stamped
three months ago is suspect. A principle stamped three years ago is fine.

This is the atomic version of the whole refresh. The course put a verification
date on 430,000 words so that reviewers could see, at a glance, what needed
re-checking.[^1] Do the same for your own operating knowledge: your pricing sheet,
your model-selection notes, your competitor list, your compliance assumptions.
Undated facts are the ones that quietly go wrong.

## Reading a source critically — the Basecamp skill, generalized

Thursday of Basecamp taught you to read a model spec critically: separate the
benchmark from the marketing, ask what the number was measured on, notice what the
spec omits.[^4] Generalize it. Every fast-moving source you read is a spec written
by someone with an incentive. The re-verification questions are the same:

- **Who benefits if I believe this?** A vendor's benchmark, an influencer's "this
  changes everything," a framework's docs claiming it is the standard.
- **What was it measured on, and does that match my case?** A benchmark on
  clean data says little about your messy inputs.
- **What is the date, and what is this claim's half-life?** A six-month-old
  pricing comparison is archaeology.
- **What does the source omit?** The refresh found real papers with invented
  author names and quotes attributed to people who never said them — fabrications
  that a single cross-check would have caught.[^1] Load-bearing claims need a
  second independent source.

Simon Willison's blog is the working model of this discipline in public: date
every observation, link the primary source, and revise openly when the facts
move.[^5] Read a few of his posts not for the content but for the *method*.

## The refresh discipline, run at your own scale

The course ran a formal refresh: eleven parallel reviewers, a landscape-delta
researcher tracking what changed in three months, a slop census, and a fix pass
that re-verified every fact it touched via live search.[^1] You do not need eleven
agents. You need the discipline, scaled down.

**A minimal refresh loop for a solo operator:**

1. **Inventory your decaying facts.** The prices, models, platform rules, and
   competitor facts your business decisions rest on. Most operators have fewer
   than twenty. Write them down with dates.
2. **Set a re-verification cadence by half-life.** Prices and model choices:
   monthly. Platform rules and compliance: quarterly, or on any announcement.
   Competitor landscape: quarterly. Principles: never, unless a genuine anomaly
   appears.
3. **Re-verify against primary sources, never memory or a single snippet.** The
   refresh's own rule of engagement: "findings files are leads, not truth;
   anything marked suspected must be confirmed or dropped."[^1] Two independent
   sources for anything load-bearing.
4. **Update the canonical home and re-stamp the date.** One authoritative place
   per fact (Wednesday's principle 13), updated, re-dated.
5. **Propagate.** When a fact changes, find everywhere your decisions depend on it
   and update them. The refresh's hardest lesson: a mispriced token invalidated
   an entire cost-math layer downstream.[^1] Facts have dependents.

Saturday's build turns steps 1–2 into a runnable scheduler so you do not have to
remember the cadence.

## Building a personal intelligence system

You cannot re-verify what you never hear about, so the practice needs an input
side: a small, deliberate information diet rather than a firehose. The research on
staying current in a field this fast converges on a few points: curate a focused
input set, set boundaries, use summarization to compress, and run one capture
system long enough to compound rather than rebuilding it every month.[^6] Tiago
Forte's PARA is one workable structure — organize by how soon you will use
something, not by topic — but the specific system matters far less than running
one consistently.[^6]

For an AI operator specifically, a defensible diet is narrow: the primary sources
for the two or three models you actually ship on (their changelogs and pricing
pages), one or two practitioners who date and cite their claims, one channel for
your niche, and a scheduled monthly sweep of your decaying-facts inventory.
Everything else is noise you can safely miss. The joy-of-missing-out framing is
not a lifestyle preference here; it is a defense against the fatigue that makes
people stop verifying anything.[^6]

The trap on the input side is the perpetual-learner loop: consuming so much new
information that you never act, which Friday treats directly. A personal
intelligence system exists to serve decisions, not to replace them.

## Knowing what to trust

The end state of this practice is calibrated trust. You stop asking "is this
true?" and start asking "how much should I trust this, given its source, its
date, and its half-life?" Three tiers, roughly:

- **Trust and act:** primary sources on their own domain (a vendor's own pricing
  page), dated and cross-checked, for a fact within its half-life.
- **Trust as a lead, verify before acting:** a practitioner you respect, a single
  benchmark, a findings file. Confirm before it drives a decision.
- **Distrust until proven:** undated claims, "this changes everything," anything
  post-dating your last verification that you have not checked, and — the course's
  own hard-won rule — any fact your model produced from training data alone about
  events after its cutoff.[^1]

That last one deserves weight. A capable model will state a stale price or a
retired model name with total confidence, because its training data said so. The
refresh's forbidden list existed for exactly this failure: "post-2025 facts from
training data alone; invented URLs; single-snippet load-bearing claims."[^1] The
graduate who internalizes this treats a confident AI answer about a fast-moving
fact as a lead to verify, never as the verification.

## Worked example: audit one week of this course

Pick any weekday lesson you studied earlier in the program. Read it with the
decay map in hand and mark every fact-shaped claim with a color: green (durable
principle), yellow (months-scale, verify before relying), red (weeks-scale,
assume stale). Then take one red claim — a price, a model name, a tool feature —
and re-verify it against a primary source today. Note whether it moved.

**Pass bar:** you found at least one red claim in the lesson, re-verified it
against a primary source, and can state whether it is still true as of today. If
you found none, you either picked a pure-principle lesson or you are not yet
seeing the decaying layer — reread the decay map.

## Common mistakes experts see

- **Trusting your own notes because you wrote them.** Your notes decay exactly
  like the course did. Date them or distrust them.
- **Re-verifying principles and ignoring prices.** Effort spent re-checking
  durable frameworks is wasted; the decay is in the facts.
- **Single-source verification.** One snippet confirming what you hoped is not
  verification. The refresh found fabricated quotes that one cross-check would
  have killed.
- **Believing a confident model over a primary source.** Confidence is not
  currency. On fast-moving facts, the model is a lead, the vendor page is the
  source.
- **Building an elaborate PKM instead of running a simple one.** The system that
  compounds is the one you actually run for a year, not the one you keep
  redesigning.
- **No propagation.** Updating a fact in one place while three dependent
  decisions still rest on the old value.

## Reflection questions

1. What are the ten decaying facts your business currently rests on, and when did
   you last verify each?
2. Which fact in your operating knowledge is most likely already wrong, and how
   would you know?
3. What is your re-verification cadence, and does it match each fact's half-life?
4. Whose public work models the date-and-cite discipline well enough that you
   would put them in your information diet?
5. When did an AI answer last state something confidently that turned out to be
   stale? What did that cost, or nearly cost?

## My take (reviewer lens)

**swyx** would push that a purely defensive information diet under-serves an
operator. His argument: staying current is also about spotting the genuine
step-change early, and an over-narrow diet makes you miss the shift that matters.
Fair tension — the answer is a narrow *verification* diet plus a small,
deliberate *exploration* budget, not one or the other.

**Willison** would want the "distrust confident AI answers on fast-moving facts"
rule stated as the headline, not a subsection. It is, in his practice, the single
most important epistemic habit of the era, and he would say this lesson buries it.
He is probably right; if you keep one thing, keep that.

**Jeremy Howard** would object to any implication that you must drink from the
firehose to stay competent. His anti-hype position: most of the daily churn is
noise, principles move slowly, and a calm operator who re-verifies a small fact
set beats an anxious one who reads everything. This lesson agrees with him, and
the perpetual-learner warning is the hinge into Friday's plan.

## Further reading

- **Must-read:** [[block-0-basecamp/week-00-ai-catalyst-program-onboarding/04-thu-reading-model-specs-critically|Reading model specs critically]] — the atomic skill this lesson generalizes.
- **Recommended:** the July 2026 refresh master report, [[00-program/_refresh-2026-07-master-report|in the program folder]] — the worked example of a real re-verification at scale, including its forbidden-facts rules.
- **Optional:** Simon Willison's blog, simonwillison.net — the date-and-cite
  discipline practiced in public.[^5]

## Citations

[^1]: AI Pro-level Course, "July 2026 Content Refresh — Master Findings Report," internal, 2026-07-17 — "skeleton is sound; skin is three months old"; decay concentrated in model names, prices, benchmarks, tool features, commands, API surfaces; forbidden-facts and two-source rules of engagement; findings are leads not truth. See [[00-program/_refresh-2026-07-master-report|the master report]].
[^2]: Anthropic, "Pricing," platform.claude.com/docs/en/about-claude/pricing and "Introducing Claude Sonnet 5," anthropic.com/news/claude-sonnet-5 — Opus 4.8 $5/$25; Sonnet 5 $2/$10 intro → $3/$15; new tokenizer adds ~1.0–1.35× tokens. Corroborated by the refresh master report. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^3]: European Union, EU AI Act, official implementation timeline — full applicability from 2 August 2026; corroborated in the refresh landscape-delta. Plus platform-rule shifts (LinkedIn AI-outreach demotion, X ranker change) documented in the same delta. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^4]: [[block-0-basecamp/week-00-ai-catalyst-program-onboarding/04-thu-reading-model-specs-critically|"Reading model specs critically," Basecamp Week 00]] — separate benchmark from marketing; ask what was measured and what is omitted.
[^5]: Simon Willison, simonwillison.net — dated observations, linked primary sources, open revision as facts move; a public model of the re-verification discipline.
[^6]: Personal knowledge management and staying-current practice, 2026 — curated information diet, PARA (Tiago Forte), run one system long enough to compound, JOMO as defense against AI fatigue; reported across atlasworkspace.ai and pretalx PyConDE/PyData 2026. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
