import type { NextConfig } from "next";

// Deployment touch: rebuild production from the latest published job and city-page state.
const nextConfig: NextConfig = {
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
