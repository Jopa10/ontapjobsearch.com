import type { Metadata } from "next";
import Link from "next/link";

const canonicalUrl = "https://www.ontapjobsearch.com/ai-at-work";

export const metadata: Metadata = {
  title: "AI at Work: Practical Tips and Course Reviews | Ontap",
  description: "Practical AI help for everyday office work: example prompts, first-hand beginner course reviews and reports on AI in job adverts.",
  alternates: { canonical: canonicalUrl },
};

const breadcrumbSchema = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    { "@type": "ListItem", position: 1, name: "Home", item: "https://www.ontapjobsearch.com/" },
    { "@type": "ListItem", position: 2, name: "AI at work", item: canonicalUrl },
  ],
};

export default function AiAtWorkPage() {
  return (
    <div className="mx-auto max-w-4xl px-5 py-8 sm:px-6 sm:py-12">
      <nav aria-label="Breadcrumb" className="mb-7 text-sm text-slate-600">
        <ol className="flex flex-wrap items-center gap-2">
          <li><Link href="/" className="underline-offset-4 hover:underline">Home</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li aria-current="page" className="font-medium text-slate-900">AI at work</li>
        </ol>
      </nav>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }} />
      <header className="mb-8">
        <p className="mb-3 text-sm font-bold uppercase tracking-wider text-blue-700">Ontap AI at work</p>
        <h1 className="mb-4 text-3xl font-extrabold tracking-tight text-slate-950 sm:text-4xl">Practical AI help for everyday office work</h1>
        <p className="max-w-2xl text-lg leading-8 text-slate-700">
          Useful tips and honest course reviews to help you use AI with confidence—in your current job or your next one.
        </p>
      </header>

      <div className="grid gap-5 sm:grid-cols-2">
        <article className="flex flex-col overflow-hidden rounded-2xl border border-blue-100 bg-white shadow-sm">
          <p className="bg-blue-50 px-6 py-4 text-sm font-bold uppercase tracking-wider text-blue-700">Practical help</p>
          <div className="flex flex-1 flex-col p-6">
            <h2 className="mb-3 text-2xl font-bold text-slate-950">Start with a task you already do</h2>
            <p className="mb-4 leading-7 text-slate-700">Four straightforward ways to try AI, with example prompts you can adapt.</p>
            <ul className="mb-6 list-disc space-y-2 pl-5 text-slate-700">
              <li>Turn meeting notes into actions</li>
              <li>Draft a clearer email</li>
              <li>Simplify a document</li>
              <li>Improve a customer reply</li>
            </ul>
            <Link href="/ai-tips" className="mt-auto font-bold text-blue-700 underline underline-offset-4 hover:text-blue-900">Read the AI tips →</Link>
          </div>
        </article>
        <article className="flex flex-col overflow-hidden rounded-2xl border border-blue-100 bg-white shadow-sm">
          <p className="bg-blue-50 px-6 py-4 text-sm font-bold uppercase tracking-wider text-blue-700">First-hand reviews</p>
          <div className="flex flex-1 flex-col p-6">
            <h2 className="mb-3 text-2xl font-bold text-slate-950">Which AI courses are useful for work?</h2>
            <p className="mb-4 leading-7 text-slate-700">What the courses teach, how practical they feel and who will get the most from them.</p>
            <ul className="mb-6 list-disc space-y-2 pl-5 text-slate-700">
              <li>Elements of AI</li>
              <li>OpenAI Academy: AI Foundations</li>
            </ul>
            <Link href="/ai-course-reviews" className="mt-auto font-bold text-blue-700 underline underline-offset-4 hover:text-blue-900">Read the course reviews →</Link>
          </div>
        </article>
      </div>

      <section aria-labelledby="ai-job-advert-watch" className="mt-8 border-b border-slate-200 py-6">
        <p className="mb-3 text-sm font-semibold text-blue-700">AI Job Advert Watch · October 2026</p>
        <h2 id="ai-job-advert-watch" className="mb-3 text-2xl font-bold text-slate-950">AI in office jobs: what employers are actually asking for</h2>
        <p className="mb-5 max-w-3xl leading-7 text-slate-700">We reviewed 3,500+ office-family adverts. Just 4% mentioned AI or a named tool, with marketing showing the clearest signal.</p>
        <Link href="/ai-at-work/ai-job-advert-watch/october-2026" className="font-bold text-blue-700 underline underline-offset-4 hover:text-blue-900">Read the October report →</Link>
      </section>

      <aside className="mt-6 flex flex-wrap items-center justify-between gap-4">
        <p className="text-slate-700">Looking for your next office role?</p>
        <Link href="/browse-jobs" className="font-bold text-blue-700 underline underline-offset-4 hover:text-blue-900">Browse current jobs →</Link>
      </aside>
    </div>
  );
}
