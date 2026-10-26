"use client";

import { useEffect, useRef, useState, type FormEvent, type MouseEvent } from "react";
import { sessionReferralForApplyClick } from "@/lib/session-referral";
import { buildApplyClickParameters, type ApplyClickDetails } from "@/lib/apply-click-tracking";
import { isCpcJobAlertEligible } from "@/lib/cpc-job-alerts";

type AlertState = "editing" | "saving" | "saved" | "failed";

export default function ApplyButton({
  apply_url, job_id, title, employer, location, region, source, slice_path, salary_text = "",
}: ApplyClickDetails) {
  const [open, setOpen] = useState(false);
  const [state, setState] = useState<AlertState>("editing");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState(title);
  const [alertLocation, setAlertLocation] = useState(location);
  const [salary, setSalary] = useState(salary_text);
  const [errorMessage, setErrorMessage] = useState("");
  const [website, setWebsite] = useState("");
  const emailRef = useRef<HTMLInputElement>(null);
  const eligible = process.env.NEXT_PUBLIC_CPC_JOB_ALERTS_ENABLED === "true" && isCpcJobAlertEligible(source, apply_url);

  useEffect(() => { if (open && window.matchMedia("(min-width: 701px)").matches) emailRef.current?.focus(); }, [open]);

  useEffect(() => {
    if (!open) return;
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      setOpen(false);
    };
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [open]);

  const trackClick = () => {
    const gtag = (window as Window & { gtag?: (...args: unknown[]) => void }).gtag;
    if (typeof gtag !== "function") return;
    gtag("event", "apply_click", {
      ...buildApplyClickParameters(
        { apply_url, job_id, title, employer, location, region, source, slice_path },
        window.location.pathname
      ),
      ...sessionReferralForApplyClick(sessionStorage, document.referrer, window.location.search),
    });
  };

  const continueToEmployer = () => {
    window.open(apply_url, "_blank", "noopener,noreferrer");
    setOpen(false);
  };

  const handleApplyClick = (event: MouseEvent<HTMLAnchorElement>) => {
    if (!eligible) { trackClick(); return; }
    event.preventDefault();
    trackClick();
    setRole(title);
    setAlertLocation(location);
    setSalary(salary_text);
    setState("editing");
    setErrorMessage("");
    setOpen(true);
  };

  const closeDialog = () => {
    setOpen(false);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setState("saving");
    setErrorMessage("");
    try {
      const response = await fetch("/api/job-alerts", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email, jobId: job_id, role, location: alertLocation, salary, website }),
      });
      if (!response.ok) {
        const result = (await response.json().catch(() => null)) as { error?: string } | null;
        throw new Error(result?.error || "We couldn’t save your alert right now.");
      }
      setState("saved");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "We couldn’t save your alert right now.");
      setState("failed");
    }
  };

  return (
    <>
      <a href={apply_url} target="_blank" rel="noopener noreferrer" onClick={handleApplyClick}
        style={{ display: "inline-block", background: "#2563eb", color: "#fff", border: "none", borderRadius: 8, padding: "10px 16px", cursor: "pointer", fontSize: 16, textDecoration: "none" }}>
        Apply Now
      </a>
      {open ? (
        <div className="cpc-job-alert-backdrop" onMouseDown={event => { if (event.target === event.currentTarget) closeDialog(); }}>
          <section className="cpc-job-alert-dialog" role="dialog" aria-modal="true"
            aria-labelledby={state === "editing" || state === "saving" ? "job-alert-title" : "job-alert-result"}>
            <button type="button" aria-label="Close alert signup" onClick={closeDialog}
              style={{ position: "absolute", right: 17, top: 13, width: 36, height: 36, border: 0, borderRadius: "50%", background: "#f1f5f9", color: "#475569", fontSize: 23, cursor: "pointer" }}>×</button>
            {state === "saved" || state === "failed" ? (
              <div style={{ paddingTop: 22 }}>
                <h2 id="job-alert-result" style={{ margin: "0 42px 8px 0", fontSize: 25, lineHeight: 1.25 }}>
                  {state === "saved" ? "Your alert is saved" : "Your alert wasn’t saved"}
                </h2>
                <p role="status" style={{ color: "#475569", lineHeight: 1.5 }}>
                  {state === "saved" ? "Your alert is saved alongside your existing alerts. Matches are combined into one daily email, with duplicate jobs removed. Unsubscribe stops all alerts." : errorMessage + " You can still continue to the employer without an alert."}
                </p>
                {state === "failed" ? <button type="button" onClick={() => setState("editing")} style={{ marginRight: 14, padding: "11px 15px", border: "1px solid #cbd5e1", borderRadius: 7, background: "#fff", color: "#1d4ed8", font: "inherit", cursor: "pointer" }}>Try again</button> : null}
                <button type="button" onClick={continueToEmployer} style={{ marginTop: 10, border: 0, borderRadius: 7, padding: "12px 15px", background: "#1d4ed8", color: "#fff", font: "inherit", fontWeight: 700, cursor: "pointer" }}>Continue to the employer</button>
              </div>
            ) : (
              <form className="cpc-job-alert-form" onSubmit={handleSubmit}>
                <div className="cpc-job-alert-fields">
                <div className="cpc-job-alert-eyebrow" style={{ color: "#64748b", fontSize: 12, fontWeight: 700, letterSpacing: ".045em" }}>BEFORE YOU CONTINUE TO THE EMPLOYER</div>
                <h2 id="job-alert-title" style={{ margin: "8px 42px 8px 0", fontSize: 25, lineHeight: 1.25 }}>Get alerts for similar jobs</h2>
                
                <label htmlFor="job-alert-email" style={{ display: "block", margin: "12px 0 5px", fontSize: 14, fontWeight: 600 }}>Email address</label>
                <input ref={emailRef} id="job-alert-email" type="email" autoComplete="email" required disabled={state === "saving"} maxLength={254} value={email} onChange={event => setEmail(event.target.value)} placeholder="you@example.com"
                  style={{ width: "100%", height: 42, padding: "9px 11px", border: "1px solid #cbd5e1", borderRadius: 6, background: "#fff", color: "#171717", font: "inherit" }} />
                <div className="cpc-job-alert-preference-panel" style={{ margin: "10px 0", padding: "10px 12px", background: "#f8fafc", border: "1px solid #dbe3ee", borderRadius: 8 }}>
                  <div style={{ marginBottom: 6, fontSize: 14, fontWeight: 600 }}>New alert preferences — change anything</div>
                  <div className="cpc-job-alert-preferences">
                    {([["Role", role, setRole], ["Location", alertLocation, setAlertLocation], ["Salary", salary, setSalary]] as const).map(([label, value, setValue]) => (
                      <label key={label} style={{ display: "block", margin: "4px 0", color: "#475569", fontSize: 14 }}>
                        {label}
                        <input type="text" required={label === "Role" || label === "Location"} disabled={state === "saving"} maxLength={120} value={value} onChange={event => setValue(event.target.value)}
                          style={{ display: "block", width: "100%", height: 38, marginTop: 3, padding: "8px 10px", border: "1px solid #cbd5e1", borderRadius: 6, background: "#fff", color: "#171717", font: "inherit" }} />
                      </label>
                    ))}
                  </div>
                </div>
                </div>
                <div className="cpc-job-alert-actions">
                <button type="submit" disabled={state === "saving"} style={{ width: "100%", border: 0, borderRadius: 7, padding: "12px 15px", background: state === "saving" ? "#94a3b8" : "#1d4ed8", color: "#fff", font: "inherit", fontWeight: 700, cursor: state === "saving" ? "wait" : "pointer" }}>
                  {state === "saving" ? "Saving your alert…" : "Yes — save alert and continue to apply"}
                </button>
                <button type="button" disabled={state === "saving"} onClick={continueToEmployer} style={{ display: "block", marginTop: 4, marginBottom: 0, padding: "8px 0", border: 0, background: "transparent", color: "#1d4ed8", font: "inherit", textDecoration: "underline", cursor: "pointer" }}>No thanks — continue to apply</button>
                <p style={{ margin: "6px 0 0", color: "#64748b", fontSize: 12, lineHeight: 1.4 }}>Save up to 10 different alerts per email. New preferences add an alert. Matches arrive in one daily email. Unsubscribe stops all alerts.</p>
                </div>
                <label aria-hidden="true" style={{ position: "absolute", left: -10000, width: 1, height: 1, overflow: "hidden" }}>Leave this field empty<input tabIndex={-1} autoComplete="off" name="website" value={website} onChange={event => setWebsite(event.target.value)} /></label>
              </form>
            )}
          </section>
        </div>
      ) : null}
    </>
  );
}
