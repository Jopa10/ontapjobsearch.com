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
