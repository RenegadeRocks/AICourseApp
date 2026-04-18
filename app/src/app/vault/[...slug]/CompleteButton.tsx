"use client";
import { useState } from "react";

export default function CompleteButton({
  slotKey,
  slug,
  label,
  initiallyDone,
}: {
  slotKey: string;
  slug: string;
  /** Short label shown next to the checkmark after completion (e.g. "Week 5 · Day 3"). */
  label: string;
  initiallyDone: boolean;
}) {
  const [done, setDone] = useState(initiallyDone);
  const [streak, setStreak] = useState<number | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function markComplete() {
    setPending(true);
    setError(null);
    try {
      const res = await fetch("/api/progress", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ slotKey, slug }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as { ok: boolean; streak: number };
      setDone(true);
      setStreak(data.streak);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to mark complete");
    } finally {
      setPending(false);
    }
  }

  if (done) {
    return (
      <div className="inline-flex items-center gap-2 text-sm text-emerald-700">
        <span
          aria-hidden
          className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-emerald-500 text-white text-xs"
        >
          ✓
        </span>
        <span>Completed · {label}</span>
        {streak !== null && (
          <span className="text-stone-500">· {streak} lesson streak</span>
        )}
      </div>
    );
  }

  return (
    <div className="inline-flex items-center gap-2">
      <button
        onClick={markComplete}
        disabled={pending}
        className="inline-flex items-center gap-2 rounded-md bg-accent px-3 py-1.5 text-sm font-medium text-white hover:bg-amber-700 disabled:opacity-50 transition"
      >
        {pending ? "Saving…" : "Mark complete"}
      </button>
      {error && <span className="text-xs text-red-600">{error}</span>}
    </div>
  );
}
