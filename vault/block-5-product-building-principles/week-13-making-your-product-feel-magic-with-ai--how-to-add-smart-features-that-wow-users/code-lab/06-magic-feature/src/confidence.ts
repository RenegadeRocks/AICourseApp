import type { Deal } from "./types";

/**
 * Confidence gating constants. Tune these against your golden set (evals/), not
 * against your intuition. See 04-thu-reliability-of-magic.
 */

/** Below this returned confidence, we degrade instead of showing a plain suggestion. */
export const CONFIDENCE_THRESHOLD = 0.7;

/** Deterministic precondition: the model needs at least this much context. */
export const MIN_MESSAGES = 2;

/**
 * Gate 1 — the cheapest, most reliable gate. A precondition you can compute in
 * code beats any confidence the model reports about itself.
 */
export function hasEnoughContext(deal: Deal): boolean {
  return deal.messages.length >= MIN_MESSAGES;
}
