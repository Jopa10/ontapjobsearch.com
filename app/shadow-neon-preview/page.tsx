import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { Client } from 'pg';

export const dynamic = 'force-dynamic';
export const metadata: Metadata = { title: 'Neon Preview Read Verification | Ontap', robots: { index: false, follow: false } };

type Sample = { public_id: string; title: string; apply_url: string };
type Report = { date: string; selected: number; review: number; unique: number; sample: Sample[] };

async function getLatestCompletedPreviewSnapshot(): Promise<Report> {
  if (process.env.VERCEL_ENV !== 'preview' ||
      process.env.ONTAP_SHADOW_NEON_PROJECT_ID !== 'noisy-fire-97386602') {
    notFound();
  }
  const raw = process.env.ONTAP_SHADOW_DATABASE_URL;
  if (!raw) throw new Error('Preview Neon database connection not configured');
  const url = new URL(raw);
  if (!url.hostname.endsWith('.neon.tech') || !['require', 'verify-full'].includes(url.searchParams.get('sslmode') || '')) {
    throw new Error('Unexpected Neon connection endpoint');
  }
  url.searchParams.set('sslmode', 'verify-full');
  const client = new Client({
    connectionString: url.toString(),
    connectionTimeoutMillis: 10000,
    query_timeout: 15000,
    application_name: 'ontap-preview-website-read-check',
  });
  await client.connect();
  try {
    await client.query('BEGIN READ ONLY');
    const dateResult = await client.query(
      "SELECT max(feed_date)::text AS date FROM ontap_shadow.selected_review_payload_records"
    );
    const date = dateResult.rows[0]?.date as string | undefined;
    if (!date) throw new Error('No completed stored feed date available');
    const summary = await client.query(
      "SELECT decision, count(*)::int AS n FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date GROUP BY decision",
      [date]
    );
    const counts = Object.fromEntries(summary.rows.map((r: {decision:string;n:number}) => [r.decision, r.n]));
    const sample = await client.query(
      "SELECT public_id, raw_payload->>'/Job/Position' AS title, raw_payload->>'/Job/ApplicationURL' AS apply_url FROM ontap_shadow.selected_review_payload_records WHERE feed_date=$1::date AND decision='SELECTED' AND raw_payload ? '/Job/Position' AND raw_payload ? '/Job/ApplicationURL' ORDER BY public_id LIMIT 20",
      [date]
    );
    await client.query('COMMIT');
    return { date, selected: counts.SELECTED ?? 0, review: counts.REVIEW ?? 0,
      unique: (counts.SELECTED ?? 0) + (counts.REVIEW ?? 0), sample: sample.rows };
  } catch (error) {
    await client.query('ROLLBACK').catch(() => {});
    throw error;
  } finally {
    await client.end();
  }
}

export default async function ShadowNeonPreviewPage() {
  const data = await getLatestCompletedPreviewSnapshot();
  return (
    <main style={{ maxWidth: 900, margin: '48px auto', padding: 24, fontFamily: 'system-ui' }}>
      <h1>Ontap Neon-to-website Preview read test</h1>
      <p>This page is built by Next.js from a read-only query to the isolated Neon Preview database. No production publishing is performed.</p>
      <p><strong>Latest stored feed:</strong> {data.date}</p>
      <p><strong>Selected:</strong> {data.selected.toLocaleString('en-GB')} · <strong>Review:</strong> {data.review.toLocaleString('en-GB')} · <strong>Unique records:</strong> {data.unique.toLocaleString('en-GB')}</p>
      <h2>Selected jobs read directly from Neon (sample)</h2>
      <ol>{data.sample.map(job => (
        <li key={job.public_id} style={{ marginBottom: 12 }}>
          <strong>{job.title}</strong> <span>({job.public_id})</span>{' '}
          <a href={job.apply_url} rel="nofollow noopener noreferrer" target="_blank">Apply link</a>
        </li>
      ))}</ol>
      <p>This is an initial read-path smoke test. Full website pages, city/region parity and publish cutover are separate checks.</p>
    </main>
  );
}
