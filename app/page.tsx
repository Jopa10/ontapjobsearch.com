export default function Page() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Yorkshire Support Worker Jobs
      </h1>

      <p className="text-lg text-gray-700 mb-3">
        Live support worker roles across West and South Yorkshire.
      </p>

      <p className="text-sm text-gray-600 mb-6">
        Updated daily • Apply directly on employer websites • No signup required
      </p>

      <a
        href="/jobs/all"
        className="inline-block text-lg font-medium underline underline-offset-4 mb-8"
      >
        Browse jobs →
      </a>

      <section className="grid gap-4">
        <a
          href="/west-yorkshire/support-worker"
          className="block rounded-xl border border-gray-200 p-5 hover:border-blue-300 hover:bg-blue-50"
        >
          <h2 className="text-xl font-semibold mb-1">
            West Yorkshire Support Worker Jobs
          </h2>
          <p className="text-gray-600">
            Current Leeds and West Yorkshire support worker roles, updated daily.
          </p>
        </a>

        <a
          href="/south-yorkshire/support-worker"
          className="block rounded-xl border border-gray-200 p-5 hover:border-blue-300 hover:bg-blue-50"
        >
          <h2 className="text-xl font-semibold mb-1">
            South Yorkshire Support Worker Jobs
          </h2>
          <p className="text-gray-600">
            Current Sheffield and South Yorkshire support worker roles, updated daily.
          </p>
        </a>
      </section>
    </main>
  );
}
