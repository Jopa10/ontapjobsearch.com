import assert from 'node:assert/strict';
import test from 'node:test';
import { decodePublishedJobId } from '../lib/published-jobs';

test('encoded JobG8 IDs resolve without changing their published URL', () => {
  assert.equal(decodePublishedJobId('1247531%20%5BJSP51654%5D'), '1247531 [JSP51654]');
});

test('plain and malformed route IDs fail safely', () => {
  assert.equal(decodePublishedJobId('23643_225466886'), '23643_225466886');
  assert.equal(decodePublishedJobId('%E0%A4%A'), '%E0%A4%A');
});
