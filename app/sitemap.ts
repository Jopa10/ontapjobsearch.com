import { MetadataRoute } from 'next'
import { getJobPath, getPublishedJobs } from '@/lib/published-jobs'

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
  '/cumbria-south/support-worker',
  '/west-yorkshire/service-administrator-jobs',
  '/south-yorkshire/service-administrator-jobs',
  '/north-east/service-administrator-jobs',
  '/london/service-administrator-jobs',
  '/hampshire/service-administrator-jobs',
]

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date()

  const staticPages = routes.map((route) => ({
    url: `${siteUrl}${route}`,
    lastModified,
  }))

  const jobPages = getPublishedJobs().map((job) => ({
    url: `${siteUrl}${getJobPath(job.job_id)}`,
  }))

  return [...staticPages, ...jobPages]
}
