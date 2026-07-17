# week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent — Refresh Review Findings (2026-07-17)

Reviewer note on verification method: the sandbox's egress gateway returned policy-denial 403s
on direct WebFetch to most third-party domains this pass (confirmed via `__agentproxy/status`:
"gateway answered 403 to CONNECT"). Where a URL could not be fetched directly, liveness and
content were verified via search-index presence (noted per item). **Do not interpret any 403
noted below as a dead link.** WebSearch budget for the session was exhausted near the end of
this review; three low-risk checks are flagged as "verify in fix phase."

## Verdict

This is a structurally excellent week whose *reasoning* has aged well (workflow-over-autonomous,
hybrid retrieval, eval-driven development, "long context doesn't obsolete RAG" — all confirmed
as the July-2026 consensus) but whose *facts* have a hard April-2026 watermark. The model
landscape is now wrong everywhere it's stated (Claude 5 generation — Fable 5/Mythos 5 — shipped
June 9, 2026; Opus 4.8 and Sonnet 5 are current; every model the experiments pin — Sonnet 4.6,
Opus 4.7 — is now on Anthropic's legacy table). The vendor landscape moved sharply: Artisan cut
entry pricing 10× to $250/mo with self-serve Ava 2.0 (May 2026), gutting Monday's pricing
guidance; Sierra re-raised at $15.8B/$150M+ ARR (May 2026); MCP's largest-ever spec revision
(2026-07-28) publishes eleven days after "today" and Tuesday doesn't know it exists. Thursday's
MTEB table — a headline artifact — names a #1 that is no longer top-five. Saturday is the most
durable lesson but has cross-week eval-threshold inconsistencies Hamel would flag, plus a
sample-size self-contradiction. Slop is low for the genre but the contrast-scaffold tic exceeds
the >2/file threshold in five of eight files.

Currency grades: 00-overview **C+** · 01-mon **C+** · 02-tue **C** · 03-wed **B+** ·
04-thu **C** · 05-fri **C+** · 06-sat **B** · 07-sun **C+**. Week overall: **C+ / B-** —
sound skeleton, stale skin; a focused refresh pass (models, vendors, MCP, MTEB/rerankers,
eval-threshold reconciliation) lifts it back to A-range.

## CRITICAL (untrue today / broken commands / dead-wrong model landscape)

- **[all files: model references] The Claude model landscape is pre-Claude-5.** Claude Fable 5
  and Claude Mythos 5 GA'd June 9, 2026 ($10/$50 per MTok, 1M context, 128K output; Mythos 5
  limited-availability via Project Glasswing). Current lineup: Fable 5, Opus 4.8 ($5/$25, 1M),
  Sonnet 5 ($3/$15; intro $2/$10 through Aug 31, 2026; 1M), Haiku 4.5 ($1/$5, 200K). **Opus
  4.7, Opus 4.6, and Sonnet 4.6 are all now on the legacy table**; Opus 4.1 is deprecated and
  retires Aug 5, 2026. Every experiment prompt in Tue/Thu/Fri/Sat pins "Claude Sonnet 4.6" as
  the build model and "Claude Opus 4.7" as the judge — the calls still run (models remain
  available) but the lesson is teaching a reader to build new systems on legacy models.
  Evidence: https://platform.claude.com/docs/en/about-claude/models/overview and
  https://www.anthropic.com/news/claude-fable-5-mythos-5 (both fetched/searched 2026-07-17).
- **[05-fri:Layer 3 "The context-window reality, as of April 2026"] The frontier framing is
  dead.** "Opus 4.7 as of April 2026 runs at 1M input / 128K output with standard $5/$25
  pricing" — Opus 4.7 is legacy; the widely-available frontier is Opus 4.8 (same price) and the
  capability frontier is Fable 5 at **$10/$50**, i.e. 2× the price the cost tables assume.
  Additional wrinkle the fix phase should exploit: per Anthropic's model docs, **Opus 4.7 /
  Opus 4.8 / Fable 5 use a new tokenizer that produces ~30% more tokens on the same text**
  than pre-4.7 models — this materially inflates the pure-long-context column in Friday's
  cost-per-correct-answer table and Sunday's Q16 math. The lesson's *conclusion* (long-context
  costs 30–50× RAG per query) survives and arguably strengthens; the numbers need recomputing.
  URL: https://platform.claude.com/docs/en/about-claude/models/overview.
