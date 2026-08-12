import assert from "node:assert/strict";
import test from "node:test";

import {
  getLondonJobArea,
  getLondonJobAreas,
  hasNorthernIrelandLocationEvidence,
  isCentralLondonJob,
  isEastLondonJob,
  isLondonJob,
  isNorthLondonJob,
  isSouthLondonJob,
  isWestLondonJob,
} from "../lib/london-job-area";

test("Belfast title evidence is excluded from London", () => {
  const job = {
    title: "Cemeteries Administrator - Belfast City Council",
    location: "City",
    description: "Administrative vacancy.",
  };

  assert.equal(hasNorthernIrelandLocationEvidence(job), true);
  assert.equal(getLondonJobArea(job), "outside-london");
  assert.equal(isLondonJob(job), false);
  assert.deepEqual(getLondonJobAreas(job), []);
});

test("generic London stays on the London parent without being guessed into a sub-area", () => {
  const job = {
    title: "Office Administrator",
    location: "London",
    description: "Office support role for a London employer.",
  };

  assert.equal(getLondonJobArea(job), "unspecified");
  assert.equal(isLondonJob(job), true);
  assert.deepEqual(getLondonJobAreas(job), []);
});

test("Central London evidence is recognised", () => {
  const job = {
    title: "Office Coordinator",
    location: "Central London - SE1",
  };

  assert.equal(getLondonJobArea(job), "central");
  assert.equal(isCentralLondonJob(job), true);
});

test("North and North-West London evidence is recognised", () => {
  const job = {
    title: "Receptionist",
    location: "Camden, North London",
  };

  assert.equal(getLondonJobArea(job), "north");
  assert.equal(isNorthLondonJob(job), true);
});

test("East and North-East London evidence is recognised", () => {
  const job = {
    title: "Customer Service Administrator",
    location: "Romford",
  };

  assert.equal(getLondonJobArea(job), "east");
  assert.equal(isEastLondonJob(job), true);
});

test("South and South-East London evidence is recognised", () => {
  const job = {
    title: "Administrator",
    location: "Croydon",
  };

  assert.equal(getLondonJobArea(job), "south");
  assert.equal(isSouthLondonJob(job), true);
});

test("West and South-West London evidence is recognised", () => {
  const job = {
    title: "Office Administrator",
    location: "Hounslow",
  };

  assert.equal(getLondonJobArea(job), "west");
  assert.equal(isWestLondonJob(job), true);
});

test("specific description evidence is used when the headline only says London", () => {
  const job = {
    title: "Team Administrator",
    location: "London",
    description: "This role is based in Canary Wharf and supports a busy office team.",
  };

  assert.equal(getLondonJobArea(job), "east");
  assert.equal(isEastLondonJob(job), true);
});

test("multi-area London roles can appear in each evidenced sub-area", () => {
  const job = {
    title: "Medical Receptionist",
    location: "London",
    description: "Work across clinics in North London, Central London and East London.",
  };

  assert.deepEqual(getLondonJobAreas(job), ["central", "north", "east"]);
  assert.equal(getLondonJobArea(job), "unspecified");
});
