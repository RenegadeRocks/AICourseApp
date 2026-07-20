import { CONFIDENCE_THRESHOLD, hasEnoughContext } from "./confidence";
import { fallbackTemplates } from "./fallback";
import type { SuggestionProvider } from "./provider";
import { DraftSchema, type FeatureInput, type FeatureResult } from "./types";

const DEFAULT_TIMEOUT_MS = 4000;

/**
 * The feature service. This is the whole contract of shippable magic in one
 * function:
 *
 *   1. Deterministic precondition gate  (cheapest, most reliable).
 *   2. Provider call, wrapped so it can NEVER throw to the caller, with timeout.
 *   3. Schema-validation gate           (never render un-validated model output).
 *   4. Confidence gate                  (degrade instead of showing low-confidence).
 *
 * It always returns a valid FeatureResult. There is no code path that throws and
 * no code path that leaves the user blocked. That is the "degrade gracefully"
 * guarantee the eval harness verifies.
 */
export async function draftFollowUp(
  input: FeatureInput,
  provider: SuggestionProvider,
  opts: { timeoutMs?: number } = {},
): Promise<FeatureResult> {
  const { deal, tone } = input;

  // Gate 1 — deterministic precondition.
  if (!hasEnoughContext(deal)) {
    return { status: "suppressed", reason: "insufficient_context" };
  }

  // Provider call — the only place the model runs, fully wrapped.
  let raw: unknown;
  try {
    raw = await withTimeout(
      provider.generate(input),
      opts.timeoutMs ?? DEFAULT_TIMEOUT_MS,
    );
  } catch (err) {
    return {
      status: "fallback",
      templates: fallbackTemplates(deal.contactName, tone),
      reason: err instanceof Error ? err.message : "provider_error",
    };
  }

  // Gate 2 — schema validation.
  const parsed = DraftSchema.safeParse(raw);
  if (!parsed.success) {
    return {
      status: "fallback",
      templates: fallbackTemplates(deal.contactName, tone),
      reason: "schema_validation_failed",
    };
  }
  const draft = parsed.data;

  // Gate 3 — confidence threshold.
  if (draft.confidence < CONFIDENCE_THRESHOLD) {
    return {
      status: "low_confidence",
      draft,
      usedContextIds: draft.usedContextIds,
    };
  }

  return { status: "suggested", draft, usedContextIds: draft.usedContextIds };
}

/** Reject after `ms` so a slow model never hangs the UI. */
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("provider_timeout")), ms);
    promise.then(
      (value) => {
        clearTimeout(timer);
        resolve(value);
      },
      (error: unknown) => {
        clearTimeout(timer);
        reject(error instanceof Error ? error : new Error(String(error)));
      },
    );
  });
}
