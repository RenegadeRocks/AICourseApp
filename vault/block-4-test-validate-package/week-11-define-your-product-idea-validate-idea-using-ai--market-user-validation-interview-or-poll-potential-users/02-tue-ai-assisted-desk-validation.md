---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 2
day_name: tue
session_slug: define-your-product-idea-validate-idea-using-ai
date_due: 2026-07-28
tags: [desk-research, deep-research-tools, market-sizing, bottom-up-tam, competitor-mapping, demand-signals, community-mining, seo-slop, sycophancy, homogenization, citation-verification]
sources:
  - felloai-deep-research-2026
  - rephrase-deep-research-2026
  - aimultiple-deep-research
  - cjr-ai-search-citation-errors
  - reddinbox-gummysearch-shutdown
  - subredditsignals-gummysearch
  - doshi-hauser-science-advances
  - creative-homogeneity-llms
  - kleinberg-raghavan-monoculture
  - userintuition-landing-tests
last_verified: 2026-07-17
word_count_target: 5300
---

# AI-assisted desk validation — an afternoon of research, and the five ways it lies to you

## Why this matters

Desk research is the cheapest evidence you will gather this week and the most dangerous, for the same reason: nothing pushes back. A deep-research agent will hand you a confident, structured, citation-studded market report on any idea in under half an hour. Yesterday's bet sentence deserves that report; it also deserves your knowledge of exactly where such reports are systematically wrong. Today you build the desk-research dossier for your idea: bottom-up market sizing, a competitor and adjacent-tool map, demand signals mined from communities and search behavior, and pricing comparables. Then you learn the five failure modes of AI-assisted research (recency gaps, SEO-slop inputs, sycophantic synthesis, fabricated specifics, and homogenized conclusions) and the verification protocol that turns a plausible-sounding report into evidence you would stake a build decision on. The skill compounds far beyond this week: every client engagement from Block 1, every packaged product from Week 9, starts with someone asking "what does the market look like?", and the person who can answer with *verified* speed is rare.

## Prerequisites

- Monday's frozen bet file (`validation/00-bet.md`). Desk research without pre-committed assumptions degrades into browsing.
- [[05-fri-niche-validation-and-unit-economics|Block 1 Week 2 Fri]] — niche-level unit economics; today's market sizing reuses its bottom-up habit at product scale.
- [[03-wed-the-scraping-stack-legally-and-technically|Block 3 Week 8 Wed]] — the canonical home for scraping law, robots.txt, ToS, and consent-aware collection. Today's community mining stays inside the rules established there; one-line recaps only.

## Layer 1 — What desk research can and cannot establish

Rank evidence by how much it cost the source to produce. Desk research sits at the bottom of this week's ladder: it can establish that a market *category* exists, what incumbents charge, how buyers describe the problem in public, and roughly how many potential buyers are reachable. It cannot establish that anyone will change behavior for *your* wedge. Treat every desk finding as an input to Wednesday's interviews and Friday's smoke test, never as a substitute. The concrete outputs today, each mapped to a Monday assumption:

1. **Sizing note** (viability): is the reachable market big enough to matter at your price?
2. **Alternatives map** (desirability + viability): who or what solves this today, at what price, with what complaints?
3. **Demand-signal digest** (desirability): where does the pain surface in public, in the customer's own words?
4. **Pricing comparables** (viability): what anchors exist for Friday's willingness-to-pay questions?
5. **Error log**: every claim your AI tools made that failed verification. This one is pedagogical today and habit-forming forever.

## Layer 2 — The 2026 deep-research stack, and how to drive it

Every frontier vendor now ships a research agent: ChatGPT Deep Research (longest, most structured reports, up to ~30 minutes per run, query-capped by plan), Claude's Research mode (strongest when the question needs judgment across sources rather than raw coverage), Gemini Deep Research (best inside a Google Docs/Drive workflow), and Perplexity Deep Research (fastest, ~2–4 minutes, citation-forward).[^1][^2] Two practical selection facts from the comparison literature: Perplexity's per-claim citations make it the easiest to *verify*, which matters more today than report quality; and the long-form tools produce better structure but bury weak claims deeper, which raises verification cost.[^1][^2][^3] On citation reliability in general-purpose AI search, the Columbia Journalism Review's Tow Center testing found error rates above 60% for some chat search products, with tools confidently citing wrong or nonexistent sources; the exact numbers move by release, but the direction has been replicated enough to set your prior: **assume any individual citation is wrong until checked.**[^4]

