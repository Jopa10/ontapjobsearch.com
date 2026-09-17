const ONTAP_ORIGIN = "https://www.ontapjobsearch.com";

export type CampaignUrlOptions = {
  url: string;
  source: string;
  medium: string;
  campaign: string;
  content?: string;
};

function requiredValue(name: string, value: string): string {
  const trimmed = value.trim();
  if (!trimmed) throw new Error(`${name} is required`);
  return trimmed;
}

export function buildCampaignUrl(options: CampaignUrlOptions): string {
  const target = new URL(options.url, ONTAP_ORIGIN);
  if (target.origin !== ONTAP_ORIGIN) {
    throw new Error("Campaign URLs must point to www.ontapjobsearch.com");
  }

  target.searchParams.set("utm_source", requiredValue("source", options.source));
  target.searchParams.set("utm_medium", requiredValue("medium", options.medium));
  target.searchParams.set("utm_campaign", requiredValue("campaign", options.campaign));
  if (options.content?.trim()) target.searchParams.set("utm_content", options.content.trim());

  return target.toString();
}
