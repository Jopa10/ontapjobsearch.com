"use client";

import { useEffect, useState, type ReactNode } from "react";
import styles from "@/components/JobViewSwitcher.module.css";
import SectorSwitchBanner from "@/components/SectorSwitchBanner";

type ViewMode = "quick" | "detailed";
type SectorView = "all" | "business" | "public";

type JobViewSwitcherProps = {
  quickView: ReactNode;
  detailedView: ReactNode;
  sectorFilterEnabled?: boolean;
  sectorCounts?: { all: number; business: number; public: number };
};

const STORAGE_KEY = "ontap-job-results-view";

export default function JobViewSwitcher({
  quickView,
  detailedView,
  sectorFilterEnabled = false,
  sectorCounts,
}: JobViewSwitcherProps) {
  const [view, setView] = useState<ViewMode>("detailed");
  const [sectorView, setSectorView] = useState<SectorView>("all");

  useEffect(() => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored === "quick" || stored === "detailed") {
        queueMicrotask(() => setView(stored));
      }
    } catch {
      // Storage can be unavailable in strict privacy modes. Detailed View remains default.
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
    <div
      className={
        sectorView === "business"
          ? styles.sectorBusiness
          : sectorView === "public"
            ? styles.sectorPublic
            : styles.sectorAll
      }
      data-sector-view={sectorFilterEnabled ? sectorView : undefined}
    >
      {sectorFilterEnabled && sectorCounts ? (
        <div className={styles.sectorBlock}>
          <div className={styles.sectorHeading}>Choose which jobs to see</div>
          <div className={styles.sectorControls} role="group" aria-label="Filter jobs by sector">
            <button
              type="button"
              className={`${styles.sectorButton} ${sectorView === "all" ? styles.sectorActive : ""}`}
              aria-pressed={sectorView === "all"}
              onClick={() => setSectorView("all")}
            >
              All jobs <span>{sectorCounts.all}</span>
            </button>
            <button
              type="button"
              className={`${styles.sectorButton} ${sectorView === "business" ? styles.sectorActive : ""}`}
              aria-pressed={sectorView === "business"}
              onClick={() => setSectorView("business")}
            >
              Business &amp; agency <span>{sectorCounts.business}</span>
            </button>
            <button
              type="button"
              className={`${styles.sectorButton} ${sectorView === "public" ? styles.sectorActive : ""}`}
              aria-pressed={sectorView === "public"}
              onClick={() => setSectorView("public")}
            >
              Public service &amp; charity <span>{sectorCounts.public}</span>
            </button>
          </div>
          <p className={styles.sectorNote}>
            Clearly identified public-service and charity vacancies are grouped for you;
            anything uncertain stays under Business &amp; agency.
          </p>
        </div>
      ) : null}

      {sectorFilterEnabled && sectorView === "public" ? (
        <SectorSwitchBanner placement="overview" />
      ) : null}

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
