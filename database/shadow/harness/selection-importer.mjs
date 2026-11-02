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
