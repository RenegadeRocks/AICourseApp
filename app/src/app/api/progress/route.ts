import { NextResponse } from "next/server";
import { z } from "zod";
import { markComplete, currentStreak } from "@/lib/db";

const Body = z.object({
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  slug: z.string().min(1),
  notes: z.string().optional(),
  minutes: z.number().int().positive().optional(),
});

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const { date, slug, notes, minutes } = parsed.data;
  markComplete(date, slug, notes, minutes);
  return NextResponse.json({ ok: true, streak: currentStreak(date) });
}
