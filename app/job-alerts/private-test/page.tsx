import { notFound, redirect } from "next/navigation";
import { getPublishedJob } from "@/lib/published-jobs";
import { PRIVATE_TEST_EMAIL, privateTestEnabled, sendPrivatePreviewTest } from "@/lib/private-job-alert-test";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";
export const metadata = { title: "Private email test | Ontap", robots: { index: false, follow: false } };

export default async function PrivateTestPage({ searchParams }: {
  searchParams: Promise<{ result?: string; error?: string }>;
}) {
  if (!privateTestEnabled(process.env)) notFound();
  const { result, error } = await searchParams;

  async function sendTest() {
    "use server";
    if (!privateTestEnabled(process.env)) notFound();
    let message = "";
    try {
      await sendPrivatePreviewTest({ env: process.env, findJob: getPublishedJob });
    } catch (error) {
      message = error instanceof Error ? error.message : "The test could not be completed.";
    }
    // Network errors can contain internal information; only show our known messages.
    const safeMessage = /^(Private test|The Preview|Could not read|The test address|The signup job|A test was|Brevo did)/.test(message)
      ? message : "The test could not be completed. Check Brevo logs before trying again.";
    redirect(message
      ? "/job-alerts/private-test?error=" + encodeURIComponent(safeMessage)
      : "/job-alerts/private-test?result=sent");
  }

  return (
    <main style={{ maxWidth: 620, margin: "8vh auto", padding: 24, color: "#171717", background: "#fff" }}>
      <h1 style={{ fontSize: 26 }}>Private Ontap email test</h1>
      <p>Send one sample job alert to <strong>{PRIVATE_TEST_EMAIL}</strong>.</p>
      <p>This uses your saved signup job and preferences. Its job and unsubscribe links open this Preview site.</p>
      {result === "sent" ? (
        <p role="status">Brevo accepted the test email. Check your inbox and spam folder, then try the job and unsubscribe links.</p>
      ) : (
        <>
          {error ? <p role="alert">{error.slice(0, 250)}</p> : null}
          <form action={sendTest}>
            <button type="submit" style={{ background: "#1d4ed8", color: "#fff", border: 0, borderRadius: 7, padding: "12px 16px", font: "inherit", cursor: "pointer" }}>
              Send private test email
            </button>
          </form>
        </>
      )}
      <p style={{ color: "#64748b", fontSize: 14 }}>Only this address receives the test. Other contacts and the daily email schedule are unchanged.</p>
    </main>
  );
}
