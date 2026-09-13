"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import styles from "@/components/SavedLocationJobs.module.css";

const STORAGE_KEY = "ontap.saved-location.v1";
const LOCATION_EVENT = "ontap:saved-location-jobs";

type SavedLocation = { town: string; region: string };
type SavedLocationPreference = SavedLocation & { count?: number };
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
  eventName: "nearby_location_click" | "nearby_location_success" | "nearby_results_click",
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
        }
      : undefined;
  } catch {
    return undefined;
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
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...data.location, count: data.count }));
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
        trackNearbyEvent("nearby_location_success", jobId, {
          location_method: method,
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
              ? `${count} current job${count === 1 ? "" : "s"} within 15 miles`
              : "Current jobs within 15 miles"
            : "See current jobs within 15 miles"}
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
