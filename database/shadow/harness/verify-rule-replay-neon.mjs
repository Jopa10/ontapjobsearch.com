import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {requirePreview,hash,MAX,RESERVE} from './publisher-safeguards.mjs';
requirePreview(process.env);
const report=JSON.parse(await fs.readFile('rule-change-report.json','utf8'));
const changes=JSON.parse(await fs.readFile('rule-change-jobs.json','utf8'));
assert.equal(report.status,'passed');assert.equal(report.revisedScopeDifferencesFromProduction.length,0);
const canon=v=>Array.isArray(v)?v.map(canon):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canon(v[k])])):v;
const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);u.searchParams.set('sslmode','verify-full');
const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:120000,application_name:'ontap-preview-rule-change-readback'});
try{
 await c.connect();
 const beforeBytes=Number((await c.query('SELECT pg_database_size(current_database())::text AS bytes')).rows[0].bytes);
 assert.ok(beforeBytes+RESERVE+16*1024*1024<MAX,'Preview headroom insufficient for rule decision evidence');
 const current=(await c.query('SELECT max(feed_date)::text AS date FROM ontap_shadow.selected_review_payload_records')).rows[0].date;
 assert.equal(current,report.feedDate);
 const payloads=(await c.query('SELECT public_id,decision,raw_payload,payload_sha256,source_row_position FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date AND public_id=ANY($2::text[])',[current,changes.map(x=>x.jobId)])).rows;
 for(const p of payloads)assert.equal(hash(JSON.stringify(canon(p.raw_payload))),p.payload_sha256,'Changed-job payload hash differs '+p.public_id);
 const byId=new Map(payloads.map(x=>[x.public_id,x]));
 for(const id of report.addedPublishedIds){assert.equal(byId.get(id)?.decision,'SELECTED','Newly selected ID absent from Neon '+id);}
 await c.query('BEGIN');
 try{
  await c.query("CREATE TABLE IF NOT EXISTS ontap_shadow.rule_replay_decisions(feed_date date NOT NULL,public_id text NOT NULL,feed_excel_row integer NOT NULL,before_revision text NOT NULL,after_revision text NOT NULL,evidence jsonb NOT NULL,PRIMARY KEY(feed_date,public_id,feed_excel_row))");
  for(const r of changes)await c.query('INSERT INTO ontap_shadow.rule_replay_decisions VALUES($1::date,$2,$3,$4,$5,$6::jsonb) ON CONFLICT(feed_date,public_id,feed_excel_row) DO UPDATE SET before_revision=excluded.before_revision,after_revision=excluded.after_revision,evidence=excluded.evidence',[current,r.jobId,Number(r.feedExcelRow),report.beforeRulesCommit,report.productionSourceCommit,JSON.stringify(r)]);
  const readback=(await c.query('SELECT public_id,feed_excel_row,evidence FROM ontap_shadow.rule_replay_decisions WHERE feed_date=$1::date ORDER BY public_id,feed_excel_row',[current])).rows;
  assert.equal(readback.length,changes.length);
  const expected=new Map(changes.map(r=>[r.jobId+':'+r.feedExcelRow,r]));
  for(const r of readback)assert.deepEqual(r.evidence,expected.get(r.public_id+':'+r.feed_excel_row));
  await c.query('COMMIT');
 }catch(e){await c.query('ROLLBACK');throw e;}
 const result={status:'passed',feedDate:current,changedDecisionRows:changes.length,changedJobIds:report.changedJobIds,exactDecisionReadback:true,changedJobPayloadsVerified:payloads.length,payloadHashesMatched:true,excludePayloadsWritten:0,productionChanged:false,sourceComparisonReport:report};
 await fs.mkdir('dist',{recursive:true});await fs.writeFile('dist/rule-replay-neon-report.json',JSON.stringify(result,null,2)+'\n');await fs.writeFile('dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><h1>Preview rule replay passed</h1>');
 console.log('ONTAP_RULE_CHANGE_NEON '+JSON.stringify({...result,sourceComparisonReport:undefined}));
}finally{await c.end();}
