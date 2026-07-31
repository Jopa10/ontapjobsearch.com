import fs from "node:fs";
import path from "node:path";

type PreviewMap = Record<string, string[]>;

const PREVIEW_PATH = path.join(
  process.cwd(),
  "data",
  "at-a-glance-preview.json"
);

let cachedPreview: PreviewMap | undefined;

function readPreview(): PreviewMap {
  if (cachedPreview) return cachedPreview;

  try {
    const parsed: unknown = JSON.parse(fs.readFileSync(PREVIEW_PATH, "utf8"));
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      cachedPreview = {};
      return cachedPreview;
    }

    cachedPreview = Object.fromEntries(
      Object.entries(parsed as Record<string, unknown>).flatMap(([jobId, value]) => {
        if (!Array.isArray(value)) return [];
        const attributes = value
          .filter((item): item is string => typeof item === "string")
          .map((item) => item.trim())
          .filter(Boolean);
        return attributes.length >= 2 ? [[jobId, attributes]] : [];
      })
    );
  } catch {
    cachedPreview = {};
  }

  return cachedPreview;
}

export function getAtAGlanceAttributes(jobId: string): string[] {
  return readPreview()[jobId] || [];
}
