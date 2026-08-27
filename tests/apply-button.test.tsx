import assert from 'node:assert/strict';
import test from 'node:test';
import { renderToStaticMarkup } from 'react-dom/server';
import ApplyButton from '../components/ApplyButton';

test('apply control exposes a normal crawlable destination', () => {
  const markup = renderToStaticMarkup(
    <ApplyButton
      apply_url="https://example.com/apply/job-1"
      job_id="job-1"
      title="Administrator"
      employer="Example Employer"
      location="Leeds"
      region="Yorkshire - West"
      source="JobG8"
      slice_path="/job-search/west-yorkshire/service-administrator-jobs"
    />
  );

  assert.match(markup, /^<a /);
  assert.match(markup, /href="https:\/\/example\.com\/apply\/job-1"/);
  assert.match(markup, /target="_blank"/);
  assert.match(markup, /rel="noopener noreferrer"/);
  assert.match(markup, />Apply Now<\/a>$/);
});
