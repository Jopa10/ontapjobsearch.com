"use client";

type Props = {
  apply_url: string;
  job_id: string;
  title: string;
  location: string;
};

export default function ApplyButton({
  apply_url,
  job_id,
  title,
  location,
}: Props) {
  const handleClick = () => {
    // fire GA event (no callback)
    if (typeof window !== "undefined" && (window as any).gtag) {
      (window as any).gtag("event", "apply_click", {
        event_category: "engagement",
        event_label: title,
        job_id,
        location,
      });
    }

    // open immediately (no delay)
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
