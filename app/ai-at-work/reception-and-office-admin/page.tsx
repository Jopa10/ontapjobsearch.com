import type { Metadata } from "next";
import Link from "next/link";

const canonicalUrl = "https://www.ontapjobsearch.com/ai-at-work/reception-and-office-admin";

export const metadata: Metadata = {
  title: "AI for Receptionists and Office Administrators | Ontap",
  description: "Practical ways receptionists and office administrators can use AI for emails, meeting notes and everyday tasks, with sensible workplace safeguards.",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    title: "Your front desk, with AI: what is changing and what to try",
    description: "Four practical AI tasks for reception and office admin, plus the safeguards that matter.",
    type: "article",
    url: canonicalUrl,
    publishedTime: "2026-11-03",
  },
};

const structuredData = [
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: "https://www.ontapjobsearch.com/" },
      { "@type": "ListItem", position: 2, name: "AI at work", item: "https://www.ontapjobsearch.com/ai-at-work" },
      { "@type": "ListItem", position: 3, name: "Reception and office admin", item: canonicalUrl },
    ],
  },
  {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: "Your front desk, with AI: what is changing and what to try this week",
    datePublished: "2026-11-03",
    dateModified: "2026-11-03",
    mainEntityOfPage: canonicalUrl,
    author: { "@type": "Organization", name: "Ontap Job Search", url: "https://www.ontapjobsearch.com" },
    publisher: { "@id": "https://www.ontapjobsearch.com/#organization" },
    inLanguage: "en-GB",
  },
];

export default function ReceptionAndOfficeAdminAiPage() {
  return (
    <div className="mx-auto max-w-4xl px-5 py-8 sm:px-6 sm:py-12">
      <nav aria-label="Breadcrumb" className="mb-7 text-sm text-slate-600">
        <ol className="flex flex-wrap items-center gap-x-2 gap-y-1">
          <li><Link href="/" className="underline-offset-4 hover:underline">Home</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li><Link href="/ai-at-work" className="underline-offset-4 hover:underline">AI at work</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li aria-current="page" className="font-medium text-slate-900">Reception and office admin</li>
        </ol>
      </nav>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />

      <article>
        <header className="mb-9 border-b border-slate-200 pb-8">
          <div className="mb-5 flex flex-wrap items-center gap-3 text-sm">
            <span className="rounded-full bg-blue-100 px-3 py-1 font-bold text-blue-800">AI advice by job type</span>
            <time dateTime="2026-11-03" className="text-slate-600">3 November 2026</time>
          </div>
          <h1 className="mb-5 max-w-3xl text-3xl font-extrabold tracking-tight text-slate-950 sm:text-5xl sm:leading-tight">
            Your front desk, with AI: what is changing and what to try this week
          </h1>
          <p className="max-w-3xl text-lg leading-8 text-slate-700">
            AI is not just for technical jobs. Used carefully, it can help receptionists and office administrators handle familiar tasks more quickly while keeping human judgement firmly in charge.
          </p>
        </header>

        <div className="mb-9 grid gap-3 sm:grid-cols-3">
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">56%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">of UK workers used AI at work in the past year</p>
          </div>
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">35%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">of non-managers have used AI at work</p>
          </div>
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">44%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">of AI users report a heavier workload</p>
          </div>
        </div>

        <div className="max-w-3xl">
          <p className="mb-5 leading-8 text-slate-700">
            PwC&apos;s latest UK survey found that 56% of workers used AI at work in the past year, and 19% now use it daily, up from 15% in 2025. The gap by seniority is large: 85% of senior executives and 73% of managers have used AI at work, compared with 35% of non-managers.
          </p>
          <p className="mb-8 leading-8 text-slate-700">
            If you work in admin or reception, that gap is an opportunity. Knowing how to use AI appropriately is becoming a useful point of difference, especially when you can explain where it saves time and where you still need to check the result.
          </p>

          <h2 className="mb-5 text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">Four things to try this week</h2>
          <ol className="mb-10 grid gap-4 sm:grid-cols-2">
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">01 · Email threads</p>
              <p className="leading-7 text-slate-700">Paste a non-confidential email thread and ask for a three-line summary plus a clear list of actions.</p>
            </li>
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">02 · Difficult replies</p>
              <p className="leading-7 text-slate-700">Ask for a polite first draft, then edit it into your own voice before sending it.</p>
            </li>
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">03 · Meeting notes</p>
              <p className="leading-7 text-slate-700">Turn rough notes into tidy minutes with decisions, actions, owners and deadlines.</p>
            </li>
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">04 · How-to guides</p>
              <p className="leading-7 text-slate-700">Create a one-page guide for a repeated task such as room booking or visitor sign-in.</p>
            </li>
          </ol>

          <section aria-labelledby="two-cautions" className="mb-10 rounded-2xl border border-amber-200 bg-amber-50 p-6 sm:p-7">
            <p className="mb-2 text-sm font-bold uppercase tracking-wider text-amber-800">Use it safely</p>
            <h2 id="two-cautions" className="mb-4 text-2xl font-bold text-slate-950">Two cautions</h2>
            <ul className="space-y-3 pl-5 text-slate-700">
              <li className="list-disc leading-7">Do not put confidential, personal or customer information into a public AI tool unless your employer has explicitly approved that use.</li>
              <li className="list-disc leading-7">Check your employer&apos;s AI policy first. Deloitte found that nearly a third of UK GenAI users use it without their employer&apos;s knowledge.</li>
            </ul>
          </section>

          <p className="mb-10 leading-8 text-slate-700">
            One more thing is worth knowing: PwC found that 44% of AI users report a heavier workload. AI does not remove work by itself. It helps most when you deliberately choose which tasks to hand over, check the output and keep responsibility for the final result.
          </p>
        </div>

        <section className="mb-10 rounded-2xl bg-slate-950 px-6 py-7 text-white sm:flex sm:items-center sm:justify-between sm:gap-6">
          <div>
            <h2 className="text-xl font-bold">Looking for your next admin role?</h2>
            <p className="mt-2 text-slate-300">Browse current receptionist, administrator and office-support vacancies.</p>
          </div>
          <Link href="/browse-jobs" className="mt-5 inline-flex rounded-full bg-white px-5 py-3 font-bold text-slate-950 transition hover:bg-blue-100 sm:mt-0">
            Browse current jobs →
          </Link>
        </section>

        <section aria-labelledby="sources" className="border-t border-slate-200 pt-8">
          <h2 id="sources" className="mb-4 text-xl font-bold text-slate-950">Sources</h2>
          <ol className="space-y-3 pl-5 text-sm leading-6 text-slate-600">
            <li className="list-decimal">
              <a href="https://www.pwc.co.uk/press-room/press-releases/research-commentary/2026/one-in-five-uk-employees-are-now-using-ai-everyday-at-work-but-4.html" target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-900">
                PwC UK Hopes and Fears Survey
              </a>, 2,023 UK workers, 1 October 2026.
            </li>
            <li className="list-decimal">
              <a href="https://www.deloitte.com/uk/en/about/press-room/british-workers-spend-one-billion-pounds-of-their-own-money-on-gen-ai-for-work.html" target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-900">
                Deloitte UK GenAI Workforce Survey
              </a>, 25,000 UK workers, 16 September 2026.
            </li>
          </ol>
        </section>
      </article>
    </div>
  );
}
