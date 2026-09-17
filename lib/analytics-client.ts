export const ANALYTICS_MEASUREMENT_ID = "G-XLJL0PXJ0V";

const AUTOMATION_USER_AGENT =
  /(?:bot\b|crawler|spider|slurp|headlesschrome|phantomjs|selenium|playwright|puppeteer|facebookexternalhit|linkedinbot|discordbot|whatsapp)/i;

export function isLikelyAutomation(userAgent: string, webdriver: boolean): boolean {
  return webdriver || AUTOMATION_USER_AGENT.test(userAgent);
}

export function pageContext(pathname: string): "job_detail" | "listing" | "site" {
  if (pathname.startsWith("/jobs/")) return "job_detail";
  if (pathname.includes("jobs")) return "listing";
  return "site";
}

export function hasCampaignParameters(search: string): boolean {
  const parameters = new URLSearchParams(search);
  return ["utm_source", "utm_medium", "utm_campaign", "gclid", "gbraid", "wbraid"]
    .some((key) => parameters.has(key));
}

export function daysBetween(earlier: number, later: number): number {
  return Math.max(0, Math.floor((later - earlier) / 86_400_000));
}
