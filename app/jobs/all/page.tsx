const jobSections = [
  {
    heading: "Support Worker Jobs",
    cards: [
      {
        title: "West Yorkshire Support Worker Jobs",
        href: "/west-yorkshire/support-worker",
      },
      {
        title: "South Yorkshire Support Worker Jobs",
        href: "/south-yorkshire/support-worker",
      },
    ],
  },
  {
    heading: "Service Administrator Jobs",
    cards: [
      {
        title: "West Yorkshire Service Administrator Jobs",
        href: "/west-yorkshire/service-administrator-jobs",
      },
      {
        title: "South Yorkshire Service Administrator Jobs",
        href: "/south-yorkshire/service-administrator-jobs",
      },
    ],
  },
];

const cardStyle = {
  display: "block",
  border: "1px solid #e5e7eb",
  borderRadius: 10,
  padding: 16,
  textDecoration: "none",
  color: "inherit",
};

export default function Page() {
  return (
    <main style={{ maxWidth: 980, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 12 }}>
        Browse Jobs
      </h1>

      <p style={{ color: "#555", marginBottom: 24 }}>
        Browse current Yorkshire job pages.
      </p>

      <div style={{ display: "grid", gap: 28 }}>
        {jobSections.map((section) => (
          <section key={section.heading}>
            <h2 style={{ fontSize: 22, fontWeight: 700, marginBottom: 12 }}>
              {section.heading}
            </h2>

            <div style={{ display: "grid", gap: 12 }}>
              {section.cards.map((card) => (
                <a key={card.href} href={card.href} style={cardStyle}>
                  <div style={{ fontWeight: 700, marginBottom: 4 }}>
                    {card.title}
                  </div>
                  <div style={{ color: "#555" }}>{card.title}</div>
                </a>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
