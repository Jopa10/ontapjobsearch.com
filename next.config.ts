import type { NextConfig } from "next";

// Deployment touch: rebuild production from the latest city homepage visibility state.
const nextConfig: NextConfig = {
  outputFileTracingExcludes: {
    // Archived feed and editorial pipeline artifacts are not read by public
    // job-detail or configured regional listing routes.
    "/jobs/*": [
      "./pipeline/input-jobg8-archive/**/*",
      "./pipeline/manifests/external/**/*",
      "./pipeline/reviews/external/**/*",
      "./pipeline/reports-daily/decision-report-admin-service.csv",
      "./pipeline/reports-daily/decision-report-support-worker.csv",
    ],
    "/job-search/*": [
      "./pipeline/input-jobg8-archive/**/*",
      "./pipeline/manifests/external/**/*",
      "./pipeline/reviews/external/**/*",
      "./pipeline/reports-daily/decision-report-admin-service.csv",
      "./pipeline/reports-daily/decision-report-support-worker.csv",
    ],
    "/job-search/*/*": [
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
