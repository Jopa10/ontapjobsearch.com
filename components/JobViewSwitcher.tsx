"use client";

import { useEffect, useState, type ReactNode } from "react";
import styles from "@/components/JobViewSwitcher.module.css";

type ViewMode = "quick" | "detailed";

type JobViewSwitcherProps = {
  quickView: ReactNode;
  detailedView: ReactNode;
};

const STORAGE_KEY = "ontap-job-results-view";

export default function JobViewSwitcher({
  quickView,
  detailedView,
}: JobViewSwitcherProps) {
  const [view, setView] = useState<ViewMode>("quick");

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "quick" || stored === "detailed") {
        setView(stored);
      }
    } catch {
      // Storage can be unavailable in strict privacy modes. Quick View remains default.
    }
  }, []);

  function choose(next: ViewMode) {
    setView(next);
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // The selected view still works for the current page load.
    }
  }

  return (
    <div>
      <div className={styles.controls} role="group" aria-label="Job results view">
        <span className={styles.prompt}>View jobs:</span>
        <button
          type="button"
          className={`${styles.button} ${view === "quick" ? styles.active : ""}`}
          aria-pressed={view === "quick"}
          onClick={() => choose("quick")}
        >
          Quick View
        </button>
        <button
          type="button"
          className={`${styles.button} ${view === "detailed" ? styles.active : ""}`}
          aria-pressed={view === "detailed"}
          onClick={() => choose("detailed")}
        >
          Detailed View
        </button>
      </div>

      <div hidden={view !== "quick"}>{quickView}</div>
      <div hidden={view !== "detailed"}>{detailedView}</div>
    </div>
  );
}
