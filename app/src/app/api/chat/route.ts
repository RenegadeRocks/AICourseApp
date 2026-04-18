import { NextResponse } from "next/server";
import { z } from "zod";
import { spawn } from "node:child_process";
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

const TOP_K = 6;
const CLI_TIMEOUT_MS = 120_000;

/**
 * Chat-with-vault route. Uses the local `claude` CLI (Claude Max subscription)
 * instead of the Anthropic API — no API key required. The CLI is invoked in
 * non-interactive print mode with the full prompt on stdin.
 */
export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const { query, history } = parsed.data;

  const hits = searchVaultForChat(query, TOP_K);
  if (hits.length === 0) {
    return NextResponse.json({
      answer:
        "I couldn't find anything in the vault that matches that query. Try different keywords, or check that vault content is present.",
      sources: [],
    });
  }

  const contextBlocks = hits
    .map(
      (h, i) =>
        `<source index="${i + 1}" path="${h.path}" title="${escapeAttr(
          h.title,
        )}">\n${h.excerpt}\n</source>`,
    )
    .join("\n\n");

  const historyTurns = history
    .map((m) => `${m.role.toUpperCase()}: ${m.content}`)
    .join("\n\n");

  // Claude Code's print mode doesn't accept a separate system prompt, so we
  // flatten everything into one prompt. The model is instructed to behave as
  // a retrieval-grounded study assistant and cite by [^N].
  const prompt = `You are a study assistant for the AI Pro-level Course vault. Answer the user's question using ONLY the information in the <source> tags below. If the answer is not in the sources, say so plainly — do not fabricate.

When you use a specific claim from a source, cite it inline as [^N] where N is the source index. Keep answers concise but include the numeric or named specifics (operator names, benchmark numbers, dates, model IDs) from the sources.

<sources>
${contextBlocks}
</sources>

${historyTurns ? `Conversation so far:\n${historyTurns}\n\n` : ""}USER: ${query}

ASSISTANT:`;

  try {
    const { stdout, code, stderr } = await runClaudeCli(prompt);
    if (code !== 0) {
      return NextResponse.json(
        {
          error: `claude CLI exited with code ${code}: ${stderr.slice(0, 500)}`,
        },
        { status: 500 },
      );
    }
    return NextResponse.json({
      answer: stdout.trim(),
      sources: hits.map((h, i) => ({
        index: i + 1,
        title: h.title,
        path: h.path,
      })),
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json(
      {
        error:
          msg.includes("ENOENT")
            ? "The `claude` CLI was not found on PATH. Install Claude Code and ensure `claude` runs from your shell."
            : msg,
      },
      { status: 500 },
    );
  }
}

/**
 * Run `claude -p` (print mode) with the prompt on stdin. Resolves with the
 * full stdout, exit code, and stderr once the process closes.
 */
function runClaudeCli(prompt: string): Promise<{
  stdout: string;
  stderr: string;
  code: number | null;
}> {
  return new Promise((resolve, reject) => {
    const child = spawn("claude", ["-p"], {
      stdio: ["pipe", "pipe", "pipe"],
      // Windows needs the shell flag to resolve `claude.cmd` from PATH.
      shell: process.platform === "win32",
    });

    let stdout = "";
    let stderr = "";
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill();
      reject(new Error(`claude CLI timed out after ${CLI_TIMEOUT_MS}ms`));
    }, CLI_TIMEOUT_MS);

    child.stdout.on("data", (d) => (stdout += d.toString()));
    child.stderr.on("data", (d) => (stderr += d.toString()));
    child.on("error", (err) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      reject(err);
    });
    child.on("close", (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ stdout, stderr, code });
    });

    child.stdin.write(prompt);
    child.stdin.end();
  });
}

function escapeAttr(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
}
