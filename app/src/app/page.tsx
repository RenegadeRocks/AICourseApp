import Link from "next/link";
import { slotForDate, nextSlotFrom, progressStats } from "@/lib/schedule";
import { readVaultFile, render } from "@/lib/vault";
import { currentStreak } from "@/lib/db";

export default async function HomePage() {
  const today = new Date();
  const todayISO = today.toISOString().slice(0, 10);
  const stats = progressStats(today);
  const streak = currentStreak(todayISO);

  const slot = slotForDate(today) ?? nextSlotFrom(today);

  if (!slot) {
    return (
      <div className="max-w-3xl">
        <h1 className="text-3xl font-bold">Welcome</h1>
        <p className="mt-3 text-stone-600">
          No lessons scheduled. Run <code>python scripts/parse_xlsx.py</code> to (re)build the schedule.
        </p>
      </div>
    );
  }

  const isFuture = slot.date > todayISO;
  const weekFolder = `${slot.block.id}/${findWeekFolder(slot.block.id, slot.week.id)}`;
  const lessonSlug = [
    ...weekFolder.split("/"),
    slot.fileBasename,
  ];
  const file = readVaultFile(lessonSlug);
  const rendered = file ? await render(file) : null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_260px] gap-10">
      <section>
        <div className="text-sm text-stone-500 uppercase tracking-wider">
          {isFuture ? `Upcoming — starts ${slot.date}` : `Today · ${slot.date}`}
          {" · "}Day {slot.day_of_cycle}/7 · {slot.role}
        </div>
        <h1 className="mt-2 text-4xl font-bold tracking-tight">{slot.anchorSession.title}</h1>
        <div className="mt-1 text-stone-600">
          {slot.block.title} · {slot.week.title}
        </div>

        {rendered ? (
          <article
            className="prose-lesson mt-8"
            dangerouslySetInnerHTML={{ __html: rendered.html }}
          />
        ) : (
          <div className="mt-8 rounded-lg border border-dashed border-stone-300 p-8 bg-white/60">
            <h2 className="text-xl font-semibold">Lesson not yet generated</h2>
            <p className="mt-2 text-stone-600">
              This week's lessons haven't been written yet. From the project root:
            </p>
            <pre className="mt-3 bg-stone-900 text-stone-100 rounded p-3 text-sm overflow-x-auto">
              {`claude\n> /generate-lesson ${slot.block.id}/${slot.week.id}`}
            </pre>
            <p className="mt-3 text-sm text-stone-500">
              Expected file: <code>vault/{lessonSlug.join("/")}</code>.md
            </p>
          </div>
        )}
      </section>

      <aside className="space-y-6 text-sm">
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Streak</div>
          <div className="mt-1 text-3xl font-bold">{streak} <span className="text-base font-normal text-stone-500">days</span></div>
        </div>
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Program progress</div>
          <div className="mt-1">
            Day <strong>{stats.daysElapsed}</strong> of <strong>{stats.total}</strong>
          </div>
          <div className="mt-2 h-2 w-full bg-stone-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-accent"
              style={{ width: `${(100 * stats.daysElapsed) / Math.max(1, stats.total)}%` }}
            />
          </div>
          <div className="mt-1 text-xs text-stone-500">{stats.daysRemaining} days remaining</div>
        </div>
        <div className="rounded-lg bg-white border border-stone-200 p-4">
          <div className="text-xs uppercase tracking-wider text-stone-500">Quick links</div>
          <ul className="mt-2 space-y-1">
            <li><Link href="/vault/00-program/how-to-study" className="text-accent hover:underline">Study protocol</Link></li>
            <li><Link href="/vault/00-program/quality-standard" className="text-accent hover:underline">Quality standard</Link></li>
            <li><Link href="/schedule" className="text-accent hover:underline">Full schedule</Link></li>
          </ul>
        </div>
      </aside>
    </div>
  );
}

function findWeekFolder(blockId: string, weekId: string): string {
  // The vault folder names include the week id prefix (e.g. "week-01-...").
  // We resolve by scanning vault at runtime via listVaultFiles results rather
  // than a hard-coded map.
  const fs = require("node:fs") as typeof import("node:fs");
  const path = require("node:path") as typeof import("node:path");
  const blockDir = path.resolve(process.cwd(), "..", "vault", blockId);
  if (!fs.existsSync(blockDir)) return weekId;
  const match = fs
    .readdirSync(blockDir)
    .find((name) => name.startsWith(`${weekId}-`) || name === weekId);
  return match ?? weekId;
}
