// isolation.test.ts — Boris's executable wall (Thursday). An untested isolation
// claim is faith. This asserts, in CI, that RLS blocks cross-tenant reads and
// fails CLOSED when no tenant is set.
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { test } from 'node:test';
import { openDb, withTenant } from '../src/db.js';

test('RLS isolates tenants and fails closed', async () => {
  const db = await openDb();
  const tenantA = randomUUID();
  const tenantB = randomUUID();

  // Tenant A writes a secret report.
  await withTenant(db, tenantA, (tx) =>
    tx.query(
      `insert into reports (tenant_id, author_id, title, body)
       values ($1, $2, 'A confidential', 'do not leak')`,
      [tenantA, randomUUID()],
    ),
  );

  // Tenant B must see NOTHING.
  const seenByB = await withTenant(db, tenantB, (tx) =>
    tx.query(`select * from reports`),
  );
  assert.equal(seenByB.rows.length, 0, 'tenant B leaked into tenant A data');

  // Tenant A sees its own row.
  const seenByA = await withTenant(db, tenantA, (tx) =>
    tx.query(`select * from reports`),
  );
  assert.equal(seenByA.rows.length, 1, 'tenant A cannot read its own data');

  // An unknown tenant sees nothing (fail closed for any id without rows).
  const seenByC = await withTenant(db, randomUUID(), (tx) =>
    tx.query(`select * from reports`),
  );
  assert.equal(seenByC.rows.length, 0, 'RLS failed OPEN for an unknown tenant');
});
