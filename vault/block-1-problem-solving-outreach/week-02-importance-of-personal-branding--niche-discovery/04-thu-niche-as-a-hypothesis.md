---
type: lesson
block: block-1-problem-solving-outreach
week: week-02
day_of_cycle: 4
day_name: thu
session_slug: niche-discovery
date_due: 2026-05-28
tags: [niche-discovery, positioning, three-axis-model, ai-services-market, falsifiable-hypothesis, dunford-vs-kahl, vertical-capability-seniority, ai-sdr-category, microconf, operator-trajectories]
sources:
  - upwork-in-demand-skills-2026
  - fiverr-business-trends-2025
  - menlo-state-of-ai-enterprise-2025
  - bessemer-state-of-ai-2025
  - bcg-ai-value-gap-2025
  - microconf-state-indie-saas-2025
  - dunford-lennys-podcast-2026
  - dunford-obviously-awesome-2019
  - kahl-bootstrapped-founder-intersection-2024
  - priestley-key-person-influence-2024
  - jason-liu-indie-consulting-maven-2025
  - hamel-husain-parlance-labs-2025
  - clay-groundtruth-ai-sdr-2025
  - pavilion-11x-ai-sdr-future-2025
  - turing-vertical-ai-agents-2025
  - finro-vertical-ai-valuation-2025
  - indexdev-freelance-rates-2025
last_verified: 2026-04-16
word_count_target: 6000
---

# Niche as a hypothesis — the three-axis model and why most AI freelancers fail on one axis

## Why this matters

Your niche is not a poetic statement. It is a falsifiable hypothesis about where your commercial pipeline will actually come from — a bet you run against the calendar with measurable success criteria, the way a product team would run an A/B test. Most first-year AI consultants and AI-native operators do not treat it that way. They write a LinkedIn headline — *"AI workflow consultant helping teams ship faster"* — and declare niche discovery complete. Then they spend six months outbound-messaging across three unrelated industries, four unrelated capabilities, and every buyer seniority from ops analyst to CFO, and wonder why reply rates stay at 1–2%, why every proposal is custom, and why their pricing keeps drifting back to hourly.

The failure is not effort and it is not intelligence. It is a one-axis conception of niche in a three-axis market. This lesson repairs that conception. By the end of it you will be able to (1) place yourself on the **three-axis model** — vertical × capability × buyer-seniority — and explain which axis is loose, which is tight, and why that combination either compounds or bleeds pipeline; (2) run a niche hypothesis the way you'd run an eval harness, with explicit success criteria, N, and kill conditions; (3) diagnose the "everything store" failure mode in your own positioning before it costs you a quarter; (4) take a defensible position on the **Dunford vs Kahl** disagreement about whether your niche is defined by who you serve or what you do, and resolve it for your specific context; (5) read a named operator's niche trajectory over 24 months and see which axis moves correlated with revenue inflection — then apply the same diagnostic to your own.

This is week two of the commercial-execution block. Week 1 gave you the sales mechanics and Monday–Wednesday of this week gave you the brand layer. This lesson is the bridge to Friday (quantitative validation) and Saturday (positioning and category). If you leave this lesson with one hypothesis you could run next week, not one aspiration you'll "figure out eventually," the lesson worked.

## Prerequisites

- You have a working sense of who you sell to (even if fuzzy) and what you sell (even if over-broad). If you have never pitched a single engagement, run this lesson with a hypothetical offer — the diagnostic still holds.
- You can read a three-column CSV and direct Claude Code to build one from public data (LinkedIn, Crunchbase, company websites). No hand-coding required — this is an AI-native builder's exercise.

## Layer 1 — The three-axis model: vertical × capability × buyer-seniority

Start with a concrete asymmetry. Bessemer Venture Partners' *State of AI 2025* tracks the rise of vertical AI — AI applications designed for a specific industry rather than horizontal utilities — and reports that vertical AI applications make up 40% of top-growing private AI companies in 2025, with the category growing fast enough that BVP now considers "vertical AI" its own asset class.[^1] Menlo Ventures' enterprise-AI survey for 2025 reports vertical AI spending at $3.5B — up roughly 6× from 2024 — and gross margins around 65%, meaningfully above undifferentiated horizontal SaaS.[^2] At the same time, generalist AI freelancers on Upwork doing "AI consulting" as a single skill tag saw *slower* year-over-year rate growth than specialists on named capabilities (AI video generation +329%, AI integration +178%, AI data annotation +154%, AI chatbot development +71% YoY).[^3] Index.dev's 2025 freelance-rates report puts AI/ML specialists at $100–$200/hr versus generalist software engineers at $60–$120/hr — a 40–60% premium that widened over 2025 as the supply of "I do AI" generalists outgrew demand faster than specialist supply did.[^4]

Hold both facts. Vertical AI (industry-specific) is winning at the product-company level. Specialist capability (named primitive) is winning at the individual-operator level. That is not a contradiction — it's the signature of a three-axis market where the axes co-vary.

A useful niche description in AI services names *all three* of these axes:

1. **Vertical** — the industry you serve. Manufacturing SMBs. Mid-market e-commerce. Am Law 100 firms. Multi-site healthcare clinics. Indian D2C brands. Regional credit unions. Film VFX studios. "Everyone" is not a vertical.

2. **Capability** — the AI primitive or domain you deliver. RAG-over-documents. Voice-agent deployment. LLM-ops and eval harness design. AI-SDR / outbound agent systems. Coding-agent integration. Internal-knowledge search. Content-generation pipelines. "AI" is not a capability.

