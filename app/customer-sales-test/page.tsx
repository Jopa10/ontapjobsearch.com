import type { Metadata } from "next";
import Link from "next/link";
import {
  CUSTOMER_SALES_TEST_SLICES,
  getCustomerSalesTestSlice,
} from "@/lib/customer-sales-test";

export const metadata: Metadata = {
  title: "Customer Sales Test Hub | Ontap Job Search",
  description: "Branch-only inspection hub for the proposed Customer Sales / Sales Advisor family.",
  robots: { index: false, follow: false },
};

export default function Page() {
  const slices = CUSTOMER_SALES_TEST_SLICES.map((slice) => getCustomerSalesTestSlice(slice.slug)).filter(Boolean);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <section className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
        <p className="text-xs font-bold uppercase tracking-wide text-amber-800">Test branch only · noindex</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-gray-900">Customer Sales / Sales Advisor test</h1>
        <p className="mt-3 max-w-3xl text-gray-700">
          Five first-wave slices from the earlier broad discovery. This test is for inspecting the real page mix,
          not re-proving the family from scratch. Genuine overlap with Service Admin is allowed.
        </p>
      </section>

      <section className="mt-7 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {slices.map((slice) => {
          if (!slice) return null;
          return (
            <Link
              key={slice.slug}
              href={`/customer-sales-test/${slice.slug}`}
              className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-blue-300 hover:shadow-md"
            >
              <h2 className="text-xl font-semibold text-gray-900">{slice.label}</h2>
              <p className="mt-2 text-3xl font-bold text-blue-700">{slice.jobs.length}</p>
              <p className="text-sm text-gray-500">broad candidate job{slice.jobs.length === 1 ? "" : "s"}</p>
              <p className="mt-4 text-sm font-semibold text-blue-700">Inspect slice →</p>
            </Link>
          );
        })}
      </section>

      <section className="mt-8 rounded-xl border border-gray-200 bg-gray-50 p-5 text-sm leading-6 text-gray-700">
        <strong>Broad family rule:</strong> office/contact-centre/home/hybrid jobs where the candidate genuinely sells,
        converts, retains or renews customers. Sales Executive, Sales Advisor, telesales, internal/inside sales,
        retention/renewals and suitable business-development-executive roles are included; customer-service/contact-centre
        roles are included when the advert contains genuine sales evidence. A role is not excluded just because it also fits Service Admin.
      </section>
    </main>
  );
}
