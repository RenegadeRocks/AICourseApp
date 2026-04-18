"use client";
import { useState } from "react";

interface ScopeOption {
  value: string;
  label: string;
  group: "all" | "block" | "week";
}

type Result =
  | null
  | { ok: true; stdout: string; stderr: string }
  | { ok: false; stdout: string; stderr: string; code: number | null };

export default function ExportForm({ scopes }: { scopes: ScopeOption[] }) {
  const [scope, setScope] = useState(scopes[0]?.value ?? "all");
  const [kind, setKind] = useState<"anki" | "notebooklm">("anki");
  const [pending, setPending] = useState(false);
  const [result, setResult] = useState<Result>(null);

  async function run() {
    setPending(true);
    setResult(null);
    try {
      const res = await fetch("/api/export", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ kind, scope }),
      });
      const data = (await res.json()) as {
        code: number | null;
        stdout: string;
        stderr: string;
      };
      setResult(
        res.ok
          ? { ok: true, stdout: data.stdout, stderr: data.stderr }
          : { ok: false, stdout: data.stdout, stderr: data.stderr, code: data.code },
      );
    } catch (e) {
      setResult({
        ok: false,
        stdout: "",
        stderr: e instanceof Error ? e.message : "Request failed",
        code: null,
      });
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="mt-8 rounded-lg border border-stone-200 bg-white p-6">
      <div className="grid gap-4 sm:grid-cols-[1fr_auto_auto]">
        <label className="block">
          <span className="text-xs uppercase tracking-wider text-stone-500">Scope</span>
          <select
            value={scope}
            onChange={(e) => setScope(e.target.value)}
            className="mt-1 w-full rounded border border-stone-300 bg-white px-3 py-2 text-sm"
          >
            {scopes.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-xs uppercase tracking-wider text-stone-500">Kind</span>
          <select
            value={kind}
            onChange={(e) => setKind(e.target.value as "anki" | "notebooklm")}
            className="mt-1 rounded border border-stone-300 bg-white px-3 py-2 text-sm"
          >
            <option value="anki">Anki (.apkg)</option>
            <option value="notebooklm">NotebookLM pack</option>
          </select>
        </label>
        <button
          onClick={run}
          disabled={pending}
          className="mt-5 sm:mt-auto rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:bg-amber-700 disabled:opacity-50 transition"
        >
          {pending ? "Running…" : "Build export"}
        </button>
      </div>

      {result && (
        <div className="mt-6 text-sm">
          <div
            className={`font-medium ${
              result.ok ? "text-emerald-700" : "text-red-700"
            }`}
          >
            {result.ok ? "✓ Export completed" : "✗ Export failed"}
          </div>
          {result.stdout && (
            <details className="mt-3" open>
              <summary className="cursor-pointer text-stone-500">stdout</summary>
              <pre className="mt-2 bg-stone-900 text-stone-100 rounded p-3 overflow-x-auto text-xs">
                {result.stdout}
              </pre>
            </details>
          )}
          {result.stderr && (
            <details className="mt-3" open={!result.ok}>
              <summary className="cursor-pointer text-stone-500">stderr</summary>
              <pre className="mt-2 bg-stone-900 text-stone-100 rounded p-3 overflow-x-auto text-xs">
                {result.stderr}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
