---
type: lesson
block: block-2-ai-employees
week: week-05
day_of_cycle: 3
day_name: wed
session_slug: ai-that-reads-your-business-reports-insights
date_due: 2026-06-17
tags:
  - data-connectivity
  - mcp
  - governance
  - read-only-tokens
  - pii-masking
  - row-level-security
  - soc2
  - ai-analyst-worker
  - langchain-document-loaders
  - llamahub
  - ipaas
  - gdpr
sources:
  - anthropic-mcp-announcement-2024-11-25
  - modelcontextprotocol-spec-2025
  - mcp-servers-github-repo
  - langchain-document-loaders-docs
  - llamahub-registry
  - motherduck-prompt-sql-docs
  - presidio-microsoft-github
  - simonwillison-mcp-prompt-injection-2025-04
  - edpb-opinion-28-2024-ai-models
  - pci-dss-v4-0-1-pcisec
  - hhs-hti-1-final-rule-2024
  - ramp-intelligence-announcement
  - postgresql-rls-docs-18
last_verified: 2026-04-17
word_count_target: 6000
---

# Data connectivity for AI analyst workers — MCP servers, read-only tokens, the governance layer, and why most deployments skip this and die in production

## Why this matters

Most AI analyst workers that get demoed on a Tuesday never ship to a Monday. They die in the gap between "Claude can read the ledger when I paste it into the chat" and "Claude can read the ledger every week, on a schedule, without a human in the loop, without a PII incident, and without tripping the SOC 2 audit in six months." That gap is not an LLM problem. It is a data-connectivity and governance problem, and it is the single most underestimated layer of the report-generator stack.

After this lesson, three things should be true of you that are not true of a sharp generalist:

1. You can pick between MCP servers, first-party SDK integrations, LangChain/LlamaHub loaders, and iPaaS connectors for a specific data source — and defend the pick on cost, speed-to-ship, and governance surface.
2. You can sketch the read-only, row-level-secured, PII-masked, audit-logged access path for an LLM touching customer data tables, and you know which controls are day-1 must-haves versus which can land in month 3.
3. You know the three most common governance breakdowns that kill production AI-analyst builds — prompt-injection via tool responses (the Willison "lethal trifecta"), silent MCP-tool redefinition ("rug pulls"), and over-broad service-account scopes — and the architectural fix for each.

If you have not read Tuesday's lesson on document understanding, the parsing layer here assumes you know how Claude Vision, LlamaParse, and Unstructured differ. If you have not done Week 4 on RAG and agent architectures, the tool-calling loop referenced in the experiment assumes that scaffolding.

## Prerequisites

- Working knowledge of OAuth2 client-credentials flow and service-account patterns (Block 0 Week 2 touched this; if it is hazy, spend 20 minutes on the Google Cloud IAM overview before continuing).
- A Postgres or BigQuery instance you can hit with read-only credentials, even if it's a local Docker container.
- Claude Code installed with at least one MCP server configured from a previous week — the reference Postgres or Filesystem server is fine.

If more than two of those are missing, do the Monday and Tuesday lessons first, then come back.

## Layer 1 — The data-source taxonomy and why it dictates your connector choice

A weekly report generator is a function of its inputs. Before you pick a connection technology, you have to classify the source, because the classification — not the vendor's marketing — determines which connector wins. Five classes, each with a different failure profile.

**OLTP (transactional databases).** Postgres, MySQL, SQL Server, MongoDB. The live application database. Data is fresh (sub-second lag), schema is normalized, and you are almost never supposed to hit it with analytical queries because a full table scan of the `orders` table at 9am will slow the checkout flow. The governance sensitivity is high: this is where customer PII, payment tokens, and auth material live. Connector pattern: **read replica or logical replica, never the primary**, and the LLM hits the replica through a narrow view or materialized query layer.

**OLAP (warehouses).** BigQuery, Snowflake, Redshift, Databricks, Motherduck. Built for analytical queries; columnar storage; batch-lag usually 5 min to 24 hr. This is the right home for an AI analyst worker because the compute model matches. Governance in 2026 looks like: warehouse-native row-level security, column masking policies, query tagging for audit, and service accounts scoped to a single dataset. Snowflake's dynamic data masking and BigQuery's column-level access control are now table stakes.

**SaaS APIs.** Stripe, QuickBooks, HubSpot, Salesforce, Segment, Google Analytics 4, Zendesk, Jira. Each has its own SDK, its own auth model (API key, OAuth, per-tenant tokens), its own rate limits, and its own quirks (Salesforce's SOQL is not SQL; HubSpot's list API paginates in a way that has broken every ETL pipeline shipped before 2023). Read-only is almost always an option in the auth layer — use it.

**Spreadsheets and semi-structured.** Google Sheets, Excel 365, Airtable, Notion databases. Dangerous not because the data is big but because the schema is implicit. A human changed column C from "Revenue" to "Revenue (USD)" last Thursday and your extraction broke silently for three weekly runs before anyone noticed. Connector pattern: pin to cell ranges with named ranges, schema-validate every read, fail loudly.

