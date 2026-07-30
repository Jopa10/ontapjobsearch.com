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
  '/hampshire/support-worker',
  '/west-yorkshire/service-administrator-jobs',
  '/south-yorkshire/service-administrator-jobs',
  '/north-east/service-administrator-jobs',
  '/london/service-administrator-jobs',
  '/london/outer-service-administrator-jobs',
  '/hampshire/service-administrator-jobs',
  '/surrey/service-administrator-jobs',
  '/kent/service-administrator-jobs',
]

export default function sitemap(): MetadataRoute.Sitemap {
  const jobs = getPublishedJobs()
  const dates = jobs
    .map((job) => dateFrom(job.posted_date))
    .filter((date): date is Date => Boolean(date))
  const latestJobDate = dates.length
    ? new Date(Math.max(...dates.map((date) => date.getTime())))
    : undefined

  const staticPages = routes.map((route) => {
    const routeDates =
      route === '/' || route === '/browse-jobs'
        ? dates
        : jobs
            .filter((job) => job.slice_path === route)
            .map((job) => dateFrom(job.posted_date))
            .filter((date): date is Date => Boolean(date))
    const lastModified = routeDates.length
      ? new Date(Math.max(...routeDates.map((date) => date.getTime())))
      : route === '/' || route === '/browse-jobs'
        ? latestJobDate
        : undefined

    return {
      url: `${siteUrl}${route}`,
      ...(lastModified ? { lastModified } : {}),
    }
  })

  const jobPages = jobs.map((job) => {
    const lastModified = dateFrom(job.posted_date)
    return {
      url: `${siteUrl}${getJobPath(job.job_id)}`,
      ...(lastModified ? { lastModified } : {}),
    }
  })

  return [...staticPages, ...jobPages]
}

function dateFrom(value: string): Date | undefined {
  if (!/^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(value)) return undefined
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? undefined : date
}
