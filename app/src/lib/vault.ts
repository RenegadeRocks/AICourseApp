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

/**
 * Resolve the actual lesson file basename for a given day-of-cycle by scanning
 * the week directory. Files are authored with topic-based slugs (e.g.
 * `01-mon-mental-model-of-llms.md`), so we match by the numeric prefix
 * `0{dayIndex}-` rather than trying to construct the slug from the schedule.
 *
 * Returns the basename without `.md`, or null if no matching file exists.
 */
export function resolveDayFileBasename(
  blockId: string,
  weekFolder: string,
  dayIndex: number, // 1..7
): string | null {
  const weekDir = path.join(VAULT_ROOT, blockId, weekFolder);
  if (!fs.existsSync(weekDir)) return null;
  const prefix = `0${dayIndex}-`;
  const match = fs
    .readdirSync(weekDir)
    .find((name) => name.startsWith(prefix) && name.endsWith(".md"));
  return match ? match.replace(/\.md$/, "") : null;
}

/**
 * Find the vault folder name for a given block + week id. Folder names include
 * the week id prefix (e.g. `week-01-<slug>`), so we match by prefix rather
 * than hard-coding a map.
 */
export function findWeekFolder(blockId: string, weekId: string): string {
  const blockDir = path.join(VAULT_ROOT, blockId);
  if (!fs.existsSync(blockDir)) return weekId;
  const match = fs
    .readdirSync(blockDir)
    .find((name) => name.startsWith(`${weekId}-`) || name === weekId);
  return match ?? weekId;
}

/**
 * Extract the title from the first H1 in the markdown body, or null if none.
 * Strips the body's leading H1 from the rendered output so the caller can
 * render it as the page heading without duplication.
 */
export function extractTitle(body: string): { title: string | null; bodyWithoutH1: string } {
  const match = body.match(/^[ \t]*#\s+(.+?)\s*$/m);
  if (!match) return { title: null, bodyWithoutH1: body };
  const title = match[1].trim();
  const bodyWithoutH1 = body.replace(match[0], "").replace(/^\s*\n/, "");
  return { title, bodyWithoutH1 };
}

export async function render(file: VaultFile): Promise<RenderedFile> {
  // Extract the leading H1 as the page title so we can render it once in the
  // layout instead of having both the <h1 class="page-title"> and a duplicate
  // <h1> inside the prose.
  const { bodyWithoutH1 } = extractTitle(file.body);
  // Resolve [[wikilinks]] to /vault/<slug> routes before parsing.
  const bodyWithLinks = bodyWithoutH1.replace(
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
    .use(rehypeAutolinkHeadings, {
      // "append" adds a small anchor link after the heading text instead of
      // wrapping the heading in a link — keeps heading typography clean.
      behavior: "append",
      properties: { className: ["heading-anchor"], ariaLabel: "Link to heading" },
      content: { type: "text", value: "#" },
    })
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

/**
 * Produce an ordered list of lesson-file slugs across the vault, suitable for
 * prev/next navigation. Only includes files inside a `week-NN-*` directory so
 * program-level docs (00-program/*) don't interleave with daily lessons.
 *
 * Ordering: block-id alpha → week-NN numeric → file-prefix numeric (00-overview
 * sits before 01-mon, 07-sun-synthesis last in the week).
 */
export interface LessonRef {
  slug: string[]; // path parts, no extension
  title: string;
  block: string;
  week: string;
  day: number; // 0 = overview, 1..7 = Mon..Sun
}

export function listLessonsInOrder(): LessonRef[] {
  const all = listVaultFiles();
  const lessons: LessonRef[] = [];
  for (const f of all) {
    if (f.slug.length < 3) continue;
    const [block, week, file] = [f.slug[0], f.slug[1], f.slug[f.slug.length - 1]];
    if (!week.startsWith("week-")) continue;
    // Only include files at the week root (depth === 3), skip nested dirs.
    if (f.slug.length !== 3) continue;
    const prefixMatch = file.match(/^0(\d)-/);
    if (!prefixMatch) continue;
    const day = parseInt(prefixMatch[1], 10);
    const frontmatterTitle =
      typeof f.data.title === "string" && f.data.title.trim().length > 0
        ? f.data.title.trim()
        : null;
    const { title: h1Title } = extractTitle(f.body);
    const title = frontmatterTitle ?? h1Title ?? prettifySlugPart(file);
    lessons.push({ slug: f.slug, title, block, week, day });
  }
  // Sort: block (alpha) → week numeric → day numeric.
  lessons.sort((a, b) => {
    if (a.block !== b.block) return a.block.localeCompare(b.block);
    const aw = parseInt((a.week.match(/week-(\d+)/)?.[1] ?? "0"), 10);
    const bw = parseInt((b.week.match(/week-(\d+)/)?.[1] ?? "0"), 10);
    if (aw !== bw) return aw - bw;
    return a.day - b.day;
  });
  return lessons;
}

export function siblingLessons(currentSlug: string[]): {
  prev: LessonRef | null;
  next: LessonRef | null;
  current: LessonRef | null;
} {
  const ordered = listLessonsInOrder();
  const key = currentSlug.join("/");
  const idx = ordered.findIndex((l) => l.slug.join("/") === key);
  if (idx === -1) return { prev: null, next: null, current: null };
  return {
    prev: idx > 0 ? ordered[idx - 1] : null,
    next: idx < ordered.length - 1 ? ordered[idx + 1] : null,
    current: ordered[idx],
  };
}

/**
 * Prettify a folder / file slug for display in breadcrumbs.
 * "week-05-ai-that-reads-your-business..." → "Week 5 · AI that reads your business..."
 */
export function prettifySlugPart(part: string): string {
  // Week/Block numeric prefix
  const weekMatch = part.match(/^week-(\d+)(?:-(.+))?$/);
  if (weekMatch) {
    const n = parseInt(weekMatch[1], 10);
    const rest = weekMatch[2] ? ` · ${weekMatch[2].replace(/--+/g, " · ").replace(/-/g, " ")}` : "";
    return `Week ${n}${rest}`;
  }
  const blockMatch = part.match(/^block-(\d+)(?:-(.+))?$/);
  if (blockMatch) {
    const n = parseInt(blockMatch[1], 10);
    const rest = blockMatch[2] ? ` · ${blockMatch[2].replace(/-/g, " ")}` : "";
    return `Block ${n}${rest}`;
  }
  // Day-prefixed lesson: "01-mon-foo-bar" → "Mon · foo bar"
  const dayMatch = part.match(/^0(\d)-(mon|tue|wed|thu|fri|sat|sun)-(.+)$/);
  if (dayMatch) {
    const dayName = dayMatch[2].charAt(0).toUpperCase() + dayMatch[2].slice(1);
    const topic = dayMatch[3].replace(/-/g, " ");
    return `${dayName} · ${topic}`;
  }
  if (part === "00-overview") return "Overview";
  // Fallback: de-hyphenate, collapse double-dashes
  return part.replace(/--+/g, " · ").replace(/-/g, " ");
}
