"use client";

import Link from "next/link";

type Gtag = (command: "event", eventName: string, parameters: Record<string, string>) => void;

export default function AiTipsReturnLink({
  href,
  label,
  sourceRegion,
  destinationRegion,
}: {
  href: string;
  label: string;
  sourceRegion: string;
  destinationRegion: string;
}) {
  function trackClick() {
    const gtag = (window as Window & { gtag?: Gtag }).gtag;
    gtag?.("event", "ai_tips_return_click", {
      page_path: window.location.pathname,
      link_url: href,
      link_text: label,
      placement: "ai_tips_return_link",
      source_region: sourceRegion,
      destination_region: destinationRegion,
    });
  }

  return (
    <Link
      href={href}
      onClick={trackClick}
      className="mb-6 inline-flex min-h-11 items-center whitespace-nowrap rounded-xl border border-blue-200 bg-white px-4 text-sm font-semibold text-blue-800 hover:bg-blue-50 focus:outline-none focus:ring-4 focus:ring-blue-100"
    >
      {label}
    </Link>
  );
}
