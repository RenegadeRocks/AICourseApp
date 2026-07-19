---
type: lesson
block: block-7-onboarding-tracking
week: week-20
session_slug: sops-for-onbaording-delivery-growth
day_of_cycle: 1
day_name: mon
date_due: 2026-09-28
tags:
  - sops
  - operations
  - checklists
  - systematization
  - ai-agents
  - documentation
sources:
  - gawande-checklist-manifesto
  - gerber-emyth
  - usewhale-ai-sop-tools
  - taskade-sop-generator
  - arxiv-agent-s-sop
  - assembly-productized-services
  - spp-scaling-framework
  - f7i-dynamic-sop
last_verified: 2026-07-17
word_count_target: 3800
---

# SOPs: the operating system of a business that scales

## Why this matters

Right now your business has one dependency that no dashboard will show you: you.
The onboarding works because you remember the steps. Delivery is good because you
check it. Growth happens because you post when you remember to. That is not a
business, it is a job you invented for yourself, and it caps at the number of
hours you can personally stay awake. An SOP, a standard operating procedure, is
the artifact that lifts a task out of your head and puts it somewhere a junior
hire, a contractor, or an AI agent can run it at the same quality you would. This
week you will write a real SOP library. Today you learn what an SOP actually is,
why the checklist form beats the beautiful document, how AI changes both the
writing and the running of them, and the harder question most operators get
wrong: which parts of your business you should never systematize.

## Prerequisites

- [[block-7-onboarding-tracking/week-19-build-async-client-dashboard-or-project-tracking-for-agency--productizing-your-service-community-market-research/00-overview|Week 19 · productized service]] (pending) — the delivery
  model these SOPs document.
- [[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/03-wed-delivery-engineering-one-build-many-customers|Week 9 · delivery engineering (one build, many customers)]] — the
  same repeatability principle, applied to product.
- [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/01-mon-the-automation-spectrum-in-2026|Week 8 · the automation spectrum]] — the
  ladder from manual to agentic that decides which SOPs become code.

## Core content

### First principle: an SOP is a decision made once, so it never has to be made again

Every task in your business is a bundle of small decisions. What do I put in the
welcome email? Which fields do I check before I send a deliverable? How do I
respond when a client asks for a refund? When those decisions live only in your
head, you re-make them every time, slightly differently, and the variation is
where quality dies. An SOP is the record of the best version of a decision,
written down so it is made once and then executed identically forever after.

This is the insight Michael Gerber built *The E-Myth Revisited* around. Most
small businesses fail, Gerber argues, because the founder is a technician who is
good at the work, and mistakes being good at the work for being able to run a
business built on the work. The fix is to work *on* the business, not *in* it: to
build a "franchise prototype," a systems-dependent business rather than a
people-dependent one, where the process is documented well enough that the
business could be duplicated by someone else.[^1] You are not literally
franchising. But the test is the same: if you were hit by a bus, could someone
open your laptop and keep your clients happy for two weeks using only what you
wrote down? If the answer is no, you do not own a business, you *are* the
business.

### The SOP is a system, not a document

The most common mistake is treating "write an SOP" as "write a nice document."
The document is the least important part. An SOP is a system with four parts, and
the prose is the smallest of them:

1. **A trigger.** What event starts this procedure? "A new client signs the
   contract." "It is Monday 9am." "A refund is requested." An SOP with no trigger
   is a suggestion, not a procedure.
2. **A checklist of steps.** The atomic actions, in order, each phrased so that
   someone can tell whether it is done. Not "handle onboarding" but "send the
   welcome email from template W-1."
3. **A definition of done, and of good.** What does the finished output look
   like? Crucially, not just "complete" but "correct." The best SOPs include an
   example of an A-grade output and the two or three ways the work usually goes
   wrong.[^2]
4. **An owner and a version.** Who is responsible for this procedure being right,
   and which version are we on? An SOP with no owner rots. An SOP with no version
   number quietly forks into five contradictory copies.

Notice what this makes an SOP: an *operating system* for a task. The trigger is
the interrupt, the checklist is the program, the definition of done is the test,
and the owner and version are the maintainer and the release. Software people
already know this shape. You are writing programs for humans (and, increasingly,
for agents) to run.

