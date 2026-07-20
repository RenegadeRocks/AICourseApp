---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 4
day_name: thu
session_slug: market-user-validation-interview-or-poll-potential-users
date_due: 2026-07-30
tags: [synthetic-users, llm-simulation, generative-agents, replication-evidence, sycophancy, distribution-collapse, causal-inference, simulate-to-design, research-ethics, ai-moderated-interviews]
sources:
  - park-generative-agents-1000
  - gui-toubia-causal-inference
  - illusion-of-intervention-2026
  - lost-in-simulation-2026
  - kapania-simulacrum-of-stories
  - nng-synthetic-users
  - syntheticusers-company
  - measuringu-synthetic-experiments
  - prelude-writing-style-replication
  - acm-energy-simulated-users-2026
  - creative-homogeneity-llms
  - stanford-hai-simulating-behavior
last_verified: 2026-07-17
word_count_target: 5800
---

# Synthetic users and simulation — promise, peril, and a protocol you can defend

## Why this matters

Somewhere this week, probably around your third unanswered recruiting message, a thought will arrive with the force of an epiphany: *why am I chasing humans when a frontier model can simulate ten of them in ninety seconds?* An entire product category agrees with you. Synthetic-user platforms sell "user research at the speed of AI," claim 85–92% parity with human studies, and cite real Stanford research in their marketing.[^1][^2] Meanwhile, the 2025–26 replication literature has been delivering a countervailing verdict with unusual consistency: LLM-simulated users are systematically more agreeable than humans, replicate only about half of experimental treatment effects, inflate success rates, and collapse the diversity of opinion that makes research informative.[^3][^4][^5] Both bodies of evidence are real. Both are cited by people with incentives. You are going to build products *with* these models and decide *about* those products using research; you need to know precisely where simulation earns its keep and where it manufactures confident fiction. This is the week's centerpiece controversy, and the outcome is a one-sentence protocol you can defend to an investor, a client, or yourself: **simulate to design studies; use humans to decide.**

## Prerequisites

- Wednesday's interview discipline and at least one real transcript. Today's comparisons need a human baseline.
- [[02-tue-ai-assisted-desk-validation|Tuesday]] — the sycophancy and homogenization failure modes; today shows both operating at their most seductive.
- [[06-sat-rag-evaluation|Block 2 Week 4 Sat]] — judge-model thinking. The "can a model stand in for a human?" question is one you have already met as "can a model grade a model?", and the answer has the same shape: yes, within validated bounds, audited.

## Layer 1 — The territory: what "synthetic users" actually means in 2026

Three distinct things travel under one label; conflating them is the source of half the discourse's confusion.

