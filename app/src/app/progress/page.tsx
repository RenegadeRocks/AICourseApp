import { buildDailySchedule } from "@/lib/schedule";
import { completionsInRange, currentStreak } from "@/lib/db";

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
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Progress</h1>
      <div className="grid grid-cols-3 gap-4 mt-8">
        <Stat label="Streak" value={`${streak}d`} />
        <Stat label="Lessons completed" value={`${done.size}`} />
        <Stat label="On-time rate" value={`${completion.toFixed(0)}%`} />
      </div>

      <h2 className="mt-10 font-semibold text-sm uppercase text-stone-500 tracking-wider">
        {first} → {last}
      </h2>
      <div className="mt-3 grid grid-cols-14 sm:grid-cols-28 gap-1">
        {schedule.map((s) => {
          const isDone = done.has(s.date);
          const isToday = s.date === today;
          const isFuture = s.date > today;
          const bg = isDone
            ? "bg-emerald-500"
            : isToday
            ? "bg-amber-400"
            : isFuture
            ? "bg-stone-100"
            : "bg-stone-300";
          return (
            <div
              key={s.date}
              className={`aspect-square rounded-sm ${bg}`}
              title={`${s.date} — ${s.anchorSession.title}`}
            />
          );
        })}
      </div>
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
