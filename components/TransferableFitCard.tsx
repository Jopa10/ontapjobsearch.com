"use client";

import { useEffect, useRef } from "react";
import type { TransferableFit } from "@/lib/transferable-fit";
import styles from "./TransferableFitCard.module.css";

type TransferableFitCardProps = {
  fit: TransferableFit;
  jobId: string;
  title: string;
  employer: string;
  location: string;
  region: string;
  source: string;
  slicePath: string;
  placement: "desktop" | "mobile";
};

type TrackingWindow = Window & {
  gtag?: (...args: unknown[]) => void;
  __ontapTransferableFitViewed?: Set<string>;
};

export default function TransferableFitCard({
  fit,
  jobId,
  title,
  employer,
  location,
  region,
  source,
  slicePath,
  placement,
}: TransferableFitCardProps) {
  const cardRef = useRef<HTMLElement>(null);
  const headingId = `transferable-fit-${placement}-${jobId}`;

  useEffect(() => {
    const element = cardRef.current;
    if (!element || typeof IntersectionObserver === "undefined") return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries.some((entry) => entry.isIntersecting && entry.intersectionRatio >= 0.5)) {
          return;
        }

        const trackingWindow = window as TrackingWindow;
        trackingWindow.__ontapTransferableFitViewed ??= new Set<string>();

        if (!trackingWindow.__ontapTransferableFitViewed.has(jobId)) {
          trackingWindow.__ontapTransferableFitViewed.add(jobId);

          if (typeof trackingWindow.gtag === "function") {
            trackingWindow.gtag("event", "transferable_fit_view", {
              job_id: jobId,
              job_title: title,
              employer,
              location,
              region,
              source,
              slice_path: slicePath,
              placement,
              page_path: window.location.pathname,
            });
          }
        }

        observer.disconnect();
      },
      { threshold: [0.5] }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [employer, jobId, location, placement, region, slicePath, source, title]);

  return (
    <section ref={cardRef} className={styles.card} aria-labelledby={headingId}>
      <h2 id={headingId} className={styles.heading}>
        Why your experience may fit
      </h2>

      <p className={styles.line}>
        <strong>Similar roles:</strong> {fit.similarRoles.join(" · ")}
      </p>

      <p className={styles.line}>
        <strong>Useful experience:</strong> {fit.usefulExperience.join(" · ")}
      </p>

      <p className={styles.summary}>{fit.plainEnglish}</p>
    </section>
  );
}
