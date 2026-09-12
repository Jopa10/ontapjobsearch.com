"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { type MouseEvent } from "react";
import { RESULTS_RETURN_KEY } from "@/components/ResultsJobLink";

type BackToResultsProps = {
  fallbackHref: string;
  className?: string;
};

export default function BackToResults({ fallbackHref, className }: BackToResultsProps) {
  const router = useRouter();

  function goBack(event: MouseEvent<HTMLAnchorElement>) {
    let hasStoredResults = false;

    try {
      const stored = window.sessionStorage.getItem(RESULTS_RETURN_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as {
          href?: string;
          destination?: string;
          savedAt?: number;
        };
        const destinationPath = parsed.destination
          ? new URL(parsed.destination, window.location.origin).pathname
          : "";
        hasStoredResults = Boolean(
          parsed.href &&
            parsed.savedAt &&
            Date.now() - parsed.savedAt < 4 * 60 * 60 * 1000 &&
            destinationPath === window.location.pathname,
        );
      }
    } catch {
      // Use the safe listing fallback below.
    }

    if (hasStoredResults && window.history.length > 1) {
      event.preventDefault();
      window.sessionStorage.removeItem(RESULTS_RETURN_KEY);
      router.back();
    }
  }

  return (
    <Link href={fallbackHref} className={className} onClick={goBack}>
      <span aria-hidden="true">←</span> Back to results
    </Link>
  );
}
