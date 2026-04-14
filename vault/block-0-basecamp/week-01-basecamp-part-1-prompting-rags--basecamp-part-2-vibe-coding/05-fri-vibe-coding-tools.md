---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 5
day_name: fri
session_slug: basecamp-part-2-vibe-coding
date_due: 2026-05-01
tags: [vibe-coding, cursor, claude-code, bolt, lovable, v0, replit, workflow, spec-driven, agentic-coding]
sources: [karpathy-vibe-coding-tweet, cursor-docs, claude-code-docs, simon-willison, boris-cherny]
last_verified: 2026-04-14
---

# Friday Deep-dive: Vibe Coding Tools — The Honest Comparison

## Why this matters (operator framing)

You will be asked to ship prototypes fast. Clients will ask you to "just build a quick demo" on a call. Prospects will want to see something working before they sign. The difference between a practitioner who can demo a working app in 90 minutes and one who can't is not talent — it is tool fluency. This lesson gives you the map of the tool landscape, when to use each tool, and how to combine them for real projects.

## Prerequisites

- [[04-thu-vibe-coding-preread]] — the three-mode spectrum and tool overview
- [[02-tue-prompting-deep-dive]] — spec-writing discipline applies directly here
- 30 minutes: try at least one of these tools before reading (Bolt.new is the lowest-friction entry point)

## Core content

### 1. The taxonomy: what problem does each tool solve?

| Tool | Primary use case | Runtime | Auth | Best for |
|------|-----------------|---------|------|----------|
| **Cursor** | Existing codebase agent | Local | Your own | Production-grade features in real projects |
| **Claude Code** | Terminal-first agent | Local | Your own | Infrastructure, scripts, large refactors |
| **Bolt** | Greenfield JS/TS app | Browser container | StackBlitz | Demos, prototypes, no-local-setup |
| **Lovable** | Full-stack + DB | Cloud | Lovable auth | Non-devs, CRUDs with Supabase |
| **v0** | React component generation | Vercel cloud | Vercel | Frontend design prototyping |
| **Replit Agent** | Cloud IDE + deploy | Replit cloud | Replit auth | Collaborative hacking, quick deploy |

This is not a ranking — each tool has a distinct niche. Trying to use Lovable for a complex data pipeline is like using a Bolt for a structural engineering project.

### 2. Cursor: the power tool for existing codebases

Cursor is a fork of VS Code with deep AI integration[^1]. Its key capabilities:

**Codebase-aware context**: Cursor indexes your entire repository (using embeddings, similar to RAG) and includes relevant files automatically when you prompt it. This is the killer feature for existing projects — it "knows" your code structure.

**Composer (agent mode)**: you give Cursor a high-level task ("add user authentication with JWT, create the middleware, update the route handlers, and write tests"), and it reads the relevant files, proposes a plan, implements changes across multiple files, and runs the terminal commands to verify. You review at checkpoints[^1].

**Rules for AI (.cursorrules)**: you can define a `.cursorrules` file at the root of your project specifying: language, framework, code style, test framework, forbidden patterns. This is Cursor's equivalent of a system prompt — operator-level instructions that apply to every Cursor session in that project.

Practical tip from Boris Cherny's talks on agentic coding[^2]: before starting a complex Cursor session, write a `SPEC.md` file describing exactly what you want. Reference it in your prompt: "Implement the feature described in SPEC.md." The model spends its context budget reading the spec rather than re-interpreting your natural language.

**Where Cursor struggles**: greenfield projects with no existing structure, non-JS/TS/Python stacks (weaker, though improving), tasks that require the model to understand deeply interconnected logic across 50+ files simultaneously.

### 3. Claude Code: the terminal-native agent

Claude Code is Anthropic's own agentic coding tool, released in 2025[^3]. It runs in your terminal, reads your file system, executes commands, and edits files. It is fundamentally different from Cursor in UX: no GUI, no IDE, just a terminal prompt.

