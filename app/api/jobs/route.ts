// app/api/jobs/route.ts - Jobs list and create API
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import prisma from '@/lib/prisma';

// GET /api/jobs - List all jobs with optional search/filter
export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url);
        const search = searchParams.get('search') || '';
        const category = searchParams.get('category');
        const type = searchParams.get('type');
        const location = searchParams.get('location');
        const page = parseInt(searchParams.get('page') || '1');
        const limit = parseInt(searchParams.get('limit') || '20');
        const skip = (page - 1) * limit;

        // Build where clause for filtering
        const where: any = {};

        if (search) {
            where.OR = [
                { jobTitle: { contains: search, mode: 'insensitive' } },
                { jobLocation: { contains: search, mode: 'insensitive' } },
                { companyName: { contains: search, mode: 'insensitive' } },
                { jobDescription: { contains: search, mode: 'insensitive' } },
                { jobCategory: { contains: search, mode: 'insensitive' } },
            ];
        }

        if (category) {
            where.jobCategory = { contains: category, mode: 'insensitive' };
        }

        if (type) {
            where.jobType = type;
        }

        if (location) {
            where.jobLocation = { contains: location, mode: 'insensitive' };
        }

        // Filter out unpublished jobs for public users (unless admin)
        const session = await getServerSession(authOptions);
        if (!session) {
            where.isPublished = true;
        }

        // Fetch jobs with pagination
        const [jobs, total] = await Promise.all([
            prisma.job.findMany({
                where,
                skip,
                take: limit,
                orderBy: { createdAt: 'desc' },
            }),
            prisma.job.count({ where }),
        ]);

        return NextResponse.json({
            jobs,
            pagination: {
                page,
                limit,
                total,
                totalPages: Math.ceil(total / limit),
            },
        });
    } catch (error) {
        console.error('Error fetching jobs:', error);
        return NextResponse.json({ error: 'Failed to fetch jobs' }, { status: 500 });
    }
}

// POST /api/jobs - Create new job (admin only)
export async function POST(request: NextRequest) {
    try {
        // Check authentication
        const session = await getServerSession(authOptions);
        if (!session) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const body = await request.json();

        // Validate required fields
        const {
            jobTitle,
            jobLocation,
            jobDescription,
            jobCategory,
            jobType,
            companyName,
            jobApplicationUrl,
        } = body;

        if (
            !jobTitle ||
            !jobLocation ||
            !jobDescription ||
            !jobCategory ||
            !jobType ||
            !companyName ||
            !jobApplicationUrl
        ) {
            return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
        }

        // Create job
        const job = await prisma.job.create({
            data: {
                jobTitle,
                jobLocation,
                jobDescription,
                jobCategory,
                jobType,
                companyName,
                companyUrl: body.companyUrl || null,
                companyLogo: body.companyLogo || null,
                jobApplicationUrl,
                otherDetails: body.otherDetails || null,
            },
        });

        return NextResponse.json(job, { status: 201 });
    } catch (error) {
        console.error('Error creating job:', error);
        return NextResponse.json({ error: 'Failed to create job' }, { status: 500 });
    }
}
