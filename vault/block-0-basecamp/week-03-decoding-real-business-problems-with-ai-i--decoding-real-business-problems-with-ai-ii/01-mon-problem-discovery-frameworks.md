---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: 1
day_name: mon
session_slug: decoding-real-business-problems-with-ai-i
date_due: 2026-05-11
tags: [problem-discovery, jobs-to-be-done, christensen, ulwick, moesta, cagan, torres, disruption-theory, ai-product-strategy, opportunity-sizing]
sources:
  - ulwick-jtbd-odi-2024
  - moesta-lennys-podcast-jtbd-2023
  - torres-continuous-discovery-2021
  - cagan-transformed-2024
  - mckinsey-econ-potential-genai-2023
  - mckinsey-state-of-ai-2025
  - bcg-ai-value-gap-2024
  - bcg-ai-radar-2025
  - humane-pin-post-mortem-engadget-2024
  - rabbit-r1-post-mortem-digitalapplied-2026
  - character-ai-google-license-cnbc-2024
  - anysphere-cursor-500m-arr-techcrunch-2025
  - anysphere-cursor-1b-arr-2025
  - harvey-legal-ai-nextword-2025
  - christensen-institute-ai-disruption-2024
last_verified: 2026-07-17
word_count_target: 6000
---

# Problem discovery frameworks — JTBD, Christensen, and why most "AI opportunity" lists fail

## Why this matters

You are now the person in the room who decides *what* to build with AI, not just *how* to prompt it or stitch it together. That shift — from prompt operator to problem selector — is where most AI operators silently fail. They get handed a McKinsey slide that says generative AI is a $4.4 trillion opportunity,[^1] a BCG deck that says only 5% of companies generate measurable value from it,[^2] and an executive mandate that says "pick three places to pilot this quarter." They go run a few discovery interviews, read *The Innovator's Dilemma* on a flight, build a RICE-scored opportunity list, and ship something that gets used twice and quietly sunsets.

What they lack is not effort but a rigorous frame for *what counts as a real problem worth solving with AI*. They treat JTBD as a vocabulary rather than a discipline, confuse capability demos for problem statements, and rank opportunities by gut feel dressed up in a spreadsheet. This lesson is the antidote. By the end of it you will be able to (1) distinguish Christensen's story-based JTBD from Ulwick's outcome-driven JTBD and know when each is the right tool, (2) explain — on a whiteboard, to a skeptical VP of Product — why McKinsey-style opportunity lists systematically fail the JTBD test, (3) run a JTBD switch interview for an AI product without the common beginner mistakes that turn it into a feature-preference survey, (4) apply a checklist to any candidate AI project that catches the seven most common discovery failures before you burn a quarter, and (5) have a defensible view on the live controversy of whether JTBD is even the right lens for *AI-native* products — or whether it's a retrofit that smuggles yesterday's product thinking into a category where capabilities arrive before needs.

## Prerequisites