### The checklist beats the essay, and there is hard evidence

The instinct of a smart person writing an SOP is to write beautiful,
comprehensive prose that explains everything. Resist it. The highest-performing
form of procedural knowledge is the humble checklist, and the evidence comes from
the highest-stakes environment there is: the operating room.

Atul Gawande, a surgeon, documented what happened when the World Health
Organization introduced a two-minute, nineteen-item surgical safety checklist
across eight hospitals worldwide. It was not new technology or smarter surgeons.
It was a list of things everyone already knew, made impossible to skip: confirm
the patient's identity, confirm antibiotics were given, confirm blood is
available. Surgical deaths fell by more than a third, and in the original study
major complications dropped substantially, across hospitals rich and poor.[^3]
The reason it worked is the reason it works for your business: experts do not
fail because they lack knowledge, they fail because complexity outruns memory,
and under pressure people skip steps they "know." A checklist externalizes the
memory. The A-player who wrote the essay-SOP still forgets step four at 6pm on a
Friday. The checklist does not.

So the form of a good SOP is closer to a pilot's pre-flight checklist than to a
textbook chapter: short, imperative, verifiable, one line per action. Save the
explanation for a linked "why" note that a new person reads once. The runnable
procedure is a list of ticks.

### The SOP hierarchy: four categories that cover a service business

Do not try to document your whole business at once, that is how SOP projects die.
Organize by the four categories that matter, and write the highest-leverage one
in each first.

