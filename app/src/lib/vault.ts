import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeHighlight from "rehype-highlight";
import rehypeStringify from "rehype-stringify";
import { VAULT_ROOT } from "./paths";

export interface VaultFile {
  /** Slug path from vault root, POSIX-separated, without extension. */
  slug: string[];
  /** Absolute filesystem path. */
  absPath: string;
  /** Parsed frontmatter. */
  data: Record<string, unknown>;
  /** Raw markdown body. */
  body: string;
}

export interface RenderedFile extends VaultFile {
  html: string;
  readingMinutes: number;
}

export function listVaultFiles(): VaultFile[] {
  const out: VaultFile[] = [];
  const walk = (dir: string, parts: string[]) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full, [...parts, entry.name]);
      } else if (entry.isFile() && entry.name.endsWith(".md")) {
        const slug = [...parts, entry.name.replace(/\.md$/, "")];
        const raw = fs.readFileSync(full, "utf-8");
        const { data, content } = matter(raw);
        out.push({ slug, absPath: full, data, body: content });
      }
    }
  };
  if (fs.existsSync(VAULT_ROOT)) walk(VAULT_ROOT, []);
  return out;
}

export function readVaultFile(slugParts: string[]): VaultFile | null {
  const candidate = path.join(VAULT_ROOT, ...slugParts) + ".md";
  if (!fs.existsSync(candidate)) return null;
  const raw = fs.readFileSync(candidate, "utf-8");
  const { data, content } = matter(raw);
  return { slug: slugParts, absPath: candidate, data, body: content };
}

export async function render(file: VaultFile): Promise<RenderedFile> {
  // Resolve [[wikilinks]] to /vault/<slug> routes before parsing.
  const bodyWithLinks = file.body.replace(
    /\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]/g,
    (_m, target: string, label?: string) => {
      const t = target.trim();
      // Treat "00-program/index" etc. as vault slugs.
      const href = `/vault/${t.replace(/^\/+/, "")}`;
      return `[${(label ?? t).trim()}](${href})`;
    }
  );
  const processed = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype)
    .use(rehypeSlug)
    .use(rehypeAutolinkHeadings, { behavior: "wrap" })
    .use(rehypeHighlight)
    .use(rehypeStringify)
    .process(bodyWithLinks);
  const words = file.body.split(/\s+/).filter(Boolean).length;
  return {
    ...file,
    html: String(processed),
    readingMinutes: Math.max(1, Math.round(words / 220)),
  };
}
