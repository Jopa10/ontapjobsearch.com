import { MetadataRoute } from 'next'
import {
  cityPageDefinitions,
  getCityPageJobs,
  isCityPageActive,
} from '@/lib/city-page-data'
import { getJobPath, getPublishedJobs } from '@/lib/published-jobs'
import { getPublishedDynamicSlices } from '@/lib/configured-job-slices'

const siteUrl = 'https://www.ontapjobsearch.com'

const baseRoutes = [
  '/',
  '/browse-jobs',
  '/about',
  '/ai-tips',
  '/contact',
  '/privacy-policy',
  '/terms-of-service',
  '/sector-switching',
  '/west-yorkshire/support-worker',
  '/south-yorkshire/support-worker',
  '/north-east/support-worker',
  '/sussex/support-worker',
  '/cumbria-south/support-worker',
  '/hampshire/support-worker',
  '/west-yorkshire/service-administrator-jobs',
  '/south-yorkshire/service-administrator-jobs',
  '/north-yorkshire/service-administrator-jobs',
  '/north-east/service-administrator-jobs',
  '/london/service-administrator-jobs',
  '/london/central-service-administrator-jobs',
  '/london/north-service-administrator-jobs',
  '/london/east-service-administrator-jobs',
  '/london/south-service-administrator-jobs',
  '/london/west-service-administrator-jobs',
  '/hampshire/service-administrator-jobs',
  '/coventry-warwickshire/service-administrator-jobs',
  '/surrey/service-administrator-jobs',
  '/kent/service-administrator-jobs',
  '/sussex/service-administrator-jobs',
]

export default function sitemap(): MetadataRoute.Sitemap {
  const jobs = getPublishedJobs()
  const activeCities = cityPageDefinitions
    .filter((definition) => isCityPageActive(definition))
    .map((definition) => ({ definition, jobs: getCityPageJobs(definition) }))
  const cityRoutes = activeCities.map(({ definition }) => definition.route)
  const configuredRoutes = getPublishedDynamicSlices().map((slice) => slice.route)
  const routes = [
    ...baseRoutes,
    ...cityRoutes.filter((route) => !baseRoutes.includes(route)),
    ...configuredRoutes.filter(
      (route) => !baseRoutes.includes(route) && !cityRoutes.includes(route)
    ),
  ]

  const dates = jobs
    .map((job) => dateFrom(job.posted_date))
    .filter((date): date is Date => Boolean(date))
  const allCityDates = activeCities.flatMap(({ jobs: cityJobs }) =>
    cityJobs
      .map((job) => dateFrom(typeof job.posted_date === 'string' ? job.posted_date : ''))
      .filter((date): date is Date => Boolean(date))
  )
  const latestJobDate = dates.length
    ? new Date(Math.max(...dates.map((date) => date.getTime())))
    : undefined

  const staticPages = routes.map((route) => {
    const city = activeCities.find(({ definition }) => definition.route === route)
    const routeDates = city
      ? city.jobs
          .map((job) => dateFrom(typeof job.posted_date === 'string' ? job.posted_date : ''))
          .filter((date): date is Date => Boolean(date))
      : route === '/' || route === '/browse-jobs'
        ? [...dates, ...allCityDates]
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