**File-based.** S3, R2, Azure Blob, GCS, Dropbox, SharePoint. PDFs, CSVs, Parquet files, zipped monthly exports. Tuesday's document-understanding stack sits on top of these; the connectivity question is just "how does the AI worker enumerate new files on a schedule and authenticate to download them." Event-driven (S3 notifications → queue) is the 2026 default for anything latency-sensitive; poll-based is fine for weekly.

The classification matters because a single report often pulls from four of these classes in one run. A weekly sales-ops report for a mid-market SaaS might hit: Postgres replica for order-line data, Stripe for revenue-recognition cross-check, HubSpot for deal-stage transitions, a Google Sheet for manual territory annotations, and S3 for the finance team's month-end PDF journal entries. Five sources, five connector shapes, five places governance has to be consistent.

## Layer 2 — The four connector layers — MCP vs SDK vs LangChain loaders vs iPaaS

Every AI analyst worker picks one of four strategies per source, sometimes mixed. The choice is not religious; it is a function of team size, governance maturity, and how production-critical the data path is.

### MCP servers

Anthropic released the Model Context Protocol on November 25, 2024, as an open specification for how AI clients (Claude Desktop, Claude Code, Cursor, Zed, Replit) discover and invoke tools exposed by servers.[^1] The reference implementations at launch included servers for Google Drive, Slack, GitHub, Git, Postgres, and Puppeteer, with Block and Apollo cited as initial enterprise adopters.[^2] By late 2025, the community repo at `github.com/modelcontextprotocol/servers` plus third-party registries (Glama, Smithery, mcp.run) had accumulated several thousand servers, most of them thin wrappers around a SaaS REST API or a local database driver.[^3]

The *mechanical* win of MCP is that a single Claude Code session can discover and invoke tools across Postgres, Stripe, HubSpot, and S3 without any of those integrations being hand-coded into the orchestrator. Tools expose a JSON schema for inputs and a typed return shape; the LLM sees them the same way it sees any other tool call; auth is pushed down into the MCP server, so the LLM never touches the Stripe secret key directly.

The *governance* win is that tools live outside the agent binary. Your security team can version and audit the Stripe MCP server independently of the agent code that calls it.[^4] When the auditor asks "what can this agent do against our Stripe account," you hand them the server's `tools/list` output and the OAuth scope it holds, and the answer is exact rather than "whatever Claude decides to call." That separation of concerns is the feature the analogous LangChain-loader model cannot cleanly offer.

The honest counter is that MCP is one year old. Simon Willison published a detailed breakdown in April 2025 of prompt-injection risks in MCP tool responses — a malicious email body returned by a Gmail MCP tool can contain instructions the LLM then executes — and the "rug pull" class of attacks where an MCP server silently mutates its tool definitions after a user has approved them.[^5] Willison coined "the lethal trifecta" (access to private data, exposure to untrusted content, ability to communicate externally) as the condition under which an MCP-equipped agent is exploitable. The mitigations exist (gateways, signed tool manifests, diff-on-change alerts) but they are not uniformly adopted.

### First-party SDKs

The Anthropic Python SDK, the OpenAI SDK, or vendor-specific libraries like `stripe-python`, `hubspot-api-client`, `snowflake-connector-python`. The pattern is: you handwrite a function that hits the API, you wrap it as a Claude tool definition, the LLM calls the tool, the function returns JSON.

Wins: fast to ship for a single integration, zero protocol overhead, full control of error handling, and the auth model is whatever the SDK natively supports. For a solo operator with one Stripe account, one Postgres DB, and one HubSpot, wiring three SDK tools into Claude Code takes an afternoon. Losses: you now maintain those integrations forever. Stripe deprecated a pagination parameter in Feb 2025; if your integration hard-coded it, you find out on the Monday the report breaks.

### LangChain Document Loaders and LlamaHub

LangChain's Document Loaders library (hundreds of community loaders: `PyPDFLoader`, `NotionDBLoader`, `GoogleDriveLoader`, `ConfluenceLoader`) and LlamaIndex's LlamaHub registry (a curated directory of LlamaIndex-compatible readers) predate MCP and solved the same problem at a different layer. A loader takes a configuration (URL, auth), returns a list of `Document` objects (text plus metadata), and plugs into a retrieval pipeline. For pure read-for-context (dump a Confluence space into a RAG index), loaders are still excellent. For interactive tool-use where the agent needs to issue a parameterized query at inference time, they feel under-specified next to MCP.

The 2026 consensus among practitioners — see Harrison Chase's own position on LangChain's MCP adapter — is that loaders and MCP are complementary: loaders for one-shot batch ingestion into a vector index, MCP for runtime tool invocation.[^6] New builds tend to lean MCP.

### iPaaS (n8n, Make, Zapier, Workato, Tray.io)

