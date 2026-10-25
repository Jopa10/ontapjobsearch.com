"use client";

import { useEffect } from "react";
import { initializeSessionReferral, touchSessionReferral } from "@/lib/session-referral";
import {
  ANALYTICS_MEASUREMENT_ID,
  ANALYTICS_READY_EVENT,
  daysBetween,
  hasCampaignParameters,
  isLikelyAutomation,
  pageContext,
} from "@/lib/analytics-client";

import { SEARCH_SOURCE_KEY, safeSearchText } from "@/lib/search-analytics";

const FIRST_SEEN_KEY = "ontap.analytics-first-seen.v1";
const LAST_SEEN_KEY = "ontap.analytics-last-seen.v1";
const RETURN_SESSION_KEY = "ontap.analytics-return-session.v1";
const QUALIFIED_SESSION_KEY = "ontap.analytics-qualified-session.v1";
const SAVED_LOCATION_KEY = "ontap.saved-location.v1";
const RETURN_GAP_MS = 30 * 60 * 1000;

type AnalyticsWindow = Window & {
  dataLayer?: unknown[];
  gtag?: (...args: unknown[]) => void;
  __ontapAnalyticsLoaded?: boolean;
  __ontapAnalyticsSuppressed?: "automation";
};

function readNumber(storage: Storage, key: string): number | undefined {
  try {
    const value = Number(storage.getItem(key));
    return Number.isFinite(value) && value > 0 ? value : undefined;
  } catch {
    return undefined;
  }
}

function writeValue(storage: Storage, key: string, value: string) {
  try {
    storage.setItem(key, value);
  } catch {
    // Analytics storage must never affect the job-search experience.
  }
}

function hasStoredValue(storage: Storage, key: string): boolean {
  try {
    return storage.getItem(key) !== null;
  } catch {
    return false;
  }
}

export default function Analytics() {
  useEffect(() => {
    const analyticsWindow = window as AnalyticsWindow;
    if (analyticsWindow.__ontapAnalyticsSuppressed) return;

    if (!analyticsWindow.__ontapAnalyticsLoaded) {
      if (isLikelyAutomation(window.navigator.userAgent)) {
        analyticsWindow.__ontapAnalyticsSuppressed = "automation";
        return;
      }

      analyticsWindow.__ontapAnalyticsLoaded = true;
      analyticsWindow.dataLayer = analyticsWindow.dataLayer ?? [];
      analyticsWindow.gtag = analyticsWindow.gtag ?? ((...args: unknown[]) => {
        analyticsWindow.dataLayer?.push(args);
      });

      const gtag = analyticsWindow.gtag;
      gtag("js", new Date());
      gtag("config", ANALYTICS_MEASUREMENT_ID);

      if (!document.querySelector(`script[src*="googletagmanager.com/gtag/js?id=${ANALYTICS_MEASUREMENT_ID}"]`)) {
        const script = document.createElement("script");
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_MEASUREMENT_ID}`;
        document.head.appendChild(script);
      }
    }

    const gtag = analyticsWindow.gtag;
    if (typeof gtag !== "function") return;
    window.dispatchEvent(new Event(ANALYTICS_READY_EVENT));

    initializeSessionReferral(sessionStorage, document.referrer, window.location.search);

    const now = Date.now();
    const firstSeen = readNumber(localStorage, FIRST_SEEN_KEY);
    const lastSeen = readNumber(localStorage, LAST_SEEN_KEY);
    const isReturn = firstSeen !== undefined
      && lastSeen !== undefined
      && now - lastSeen >= RETURN_GAP_MS;

    if (firstSeen === undefined) writeValue(localStorage, FIRST_SEEN_KEY, String(now));
    writeValue(localStorage, LAST_SEEN_KEY, String(now));

    if (isReturn && !hasStoredValue(sessionStorage, RETURN_SESSION_KEY)) {
      writeValue(sessionStorage, RETURN_SESSION_KEY, "tracked");
      gtag("event", "returning_browser", {
        days_since_first_seen: daysBetween(firstSeen, now),
        saved_location_present: hasStoredValue(localStorage, SAVED_LOCATION_KEY) ? 1 : 0,
        referrer_present: document.referrer ? 1 : 0,
        campaign_parameters_present: hasCampaignParameters(window.location.search) ? 1 : 0,
        page_context: pageContext(window.location.pathname),
        page_path: window.location.pathname,
      });
    }

    const trackSearch = (event: Event) => {
      try {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;
        const target = new URL(form.action, window.location.href);
        if (target.origin !== window.location.origin || target.pathname !== "/jobs/search") return;
        const fields = new FormData(form);
        const query = String(fields.get("q") || "").trim();
        const location = String(fields.get("location") || "").trim();
        if (!query && !location) return;
        // Store only sanitised inputs; navigation and search never depend on storage.
        try {
          sessionStorage.setItem(SEARCH_SOURCE_KEY, JSON.stringify({
            query: safeSearchText(query), location: safeSearchText(location),
            path: window.location.pathname, at: Date.now(),
          }));
        } catch { /* Storage is optional. */ }
        gtag("event", "job_search_submit", {
          search_term: safeSearchText(query), search_location: safeSearchText(location),
          source_page: window.location.pathname, form_id: form.id || "search-results-form",
          transport_type: "beacon",
        });
      } catch { /* Analytics must never block a form submission. */ }
    };
    document.addEventListener("submit", trackSearch, true);

    const events = ["pointerdown", "keydown", "touchstart", "scroll"] as const;
    const refreshReferralActivity = (event: Event) => {
      if (event.isTrusted) touchSessionReferral(sessionStorage);
    };
    events.forEach((eventName) =>
      window.addEventListener(eventName, refreshReferralActivity, { capture: true, passive: true })
    );

    const trackQualifiedVisit = (event: Event) => {
      if (!event.isTrusted) return;
      touchSessionReferral(sessionStorage);
      if (hasStoredValue(sessionStorage, QUALIFIED_SESSION_KEY)) return;
      writeValue(sessionStorage, QUALIFIED_SESSION_KEY, "tracked");
      gtag("event", "qualified_visit", {
        qualification_signal: event.type,
        returning_browser: isReturn ? 1 : 0,
        saved_location_present: hasStoredValue(localStorage, SAVED_LOCATION_KEY) ? 1 : 0,
        referrer_present: document.referrer ? 1 : 0,
        campaign_parameters_present: hasCampaignParameters(window.location.search) ? 1 : 0,
        page_context: pageContext(window.location.pathname),
        page_path: window.location.pathname,
      });
      events.forEach((eventName) => window.removeEventListener(eventName, trackQualifiedVisit));
    };

    events.forEach((eventName) => window.addEventListener(eventName, trackQualifiedVisit, { passive: true }));

    return () => {
      document.removeEventListener("submit", trackSearch, true);
      events.forEach((eventName) => {
        window.removeEventListener(eventName, refreshReferralActivity, true);
        window.removeEventListener(eventName, trackQualifiedVisit);
      });
    };
  }, []);

  return null;
}
