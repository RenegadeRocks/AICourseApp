---
type: lesson
block: block-7-onboarding-tracking
week: week-20
session_slug: sops-for-onbaording-delivery-growth
day_of_cycle: 3
day_name: wed
date_due: 2026-09-30
tags:
  - delivery
  - quality-gates
  - growth-sops
  - sop-to-agent
  - automation
  - eval
sources:
  - manyrequests-productized-guide
  - spp-scaling-framework
  - assembly-productized-services
  - systemseffect-scale-without-hiring
  - arxiv-agent-s-sop
  - v7labs-automate-sops
  - gawande-checklist-manifesto
  - taskade-sop-generator
last_verified: 2026-07-17
word_count_target: 3100
---

# Delivery & growth SOPs: the runbook and the machine

## Why this matters

Onboarding gets the customer to first value. Delivery keeps them there, and growth
brings the next one. Both need to happen the same way every time, at a quality you
can guarantee, whether you personally touch them or not. Today you build the two
remaining SOP categories: the delivery runbook that lets the same work be done by
someone other than you without quality collapsing, and the growth SOP library that
turns "post when I remember" into a machine that runs on a cadence. You will also
learn the quality-gate discipline that keeps systematized delivery from becoming
systematized mediocrity, and the SOP-to-agent pipeline that decides which of your
procedures graduate from human-run to automated. By Saturday you will have written
three of these; today is where you learn to write them well.

## Prerequisites

- [[01-mon-sops-the-operating-system-of-a-scaling-business|Mon]] — the SOP form
  and the when-not-to-systematize rule.
- [[02-tue-onboarding-sops-the-first-30-days|Tue]] — the first SOP category;
  today is the other three.
- [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|Week 4 · evaluation]] — the eval discipline that
  quality gates borrow from. We apply it, we do not re-teach it.
- [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/03-wed-growth-loops-vs-funnels|Week 17 · growth loops]] — the loops the growth SOPs
  operationalize.

## Core content

### Delivery SOPs: getting the method out of your head

The single hardest constraint on a service business is stated plainly by operators
who scale productized services: the method lives in the founders' and seniors'
heads, so the service only works when specific hands do it.[^1] As long as that is
true, you cannot delegate, you cannot take a holiday, and you cannot serve more
clients without cloning yourself. The delivery SOP is the tool that moves the
method from your head into a document, so that "the same people can serve more
clients at the same quality," and eventually so that *different* people (or agents)
can too.[^2]

A delivery SOP is the runbook for producing one unit of the thing you sell. Its
structure is the SOP form from Monday, specialized:

- **Trigger:** a delivery cycle begins (new client kicked off, monthly report due,
  ticket assigned).
- **Inputs:** exactly what the person needs before starting (the client's data,
  the brief, access). Naming inputs prevents the most common delivery stall, which
  is starting work you cannot finish because something is missing.
- **The production checklist:** the ordered steps to produce the deliverable.
- **The quality gate:** the check that the output is good, not just done (its own
  section below).
- **The handoff:** how the finished work reaches the client, and what gets recorded.

The productized-service refinement matters most here: for your highest-leverage
deliverables, write the SOP so it captures *what good looks like*, not just the
click-by-click, and include an example of an A-grade output plus the two or three
ways the work usually goes wrong.[^3] A delivery SOP that lists the steps but not
the standard produces work that is procedurally complete and qualitatively
mediocre, which is the exact failure mode that makes founders afraid to delegate.

### Quality gates: eval discipline for delivered work

Systematized delivery has a specific danger: you make the process repeatable, and
what you repeat is mediocre. The defense is the quality gate, a checkpoint the
work must pass before it reaches the client. This is the same discipline you
learned for AI systems in
[[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|Week 4]],
applied to human (and increasingly agent) delivery: you do not trust that the
process produced good output, you *check* against an explicit standard.

A good quality gate has three properties borrowed straight from eval practice:

1. **An explicit rubric, not a vibe.** "Good" must be written down as checkable
   criteria: the report has no factual errors, every claim is sourced, the tone
   matches the client's brand, the deliverable answers the actual question asked.
   A gate with no rubric is just someone glancing at the work.
2. **A gate owned by someone other than the producer where possible.** The person
   who made the thing is the worst judge of whether it is good, because they see
   what they meant, not what they made. Even a lightweight peer check catches what
   self-review misses.
