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
      (window as any).gtag("event", "apply_click", {
        job_id,
        title,
        location,
      });
    }
  };

  return (
    <a
      href={apply_url}
      target="_blank"
      rel="noopener noreferrer"
      onClick={handleClick}
    >
      Apply
    </a>
  );
}
