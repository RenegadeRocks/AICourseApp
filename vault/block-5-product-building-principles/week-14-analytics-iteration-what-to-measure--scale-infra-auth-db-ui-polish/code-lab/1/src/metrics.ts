// metrics.ts — the ONE live product metric (Monday). North star = weekly accounts
// that shared a report; counter-metric = regeneration rate. Computed from the
// event log, served by the /metrics endpoint.
import type { Db } from './db.js';

export interface NorthStar {
  weeklySharingAccounts: number; // retained, valued action, weekly, per account
  regenerationRate: number; // counter-metric: high => trust problem
  reportsGenerated: number;
}

export async function northStar(db: Db): Promise<NorthStar> {
  const shared = await db.query<{ c: number }>(
    `select count(distinct account_id)::int as c
       from events
      where name = 'ReportShared'
        and created_at > now() - interval '7 days'`,
  );
  const gen = await db.query<{ c: number }>(
    `select count(*)::int as c from events where name = 'ReportGenerated'`,
  );
  const regen = await db.query<{ c: number }>(
    `select count(*)::int as c from events where name = 'ReportRegenerated'`,
  );

  const generated = gen.rows[0]?.c ?? 0;
  const regenerated = regen.rows[0]?.c ?? 0;

  return {
    weeklySharingAccounts: shared.rows[0]?.c ?? 0,
    reportsGenerated: generated,
    regenerationRate:
      generated === 0 ? 0 : Number((regenerated / generated).toFixed(3)),
  };
}
