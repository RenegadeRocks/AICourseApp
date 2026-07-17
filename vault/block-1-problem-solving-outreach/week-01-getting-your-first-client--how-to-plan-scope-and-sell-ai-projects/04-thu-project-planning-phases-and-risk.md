---
type: lesson
block: block-1-problem-solving-outreach
week: week-01
day_of_cycle: 4
day_name: thu
session_slug: how-to-plan-scope-and-sell-ai-projects
date_due: 2026-05-21
tags: [project-planning, phased-engagement, poc-to-production, ai-risk-model, exit-ramps, pilot-trap, kill-criteria, vendor-lock, model-drift, eval-sla, sponsorship-risk, commercial-structure]
sources:
  - gartner-30pct-poc-abandoned-2024
  - gartner-agentic-cancellations-2027
  - mit-nanda-genai-divide-2025
  - mckinsey-state-of-ai-2025
  - bcg-ai-radar-2025
  - bcg-widening-ai-value-gap-2025
  - idc-ai-pocs-production-2025
  - omdia-ai-pocs-balanced-perspective-2025
  - cio-88pct-pilots-fail-2025
  - husain-field-guide-2025
  - husain-evals-faq-2026
  - morgan-lewis-ai-contract-provisions-2026
  - tascon-ai-contract-clauses-2025
  - ccsd-third-party-ai-risk-clauses-2025
  - a16z-enterprise-genai-2025
  - mckinsey-agentic-scaling-2025
  - accenture-genai-bookings-2025
  - stark-value-pricing-phase-delivery-2024
  - patio11-consulting-greatest-hits
  - planet-a-pilot-hell-2024
last_verified: 2026-04-16
word_count_target: 6000
---

# Project planning for AI engagements — discovery, POC, pilot, production, and the risk model that decides whether any of it reaches production

## Why this matters

