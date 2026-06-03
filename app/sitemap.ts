import { MetadataRoute } from 'next'

const siteUrl = 'https://www.ontapjobsearch.com'

const routes = [
  '/',
  '/west-yorkshire/support-worker',
  '/south-yorkshire/support-worker',
  '/west-yorkshire/service-administrator-jobs',
  '/south-yorkshire/service-administrator-jobs',
]

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date()

  return routes.map((route) => ({
    url: `${siteUrl}${route}`,
    lastModified,
  }))
}
