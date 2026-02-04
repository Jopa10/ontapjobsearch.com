
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/Button';
import toast from 'react-hot-toast';

export default function AddJobPage() {
    const router = useRouter();
    const [saving, setSaving] = useState(false);
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
        isPublished: true, // Default to published
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);

        try {
            const res = await fetch('/api/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(job),
            });

            if (res.ok) {
                toast.success('Job created successfully!');
                const newJob = await res.json();
                // Redirect to edit page to allow adding logo, or back to list?
                // Let's redirect to list for now as it's standard.
                router.push('/admin/jobs');
            } else {
                const error = await res.json();
                toast.error(`Failed to create job: ${error.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error creating job:', error);
            toast.error('Failed to create job');
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="max-w-4xl">
            <div className="flex items-center justify-between mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Add New Job</h1>
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
                                placeholder="e.g. Senior React Developer"
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
                                placeholder="e.g. Remote, New York, NY"
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
                            placeholder="Describe the role, responsibilities, and requirements..."
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Category *
                            </label>
                            <input
                                type="text"
                                required
                                value={job.jobCategory}
                                onChange={(e) => setJob({ ...job, jobCategory: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                                placeholder="e.g. Engineering"
                            />
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
                                placeholder="e.g. Acme Corp"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Company URL
                            </label>
                            <input
                                type="url"
                                value={job.companyUrl}
                                onChange={(e) => setJob({ ...job, companyUrl: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                                placeholder="https://company.com"
                            />
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
                            value={job.otherDetails}
                            onChange={(e) => setJob({ ...job, otherDetails: e.target.value })}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                            placeholder="Any extra info..."
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Company Logo
                        </label>
                        <div className="space-y-4">
                            {/* Logo Preview */}
                            {job.companyLogo && (
                                <div>
                                    <p className="text-sm text-gray-600 mb-2">Logo Preview:</p>
                                    <img
                                        src={job.companyLogo}
                                        alt="Logo preview"
                                        className="w-32 h-32 object-cover rounded-lg border border-gray-300"
                                    />
                                    <Button
                                        type="button"
                                        variant="secondary"
                                        className="mt-2 text-sm"
                                        onClick={() => setJob({ ...job, companyLogo: '' })}
                                    >
                                        Remove Logo
                                    </Button>
                                </div>
                            )}

                            {/* File Input */}
                            {!job.companyLogo && (
                                <div>
                                    <input
                                        type="file"
                                        accept="image/jpeg,image/jpg,image/png,image/webp"
                                        onChange={(e) => {
                                            const file = e.target.files?.[0];
                                            if (file) {
                                                const reader = new FileReader();
                                                reader.onloadend = () => {
                                                    setJob({ ...job, companyLogo: reader.result as string });
                                                };
                                                reader.readAsDataURL(file);
                                            }
                                        }}
                                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                                    />
                                    <p className="text-xs text-gray-500 mt-1">
                                        Accepted formats: JPG, PNG, WebP. Max size: 5MB
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="flex gap-4 pt-4">
                        <Button type="submit" loading={saving}>
                            Create Job
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
