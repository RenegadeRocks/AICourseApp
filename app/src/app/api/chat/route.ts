import { NextResponse } from "next/server";
import { z } from "zod";
import Anthropic from "@anthropic-ai/sdk";
import { searchVaultForChat } from "@/lib/search";

const Body = z.object({
  query: z.string().min(1).max(2000),
  history: z
    .array(
      z.object({
        role: z.enum(["user", "assistant"]),
        content: z.string(),
      }),
    )
    .default([]),
});

const MODEL = "claude-sonnet-4-6";
const MAX_TOKENS = 2048;
const TOP_K = 6;

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const { query, history } = parsed.data;

  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json(
      {
        error:
          "ANTHROPIC_API_KEY is not set. Add it to app/.env.local to enable chat.",
      },
      { status: 500 },
    );
  }

  const hits = searchVaultForChat(query, TOP_K);
  if (hits.length === 0) {
    return NextResponse.json({
      answer:
        "I couldn't find anything in the vault that matches that query. Try different keywords, or check that vault content is present.",
      sources: [],
    });
  }

  // Build the retrieval context. Each chunk is wrapped in a tagged block so
  // the model can cite specific sources by index.
  const contextBlocks = hits
    .map(
      (h, i) =>
        `<source index="${i + 1}" path="${h.path}" title="${escapeAttr(
          h.title,
        )}">\n${h.excerpt}\n</source>`,
    )
    .join("\n\n");

  const system = `You are a study assistant for the AI Catalyst C3 vault. Answer the user's question using ONLY the information in the <source> tags below. If the answer is not in the sources, say so plainly — do not fabricate.

When you use a specific claim from a source, cite it inline as [^N] where N is the source index. Keep answers concise but include the numeric or named specifics (operator names, benchmark numbers, dates, model IDs) from the sources.

<sources>
${contextBlocks}
</sources>`;

  const client = new Anthropic();

  try {
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      system,
      messages: [
        ...history.map((m) => ({ role: m.role, content: m.content })),
        { role: "user" as const, content: query },
      ],
    });
    const answer = response.content
      .filter((c) => c.type === "text")
      .map((c) => (c as { type: "text"; text: string }).text)
      .join("");
    return NextResponse.json({
      answer,
      sources: hits.map((h, i) => ({
        index: i + 1,
        title: h.title,
        path: h.path,
      })),
      usage: response.usage,
    });
  } catch (err) {
    return NextResponse.json(
      {
        error: err instanceof Error ? err.message : "Claude API call failed",
      },
      { status: 500 },
    );
  }
}

function escapeAttr(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
}
