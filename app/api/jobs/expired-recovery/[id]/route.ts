import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ error: "Expired job recovery is temporarily unavailable" }, { status: 404 });
}
