export type JobDescriptionBlock = {
  type: "heading" | "paragraph" | "bullet";
  text: string;
};

const NHS_SOURCE = "nhs jobs";
const KNOWN_HEADINGS = new Set([
  "job summary",
  "main duties of the job",
  "job responsibilities",
]);
const ABBREVIATIONS = new Set([
  "mr.",
  "mrs.",
  "ms.",
  "dr.",
  "prof.",
  "e.g.",
  "i.e.",
  "etc.",
]);

function clean(value: string) {
  return value.replace(/\s+/g, " ").trim();
}

function structuredBlocks(value: string): JobDescriptionBlock[] {
  const paragraphs = value.replace(/\r\n?/g, "\n").split(/\n{2,}/);
  const output: JobDescriptionBlock[] = [];

  for (const paragraph of paragraphs) {
    const lines = paragraph.split("\n").map(clean).filter(Boolean);
    if (!lines.length) continue;

    const hasStructuredLine = lines.some(
      (line) => KNOWN_HEADINGS.has(line.toLowerCase()) || /^[•*-]\s+/.test(line)
    );
    if (!hasStructuredLine) {
      output.push({ type: "paragraph", text: clean(lines.join(" ")) });
      continue;
    }

    for (const line of lines) {
      const lower = line.toLowerCase();
      if (KNOWN_HEADINGS.has(lower)) {
        output.push({ type: "heading", text: line });
      } else if (/^[•*-]\s+/.test(line)) {
        output.push({ type: "bullet", text: clean(line.replace(/^[•*-]\s+/, "")) });
      } else {
        output.push({ type: "paragraph", text: line });
      }
    }
  }

  return output;
}

function sentenceBreaks(value: string): string[] {
  const text = clean(value);
  const output: string[] = [];
  let start = 0;

  for (let index = 0; index < text.length; index += 1) {
    if (!".!?".includes(text[index])) continue;

    let end = index + 1;
    while (end < text.length && ".!?".includes(text[end])) end += 1;

    let next = end;
    while (next < text.length && /\s/.test(text[next])) next += 1;
    if (next >= text.length) {
      output.push(text.slice(start).trim());
      start = text.length;
      break;
    }
    if (!/[A-Z0-9]/.test(text[next])) continue;

    const before = text.slice(start, end).trim();
    const token = before.split(/\s+/).at(-1)?.toLowerCase() || "";
    if (ABBREVIATIONS.has(token)) continue;

    output.push(before);
    start = next;
    index = next - 1;
  }

  if (start < text.length) output.push(text.slice(start).trim());
  return output.filter(Boolean);
}

function readableNhsParagraphs(value: string): JobDescriptionBlock[] {
  const sentences = sentenceBreaks(value);
  if (sentences.length < 3) return [{ type: "paragraph", text: clean(value) }];

  const output: JobDescriptionBlock[] = [];
  for (let index = 0; index < sentences.length; index += 2) {
    output.push({
      type: "paragraph",
      text: sentences.slice(index, index + 2).join(" "),
    });
  }
  return output;
}

/**
 * Presentation-only formatting. It does not rewrite or summarise vacancy text.
 * NHS descriptions currently arrive as factual source text flattened into one
 * line, so long NHS copy is split into short sentence groups for readability.
 */
export function descriptionBlocks(value: string, source: string): JobDescriptionBlock[] {
  const text = value.trim();
  if (!text) return [];

  if (/\r|\n/.test(text)) return structuredBlocks(text);
  if (source.trim().toLowerCase() === NHS_SOURCE && clean(text).length >= 240) {
    return readableNhsParagraphs(text);
  }
  return [{ type: "paragraph", text: clean(text) }];
}
