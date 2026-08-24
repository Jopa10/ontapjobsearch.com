// app/layout.tsx – Root layout with providers

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import SessionProvider from '@/components/SessionProvider';
import DeploymentRefresh from '@/components/DeploymentRefresh';
import { Toaster } from 'react-hot-toast';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
});

const siteUrl = 'https://www.ontapjobsearch.com';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: 'Ontap Job Search – Find Your Perfect Job',
  description: 'Discover job opportunities tailored to your skills and ambitions on Ontap Job Search.',
  icons: {
    icon: [
      {
        url: '/assets/ontap-icon-v2.svg',
        type: 'image/svg+xml',
      },
    ],
    shortcut: '/assets/ontap-icon-v2.svg',
    apple: '/assets/ontap-icon-v2.svg',
  },
};

const organizationStructuredData = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': `${siteUrl}/#organization`,
  name: 'Ontap Job Search',
  legalName: 'Ontap Learning Ltd',
  url: siteUrl,
  logo: {
    '@type': 'ImageObject',
    url: `${siteUrl}/assets/ontap-icon-v2.svg`,
  },
  email: 'john@ontapcreative.co.uk',
  contactPoint: {
    '@type': 'ContactPoint',
    contactType: 'general enquiries',
    email: 'john@ontapcreative.co.uk',
    availableLanguage: 'English',
  },
};

const websiteStructuredData = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': `${siteUrl}/#website`,
  name: 'Ontap Job Search',
  url: siteUrl,
  publisher: {
    '@id': `${siteUrl}/#organization`,
  },
  inLanguage: 'en-GB',
};

function deploymentVersion() {
  return (
    process.env.VERCEL_GIT_COMMIT_SHA ||
    process.env.VERCEL_URL ||
    null
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta
          name="impact-site-verification"
          {...{ value: '04d049d4-d81c-4ec1-8457-5d8d8bc86487' }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organizationStructuredData),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(websiteStructuredData),
          }}
        />
        <script
          async
          src="https://www.googletagmanager.com/gtag/js?id=G-XLJL0PXJ0V"
        ></script>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-XLJL0PXJ0V');
            `,
          }}
        />
      </head>
      <body className={`${inter.className} antialiased flex flex-col min-h-screen`} suppressHydrationWarning>
        <Toaster position="top-right" />
        <DeploymentRefresh deploymentVersion={deploymentVersion()} />
        <SessionProvider>
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
        </SessionProvider>
      </body>
    </html>
  );
}
