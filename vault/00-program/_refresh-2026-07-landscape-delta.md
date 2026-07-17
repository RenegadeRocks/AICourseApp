# LANDSCAPE DELTA — mid-April 2026 → 2026-07-17

Prepared for the AI Pro-level Course refresh. Course weeks were written 2026-04-14→18.
Every item: WHAT / WHEN / URL / AFFECTED WEEKS. All claims web-verified 2026-07-17.
Week codes: b0w0 model landscape/context economics; b0w1 prompting/RAG/vibe-coding; b0w2 MCP/voice/n8n; b0w3 business problems/pricing/case studies; b1w1 clients/selling; b1w2 branding/niche; b2w3 landing pages/codegen tools; b2w4 sales agent/RAG build/evals; b2w5 document understanding/report generation.

---

## 1. Frontier model releases & capability shifts

The course's model-landscape material is now **three Anthropic generations, two OpenAI generations, and one open-source generation stale**. Chronologically:

- **Claude Opus 4.7 (Anthropic)** — GA 2026-04-16. Improvement over Opus 4.6 on hard software-engineering tasks; pricing unchanged at $5/$25 per M tokens. Landed *during* the course-writing week, so some lessons may already predate it.
  - https://www.anthropic.com/news/claude-opus-4-7 ; https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/
  - Affects: b0w0, b0w1, b2w4 (any "current best model" or pricing claims)

- **GPT-5.5 (OpenAI)** — released 2026-04-23 (API 04-24, incl. GPT-5.5 Pro). First OpenAI model with a **1M-token API context window** (1,050,000 ctx / 128K output); $5/$30 per M. Uses significantly fewer tokens per Codex task.
  - https://openai.com/index/introducing-gpt-5-5/ ; https://developers.openai.com/api/docs/models/gpt-5.5
  - Affects: b0w0 (context economics tables), b2w3, b2w4

- **DeepSeek V4 Preview (V4-Pro, V4-Flash)** — 2026-04-24. This is the reasoning model DeepSeek actually shipped; **R2 remains unreleased** as of 2026-07-11 (widely-circulated "R2" specs are leaks). Course must not cite R2 as real.
  - https://api-docs.deepseek.com/news/news260424/ ; https://chat-deep.ai/guide/deepseek-roadmap-rumors/
  - Affects: b0w0

- **Gemini 3.5 Flash (Google)** — GA 2026-05-19 at I/O. $1.50/$9.00 per M, 1M context, ~4x output throughput vs comparable frontier models. **Gemini 3.5 Pro announced same day but still NOT shipped as of 2026-07-17** — base model scrapped and rebuilt; missed June, then July-17 target; specs (2M ctx, Deep Think) are third-party reports only. Teach the Flash reality, flag Pro as pending.
  - https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-june-2026/ ; https://www.techtimes.com/articles/320736/20260716/rebuilt-gemini-35-pro-misses-third-deadline-google-eyes-stopgap-release.htm
  - Affects: b0w0, b0w1

- **Claude Opus 4.8 (Anthropic)** — 2026-05-28. Same $5/$25 pricing; new **fast mode** (~2.5x speed, ~3x cheaper than prior fast pricing); defaults to high effort; ~4x less likely to let flaws in its own code pass unremarked; "dynamic workflows" research preview (hundreds of parallel subagents in Claude Code).
  - https://www.anthropic.com/news/claude-opus-4-8 ; https://simonwillison.net/2026/May/28/claude-opus-4-8/
  - Affects: b0w0, b0w1, b2w3, b2w4

- **Claude Fable 5 / Mythos 5 (Anthropic) — the headline event of the period.** Released 2026-06-09 as the first "Mythos-class" tier **above** Opus. SOTA on nearly all tested benchmarks. **1M-token context by default, 128K output, $10/$50 per M** (2x Opus 4.8). Fable 5 = safeguarded general release; Mythos 5 = fewer safeguards, restricted to "Project Glasswing" defensive-cyber partners. Days after launch it was **taken offline under a US government export directive**, then redeployed globally 2026-07-01 with new cybersecurity classifiers after export controls were lifted (announced 06-30). This governance episode (a frontier model suspended by the state, then re-released with classifiers) is itself course material.
  - https://www.anthropic.com/news/claude-fable-5-mythos-5 ; https://www.anthropic.com/news/redeploying-fable-5 ; https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/ ; https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html
  - Affects: b0w0 (new model tier + access model + context economics), b0w3 (governance/risk case study), b2w4

- **GPT-5.6 family: Sol / Terra / Luna (OpenAI)** — limited preview 2026-06-26 (gated behind a US-government safety review, mirroring the Fable 5 pattern), **GA 2026-07-09** across ChatGPT, Codex, and API. Sol = flagship (agentic coding, biology, cybersecurity gains); Terra ≈ GPT-5.5 performance at **2x cheaper**; Luna = lowest-cost tier.
  - https://openai.com/index/gpt-5-6/ ; https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html ; https://openai.com/index/previewing-gpt-5-6-sol/
  - Affects: b0w0, b2w3, b2w4

