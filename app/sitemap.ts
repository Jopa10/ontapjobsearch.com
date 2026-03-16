import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://www.ontapjobsearch.com',
      lastModified: new Date(),
    },
    {
      url: 'https://www.ontapjobsearch.com/leeds/nhs-admin-jobs',
      lastModified: new Date(),
    }
  ]
}