Visual workflow tools. Non-coders build a pipeline by dragging Stripe → Transform → Postgres → Slack. In 2024-2025 these tools all bolted on "AI" blocks: call OpenAI or Claude with a prompt inside the workflow, capture the output, route it. For a small team where the bottleneck is not code but integration plumbing (OAuth dances, webhook endpoints, retry logic), iPaaS can get a v1 report generator live in a day.

The tradeoff is opacity. Debugging an n8n workflow that pulls the wrong column from HubSpot because the node configuration hid the problem is slower than debugging an SDK call where the code is in front of you. For enterprise-grade governance (field-level lineage, SOC 2 evidence, write-path gating), iPaaS is thinner than purpose-built tooling. Zapier's 2024 enterprise tier added audit logging and SSO; Workato has been enterprise-native longer; n8n's self-hosted story makes it attractive for EU-data-residency use cases. Pick iPaaS when speed-to-ship dominates and governance is "we'll add it later." Do not pick iPaaS when speed-to-audit dominates.

### The decision table

For a solo operator or two-person team shipping a first AI-analyst worker in 30 days:

| Source class | First pick | Second pick | Avoid |
|---|---|---|---|
| OLTP (Postgres replica) | MCP Postgres reference server | SDK + hand-written tool | iPaaS (too opaque for SQL) |
| OLAP (BigQuery, Snowflake) | Native SDK with read-only service account | Motherduck MCP for natural-language SQL | iPaaS (cost + opacity) |
| SaaS API with official MCP | Community MCP server, audited | Vendor SDK | Zapier (unless already in use) |
| SaaS API without MCP | Vendor SDK | LangChain loader if read-only batch | — |
| Spreadsheet | Google Sheets MCP or SDK | iPaaS node | Unstructured loader (schema drift) |
| File-based (S3/GDrive) | MCP filesystem / GDrive server | Boto3 + tool wrapper | — |

For a 10-200 person team with a platform team, the second pick often wins on day one: SDK-first gives you full control of retries, rate-limits, and error reporting; MCP becomes the interface layer you expose to the agent once the SDK is battle-tested. For enterprise (>200) the governance question flips — you want everything behind a gateway (MCP gateway, or internal service mesh) with centralized auth, and the choice of "MCP vs SDK" is mostly about which team owns the tool.

## Layer 3 — The read-path / write-path distinction and the governance layer

Every AI analyst worker starts as read-only. Some graduate to write. The graduation is where incidents happen.

### Read-path first

The default posture for a report generator is: the agent reads data, computes, drafts narrative, ships a document. It does not post to Slack channels, send email, update CRM records, or commit to the ledger. Every action it takes is reversible, because the only artifact is the report itself — a draft a human reviews before any downstream change.

Read-path sounds safe. In 2026 the thing that kills read-path deployments is over-broad scopes. A Postgres service account provisioned with `CONNECT` plus `SELECT` on the whole `public` schema can read the `users` table, the `payment_methods` table, the `internal_notes` table, and the row containing the CEO's home address that someone dumped in as a test fixture three years ago. The LLM now has implicit access to every column. When the LLM is asked to "show me top customers by revenue," it might obligingly join `orders` to `users` and leak `users.email_hash_salt` into the chain-of-thought which ends up in a Braintrust trace which ends up in your observability vendor's S3 bucket.

The architectural fix, in order of sophistication:

1. **Narrow the scope at the database level.** Create `report_agent_ro` with `SELECT` on a curated set of views, not base tables. Views hide columns the agent has no business seeing — `user_id` stays, `ssn_encrypted` is not projected. This is cheap (one SQL script) and it is the single highest-leverage control.
2. **Row-level security (RLS).** Postgres has had RLS since 9.5; the docs in the current version describe policies that restrict visibility per session role.[^7] For multi-tenant AI-analyst tools where one deployment serves multiple customers, RLS is how you prevent a prompt-injected agent from reading customer B's data when it's logged in for customer A. The standard pattern: every tenant-scoped table has a `tenant_id` column, policies `USING (tenant_id = current_setting('app.tenant_id')::int)`, and the MCP server sets `app.tenant_id` via `SET LOCAL` at the start of every session.[^8] Snowflake and BigQuery have equivalent primitives (row access policies, authorized views with session variables).
3. **Column masking / PII redaction at the connector layer.** Microsoft Presidio is the open-source de-facto here; it provides Analyzer and Anonymizer engines that identify entities (names, SSNs, credit cards, custom patterns) via NER and regex and either redact, hash, or replace them before the text reaches the LLM.[^9] The integration pattern: the MCP or SDK layer pulls the data, pipes it through Presidio's Anonymizer with a policy, and only the masked version enters the prompt. LiteLLM has a first-class Presidio integration; LangGraph has community patterns for Presidio-in-the-middle.[^10] The tradeoff is latency (tens of ms per document on CPU) and recall (Presidio will miss novel PII patterns; tune it to your domain).
4. **Audit logging.** Every tool call the agent makes — query, parameters, rows returned (counts, not content), timestamp, session ID — flows to an append-only log. At a minimum, warehouse query tags plus Claude Code's own trace log. At enterprise scale, a dedicated observability vendor (Braintrust, Langfuse, Arize) that stores the full trace with redaction applied.

