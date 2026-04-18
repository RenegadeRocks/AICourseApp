import { NextResponse } from "next/server";
import { z } from "zod";
import { spawn } from "node:child_process";
import path from "node:path";
import { PROJECT_ROOT } from "@/lib/paths";

const Body = z.object({
  kind: z.enum(["anki", "notebooklm"]),
  scope: z.string().min(1),
});

/**
 * Spawn `python scripts/<kind>_export.py <scope>` and return its exit code,
 * stdout, stderr. Assumes Python is on PATH and scripts/requirements.txt is
 * installed.
 */
export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const { kind, scope } = parsed.data;
  const scriptRel =
    kind === "anki" ? "scripts/anki_export.py" : "scripts/notebooklm_export.py";
  const scriptAbs = path.join(PROJECT_ROOT, scriptRel);

  const result = await runPython([scriptAbs, scope]);
  return NextResponse.json(result, { status: result.code === 0 ? 200 : 500 });
}

function runPython(args: string[]): Promise<{
  code: number | null;
  stdout: string;
  stderr: string;
}> {
  return new Promise((resolve) => {
    const pyExe = process.platform === "win32" ? "python" : "python3";
    const child = spawn(pyExe, args, { cwd: PROJECT_ROOT });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d.toString()));
    child.stderr.on("data", (d) => (stderr += d.toString()));
    child.on("close", (code) => resolve({ code, stdout, stderr }));
    child.on("error", (err) =>
      resolve({ code: 1, stdout, stderr: String(err) }),
    );
  });
}
