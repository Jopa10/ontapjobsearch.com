// app/jobs/[id]/page.tsx - Job detail page with comprehensive sections
'use client';

import { use, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import JobCard from '@/components/JobCard';
import Button from '@/components/Button';
import toast from 'react-hot-toast';

export default function JobDetailPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const [job, setJob] = useState<any>(null);
    const [similarJobs, setSimilarJobs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        async function fetchJob() {
            try {
                const [jobRes, similarRes] = await Promise.all([
                    fetch(`/api/jobs/${id}`),
                    fetch(`/api/jobs/similar/${id}`),
                ]);

                if (jobRes.ok) {
                    setJob(await jobRes.json());
                } else {
                    // Handle 404 or other errors
                    setJob(null);
                }
                if (similarRes.ok) {
                    setSimilarJobs(await similarRes.json());
                }
            } catch (error) {
                console.error('Error fetching job:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchJob();
    }, [id]);

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: `Apply for ${job.jobTitle} at ${job.companyName}`,
                    text: `Check out this opening for ${job.jobTitle} at ${job.companyName}`,
                    url: window.location.href,
                });
            } catch (err) {
                if (err instanceof Error && err.name !== 'AbortError') {
                    console.error('Error sharing:', err);
                    toast.error('Failed to share');
                }
            }
        } else {
            try {
                await navigator.clipboard.writeText(window.location.href);
                toast.success('Link copied to clipboard!');
            } catch (err) {
                toast.error('Failed to copy link');
            }
        }
    };

    const handleApply = async () => {
        try {
            // Track application
            const res = await fetch('/api/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ jobId: id }),
            });

            if (res.ok) {
                const { jobApplicationUrl } = await res.json();
                // Open mock application page for now (as per requirements)
                window.open('/apply/mock', '_blank');
                // In production, would use: window.open(jobApplicationUrl, '_blank');
            }
        } catch (error) {
            console.error('Error tracking application:', error);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading job details...</p>
                </div>
            </div>
        );
    }

    if (!job) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-2xl font-bold text-gray-900 mb-4">Job Not Found</h1>
                    <Link href="/" className="text-blue-600 hover:text-blue-700">
                        Return to Home
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Breadcrumb */}
                <nav className="text-sm text-gray-600 mb-6">
                    <Link href="/" className="hover:text-blue-600">
                        Home
                    </Link>
                    <span className="mx-2">/</span>
                    <Link href="/jobs/search/all" className="hover:text-blue-600">
                        Jobs
                    </Link>
                    <span className="mx-2">/</span>
                    <span className="text-gray-900">{job.jobTitle}</span>
                </nav>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Content */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Job Header */}
                        <div className="bg-white rounded-lg shadow p-8">
                            <div className="flex items-start gap-6 mb-6">
                                {job.companyLogo ? (
                                    <Image
                                        src={job.companyLogo}
                                        alt={job.companyName}
                                        width={80}
                                        height={80}
                                        className="w-20 h-20 rounded-lg object-cover"
                                    />
                                ) : (
                                    <div className="w-20 h-20 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl">
                                        {job.companyName.charAt(0)}
                                    </div>
                                )}
                                <div className="flex-1">
                                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                                        {job.jobTitle}
                                    </h1>
                                    <div className="flex items-center gap-4 text-gray-700 mb-4">
                                        <span className="font-semibold text-lg">{job.companyName}</span>
                                        {job.companyUrl && (
                                            <a
                                                href={job.companyUrl}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-600 hover:text-blue-700 text-sm"
                                            >
                                                Visit Website →
                                            </a>
                                        )}
                                    </div>
                                    <div className="flex flex-wrap gap-3">
                                        <div className="flex items-center gap-2 text-gray-700 bg-gray-50 px-3 py-1.5 rounded-md">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            <span className="text-sm">{job.jobLocation}</span>
                                        </div>
                                        <div className="flex items-center gap-2 text-gray-700 bg-gray-50 px-3 py-1.5 rounded-md">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                            </svg>
                                            <span className="text-sm">{job.jobType}</span>
                                        </div>
                                        <span className="px-3 py-1.5 bg-blue-50 text-blue-700 font-medium rounded-md text-sm">
                                            {job.jobCategory}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Quick Overview */}
                        <div className="bg-blue-50 border-l-4 border-blue-600 rounded-lg p-6">
                            <h3 className="font-semibold text-blue-900 mb-4">Quick Overview</h3>
                            <div className="grid grid-cols-3 gap-4">
                                <div>
                                    <p className="text-sm text-blue-700 mb-1">Location</p>
                                    <p className="font-semibold text-blue-900">{job.jobLocation}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-blue-700 mb-1">Job Type</p>
                                    <p className="font-semibold text-blue-900">{job.jobType}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-blue-700 mb-1">Category</p>
                                    <p className="font-semibold text-blue-900">{job.jobCategory}</p>
                                </div>
                            </div>
                        </div>

                        {/* Job Description */}
                        <div className="bg-white rounded-lg shadow p-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6">Job Description</h2>
                            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed">
                                {job.jobDescription}
                            </div>
                        </div>

                        {/* Additional Details */}
                        {job.otherDetails && (
                            <div className="bg-white rounded-lg shadow p-8">
                                <h2 className="text-2xl font-bold text-gray-900 mb-6">Additional Details</h2>
                                <div className="prose max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed">
                                    {job.otherDetails}
                                </div>
                            </div>
                        )}

                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Application Section */}
                        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 text-center border border-blue-200">
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Ready to Apply?</h3>
                            <p className="text-gray-700 text-sm mb-4">
                                Join {job.companyName} and take the next step in your career
                            </p>
                            <div className="flex flex-col gap-3">
                                <Button onClick={handleApply} size="lg" className="w-full">
                                    Apply for this Position
                                </Button>
                                <button
                                    onClick={handleShare}
                                    className="w-full px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 font-medium text-base"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                                    </svg>
                                    Share
                                </button>
                            </div>
                        </div>

                        {/* Company Overview */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Company Overview</h3>
                            <div className="flex items-center gap-4 mb-4">
                                {job.companyLogo ? (
                                    <Image
                                        src={job.companyLogo}
                                        alt={job.companyName}
                                        width={60}
                                        height={60}
                                        className="w-15 h-15 rounded-lg object-cover"
                                    />
                                ) : (
                                    <div className="w-15 h-15 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                                        {job.companyName.charAt(0)}
                                    </div>
                                )}
                                <div>
                                    <h4 className="font-bold text-gray-900">{job.companyName}</h4>
                                    {job.companyUrl && (
                                        <a
                                            href={job.companyUrl}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-sm text-blue-600 hover:text-blue-700"
                                        >
                                            Visit Website
                                        </a>
                                    )}
                                </div>
                            </div>
                            <p className="text-sm text-gray-600 leading-relaxed">
                                Learn more about {job.companyName} and explore their opportunities in {job.jobCategory}.
                            </p>
                        </div>

                        {/* Job Details */}
                        <div className="bg-white rounded-lg shadow p-6">
                            <h3 className="text-lg font-bold text-gray-900 mb-4">Job Details</h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-start pb-3 border-b border-gray-100">
                                    <span className="text-sm text-gray-600">Location</span>
                                    <span className="text-sm font-medium text-gray-900 text-right">{job.jobLocation}</span>
                                </div>
                                <div className="flex justify-between items-start pb-3 border-b border-gray-100">
                                    <span className="text-sm text-gray-600">Job Type</span>
                                    <span className="text-sm font-medium text-gray-900">{job.jobType}</span>
                                </div>
                                <div className="flex justify-between items-start pb-3 border-b border-gray-100">
                                    <span className="text-sm text-gray-600">Category</span>
                                    <span className="text-sm font-medium text-gray-900">{job.jobCategory}</span>
                                </div>
                                <div className="flex justify-between items-start">
                                    <span className="text-sm text-gray-600">Posted</span>
                                    <span className="text-sm font-medium text-gray-900">
                                        {new Date(job.createdAt).toLocaleDateString('en-US', {
                                            month: 'short',
                                            day: 'numeric',
                                            year: 'numeric'
                                        })}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Similar Jobs */}
                {similarJobs.length > 0 && (
                    <div className="mt-12">
                        <h2 className="text-3xl font-bold text-gray-900 mb-8">Similar Jobs</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {similarJobs.slice(0, 6).map((similarJob) => (
                                <JobCard key={similarJob.id} job={similarJob} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
