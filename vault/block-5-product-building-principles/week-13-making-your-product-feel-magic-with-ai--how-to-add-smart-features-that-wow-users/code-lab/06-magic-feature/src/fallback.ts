import type { TonePreference } from "./types";

/**
 * The non-AI path. It always works, needs no model, and never throws. When the
 * model is unavailable, uncertain, or produces invalid output, the user lands
 * here: exactly where they would have been without the feature, never worse off.
 */
export function fallbackTemplates(
  contactName: string,
  tone: TonePreference,
): string[] {
  const opener = tone === "formal" ? `Dear ${contactName},` : `Hi ${contactName},`;
  return [
    `${opener}\n\nJust following up on our last conversation — is this still a priority on your side? Happy to help move it forward.`,
    `${opener}\n\nChecking in to see whether you have any open questions I can answer. Let me know a good time to reconnect.`,
  ];
}
