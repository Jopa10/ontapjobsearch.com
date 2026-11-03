import {canonicalSelection,encodeHistory,decodeHistory} from './selection-history.mjs';
import assert from 'node:assert/strict';
import { contentHash, stableId } from './importer.mjs';
import { measure, DEFAULT_BUDGET } from './staged-importer.mjs';
export const PIN='046881410cda7588c5589af808449b6e3f41c8b889955de8b57c23be426ab5bd';

export async function attachSelection(client, fixture) {
  const {report,decisions,sourceHashes}=fixture;
  assert.equal(report.archiveSha256,PIN,'Wrong pinned archive');
  assert.equal(report.exactFileOutputParity,true);
  assert.equal(report.unknowns,0,'Incomplete evidence');
  assert.match(report.rulesRevision,/^[a-f0-9]{40}$/);
  assert.ok(report.cleanRecords>0 && report.cleanRecords<=60000);
  assert.equal(sourceHashes.length,report.cleanRecords);
  assert.equal(decisions.length,sourceHashes.length*8);
  const known=new Map(sourceHashes);
  assert.equal(known.size,sourceHashes.length);
  const scopes=new Set(['admin_service','support_worker','customer_sales','finance_accounts','hr_recruitment','marketing','legal_assistant_paralegal','customer_service_contact_centre'].map(f=>'production:'+f));
  const keys=new Set();
  for (const row of decisions) {
    assert.ok(known.has(row.ref) && scopes.has(row.scope));
    assert.ok(['include','exclude','review'].includes(row.decision));
    assert.ok(typeof row.reason==='string' && row.reason.length>0 && row.reason.length<10000);
    assert.ok(typeof row.gate==='string' && row.gate.length<10000);
    assert.ok(Array.isArray(row.regions) && row.regions.every(r=>typeof r==='string' && r.length>0 && r.length<300));
    assert.equal(new Set(row.regions).size,row.regions.length);
    assert.equal(row.regions.length>0,row.decision==='include');
    const key=row.scope+':'+row.ref;
    assert.ok(!keys.has(key),'Duplicate decision'); keys.add(key);
  }
  const checksum=contentHash({report,decisions,sourceHashes});
  const before=await measure(client);
  assert.ok(before.databaseBytes<DEFAULT_BUDGET,'Measured selection storage exceeds ceiling');
  let projected;
  await client.query('BEGIN');
  try {
    await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
    const run=(await client.query(`SELECT r.id,r.supplier_id,r.diagnostics FROM ontap_shadow.feed_runs r JOIN ontap_shadow.suppliers s ON s.id=r.supplier_id WHERE s.code='jobg8' AND r.feed_key=$1 AND r.status='accepted'`,[`raw-stage:${PIN}:100`])).rows[0];
    assert.ok(run,'Missing accepted full pinned import');
    const stored=(await client.query('SELECT supplier_job_id,content_hash FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1',[run.supplier_id])).rows;
    assert.equal(stored.length,known.size);
    for (const row of stored) assert.equal(row.content_hash,known.get(row.supplier_job_id),'Database advert differs from pinned input');
    const prior=run.diagnostics.selection_parity;
    if (prior) {
      assert.equal(prior.checksum,checksum,'Conflicting selector replay');
      const existing=(await client.query("SELECT a.supplier_job_id AS ref,d.scope,d.decision,d.reason,d.evidence->>'gate' AS gate,d.evidence->'regions' AS regions FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%'",[run.id])).rows;
      const order=(a,b)=>(a.scope+':'+a.ref).localeCompare(b.scope+':'+b.ref);
      assert.deepEqual(existing.sort(order),[...decisions].sort(order));
      const count=existing.length;
      await client.query('COMMIT');
      return {replayed:true,before,after:await measure(client),decisionCount:count,checksum};
    }
    const current=await measure(client);
    projected=current.databaseBytes+Buffer.byteLength(JSON.stringify(decisions))*3+decisions.length*512;
    assert.ok(projected<DEFAULT_BUDGET,'Selection storage preflight exceeds ceiling');
    for (let offset=0;offset<decisions.length;offset+=1000) {
      const rows=decisions.slice(offset,offset+1000).map(r=>({...r,id:stableId(`selection:${run.id}:${r.scope}:${r.ref}`)}));
      const inserted=await client.query(`INSERT INTO ontap_shadow.selection_decisions(id,advert_id,feed_run_id,scope,decision,reason,rules_revision,evidence)
        SELECT r.id,a.id,$2,r.scope,r.decision,r.reason,$3,jsonb_build_object('gate',r.gate,'regions',r.regions)
        FROM jsonb_to_recordset($1::jsonb) AS r(id uuid,ref text,scope text,decision text,reason text,gate text,regions jsonb)
        JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$4 AND a.supplier_job_id=r.ref`,[JSON.stringify(rows),run.id,report.rulesRevision,run.supplier_id]);
      assert.equal(inserted.rowCount,rows.length);
    }
    // Compare every stored ID/outcome/reason/gate, not just aggregate counts.
    const actual=(await client.query("SELECT a.supplier_job_id AS ref,d.scope,d.decision,d.reason,d.evidence->>'gate' AS gate,d.evidence->'regions' AS regions FROM ontap_shadow.selection_decisions d JOIN ontap_shadow.supplier_adverts a ON a.id=d.advert_id WHERE d.feed_run_id=$1 AND d.scope LIKE 'production:%'",[run.id])).rows;
    const order=(a,b)=>(a.scope+':'+a.ref).localeCompare(b.scope+':'+b.ref);
    assert.deepEqual(actual.sort(order),[...decisions].sort(order));
    const summary={checksum,decisions:decisions.length,rules_revision:report.rulesRevision,outputs_sha256:report.outputsSha256,scope:'JobG8 family generation',unknowns:0};
    await client.query("UPDATE ontap_shadow.feed_runs SET diagnostics=jsonb_set(diagnostics,'{selection_parity}',$2::jsonb) WHERE id=$1",[run.id,JSON.stringify(summary)]);
    // All test jobs remain withheld; no availability, raw payload or public ID update.
    assert.equal(Number((await client.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status<>'withheld'")).rows[0].n),0);
    const after=await measure(client);
    assert.ok(after.databaseBytes<DEFAULT_BUDGET,'Measured selection storage exceeds ceiling');
    await client.query('COMMIT');
    return {replayed:false,before,after,decisionCount:actual.length,checksum,projectedDatabaseBytes:projected};
  } catch (error) {await client.query('ROLLBACK');throw error;}
}

// Alternative representation in existing run diagnostics; legacy pinned rows
// and display evidence are preserved. No selector evaluation is skipped.
export async function readCompactSelection(client,runId,visited=new Set()) {
  assert.ok(!visited.has(runId)&&visited.size<=6,'Invalid compact history ancestry');visited.add(runId);
  const run=(await client.query('SELECT id,supplier_id,feed_date::text, status,diagnostics FROM ontap_shadow.feed_runs WHERE id=$1',[runId])).rows[0];
  assert.ok(run?.status==='accepted','Missing accepted history run');
  const saved=run.diagnostics.compact_selection;
  assert.ok(saved?.envelope,'Missing compact history');
  let parent=null;
  if(saved.envelope.kind==='delta'){
    assert.ok(saved.parentRunId,'Missing parent run');
    const prior=await readCompactSelection(client,saved.parentRunId,visited);
    assert.equal(String(prior.run.supplier_id),String(run.supplier_id));
    assert.ok(prior.run.feed_date<run.feed_date,'History must advance by feed date');
    assert.equal(saved.envelope.depth,prior.envelope.depth+1);
    parent=prior.state;
  }else assert.equal(saved.parentRunId,null);
  const state=decodeHistory(saved.envelope,parent);
  assert.equal(state.report.archiveSha256,run.diagnostics.archive_sha256,'History raw-run provenance mismatch');
  assert.equal(state.sourceHashes.length,run.diagnostics.imported_records,'History membership count mismatch');
  return {state,envelope:saved.envelope,run};
}
export async function attachCompactSelection(client,{runId,fixture,context,parentRunId=null}) {
  const expected=canonicalSelection(fixture,context);
  await client.query('BEGIN');
  try{
    await client.query("SELECT pg_advisory_xact_lock(hashtext('ontap_shadow:jobg8'))");
    const run=(await client.query(`SELECT r.id,r.supplier_id,r.feed_date::text,r.diagnostics FROM ontap_shadow.feed_runs r JOIN ontap_shadow.suppliers s ON s.id=r.supplier_id WHERE r.id=$1 AND r.status='accepted' AND s.code='jobg8'`,[runId])).rows[0];
    assert.ok(run,'Missing accepted JobG8 run');
    if(run.diagnostics.compact_selection){
      const saved=await readCompactSelection(client,runId);
      assert.deepEqual(saved.state,expected,'Conflicting compact replay');
      await client.query('COMMIT');
      return {replayed:true,decisionCount:expected.decisions.length,newDecisionRows:0,stateSha256:saved.envelope.stateSha256};
    }
    assert.equal(run.diagnostics.percentage,100,'Full raw import required');
    assert.equal(run.diagnostics.archive_sha256,fixture.report.archiveSha256);
    assert.equal(run.diagnostics.imported_records,fixture.sourceHashes.length);
    // Membership is specific to the accepted raw run, not the whole historical
    // advert table. Existing staged imports assign appearances to the full run.
    const stored=(await client.query(`SELECT a.supplier_job_id AS ref,a.content_hash FROM ontap_shadow.advert_appearances p JOIN ontap_shadow.supplier_adverts a ON a.id=p.advert_id WHERE p.feed_run_id=$1 AND p.supplier_id=$2`,[runId,run.supplier_id])).rows;
    const hashes=new Map(fixture.sourceHashes);assert.equal(stored.length,hashes.size,'Run membership mismatch');
    for(const row of stored)assert.equal(row.content_hash,hashes.get(row.ref),'Current raw advert differs from verified selection');
    let parent=null;
    if(parentRunId){
      parent=await readCompactSelection(client,parentRunId);
      assert.equal(String(parent.run.supplier_id),String(run.supplier_id));
      assert.ok(parent.run.feed_date<run.feed_date,'History must advance by feed date');
    }
    const encoded=encodeHistory(fixture,context,parent);
    const saved={parentRunId:encoded.envelope.kind==='delta'?parentRunId:null,envelope:encoded.envelope};
    const before=await measure(client),reserve=64*1024*1024;
    const projected=before.databaseBytes+Buffer.byteLength(JSON.stringify(saved))*3+65536;
    assert.ok(projected+reserve<DEFAULT_BUDGET,'Compact history storage preflight exceeds reserved ceiling');
    await client.query(`UPDATE ontap_shadow.feed_runs SET diagnostics=diagnostics || jsonb_build_object('compact_selection',$2::jsonb,'selection_representation','compact_v1','selection_status','verified') WHERE id=$1`,[runId,JSON.stringify(saved)]);
    assert.deepEqual((await readCompactSelection(client,runId)).state,expected,'Compact database readback differs');
    assert.equal(Number((await client.query("SELECT count(*)::int AS n FROM ontap_shadow.jobs WHERE publication_status<>'withheld'")).rows[0].n),0);
    const after=await measure(client);assert.ok(after.databaseBytes+reserve<DEFAULT_BUDGET,'Compact history measured storage exceeds reserved ceiling');
    await client.query('COMMIT');
    return {replayed:false,decisionCount:expected.decisions.length,newDecisionRows:0,changedDecisions:encoded.envelope.changedDecisions,compressedBytes:encoded.compressedBytes,encodedBytes:encoded.encodedBytes,stateSha256:encoded.envelope.stateSha256,kind:encoded.envelope.kind,projectedDatabaseBytes:projected,before,after};
  }catch(error){await client.query('ROLLBACK');throw error;}
}