1. **Synthetic respondents.** An LLM prompted to *be* the research subject: personas answering interview questions or surveys. This is what Synthetic Users (the company) sells per-interview, what NN/g tested, and what most of the replication literature evaluates.[^1][^6] All of today's peril concentrates here.
2. **AI-moderated research on real humans.** An AI *interviewer* conducting or probing conversations with actual people (Koji, Perspective AI's conversational surveys, AI-moderated follow-ups). The respondent is human; the machine runs the protocol. Different epistemics entirely: the evidence is real, and the interesting questions are about moderation quality and consent disclosure.
3. **Agent-based simulation for system testing.** Simulated users exercising a *system* (your agent, your checkout flow) to find defects, in the lineage of Park et al.'s generative-agent work and standard practice in agent evals.[^2][^5] Here the simulated entity is a test harness, and its output is "the system broke," which a human need not have witnessed to be true.

Keep the taxonomy loaded. The defensible protocol will treat the three completely differently, and vendors blur them deliberately: parity statistics earned in narrow attitudinal replications get marketed as if they covered discovery research generally.

## Layer 2 — The strongest case FOR simulation (steelman first)

The pro-simulation case rests on real research, and the strongest single piece is Joon Sung Park and colleagues' *Generative Agent Simulations of 1,000 People* (Stanford/DeepMind, arXiv 2411.10109): build an agent per person from a two-hour qualitative interview with that specific person, then test whether the agent answers as they do. Result: agents replicated their humans' General Social Survey responses at 85% of the humans' *own* test-retest consistency two weeks later, performed comparably on Big Five prediction, and reduced accuracy gaps across racial and ideological groups relative to demographic-prompted personas.[^2][^7] Two honest readings coexist. The enthusiast's: individual-level human simulation is empirically real, today. The methodologist's, which matters more for you: the result required *two hours of real interview per simulated person*; the paper is a monument to how much human grounding it takes before simulation tracks an individual, and demographic-prompt personas (what commercial tools mostly ship) were precisely the condition it outperformed.

Beyond Park, the defensible pro-use cases have a common structure: the simulation's output is *checked by something other than the simulation*.

- **Piloting instruments.** Run your interview guide against simulated respondents to find confusing questions, leading phrasing, ordering effects, and dead ends before spending a real prospect on a broken guide. If the pilot finds a flaw, the flaw is real regardless of whether the simulated "respondent" resembles anyone. Wednesday's adversarial mock was exactly this.
- **Message and copy pre-screening.** Generate rival value-prop framings, have simulated segment members react, and use the *spread* to rank which 2–3 variants earn a slot in Friday's real smoke test. The smoke test, not the simulation, decides.
- **Segment and hypothesis brainstorming.** Simulated panels are excellent at proposing segments, objections, and edge cases you had not considered, i.e., at expanding the hypothesis space cheaply. Hypotheses are free to generate and expensive to believe; simulation only touches the free half.
- **System-defect surfacing.** The "Lost in Simulation" authors, despite their negative headline results, propose exactly this rehabilitation: simulated users as diagnostics that reliably surface defects any user would hit, analogous to automated software testing.[^5]
- **Rehearsal.** Practicing your own interviewing and selling against a simulated hostile customer, as Wednesday assigned. The training target is you, not knowledge about the market.

The vendor articulation of the pro case is worth reading in the original: Synthetic Users (Hugo Alves, co-founder) publishes "science posts" mapping its multi-agent, OCEAN-profiled architecture onto the academic literature, and reports parity between 85% and 92% with matched human studies depending on audience type.[^1] Treat those numbers as vendor-reported, methodology largely in-house, and note the pattern from Layer 1: parity on *thematic overlap with attitudinal research* is the claim; "replace your discovery interviews" is the marketing inference.

## Layer 3 — The case AGAINST: what the 2025–26 replication evidence actually says

Now the ledger's other column, and it is long. Five findings, each from a different research group, each attacking a different joint of the simulation thesis.

**1. Treatment effects don't replicate: Gui & Toubia.** George Gui and Olivier Toubia (Columbia) put the causal-inference frame on the problem: when you vary something in a prompt (price, feature, framing), you do not cleanly manipulate one variable in the simulated subject's world; you shift the model's inference about *everything else* correlated with it in training data, violating the unconfoundedness that experiments exist to secure. Across 11 canonical behavioral-economics experiments, LLM simulations achieved high individual-level predictive accuracy yet replicated only about half of the aggregate treatment effects.[^3] For validation, treatment effects are the whole game: "would demand change if I priced at $200 vs $99?" *is* a treatment-effect question. A tool that gets these right half the time, with no flag telling you which half, is a coin with better prose.

**2. Your simulated experiment is an observational study: "The Illusion of Intervention."** A 2026 follow-on formalizes the same critique: prompting an LLM persona with an "intervention" produces something epistemically equivalent to observing correlated text, not running an experiment, and the paper shows how the resulting "user drift" (the implicit simulated population shifting across treatment conditions) can inflate or attenuate estimated effects unpredictably.[^4] The title is the lesson.

**3. Simulated users are too nice, and miscalibrated: "Lost in Simulation."** The 2026 agentic-evaluation study closest to your daily work: LLM-simulated users evaluating conversational agents were systematically more cooperative than humans, inflated task-success rates, failed to reproduce demographic-specific interaction patterns, varied by up to 9 percentage points depending on which LLM played the user, and were miscalibrated in a structured way (underestimating agents on hard tasks, overestimating on moderate ones).[^5] Sycophancy is not an occasional bug; it is the persistent direction of error, and it points exactly where your motivated reasoning wants to go.

**4. The qualitative critique: "Simulacrum of Stories."** Shivani Kapania and colleagues' CHI paper interviewed qualitative researchers using LLM-generated "participants" and documented the epistemic losses: consent becomes meaningless, the researcher-participant relationship (where surprise and correction come from) disappears, and the outputs flatten lived particulars into plausible composites; the authors argue such data ultimately "epistemically harms" the communities research is meant to represent.[^6] NN/g's practitioner replication (Maria Rosala & Kate Moran) landed on the same texture from the industry side: they re-ran three of their own human studies against a leading synthetic-user tool and found the synthetic responses shallow, one-dimensional, and sycophantic, useful marginally for broad attitudinal shape, and "user research needs real users" as the closing verdict.[^8]

**5. Distribution collapse.** The homogenization results from Tuesday apply with full force to simulated *populations*: LLM outputs cluster around modal, socially-smooth positions, across models, so a synthetic "panel of ten" is closer to one median respondent with ten phrasings than ten draws from a real distribution.[^9] Real validation lives in the tails: the one buyer in ten with hair-on-fire urgency is your beachhead, and the crank with the furious objection is your churn model. Simulation systematically sands both away. Domain replications keep finding the same limits in situ; a 2026 ACM study of simulated users for conversational energy-management systems concluded they could mimic surface interaction patterns while diverging on the behavioral variables that mattered, and MeasuringU's running review of synthetic-respondent experiments lands on "sometimes matches direction, unreliable on magnitude, worst where you need it most."[^10][^11]

Aggregate the five and a shape emerges. Simulation fails precisely at the three properties your evidence ledger prices highest: *costliness* (a synthetic yes costs the yes-sayer nothing, and Wednesday taught you zero-cost yeses score zero), *causality* (treatment effects are coin flips), and *variance* (the tails are gone). What survives is everything upstream of belief: generation, rehearsal, instrument testing, defect surfacing.

## Layer 4 — Why it fails: mechanism, so the boundary generalizes

Four mechanisms, so you can predict failure cases the literature has not tested yet:

1. **Sycophancy is trained in.** RLHF-style post-training optimizes for being helpful and agreeable to the person prompting. You are the person prompting. The simulated customer's accommodating drift is the assistant's core disposition bleeding through the persona mask, and it survives "be brutally honest" instructions in exactly the way a personality survives a costume.
2. **Personas are priors, not people.** A demographic prompt ("38-year-old ops manager at a logistics firm") retrieves the training distribution's *median text about* such people, plus stereotype. Park et al. shows what it takes to beat this, two hours of individual interview grounding, which is why their result is simultaneously the best pro-simulation evidence and the best argument that cheap personas are hollow.[^2]
3. **No stakes, no information.** Real answers are shaped by consequence: time, money, reputation, embarrassment. A simulated respondent faces none, so questions whose informativeness *comes from* cost (everything in Wednesday's currency framework) return noise with confident grammar.
4. **Staleness and coverage gaps.** Models carry their training snapshot of who says what; your niche's 2026 mood, your local market's quirks, and any population thinly represented in training text are flattened or absent, the same recency-and-coverage failure as Tuesday's desk research, now wearing a human face.

## Layer 5 — The protocol: simulate to DESIGN, humans to DECIDE

The rule, operationalized as a boundary you can audit:

**Simulation is permitted upstream of evidence.** Guide piloting, question de-biasing, copy variant generation and pre-ranking, segment/objection brainstorming, interviewer rehearsal, survey red-teaming, agent-system defect testing. In every permitted use, one property holds: *the output is a design choice or a hypothesis that a downstream human-grounded instrument will check.*

**Simulation is forbidden as evidence.** No synthetic atom enters the evidence ledger's FOR or AGAINST columns on desirability or viability. Saturday's ledger tool enforces this mechanically: evidence of class `synthetic` carries weight zero in decision scoring, exists in the record only as provenance for a hypothesis, and cannot satisfy any kill-criterion threshold in either direction. (Feasibility is the one partial exception: simulated *load* on your own system is a legitimate feasibility instrument, per Layer 1's third category, because there the thing being measured is your system, not a human. In the ledger, log those runs as `behavioral` evidence about your system — the `synthetic` class, and its weight of zero, is reserved for simulated *humans*.)

**Disclosure is mandatory.** If synthetic research output ever appears in anything a client, investor, or cohort sees, it is labeled as simulated. The Kapania paper's ethics concerns are not abstract; "we validated with users" meaning "we prompted GPT" is a misrepresentation that will, eventually, be discovered.[^6]

**And the AI-moderated middle path is usually the better trade.** If what tempts you about synthetic users is scale and scheduling, category 2 from Layer 1 gives you most of it without the epistemic hole: AI-moderated interviews of *real* humans scale the interviewer, not the truth source. The Mom Test's author has himself leaned into this hybrid; AI moderation is arguably *better* than founders at not pitching, since it has no ego in the idea, though it still needs your consent standards from Wednesday.[^12]

## Worked example — the meeting-follow-up agent meets a synthetic panel

Continuing the running example. On Tuesday night, before any real interview, you run a synthetic panel: five personas (boutique-consultancy principals, varied by firm size and tech appetite) through your interview guide in Claude. The panel: loves the drafting feature ("huge time-saver"), estimates willingness to pay of $150–400/month, raises data-security as the top objection, and never once mentions CRM field rot.

Wednesday's real interview (P3, from yesterday's worked example) then produces: drafting explicitly *not* the pain ("I like writing the client emails myself"), CRM fields and task handoffs named as the actual rot, a dead Zapier workaround as a demand receipt, and a shrug on price.

Score the panel honestly. It was *right* to make you rehearse the security objection (P3 raised a version of it too) and its guide-pilot pass caught a leading question in Movement 4. It was *wrong*, in the direction the literature predicts, about enthusiasm (uniform where humans were split), about willingness to pay (invented numbers with no cost behind them), and, most dangerously, it was *silent* about the actual wedge-breaking insight, because "the drafting is the fun part, the plumbing is the pain" is a tail-of-distribution particular that no median-text persona surfaces. One real conversation falsified the panel's most decision-relevant output. That asymmetry, not any benchmark, is the lesson.

## Runnable experiment — the divergence audit (60–90 min)

Requires: your interview guide, one real interview transcript (Wednesday's P1), Claude.

**Step 1 (20 min).** Build a 5-persona synthetic panel matched to your customer definition. For each persona, run your full five-movement guide in a fresh conversation (fresh context per persona; shared context homogenizes further). Log answers.

**Step 2 (10 min).** Atomize the synthetic outputs with Wednesday's schema, but tag every atom `class: synthetic`.

**Step 3 (20 min).** Divergence audit against your real transcript(s), four rows: (a) claims the panel made that the human contradicted; (b) claims the panel made that the human never raised (unverified inventions); (c) things the human said that no persona produced (the tails you would have lost); (d) places the panel and human agree (candidate hypotheses, still requiring more human confirmation).
**Step 4 (15 min).** Extract the design value: 2–3 guide improvements, 1–2 new objections to probe, copy phrasings for Friday. Then write the boundary memo, five sentences max: which synthetic claims you explicitly refuse to believe without human evidence.

**Step 5 (5 min).** Commit `validation/03-synthetic-audit.md`.

**Pass bar:** (a) rows (a)–(c) each non-empty, or if any is empty, a written note explaining why you believe your idea is the special case where simulation nailed reality (you will delete this note with embarrassment later, which is itself instructive); (b) boundary memo lists ≥3 refused claims; (c) zero `synthetic` atoms tagged FOR/AGAINST on desirability or viability in your ledger.

## Common mistakes experts see

1. **Substitution creep.** Simulation enters as a guide pilot and, three days later, its "willingness to pay" numbers are in your pricing slide. The ledger's zero-weight rule exists because creep is the default, not the exception.
2. **Believing the agreement.** When panel and humans agree, founders log it as double confirmation. It is single confirmation plus an echo; the panel's agreement adds no weight, per the protocol.
3. **Demographic-prompt personas mistaken for Park-style agents.** The 85% headline came from two-hour individual interviews per agent; your three-line persona inherits none of it.[^2]
4. **One shared chat for the whole panel.** Context bleed makes five personas into one persona with wardrobe changes. Fresh context per respondent, always.
5. **"Be brutally honest" as a fix.** You cannot instruction-tune away post-training dispositions; you get theatrical harshness with the same underlying agreeableness.
6. **Using simulation where its errors are worst.** Price sensitivity, feature trade-offs, adoption prediction: all treatment-effect questions, the documented ~50% zone.[^3]
7. **Undisclosed synthetic "research" in client or investor material.** Career-grade integrity risk, and increasingly checkable.[^6]

## Open questions — what's not settled

**1. Do interview-grounded digital twins change the verdict?** Park et al. is a proof that individual-level fidelity is buyable at two hours of interview per person, and the obvious commercial extrapolation is a panel product built on real interview corpora rather than demographic prompts: your ten Wednesday transcripts, resurrected as a standing panel you can re-question all year.[^2] Whether the fidelity survives *new* questions (rather than held-out items from the same instrument), whether it decays as the person's situation changes, and whether the treatment-effect problem persists even with grounding are all empirically open; Gui & Toubia's confounding argument is about the simulation *mechanism*, not the persona quality, which suggests grounding alone does not fix causal questions.[^3] Watch this space with your acceptance criteria written down first (reflection question 6).

**2. Is the zero-weight rule too blunt?** A principled alternative exists: weight synthetic evidence by measured, question-class-specific validity (some attitudinal directions replicate reliably; some domains have local validation data), a dose-response schedule instead of prohibition. The counter-case, and the reason this course keeps zero: the weighting metadata would be maintained by the same motivated founder the rule protects against, and a tunable dial under motivated reasoning converges on whatever value admits the desired evidence. Institutions with independent methodologists can responsibly run graded weights; a solo founder probably cannot. Where the boundary of "probably" sits is unsettled.

**3. Who consents to being simulated?** The ethics frontier Kapania et al. opened is widening: synthetic panels claiming to represent specific communities (patients, minority professionals, your own customers) make representational claims no member of those communities agreed to, and Park-style twins built from real interviews raise a sharper version, since the source humans exist and are identifiable.[^6] Norms, disclosure standards, and possibly law (the EU AI Act's transparency provisions are the nearest live instrument) are all in motion. If your validation practice ever grows into a research offering for clients, this is the compliance question to have answered before a procurement team asks it.

## Reflection questions

1. Your divergence audit's row (c) contains things no persona produced. What structural property of your customer's situation made those invisible to a median-text simulation? What else shares that property?
2. Park et al. needed two hours of human interview per faithful agent. What is the minimum human grounding you would need before trusting a simulation of *your* buyer for guide-piloting? For copy ranking? For anything more?
3. The "Lost in Simulation" rehabilitation (simulation as system diagnostic) survives the sycophancy critique. Why? What exactly about "the system broke" is immune to the mechanisms in Layer 4?
4. Construct the best-faith argument that the zero-weight rule is *too strict* for some viability question you face. Where does the argument break, or does it? (If it doesn't, propose the amendment and the audit that would keep it honest.)
5. AI-moderated interviews of real humans inherit which of today's failure modes, and dodge which? Be precise; the taxonomy does real work here.
6. In five years, if synthetic panels *do* become decision-grade for some question class, what published evidence would convince you? Write the acceptance criteria now, while you have no stake in the answer.

## My take (reviewer lens)

**Lilian Weng** would tighten Layer 4's mechanisms: "sycophancy" and "distribution collapse" are described here at folk-psychology altitude, and she would want the underlying claims (post-training objectives, mode-seeking under low temperature, persona conditioning as distribution shift) stated carefully enough to predict *quantitatively* when simulation degrades, noting that several cited results are single studies on specific model generations and the field is moving; a protocol built on mechanisms should update as post-training methods change. Fair, and the acceptance-criteria reflection question is the hedge. **Ethan Mollick** would object that the lesson's net vibe is more negative than his read of the evidence: he has argued publicly that LLMs are already remarkably useful research instruments and that dismissing simulated respondents wholesale repeats the "AI can't do X" pattern that ages badly; he would emphasize Park et al. as a floor, not a ceiling. The lesson's answer is that the protocol is not a capability claim but a *decision-hygiene* rule under motivated reasoning: even a much better simulator stays upstream of belief while its errors correlate with what the founder wants to hear. **Hamel Husain** would approve the zero-weight rule and add the eval-shaped critique: "simulate to design, humans to decide" is a slogan until it has a measurement attached, so the divergence audit should be a *standing* instrument (re-run per model generation, track rows (a)–(c) counts over time), turning this lesson's position from dogma into a dashboard. That is the correct upgrade, and the Saturday tool's schema supports it.

## Further reading

**Must-read**

- Park et al., "Generative Agent Simulations of 1,000 People," arXiv 2411.10109 (2024), §2–4.[^2]
- Gui & Toubia, "The Challenge of Using LLMs to Simulate Human Behavior: A Causal Inference Perspective," arXiv 2312.15524.[^3]
- Rosala & Moran (NN/g), "Synthetic Users: If, When, and How to Use AI-Generated 'Research'" (2024).[^8]

**Recommended**

- "Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations," arXiv 2601.17087 (2026).[^5]
- Kapania et al., "'Simulacrum of Stories': Examining Large Language Models as Qualitative Research Participants," arXiv 2409.19430.[^6]
- Stanford HAI policy brief, "Simulating Human Behavior with AI Agents."[^7]

**Optional**

- "The Illusion of Intervention: Your LLM-Simulated Experiment is an Observational Study," arXiv 2605.20767 (2026).[^4]
- MeasuringU, "A Review of Experiments with Synthetic Users."[^11]
- Synthetic Users' science posts (read as the steelman from the selling side).[^1]

## Citations

[^1]: Synthetic Users (company), https://www.syntheticusers.com/ — per-interview pricing, multi-agent OCEAN-profiled architecture, and vendor-reported 85–92% parity claims; science posts at https://www.syntheticusers.com/science-posts/three-research-papers-that-helped-us-build-synthetic-users ; co-founder Hugo Alves; third-party review coverage at https://ai-cmo.net/tools/synthetic-users . Parity figures are vendor-reported and treated as such (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Joon Sung Park, Carolyn Q. Zou, Aaron Shaw, Benjamin Mako Hill, Carrie Cai, Meredith Ringel Morris, Robb Willer, Percy Liang, Michael S. Bernstein, "Generative Agent Simulations of 1,000 People," arXiv 2411.10109 (Nov 2024). https://arxiv.org/abs/2411.10109 — 1,052 interview-grounded agents; 85% GSS replication normalized to participants' own two-week test-retest; reduced bias vs. demographic personas; two-hour interviews per agent; two-tier data access. Corroborated by Stanford AI4PB project page https://ai4pb.stanford.edu/projects/generative-agent-simulations-of-1,000-people

[^3]: George Gui & Olivier Toubia, "The Challenge of Using LLMs to Simulate Human Behavior: A Causal Inference Perspective," arXiv 2312.15524 (SSRN 4650172). https://arxiv.org/abs/2312.15524 — prompt-based treatments violate unconfoundedness; ~50% of aggregate treatment effects replicated across 11 behavioral-economics experiments despite high individual-level predictive accuracy; unblinding (revealing the design) as partial mitigation.

[^4]: "The Illusion of Intervention: Your LLM-Simulated Experiment is an Observational Study," arXiv 2605.20767 (2026). https://arxiv.org/pdf/2605.20767 — formalizes the confounding/selection bias from intervention-induced "user drift" and proposes negative-control outcomes as a diagnostic (search-verified 2026-07-17 and re-corroborated 2026-07-18 via arXiv listing + ResearchGate; fetch egress-blocked — liveness pass pending).

[^5]: "Lost in Simulation: LLM-Simulated Users are Unreliable Proxies for Human Users in Agentic Evaluations," arXiv 2601.17087 (2026). https://arxiv.org/html/2601.17087v1 — simulated users more cooperative, inflate success rates, miss demographic-specific patterns; up to 9pp success-rate variance across user-LLMs; systematic miscalibration by task difficulty; proposes the system-diagnostic rehabilitation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Shivani Kapania et al., "'Simulacrum of Stories': Examining Large Language Models as Qualitative Research Participants," arXiv 2409.19430 (CHI 2025). https://arxiv.org/abs/2409.19430 — consent, researcher-participant relationship, and epistemic-harm critique from 19 interviewed qualitative researchers.

[^7]: Stanford HAI, "Simulating Human Behavior with AI Agents" (policy brief). https://hai.stanford.edu/policy/simulating-human-behavior-with-ai-agents — accessible summary of [^2] with governance framing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Maria Rosala & Kate Moran (Nielsen Norman Group), "Synthetic Users: If, When, and How to Use AI-Generated 'Research'," June 2024, updated since. https://www.nngroup.com/articles/synthetic-users/ and companion video https://www.nngroup.com/videos/ai-generated-users/ — re-ran three human studies synthetically; verdict: shallow, one-dimensional, sycophantic; "user research needs real users" (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: "We're Different, We're the Same: Creative Homogeneity Across LLMs," arXiv 2501.19361; with Doshi & Hauser, *Science Advances* (2024), per [[02-tue-ai-assisted-desk-validation|Tuesday]]'s citations — cross-model output clustering; collective-diversity loss applied here to simulated populations.

[^10]: "What LLM-Simulated Users Can and Cannot Tell Us About Conversational Energy Management Systems," Proceedings of the 2026 ACM Sustainability Week. https://dl.acm.org/doi/10.1145/3765611.3815484 — domain replication: surface interaction patterns mimicked, decision-relevant behavioral variables diverge (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: MeasuringU, "A Review of Experiments with Synthetic Users." https://measuringu.com/review-of-experiments-with-synthetic-users/ — running methodological review; direction sometimes matched, magnitude unreliable (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^12]: AI-moderated (real-human) interview platforms and the hybrid position: Prelaunch, "How to Scale the Mom Test with AI Interviews," https://prelaunch.com/blog/how-to-scale-the-mom-test-with-ai-interviews ; Koji's AI-moderated methodology docs https://www.koji.so/docs/mom-test-methodology — the moderator scales, the truth source stays human (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
