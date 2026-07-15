import assert from "node:assert/strict";
import test from "node:test";
import { renderToStaticMarkup } from "react-dom/server";
import WorkingArrangementBadge from "../components/WorkingArrangementBadge";

test("renders the hybrid badge and exact arrangement for a qualifying job", () => {
  const html = renderToStaticMarkup(
    <WorkingArrangementBadge
      workingArrangement="hybrid"
      workingArrangementText="2 days from home"
    />,
  );

  assert.match(html, /Hybrid working/);
  assert.match(html, /2 days from home/);
  assert.match(html, /data-working-arrangement-badge="hybrid"/);
});

test("renders the badge without duplicate generic wording", () => {
  const html = renderToStaticMarkup(
    <WorkingArrangementBadge
      workingArrangement="partly_remote"
      workingArrangementText="Hybrid working"
    />,
  );

  assert.equal((html.match(/Hybrid working/g) || []).length, 1);
  assert.doesNotMatch(html, /data-working-arrangement-detail/);
});

test("does not render a badge for onsite or unclassified jobs", () => {
  assert.equal(
    renderToStaticMarkup(
      <WorkingArrangementBadge workingArrangement="onsite_or_not_stated" />,
    ),
    "",
  );
  assert.equal(renderToStaticMarkup(<WorkingArrangementBadge />), "");
});
