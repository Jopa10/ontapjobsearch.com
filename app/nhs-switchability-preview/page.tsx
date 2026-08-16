import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "NHS switchability preview | Ontap",
  robots: { index: false, follow: false },
};

type PreviewJob = {
  id: string;
  title: string;
  employer: string;
  location: string;
  salary: string;
  employmentType: string;
  source: "Commercial" | "NHS Jobs";
  href: string;
  switcherText?: string;
  switcherDetail?: string;
};

const jobs: PreviewJob[] = [
  {
    id: "23643_225468085",
    title: "Administrator - Temporary to Permanent - Team Valley",
    employer: "Office Angels",
    location: "Gateshead",
    salary: "£13 per hour",
    employmentType: "Temporary",
    source: "Commercial",
    href: "/jobs/23643_225468085",
  },
  {
    id: "C9317-26-0646",
    title: "Clinical Administrator",
    employer: "The Newcastle upon Tyne Hospitals NHS Foundation Trust",
    location: "Newcastle upon Tyne",
    salary: "£25,760 to £27,476",
    employmentType: "Permanent",
    source: "NHS Jobs",
    href: "https://beta.jobs.nhs.uk/candidate/jobadvert/C9317-26-0646",
    switcherText: "Open to applicants from outside the NHS",
    switcherDetail: "No essential NHS, healthcare or named-system experience is required — relevant experience from other sectors can count.",
  },
  {
    id: "20279_61775-deab967b99c6e63d0dd459a12179664a",
    title: "Call Centre Agent",
    employer: "EE",
    location: "Gateshead",
    salary: "£26,116 rising to £26,738",
    employmentType: "Permanent",
    source: "Commercial",
    href: "/jobs/20279_61775-deab967b99c6e63d0dd459a12179664a",
  },
  {
    id: "A4389-26-0007",
    title: "Care Navigator / Medical Receptionist",
    employer: "Newburn Surgery",
    location: "Newcastle upon Tyne",
    salary: "Salary negotiable",
    employmentType: "Permanent",
    source: "NHS Jobs",
    href: "https://beta.jobs.nhs.uk/candidate/jobadvert/A4389-26-0007",
    switcherText: "Open to applicants from outside the NHS",
    switcherDetail: "No essential NHS, healthcare or named-system experience is required — relevant experience from other sectors can count.",
  },
  {
    id: "23643_225444106",
    title: "Administrator - Gateshead - Temp to Perm",
    employer: "Office Angels",
    location: "Gateshead",
    salary: "£13 per hour; £28,000–£30,000 permanent salary",
    employmentType: "Temporary to permanent",
    source: "Commercial",
    href: "/jobs/23643_225444106",
  },
  {
    id: "C9263-26-0682",
    title: "Mental Health Legislation Administrator",
    employer: "Cumbria, Northumberland, Tyne and Wear NHS Foundation Trust",
    location: "Gosforth",
    salary: "£28,392 to £31,157",
    employmentType: "Permanent",
    source: "NHS Jobs",
    href: "https://beta.jobs.nhs.uk/candidate/jobadvert/C9263-26-0682",
    switcherText: "Open to applicants from outside the NHS",
    switcherDetail: "No essential NHS, healthcare or named-system experience is required — relevant experience from other sectors can count.",
  },
  {
    id: "B0170-26-0034",
    title: "Patient Services Administrator",
    employer: "South Tyneside Health Collaboration",
    location: "Sunderland",
    salary: "£24,852.61 to £25,143.22",
    employmentType: "Permanent",
    source: "NHS Jobs",
    href: "https://beta.jobs.nhs.uk/candidate/jobadvert/B0170-26-0034",
    switcherText: "Open to applicants from outside the NHS",
    switcherDetail: "No essential NHS, healthcare or named-system experience is required — relevant experience from other sectors can count.",
  },
];

const pageStyle = {
  maxWidth: 1180,
  margin: "36px auto",
  padding: "0 16px 48px",
} as const;