Protocol for the dossier (this is the worked shape; the experiment section makes it concrete):

- **Two-tool rule.** Run the same research brief through two different vendors' research agents. Claims that appear in both, with independent sources, get promoted to "check-worthy." Claims in one but not the other get flagged. This is cheap triangulation against single-model failure, and it also surfaces the homogenization problem in Layer 6 when both reports come back eerily similar.
- **Brief like an operator.** A research agent given "is there a market for X?" will answer yes; the question embeds the desired answer. Brief it with falsification framing: *"Find evidence for and against the claim that [assumption]. Separate the two lists. For every quantitative claim, give the primary source, its date, and its methodology in one line. Explicitly list what you could not find."* The for/against separation mirrors the evidence-ledger discipline you will build Saturday.
- **Date-fence everything.** Ask for source dates inline. Deep-research agents mix a 2022 market report with a 2026 pricing page without blinking, and AI-market numbers from even 18 months ago are archaeology; you watched an entire coding-agent market restructure in one quarter of 2026.

## Layer 3 — Market sizing: bottom-up only

Top-down sizing ("the AI agents market will be $47B by 2030, we need 0.1%") is what this course calls TAM theater. Its numbers come from analyst reports whose incentive is a big headline, its arithmetic launders a fantasy through a citation, and no decision you make this week changes if the headline number doubles. Investors discount it on sight; you should too.

Bottom-up sizing starts from *countable* units and multiplies only observables:

> reachable buyers × plausible penetration × your price = revenue envelope

For the meeting-follow-up agent from Monday's worked example: LinkedIn Sales Navigator gives you a countable proxy for US boutique consultancies (say a filtered count of firms with 2–15 employees in relevant categories); assume single-digit-percent penetration of the *reachable* subset (the ones inside your niche's distribution surface, per [[05-fri-niche-validation-and-unit-economics|Block 1 Week 2 Fri]]); multiply by $200/month. The point of the exercise is rarely the number itself. It is the shape of the sensitivity: if the envelope only clears your opportunity-cost bar at 20% penetration or a 5× price, the viability assumption just failed on paper, before you spent a single interview on it.

Use the deep-research agents to *fetch the countables* (directory sizes, association memberships, job-posting counts for the role that currently does the task, tool-user counts from public pages), not to do the multiplication. Every countable gets a URL in the dossier. A number without a primary source is a rumor with formatting.

## Layer 4 — The alternatives map: who solves this today

Build a table with one row per alternative and columns for: what it is, price, what it does well, the complaint pattern (verbatim quotes from reviews/communities), and what your wedge does that it cannot. Force these five rows to exist even when uncomfortable:

1. **A human** (the assistant, the junior, the founder at 11pm). Price = loaded hourly cost. Complaint pattern = turnover, inconsistency, "I do it myself because explaining takes longer."
2. **The incumbent's feature.** For almost any workflow, some incumbent SaaS has shipped an "AI" checkbox by mid-2026. Their complaint pattern lives in G2/Capterra reviews and community threads; mine it verbatim, because those quotes are Wednesday's interview probes and Friday's landing-page copy.
3. **The horizontal default: paste it into ChatGPT/Claude.** Price: ~$20/month, already paid. This row's "complaint pattern" is your entire differentiation thesis: no system access, no consistency, no memory of house style, nobody remembers to do it. If you cannot fill that cell with specifics, Monday's wedge needs revisiting. Note also Anthropic's own march up this stack (Claude Cowork going cross-platform in July 2026, agent templates for financial services): for any generic knowledge-work wedge, "the platform ships it natively" is a live viability risk to log, not a hypothetical.[^5]
4. **The DIY builder.** Your buyer's technically-inclined employee with n8n or Claude Code. You know precisely what that path costs because you *are* that path; price it honestly.
5. **Nothing / tolerate it.** The most common alternative and the most informative: what fraction of the community discussion is complaint-without-search-for-solution? High tolerance signals vitamin.

## Layer 5 — Demand signals: mining public pain, legally

