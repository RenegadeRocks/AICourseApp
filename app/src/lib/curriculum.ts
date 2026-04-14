import fs from "node:fs";
import { CURRICULUM_JSON } from "./paths";

export interface Session {
  slug: string;
  title: string;
  date: string | null;
  kind: "live-session" | "office-hours" | "resource-drop" | "onboarding" | "special";
}

export interface Week {
  id: string;
  title: string;
  live_week_number: number | null;
  sessions: Session[];
}

export interface Block {
  id: string;
  title: string;
  order: number;
  weeks: Week[];
}

export interface Curriculum {
  program: {
    name: string;
    instructor: string;
    start_date: string;
    end_date: string;
    session_time_ist: string;
    office_hours_day: string;
    core_session_days: string[];
    resource_drop_day: string;
    source_file: string;
    parsed_at: string;
  };
  blocks: Block[];
}

let _cache: Curriculum | null = null;

export function getCurriculum(): Curriculum {
  if (_cache) return _cache;
  const raw = fs.readFileSync(CURRICULUM_JSON, "utf-8");
  _cache = JSON.parse(raw) as Curriculum;
  return _cache;
}

export function allLiveSessions(): Array<{ block: Block; week: Week; session: Session }> {
  const out: Array<{ block: Block; week: Week; session: Session }> = [];
  for (const block of getCurriculum().blocks) {
    for (const week of block.weeks) {
      for (const session of week.sessions) {
        if (session.kind === "live-session" || session.kind === "onboarding") {
          out.push({ block, week, session });
        }
      }
    }
  }
  return out.sort((a, b) => (a.session.date ?? "").localeCompare(b.session.date ?? ""));
}