- **Onboarding SOPs.** Everything from "signed" to "activated." The single
  highest-leverage category, because the first 30 days decide retention (that is
  tomorrow's whole lesson). Example: the new-client kickoff sequence.
- **Delivery SOPs.** The repeatable production of the thing you sell. The
  productized-service runbook. Example: "produce and QA one monthly report."
- **Growth SOPs.** The activities that bring in and warm up demand: content
  publishing, outreach cadence, referral asks. Example: "publish one case study
  per week."
- **Support and admin SOPs.** The reactive and back-office procedures: refunds,
  bug triage, invoicing, offboarding. Example: "process a refund request."

A useful rule for sequencing: write the SOP for the task you do most often and
hate most, first. Frequency times pain equals leverage. The thing you do twenty
times a month and dread is the thing whose systematization buys back the most of
your life and your sanity.

### Writing SOPs that actually get followed

A library of SOPs nobody follows is worse than none, because it creates the
illusion of a system. Four properties separate SOPs that get used from shelfware:

1. **Findable at the moment of need.** The SOP must live where the work happens.
   An onboarding checklist that lives in a Notion page nobody opens loses to a
   worse checklist embedded as a task template in the project tool the team
   already uses. Reduce the distance between "I need to do X" and "here is how."
2. **Short enough to actually read.** If the checklist runs to three screens, it
   will be skimmed and then ignored. Split it. One procedure, one screen.
3. **Written at the level of the least experienced person who will run it.** Not
   "configure the integration" but "click Settings, then Integrations, then paste
   the key from 1Password entry named X." When in doubt, over-specify. You can
   always compress once you see it followed.
4. **Owned and dated.** Every SOP has one human owner and a last-reviewed date.
   Ownerless SOPs are how a team ends up confidently doing the wrong thing for
   six months.

The modern refinement, from operators who scale productized services: write the
SOP so it captures *what good looks like*, not only the click-by-click. Include an
example of an A-grade output, and name the two or three ways the work usually
goes wrong, so the person running it can self-check against quality, not just
completion.[^2] A checklist tells you the steps. A great SOP also tells you how to
know you did them well.

### The AI angle: SOPs that AI writes, and SOPs that AI runs

This is 2026, and there are two distinct ways AI changes the SOP layer. Do not
conflate them.

**AI writes the first draft.** The blank page is the reason most SOPs never get
written. That problem is now largely solved. You can hand a model a screen
recording, a transcript of you talking through a task, or just a rough bullet
list, and get a structured, checklist-form SOP back in minutes instead of hours.
Dedicated tools have productized this: Whale, Taskade, Scribe, and others generate
and manage SOP libraries, with vendors claiming AI now automates the majority of
the documentation-writing work.[^4][^5] The honest framing: AI removes the
activation energy of *drafting*, and it is genuinely good at turning your messy
narration into a clean checklist. It is not good at knowing which of your
idiosyncratic quality standards matter. So the workflow is: you narrate the task
once, AI drafts the SOP, you edit in the judgment. Treat the AI draft as a
articulate junior who has watched you work but does not yet know what "good"
means to you.

**AI runs the procedure.** The deeper shift is that some SOPs stop being
instructions for humans and become instructions for agents. A well-written SOP,
because it is already a trigger plus an ordered checklist plus a definition of
done, is close to an agent specification. The research literature has caught up
to this: work like Agent-S and related systems studies how to feed SOPs into
LLM-based agents to improve their controllability and reliability, precisely
because a structured procedure constrains an otherwise wandering model.[^6] The
practical implication for you is a two-column view of your SOP library: for each
procedure, ask "human-run or agent-run?" The routine, deterministic,
high-frequency procedures (send the welcome sequence, generate the first-draft
report, triage inbound by category) are candidates to graduate into automation,
using the agent patterns from
[[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/01-mon-the-automation-spectrum-in-2026|Week 8]].
The judgment-heavy ones (the strategy call, the hard client conversation, the
"is this actually good?" review) stay human. Writing the SOP is the prerequisite
either way: you cannot automate a process you have not first made explicit.

> My take: the "AI runs the SOP" story is real but oversold in vendor copy. A
> checklist for a human tolerates ambiguity because the human fills gaps with
> context. An agent does not, and will confidently do the wrong thing in the gap.
> So the SOPs you hand to agents need to be *stricter* than the ones you hand to
> people, with the failure modes and the stop conditions spelled out. The
> discipline of writing an agent-grade SOP is itself the useful work.

### Versioning and ownership: the part everyone skips

An SOP is not written once. Your business changes, tools change, and a procedure
that was right in January is wrong by June. The failure mode is not that SOPs are
never written, it is that they are written once, never updated, and quietly
become lies that new hires trust. Three lightweight practices prevent this:

1. **A single source of truth.** All SOPs live in one place, not scattered across
   Google Docs, Slack messages, and someone's memory. The place matters less than
   the singularity.
2. **A review cadence.** Each SOP has a last-reviewed date and a review interval
   (quarterly is a reasonable default for a small business). Overdue SOPs surface
   automatically. This is exactly the "dynamic, digital workflow" framing that
   distinguishes a modern SOP from a static manual: the procedure is a living
   trigger system, not a reference PDF.[^7]
3. **Change through the owner.** When reality changes, the owner updates the SOP
   and bumps the version. Anyone can *flag* an SOP as wrong; only the owner
   changes it, so it does not fork.

### When NOT to systematize (the controversy)

Here is where the operations-obsessed and the founder-instinct camps openly
disagree, and you should hold both in your head.

The pro-process case, from the productized-services world, is that
systematization is what lets you scale without your quality collapsing or your
life ending, and that founders under-document out of ego and laziness.[^2] The
counter-case, associated with early-stage founder culture, is that heavy process
at small scale is premature optimization: you spend a week documenting a
procedure that will change next month, you ossify a way of working before you
know it is the right one, and you replace the judgment that is your actual
competitive edge with a rigid checklist that a bigger competitor will also have.

The resolution is not a compromise, it is a rule about *what* and *when*:

- **Systematize the repeated and stable.** If you have done a task the same way
  five-plus times and expect to keep doing it, document it. The onboarding
  sequence, the monthly report, the refund process.
- **Do NOT systematize the rare, the still-changing, or the judgment-defined.**
  If you have done it twice and it changed both times, writing an SOP is
  documenting a guess. If the task *is* judgment (which client to fire, how to
  price a weird deal, whether this creative direction is good), an SOP will make
  you worse, not better, because it replaces thinking with box-ticking.
- **The dividing line is variance, not importance.** Important-but-stable tasks
  (payroll, deploys) should be heavily systematized. Important-but-high-variance
  tasks (strategy, hard judgment calls) should not.

> My take: at the scale most readers of this course are at (solo, or two to five
> people), the more common error is far and away *under*-documentation, not over.
> The founder who "keeps it in their head to stay flexible" is usually just
> avoiding the boring work of writing it down, and pays for it in inconsistent
> delivery and an inability to ever take a vacation. Systematize aggressively, but
> only the things you have genuinely done the same way several times. Judgment
> stays yours.

## Worked example: turning a task you hate into an SOP

Let us make this concrete with a task almost every service business has: sending a
new client their kickoff package after they sign.

**Step 1 — Narrate it once.** Open a voice memo or a Claude conversation and
describe, start to finish, exactly what you do when a client signs. Do not
organize it, just talk. "Okay so when someone signs, first I check the contract
came back fully signed in the e-sign tool, then I add them to the CRM with the
'active' tag, then I send the welcome email which has the intake form and the
Calendly link for the kickoff call, then I create their project in the tracker
from the template, then I set a reminder to check they filled the intake form
within 48 hours..."

**Step 2 — Let AI structure it.** Paste the narration into a model and ask for a
checklist-form SOP with a trigger, ordered steps, a definition of done, an owner
field, and a version. You will get back something clean in seconds. This is where
tools like Whale or Taskade slot in if you want a managed library, but a plain
Markdown file works to start.[^4][^5]

**Step 3 — Edit in the judgment.** The AI draft will be procedurally correct and
qualitatively naive. This is where you add the parts only you know: "the welcome
email must go out within 2 business hours of signature, because the data on
time-to-first-value says the first day is when retention is won or lost" (that is
tomorrow's lesson). Add the definition of good: "an A-grade kickoff means the
client has booked the call AND submitted the intake form before day two." Name the
failure mode: "the usual way this goes wrong is the intake form sits unfilled and
we start the kickoff call blind."

**Step 4 — Tag it for automation.** Ask the two-column question. Of these five
steps, which are deterministic enough to hand to an agent? Adding the CRM tag,
sending the templated welcome email, and creating the project from a template are
all trigger-plus-template operations, exactly the routine work that graduates into
automation. Checking that the contract is genuinely complete and personally
reviewing the kickoff are the parts you keep. You have just designed both an SOP
*and* your first automation target, from one narration.

The full runnable version of this, an SOP-template generator that takes a task
spec and emits a structured checklist SOP, is the Saturday
[[06-sat-build-sop-library-and-community-launch|build]] in `code-lab/1/`.

## Common mistakes experts see

1. **Writing essays instead of checklists.** The beautiful comprehensive document
   is skimmed once and never used. Imperative, verifiable, one line per step, like
   a pre-flight checklist.[^3]
2. **No trigger and no owner.** A procedure with no starting event is a
   suggestion; one with no owner rots into a lie within months.
3. **Documenting the whole business at once.** SOP projects die from scope. Write
   the one task you do most and hate most, first. Ship one, then the next.
4. **Systematizing judgment.** Turning a genuinely high-variance, judgment-defined
   task into a rigid checklist makes you worse. Systematize the stable and
   repeated; keep the judgment human.
5. **Treating the AI draft as finished.** AI removes the blank-page problem but
   does not know your quality bar. The draft is a well-spoken junior; you still
   supply the definition of "good."
6. **Writing once and never reviewing.** An unreviewed SOP silently goes stale and
   new people trust it. Owner plus last-reviewed date plus a review interval, or it
   becomes a hazard.

## Reflection questions

1. If you were unreachable for two weeks, what is the first thing that would break
   in your business? That is your first SOP. Why have you not written it yet?
2. Pick a task you do weekly. Is its variance low enough to systematize, or is it
   genuinely judgment each time? How can you tell the difference honestly, rather
   than using "it's judgment" as an excuse not to document?
3. For your single highest-frequency procedure, which steps are deterministic
   enough to hand to an agent, and which require your judgment? Where exactly is
   the line?
4. Gawande's checklist worked because it made skipping a step impossible, not
   because it taught anything new. What step do *you* skip under pressure that a
   checklist would catch?
5. What is your current single source of truth for "how we do things"? If the
   answer is "my memory," what is that costing you that you cannot see?

## My take (reviewer lens)

**Michael Seibel** would push back on the whole premise for a first-time founder
with three clients: you do not have a systematization problem, you have a "not
enough customers" problem, and a week spent writing SOPs is a week not spent
selling. He is right for the earliest stage, and the lesson concedes it in the
"when not to systematize" section. The honest scope: SOPs earn their keep the
moment you have done a thing five times and it is eating your week, not before.
Do not let a beautifully organized SOP library become the productive-feeling
procrastination that keeps you from the phone.

**Boris Cherny**, whose recent public work is fleet-scale agent management, would
flag the agent-run-SOP framing as the place most likely to bite you: a checklist
that a human runs safely is not safe for an agent, because the human silently
handles the edge cases the checklist omits and the agent does not. His correction
is the stricter-SOP point above, spelled-out failure modes and explicit stop
conditions, and it is load-bearing enough that Saturday's generator asks for them
by default.

**Ethan Mollick** would add the adoption angle: the reason SOPs fail is almost
never that they are badly written, it is that they are not where the work happens
and nobody is held to them. His research lens says the bottleneck is behavioral,
not documentary, so the "findable at the moment of need" property matters more
than the prose quality, and it is the property founders most neglect.

## Further reading

**Must-read**

- Atul Gawande, *The Checklist Manifesto*. The evidence and the philosophy for why
  checklists beat expertise-plus-memory. Read at least the WHO surgical-checklist
  chapter.[^3]

**Recommended**

- Michael Gerber, *The E-Myth Revisited*. The "work on the business, not in it"
  and franchise-prototype framing that motivates the whole SOP layer.[^1]
- SPP / productized-services operators on writing SOPs that capture "what good
  looks like," not just the clicks.[^2]

**Optional**

- Whale and Taskade on AI SOP generation, for the tooling if you want a managed
  library rather than Markdown files.[^4][^5]
- The Agent-S line of work on feeding SOPs into agents, if you want the research
  view of SOP-to-automation.[^6]

## Citations

[^1]: Michael E. Gerber, *The E-Myth Revisited*, summary and key concepts. Reading
Graphics. https://readingraphics.com/book-summary-the-e-myth-revisited/ — "work on
the business, not in it"; the franchise prototype as a systems-dependent, not
people-dependent, business. (Evergreen; corroborated by systemhub.com/your-own-e-myth/.)
[^2]: "Scaling Productized Services: 3-Pillar Quality Framework," SPP.
https://spp.co/blog/scaling-productized-services-framework/ — write SOPs that
capture what good looks like, include an A-grade example and the common failure
modes. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending;
corroborated by assembly.com/blog/productized-services.)
[^3]: Atul Gawande, *The Checklist Manifesto: How to Get Things Right*.
https://atulgawande.com/book/the-checklist-manifesto/ — the WHO surgical safety
checklist cut deaths by more than a third across eight hospitals. (Evergreen;
corroborated by NIH PMC review https://pmc.ncbi.nlm.nih.gov/articles/PMC4953332/.)
[^4]: "Discover 2026's Top AI Tools for Managing SOPs," Whale.
https://usewhale.io/blog/discover-2026s-top-ai-tools-for-managing-sops/ — AI SOP
generators cut documentation time from hours to minutes. (search-verified
2026-07-17; corroborated by Taskade below.)
[^5]: "What Is an SOP Generator? AI SOP Guide (2026)," Taskade.
https://www.taskade.com/blog/what-is-an-sop-generator — AI generation and
management of SOP libraries; automation of the drafting work. (search-verified
2026-07-17; corroborated by Whale above.)
[^6]: "Agent-S: LLM Agentic workflow to automate Standard Operating Procedures,"
arXiv 2503.15520. https://arxiv.org/pdf/2503.15520 — feeding SOPs into LLM agents
to improve controllability and reliability. (search-verified 2026-07-17;
corroborated by v7labs.com/automations/standard-operating-procedures-sops.)
[^7]: "Standard Operating Procedure: The 2026 Framework," F7i.
https://f7i.ai/blog/standard-operating-procedure-sop-the-definitive-guide-to-dynamic-industrial-workflows-in-2026
— the modern SOP as a dynamic digital workflow and trigger system, not a static
manual. (search-verified 2026-07-17; corroborated by creately.com/guides/ai-for-standard-operating-procedures/.)

_last_verified: 2026-07-17_