- **Claude Sonnet 5 (Anthropic)** — 2026-06-30. "Most agentic Sonnet"; near-Opus-4.8 performance; **intro pricing $2/$10 per M through 2026-08-31, then $3/$15**; default model on Free/Pro and in Claude Code with a 1M context window. Resets the cost floor for agent workloads — directly changes any per-call cost math in the build weeks.
  - https://www.anthropic.com/news/claude-sonnet-5 ; https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/
  - Affects: b0w0, b0w3 (pricing), b2w4, b2w5

- **Grok 4.5 (xAI, now branded SpaceXAI post-IPO)** — 2026-07-08; 1.5T-parameter coding-focused model Musk calls "Opus-class." **Grok 5 still unreleased** (slipped past Q1 and Q2 targets; now Q3+). xAI also shipped Grok Voice (06-04).
  - https://x.ai/news/grok-4-5 ; https://techcrunch.com/2026/07/08/spacexai-releases-grok-4-5-which-elon-describes-as-an-opus-class-model/ ; https://felloai.com/all-we-know-so-far-about-grok-5/
  - Affects: b0w0

- **Meta: Llama effectively retired; Muse Spark launched** — 2026-04-08, first major model from Meta Superintelligence Labs under Alexandr Wang; **proprietary/closed-source**, a strategic reversal from Llama's open-weights approach ("hope to open-source future versions"). Claims Llama-4-midsize capability at ~1 order of magnitude less training compute.
  - https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html ; https://venturebeat.com/technology/goodbye-llama-meta-launches-new-proprietary-ai-model-muse-spark-first-since
  - Affects: b0w0 (open-vs-closed narrative must flip: Meta closed, China open)

- **Kimi K3 (Moonshot AI)** — unveiled 2026-07-16/17, **2.8T-parameter open-source MoE, 1M context, multimodal** — largest open-weight model ever; full weights promised 2026-07-27. In LMArena blind testing developers preferred Kimi over Fable 5 and GPT-5.6 Sol for front-end coding; K3 outranked standard Opus 4.8 on text and tied Sol. The open-source frontier gap has effectively closed — from China.
  - https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html ; https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems ; https://www.axios.com/2026/07/16/moonshot-kimi-ai-china-model-openai-anthropic
  - Affects: b0w0, b0w3 (cost/sovereignty arguments), b2w4