- **[01-mon:Layer 4 pricing + Artisan teardown] Artisan's pricing/positioning is obsolete.**
  Artisan launched **Ava 2.0 in May 2026: self-serve, GA, entry pricing cut 10× from
  $2,500/month to $250/month**, $300 free credits, no-credit-card onboarding (~$50.6M total
  raised). Monday's market map ("AiSDR ~$900/mo… Salesforge ~$599… 11x $5,000+/mo") and its
  operator advice ("the hybrid pattern — a low seat floor ($1–3k/month)… is what you should
  price your own builds at by default") now sit against a market where the best-known AI BDR
  costs $250/mo self-serve. The pricing-position problem set (Problem 5) is answering a market
  that no longer exists. Evidence:
  https://www.artisan.co/blog/artisan-launches-ava-2-0-the-first-autonomous-ai-bdr-now-self-serve
  (found via search; direct fetch blocked by sandbox).
- **[04-thu:Layer 3 MTEB table] "Google Gemini Embedding 001 — Current #1 English MTEB" is
  false in July 2026.** Current leaderboard state: **QZhou-Embedding leads MTEB at ~75.97**;
  on the official multilingual board **Tencent KaLM-Embedding-Gemma3-12B is #1 at 72.32** (as
  of July 2026); Qwen3-Embedding open-weight models outrank Gemini Embedding. The whole table
  (scores in the 62–68 band) reads as a snapshot of an earlier leaderboard era, and it also
  conflates English-MTEB and multilingual-MMTEB numbers without saying which board each row is
  from. The lesson's own advice ("benchmark on your corpus") survives; the table is the thing
  readers will screenshot, and it's wrong. Evidence:
  https://www.codesota.com/benchmarks/mteb, https://huggingface.co/spaces/mteb/leaderboard,
  https://app.ailog.fr/en/blog/news/rag-benchmark-mteb-2026 (via search).
- **[02-tue:Layer 4 + Further reading §6] MCP guidance predates the largest spec revision since
  launch, publishing 11 days from now.** The **2026-07-28 MCP spec** (release candidate locked
  May 21, 2026; final scheduled July 28, 2026) removes the protocol-level session and
  initialize/initialized handshake (stateless core), adds the Extensions framework, Tasks,
  MCP Apps, and **mandatory OAuth 2.0 Protected Resource Metadata + Resource Indicators** —
  which directly changes the lesson's security calculus (the "43% of MCP servers have auth
  flaws" claim describes the pre-hardening world). Telling a July-2026 reader to "skim the
  2025-11-25 spec" without mentioning the RC is teaching them a protocol version about to be
  superseded. Evidence: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/,
  https://workos.com/blog/mcp-2026-spec-agent-authentication,
  https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/.

## MAJOR (stale, weakened, shifted controversy, missing must-have development)

- **[02-tue:Layer 5 + Case 1] Sierra numbers superseded.** May 4, 2026: Sierra raised **$950M
  Series E at $15.8B post-money** (Tiger Global + GV; Benchmark/Sequoia/Greenoaks
  participating), disclosing **$150M+ ARR in eight quarters** and customers incl. Prudential,
  Cigna, Blue Cross Blue Shield, Rocket Mortgage, "one in three of the world's largest banks."
  Lesson states $100M ARR / $10B valuation as current. The architectural point (workflow +
  policy gates won) is *strengthened* by the new round — easy fix, high visibility. Evidence:
  https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/,
  https://www.cnbc.com/2026/05/04/bret-taylor-sierra-fundraise-openai.html.