### Write-path is explicit

There are legitimate reasons for an AI analyst worker to write: posting the final report to a Confluence page, emailing the PDF to a stakeholder list, updating a status row in a `reports_ledger` table for idempotency. Each of these should have an explicit human or system gate.

Ramp's public posture in their 2024-2025 product announcements is instructive: their policy-enforcement agents auto-approve only low-risk spend and route everything else to human judgment; their AP agents produce coded line items that still land in an approval queue before cash moves.[^11] The pattern is the same for analyst workers — writes are scoped, logged, and gated.

Barry McCardel of Hex has a sharper position, public on the Hex blog and in podcasts: "AI without analysts produces confidently-wrong reports at rates that survive casual review but fail audit." In his framing, the write gate is not a temporary safety measure while the tech matures; it is a permanent architectural choice that says "the AI is the drafter, a human is the publisher." For any report that will be cited in a regulatory filing, a board document, or an external communication, that framing is correct in 2026.

### Compliance surfaces: SOC 2, GDPR, HIPAA, PCI

Four regulatory surfaces that will touch nearly every AI-analyst deployment:

**SOC 2 Type II.** If your client is selling B2B SaaS, they have a SOC 2 report, and your AI-analyst worker is now in scope. The controls the auditor will ask about: least-privilege access (your read-only scopes prove it), change management (every MCP server version and prompt change tracked in git), incident response (you have a runbook for "the agent leaked PII"), and vendor risk (the LLM vendor's SOC 2 is in the trust portfolio — Anthropic's, OpenAI's, Google's are all available under NDA or via Trust Center portals).

**GDPR.** The EDPB's Opinion 28/2024 on AI models (December 2024) is the authoritative recent guidance and clarifies that data minimization, purpose limitation, and the Article 5 principles apply throughout AI development and deployment.[^12] For an AI analyst worker that reads customer data, the implications are concrete: you need a lawful basis (almost always legitimate interest or contract), you need to document the purpose (weekly reporting for the client), you need the minimum data necessary (do not pull `users.*` when `user_id, revenue` will do), and EU data subjects have rights to information, access, and in some cases erasure that your pipeline must be able to honor.

**HIPAA.** If the data touches PHI — healthcare payer, provider, or any covered entity — the BAA chain extends to the LLM vendor. Anthropic, OpenAI, and Google all offer BAAs on their enterprise tiers; you need one. The HHS's HTI-1 final rule, effective January 1, 2025, introduced Decision Support Intervention (DSI) transparency requirements for certified health IT that touches clinical workflows, which pulls AI-analyst tooling that feeds into EHR reporting into its scope.[^13] Safe Harbor de-identification (the 18 HIPAA identifiers) or Expert Determination is typically where you want to sit for any analyst worker against PHI; sending raw PHI to a general-purpose LLM is the failure mode.

**PCI DSS 4.0.1.** PCI DSS v4.0 became mandatory March 31, 2024, and was succeeded by v4.0.1 as the active standard at the end of 2024, with future-dated requirements enforceable from March 31, 2025.[^14] For an AI-analyst worker that touches anything near cardholder data, the rules are strict: masking of the PAN except for the last four digits in all queries and logs, hardened authentication on service accounts, documented scope of the cardholder-data environment. In practice, the architecturally correct move is to never let the AI worker see PAN data at all — mask it at the warehouse view layer, and design the reports to work on tokenized references.

### PII masking: architecture vs theater

The honest question is when Presidio-style masking is architecturally correct versus when it is security theater.

It is architectural when: (a) the data you're feeding the LLM contains PII incidentally (an email body whose subject contains a name, a support ticket whose description contains a phone number), (b) the report genuinely does not need the PII to be useful, and (c) the masking is deterministic and reversible where needed (a token that maps back to the real value via a secure lookup in the final render). In that shape, Presidio prevents the PII from ever entering the LLM's context, the trace store, or the observability vendor — genuine defense in depth.

It becomes theater when: (a) the LLM is re-ingesting aggregate tables where PII has already been removed upstream (you are paying latency for zero marginal safety), (b) the masking rule is so aggressive it destroys the signal (you masked every dollar amount, the report is now useless), or (c) the "masking" is just regex for email addresses in a domain where the PII is actually non-standard identifiers the regex will never catch. The discipline is to write down what specific threat the masking mitigates, measure whether the threat is actually present at that stage of the pipeline, and cut the step if not.

## Operator case studies / war stories

