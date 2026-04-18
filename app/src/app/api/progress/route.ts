import { NextResponse } from "next/server";
import { z } from "zod";
import { markLessonComplete } from "@/lib/db";
import { streakFromCompletions } from "@/lib/schedule";
import { getCompletedSlotKeys } from "@/lib/db";

const Body = z.object({
  slotKey: z.string().min(1),
  slug: z.string().min(1),
  notes: z.string().optional(),
  minutes: z.number().int().positive().optional(),
});

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const { slotKey, slug, notes, minutes } = parsed.data;
  markLessonComplete(slotKey, slug, notes, minutes);
  return NextResponse.json({
    ok: true,
    streak: streakFromCompletions(getCompletedSlotKeys()),
  });
}
