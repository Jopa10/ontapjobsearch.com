import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const component = readFileSync("components/JobPageSearch.tsx", "utf8");
const styles = readFileSync("components/JobPageSearch.module.css", "utf8");
const header = readFileSync("components/Header.tsx", "utf8");
const jobPage = readFileSync("app/jobs/[id]/page.tsx", "utf8");
const jobPageStyles = readFileSync("app/jobs/[id]/job-page.module.css", "utf8");

test("job-page search submits both governed search fields", () => {
  assert.match(component, /action="\/jobs\/search"/);
  assert.match(component, /name="q"/);
  assert.match(component, /name="location"/);
  assert.match(component, /Role or keyword/);
  assert.match(component, /Town or region/);
});

test("mobile search starts collapsed and exposes the Ontap magnifying glass", () => {
  assert.match(component, /useState\(false\)/);
  assert.match(component, /Tap to search other jobs ↓/);
  assert.match(component, /Hide search ↑/);
  assert.match(component, /ontap-magnifying-glass\.svg/);
  assert.match(styles, /\.form\.expanded\s*\{[\s\S]*?display: grid;/);
});

test("mobile navigation keeps Home and hides Browse Jobs", () => {
  assert.match(header, /<nav className="ml-auto flex shrink-0/);
  assert.match(header, /className="hidden[^\"]*sm:inline"[\s\S]*?>\s*Browse Jobs/);
});

test("mobile job pages hide only the secondary regional listing link", () => {
  assert.match(jobPage, /index === 1 \? styles\.secondaryListingLink/);
  assert.match(
    jobPageStyles,
    /@media \(max-width: 640px\)[\s\S]*?\.secondaryListingLink\s*\{\s*display: none;/
  );
});