- **[01-mon:11x teardown] 11x's 2026 state is absent.** 11x is alive under CEO Prabhav Jain
  (ex-CTO; Sukkar stepped down May 2025 — Wednesday mentions this, **Monday's teardown never
  does**), shipped **Julian (AI phone rep, ~$4–6K/mo reported)** and a rebuilt agentic Alice,
  and joined IBM watsonx Orchestrate's Agent Connect. ~77 employees as of May 2026. The
  teardown ends the story in mid-2025; a July-2026 read needs the post-scandal chapter (and
  the Mon/Wed internal inconsistency fixed). Evidence: https://toarn.com/insights/11x-ai,
  https://www.11x.ai/blog (via search).
- **[02-tue: whole lesson] The July-2026 agent-stack is missing: Claude Agent SDK, OpenAI
  Agents SDK, LangChain 1.x/Deep Agents-as-product.** The lesson frames the build choice as
  "direct Anthropic SDK tool-use loop vs MCP (with LangGraph as an aside)." The 2026 landscape
  splits into provider-native harnesses (**Claude Agent SDK** — extracted from Claude Code;
  **OpenAI Agents SDK**; Google) vs cross-provider frameworks (LangGraph ~47M monthly
  downloads, CrewAI, Pydantic AI), and LangChain's **Deep Agents is now a shipped product with
  an official comparison page against the Claude Agent SDK** — not "LangGraph's 2025 Deep
  Agents paradigm" as the lesson has it. A reader building the Tuesday sales agent in July
  2026 would most plausibly reach for the Claude Agent SDK; the lesson never names it.
  Evidence: https://docs.langchain.com/oss/python/deepagents/comparison,
  https://www.morphllm.com/ai-agent-framework, https://qubittool.com/blog/ai-agent-framework-comparison-2026.
- **[01-mon:^22 / 02-tue:Layer 2 / 07-sun:Q6] BFCL numbers stale; leaderboard refreshed.**
  BFCL is still on V4 (good — no version break), but the board was updated July 2026 and is
  now led by **Qwen3.7 Max at 0.750**; the lesson's cited "Claude Sonnet 4 70.29% / Claude
  Opus 4.1 70.36% / GPT-5 59.22%" names one deprecated model and one superseded generation.
  Also (pre-existing weakness): the "~6–8 tools then 5–15pp degradation" claim in Sun Q6/
  flashcard 10 is attributed to BFCL, but BFCL does not publish a tool-count-threshold
  result — this is an operator heuristic dressed as a benchmark finding, and Anthropic's
  advanced tool use (tool_search_tool, programmatic tool calling — which Tue's own reviewer
  lens concedes) further relaxes it. Evidence: https://llm-stats.com/benchmarks/bfcl-v4,
  https://gorilla.cs.berkeley.edu/leaderboard.html.
- **[04-thu:Layer 5] Reranker section is a generation behind.** The text centers **rerank-2
  (Sept 2024)** as "the quality benchmark at release" while its own footnote [^28] casually
  cites "Voyage Rerank 2.5" from the Agentset table — **rerank-2.5 / 2.5-lite shipped August
  2025** (7.94%/7.16% over Cohere Rerank v3.5; first instruction-following rerankers; 32K
  context = 8× Cohere 3.5), i.e. the lesson was already ~8 months behind at generation time
  and is now doubly so. Voyage is also now branded **"Voyage AI by MongoDB"** (MongoDB
  acquisition, Feb 2025) — never mentioned; blog.voyageai.com citations should be checked for
  redirects to mongodb.com. Evidence:
  https://www.mongodb.com/company/blog/product-release-announcements/rerank-2-5-and-rerank-2-5-lite-instruction-following-rerankers,
  https://www.mongodb.com/docs/voyageai/models/rerankers/.
