// Deliberate Preview-only storage audit: SELECTs in one read-only transaction.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import pg from 'pg';
import {readExcludePayloadBreakdown} from './exclude-retention.mjs';
async function main(){
 assert.equal(process.env.VERCEL_ENV,'preview');
 assert.equal(process.env.ONTAP_SHADOW_NEON_PROJECT_ID,'noisy-fire-97386602');
 const u=new URL(process.env.ONTAP_SHADOW_DATABASE_URL);
 assert.ok(u.hostname.endsWith('.neon.tech'));
 assert.ok(['require','verify-full'].includes(u.searchParams.get('sslmode')));
 u.searchParams.set('sslmode','verify-full');
 const c=new pg.Client({connectionString:u.toString(),connectionTimeoutMillis:15000,query_timeout:60000,statement_timeout:45000,application_name:'ontap-shadow-readonly-retention-audit'});
 const report={measuredAt:new Date().toISOString(),readOnly:true,maximumDatabaseBytes:838860800};
 try{
  await c.connect();await c.query('BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY');
  report.transactionReadOnly=(await c.query('SHOW transaction_read_only')).rows[0].transaction_read_only;
  assert.equal(report.transactionReadOnly,'on');
  report.database=(await c.query(`SELECT pg_database_size(current_database())::text AS bytes`)).rows[0];
  report.tables=(await c.query(`SELECT c.relname AS name,pg_relation_size(c.oid)::text AS heap_bytes,pg_table_size(c.oid)::text AS table_with_toast_bytes,pg_indexes_size(c.oid)::text AS index_bytes,pg_total_relation_size(c.oid)::text AS total_bytes,s.n_live_tup::text,s.n_dead_tup::text FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace LEFT JOIN pg_stat_user_tables s ON s.relid=c.oid WHERE n.nspname='ontap_shadow' AND c.relkind='r' ORDER BY pg_total_relation_size(c.oid) DESC`)).rows;
  report.adverts=(await c.query(`SELECT count(*)::text AS rows,count(raw_payload)::text AS payload_rows,coalesce(sum(pg_column_size(raw_payload)),0)::text AS stored_payload_bytes,coalesce(sum(octet_length(raw_payload::text)),0)::text AS text_payload_bytes,min(first_seen)::text,max(last_seen)::text,count(*) FILTER(WHERE inactive_since IS NOT NULL)::text AS inactive_rows FROM ontap_shadow.supplier_adverts`)).rows[0];
  report.excludeReviewBaseline=await readExcludePayloadBreakdown(c);
  report.decisions=(await c.query(`SELECT scope,decision,count(*)::text AS rows,sum(pg_column_size(d))::text AS row_bytes,sum(pg_column_size(evidence))::text AS stored_evidence_bytes,sum(octet_length(evidence::text))::text AS text_evidence_bytes,sum(CASE WHEN evidence ? 'displayRows' THEN octet_length((evidence->'displayRows')::text) ELSE 0 END)::text AS display_text_bytes FROM ontap_shadow.selection_decisions d GROUP BY scope,decision ORDER BY scope,decision`)).rows;
  report.appearances=(await c.query(`SELECT seen_on::text,count(*)::text AS rows,sum(pg_column_size(a))::text AS row_bytes FROM ontap_shadow.advert_appearances a GROUP BY seen_on ORDER BY seen_on`)).rows;
  report.runs=(await c.query(`SELECT feed_key,feed_date::text,status,received_count,rules_revision FROM ontap_shadow.feed_runs ORDER BY started_at`)).rows;
  report.jobs=(await c.query(`SELECT publication_status,count(*)::text AS rows,sum(pg_column_size(j))::text AS row_bytes FROM ontap_shadow.jobs j GROUP BY publication_status`)).rows;
  await c.query('COMMIT');
 }finally{await c.end();}
 await fs.mkdir('retention-dist',{recursive:true});
 await fs.writeFile('retention-dist/report.json',JSON.stringify(report,null,2)+'\n');
 await fs.writeFile('retention-dist/index.html','<!doctype html><meta name="robots" content="noindex,nofollow"><title>Ontap read-only storage audit</title><p>Storage measurement completed. No database records changed.</p>');
 for (const [key,value] of Object.entries(report)) console.log('ONTAP_RETENTION_AUDIT '+JSON.stringify({[key]:value}));
}
main().catch(e=>{console.error('ONTAP_RETENTION_AUDIT_FAILED',e.code||'audit_error');process.exitCode=1;});
