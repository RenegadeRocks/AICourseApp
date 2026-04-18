import Link from "next/link";
import type { Route } from "next";
import { buildDailySchedule } from "@/lib/schedule";
import { completionsInRange, currentStreak } from "@/lib/db";
import { findWeekFolder, resolveDayFileBasename } from "@/lib/vault";

export default function ProgressPage() {
  const schedule = buildDailySchedule();
  if (schedule.length === 0) return <p>No schedule.</p>;
  const today = new Date().toISOString().slice(0, 10);
  const first = schedule[0].date;
  const last = schedule[schedule.length - 1].date;
  const done = completionsInRange(first, last);
  const streak = currentStreak(today);
  const pastOrToday = schedule.filter((s) => s.date <= today);
  const completion = (100 * done.size) / Math.max(1, pastOrToday.length);

  return (
    <div className="max-w-4xl">
      <h1 className="text-3xl font-bold tracking-tight">Progress</h1>
      <div className="grid grid-cols-3 gap-4 mt-8">
        <Stat label="Streak" value={`${streak}d`} />
        <Stat label="Lessons completed" value={`${done.size}`} />
        <Stat label="On-time rate" value={`${completion.toFixed(0)}%`} />
      </div>

      <h2 className="mt-10 font-semibold text-sm uppercase text-stone-500 tracking-wider">
        {first} → {last}
      </h2>
      <div
        className="mt-3 gap-1"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(22px, 1fr))",
        }}
      >
        {schedule.map((s) => {
          const isDone = done.has(s.date);
          const isToday = s.date === today;
          const isFuture = s.date > today;
          const bg = isDone
            ? "bg-emerald-500 hover:bg-emerald-600"
            : isToday
            ? "bg-amber-400 hover:bg-amber-500"
            : isFuture
            ? "bg-stone-100 hover:bg-stone-200"
            : "bg-stone-300 hover:bg-stone-400";
          const weekFolder = findWeekFolder(s.block.id, s.week.id);
          const basename = resolveDayFileBasename(s.block.id, weekFolder, s.day_of_cycle);
          const href = basename
            ? `/vault/${s.block.id}/${weekFolder}/${basename}`
            : null;
          const cellClass = `aspect-square rounded-sm transition ${bg}`;
          const title = `${s.date} · ${s.day_name.toUpperCase()} · ${s.anchorSession.title}${isDone ? " · ✓" : ""}`;
          return href ? (
            <Link key={s.date} href={href as Route} className={cellClass} title={title} />
          ) : (
            <div key={s.date} className={cellClass} title={title} />
          );
        })}
      </div>
      <div className="mt-4 flex gap-4 text-xs text-stone-500 flex-wrap">
        <Legend color="bg-emerald-500" label="Completed" />
        <Legend color="bg-amber-400" label="Today" />
        <Legend color="bg-stone-300" label="Missed" />
        <Legend color="bg-stone-100 border border-stone-200" label="Upcoming" />
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

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-stone-200 bg-white p-4">
      <div className="text-xs uppercase tracking-wider text-stone-500">{label}</div>
      <div className="mt-1 text-3xl font-bold">{value}</div>
    </div>
  );
}