- **[06-sat:Layer 2/5 + 07-sun] RAGAS/DeepEval tooling drift.** RAGAS docs are now v0.3.x and
  the repo has moved orgs (github.com/**vibrantlabsai**/ragas; was explodinggradients), with
  the v0.1→v0.2 migration having renamed metric imports (`faithfulness` → `Faithfulness`
  class, `SingleTurnSample`/`EvaluationDataset` schema, `ascore` deprecated) and v0.4
  migration guides now appearing — any reader following older RAGAS tutorials will hit import
  errors; the lesson's harness prompt doesn't pin a version. **DeepEval shipped 4.0 in 2026**
  (agent-native eval harness, coding-agent eval-driven-iteration loops for Claude Code/Cursor,
  terminal trace TUI) — Saturday's build-vs-buy table describes DeepEval as "an eval library,
  not a platform," which undersells its current shape. Evidence:
  https://github.com/vibrantlabsai/ragas/releases, https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/,
  https://deepeval.com/changelog/changelog-2026.
- **[06-sat vs 07-sun] Eval-threshold incoherence (Hamel lens, hard).** The week states three
  different judge-validation bars as if canonical: Sat Layer 3/4 — ">90% judge-expert
  agreement" (correct per Hamel's Field Guide); Sun Q19/flashcard 40 — "**>95%** agreement";
  Sun mental-move 13 — "validated against 20 human labels to **>85%** agreement." Pick one
  operationalization (Hamel's published number is >90% on Honeycomb) and propagate. A student
  drilling the flashcards learns a number the source doesn't support.
- **[06-sat:experiment + 07-sun:exercise] Sample-size self-contradiction.** Sat's "Common
  failure modes" correctly warns that N=30 binary judgments carry ~±9pp at 95% CI ("small-N
  overconfidence") — yet the Sat harness uses a **30-query regression set** with a **2pp
  assertion gate**, and Sun's exercise sets "faithfulness >0.9 on a 30-query eval set." A 2pp
  gate on N=30 (or even the referenced 200-example set: 2pp = 4 examples) is inside noise. The
  regression-gate spec needs either bigger N or a significance test in the gate rule — the
  lesson's own McCardel reviewer-lens point (Sun #5) flags this and the harness ignores it.
- **[05-fri + 07-sun] Gemini state is wrong/missing.** Sun Open Q4 credits "**Gemini 2.5
  Pro's 2M context**" — Gemini 2.5 Pro shipped at 1M (2M was a 1.5-Pro-era spec); and
  **Gemini 3 (Nov 2025) predates generation yet is absent from the entire week**, while Friday
  frames the long-context frontier as "Gemini 1.5 Pro… since 2024." The long-context debate
  section names the right papers but the wrong current models. (Model-name check ran out of
  search budget for exact Gemini 3 context specs — verify in fix phase.)
- **[03-wed] Holds up best; two aging notes.** (1) Gmail moved to **hard enforcement (outright
  rejection) of non-compliant bulk traffic starting Nov 2025** — the lesson's "filtered to
  spam" framing is now the lenient case; 2026 guides describe rejection as the default
  penalty. (2) The CAN-SPAM $53,088/email figure is the Jan-2025 inflation adjustment; the FTC
  adjusts annually each January — verify the 2026 figure. Evidence:
  https://redsift.com/guides/bulk-email-sender-requirements,
  https://www.scaledmail.com/blogs/email-deliverability-news.
- **[01-mon:Regie section] Regie's scale framing is off.** Regie.ai raised a **$30M Series B
  in March 2025** (total ~$65.6M; Foundation Capital/Scale/Khosla) and secured an AI-agent
  patent (Oct 2025) — the lesson characterizes it via an "ExtRuct AI estimates ~$3.8M revenue"
  data point (a low-quality scraped estimate) and omits the Series B, which predates
  generation. The "component of the stack" positioning read is fine; the evidence base is
  weak. Evidence: https://tracxn.com/d/companies/regie-ai/…, https://www.crunchbase.com/organization/regie-da23.
- **[04-thu:Layer 1 cost math + experiment] Contextual Retrieval cost math silently switches
  models.** The $1.02/M-doc-tokens figure is Anthropic's number **using Claude 3 Haiku
  ($0.25/M input)**; the experiment tells the reader to "use Claude Haiku 4.5 with prompt
  caching" ($1/M input) — ~4× the ingestion cost of the quoted figure. Either quote the
  Claude-3-Haiku basis explicitly or recompute for Haiku 4.5. (Conceptual claim — caching is
  the enabler — remains true and was verified against the Anthropic post in April.)
- **[06-sat] Missing: the evals field now has a book of record.** Husain & Shankar, *Evals for
  AI Engineers* (O'Reilly), publishes **Oct 31, 2026** (course cohort re-runs Sept 2026). For
  a lesson whose thesis is "evals are the moat," the canonical forthcoming text should be in
  Further Reading. Evidence: https://www.oreilly.com/library/view/evals-for-ai/9798341660717/,
  https://maven.com/parlance-labs/evals.
- **[02-tue:Layer 1] Anthropic's own successor guidance is absent.** Anthropic's *Effective
  context engineering for AI agents* (engineering blog, pre-dates generation) extends
  Building Effective Agents with the "minimal viable tool set" and context-curation guidance
  that directly supports the lesson's ≤6-tools argument — citing it would both modernize and
  strengthen Layer 3. Evidence:
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents.

## CITATIONS (dead / fabricated / misattributed / overclaimed)

Method note: direct fetches were blocked by the sandbox proxy (403 CONNECT denials) for most
domains; items below marked **[search-verified]** were confirmed live + content-matched via
search results; **[unverified this pass]** items could not be re-checked before the search
budget exhausted — none showed evidence of being dead.

- **[01-mon:^10 / regie.ai/customers/reputation] VERIFIED.** Page exists: "How Regie.ai
  Unlocked 48% Positive Email Reply Sentiment… at Reputation"; 48% positive sentiment, 7%
  reply rate, 66.7% open rate confirmed. [search-verified]
- **[03-wed: Mailgun Becker interview] VERIFIED.** Page exists; Becker (Sr. Director PM,
  Yahoo) and the "if you send 4,999 messages you still have to follow the requirements"
  sentiment both confirmed. Note: lesson credits interviewer "Eivind Sarto" — not confirmed in
  search snippets; verify byline in fix phase. [search-verified]
- **[02-tue:^16 / scalifiai.com "Six Fatal Flaws of MCP"] EXISTS but is vendor content
  marketing** — Scalifi sells Cognis AI, a "Multi-LLM Agentic platform," positioned against
  MCP; the piece is a competitor's takedown, not neutral security research. The lesson leans
  on it for the Postmark-breach, "43% OAuth flaw rate," and "40K-token tax" numbers (footnote
  hedges that these come from "linked community incident reports"). The Postmark-MCP npm
  breach is independently real (Koi Security, Sept 2025), but this load-bearing security
  paragraph deserves a primary source (e.g., the Koi/Snyk writeups or the arxiv MCP
  measurement study 2509.25292). Overclaimed-by-sourcing. [search-verified existence]
- **[05-fri:^lazygraph] MISATTRIBUTION.** "Writer's 2024 RobustQA reported knowledge-graph
  approaches at 86.31% vs 59–75% for RAG baselines" is cited to the Microsoft LazyGraphRAG
  blog — that number is from **Writer's own RobustQA benchmark marketing**, not Microsoft's
  post. Needs its own citation (writer.com engineering blog) with a vendor-disclosed caveat.
- **[01-mon:^1 vs 03-wed:Case 2] INCONSISTENT AUTHOR ATTRIBUTION.** The same March 24, 2025
  TechCrunch 11x investigation is credited to "Julie Bort" (Mon, Sun ^1) and "Marina Temkin"
  (Wed). At most one is right — verify the byline and unify. (URL itself is consistent and
  was live at April verification.)
- **[02-tue:^7 BFCL PMLR quote] SUSPECT QUOTE FIDELITY.** The block quote attributed to the
  PMLR 2025 BFCL paper — "State-of-the-art LLMs excel at single-turn calls, memory, dynamic
  decision-making, and long-horizon reasoning remain open challenges. Early results reveal a
  split personality: top AIs ace the one-shot questions…" — is grammatically broken (comma
  splice) and reads like blog/press phrasing, not an academic abstract. Verify against the
  actual paper; likely a paraphrase presented as verbatim.
- **[04-thu:^2] ADMITTED NON-CITATION.** Footnote for the lesson's framing numbers ("default
  RAG hits 60–75% retrieval hit-rate… 50–65% end-to-end correctness") literally reads "Common
  knowledge enterprise RAG deployments hit 50–65%…" attached to a Menlo report that doesn't
  contain those numbers. These are the second and third numbers in the lesson; they need a
  real source or explicit "operator folklore" labeling.
- **[03-wed:reviewer lens] SUSPECTED MISATTRIBUTED PERSON.** "Vaibhav Kakkar (Founder,
  Smartlead)" — Smartlead's founder is widely identified as **Vaibhav Namburi**; "Vaibhav
  Kakkar" is a different person (Digital Web Solutions CEO). Could not web-confirm before
  budget exhausted — high-priority verify; if wrong, this is a named-person error in a
  reviewer-lens section, the exact place the vault promises named accuracy.
