import { buildCampaignUrl } from "../lib/campaign-url";

function argument(name: string): string | undefined {
  const index = process.argv.indexOf(`--${name}`);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

try {
  const url = argument("url");
  const source = argument("source");
  const medium = argument("medium");
  const campaign = argument("campaign");
  if (!url || !source || !medium || !campaign) {
    throw new Error(
      "Usage: npm run campaign:url -- --url /page --source linkedin --medium organic_social --campaign campaign_name [--content link_name]",
    );
  }

  console.log(buildCampaignUrl({
    url,
    source,
    medium,
    campaign,
    content: argument("content"),
  }));
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
}
