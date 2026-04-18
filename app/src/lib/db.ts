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

export function markComplete(date: string, slug: string, notes?: string, minutes?: number) {
  db()
    .prepare(
      `INSERT INTO completions (date, slug, completed_at, notes, minutes)
       VALUES (?, ?, ?, ?, ?)
       ON CONFLICT(date) DO UPDATE SET
         slug = excluded.slug,
         completed_at = excluded.completed_at,
         notes = COALESCE(excluded.notes, completions.notes),
         minutes = COALESCE(excluded.minutes, completions.minutes)`
    )
    .run(date, slug, new Date().toISOString(), notes ?? null, minutes ?? null);
}

export function currentStreak(today: string): number {
  const rows = db()
    .prepare("SELECT date FROM completions ORDER BY date DESC")
    .all() as Array<{ date: string }>;
  const set = new Set(rows.map((r) => r.date));
  let streak = 0;
  const d = new Date(today);
  while (set.has(d.toISOString().slice(0, 10))) {
    streak++;
    d.setUTCDate(d.getUTCDate() - 1);
  }
  return streak;
}

export function completionsInRange(from: string, to: string): Set<string> {
  const rows = db()
    .prepare("SELECT date FROM completions WHERE date BETWEEN ? AND ?")
    .all(from, to) as Array<{ date: string }>;
  return new Set(rows.map((r) => r.date));
}

export function isCompleted(date: string): boolean {
  const row = db()
    .prepare("SELECT 1 FROM completions WHERE date = ?")
    .get(date) as { 1: number } | undefined;
  return !!row;
}
