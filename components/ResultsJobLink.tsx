"use client";

import Link from "next/link";
import type { ComponentProps, MouseEvent } from "react";

export const RESULTS_RETURN_KEY = "ontap-results-return";

type ResultsJobLinkProps = ComponentProps<typeof Link>;

export default function ResultsJobLink({ href, onClick, ...props }: ResultsJobLinkProps) {
  function rememberResults(event: MouseEvent<HTMLAnchorElement>) {
    try {
      window.sessionStorage.setItem(
        RESULTS_RETURN_KEY,
        JSON.stringify({
          href: `${window.location.pathname}${window.location.search}${window.location.hash}`,
          destination: typeof href === "string" ? href : href.pathname,
          savedAt: Date.now(),
        }),
      );
    } catch {
      // Browser history still provides the normal back behaviour if storage is unavailable.
    }

    onClick?.(event);
  }

  return <Link {...props} href={href} onClick={rememberResults} />;
}
