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
    // push to dataLayer (GTM-friendly)
    if (typeof window !== "undefined" && (window as any).dataLayer) {
      (window as any).dataLayer.push({
        event: "apply_click",
        job_id: job_id,
        title: title,
        location: location,
      });
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
