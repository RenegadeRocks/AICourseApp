// observability.ts — structured logging with redaction at the boundary (Tuesday).
// The observability store must never become the least-secured copy of your PII,
// so we redact sensitive keys BEFORE anything is written.
import { randomUUID } from 'node:crypto';

const REDACT_KEYS = new Set(['password', 'passwordHash', 'password_hash', 'token', 'email']);

export function newRequestId(): string {
  return randomUUID();
}

type Level = 'info' | 'warn' | 'error';

/** Emit one structured JSON log line. Swap console for your real sink; the
 *  redaction is the load-bearing part, not the transport. */
export function log(
  level: Level,
  msg: string,
  fields: Record<string, unknown> = {},
): void {
  const line = {
    ts: new Date().toISOString(),
    level,
    msg,
    ...redact(fields),
  };
  process.stdout.write(JSON.stringify(line) + '\n');
}

function redact(fields: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(fields)) {
    out[k] = REDACT_KEYS.has(k) ? '[redacted]' : v;
  }
  return out;
}
