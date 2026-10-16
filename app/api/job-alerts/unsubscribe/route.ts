import { createHmac, timingSafeEqual } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

function decodeToken(token: string, secret: string): string | null {
  if (token.length > 2_000) return null;
  const [payload, signature, extra] = token.split(".");
  if (!payload || !signature || extra) return null;
  try {
    const expected = createHmac("sha256", secret).update(payload, "ascii").digest();
    const actual = Buffer.from(signature, "base64url");
    if (actual.length !== expected.length || !timingSafeEqual(actual, expected)) return null;
    const decoded = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as { email?: unknown; version?: unknown };
    if (decoded.version !== 1 || typeof decoded.email !== "string") return null;
    const email = decoded.email.trim().toLowerCase();
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? email : null;
  } catch {
    return null;
  }
}

function htmlResponse(message: string, status = 200) {
  const safeMessage = message.replace(/[&<>"]/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",
  })[character] || character);
  return new NextResponse(
    `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Job alert preferences</title><body style="font:16px/1.5 Arial,sans-serif;max-width:620px;margin:12vh auto;padding:24px;color:#171717"><h1>Job alert preferences</h1><p>${safeMessage}</p><p><a href="/">Return to Ontap</a></p></body></html>`,
    { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } }
  );
}

export async function POST(request: NextRequest) {
  const secret = process.env.JOB_ALERTS_UNSUBSCRIBE_SECRET;
  const apiKey = process.env.BREVO_API_KEY;
  if (!secret || !apiKey) return htmlResponse("Unsubscribe is temporarily unavailable. Please try again later.", 503);

  let token = "";
  try {
    const form = await request.formData();
    token = String(form.get("token") || "");
  } catch {
    return htmlResponse("This unsubscribe link is invalid.", 400);
  }

  const email = decodeToken(token, secret);
  if (!email) return htmlResponse("This unsubscribe link is invalid.", 400);

  try {
    const response = await fetch(`https://api.brevo.com/v3/contacts/${encodeURIComponent(email)}`, {
      method: "PUT",
      headers: { "api-key": apiKey, "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ emailBlacklisted: true }),
      signal: AbortSignal.timeout(8_000),
      cache: "no-store",
    });
    if (!response.ok) {
      console.error("Brevo CPC alert unsubscribe failed", response.status);
      return htmlResponse("We couldn’t update your email preferences just now. Please try again.", 502);
    }
    return htmlResponse("You’re unsubscribed from Ontap CPC job alerts.");
  } catch (error) {
    console.error("CPC alert unsubscribe request failed", error);
    return htmlResponse("We couldn’t update your email preferences just now. Please try again.", 502);
  }
}
