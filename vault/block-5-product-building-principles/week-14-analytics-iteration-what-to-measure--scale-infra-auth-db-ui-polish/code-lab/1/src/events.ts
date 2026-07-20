// events.ts — the typed event taxonomy (Tuesday). Events are defined ONCE, here,
// and emitted only through emit(). No raw string event names sprinkled across the
// codebase, so a rename can't leave half the app firing the old name.
import type { PGlite, Transaction } from '@electric-sql/pglite';

export const EVENTS = [
  'ReportGenerated',
  'ReportShared',
  'ReportRegenerated',
  'ReportOutcome',
] as const;

export type EventName = (typeof EVENTS)[number];

export interface AnalyticsEvent {
  name: EventName;
  accountId: string;
  userId: string;
  requestId: string; // the shared id that joins product + AI pipes
  props?: Record<string, unknown>;
}

/** Insert one event. Accepts a tenant transaction or the raw db; the events
 *  table is not tenant-isolated (it is the operator's product-wide log). */
export async function emit(
  q: PGlite | Transaction,
  e: AnalyticsEvent,
): Promise<void> {
  await q.query(
    `insert into events (name, account_id, user_id, request_id, props)
     values ($1, $2, $3, $4, $5)`,
    [e.name, e.accountId, e.userId, e.requestId, JSON.stringify(e.props ?? {})],
  );
}
