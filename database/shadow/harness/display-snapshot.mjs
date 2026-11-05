import {gzipSync,gunzipSync} from 'node:zlib';
import {readCompactSelection} from './selection-importer.mjs';
import assert from 'node:assert/strict';
import {contentHash} from './importer.mjs';
import {measure,DEFAULT_BUDGET} from './staged-importer.mjs';
export function projection(outputs) {
  const groups=new Map();
  for(const [scope,rows] of Object.entries(outputs)) {
    const cut=scope.indexOf(':'); assert.ok(cut>0); const family=scope.slice(0,cut),region=scope.slice(cut+1);
    assert.ok(Array.isArray(rows)); const seen=new Set();
    rows.forEach((row,position)=>{assert.equal(typeof row.job_id,'string');assert.ok(!seen.has(row.job_id));seen.add(row.job_id);
      const url=new URL(row.apply_url);assert.ok(['http:','https:'].includes(url.protocol));assert.ok(row.title);
      const key='production:'+family+':'+row.job_id;
      if(!groups.has(key))groups.set(key,{ref:row.job_id,scope:'production:'+family,displayRows:[]});
      groups.get(key).displayRows.push({region,position,row});
    });
  }
  return [...groups.values()];
}
export function reconstruct(rows,scopes) {
  const out=Object.fromEntries(scopes.map(s=>[s,[]]));
  for(const d of rows)for(const v of d.displayRows){const scope=d.scope.slice('production:'.length)+':'+v.region;assert.ok(scope in out);out[scope].push(v);}
  for(const scope of scopes)out[scope]=out[scope].sort((a,b)=>a.position-b.position).map((v,i)=>{assert.equal(v.position,i);return v.row;});
  return out;
}
export async function attachDisplay(client,outputs,receipt) {
  assert.equal(receipt.status,'passed');assert.equal(receipt.unknowns,0);assert.equal(receipt.exactFileOutputParity,true);
  assert.equal(contentHash(outputs),receipt.outputsSha256,'Wrong replay display hash');
  const groups=projection(outputs);const before=await measure(client);
  assert.ok(before.databaseBytes+Buffer.byteLength(JSON.stringify(groups))*3<DEFAULT_BUDGET,'Display storage ceiling');
  await client.query('BEGIN');
  try {
    await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
    const run=(await client.query("SELECT id,diagnostics FROM ontap_shadow.feed_runs WHERE feed_key=$1 AND status='accepted'",['raw-stage:'+receipt.archiveSha256+':100'])).rows[0];
    assert.equal(run?.diagnostics.selection_parity?.outputs_sha256,receipt.outputsSha256);
    const selected=(await client.query(`SELECT a.supplier_job_id AS ref,d.scope,d.evidence->'regions' AS regions,a.apply_url FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%' AND d.decision='include'`,[run.id])).rows;
    assert.equal(groups.length,selected.length);const known=new Map(selected.map(d=>[d.scope+':'+d.ref,d]));
    for(const g of groups){const d=known.get(g.scope+':'+g.ref);assert.ok(d);assert.deepEqual(g.displayRows.map(v=>v.region).sort(),d.regions.slice().sort());for(const v of g.displayRows)assert.equal(v.row.apply_url,d.apply_url);}
    const prior=run.diagnostics.display_snapshot;
    if(prior)assert.equal(prior.outputs_sha256,receipt.outputsSha256);
    else {
      for(let i=0;i<groups.length;i+=100){const part=groups.slice(i,i+100);const q=await client.query(`UPDATE ontap_shadow.selection_decisions d SET evidence=jsonb_set(d.evidence,'{displayRows}',r."displayRows") FROM jsonb_to_recordset($2::jsonb) AS r(ref text,scope text,"displayRows" jsonb),ontap_shadow.supplier_adverts a WHERE d.feed_run_id=$1 AND d.advert_id=a.id AND a.supplier_job_id=r.ref AND d.scope=r.scope AND d.decision='include'`,[run.id,JSON.stringify(part)]);assert.equal(q.rowCount,part.length);}
    }
    const rows=(await client.query(`SELECT d.scope,d.evidence->'displayRows' AS "displayRows" FROM ontap_shadow.selection_decisions d WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%' AND d.decision='include'`,[run.id])).rows;
    const actual=reconstruct(rows,Object.keys(outputs));assert.deepEqual(actual,outputs,'Database display differs');
    const after=await measure(client);assert.ok(after.databaseBytes<DEFAULT_BUDGET);
    const summary={outputs_sha256:contentHash(actual),scopes:Object.keys(actual).length,selectedDecisionRows:rows.length,source:'verified production selector outputs',beforeBytes:before.databaseBytes,afterBytes:after.databaseBytes};
    if(!prior)await client.query("UPDATE ontap_shadow.feed_runs SET diagnostics=jsonb_set(diagnostics,'{display_snapshot}',$2::jsonb) WHERE id=$1",[run.id,JSON.stringify(summary)]);
    assert.equal((await client.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status<>'withheld'")).rows[0].n,0);
    await client.query('COMMIT');return {outputs:actual,report:{...summary,replayed:!!prior}};
  }catch(e){await client.query('ROLLBACK');throw e;}
}

// Opt-in compact display representation; legacy pinned display evidence is intact.
export function encodeCompactDisplay(outputs,state){
 assert.equal(contentHash(outputs),state.report.outputsSha256,'Wrong compact display hash');
 const groups=projection(outputs),selected=state.decisions.filter(d=>d.decision==='include');
 assert.equal(groups.length,selected.length,'Incomplete compact display');
 const known=new Map(selected.map(d=>[d.scope+':'+d.ref,d]));
 for(const g of groups){const d=known.get(g.scope+':'+g.ref);assert.ok(d);assert.deepEqual(g.displayRows.map(x=>x.region).sort(),[...d.regions].sort());}
 const payload=gzipSync(Buffer.from(JSON.stringify(outputs)),{level:9}).toString('base64');
 assert.ok(payload.length<=32*1024*1024);
 return {version:1,codec:'gzip-base64',outputsSha256:contentHash(outputs),selectionStateSha256:contentHash(state),payload};
}
export function decodeCompactDisplay(saved,state){
 assert.equal(saved.version,1);assert.equal(saved.codec,'gzip-base64');assert.ok(saved.payload.length<=32*1024*1024);
 assert.equal(saved.selectionStateSha256,contentHash(state),'Wrong display selection state');
 const outputs=JSON.parse(gunzipSync(Buffer.from(saved.payload,'base64'),{maxOutputLength:128*1024*1024}));
 assert.equal(contentHash(outputs),saved.outputsSha256,'Corrupt compact display');
 encodeCompactDisplay(outputs,state);return outputs;
}
export async function attachCompactDisplay(client,runId,outputs){
 await client.query('BEGIN');try{
  await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
  const {state}=await readCompactSelection(client,runId);const packed=encodeCompactDisplay(outputs,state);
  const run=(await client.query('SELECT supplier_id,diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId])).rows[0];
  if(run.diagnostics.compact_display){assert.deepEqual(decodeCompactDisplay(run.diagnostics.compact_display,state),outputs);await client.query('COMMIT');return {replayed:true};}
  const ads=(await client.query('SELECT supplier_job_id,apply_url FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1',[run.supplier_id])).rows;
  const urls=new Map(ads.map(a=>[a.supplier_job_id,a.apply_url]));
  for(const rows of Object.values(outputs))for(const row of rows)assert.equal(row.apply_url,urls.get(row.job_id),'Apply URL differs from raw advert');
  const before=await measure(client);assert.ok(before.databaseBytes+Buffer.byteLength(JSON.stringify(packed))*3+64*1024*1024<DEFAULT_BUDGET,'Compact display storage ceiling');
  await client.query("UPDATE ontap_shadow.feed_runs SET diagnostics=jsonb_set(diagnostics,'{compact_display}',$2::jsonb) WHERE id=$1",[runId,JSON.stringify(packed)]);
  const saved=(await client.query('SELECT diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId])).rows[0].diagnostics.compact_display;
  assert.deepEqual(decodeCompactDisplay(saved,state),outputs);
  assert.ok((await measure(client)).databaseBytes+64*1024*1024<DEFAULT_BUDGET);
  await client.query('COMMIT');return {replayed:false,encodedBytes:Buffer.byteLength(JSON.stringify(packed))};
 }catch(e){await client.query('ROLLBACK');throw e;}
}
export async function readCompactDisplay(client,runId){
 const {state}=await readCompactSelection(client,runId);
 const run=(await client.query('SELECT diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId])).rows[0];
 assert.ok(run?.diagnostics.compact_display,'Missing verified compact display');
 return decodeCompactDisplay(run.diagnostics.compact_display,state);
}
