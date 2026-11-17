const CPC_SOURCE = "jobg8";
const JOBG8_APPLY_HOST = "www.jobg8.com";
const JOBG8_APPLY_PATH = "/traffic.aspx";

/** Require Ontap's source label and the JobG8 CPC apply endpoint to agree. */
export function isCpcJobAlertEligible(source: string, applyUrl: string): boolean {
  if (source.trim().toLowerCase() !== CPC_SOURCE) return false;
  try {
    const url = new URL(applyUrl);
    return url.protocol === "https:" &&
      url.hostname.toLowerCase() === JOBG8_APPLY_HOST &&
      url.pathname.toLowerCase() === JOBG8_APPLY_PATH;
  } catch {
    return false;
  }
}
