---
type: program-index
program: AI Catalyst C3
start: 2026-04-18
end: 2026-10-22
---

# AI Catalyst C3 — Personal Study Program

> Built to make you walk into every live session from a position of mastery.

## The Program

- **Provider**: Outskill — AI Catalyst C3 cohort
- **Instructor**: Dileep (<dileep@outskill.com>) and the Outskill faculty
- **Duration**: 26 calendar weeks — **April 18 2026 → October 22 2026**
- **Live sessions**: Every Saturday & Sunday, 7:30 PM IST (2:00 PM UTC, 10:00 AM EST)
- **Office hours**: Thursdays, 7:30 PM IST
- **Resource drops**: Mondays on the LMS (recordings, worksheets, prompts)
- **Structure**: 9 blocks → ~50 live sessions + 22 office hours + weekly resource drops

## The 9 Blocks

| # | Block | Weeks | Dates |
|---|---|---|---|
| 0 | Basecamp & Revision | 4 | Apr 18 – May 17 |
| 1 | Problem Solving with AI & Outreach | 2 | May 23 – Jun 4 |
| 2 | AI Employees / Interns | 3 | Jun 6 – Jun 25 |
| 3 | Advanced Topics & Voice Agents | 3 | Jun 27 – Jul 16 |
| 4 | Test, Validate & Package | 3 | Jul 18 – Aug 6 |
| 5 | Product Building Principles | 3 | Aug 8 – Aug 27 |
| 6 | Launch & Monetization | 3 | Aug 29 – Sep 17 |
| 7 | Onboarding & Tracking | 3 | Sep 19 – Oct 8 |
| 8 | Wind-up & Checklists | 2 | Oct 10 – Oct 22 |

## How To Use This Vault

This vault is the **source of truth**. You can open it in:

- **This repo's Next.js app** → `cd app && npm run dev` → <http://localhost:3000>
- **Obsidian** → Open the `vault/` folder as a vault
- **NotebookLM** → drag any week's `07-notebooklm-pack/` folder in
- **Cursor / VS Code** → browse files directly
- **Claude Code** → `cd vault && claude` — ask anything via `/chat-course`

See [how-to-study](how-to-study.md) for the daily protocol.

## Quality Standard

Every lesson file in this vault is held to a strict standard. See
[quality-standard](quality-standard.md) — the short version:

1. **5–12 primary-source citations per lesson**, from a tiered list of operator-grade sources.
2. **Structure**: Why → Prerequisites → Mechanics → Worked example → Pitfalls → Reflection → Further reading.
3. **Currency**: generated the week of the live class, so state-of-the-art is captured.
4. **Runnable code** in `code-lab/`, pinned dependencies.
5. **Reviewer lens**: every lesson ends with "what would Karpathy / Seibel / Boris push back on?"

## Master Reading List

The canonical sources this program draws on. Each lesson cites a subset with
inline links; this is the menu.

### Foundations / ML
- **Karpathy — Neural Networks: Zero to Hero** (YouTube playlist)
- **Karpathy — nanoGPT, makemore, minGPT** (GitHub)
- **Karpathy — "Let's build GPT" & "Let's build the GPT Tokenizer"** (YouTube)
- **Karpathy — "Deep Dive into LLMs like ChatGPT"** (YouTube, 2024)
- Stanford **CS224n** (NLP), **CS25** (Transformers), **CS336** (Language Modeling)
- **fast.ai** — Jeremy Howard's Practical Deep Learning
- **3Blue1Brown** — "Neural Networks" series
- **Chip Huyen** — *Designing ML Systems* + *AI Engineering* (O'Reilly 2024)

### LLM Engineering & Tooling
- **Anthropic Cookbook** (<github.com/anthropics/anthropic-cookbook>)
- **Anthropic Docs** — prompt engineering guide, tool use, vision, PDF support
- **OpenAI Cookbook**
- **Simon Willison's blog** — <simonwillison.net> (current state of LLM practice)
- **Hamel Husain** — "Your AI Product Needs Evals"
- **Eugene Yan** — <eugeneyan.com> (LLM patterns, evals, RAG)
- **LangChain** & **LlamaIndex** docs

### Claude Code & MCP
- **Boris Cherny** — Claude Code engineering talks & posts
- **Anthropic MCP specification** + reference servers
- **Claude Code documentation** & changelog
- **Claude.ai/code** posts

### RAG
- Anthropic — **"Introducing Contextual Retrieval"** (Sep 2024)
- **Jerry Liu** (LlamaIndex) — RAG lectures
- **Jason Liu** — <jxnl.co> RAG consulting posts
- Wang et al. — **"Searching for Best Practices in RAG"** (2024)
- **GraphRAG** (Microsoft Research, 2024)

### Agents
- Anthropic — **"Building effective agents"** (Dec 2024)
- **LangGraph**, **CrewAI**, **AutoGen** docs
- **Lindy**, **Relevance AI**, **Gumloop** — no-code agent platforms
- **Lilian Weng** — "LLM Powered Autonomous Agents"

### Voice / Telephony / WhatsApp
- **VAPI** docs & examples
- **Twilio** voice & WhatsApp Business API docs
- **WATI**, **AiSensy** — WhatsApp Business automation
- **ElevenLabs**, **Deepgram**, **Cartesia** — TTS/STT
- **Retell AI** case studies

### Automation (n8n / Make / Zapier)
- **Official n8n documentation** + community workflows
- **Zapier & Make** official guides
- **Tomaz @ Coding Money** (YouTube — n8n deep-dives)

### YC / Operator thinking
- **Paul Graham** — <paulgraham.com> essays
- **YC Startup School** (library.ycombinator.com)
- **Michael Seibel**, **Garry Tan**, **Harj Taggar** — talks
- **Jason Lemkin** (SaaStr) — SaaS pricing & sales
- **Lenny Rachitsky** — <lennysnewsletter.com>

### Product / GTM / Pricing
- **a16z AI Canon** (<a16z.com/ai-canon>)
- **First Round Review**
- **Marty Cagan** — *Inspired*, *Empowered*
- **Superhuman's onboarding playbook** (First Round Review)
- **Reforge** content (Growth / Retention / Monetization)
- **April Dunford** — *Obviously Awesome* (positioning)

### Design / Frontend
- **Refactoring UI** — Steve Schoger & Adam Wathan
- **Linear's design principles**
- **Vercel**, **shadcn/ui**, **Aceternity UI** — reference patterns
- **Rauno Freiberg** — design interactions

### Papers (must-knows)
- Vaswani et al. — **Attention Is All You Need** (2017)
- **GPT-3** (Brown et al. 2020), **InstructGPT / RLHF** (Ouyang et al.)
- **Chinchilla** (Hoffmann et al. 2022)
- **DPO** (Rafailov et al. 2023)
- **RAG** (Lewis et al. 2020)
- **ReAct** (Yao et al. 2022)
- **Toolformer** (Schick et al. 2023)

## Tracking

- Daily completion stamps live in `app/progress.db` (SQLite, per-machine).
- Sync completions across Mac/Windows via `progress.json` (optional, git-tracked).
- Streak, time-on-lesson, quiz scores all captured in-app.
