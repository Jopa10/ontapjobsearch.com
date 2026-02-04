// app/api/jobs/upload/route.ts - CSV/JSON upload API for bulk job import
import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import prisma from '@/lib/prisma';
import Papa from 'papaparse';

export async function POST(request: NextRequest) {
    try {
        // Check authentication
        const session = await getServerSession(authOptions);
        if (!session) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
            return NextResponse.json({ error: 'No file provided' }, { status: 400 });
        }

        const fileContent = await file.text();
        const fileType = file.name.endsWith('.json') ? 'json' : 'csv';

        let jobs: any[] = [];

        if (fileType === 'json') {
            // Parse JSON file
            try {
                const jsonData = JSON.parse(fileContent);
                jobs = Array.isArray(jsonData) ? jsonData : [jsonData];
            } catch (error) {
                return NextResponse.json({ error: 'Invalid JSON format' }, { status: 400 });
            }
        } else {
            // Parse CSV file
            const result = Papa.parse(fileContent, {
                header: true,
                skipEmptyLines: true,
            });

            if (result.errors.length > 0) {
                return NextResponse.json({ error: 'Invalid CSV format' }, { status: 400 });
            }

            jobs = result.data;
        }

        // Validate and transform jobs data
        const createdJobs = [];
        const errors = [];

        for (let i = 0; i < jobs.length; i++) {
            const jobData = jobs[i];

            // Map CSV/JSON fields to database fields
            const job = {
                jobTitle: jobData.jobtitle || jobData.jobTitle,
                jobLocation: jobData.joblocation || jobData.jobLocation,
                jobDescription: jobData.jobdescription || jobData.jobDescription,
                jobCategory: jobData.jobcategory || jobData.jobCategory,
                jobType: jobData.jobtype || jobData.jobType,
                companyName: jobData.companyname || jobData.companyName,
                companyUrl: jobData.companyurl || jobData.companyUrl || null,
                companyLogo: null, // Logo must be uploaded manually in edit mode
                jobApplicationUrl: jobData.jobapplicationurl || jobData.jobApplicationUrl,
                otherDetails: jobData.otherdetails || jobData.otherDetails || null,
            };

            // Validate required fields
            if (
                !job.jobTitle ||
                !job.jobLocation ||
                !job.jobDescription ||
                !job.jobCategory ||
                !job.jobType ||
                !job.companyName ||
                !job.jobApplicationUrl
            ) {
                errors.push({ row: i + 1, error: 'Missing required fields' });
                continue;
            }

            try {
                const created = await prisma.job.create({ data: job });
                createdJobs.push(created);
            } catch (error) {
                errors.push({ row: i + 1, error: 'Failed to create job' });
            }
        }

        return NextResponse.json({
            success: true,
            created: createdJobs.length,
            errors: errors.length,
            errorDetails: errors,
        });
    } catch (error) {
        console.error('Error uploading jobs:', error);
        return NextResponse.json({ error: 'Failed to upload jobs' }, { status: 500 });
    }
}
