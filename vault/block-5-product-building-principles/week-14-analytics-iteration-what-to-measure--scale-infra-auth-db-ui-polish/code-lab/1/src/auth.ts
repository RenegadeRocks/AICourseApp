// auth.ts — password hashing and opaque session tokens using Node's standard
// crypto primitives. We do NOT invent crypto (Thursday): scrypt is a vetted KDF,
// tokens are random and stored only as SHA-256 digests.
import { createHash, randomBytes, scrypt, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';

const scryptAsync = promisify(scrypt);
const KEYLEN = 64;
const SESSION_TTL_MS = 1000 * 60 * 60 * 24 * 7; // 7 days

/** Hash a password as `saltHex:hashHex`. */
export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16);
  const derived = (await scryptAsync(password, salt, KEYLEN)) as Buffer;
  return `${salt.toString('hex')}:${derived.toString('hex')}`;
}

/** Constant-time verification against a stored `saltHex:hashHex`. */
export async function verifyPassword(
  password: string,
  stored: string,
): Promise<boolean> {
  const [saltHex, hashHex] = stored.split(':');
  if (!saltHex || !hashHex) return false;
  const salt = Buffer.from(saltHex, 'hex');
  const expected = Buffer.from(hashHex, 'hex');
  const derived = (await scryptAsync(password, salt, KEYLEN)) as Buffer;
  return derived.length === expected.length && timingSafeEqual(derived, expected);
}

export interface NewSession {
  token: string; // returned to the client once, set as an httpOnly cookie
  tokenHash: string; // the only thing we persist
  expiresAt: Date;
}

/** Mint a session: a random token for the cookie, its digest for the DB. */
export function newSession(): NewSession {
  const token = randomBytes(32).toString('hex');
  return {
    token,
    tokenHash: hashToken(token),
    expiresAt: new Date(Date.now() + SESSION_TTL_MS),
  };
}

export function hashToken(token: string): string {
  return createHash('sha256').update(token).digest('hex');
}
