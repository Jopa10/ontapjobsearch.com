import type { Metadata } from "next";
import Link from "next/link";
export const metadata: Metadata = { title: "AI Job Advert Watch | Ontap", description: "Dated snapshots of AI mentions in Ontap office-job adverts, separating workplace skills and tasks from recruitment notices.", alternates: { canonical: "https://www.ontapjobsearch.com/ai-at-work/ai-job-advert-watch" } };
const breadcrumbSchema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.ontapjobsearch.com/"}, {"@type": "ListItem", "position": 2, "name": "AI at work", "item": "https://www.ontapjobsearch.com/ai-at-work"}, {"@type": "ListItem", "position": 3, "name": "AI Job Advert Watch", "item": "https://www.ontapjobsearch.com/ai-at-work/ai-job-advert-watch"}]};
export default function AiJobAdvertWatchPage() {
 return <div className="mx-auto max-w-4xl px-5 py-8 sm:px-6 sm:py-12">
<nav aria-label="Breadcrumb" className="mb-7 text-sm text-slate-600"><ol className="flex flex-wrap items-center gap-x-2 gap-y-1"><li><Link href="/" className="underline-offset-4 hover:underline">Home</Link></li><li aria-hidden="true">›</li>
<li><Link href="/ai-at-work" className="underline-offset-4 hover:underline">AI at work</Link></li><li aria-hidden="true">›</li><li aria-current="page" className="font-medium text-slate-900">AI Job Advert Watch</li></ol></nav>
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }} />
<header className="mb-8"><h1 className="mb-4 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">AI Job Advert Watch</h1><p className="max-w-3xl text-lg leading-8 text-slate-700">What are employers actually asking for? Dated snapshots of AI in office-job adverts and what the wording means for you.</p></header>
<article className="rounded-2xl border border-blue-100 bg-white p-6 shadow-sm sm:p-8"><p className="mb-3 text-sm font-semibold text-blue-700">October 2026 · Snapshot taken 16 October</p><h2 className="mb-4 text-2xl font-bold text-slate-950">AI in office jobs: what employers are actually asking for</h2><p className="mb-5 leading-7 text-slate-700">We reviewed 3,500+ office-family adverts. Just 4% mentioned AI or a named tool, with marketing showing the clearest signal.</p><Link href="/ai-at-work/ai-job-advert-watch/october-2026" className="font-bold text-blue-700 underline underline-offset-4 hover:text-blue-900">Read the October report →</Link></article>
</div>;
}
