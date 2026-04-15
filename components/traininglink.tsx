"use client";

type Props = {
  href: string;
  title: string;
  provider: string;
};

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}

export default function TrainingLink({ href, title, provider }: Props) {
  function handleClick() {
    if (typeof window !== "undefined" && typeof window.gtag === "function") {
      window.gtag("event", "training_click", {
        course_title: title,
        provider,
        link_url: href,
        page_path: window.location.pathname,
      });
    }
  }

  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      onClick={handleClick}
      style={{ fontSize: 12, color: "#2563eb" }}
    >
      Course details
    </a>
  );
}
