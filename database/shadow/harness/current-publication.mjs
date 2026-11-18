import assert from 'node:assert/strict';

export function safeSchema(schema){
 assert.ok(['ontap_shadow','pg_temp'].includes(schema),'Unexpected publication schema');
 return schema;
}
export async function readCurrentPublication(client,{schema='ontap_shadow'}={}){
 const s=safeSchema(schema);
 const date=(await client.query('SELECT max(feed_date)::text AS date FROM '+s+'.daily_refresh_receipts')).rows[0].date;
 assert.ok(date,'No completed daily refresh receipt');
 const records=(await client.query(
  "SELECT j.public_id,'SELECTED'::text AS decision,a.raw_payload,aa.payload_sha256,aa.source_row_position "+
  "FROM "+s+".advert_appearances aa "+
  "JOIN "+s+".supplier_adverts a ON a.id=aa.advert_id AND a.supplier_id=aa.supplier_id "+
  "JOIN "+s+".jobs j ON j.id=a.job_id "+
  "JOIN "+s+".suppliers sup ON sup.id=aa.supplier_id "+
  "JOIN "+s+".selection_decisions d ON d.advert_id=aa.advert_id AND d.feed_run_id=aa.feed_run_id AND d.scope='daily_selected' "+
  "WHERE aa.seen_on=$1::date AND sup.code='jobg8' AND d.decision='include' ORDER BY j.public_id",[date])).rows;
 const scopes=(await client.query('SELECT scope,jobg8_ids FROM '+s+'.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',[date])).rows;
 const ids=new Set(records.map(r=>r.public_id)),placed=new Set();
 for(const row of records){
  assert.ok(row.raw_payload,'Current selected master payload missing: '+row.public_id);
  assert.ok(row.payload_sha256,'Current appearance payload hash missing: '+row.public_id);
  assert.ok(Number.isInteger(row.source_row_position)&&row.source_row_position>0,'Current appearance feed position missing: '+row.public_id);
 }
 for(const scope of scopes){
  assert.ok(Array.isArray(scope.jobg8_ids));assert.equal(new Set(scope.jobg8_ids).size,scope.jobg8_ids.length);
  for(const id of scope.jobg8_ids){assert.ok(ids.has(id),'Scope includes a job outside latest selected set');placed.add(id);}
 }
 assert.deepEqual([...placed].sort(),[...ids].sort(),'Latest selected set and scope membership differ');
 return {feedDate:date,records,scopes};
}