3. **Buyer seniority** — the role of the person who decides to spend the money. Operator / line-manager (solving their own pain, budget $1–$10k). Function-head / director (departmental remit, budget $10–$100k). VP or CXO (strategic mandate, budget $100k+, procurement involved). The selling motion, the story, the artifacts, and the trust stack required are radically different at each level.

Plot yourself at the intersection of all three and you get a specific, testable cell. *"RAG-over-contracts for Am Law 100 practice-group leaders."* *"Voice-agent deployment for mid-market dental DSOs, decision-maker is the COO."* *"LLM-ops eval harness for Series-B B2B SaaS, decision-maker is the VP of Engineering."* Each of those is a hypothesis you can falsify in weeks, not a direction you'll "explore."

Most AI freelancers fail on one specific axis: **vertical**. They tighten on capability ("RAG consultant"), they tighten on seniority implicitly (whoever takes the call), and they leave vertical wide open. Why? Because capability is the axis they're proudest of — they earned it. Vertical feels arbitrary, limiting, possibly beneath them. Seniority feels like something that happens *to* the deal rather than a choice. The three-axis framing forces you to confront both omissions at once.

The single sharpest diagnostic in this lesson: **look at your last 10 outbound messages and ask which axis is specified.** If capability is the only axis that shows up — if your message could have been sent to a dentist, a CMO, and a fintech founder without modification — your niche is one-axis. The market will punish that.

### Axis interaction — why tightening vertical often loosens the other two profitably

The non-obvious property of the three-axis model is that axes are not independent. Tightening vertical usually *enables* you to widen capability profitably, because within a vertical, buyers want the end-to-end solution rather than a single primitive. The credit-union AI operator who starts with loan-underwriting RAG ends up selling agent-based member support, then internal-policy search, then compliance-document summarization — all to the same CFO/COO pair at the same 200 U.S. credit unions. Menlo's 2025 enterprise report notes precisely this pattern: vertical AI vendors expand ARPA (average revenue per account) at 1.4–2× the rate of horizontal AI vendors because the trust-stack cost of landing inside an account amortizes across more surface area.[^2]

Tightening capability without tightening vertical has the opposite property: the capability cross-pollinates into unrelated verticals that each need their own sales cycle, their own trust stack, their own compliance story. You end up with thirty one-off deals in thirty different worlds, and your second year looks like your first.

## Layer 2 — Niche as a falsifiable hypothesis, not a poetic statement

