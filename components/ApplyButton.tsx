"use client";

import {
  buildApplyClickParameters,
  type ApplyClickDetails,
} from "@/lib/apply-click-tracking";

export default function ApplyButton({
  apply_url,
  job_id,
  title,
  location,
  region,
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
          { apply_url, job_id, title, location, region, slice_path },
          window.location.pathname
        )
      );
    }

    // open immediately
    window.open(apply_url, "_blank", "noopener,noreferrer");
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      style={{
        background: "#2563eb",
        color: "#fff",
        border: "none",
        borderRadius: "8px",
        padding: "10px 16px",
        cursor: "pointer",
        fontSize: "16px",
      }}
    >
      Apply Now
    </button>
  );
}
