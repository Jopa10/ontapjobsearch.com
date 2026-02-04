// app/admin/jobs/upload/page.tsx - CSV/JSON upload page
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/Button';

import toast from 'react-hot-toast';

export default function UploadJobsPage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        setUploading(true);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch('/api/jobs/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();
            setResult(data);

            if (res.ok) {
                if (data.created > 0) {
                    toast.success(`Successfully improved ${data.created} jobs!`);
                    if (data.errors === 0) {
                        setTimeout(() => router.push('/admin/jobs'), 2000);
                    }
                } else if (data.errors > 0) {
                    toast.error(`Failed to import some jobs. Check details below.`);
                }
            } else {
                toast.error(data.error || 'Upload failed');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            toast.error('Failed to upload file');
            setResult({ error: 'Failed to upload file' });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="max-w-3xl">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Upload Jobs (CSV/JSON)</h1>

            <div className="bg-white rounded-lg shadow p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Select CSV or JSON File
                        </label>
                        <input
                            type="file"
                            accept=".csv,.json"
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none p-2"
                        />
                        <p className="mt-2 text-sm text-gray-500">
                            Upload a CSV or JSON file with job listings. Required fields: jobtitle, joblocation,
                            jobdescription, jobcategory, jobtype, companyname, jobapplicationurl.
                        </p>
                    </div>

                    {/* Sample Files Info */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h3 className="font-medium text-blue-900 mb-2">Sample Files</h3>
                        <p className="text-sm text-blue-700 mb-2">
                            Sample test data files are available in the testdata folder:
                        </p>
                        <ul className="text-sm text-blue-700 list-disc list-inside">
                            <li>testdata/csv/jobs.csv</li>
                            <li>testdata/json/jobs.json</li>
                        </ul>
                    </div>

                    {/* CSV Format */}
                    <div className="bg-gray-50 rounded-lg p-4">
                        <h3 className="font-medium text-gray-900 mb-2">CSV Format</h3>
                        <pre className="text-xs bg-white p-3 rounded border border-gray-200 overflow-x-auto">
                            {`jobtitle,joblocation,jobdescription,jobcategory,jobtype,companyname,companyurl,companylogo,jobapplicationurl,otherdetails
Planning Officer,Manchester,...`}
                        </pre>
                    </div>

                    {/* JSON Format */}
                    <div className="bg-gray-50 rounded-lg p-4">
                        <h3 className="font-medium text-gray-900 mb-2">JSON Format</h3>
                        <pre className="text-xs bg-white p-3 rounded border border-gray-200 overflow-x-auto">
                            {`[
  {
    "jobtitle": "Planning Officer",
    "joblocation": "Manchester",
    ...
  }
]`}
                        </pre>
                    </div>

                    <div className="flex gap-4">
                        <Button type="submit" loading={uploading} disabled={!file}>
                            Upload Jobs
                        </Button>
                        <Button type="button" variant="secondary" onClick={() => router.back()}>
                            Cancel
                        </Button>
                    </div>
                </form>

                {/* Results */}
                {result && (
                    <div
                        className={`mt-6 p-4 rounded-lg ${result.error ? 'bg-red-50 text-red-900' : 'bg-green-50 text-green-900'
                            }`}
                    >
                        {result.error ? (
                            <p className="font-medium">Error: {result.error}</p>
                        ) : (
                            <div>
                                <p className="font-medium mb-2">Upload successful!</p>
                                <p className="text-sm">Created: {result.created} jobs</p>
                                {result.errors > 0 && <p className="text-sm">Errors: {result.errors}</p>}
                                <p className="text-sm mt-2">Redirecting to jobs list...</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