Three signal families, in rising order of specificity:

**Search behavior.** Google Trends for the problem phrase (not your product category; buyers search their pain, not your solution shape). Rising multi-year interest in "automate [task]" phrasings is weak but real desirability evidence; flat lines are informative too. Free, five minutes, screenshot it into the dossier.

**Community pain.** Reddit, niche Discords, professional forums and Slacks, X. You want verbatim complaint language, workaround inventories ("I currently export to a spreadsheet and..."), and tool-recommendation threads (whose absence is itself a signal). A 2026 cautionary tale for tool dependence here: GummySearch, for years the default Reddit research tool, shut down after failing to secure a commercial license under Reddit's Data API terms (commercial access runs on the order of $0.24 per 1,000 calls), stranding its users; a cluster of successors now competes for the niche.[^6][^7] The durable skill is therefore not any tool but the method: search operators on the platform itself (`site:reddit.com "[task]" "hours"`, sort by recent), reading full threads rather than snippets, and logging quotes with URLs. Collection rules are the ones from [[03-wed-the-scraping-stack-legally-and-technically|Block 3 Week 8 Wed]]: public pages, platform ToS respected, no scraping behind logins, and quotes used for research get paraphrased or anonymized when they surface in your public copy. One-line recap; the full law and ethics live there.

**Money signals.** People already paying adjacent tools (their public pricing pages and case studies), freelancer marketplaces listing the task (Upwork postings for "meeting notes CRM entry" are demand receipts with dollar figures attached), and job postings for roles whose description *is* the task. A job posting is the strongest desk-level demand signal there is: someone budgeted a salary for this pain.

**Pricing comparables** fall out of the same pass: the incumbent feature's tier delta, the freelancer's hourly, the adjacent tool's per-seat price. Log each with its unit (per seat, per usage, per outcome), because Week 9's packaging logic ([[../week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/_week|Week 9]]) will want the unit as much as the number.

## Layer 6 — Where AI desk research systematically misleads, and the defenses

Five failure modes. Name them in your dossier's error log as you catch them; catching at least one today is part of the pass bar.

1. **Recency gaps.** Research agents blend training-data memory with live retrieval, and the blend is invisible. In a field where a quarter reshapes the tool landscape (you hold receipts: Windsurf became Devin Desktop, Cursor sold to SpaceX, GummySearch died), any uncached claim about "current" tools or prices is suspect. Defense: date-fence the brief; spot-check every load-bearing "current" claim against the vendor's own page.
2. **SEO-slop inputs.** Search-grounded agents inherit the affiliate-content economy: listicles that recycle each other, "review" sites that have never touched the product, statistics pages whose numbers trace to a decade-old press release through four layers of citation laundering. The comparison-shopping content you will retrieve about validation tools is itself largely this. Defense: for any statistic, walk the citation chain to a primary source; if the chain circles among content farms, discard. Simon Willison's long-standing rule applies: the model's output is a claim about sources, and claims get checked.[^8]
3. **Sycophantic synthesis.** Ask "is there a market for X?" and the agent finds one, because agreeable synthesis is the low-loss completion and your phrasing leaked the answer you wanted. This is the desk-research shadow of the interviewing sin Wednesday kills ("would you use this?"). Defense: the for/against brief structure from Layer 2, plus one dedicated adversarial run: *"Argue that this market is a trap. Steelman the bear case with sources."*
4. **Fabricated or laundered specifics.** The CJR/Tow Center line of testing keeps finding AI search tools confidently attaching real-looking citations to wrong claims.[^4] Deep-research products are better than chat search here, and still not good enough to skip verification. Defense: the five-citation spot check in today's experiment; permanent habit thereafter.
5. **Homogenized insight.** The subtle one. Doshi and Hauser showed in *Science Advances* that writers aided by GPT-4 produced individually better but collectively more similar stories; follow-up work finds the same homogenization across ideation tasks and across different LLMs, whose "distinct" outputs cluster tightly compared to human cohorts; Kleinberg and Raghavan's algorithmic-monoculture model predicts the systemic cost when many actors adopt the same decision aid.[^9][^10][^11] The desk-research corollary: every founder circling your space is running similar prompts through the same three research agents and receiving similar "insights," similar "underserved segments," similar "positioning gaps." AI-assisted desk research is table stakes for speed and *negative* differentiation on insight. Defense: treat the AI dossier as the commodity baseline, and mine your differentiation from the sources agents underweight: your Block 1 niche relationships, full community threads read end-to-end, and above all Wednesday's interviews, which no competitor can run through an API.

