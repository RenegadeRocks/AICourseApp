# Week 12 code-lab — MVP AI product skeleton

A thin backend + a streaming AI endpoint + a minimal AI-native frontend, in
**zero runtime dependencies** (native `node:http` + native `fetch`, Node 20+).
It is deliberately framework-free so you can read every line of the
request → model → SSE stream → render loop the lessons teach. The production
stack the lessons recommend (Next.js 16 + Vercel AI SDK v5) is shown at the
bottom, mapped 1:1.

## What it demonstrates

| Lesson | In this lab |
|---|---|
| Mon — usability floor | `public/index.html`: AA-contrast colors, visible focus ring, 48px primary target (Fitts), example-prompt empty state |
| Tue — AI-native UX | optimistic render of the user message, token streaming into a placeholder, graceful failure that **preserves input** with a Retry |
| Thu — thin backend | `src/server.ts`: server-side-only API key, per-caller rate limit, input validation, per-call cost logging |
| Fri — streaming loop | `POST /api/generate` streams SSE; the client reads the stream and renders tokens as they arrive |

## Run it

```bash
cp .env.example .env          # then paste a real ANTHROPIC_API_KEY into .env
npm install                   # dev-only deps: typescript, eslint
npm run typecheck             # tsc --noEmit  -> passes clean
npm run lint                  # eslint src    -> passes clean
export $(grep -v '^#' .env | xargs)   # load env (or use a dotenv runner)
npm run dev                   # tsc + node dist/server.js
# open http://localhost:3000
```

Verified on Node 20+: `npm run typecheck` and `npm run lint` both exit 0.

### Pass-bar checks (Saturday)

```bash
# 1. Tokens stream (not one dump): watch them appear in the browser, or:
curl -N -X POST localhost:3000/api/generate \
  -H 'content-type: application/json' \
  -d '{"prompt":"count slowly to five"}'      # you see event: token frames arrive incrementally

# 2. The key is NOT in anything the browser receives:
grep -r "sk-ant" dist/ public/ ; echo "exit=$?"   # must find nothing (exit 1)

# 3. Failure preserves input: stop your network mid-stream ->
#    the assistant bubble shows a recoverable error + Retry, and Retry
#    refills your prompt. (Kill wifi, or point ANTHROPIC_API_KEY at a bad value.)

# 4. Cost is metered: every generation logs a line like
#    [generate] caller=... in=12 out=210 cost=$0.00213
```

## How the streaming works (the load-bearing part)

1. Browser `POST`s `{prompt}` to `/api/generate`.
2. Server rate-limits the caller, validates the prompt, then calls Anthropic's
   `/v1/messages` with `stream: true` using the **server-side** key.
3. Anthropic streams SSE frames (`content_block_delta` → `text_delta`). The
   server parses each and re-emits `event: token / data: {"text":"..."}` to the
   browser.
4. The client reads its own response body with `reader.read()`, splits on
   `\n\n`, and appends each token's text to the assistant bubble.
5. On completion the server logs tokens + cost and sends `event: done`.

## Deploy path

**Any Node host (Render / Railway / Fly / a VM):**

1. Set the env var `ANTHROPIC_API_KEY` (and optionally `ANTHROPIC_MODEL`,
   `PORT`) in the host's dashboard — never in the repo.
2. Build command: `npm install && npm run build`.
3. Start command: `npm start` (runs `node dist/server.js`).
4. The host provides `PORT`; the server already reads `process.env.PORT`.

**Production stack the lessons teach (recommended for a real product):**

Port this lab to **Next.js 16 + Vercel AI SDK v5**, deploy to Vercel with
`vercel deploy`, set `ANTHROPIC_API_KEY` in Vercel project env vars. The
streaming route becomes:

```ts
// app/api/generate/route.ts
import { anthropic } from "@ai-sdk/anthropic";
import { streamText } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({ model: anthropic("claude-sonnet-5"), messages });
  return result.toUIMessageStreamResponse();   // SSE, handled by the SDK
}
```

```tsx
// app/page.tsx  (Client Component)
"use client";
import { useChat } from "@ai-sdk/react";

export default function Page() {
  const { messages, sendMessage, status } = useChat();
  // render messages (streaming), an example-prompt empty state,
  // and a failure state that preserves input — same patterns as this lab.
}
```

Add Supabase for auth + a `generations` table (persist prompt, response,
tokens, cost) and a per-user rate limit, exactly as the Thursday lesson
specifies. For long multi-step agents that exceed the serverless timeout, move
the work to Inngest or Vercel Workflows (Friday's "slow loop").

## Security notes

- The API key is read from `process.env` and used only inside the server. It is
  never sent to the browser. `grep -r sk-ant dist public` finds nothing.
- Input is length-capped and type-checked. This is the prompt-injection surface;
  in a real product with tools, apply the Block 3 agent-hardening material.
- The in-memory rate limit resets on restart. Use Redis/Upstash in production.
