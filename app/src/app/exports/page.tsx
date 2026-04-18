import fs from "node:fs";
import path from "node:path";
import { VAULT_ROOT } from "@/lib/paths";
import ExportForm from "./ExportForm";

export interface ScopeOption {
  value: string; // arg to pass to the python script
  label: string; // human-readable dropdown entry
  group: "all" | "block" | "week";
}

/**
 * Build the scope dropdown options from the vault tree so the UI stays in
 * sync with whatever content is on disk — no hardcoded lists.
 */
function buildScopes(): ScopeOption[] {
  const scopes: ScopeOption[] = [{ value: "all", label: "All weeks (entire vault)", group: "all" }];
  if (!fs.existsSync(VAULT_ROOT)) return scopes;

  const blocks = fs
    .readdirSync(VAULT_ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith("block-"))
    .map((d) => d.name)
    .sort();

  for (const block of blocks) {
    scopes.push({ value: block, label: prettyBlock(block), group: "block" });
    const weeks = fs
      .readdirSync(path.join(VAULT_ROOT, block), { withFileTypes: true })
      .filter((d) => d.isDirectory() && d.name.startsWith("week-"))
      .map((d) => d.name)
      .sort();
    for (const week of weeks) {
      scopes.push({
        value: `${block}/${week}`,
        label: `${prettyBlock(block)} · ${prettyWeek(week)}`,
        group: "week",
      });
    }
  }
  return scopes;
}

function prettyBlock(name: string) {
  const match = name.match(/^block-(\d+)(?:-(.+))?$/);
  if (!match) return name;
  const rest = match[2] ? ` · ${match[2].replace(/-/g, " ")}` : "";
  return `Block ${parseInt(match[1], 10)}${rest}`;
}

function prettyWeek(name: string) {
  const match = name.match(/^week-(\d+)(?:-(.+))?$/);
  if (!match) return name;
  const rest = match[2] ? ` · ${match[2].replace(/--+/g, " · ").replace(/-/g, " ")}` : "";
  return `Week ${parseInt(match[1], 10)}${rest}`;
}

export default function ExportsPage() {
  const scopes = buildScopes();
  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Exports</h1>
      <p className="mt-2 text-stone-600 text-sm">
        Bundle lessons for offline study. Anki: importable <code>.apkg</code> decks
        from each week&rsquo;s <code>06-flashcards.md</code>. NotebookLM: cleaned
        Markdown packs with frontmatter stripped and wikilinks flattened.
      </p>
      <ExportForm scopes={scopes} />
      <div className="mt-10 text-sm text-stone-500 space-y-2">
        <p>
          <strong>Requirements:</strong> Python 3 on PATH and{" "}
          <code>pip install -r scripts/requirements.txt</code> (genanki).
        </p>
        <p>
          Outputs land in <code>exports/anki/</code> and
          <code> vault/&lt;scope&gt;/07-notebooklm-pack/</code>.
        </p>
      </div>
    </div>
  );
}
