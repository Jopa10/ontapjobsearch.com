import assert from "node:assert/strict";
import test from "node:test";

import {
  getLondonJobArea,
  hasNorthernIrelandLocationEvidence,
  isCentralInnerLondonJob,
  isOuterLondonJob,
} from "../lib/london-job-area";

test("Belfast title evidence is excluded from both London slices", () => {
  const job = {
    title: "Cemeteries Administrator - Belfast City Council",
    location: "City",
    description: "Administrative vacancy.",
  };

  assert.equal(hasNorthernIrelandLocationEvidence(job), true);
  assert.equal(getLondonJobArea(job), "outside-london");
  assert.equal(isCentralInnerLondonJob(job), false);
  assert.equal(isOuterLondonJob(job), false);
});

test("Belfast-based description evidence is excluded from London", () => {
  const job = {
    title: "Administrator (Part time 12-15 hours)",
    location: "City",
    description: "A Belfast-based role with hybrid working.",
  };

  assert.equal(getLondonJobArea(job), "outside-london");
});

test("generic City without contradictory evidence keeps existing London behaviour", () => {
  assert.equal(
    getLondonJobArea({
      title: "Office Administrator",
      location: "City",
      description: "Office support role for a London employer.",
    }),
    "central-inner"
  );
});

test("outer London evidence is unaffected", () => {
  assert.equal(
    getLondonJobArea({
      title: "Receptionist",
      location: "Romford",
      description: "Reception role in Romford.",
    }),
    "outer"
  );
});