## Worked example — one hour on the meeting-follow-up agent

Continuing Monday's example, an abbreviated dossier: Sizing: ~14,000 US management-consulting firms with 2–15 employees countable via directory filters; reachable subset through the reader's ops-consulting niche perhaps 400; at 5% penetration and $200/month the envelope is ~$48K ARR, which fails a venture bar and clears a product-line bar, so viability is reframed as "wedge for a broader admin-agent line," logged as a new assumption. Alternatives map: notetakers (Otter/Fireflies/Granola tier, $10–30/seat) own transcription but reviews complain summaries "don't go anywhere"; CRMs ship AI note-sync features (complaint pattern: wrong fields, no voice); ChatGPT-paste covers drafting but drops CRM/tasks; VAs at $8–15/hr. Demand signals: Upwork postings for "CRM data entry from call notes" at $400–900/month budgets (money receipt); r/consulting threads on follow-up lag with workaround inventories; Trends flat on the category phrase but rising on "AI meeting notes to CRM." Error log from the two-tool run: one agent cited a "2026 survey" of consultancies that resolves to a vendor blog with no methodology (discarded); the two reports proposed nearly identical "insights" sections, homogenization observed in the wild. Elapsed: 65 minutes plus verification. The dossier's job is done: it sharpened two interview probes, one landing-page line, and one viability reframe, and it decided nothing, which is exactly its jurisdiction.

## Runnable experiment — the dueling-dossiers protocol (75–90 min)

**Step 1 (10 min).** Write the research brief from your Monday assumptions using the for/against, primary-source, date-fenced template in Layer 2. Save the brief; it is reusable IP.

**Step 2 (30 min, mostly waiting).** Run it through two research agents from different vendors (e.g., Claude Research and Perplexity Deep Research; any two-vendor pair works). While they run, do the five-minute Google Trends pass and one Upwork/job-board search by hand.

**Step 3 (20 min).** Diff the reports: claims in both / in one / contradictions. Contradictions are gold; log them explicitly.

**Step 4 (20 min).** Verification pass: pick the five most decision-relevant quantitative claims and walk each to a primary source. Score each: VERIFIED (primary source found, number matches), LAUNDERED (source exists, number distorted or stale), FABRICATED (no such source), UNVERIFIABLE (paywalled/private). Log all five in the error log with URLs.

**Step 5 (10 min).** Write the one-paragraph dossier summary: what desk evidence says for and against each Monday assumption, and what it cannot say. Commit `validation/01-dossier.md`.

**Pass bar:** (a) two-tool diff completed with at least one contradiction or one single-tool-only claim identified; (b) five citations scored, with at least one landing outside VERIFIED (if all five verify cleanly, either your idea inhabits an unusually well-documented market or your five picks were soft; re-pick harder claims once); (c) every number in your dossier summary carries a primary-source URL; (d) the bear-case adversarial run appears in the dossier, not just the bull case.

## Common mistakes experts see

1. **Research as procrastination with better graphics.** The dossier is time-boxed to an afternoon. Its marginal value collapses after that; interviews' does not.
2. **Top-down TAM in the dossier.** One analyst headline number quoted as evidence and the whole document's credibility is spent. Bottom-up or nothing.
3. **Accepting the agent's citations at face value.** The single most common failure. The CJR error-rate prior applies to you personally.[^4]
4. **Briefing for confirmation.** "Find the market size for X" presumes the market. For/against framing or you are paying for sycophancy at deep-research prices.
5. **Mining communities through a summarizer.** Thread summaries strip the verbatim language that makes community mining valuable. Read the top threads yourself; quote exactly.
6. **Ignoring the platform-risk row.** GummySearch's users lost their tool to an API-licensing decision overnight.[^6][^7] If your product idea depends on someone else's data faucet, that is a first-class viability assumption, not a footnote.
7. **Confusing category growth with wedge demand.** "AI agents market growing 40%" says nothing about whether ops managers want *your* follow-up drafts. Category tailwinds are the weakest admissible evidence in the ledger.