- **Qwen 3.6 (Alibaba)** — current open-weight line; Qwen 3.6 Plus approaches Claude Opus 4.6 on agentic coding at much lower cost. (No "Qwen 4" exists — don't cite it.)
  - https://kingy.ai/news/best-open-weight-ai-models-in-2026-glm-5-2-vs-deepseek-v4-vs-kimi-k2-6-vs-qwen-vs-mistral/
  - Affects: b0w0

- **Thinking Machines Lab "Inkling"** — 2026-07-15, first model from Mira Murati's lab: **open-weight MoE, 975B total / ~41B active params, trained on 45T tokens of text+image+audio+video**, positioned as a base for customization via Tinker rather than a finished assistant. (Detail in §10.)
  - https://techcrunch.com/2026/07/15/thinking-machines-amps-up-its-bet-against-one-size-fits-all-ai-with-its-first-open-model-inkling/
  - Affects: b0w0, b1w2 (differentiation-by-customization thesis)

**Net capability/pricing shifts to reflect in b0w0:** 1M-token context is now table stakes at every major lab (Fable 5, Sonnet 5, GPT-5.5/5.6, Gemini 3.5 Flash, Kimi K3); a new super-tier exists above Opus (Mythos-class, 2x Opus pricing); the cheap-agentic tier collapsed in price (Sonnet 5 $2/$10 intro, Terra 2x cheaper than GPT-5.5, Luna, Gemini Flash $1.50/$9); and government sign-off before/after release became part of the frontier release process (Fable 5 suspension; GPT-5.6 gated preview).

---

## 2. Claude Code / coding-agent ecosystem & vibe-coding discourse

- **Claude Code defaults changed** — v2.1.197 (2026-06-30) made **Sonnet 5 the default with 1M-token context**; v2.1.198 (07-01) brought **Chrome integration out of beta**; week of 07-06/10 added an **in-app browser on Desktop**, `/doctor` setup checkup, `/fork` (conversation copies into background sessions; old in-session behavior is now `/subtask`), `/resume` session picker, MCP calls >2min auto-backgrounded, WebSearch session cap. Opus 4.8's "dynamic workflows" preview runs hundreds of parallel subagents in one session (2026-05-28). Any Claude Code screenshots/walkthroughs from April are visibly outdated.
  - https://code.claude.com/docs/en/whats-new ; https://www.anthropic.com/news/claude-opus-4-8
  - Affects: b0w1, b2w3, b2w4

- **Claude Cowork went cross-platform** — Anthropic's Claude-Code-style agent for general (non-coding) knowledge work, desktop-only since January, launched on **web + mobile 2026-07-07** for Max subscribers, with tasks continuing in the cloud even when devices are offline. Anthropic usage data: most Cowork users aren't coding. The "coding agent pattern generalizes to all knowledge work" story is now a shipped product.
  - https://techcrunch.com/2026/07/07/the-coding-agent-wars-are-spilling-into-the-rest-of-the-office-claude-cowork/ ; https://venturebeat.com/technology/anthropic-brings-claude-cowork-to-mobile-and-web-as-usage-data-shows-most-users-arent-coding
  - Affects: b0w1, b0w3, b2w5

- **Claude Agent SDK billing split announced, then paused** — a separate credit pool for programmatic (SDK) usage at API rates was to start 2026-06-15; Anthropic **paused it on 06-15** with no replacement announced. Relevant to anyone the course tells to build on subscription-backed agents.
  - https://devops.com/anthropic-hits-pause-on-claude-agent-sdk-billing-change-for-now/
  - Affects: b0w3 (pricing/unit economics), b2w4

- **Windsurf is dead as a brand → "Devin Desktop"** — Cognition retired the Windsurf name 2026-06-02, relaunching around an Agent Command Center and the open **Agent Client Protocol (ACP)**. Course references to "Windsurf" need renaming.
  - https://www.shareuhack.com/en/posts/cursor-vs-claude-code-vs-windsurf-2026 ; https://andrew.ooo/answers/cursor-3-7-vs-cursor-4-vs-windsurf-vs-claude-code-june-2026/
  - Affects: b0w1, b2w3

- **Cursor: multi-agent rework + acquired by SpaceX** — Cursor's 2026 releases center on multiple parallel agents and cloud agent environments (isolated repo copies). Then **SpaceX agreed to acquire Anysphere/Cursor for $60B all-stock on 2026-06-16** — largest startup acquisition ever (details §8).
  - https://thenewstack.io/claude-code-vs-cursor-vs-codex-vs-antigravity-2026/ ; https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html
  - Affects: b0w1, b2w3, b0w3

- **OpenAI Codex** — GPT-5.6 in Codex for Plus+ plans (2026-07-09); Codex now inside the ChatGPT desktop app (macOS/Windows); faster Computer Use.
  - https://openai.com/index/gpt-5-6/ ; https://developers.openai.com/codex/changelog
  - Affects: b0w1, b2w3

- **Cline shipped an open agent runtime** — `@cline/sdk` (Apache-2.0, TypeScript) released 2026-05-13; same runtime powers its VS Code extension, CLI, and Kanban surfaces; Cline CLI on claude-opus-4.7 scores 74.2% on Terminal Bench 2.0 (vs 69.4% Claude Code, same model); 30+ providers incl. local.
  - https://www.testingcatalog.com/cline-releases-open-source-agent-runtime-sdk-for-coding-agents/ ; https://github.com/cline/cline
  - Affects: b0w1, b2w3

- **Convergence + conventions** — Claude Code, Cursor, Codex, and Google Antigravity converged on one agentic-coding blueprint; **AGENTS.md** (repo-as-onboarding-guide) is read natively by Codex, Cursor, Copilot, Windsurf and sits under the Linux Foundation's Agentic AI Foundation alongside MCP (since Dec 2025).
  - https://thenewstack.io/claude-code-vs-cursor-vs-codex-vs-antigravity-2026/
  - Affects: b0w1, b2w3

- **Vibe-coding discourse hardened against "no-review" vibe coding** — mid-2026 consensus: vibe coding in Karpathy's original accept-without-review sense "is over as a legitimate professional strategy"; the premium skill is directing + evaluating AI output. Ammunition: Veracode found **45% of AI-generated code contains OWASP Top-10 vulnerabilities**; CodeRabbit found AI co-authored code has 1.7x more major issues and 2.74x more security vulnerabilities; the **Moltbook breach** (late Jan–early Feb 2026: agent-social-network DB fully exposed, millions of auth tokens) is the canonical cautionary tale; a Jan 2026 academic paper argues vibe coding is draining open-source maintainership.
  - https://thenewstack.io/vibe-coding-could-cause-catastrophic-explosions-in-2026/ ; https://kingy.ai/news/the-state-of-vibe-coding-2026/ ; https://digitalbiztalk.com/article/vibe-coding-is-killing-open-source-the-2026-developer-crisis
  - Affects: b0w1 (reframe vibe-coding lesson around review discipline), b2w3, b2w4 (evals as the answer)

---

## 3. MCP ecosystem

- **New spec revision: 2026-07-28 (RC locked 2026-05-21, final publishes 11 days after today).** Headline changes: **stateless protocol core** (horizontal server scaling; `.well-known` metadata for connection-less capability discovery), **Extensions framework**, **Tasks**, **MCP Apps**, **six SEPs hardening authorization** toward real-world OAuth 2.0/OIDC deployment, and a **formal deprecation policy** (SEP-2596: Active/Deprecated/Removed lifecycle). Course MCP content written against the 2025-11-25 spec needs a forward-pointer at minimum.
  - https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ ; https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ ; https://stacktr.ee/blog/mcp-2026-spec-changes
  - Affects: b0w2 (core), b2w4

- **Adoption milestones** — ~19,800+ servers indexed (Glama registry), ~97M monthly SDK downloads, backing from Anthropic, OpenAI, Google, Microsoft; MCP governed under the Linux Foundation's Agentic AI Foundation.
  - https://openclaw.direct/mcp-guide/model-context-protocol-news
  - Affects: b0w2

- **Security went from theoretical to measured.** Since April: **MCPTox** benchmark shows tool-poisoning succeeds broadly against real servers; arXiv 2603.22489 (2026) formal threat model of prompt injection via tool poisoning; **"Parasites in the Toolchain"** large-scale ecosystem attack study (370 servers / 1,062 tools exploitable for its parasite toolchain attack); MCP-ITP automated implicit tool-poisoning generation (Li et al., 2026); a 2026 disclosure found **up to ~200,000 exposed/vulnerable MCP instances** across IDEs, internal tools, and cloud services. Canonical attack taxonomy now: tool poisoning, rug pulls, tool shadowing, cross-server attacks, confused deputy/OAuth, and the "lethal trifecta" (private data + untrusted content + exfiltration channel).
  - https://arxiv.org/abs/2603.22489 ; https://arxiv.org/pdf/2509.06572 ; https://www.practical-devsecops.com/mcp-security-statistics-2026-report/ ; https://itecsonline.com/post/mcp-tool-poisoning-enterprise-ai-agent-security-2026
  - Affects: b0w2 (must add an MCP-security segment), b2w4 (agent hardening)

---

## 4. Agent tooling & frameworks

- **OpenAI killed AgentKit's visual builder** — 2026-06-03: Agent Builder and Evals products wind down, **EOL 2026-11-30**; migration path is the code-first **Agents SDK** (or Workspace Agents in ChatGPT); ChatKit survives. Any course mention of AgentKit/Agent Builder as a recommended path must be rewritten.
  - https://mcp.directory/blog/openai-agentkit-deprecation-2026 ; https://openai.com/index/the-next-evolution-of-the-agents-sdk/
  - Affects: b0w2, b2w4

- **OpenAI Agents SDK upgraded** — 2026-04-15: native sandbox execution + model-native harness for long-running agents; June 2026: **Lockdown Mode** against prompt-injection exfiltration for enterprise data.
  - https://techcrunch.com/2026/04/15/openai-updates-its-agents-sdk-to-help-enterprises-build-safer-more-capable-agents/ ; https://devops.com/openai-upgrades-its-agents-sdk-with-sandboxing-and-a-new-model-harness/
  - Affects: b2w4

- **LangChain/LangGraph 1.0** — GA since 2025-10-22 (pre-course, but stability commitment "no breaking changes until 2.0" holds through this period; `langgraph.prebuilt` deprecated into `langchain.agents`). Verify course code samples against 1.x idioms.
  - https://www.langchain.com/blog/langchain-langgraph-1dot0
  - Affects: b2w4

- **LlamaIndex Workflows 1.0** — standalone package/repo, latest release 2026-06-30; typed workflow state (Py+TS), event-driven steps as the recommended architecture; ACP integrations; OpenTelemetry/Arize observability.
  - https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems ; https://pypi.org/project/llama-index-workflows/
  - Affects: b2w4, b2w5

- **Anthropic Claude Agent SDK** — the library under Claude Code, exposed for custom agents; June-July: subagent text streaming, background-agent improvements, Admin API beta for Enterprise orgs; billing-split pause (see §2).
  - https://code.claude.com/docs/en/agent-sdk/overview ; https://releasebot.io/updates/anthropic/claude-code
  - Affects: b2w4

- **n8n: SAP strategic investment at $5.2B valuation** — 2026-05-12 (up from $2.5B in Oct 2025); multi-year deal embedding n8n into SAP Joule Studio; 1,400+ enterprise customers, 1.7M monthly active builders. Product: **n8n 2.0** with native AI Agent nodes, MCP support, multi-agent orchestration and RAG out of the box; June 2026 execution-replay debugging engine.
  - https://www.bloomberg.com/news/articles/2026-05-12/sap-invests-in-ai-automation-startup-n8n-at-5-2-billion-value ; https://blog.n8n.io/series-c/ ; https://nodesify.com/blog/n8n-workflow-automation-guide-2026
  - Affects: b0w2 (n8n lessons), b0w3, b1w1 (enterprise credibility of the stack)

- **Make.com AI Agents (New) GA** — 2026-02-11: production agents on every plan, built/debugged on the same canvas as scenarios; credit-based pricing (~43-50 credits per agent run on built-in Small model; BYO OpenAI/Anthropic keys).
  - https://www.make.com/en/blog/announcing-next-generation-make-ai-agents ; https://www.lindy.ai/blog/make-com-pricing
  - Affects: b0w2, b0w3

---

## 5. Voice stack

- **OpenAI Realtime: two model generations since April.** 2026-05-07: **GPT-Realtime-2** (first realtime voice model with GPT-5-class reasoning), **GPT-Realtime-Translate**, **GPT-Realtime-Whisper**. 2026-05-12: legacy Realtime API **Beta removed** (migration required — breaks old course code). 2026-07-06/07: **GPT-Realtime-2.1 and 2.1-mini** (reasoning + tool use at mini price), plus **≥25% p95 latency reduction** across Realtime voice models via caching.
  - https://openai.com/index/introducing-gpt-realtime/ ; https://www.marktechpost.com/2026/07/06/openai-gpt-realtime-2-1-mini-reasoning-realtime-api/ ; https://developers.openai.com/api/docs/changelog ; https://www.ghacks.net/2026/05/11/openai-releases-three-new-realtime-voice-models-for-the-api-with-gpt-5-class-reasoning/
  - Affects: b0w2 (voice), b2w4 (sales agent)

- **ElevenLabs: $500M Series D at $11B** — 2026-02-04, led by Sequoia; eyeing IPO; pushing "Agents" (talk, type, take action) beyond TTS. ElevenLabs Agents run ~$0.08–$0.12/min all-inclusive.
  - https://elevenlabs.io/blog/series-d ; https://www.cnbc.com/2026/02/04/nvidia-backed-ai-startup-elevenlabs-11-billion-valuation.html
  - Affects: b0w2, b0w3

- **Mid-2026 per-minute economics (verify against any April numbers in the vault):** VAPI $0.05/min platform fee, **real all-in $0.15–$0.36/min** once LLM/TTS/STT/telephony are added; Retell $0.07/min base, ~620ms measured latency, HIPAA included, typical all-in $0.13–$0.31/min; ElevenLabs $0.08–$0.24/min bundled. Positioning consensus: Retell for production business agents, VAPI for full-stack control, ElevenLabs when voice quality is the product.
  - https://devaland.com/blog/voice-ai-pricing-comparison-2025 ; https://www.cekura.ai/blogs/retell-ai-pricing-per-minute ; https://www.digitalapplied.com/blog/voice-ai-agents-business-elevenlabs-vapi-retell-bland
  - Affects: b0w2, b0w3 (pricing case studies)

- **xAI Grok Voice** — 2026-06-04, new consumer voice entrant.
  - https://felloai.com/all-we-know-so-far-about-grok-5/
  - Affects: b0w2 (minor)

---

## 6. UI-gen / app-gen tools

- **Cursor → SpaceX ($60B, 2026-06-16)** — see §8; changes the "independent startup" framing in codegen-tool lessons.
- **Lovable** — $400M ARR (Feb 2026), **$6.6B valuation after a $330M Series B**; pricing now Free ($5 credits/mo) / Team $30/user / Business $100/user; whole-team credit pooling is its wedge vs Bolt's per-user unshared tokens.
  - https://www.vibecodingacademy.ai/blog/lovable-vs-bolt-vs-replit-comparison-2026 ; https://altar.io/lovable-vs-bolt-vs-v0-vs-replit-vs-base44/
  - Affects: b2w3, b0w3
- **Replit Agent 4** — launched March 2026: long autonomous builds, auth + database management, real-time shipping; agent "intelligence" now scales by plan tier.
  - https://www.news.aakashg.com/p/ai-prototyping-tools-2026
  - Affects: b2w3
- **Bolt** — Pro $25/mo, Teams $30/user/mo; no death/pivot found — still an active independent player.
  - https://www.vibecodingacademy.ai/blog/lovable-vs-bolt-vs-replit-comparison-2026
  - Affects: b2w3
- **v0 (Vercel)** — moved to **model-tier token pricing** (v0 Mini/Pro/Max/Max Fast with input/cache/output rates) rather than flat plans; positions v0 as a model+API, not just an app.
  - https://wz-it.com/en/blog/lovable-vs-bolt-vs-v0-comparison-2026/
  - Affects: b2w3
- **Figma Make matured into a suite** — Figma AI now spans Agent (ideation), Weave (asset gen), Make (apps), Dev Mode/Code Layers; Make is **multi-model (choose latest Claude/Gemini/GPT)**, supports MCP connections to external tools, uses your design files + team libraries as generation context, and allows code export on paid Full seats.
  - https://www.banani.co/blog/figma-ai-features-review ; https://blog.logrocket.com/ux-design/figma-ai-2026-quick-overview/
  - Affects: b2w3
- **No major deaths** in this category April→July; the consolidation story is acquisition (Cursor) and enterprise pivots, not shutdowns.

---

## 7. RAG / retrieval

- **The "RAG is dead" debate resolved into "naive RAG is dead; retrieval lives inside agents."** Mid-2026 consensus architecture: **agentic RAG** — retrieval as a multi-step decision process the agent controls, not a fixed retrieve-then-generate pipeline. Hybrid pattern now taught widely: long context for conversation history, RAG for precision + citations, GraphRAG/agentic workflows for complex analysis, web-search-augmented (CRAG-style) for freshness.
  - https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/ ; https://lighton.ai/lighton-blogs/rag-is-dead-long-live-rag-retrieval-in-the-age-of-agents ; https://commandcode.ai/guides/rag-in-2026
  - Affects: b0w1, b2w4, b2w5

- **Economics argument sharpened by 1M-context ubiquity:** RAG measured **8–82x cheaper** than long-context stuffing for typical workloads, with better latency; long-context evaluation studies (e.g., "Long Context vs. RAG for LLMs: An Evaluation and Revisits", arXiv 2501.01880) show RAG winning below ~32K effective context and retrieval-reordering methods (OP-RAG chunk-order preservation, retrieval reordering) closing long-context gaps. With Sonnet 5/Fable 5/GPT-5.5 all at 1M tokens, the course's context-economics math (b0w0) and the RAG-build week (b2w4) both need the "you *can* stuff it, but should you pay for it" framing updated with 2026 prices.
  - https://arxiv.org/pdf/2501.01880 ; https://open-techstack.com/blog/rag-vs-long-context-2026/
  - Affects: b0w0, b0w1, b2w4

- **Taxonomy expansion** — surveys now catalogue ~20 named RAG variants (agentic, graph, corrective, self-reflective, etc.); useful map for the b2w4 build week.
  - https://www.turingpost.com/p/ragtypes
  - Affects: b2w4, b2w5

---

## 8. Business / market

- **Record capital concentration** — Global VC hit **$510B in H1 2026** (more than all of 2025); **OpenAI + Anthropic alone took $217B = 43% of all H1 startup funding**. Anthropic raised a **$65B Series H at a $965B post-money valuation** (May 2026, Altimeter/Dragoneer/Greenoaks/Sequoia).
  - https://news.crunchbase.com/venture/global-startup-exits-ipo-ma-soar-ai-q2-h1-2026/ ; https://news.crunchbase.com/venture/na-startup-funding-ma-shattered-records-ai-q2-2026/
  - Affects: b0w0, b0w3, b1w1

- **SpaceX: largest IPO ever + largest startup acquisition ever, in one week.** IPO 2026-06-12 at $135/share raising $75B ($86.2B with greenshoe), valuing SpaceX at $1.77T; 2026-06-16 announced **$60B all-stock acquisition of Anysphere (Cursor)** (~15x revenue; option signed 2026-04-21 with ~$10B walk-away fee); stock closed $192.46 that day, total value past $2.7T. xAI/Grok now ships under "SpaceXAI."
  - https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html ; https://www.forbes.com/sites/sandycarter/2026/06/16/spacex-buys-cursor-in-largest-startup-acquisition-ever-at-60-billion/
  - Affects: b0w0, b0w3, b2w3

- **Consolidation is running through talent deals and tech licenses**, not press-release M&A — four lab acquisitions in five days in May 2026; Cerebras raised $5.6B in its May IPO.
  - https://www.startuphub.ai/ai-news/ai-news/2026/four-labs-four-acquisitions-ai-consolidation-may-2026 ; https://news.crunchbase.com/venture/global-startup-exits-ipo-ma-soar-ai-q2-h1-2026/
  - Affects: b0w3, b1w1

- **Adoption stats for course slides (2026 vintages):** 91% of businesses use AI somewhere; **31% of enterprises have ≥1 agent in production** (banking/insurance lead at 47%); ~2/3 still in pilot mode; **88% of agent pilots never reach production** (Anaconda/Forrester); 79% report adoption challenges; IDC/Microsoft measure 3.7x avg return per $1 while IBM finds only 25% of initiatives hit expected ROI. Gartner-style projection: 40% of enterprise apps embed task-specific agents by end-2026 (vs <5% in 2025).
  - https://prefactor.tech/learn/ai-agent-adoption-statistics ; https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points ; https://writer.com/blog/enterprise-ai-adoption-2026/
  - Affects: b0w3, b1w1

- **Agency/services market shifted to outcomes** — **56.8% of agencies selling or moving to outcome-based engagements** (per a 250-agency 2026 survey); buyer demand moved from "help us try AI" to "automate a real process with clear ROI"; AI automation pricing fell ~35% from 2024→2026 as open models matured. Directly updates the course's pricing-models and selling weeks.
  - https://www.digitalapplied.com/blog/agentic-ai-adoption-survey-2026-250-agencies ; https://wazobia.tech/blog/ai-and-automation-trends-2026
  - Affects: b0w3, b1w1, b1w2

- **Regulation — EU AI Act hits full applicability 16 days after today:** 2026-08-02 = high-risk obligations + Commission GPAI enforcement powers (with fines) enter application. The **"AI omnibus"/Digital Package** (political agreement 2026-05-07) extends the transition for high-risk AI embedded in regulated products to 2028-08-02 and simplifies implementation — course compliance content must reflect both the deadline and the softening.
  - https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai ; https://artificialintelligenceact.eu/implementation-timeline/ ; https://www.legiscope.com/blog/eu-ai-act-timeline-deadlines.html
  - Affects: b0w3, b1w1, b2w5

- **Litigation** — NYT-led consolidated case vs OpenAI (16 suits, SDNY MDL): Jan 2026 order compels production of the full 20M ChatGPT-log sample; **2026-07-09 plaintiffs moved to sanction OpenAI** for allegedly lying about its ability to search its models for copyrighted material. Plus the Fable 5 export-control suspension (§1) as the first state-ordered takedown of a frontier model.
  - https://www.washingtonpost.com/business/2026/07/09/openai-new-york-times-ai-copyright-lawsuit/1f749fa0-7ba4-11f1-b194-f872dd4ec5aa_story.html ; https://natlawreview.com/article/openai-loses-privacy-gambit-20-million-chatgpt-logs-likely-headed-copyright
  - Affects: b0w3, b2w5 (provenance/citation hygiene)

---

## 9. Notable papers & research (April→July 2026)

- **METR time-horizon program** — 50%-time-horizon doubling every ~4.3 months post-2023; Claude Opus 4.6 tops the public chart at **14h30m** (Feb 2026); **May 2026: Claude Mythos Preview added, with METR noting measurements above 16 hrs are unreliable on the current task suite** — i.e., the frontier outgrew the yardstick during the course-writing window. Cite metr.org/time-horizons as the living reference.
  - https://metr.org/time-horizons/ ; https://metr.org/blog/2026-1-29-time-horizon-1-1/
  - Affects: b0w0, b2w4

- **Anthropic: Natural Language Autoencoders (NLA)** — interpretability system where one Claude copy verbalizes another's activations and a second reconstructs them; **training code open-sourced 2026-05-07**. Strong teachable artifact for "can we see inside the model."
  - https://www.buildfastwithai.com/blogs/anthropic-claude-nla-interpretability-2026 ; https://www.anthropic.com/research
  - Affects: b0w0

- **Anthropic: "Teaching Claude Why"** — training interventions that took agentic-misalignment behaviors (incl. blackmail scenarios) from near-universal to zero since Haiku 4.5, using ~3M tokens of constitutional documents + synthetic stories; generalized beyond the training scenarios.
  - https://www.buildfastwithai.com/blogs/anthropic-claude-nla-interpretability-2026 (secondary) ; https://www.anthropic.com/research/team/alignment
  - Affects: b0w0, b2w4 (why evals/alignment matter to builders)

- **MCP security literature (see §3):** arXiv 2603.22489 (threat modeling tool poisoning), "Parasites in the Toolchain" (arXiv 2509.06572), MCPTox benchmark, MCPXKIT (arXiv 2508.12538). Affects b0w2.

- **Karpathy's autoresearch** (March 2026) — ~630-line harness letting agents run their own ML experiments; a 2-day run found ~20 improvements cutting nanochat's time-to-GPT-2 by ~11%. Plus nanochat's documented **~$73 / 3-hour GPT-2-class training run** (Jan 2026) — the best available "train an LLM yourself" cost anchor.
  - https://blockchain.news/ainews/karpathy-s-autoresearch-boosts-nanochat-training-11-faster-time-to-gpt-2-benchmark-analysis-and-business-implications ; https://www.startuphub.ai/ai-news/ai-figures/2026/figure-andrej-karpathy-nano-series-technical-contribution-2026-07-16
  - Affects: b0w0, b0w1

- **AI-code-quality evidence base** — Veracode (45% of AI code has OWASP Top-10 vulns), CodeRabbit (1.7x major issues, 2.74x security vulns), and the Jan 2026 "vibe coding is killing open source" paper (§2). Affects b0w1, b2w3.

- **Agent-research trendline (May–Jun 2026 arXiv):** cost-aware agent architecture (context/hierarchy/reasoning depth as budgeted choices), memory-in-the-loop retrieval as working memory (arXiv 2607.05690), long-horizon planning paradigms (MAP, arXiv 2605.13037), dynamic multi-agent topologies (DyTopo). VoltAgent's curated 2026 agent-papers list is a good ongoing source: https://github.com/VoltAgent/awesome-ai-agent-papers
  - Affects: b2w4, b2w5

---

## 10. Reviewer roster: Murati verification + proposed additions

**Mira Murati — verified as of 2026-07-17.** Founder/CEO of **Thinking Machines Lab** (founded after leaving OpenAI as CTO). What the lab has actually shipped:
- **Tinker** — its revenue-generating fine-tuning/customization platform; customers include Bridgewater Associates (financial-task tuning).
- **Inkling** — first in-house model, released **2026-07-15**: open-weight MoE, 975B total / ~41B active parameters, trained on 45T tokens spanning text/image/audio/video with native cross-modal reasoning; explicitly positioned as a *starting point for customization via Tinker*, a bet against one-size-fits-all frontier assistants.
- Her authentic lens for lesson review: **"customization beats generality"** — open weights + fine-tuning as the differentiation path for practitioners, which maps cleanly onto b1w2 (niche/differentiation) and b2w4/b2w5 (tuned components vs prompted generalists). Do not portray her as an OpenAI executive or a closed-model maximalist.
  - https://techcrunch.com/2026/07/15/thinking-machines-amps-up-its-bet-against-one-size-fits-all-ai-with-its-first-open-model-inkling/ ; https://fortune.com/2026/07/15/what-is-mira-murati-thinking-machines-first-ai-model-inkling/ ; https://www.axios.com/2026/07/15/mira-murati-thinking-machines-open-weight-model-inkling

**Proposed additions (2–3, all verified current):**

1. **Andrej Karpathy — now on Anthropic's pretraining team (joined May 2026),** after nanochat (~$73 GPT-2-class run) and autoresearch (agents improving their own training). Highest-signal persona for: what models actually learn, cost-of-training intuition, and the *original* definition of vibe coding — he can police the course's vibe-coding framing from the source. Lens weeks: b0w0, b0w1, b2w3.
   - https://www.startuphub.ai/ai-news/ai-figures/2026/figure-andrej-karpathy-anthropic-pretraining-2026-05-31 ; https://felloai.com/who-is-andrej-karpathy/

2. **Simon Willison — independent researcher/blogger, actively publishing through the period** (e.g., Opus 4.8 review 2026-05-28) and originator of the **"lethal trifecta"** prompt-injection framing that now anchors MCP security discourse. Ideal skeptical-practitioner lens for b0w2 (MCP security), b0w1 (tool claims vs reality), b2w4 (evals).
   - https://simonwillison.net/2026/May/28/claude-opus-4-8/ ; https://www.practical-devsecops.com/mcp-security-vulnerabilities/

3. **Yang Zhilin (Moonshot AI founder/CEO) — or a composite "open-weights frontier" lens.** With Kimi K3 (2.8T-param open-weight, 1M ctx, beats/ties US flagships in Arena front-end coding) landing 2026-07-16/17 and weights due 07-27, the course needs a reviewer voice that pressure-tests every "use the closed API" recommendation against the now-real open frontier: cost, sovereignty, EU-compliance, and agency-margin implications. Lens weeks: b0w0, b0w3, b2w4.
   - https://www.cnbc.com/2026/07/17/moonshot-ai-kimi-k3-model-openai-anthropic-china.html ; https://www.axios.com/2026/07/16/moonshot-kimi-ai-china-model-openai-anthropic

---

## Verification caveats (things NOT to teach as fact)
- Gemini 3.5 Pro: **unreleased** as of 2026-07-17 (missed its July-17 target; all specs third-party). — https://www.techtimes.com/articles/320736/20260716/rebuilt-gemini-35-pro-misses-third-deadline-google-eyes-stopgap-release.htm
- Grok 5: unreleased; 6T-param specs are speculation. — https://felloai.com/all-we-know-so-far-about-grok-5/
- DeepSeek R2: unreleased; circulating benchmarks are leaks. — https://chat-deep.ai/guide/deepseek-roadmap-rumors/
- Kimi K3 weights: announced for 2026-07-27, not yet downloadable today.
- MCP 2026-07-28 spec: RC only until it publishes on 07-28.
- Sonnet 5 pricing: intro rate ends 2026-08-31 ($2/$10 → $3/$15) — date-stamp any pricing tables.