**Ramp and the spend-intelligence read-path.** Ramp's publicly-disclosed architecture around their AI Reporting and AI token-spend intelligence features is a read-path-first design against their own customers' transaction corpora. The January-2025 blog describing 13x growth in monthly AI token spend across Ramp customers — and the observation that "a single prompt template change can triple your bill overnight, a junior engineer experimenting on a Friday can blow through a quarterly budget by Monday" — is itself an artifact of an AI worker (Ramp's own) reading a structured warehouse (Ramp's transaction store) and writing a narrative output.[^11] The governance pattern visible in their disclosures: tenant isolation at the warehouse layer, service-account scoping, write gates for anything that touches cash movement. The principle generalizes: read-path produces the insight; write-path is always gated.

**The Simon Willison "lethal trifecta" case.** In April 2025 Willison documented a class of attacks where a Gmail MCP server returning an email body containing adversarial instructions caused an agent to take unintended actions — the classic confused-deputy.[^5] The specific fix patterns that emerged in the 2025 MCP community: (a) MCP gateways that intermediate tool calls and apply policies, (b) signed tool manifests with pinned versions, (c) client-side UI that shows tool definitions on every invocation so silent rug-pulls become visible. For any AI analyst worker reading email, Slack messages, or Zendesk tickets — any source where an adversary can plant tokens — one of these mitigations is required. The cost is real (gateway introduces ~50ms latency; UI prompts degrade autonomy) and worth it.

**The over-scoped service account that survived three audits.** A recurring pattern in postmortems and SOC 2 observations: an analyst-worker ships with `postgres_ro` permissioned to `USAGE` on the whole schema because that was convenient in dev. The report works. Three quarters later an auditor samples the service-account scope and finds read access to a `user_auth_tokens` table that contains refresh tokens. Nothing has been exploited — but the finding is a major nonconformity because least-privilege was violated. The fix costs a week (build views, migrate queries, rotate the account, retest). The lesson: provision the scope correctly on day one; retrofitting least-privilege under audit pressure is 10x more expensive than designing it in. Vanta's public trust center and case studies have multiple variants of this exact narrative pattern.

## Runnable experiment

Four phases. The goal is to produce a defended connector matrix for one real use case, then stand up the single most important connector for real and verify it works end-to-end.

**Phase 1 — Pick a use case and enumerate sources.** Select one AI-report use case you actually care about from Monday's lesson (your own weekly sales-ops report, a client's finance snapshot, a competitive-intel brief). Write down 3 to 5 real connectors required. A concrete example for a mid-market SaaS weekly sales-ops report: (a) Postgres read replica for `orders` and `line_items`, (b) Stripe API for revenue recognition, (c) HubSpot API for deal-stage transitions, (d) a Google Sheet with manual territory annotations, (e) S3 bucket with month-end journal PDFs.

**Phase 2 — Ask Claude Code to produce a defended decision table.** Prompt:

> "For each of the following 5 data sources [list], propose the best connector choice from {MCP server, first-party SDK, LangChain/LlamaHub loader, iPaaS node}. I want three scenarios: (a) I am a solo operator shipping in 7 days, (b) I am a 15-person startup with a platform engineer, (c) I am inside a 500-person enterprise with a security team. For each cell in the 5×3 matrix, give: the pick, the one-line rationale, the single biggest risk, and a URL to the docs or repo for that connector. Output as a markdown table with footnotes. Cite real MCP server URLs from github.com/modelcontextprotocol/servers or glama.ai."

Read the output critically. Where does it pick MCP because MCP is fashionable rather than because it wins? Where does the enterprise column propose iPaaS where you'd actually want an internal service?

**Phase 3 — Stand up ONE connector for real.** The Postgres MCP server is the right target because it's the canonical reference and the lessons generalize. Concretely: spin up a local Postgres in Docker, load 500 rows of synthetic orders data, create two roles — `report_agent_ro` with `SELECT` on a view that hides PII columns, and `report_agent_rw` which you do not give to the agent. Configure the Postgres MCP server in your Claude Code config pointing to the read-only role. Then issue three natural-language queries through Claude Code:

