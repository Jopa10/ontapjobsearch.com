import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://www.ontapjobsearch.com/',
      lastModified: new Date(),
    },
    {
      url: 'https://www.ontapjobsearch.com/west-yorkshire/support-worker',
      lastModified: new Date(),
    },
    {
      url: 'https://www.ontapjobsearch.com/south-yorkshire/support-worker',
      lastModified: new Date(),
    }
  ]
}
