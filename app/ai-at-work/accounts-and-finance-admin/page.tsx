import type { Metadata } from "next";
import Link from "next/link";

const canonicalUrl = "https://www.ontapjobsearch.com/ai-at-work/accounts-and-finance-admin";
const publishedDate = "2026-11-11";

export const metadata: Metadata = {
  title: "AI for Accounts Assistants: Why Checking Matters | Ontap",
  description: "How accounts assistants can use AI for routine drafts and explanations while checking every figure and protecting financial data.",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    title: "AI is doing the data entry. Checking is your skill.",
    description: "Practical ways accounts assistants can use AI while keeping control of every figure.",
    type: "article",
    url: canonicalUrl,
    publishedTime: publishedDate,
  },
};

const structuredData = [
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: "https://www.ontapjobsearch.com/" },
      { "@type": "ListItem", position: 2, name: "AI at work", item: "https://www.ontapjobsearch.com/ai-at-work" },
      { "@type": "ListItem", position: 3, name: "Accounts and finance admin", item: canonicalUrl },
    ],
  },
  {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: "AI is doing the data entry. Checking is your skill.",
    datePublished: publishedDate,
    dateModified: publishedDate,
    mainEntityOfPage: canonicalUrl,
    author: { "@type": "Organization", name: "Ontap Job Search", url: "https://www.ontapjobsearch.com" },
    publisher: { "@id": "https://www.ontapjobsearch.com/#organization" },
    inLanguage: "en-GB",
  },
];