export default function Page() {
  return (
    <main style={pageStyle}>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 1fr)",
          gap: 18,
        }}
      >
        <section>
          <div
            style={{
              display: "inline-flex",
              padding: "5px 9px",
              borderRadius: 999,
              background: "#f3f4f6",
              color: "#4b5563",
              fontSize: 12,
              fontWeight: 700,
              marginBottom: 10,
            }}
          >
            REVIEW PREVIEW — NOT LIVE PUBLISHING
          </div>
          <h1 style={{ fontSize: 28, fontWeight: 800, margin: "0 0 6px" }}>
            Newcastle Admin & Customer Service Jobs
          </h1>
          <p style={{ color: "#6b7280", fontSize: 14, margin: 0, lineHeight: 1.55 }}>
            Example of NHS Jobs mixed into the normal Ontap slice. Commercial and NHS roles stay in one list; Ontap only adds eligibility guidance where the person specification supports it.
          </p>
        </section>

        <div
          style={{
            border: "1px solid #dbe3ee",
            borderRadius: 12,
            background: "#fff",
            overflow: "hidden",
          }}
        >
          {jobs.map((job, index) => {
            const external = job.source === "NHS Jobs";
            return (
              <a
                key={job.id}
                href={job.href}
                target={external ? "_blank" : undefined}
                rel={external ? "noreferrer" : undefined}
                style={{
                  display: "block",
                  padding: "15px 16px",
                  borderBottom: index === jobs.length - 1 ? "none" : "1px solid #e5e7eb",
                  textDecoration: "none",
                  color: "inherit",
                  background: "#fff",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    gap: 12,
                    alignItems: "flex-start",
                    justifyContent: "space-between",
                  }}
                >
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontSize: 13, fontWeight: 800, color: "#374151", marginBottom: 3 }}>
                      {job.location}
                    </div>
                    <div style={{ fontSize: 17, fontWeight: 800, lineHeight: 1.3 }}>
                      {job.title}
                    </div>
                    <div style={{ color: "#4b5563", fontSize: 14, marginTop: 4 }}>
                      {job.employer}
                    </div>
                  </div>
                  <span style={{ fontSize: 20, color: "#6b7280", lineHeight: 1 }}>→</span>
                </div>

                <div style={{ display: "flex", flexWrap: "wrap", gap: 7, marginTop: 9, alignItems: "center" }}>
                  <span style={{ fontSize: 13, color: "#4b5563" }}>{job.salary}</span>
                  <span style={{ color: "#c4c7cc" }}>·</span>
                  <span style={{ fontSize: 13, color: "#4b5563" }}>{job.employmentType}</span>
                  {job.source === "NHS Jobs" ? (
                    <>
                      <span style={{ color: "#c4c7cc" }}>·</span>
                      <span style={{ fontSize: 12, color: "#6b7280" }}>NHS Jobs</span>
                    </>
                  ) : null}
                </div>

                {job.switcherText ? (
                  <div style={{ marginTop: 10 }}>
                    <span
                      style={{
                        display: "inline-flex",
                        alignItems: "center",
                        border: "1px solid #b8d7c4",
                        background: "#f3faf6",
                        borderRadius: 999,
                        padding: "4px 8px",
                        fontSize: 12,
                        fontWeight: 800,
                        color: "#275c3b",
                      }}
                    >
                      {job.switcherText} · No NHS experience required
                    </span>
                    <div style={{ fontSize: 12, color: "#6b7280", lineHeight: 1.45, marginTop: 6 }}>
                      {job.switcherDetail}
                    </div>
                  </div>
                ) : null}
              </a>
            );
          })}
        </div>

        <aside
          style={{
            border: "1px solid #e5e7eb",
            borderRadius: 12,
            padding: "14px 16px",
            background: "#f9fafb",
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 5 }}>How Ontap could use this</div>
          <div style={{ color: "#5f6368", fontSize: 13, lineHeight: 1.55 }}>
            Keep sector and employer neutral in the main list. Add a small eligibility cue only when Ontap has checked the essential person specification. Later, the same cue can work for council, university, charity and civil-service roles — so “Looking to switch” is an Ontap feature, not an NHS feature.
          </div>
        </aside>
      </div>
    </main>
  );
}