## Open questions — what's not settled

**1. Does verification scale, or is it a tax only the diligent pay?** The protocol in this lesson costs perhaps 30 minutes per dossier. At research volume (an agency running dossiers weekly, a fund screening hundreds of ideas), per-claim human verification stops scaling, and the tempting fix is to have a second model verify the first, which re-imports the correlated-error problem the verification exists to catch. The unsolved version: nobody has yet demonstrated a verification pipeline that is simultaneously cheap, automated, and robust to the shared-substrate failure (same index, same slop, similar models). Until someone does, the honest rule is that verified research has a human-minutes floor, and pricing research work (yours or a vendor's) below that floor should tell you what you are actually buying.

**2. What happens to the research commons the tools depend on?** Deep-research agents free-ride on an open web whose economics they are simultaneously eroding: the affiliate-slop pages they must filter are themselves increasingly AI-generated, and the high-quality primary sources they prefer (journalism, analyst work, forums) are being paywalled, licensed, or drained of contributors. Reddit's API pricing, the GummySearch death, and the NYT litigation are all fronts in the same enclosure.[^6] Whether the 2028 open web can still support desk research of today's quality is genuinely unknown; the practical hedge is the one this lesson already teaches, cultivate evidence sources that do not route through the commons: your niche's humans, your own data, paid primary sources.

**3. Is the homogenization effect self-correcting?** One argument says yes: as AI-derived insight becomes commodity, its market value falls, contrarian human-sourced insight commands a premium, and incentives rebalance. The counter-argument says the loop runs the other way: homogenized research produces homogenized products, which produce homogenized training data for the next model generation, compounding the collapse (the "monoculture" dynamic formalized by Kleinberg & Raghavan, now with a feedback term).[^11] Early empirical work exists on both sides and settles nothing. For your purposes the hedge is identical either way, which is why this lesson is comfortable teaching it as a rule despite the open theory: differentiation must come from evidence channels your competitors' agents cannot reach.

## Reflection questions

1. Which cell of your alternatives map was hardest to fill honestly, and what does that difficulty tell you about where your motivated reasoning concentrates?
2. Your two research agents agreed on most conclusions. Given Layer 6's homogenization evidence, how much of that agreement is corroboration and how much is monoculture? How would you tell the difference?
3. A job posting is described as the strongest desk-level demand signal. Construct a case where it misleads (the posting exists, but your product still fails). What does that case imply for Wednesday's interview questions?
4. If Reddit tripled its API price tomorrow, which parts of your demand-signal method survive? Which parts of your *product idea* survive, if any depend on platform data?
5. Your sizing envelope came out at some number. What is the smallest number at which you would still personally pursue this, and is that threshold written in your Monday decision rule? If not, why not?
6. What is one claim in your dossier you *want* to be true badly enough that you should assign someone else (or an adversarial prompt) to attack it?

## My take (reviewer lens)

**Simon Willison** would endorse the verification protocol and then sharpen it: the two-tool diff is weaker than it looks, because "two different vendors" increasingly means two agents retrieving from the same SEO-saturated index and reasoning with models trained on overlapping corpora; real triangulation needs at least one *non-search* leg (a primary dataset, a human, a paywalled report you actually buy). He would also note, correctly, that the error-log habit is the lesson's most valuable artifact and deserves to outlive the week. **Jeremy Howard** would push against the tool-forward framing of Layer 2: teaching four branded research agents in a fast-moving market is exactly the kind of content that fossilizes (this vault's own July refresh graded April's tool-comparison lesson a D+ for the same sin), and the durable lesson is the brief template and the verification ladder, which would survive every product in the layer being renamed by Christmas. Fair, and it is why the layer teaches selection *principles* with the products as this quarter's instances. **swyx** would add a builder's note: the highest-leverage output of today is not the dossier but the reusable research-brief-plus-verifier pattern, which is one Claude Code command away from being a product feature of your own; noticing that is the AI-engineering reflex this course keeps trying to install.

## Further reading

**Must-read**

- Columbia Journalism Review (Tow Center), "AI Search Has A Citation Problem" (Klaudia Jaźwińska & Aisvarya Chandrasekar, Mar 2025).[^4]
- Doshi & Hauser, "Generative AI enhances individual creativity but reduces the collective diversity of novel content," *Science Advances* (2024).[^9]

**Recommended**

- Fello AI, "AI Search and Deep Research Tools Compared" (2026) plus one second comparison source of your choosing, read for the *selection criteria*, not the verdicts.[^1][^2]
- Kleinberg & Raghavan, "Algorithmic monoculture and social welfare," *PNAS* (2021).[^11]

**Optional**

- "We're Different, We're the Same: Creative Homogeneity Across LLMs" (arXiv 2501.19361).[^10]
- User Intuition, "Landing Page Tests: Measuring Demand Before Building," for how desk numbers hand off to Friday's instruments.[^12]

## Citations

[^1]: Fello AI, "AI Search and Deep Research Tools Compared 2026." https://felloai.com/ai-search-deep-research-comparison/ — positioning of ChatGPT Deep Research (long structured reports, ~30-min runs, plan-based query caps), Perplexity (2–4 min, per-claim citations), Claude Research (judgment-heavy work), Gemini (Workspace integration) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Rephrase, "AI Deep Research Tools Compared for 2026." https://rephrase-it.com/blog/ai-deep-research-tools-compared-for-2026 — independent corroboration of the tool-positioning claims in [^1] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: AIMultiple, "AI Deep Research: Claude vs ChatGPT vs Grok." https://aimultiple.com/ai-deep-research — third corroborating comparison; used only for claims appearing in ≥2 of [^1][^2][^3] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Klaudia Jaźwińska & Aisvarya Chandrasekar, "AI Search Has A Citation Problem," Columbia Journalism Review / Tow Center, March 2025. https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php — >60% incorrect citations across tested chat-search tools in aggregate; error rates vary by product; direction replicated in later comparison testing cited in [^1] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Anthropic Claude Cowork cross-platform launch (web + mobile, Jul 7, 2026) and most-users-aren't-coding usage data: TechCrunch https://techcrunch.com/2026/07/07/the-coding-agent-wars-are-spilling-into-the-rest-of-the-office-claude-cowork/ and VentureBeat https://venturebeat.com/technology/anthropic-brings-claude-cowork-to-mobile-and-web-as-usage-data-shows-most-users-arent-coding ; URL-verified in `_refresh-2026-07-landscape-delta.md` §2 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Reddinbox, "GummySearch is Gone: The Best Alternatives in 2026." https://reddinbox.com/blog/best-gummysearch-alternative — shutdown after failing to secure a Reddit commercial Data API license; Reddit commercial access on the order of $0.24 per 1,000 API calls (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: SubredditSignals, "GummySearch Shut Down: Best Alternatives in 2026." https://www.subredditsignals.com/blog/gummysearch-alternatives-in-2026-best-reddit-monitoring-tools — independent corroboration of the shutdown and its API-licensing cause; sources differ on the exact wind-down date (late 2025 shutdown vs. paid access through Nov 30, 2026), so this lesson asserts only the fact and cause of shutdown (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Simon Willison's ongoing writing on verifying LLM tool claims and treating model output as unverified claims about sources, e.g., https://simonwillison.net/ (evergreen practice; specific posts vary).

[^9]: Anil R. Doshi & Oliver P. Hauser, "Generative AI enhances individual creativity but reduces the collective diversity of novel content," *Science Advances* 10(28), 2024. https://www.science.org/doi/10.1126/sciadv.adn5290

[^10]: "We're Different, We're the Same: Creative Homogeneity Across LLMs," arXiv 2501.19361 (2025). https://arxiv.org/abs/2501.19361 — outputs from different LLMs cluster tightly relative to human cohorts; corroborates the cross-model homogenization claim alongside [^9] and the homogenization-in-ideation literature (arXiv 2402.01536).

[^11]: Jon Kleinberg & Manish Raghavan, "Algorithmic monoculture and social welfare," *PNAS* 118(22), 2021. https://www.pnas.org/doi/10.1073/pnas.2018340118

[^12]: User Intuition, "Landing Page Tests: Measuring Demand Before Building." https://www.userintuition.ai/reference-guides/landing-page-tests-measuring-demand-before-building/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
