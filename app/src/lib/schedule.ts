import { allLiveSessions, type Block, type Session, type Week } from "./curriculum";

/**
 * 7-day cycle per week: day-of-cycle 1..7 = Mon..Sun. The program is 9 blocks
 * × up to 4 weeks × 7 daily lessons. This module emits a flat ordered list of
 * those slots so the app can index by (block, week, day) without any calendar
 * dates — the course is self-paced and has no cohort calendar.
 */

export interface DailySlot {
  /** 0-based index into the full program (0 .. total-1). */
  sequenceIndex: number;
  /** 1-based week position across the entire program (1 .. 26). */
  weekInProgram: number;
  /** 1..7 — Monday..Sunday within the week. */
  day_of_cycle: number;
  day_name: "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun";
  block: Block;
  week: Week;
  /** The nominal anchor session this slot maps to — used for the fallback
   *  title when a lesson file hasn't been generated yet. */
  anchorSession: Session;
  /** Cycle role — roughly pre-read → deep-dive → recap. */
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

/**
 * Flat ordered program schedule. Order: block index (from curriculum.json)
 * → week index → day_of_cycle (1..7). Dates are intentionally absent.
 */
export function buildDailySchedule(): DailySlot[] {
  const slots: DailySlot[] = [];
  // Use allLiveSessions() to discover which (block, week) buckets exist in
  // curriculum.json — we don't care about the session dates here, only that
  // at least one session anchors the week so we know it's a live-class week.
  const live = allLiveSessions();
  const buckets = new Map<string, { block: Block; week: Week; sessions: Session[]; orderKey: string }>();
  for (const { block, week, session } of live) {
    const key = `${block.id}::${week.id}`;
    if (!buckets.has(key)) {
      buckets.set(key, { block, week, sessions: [], orderKey: key });
    }
    buckets.get(key)!.sessions.push(session);
  }
  const ordered = [...buckets.values()].sort((a, b) => {
    if (a.block.id !== b.block.id) return a.block.id.localeCompare(b.block.id);
    const aw = parseInt(a.week.id.match(/week-(\d+)/)?.[1] ?? "0", 10);
    const bw = parseInt(b.week.id.match(/week-(\d+)/)?.[1] ?? "0", 10);
    return aw - bw;
  });

  let seq = 0;
  let weekInProgram = 0;
  for (const bucket of ordered) {
    weekInProgram += 1;
    // Use the first session as the anchor for days 1–3, the second (if any)
    // for days 4–7, so the anchor titles line up with the structure the
    // vault generator produces.
    const s0 = bucket.sessions[0];
    const s1 = bucket.sessions[1] ?? s0;
    for (let i = 0; i < 7; i++) {
      slots.push({
        sequenceIndex: seq,
        weekInProgram,
        day_of_cycle: i + 1,
        day_name: DAY_NAMES[i],
        block: bucket.block,
        week: bucket.week,
        anchorSession: i < 3 ? s0 : s1,
        role: ROLE_BY_CYCLE[i],
      });
      seq += 1;
    }
  }
  return slots;
}

/**
 * Build a canonical slug for a slot so the progress store can key by it.
 * The slug is NOT the markdown-file basename (that's topic-based) — it's a
 * stable identifier derived from the slot's position in the program.
 */
export function slotKey(slot: DailySlot): string {
  return `${slot.block.id}/${slot.week.id}/day-${slot.day_of_cycle}`;
}

/**
 * Reverse: given a vault slug [blockId, weekFolder, fileBasename] find the
 * slot. Uses the day number prefix (01-mon → 1) to match.
 */
export function slotForVaultSlug(slugParts: string[]): DailySlot | null {
  if (slugParts.length < 3) return null;
  const [blockId, weekFolder, file] = slugParts;
  const weekId = weekFolder.match(/^(week-\d+)/)?.[1];
  if (!weekId) return null;
  const dayMatch = file.match(/^0(\d)-/);
  if (!dayMatch) return null;
  const day = parseInt(dayMatch[1], 10);
  const schedule = buildDailySchedule();
  return (
    schedule.find(
      (s) => s.block.id === blockId && s.week.id === weekId && s.day_of_cycle === day,
    ) ?? null
  );
}

/** First slot whose slot-key isn't in the `completedKeys` set, or null if
 *  every slot is done. */
export function firstIncompleteSlot(
  completedKeys: ReadonlySet<string>,
): DailySlot | null {
  const schedule = buildDailySchedule();
  return schedule.find((s) => !completedKeys.has(slotKey(s))) ?? null;
}

export function programStats(completedCount: number) {
  const total = buildDailySchedule().length;
  return {
    total,
    completed: Math.min(completedCount, total),
    remaining: Math.max(0, total - completedCount),
  };
}

/**
 * Streak = number of trailing completed slots up to the last completed one.
 * (In a self-paced program, "consecutive calendar days" no longer makes
 * sense, so we define the streak as the tail of consecutive completions in
 * schedule order.)
 */
export function streakFromCompletions(
  completedKeys: ReadonlySet<string>,
): number {
  const schedule = buildDailySchedule();
  let tail = 0;
  for (let i = schedule.length - 1; i >= 0; i--) {
    if (completedKeys.has(slotKey(schedule[i]))) {
      tail += 1;
    } else if (tail > 0) {
      break;
    }
  }
  return tail;
}
