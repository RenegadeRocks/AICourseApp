import Link from "next/link";
import { buildDailySchedule } from "@/lib/schedule";
import { completionsInRange } from "@/lib/db";

export default function SchedulePage() {
  const schedule = buildDailySchedule();
  if (schedule.length === 0) {
    return <p className="text-stone-600">Schedule empty.</p>;
  }
  const first = schedule[0].date;
  const last = schedule[schedule.length - 1].date;
  const done = completionsInRange(first, last);
  const today = new Date().toISOString().slice(0, 10);

  const byMonth = new Map<string, typeof schedule>();
  for (const s of schedule) {
    const month = s.date.slice(0, 7);
    if (!byMonth.has(month)) byMonth.set(month, [] as typeof schedule);
    byMonth.get(month)!.push(s);
  }

  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Program Schedule</h1>
      <p className="mt-2 text-stone-600 text-sm">
        {schedule.length} daily slots · {first} → {last}
      </p>
      <div className="mt-8 space-y-10">
        {[...byMonth.entries()].map(([month, slots]) => (
          <section key={month}>
            <h2 className="text-sm uppercase tracking-wider text-stone-500">{month}</h2>
            <ul className="mt-2 divide-y divide-stone-100 rounded-md border border-stone-200 bg-white">
              {slots.map((s) => {
                const isDone = done.has(s.date);
                const isToday = s.date === today;
                return (
                  <li
                    key={s.date}
                    className={`flex items-center justify-between px-4 py-2 text-sm ${
                      isToday ? "bg-amber-50" : ""
                    }`}
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className="tabular-nums text-stone-400 w-24">{s.date}</span>
                      <span className="uppercase text-[10px] tracking-wider text-stone-400 w-10">
                        {s.day_name}
                      </span>
                      <Link
                        href={`/vault/${s.block.id}/${weekFolderFromId(
                          s.block.id,
                          s.week.id,
                        )}/${s.fileBasename}`}
                        className="truncate hover:text-accent"
                      >
                        {s.anchorSession.title}
                      </Link>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-stone-500 shrink-0">
                      <span>{s.role}</span>
                      <span className={isDone ? "text-emerald-600" : "text-stone-300"}>
                        {isDone ? "●" : "○"}
                      </span>
                    </div>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}

function weekFolderFromId(blockId: string, weekId: string): string {
  const fs = require("node:fs") as typeof import("node:fs");
  const path = require("node:path") as typeof import("node:path");
  const blockDir = path.resolve(process.cwd(), "..", "vault", blockId);
  if (!fs.existsSync(blockDir)) return weekId;
  const match = fs
    .readdirSync(blockDir)
    .find((name) => name.startsWith(`${weekId}-`) || name === weekId);
  return match ?? weekId;
}
