import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import QuickJobList from '@/components/QuickJobList';
import { getAtAGlanceAttributes } from '@/lib/at-a-glance-preview';
import {
  broadCityDefinitions,
  getBroadCityDefinition,
  getBroadCityJobs,
  getRegionSearchPath,
} from '@/lib/broad-city-pages';
import { getJobPath, type PublishedJob } from '@/lib/published-jobs';

const siteUrl = 'https://www.ontapjobsearch.com';

export const dynamicParams = false;

export function generateStaticParams() {
  return broadCityDefinitions.map((city) => ({ city: city.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ city: string }> }): Promise<Metadata> {
  const { city: slug } = await params;
  const city = getBroadCityDefinition(slug);
  if (!city) return {};
  const canonical = `${siteUrl}${city.route}`;
  return {
    title: `${city.display_name} Jobs | Current Vacancies | Ontap Job Search`,
    description: `Browse current jobs in ${city.display_name} across all live Ontap job categories, with direct employer application links.`,
    alternates: { canonical },
  };
}

function withAttributes(jobs: PublishedJob[]) {
  return jobs.map((job) => ({ ...job, at_a_glance_attributes: getAtAGlanceAttributes(job.job_id) }));
}

export default async function BroadCityPage({ params }: { params: Promise<{ city: string }> }) {
  const { city: slug } = await params;
  const city = getBroadCityDefinition(slug);
  if (!city) notFound();
  const { exact, nearby } = getBroadCityJobs(city);
  const regionPath = getRegionSearchPath(city.region);
  const breadcrumbs = [
    { name: 'Home', item: `${siteUrl}/` },
    { name: 'Jobs', item: `${siteUrl}/browse-jobs` },
    { name: city.region, item: `${siteUrl}${regionPath}` },
    { name: city.display_name, item: `${siteUrl}${city.route}` },
  ];
  const itemList = [...exact, ...nearby].map((job, index) => ({
    '@type': 'ListItem',
    position: index + 1,
    url: `${siteUrl}${getJobPath(job.job_id)}`,
    name: job.title,
  }));
  const schema = [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: `${city.display_name} Jobs`,
      url: `${siteUrl}${city.route}`,
      description: `Current vacancies in ${city.display_name} across all live Ontap job categories.`,
      isPartOf: { '@type': 'WebSite', name: 'Ontap Job Search', url: siteUrl },
    },
    {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: breadcrumbs.map((crumb, index) => ({
        '@type': 'ListItem', position: index + 1, name: crumb.name, item: crumb.item,
      })),
    },
    { '@context': 'https://schema.org', '@type': 'ItemList', itemListElement: itemList },
  ];

  return (
    <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      <nav aria-label="Breadcrumb" className="mb-4 flex flex-wrap gap-2 text-sm text-gray-600">
        <Link className="text-blue-700 underline" href="/">Home</Link><span aria-hidden="true">›</span>
        <Link className="text-blue-700 underline" href="/browse-jobs">Jobs</Link><span aria-hidden="true">›</span>
        <Link className="text-blue-700 underline" href={regionPath}>{city.region}</Link><span aria-hidden="true">›</span>
        <span aria-current="page">{city.display_name}</span>
      </nav>

      <h1 className="text-3xl font-bold tracking-tight text-gray-950 sm:text-4xl">Jobs in {city.display_name}</h1>
      <p className="mt-3 max-w-3xl text-base leading-7 text-gray-600">
        Current vacancies in {city.display_name} across all live job categories and providers. Jobs are refreshed daily and applications go to the employer site.
      </p>

      <aside className="my-6 flex flex-col justify-between gap-3 rounded-xl border border-blue-200 bg-blue-50 p-4 sm:flex-row sm:items-center">
        <div><div className="text-xs font-bold uppercase tracking-wide text-blue-900">Wider area</div><p className="mt-1 text-gray-700">See jobs across {city.region}.</p></div>
        <Link href={regionPath} className="font-semibold text-blue-700">View regional jobs →</Link>
      </aside>

      <section aria-labelledby="city-jobs-heading">
        <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="city-jobs-heading" className="text-2xl font-semibold text-gray-950">Jobs in {city.display_name}</h2>
          <span className="text-sm text-gray-600">{exact.length} current job{exact.length === 1 ? '' : 's'}</span>
        </div>
        {exact.length ? <QuickJobList jobs={withAttributes(exact)} sectorFilterEnabled /> : <p className="rounded-xl border border-gray-200 bg-gray-50 p-5 text-gray-700">There are no exact-{city.display_name} vacancies today. This permanent page will update automatically when new jobs arrive.</p>}
      </section>

      {nearby.length ? (
        <section aria-labelledby="nearby-jobs-heading" className="mt-8">
          <h2 id="nearby-jobs-heading" className="mb-3 text-2xl font-semibold text-gray-950">Approved nearby jobs</h2>
          <p className="mb-3 text-sm text-gray-600">These vacancies are in approved nearby locations; each listing keeps its actual location.</p>
          <QuickJobList jobs={withAttributes(nearby)} sectorFilterEnabled />
        </section>
      ) : null}
    </main>
  );
}
