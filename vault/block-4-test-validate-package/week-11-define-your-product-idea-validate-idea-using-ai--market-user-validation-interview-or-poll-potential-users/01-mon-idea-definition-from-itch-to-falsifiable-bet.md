---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 1
day_name: mon
session_slug: define-your-product-idea-validate-idea-using-ai
date_due: 2026-07-27
tags: [idea-definition, falsifiable-bets, riskiest-assumption, kill-criteria, assumption-mapping, desirability-viability-feasibility, painkiller-test, agent-products, motivated-reasoning, pre-registration]
sources:
  - cagan-four-big-risks
  - bland-testing-business-ideas
  - fitzpatrick-mom-test
  - yc-rfs-2026
  - nyu-shipping-not-asking-2026
  - andres-max-validate-2026
  - anaconda-forrester-agent-pilots
  - nosek-preregistration-pnas
  - higham-riskiest-assumption-test
  - crunchbase-h1-2026-funding
last_verified: 2026-07-17
word_count_target: 5200
---

# Idea definition — from itch to falsifiable bet

## Why this matters

You are three blocks past the point where building is the hard part. You can ship a RAG agent, a voice squad, a scraper-summarizer hybrid, and a landing page to sell any of them. That competence creates a new failure mode: because you *can* build anything in a weekend, the cheapest-feeling way to answer "is this a good idea?" is to build it and see. Sometimes that is even right; we will engage that argument honestly on Friday. But an unexamined build-first reflex has a documented base rate attached to it: 88% of enterprise AI agent pilots never reach production, per the Anaconda/Forrester data you first met in [[02-tue-when-ai-fits-a-problem|Block 0 Week 3]], and the H1 2026 funding flood ($510B of global VC, 43% of it to just two labs) means every plausible agent idea you have is being attempted by several funded teams simultaneously.[^1][^2] The scarce asset is not an idea and not a build. It is *evidence* that a specific set of people will change their behavior and pay. Today you turn your idea into something evidence can act on: a falsifiable bet with ranked assumptions and kill criteria written down before any evidence arrives. Everything else this week (desk research, interviews, synthetic panels, smoke tests) is machinery for feeding that bet.

## Prerequisites

- [[01-mon-problem-discovery-frameworks|Block 0 Week 3 Mon]] — JTBD schools, problem-first vs technology-first discovery. That lesson taught discovery for *client* problems. Today reuses its vocabulary and inverts its psychology: the client's motivated reasoning was their problem; now the motivated reasoning is yours.
- [[03-wed-scoping-ai-projects|Block 0 Week 3 Wed]] — the canonical home for kill criteria in engagement scoping. Today extends kill criteria from projects to product bets; we do not re-derive them.
- [[04-thu-niche-as-a-hypothesis|Block 1 Week 2 Thu]] — your niche-as-hypothesis work. Your product idea should sit inside a niche you already have surface area in; if it does not, note that as an assumption to test, because Wednesday's recruiting will be much harder.
- A candidate idea. If you genuinely have none, take the agent you packaged conceptually in Week 9 and ask "who would pay for this without me attached as a consultant?" That question is a product idea generator by itself.

## Layer 1 — The one-pager: problem, customer, wedge

An idea in your head is unfalsifiable by construction. It shifts shape every time evidence approaches: "well, obviously I meant it for agencies, not freelancers." The first discipline is to pin it to a page so that evidence has something stationary to hit.

The one-pager has five fields. Write each as a single declarative sentence, no "and."