3. **Failure modes named in advance.** Just as an eval set includes the hard cases,
   a quality gate lists the specific ways this deliverable usually goes wrong, so
   the checker looks for them rather than rubber-stamping.

The AI-delivery wrinkle for 2026: much of your delivery may itself be produced by
AI (the report drafted by a model, the automation built with agent help). That
does not remove the quality gate, it makes it more important, because AI output is
fluent enough to look right while being wrong. The gate is where you catch the
confident hallucination before the client does. Run the deterministic checks
first (does it compile, are the numbers internally consistent, are the sources
real), then the judgment check (is it actually good and correct), exactly the
layered eval pattern from Week 4.

> My take: the quality gate is the part of delivery systematization founders skip,
> because it feels like bureaucracy when you are the one doing the work and you
> "know" it is good. It stops feeling optional the first time you delegate and get
> back work that followed every step and was still embarrassing. Write the rubric
> before you delegate, not after the first bad deliverable reaches a client.

### The growth SOP library

Growth is where founders most resist systematization, because it feels creative
and mood-dependent. That resistance is the enemy. The businesses that grow
predictably are the ones that made growth a set of procedures on a cadence, not a
burst of activity when inspiration or panic strikes. The growth SOP library
operationalizes the loops you learned in
[[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/03-wed-growth-loops-vs-funnels|Week 17]]
into repeatable actions. Three core growth SOPs cover most of the ground:

- **The content SOP.** The repeatable production of the content that feeds your
  top of funnel. Trigger: it is the scheduled publishing day. Checklist: the steps
  from idea to published post, including where ideas come from (so you are never
  staring at a blank page), the format template, and the distribution steps.
  Definition of good: on-brand, useful to the target reader, with a clear next
  step. This turns "I should post more" into a Tuesday task anyone can execute.
- **The outreach SOP.** The repeatable warm and cold outreach cadence. Trigger:
  daily or weekly outreach block. Checklist: how prospects enter the list, the
  message sequence, the follow-up timing, and the CRM hygiene. The 2026 constraint,
  carried from earlier blocks: outreach that reads as AI-generated is actively
  demoted or penalized on the major platforms, so the SOP must produce genuinely
  personalized contact, not templated spam at scale.
- **The referral SOP.** The repeatable ask, at the moment of delight. Trigger: a
  client hits a defined success milestone (delivered a great result, gave positive
  feedback). Checklist: the ask, the mechanism, the tracking. This operationalizes
  the referral mechanics from Week 17, moving referral from "I hope people tell
  their friends" to a triggered procedure.

