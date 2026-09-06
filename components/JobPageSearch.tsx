"use client";

import { useState } from "react";
import styles from "@/components/JobPageSearch.module.css";

export default function JobPageSearch() {
  const [expanded, setExpanded] = useState(false);

  return (
    <section className={styles.search} aria-label="Search other jobs">
      <button
        type="button"
        className={styles.mobileToggle}
        aria-expanded={expanded}
        aria-controls="job-page-search-fields"
        onClick={() => setExpanded((current) => !current)}
      >
        <img
          src="/assets/ontap-magnifying-glass.svg"
          alt=""
          aria-hidden="true"
          className={styles.icon}
        />
        <span>{expanded ? "Hide search ↑" : "Tap to search other jobs ↓"}</span>
      </button>

      <form
        id="job-page-search-fields"
        method="get"
        action="/jobs/search"
        className={`${styles.form} ${expanded ? styles.expanded : ""}`}
      >
        <div className={styles.heading}>Search other jobs</div>

        <label className={styles.field}>
          <span className={styles.srOnly}>Role or keyword</span>
          <input
            name="q"
            type="search"
            placeholder="Role or keyword"
            autoCorrect="on"
            spellCheck={true}
          />
        </label>

        <label className={styles.field}>
          <span className={styles.srOnly}>Town or region</span>
          <input
            name="location"
            type="search"
            placeholder="Town or region"
            autoCorrect="on"
            spellCheck={true}
          />
        </label>

        <button type="submit" className={styles.submit}>
          Search jobs <span aria-hidden="true">→</span>
        </button>
      </form>
    </section>
  );
}
