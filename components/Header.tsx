// components/Header.tsx - Site header component
'use client';

import Link from 'next/link';
import { useSession } from 'next-auth/react';

import { usePathname } from 'next/navigation';

export default function Header() {
    const { data: session } = useSession();
    const pathname = usePathname();
    const isAdmin = pathname?.startsWith('/admin');
    const isHome = pathname === '/';

    if (isAdmin) {
        return null;
    }

    const homeLink = isAdmin ? '/admin/jobs' : '/';

    return (
        <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex min-h-16 items-center justify-between gap-3 py-3">
                    {/* Logo */}
                    <Link href={homeLink} className="shrink-0">
                        <div className="leading-tight">
  <div className="text-[19px] font-medium tracking-tight text-gray-900">
    Ontap Job Search
  </div>
  <div className="mt-1 text-[11px] text-slate-500">
    Updated daily • No sign-up
  </div>
</div>
                    </Link>

                    {/* Navigation */}
                    <nav className="ml-auto flex flex-wrap items-center justify-end gap-x-4 gap-y-1 text-sm sm:gap-x-6">
                        <Link
                            href="/ai-at-work"
                            className={`text-gray-700 hover:text-blue-600 font-normal transition-colors ${isHome ? '' : 'hidden sm:inline'}`}
                        >
                            AI at work
                        </Link>
                        {!isHome && (
                            <Link
                               href="/"
                                className="text-gray-700 hover:text-blue-600 font-normal transition-colors"
                            >
                                Home
                            </Link>
                        )}
                        {!isAdmin && (
                            <Link
                                href="/browse-jobs"
                                className={`text-gray-700 hover:text-blue-600 font-normal transition-colors ${isHome ? '' : 'hidden sm:inline'}`}
                            >
                                Browse Jobs
                            </Link>
                        )}
                        {session && !isHome && !isAdmin && (
                            <Link
                                href="/admin/jobs"
                                className="text-gray-700 hover:text-blue-600 font-normal transition-colors"
                            >
                                Admin
                            </Link>
                        )}
                    </nav>
                </div>
            </div>
        </header>
    );
}
