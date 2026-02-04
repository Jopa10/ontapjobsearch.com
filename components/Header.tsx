// components/Header.tsx - Site header component
'use client';

import Link from 'next/link';
import Image from 'next/image';
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
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href={homeLink} className="flex items-center gap-2">
                        <Image
                            src="/assets/ontap-icon.svg"
                            alt="Ontap"
                            width={32}
                            height={32}
                            className="w-8 h-8"
                        />
                        <span className="text-xl font-bold text-gray-900 leading-tight">
                            Ontap Job Search
                        </span>
                    </Link>

                    {/* Navigation */}
                    <nav className="flex items-center gap-6">
                        {!isHome && (
                            <Link
                                href={homeLink}
                                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                            >
                                Home
                            </Link>
                        )}
                        {!isHome && !isAdmin && (
                            <Link
                                href="/jobs/search/all"
                                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                            >
                                Browse Jobs
                            </Link>
                        )}
                        {session && !isHome && !isAdmin && (
                            <Link
                                href="/admin/jobs"
                                className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
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
