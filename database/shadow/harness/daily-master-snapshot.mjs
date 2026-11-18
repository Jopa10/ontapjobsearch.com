import assert from 'node:assert/strict';
import {stableId,contentHash} from './importer.mjs';

const number=v=>{if(v===''||v==null)return null;const n=Number(v);return Number.isFinite(n)?n:null;};
const text=(v)=>typeof v==='string'&&v.trim()?v.trim():null;
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);

export function changedPayloadFields(before,after){
 if(!before)return [];
 return [...new Set([...Object.keys(before||{}),...Object.keys(after||{})])]
  .filter(k=>!equal(before?.[k],after?.[k])).sort();
}
export function changeNote(fields){
 if(!fields.length)return null;
 const names=fields.map(k=>{
  const leaf=k.split('/').filter(Boolean).at(-1)||k;
  return leaf.replaceAll('_',' ').replace(/([a-z])([A-Z])/g,'$1 $2').toLowerCase();
 });
 return [...new Set(names)].map(name=>name+' updated').join('; ');
}
export async function ensureDailyMasterSchema(c){
 await c.query('ALTER TABLE ontap_shadow.advert_appearances ADD COLUMN IF NOT EXISTS payload_sha256 text');
 await c.query("ALTER TABLE ontap_shadow.advert_appearances ADD COLUMN IF NOT EXISTS changed_fields jsonb NOT NULL DEFAULT '[]'::jsonb");
 await c.query('ALTER TABLE ontap_shadow.advert_appearances ADD COLUMN IF NOT EXISTS change_note text');
}
export async function readMasterAppearance(c,feedDate){
 return (await c.query(
  "SELECT j.public_id,'SELECTED'::text AS decision,a.raw_payload,aa.payload_sha256,aa.source_row_position,aa.changed_fields,aa.change_note "+
  "FROM ontap_shadow.advert_appearances aa JOIN ontap_shadow.supplier_adverts a ON a.id=aa.advert_id "+
  "JOIN ontap_shadow.jobs j ON j.id=a.job_id JOIN ontap_shadow.suppliers s ON s.id=aa.supplier_id "+
  "WHERE aa.seen_on=$1::date AND s.code='jobg8' ORDER BY j.public_id",[feedDate])).rows;
}
export async function upsertSelectedMaster(c,{snapshot,scopes,source}){
 await ensureDailyMasterSchema(c);
 const ids=snapshot.records.map(r=>r.public_id);
 const supplier=Number((await c.query("INSERT INTO ontap_shadow.suppliers(code,name) VALUES('jobg8','JobG8') ON CONFLICT(code) DO UPDATE SET name=EXCLUDED.name RETURNING id")).rows[0].id);
 const oldRows=(await c.query(
  'SELECT id,job_id,supplier_job_id,content_hash,raw_payload FROM ontap_shadow.supplier_adverts WHERE supplier_id=$1 AND supplier_job_id=ANY($2::text[]) FOR UPDATE',[supplier,ids])).rows;
 const oldById=new Map(oldRows.map(r=>[r.supplier_job_id,r]));
 const runKey='selected-daily:'+snapshot.feedDate+':'+snapshot.archiveSha256+':'+snapshot.productionWorkflowRunId;
 const runId=stableId('run:jobg8:'+runKey);
 const sourceChecksum=source.payloadPackageSha256;
 const priorRun=(await c.query('SELECT id,status,source_checksum FROM ontap_shadow.feed_runs WHERE supplier_id=$1 AND feed_key=$2',[supplier,runKey])).rows[0];
 if(priorRun){assert.equal(priorRun.status,'accepted','Daily master feed run is incomplete');assert.equal(priorRun.source_checksum,sourceChecksum,'Conflicting same-day selected payload package');}
 else await c.query(
  "INSERT INTO ontap_shadow.feed_runs(id,supplier_id,feed_key,feed_date,source_checksum,status,started_at,completed_at,received_count,published_count,rules_revision,diagnostics) "+
  "VALUES($1,$2,$3,$4::date,$5,'accepted',now(),now(),$6,$7,$8,$9::jsonb)",
  [runId,supplier,runKey,snapshot.feedDate,sourceChecksum,snapshot.rawFeedJobNodes,snapshot.selectedIds,snapshot.productionRunCommit,
   JSON.stringify({selection_representation:'selected_only_master',production_run_id:snapshot.productionWorkflowRunId,production_app_commit:snapshot.productionAppCommit,archive_sha256:snapshot.archiveSha256,review_payloads_stored:false,excluded_payloads_stored:false})]);
 const scopeForId=new Map();
 for(const scope of scopes)for(const id of scope.jobg8Ids){if(!scopeForId.has(id))scopeForId.set(id,[]);scopeForId.get(id).push(scope.scope);}
 const rows=snapshot.records.map(r=>{
  const raw=r.raw_payload,old=oldById.get(r.public_id);
  const changed=old?.raw_payload&&old.content_hash!==r.payload_sha256?changedPayloadFields(old.raw_payload,raw):[];
  const advertId=old?.id||stableId('advert:jobg8:'+r.public_id);
  const jobId=old?.job_id||stableId('job:jobg8:'+r.public_id);
  const scopesFor=scopeForId.get(r.public_id)||[];
  const first=scopesFor[0]||'';
  const split=first.indexOf(':');
  return {public_id:r.public_id,advert_id:advertId,job_id:jobId,title:text(raw['/Job/Position'])||'Unknown title',
   employer:text(raw['/Job/AdvertiserName']),location:text(raw['/Job/Location']),region:split>=0?first.slice(split+1):null,
   role_family:split>=0?first.slice(0,split):null,salary_min:number(raw['/Job/SalaryMinimum']),salary_max:number(raw['/Job/SalaryMaximum']),
   salary_period:text(raw['/Job/SalaryPeriod']),salary_text:text(raw['/Job/SalaryAdditional']),advertiser:text(raw['/Job/AdvertiserName']),
   apply_url:text(raw['/Job/ApplicationURL']),raw_payload:raw,content_hash:r.payload_sha256,source_row_position:r.source_row_position,
   changed_fields:changed,change_note:changeNote(changed),scopes:scopesFor,first_seen:snapshot.feedDate});
 });
 for(let i=0;i<rows.length;i+=250){
  const batch=rows.slice(i,i+250);
  const json=JSON.stringify(batch);
  await c.query(
   'INSERT INTO ontap_shadow.jobs(id,public_id,title,employer,location,region,role_family,salary_min,salary_max,salary_period,salary_text,classification_evidence,first_seen,last_seen,publication_status) '+
   'SELECT r.job_id,r.public_id,r.title,r.employer,r.location,r.region,r.role_family,r.salary_min,r.salary_max,r.salary_period,r.salary_text,jsonb_build_object(\'selected_daily_scopes\',r.scopes),$2::date,$2::date,\'withheld\' '+
   'FROM jsonb_to_recordset($1::jsonb) AS r(job_id uuid,public_id text,title text,employer text,location text,region text,role_family text,salary_min numeric,salary_max numeric,salary_period text,salary_text text,scopes jsonb) '+
   'ON CONFLICT(id) DO UPDATE SET title=EXCLUDED.title,employer=EXCLUDED.employer,location=EXCLUDED.location,region=EXCLUDED.region,role_family=EXCLUDED.role_family,salary_min=EXCLUDED.salary_min,salary_max=EXCLUDED.salary_max,salary_period=EXCLUDED.salary_period,salary_text=EXCLUDED.salary_text,classification_evidence=EXCLUDED.classification_evidence,last_seen=GREATEST(ontap_shadow.jobs.last_seen,EXCLUDED.last_seen)',
   [JSON.stringify(batch.map(r=>({job_id:r.job_id,public_id:r.public_id,title:r.title,employer:r.employer,location:r.location,region:r.region,role_family:r.role_family,salary_min:r.salary_min,salary_max:r.salary_max,salary_period:r.salary_period,salary_text:r.salary_text,scopes:r.scopes}))),snapshot.feedDate]);
  await c.query(
   'INSERT INTO ontap_shadow.supplier_adverts(id,supplier_id,supplier_job_id,job_id,title,advertiser_name,location,apply_url,raw_payload,content_hash,first_seen,last_seen,availability) '+
   'SELECT r.advert_id,$2,r.public_id,r.job_id,r.title,r.advertiser,r.location,r.apply_url,r.raw_payload,r.content_hash,$3::date,$3::date,\'seen\' '+
   'FROM jsonb_to_recordset($1::jsonb) AS r(advert_id uuid,public_id text,job_id uuid,title text,advertiser text,location text,apply_url text,raw_payload jsonb,content_hash text) '+
   'ON CONFLICT(supplier_id,supplier_job_id) DO UPDATE SET title=EXCLUDED.title,advertiser_name=EXCLUDED.advertiser_name,location=EXCLUDED.location,apply_url=EXCLUDED.apply_url,'+
   'raw_payload=CASE WHEN ontap_shadow.supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR ontap_shadow.supplier_adverts.raw_payload IS NULL THEN EXCLUDED.raw_payload ELSE ontap_shadow.supplier_adverts.raw_payload END,'+
   'content_hash=EXCLUDED.content_hash,first_seen=LEAST(ontap_shadow.supplier_adverts.first_seen,EXCLUDED.first_seen),last_seen=GREATEST(ontap_shadow.supplier_adverts.last_seen,EXCLUDED.last_seen),inactive_since=NULL,availability=\'seen\','+
   'content_purged_at=CASE WHEN ontap_shadow.supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR ontap_shadow.supplier_adverts.raw_payload IS NULL THEN NULL ELSE ontap_shadow.supplier_adverts.content_purged_at END,'+
   'exclude_review_started_on=CASE WHEN ontap_shadow.supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash THEN NULL ELSE ontap_shadow.supplier_adverts.exclude_review_started_on END WHERE ontap_shadow.supplier_adverts.content_hash IS DISTINCT FROM EXCLUDED.content_hash OR ontap_shadow.supplier_adverts.raw_payload IS NULL OR ontap_shadow.supplier_adverts.last_seen < EXCLUDED.last_seen OR ontap_shadow.supplier_adverts.title IS DISTINCT FROM EXCLUDED.title OR ontap_shadow.supplier_adverts.advertiser_name IS DISTINCT FROM EXCLUDED.advertiser_name OR ontap_shadow.supplier_adverts.location IS DISTINCT FROM EXCLUDED.location OR ontap_shadow.supplier_adverts.apply_url IS DISTINCT FROM EXCLUDED.apply_url OR ontap_shadow.supplier_adverts.inactive_since IS NOT NULL OR ontap_shadow.supplier_adverts.availability IS DISTINCT FROM 'seen' OR ontap_shadow.supplier_adverts.content_purged_at IS NOT NULL',
   [json,supplier,snapshot.feedDate]);
  await c.query(
   'INSERT INTO ontap_shadow.advert_appearances(advert_id,seen_on,supplier_id,feed_run_id,source_row_position,payload_sha256,changed_fields,change_note) '+
   'SELECT r.advert_id,$2::date,$3,$4,r.source_row_position,r.content_hash,r.changed_fields,r.change_note FROM jsonb_to_recordset($1::jsonb) AS r(advert_id uuid,source_row_position integer,content_hash text,changed_fields jsonb,change_note text) '+
   'ON CONFLICT(advert_id,seen_on) DO UPDATE SET feed_run_id=EXCLUDED.feed_run_id,source_row_position=EXCLUDED.source_row_position,'+
   'changed_fields=CASE WHEN ontap_shadow.advert_appearances.payload_sha256 IS DISTINCT FROM EXCLUDED.payload_sha256 THEN EXCLUDED.changed_fields ELSE ontap_shadow.advert_appearances.changed_fields END,'+
   'change_note=CASE WHEN ontap_shadow.advert_appearances.payload_sha256 IS DISTINCT FROM EXCLUDED.payload_sha256 THEN EXCLUDED.change_note ELSE ontap_shadow.advert_appearances.change_note END,payload_sha256=EXCLUDED.payload_sha256',
   [JSON.stringify(batch.map(r=>({advert_id:r.advert_id,source_row_position:r.source_row_position,content_hash:r.content_hash,changed_fields:r.changed_fields,change_note:r.change_note}))),snapshot.feedDate,supplier,runId]);
  await c.query(
   "INSERT INTO ontap_shadow.selection_decisions(id,advert_id,feed_run_id,scope,decision,reason,rules_revision,evidence) "+
   "SELECT r.id,a.id,$2,'daily_selected','include','Present in final production-selected JobG8 output.',$3,jsonb_build_object('payload_sha256',r.content_hash,'source_row_position',r.source_row_position,'scopes',r.scopes) "+
   "FROM jsonb_to_recordset($1::jsonb) AS r(id uuid,public_id text,content_hash text,source_row_position integer,scopes jsonb) JOIN ontap_shadow.supplier_adverts a ON a.supplier_id=$4 AND a.supplier_job_id=r.public_id ON CONFLICT(advert_id,feed_run_id,scope) DO UPDATE SET decision='include',reason=EXCLUDED.reason,rules_revision=EXCLUDED.rules_revision,evidence=EXCLUDED.evidence",
   [JSON.stringify(batch.map(r=>({id:stableId('daily-selected:'+runId+':'+r.advert_id),public_id:r.public_id,content_hash:r.content_hash,source_row_position:r.source_row_position,scopes:r.scopes}))),runId,snapshot.productionRunCommit,supplier]);
 }
 await c.query('UPDATE ontap_shadow.jobs j SET preferred_advert_id=a.id FROM ontap_shadow.supplier_adverts a WHERE a.job_id=j.id AND a.preferred_advert_id IS NULL AND a.supplier_id=$1',[supplier]);
 const rows=await readMasterAppearance(c,snapshot.feedDate);
 assert.equal(rows.length,snapshot.records.length,'Master daily appearance count mismatch');
 const byId=new Map(rows.map(r=>[r.public_id,r]));
 for(const expected of snapshot.records){const actual=byId.get(expected.public_id);assert.ok(actual,'Missing master row '+expected.public_id);assert.equal(actual.payload_sha256,expected.payload_sha256,'Master payload hash differs '+expected.public_id);assert.deepEqual(actual.raw_payload,expected.raw_payload,'Master raw payload differs '+expected.public_id);assert.equal(actual.source_row_position,expected.source_row_position);}
 const oldMasterCount=oldRows.length;
 const changedCount=rows.filter(r=>{const old=oldById.get(r.public_id);return old&&old.content_hash!==r.payload_sha256;}).length;
 const insertedMasterCount=rows.length-oldMasterCount;
 const noteCount=rows.filter(r=>r.changed_fields?.length).length;
 return {supplierId:supplier,feedRunId:runId,feedKey:runKey,insertedMasterRows:insertedMasterCount,updatedPayloadRows:changedCount,unchangedMasterRows:rows.length-insertedMasterCount-changedCount,appearanceRows:rows.length,changedAdvertCount:noteCount};
}
