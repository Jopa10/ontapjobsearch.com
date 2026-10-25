import assert from 'node:assert/strict';
import test from 'node:test';
import { safeSearchText, searchResultParameters } from '../lib/search-analytics';

test('search analytics keeps the requested role and location with actual count', () => {
  const values = searchResultParameters('Accounts Assistant', 'Hertford', 7, true, false);
  assert.equal(values.search_term, 'Accounts Assistant');
  assert.equal(values.search_location, 'Hertford');
  assert.equal(values.result_count, 7);
  assert.equal(values.search_outcome, 'results');
});
test('a recognised place with no jobs is distinct from an unrecognised place', () => {
  assert.equal(searchResultParameters('admin', 'Hertford', 0, true, false).location_status, 'recognised');
  assert.equal(searchResultParameters('admin', 'xyzabc', 0, false, false).location_status, 'unrecognised');
  assert.equal(searchResultParameters('admin', '', 0, false, false).location_status, 'not_provided');
  assert.equal(searchResultParameters('admin', 'Hertford', 0, true, false).search_outcome, 'no_results');
  assert.equal(searchResultParameters('', 'Hertford', 0, true, true).search_mode, 'nearby');
});
test('contact details and excessive free text are not sent', () => {
  assert.equal(safeSearchText('admin john@example.com +44 7700 900123'), 'admin [redacted] [redacted]');
  assert.equal(safeSearchText('x'.repeat(200)).length, 100);
  assert.equal(safeSearchText(' admin\nassistant '), 'admin assistant');
});
