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
  if (typeof window !== "undefined" && (window as any).gtag) {
  (window as any).gtag("event", "select_content", {
    content_type: "job",
    item_id: job_id,
    item_name: title,
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
