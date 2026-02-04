// app/admin/jobs/page.tsx - Admin jobs dashboard
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Button from '@/components/Button';

import toast from 'react-hot-toast';

export default function AdminJobsPage() {
    const [jobs, setJobs] = useState<any[]>([]);
    const [filteredJobs, setFilteredJobs] = useState<any[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const filtered = jobs.filter((job) =>
            job.jobTitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
            job.companyName.toLowerCase().includes(searchQuery.toLowerCase()) ||
            job.jobLocation.toLowerCase().includes(searchQuery.toLowerCase())
        );
        setFilteredJobs(filtered);
    }, [searchQuery, jobs]);

    const handleSearch = () => {
        setSearchQuery(searchTerm);
    };

    const handleClear = () => {
        setSearchTerm('');
        setSearchQuery('');
    };

    async function togglePublish(job: any) {
        try {
            const newStatus = !job.isPublished;
            const res = await fetch(`/api/jobs/${job.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ isPublished: newStatus }),
            });

            if (res.ok) {
                setJobs(jobs.map((j) => (j.id === job.id ? { ...j, isPublished: newStatus } : j)));
                toast.success(newStatus ? 'Job published' : 'Job unpublished');
            } else {
                toast.error('Failed to update status');
            }
        } catch (error) {
            console.error('Error updating status:', error);
            toast.error('Error updating status');
        }
    }

    useEffect(() => {
        fetchJobs();
    }, []);

    async function fetchJobs() {
        try {
            const res = await fetch('/api/jobs');
            if (res.ok) {
                const data = await res.json();
                setJobs(data.jobs || []);
            }
        } catch (error) {
            console.error('Error fetching jobs:', error);
            toast.error('Failed to fetch jobs');
        } finally {
            setLoading(false);
        }
    }

    async function deleteJob(id: string) {
        if (!confirm('Are you sure you want to delete this job?')) return;

        try {
            const res = await fetch(`/api/jobs/${id}`, { method: 'DELETE' });
            if (res.ok) {
                setJobs(jobs.filter((job) => job.id !== id));
                toast.success('Job deleted successfully');
            } else {
                toast.error('Failed to delete job');
            }
        } catch (error) {
            console.error('Error deleting job:', error);
            toast.error('Error deleting job');
        }
    }

    if (loading) {
        return (
            <div className="text-center py-12">
                <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"></div>
            </div>
        );
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Manage Jobs</h1>
                <div className="flex gap-4">
                    <Link href="/admin/jobs/upload">
                        <Button variant="secondary">Upload CSV/JSON</Button>
                    </Link>
                    <Link href="/admin/jobs/add">
                        <Button>Add New Job</Button>
                    </Link>
                </div>
            </div>

            {/* Search Bar */}
            <div className="mb-6 flex gap-2">
                <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                    <input
                        type="text"
                        className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition duration-150 ease-in-out"
                        placeholder="Search jobs by title, company, or location..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    />
                </div>
                <Button onClick={handleSearch}>Search</Button>
                <Button variant="secondary" onClick={handleClear}>Clear</Button>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Job Title
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Company
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Location
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Date Posted
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Type
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Published
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {filteredJobs.map((job) => (
                            <tr key={job.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4">
                                    <div className="text-sm font-medium text-gray-900 mb-1">{job.jobTitle}</div>
                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                                        {job.jobCategory}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-900">{job.companyName}</td>
                                <td className="px-6 py-4 text-sm text-gray-900">{job.jobLocation}</td>
                                <td className="px-6 py-4 text-sm text-gray-500">
                                    {new Date(job.createdAt).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-900">{job.jobType}</td>
                                <td className="px-6 py-4 text-sm">
                                    <button
                                        onClick={() => togglePublish(job)}
                                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${job.isPublished ? 'bg-green-500' : 'bg-gray-200'
                                            }`}
                                    >
                                        <span
                                            className={`${job.isPublished ? 'translate-x-6' : 'translate-x-1'
                                                } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
                                        />
                                    </button>
                                </td>
                                <td className="px-6 py-4 text-sm">
                                    <div className="flex gap-3">
                                        <Link
                                            href={`/jobs/${job.id}`}
                                            target="_blank"
                                            className="text-blue-600 hover:text-blue-900 transition-colors p-1 hover:bg-blue-50 rounded"
                                            title="View Job"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </Link>
                                        <Link
                                            href={`/admin/jobs/edit/${job.id}`}
                                            className="text-green-600 hover:text-green-900 transition-colors p-1 hover:bg-green-50 rounded"
                                            title="Edit Job"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </Link>
                                        <button
                                            onClick={() => deleteJob(job.id)}
                                            className="text-red-600 hover:text-red-900 transition-colors p-1 hover:bg-red-50 rounded"
                                            title="Delete Job"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                            </svg>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {jobs.length === 0 && (
                    <div className="text-center py-12 text-gray-500">
                        <p>No jobs found. Add your first job to get started!</p>
                    </div>
                )}
            </div>
        </div>
    );
}
