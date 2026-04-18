import { notFound } from "next/navigation";
import Link from "next/link";
import type { Route } from "next";
import { readVaultFile, render, extractTitle, prettifySlugPart, siblingLessons } from "@/lib/vault";
import { slotForVaultSlug, slotKey } from "@/lib/schedule";
import { isLessonCompleted } from "@/lib/db";
import CompleteButton from "./CompleteButton";

export default async function VaultPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const file = readVaultFile(slug);
  if (!file) return notFound();
  const rendered = await render(file);

  const frontmatterTitle =
    typeof file.data.title === "string" && file.data.title.trim().length > 0
      ? file.data.title.trim()
      : null;
  const { title: h1Title } = extractTitle(file.body);
  const title = frontmatterTitle ?? h1Title ?? prettifySlugPart(slug[slug.length - 1]);

  const crumbs = slug.map((part, i) => ({
    label: prettifySlugPart(part),
    href: `/vault/${slug.slice(0, i + 1).join("/")}`,
  }));

  const { prev, next } = siblingLessons(slug);

  // Map this vault slug back to a program slot so we can show week/day context
  // and wire the Mark-complete button.
  const slot = slotForVaultSlug(slug);
  const slotKeyStr = slot ? slotKey(slot) : null;
  const positionLabel = slot
    ? `Week ${slot.weekInProgram} · Day ${slot.day_of_cycle} · ${slot.day_name.toUpperCase()}`
    : null;
  const done = slotKeyStr ? isLessonCompleted(slotKeyStr) : false;

  return (
    <div>
      <nav className="text-sm text-stone-500 flex flex-wrap items-center gap-x-1">
        <Link href="/" className="hover:text-accent hover:underline">home</Link>
        {crumbs.map((crumb, i) => (
          <span key={i} className="flex items-center gap-x-1">
            <span className="text-stone-300">/</span>
            {i < crumbs.length - 1 ? (
              <Link href={crumb.href as Route} className="hover:text-accent hover:underline">
                {crumb.label}
              </Link>
            ) : (
              <span className="text-stone-700">{crumb.label}</span>
            )}
          </span>
        ))}
      </nav>
      <h1 className="mt-4 text-3xl font-bold tracking-tight leading-tight">{title}</h1>
      <div className="mt-1 flex items-center gap-3 text-xs text-stone-500">
        <span>{rendered.readingMinutes} min read</span>
        {positionLabel && (
          <>
            <span className="text-stone-300">·</span>
            <span>{positionLabel}</span>
          </>
        )}
      </div>
      {slotKeyStr && positionLabel && (
        <div className="mt-4">
          <CompleteButton
            slotKey={slotKeyStr}
            slug={slug.join("/")}
            label={`Week ${slot!.weekInProgram} · Day ${slot!.day_of_cycle}`}
            initiallyDone={done}
          />
        </div>
      )}
      <article
        className="prose-lesson mt-8"
        dangerouslySetInnerHTML={{ __html: rendered.html }}
      />
      {slotKeyStr && positionLabel && !done && (
        <div className="mt-12 flex justify-end">
          <CompleteButton
            slotKey={slotKeyStr}
            slug={slug.join("/")}
            label={`Week ${slot!.weekInProgram} · Day ${slot!.day_of_cycle}`}
            initiallyDone={false}
          />
        </div>
      )}
      <PrevNextNav prev={prev} next={next} />
    </div>
  );
}

function PrevNextNav({
  prev,
  next,
}: {
  prev: ReturnType<typeof siblingLessons>["prev"];
  next: ReturnType<typeof siblingLessons>["next"];
}) {
  if (!prev && !next) return null;
  return (
    <nav
      aria-label="Lesson navigation"
      className="mt-16 pt-6 border-t border-stone-200 grid grid-cols-1 sm:grid-cols-2 gap-4 not-prose"
    >
      {prev ? (
        <Link
          href={`/vault/${prev.slug.join("/")}` as Route}
          className="group block rounded-lg border border-stone-200 bg-white px-4 py-3 hover:border-accent hover:bg-stone-50 transition"
        >
          <div className="text-xs uppercase tracking-wider text-stone-500 group-hover:text-accent">
            ← Previous
          </div>
          <div className="mt-1 font-medium text-ink line-clamp-2">{prev.title}</div>
        </Link>
      ) : (
        <div />
      )}
      {next ? (
        <Link
          href={`/vault/${next.slug.join("/")}` as Route}
          className="group block rounded-lg border border-stone-200 bg-white px-4 py-3 text-right hover:border-accent hover:bg-stone-50 transition"
        >
          <div className="text-xs uppercase tracking-wider text-stone-500 group-hover:text-accent">
            Next →
          </div>
          <div className="mt-1 font-medium text-ink line-clamp-2">{next.title}</div>
        </Link>
      ) : (
        <div />
      )}
    </nav>
  );
}