"We help ambitious mid-market companies unlock AI's potential to transform how they work." Count the falsifiable claims in that sentence. Zero. It could be true for anyone, which means it is predictive of nothing. Compare it to: "We help U.S. credit unions with $500M–$2B in assets deploy AI-underwriting agents that cut loan-decision time from hours to under fifteen minutes." Count the falsifiable claims: the vertical (U.S. credit unions in a specific AUM band), the capability (AI-underwriting agents), the outcome-metric (loan-decision latency under 15 minutes), the implicit buyer (CFO/COO, because that's who owns underwriting latency). You can run a 30-account outbound against the second statement in 14 days. You cannot run an experiment against the first statement at all.

The hypothesis form that works for AI services looks like this:

> **If my niche is [vertical] × [capability] × [seniority], then [N] well-crafted outbound touches in [time window] will produce [≥M first replies], [≥K qualified discovery calls], and [≥J signed pilot / paid discovery] at conversation depth [specific quality criteria]. Failure on any of these thresholds means the niche hypothesis is falsified, not that I should send more outbound.**

This is the eval-harness mindset from Block 0 Week 3 applied to commercial discovery. You set success criteria *before* you run the test, you commit to the test duration, and you honor the result — you do not move the goalposts when replies don't come. The most common way first-year AI operators fool themselves is by quietly replacing failed niche tests with vaguer niche tests until some version "works" for ambiguous reasons. That is the p-hacking equivalent of commercial positioning.

BCG's 2025 *AI Value Gap* data is the operator evidence: 5% of companies generate measurable value from AI, 60% achieve no material value, and 35% scale without going far or fast enough — and the 5% are disproportionately those who ran tight, falsifiable AI-project hypotheses (defined metric, defined timeline, defined kill criteria) rather than exploratory programs.[^5] The same discipline applies to your niche hypothesis: tight-and-falsifiable versus exploratory-and-permissive is the difference between 5% of companies / 5% of operators realizing outcomes and the 95% who don't.

### What makes a hypothesis *well-formed* for niche discovery

Four properties:

- **Specific enough to reject.** The vertical names a bounded set of accounts you can list (a CSV). The capability names an offer artifact you can describe in three sentences. The seniority names a role title you can find on LinkedIn.
- **Observable outcome in a short window.** Reply rate, first-call rate, and qualified-discovery rate at day-14 and day-30 are your dependent variables. Not "pipeline over 12 months."
- **Pre-registered kill conditions.** What reply rate below which kills the hypothesis? For cold outbound on a tight vertical × capability × seniority cell, operator benchmarks from named practitioners converge around a floor of 2–4% first-reply rate at N≥30 touches; below that, your message-market fit is wrong or the niche is wrong.[^6] Specify your floor before you run.
- **Bound on cost.** You will spend *K* hours and *$M* (tools, data, research) on the test. If you exceed that, you kill regardless of early signals.

The three-axis model plus the hypothesis form gives you a compact planning object: one page describing the cell, the hypothesis, the test design, the success criteria, and the kill conditions. You commit to it. You run it. You read the result honestly.

## Layer 3 — The "everything store" failure mode for first-year AI operators

Bezos famously called Amazon an "everything store." The model works at scale because the demand aggregation, logistics, and data flywheel pay for the breadth. For a one-person AI consultancy, "everything store" is a death sentence, and it is the most common positioning in the market.

An everything-store AI freelancer looks like this: LinkedIn headline reads *"AI Consultant | Workflow Automation | Chatbots | RAG | Content | Agents | Voice | Computer Vision."* Portfolio shows a chatbot for a law firm, a content pipeline for a D2C brand, an internal-search tool for a construction company, and a voice demo for a dental office. Proposals are rebuilt from scratch every time. Deal sizes cluster between $2k and $12k. Reply rates on outbound sit at 1–2%. Referrals come in once a quarter and rarely match prior work. Second-year revenue looks like first-year revenue.

The failure mechanism has three parts.

**(1) No compounding artifact stack.** Every deal produces artifacts — a case study, an eval harness, a domain-specific prompt library, an integration scaffold — but each artifact sits in its own vertical and can't be reused. Artifacts from the dental voice-agent deal don't help land the construction-company search project. This is the opposite of a portfolio; it's thirty disconnected items. Specialists accumulate. Everything-stores reset.

**(2) No buyer-recognizable signal.** Jason Liu, who explicitly teaches "Indie AI Consulting: Positioning, Pricing, and Proposals" after scaling his own consulting from $170/hr to >$100k/month in about a year, is direct about this: *"capitalize on current AI expertise scarcity and identify your specialty."*[^7] When a VP of Engineering at a B2B SaaS company has a concrete problem — "our RAG system is answering wrong 30% of the time and we don't know why" — and they Google or ask a peer, the everything-store freelancer does not surface. Specialists do. Hamel Husain built Parlance Labs around AI evals specifically, published deep field guides on eval-driven development, and teaches an AI Evals course to 3,000+ students from 500+ companies including OpenAI, Anthropic, and Google.[^8] When evals come up, he is one of the first two or three names mentioned. That recognition is what non-everything-stores buy with their focus.

**(3) No pricing power.** Index.dev's 2025 rate data is explicit: generalists compete on price, specialists compete on expertise, and the specialist premium over generalist rates for AI work is 40–60%.[^4] Upwork's *In-Demand Skills 2026* report shows the same pattern at the platform level: specialized AI skills grew 109% YoY in demand, while undifferentiated "AI consulting" listings saw rate compression.[^3] An everything-store is structurally priced against a vast undifferentiated pool; a three-axis niche is priced against a narrow, usually short pool of credible alternatives.

The counter-argument — "but I'm early in my career and I need to take everything that comes in to figure out what I want to do" — is partly right, and we'll treat it honestly. The honest framing is: **exploration is a time-boxed phase, not a positioning.** For 90–180 days you can legitimately take a range of work to run experiments across cells. After that, the evidence you've collected has to converge into a hypothesis. If it doesn't, you are not exploring — you are drifting, and drift is the failure mode in disguise.

The operator move during exploration: **take the deal, then tag the data.** Every project you accept during the exploration window, log against the three axes (which vertical, which capability, which seniority), outcome (revenue, NPS, referral produced), and effort (hours, margin). At month 4 or 6 you look at the table and ask where energy compounded versus where it leaked. That cell is your hypothesis.

## Layer 4 — Controversy: Dunford ("what you do") vs Kahl ("who you serve")

Here is the live disagreement worth staking a position on. Both sides hold the position seriously; the resolution depends on context, and being clear about the context is the thing an operator must do.

**Position A — April Dunford: positioning is about the market category your value becomes obvious in.** Dunford's *Obviously Awesome* (2019) and her 2024–2026 Lenny's Podcast appearances argue that the single most load-bearing positioning decision is choosing the *market category* the buyer places you in when they evaluate alternatives.[^9][^10] On her March 2026 Lenny's episode, she extends this explicitly to AI-native products: the capability has become trivial (AI can be built in a weekend), distribution has become the hard part, and the market-category choice — *what* you are — is the distribution lever.[^10] In Dunford's frame, "who you serve" is a downstream clarification once the category is set. If you call yourself a "RAG consultant," the buyer compares you to other RAG consultants; if you call yourself a "legal document AI specialist," the buyer compares you to other legal-vertical AI firms. The competitive reference set — the alternatives you're evaluated against — is set by the category label, and the category label is *what you do* expressed in the buyer's language.

**Position B — Arvid Kahl: the niche is the audience, and the offer follows.** Kahl's *Embedded Entrepreneur* and his ongoing Bootstrapped Founder writing argue the opposite entry point: find a niche audience first — a tribe with shared interests, shared language, shared problems — embed in it until you see their actual pain, *then* build.[^11] His canonical frame is the intersection of expertise × social circles × pain points: if you're a coder who loves gardening, look at what professional landscapers hate doing on their computers. Kahl's FeedbackPanda case ($0 to $55K MRR in two years, seven-figure exit, no employees) was built for an ultra-specific audience — freelance English teachers who teach Chinese students and must write mandatory student feedback to get paid — before the product scope was locked.[^11][^12] In Kahl's frame, the category label is an artifact; the *audience* is the asset.

**Where they genuinely disagree.** Dunford starts with the competitive reference set the buyer uses in their head. Kahl starts with the audience the operator can embed in. Both agree on the end state (legible positioning + real customer love), and both agree the one-axis "AI consultant" label is garbage. They disagree on the *entry point* and therefore on what you commit to first.

**Where they actually resolve.** The three-axis model is the resolution device. Dunford's "market category" is most load-bearing when your *capability* axis is the differentiator — you are selling into a category of alternatives the buyer will benchmark you against (RAG consultants, eval specialists, voice-agent deployers). Kahl's "embedded audience" is most load-bearing when your *vertical* axis is the differentiator — you are selling to a tribe whose cross-capability needs you can serve because you speak their language and know their operational details. Buyer-seniority is the mediator: operator-level buyers value *audience embeddedness* (they want to work with someone who gets their world); VP/CXO buyers value *category legibility* (they want to defend the purchase to peers and procurement).

So the operator question is not "Dunford or Kahl." It is: **for your specific three-axis cell, which axis is your first-order differentiator, and which framework rides shotgun on it?** If capability is your tight axis (Hamel on evals, Jason Liu on RAG), you're in Dunford-land for positioning and you use Kahl to find the specific first twenty accounts to land. If vertical is your tight axis (the credit-union AI specialist, the dental-DSO voice-agent specialist), you're in Kahl-land for audience and you use Dunford to name the category once you're ready to scale.

The resolution is useful but it is not universal. **Simon Willison is the named counter-operator who breaks the frame**: his axis structure is capability-tight (LLM tooling, prompt injection, Datasette), yet his distribution motion is Kahl-style audience embedding, not Dunford-style category legibility — he writes daily for a specific community of LLM practitioners, earns trust through 23 years of published work, and the buyers who pay him for consulting find him because they're already in that community, not because they placed him in a comparison shortlist. Simon's trajectory falsifies the clean "capability-tight → Dunford-land" half of the resolution. The honest reading: the resolution is directionally right for most operators and wrong for a specific sub-type (long-archive, audience-embedded, capability-deep) where the two frameworks fuse rather than trading roles. If you think you might be in Simon's sub-type, stop trying to pick between Dunford and Kahl and start publishing on a 10-year horizon.

Both are right, deployed in the wrong order and you get the everything-store. Deployed in the right order and you get the operators the next section studies — with the Simon exception as the honest boundary condition.

## Named-operator niche trajectories (war stories with numbers)

### Jason Liu — capability-first, audience-second, ~12-month revenue 10×

Jason Liu built the Instructor Python library for structured LLM outputs and established deep credibility in RAG and applied LLMs through his blog, talks (World's Fair 2024), and the *Systematically Improving RAG* Maven cohort (400+ engineers through the program).[^13][^7] Over roughly 12 months he scaled his consulting from ~$170/hr (a rate he has publicly stated on jxnl.co was underpriced — the client accepted so quickly that it told him what the ceiling really was) to a $15,000/month engagement minimum and a reported $50,000–$120,000/month range through expert calls and retainers, verified against his own writing on jxnl.co.[^7] His explicit playbook is shift-to-value-based pricing, build teachable artifacts (blog, course, library), and specialize hard on the capability.[^7] Axis map: *capability = very tight (RAG + Instructor library); vertical = loose (any company with a RAG problem, bias toward Sequoia/YC/OpenAI-backed startups); seniority = tight (VPs of Engineering and applied-AI leads who own a production RAG system).* His wins come from Dunford-style category legibility ("the RAG eval guy") executed on a Kahl-style embedded audience (the applied-LLM practitioners who read his blog and attend his cohorts). Price delta over an undifferentiated "AI consultant": ~10× on an hourly basis, more on deal structure.

### Hamel Husain — capability axis anchored by published depth

Hamel runs Parlance Labs with a tight positioning around AI evals and LLM-product debugging. His *Field Guide to Rapidly Improving AI Products* and *LLM Evals: Everything You Need to Know* pieces are cited across the applied-LLM community.[^8] His Maven cohort on *AI Evals for Engineers and PMs* — co-taught with Shreya Shankar — has run with 3,000+ students from 500+ companies including OpenAI, Anthropic, and Google.[^8] Axis map: *capability = extremely tight (evals and data-driven LLM product improvement); vertical = loose-by-design (horizontal across any company shipping LLM products, with weight toward well-funded AI-native teams); seniority = tight (engineering and product leads who own production LLM systems).* Hamel's trajectory illustrates Dunford's point in extremis: when your category label is sharp enough and your published depth is real, the category itself becomes the distribution — peers surface you by default.

### Arvid Kahl — vertical-first micro-SaaS, then operator platform

Kahl's FeedbackPanda (pre-AI era but canonical) served a single ultra-specific vertical — freelance English teachers teaching Chinese students who had to write mandatory student feedback for payment. $0 to $55K MRR in two years, seven-figure exit.[^11][^12] He did not start from "the category of teacher-productivity tools"; he started from an audience (his partner was in it). Post-exit, his Bootstrapped Founder brand has become the *operator* platform — audience of founders who operate the same way — and Podscan.fm continues the pattern of a tight vertical cell (podcast-data infrastructure for ops-type founders). Axis map (FeedbackPanda): *vertical = ultra-tight (one teacher-platform's freelancer base); capability = emergent (a browser extension that collapsed a multi-step feedback-writing workflow); seniority = flat (the teacher was both buyer and user).* Kahl's trajectory illustrates his own framework: audience first, capability second, category label never really needed because the audience knew exactly what the product did.

### The 11x.ai / AI-SDR cautionary tale — category creation without niche tightening

11x.ai raised $74M from top-tier VCs pitching an "AI SDR" — an AI agent that replaces sales development reps. Reporting through late 2025 (Pavilion, Broadn, TechCrunch coverage) documented customer churn of 70–80% within months of contract start, allegedly fabricated or heavily massaged customer claims (including ZoomInfo and Airtable named as customers despite, per reporting, only short failed trials), and ZoomInfo threatening legal action.[^14][^15] Broadn's post-mortem frames the structural issue precisely: the AI-SDR category collapsed a range of genuinely different buyer cells — a Series-B SaaS VP of Sales with a 5-person SDR team, a seed-stage founder running outbound solo, a mid-market CRO with procurement scrutiny — into one offer. The category label ("AI SDR") was Dunford-sharp. The niche was one-axis. Customers in different cells wanted radically different behaviors from the same product and churned when they didn't get them.[^14] Clay's public positioning explicitly carves the opposite path: it sells into specific seniority cells within specific go-to-market maturities, with heavy playbooks and community for each.[^15] The lesson for an AI operator: **a sharp category label without three-axis tightening is a churn engine dressed as a moat.**

Pattern across the four: the operators who compound revenue on a 12–24 month arc tightened two axes deliberately and were clear about which was their "primary" and which was their "secondary." Those who tightened one axis and papered the other two with a cool label ran high-variance outcomes that, in the 11x case, included public fraud allegations and category damage.

## Runnable experiment — run your three-axis cell through Claude Code in 90 minutes

You are going to produce three artifacts: a 30-cell niche scoring table, five concrete niche hypotheses with success criteria, and one committed 30-day test plan.

**Phase 1 — Generate and score the 30 cells.**

Open Claude Code. Paste this prompt, adapting the bracketed pieces to your own inputs:

> "You are helping me do niche discovery as an AI operator. I am going to run a three-axis model: **vertical × capability × buyer-seniority**.
>
> Inputs:
> - My capability strengths (things I can credibly deliver a six-figure outcome on): [list 3–5].
> - Verticals I have some existing credibility in (domain knowledge, prior projects, strong contacts, or a spouse/friend deeply embedded): [list 5–10].
> - Buyer-seniority levels I can plausibly reach: [list which of operator / director / VP / CXO you can realistically get meetings with today].
>
> Task: generate 30 specific niches at the intersection of 10 verticals × 10 AI capabilities × 3 buyer-seniority levels (you can re-use capability and vertical entries to cover the 3 seniority levels cleanly). For each cell, return a row in a Markdown table with columns:
>
> 1. Vertical (specific: 'U.S. credit unions $500M–$2B AUM', not 'financial services')
> 2. Capability (specific: 'RAG-over-contracts with eval harness', not 'RAG')
> 3. Buyer seniority (Operator / Director / VP or CXO) with specific role title
> 4. Score — buyer urgency today (1–5, with one-line justification citing a recent signal: funding, regulatory, layoff, hiring)
> 5. Score — my credibility starting state (1–5, honest)
> 6. Score — competition density (1–5, where 1 = uncrowded and 5 = everyone is here)
> 7. Score — contract-size ceiling (1–5, where 5 = $100k+ first deal plausible)
> 8. Score — compounding-upsell potential (1–5, where 5 = a tight cell that naturally expands to adjacent capabilities)
> 9. Total (sum)
> 10. One-line rationale
>
> After the table, give me the top 5 cells by total score with a 2–3 sentence explanation of why each made the cut."

Read the output. Push back on any row that feels generic; ask Claude to make it more specific. Iterate twice.

**Phase 2 — Write five falsifiable hypotheses.**

For each of the top 5 cells, write (in Claude.ai or by hand) a hypothesis in this exact form:

> *"If my niche is [vertical] × [capability] × [seniority], then [N] well-crafted outbound touches in [time window] will produce [≥M first replies], [≥K qualified discovery calls], and [≥J signed pilot] at conversation depth [specific criteria: e.g., 'buyer articulates the underserved outcome in their own words, with a current cost number']. I will spend at most [K] hours and [$X] on this test. Kill conditions: reply rate < [R%] at day 14 with N≥30 touches; or zero qualified discovery calls by day 21; or buyer-urgency score drops below [X] in early conversations."*

If you cannot fill the blanks with specific numbers, the cell is not ready to test — it's still aspirational. Go back and sharpen.

**Phase 3 — Commit to one.**

Pick the single hypothesis you will run in the next 30 days. Put it in your calendar. Tell one person who will ask you on day 30 whether you ran it and what happened. The commitment device is not optional — the failure mode of this whole exercise is running the analysis and never running the test.

**Phase 4 (optional, same session) — Stress-test with Claude as adversary.**

Paste your chosen hypothesis back into Claude Code with: *"Play the role of a skeptical senior consultant who has done niche-testing fifty times. Where will this hypothesis break? What are the three most likely reasons the 30-day test will produce noise instead of signal? What's the single change to the hypothesis that would make the result most interpretable?"* Read the critique and adjust before day 1.

Expected cost: 90 minutes for Phases 1–3. The output — one committed, tight, falsifiable niche hypothesis — is worth more than a week of vague "market research."

## Problem set

Five problems. Each demands a written artifact or a defensible position, not a reflection.

**P1 — Place yourself on the three-axis model with evidence.** Write three sentences for each axis:
- On the vertical axis I am currently [tight / loose / exploring]; evidence: the last 10 outbound messages I sent had [N] distinct verticals.
- On the capability axis I am currently [tight / loose / exploring]; evidence: my LinkedIn headline lists [N] capabilities; a buyer reading it would expect me to deliver [specific capability].
- On the buyer-seniority axis I am currently [tight / loose / exploring]; evidence: my last 5 discovery calls were with roles [X, Y, Z, ...].

Submit this as a short written assessment to yourself. Calendar a review in 90 days to compare.

**P2 — Take a defensible position on niche-or-die in 2026 AI services.** Write 250–400 words answering: *is niche-or-die still true for AI operators in 2026, given that AI capabilities cross-pollinate across verticals faster than SaaS did?* Cite at least two named operators on each side. A defensible answer engages the honest counter-argument that AI-native operators can serve more verticals with less specialization cost per vertical. Your position can be "yes," "no," or "yes-on-axis-X-no-on-axis-Y" — all three are defensible; hand-wavy is not.

**P3 — Three falsifiable niche hypotheses.** Write three niche hypotheses in the Layer 2 form (vertical × capability × seniority, with N, M, K, J, kill conditions). At least one must be a niche you would genuinely hesitate to commit to because it feels "too small." For each, estimate the 12-month revenue ceiling and decide whether that's enough to matter to your life this year.

**P4 — Diagnose one "everything store" drift signal in your own positioning.** Audit your LinkedIn, website, portfolio, and last 10 pitches. Find *one* specific signal of everything-store drift — a capability listed that you don't actually want deals in, a vertical example in your portfolio that attracts the wrong inbound, a testimonial that positions you cross-vertically when you want vertical tightness. Commit to cutting it by date and record what you'll replace it with (often: nothing — the cut is the move).

**P5 — Reverse-engineer a named operator's three-axis niche.** Pick a named AI operator you admire (Hamel Husain, Jason Liu, April Dunford, Arvid Kahl, or someone in your own orbit). Read their last 20 LinkedIn / blog / podcast touchpoints. Write their three-axis placement and identify the axis that is tightest, the axis that is secondarily tight, and the axis that is deliberately loose. Compare to your own placement in P1. Where are you mimicking a tight axis without the corresponding published depth? Where are you tighter than the operator and haven't cashed in on it yet?

## Common failure modes at scale

Six mistakes that kill first-year AI operators on the niche axis, each with the tell-tale signal:

- **"I do AI for businesses."** The one-axis capability-only headline. Signal: reply rate under 1% on outbound, every discovery call opens with "so tell me exactly what you do." Fix: pick a vertical, commit for 90 days, watch what happens to reply rate.
- **Everything-store portfolio.** Seven case studies across seven verticals with no through-line. Signal: referrals don't match prior work; you keep getting asked whether you "also do" things you don't want to do. Fix: prune the portfolio to the three items that point in the same direction, hide the rest, and write a positioning sentence that only fits those three.
- **"Exploration" that never converges.** Six months of taking any deal that comes in, without a date or a decision criterion. Signal: you cannot describe your niche today without saying "I'm still figuring that out." Fix: set a hard date, tag your past deals against the three-axis model, pick the cell with the best leading indicators.
- **Capability-level positioning for vertical-level buyers.** You sell into a vertical (say, legal) but your positioning says "RAG consultant." Signal: Am Law 100 firms hire Harvey or Ironclad; they don't hire "RAG consultants." Fix: re-label in the vertical's language — "AI infrastructure for legal workflows" — even if your underlying capability is unchanged.
- **Buyer-seniority mismatch.** Your content, artifacts, and pricing are designed for an operator-level buyer, but you're trying to sell to VPs. Or inverse. Signal: deals take 6× as long as you expected, procurement kills velocity, and pilots die in "stakeholder alignment." Fix: match the seniority of your prospecting, artifacts, and pricing to the seniority you actually want; if you want VP deals, you need VP-grade artifacts (security docs, case studies with enterprise logos, proposals with procurement metadata).
- **Category-label theatre without niche substance.** The 11x.ai pattern at individual scale: you adopt a cool category label ("AI agent architect," "AI workflow engineer") and skip the three-axis tightening. Signal: the label attracts inbound, but no inbound converts because the label matches radically different buyer cells. Fix: sharper cells, less sexy label.

## Open questions — what is not settled

**(1) Does AI-native capability collapse the niche calculus?** Some operators argue that because AI capabilities are more cross-domain than past technology waves — a voice-agent pipeline works in dental, legal, and logistics with modest adaptation — the specialization tax per additional vertical is lower and the niche axis can be wider than it used to be. The counter-evidence: Menlo's 2025 data shows vertical AI vendors capturing 25–50% of an employee's work value versus 1–5% for horizontal platforms; Bessemer's 2025 report treats vertical AI as a distinct category; BCG's value-gap data shows scaled AI implementations disproportionately in tight-vertical deployments.[^1][^2][^5] My read: the cross-pollination is real at the capability layer, but the trust-stack and compliance layer remains vertical-bounded, and buyers pay for trust. I suspect this debate resolves in favor of tighter vertical niching for operators who want premium pricing, and looser vertical niching for operators who want volume at commodity rates — the market segments.

**(2) Is there a stable middle between operator-level and VP-level buyer?** The director / function-head tier is the messiest. Budgets are real, procurement is light, but selling cycles are longer than operator cycles and shorter than VP cycles — which means neither operator playbooks nor enterprise playbooks fully work. I'm not sure whether this tier is a sustainable niche or a transit zone, and I watch operators in 2026 to see who holds it over 24 months.

**(3) Will category creation by individual operators work in AI services, or is it a company-level-only move?** April Dunford implicitly argues categories are created by companies with the resources to invest in the category; Christopher Lochhead's *Play Bigger* treats category creation as a multi-company coordination game. Operators who try to create personal categories ("the X consultant") may be doing a lighter version of the same move — or may be doing a vanity exercise. Saturday's lesson makes the case that for individual operators, personal category creation is statistically a bad bet (fewer than 35 companies, across 15 years, genuinely created and dominated a category by Dunford's count), but that *sub-category creation* — carving a narrower slice inside an existing category where you are the obvious reference — is operator-scale and often correct; the Hamel-Husain-on-AI-evals case study in Saturday's teardown is the worked example. For now, be suspicious of any category label you invented yourself that the market hasn't echoed back to you in 6 months.

## Reviewer lens — named critics with specific disagreements

- **April Dunford (obviouslyawesome.com/blog; Lenny's Podcast episode March 2026[^10])** would push back on the Layer 4 framing that "who you serve" and "what you do" are a genuine dichotomy. Her position: the market category *is* the who-you-serve, because categories are defined by the set of buyers who use the same comparison shortlist. Splitting them into two competing frames, as this lesson does, misrepresents her view. She'd want the lesson to say: Dunford's category = Kahl's audience, described from the buyer's side of the table rather than the operator's. My concession: partially fair. The dichotomy is a teaching device; the strongest version of Dunford collapses the distinction. I keep the dichotomy because the *entry point* differs operationally even if the end-state overlaps.

- **Arvid Kahl (thebootstrappedfounder.com; *The Embedded Entrepreneur*[^11])** would push back on Layer 3's treatment of exploration. His view: the 90–180 day exploration window I endorse is too long for audience embedding, because real audience knowledge compounds only when you commit to the community and go deep. Two cells in a 180-day window produces surface knowledge of both and embedded knowledge of neither. He'd advocate committing to one audience for 12+ months and refusing adjacent work that would pull you out. My partial concession: his move is right for the Kahl path (vertical-first); on the Dunford path (capability-first), the exploration tax is lower because the capability carries across vertical experiments.

- **Hamel Husain (hamel.dev/blog[^8])** would push back on the use of his trajectory as a "capability axis tight, vertical axis loose" exemplar. His actual distribution is heavily weighted toward well-funded AI-native teams at Series-B-and-later SaaS companies — that's a de facto vertical ("applied-LLM teams at well-capitalized AI-adjacent software companies") even if it's not named as one. I should treat his implicit vertical as tight, not loose, and the lesson misses that nuance.

- **Jason Liu (jxnl.co; Maven *Indie AI Consulting*[^7])** would agree with the broad shape of Layer 3 but push back on treating the Jason Liu → Hamel Husain trajectory as a single pattern. His explicit teaching is that *value-based pricing* and *teachable artifact production* are the load-bearing moves, not the axis structure. He'd argue the three-axis model is necessary but not sufficient — plenty of operators with tight three-axis cells still price hourly and still don't productize their expertise, and those operators stall. The axes are the *where*; the pricing and artifacts are the *how*.

- **Christopher Lochhead (Play Bigger / *Niche Down*)** would push back on the whole Layer 4 framing as "deciding between Dunford and Kahl." In his view, the real move is *category design* — naming a new category neither side is currently defending — which neither Dunford (who treats category as chosen from existing reference sets) nor Kahl (who treats category as incidental to audience) emphasizes. Saturday's lesson engages this directly; the Thursday lesson under-weights category creation as an option for individual AI operators. My response: Saturday is the right place for that argument; Thursday is about the hypothesis-level discipline, which is prior to the category-design question.

## Further reading

**Must-read (≤5)**

- April Dunford, *Obviously Awesome* (2019) + her March 2026 Lenny's Podcast episode on AI-era positioning.[^9][^10]
- Arvid Kahl, *The Embedded Entrepreneur* (audience-first niche discovery method).[^11]
- Bessemer Venture Partners, *The State of AI 2025* — vertical AI share of private AI top-growers.[^1]
- Jason Liu, *Indie AI Consulting: Positioning, Pricing, and Proposals* (Maven cohort, materials summarized on jxnl.co).[^7]
- BCG, *AI Value Gap 2025* — the 5% / 60% / 35% split and what separates the 5%.[^5]

**Recommended**

- Menlo Ventures, *2025: The State of Generative AI in the Enterprise* + their healthcare-vertical deep-dive.[^2]
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (2025).[^8]
- Daniel Priestley, *Key Person of Influence* (revised edition) + *Oversubscribed* — the "own a micro-niche" framing.[^16]
- Rob Walling / MicroConf, *2025 State of TinySeed* episode on why vertical SaaS is outperforming horizontal.[^17]

**Optional**

- Pavilion, *The 11X Fraud vs. the AI SDR Future* (2025) — a sharp operator post-mortem on category-creation-without-niche-tightening.[^14]
- Broadn, *Why AI SDRs Were Doomed to Fail* (2025) — structural critique of the AI-SDR category.[^15]
- Upwork, *In-Demand Skills 2026* report (AI skill demand +109% YoY, capability-specific breakdown).[^3]

## Citations

[^1]: Bessemer Venture Partners, *The State of AI 2025*, bvp.com/atlas/the-state-of-ai-2025 — vertical AI applications make up ~40% of top-growing private AI companies; vertical AI treated as distinct asset class. https://www.bvp.com/atlas/the-state-of-ai-2025

[^2]: Menlo Ventures, *2025: The State of Generative AI in the Enterprise* and *2025: The State of AI in Healthcare*, menlovc.com — vertical AI spending $3.5B in 2025 (~6× 2024), ~65% gross margins, healthcare as largest vertical AI segment (8 unicorns), vertical AI captures 25–50% of an employee's work value vs 1–5% for horizontal platforms. https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/ ; https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/

[^3]: Upwork Inc., *In-Demand Skills 2026: Demand for Top AI Skills More Than Doubles*, investors.upwork.com news release and Upwork Research Institute brief, Feb 2026 — AI skill demand +109% YoY; AI video generation +329%; AI integration +178%; AI data annotation +154%; AI chatbot development +71%; 18M registered freelancers; AI GSV +25% YoY in Q1 2025. https://investors.upwork.com/news-releases/news-release-details/upworks-demand-skills-2026-demand-top-ai-skills-more-doubles-ai ; https://www.upwork.com/research/in-demand-skills-2025

[^4]: index.dev, *Freelance Developer Rates 2025* — AI/ML specialists $100–$200/hr vs generalist software engineers $60–$120/hr (40–60% specialist premium); LLM specialists $150–$250/hr; computer vision $120–$200/hr; MLOps $100–$180/hr; gap widened in 2025. https://www.index.dev/blog/freelance-developer-rates-by-country

[^5]: BCG, *Are You Generating Value from AI? The Widening Gap* and *From Potential to Profit: Closing the AI Impact Gap* (2025) — 5% of companies generate measurable value from AI, 60% no material value, 35% scale without going far or fast; 10/20/70 investment allocation across algorithms / tech-and-data / people-and-processes. https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap ; https://www.bcg.com/publications/2025/closing-the-ai-impact-gap

[^6]: Operator benchmarks for cold-outbound first-reply rates on tight niche cells are community-sourced (Pavilion, MicroConf founder threads, Justin Welsh public disclosures) rather than a single published paper; 2–4% floor at N≥30 represents a rough convergence across disclosed 2024–2025 operator data. Treat as heuristic, not benchmark.

[^7]: Jason Liu, *Indie AI Consulting: Positioning, Pricing, and Proposals* (Maven cohort) and jxnl.co blog — scaled from ~$170/hr to >$100k/month in ~12 months, five-figure solo deals, waitlist, course with 4.6 stars / 62 reviews at $750 USD. https://maven.com/indie-consulting/ai-consultant-accelerator ; https://jxnl.co/

[^8]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (March 2025) and *AI Evals for Engineers & Product Managers* Maven cohort (with Shreya Shankar) — 3,000+ students from 500+ companies including OpenAI, Anthropic, Google. https://hamel.dev/blog/posts/field-guide/ ; https://maven.com/parlance-labs/evals ; https://hamel.dev/

[^9]: April Dunford, *Obviously Awesome: How to Nail Product Positioning so Customers Get It, Buy It, Love It* (Ambient Press, 2019) — five-component positioning structure: competitive alternatives, unique attributes, value, best-fit customers, market category.

[^10]: April Dunford on Lenny's Podcast, *A Guide to Advanced B2B Positioning* (March 10, 2026) — AI-era distribution challenge and the market-category choice as the distribution lever. https://www.lennysnewsletter.com/p/a-guide-to-advanced-b2b-positioning ; April Dunford Substack, *Special Lenny's Podcast Drop and How to Manage A Big Positioning Change*. https://aprildunford.substack.com/p/special-lennys-podcast-drop-and-how

[^11]: Arvid Kahl, *The Embedded Entrepreneur: How to Build an Audience-Driven Business* (2021) and *Finding an Audience for Your Side Business*, thebootstrappedfounder.com — intersection of expertise × social circles × pain points; embed-then-build methodology. https://thebootstrappedfounder.com/finding-an-audience-for-your-side-business/

[^12]: Zack Liu, *The FeedbackPanda Blueprint: 9 Lessons on How Arvid Kahl Built and Sold a 2-Person Empire*, Medium (Feb 2026) — FeedbackPanda $0→$55K MRR in 2 years, seven-figure SaaS exit, no employees; built for freelance online English teachers serving Chinese students. https://medium.com/@zack_liu/the-feedbackpanda-blueprint-9-lessons-on-how-arvid-kahl-built-and-sold-a-2-person-empire-a9a049c1c296

[^13]: Jason Liu, *Systematically Improving RAG Applications* (Maven cohort), 400+ engineers through program; Instructor library creator. https://maven.com/applied-llms/rag-playbook ; https://jxnl.co/systematically-improve-your-rag/

[^14]: Pavilion, *The 11X Fraud vs. The AI SDR Future* (2025) — 11x reported 70–80% customer churn within months; allegations of fabricated customer claims (ZoomInfo, Airtable) and massaged internal numbers; ZoomInfo threatened legal action despite 11x having raised $74M. https://www.joinpavilion.com/blog/the-11x-fraud-vs.-the-ai-sdr-future

[^15]: Broadn, *Why AI SDRs Were Doomed to Fail — and What Comes Next* (2025) — structural critique: category collapsed heterogeneous buyer cells; Clay's contrasting vertical-and-seniority-specific playbooks. https://www.broadn.io/blogs/ai-sdrs-doomed-to-fail

[^16]: Daniel Priestley, *Key Person of Influence (Revised Edition)* (Rethink Press, updated 2024) and *Oversubscribed* — "owning a micro-niche is as valuable as owning land"; supply-and-demand imbalance as the positioning move. https://www.amazon.com/Key-Person-Influence-Revised-Five-Step/dp/178133109X

[^17]: Rob Walling / MicroConf, *Startups For the Rest of Us* Episode 812 *The 2025 State of TinySeed* and Episode 813 *SaaS Predictions for 2026* — vertical SaaS outperforming horizontal; 192-startup dataset on 7 SaaS growth plateaus. https://www.startupsfortherestofus.com/episodes/episode-812-the-2025-state-of-tinyseed ; https://www.startupsfortherestofus.com/episodes/episode-813-saas-predictions-for-2026-reflections-on-2025

_last_verified: 2026-04-16_