1. **Problem.** A specific, recurring, costly activity or failure in someone's current workflow. Not a technology gap ("no one has an AI for X") but a behavioral fact ("X currently takes someone 4 hours every Friday and is wrong often enough that someone else re-checks it"). The [[01-mon-problem-discovery-frameworks|JTBD tests]] from Block 0 apply verbatim: if you cannot name the struggling moment, you have a capability looking for a problem.
2. **Customer.** The person (title, context, company shape) who feels the problem *and* can pay. For B2B agent products these are frequently different people; name both if so, and mark the gap as an assumption.
3. **Wedge.** The narrow first use case you win before anything else. "AI for legal ops" is a category, not a wedge. "Turns inbound NDA review requests into a redline draft plus a risk summary in the firm's house style" is a wedge. Wedge width is the most common self-deception in this exercise: motivated reasoning wants a wide wedge because a wide wedge is harder to falsify.
4. **Current alternative.** What the customer does today: a person, a spreadsheet, an incumbent tool's mediocre feature, or (the alternative every 2026 agent product must beat) "pastes it into ChatGPT/Claude themselves." If your honest answer is "nothing, they just suffer," treat that as a red flag, not an opportunity. People who tolerate a problem without any workaround usually do not feel it strongly enough to buy.
5. **Why you, why now.** One sentence each. "Why now" must be a change in the world (model capability crossing a threshold, a regulation like the EU AI Act's August 2026 full applicability, a price collapse), not "AI is hot." "Why you" should trace to your Block 1 niche surface area.

Then compress the whole thing into one **bet sentence** in this exact shape:

> We believe **[customer]** experiences **[problem]** at least **[frequency]**, currently handles it with **[alternative]** at a cost of **[time/money/risk]**, and enough of them will **[specific behavioral commitment: pay, pre-order, run a paid pilot, switch]** for **[wedge]** that this is worth building.

Every bracket is a claim that can be wrong. That is the point. A bet you cannot lose is not a bet; it is a mood.

## Layer 2 — Rank the assumptions: desirability, viability, feasibility

Marty Cagan's four product risks (value, usability, feasibility, viability) are the standard decomposition; David Bland's *Testing Business Ideas* collapses them for early-stage work into three questions: do they want it (desirability), should we do it commercially (viability), can we do it (feasibility).[^3][^4] The move that matters is not naming the categories. It is *ranking* your specific assumptions by (risk of being wrong × cost if wrong) and pointing all early evidence-gathering at the top of the list. Bland calls the artifact an assumption map; Rik Higham's "Riskiest Assumption Test" framing makes the same argument against premature MVPs: do not build the smallest product, design the smallest *test* of the deadliest assumption.[^5]

### The 2026 calibration for agent products

For most software history, feasibility earned its place at the top of the risk ranking. For agent products in 2026, it usually does not, and mis-ranking it is the signature error of technical founders. You spent Blocks 2 and 3 demonstrating that a competent generalist can build a working agent for almost any white-collar workflow in weeks. Frontier models are at 1M-token context across every major lab, and the cheap-agentic tier (Sonnet 5 at $2/$10 intro pricing, GPT-5.6 Terra, Gemini 3.5 Flash) has collapsed the marginal cost of trying.[^2] When building is cheap and capability is abundant, **feasibility is rarely the binding risk. Desirability usually is.** The graveyard evidence agrees: the dominant reported failure causes for agent pilots are unclear business value and workflow fit, not "the model couldn't do it."[^1]

Three exceptions where feasibility genuinely stays on top, so you do not over-learn the rule:

- **Reliability-threshold products.** If the workflow tolerates zero errors (funds transfer, regulatory filing, medical), the feasibility question is not "can it do the task" but "can it do the task at 99.x% with acceptable escalation," which is a different and much harder claim. [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8 Fri]] is the canonical treatment of that gap.
- **Data-access products.** If the value depends on data you do not have rights or plumbing to reach, feasibility is really a distribution/permission risk wearing a technical costume.
- **Latency/cost-envelope products.** Real-time voice at consumer price points, high-volume low-margin workflows: the unit economics are a feasibility claim.

### Writing testable assumptions

For each of the three categories, extract 2–4 assumptions from your one-pager and force each into a falsifiable, quantified form:

- Desirability, weak form (untestable): "Ops managers hate compiling the weekly report."
- Desirability, testable: "At least 6 of 10 ops managers we interview will describe, unprompted, a specific instance in the last month where the weekly report was late or wrong and it cost them something."
- Viability, testable: "At least 2 of 10 will agree to a paid pilot at ≥$300/month when offered at the end of a discovery conversation."
- Feasibility, testable: "On a 20-item golden set of real report inputs, a Sonnet 5 pipeline reaches ≥90% field-level accuracy inside $0.40/report." (You know how to run exactly this test from [[06-sat-rag-evaluation|Block 2 Week 4]].)

Note what quantification does: it converts an argument you could win in your own head into a measurement you can lose in the world.

## Layer 3 — Kill criteria before evidence: pre-registration for founders

Here is the mechanism design problem. You are about to spend a week gathering evidence about an idea you are attached to. Confirmation bias does not feel like bias from the inside; it feels like pattern recognition. The scientific community's answer to the same problem is pre-registration: commit to the hypothesis, method, and analysis *before* seeing data, so the data cannot be quietly reinterpreted afterward. Nosek and colleagues' case for it ("The preregistration revolution," PNAS 2018) is one of the most operator-relevant papers in metascience, because the failure it targets, generating a hypothesis after results are known and calling it a prediction, is precisely what founders do with validation data.[^6]

The founder version, written today, before Tuesday:

