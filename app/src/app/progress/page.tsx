import Link from "next/link";
import type { Route } from "next";
import {
  buildDailySchedule,
  slotKey,
  streakFromCompletions,
  programStats,
} from "@/lib/schedule";
import { getCompletedSlotKeys } from "@/lib/db";
import { findWeekFolder, resolveDayFileBasename } from "@/lib/vault";

export default function ProgressPage() {
  const schedule = buildDailySchedule();
  if (schedule.length === 0) return <p>No schedule.</p>;
  const done = getCompletedSlotKeys();
  const stats = programStats(done.size);
  const streak = streakFromCompletions(done);
  const completionRate = (100 * stats.completed) / Math.max(1, stats.total);

  return (
    <div className="max-w-4xl">
      <h1 className="text-3xl font-bold tracking-tight">Progress</h1>
      <div className="grid grid-cols-3 gap-4 mt-8">
        <Stat label="Streak" value={`${streak}`} unit="lessons" />
        <Stat label="Lessons completed" value={`${stats.completed}`} unit={`of ${stats.total}`} />
        <Stat label="Completion" value={`${completionRate.toFixed(0)}%`} />
      </div>

      <h2 className="mt-10 font-semibold text-sm uppercase text-stone-500 tracking-wider">
        Program heatmap
      </h2>
      <p className="mt-1 text-xs text-stone-500">
        One cell per lesson · 7 columns = Mon…Sun · rows are weeks in order.
      </p>

      {/* 7 cols wide; rows auto. One cell per slot. */}
      <div
        className="mt-3 gap-1 max-w-md"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, minmax(24px, 1fr))",
        }}
      >
        {schedule.map((s) => {
          const isDone = done.has(slotKey(s));
          const bg = isDone
            ? "bg-emerald-500 hover:bg-emerald-600"
            : "bg-stone-200 hover:bg-stone-300";
          const weekFolder = findWeekFolder(s.block.id, s.week.id);
          const basename = resolveDayFileBasename(s.block.id, weekFolder, s.day_of_cycle);
          const href = basename
            ? (`/vault/${s.block.id}/${weekFolder}/${basename}` as Route)
            : null;
          const title = `Week ${s.weekInProgram} · ${s.day_name.toUpperCase()} · ${s.anchorSession.title}${isDone ? " · ✓" : ""}`;
          const cellClass = `aspect-square rounded-sm transition ${bg}`;
          return href ? (
            <Link key={slotKey(s)} href={href} className={cellClass} title={title} />
          ) : (
            <div key={slotKey(s)} className={cellClass} title={title} />
          );
        })}
      </div>
      <div className="mt-4 flex gap-4 text-xs text-stone-500 flex-wrap">
        <Legend color="bg-emerald-500" label="Completed" />
        <Legend color="bg-stone-200" label="Not yet completed" />
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  unit,
}: {
  label: string;
  value: string;
  unit?: string;
}) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-4">
      <div className="text-xs uppercase tracking-wider text-stone-500">{label}</div>
      <div className="mt-1 text-3xl font-bold">
        {value}
        {unit && <span className="ml-2 text-base font-normal text-stone-500">{unit}</span>}
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={`inline-block w-3 h-3 rounded-sm ${color}`} />
      <span>{label}</span>
    </div>
  );
}
