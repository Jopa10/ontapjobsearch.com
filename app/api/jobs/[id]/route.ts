// app/api/jobs/[id]/route.ts - Individual job operations (GET, PUT, DELETE)
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import prisma from '@/lib/prisma';

// GET /api/jobs/[id] - Get single job by ID
export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    try {
        const job = await prisma.job.findUnique({
            where: { id },
        });

        if (!job) {
            return NextResponse.json({ error: 'Job not found' }, { status: 404 });
        }

        // Access control: if job is not published, check if user is admin
        if (!job.isPublished) {
            const session = await getServerSession(authOptions);
            if (!session) {
                // Return 404 to hide existence of unpublished jobs from public
                return NextResponse.json({ error: 'Job not found' }, { status: 404 });
            }
        }

        return NextResponse.json(job);
    } catch (error) {
        console.error('Error fetching job:', error);
        return NextResponse.json({ error: 'Failed to fetch job' }, { status: 500 });
    }
}

// PUT /api/jobs/[id] - Update job (admin only)
export async function PUT(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    try {
        // Check authentication
        const session = await getServerSession(authOptions);
        if (!session) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();

        // Prepare update data by filtering out undefined fields
        const updateData: any = {};
        const allowedFields = [
            'jobTitle', 'jobLocation', 'jobDescription', 'jobCategory',
            'jobType', 'companyName', 'companyUrl', 'companyLogo',
            'jobApplicationUrl', 'otherDetails', 'isPublished'
        ];

        for (const field of allowedFields) {
            if (body[field] !== undefined) {
                updateData[field] = body[field];
            }
        }

        console.log('Updating job with data:', updateData);

        // Update job
        const job = await prisma.job.update({
            where: { id },
            data: updateData,
        });

        return NextResponse.json(job);
    } catch (error: any) {
        console.error('Error updating job:', error);
        return NextResponse.json({
            error: error.message || 'Failed to update job',
            details: error.toString()
        }, { status: 500 });
    }
}

// DELETE /api/jobs/[id] - Delete job (admin only)
export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    try {
        // Check authentication
        const session = await getServerSession(authOptions);
        if (!session) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        await prisma.job.delete({
            where: { id },
        });

        return NextResponse.json({ message: 'Job deleted successfully' });
    } catch (error) {
        console.error('Error deleting job:', error);
        return NextResponse.json({ error: 'Failed to delete job' }, { status: 500 });
    }
}