export default function AccountsAndFinanceAdminAiPage() {
  return (
    <div className="mx-auto max-w-4xl px-5 py-8 sm:px-6 sm:py-12">
      <nav aria-label="Breadcrumb" className="mb-7 text-sm text-slate-600">
        <ol className="flex flex-wrap items-center gap-x-2 gap-y-1">
          <li><Link href="/" className="underline-offset-4 hover:underline">Home</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li><Link href="/ai-at-work" className="underline-offset-4 hover:underline">AI at work</Link></li>
          <li aria-hidden="true">&gt;</li>
          <li aria-current="page" className="font-medium text-slate-900">Accounts and finance admin</li>
        </ol>
      </nav>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />

      <article>
        <header className="mb-9 border-b border-slate-200 pb-8">
          <div className="mb-5 flex flex-wrap items-center gap-3 text-sm">
            <span className="rounded-full bg-blue-100 px-3 py-1 font-bold text-blue-800">AI advice by job type</span>
            <time dateTime={publishedDate} className="text-slate-600">11 November 2026</time>
          </div>
          <h1 className="mb-5 max-w-3xl text-3xl font-extrabold tracking-tight text-slate-950 sm:text-5xl sm:leading-tight">
            AI is doing the data entry. Checking is your skill.
          </h1>
          <p className="max-w-3xl text-lg leading-8 text-slate-700">
            Accounts software is taking on more routine work. Here are practical ways to use AI for drafts and explanations while keeping responsibility for every figure.
          </p>
        </header>

        <div className="mb-9 grid gap-3 sm:grid-cols-3">
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">98%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">of practices in Xero&apos;s survey used AI for some day-to-day tasks</p>
          </div>
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">31%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">less time on those tasks, on average, according to the survey</p>
          </div>
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5">
            <p className="text-3xl font-extrabold text-blue-900">76%</p>
            <p className="mt-1 text-sm leading-6 text-slate-700">of surveyed practices said AI had influenced their hiring strategy</p>
          </div>
        </div>

        <div className="max-w-3xl">
          <p className="mb-5 leading-8 text-slate-700">
            Xero began rolling out automatic bank reconciliation powered by JAX in beta in November 2025. It can match high-confidence bank statement lines to transactions, with people able to review or adjust the result.
          </p>
          <p className="mb-8 leading-8 text-slate-700">
            Xero&apos;s 2025 research, commissioned with Cebr and Censuswide, surveyed 515 UK accountants and bookkeepers. It found that 98% of the practices surveyed used AI for some day-to-day tasks and that accountants completed those tasks in 31% less time on average. Three quarters of the practices said AI had influenced their hiring strategy; among those, 62% said they were hiring more non-accounting professionals. These are survey findings from research commissioned by an accounting software provider, not a prediction about every employer or job.
          </p>

          <h2 className="mb-4 text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">What this means for you</h2>
          <p className="mb-5 leading-8 text-slate-700">
            An approved AI tool may help draft an overdue-invoice reminder, put a variance into plain English, or explain an unfamiliar VAT term. That can save time, but its answer is a starting point, not the final check.
          </p>
          <p className="mb-8 leading-8 text-slate-700">
            AI can sound certain and still be wrong. In research commissioned by accounting software firm Dext, half of 500 surveyed UK accountants and bookkeepers said they were aware of businesses that had suffered financial losses linked to incorrect or misleading AI-generated advice. That records respondents&apos; awareness; it is not a measured error rate across all UK businesses. Tax and financial figures need to be checked against the ledger, invoice, source document or current HMRC guidance.
          </p>

          <h2 className="mb-5 text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">Three habits worth building</h2>
          <ol className="mb-10 grid gap-4">
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">01 · Draft and explain</p>
              <p className="leading-7 text-slate-700">Use AI to prepare a first draft or explain a process. Keep it away from confidential or personal financial information unless your employer has approved that tool and use.</p>
            </li>
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">02 · Check every figure</p>
              <p className="leading-7 text-slate-700">Trace numbers back to the ledger, invoice, bank record or other source. Follow your employer&apos;s process for checking tax and compliance information.</p>
            </li>
            <li className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="mb-2 text-sm font-bold uppercase tracking-wider text-blue-700">03 · Learn the tools you use</p>
              <p className="leading-7 text-slate-700">Build confidence with the accounting software in your workplace, such as Xero, Sage, QuickBooks or Dext, and learn where its AI features need a human review.</p>
            </li>
          </ol>

          <p className="mb-10 leading-8 text-slate-700">
            If it reflects work you have actually done, a CV example such as “reviewed and verified AI-assisted reconciliations” can show how you use new tools while taking responsibility for accuracy.
          </p>
        </div>

        <section className="mb-10 rounded-2xl bg-slate-950 px-6 py-7 text-white sm:flex sm:items-center sm:justify-between sm:gap-6">
          <div>
            <h2 className="text-xl font-bold">Looking for an accounts role?</h2>
            <p className="mt-2 text-slate-300">Browse current accounts assistant and finance administration vacancies on Ontap.</p>
          </div>
          <Link href="/browse-jobs" className="mt-5 inline-flex rounded-full bg-white px-5 py-3 font-bold text-slate-950 transition hover:bg-blue-100 sm:mt-0">
            Browse current jobs →
          </Link>
        </section>

        <section aria-labelledby="sources" className="border-t border-slate-200 pt-8">
          <h2 id="sources" className="mb-4 text-xl font-bold text-slate-950">Sources</h2>
          <ol className="space-y-3 pl-5 text-sm leading-6 text-slate-600">
            <li className="list-decimal">
              <a href="https://blog.xero.com/product-updates/automatic-bank-reconciliation-jax-beta/" target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-900">
                Xero: Automatic bank reconciliation powered by JAX (beta)
              </a>, 20 November 2025.
            </li>
            <li className="list-decimal">
              <a href="https://www.xero.com/us/media-releases/uk-accounting-sector-profits-surge-with-ai-adoption/" target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-900">
                Xero: Accounting sector profits surge with AI adoption
              </a>, 3 November 2025. Research by Cebr and Censuswide.
            </li>
            <li className="list-decimal">
              <a href="https://dext.com/en/news/uk-businesses-losing-money-to-chatgpt-style-tax-and-financial-advice-accountants-warn" target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 underline underline-offset-4 hover:text-blue-900">
                Dext: UK businesses losing money to ChatGPT-style tax and financial advice, accountants warn
              </a>, 18 December 2025. Research by Censuswide among 500 UK accountants and bookkeepers.
            </li>
          </ol>
        </section>
      </article>
    </div>
  );
}
