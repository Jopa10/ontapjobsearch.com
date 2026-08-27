"use client";

import {
  buildApplyClickParameters,
  type ApplyClickDetails,
} from "@/lib/apply-click-tracking";

export default function ApplyButton({
  apply_url,
  job_id,
  title,
  employer,
  location,
  region,
  source,
  slice_path,
}: ApplyClickDetails) {
  const handleClick = () => {
    const gtag = (
      window as Window & { gtag?: (...args: unknown[]) => void }
    ).gtag;

    if (typeof gtag === "function") {
      gtag(
        "event",
        "apply_click",
        buildApplyClickParameters(
          {
            apply_url,
            job_id,
            title,
            employer,
            location,
            region,
            source,
            slice_path,
          },
          window.location.pathname
        )
      );
    }
  };

  return (
    <a
      href={apply_url}
      target="_blank"
      rel="noopener noreferrer"
      onClick={handleClick}
      style={{
        display: "inline-block",
        background: "#2563eb",
        color: "#fff",
        border: "none",
        borderRadius: "8px",
        padding: "10px 16px",
        cursor: "pointer",
        fontSize: "16px",
        textDecoration: "none",
      }}
    >
      Apply Now
    </a>
  );
}
