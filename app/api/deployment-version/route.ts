import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

function currentDeploymentVersion() {
  return (
    process.env.VERCEL_GIT_COMMIT_SHA ||
    process.env.VERCEL_URL ||
    null
  );
}

export async function GET() {
  return NextResponse.json(
    { version: currentDeploymentVersion() },
    {
      headers: {
        "Cache-Control": "no-store, max-age=0",
      },
    },
  );
}
