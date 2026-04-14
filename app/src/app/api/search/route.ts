import { NextResponse } from "next/server";
import { searchVault } from "@/lib/search";

export const dynamic = "force-dynamic";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get("q") ?? "";
  if (!q.trim()) return NextResponse.json({ hits: [] });
  const hits = searchVault(q, 30);
  return NextResponse.json({ hits });
}
