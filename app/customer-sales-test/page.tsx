import type { Metadata } from "next";
import Link from "next/link";
import {
  CUSTOMER_SALES_TEST_SLICES,
  getCustomerSalesTestSlice,
} from "@/lib/customer-sales-test";

export const metadata: Metadata = {
  title: "Customer Sales Proof Test | Ontap Job Search",
  description: "Branch-only inspection hub for the proposed Customer Sales / Sales Advisor family.",
  robots: { index: false, follow: false },
};

export default function Page() {
  const slices = CUSTOMER_SALES_TEST_SLICES.map((slice) => getCustomerSalesTestSlice(slice.slug)).filter(Boolean);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
        <p className="text-xs font-bold uppercase tracking-wide text-amber-800">Governed proof test · branch only · noindex</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-gray-900">Customer Sales / Sales Advisor proof regions</h1>
        <p className="mt-3 max-w-3xl text-gray-700">
          Hampshire, Manchester & Salford and West Yorkshire only. These pages are for inspecting the actual job mix,
          employer concentration, duplicate/campaign effects and page quality before any LIVE decision. Genuine overlap
          with Service Admin is allowed and is not an exclusion reason.
        </p>
      </section>

      <section className="mt-7 grid gap-4 md:grid-cols-3">
        {slices.map((slice) => {
          if (!slice) return null;
          const topEmployer = slice.stats.topEmployers[0];
          return (
            <Link
              key={slice.slug}
              href={`/customer-sales-test/${slice.slug}`}
              className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-blue-300 hover:shadow-md"
            >
              <h2 className="text-xl font-semibold text-gray-900">{slice.label}</h2>
              <p className="mt-2 text-3xl font-bold text-blue-700">{slice.jobs.length}</p>
              <p className="text-sm text-gray-500">candidate job{slice.jobs.length === 1 ? "" : "s"}</p>
              <dl className="mt-4 space-y-1 text-sm text-gray-600">
                <div className="flex justify-between gap-3">
                  <dt>Employers</dt>
                  <dd className="font-semibold text-gray-900">{slice.stats.employerCount}</dd>
                </div>
                <div className="flex justify-between gap-3">
                  <dt>Duplicate groups</dt>
                  <dd className="font-semibold text-gray-900">{slice.stats.duplicateGroups.length}</dd>
                </div>
                {topEmployer ? (
                  <div className="pt-2 text-xs text-gray-500">
                    Top employer: {topEmployer.name} ({topEmployer.count}/{slice.jobs.length})
                  </div>
                ) : null}
              </dl>
              <p className="mt-4 text-sm font-semibold text-blue-700">Inspect slice →</p>
            </Link>
          );
        })}
      </section>

      <section className="mt-8 rounded-xl border border-gray-200 bg-gray-50 p-5 text-sm leading-6 text-gray-700">
        <strong>Proof family rule:</strong> office/contact-centre/home/hybrid jobs where the candidate genuinely sells,
        converts, retains or renews customers. Direct sales-advisor/executive, telesales, internal/inside sales,
        retention/renewals and suitable business-development-executive roles are candidates; customer-service/contact-centre
        roles need genuine sales evidence. Generic account roles only re-enter when the advert shows strong sales plus
        office/digital evidence. Field, senior-management, technical, retail/showroom and sales-admin/support roles are excluded.
      </section>
    </main>
  );
}
