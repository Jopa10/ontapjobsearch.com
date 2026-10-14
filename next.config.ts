import type { NextConfig } from "next";

// Keep pipeline-only archives and reports out of deployed route traces. These
// files are consumed by GitHub Actions workflows, not by the site's runtime.
const nextConfig: NextConfig = {
  outputFileTracingExcludes: {
    "/*": [
      "./pipeline/input-jobg8-archive/**/*",
      "./pipeline/manifests/external/**/*",
      "./pipeline/reviews/external/**/*",
      "./pipeline/reports-daily/decision-report-admin-service.csv",
      "./pipeline/reports-daily/decision-report-support-worker.csv",
    ],
  },

  async redirects() {
    return [
      {
        source: "/jobs/all",
        destination: "https://www.ontapjobsearch.com/browse-jobs",
        permanent: true,
      },
      {
        source: "/:path*",
        has: [{ type: "host", value: "ontapjobsearch.com" }],
        destination: "https://www.ontapjobsearch.com/:path*",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
