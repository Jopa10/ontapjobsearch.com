// components/JobCard.tsx - Reusable job card component
import Link from 'next/link';
import Image from 'next/image';

interface Job {
    id: string;
    jobTitle: string;
    jobLocation: string;
    jobType: string;
    jobCategory: string;
    companyName: string;
    companyLogo?: string | null;
    createdAt?: string | Date;
}

interface JobCardProps {
    job: Job;
}

export default function JobCard({ job }: JobCardProps) {
    return (
        <Link href={`/jobs/${job.id}`}>
            <div className="bg-white rounded-lg border border-gray-200 hover:border-blue-500 hover:shadow-lg transition-all duration-200 p-6 cursor-pointer">
                <div className="flex items-start gap-4">
                    {/* Company Logo */}
                    {job.companyLogo ? (
                        <Image
                            src={job.companyLogo}
                            alt={job.companyName}
                            width={48}
                            height={48}
                            className="w-12 h-12 rounded-lg object-cover"
                        />
                    ) : (
                        <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg">
                            {job.companyName.charAt(0)}
                        </div>
                    )}

                    {/* Job Info */}
                    <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1 hover:text-blue-600 transition-colors">
                            {job.jobTitle}
                        </h3>
                        <p className="text-gray-700 font-medium mb-2">{job.companyName}</p>

                        <div className="flex flex-wrap gap-3 text-sm text-gray-600">
                            <span className="flex items-center gap-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                {job.jobLocation}
                            </span>
                            <span className="flex items-center gap-1">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                                {job.jobType}
                            </span>
                        </div>

                        <div className="mt-3">
                            <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 text-xs font-medium rounded-full">
                                {job.jobCategory}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </Link>
    );
}
