import test from 'node:test';
import assert from 'node:assert/strict';
import {applyExcludeReviewWindow} from './exclude-retention.mjs';

test('retired three-day helper refuses EXCLUDE payload retention before database access',async()=>{
 let calls=0;
 const client={query(){calls++;throw new Error('Database should not be accessed');}};
 await assert.rejects(
  applyExcludeReviewWindow(client,{runId:'legacy',fullyExcludedRefs:['excluded']}),
  /EXCLUDE payload retention is disabled/
 );
 assert.equal(calls,0);
});
