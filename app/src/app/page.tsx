import Link from "next/link";
import type { Route } from "next";
import {
  firstIncompleteSlot,
  programStats,
  slotKey,
  type DailySlot,
} from "@/lib/schedule";
import {
  readVaultFile,
  render,
  findWeekFolder,
  resolveDayFileBasename,
} from "@/lib/vault";
import { getCompletedSlotKeys, isLessonCompleted } from "@/lib/db";
import CompleteButton from "./vault/[...slug]/CompleteButton";
import { streakFromCompletions } from "@/lib/schedule";

export default async function HomePage() {
  const completed = getCompletedSlotKeys();
  const stats = programStats(completed.size);
  const streak = streakFromCompletions(completed);

  // "Next up" is the first uncompleted slot in schedule order.
  const slot: DailySlot | null = firstIncompleteSlot(completed);

  if (!slot) {
    return (
      <div className="max-w-3xl">
        <div className="text-sm text-stone-500 uppercase tracking-wider">
          Program complete
        </div>
        <h1 className="mt-2 text-4xl font-bold tracking-tight">
          You&rsquo;ve finished every lesson.
        </h1>
        <p className="mt-4 text-stone-600">
          {stats.total} lessons · {stats.completed} completed · {streak} lesson
          streak. Go review the <Link href="/progress" className="text-accent hover:underline">progress heatmap</Link>.
        </p>
      </div>
    );
  }

  const weekFolderName = findWeekFolder(slot.block.id, slot.week.id);
  const basename = resolveDayFileBasename(
    slot.block.id,
    weekFolderName,
    slot.day_of_cycle,
  );
  const lessonSlug = basename
    ? [slot.block.id, weekFolderName, basename]
    : null;
  const file = lessonSlug ? readVaultFile(lessonSlug) : null;
  const rendered = file ? await render(file) : null;
  const lessonHref = lessonSlug
    ? (`/vault/${lessonSlug.join("/")}` as Route)
    : null;
  const slotKeyStr = slotKey(slot);
  const done = isLessonCompleted(slotKeyStr);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_260px] gap-10">
      <section>
        <div className="text-sm text-stone-500 uppercase tracking-wider">
          Next up · Week {slot.weekInProgram} · Day {slot.day_of_cycle}/7 · {slot.role}
        </div>
        <h1 className="mt-2 text-4xl font-bold tracking-tight">{slot.anchorSession.title}</h1>
        <div className="mt-1 text-stone-600">
          {slot.block.title}
        </div>

        {file && lessonHref && (
          <div className="mt-4 flex items-center gap-4">
            <CompleteButton
              slotKey={slotKeyStr}
              slug={lessonSlug!.join("/")}
              label={`Week ${slot.weekInProgram} · Day ${slot.day_of_cycle}`}
              initiallyDone={done}
            />
            <Link
              href={lessonHref}
              className="text-sm text-stone-500 hover:text-accent hover:underline"
            >
              Open full lesson →
            </Link>
          </div>
        )}

        {rendered ? (
          <article
            className="prose-lesson mt-8"
            dangerouslySetInnerHTML={{ __html: rendered.html }}
          />
        ) : (
          <div className="mt-8 rounded-lg border border-dashed border-stone-300 p-8 bg-white/60">
            <h2 className="text-xl font-semibold">Lesson not yet generated</h2>
            <p className="mt-2 text-stone-600">
              This lesson hasn&rsquo;t been written yet. From the project root:
            </p>
            <pre className="mt-3 bg-stone-900 text-stone-100 rounded p-3 text-sm overflow-x-auto">
              {`claude\n> /generate-lesson ${slot.block.id}/${slot.week.id}`}
            </pre>
            {lessonSlug && (
              <p className="mt-3 text-sm text-stone-500">
                Expected file: <code>vault/{lessonSlug.join("/")}</code>.md
              </p>
            )}
          </div>
        )}
      </section>

      <aside className="space-y-6 text-sm">
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Streak</div>
          <div className="mt-1 text-3xl font-bold">
            {streak} <span className="text-base font-normal text-stone-500">lessons</span>
          </div>
        </div>
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Program progress</div>
          <div className="mt-1">
            <strong>{stats.completed}</strong> of <strong>{stats.total}</strong> lessons
          </div>
          <div className="mt-2 h-2 w-full bg-stone-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-accent"
              style={{ width: `${(100 * stats.completed) / Math.max(1, stats.total)}%` }}
            />
          </div>
          <div className="mt-1 text-xs text-stone-500">{stats.remaining} lessons remaining</div>
        </div>
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Quick links</div>
          <ul className="mt-2 space-y-1">
            <li><Link href="/vault/00-program/index" className="text-accent hover:underline">Program index</Link></li>
            <li><Link href="/vault/00-program/how-to-study" className="text-accent hover:underline">How to study</Link></li>
            <li><Link href="/schedule" className="text-accent hover:underline">Full schedule</Link></li>
          </ul>
        </div>
      </aside>
    </div>
  );
}
