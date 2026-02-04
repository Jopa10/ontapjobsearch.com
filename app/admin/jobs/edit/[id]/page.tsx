// app/admin/jobs/edit/[id]/page.tsx - Edit job page
'use client';

import { use, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/Button';
import toast from 'react-hot-toast';

export default function EditJobPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [uploadingLogo, setUploadingLogo] = useState(false);
    const [logoFile, setLogoFile] = useState<File | null>(null);
    const [logoPreview, setLogoPreview] = useState<string>('');
    const [job, setJob] = useState({
        jobTitle: '',
        jobLocation: '',
        jobDescription: '',
        jobCategory: '',
        jobType: '',
        companyName: '',
        companyUrl: '',
        companyLogo: '',
        jobApplicationUrl: '',
        otherDetails: '',
    });

    useEffect(() => {
        async function fetchJob() {
            try {
                const res = await fetch(`/api/jobs/${id}`);
                if (res.ok) {
                    const data = await res.json();
                    setJob(data);
                } else {
                    toast.error('Job not found');
                    router.push('/admin/jobs');
                }
            } catch (error) {
                console.error('Error fetching job:', error);
                toast.error('Failed to load job');
            } finally {
                setLoading(false);
            }
        }

        fetchJob();
    }, [id, router]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);

        try {
            const jobToUpdate = { ...job };
            // We now send the logo in the update payload


            const res = await fetch(`/api/jobs/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(jobToUpdate),
            });

            if (res.ok) {
                toast.success('Job updated successfully!');
                router.push('/admin/jobs');
            } else {
                const error = await res.json();
                toast.error(`Failed to update job: ${error.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error updating job:', error);
            toast.error('Failed to update job');
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async () => {
        if (!confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
            return;
        }

        try {
            const res = await fetch(`/api/jobs/${id}`, {
                method: 'DELETE',
            });

            if (res.ok) {
                toast.success('Job deleted successfully!');
                router.push('/admin/jobs');
            } else {
                const error = await res.json();
                toast.error(`Failed to delete job: ${error.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error deleting job:', error);
            toast.error('Failed to delete job');
        }
    };

    const handleLogoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setJob({ ...job, companyLogo: reader.result as string });
            };
            reader.readAsDataURL(file);
        }
    };

    const handleRemoveLogo = () => {
        setJob({ ...job, companyLogo: '' });
        // Reset file input if needed (optional via ref, but state update explains UI enough)
    };


    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading job...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl">
            <div className="flex items-center justify-between mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Edit Job</h1>
                <Button variant="danger" onClick={handleDelete}>
                    Delete Job
                </Button>
            </div>

            <div className="bg-white rounded-lg shadow p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Job Title *
                            </label>
                            <input
                                type="text"
                                required
                                value={job.jobTitle}
                                onChange={(e) => setJob({ ...job, jobTitle: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Location *
                            </label>
                            <input
                                type="text"
                                required
                                value={job.jobLocation}
                                onChange={(e) => setJob({ ...job, jobLocation: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Job Description *
                        </label>
                        <textarea
                            required
                            rows={8}
                            value={job.jobDescription}
                            onChange={(e) => setJob({ ...job, jobDescription: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Category *
                            </label>
                            <select
                                required
                                value={job.jobCategory}
                                onChange={(e) => setJob({ ...job, jobCategory: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            >
                                <option value="">Select category</option>
                                <option value="Technology">Technology</option>
                                <option value="Healthcare">Healthcare</option>
                                <option value="Finance">Finance</option>
                                <option value="Education">Education</option>
                                <option value="Government">Government</option>
                                <option value="Construction">Construction</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Job Type *
                            </label>
                            <select
                                required
                                value={job.jobType}
                                onChange={(e) => setJob({ ...job, jobType: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            >
                                <option value="">Select type</option>
                                <option value="Full-time">Full-time</option>
                                <option value="Part-time">Part-time</option>
                                <option value="Contract">Contract</option>
                                <option value="Internship">Internship</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Company Name *
                            </label>
                            <input
                                type="text"
                                required
                                value={job.companyName}
                                onChange={(e) => setJob({ ...job, companyName: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Company URL
                            </label>
                            <input
                                type="url"
                                value={job.companyUrl || ''}
                                onChange={(e) => setJob({ ...job, companyUrl: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                                placeholder="https://company.com"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Company Logo
                        </label>
                        <div className="space-y-4">
                            {/* Logo Display & Actions */}
                            {job.companyLogo ? (
                                <div className="flex items-start gap-4">
                                    <img
                                        src={job.companyLogo}
                                        alt="Company logo"
                                        className="w-32 h-32 object-cover rounded-lg border border-gray-300"
                                    />
                                    <div className="space-y-2">
                                        <Button
                                            type="button"
                                            variant="secondary"
                                            onClick={handleRemoveLogo}
                                            className="w-full"
                                        >
                                            Remove Logo
                                        </Button>
                                        <div className="relative">
                                            <input
                                                type="file"
                                                id="logo-upload"
                                                accept="image/*"
                                                onChange={handleLogoChange}
                                                className="hidden"
                                            />
                                            <label
                                                htmlFor="logo-upload"
                                                className="inline-block w-full px-4 py-2 bg-blue-600 text-white rounded-lg text-center cursor-pointer hover:bg-blue-700 transition-colors"
                                            >
                                                Change Logo
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div>
                                    <input
                                        type="file"
                                        id="logo-upload"
                                        accept="image/*"
                                        onChange={handleLogoChange}
                                        className="hidden"
                                    />
                                    <label
                                        htmlFor="logo-upload"
                                        className="inline-block px-6 py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 cursor-pointer hover:border-blue-500 hover:text-blue-500 transition-colors"
                                    >
                                        <span className="flex items-center gap-2">
                                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                            </svg>
                                            Upload Logo
                                        </span>
                                    </label>
                                    <p className="text-xs text-gray-500 mt-2">
                                        Accepted formats: JPG, PNG, WebP. Max size: 5MB
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Application URL *
                        </label>
                        <input
                            type="url"
                            required
                            value={job.jobApplicationUrl}
                            onChange={(e) => setJob({ ...job, jobApplicationUrl: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            placeholder="https://company.com/apply"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Additional Details
                        </label>
                        <textarea
                            rows={6}
                            value={job.otherDetails || ''}
                            onChange={(e) => setJob({ ...job, otherDetails: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            placeholder="Any additional information about the job..."
                        />
                    </div>

                    <div className="flex gap-4 pt-4">
                        <Button type="submit" loading={saving}>
                            Save Changes
                        </Button>
                        <Button type="button" variant="secondary" onClick={() => router.back()}>
                            Cancel
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
}