- **[00-overview L60 + _review roster] SUSPECTED PHANTOM PERSONA.** "Aman Hylak (sales-eng
  pragmatics)" — no such public figure surfaced in any search this pass; almost certainly a
  garbling of **Ben Hylak** (raindrop.ai — who is real, and is correctly cited in Tue/Thu
  bodies, but is a product/AI-UX person, not sales-eng). The phantom name appears only in the
  overview's reviewer list and _review.md. Verify → excise.
- **[05-fri] "How Significant Are the Real Performance Gains?" (arxiv 2506.06331)** —
  plausible June-2025 third-party GraphRAG evaluation; not verified this pass. [unverified
  this pass]
- **[04-thu:^10 firecrawl.dev chunking benchmark; ^28 agentset.ai rerankers]** — direct fetch
  blocked; not search-verified before budget exhausted. Both were "verified 2026-04-17" and
  both are the sole source for load-bearing numbers (69% recursive-512 accuracy; 595–603ms
  reranker latencies). Re-verify in fix phase; both are blog-tier sources carrying
  benchmark-grade weight — consider demoting to "one vendor benchmark reports…" framing.
  [unverified this pass]
- **[01-mon:^6 outreach.ai URL]** — the Outreach survey is cited at `outreach.ai` (company's
  primary domain has historically been `outreach.io`). Search confirmed the report's existence
  but I could not confirm the .ai domain resolves. Verify. [unverified this pass]
