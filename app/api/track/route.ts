// app/api/track/route.ts - Application tracking API
import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';
import prisma from '@/lib/prisma';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { jobId } = body;

        if (!jobId) {
            return NextResponse.json({ error: 'Job ID is required' }, { status: 400 });
        }

        // Verify job exists
        const job = await prisma.job.findUnique({
            where: { id: jobId },
        });

        if (!job) {
            return NextResponse.json({ error: 'Job not found' }, { status: 404 });
        }

        // Create tracking cookie (UUID)
        const trackingCookie = uuidv4();

        // Create application tracking record
        const application = await prisma.application.create({
            data: {
                jobId,
                trackingCookie,
            },
        });

        return NextResponse.json({
            trackingCookie,
            jobApplicationUrl: job.jobApplicationUrl,
        });
    } catch (error) {
        console.error('Error tracking application:', error);
        return NextResponse.json({ error: 'Failed to track application' }, { status: 500 });
    }
}
