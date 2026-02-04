// app/jobs/search/[term]/page.tsx - Job search results page
import JobCard from '@/components/JobCard';
import Link from 'next/link';
import IndustryBrowser from '@/components/IndustryBrowser';

async function searchJobs(term: string) {
    try {
        const searchQuery = term === 'all' ? '' : term;
        const res = await fetch(
            `${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/api/jobs?search=${encodeURIComponent(searchQuery)}`,
            { cache: 'no-store' }
        );
        if (!res.ok) return { jobs: [], total: 0 };
        return await res.json();
    } catch (error) {
        console.error('Error searching jobs:', error);
        return { jobs: [], total: 0 };
    }
}

export default async function SearchResultsPage({ params }: { params: Promise<{ term: string }> }) {
    const { term } = await params;
    const { jobs, pagination } = await searchJobs(term);
    const searchTerm = decodeURIComponent(term);

    return (
        <div className="min-h-screen bg-gray-50 py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <nav className="text-sm text-gray-600 mb-4">
                        <Link href="/" className="hover:text-blue-600">
                            Home
                        </Link>
                        <span className="mx-2">/</span>
                        <span className="text-gray-900">Search Results</span>
                    </nav>
                    <h1 className="text-4xl font-bold text-gray-900">
                        {searchTerm === 'all' ? 'All Jobs' : `Results for "${searchTerm}"`}
                    </h1>
                    <p className="text-gray-600 mt-2">
                        {pagination?.total || 0} job{pagination?.total !== 1 ? 's' : ''} found
                    </p>
                </div>

                {/* Results */}
                {jobs.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {jobs.map((job: any) => (
                            <JobCard key={job.id} job={job} />
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-16">
                        <svg
                            className="w-16 h-16 text-gray-400 mx-auto mb-4"
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
                        <h2 className="text-2xl font-semibold text-gray-900 mb-2">No jobs found</h2>
                        <p className="text-gray-600 mb-6">
                            Try searching with different keywords or browse all jobs
                        </p>
                        <Link
                            href="/jobs/search/all"
                            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            Browse All Jobs
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );
}
