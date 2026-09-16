"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import styles from "@/components/SavedLocationJobs.module.css";

const STORAGE_KEY = "ontap.saved-location.v1";
const LOCATION_EVENT = "ontap:saved-location-jobs";
const RETURN_SESSION_KEY = "ontap.saved-location-return-session.v1";
const RETURN_RESULTS_KEY = "ontap.saved-location-return-results.v1";

type SavedLocation = { town: string; region: string };
type SavedLocationPreference = SavedLocation & { count?: number; savedAt?: number };
type NearbyJob = {
  job_id: string;
  title: string;
  location: string;
  salary_text: string;
  employment_type: string;
  distance_miles: number;
};
type NearbyResponse = {
  location: SavedLocation;
  count: number;
  suitableJobs: NearbyJob[];
  error?: string;
};
type LocationMethod = "saved" | "geolocation" | "manual";

export const savedLocationJobsEvent = LOCATION_EVENT;

function trackNearbyEvent(
  eventName:
    | "nearby_location_click"
    | "nearby_location_success"
    | "nearby_results_click"
    | "saved_location_return"
    | "saved_location_results_loaded",
  jobId: string | undefined,
  parameters: Record<string, string | number> = {},
) {
  const gtag = (window as Window & { gtag?: (...args: unknown[]) => void }).gtag;
  if (typeof gtag !== "function") return;

  gtag("event", eventName, {
    page_context: jobId ? "job_detail" : "homepage",
    page_path: window.location.pathname,
    ...parameters,
  });
}

function readSavedLocation(): SavedLocationPreference | undefined {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "null") as Partial<SavedLocationPreference> | null;
    return parsed?.town && parsed?.region
      ? {
          town: parsed.town,
          region: parsed.region,
          count: typeof parsed.count === "number" ? parsed.count : undefined,
          savedAt: typeof parsed.savedAt === "number" ? parsed.savedAt : undefined,
        }
      : undefined;
  } catch {
    return undefined;
  }
}