- You have read, or are willing to skim while we reference it, Bob Moesta's Lenny Rachitsky podcast appearance on JTBD (2023, ~70 min).[^3] This lesson does not require it — we explain what we use — but the interview will pay for itself by Wednesday.
- Familiarity with a "problem statement" discovery workshop. If you have ever written a PRD, user story, or product brief, you qualify.
- The substrate mental model from [[week-00-program-onboarding/01-mon-mental-model-of-llms|Week 0's LLM mental model]] — discovery for AI products presumes you know what the technology can and cannot do. Tomorrow's [[02-tue-when-ai-fits-a-problem|fit rubric]] formalizes that judgment.
- Optional: Teresa Torres, *Continuous Discovery Habits* (2021). Five years old and still the most operational treatment of weekly discovery rhythm. Torres shipped her own first AI products in 2025 and has publicly updated the framework in that context.[^4]

## Layer 1 — Three JTBD schools, and why the difference matters for AI

There is no single "Jobs To Be Done." There are at least three traditions with different parentage, different claims, and different techniques, and practitioners routinely bolt them together without noticing the seams. For an AI operator picking problems, the seams are where projects die.

### The Christensen / Moesta school — story-based JTBD

Clayton Christensen popularized the phrase "customers hire products to do a job" in *The Innovator's Solution* (2003), working from Bob Moesta's milkshake fieldwork at a fast-food chain. The case has been told so often it has lost its edge, so let's recover the precise claim. Moesta's team spent a day in a restaurant parking lot and realized a disproportionate share of milkshakes were bought before 9 a.m., consumed alone in a car, and ordered by commuters who were not especially hungry. The product they had "hired" had a job: *keep my left hand occupied and my stomach quiet until lunch, during a boring solo drive, without making a mess*. The competitors were not Wendy's or Dairy Queen; they were bananas (gone in two bites, leaves a peel), bagels (crumb everywhere), and doughnuts (sugar crash at 11 a.m.).[^5]

The operational move in Moesta's tradition is the *switch interview*: find someone who recently hired your product, press them backward through the timeline until you hit the trigger moment — the thing that happened in their life that made them aware of a struggle they had previously tolerated. Moesta's phrase, borrowed from Intercom's podcast with him, is *"freeze time at the spring dug into my back moment."*[^6] The output is a job story — narrative, causal, anchored in a specific human's specific day. Christensen's definition of the job is functional-plus-emotional-plus-social: *when I [situation], help me [motivation], so I can [expected outcome]*.

### The Ulwick / ODI school — outcome-based JTBD

Tony Ulwick developed Outcome-Driven Innovation (ODI) at Strategyn starting in 1991 — a full decade before Christensen labeled the pattern "JTBD" and credited Ulwick in *The Innovator's Solution*.[^7] ODI starts from a different premise: if a customer is hiring a product to get a job done, the *job* is stable across time and technology (people have been hiring things to "listen to music on the go" since the Walkman), but the *desired outcomes* — the measurable metrics by which the customer judges whether the job got done well — are what innovation should target. Ulwick's canonical example: for the job of *cutting the grass*, the desired outcomes include "minimize the time it takes to cut the grass," "minimize the likelihood of damaging the lawn," "minimize the noise level during cutting." Each is a measurable, direction-plus-metric-plus-object statement. An ODI study produces 50–150 such outcome statements per job, then quantitatively surveys hundreds of customers to find *underserved* outcomes (high importance, low satisfaction) — the innovation targets.[^8]

The two schools feel similar at first and are fiercely distinct in practice. A Moesta-style engagement is qualitative, narrative, focused on understanding *why someone switched*. An Ulwick-style engagement is quantitative, structured, focused on *which metrics are under-delivered*. Moesta gives you a story you can put in a pitch deck. Ulwick gives you a ranked backlog of 150 rows with statistical significance. Both are real JTBD; they answer different questions.

### Why the seams matter for AI product selection

For AI work, the choice between schools is structural. AI capabilities — draft a document, extract structured data from unstructured text, generate a plan, review a diff — tend to improve *outcomes* on existing jobs rather than replacing jobs wholesale. If your candidate project is *"use LLMs to help sales reps write better follow-up emails,"* a Moesta switch interview will tell you a story ("our rep Sarah had a prospect go cold after a demo, she wrote a follow-up at 11 p.m., it fell flat, she switched to using ChatGPT on her phone the next morning") that is compelling but doesn't tell you *which* metric of follow-up-email-writing is underserved. An Ulwick outcome map will tell you that "minimize time to produce a follow-up email that references the specific objection raised in the demo" is a high-importance, low-satisfaction outcome for 68% of AEs surveyed. The story sells the project to a VP; the outcome map tells you what to actually build and how you'll know it worked.

Operator rule: **run Moesta first, Ulwick second.** Switch interviews surface whether there's a real struggle worth caring about. Outcome decomposition tells you what to build, how to measure it, and what the bar is. Skipping Ulwick because "it's heavy" is how you end up shipping a feature that writes follow-up emails faster without checking whether speed was ever the underserved outcome. (Often it isn't — the underserved outcome is *specificity to the prospect's stated objection*, which is an entirely different engineering problem.)

## Layer 2 — Christensen disruption theory, applied to 2024–2026 AI

Christensen's *disruption theory* is a separate construct from JTBD, though both bear his name. It is a theory of how *low-end* and *new-market* entrants unseat incumbents. Low-end disruption attacks the most overserved, least profitable customers with a "good enough" product at a lower price. New-market disruption creates a new value network of customers who previously did not consume the incumbent's product at all — they used nothing, or they used a distant substitute.[^9] The diagnostic, per the Christensen Institute's 2024 reassessment of AI, is that generative AI *itself* is not disruptive; the *business model wrapped around it* is what determines disruption.[^10] That reframe is the single most important sentence in this section. Hold it while we apply it.

**Case 1 — AI coding: low-end disruption of who?** Cursor (Anysphere) hit $100M ARR by January 2025, $500M ARR by June 2025, crossed $1B annualized by November 2025, and reached roughly $4B annualized by June 2026 — about $2.6B of it enterprise — at which point SpaceX agreed to acquire the company for $60B in stock, the largest acquisition of a venture-backed startup ever.[^11][^12][^13] On its face the product looks like disruption of IDEs (JetBrains, VS Code). It isn't. VS Code is free; you don't disrupt a free incumbent on price. Cursor is competing on *developer outcomes*: lines of working code shipped per hour, time from bug report to fix, onboarding time for new hires. The underserved outcome was "minimize the time between understanding what code should do and having working code exist." Whom is that disrupting? Not IDE vendors — the outsourced-development offshore firms and junior-developer labor markets whose core product was "cheap hands to write the obvious code." By mid-2026 the category has its own Gartner Magic Quadrant for Enterprise AI Coding Agents, with Cursor named a Leader alongside OpenAI, Anthropic, and GitHub.[^25] The displacement shows up in reduced junior-dev hiring at firms adopting Cursor-class tools, not in IDE market share — and the endgame, at least for the category leader, was acquisition by a compute-and-model conglomerate, not IPO.

**Case 2 — Legal AI: the billable-hour problem.** Harvey reached enterprise adoption at Reed Smith, Nixon Peabody, and other Am Law 100 firms in 2024–2025, positioned as an AI platform for legal professional services.[^14] Here Christensen's theory gives you a sharper question than "will lawyers be replaced?" The question is: *which business model breaks first?* Billable-hour firms face an incentive inversion — AI that cuts a 6-hour memo to 40 minutes *reduces* revenue under hourly billing. Seventy-one percent of clients now prefer flat fees, and flat-fee billables grew 34% between 2016 and 2025.[^14] The disruption is not of lawyers but of the *hourly pricing model*, which then cascades into associate headcount and the pyramid structure of Big Law. Harvey is the instrument; the disrupted value network is the one that priced junior-associate attention as a scarce resource.

**Case 3 — Consumer AI companions: the disruption that wasn't.** Character.AI raised at a $1B+ valuation on the premise that AI companions were a new-market disruption — people who didn't previously "consume" a therapist or a friend could now hire an AI for that job. By August 2024, the company had licensed its models to Google for $2.7B, had its founders re-hired by Google, and exited the frontier-model race to pivot to a consumer chatbot platform on top of Meta's Llama.[^15] The Christensen diagnostic would have flagged this in 2023: *what is the value network, and does it have a moat?* "AI chatbot companions" had negligible barriers to entry — any team with API access could replicate the product. The JTBD diagnostic would have flagged a different problem: the "job" being hired for (companionship, emotional regulation, roleplay) had no stable outcome metric the product could optimize against, and the demographic doing the hiring was partly teenagers, a segment that would later produce the lawsuits Google and Character.AI settled in January 2026.[^15] *Both* frames flagged the project; neither was applied with enough rigor at founding.

The pattern across the three cases: AI capability lands, and the question is not "is this a good demo?" but "which value network does the wrapped business model actually attack, and is that attack sustainable?" That is Christensen 101 — applied to AI, still load-bearing.

## Layer 3 — Why "AI opportunity" lists fail the JTBD test

McKinsey's $4.4 trillion figure gets cited constantly. Let's look at it honestly. The 2023 MGI report "The economic potential of generative AI" identified 63 use cases across 16 business functions and estimated $2.6T–$4.4T in annual value, with customer operations, marketing and sales, software engineering, and R&D holding the largest pools.[^1] The 2025 "State of AI" found that only 39% of organizations can link any EBIT impact to AI, and for most, the impact is below 5% of EBIT; in 2025 only about one-third of organizations reported scaling AI across the enterprise.[^16] BCG's 2025 AI Radar is sharper still: only 5% of companies generate measurable value from AI, 60% achieve no material value, and 35% scale efforts without going far or fast enough.[^2][^17]

Here is where a problem-discovery discipline pays for itself. The opportunity lists fail the JTBD test on three specific dimensions:

**(1) Aggregation erases the job.** "Customer operations: $400B of value" is a value pool, not a job. Customer operations contains dozens of jobs — resolve billing dispute, escalate outage, diagnose return reason, route to right specialist — each with distinct outcomes, distinct underserved metrics, and distinct incumbents. Hiring "AI for customer operations" is like hiring "transportation for my day" — the right tool depends on whether the job is a 2-mile errand or a 2000-mile move. When you implement a consultant's opportunity list literally, you build horizontally across an aggregate and find that no individual job was well-enough defined to measure improvement on.

**(2) Outcome specificity is absent.** Ulwick's test: can you state the desired outcome as *direction + metric + object of control + contextual clarifier*? "Reduce handle time in customer service" is not an outcome; it's a KPI dressed as one. The real outcomes are "minimize the likelihood that a billing dispute escalates to a supervisor in the first call" or "minimize the number of times a customer has to re-state their account history during a single interaction." An opportunity list that reports dollar value against KPIs rather than ODI-style outcomes is missing the layer that tells you *what to build*.

**(3) Integration cost is systematically omitted.** The McKinsey and BCG numbers are gross potential. They do not discount for the change-management, data, and process work required to realize them. BCG's own data shows leaders put 10% of AI investment into algorithms, 20% into tech and data, and 70% into people and processes[^2] — which means 90% of the work is not the AI. Opportunity lists that price only the algorithmic layer are off by a factor of ten on the implementation side. The gap between $4.4T potential and 5% of companies realizing value[^1][^17] is largely the unacknowledged 70%.

> My take: the McKinsey number is not dishonest — it's an unconditional upper bound computed from a reasonable methodology. It is, however, *operationally useless* for an AI operator. Treating it as a target produces exactly the value gap BCG measures. The right use of the number is political (it gets you budget); the wrong use is planning (it gets you pilots that never scale).

## Layer 4 — Problem-first vs technology-first: the discovery discipline

Marty Cagan's *Transformed* (March 2024) is the current canonical text on the "product operating model," and its central claim is that modern product companies are distinguished not by what they sell but by how they decide what to build.[^18] Cagan's four-part AI opportunity assessment — value, viability, usability, feasibility — is not new as vocabulary, but the demand that you hit all four on an AI opportunity is binding: teams routinely ship AI features that are technically feasible, demonstrably better for the user, but *commercially unviable* because the inference costs destroy margin, or usable in a demo but unusable in the production workflow because the model output requires review no one has time for.[^19]

Teresa Torres's *Continuous Discovery Habits* (2021) supplies the rhythm: weekly touches with customers, a persistent opportunity-solution tree that connects business outcomes to opportunities to candidate solutions to assumption tests, and a refusal to let discovery collapse into a one-time kickoff.[^4] Torres's 2025 update — delivered as masterclasses and in the building of her own AI products — argues that AI *increases* the need for continuous discovery because AI features have unusually high variance in how they land with users, and you cannot infer from a prototype demo how the feature will behave after two weeks of actual use.[^20]

The operator distillation is this. **Technology-first** says: we have AI; what can we do with it? It produces opportunity lists sorted by capability. It is the dominant mode in 2024–2026 because the capability curve is moving so fast that it feels like leaving value on the table to start anywhere else. **Problem-first** says: we have a customer with an underserved outcome on a job they already have; does AI help? It produces opportunity lists sorted by severity of struggle. Problem-first is slower at generating hypotheses and faster at killing bad ones. Over a year, problem-first ships fewer projects and more value — which is exactly the signature of the 5% of companies BCG identifies as AI leaders.[^17]

There is an honest counter-argument here, and it deserves stating at full strength. We'll come back to it as the live controversy.

## Layer 5 — How to run a JTBD switch interview for an AI product without screwing it up

This is the most operational section. Most JTBD interviews an AI operator will run in the wild are bad — not because the framework is complex but because the mode of inquiry runs against ordinary instincts. Four failure patterns dominate.

**Failure 1: asking about preferences instead of switches.** "Would you use an AI that could draft your follow-up emails?" is useless. You get a social answer. The Moesta move is: "Tell me about the last time you sent a follow-up email you were unhappy with. When exactly? Who was the prospect? What had just happened? What did you do first? What did you try second?" You are reconstructing a specific timeline of a specific switch.

**Failure 2: letting the interviewee narrate at the goal level.** "I wanted to close the deal" is the goal, not the job. The job is hidden three layers down: "I wanted to produce a follow-up email that referenced the specific objection he raised on the call so that when my VP reviewed my forecast I could show the account was still alive." Moesta's technique, delivered verbatim on the Lenny Rachitsky episode: *"push past the first three why's."*[^3]

**Failure 3: interviewing hypothetical customers.** The switch interview's validity comes from the interviewee having actually switched. If you're interviewing people who *might* adopt your AI product, you are running a concept test, not a JTBD interview. For AI products in categories that don't exist yet, find an analog — someone who switched from manual drafting to ChatGPT in their personal workflow, or from a consulting firm to a SaaS tool for the adjacent job. The switch is what exposes the triggering struggle.

**Failure 4: forgetting the "forces of progress" frame.** Moesta's model of switching has four forces acting simultaneously: *push* (what's painful about the current solution), *pull* (what's attractive about the new one), *anxiety* (what could go wrong with switching), and *habit* (inertia of the current way).[^6] For AI products, anxiety is usually the dominant force and usually the one interviewers ignore. "Will it hallucinate on my client's data?" "Will my partner find out I'm using AI to draft her emails?" "Will my team think I'm cheating?" Anxiety, if not surfaced and addressed, kills adoption independently of whether the pull is strong.

A decent interview protocol for an AI work context — 45 minutes, recorded, one interviewer, one notetaker:

1. **Set the frame** (2 min): "I'm studying how people actually handle [job]. I'm not selling anything. I want your real story, mistakes and all."
2. **Anchor on a specific recent switch** (5 min): "Tell me about the most recent time you used [AI tool / new approach] for [task]. What's the date? What was the thing that made you reach for it that time?"
3. **Walk back to the trigger** (10 min): "What was happening the day before? The week before? When did you first become aware this was a problem? What had you been doing instead?" You are looking for the spring-dug-into-my-back moment.
4. **Map the four forces** (15 min): push (what was broken with the old way), pull (what drew you to the new), anxiety (what you worried about), habit (what almost kept you where you were). Ask for each: "What was the specific moment you felt that?"
5. **Surface the hired job** (8 min): "If [AI tool] disappeared tomorrow and you had to get [outcome] done, what would you reach for? Why that, not something else?" The competitive set this surfaces is often not what you expected.
6. **Check for outcome metrics** (5 min): "How did you know it had worked? What were you comparing against?" This is your bridge to Ulwick outcomes. Concrete outcomes sound like: in finance — "minimize time to reconcile a month-end variance"; in ops — "minimize the number of open incidents older than 24 hours at shift handover"; in legal — "minimize cited-authority errors per memo page." Direction + metric + object + context, never "improve accuracy."

Run five of these for any AI project before writing a PRD. The first two will be bad; the third will surprise you; the fourth and fifth will reveal the pattern.

## Layer 6 — Real case: Humane AI Pin as a problem-discovery failure

Humane shipped the AI Pin in April 2024 at $699 plus $24/month, having raised $230M at a $850M valuation. By early 2025 the product was discontinued; HP acquired the assets for $116M, a ~$115M write-down on the raised capital.[^21][^22] The failure has been dissected for hardware reasons — two-to-four-hour battery life, a heavy magnet-held device that dragged on clothing, a projector that was unreadable in sunlight, voice response latency that made basic queries feel broken.[^21] Those were symptoms. The problem-discovery failure was upstream.

Run the JTBD diagnostic on the Pin with what Humane actually shipped:

- *What job were customers hiring the Pin to do?* The marketing said "ambient computing" — freeing you from your phone. But the switching cost was extreme: you didn't *replace* your phone; you carried a second device. The job "free me from my phone" was not a job anyone had been struggling with in a way that could absorb a $699 + $24/month + 4-hour-battery cost, given the phone they already owned was free at the point of use. The real job candidates — "help me capture an idea while I'm walking without pulling out my phone," "help me translate a menu in real time" — each had cheaper, more reliable incumbents (voice memos, Google Lens).
- *What were the desired outcomes, in Ulwick's sense?* Unknown. There is no public evidence of Humane having run outcome decomposition. The product optimized for a vision ("post-smartphone computing") rather than measured outcomes on any specific job.
- *What was the switch pattern?* Also unknown. Humane's user research, insofar as it has been reported, was demo-driven; TED-talk-grade presentation rather than switch-interview-grade fieldwork.[^22] The device shipped to reviewers who were immediately unable to complete basic tasks — setting a timer, answering questions correctly — because no switching journey had been instrumented to reveal the gap.

The Inc. post-mortem reports that Humane's founders were documented as preferring internal positivity and disregarding warnings about battery life and power consumption during design.[^23] That is a culture problem, but also a *discovery* problem: a product organization optimized for conviction rather than disconfirmation cannot run honest switch interviews, because the evidence from switch interviews is, by design, mostly disconfirming. You go in hoping to find a struggle; most conversations reveal the struggle isn't actually there, or isn't severe enough, or has a better competitor than the one you built around.

The Rabbit R1 tells a near-identical story 90 days later. CES 2024 demo showed an autonomous agent ordering Ubers and booking restaurants via a "Large Action Model." Shipped product sold 100K units on pre-order strength, then couldn't reliably perform the demo tasks; voice latency reached 10 seconds; third-party app integrations were buggy or absent. By September 2025, a year-plus post-launch, Rabbit had pivoted RabbitOS 2 away from assistant duties entirely.[^24] The discovery failure: treating viral demo excitement as market validation, and shipping locked hardware before the JTBD was tested. "Hardware AI products are locked into their launch-day capabilities for months or years," the post-mortem notes; "when users discovered the gap between demo promises and actual performance, the products could not evolve fast enough to close it."[^24]

Pattern: in both cases, the JTBD wasn't *wrong* per se — some ambient capture / autonomous agent job plausibly exists — it was *un-instrumented*. No one had run switch interviews that revealed the real competitors (phones that already existed and worked), the real anxieties (looking weird, being overheard), or the real underserved outcomes (probably not speed, probably privacy and discretion). The companies did not so much pick the wrong job as fail to discover any job at all, and shipped at hardware timescales against a JTBD hypothesis that a $20K study could have killed in six weeks.

## Layer 7 — Live controversy: is JTBD still the right lens for AI?

Here is the disagreement worth staking a position on. Two named positions, both held seriously.

**Position A — JTBD is evergreen; AI doesn't change the need for it.** Ulwick, Moesta, Torres, and Cagan all argue this in 2024–2025 writing and interviews.[^4][^18][^20] The argument: jobs are stable across technology generations. People were hiring something to "get from point A to point B" before cars, during cars, and will be after cars. AI is a new class of solution, not a new class of job. Skipping JTBD because "AI is different" produces Humane Pins and Rabbit R1s. The evidence base — McKinsey's 39% EBIT linkage, BCG's 5% measurable-value rate[^16][^17] — reads as *failure to apply JTBD*, not failure of JTBD.

**Position B — AI is capability-first; JTBD retrofits the story post-hoc.** The counter, articulated in various forms by a16z partners, by parts of the OpenAI product organization, and implicitly by the Character.AI / Replit / Cursor founding pattern, is that AI creates jobs that *did not exist* before the capability existed. No one was "hiring" something to generate a draft contract in 30 seconds because no product that cheap and fast existed; no one was "hiring" something to pair-program at the level of a mid-level engineer at $20/month because that was a science-fiction SKU. The Cursor founders didn't find an underserved outcome on existing IDE users; they built a new mode of coding that users then retroactively described as having needed. In this view, JTBD applied too early produces incrementalism (faster email, better search); the breakout AI products come from capability-first experimentation and find their JTBD post-launch.

**My position:** Position A is right *for selection* and Position B is right *for expansion*. The selection decision — do we start a project here, yes or no — needs JTBD discipline, because capability-first selection at the portfolio level produces the hit rate in the McKinsey and BCG numbers (single-digit percent of companies realize material value). You cannot run a portfolio on "let's build whatever the model is newly capable of"; the hit rate is too low and the integration costs too high. But *within* a project, once JTBD has identified a real struggle, capability-first expansion is how you find the product surface that matters. Cursor is instructive: the initial JTBD was tight and recognizable — "help me write code faster with fewer lookups" — and only *after* product-market fit did the capability-first expansion (agent mode, background tasks, codebase-wide refactors) unlock the $500M → $1B → $4B ARR run that ended in the June 2026 SpaceX acquisition.[^12][^13] Flipping the order — capability-first selection followed by JTBD retrofit — is the Humane pattern.

An AI operator who says "we are capability-first" is usually either (a) a foundation-model lab, where the economics genuinely work that way, or (b) running the Humane playbook and hasn't noticed.

## Problem-discovery checklist for AI projects

Use this before any AI project passes the "should we start" gate. If you cannot answer "yes" to all seven, the project is not ready.

1. **Named job.** Can you state the job the customer is hiring AI to do, in Christensen's "when I [situation], help me [motivation], so I can [expected outcome]" format? If the job statement refers to a technology ("use GPT to…"), it is not a job statement.
2. **Documented switches.** Have you interviewed at least five people who have *actually switched* — from a prior solution to an AI solution for the adjacent job — and mapped the four forces for each? If all your interviews are hypothetical, you have a concept test, not a JTBD study.
3. **Quantified outcomes.** Do you have 10–30 outcome statements in Ulwick's format, and importance/satisfaction data on at least a subset, showing which outcomes are underserved?
4. **Named competitors, including non-obvious ones.** What does the customer reach for if your AI disappears tomorrow? If the answer is only "a human" or only "another AI," you haven't probed. The honest answer usually includes a non-AI substitute (a checklist, a colleague, a policy).
5. **Anxiety surface.** What specific anxieties did switch interviews surface, and how will the product address each? For AI: hallucination risk, data privacy, social acceptability, loss of skill, auditability.
6. **Cagan's four tests.** Value (demonstrably better for the customer, not just technically impressive), viability (inference cost, compliance, channel), usability (fits existing workflow, not just a demo), feasibility (team can ship it, not just POC it).[^18][^19]
7. **Kill criteria.** What observation, between now and 90 days from launch, would cause you to kill the project? Specify metric + threshold + decision, e.g., "if <40% of week-4 switch interviews confirm the struggle statement, or if LLM-judge rubric pass-rate on the held-out eval set stays below 70% after two prompt/retrieval iterations, we kill." If the answer is "none we've specified," you have a religious commitment, not a project.

## Exercise — produce your artifacts

**Time:** 90 minutes, one pass. You will produce two artifacts you can reuse for every AI project you evaluate this year.

**Inputs you need:**
- One AI project you are currently considering, or have been asked to consider, at your company or for yourself.
- One customer or user — real, reachable — who has already done a switch in the adjacent space. (If you cannot name one, that is itself the first finding.)

**Artifact 1 — one-page JTBD interview guide.** Write, as a single page:
- The job hypothesis, in Christensen format.
- Three switch-anchor questions (e.g., "tell me about the last time you…").
- Four-force probe questions, one per force (push, pull, anxiety, habit).
- Three outcome-probing questions ("how did you know it worked?").
- One hidden-competitor question ("if this went away tomorrow, what next?").

Constraint: fit on one page, ≤400 words. The constraint forces precision.

**Artifact 2 — three problem-statement options, filtered.** Write three candidate problem statements for the project, in the form:

> *When [situation], [customer segment] struggles to [struggle verb phrase] because [root cause]. Today they cope by [current solution]; this is unsatisfactory because [underserved outcome]. If we could [capability hypothesis], they would [measurable change].*

Now run each through the 7-item checklist above. Score each statement 0/1 on each item. The statement with the highest score is your candidate; if none scores above 5/7, your project isn't ready.

**Deliverable:** both artifacts in a single doc, saved and dated. You will return to this doc at the end of Week 3 to audit whether your subsequent decisions stayed consistent with the problem statement you picked, or silently drifted toward the capability you wanted to use.

## Common mistakes experts see

- **Treating JTBD as a vocabulary.** Using phrases like "the job to be done is…" in a deck without ever having run a switch interview. The framework is the fieldwork, not the noun.
- **Running opinion interviews.** "Would you use this?" is not a JTBD interview. It is an opinion poll with a sample size of one.
- **Skipping outcome decomposition.** Moesta gets you the story; Ulwick gets you the metrics. If you only do the first, your PM team has nothing to build against.
- **Benchmarking against AI competitors only.** The real competitor for an AI scheduling tool might be "my assistant's Google Calendar discipline," not "the other AI scheduling tool." Non-AI substitutes are the ones that silently win.
- **Treating opportunity-size decks as project briefs.** McKinsey and BCG numbers are portfolio signals, not project plans. They don't survive contact with a specific customer's specific day.
- **Launching hardware before JTBD is tested.** Humane and Rabbit burned $100M+ each proving this. Software can pivot; hardware can't.
- **Ignoring anxiety.** For AI specifically, the switching anxiety (hallucination, privacy, social acceptability) is often decisive and usually under-instrumented in discovery.

## Reflection — questions your artifacts should answer

These aren't reflection filler — they're the checks you should be able to pass before you defend your problem statement in a review.

1. If your chosen problem statement is right, what should the switch-interview transcripts show, specifically, in the "anxiety" force? If they don't, what does that imply?
2. Name a non-AI competitor for your candidate AI product that a naive opportunity list would have missed. How did you find it?
3. Your project's best-case outcome, in ODI format (direction + metric + object + context). Is this outcome *underserved*, or is it already being delivered by an existing solution you're attacking on a different axis (price, integration, brand)?
4. If, in six months, BCG's 5%-of-companies-realize-value number applies to your project and you're in the 95%, what will the retrospective identify as the discovery failure? (Answering this now is a pre-mortem.)
5. Where does your project sit on the JTBD vs capability-first controversy — Position A, Position B, or the hybrid position? What evidence would flip you from one to the other?

## My take (reviewer lens) — where this lesson can be pushed back on

Five specific disagreements a skeptical reviewer could raise:

- **"Switch interviews don't scale to AI products with zero existing adopters."** Fair — for truly novel categories (generative video, agentic browsing in 2023), switch interviews on the target product are impossible. The answer is to interview switchers on the *adjacent* job, not to abandon the method. But the lesson could be more explicit that the first year of a category-creating AI product runs on capability bets with loose JTBD hypotheses, and that this is defensible *at the project level* even as it remains indefensible at the portfolio level. The position I staked glosses the category-creation edge case.
- **"Ulwick outcome decomposition is overkill for a 4-person startup."** Also fair. A full ODI study runs roughly $50K–$500K (operator estimate, based on Strategyn-tier engagement scopes — Ulwick/Strategyn does not publish a rate card) and is inappropriate for early-stage work. The operator move is a two-hour team exercise generating 10–15 candidate outcomes and cheap-testing importance via landing-page or sales-call instrumentation. The lesson treats ODI more reverentially than a startup context warrants.
- **"Christensen disruption theory has been contested since at least 2014."** Jill Lepore's *New Yorker* critique, and the subsequent academic pushback, argues the theory over-predicts disruption and under-explains why incumbents often win. The 2024 applications here are cleaner than the historical cases Lepore attacked, but a rigorous treatment would note that disruption theory is a useful hypothesis generator, not a settled law.
- **"The McKinsey / BCG critique is too harsh — those reports have operational value."** They do, as executive-education artifacts and budget-justification tools. The critique in this lesson is about their use as project briefs, which is a misuse rather than a flaw of the reports. A fairer framing would distinguish the two uses.
- **"The Position A / Position B controversy collapses too neatly into 'A for selection, B for expansion.'"** Possibly. The harder version of Position B is that *selection itself* is sometimes capability-first in genuinely novel categories, and the JTBD retrofit isn't a mistake — it's the correct order when the capability is unprecedented. The tidy hybrid I proposed may be a selection-biased reading from an enterprise vantage; a YC-stage founder in a novel AI category might correctly run capability-first selection and be right.

## Further reading

**Must-read**
- Bob Moesta on Lenny Rachitsky's podcast, *The ultimate guide to JTBD* (Aug 2023).[^3] The interview is more operational than any book chapter.
- Tony Ulwick, *What Is Jobs-to-be-Done?* (2024 update on jobs-to-be-done.com).[^7] Ulwick's own account of the theory's history and how ODI differs from Christensen.
- McKinsey Global Institute, *The economic potential of generative AI* (2023, with 2024–2025 updates).[^1][^16] Read critically, as instructed above.
- BCG, *Are You Generating Value from AI? The Widening Gap* (2025).[^17] The 5% number is the operator benchmark.

**Recommended**
- Marty Cagan, *Transformed: Moving to the Product Operating Model* (March 2024).[^18] For the discovery discipline's institutional form.
- Teresa Torres, *Continuous Discovery Habits* (2021).[^4] Five years old and still the cleanest rhythm-level treatment.
- Christensen Institute, *What does Disruptive Innovation Theory have to say about AI?* (2024).[^10] The Institute's own reassessment, more disciplined than most secondary commentary.

**Optional**
- Rabbit R1 post-mortems: DigitalApplied (2026),[^24] Humane Pin coverage: Engadget (2024),[^21] Inc. on Humane culture (2024).[^23]
- Character.AI / Google deal coverage: CNBC, Bloomberg, Axios (August 2024).[^15]

## Citations

[^1]: McKinsey Global Institute, *The economic potential of generative AI: The next productivity frontier*, 2023 (value range $2.6T–$4.4T across 63 use cases). https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier

[^2]: BCG, *From Potential to Profit: Closing the AI Impact Gap*, 2025 — investment allocation rule (10% algorithms / 20% tech & data / 70% people & processes); agentic AI 17% of AI value in 2025, projected 29% by 2028. https://www.bcg.com/publications/2025/closing-the-ai-impact-gap

[^3]: Lenny Rachitsky, *The ultimate guide to JTBD | Bob Moesta (co-creator of the framework)*, Lenny's Podcast, Aug 24 2023. https://www.lennysnewsletter.com/p/the-ultimate-guide-to-jtbd-bob-moesta

[^4]: Teresa Torres, *Continuous Discovery Habits*, Product Talk LLC, 2021; Product Talk events and writing 2024–2025 on applying CDH to AI products. https://www.producttalk.org/

[^5]: Bob Moesta / Re-Wired Group, *Milkshakes in the Morning — The JTBD Story*, case write-up. https://therewiredgroup.com/case-studies/milkshakes/

[^6]: Intercom, *Bob Moesta on unpacking customer motivations with Jobs-to-be-Done*, Inside Intercom podcast. https://www.intercom.com/blog/podcasts/bob-moesta-on-unpacking-customer-motivations-with-jobs-to-be-done/

[^7]: Tony Ulwick, *What Is Jobs-to-be-Done?* and *The History of Jobs-to-be-Done and Outcome-Driven Innovation*, jobs-to-be-done.com (2024). https://jobs-to-be-done.com/what-is-jobs-to-be-done-fea59c8e39eb ; https://jobs-to-be-done.com/the-history-of-jobs-to-be-done-and-outcome-driven-innovation-a2fdfd0c7a9a

[^8]: Strategyn, *Jobs to Be Done (JTBD): The Original Framework by Tony Ulwick*. https://strategyn.com/jobs-to-be-done/

[^9]: Harvard Business School Online, *What Is Disruptive Innovation Theory? 4 Key Concepts*. https://online.hbs.edu/blog/post/4-keys-to-understanding-clayton-christensens-theory-of-disruptive-innovation

[^10]: Christensen Institute, *What does Disruptive Innovation Theory have to say about AI?* and *AI and Disruptive Innovation*, 2024. https://www.christenseninstitute.org/blog/what-does-disruptive-innovation-say-about-ai/ ; https://www.christenseninstitute.org/blog/ai-and-disruptive-innovation/

[^11]: TechCrunch, *Cursor's Anysphere nabs $9.9B valuation, soars past $500M ARR*, Jun 5 2025. https://techcrunch.com/2025/06/05/cursors-anysphere-nabs-9-9b-valuation-soars-past-500m-arr/

[^12]: Bloomberg reporting via Contrary Research's Cursor business breakdown (late 2025 / early 2026): ~$1B ARR reached November 2025, >1M daily active users, ~50K businesses on the platform — https://research.contrary.com/company/cursor. ~$4B annualized (~$2.6B enterprise) by June 2026: Dealroom, *Cursor tops $4B annualized revenue* (June 2026) https://app.dealroom.co/news/note/cursor-tops-4b-annualized-revenue-june-2026 (verified 2026-07-17).

[^13]: CNBC, *SpaceX to acquire the AI coding startup Cursor for $60 billion*, Jun 16 2026. https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html ; TechCrunch, *SpaceX to acquire Cursor for $60B in stock, days after blockbuster IPO*, Jun 16 2026. https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/ — all-stock deal, option signed 2026-04-21, expected close Q3 2026. Verified 2026-07-17.

[^14]: Nextword / Enterprise AI Trends, *Legal AI adoption is soaring (ft. Harvey)*, 2025. https://nextword.substack.com/p/legal-ai-landscape-and-harvey-ai-strategy

[^15]: CNBC, *Ex-Google engineers who founded Character.AI rejoin company with new AI partnership*, Aug 2 2024; Btimes, *Character.ai Quits AI Model Race After $4 Billion Google Deal*, Oct 3 2024; Fortune, *Google and Character.AI agree to settle lawsuits over teen suicides linked to AI chatbots*, Jan 8 2026. https://www.cnbc.com/2024/08/02/ex-google-engineers-from-characterai-re-join-company-with-ai-partnership-.html ; https://www.btimesonline.com/articles/169707/20241003/character-ai-quits-ai-model-race-after-4-billion-google-deal-shifts-focus-to-consumer-chatbot-platform.htm ; https://fortune.com/2026/01/08/google-character-ai-settle-lawsuits-teenage-child-suicides-chatbots/

[^16]: McKinsey, *The state of AI in 2025: Agents, innovation, and transformation* (39% EBIT linkage; one-third scaling). https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

[^17]: BCG, *Are You Generating Value from AI? The Widening Gap*, 2025 (5% measurable value / 60% no material value / 35% scaling without going far or fast). https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap

[^18]: Marty Cagan, *Transformed: Moving to the Product Operating Model*, Wiley / SVPG, Mar 12 2024.

[^19]: Silicon Valley Product Group, *AI Product Management 2 Years In*, 2024, and airfocus summary of Cagan's value/viability/usability/feasibility test for AI. https://www.svpg.com/ai-product-management-2-years-in/ ; https://airfocus.com/blog/ai-product-management-marty-cagan/

[^20]: Product Talk / airfocus, *Behind the build: Teresa Torres' first AI product*, 2025 webinar and write-up. https://airfocus.com/resources/events/behind-the-build-teresa-torres-first-ai-product/

[^21]: Engadget, *The Humane AI Pin debacle is a reminder that AI alone doesn't make a compelling product*, 2024. https://www.engadget.com/ai/the-humane-ai-pin-debacle-is-a-reminder-that-ai-alone-doesnt-make-a-compelling-product-190119112.html

[^22]: TechResearchOnline, *The Humane AI Pin Failure: A $700 Lesson in Product Strategy and Market Reality*; ComplexDiscovery, *The End of Humane AI Pin: HP's Strategic Shift Toward AI Integration* (HP acquisition at $116M). https://techresearchonline.com/blog/humane-ai-pin-failure/ ; https://complexdiscovery.com/the-end-of-humane-ai-pin-hps-strategic-shift-toward-ai-integration/

[^23]: Inc., *Humane Founders' Toxic Positivity May Have Killed Its AI Pin Device*, 2024. https://www.inc.com/kit-eaton/humane-founders-toxic-positivity-may-have-killed-its-ai-pin-device.html

[^24]: DigitalApplied, *AI Product Failures 2026: Sora, Humane & Rabbit R1* (Rabbit sold ~100K units on CES demo; voice latency up to 10s; RabbitOS 2 pivot Sep 2025). https://www.digitalapplied.com/blog/ai-product-failures-2026-sora-humane-rabbit-lessons — direct fetch bot-blocked; domain confirmed active and publishing through mid-2026.

[^25]: OpenAI, *OpenAI named a Leader in enterprise coding agents by Gartner* (2026 Gartner Magic Quadrant for Enterprise AI Coding Agents; Leaders include OpenAI, Anthropic Claude Code, GitHub Copilot, and Cursor). https://openai.com/index/gartner-2026-agentic-coding-leader/ Verified 2026-07-17.

_last_verified: 2026-07-17_
