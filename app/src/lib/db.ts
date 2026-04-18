import Database from "better-sqlite3";
import { PROGRESS_DB } from "./paths";

let _db: Database.Database | null = null;

export function db(): Database.Database {
  if (_db) return _db;
  _db = new Database(PROGRESS_DB);
  _db.pragma("journal_mode = WAL");
  _db.exec(`
    CREATE TABLE IF NOT EXISTS completions (
      date TEXT PRIMARY KEY,
      slug TEXT NOT NULL,
      completed_at TEXT NOT NULL,
      notes TEXT,
      minutes INTEGER
    );
    CREATE TABLE IF NOT EXISTS lesson_completions (
      slot_key TEXT PRIMARY KEY,
      slug TEXT NOT NULL,
      completed_at TEXT NOT NULL,
      notes TEXT,
      minutes INTEGER
    );
    CREATE TABLE IF NOT EXISTS quiz_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      slug TEXT NOT NULL,
      score INTEGER NOT NULL,
      total INTEGER NOT NULL,
      attempted_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS reflections (
      slug TEXT NOT NULL,
      question_idx INTEGER NOT NULL,
      answer TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      PRIMARY KEY (slug, question_idx)
    );
  `);
  return _db;
}

/**
 * Mark a lesson completed. The `slotKey` is the program-relative key
 * (e.g. "block-0-basecamp/week-01/day-3"); the `slug` is the vault
 * path so we can render back-references.
 */
export function markLessonComplete(
  slotKey: string,
  slug: string,
  notes?: string,
  minutes?: number,
) {
  db()
    .prepare(
      `INSERT INTO lesson_completions (slot_key, slug, completed_at, notes, minutes)
       VALUES (?, ?, ?, ?, ?)
       ON CONFLICT(slot_key) DO UPDATE SET
         slug = excluded.slug,
         completed_at = excluded.completed_at,
         notes = COALESCE(excluded.notes, lesson_completions.notes),
         minutes = COALESCE(excluded.minutes, lesson_completions.minutes)`,
    )
    .run(slotKey, slug, new Date().toISOString(), notes ?? null, minutes ?? null);
}

export function isLessonCompleted(slotKey: string): boolean {
  const row = db()
    .prepare("SELECT 1 FROM lesson_completions WHERE slot_key = ?")
    .get(slotKey) as { 1: number } | undefined;
  return !!row;
}

export function getCompletedSlotKeys(): Set<string> {
  const rows = db()
    .prepare("SELECT slot_key FROM lesson_completions")
    .all() as Array<{ slot_key: string }>;
  return new Set(rows.map((r) => r.slot_key));
}
