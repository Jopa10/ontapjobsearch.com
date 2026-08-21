import assert from "node:assert/strict";
import test from "node:test";
import { descriptionBlocks } from "../lib/job-description";

function blockText(value: string, source: string) {
  return descriptionBlocks(value, source).map(({ text }) => text).join(" ");
}

test("long flat NHS descriptions become several readable paragraphs without rewriting text", () => {
  const description =
    "The practice is seeking an enthusiastic administrator to join the team. The role supports patients and clinicians across the service. You will maintain accurate records and process routine correspondence. You will also answer queries and help coordinate appointments. The successful candidate will work closely with colleagues across the practice. Please see the original advert for the complete requirements.";
  const blocks = descriptionBlocks(description, "NHS Jobs");

  assert.ok(blocks.length >= 3);
  assert.ok(blocks.every(({ type }) => type === "paragraph"));
  assert.equal(blockText(description, "NHS Jobs"), description);
});

test("existing structured descriptions preserve headings, paragraphs and bullets", () => {
  const description =
    "Job summary\n\nHelp the service with day-to-day administration.\n\nMain duties of the job\n- Manage bookings\n- Maintain accurate records";
  const blocks = descriptionBlocks(description, "NHS Jobs");

  assert.deepEqual(
    blocks.map(({ type, text }) => [type, text]),
    [
      ["heading", "Job summary"],
      ["paragraph", "Help the service with day-to-day administration."],
      ["heading", "Main duties of the job"],
      ["bullet", "Manage bookings"],
      ["bullet", "Maintain accurate records"],
    ]
  );
});

test("short flat non-NHS descriptions are left as one paragraph", () => {
  const blocks = descriptionBlocks("A concise externally sourced role overview.", "NEJobs");
  assert.deepEqual(blocks, [
    { type: "paragraph", text: "A concise externally sourced role overview." },
  ]);
});