- **[05-fri:^claude1m claude.com/blog/1m-context-ga]** — consistent with the verified current
  model docs (1M standard on Opus 4.6+); URL itself not re-fetched. [unverified this pass]
- Positive note: the April pass's citation hygiene is genuinely good — the ^9 (Stebbings/Latka)
  "unverifiable-secondary" tag, the ^13 MCP-stats hedge, the ^28 Agentset table-vs-prose
  discrepancy note, and the Endex vendor-disclosure caveat (Fri Case 2) are exactly the right
  practice and were confirmed still accurate in structure.

## SLOP (per file: contrast-tic count, fluff, repetition)

Contrast-scaffold tic ("X is not Y — it is Z" family), grep-counted (patterns:
`— it is/it's`, `is not … —`, `not …. It/This/That is`) plus hand-read instances; threshold
is >2/file:

- **00-overview**: 0 grep hits. Clean. Minor: "inbox-flooding theatre" coinage repeats across
  the week (overview, Mon, Wed, Sun — 4×; it's a good coinage used 2× too often).
- **01-mon**: ~8 (e.g., "That story is not the story of one bad actor. It is the story of an
  entire product category"; "the implication is not 'avoid AI SDR' — it is…"; "It's not 'we
  book X meetings' — it's…"). **Over threshold.**
- **02-tue**: ~11, the worst offender ("That is not a reason to abandon tools — it is a
  reason…"; "The fix is not a better model; it is splitting…"; "Error loudness is a feature,
  not a bug"; "not 'more capable single agent'"). Also "load-bearing" ×5 in one file — a
  vault-wide verbal tic (16 uses across the week incl. front-matter prose); ration it.
  **Over threshold.**
- **03-wed**: ~3 ("The mechanism isn't 'AI detection' — it's…"; "a generator-diversity
  problem, not a human-vs-AI problem"). Borderline-over. Otherwise the least sloppy lesson;
  "This is a 15-line routing rule, not a PhD" earns its keep.
- **04-thu**: ~4 ("That is not a criticism — it is a scoping observation"; "It's boring
  engineering — and it's why it works"; "The decision you're making is not 'which intervention
  is best.' It's…"). **Over threshold.**
- **05-fri**: ~7 ("The trade is not 'graphs make RAG better for free'; it is…"; "This is not a
  technical trade-off — it is a product trade-off"; "not accuracy alone and not cost alone —
  it's cost per correct answer"). **Over threshold.**
- **06-sat**: ~3 + the opening anaphora ("'Looks good' is not an evaluation. 'The demo
  convinced the CEO' is not an evaluation…") — rhetorically effective once; the "you don't
  have evals — you have a dashboard" move then repeats at the end of war-story 3 ("you don't
  have an eval program, you have a dashboard") — same punchline twice in one file.
- **07-sun**: low tic density (synthesis format helps); "reshapes the decision boundary"
  appears twice (Q20 answer + Open Q4).
- **Repetition across the week**: the ZoomInfo legal-threat quote ("deceptive trade practices,
  trademark infringement, misappropriation of goodwill, and false advertising") appears
  verbatim **3×** (Mon ×2, Wed ×1) — once as evidence, twice as recycling. The Schluntz/Zhang
  "simplest solution possible" quote appears Tue + Sun mental-move 2 + overview (3×;
  acceptable for a thesis quote, but Sun could paraphrase). Contextual Retrieval
  5.7→2.9/49%/67% appears in overview + Thu + Fri + Sun Q11/Q12 + flashcards 18–19 (≥6
  statements; quiz/flashcard repetition is by design, prose repetition in overview+Fri could
  compress).
- **Fluff**: genuinely low. No "delve"/"game-changer"/"In a world where" instances found. The
  week earns its word count almost everywhere; the padded spots are the triple-restatement of
  war stories (Sat Layer 4 vs "Operator war stories" retells Nurture Boss and Honeycomb nearly
  in full twice within one file — "Already cited above but worth restating as a full war
  story" is an admission, not a justification).

## MISSING (what a July-2026 reader needs that isn't here)

1. **Claude 5 generation (Fable 5 / Mythos 5), Opus 4.8, Sonnet 5** — model references,
   experiment pins, judge choices, and all cost tables (see CRITICAL).
2. **MCP 2026-07-28 spec revision** — stateless core, Extensions, Tasks, MCP Apps, OAuth PRM
   mandate; also reframes the Tue security section and the "fat-vs-thin server" discussion.
3. **Agent harness layer**: Claude Agent SDK, OpenAI Agents SDK, LangChain Deep Agents
   (product), and the provider-native-vs-cross-provider framework split that defines the July
   2026 stack conversation.
4. **Artisan Ava 2.0 self-serve at $250/mo** and the resulting AI-SDR price collapse; 11x's
   post-scandal chapter (Jain as CEO, Julian voice rep, IBM watsonx distribution).
5. **Sierra $950M Series E / $15.8B / $150M+ ARR** (May 2026).
6. **Current MTEB reality**: QZhou-Embedding, KaLM-Embedding-Gemma3-12B, Qwen3-Embedding tier;
   voyage-3.5; "Voyage AI by MongoDB" branding; rerank-2.5 instruction-following rerankers.
7. **Gemini 3** (Nov 2025 — already missing at generation) in the long-context landscape;
   GPT-5.5 exists and Sun/Mon references to "GPT-4.x/GPT-5" tiers need a refresh.
8. **RAGAS v0.3+/org move and DeepEval 4.0** — pin versions in harness prompts.
9. **Husain & Shankar, *Evals for AI Engineers* (O'Reilly, Oct 31, 2026)** in Sat further
   reading; Anthropic's *Effective context engineering for AI agents* in Tue.
10. **Gmail's Nov-2025 enforcement hardening** (rejection, not spam-foldering) in Wed; 2026
    FTC penalty adjustment check.
11. Validation the fix phase can bank: the week's three big *positions* — workflows-over-
    autonomous, hybrid retrieval + rerank, "long context doesn't kill RAG" (2026 consensus:
    retrieve 50–200K then long-context-reason; RAG framework usage grew ~400% 2024→2026) —
    all held. The refresh is factual, not conceptual.

## PERSONA VERDICTS

- **Karpathy**: The mechanism explanations (RRF math, CR preprocessing, pass^k vs pass@k) are
  right; the "6–8 tools then accuracy craters" number is folklore wearing a benchmark costume —
  source it or soften it.
- **Chip Huyen**: Every cost table silently assumes April pricing and the old tokenizer; the
  CR cost math even swaps Haiku generations mid-lesson — recompute all $/query and $/M-token
  figures against the July 2026 price sheet.
- **Jerry Liu**: Retrieval patterns are still right, but the reranker/embedder sections teach
  the September-2024 generation of a stack that has since shipped instruction-following
  rerankers and a new leaderboard top — and agentic retrieval is now framework-native, not a
  paper exercise.
- **Hamel Husain**: The week quotes my numbers correctly and then contradicts itself — 85% vs
  90% vs 95% agreement bars across three files, and a 2pp gate on an N=30 set the same lesson
  admits has ±9pp noise. Reconcile the thresholds and put a significance test in the gate.
- **Simon Willison**: MCP security guidance is about to be versioned-out by the 2026-07-28
  auth hardening, and the scariest numbers rest on one vendor's anti-MCP marketing post —
  re-source from primary incident reports.
- **Michael Seibel**: The pricing advice tells a solo operator to hold a $1–3K/mo floor in a
  market where Artisan just went $250/mo self-serve — either defend the premium explicitly or
  the advice is a way to lose deals.
- **Boris Cherny**: Every experiment pins legacy models ("Sonnet 4.6" build, "Opus 4.7"
  judge); a July reader in Claude Code gets better and cheaper results from current defaults —
  and the lesson still under-teaches tool_search_tool/programmatic tool calling for >6-tool
  scopes.
- **Cohort peer**: Readable and genuinely gripping (11x teardown, Nurture Boss), but I can't
  tell which numbers are still true — a "last-verified" stamp per table, not per file, would
  save me.
- **Mira Murati**: The lesson's model map ends one frontier generation ago — no Claude 5, no
  Gemini 3, no GPT-5.5; its picture of "frontier at $5/$25" understates frontier pricing 2×
  and misses that capability tiers now bifurcate (widely-released vs limited-release models).
- **swyx**: The stack the lesson teaches (raw SDK loop + MCP + maybe LangGraph) is a 2025
  stack; the 2026 AI engineer picks a harness first (Claude Agent SDK / OpenAI Agents SDK /
  Deep Agents) and drops to raw SDK only at the edges — the lesson never has that conversation.
- **Ethan Mollick**: Adoption claims lean on one vendor survey (Outreach) frozen at 2025;
  the hybrid-beats-autonomous conclusion is probably still right but a 2026 lesson should cite
  2026 adoption data, and the "22% full replacement" cohort's fate is now knowable — go look.
- **Lilian Weng**: The memory layer is still punted (acknowledged in Tue's own reviewer lens
  and never fixed per the April review's line-item); agent-memory has a 2025–26 literature now
  and "the CRM is the memory" is no longer a sufficient answer for research subagents.
- **Jeremy Howard**: The taxonomies (8 layers, 5 patterns, 3 grounding layers) mostly teach
  understanding, not ceremony — but the flashcards drill leaderboard trivia (BFCL percentages,
  MTEB ranks) that this review just proved perishable; drill the invariants, link the numbers.
