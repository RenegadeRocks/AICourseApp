/**
 * MVP AI product backend — a thin backend with a streaming AI endpoint.
 *
 * Demonstrates the Week 12 backend lesson in ~200 lines with ZERO runtime
 * dependencies (native `node:http` + native `fetch`, Node 20+). The concepts
 * map 1:1 onto the Next.js + Vercel AI SDK stack the lessons teach; see README.
 *
 * Responsibilities (Thursday's "thin backend"):
 *   1. Hold the ANTHROPIC_API_KEY server-side only (never reaches the browser).
 *   2. Authenticate/identify the caller (here: by IP — a real app uses Supabase Auth).
 *   3. Rate-limit per caller so one user cannot run up the API bill.
 *   4. Validate input (prompt-injection surface).
 *   5. Stream the model response to the browser over SSE.
 *   6. Log tokens + cost per call (unit economics from day one).
 */

import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const PORT = Number(process.env.PORT ?? 3000);
const API_KEY = process.env.ANTHROPIC_API_KEY ?? "";
const MODEL = process.env.ANTHROPIC_MODEL ?? "claude-sonnet-5";
// Sonnet 5 intro pricing, USD per million tokens (verify current before pricing a product).
const PRICE_IN = 2 / 1_000_000;
const PRICE_OUT = 10 / 1_000_000;

// --- naive per-caller rate limit (in-memory; a real app uses Redis/Upstash) ---
const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = 10;
const hits = new Map<string, number[]>();

function rateLimited(caller: string): boolean {
  const now = Date.now();
  const recent = (hits.get(caller) ?? []).filter((t) => now - t < WINDOW_MS);
  recent.push(now);
  hits.set(caller, recent);
  return recent.length > MAX_PER_WINDOW;
}

// --- SSE helpers ---
function sse(res: ServerResponse, event: string, data: unknown): void {
  res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);
}

interface AnthropicDelta {
  type: string;
  delta?: { type?: string; text?: string };
  usage?: { input_tokens?: number; output_tokens?: number };
  message?: { usage?: { input_tokens?: number } };
}

async function readBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) chunks.push(chunk as Buffer);
  return Buffer.concat(chunks).toString("utf-8");
}

/** Stream a generation from Anthropic to the browser over SSE. */
async function handleGenerate(req: IncomingMessage, res: ServerResponse): Promise<void> {
  const caller = req.socket.remoteAddress ?? "unknown";

  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    Connection: "keep-alive",
  });

  // 1. Rate limit before spending a token.
  if (rateLimited(caller)) {
    sse(res, "error", { message: "Rate limit reached. Try again in a minute." });
    res.end();
    return;
  }

  // 2. Validate input (never trust the body; this is the prompt-injection surface).
  let prompt = "";
  try {
    const body = JSON.parse(await readBody(req)) as { prompt?: unknown };
    if (typeof body.prompt !== "string" || body.prompt.trim().length === 0) {
      sse(res, "error", { message: "A non-empty prompt is required." });
      res.end();
      return;
    }
    prompt = body.prompt.slice(0, 4000); // cap length
  } catch {
    sse(res, "error", { message: "Invalid request body." });
    res.end();
    return;
  }

  if (!API_KEY) {
    sse(res, "error", { message: "Server is not configured (missing ANTHROPIC_API_KEY)." });
    res.end();
    return;
  }

  // 3. Call the model with the SERVER-SIDE key and stream the result.
  let inputTokens = 0;
  let outputTokens = 0;
  try {
    const upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 1024,
        stream: true,
        messages: [{ role: "user", content: prompt }],
      }),
    });

    if (!upstream.ok || upstream.body === null) {
      sse(res, "error", { message: `Model error (${upstream.status}). Please retry.` });
      res.end();
      return;
    }

    const reader = upstream.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const frames = buffer.split("\n\n");
      buffer = frames.pop() ?? "";
      for (const frame of frames) {
        const dataLine = frame.split("\n").find((l) => l.startsWith("data: "));
        if (dataLine === undefined) continue;
        const json = dataLine.slice(6);
        if (json === "[DONE]") continue;
        let evt: AnthropicDelta;
        try {
          evt = JSON.parse(json) as AnthropicDelta;
        } catch {
          continue;
        }
        if (evt.type === "message_start") {
          inputTokens = evt.message?.usage?.input_tokens ?? 0;
        } else if (evt.type === "content_block_delta" && evt.delta?.type === "text_delta") {
          sse(res, "token", { text: evt.delta.text ?? "" });
        } else if (evt.type === "message_delta") {
          outputTokens = evt.usage?.output_tokens ?? outputTokens;
        }
      }
    }

    // 4. Meter cost per call (Thursday's rule). A real app persists this.
    const cost = inputTokens * PRICE_IN + outputTokens * PRICE_OUT;
    console.log(
      `[generate] caller=${caller} in=${inputTokens} out=${outputTokens} cost=$${cost.toFixed(5)}`,
    );
    sse(res, "done", { inputTokens, outputTokens, cost });
    res.end();
  } catch {
    // 5. Graceful failure: the client preserves the user's input and offers retry.
    sse(res, "error", { message: "The generation failed. Your prompt is preserved — retry." });
    res.end();
  }
}

async function serveFile(res: ServerResponse, absPath: string, type: string): Promise<void> {
  try {
    const body = await readFile(absPath);
    res.writeHead(200, { "Content-Type": type });
    res.end(body);
  } catch {
    res.writeHead(404).end("Not found");
  }
}

const server = createServer((req, res) => {
  const url = req.url ?? "/";
  if (req.method === "POST" && url === "/api/generate") {
    void handleGenerate(req, res);
  } else if (url === "/app.js") {
    // The client is compiled from src/client.ts and sits next to this file in dist/.
    void serveFile(res, join(__dirname, "client.js"), "text/javascript");
  } else if (url === "/" || url === "/index.html") {
    void serveFile(res, join(__dirname, "..", "public", "index.html"), "text/html");
  } else {
    res.writeHead(404).end("Not found");
  }
});

server.listen(PORT, () => {
  console.log(`MVP AI backend on http://localhost:${PORT} (model=${MODEL})`);
});
