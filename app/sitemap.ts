import { MetadataRoute } from 'next'

const siteUrl = 'https://www.ontapjobsearch.com'

const routes = [
  '/',
  '/browse-jobs',
  '/contact',
  '/privacy-policy',
  '/terms-of-service',
  '/west-yorkshire/support-worker',
  '/south-yorkshire/support-worker',
  '/north-east/support-worker',
  '/sussex/support-worker',
  '/west-yorkshire/service-administrator-jobs',
  '/south-yorkshire/service-administrator-jobs',
  '/north-east/service-administrator-jobs',
  '/london/service-administrator-jobs',
]

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date()

  return routes.map((route) => ({
    url: `${siteUrl}${route}`,
    lastModified,
  }))
}
