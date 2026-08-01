import type { Metadata } from "next";
import Link from "next/link";
import { cleanEmployerName } from "@/lib/job-facts";
import { getAtAGlanceAttributes } from "@/lib/at-a-glance-preview";
import { getJobPath, getPublishedJobs } from "@/lib/published-jobs";
import styles from "@/app/at-a-glance-preview/preview.module.css";

export const metadata: Metadata = {
  title: "Compact job-list preview | Ontap Job Search",
  robots: { index: false, follow: false },
};

export default function AtAGlancePreviewPage() {
  const jobs = getPublishedJobs()
    .map((job) => ({
      job,
      attributes: getAtAGlanceAttributes(job.job_id),
    }))
    .filter(({ attributes }) => attributes.length >= 2)
    .sort((left, right) => {
      const categoryOrder = left.job.category.localeCompare(right.job.category);
      if (categoryOrder) return categoryOrder;
      const regionOrder = left.job.region.localeCompare(right.job.region);
      if (regionOrder) return regionOrder;
      return left.job.title.localeCompare(right.job.title);
    });

  const sampleJobs = jobs.filter((_, index) => index % 3 === 0).slice(0, 15);

  return (
    <main className={styles.page}>
      <div className={styles.intro}>
        <div className={styles.reviewBadge}>Review preview — not live</div>
        <h1 className={styles.heading}>Rapid job-list comparison</h1>
        <p className={styles.introText}>
          The same {sampleJobs.length} current vacancies are shown twice. Click any
          row to open the normal full job page. The purpose here is simply to see
          which compact layout makes jobs fastest to scan.
        </p>
        <div className={styles.jumpLinks}>
          <a className={styles.jumpLink} href="#one-line">
            A — single line
          </a>
          <a className={styles.jumpLink} href="#two-line">
            B — two lines
          </a>
        </div>
      </div>

      <section id="one-line" className={styles.section}>
        <h2 className={styles.sectionHeading}>A — single-line list</h2>
        <p className={styles.sectionNote}>
          Maximum density: role, employer/location, pay/contract and three key
          duties in one clickable row.
        </p>

        <div className={styles.listShell}>
          <div className={styles.oneLineHeader} aria-hidden="true">
            <span>Role</span>
            <span>Employer · location</span>
            <span>Pay · contract</span>
            <span>Quick duties</span>
            <span />
          </div>

          {sampleJobs.map(({ job, attributes }) => {
            const employerLocation = [cleanEmployerName(job), job.location]
              .filter(Boolean)
              .join(" · ");
            const terms = [job.salary_text || "Salary not stated", job.employment_type]
              .filter(Boolean)
              .join(" · ");
            const duties = attributes.slice(0, 3).join(" • ");

            return (
              <Link
                key={`one-${job.job_id}`}
                href={getJobPath(job.job_id)}
                className={styles.oneLineRow}
              >
                <span className={styles.oneLineRole} title={job.title}>
                  {job.title}
                </span>
                <span className={styles.oneLineEmployer} title={employerLocation}>
                  {employerLocation}
                </span>
                <span className={styles.oneLineTerms} title={terms}>
                  {terms}
                </span>
                <span className={styles.oneLineDuties} title={attributes.join(" • ")}>
                  {duties}
                </span>
                <span className={styles.arrow} aria-hidden="true">
                  →
                </span>
              </Link>
            );
          })}
        </div>
      </section>

      <section id="two-line" className={styles.section}>
        <h2 className={styles.sectionHeading}>B — two-line list</h2>
        <p className={styles.sectionNote}>
          Slightly more breathing room: the first line carries the decision facts;
          the second uses compact duty tags.
        </p>

        <div className={styles.listShell}>
          {sampleJobs.map(({ job, attributes }) => {
            const employerLocation = [cleanEmployerName(job), job.location]
              .filter(Boolean)
              .join(" · ");
            const terms = [job.salary_text || "Salary not stated", job.employment_type]
              .filter(Boolean)
              .join(" · ");

            return (
              <Link
                key={`two-${job.job_id}`}
                href={getJobPath(job.job_id)}
                className={styles.twoLineRow}
              >
                <span className={styles.twoLineTop}>
                  <span className={styles.twoLineRole} title={job.title}>
                    {job.title}
                  </span>
                  <span className={styles.twoLineTerms} title={terms}>
                    {terms}
                  </span>
                  <span className={styles.arrow} aria-hidden="true">
                    →
                  </span>
                </span>

                <span className={styles.twoLineBottom}>
                  <span className={styles.twoLineMeta} title={employerLocation}>
                    {employerLocation}
                  </span>
                  <span className={styles.tags}>
                    {attributes.slice(0, 4).map((attribute) => (
                      <span key={attribute} className={styles.tag}>
                        {attribute}
                      </span>
                    ))}
                  </span>
                </span>
              </Link>
            );
          })}
        </div>
      </section>
    </main>
  );
}
