// db.ts — one Postgres (via PGlite, real Postgres in-process), migrations run on
// boot, and the per-request tenant context that activates RLS (Friday + Thursday).
import { PGlite } from '@electric-sql/pglite';
import type { Transaction } from '@electric-sql/pglite';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const MIGRATIONS_DIR = join(HERE, '..', 'migrations');

export type Db = PGlite;

/** Open the database and bring the schema up to date. In-memory unless
 *  DATABASE_DIR is set (e.g. "./pgdata" for a persistent local file store). */
export async function openDb(): Promise<Db> {
  const dir = process.env.DATABASE_DIR;
  const db = dir ? new PGlite(dir) : new PGlite();
  await runMigrations(db);
  return db;
}

/** Ordered, idempotent migration runner. Applies any *.sql not yet recorded.
 *  The discipline that matters (Friday): versioned, ordered, never by hand. */
async function runMigrations(db: Db): Promise<void> {
  await db.exec(
    `create table if not exists _migrations (
       name text primary key,
       applied_at timestamptz not null default now()
     );`,
  );
  const files = readdirSync(MIGRATIONS_DIR)
    .filter((f) => f.endsWith('.sql'))
    .sort();
  for (const file of files) {
    const seen = await db.query<{ name: string }>(
      `select name from _migrations where name = $1`,
      [file],
    );
    if (seen.rows.length > 0) continue;
    const sql = readFileSync(join(MIGRATIONS_DIR, file), 'utf8');
    await db.exec(sql);
    await db.query(`insert into _migrations (name) values ($1)`, [file]);
  }
}

/** Run `fn` inside a transaction with app.tenant_id set LOCALLY, so the RLS
 *  policy on `reports` filters every query to this tenant. Transaction-scoped
 *  (is_local = true) is the production-correct choice under a connection pool
 *  (Friday): the setting cannot leak to the next request on a reused connection. */
export async function withTenant<T>(
  db: Db,
  tenantId: string,
  fn: (tx: Transaction) => Promise<T>,
): Promise<T> {
  return db.transaction(async (tx) => {
    // Drop from the superuser owner to the non-superuser app role so RLS applies,
    // then scope the tenant. Both are LOCAL: they reset when the tx ends.
    await tx.query(`set local role app_user`);
    await tx.query(`select set_config('app.tenant_id', $1, true)`, [tenantId]);
    return fn(tx);
  });
}
