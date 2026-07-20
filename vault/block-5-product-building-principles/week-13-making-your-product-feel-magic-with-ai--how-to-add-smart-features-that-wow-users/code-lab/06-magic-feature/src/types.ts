import { z } from "zod";

/**
 * Domain types for the running example: a lightweight CRM for freelancers.
 * The magical feature: a proactive, gated, editable follow-up draft for a deal
 * that has gone quiet. Deterministic detection + gated generation + human on the
 * irreversible send.
 */

export const MessageSchema = z.object({
  from: z.enum(["user", "contact"]),
  text: z.string(),
});
export type Message = z.infer<typeof MessageSchema>;

export const DealSchema = z.object({
  id: z.string(),
  contactName: z.string(),
  /** Optional: when absent, the model's context is thin (a jagged-frontier input). */
  product: z.string().optional(),
  daysQuiet: z.number().int().nonnegative(),
  messages: z.array(MessageSchema),
});
export type Deal = z.infer<typeof DealSchema>;

export const TonePreferenceSchema = z.enum(["concise", "warm", "formal"]);
export type TonePreference = z.infer<typeof TonePreferenceSchema>;

export interface FeatureInput {
  deal: Deal;
  tone: TonePreference;
  /** Test hook: simulate a provider outage/timeout to exercise the fallback path. */
  simulateFailure?: boolean;
}

/**
 * Structured model output. This is what drives the UI: `subject` and `body`
 * populate the editable fields, `usedContextIds` renders provenance chips, and
 * `confidence` drives the gate. We NEVER render un-validated model output, so
 * every provider result is parsed against this schema before use.
 */
export const DraftSchema = z.object({
  subject: z.string().min(1).max(200),
  body: z.string().min(1).max(2000),
  confidence: z.number().min(0).max(1),
  usedContextIds: z.array(z.string()),
});
export type Draft = z.infer<typeof DraftSchema>;

/**
 * The feature never throws to the caller. It always returns one of these
 * degradation levels, and every level is a usable, valid state for the UI.
 */
export type FeatureResult =
  | { status: "suggested"; draft: Draft; usedContextIds: string[] }
  | { status: "low_confidence"; draft: Draft; usedContextIds: string[] }
  | { status: "suppressed"; reason: string }
  | { status: "fallback"; templates: string[]; reason: string };