function readSessionMarker(key: string): string | null {
  try {
    return sessionStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeSessionMarker(key: string, value: string) {
  try {
    sessionStorage.setItem(key, value);
  } catch {
    // Tracking must never prevent the nearby-jobs experience from working.
  }
}

export default function SavedLocationJobs({ jobId }: { jobId?: string }) {
  const [status, setStatus] = useState<"idle" | "loading" | "saved" | "error">("idle");
  const [saved, setSaved] = useState<SavedLocation>();
  const [count, setCount] = useState<number>();
  const [message, setMessage] = useState("");
  const [showManual, setShowManual] = useState(false);

  async function lookup(payload: Record<string, unknown>, method: LocationMethod) {
    if (method !== "saved") {
      setStatus("loading");
      setMessage("");
    }
    try {
      const response = await fetch("/api/jobs/nearby", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...payload, jobId }),
      });
      const data = await response.json() as NearbyResponse;
      if (!response.ok) throw new Error(data.error || "Location lookup failed.");
      const existingPreference = method === "saved" ? readSavedLocation() : undefined;
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        ...data.location,
        count: data.count,
        savedAt: existingPreference?.savedAt ?? Date.now(),
      }));
      setSaved(data.location);
      setCount(data.count);
      setStatus("saved");
      setShowManual(false);
      window.dispatchEvent(new CustomEvent(LOCATION_EVENT, {
        detail: {
          jobId,
          location: data.location,
          jobs: data.suitableJobs,
          searchPath: `/jobs/search?near=${encodeURIComponent(data.location.town)}`,
        },
      }));
      if (method !== "saved") {
        writeSessionMarker(RETURN_SESSION_KEY, "current");
        trackNearbyEvent("nearby_location_success", jobId, {
          location_method: method,
          nearby_job_count: data.count,
        });
      } else if (
        readSessionMarker(RETURN_SESSION_KEY) === "return"
        && readSessionMarker(RETURN_RESULTS_KEY) !== "tracked"
      ) {
        writeSessionMarker(RETURN_RESULTS_KEY, "tracked");
        trackNearbyEvent("saved_location_results_loaded", jobId, {
          nearby_job_count: data.count,
        });
      }
    } catch (error) {
      if (method === "saved") return;
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Location lookup failed.");
      setShowManual(true);
    }
  }

  useEffect(() => {
    const location = readSavedLocation();
    if (location) {
      if (readSessionMarker(RETURN_SESSION_KEY) === null) {
        writeSessionMarker(RETURN_SESSION_KEY, "return");
        const daysSinceSaved = location.savedAt === undefined
          ? undefined
          : Math.max(0, Math.floor((Date.now() - location.savedAt) / 86_400_000));
        trackNearbyEvent("saved_location_return", jobId, {
          ...(daysSinceSaved === undefined ? {} : { days_since_saved: daysSinceSaved }),
          nearby_job_count: location.count ?? 0,
        });
      }
      setSaved({ town: location.town, region: location.region });
      setCount(location.count);
      setStatus("saved");
      void lookup({ location: location.town, region: location.region }, "saved");
    }
    // The saved preference is intentionally restored once when this page loads.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId]);

  function useMyLocation() {
    trackNearbyEvent("nearby_location_click", jobId, { location_method: "geolocation" });
    if (!navigator.geolocation) {
      setStatus("error");
      setMessage("Location is not available in this browser.");
      setShowManual(true);
      return;
    }
    setStatus("loading");
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => void lookup({ latitude: coords.latitude, longitude: coords.longitude }, "geolocation"),
      () => {
        setStatus("error");
        setMessage("Location permission was not granted. Enter a town instead.");
        setShowManual(true);
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
    );
  }

  function submitTown(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const town = String(form.get("town") ?? "").trim();
    if (town) void lookup({ location: town }, "manual");
  }

  function clearLocation() {
    localStorage.removeItem(STORAGE_KEY);
    setSaved(undefined);
    setCount(undefined);
    setMessage("");
    setShowManual(false);
    setStatus("idle");
    window.dispatchEvent(new CustomEvent(LOCATION_EVENT, {
      detail: { jobId, clear: true },
    }));
  }

  return (
    <section className={styles.panel} aria-label="Jobs near your location">
      <span className={styles.pin} aria-hidden="true">●</span>
      <div className={styles.copy}>
        <div className={styles.heading}>{saved ? `Jobs near ${saved.town}` : "Find jobs near you"}</div>
        <div className={styles.supporting}>
          {saved
            ? typeof count === "number"
              ? `${count} current job${count === 1 ? "" : "s"} within 20 miles`
              : "Current jobs within 20 miles"
            : "See current jobs within 20 miles"}
        </div>
        {message ? <div className={styles.error} role="status">{message}</div> : null}
        {showManual ? (
          <form className={styles.manualForm} onSubmit={submitTown}>
            <label className={styles.srOnly} htmlFor={`saved-location-town-${jobId ?? "site"}`}>Town or city</label>
            <input id={`saved-location-town-${jobId ?? "site"}`} name="town" placeholder="Town or city" required />
            <button type="submit">Use town</button>
          </form>
        ) : null}
      </div>
      <div className={styles.actions}>
        {saved ? (
          <>
            <Link
              href={`/jobs/search?near=${encodeURIComponent(saved.town)}`}
              className={styles.primary}
              onClick={() => trackNearbyEvent("nearby_results_click", jobId, { nearby_job_count: count ?? 0 })}
            >
              View nearby jobs
            </Link>
            <button type="button" className={styles.textButton} onClick={() => setShowManual(true)}>Change location</button>
            <button type="button" className={styles.textButton} onClick={clearLocation}>Clear</button>
          </>
        ) : (
          <button type="button" className={styles.primary} onClick={useMyLocation} disabled={status === "loading"}>
            {status === "loading" ? "Finding…" : "Use my location"}
          </button>
        )}
      </div>
    </section>
  );
}
