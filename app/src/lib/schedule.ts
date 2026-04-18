import { addDays, differenceInCalendarDays, parseISO, startOfDay } from "date-fns";
import { allLiveSessions, type Block, type Session, type Week } from "./curriculum";

/**
 * 7-day cycle mapping per live-class week (see vault/00-program/how-to-study.md).
 * Day-of-cycle 1..7 corresponds to Mon..Sun of the live week.
 * Live sessions are Sat (day 6) and Sun (day 7).
 *
 * For a live-week that has TWO live sessions (Sat + Sun), this file expands
 * into 7 daily lessons. We compute "today's lesson" as the lesson whose
 * date_due equals today's date, walking forward from the program start.
 */

export interface DailySlot {
  date: string; // YYYY-MM-DD
  day_of_cycle: number; // 1..7
  day_name: "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun";
  block: Block;
  week: Week;
  /** The live session this slot is preparing for (or wrapping up). */
  anchorSession: Session;
  /** Suggested lesson file basename in the vault. */
  fileBasename: string;
  /** Cycle role: pre-read / deep-dive / live / recap. */
  role:
    | "pre-read-1"
    | "deep-dive-1a"
    | "deep-dive-1b"
    | "pre-read-2"
    | "deep-dive-2a"
    | "deep-dive-2b-live"
    | "recap";
}

const DAY_NAMES: DailySlot["day_name"][] = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];

const ROLE_BY_CYCLE: DailySlot["role"][] = [
  "pre-read-1",
  "deep-dive-1a",
  "deep-dive-1b",
  "pre-read-2",
  "deep-dive-2a",
  "deep-dive-2b-live",
  "recap",
];

function cycleStartForSaturday(saturday: Date): Date {
  // Saturday == day-of-cycle 6. Monday of the same week == saturday - 5 days.
  return addDays(saturday, -5);
}

/**
 * Build the full daily schedule by expanding every live-week into 7 slots.
 * Returns slots in ascending date order.
 */
export function buildDailySchedule(): DailySlot[] {
  const slots: DailySlot[] = [];
  const live = allLiveSessions();
  // Group sessions into (block, week) buckets with their live sessions in order.
  const buckets = new Map<string, { block: Block; week: Week; sessions: Session[] }>();
  for (const { block, week, session } of live) {
    const key = `${block.id}::${week.id}`;
    if (!buckets.has(key)) buckets.set(key, { block, week, sessions: [] });
    buckets.get(key)!.sessions.push(session);
  }

  for (const { block, week, sessions } of buckets.values()) {
    if (sessions.length === 0) continue;
    // Anchor Saturday = earliest dated session in this bucket (usually the Sat class).
    const sorted = sessions
      .filter((s) => s.date)
      .sort((a, b) => (a.date ?? "").localeCompare(b.date ?? ""));
    if (sorted.length === 0) continue;
    const saturday = parseISO(sorted[0].date as string);
    const monday = cycleStartForSaturday(saturday);

    for (let i = 0; i < 7; i++) {
      const dt = addDays(monday, i);
      const anchor = i < 3 ? sorted[0] : sorted[Math.min(1, sorted.length - 1)];
      const role = ROLE_BY_CYCLE[i];
      slots.push({
        date: dt.toISOString().slice(0, 10),
        day_of_cycle: i + 1,
        day_name: DAY_NAMES[i],
        block,
        week,
        anchorSession: anchor,
        fileBasename: `0${i + 1}-${DAY_NAMES[i]}-${anchor.slug}`,
        role,
      });
    }
  }
  return slots.sort((a, b) => a.date.localeCompare(b.date));
}

/**
 * Reverse-lookup: given a vault slug [blockId, weekFolder, "0N-dayname-topic"]
 * find the scheduled date for that lesson (if any). Non-lesson files (e.g.
 * program docs) return null.
 */
export function dateForLessonSlug(slug: string[]): string | null {
  if (slug.length < 3) return null;
  const [blockId, weekFolder, file] = slug;
  const weekId = weekFolder.match(/^(week-\d+)/)?.[1];
  if (!weekId) return null;
  const dayMatch = file.match(/^0(\d)-/);
  if (!dayMatch) return null;
  const day = parseInt(dayMatch[1], 10);
  const schedule = buildDailySchedule();
  const hit = schedule.find(
    (s) => s.block.id === blockId && s.week.id === weekId && s.day_of_cycle === day,
  );
  return hit?.date ?? null;
}

export function slotForDate(date: Date): DailySlot | null {
  const target = date.toISOString().slice(0, 10);
  const schedule = buildDailySchedule();
  return schedule.find((s) => s.date === target) ?? null;
}

export function nextSlotFrom(date: Date): DailySlot | null {
  const target = date.toISOString().slice(0, 10);
  const schedule = buildDailySchedule();
  return schedule.find((s) => s.date >= target) ?? null;
}

export function progressStats(today: Date) {
  const schedule = buildDailySchedule();
  if (schedule.length === 0) return { total: 0, daysElapsed: 0, daysRemaining: 0 };
  const first = parseISO(schedule[0].date);
  const last = parseISO(schedule[schedule.length - 1].date);
  const t = startOfDay(today);
  const elapsed = Math.max(0, differenceInCalendarDays(t, first) + 1);
  const total = differenceInCalendarDays(last, first) + 1;
  return {
    total,
    daysElapsed: Math.min(elapsed, total),
    daysRemaining: Math.max(0, total - elapsed),
  };
}
