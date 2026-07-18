export type LondonJobArea = "central-inner" | "outer";

export type LondonJobLocationInput = {
  title?: string;
  location?: string;
  description?: string;
  full_description?: string;
};

const outerLondonLocations = [
  "alperton",
  "barking",
  "barnet",
  "beckenham",
  "bexley",
  "bexleyheath",
  "brent",
  "brentford",
  "bromley",
  "carshalton",
  "chingford",
  "coulsdon",
  "croydon",
  "dagenham",
  "ealing",
  "edgware",
  "edmonton",
  "eltham",
  "enfield",
  "erith",
  "epsom",
  "feltham",
  "finchley",
  "greenford",
  "hanworth",
  "harrow",
  "havering",
  "hayes",
  "heathrow",
  "hillingdon",
  "hounslow",
  "ilford",
  "isleworth",
  "kingston",
  "kingsbury",
  "mitcham",
  "morden",
  "new malden",
  "northolt",
  "orpington",
  "petts wood",
  "pinner",
  "redbridge",
  "richmond",
  "romford",
  "ruislip",
  "sutton",
  "twickenham",
  "uxbridge",
  "waltham forest",
  "watford",
  "wembley",
  "west drayton",
  "woodford",
  "worcester park",
] as const;

const outerLondonPostcode =
  /\b(?:BR|CR|DA|EN|HA|IG|KT|RM|SM|TW|UB|WD)\d{1,2}[A-Z]?\b|\bNW(?:7|9|10|11)\b|\bSE(?:2|6|7|9|12|18|20|25|28)\b|\bSW(?:19|20)\b/i;

function containsLocation(text: string, location: string) {
  const escaped = location.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`\\b${escaped}\\b`, "i").test(text);
}

export function getLondonJobArea(job: LondonJobLocationInput): LondonJobArea {
  const searchableText = [
    job.title,
    job.location,
    job.description,
    job.full_description,
  ]
    .filter(Boolean)
    .join(" ");

  if (
    outerLondonPostcode.test(searchableText) ||
    outerLondonLocations.some((location) => containsLocation(searchableText, location))
  ) {
    return "outer";
  }

  // Generic "London" jobs remain on the established page unless the advert
  // provides reliable outer-London evidence.
  return "central-inner";
}

export function isCentralInnerLondonJob(job: LondonJobLocationInput) {
  return getLondonJobArea(job) === "central-inner";
}

export function isOuterLondonJob(job: LondonJobLocationInput) {
  return getLondonJobArea(job) === "outer";
}