In November 2025 McKinsey's global *State of AI* survey reported that 23% of organizations are scaling at least one agentic AI system, another 39% are experimenting, and just 6% qualify as "AI high performers" extracting more than 5% EBIT from AI.[^1] In July 2025 MIT's Project NANDA published *The GenAI Divide*, a study of 300+ disclosed initiatives, 52 structured interviews, and 153 senior-leader surveys, concluding that 95% of enterprise generative-AI pilots deliver no measurable P&L impact.[^2] (This lesson is the week's canonical home for interrogating that figure; it is first introduced in [[02-tue-when-ai-fits-a-problem]], Block 0 Week 3, and other Week-1 lessons should link here or there rather than re-cite it.) In January 2025 BCG's AI Radar placed 5% of companies in the "future-built" band and 60% in a "no material value" band.[^3] IDC's 2025 analysis found that only 4 of every 33 AI POCs reach production, a conversion rate of roughly 12%.[^4] In April 2026 Gartner reported that AI projects in infrastructure and operations are stalling ahead of meaningful ROI returns, with 40% of agentic AI projects forecast to be cancelled by end of 2027.[^5] CIO.com's March 2025 synthesis of a Deloitte–Informatica–S&P Global dataset put the pilot-to-production failure rate at 88%.[^6]

Those numbers describe one phenomenon from five angles. Call it the *pilot trap*: the engagement that POCs convincingly, pilots politely, and dies at the production gate because no one designed the path through the gate.

Block 0 Week 3 Wednesday taught you the technical scoping pattern — walking-skeleton MVP with an eval harness, hard eval gates, weekly iteration, scope discipline ([[03-wed-scoping-ai-projects]]). That lesson is load-bearing; this one extends it. Where that lesson was about *what you build in each sprint*, this one is about *how you commercially structure the engagement around those sprints* so the project can (a) reach production, (b) be killed cheaply when it shouldn't, and (c) not wreck you when the model provider, the data, or the sponsor moves under you.

By the end of this lesson you will be able to (1) map any candidate AI engagement onto the canonical four-phase structure — discovery, POC, pilot, production — with phase-specific goals, deliverables, fees, and go/no-go gates; (2) apply the five-part AI risk model (data, drift, vendor, eval, sponsorship) to identify which phase surfaces which risk and which mitigations belong in the contract versus the runbook versus the backlog; (3) design commercial exit ramps that protect both sides and make kill-the-project the natural choice when the evidence says kill; (4) take a defensible position on whether the pilot trap is primarily a contract-structure problem or a technical-fit problem, with named operators on both sides; and (5) price each phase in a way that survives the token-cost and scope-change shocks the data says you will experience.

## Prerequisites

- Block 0 Week 3 Wednesday on walking-skeleton MVPs, eval gates, and kill criteria ([[03-wed-scoping-ai-projects]]). Everything in this lesson sits on top of that technical frame. If you do not have the eval-gate pattern in muscle memory, this lesson will read as a vocabulary tour.
- Operational familiarity with one real AI engagement — even a small one — where you can point at the moment the project crossed, or should have crossed, from POC into pilot. If you cannot, pick a recent public failure (Klarna's partial customer-service rollback in 2024, any agentic-automation launch you followed) and use it as your running case.

## Layer 1 — The four phases, and why you need all four

The canonical phase structure for AI engagements is *discovery → POC → pilot → production*. It is not new as vocabulary; enterprise services firms have used a version of it since the 1990s. What is new is the *coupling* between the phases and the eval regime. In traditional software, the phases are mostly a project-management convenience. In AI, each phase *answers a different question the prior one could not*, and skipping any phase reliably breaks the project.

### The questions each phase answers

**Discovery** answers *is there a real job worth solving with AI, and what would "worked" look like as a measurable outcome?* It is the cheapest phase, and the one cut first by buyers under pressure. It is also the phase whose absence correlates with every dataset of pilot-to-production failure cited above.[^2][^5][^6] Outputs: a named job-to-be-done in the Christensen format, an outcome spec in Ulwick's direction-plus-metric-plus-object-plus-context form, a candidate eval rubric, a sponsor map, a preliminary data-access inventory, and a decision document — go / no-go / pivot — signed by the sponsor.

**POC** answers *given the job and the outcome spec, can the system meet the eval bar at all, on a realistic slice of real inputs, inside a cost envelope that makes commercial sense?* This is the walking-skeleton phase of Block 0 Week 3 Wednesday. You build end-to-end, not deep on any layer, and you instrument for the eval rubric from discovery. Outputs: a working end-to-end system on a realistic data slice; an eval harness reporting the rubric with confidence intervals; a cost-per-task measurement; a kill-or-continue recommendation with the rubric evidence to back it.

**Pilot** answers *does the system work for real users in real conditions, including the long tail that demo data did not cover, the workflow integration that POC did not need, and the operational load the sponsor did not yet feel?* This is where the project usually dies, and where the failure modes are the least technical. Outputs: a bounded production deployment (a department, a subset of traffic, a named customer cohort); live traffic evals; incident log; integration findings; sponsor retrospective; production readiness decision.

**Production** answers *will this system keep working as the world, the model, and the workflow change around it?* This is the SLA phase. Outputs: an operational runbook; drift monitoring; rollback plan; change-management process; budget for ongoing evals and adjustments; exit plan for when the system or the engagement ends.

Hamel Husain's *Field Guide to Rapidly Improving AI Products* (Mar 2025) is the current operator-level reference for what "working" looks like in each phase; his structural claim — tight time-boxes, decision points, and evaluation infrastructure *before* features — is the spine of every phase structure that converts.[^7] He pegs feasibility and foundation at 2–3 months, prototype and testing at 6+ weeks, and scaling-with-trust at however long it takes to prove human–judge alignment above roughly 90%.

### Why skipping phases fails, in data

Skipping discovery: the 88% pilot failure rate in the CIO/Deloitte synthesis is heavily weighted to projects that entered POC on a capability hypothesis without an outcome spec, which is the operational definition of skipping discovery.[^6] MIT NANDA's principal finding — "most GenAI systems do not retain feedback, adapt to context, or improve over time" — is downstream of never having specified the feedback or the context to begin with.[^2]

Skipping POC: rare but catastrophic when it happens. The shape is a vendor pitching "we'll just build it in pilot" to a buyer who wants to compress timeline. The pilot discovers what POC would have flagged in week three (the data is messier than the sample, the eval metric isn't what the business cares about), and the cost to recover is now the cost of a pilot, not a POC.

Skipping pilot: the most seductive and the most expensive. A POC that looks good on a synthetic slice is promoted straight to production. The omitted discovery — that real traffic has a long tail the synthetic slice didn't represent — shows up as the 95% no-measurable-P&L number in MIT NANDA.[^2] The system "works" in the sense that it doesn't crash; it doesn't work in the sense that no one will pay for it or keep using it.

Skipping production planning: the system ships, and six months later a model-provider update subtly changes output format, an upstream data source drifts, or the sponsor leaves, and no one owns the re-eval. The CCSD Council's 2025 analysis of third-party AI risk catalogues the absent termination, data, and change-control clauses this produces.[^8]

### The phase-coupling rule

The unintuitive claim, and the one most buyers push back on, is that *each phase's deliverables are only valuable if the next phase is designed around them*. A discovery document written as a consulting artifact — pretty slides, named personas, outcome framing — and then handed to a POC team that builds against a different interpretation of the job is worse than no discovery. The eval rubric from discovery has to be the rubric POC measures. The cost model from POC has to be the budget pilot commits to. The incidents from pilot have to become the operational runbook production inherits. If any link breaks, the phase before it was wasted.

This is why the right commercial structure is phased but *integrated* — one engagement with four gates, not four separate procurements. We come back to this in Layer 4.

## Layer 2 — The AI risk model, five axes

Generic IT risk frameworks (COBIT, NIST RMF, ISO 27001) were designed before foundation models. They still apply, but they miss five AI-specific risks that dominate the pilot-to-production crossing. Any engagement without explicit owners for each of these is running uninsured.

### Data risk

The most cited failure mode and the least respected at kickoff. Gartner's 2025 survey of CIOs found that 63% of organizations either lack appropriate AI-ready data or are unsure whether their data is AI-ready; Gartner predicts that at least 60% of AI projects will be abandoned through 2026 without AI-ready data.[^9] The operational failure modes: access not granted when the POC started (takes 6 weeks to resolve, eating half the POC), schema drift between the sample and production (the labels you trained on no longer exist), personally-identifiable data encountered at scale that triggers a compliance review no one budgeted for (2–4 weeks), and the killer — the sponsor thought a corpus was available that was in fact owned by another business unit that declines to share.

Owner in the contract: the buyer's sponsor, named. If data access isn't the sponsor's to grant, the engagement isn't ready for POC — it's still in discovery.

### Drift risk

Covers three distinct phenomena operators routinely conflate. *Data drift* is a change in the distribution of inputs (new product categories, new customer segments, new document formats). *Concept drift* is a change in the relationship between inputs and outputs (a fraud pattern that used to be rare becomes common; a policy that used to accept X now rejects X). *Model drift* — more properly *model provider drift* — is the silent update the vendor ships that shifts your outputs without changelog notice.

Arize AI's 2025 operator writing documents the ML-observability stack that now handles the first two; Fulcrum Digital's 2025 analysis argues latency-SLA monitoring (p50/p95/p99 plus time-to-first-token) now belongs next to accuracy SLAs.[^10] The third — provider drift — is under-instrumented in most enterprise engagements and is why an eval-regression suite that runs on a fixed sample *weekly* is not optional. In the CCSD Council and Morgan Lewis writing on 2025–26 AI contract clauses, the emerging market norm is a 12-month notice requirement for API-endpoint deprecation, with 6 months as the negotiating floor.[^8][^11]

Owner in the contract: the vendor (you, the builder) owns eval-regression and provider-drift monitoring as a deliverable; the buyer owns input-distribution monitoring because they own the inputs. If the contract doesn't split those, both parties assume the other is watching.

### Vendor risk

The risk that your model provider, your tooling provider, or your own subcontractor changes terms, pricing, retention, availability, or existence. OpenAI's enterprise default for API data retention has been ZDR-by-request since 2024; in 2025 the enterprise retention defaults and the list of ZDR-eligible endpoints shifted multiple times, as documented in OpenAI's policy page history and in Microsoft's Azure OpenAI Q&A thread on the changes.[^12] The Anthropic enterprise agreement saw similar amendments. The lesson is not that any one vendor is unreliable; it is that *every* frontier vendor is shipping policy at roughly the same pace as product, and a one-year engagement signed on November defaults will hit May defaults mid-pilot.

The 2026 war story that makes this concrete — and that exposes a sub-axis the classic five-risk model doesn't name — is the **Claude Fable 5 / Mythos 5 export-control suspension.** Anthropic launched Fable 5 (its first public "Mythos-class" tier, $10/$50 per M tokens) on June 9, 2026. Three days later, on June 12, a US government export-control directive ordered access suspended for all foreign nationals worldwide; Anthropic disabled the models globally. The Department of Commerce lifted the controls and Anthropic redeployed globally on July 1, 2026.[^27] For any SOW that had named "the flagship Claude tier" as its delivery model, a frontier model became *unavailable mid-quarter for a regulatory reason neither the builder nor the buyer controlled or could have forecast.* That is not pricing risk, retention risk, or deprecation risk — it is **regulatory-availability risk**, a government-directive sub-category the five-axis model above folds into "vendor risk" but which deserves its own line in a 2026 risk map, because its mitigation is different: not a portability clause but a *named fallback model of a different provenance* the engagement can fail over to inside 48 hours.

The contract clauses that earn their keep: a termination-for-convenience right with 60–90 day notice, a data-portability clause requiring export of prompts, logs, embeddings, fine-tunes in open formats, a 90-day transition-support obligation, ownership of fine-tuned weights when the buyer supplied the training data, and — new for 2026 — a named cross-provider fallback so a single-vendor availability shock does not halt the engagement. Methodmi's 2026 analysis of vendor lock-in in procurement platforms argues the first four clauses together are what makes "exit ramp" more than rhetoric;[^13] the Fable 5 episode adds the fifth.

Owner: shared, and named. The builder owns model-provider risk monitoring (including the fallback-model plan); the buyer owns data-provider and internal-system risk monitoring. The engagement owns the contract clauses that make each side's monitoring actionable.

### Eval risk

The risk that your evaluation regime doesn't measure what the business cares about, or measures it in a way that systematically overestimates quality. Shreya Shankar's *Who Validates the Validators?* (UIST 2024) is the canonical academic treatment — LLM-as-judge pipelines are only trustworthy when their outputs have been aligned to human judgment at a validated threshold, typically >90%.[^14] Husain's *Evals FAQ* post (Jan 2026) pushes the operational version: the common failure is to practice *eval-driven development* as ritual — writing evaluators for errors you imagined rather than errors you observed in production logs. His correction: start with error analysis on real production traces, write evaluators for the errors you discover, and use EDD only when you know exactly what success looks like at the edge (e.g., "never mention competitors").[^15]

The eval-risk failure mode at the phase boundary: a POC that passes its rubric because the rubric was written by the builder against the builder's intuition of the job, never validated against the sponsor's actual definition of success. Pilot exposes the gap; the cost to re-do the rubric at pilot is the cost of the POC again.

Owner: the engagement runs an eval-rubric sign-off with the sponsor as a discovery deliverable, not a POC one. That sign-off is what makes the eval risk the builder's problem after POC.

### Sponsorship risk

The most expensive and the least modelled. The risk that your sponsor leaves, loses mandate, reorganizes, or de-prioritizes the project. In a typical enterprise AI engagement — 6–12 month pipeline from discovery to production — the sponsor-change rate is not zero. BCG's 2025 *Widening AI Value Gap* report shows the leader cohort (top 5% of firms) have fundamentally different governance structures — CEO-level ownership, executive-committee steering, allocated cross-functional staffing — that shield projects from sponsor volatility.[^16] Most engagements don't have that cover. The operational signal: when the sponsor can't name the next senior decision-maker who would inherit the project on their departure, the project has sponsorship risk the contract should price in.

Owner: the buyer, explicitly. The clause that earns its keep is a change-of-sponsor notice plus a 30-day re-alignment window before the next phase-gate fee becomes due.

### Applying the five together

A risk map for any engagement should name the owner, the surfacing phase, and the mitigation for each axis. A worked example for a mid-market intake-triage agent engagement (say, for a regional law firm):

- *Data:* sponsor owns; surfaces in discovery; mitigation = data-access inventory as discovery deliverable, with sign-off before POC fee is released.
- *Drift:* split ownership; input drift surfaces in pilot, provider drift surfaces continuously; mitigation = weekly eval regression + monthly ML-observability review as contractual deliverables.
- *Vendor:* split; surfaces continuously; mitigation = termination-for-convenience + data-portability + fine-tune ownership + API-deprecation notice clauses in master agreement.
- *Eval:* builder owns after discovery sign-off; surfaces in POC; mitigation = rubric-alignment session with sponsor before POC build, LLM-judge validation at >90% alignment before POC closes.
- *Sponsorship:* buyer owns; surfaces at every phase gate; mitigation = named secondary sponsor, change-of-sponsor notice clause, re-alignment window.

That map, as a one-page artifact, is the single highest-leverage document in the engagement. More valuable than the SOW. Every named operator cited in Further Reading has a version of it.

## Layer 3 — What the data says about POC-to-production conversion, and why the headline numbers mislead

The numbers in the opening paragraph are real, and they are also systematically misunderstood. Three specific distortions matter for planning.

### Distortion 1: the denominator problem

"88% of pilots fail" and "95% of pilots deliver no P&L" are not the same measurement. The CIO/Deloitte synthesis counts pilots that "reach production" as the numerator and uses any completed pilot as the denominator.[^6] MIT NANDA's 95% counts projects with *measurable P&L impact at the enterprise level* as the numerator, which is a much higher bar.[^2] Gartner's 30% abandoned-after-POC figure counts projects that cross the abandon threshold before end of 2025, with the rest including many that are still in-flight, not succeeding.[^17] BCG's 5% "future-built" is a governance/posture measure, not a project-level success rate.[^3]

Operator implication: when you're planning a project, the question isn't "will we be in the 5%" — it's "which of these definitions of success applies to our engagement, and what would evidence for each look like at each phase gate?" Most buyers conflate all four, which means "success" moves depending on who's in the room.

### Distortion 2: pilot hell is a contract problem at least as much as a technical problem

Planet A Ventures' 2024 essay *Escaping Pilot Hell* — written from the industrial-adoption side but directly applicable to AI — argues that most industrial pilots never convert *because the contract didn't make conversion the default*.[^18] A Morgan Lewis April 2026 analysis of where the AI-commercial-contract market is heading reaches the same diagnosis for AI: contract design plays a disproportionate role in pilot-to-production conversion, and the clauses that move the rate are a defined conversion timeframe, pre-negotiated next-phase pricing, a unilateral buyer termination right tied to pilot criteria, and substantive IP/liability/data-governance provisions rather than boilerplate.[^11]

This is the reason the lesson's title couples "phases, risk model, and exit ramps" — the exit ramps *are* the conversion mechanism, counter-intuitively. A pilot with a pre-negotiated production contract, a unilateral termination right on criteria failure, and a defined 60-day conversion window converts at higher rates than a pilot with "we'll figure out production if this works." The optionality is what makes the commitment credible on both sides.

### Distortion 3: the "only 5% win" framing hides the leader-laggard gap

BCG's September 2025 *Widening AI Value Gap* reports that leader firms outpace laggards with 1.7× revenue growth, 3.6× three-year TSR, and 1.6× EBIT margin.[^16] The McKinsey *State of AI 2025* finds AI high performers are 3.6× more likely to pursue transformational change and 55% fundamentally rework workflows when deploying AI.[^1] The leader cohort isn't lucky; they're structurally different. They allocate 80%+ of AI investment to reshaping functions and inventing new offerings rather than point-tool pilots. They have CEO-level ownership. They run portfolios of five to ten projects concurrently rather than betting on one.

Operator implication for a buyer who isn't yet in the leader cohort: *your first-engagement AI project is being planned in an environment where the baseline success rate is low because the environment's governance and investment posture is low-maturity*. The project's planning has to compensate. Which is why the phase structure and risk model in this lesson are not abstract discipline — they are the *substitute for institutional maturity the buyer doesn't yet have*.

## Layer 4 — Phase pricing that survives reality

Three pricing archetypes dominate AI engagements in 2026, and each works for a specific phase shape and breaks in a specific failure mode.

### Archetype A — flat-fee-per-phase

The cleanest for buyer and seller. Each phase has a fixed fee, a fixed duration, and fixed deliverables. Payment is on gate-passage. Advantages: predictable for both sides, no token-cost surprises for buyer, no scope-creep erosion for seller. Failure mode: a flat fee that assumed certain data access, vendor pricing, or token volumes collapses when any of those shift — **and in 2026 the shift goes both ways.** Through 2024–25 frontier prices mostly fell (GPT-4-Turbo → GPT-4o repricing, the Claude 3.5 generation), so an un-hedged flat fee tended to over-quote the buyer. But June 2026 broke that pattern: Claude Fable 5 launched at $10/$50 per M tokens — *2× Opus 4.8* — so a client whose plan named "the flagship Claude tier" saw unit costs roughly double at the upgrade, while at the cheap end Sonnet 5 launched at $2/$10 intro pricing. A flat-fee-per-phase engagement without a two-directional token-cost pass-through clause now either eats an *increase* (seller) or over-quotes on an assumed *decrease* (buyer); either way the missing clause triggers a change order that feels adversarial. Friday's SOW lesson ([[05-fri-commercial-sow-for-ai-projects]]) rebuilds the pass-through formula for exactly this two-sided regime.

Jonathan Stark's value-pricing writing (including his December 2024 daily post *The Obvious Switch to Value Pricing*) argues for value-based pricing as an alternative; his phase-delivery-pricing method is the operational compromise — flat fee per phase, but priced to the buyer's expected value rather than the seller's cost, with explicit carve-outs for cost-pass-through on specified inputs.[^19]

### Archetype B — time-and-materials with hard cap

Used on engagements where the seller cannot yet estimate the work — typical for discovery, sometimes POC. Advantages: the seller doesn't gamble on an unknown; the buyer sees real cost. Failure mode: T&M without a hard cap drifts, and the cap has to be both real (seller stops when hit) and calibrated (not so low the seller stops before value). The calibration is the seller's job, and it is the thing that distinguishes experienced AI consultants from new ones. Hamel Husain's *Field Guide* 2-3 month foundation phase is typically priced T&M-with-cap, because the work in that phase is genuinely exploratory.[^7]

### Archetype C — outcome-tied / success fees

Tempting for buyers, dangerous for sellers with less than three case studies. The model: a portion of the fee is contingent on hitting a pre-specified outcome metric (eval pass-rate at production, operator acceptance rate, cost-per-task ceiling, specified business KPI). Advantages: aligns incentives, closes "why would I pay before I know it works" objection. Failure modes: first, the specified metric can be gamed (a 95% eval pass-rate on a rubric the seller wrote isn't a 95% pass-rate on the job); second, the seller absorbs risks they don't control (sponsor change, buyer data delays, vendor pricing); third, margin destruction — a 30% contingent fee on a project that doesn't hit criteria is a 30% loss against fixed cost.

Patrick McKenzie's greatest-hits writing on consulting argues that outcome-tied pricing works only for established consultants with three-plus case studies, a buyer who can actually influence the outcome without the seller, and outcomes measurable cleanly without gaming.[^20] For first-engagement AI projects, outcome-tied pricing is usually a red flag that the buyer is transferring their uncertainty to the seller. The honest operator move is to offer a phase-gated structure with generous kill rights (which is optionality the buyer actually values) rather than an outcome contingency (which is risk dressed as alignment).

### The hybrid that usually wins for AI engagements

For a mid-market first-engagement AI project, the structure that converts most often is: discovery T&M-with-cap (the scope genuinely is unknown), POC flat-fee with token-cost pass-through above a threshold (the scope is now known, but costs have known swing), pilot flat-fee with a unilateral buyer termination on criteria (the commitment is credible because the exit is credible), production retainer with explicit ongoing-eval and drift-monitoring line items (the thing that dies without this budget is the production system itself).

Indicative fee shape for a mid-market engagement with a small integrator (two senior, one mid; US market, 2026) — ranges below are a composite operator-estimate triangulated from the public Parlance Labs services page (floor: $285.5K advisory / 8 weeks, cross-referenced in Mon's Segment 5 and Wed's Story 1), the Distyl AI enterprise-AI-services market positioning (validated by the 2025 $175M / $1.8B funding round referenced below[^21]), and four boutique-AI-services practitioner reports aggregated through late 2025; they are *not* sourced from a single published survey and a buyer should expect ±30% variance against any specific engagement shape:

- Discovery: $15k–$35k over 2–4 weeks; T&M-with-cap.
- POC: $40k–$90k over 4–8 weeks; flat fee; token cost pass-through above $2k/month.
- Pilot: $75k–$180k over 8–16 weeks; flat fee; criteria-based termination right; pre-negotiated production conversion price.
- Production: $8k–$25k/month retainer for first 6 months, then annual review; includes eval regression, drift monitoring, one change-request per quarter, incident response.

These numbers assume the engagement shape described; they scale up roughly 2–4× for Fortune 500 buyers (longer discovery, more stakeholders, heavier compliance review) and down 30–50% for SMB and boutique-professional-service buyers. They move in line with Accenture's reported generative-AI bookings run-rate ($5.9B booked over 12 months to August 2025) in the direction of higher — enterprise services firms price discovery alone higher than a boutique prices POC.[^21]

## Layer 5 — Designing exit ramps so the project can die cheaply

The phrase "exit ramp" gets used two ways. It is worth separating them.

### Exit ramp type 1 — kill at phase gate

The good case. A phase gate produces evidence, and the evidence says the project should not continue. Either because the eval rubric didn't clear the bar (POC exit), the pilot didn't move the business metric (pilot exit), or the outcome that looked worthwhile at discovery looks worthless now that the sponsor understands the cost envelope (any exit). The engagement should end, on good terms, with the buyer having spent roughly the cost of the phases completed and the seller having been paid for work delivered.

The mechanics: each phase-gate deliverable includes an explicit go/no-go recommendation, signed by the builder; the buyer signs either go (triggering the next phase fee) or no-go (triggering the wind-down, data handback, and any remaining materials); no penalty on either side for a no-go. The kill criterion metric is named in advance ("POC exits no-go if the eval pass-rate on the held-out sample stays below 70% after two iteration cycles"). The sponsor's political cover for the no-go is explicit ("the engagement was designed to be killed here if the evidence went this way").

This pattern is what Block 0 Week 3 Wednesday's *kill criteria* concept becomes in commercial form. Technical kill criteria become contractual exit rights.

### Exit ramp type 2 — involuntary exit at any point

The messier case. Something outside the project forces one side or both to exit: the sponsor leaves (no replacement), the buyer's industry shifts (M&A, regulation, budget freeze), the vendor's terms change materially (retention defaults, deprecation of a critical endpoint, pricing shift outside the pass-through envelope), the seller's firm changes (key staff leave, insolvency), or a compliance finding makes the project unshippable.

The contract clauses that handle this cleanly, collected from the 2025–26 AI-contract writing — CCSD Council, Morgan Lewis, Tascon, and several legal-ops blogs — cluster into five categories:[^8][^11][^22]

1. **Termination for convenience**, either side, with 60–90 day notice, with fees due only for work-in-progress.
2. **Termination for cause** with specific triggers: sponsor change without a named successor within 30 days; vendor material-terms change outside the pass-through envelope; compliance finding; specific eval-metric failure.
3. **Data handback and portability**: return or delete client data within 30 days with a deletion certificate; export of prompts, logs, embeddings, fine-tunes in open formats (JSON/CSV/Parquet); 90 days of transition support.
4. **Fine-tune ownership**: weights trained on buyer data belong to the buyer at termination, regardless of which side ran the training run.
5. **IP allocation**: base-model IP to the model provider; custom prompts and evals to the engagement; fine-tunes to the buyer; generalized patterns the seller learns can be reused non-competitively.

A rule of thumb: the total termination section should be longer and more specific than the deliverables section. Buyers who push back on termination clauses as "unnecessary distrust" are signalling that they don't understand AI vendor risk. The right builder response is to frame the clauses as mutual protection — the buyer's right to exit if the seller underperforms is the seller's right to exit if the buyer fails to provide data or sponsorship.

### The "soft exit" at end of POC

A specific sub-pattern worth isolating. The end of POC is the most common kill point in a well-structured AI engagement and the moment both sides are under the most emotional pressure to continue. The builder has working demo; the buyer has sunk cost; the sponsor has a deck to present. The temptation is to promote to pilot on momentum.

A *soft exit* at POC works like this. The POC deliverable bundle includes three documents: the system and its eval results; a go/no-go recommendation from the builder with the rubric evidence; and a *pre-mortem* where the builder and sponsor together list the top five reasons the pilot would fail if promoted, each mapped to a specific mitigation or acknowledgement. The pre-mortem is the de-escalation instrument. It forces both sides to write down the risks they'd otherwise glide past. If any of the top five is unmitigated, the default is soft exit: pause, revisit in 90 days, no fee commitment for pilot. If all are mitigated, promote. The mechanism converts momentum into evidence and makes the kill cheap when it should be cheap.

## Layer 6 — Operator war stories

Three specific engagements, with names, numbers, and dates. The detail is the education.

### Story 1 — Hamel Husain's 35+ engagements and the "eval-infrastructure-first" move

Hamel Husain's *Field Guide to Rapidly Improving AI Products* (March 24, 2025) reports patterns from 30+ AI engagements. The single operational move he attributes to the engagements that reached production: building evaluation infrastructure *before* committing to features.[^7] In practice, this means the first 2–3 months are not "we're building your agent" but "we're building the measurement apparatus that will tell us whether your agent works." Buyers who don't yet understand AI engineering push back because it feels like buying scaffolding. Builders who hold the line report that the scaffolding is the engagement; the features fall out of what the scaffolding shows.

The commercial translation: discovery + early POC are sold as *evaluation-infrastructure sprints*, not as "build a prototype." The deliverable is the eval harness and the rubric alignment, with a minimum viable system attached. The go/no-go at end of POC is a rubric-pass decision, not a demo reaction.

This is the operator move that most closely maps to the Block 0 Week 3 Wednesday walking-skeleton pattern. Block 1 Thursday adds: sell the skeleton, price the skeleton, gate on the skeleton.

### Story 2 — the Omdia "balanced perspective" on POC conversion

Omdia published *AI POCs to production: a balanced perspective* in November 2025, arguing against the dominant "95% fail" narrative by distinguishing between POCs designed to be production-bound and POCs designed as learning exercises — and noting that the latter category is routinely reported as failure when it was never intended to convert.[^23] Omdia's operator recommendation: name the POC type at kickoff (production-bound vs learning), and set conversion expectations accordingly. A "learning POC" that produces a clear no-go is a successful engagement at a fraction of the cost of a production-bound engagement that limped through gates.

Commercial translation: at the end of discovery, the engagement document should explicitly state whether the POC is *production-bound* (the buyer has committed to pilot conditional on criteria) or *exploratory* (the buyer has committed to evidence, not to continuation). These have different pricing, different timelines, and different success definitions. Conflating them is a primary cause of the headline failure numbers.

### Story 3 — Accenture's agentic scaling and the industrial-scale version

Accenture reported generative AI and agentic AI revenues tripled year-over-year to $2.7 billion, with bookings nearly doubling to $5.9 billion in the 12 months ending August 2025.[^21] The firm committed $3 billion to expanding its Data & AI practice with plans to double the AI specialist headcount to 80,000; Deloitte announced $4 billion in matching investment with Google Cloud and ServiceNow alliances for agentic adoption.

At that scale, the phase structure we've described is the operating model, with two adaptations: discovery phases compress (weeks, not months) because the firm reuses patterns across engagements; production phases extend (multi-year retainers) because the integration footprint is deeper. The risk model is the same. The clauses — vendor notice, data portability, sponsor change, eval-regression ownership — are the same. What changes is the pricing: discovery alone at an Accenture-tier engagement is routinely $250k+ for a Fortune 500 buyer, with the full four-phase engagement running $5M–$50M. The $250k+ discovery figure is an operator estimate — not a single published Accenture line item — triangulated from the disclosed $5.9B FY2025 bookings ÷ ~6,000 projects (~$1M average project size, with the long tail going to $50M+)[^21] and the Q1 FY2026 $2.2B-in-one-quarter run-rate[^21], cross-referenced against Mon's Segment 1 analysis of Big Four pricing dominance; treat it as the shape implied by the bookings math, not as a quotable published number. A Fortune 500 buyer seeking a fixed Accenture-published discovery rate will not find one — the Big Four do not publish rate cards — but the aggregate bookings/project arithmetic is the most defensible public anchor available in 2026.

Commercial translation for an independent or boutique: the *same structure* works at 1/10th to 1/100th the scale. The enterprise firms aren't doing something fundamentally different; they are running the same phase gates with more people, more compliance review, and more stakeholders. A boutique that runs the structure cleanly with one senior on each side of the table can out-convert a Big Four engagement that runs the same structure under committee.

## Runnable experiment — direct Claude Code to plan a phased engagement, then stress-test it

You will produce two artifacts. Allow 90 minutes. Do this for a real candidate engagement on your plate if you have one; if not, pick one from the cross-domain prompts below.

**Cross-domain engagement prompts** (pick one or supply your own):

- *Legal ops*: intake-triage agent for a mid-market law firm (200 lawyers, corporate / litigation / employment practice).
- *Finance*: month-end variance-reconciliation assistant for a Series C SaaS (40 engineers, consolidated reporting across two geographies).
- *Marketing*: brand-compliant content drafting agent for a B2B manufacturer (internal comms, sales enablement, trade press).
- *Operations*: incident-triage agent for a regional logistics operator (400 trucks, dispatch + compliance + customer comms).
- *Research*: literature-mapping agent for a biotech R&D team (10 researchers, targeted therapeutics).
- *Customer support*: tier-1 deflection agent for a D2C brand (200k monthly tickets, 60% reset-password and return-label).

**Phase 1 — Plan.** In Claude Code, paste:

> *Given this proposed AI engagement [paste your chosen engagement or your real one], generate a four-phase plan (discovery, POC, pilot, production). For each phase provide: phase goal, deliverables, duration, fee range with justification, kill-criteria metric with threshold, go/no-go gate question, and named owner on each of the five AI risks (data, drift, vendor, eval, sponsorship). Format as a table. Then provide a second table: the five exit-ramp contract clauses specific to this engagement (termination for convenience, termination for cause triggers, data handback, fine-tune ownership, IP allocation). Keep output under 1500 words.*

**Phase 2 — Stress test.** In a fresh Claude.ai conversation (or Claude Code, whichever you prefer), paste the plan and prompt:

> *You are the CFO of the buyer company. You have seen the attached four-phase plan. You have budget pressure. List the 10 most likely failure points for this engagement, each mapped to which phase surfaces it, and for each name one clause or process you'd insist on before signing.*

Record the CFO's list verbatim. Then run a second stress-test with a different persona:

> *You are the general counsel of the buyer company. Review the five exit-ramp clauses. For each clause, either (a) approve as-written, (b) propose a specific amendment, or (c) flag as unacceptable and explain why.*

**Phase 3 — Rewrite.** Take the original plan and the two stress tests. Rewrite the phase plan and the exit-ramp clauses to address the top five concerns across both personas. Mark each change with the concern it addresses.

**Output:** two documents saved, dated, and filed with today's date in the filename.

**What you are learning.** Not the specific plan — that's disposable. You are learning to feel where the phase structure gets thin under CFO pressure and where the contract clauses get brittle under counsel pressure. Most first-draft plans are thin at pilot (it's the hardest phase) and brittle at exit (the clauses sound reasonable until counsel reads them). After running this three times on three different engagements, you will have an internal pattern library.

## Problem set

1. **Map one real or hypothetical AI engagement to the four phases.** List the kill-criterion metric for each phase, with threshold and measurement. If the metric for a phase is "we'll know it when we see it," the phase is not scopable and the engagement is not ready. Pass: every phase has a measurable criterion; fail: any phase uses a vibes-based criterion.

2. **Take a position: the pilot trap is primarily a contract-structure problem, not a technical-fit problem.** Argue yes or no in ≤400 words. Cite ≥2 data points and ≥2 named operators from opposing positions (Morgan Lewis / Planet A Ventures on the contract side; Hamel Husain / Gartner on the technical-fit side). Defensible pass: your position explicitly addresses the strongest version of the counter-argument.

3. **Design a soft-exit clause for end-of-POC.** Produce a ≤250-word clause that includes: (a) the POC deliverable bundle, (b) the pre-mortem format, (c) the soft-exit default trigger, (d) the re-engagement option. Test it against the buyer-counsel persona in Claude.ai — if counsel flags it as unfair to the buyer, iterate.

4. **For an AI project of your choice, list the top 5 risks across the five axes (data, drift, vendor, eval, sponsorship) with named mitigation owner for each.** Each risk must be specific to the engagement, not generic. "Data quality is a risk" fails. "The 2019–2023 case file PDFs have inconsistent OCR and the buyer's DMS team is not resourced to clean them before POC" passes.

5. **Defend or reject: "In 2026, a first-engagement AI project without a 4–6 week discovery phase is strictly underpriced."** Argue in ≤350 words, citing at least two of: MIT NANDA 2025, BCG AI Radar 2025, McKinsey State of AI 2025, Gartner 2024–25, Hamel's *Field Guide*. The honest answer is probably "yes, with exceptions" — name the exceptions.

## Common failure modes at scale

- **Compressing discovery to a kickoff workshop.** The buyer's pressure for speed collapses a 3–4 week discovery into a two-day workshop. The workshop produces a shared hallucination that feels like alignment. POC discovers the gap. Cost to recover = cost of one POC plus political capital.
- **POC demo inflation.** The POC works on curated inputs; the builder and sponsor both know it; neither says so in the demo. Pilot reveals the long tail. The builder is blamed for "overselling"; the sponsor is blamed for "under-scoping." Both are right; the failure was upstream at the rubric-alignment step.
- **No named secondary sponsor.** Primary sponsor leaves mid-pilot. The project floats for 6–8 weeks while a new owner is appointed, then gets quietly de-prioritized. The buyer pays for a pilot that never produces a production decision.
- **Token cost pass-through missing.** API pricing moves 20%+ during the POC-to-pilot window. Builder eats it or triggers an awkward change order. Either way, trust drops. Had the clause been in the SOW, the conversation would have been a line-item adjustment, not a renegotiation.
- **Eval rubric built by the builder alone.** The rubric measures what the builder can build; the sponsor's actual success criteria aren't reflected. POC passes; pilot fails. The builder re-does discovery inside pilot. Cost = pilot pace, discovery deliverable.
- **No data-handback clause.** Engagement ends, amicably or otherwise. The buyer asks for embeddings and fine-tuned weights. The contract is silent. A 6-week legal negotiation follows. The buyer learns that silence in the SOW is a default in favor of the seller.
- **Confusing POC learning goal with POC conversion goal.** The seller treated the POC as production-bound; the buyer treated it as exploratory. At POC close, the buyer is surprised by the pilot ask and the seller is surprised by the hesitation. Omdia's November 2025 note is the explicit correction.[^23]
- **Outcome-tied pricing on a first engagement.** The builder has no case studies, the buyer has budget pressure, and they split a contingent 30% fee on a KPI the builder doesn't fully control. The engagement hits 80% of the KPI; the builder takes a margin hit; both parties feel cheated.

## Open questions — what's not settled

**1. Is eval-driven development the default, or an overfit?** Hamel Husain's *Evals FAQ* (Jan 2026) pushes back on the idea that you should write evaluators before observing production errors — he argues that practicing EDD as a ritual produces evaluators for imagined errors rather than real ones.[^15] The counter-position, advanced by most ML-systems textbooks and Shreya Shankar's 2024 UIST paper, is that eval infrastructure must exist before production to catch errors when they appear.[^14] The honest synthesis: eval *infrastructure* is load-bearing from POC; eval *rubric* specificity can and should evolve as production logs accumulate. But the phrase "eval-driven development" is used to mean both, and which you mean matters.

**2. Does build-measure-learn survive AI eval overhead?** The Lean Startup loop assumes cheap, fast measurement. AI systems have a dual measurement burden — the business outcome (classic B-M-L) and the system quality (eval rubric with human alignment). Each iteration costs more. Andrew Ng's AI Fund operating pattern (MVPs built over year-long refinement phases, not weekly sprints) is one reaction; tight eval-loop teams running daily iteration on a narrow surface is another.[^24] No consensus. The right answer is probably domain-specific: high-volume consumer AI can run daily eval loops; regulated-industry enterprise AI can't.

**3. The MIT NANDA 95% number — research finding or press artefact?** The July 2025 report is rigorous in methodology; the "95% fail" framing has been aggressively contested by Medium-tier critics (*The Ai Consultancy*'s *What it gets wrong* piece) and by Unite.AI's response piece, both arguing that the denominator is too broad and the P&L threshold too narrow.[^25][^26] The finding may still be broadly correct; the framing is doing work. Operator implication: use the research, interrogate the framing, and do not let either party in a sales conversation use the 95% number as a conclusion-by-citation.

## Reviewer lens — named critics with specific disagreements

- **Hamel Husain (parlance-labs, *Field Guide to Rapidly Improving AI Products*, Mar 2025).** Husain would push back on Layer 1's phase structure as under-weighting the eval-infrastructure work relative to the "build the system" work. His argument, per the *Field Guide*: the first 2–3 months should be *mostly* evaluation infrastructure, not discovery + POC as parallel tracks; treating discovery as primarily a business-scoping exercise and POC as primarily a technical-prototype exercise smuggles in a waterfall model he argues against. The correction he'd urge: reframe discovery and early POC as one integrated "evaluation-infrastructure sprint" with the business scoping folded in as rubric definition.

- **Shreya Shankar (UC Berkeley, *Who Validates the Validators?*, UIST 2024).** Shankar would push back on Layer 2's eval-risk section for treating LLM-judge validation as a single step ("validate at >90% alignment") rather than as a continuous discipline. Her paper documents that LLM-judge alignment drifts over time as the data distribution shifts and the judge model updates; a single one-time validation is a false confidence signal. She'd insist the eval-risk axis should include *judge-model-drift* as a sub-category, with a monthly re-alignment cadence, not just rubric alignment at POC.

- **Patrick McKenzie (patio11, Kalzumeus *Greatest Hits*).** Patio11 would push back on Layer 4's pricing archetypes — particularly the dismissal of outcome-tied pricing for first-engagement work — as insufficiently distinguishing between *outcome-tied* and *value-priced*. His position, from his writings on consulting pricing: the right move for a first-engagement operator is to price at the value created (which can be high) but to structure payment as phase-gated flat fees (which can be predictable), not to hitch payment to a contingent outcome (which is dangerous for the reasons the lesson names). The lesson's hybrid archetype is close to his position; he'd argue for making that distinction explicit earlier.

- **Teresa Torres (Product Talk).** Torres would push back on Layer 5's soft-exit pattern as too transactional for AI projects specifically. Her 2025 writing on AI product discovery argues that AI features have unusually high post-launch variance and that continuous discovery must run *through* pilot and production, not end at the phase gates. She'd propose a fifth phase after production — "continuous discovery retainer" — as a standard line item, with a soft-exit equivalent at each quarterly review rather than only at phase transitions.

- **Jonathan Stark (value-pricing podcast and bootcamp).** Stark would push back on the fee ranges in Layer 4 as grounded in seller cost rather than buyer value. His bootcamp teaches that discovery at a "T&M-with-cap" anchors the fee to hours, which teaches the buyer to think in hours for the rest of the engagement; he'd propose a flat discovery fee priced to the decision value ("we will produce a defensible go/no-go on a $500k pilot commitment, for a $25k–$40k discovery fee") even when the scope is uncertain. The counter is that uncertain scope produces seller risk the flat fee has to absorb — which is precisely the tradeoff the lesson navigates by hybrid.

## Further reading

**Must-read**

- Hamel Husain, *A Field Guide to Rapidly Improving AI Products*, Mar 24 2025. The single best operator-level source on phase-wise AI engagements.[^7]
- MIT Project NANDA, *The GenAI Divide: State of AI in Business 2025*, Jul 2025.[^2]
- Morgan Lewis, *Negotiating AI Provisions in Commercial and Technology Contracts: Where the Market Is Heading*, April 2026. The cleanest practitioner source on what clauses are stabilizing and which remain contested.[^11]
- BCG, *The Widening AI Value Gap*, Sep 2025.[^16]

**Recommended**

- Gartner press release, *30% of Generative AI Projects Will Be Abandoned After Proof of Concept by End of 2025*, Jul 29 2024.[^17]
- McKinsey QuantumBlack, *The state of AI in 2025: Agents, innovation, and transformation*, Nov 2025.[^1]
- Omdia, *AI POCs to production: a balanced perspective*, Nov 2025.[^23]
- CCSD Council, *Third-Party AI Risk: The Five Clauses Your Contracts Can't Skip in 2025*.[^8]

**Optional**

- Planet A Ventures, *Lesson 4: Escaping Pilot Hell*, 2024. Industrial-adoption lens, directly applicable to AI.[^18]
- Shreya Shankar et al., *Who Validates the Validators?*, UIST 2024.[^14]
- Hamel Husain, *Q: Should I practice eval-driven development?* (*Evals FAQ*), Jan 2026.[^15]
- Jonathan Stark, *The Obvious Switch to Value Pricing*, Dec 2024 daily post.[^19]
- Tascon Legal, *AI Clauses In Contracts: The Practical Guide For 2025*.[^22]

## Citations

[^1]: McKinsey QuantumBlack, *The state of AI in 2025: Agents, innovation, and transformation*, November 2025 (39% EBIT linkage; 6% high performers with >5% EBIT; 23% scaling agentic systems, 39% experimenting). https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

[^2]: MIT Media Lab, Project NANDA, *The GenAI Divide: State of AI in Business 2025*, July 2025 (95% of integrated pilots show no measurable P&L impact; $30–40B enterprise spend; 300+ disclosed initiatives reviewed). Primary report summary at https://www.aigl.blog/state-of-ai-in-business-2025/ and Fortune coverage at https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/

[^3]: BCG, *AI Radar 2025: From Potential to Profit — Closing the AI Impact Gap*, January 2025 (5% of firms "future-built"; 35% scaling; investment allocation norms). https://www.bcg.com/publications/2025/closing-the-ai-impact-gap ; slideshow https://web-assets.bcg.com/0b/f6/c2880f9f4472955538567a5bcb6a/ai-radar-2025-slideshow-jan-2025-r.pdf

[^4]: IDC / Lenovo AI POC-to-production survey, March 2025 (88% of observed POCs do not reach wide-scale deployment; for every 33 POCs, only 4 graduate to production). Primary coverage: Paula Rooney, *88% of AI pilots fail to reach production — but that's not all on IT*, CIO.com, Mar 2025, https://www.cio.com/article/3850763/88-of-ai-pilots-fail-to-reach-production-but-thats-not-all-on-it.html ; secondary synthesis: Omdia, *AI POCs to production: a balanced perspective*, Nov 2025, https://omdia.tech.informa.com/blogs/2025/nov/ai-pocs-to-production-a-balanced-perspective

[^5]: Gartner, *AI Projects in I&O Stall Ahead of Meaningful ROI Returns*, April 7 2026 (40% of agentic AI projects forecast cancelled by end of 2027; only 28% of I&O AI use cases fully succeed). https://www.gartner.com/en/newsroom/press-releases/2026-04-07-gartner-says-artificial-intelligence-projects-in-infrastructure-and-operations-stall-ahead-of-meaningful-roi-returns

[^6]: CIO.com, *88% of AI pilots fail to reach production — but that's not all on IT*, 2025 (synthesis of Deloitte, Informatica, S&P Global data). https://www.cio.com/article/3850763/88-of-ai-pilots-fail-to-reach-production-but-thats-not-all-on-it.html

[^7]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products*, Mar 24 2025 (phase structure: 2–3 months feasibility/foundation, 6+ weeks prototype/testing, scaling-with-trust with >90% human–judge alignment; "teams that succeed barely talk about tools at all"). https://hamel.dev/blog/posts/field-guide/

[^8]: CCSD Council, *Third-Party AI Risk: The Five Clauses Your Contracts Can't Skip in 2025*. https://www.ccsdcouncil.org/third-party-ai-risk-the-five-clauses-your-contracts-cant-skip-in-2025/

[^9]: Gartner, *Lack of AI-Ready Data Puts AI Projects at Risk*, February 26 2025 (63% of orgs lack or are unsure about AI-ready data; 60% abandonment prediction through 2026). https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk

[^10]: Fulcrum Digital, *AI Model Drift in Production: What Enterprises Must Monitor*, 2025 (p50/p95/p99 latency SLA monitoring norms; data vs concept vs model drift taxonomy). https://fulcrumdigital.com/blogs/ai-model-drift-in-production-what-enterprises-must-monitor/

[^11]: Doneld G. Shelkey, *Negotiating AI Provisions in Commercial and Technology Contracts: Where the Market Is Heading*, Morgan Lewis Sourcing blog, Apr 2 2026 (AI service scope definitions for agentic AI, performance standards and accuracy thresholds, IP ownership of AI-generated outputs, regulatory compliance allocation, end-of-term planning including transition assistance and data return/deletion). https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/04/negotiating-ai-provisions-in-commercial-and-technology-contracts-where-the-market-is-heading

[^12]: OpenAI policies page and Microsoft Azure OpenAI Data Retention 2025 Q&A (zero data retention as opt-in for API/Enterprise; 2024–25 changes to enterprise retention defaults). https://openai.com/policies/ ; https://learn.microsoft.com/en-us/answers/questions/2181252/azure-openai-data-retention-privacy-2025

[^13]: Methodmi, *Vendor Lock-In Escape Plan for Procurement Platforms (Exit Clauses + Data Portability)*, 2026 (termination for convenience, data portability in JSON/CSV/Parquet, 90-day transition support, fine-tune weight ownership, 12-month / 6-month API-deprecation notice). https://methodmi.com/vendor-lock-in-escape-plan-for-procurement-platforms/

[^14]: Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya G. Parameswaran, Eugene Wu, *Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences*, UIST 2024, October 2024. https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.pdf

[^15]: Hamel Husain, *Q: Should I practice eval-driven development?* — *LLM Evals FAQ*, January 2026 (EDD as ritual creates evaluators for imagined errors; better to start with error analysis on production traces). https://hamel.dev/blog/posts/evals-faq/should-i-practice-eval-driven-development.html

[^16]: BCG, *Are You Generating Value from AI? The Widening Gap*, September 2025 (leaders 1.7× revenue growth, 3.6× three-year TSR, 1.6× EBIT margin; 80%+ investment allocation to reshaping functions and inventing offerings). https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap ; full PDF https://media-publications.bcg.com/The-Widening-AI-Value-Gap-October-2025.pdf

[^17]: Gartner, *Gartner Predicts 30% of Generative AI Projects Will Be Abandoned After Proof of Concept By End of 2025*, July 29 2024 press release (abandonment drivers: poor data quality, inadequate risk controls, escalating costs, unclear business value). https://www.gartner.com/en/newsroom/press-releases/2024-07-29-gartner-predicts-30-percent-of-generative-ai-projects-will-be-abandoned-after-proof-of-concept

[^18]: Planet A Ventures, *Lesson 4: Escaping Pilot Hell*, 2024 (contract design as primary lever for pilot-to-production conversion in industrial adoption; directly applicable to AI). https://planet-a.medium.com/lesson-4-escaping-pilot-hell-cd9ea0192809

[^19]: Jonathan Stark, *The Obvious Switch to Value Pricing with Jonathan Stark*, daily post Dec 20 2024; Value Pricing Bootcamp materials. https://jonathanstark.com/daily/20241220-2155-the-obvious-switch-to-value-pricing-with-jonathan-stark ; https://jonathanstark.com/vpb

[^20]: Patrick McKenzie (patio11), *Patio11's Greatest Hits* and *Talking About Money* (outcome-tied pricing works only with case studies, buyer influence over outcome, and ungameable metrics; $30k/week consulting rate progression; $60k B2B SaaS engagement anchor). https://www.kalzumeus.com/greatest-hits/ ; https://www.kalzumeus.com/2015/05/01/talking-about-money/

[^21]: CIO Dive, *Accenture completes 'reinvention' as generative AI revenues roll in*, 2025 (GenAI + agentic revenues tripled to $2.7B; bookings nearly doubled to $5.9B in 12 months ending Aug 2025; Q1 FY2026 GenAI bookings $2.2B). https://www.ciodive.com/news/accenture-generative-ai-revenue-skills-training-data-modernization/761161/ ; Accenture press release https://newsroom.accenture.com/news/2023/accenture-to-invest-3-billion-in-ai-to-accelerate-clients-reinvention

[^22]: Tascon Legal, *AI Clauses In Contracts: The Practical Guide For 2025*. https://tasconlegal.com/ai-clauses-in-contracts-the-practical-guide-for-2025/

[^23]: Omdia (Informa), *AI POCs to production: a balanced perspective*, November 2025 (production-bound vs learning POC distinction; IDC 12% conversion stat). https://omdia.tech.informa.com/blogs/2025/nov/ai-pocs-to-production-a-balanced-perspective

[^24]: AI Fund, *Andrew Ng*; TechCrunch coverage, *Andrew Ng plans to raise $120M for next AI Fund*, June 27 2024 (pre-seed to year-long refinement MVP pattern; agent workflows as next stage). https://aifund.ai/team-member/andrew-ng/ ; https://techcrunch.com/2024/06/27/andrew-ng-plans-to-raise-120m-for-next-ai-fund/

[^25]: The Ai Consultancy, *The MIT "95% of GenAI Pilots Fail" Report: What It Gets Wrong and What Leaders Should Do Instead*, 2025. https://medium.com/@ai_93276/the-mit-95-of-genai-pilots-fail-report-what-it-gets-wrong-and-what-leaders-should-do-instead-3a6a1bd7a3d5

[^26]: Unite.AI, *Looking Into MIT NANDA July 2025 Report: Why 95% AI Pilot Failure Rate Is Not the End*, 2025. https://www.unite.ai/looking-into-mit-nanda-july-2025-report-why-95-ai-pilot-failure-rate-is-not-the-end/

[^27]: Claude Fable 5 / Mythos 5 export-control suspension — launched June 9 2026 ($10/$50 per M tokens, first public "Mythos-class" tier); US export-control directive June 12 2026 suspended access for all foreign nationals worldwide (Anthropic disabled the models globally); Department of Commerce lifted controls and Anthropic redeployed globally July 1 2026. Anthropic, *Statement on the US government directive to suspend access to Fable 5 and Mythos 5*, https://www.anthropic.com/news/fable-mythos-access ; CNBC, *Anthropic says Trump admin has lifted export controls on Claude Fable 5 and Mythos 5*, June 30 2026, https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html ; Forbes, June 16 2026, https://www.forbes.com/sites/anishasircar/2026/06/16/anthropic-disabled-fable-5-and-mythos-5-after-a-us-export-control-order-heres-what-happened/ (verified 2026-07-17)

_last_verified: 2026-07-17_