1. "What was total revenue last week by region?"
2. "Which 5 customers had the biggest week-over-week revenue drop?"
3. "Show me the top customers' email addresses." (This should fail gracefully because the view doesn't project the email column. Verify the failure mode is a clear error, not a hallucinated answer.)

Verify each result against a direct SQL query you run in `psql`. Numbers match? Good. Numbers don't match? The MCP server is doing something you don't expect — possibly rounding, possibly pagination truncation, possibly it's executing a different query than you think. Inspect the Claude Code trace.

**Phase 4 — Write 300 words on the abstraction cost.** Specifically: (a) what did the MCP abstraction hide that you would have seen with direct SDK, (b) at what team size does the hidden thing become a liability, (c) what's the minimum observability you'd want to add before running this in production. This is the output of the experiment — a defensible written position, not a green checkmark.

Expected observations: the MCP abstraction hides query plans (you don't see EXPLAIN; slow queries look like slow LLM responses), it hides pagination semantics (if the agent silently truncates at 1000 rows, your aggregate is wrong), and it hides auth refresh. At solo-operator scale, all three are fine. At 15-person scale you probably want a query-tagging middleware so your DBA can trace agent queries in `pg_stat_statements`. At enterprise, you want a full MCP gateway with policy enforcement.

## Problem set

1. **Connector matrix for your niche.** For five data sources relevant to your Block 1 Week 2 niche (not the generic example), pick MCP vs SDK vs iPaaS with a defended tradeoff per pick. Include one source where you change your pick between solo-operator and 15-person team scenarios, and articulate why. Rubric: the defense must cite at least two concrete properties of the source (auth model, rate limit, governance surface, schema stability), not just "MCP is newer."

2. **Position: MCP replaces LangChain loaders by 2027.** Defend or refute: "By end of 2027, MCP servers are the default connector layer for new AI analyst builds and LangChain Document Loaders are a legacy option maintained for existing deployments." Your position must cite at least three data points — one adoption metric from a recent state-of-AI report or a GitHub-stars trend, one specific architectural capability either has and the other doesn't, and one named operator's public position.

3. **Day-1 governance checklist.** Design the governance checklist for an AI report worker accessing customer-data tables at a 20-person SaaS that sells to regulated buyers. Categorize every item as day-1 must-have, day-30 should-have, day-90 nice-to-have. Must-have items should include at minimum: least-privilege read-only credentials, PII column masking at the view layer, audit logging of every tool call, documented scope of the cardholder-data environment if PCI applies. Should-haves include: RLS, Presidio or equivalent text-layer masking, BAA in place if any chance of PHI. Nice-to-haves include: MCP gateway, signed tool manifests, tiered redaction by report consumer. Defend each placement.

4. **Write-path position.** Take a position on write access for AI report workers: "Under what conditions, if any, should an AI analyst worker have direct write access to production systems?" Your answer must name at least one case where write is justified, one where it is not, and the minimum architectural gate that makes the justified case acceptable. Engage Barry McCardel's public position vs the Ramp product posture.

5. **PII leak trace.** For one read-path in your Phase-1 use case, trace a query from natural-language prompt through tool call, query execution, result parsing, prompt assembly, model inference, response rendering, and final report. At every layer, mark where PII could leak (to logs, to the trace store, to an observability vendor's S3, to the rendered report, to a human reviewer who shouldn't see it). Identify the single architectural point where masking gives the highest marginal safety, and defend that placement over the alternatives.

## Common failure modes at scale

**The MCP tool-redefinition silent attack.** A community MCP server you installed in March returns a new tool description in September that references a suspiciously-named resource. Claude approves it because you configured "auto-approve" in dev and forgot to tighten it in prod. Mitigation: never auto-approve tool-list changes in production; wire a diff-on-change alert into the Claude Code configuration.

**The Stripe-webhook replay.** Your agent reads Stripe events via a webhook-backed database. A Stripe engineer reprocesses a batch of events to fix a billing bug; your DB now has duplicate rows with the same event ID. The agent double-counts revenue in the weekly report. Mitigation: idempotency keys at the ingest layer, dedupe before the agent ever queries.

**The Google Sheets schema drift.** A finance teammate adds a column. The agent's query returns the new column silently because it uses `SELECT *` via the Sheets MCP. The LLM interprets the new column as one it recognizes and produces confidently wrong narrative. Mitigation: pinned column names, schema validation on read, a "new column detected" alert that blocks the run.

**The service-account that expires on a holiday.** Your HubSpot OAuth token has a 30-day expiry. The agent runs on a Monday morning; the token expired Sunday night; the run fails or worse, the agent decides to retry without the data and ships an empty report. Mitigation: refresh tokens with alerting on refresh failure, explicit fail-loud-don't-fail-silent in the orchestration.

**The cost-blowup from recursive tool use.** Agent is given both a SQL MCP and a "summarize" SDK tool. A query returns 50,000 rows; the agent summarizes them; the summarization calls another tool; you discover you spent $140 on one weekly run. Mitigation: token/cost ceilings per tool call, row-count caps at the query layer, circuit breaker at the orchestration layer.

**The SOC 2 scope explosion.** You added an observability vendor (Braintrust, Langfuse) and didn't put them through vendor risk. The auditor flags it as an unapproved sub-processor of customer data. Mitigation: any vendor that sees agent traces is a sub-processor; run them through risk intake before enabling.

## Open questions / what's not settled

**Does MCP win the connector-layer war, or is it absorbed into something bigger?** Pro-MCP: adoption in the first 12 months was extraordinary, the ecosystem includes real enterprise-grade gateways (Gopher Security, Glama, Smithery), and the LangChain team has shipped an MCP adapter rather than competing.[^6] Anti-MCP: the protocol is a thin layer over JSON-RPC, the security model is still maturing, and the real integration work (auth refresh, rate limiting, retries) still lives inside each server. Possible 2027 outcome: MCP is the discovery/metadata layer and the actual tool implementations move to a more opinionated framework (LangGraph, Pydantic AI workflows, vendor-managed tools).

**Where is the PII-masking ceiling?** Presidio and its commercial competitors (Nightfall, Skyflow) work well on common PII classes — SSNs, emails, credit cards, names in common scripts. They systematically miss domain-specific identifiers (internal ticket IDs that correlate to customers, free-text medical codes, non-Latin-script names). The open question: at what point do you need a domain-tuned NER model per deployment? 2025 arxiv papers suggest 10-20% recall gains with fine-tuned models on domain corpora, but the operational cost (label, train, maintain) is nontrivial.

**Is the read-only posture durable?** The case for never granting AI write-path is strongest today because the failure modes (hallucinated writes, prompt-injection-induced writes) are frequent and expensive. The case against is that the largest productivity gains — automated close, auto-coded AP, autonomous finance per the Ramp CEO's three-year horizon — require writes.[^11] The likely 2027 shape is not "AI writes directly" but "AI drafts a proposed write, a deterministic validator checks it, a structured approval queue gates it" — the workflow pattern Brex and Ramp already implement.

## Reviewer lens — named critics with specific disagreements

- **Simon Willison** would push back on the Layer-2 framing that "MCP wins by default for new builds." In his April 2025 post on MCP prompt-injection and in his subsequent "lethal trifecta" talks, his position is that MCP-equipped agents are exploitable by default in any setting where the tools touch untrusted content (email, web pages, tickets), and that the ecosystem's mitigations are uneven.[^5] His counter to the lesson: the decision matrix should have a column for "adversarial exposure of the source content" and when that column is high, the pick is SDK-in-a-sandbox, not MCP.

- **Harrison Chase (LangChain)** would push back on the binary "loaders vs MCP" framing in Layer 2. His public position (LangChain blog posts on the MCP adapter, and the `langchain-mcp-adapters` package) is that loaders and MCP solve different problems — loaders are for batch ingestion into a retrieval index, MCP is for runtime tool invocation — and a production system usually has both.[^6] His counter: the lesson should separate "how do I get data into a RAG index" from "how does my agent call tools at inference time" and not force a single-connector choice.

- **Barry McCardel (Hex)** would push back on the Ramp write-gate framing in Layer 3. His position, repeated in Hex blog posts and podcast appearances throughout 2024-2025, is that "AI without analysts" — even with careful write gates — produces confidently-wrong outputs that survive casual human review but fail audit. His counter: the write-path section understates the problem. Even read-path, if the analyst-in-the-loop is a junior who trusts the narrative, the failure mode recurs. The architectural fix isn't "write gate"; it's "expert-in-the-loop on the published product."

- **David Soria Parra and Justin Spahr-Summers (Anthropic, MCP authors)** would push back on the lesson's casual treatment of MCP as "mostly REST API wrappers." Their public framing in the MCP specification and the associated engineering posts is that MCP's real innovation is the *bidirectional* primitive set (resources, prompts, tools, roots, sampling) — and treating it as just tool discovery misses the architectural win.[^1] Their counter: teaching MCP as "fancy OpenAPI" underplays the client-side primitives (sampling, roots) that are exactly what enables governance-by-default.

- **Christina Cacioppo (Vanta)** would push back on the governance checklist in problem 3. Her position, consistent across Vanta blog posts on AI-specific compliance in 2024-2025, is that the modern SOC 2 audit increasingly treats AI sub-processors (the LLM vendor, the observability vendor, the vector DB) as day-1 risk items, not day-30. Her counter: "observability vendor runs through risk intake" should be day-1 must-have, not should-have, for any client-facing deployment.

## Further reading

**Must-read (under 5):**

- *Introducing the Model Context Protocol* — Anthropic announcement post, Nov 25, 2024. The source of record on what MCP is and why.
- *Model Context Protocol has prompt injection security problems* — Simon Willison, Apr 9, 2025. The counterweight. Read immediately after the Anthropic post.
- *Row Security Policies* — PostgreSQL 18 documentation. The ground truth for RLS semantics; 20 minutes well spent.
- *Opinion 28/2024 on AI models* — European Data Protection Board, Dec 2024. The single most important regulatory document on AI + personal data in the EU context.

**Recommended:**

- Microsoft Presidio docs (`microsoft.github.io/presidio`) — the default PII toolchain.
- LlamaHub registry (`llamahub.ai`) — the canonical LlamaIndex loader directory.
- Motherduck `PROMPT_SQL` documentation — for natural-language-to-SQL patterns against OLAP.
- Ramp Intelligence product posts — for the reference architecture of a shipped AI-finance worker.

**Optional:**

- Harrison Chase on LangChain's MCP adapter (LangChain blog, 2025).
- HTI-1 final rule (HHS, 2024) if healthcare-adjacent.
- PCI DSS v4.0.1 standard (PCI SSC, 2024) if payment-data-adjacent.

## Citations

[^1]: Anthropic, "Introducing the Model Context Protocol," Nov 25, 2024. `https://www.anthropic.com/news/model-context-protocol`. Verified 2026-04-17. Supports: launch date, reference servers (Google Drive, Slack, GitHub, Git, Postgres, Puppeteer), initial enterprise adopters (Block, Apollo), developer-tool partners (Zed, Replit, Codeium, Sourcegraph).

[^2]: Model Context Protocol specification site, `https://modelcontextprotocol.io/` and related InfoQ coverage, "Anthropic Publishes Model Context Protocol Specification for LLM App Integration," Dec 2024, `https://www.infoq.com/news/2024/12/anthropic-model-context-protocol/`. Verified 2026-04-17. Supports: the JSON-RPC 2.0 transport and the primitive set (prompts, resources, tools, roots, sampling).

[^3]: MCP reference servers repository, `https://github.com/modelcontextprotocol/servers`, and community registries Glama (`https://glama.ai`), Smithery, and mcp.run. Verified 2026-04-17. Supports: scale of the community-server ecosystem.

[^4]: Gopher Security, "MCP vs LangChain: Framework Comparison," `https://www.gopher.security/mcp-security/mcp-vs-langchain-framework-comparison`. Verified 2026-04-17. Supports: the governance claim that MCP allows tools to be versioned, audited, and maintained separately from agent code.

[^5]: Simon Willison, "Model Context Protocol has prompt injection security problems," Apr 9, 2025, `https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/`, and "The Lethal Trifecta" talk materials (Aug 2025). Verified 2026-04-17. Supports: the prompt-injection-via-tool-response threat, the rug-pull silent-redefinition class, and the lethal-trifecta framing.

[^6]: LangChain MCP adapters package (`langchain-mcp-adapters` on PyPI) and LangChain blog posts on MCP integration, 2025. Also Apigene's "LangChain vs MCP: When to Use Each" 2026 guide, `https://apigene.ai/blog/langchain-vs-mcp`. Verified 2026-04-17. Supports: the complementary framing of loaders + MCP in production systems.

[^7]: PostgreSQL 18 Documentation, "5.9. Row Security Policies," `https://www.postgresql.org/docs/current/ddl-rowsecurity.html`. Verified 2026-04-17. Supports: RLS semantics and the policy-restriction mechanism.

[^8]: Permit.io, "Postgres RLS Implementation Guide — Best Practices, and Common Pitfalls," `https://www.permit.io/blog/postgres-rls-implementation-guide`, and AWS Prescriptive Guidance on RLS for multi-tenant SaaS on PostgreSQL, `https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-managed-postgresql/rls.html`. Verified 2026-04-17. Supports: the `SET LOCAL` session-context pattern for tenant isolation.

[^9]: Microsoft Presidio GitHub repository and documentation, `https://github.com/microsoft/presidio` and `https://microsoft.github.io/presidio/`. Verified 2026-04-17. Supports: Presidio's Analyzer/Anonymizer engines and detection methods (regex, NER, custom recognizers).

[^10]: LiteLLM Presidio PII Masking tutorial, `https://docs.litellm.ai/docs/tutorials/presidio_pii_masking`. Verified 2026-04-17. Supports: the production integration pattern for Presidio in an LLM pipeline.

[^11]: Ramp, "Ramp Intelligence: the future of finance is finally here," `https://ramp.com/blog/announcing-ramp-intelligence`; Ramp 2025 Release Notes, `https://ramp.com/blog/2025-release-notes`; Ramp AI token-spend intelligence post, `https://ramp.com/blog/trillion-dollar-ai-blindspot`; and "Autonomous finance will arrive within three years: Ramp CEO," CFO Dive, `https://www.cfodive.com/news/autonomous-finance-will-arrive-within-three-years-ramp-ceo-ai-agents/756766/`. Verified 2026-04-17. Supports: the Ramp product posture on read-path-first AI, write-path gates, and the 13x token-spend growth observation.

[^12]: European Data Protection Board, "Opinion 28/2024 on certain data protection aspects related to the processing of personal data in the context of AI models," Dec 2024, `https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf`. Verified 2026-04-17. Supports: Article 5 GDPR principles (data minimization, purpose limitation) applied to AI development and deployment.

[^13]: HHS Office of the National Coordinator for Health IT, HTI-1 Final Rule (2024), and Foley & Lardner analysis, "HIPAA Compliance for AI in Digital Health: What Privacy Officers Need to Know," `https://www.foley.com/insights/publications/2025/05/hipaa-compliance-ai-digital-health-privacy-officers-need-know/`. Verified 2026-04-17. Supports: HTI-1's DSI transparency requirements effective Jan 1, 2025, and the BAA requirement for any LLM vendor processing PHI.

[^14]: PCI Security Standards Council, "Just Published: PCI DSS v4.0.1," `https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1`, and Eckoh, "PCI DSS 4.0 becomes mandatory on April 1 2024," `https://www.eckoh.com/blog/pci-dss-4-0-becomes-mandatory-on-april-1-2024-heres-what-you-need-to-consider`. Verified 2026-04-17. Supports: the March 31, 2024 mandatory date for v4.0, the transition to v4.0.1 at end of 2024, and the March 31, 2025 enforcement date for future-dated requirements.
