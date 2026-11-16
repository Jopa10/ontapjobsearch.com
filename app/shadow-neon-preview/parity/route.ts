import { NextResponse } from 'next/server';
import { Client } from 'pg';
import { createHash } from 'node:crypto';
export const dynamic = 'force-dynamic';
const sha = (value: string) => createHash('sha256').update(value).digest('hex');
export async function GET() {
  if (process.env.VERCEL_ENV !== 'preview' ||
      process.env.ONTAP_SHADOW_NEON_PROJECT_ID !== 'noisy-fire-97386602') {
    return new NextResponse('Not found', {status: 404});
  }
  const secret = process.env.ONTAP_SHADOW_DATABASE_URL;
  if (!secret) return NextResponse.json({ error: 'Preview Neon connection missing' }, { status: 503 });
  const url = new URL(secret);
  if (!url.hostname.endsWith('.neon.tech') || !['require','verify-full'].includes(url.searchParams.get('sslmode') || '')) {
    return NextResponse.json({ error: 'Preview connection guard failed' }, {status:503});
  }
  url.searchParams.set('sslmode','verify-full');
  const client = new Client({connectionString:url.toString(), connectionTimeoutMillis:15000, query_timeout:30000,
    application_name:'ontap-neon-publication-parity-readonly'});
  try {
    await client.connect();
    await client.query('BEGIN READ ONLY');
    const latest = await client.query("SELECT max(feed_date)::text AS date FROM ontap_shadow.selected_review_payload_records");
    const date: string | null = latest.rows[0]?.date ?? null;
    if (!date) throw new Error('No dated Neon snapshot');
    const r = await client.query(
      "SELECT public_id, decision, raw_payload->>'/Job/Position' AS title, raw_payload->>'/Job/ApplicationURL' AS apply_url FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date ORDER BY public_id",
      [date]
    );
    await client.query('COMMIT');
    const selected = r.rows.filter(x => x.decision === 'SELECTED');
    const review = r.rows.filter(x => x.decision === 'REVIEW');
    const ids = selected.map(x => String(x.public_id));
    const apply = selected.map(x => String(x.public_id)+'\\t'+String(x.apply_url ?? ''));
    const title = selected.map(x => String(x.public_id)+'\\t'+String(x.title ?? ''));
    return NextResponse.json({
      snapshotDate: date, selectedCount: selected.length, reviewCount: review.length,
      selectedUniqueIds: new Set(ids).size, selectedIdsSha256: sha(ids.join('\\n')),
      applyUrlsSha256: sha(apply.join('\\n')), titlesSha256: sha(title.join('\\n')),
      missingTitle: selected.filter(x=>!x.title).length,
      missingApplyUrl: selected.filter(x=>!x.apply_url).length,
      source: 'ontap_shadow.selected_review_payload_records', neonReadOnly:true,
      comparisonScope: 'JobG8 exact selected IDs, raw title and Apply URL, not per-region/page publisher output'
    }, {headers:{'Cache-Control':'no-store','X-Robots-Tag':'noindex, nofollow'}});
  } catch (error) {
    await client.query('ROLLBACK').catch(()=>{});
    return NextResponse.json({error: error instanceof Error?error.message:'Neon read failed'}, {status:500});
  } finally { await client.end().catch(()=>{}); }
}