1. **Kill criteria per assumption.** For each top-3 assumption, the specific evidence outcome that kills or forces a pivot. "If fewer than 3 of 10 interviewees can cite a specific recent instance of the problem, the desirability assumption is dead." Kill criteria for engagements were built in [[03-wed-scoping-ai-projects|Block 0 Week 3 Wed]]; the product version differs only in who you are protecting the decision from (there: the client's sunk cost; here: your own).
2. **The decision rule.** One paragraph: what combination of assumption outcomes maps to BUILD, what maps to PIVOT (and along which axis: customer, problem, or wedge), what maps to KILL. Friday formalizes this into the evidence ledger; Saturday's code-lab tool enforces it. Today's handwritten paragraph is the binding version, because it is the only one that provably predates your evidence.
3. **The escape-hatch inventory.** Write down the three excuses you predict you will reach for if the evidence is bad ("wrong interviewees," "they just don't get it yet," "the smoke test copy was weak"). Pre-naming your own rationalizations is crude and works. If the evidence is bad *and* the excuse you wrote down appears in your head on schedule, you are watching your motivated reasoning in real time.

One boundary to keep the analogy honest: pre-registration in science protects inference from noise-mining across many analyses. Your n will be 10 interviews and a few hundred page visits; nothing you do this week is statistically decisive, and Friday's Wilson-interval discipline will keep you humble about that. The kill criteria are not there to make your study rigorous. They are there to make your *decision* precommitted.

## Layer 4 — Vitamin, painkiller, or fine-you're-fired

The classic vitamin/painkiller test asks whether the product is a nice-to-have or a need-to-have. For agent products, add a third rung, because agents do work someone is currently *accountable* for:

- **Vitamin:** the buyer would like it. Usage decays after novelty. Most "AI assistant for X" ideas live here, and here is where the 88% pilot mortality concentrates.[^1]
- **Painkiller:** the buyer has an active, recurring pain with a cost they can name. They have already tried workarounds (the workaround inventory from Layer 1 is your diagnostic).
- **Fine-you're-fired:** the task is attached to a consequence: a compliance deadline, an SLA, a customer commitment, a boss who checks. If the work does not happen or is wrong, a specific person suffers a specific consequence. Agent products in this band get adopted fastest and churn least, because the agent is absorbing accountability-bearing work, and they also carry the highest reliability bar, which is why the feasibility exception in Layer 2 exists. Price tracks the consequence, not the effort saved.

The test in interview form (Wednesday will refine it): "walk me through the last time this went wrong; what happened next?" If the answer involves a named unhappy human within 48 hours, you are at rung three.

A related 2026-specific check: **the ChatGPT-default test.** Your real competitor for painkiller-grade knowledge work is often the buyer pasting the task into a frontier chat model they already pay $20/month for. Your wedge must name what the default cannot do: the plumbing (it does not connect to their systems), the reliability (no evals, no consistency), the accountability (no audit trail), or the workflow position (nobody remembers to paste). "Better prompts" is not a wedge; you learned why when packaging in Week 9 ([[../week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/_week|Week 9]] (pending)).

## Layer 5 — Where ideas come from in 2026, and the live controversy

Two currents shape the idea landscape you are betting into. First, demand-side guidance: YC's 2026 Requests for Startups and its partner communication keep hammering one note, that founders should ground ideas in specific painful workflows discovered through conversation, and that the first weeks of every batch are still "talk to users and iterate," AI boom or not.[^7] Second, supply-side pressure: with capital concentrated at record levels and build costs collapsed, the moat question ("what stops a funded team or the platform vendor from doing this?") has to appear on your one-pager as a viability assumption rather than a shrug.[^2]

**The controversy you must have a position on: is validation itself procrastination?** The ship-school argument, stated sharply by designer-founder Andrés Max ("the old playbook is dead") and echoed across 2026 founder discourse, runs: building is now so fast and cheap that shipping a real product *is* the validation; run five conversations, then build and ship in two weeks, because interview cost stayed flat while build cost collapsed, so the optimal mix shifted toward less talking and more shipping.[^8] One Substack series on high-conviction founders even puts a number on it: more than five interviews is procrastination dressed as research.[^9] The discovery-school reply, put well by NYU's entrepreneurship center in May 2026 ("Shipping Is Not a Substitute for Asking"): shipping tells you *whether* people convert, and conversation tells you *why* and *what else*; a shipped product with no discovery behind it generates uninterpretable silence when it fails, and the failure mode of endless discovery ("a research museum where no experiment is allowed to come back no") is an argument for kill criteria, not for skipping discovery.[^10]

My synthesis, which the rest of the week operationalizes: the schools disagree less than they posture. Both condemn validation *theater*, evidence-gathering with no decision rule attached. Both endorse cheap real-world tests. The genuine disagreement is about interview counts and sequencing, and the resolution depends on reversibility: when shipping is cheap AND the audience is reachable AND a failed launch costs you nothing (no reputation burn in a niche you have spent Block 1 building), bias toward shipping. When any of those fails, the interview is the cheaper experiment. You, specifically, have a niche reputation as distribution; a sloppy launch spends it. That asymmetry is why this course sequences one week of validation before telling you to pour fuel on the Week 10 launch page.

## Worked example — from itch to bet in one sitting

Take a concrete idea: "an agent that turns client-meeting recordings into a drafted follow-up email, updated CRM fields, and a task list, for boutique consultancies."

One-pager, compressed: Problem: consultants lose 30–60 min per meeting on follow-up admin, and late follow-ups stall deals. Customer: founder-principal at a 2–15 person consultancy (feels it AND pays). Wedge: post-meeting follow-up package for client calls, in the firm's voice. Current alternative: an AI notetaker's generic summary plus manual everything else, or pasting a transcript into Claude. Why now: meeting transcripts became ambient (every call is already recorded); consent law and the notetaker lawsuits (Wednesday's material) are pushing firms toward tools with a compliance story. Why you: you have built exactly this pipeline shape in [[06-sat-build-the-weekly-report-generator|Block 2 Week 5]].

Bet sentence: "We believe founder-principals at 2–15 person consultancies lose ≥30 minutes of admin per client meeting, currently patch it with notetaker summaries plus manual CRM entry, and at least 2 of the first 10 we talk to will start a $200/month paid pilot for an agent that drafts the follow-up email, CRM update, and task list within 10 minutes of the call."

Ranked assumptions: (1) Desirability: the pain is the *admin bundle*, not the notes; notetaker incumbents feel "good enough" to fewer than half. (2) Viability: $200/month clears their willingness-to-pay for admin removal; the buyer is reachable through your niche network. (3) Feasibility: house-voice drafting at acceptable quality from messy transcripts, testable on a golden set in a day.

Kill criteria: fewer than 3 of 10 naming a specific recent follow-up failure kills desirability; zero paid-pilot acceptances at any price point after 10 conversations forces a viability pivot; below 80% acceptable-draft rate on the golden set after two iteration cycles sends feasibility back to the bench. Escape hatches pre-named: "wrong firm size," "they didn't see the demo," "the price anchored wrong."

Total elapsed time: about 90 minutes. Notice that nothing here required research yet. That is deliberate: today's artifacts are the *targets* for the week's evidence, and writing them first is what makes the evidence mean something.

## Runnable experiment — adversarial definition with Claude (60–75 min)

The experiment medium is Claude (Claude.ai or Claude Code), used as an adversary, never as a validator. Pass bar at the end.

**Step 1 (20 min).** Draft your one-pager and bet sentence unaided. Resist the urge to ask the model for idea help first; you are measuring your own clarity.

**Step 2 (15 min).** Adversarial pass. Paste the one-pager with this prompt: *"You are a skeptical operator who has watched 88% of agent pilots die. Do not improve my idea. Attack it: (1) restate my wedge in the narrowest form that could still be a business and the widest form I am secretly imagining; (2) name the three assumptions most likely to be false, with the cheapest test for each; (3) tell me what the customer's current alternative does well that I am underrating, including 'paste it into ChatGPT'; (4) predict the excuse I will use when evidence is bad."* The instruction "do not improve my idea" matters; without it, the model's helpfulness training will start co-authoring, and you will like the idea more with every turn. Sycophancy is Thursday's topic, but its shadow falls on today.

**Step 3 (15 min).** Rewrite: one-pager v2, three ranked assumptions in quantified/falsifiable form, kill criteria per assumption, decision-rule paragraph, escape-hatch inventory.

**Step 4 (10 min).** Date-stamp and freeze. Save as `validation/00-bet.md` in your project repo; commit it. Saturday's evidence-ledger tool will import these assumptions verbatim, and the commit timestamp is your pre-registration receipt.

**Pass bar:** (a) three assumptions, each with a number in it and a named kill threshold; (b) a decision rule that includes at least one outcome mapping to KILL (if no realistic evidence pattern kills the idea, return to Step 3); (c) the model's predicted excuse written into your escape-hatch inventory. Fail any of these and the rest of the week degrades into theater.

## Common mistakes experts see

1. **Wedge inflation.** Defining the wedge wide enough that no evidence can miss it ("AI for operations teams"). Narrow until an interviewee could say "that's not for me."
2. **Feasibility-first comfort testing.** Spending the week on golden sets and evals (fun, familiar from Block 2) while the desirability assumption sits untested. Test the assumption that kills, not the one you know how to test.
3. **Unfalsifiable desirability claims.** "People hate doing X" survives any interview. "6 of 10 will cite a specific instance last month" does not.
4. **Kill criteria written after the first interview.** One enthusiastic conversation recalibrates "what success looks like" upward or downward to fit. The commit timestamp exists precisely to make this visible.
5. **"No current alternative" read as opportunity.** It is usually evidence of a vitamin. The workaround inventory is the demand signal.
6. **Treating the ChatGPT default as beneath consideration.** Buyers price your product against $20/month and a paste. Name your delta explicitly or discover it in the sales call.
7. **Solo-brainstorming with a helpful model.** Un-adversarial Claude sessions produce ideas you are *more* attached to and *less* able to falsify, the worst possible trade for this week.

## Open questions — what's not settled

**1. Does idea quality still matter, or only distribution?** A serious 2026 position holds that when everyone can build everything, idea selection contributes almost nothing to outcomes; distribution and execution speed decide, so validation optimizes a variable with a small coefficient. The counter-evidence is the pilot graveyard: 88% mortality is not a distribution statistic, it is overwhelmingly a wrong-problem statistic.[^1] The honest synthesis is conditional: within a niche you already have distribution in, idea selection among reachable wedges is the dominant lever, which is exactly the situation Block 1 spent two weeks engineering you into. Whether that holds for founders without a niche is genuinely unsettled.

**2. Is wedge-first doctrine safe when platforms are expanding this fast?** The narrow-wedge orthodoxy assumes the wedge stays yours long enough to expand from. But 2026's pattern is platform vendors marching upward into application territory (Claude Cowork into general knowledge work, agent templates into vertical analysis). A wedge that is merely a *thin UI over a capability the platform will ship natively* validates beautifully and dies at the next model release. No framework reliably distinguishes defensible wedges from doomed ones ex ante; the best available proxy is whether your wedge's value concentrates in things platforms historically avoid: proprietary data plumbing, workflow position, and accountability. Treat "the platform ships it" as a viability assumption with a probability, not a boolean.

**3. How much pre-commitment is too much?** Pre-registration guards against motivated reasoning, but founders are not running clinical trials; the evidence you meet this week may legitimately reframe the question itself, and a decision rule written Monday can be *wrongly specified*, not just inconveniently failed. The escape valve this course teaches (overrides allowed, but written, logged, and witnessed) is a compromise position, not a solved problem. Where the line sits between disciplined updating and rationalized drift is a judgment call the apparatus can expose but never make for you.

## Reflection questions

1. Your bet sentence contains a behavioral commitment (pay, pre-order, pilot). What would you accept as the *weakest* commitment that still counts as evidence, and why that line?
2. Which of your three assumptions would you least like to test first? (That reluctance is usually diagnostic. Of what, in your case?)
3. Construct a realistic evidence pattern under which your idea survives desirability but dies on viability. What pivot does your decision rule prescribe, and do you actually believe you would execute it?
4. The ship-school says five interviews then build. For *your* idea and *your* current distribution, what is the strongest concrete argument that they are right, and what single fact would flip it?
5. If a funded team shipped your exact wedge tomorrow, which of your one-pager fields changes? (If the answer is "none," is that confidence or denial?)
6. What consequence-bearing task (fine-you're-fired rung) sits adjacent to your current wedge, and what would it cost to move the wedge there?

## My take (reviewer lens)

**Michael Seibel** would push on the week's very existence: for a builder with your speed, he would say, the one-pager plus five honest conversations plus an ugly live version is strictly better evidence than any amount of assumption cartography, and the real risk in this lesson is that mapping assumptions *feels* like progress in exactly the way he warns founders about. He would be half right, and the lesson concedes the half: every artifact today is time-boxed to one sitting, and the week ends in a shipped smoke test, not a document. **Ethan Mollick** would question the confident claim that "feasibility is rarely the risk": his adoption research keeps finding that the gap between demo-grade and dependable-in-workflow performance is where organizational AI value actually dies, so "we can build it" and "they can adopt it" are further apart than the desirability/feasibility split implies. Fair; that is why the fine-you're-fired rung imports the reliability bar from Block 3 rather than waving at it. And **a cohort peer** would flag the quiet privilege in "you have a niche reputation as distribution": readers who skipped Block 1's brand-building have neither the recruiting surface Wednesday assumes nor the launch asset Friday leverages, and for them the honest advice is to run this week's motions at smaller scale while rebuilding that surface, not to pretend ten strangers will answer a cold DM because the lesson said to interview ten people.

## Further reading

**Must-read**

- Rob Fitzpatrick, *The Mom Test* (2013; the canonical text behind Wednesday, worth starting today; ~2h read).[^11]
- David J. Bland & Alexander Osterwalder, *Testing Business Ideas* (2019), chapters 1–3 on assumption mapping and experiment selection.[^4]

**Recommended**

- Marty Cagan, "The Four Big Risks," SVPG blog.[^3]
- Nosek et al., "The preregistration revolution," PNAS 2018.[^6]
- Y Combinator, Requests for Startups (2026 edition), read as a demand-signal document, not an instruction.[^7]

**Optional**

- Rik Higham, "The MVP is dead. Long live the RAT."[^5]
- NYU Entrepreneurship, "Shipping Is Not a Substitute for Asking" (May 2026), for the discovery-school side of the controversy.[^10]

## Citations

[^1]: Anaconda/Forrester survey finding that 88% of AI agent pilots never reach production; ~2/3 of enterprises still in pilot mode. Corroborated across https://prefactor.tech/learn/ai-agent-adoption-statistics and https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points ; canonical vault treatment in [[02-tue-when-ai-fits-a-problem|Block 0 Week 3]] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: H1 2026 funding concentration: $510B global VC in H1 2026, OpenAI + Anthropic taking $217B ≈ 43%; cheap-agentic price tier (Sonnet 5 $2/$10 intro through 2026-08-31, GPT-5.6 Terra, Gemini 3.5 Flash $1.50/$9). Crunchbase News, https://news.crunchbase.com/venture/global-startup-exits-ipo-ma-soar-ai-q2-h1-2026/ and https://news.crunchbase.com/venture/na-startup-funding-ma-shattered-records-ai-q2-2026/ ; pricing per Anthropic https://www.anthropic.com/news/claude-sonnet-5 and TechCrunch coverage. URL-verified in `vault/00-program/_refresh-2026-07-landscape-delta.md` (counts as one corroboration) plus original announcements (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Marty Cagan, "The Four Big Risks" (value, usability, feasibility, business viability), Silicon Valley Product Group. https://www.svpg.com/four-big-risks/

[^4]: David J. Bland & Alexander Osterwalder, *Testing Business Ideas: A Field Guide for Rapid Experimentation* (Wiley, 2019), Part 1 (assumption mapping, experiment sequencing by evidence strength).

[^5]: Rik Higham, "The MVP is dead. Long live the RAT (Riskiest Assumption Test)," 2016. https://hackernoon.com/the-mvp-is-dead-long-live-the-rat-233d5d16ab02

[^6]: Brian A. Nosek, Charles R. Ebersole, Alexander C. DeHaven, David T. Mellor, "The preregistration revolution," *PNAS* 115(11), 2018. https://www.pnas.org/doi/10.1073/pnas.1708274114 — the postdiction-vs-prediction distinction that Layer 3 ports to founder decisions.

[^7]: Y Combinator, Requests for Startups, 2026 editions. https://www.ycombinator.com/rfs ; Summer 2026 RFS coverage at https://techstartups.com/2026/02/04/y-combinator-is-out-with-its-2026-request-for-startups/ and https://www.thevccorner.com/p/yc-summer-2026-requests-for-startups-ideas — consistent emphasis: ground ideas in specific painful workflows via user conversations; first batch weeks are talk-to-users-and-iterate (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Andrés Max, "How to Validate a Startup Idea in 2026 (The Old Playbook Is Dead)." https://andresmax.com/validate-startup-idea/ — the ship-school position: ~5 conversations, then build and ship in ~2 weeks; shipping as validation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Traction Thinking, "High Conviction Founder Series" (2026), incl. "They think like scientists, act like founders" and "They prioritize shortening time-to-customer." https://tractionthinking.substack.com/p/high-conviction-founder-series-they-f0b — source of the "more than five interviews is procrastination" claim and the "procrastivity" coinage; quoted as a named position in a live debate, not as settled fact (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: NYU Entrepreneurship blog, "Shipping Is Not a Substitute for Asking: Why Customer Discovery Doesn't Stop When You Ship," May 8, 2026. https://entrepreneur.nyu.edu/blog/2026/05/08/shipping-is-not-a-substitute-for-asking/ — the discovery-school reply; also the "research museum" critique of validation theater (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: Rob Fitzpatrick, *The Mom Test: How to talk to customers & learn if your business is a good idea when everyone is lying to you* (2013). https://www.momtestbook.com/

_last_verified: 2026-07-17_
