import Link from "next/link";
import type { Route } from "next";
import { buildDailySchedule, slotKey } from "@/lib/schedule";
import { getCompletedSlotKeys } from "@/lib/db";
import { findWeekFolder, resolveDayFileBasename } from "@/lib/vault";

export default function SchedulePage() {
  const schedule = buildDailySchedule();
  if (schedule.length === 0) {
    return <p className="text-stone-600">Schedule empty.</p>;
  }
  const done = getCompletedSlotKeys();

  // Group by (block, week). Preserve schedule order.
  type Group = {
    blockId: string;
    blockTitle: string;
    weekId: string;
    weekTitle: string;
    weekInProgram: number;
    slots: typeof schedule;
  };
  const groups = new Map<string, Group>();
  for (const s of schedule) {
    const key = `${s.block.id}::${s.week.id}`;
    if (!groups.has(key)) {
      groups.set(key, {
        blockId: s.block.id,
        blockTitle: s.block.title,
        weekId: s.week.id,
        weekTitle: s.week.title,
        weekInProgram: s.weekInProgram,
        slots: [],
      });
    }
    groups.get(key)!.slots.push(s);
  }

  // Also group weeks by block so we can render <Block> → <Week> → <Day>.
  type BlockBucket = { id: string; title: string; weeks: Group[] };
  const blocks = new Map<string, BlockBucket>();
  for (const g of groups.values()) {
    if (!blocks.has(g.blockId)) {
      blocks.set(g.blockId, { id: g.blockId, title: g.blockTitle, weeks: [] });
    }
    blocks.get(g.blockId)!.weeks.push(g);
  }

  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight">Program Schedule</h1>
      <p className="mt-2 text-stone-600 text-sm">
        {schedule.length} daily lessons · {groups.size} weeks · self-paced
      </p>
      <div className="mt-8 space-y-10">
        {[...blocks.values()].map((b) => (
          <section key={b.id}>
            <h2 className="text-sm uppercase tracking-wider text-stone-500">
              {b.title}
            </h2>
            <div className="mt-3 space-y-4">
              {b.weeks.map((w) => (
                <div
                  key={w.weekId}
                  className="rounded-md border border-stone-200 bg-white overflow-hidden"
                >
                  <div className="px-4 py-2 border-b border-stone-100 bg-stone-50 text-sm font-medium">
                    Week {w.weekInProgram}
                  </div>
                  <ul className="divide-y divide-stone-100">
                    {w.slots.map((s) => {
                      const isDone = done.has(slotKey(s));
                      const weekFolder = findWeekFolder(s.block.id, s.week.id);
                      const basename = resolveDayFileBasename(
                        s.block.id,
                        weekFolder,
                        s.day_of_cycle,
                      );
                      const href = basename
                        ? (`/vault/${s.block.id}/${weekFolder}/${basename}` as Route)
                        : null;
                      return (
                        <li
                          key={slotKey(s)}
                          className="flex items-center justify-between px-4 py-2 text-sm"
                        >
                          <div className="flex items-center gap-3 min-w-0">
                            <span className="uppercase text-[10px] tracking-wider text-stone-400 w-10">
                              {s.day_name}
                            </span>
                            <span className="tabular-nums text-stone-400 w-10">
                              D{s.day_of_cycle}
                            </span>
                            {href ? (
                              <Link href={href} className="truncate hover:text-accent">
                                {s.anchorSession.title}
                              </Link>
                            ) : (
                              <span
                                className="truncate text-stone-400"
                                title="Lesson not yet generated"
                              >
                                {s.anchorSession.title}
                              </span>
                            )}
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
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
