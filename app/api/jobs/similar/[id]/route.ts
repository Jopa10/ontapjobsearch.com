// app/api/jobs/similar/[id]/route.ts - Get similar jobs API
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    try {
        // Get the main job
        const mainJob = await prisma.job.findUnique({
            where: { id },
        });

        if (!mainJob) {
            return NextResponse.json({ error: 'Job not found' }, { status: 404 });
        }

        // Find similar jobs based on category, type, and location
        const similarJobs = await prisma.job.findMany({
            where: {
                AND: [
                    { id: { not: id } }, // Exclude the main job
                    { isPublished: true }, // Only show published jobs
                    {
                        OR: [
                            { jobCategory: mainJob.jobCategory },
                            { jobType: mainJob.jobType },
                            { jobLocation: { contains: mainJob.jobLocation, mode: 'insensitive' } },
                        ],
                    },
                ],
            },
            take: 15, // Get up to 15 similar jobs
            orderBy: { createdAt: 'desc' },
        });

        return NextResponse.json(similarJobs);
    } catch (error) {
        console.error('Error fetching similar jobs:', error);
        return NextResponse.json({ error: 'Failed to fetch similar jobs' }, { status: 500 });
    }
}