**What makes it different**:
- **Bash-native**: it can run any terminal command, including `git`, `pip`, `npm`, `docker`, `curl`. Cursor can do this too, but Claude Code was built from the ground up for it.
- **System-level tasks**: setting up dev environments, writing CI/CD configs, migrating databases, auditing security configs — tasks that require both file editing and command execution.
- **Large-scale refactors**: Claude Code's context management (via conversation compaction) handles multi-session refactors better than Cursor's in-session context.

**The slash commands**: Claude Code has built-in commands like `/chat-course`, `/generate-lesson`, `/review-pr` that can be customized per project via `.claude/commands/`. This is the capability you're using right now in this vault.

**Permission model**: Claude Code asks for permission before running commands that have side effects (file writes, installs, network calls). This is not a limitation — it's a safety design. In agent mode, grant permissions broadly; in review mode, approve each one.

**Pricing note**: as of April 2026, Claude Code is billed per-token via the Anthropic API (not a flat subscription). Heavy usage costs $10–50/month depending on project size; a 2-hour focused coding session typically runs $2–8[^3].

### 4. Bolt: greenfield speed

Bolt (bolt.new by StackBlitz) is the fastest path from idea to working browser-based app[^4]. You type a description, and within 30–60 seconds you have a full-stack JavaScript/TypeScript app running in a sandboxed browser container.

**What Bolt does well**:
- React/Vue/Svelte frontends with a Node.js backend
- Quick CRUD apps
- Integrations with familiar APIs (OpenAI, Stripe, SendGrid)
- Zero local setup — everything runs in the browser

