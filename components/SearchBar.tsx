// components/SearchBar.tsx - Search bar component for home page
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from './Button';

export default function SearchBar() {
    const [searchTerm, setSearchTerm] = useState('');
    const router = useRouter();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchTerm.trim()) {
            router.push(`/jobs/search/${encodeURIComponent(searchTerm.trim())}`);
        }
    };

    return (
        <form onSubmit={handleSearch} className="w-full max-w-4xl mx-auto relative z-10">
            <div className="flex gap-2 bg-white rounded-lg shadow-lg p-2">
                <div className="flex-1 relative">
                    <svg
                        className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                    </svg>
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search job title, company, location..."
                        className="w-full pl-12 pr-4 py-3 text-lg rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                    />
                </div>
                <Button
                    type="submit"
                    size="lg"
                    className="px-8"
                    disabled={!searchTerm.trim()}
                >
                    Search Jobs
                </Button>
            </div>
        </form>
    );
}
