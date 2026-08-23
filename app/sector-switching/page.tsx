import type { Metadata } from "next";
import Link from "next/link";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Switching Between Business, Public Service & Charity Jobs | Ontap",
  description:
    "See how admin and customer-service skills can transfer between business, agency, NHS, school, council and charity roles.",
  alternates: {
    canonical: "https://www.ontapjobsearch.com/sector-switching",
  },
};

const comparisons = [
  ["Customer enquiries", "Patients, residents, parents, service users or supporters"],
  ["Booking and scheduling", "Appointments, clinics, meetings, rotas or school activities"],
  ["Records and CRM updates", "Case, patient, pupil, donor or service records"],
  ["Working across teams", "Coordinating with clinical, teaching, council or charity teams"],
];

export default function SectorSwitchingPage() {
  return (
    <main className={styles.main}>
      <div className={styles.eyebrow}>Career switching guide</div>
      <h1>One set of admin skills, several sectors</h1>
      <p className={styles.lead}>
        Business, agency, public-service and charity employers often use different job
        titles for closely related work. Focus on the tasks and skills, not only the title.
      </p>

      <section className={styles.panel}>
        <h2>How your experience can translate</h2>
        <div className={styles.comparisons}>
          {comparisons.map(([experience, equivalent]) => (
            <div className={styles.comparison} key={experience}>
              <strong>{experience}</strong>
              <span aria-hidden="true">→</span>
              <span>{equivalent}</span>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.copy}>
        <h2>Before you apply</h2>
        <p>
          Check the essential criteria, any safeguarding or background checks, and whether
          sector-specific systems are required. If the advert says training is provided,
          show the transferable evidence you already have: accuracy, confidentiality,
          empathy, organisation and calm communication.
        </p>
      </section>

      <Link className={styles.back} href="/london/service-administrator-jobs">
        Browse London admin and customer-service jobs →
      </Link>
    </main>
  );
}
