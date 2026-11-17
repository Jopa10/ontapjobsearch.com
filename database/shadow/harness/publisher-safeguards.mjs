import assert from 'node:assert/strict';
import {gzipSync,gunzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
export const MAX=838860800,RESERVE=67108864;
export const hash=b=>createHash('sha256').update(b).digest('hex');
export function requirePreview(env){
 assert.equal(env.VERCEL_ENV,'preview','Preview only');
 assert.equal(env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602','Wrong isolated Neon project');
 const u=new URL(env.ONTAP_SHADOW_DATABASE_URL);
 assert.ok(u.hostname.endsWith('.neon.tech'),'Expected Neon hostname');
 assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')),'TLS required');
 return true;
}
export function requireBudget(before,packedBytes){
 assert.ok(before+packedBytes*4+32*1024*1024+RESERVE<MAX,'Insufficient Neon test database headroom');
}
export function unpackSnapshot(packed,expectedHash){
 const raw=gunzipSync(packed,{maxOutputLength:128*1024*1024});
 assert.equal(hash(raw),expectedHash,'Snapshot hash differs');
 return JSON.parse(raw.toString('utf8'));
}
export function packSnapshot(rows){
 const raw=Buffer.from(JSON.stringify(rows));
 return {packed:gzipSync(raw,{level:9}),sha256:hash(raw),rawBytes:raw.length};
}
export function requireSameDay(feedDate,latestDate){
 assert.match(feedDate,/^20\d\d-\d\d-\d\d$/);
 assert.equal(feedDate,latestDate,'Feed date differs from latest verified Neon snapshot');
}
