export type LondonSubArea = "central" | "north" | "east" | "south" | "west";
export type LondonJobArea = LondonSubArea | "unspecified" | "outside-london";

export type LondonJobLocationInput = {
  title?: string;
  location?: string;
  description?: string;
  full_description?: string;
};

const northernIrelandHeadline =
  /\b(?:belfast|londonderry|derriaghy|northern ireland|l['’]?derry|derry)\b/i;

const northernIrelandDescription =
  /\b(?:belfast|londonderry|derriaghy|l['’]?derry|derry)(?:\s+city\s+centre)?(?:-based|\s+based)?\b|\bbased\s+(?:in|at)\s+(?:belfast|londonderry|derriaghy|l['’]?derry|derry)\b|\bnorthern\s+ireland\b/i;

const areaPatterns: Record<LondonSubArea, RegExp[]> = {
  central: [
    /\bcentral london\b/i,
    /\bcity of london\b/i,
    /\bwest end\b/i,
    /\bwestminster\b/i,
    /\bholborn\b/i,
    /\bliverpool street\b/i,
    /\bst paul['’]?s\b/i,
    /\btower hill\b/i,
    /\bbarbican\b/i,
    /\bcannon street\b/i,
    /\bchancery lane\b/i,
    /\bcovent garden\b/i,
    /\bmayfair\b/i,
    /\bmarylebone\b/i,
    /\boxford circus\b/i,
    /\bsoho\b/i,
    /\bwaterloo\b/i,
    /\blondon bridge\b/i,
    /\bsouthwark\b/i,
    /\bclerkenwell\b/i,
    /\bfarringdon\b/i,
    /\bfitzrovia\b/i,
    /\bbloomsbury\b/i,
    /\beuston\b/i,
    /\baldgate\b/i,
    /\b(?:EC[1-4][A-Z]?|WC[12][A-Z]?|W1[A-Z]?|SW1[A-Z]?|SE1)\b/i,
  ],
  north: [
    /\bnorth(?:-|\s)west london\b/i,
    /\bnorth london\b/i,
    /\bcamden\b/i,
    /\bislington\b/i,
    /\bbarnet\b/i,
    /\benfield\b/i,
    /\bharrow\b/i,
    /\bhendon\b/i,
    /\bgolders green\b/i,
    /\bfinchley\b/i,
    /\bedgware\b/i,
    /\bstanmore\b/i,
    /\bnorthwood\b/i,
    /\bhampstead\b/i,
    /\bhighgate\b/i,
    /\barchway\b/i,
    /\bholloway\b/i,
    /\bmuswell hill\b/i,
    /\bwood green\b/i,
    /\btottenham\b/i,
    /\bedmonton\b/i,
    /\bkilburn\b/i,
    /\bwembley\b/i,
    /\bwillesden\b/i,
    /\b(?:N(?:[1-9]|1\d|2[0-2])[A-Z]?|NW(?:[1-9]|1[01])[A-Z]?|HA\d{1,2}[A-Z]?|EN\d{1,2}[A-Z]?)\b/i,
  ],
  east: [
    /\bnorth(?:-|\s)east london\b/i,
    /\beast london\b/i,
    /\bcanary wharf\b/i,
    /\bstratford\b/i,
    /\btower hamlets\b/i,
    /\bnewham\b/i,
    /\bbarking\b/i,
    /\bdagenham\b/i,
    /\bilford\b/i,
    /\bredbridge\b/i,
    /\bwaltham forest\b/i,
    /\bhackney\b/i,
    /\bleyton\b/i,
    /\bbethnal green\b/i,
    /\bpoplar\b/i,
    /\bdocklands\b/i,
    /\bromford\b/i,
    /\bhavering\b/i,
    /\bwoodford\b/i,
    /\b(?:E(?:[1-9]|1\d|20)[A-Z]?|IG\d{1,2}[A-Z]?|RM\d{1,2}[A-Z]?)\b/i,
  ],
  south: [
    /\bsouth(?:-|\s)east london\b/i,
    /\bsouth london\b/i,
    /\bcroydon\b/i,
    /\bbromley\b/i,
    /\bbeckenham\b/i,
    /\borpington\b/i,
    /\bsutton\b/i,
    /\bcarshalton\b/i,
    /\bmitcham\b/i,
    /\bwallington\b/i,
    /\bcatford\b/i,
    /\bgreenwich\b/i,
    /\blewisham\b/i,
    /\bpeckham\b/i,
    /\bdulwich\b/i,
    /\bbrixton\b/i,
    /\bcamberwell\b/i,
    /\bcrystal palace\b/i,
    /\bsanderstead\b/i,
    /\bwoolwich\b/i,
    /\beltham\b/i,
    /\bbexley\b/i,
    /\bbexleyheath\b/i,
    /\b(?:SE(?:[2-9]|1\d|2[0-8])[A-Z]?|CR\d{1,2}[A-Z]?|BR\d{1,2}[A-Z]?|SM\d{1,2}[A-Z]?)\b/i,
  ],
  west: [
    /\bsouth(?:-|\s)west london\b/i,
    /\bwest london\b/i,
    /\bhammersmith\b/i,
    /\bfulham\b/i,
    /\bkensington\b/i,
    /\bchelsea\b/i,
    /\bealing\b/i,
    /\bhounslow\b/i,
    /\bchiswick\b/i,
    /\bbrentford\b/i,
    /\bgreenford\b/i,
    /\bhayes\b/i,
    /\buxbridge\b/i,
    /\btwickenham\b/i,
    /\bteddington\b/i,
    /\brichmond\b/i,
    /\bkingston\b/i,
    /\bnew malden\b/i,
    /\bwandsworth\b/i,
    /\bputney\b/i,
    /\bbattersea\b/i,
    /\bclapham\b/i,
    /\bwimbledon\b/i,
    /\bmorden\b/i,
    /\bheathrow\b/i,
    /\bisleworth\b/i,
    /\bfeltham\b/i,
    /\bosterley\b/i,
    /\bwest drayton\b/i,
    /\bpaddington\b/i,
    /\b(?:W(?:[2-9]|1[0-4])[A-Z]?|SW(?:[2-9]|1\d|20)[A-Z]?|TW\d{1,2}[A-Z]?|UB\d{1,2}[A-Z]?)\b/i,
  ],
};

export function hasNorthernIrelandLocationEvidence(
  job: LondonJobLocationInput
) {
  const headline = [job.title, job.location].filter(Boolean).join(" ");
  const description = [job.description, job.full_description]
    .filter(Boolean)
    .join(" ");

  return (
    northernIrelandHeadline.test(headline) ||
    northernIrelandDescription.test(description)
  );
}

function matchingAreas(text: string): LondonSubArea[] {
  return (Object.keys(areaPatterns) as LondonSubArea[]).filter((area) =>
    areaPatterns[area].some((pattern) => pattern.test(text))
  );
}

export function getLondonJobAreas(job: LondonJobLocationInput): LondonSubArea[] {
  if (hasNorthernIrelandLocationEvidence(job)) return [];

  const directText = [job.title, job.location].filter(Boolean).join(" ");
  const directAreas = matchingAreas(directText);
  if (directAreas.length) return directAreas;

  // Precise workplace wording is commonly present near the start of JobG8
  // descriptions even when the location field only says "London".
  const descriptionText = [job.description, job.full_description]
    .filter(Boolean)
    .join(" ")
    .slice(0, 2500);

  return matchingAreas(descriptionText);
}

export function getLondonJobArea(job: LondonJobLocationInput): LondonJobArea {
  if (hasNorthernIrelandLocationEvidence(job)) return "outside-london";

  const areas = getLondonJobAreas(job);
  return areas.length === 1 ? areas[0] : "unspecified";
}

export function isCentralLondonJob(job: LondonJobLocationInput) {
  return getLondonJobAreas(job).includes("central");
}

export function isNorthLondonJob(job: LondonJobLocationInput) {
  return getLondonJobAreas(job).includes("north");
}

export function isEastLondonJob(job: LondonJobLocationInput) {
  return getLondonJobAreas(job).includes("east");
}

export function isSouthLondonJob(job: LondonJobLocationInput) {
  return getLondonJobAreas(job).includes("south");
}

export function isWestLondonJob(job: LondonJobLocationInput) {
  return getLondonJobAreas(job).includes("west");
}

export function isLondonJob(job: LondonJobLocationInput) {
  return !hasNorthernIrelandLocationEvidence(job);
}
