// server.ts — the hardened product surface (Saturday). Real auth, tenant-isolated
// data (RLS), an observability hook on every request, and a protected live metric.
import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import type { Context } from 'hono';
import { deleteCookie, getCookie, setCookie } from 'hono/cookie';
import { createMiddleware } from 'hono/factory';
import { hashPassword, hashToken, newSession, verifyPassword } from './auth.js';
import { openDb, withTenant, type Db } from './db.js';
import { emit } from './events.js';
import { northStar } from './metrics.js';
import { log, newRequestId } from './observability.js';

interface SessionUser {
  id: string;
  accountId: string;
  email: string;
  role: string;
}

type AppEnv = { Variables: { user: SessionUser; requestId: string } };

const PROD = process.env.NODE_ENV === 'production';

export function createApp(db: Db): Hono<AppEnv> {
  const app = new Hono<AppEnv>();

  // Observability hook: one structured, redacted log line per request.
  app.use('*', async (c, next) => {
    const requestId = newRequestId();
    c.set('requestId', requestId);
    await next();
    log('info', 'request', {
      requestId,
      method: c.req.method,
      path: c.req.path,
      status: c.res.status,
    });
  });

  const requireAuth = createMiddleware<AppEnv>(async (c, next) => {
    const token = getCookie(c, 'session');
    if (!token) return c.json({ error: 'unauthorized' }, 401);
    const res = await db.query<{
      id: string;
      account_id: string;
      email: string;
      role: string;
    }>(
      `select u.id, u.account_id, u.email, u.role
         from sessions s
         join users u on u.id = s.user_id
        where s.token_hash = $1 and s.expires_at > now()`,
      [hashToken(token)],
    );
    const u = res.rows[0];
    if (!u) return c.json({ error: 'unauthorized' }, 401);
    c.set('user', {
      id: u.id,
      accountId: u.account_id,
      email: u.email,
      role: u.role,
    });
    await next();
  });

  function setSessionCookie(c: Context<AppEnv>, token: string, expires: Date): void {
    setCookie(c, 'session', token, {
      httpOnly: true,
      secure: PROD,
      sameSite: 'Lax',
      path: '/',
      expires,
    });
  }

  app.get('/healthz', (c) => c.json({ status: 'ok' }));

  app.post('/auth/signup', async (c) => {
    const body = await c.req
      .json<{ email?: string; password?: string; accountName?: string }>()
      .catch(() => ({}) as { email?: string; password?: string; accountName?: string });
    const email = (body.email ?? '').trim().toLowerCase();
    const password = body.password ?? '';
    if (!email || password.length < 8) {
      return c.json({ error: 'email and 8+ char password required' }, 400);
    }
    try {
      const account = await db.query<{ id: string }>(
        `insert into accounts (name) values ($1) returning id`,
        [body.accountName ?? email],
      );
      const accountId = account.rows[0]?.id;
      if (!accountId) return c.json({ error: 'account creation failed' }, 500);
      const user = await db.query<{ id: string }>(
        `insert into users (account_id, email, password_hash, role)
         values ($1, $2, $3, 'owner') returning id`,
        [accountId, email, await hashPassword(password)],
      );
      const userId = user.rows[0]?.id;
      if (!userId) return c.json({ error: 'user creation failed' }, 500);
      const s = newSession();
      await db.query(
        `insert into sessions (token_hash, user_id, expires_at) values ($1, $2, $3)`,
        [s.tokenHash, userId, s.expiresAt.toISOString()],
      );
      setSessionCookie(c, s.token, s.expiresAt);
      return c.json({ id: userId, accountId }, 201);
    } catch {
      // unique_violation on email, etc. Never echo the DB error to the client.
      return c.json({ error: 'email already registered' }, 409);
    }
  });

  app.post('/auth/login', async (c) => {
    const body = await c.req
      .json<{ email?: string; password?: string }>()
      .catch(() => ({}) as { email?: string; password?: string });
    const email = (body.email ?? '').trim().toLowerCase();
    const res = await db.query<{ id: string; password_hash: string }>(
      `select id, password_hash from users where email = $1`,
      [email],
    );
    const u = res.rows[0];
    // Verify even on miss to keep timing uniform (avoid user enumeration).
    const ok = u
      ? await verifyPassword(body.password ?? '', u.password_hash)
      : await verifyPassword(body.password ?? '', 'x:y');
    if (!u || !ok) return c.json({ error: 'invalid credentials' }, 401);
    const s = newSession();
    await db.query(
      `insert into sessions (token_hash, user_id, expires_at) values ($1, $2, $3)`,
      [s.tokenHash, u.id, s.expiresAt.toISOString()],
    );
    setSessionCookie(c, s.token, s.expiresAt);
    return c.json({ ok: true });
  });

  app.post('/auth/logout', async (c) => {
    const token = getCookie(c, 'session');
    if (token) {
      await db.query(`delete from sessions where token_hash = $1`, [hashToken(token)]);
    }
    deleteCookie(c, 'session', { path: '/' });
    return c.json({ ok: true });
  });

  app.post('/reports', requireAuth, async (c) => {
    const user = c.get('user');
    const requestId = c.get('requestId');
    const body = await c.req
      .json<{ title?: string; body?: string }>()
      .catch(() => ({}) as { title?: string; body?: string });
    const title = (body.title ?? '').trim();
    if (!title) return c.json({ error: 'title required' }, 400);
    const id = await withTenant(db, user.accountId, async (tx) => {
      const res = await tx.query<{ id: string }>(
        `insert into reports (tenant_id, author_id, title, body)
         values ($1, $2, $3, $4) returning id`,
        [user.accountId, user.id, title, body.body ?? ''],
      );
      const reportId = res.rows[0]?.id;
      await emit(tx, {
        name: 'ReportGenerated',
        accountId: user.accountId,
        userId: user.id,
        requestId,
        props: { reportId },
      });
      return reportId;
    });
    return c.json({ id }, 201);
  });

  app.get('/reports', requireAuth, async (c) => {
    const user = c.get('user');
    const rows = await withTenant(db, user.accountId, (tx) =>
      tx.query<{ id: string; title: string; shared: boolean; created_at: string }>(
        `select id, title, shared, created_at from reports order by created_at desc`,
      ),
    );
    return c.json({ reports: rows.rows });
  });

  app.post('/reports/:id/share', requireAuth, async (c) => {
    const user = c.get('user');
    const requestId = c.get('requestId');
    const id = c.req.param('id');
    const shared = await withTenant(db, user.accountId, async (tx) => {
      const res = await tx.query(`update reports set shared = true where id = $1`, [id]);
      const affected = res.affectedRows ?? 0;
      if (affected > 0) {
        await emit(tx, {
          name: 'ReportShared',
          accountId: user.accountId,
          userId: user.id,
          requestId,
          props: { reportId: id },
        });
      }
      return affected > 0;
    });
    return shared ? c.json({ shared: true }) : c.json({ error: 'not found' }, 404);
  });

  app.post('/reports/:id/regenerate', requireAuth, async (c) => {
    const user = c.get('user');
    const requestId = c.get('requestId');
    const id = c.req.param('id');
    await withTenant(db, user.accountId, (tx) =>
      emit(tx, {
        name: 'ReportRegenerated',
        accountId: user.accountId,
        userId: user.id,
        requestId,
        props: { reportId: id },
      }),
    );
    return c.json({ ok: true });
  });

  // Live product metric. Protected by a bearer token so a hostile stranger
  // cannot scrape your business numbers (Monday + Thursday).
  app.get('/metrics', async (c) => {
    const expected = process.env.METRICS_TOKEN;
    if (!expected || c.req.header('authorization') !== `Bearer ${expected}`) {
      return c.json({ error: 'forbidden' }, 403);
    }
    return c.json(await northStar(db));
  });

  return app;
}

// Boot.
const db = await openDb();
const app = createApp(db);
const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => log('info', 'listening', { port: info.port }));
