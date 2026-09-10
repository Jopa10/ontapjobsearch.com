"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import styles from "@/components/SavedLocationJobs.module.css";

const STORAGE_KEY = "ontap.saved-location.v1";
const LOCATION_EVENT = "ontap:saved-location-jobs";

type SavedLocation = { town: string; region: string };
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

export const savedLocationJobsEvent = LOCATION_EVENT;

function readSavedLocation(): SavedLocation | undefined {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "null") as Partial<SavedLocation> | null;
    return parsed?.town && parsed?.region ? { town: parsed.town, region: parsed.region } : undefined;
  } catch {
    return undefined;
  }
}

export default function SavedLocationJobs({ jobId }: { jobId?: string }) {
  const [status, setStatus] = useState<"idle" | "loading" | "saved" | "error">("idle");
  const [saved, setSaved] = useState<SavedLocation>();
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState("");
  const [showManual, setShowManual] = useState(false);

  async function lookup(payload: Record<string, unknown>, remember: boolean) {
    setStatus("loading");
    setMessage("");
    try {
      const response = await fetch("/api/jobs/nearby", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...payload, jobId }),
      });
      const data = await response.json() as NearbyResponse;
      if (!response.ok) throw new Error(data.error || "Location lookup failed.");
      if (remember) localStorage.setItem(STORAGE_KEY, JSON.stringify(data.location));
      setSaved(data.location);
      setCount(data.count);
      setStatus("saved");
      setShowManual(false);
      window.dispatchEvent(new CustomEvent(LOCATION_EVENT, {
        detail: {
          jobId,
          location: data.location,
          jobs: data.suitableJobs,
          searchPath: `/jobs/search?location=${encodeURIComponent(data.location.town)}`,
        },
      }));
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Location lookup failed.");
      setShowManual(true);
    }
  }

  useEffect(() => {
    const location = readSavedLocation();
    if (location) void lookup({ location: location.town, region: location.region }, false);
    // The saved preference is intentionally restored once when this page loads.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jobId]);

  function useMyLocation() {
    if (!navigator.geolocation) {
      setStatus("error");
      setMessage("Location is not available in this browser.");
      setShowManual(true);
      return;
    }
    setStatus("loading");
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => void lookup({ latitude: coords.latitude, longitude: coords.longitude }, true),
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
    if (town) void lookup({ location: town }, true);
  }

  function clearLocation() {
    localStorage.removeItem(STORAGE_KEY);
    setSaved(undefined);
    setCount(0);
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
          {saved ? `${count} current job${count === 1 ? "" : "s"} within 15 miles` : "See current jobs within 15 miles"}
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
            <Link href={`/jobs/search?location=${encodeURIComponent(saved.town)}`} className={styles.primary}>View nearby jobs</Link>
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