The through-line: a growth SOP converts an intention ("we should do more content /
outreach / referral") into a triggered, checklisted, ownable procedure that runs
whether or not the founder feels inspired that week. Consistency is the growth
lever most within your control, and SOPs are how you get it.

### Handoff-ready documentation: the delegation test

The real test of a delivery or growth SOP is not whether *you* can follow it, it
is whether someone else can. The productized-service operators call this role
clarity: what lets you push work down without it bouncing straight back up to the
founder the first time something is ambiguous.[^2] Write every SOP for the least
experienced person who will run it, and you get two payoffs: you can delegate to a
junior hire or contractor, and you can hand the deterministic parts to an agent
(which is even less able than a junior to fill an ambiguous gap with judgment).

The concrete test: before you consider an SOP done, have someone who has never done
the task try to run it from the document alone, with you watching silently. Every
time they hesitate, ask a question, or do it wrong, that is a gap in the SOP, not a
failure of the person. Fix the SOP, not the person. This is the SOP equivalent of
usability testing, and it is the fastest way to find the assumptions you did not
know you were making.

### The SOP-to-automation pipeline: which procedures become agents

This is where Block 7's operations layer connects to Block 3's automation layer.
Not every SOP should become an agent, and choosing wrong in either direction is
costly: automate a judgment task and it fails silently in the gaps; keep a
deterministic high-frequency task manual and you waste your life on it.

The selection rubric, per procedure, on three axes:

1. **Frequency.** How often does this run? High-frequency procedures pay back
   automation fastest. A once-a-quarter procedure rarely justifies the build.
2. **Determinism.** How much judgment does it require? Low-judgment, rule-following
   procedures (send the templated welcome, generate the first-draft report, triage
   inbound by category, compile the weekly metrics) are agent candidates.
   High-judgment procedures (the hard client call, the pricing exception, the "is
   this good?" review) stay human.
3. **Cost of error.** What happens if it goes wrong unnoticed? Even a deterministic
   procedure with a catastrophic failure mode may keep a human in the loop as the
   gate.

The research context, from yesterday: a well-formed SOP is already close to an
agent specification, because it is a trigger plus an ordered checklist plus a
definition of done, which is why the literature on feeding SOPs into agents (the
Agent-S line of work) finds structured procedures improve agent controllability
and reliability.[^4] Vendors now claim AI can automate the majority of SOP
*creation* work; the more consequential claim is that structured SOPs make SOP
*execution* by agents viable for the routine slice.[^5] The practical output is a
two-column view of your whole SOP library: human-run and agent-run. The agent-run
column, built with the patterns from
[[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/01-mon-the-automation-spectrum-in-2026|Week 8]],
is where your business starts to run without you.

The critical caveat, load-bearing enough to repeat from Monday: an SOP handed to an
agent must be *stricter* than one handed to a human, with failure modes and stop
conditions explicit, because the agent will not fill an ambiguous gap with
context, it will fill it with a confident guess. Automating an under-specified SOP
is how you scale mistakes.

### Maintaining SOPs as the business changes

The final delivery-and-growth discipline is the one that determines whether your
SOP library is an asset or a liability in a year. A stale SOP is worse than none,
because new people and agents trust it. Three maintenance practices:

- **Version everything, and let anyone flag but only the owner change.** Reality
  changes constantly; the SOP must change with it, through a controlled path so it
  does not fork into contradictory copies.
- **Review on a cadence.** A last-reviewed date and a quarterly review interval so
  overdue SOPs surface. This is the "dynamic workflow, not static manual" principle
  in practice.
- **Let the failure teach the SOP.** When something goes wrong in delivery, the fix
  is not just to fix the instance, it is to update the SOP so the failure cannot
  recur. This is how an SOP library compounds: every mistake becomes a permanent
  improvement, the same blameless-postmortem logic that mature engineering teams use.

## Worked example: from delivery SOP to delivery agent

Take the monthly-report deliverable from a productized AI service. Here is the
delivery SOP and its automation split.

**Delivery SOP: produce one monthly client report.**

- **Trigger:** first business day of the month.
- **Inputs:** client's data sources connected, the report template, last month's
  report for continuity.
- **Production checklist:** (1) pull the month's metrics from the connected
  sources; (2) generate the narrative draft from the metrics using the report
  template; (3) add the "what changed and why it matters" analysis; (4) add the
  recommended actions for next month.
- **Quality gate (rubric):** every number traces to a source and is internally
  consistent; the analysis is specific to this client, not generic; the
  recommendations are actionable, not platitudes; no hallucinated facts. Named
  failure mode: the AI-drafted analysis sounds insightful but is generic filler
  that would fit any client.
- **Handoff:** published to the client dashboard, notification sent, recorded as
  delivered.

**The automation split.** Steps 1 and 2 (pull metrics, generate first-draft
narrative) are high-frequency and deterministic: agent candidates. Step 3's
first pass can be agent-drafted but the "why it matters" judgment needs your
review. Step 4 (recommendations) and the entire quality gate stay human, because
recommendation quality and catching the generic-filler failure mode are exactly
the judgment an agent lacks. The result: an agent produces the mechanical 70% (data
pull, draft narrative, formatting) on the first of the month automatically, and you
spend your time on the 30% that is analysis, recommendations, and the quality gate,
which is the part the client actually pays for. That is the SOP-to-agent pipeline
delivering its promise, more capacity without more of your hours, without
sacrificing the quality gate. The runnable SOP-template generator that produces
these structured SOPs is the Saturday
[[06-sat-build-sop-library-and-community-launch|build]].

## Common mistakes experts see

1. **Systematizing delivery without a quality gate.** A repeatable process with no
   quality check produces repeatable mediocrity. Write the rubric and name the
   failure modes before you delegate.[^3]
2. **Delivery SOPs that list steps but not the standard.** Capture what good looks
   like with an A-grade example, or you get procedurally complete, qualitatively
   poor work.
3. **Treating growth as mood, not procedure.** "Post when inspired" does not scale.
   Turn content, outreach, and referral into triggered, checklisted SOPs on a
   cadence.
4. **Testing SOPs only by whether you can follow them.** The test is whether a
   stranger can. Every hesitation in a silent run-through is a gap in the SOP, not
   the person.
5. **Automating an under-specified SOP.** An agent will fill an ambiguous gap with
   a confident guess. Agent-run SOPs must be stricter than human-run ones, with
   failure modes and stop conditions explicit.[^4]
6. **Never updating SOPs after a failure.** If a delivery mistake does not result
   in an SOP update, you will make it again. Every failure should become a
   permanent improvement to the procedure.

## Reflection questions

1. What is the one deliverable that only works when *you* personally do it? What
   specifically lives in your head that is not yet written down, and why?
2. Write the quality-gate rubric for your main deliverable. What are the two or
   three specific ways it usually goes wrong, and would your current process catch
   them?
3. Which of your growth activities is currently mood-dependent? What would it look
   like as a triggered SOP on a cadence, and what is stopping you from making it one?
4. Run the SOP-to-agent rubric (frequency, determinism, cost of error) on your
   delivery process. Which steps are honestly agent candidates, and which are you
   tempted to automate that you should not?
5. When something last went wrong in delivery, did you update the SOP, or just fix
   the instance? What does your answer tell you about whether your business is
   compounding or repeating?

## My take (reviewer lens)

**Hamel Husain** would push hardest on the quality gate as an eval problem: he has
argued repeatedly that teams skip the unglamorous work of writing down what "good"
means and building the checks, then wonder why quality is inconsistent. His
correction here is to treat the delivery rubric as a real eval set, with named hard
cases and failure modes, not a vibe check, and to run the deterministic checks
before the judgment check. That is exactly the layered discipline from Week 4,
applied to delivered work rather than model output.

**Jerry Liu** would flag the AI-delivery risk specifically: as more of your
delivery is drafted by agents, the fluency of the output masks its errors, so the
quality gate has to get sharper precisely as the production gets faster. The temptation
is to let the agent's polish substitute for the gate. It cannot; a confident,
well-formatted, wrong deliverable is worse than an obviously rough one, because the
client trusts it.

**Michael Seibel** would caution against building the full three-column growth SOP
library before you have a growth motion that works at all: systematizing a growth
channel you have not yet proven is documenting a hope. His rule, which the lesson
should hold, is to systematize the growth activity only *after* you have made it
work manually a few times and seen it produce results, not as a way of pretending
you have a growth engine you do not.

## Further reading

**Must-read**

- ManyRequests / SPP on productized-service delivery and getting the method out of
  the founder's head, the core constraint this lesson attacks.[^1][^3]

**Recommended**

- The Systems Effect on how agencies scale delivery without constantly hiring, by
  productizing the delivery work itself.[^2]
- Back to [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|Week 4 evaluation]] for the quality-gate
  discipline in its original AI-systems form.

**Optional**

- The Agent-S / SOP-to-agent research, for the technical view of when structured
  procedures make agent execution viable.[^4]

## Citations

[^1]: "The Productized Service Guide: How to Build, Price, and Scale [2026],"
ManyRequests. https://www.manyrequests.com/blog/productized-service-guide — the core
constraint that delivery lives in founders' and seniors' heads. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending; corroborated by
assembly.com/blog/productized-services.)
[^2]: "How Agencies Scale Without Constantly Hiring," The Systems Effect.
https://thesystemseffect.com/how-agencies-scale-without-hiring/ — productize the
delivery work so the same people serve more clients; role clarity prevents work
bouncing back to the founder. (search-verified 2026-07-17; corroborated by
silverspoonagency.com/how-to-scale-a-service-business/.)
[^3]: "Scaling Productized Services: 3-Pillar Quality Framework," SPP.
https://spp.co/blog/scaling-productized-services-framework/ — write SOPs that
capture what good looks like; include an A-grade example and common failure modes.
(search-verified 2026-07-17; corroborated by ManyRequests guide above.)
[^4]: "Agent-S: LLM Agentic workflow to automate Standard Operating Procedures,"
arXiv 2503.15520. https://arxiv.org/pdf/2503.15520 — structured SOPs improve agent
controllability and reliability. (search-verified 2026-07-17; corroborated by
v7labs.com/automations/standard-operating-procedures-sops.)
[^5]: "What Is an SOP Generator? AI SOP Guide (2026)," Taskade.
https://www.taskade.com/blog/what-is-an-sop-generator — AI generation and management
of SOP libraries; automation of documentation work. (search-verified 2026-07-17;
corroborated by usewhale.io/blog/discover-2026s-top-ai-tools-for-managing-sops/.)

_last_verified: 2026-07-17_
