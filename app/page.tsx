export default function Page() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Yorkshire Support Worker Jobs
      </h1>

      <p className="text-lg text-gray-700 mb-6">
        Focused listings across West and South Yorkshire. More regions coming soon.
      </p>

      <a
        href="/jobs/search/all"
        className="inline-block text-lg font-medium underline underline-offset-4"
      >
        Browse jobs →
      </a>
    </main>
  );
}
