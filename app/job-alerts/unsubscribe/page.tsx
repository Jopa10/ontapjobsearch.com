type PageProps = { searchParams: Promise<{ token?: string }> };

export default async function UnsubscribePage({ searchParams }: PageProps) {
  const { token = "" } = await searchParams;
  const safeToken = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(token) ? token : "";

  return (
    <main style={{ maxWidth: 620, margin: "12vh auto", padding: "24px", fontFamily: "Arial, sans-serif", color: "#171717" }}>
      <h1 style={{ fontSize: 26 }}>Unsubscribe from CPC job alerts</h1>
      {safeToken ? (
        <>
          <p style={{ color: "#475569", lineHeight: 1.6 }}>Confirm below to stop Ontap CPC job alert emails for this address.</p>
          <form method="post" action="/api/job-alerts/unsubscribe">
            <input type="hidden" name="token" value={safeToken} />
            <button type="submit" style={{ border: 0, borderRadius: 7, padding: "12px 16px", background: "#1d4ed8", color: "#fff", font: "inherit", fontWeight: 700, cursor: "pointer" }}>
              Unsubscribe
            </button>
          </form>
        </>
      ) : (
        <p style={{ color: "#475569" }}>This unsubscribe link is invalid. Use the unsubscribe link in a recent alert email.</p>
      )}
    </main>
  );
}
