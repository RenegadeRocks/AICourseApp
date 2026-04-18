---
type: program-index
program: AI Pro-level Course
---

# AI Pro-level Course — Personal Study Program

> Built to make you walk into every topic from a position of mastery.

## The Program

- **Provider**: Renegade Rocks
- **Instructor**: Claude Opus 4.6 and 4.7
- **Duration**: 26 calendar weeks (self-paced)
- **Structure**: 9 blocks, each week expands into 7 daily lessons

## The 9 Blocks

| # | Block | Weeks |
|---|---|---|
| 0 | Basecamp & Revision | 4 |
| 1 | Problem Solving with AI & Outreach | 2 |
| 2 | AI Employees / Interns | 3 |
| 3 | Advanced Topics & Voice Agents | 3 |
| 4 | Test, Validate & Package | 3 |
| 5 | Product Building Principles | 3 |
| 6 | Launch & Monetization | 3 |
| 7 | Onboarding & Tracking | 3 |
| 8 | Wind-up & Checklists | 2 |

## How To Use This Vault

This vault is the **source of truth**. You can open it in:

- **This repo's Next.js app** (primary) → `cd app && npm run dev` → <http://localhost:3000>
- **Obsidian** (optional) → open the `vault/` folder as a vault — wikilinks and frontmatter are already compatible
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
- [**Karpathy — Neural Networks: Zero to Hero**](https://karpathy.ai/zero-to-hero.html) (YouTube playlist)
- Karpathy — [**nanoGPT**](https://github.com/karpathy/nanoGPT), [**makemore**](https://github.com/karpathy/makemore), [**minGPT**](https://github.com/karpathy/minGPT) (GitHub)
- Karpathy — [**"Let's build GPT"**](https://www.youtube.com/watch?v=kCc8FmEb1nY) & [**"Let's build the GPT Tokenizer"**](https://www.youtube.com/watch?v=zduSFxRajkE) (YouTube)
- [**Karpathy — "Deep Dive into LLMs like ChatGPT"**](https://www.youtube.com/watch?v=7xTGNNLPyMI) (YouTube, 2024)
- Stanford [**CS224n**](https://web.stanford.edu/class/cs224n/) (NLP), [**CS25**](https://web.stanford.edu/class/cs25/) (Transformers), [**CS336**](https://stanford-cs336.github.io/spring2025/) (Language Modeling)
- [**fast.ai**](https://course.fast.ai/) — Jeremy Howard's Practical Deep Learning
- [**3Blue1Brown — "Neural Networks" series**](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- [**Chip Huyen**](https://huyenchip.com/books/) — *Designing ML Systems* + *AI Engineering* (O'Reilly 2024)

### LLM Engineering & Tooling
- [**Anthropic Cookbook**](https://github.com/anthropics/anthropic-cookbook)
- [**Anthropic Docs**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — prompt engineering guide, tool use, vision, PDF support
- [**OpenAI Cookbook**](https://cookbook.openai.com/)
- [**Simon Willison's blog**](https://simonwillison.net/) (current state of LLM practice)
- [**Hamel Husain — "Your AI Product Needs Evals"**](https://hamel.dev/blog/posts/evals/)
- [**Eugene Yan**](https://eugeneyan.com/) (LLM patterns, evals, RAG)
- [**LangChain**](https://python.langchain.com/docs/introduction/) & [**LlamaIndex**](https://docs.llamaindex.ai/en/stable/) docs

### Claude Code & MCP
- [**Boris Cherny — Head of Claude Code (Lenny's Podcast)**](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) — Claude Code engineering talks & posts
- [**Anthropic MCP specification**](https://modelcontextprotocol.io/) + reference servers
- [**Claude Code documentation**](https://docs.claude.com/en/docs/claude-code/overview) & changelog
- [**Claude.ai/code**](https://www.claude.com/product/claude-code) posts

### RAG
- Anthropic — [**"Introducing Contextual Retrieval"**](https://www.anthropic.com/news/contextual-retrieval) (Sep 2024)
- **Jerry Liu** (LlamaIndex) — RAG lectures <!-- TODO: no verified URL found -->
- [**Jason Liu**](https://jxnl.co/) — RAG consulting posts
- Wang et al. — [**"Searching for Best Practices in RAG"**](https://arxiv.org/abs/2407.01219) (2024)
- [**GraphRAG**](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) (Microsoft Research, 2024)

### Agents
- Anthropic — [**"Building effective agents"**](https://www.anthropic.com/research/building-effective-agents) (Dec 2024)
- [**LangGraph**](https://langchain-ai.github.io/langgraph/), [**CrewAI**](https://docs.crewai.com/), [**AutoGen**](https://microsoft.github.io/autogen/stable/) docs
- **Lindy**, **Relevance AI**, **Gumloop** — no-code agent platforms <!-- TODO: no verified URL found -->
- [**Lilian Weng — "LLM Powered Autonomous Agents"**](https://lilianweng.github.io/posts/2023-06-23-agent/)

### Voice / Telephony / WhatsApp
- [**VAPI**](https://docs.vapi.ai/) docs & examples
- Twilio [**voice**](https://www.twilio.com/docs/voice) & [**WhatsApp Business API**](https://www.twilio.com/docs/whatsapp) docs
- [**WATI**](https://www.wati.io/), [**AiSensy**](https://www.aisensy.com/) — WhatsApp Business automation
- [**ElevenLabs**](https://elevenlabs.io/), [**Deepgram**](https://deepgram.com/), [**Cartesia**](https://cartesia.ai/) — TTS/STT
- [**Retell AI**](https://www.retellai.com/) case studies

### Automation (n8n / Make / Zapier)
- [**Official n8n documentation**](https://docs.n8n.io/) + community workflows
- [**Zapier**](https://zapier.com/learn/) & [**Make**](https://help.make.com/) official guides
- **Tomaz @ Coding Money** (YouTube — n8n deep-dives) <!-- TODO: no verified URL found -->

### YC / Operator thinking
- [**Paul Graham essays**](https://paulgraham.com/articles.html)
- [**YC Startup School**](https://www.startupschool.org/)
- **Michael Seibel**, **Garry Tan**, **Harj Taggar** — talks <!-- TODO: no verified URL found -->
- [**Jason Lemkin (SaaStr)**](https://www.saastr.com/) — SaaS pricing & sales
- [**Lenny Rachitsky**](https://www.lennysnewsletter.com/)

### Product / GTM / Pricing
- [**a16z AI Canon**](https://a16z.com/ai-canon/)
- [**First Round Review**](https://review.firstround.com/)
- [**Marty Cagan**](https://www.svpg.com/books/inspired-how-to-create-tech-products-customers-love-2nd-edition/) — *Inspired*, *Empowered*
- [**Superhuman's onboarding playbook**](https://review.firstround.com/superhuman-onboarding-playbook/) (First Round Review)
- [**Reforge**](https://www.reforge.com/) content (Growth / Retention / Monetization)
- [**April Dunford — *Obviously Awesome***](https://www.aprildunford.com/obviously-awesome) (positioning)

### Design / Frontend
- [**Refactoring UI**](https://www.refactoringui.com/) — Steve Schoger & Adam Wathan
- [**Linear's design principles**](https://linear.app/method)
- [**Vercel**](https://vercel.com/), [**shadcn/ui**](https://ui.shadcn.com/), [**Aceternity UI**](https://ui.aceternity.com/) — reference patterns
- [**Rauno Freiberg**](https://rauno.me/) — design interactions

### Papers (must-knows)
- Vaswani et al. — [**Attention Is All You Need**](https://arxiv.org/abs/1706.03762) (2017)
- [**GPT-3**](https://arxiv.org/abs/2005.14165) (Brown et al. 2020), [**InstructGPT / RLHF**](https://arxiv.org/abs/2203.02155) (Ouyang et al.)
- [**Chinchilla**](https://arxiv.org/abs/2203.15556) (Hoffmann et al. 2022)
- [**DPO**](https://arxiv.org/abs/2305.18290) (Rafailov et al. 2023)
- [**RAG**](https://arxiv.org/abs/2005.11401) (Lewis et al. 2020)
- [**ReAct**](https://arxiv.org/abs/2210.03629) (Yao et al. 2022)
- [**Toolformer**](https://arxiv.org/abs/2302.04761) (Schick et al. 2023)

## Tracking

- Daily completion stamps live in `app/progress.db` (SQLite, per-machine).
- Sync completions across Mac/Windows via `progress.json` (optional, git-tracked).
- Streak, time-on-lesson, quiz scores all captured in-app.
