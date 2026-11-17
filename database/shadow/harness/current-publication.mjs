import assert from 'node:assert/strict';
export function safeSchema(schema){
 assert.ok(['ontap_shadow','pg_temp'].includes(schema),'Unexpected publication schema');
 return schema;
}
export async function readCurrentPublication(client,{schema='ontap_shadow'}={}){
 const s=safeSchema(schema);
 const date=(await client.query('SELECT max(feed_date)::text AS date FROM '+s+'.daily_refresh_receipts')).rows[0].date;
 assert.ok(date,'No completed daily refresh receipt');
 const records=(await client.query('SELECT public_id,decision,raw_payload,payload_sha256,source_row_position FROM '+s+".selected_review_payload_records WHERE feed_date=$1::date AND decision='SELECTED' ORDER BY public_id",[date])).rows;
 const scopes=(await client.query('SELECT scope,jobg8_ids FROM '+s+'.daily_publication_scopes WHERE feed_date=$1::date ORDER BY scope',[date])).rows;
 const ids=new Set(records.map(r=>r.public_id)),placed=new Set();
 for(const scope of scopes){
  assert.ok(Array.isArray(scope.jobg8_ids));assert.equal(new Set(scope.jobg8_ids).size,scope.jobg8_ids.length);
  for(const id of scope.jobg8_ids){assert.ok(ids.has(id),'Scope includes a job outside latest selected set');placed.add(id);}
 }
 assert.deepEqual([...placed].sort(),[...ids].sort(),'Latest selected set and scope membership differ');
 return {feedDate:date,records,scopes};
}
