// eslint-disable-next-line @typescript-eslint/no-explicit-any
import FlexSearch from "flexsearch";
import { listVaultFiles, extractTitle, prettifySlugPart } from "./vault";

type Doc = { id: string; title: string; body: string; path: string };

// FlexSearch's bundled types pre-date Document store options; cast to any.
let _idx: any = null;
let _docs: Map<string, Doc> | null = null;

function build() {
  const idx: any = new (FlexSearch as any).Document({
    document: {
      id: "id",
      index: ["title", "body"],
      store: ["title", "path"],
    },
    tokenize: "forward",
  });
  const docs = new Map<string, Doc>();
  for (const f of listVaultFiles()) {
    const id = f.slug.join("/");
    const frontmatterTitle =
      typeof f.data.title === "string" && f.data.title.trim().length > 0
        ? f.data.title.trim()
        : null;
    const { title: h1Title } = extractTitle(f.body);
    const title =
      frontmatterTitle ?? h1Title ?? prettifySlugPart(f.slug[f.slug.length - 1]);
    const doc = { id, title, body: f.body, path: id };
    idx.add(doc);
    docs.set(id, doc);
  }
  _idx = idx;
  _docs = docs;
}

/**
 * RAG variant: returns top hits with a body excerpt suitable for stuffing
 * into a Claude context window. Excerpts are centered on the first
 * occurrence of a query term, or the document head if no match is found.
 */
export function searchVaultForChat(
  query: string,
  limit = 6,
  excerptChars = 2400,
): Array<{ id: string; title: string; path: string; excerpt: string }> {
  if (!_idx || !_docs) build();
  const hits = searchVault(query, limit);
  const lowerTerms = query
    .toLowerCase()
    .split(/\s+/)
    .filter((t) => t.length > 2);
  return hits.slice(0, limit).map((h) => {
    const doc = _docs!.get(h.id);
    const body = doc?.body ?? "";
    // Find the first match of any query term; fall back to the document head.
    let start = 0;
    for (const term of lowerTerms) {
      const idx = body.toLowerCase().indexOf(term);
      if (idx >= 0) {
        start = Math.max(0, idx - 200);
        break;
      }
    }
    const excerpt = body.slice(start, start + excerptChars);
    return { id: h.id, title: h.title, path: h.path, excerpt };
  });
}

export function searchVault(query: string, limit = 20) {
  if (!_idx || !_docs) build();
  const results = _idx.search(query, { limit, enrich: true }) as Array<{
    field: string;
    result: Array<{ id: string; doc: Doc }>;
  }>;
  const seen = new Set<string>();
  const out: Array<{ id: string; title: string; path: string; field: string }> = [];
  for (const { field, result } of results) {
    for (const r of result) {
      if (seen.has(r.id)) continue;
      seen.add(r.id);
      out.push({ id: r.id, title: r.doc.title, path: r.doc.path, field });
    }
  }
  return out;
}
