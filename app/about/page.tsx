import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'About Ontap and How We Select Jobs | Ontap Job Search',
  description:
    'Learn how Ontap curates current UK vacancies by role and region, removes expired jobs and links jobseekers directly to employers and original job providers.',
}

export default function AboutPage() {
  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-semibold mb-6">About Ontap</h1>

      <p className="mb-5">
        Ontap is a UK job-search service that curates current vacancies by
        occupation and region. We focus on making it easier for jobseekers to
        find relevant roles without working through large numbers of unsuitable
        results.
      </p>

      <p className="mb-8">
        Jobs are checked regularly, irrelevant roles are filtered out and
        expired vacancies are removed from our live job pages. No signup is
        required. When you choose to apply, Ontap sends you directly to the
        employer, recruitment agency or original job provider handling the
        application.
      </p>

      <h2 className="text-2xl font-semibold mb-4">The jobs we cover</h2>

      <p className="mb-5">
        Ontap currently specialises in admin, office support, customer service
        and support-worker vacancies. Coverage is organised into clear regional
        pages so jobseekers can browse roles that are relevant to both the work
        they want and the area in which they are looking.
      </p>

      <p className="mb-8">
        Current coverage includes parts of London, the North East, Yorkshire,
        Cumbria, Hampshire, Surrey, Kent and Sussex. The exact combination of
        occupations and locations available changes as Ontap expands and as
        suitable live vacancies become available. Our{' '}
        <Link href="/browse-jobs" className="underline hover:no-underline">
          Browse Jobs
        </Link>{' '}
        page shows the job areas currently live.
      </p>

      <h2 className="text-2xl font-semibold mb-4">How we select jobs</h2>

      <p className="mb-5">
        Ontap reviews vacancies against the occupation and location of each job
        page. Roles that are clearly outside that page&apos;s purpose are not
        included. We also check for duplicate vacancies and remove jobs when
        they are no longer current.
      </p>

      <p className="mb-5">
        Vacancies may come directly from employers, through recruitment
        agencies, or from established public-sector and charity-sector job
        providers. Whatever the source, the aim is the same: to show suitable,
        current opportunities in a simple and consistent format while keeping
        the original application route clear.
      </p>

      <p className="mb-8">
        Ontap does not employ candidates, make hiring decisions or accept job
        applications. Questions about a vacancy or application should be sent
        to the employer or job provider shown on the job listing.
      </p>

      <h2 className="text-2xl font-semibold mb-4">Who operates Ontap</h2>

      <p className="mb-5">
        Ontap Job Search is operated by Ontap Learning Ltd, a UK-registered
        company.
      </p>

      <p>
        For general enquiries, visit our{' '}
        <Link href="/contact" className="underline hover:no-underline">
          Contact page
        </Link>
        .
      </p>
    </main>
  )
}
