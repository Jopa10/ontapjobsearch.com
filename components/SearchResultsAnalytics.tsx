'use client';

import { useEffect, useRef } from 'react';
import { ANALYTICS_READY_EVENT } from '@/lib/analytics-client';
import { SEARCH_SOURCE_KEY, safeSearchText, searchResultParameters } from '@/lib/search-analytics';

export default function SearchResultsAnalytics({ query, location, count, recognised, nearby }: {
  query: string; location: string; count: number; recognised: boolean; nearby: boolean;
}) {
  const sent = useRef('');
  useEffect(() => {
    const key = JSON.stringify([query, location, count, recognised, nearby]);
    const send = () => {
      const current = window as Window & { gtag?: (...args: unknown[]) => void; __ontapAnalyticsSuppressed?: string };
      if (sent.current === key || current.__ontapAnalyticsSuppressed || !current.gtag) return;
      try {
        let source = '';
        try {
          const saved = JSON.parse(sessionStorage.getItem(SEARCH_SOURCE_KEY) || 'null');
          // Only associate the immediately preceding matching form submission.
          if (saved && saved.query === safeSearchText(query) && saved.location === safeSearchText(location) && Date.now() - saved.at < 120000) {
            source = saved.path;
            sessionStorage.removeItem(SEARCH_SOURCE_KEY);
          }
        } catch { /* Storage is optional. */ }
        current.gtag('event', 'job_search_results', {
          ...searchResultParameters(query, location, count, recognised, nearby),
          source_page: source || 'direct_or_link',
          page_path: window.location.pathname,
        });
        sent.current = key;
      } catch { /* Measurement must never affect search. */ }
    };
    send();
    window.addEventListener(ANALYTICS_READY_EVENT, send);
    return () => window.removeEventListener(ANALYTICS_READY_EVENT, send);
  }, [query, location, count, recognised, nearby]);
  return null;
}
