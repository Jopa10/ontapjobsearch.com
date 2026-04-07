export default function Page() {
  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 12 }}>
        Browse Support Worker Jobs
      </h1>

      <p style={{ color: "#555", marginBottom: 24 }}>
        Browse current Yorkshire support worker slices.
      </p>

      <div style={{ display: "grid", gap: 12 }}>
        <a
          href="/west-yorkshire/support-worker"
          style={{
            display: "block",
            border: "1px solid #e5e7eb",
            borderRadius: 10,
            padding: 16,
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 4 }}>
            West Yorkshire Support Worker Jobs
          </div>
          <div style={{ color: "#555" }}>
            Primary Yorkshire slice
          </div>
        </a>

        <a
          href="/south-yorkshire/support-worker"
          style={{
            display: "block",
            border: "1px solid #e5e7eb",
            borderRadius: 10,
            padding: 16,
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 4 }}>
            South Yorkshire Support Worker Jobs
          </div>
          <div style={{ color: "#555" }}>
            Secondary Yorkshire slice
          </div>
        </a>
      </div>
    </main>
  );
}