**What Bolt does badly**:
- Complex state management
- Apps that need to persist data across sessions without a real database
- Non-JS stacks (Python, Go, Rust — not supported)
- Production deployments (you can export, but you'll need to redeploy elsewhere)

**The Bolt workflow for a prototype**:
1. Describe your app in 2–3 sentences ("A task tracker with user login, project boards, and drag-and-drop task ordering")
2. Let it generate. Watch the terminal output for errors.
3. If it errors, paste the error message back and say "fix this."
4. Export when happy. Clean up the exported code before deploying.

> My take: Bolt is best as an idea-to-mockup tool, not an idea-to-production tool. The generated code is often fine for demos but has structural issues (no error handling, hardcoded values, no tests) that require cleanup before shipping.

### 5. Lovable: the non-developer's full stack

Lovable (formerly GPT Engineer) generates React frontends backed by Supabase (PostgreSQL + auth + storage)[^5]. Its distinguishing feature is the first-class Supabase integration — it generates the database schema, the row-level security policies, and the frontend in one shot.

**Best use case**: a solo operator who needs a CRUD web app with user authentication and wants to ship it without writing any code. Lovable handles the Supabase setup, generates the React app, and even deploys it.

**The tradeoff**: generated apps follow Lovable's patterns, which can conflict with yours when you take ownership of the code. The moment you start editing the Supabase schema manually, you risk breaking the Lovable sync.

**When to choose Lovable over Bolt**: when you need a real database and auth from day one. When to choose Bolt: when you want UI speed and don't need persistence yet.

### 6. v0 by Vercel: component-first generation

v0 is not an application generator — it's a component generator[^6]. You describe a UI component in natural language, and v0 generates Shadcn/UI + Tailwind CSS React code. The output is production-quality front-end code that drops into any React project.

**The workflow**: describe the component → v0 generates → copy the code into your Cursor or Next.js project. It is a component library on demand.

**Use v0 when**: you know what the app should look like and want to generate the shell quickly. Don't use v0 to generate entire applications — use it to generate individual pages or components that you assemble.

Simon Willison uses v0 for rapid UI prototyping even in projects he's otherwise developing "the old way" — he generates the component structure then edits it manually[^7].

### 7. Replit Agent: cloud-native collaboration

Replit is a cloud IDE that added an AI agent ("Replit Agent") in 2024[^8]. The agent can spin up a project, install dependencies, write code, and deploy it — all in the browser. Replit's cloud execution means the agent can actually run the code during generation.

**Where Replit excels**:
- Teaching contexts (no local setup)
- Multi-language projects (Python, Node.js, Go, Ruby — all supported)
- Quick deployment (Replit hosts by default)
- Collaboration (share a Replit with a client who can then see and edit)

**Limitations**: Replit's compute is shared and slower than local. For production, you'd migrate off Replit. The free tier has execution time limits.

### 8. The spec-driven workflow: getting consistent quality

The gap between "vibe coding that works" and "vibe coding that produces garbage" is almost always the quality of the specification[^2]. The best practitioners — Boris Cherny, Simon Willison, top Cursor power users — all converge on writing a spec before prompting.

**The one-page spec template**:
```markdown
# [Project Name] Spec

## What it does (one sentence)
[Product description]

## Users
[Who uses it and what they want to do]

## Core features (ranked by priority)
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

## Tech stack
- Frontend: [React / Vue / plain HTML]
- Backend: [Node.js / Python / none]
- Database: [Supabase / SQLite / none]
- Auth: [Supabase Auth / none / basic]
- Deployment: [Vercel / Fly.io / Replit]

## What it must NOT do
- [Hard constraints — e.g., no external API calls, no user data storage]

## Success definition
[What does "working" look like? Be specific.]
```

Give this spec to any tool and the output quality jumps dramatically. Karpathy's tweet described the zero-spec extreme — it works for throwaway experiments. For anything that ships to a real user, write the spec.

### 9. Workflow comparison: pick the right tool for the job

**Scenario 1: Client asks for a demo of a lead capture page in the next 2 hours**
Tool: v0 (for the component) + Bolt (for the app shell) or Lovable if they want to capture emails in a real database. Time to working demo: 20 minutes.

**Scenario 2: You need to add a new feature to an existing Python FastAPI backend**
Tool: Cursor (agent mode) or Claude Code (terminal). Read the codebase, write the spec, let the agent implement. Time: 30–60 minutes.

**Scenario 3: You want to automate a weekly report scraper that runs on your local machine**
Tool: Claude Code. Write it, test it, schedule it with cron. Time: 15–30 minutes.

**Scenario 4: A non-technical client wants to build their own internal dashboard**
Tool: Lovable. They can iterate without you after initial setup. Time: 45 minutes of setup then hand off.

**Scenario 5: You're exploring a new architecture pattern and want to spike it quickly**
Tool: Replit Agent or Bolt. Throwaway spike, no local contamination.

## Worked example

Build this today (35–45 minutes):

**Goal**: A simple "Daily Stand-up Bot" — a Telegram or Slack webhook that, when triggered, DMs each team member asking for their stand-up, collects responses, and posts a summary to a channel.

You can stub the Telegram/Slack parts with a local mock.

**Using Cursor/Claude Code** (recommended if you have a coding background):
1. Write the spec (5 min) — use the template above.
2. Open Claude Code or a new Cursor session. Paste the spec.
3. Let it scaffold: project structure, dependencies, main bot logic, summary generation with the Anthropic API.
4. Run it locally with a test webhook payload.

**Using Bolt** (if you prefer browser-based):
1. Go to bolt.new, describe the stand-up bot.
2. Swap the Telegram SDK mock for a UI that simulates the message flow.
3. Download the code, note what you'd need to change to make it production.

Regardless of which tool you use: write down exactly where the model went wrong and how you corrected it. That correction log is your most valuable output from this exercise.

## Common mistakes experts see

- **No spec → vague output → frustration → blaming the tool**: every experienced vibe coder will tell you the spec is 80% of the result. Write it before you open the tool.
- **One giant prompt**: "Build me a full e-commerce platform with product listings, cart, checkout with Stripe, user accounts, admin panel, and email receipts." The model will hallucinate on the parts it isn't sure about. Decompose into steps.
- **Not using `.cursorrules` or `.claude/` configs**: these are the operator-level system prompts for your project. A project-level config that says "always use TypeScript strict mode, always write tests, always handle errors explicitly" will raise output quality across hundreds of sessions.
- **Ignoring generated test coverage**: generated code almost never generates meaningful tests unless you explicitly ask. Always prompt: "now write tests for this" and run them.
- **Not using version control**: git commit after every working state. This is the cheapest undo mechanism in the world.
- **Shipping security-blind generated code**: OWASP Top 10 violations are common in generated code. SQL injection, unvalidated inputs, insecure cookies. Run a linter (`bandit` for Python, `eslint-plugin-security` for JS) on anything you ship.

## Reflection questions

1. Compare Cursor's `.cursorrules` file to a system prompt for a model API. What are the similarities and differences?
2. You need to build a SaaS MVP in a weekend. Walk through which tools you'd use at each stage (frontend wireframe → backend logic → database → deployment → payment integration).
3. Why does the quality of the natural language spec predict output quality better than the choice of tool?
4. Karpathy described not even reading the generated code. Simon Willison argues that's irresponsible for anything shipped to users. How would you reconcile these positions for your own practice?
5. What would a `.cursorrules` file for a Python FastAPI + PostgreSQL + pytest project look like? Write a draft.
6. Claude Code can execute arbitrary terminal commands. What are the security implications of running it in agent mode on a production server?

## My take (reviewer lens)

Karpathy would say most developers are moving too slowly and with too much guilt about "not understanding" generated code. His implicit argument is that as long as the software is correct (verified by running it), the implementation details are irrelevant. This is correct for scripts and prototypes. It is wrong for systems that carry customer data, process payments, or run in regulated industries — and Karpathy hasn't claimed otherwise, though many have misread him as endorsing zero-understanding across the board.

Seibel would cut straight to the business question: "What did you ship this week?" The tool that helps you ship most reliably to your actual customer base wins. That might be Cursor for a developer, Lovable for a designer, Claude Code for an infrastructure person. There is no universal winner and wasting time picking the "right" tool is itself a mistake.

Boris Cherny would say the tools you're comparing are at different layers of abstraction. v0 and Lovable are in the "application generator" layer. Cursor and Claude Code are in the "developer agent" layer. A mature practitioner uses both layers: generate the scaffold with Lovable, then bring it into Cursor for the custom business logic. The mistake is treating them as alternatives rather than complements.

## Further reading

**Must-read**
- Karpathy vibe coding tweet — <https://x.com/karpathy/status/1886192184808149383>
- Claude Code documentation — <https://docs.anthropic.com/en/docs/claude-code>

**Recommended**
- Cursor documentation, "Rules for AI" — <https://docs.cursor.com/context/rules-for-ai>
- Simon Willison, posts tagged "llm-tools" — <https://simonwillison.net/tags/llm-tools/>

**Optional**
- Lovable documentation — <https://docs.lovable.dev>
- Bolt documentation — <https://docs.bolt.new>
- v0 documentation — <https://v0.dev/docs>

## Citations

[^1]: Cursor, "Cursor Features — Composer Agent," *Cursor Documentation*, <https://docs.cursor.com/cmdk/overview>, accessed 2026-04-14. Covers multi-file agent mode, .cursorrules, and codebase indexing.

[^2]: Boris Cherny, talks and posts on Claude Code and agentic coding, *Anthropic*, 2025. Referenced in Anthropic engineering blog; key insight: spec-first prompting is the highest-leverage practice for agentic tools.

[^3]: Anthropic, "Claude Code overview," *Anthropic Documentation*, <https://docs.anthropic.com/en/docs/claude-code>, accessed 2026-04-14. Covers terminal-native workflow, slash commands, permission model, and pricing.

[^4]: StackBlitz, "Bolt.new — AI Full-Stack Web Development in the Browser," <https://bolt.new>, accessed 2026-04-14.

[^5]: Lovable, "How Lovable works," *Lovable Documentation*, <https://docs.lovable.dev/introduction>, accessed 2026-04-14. Covers React + Supabase generation and row-level security generation.

[^6]: Vercel, "v0 — Build UI with natural language," <https://v0.dev>, accessed 2026-04-14. Shadcn/UI + Tailwind React component generation.

[^7]: Simon Willison, "I've been using v0 for rapid UI work," *simonwillison.net*, 2025, <https://simonwillison.net>. Description of component-level workflow.

[^8]: Replit, "Replit Agent," *Replit Documentation*, <https://docs.replit.com/replitai/agent>, accessed 2026-04-14. Multi-language cloud IDE agent with deployment.

_last_verified: 2026-04-14_
