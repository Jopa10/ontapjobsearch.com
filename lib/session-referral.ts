export const SESSION_REFERRAL_KEY = "ontap.analytics-session-referral.v1";
export const SESSION_REFERRAL_TIMEOUT_MS = 30 * 60 * 1000;

export type SessionReferralParameters = {
  entry_referrer_host: string;
  entry_utm_source: string;
  entry_source_type: string;
};

type StoredSessionReferral = SessionReferralParameters & { last_activity: number };
type StorageLike = Pick<Storage, "getItem" | "setItem">;

export function buildSessionReferralParameters(referrer: string, search: string): SessionReferralParameters {
  let host = "(direct)";
  if (referrer) {
    try {
      host = new URL(referrer).hostname.replace(/^www\./i, "").toLowerCase() || "(unknown)";
    } catch {
      host = "(unknown)";
    }
  }
  const utmSource = new URLSearchParams(search).get("utm_source")?.trim() || "(none)";
  const normalizedHost = host === "ontapjobsearch.com" || host.endsWith(".ontapjobsearch.com") ? "(internal)" : host;
  return {
    entry_referrer_host: normalizedHost,
    entry_utm_source: utmSource,
    entry_source_type: utmSource !== "(none)" ? utmSource.toLowerCase() : normalizedHost,
  };
}

function readStored(storage: StorageLike): StoredSessionReferral | undefined {
  try {
    const raw = storage.getItem(SESSION_REFERRAL_KEY);
    if (!raw) return undefined;
    const value = JSON.parse(raw) as StoredSessionReferral;
    if (typeof value.last_activity !== "number" || typeof value.entry_referrer_host !== "string" ||
        typeof value.entry_utm_source !== "string" || typeof value.entry_source_type !== "string") return undefined;
    return value;
  } catch {
    return undefined;
  }
}

function writeStored(storage: StorageLike, value: StoredSessionReferral): void {
  try { storage.setItem(SESSION_REFERRAL_KEY, JSON.stringify(value)); } catch {
    // Analytics storage must never affect the job-search experience.
  }
}

export function initializeSessionReferral(storage: StorageLike, referrer: string, search: string, now = Date.now()): SessionReferralParameters {
  const stored = readStored(storage);
  if (stored && now >= stored.last_activity && now - stored.last_activity < SESSION_REFERRAL_TIMEOUT_MS) {
    writeStored(storage, { ...stored, last_activity: now });
    return { entry_referrer_host: stored.entry_referrer_host, entry_utm_source: stored.entry_utm_source, entry_source_type: stored.entry_source_type };
  }
  const parameters = buildSessionReferralParameters(referrer, search);
  writeStored(storage, { ...parameters, last_activity: now });
  return parameters;
}

export function sessionReferralForApplyClick(storage: StorageLike, referrer: string, search: string, now = Date.now()): SessionReferralParameters {
  const stored = readStored(storage);
  if (stored && now >= stored.last_activity && now - stored.last_activity >= SESSION_REFERRAL_TIMEOUT_MS) {
    const expired = { entry_referrer_host: "(session_expired_tab)", entry_utm_source: "(none)", entry_source_type: "session_expired_tab" };
    writeStored(storage, { ...expired, last_activity: now });
    return expired;
  }
  return initializeSessionReferral(storage, referrer, search, now);
}

export function touchSessionReferral(storage: StorageLike, now = Date.now()): void {
  const stored = readStored(storage);
  if (!stored) return;
  if (now < stored.last_activity || now - stored.last_activity >= SESSION_REFERRAL_TIMEOUT_MS) {
    writeStored(storage, { entry_referrer_host: "(session_expired_tab)", entry_utm_source: "(none)", entry_source_type: "session_expired_tab", last_activity: now });
    return;
  }
  writeStored(storage, { ...stored, last_activity: now });
}
