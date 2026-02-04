// components/Footer.tsx - Site footer component
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Footer() {
    const pathname = usePathname();
    const isAdmin = pathname?.startsWith('/admin');
    const currentYear = new Date().getFullYear();

    if (isAdmin) {
        return null;
    }

    return (
        <footer className="bg-gray-900 text-gray-300 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Company Info */}
                    <div className="col-span-1 md:col-span-2">
                        <h3 className="text-white text-lg font-bold mb-4">Ontap Job Search</h3>
                        <p className="text-sm mb-4">
                            Your trusted platform for matching the perfect job opportunities with talented
                            professionals.
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="text-white text-sm font-semibold mb-4 uppercase tracking-wider">
                            Quick Links
                        </h4>
                        <ul className="space-y-2">
                            <li>
                                <Link href="/" className="text-sm hover:text-white transition-colors">
                                    Home
                                </Link>
                            </li>
                            <li>
                                <Link href="/jobs/search/all" className="text-sm hover:text-white transition-colors">
                                    Browse Jobs
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Legal */}
                    <div>
                        <h4 className="text-white text-sm font-semibold mb-4 uppercase tracking-wider">
                            Legal
                        </h4>
                        <ul className="space-y-2">
                            <li>
                                <Link href="#" className="text-sm hover:text-white transition-colors">
                                    Privacy Policy
                                </Link>
                            </li>
                            <li>
                                <Link href="#" className="text-sm hover:text-white transition-colors">
                                    Terms of Service
                                </Link>
                            </li>
                            <li>
                                <Link href="#" className="text-sm hover:text-white transition-colors">
                                    Contact Us
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Copyright */}
                <div className="mt-8 pt-8 border-t border-gray-800 text-center">
                    <p className="text-sm">
                        © {currentYear} Ontap Job Search. All rights reserved.
                    </p>
                </div>
            </div>
        </footer>
    );
}
