import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const component = readFileSync("components/JobPageSearch.tsx", "utf8");
const styles = readFileSync("components/JobPageSearch.module.css", "utf8");

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
