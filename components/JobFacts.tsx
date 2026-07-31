import { buildJobFacts, type JobFactsInput } from "@/lib/job-facts";
import styles from "@/components/JobFacts.module.css";

type JobFactsProps = {
  job: JobFactsInput;
  anchorTown?: string;
  variant?: "card" | "detail";
};

export default function JobFacts({
  job,
  anchorTown,
  variant = "card",
}: JobFactsProps) {
  const facts = buildJobFacts(job);
  if (!facts.length) return null;

  return (
    <dl
      className={`${styles.facts} ${
        variant === "detail" ? styles.detail : styles.card
      }`}
    >
      {facts.map((fact) => {
        const compactSource = variant === "card" && fact.key === "source";

        return (
          <div
            className={`${styles.fact} ${compactSource ? styles.compactSource : ""}`}
            key={fact.key}
          >
            <dt className={styles.label}>{fact.label}</dt>
            <dd className={styles.value}>
              {fact.value}
              {fact.key === "location" && anchorTown && fact.value === anchorTown ? (
                <span className={styles.anchorTown}>{anchorTown}</span>
              ) : null}
            </dd>
          </div>
        );
      })}
    </dl>
  );
}
