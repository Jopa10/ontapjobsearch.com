
import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import { Pool } from 'pg';
import dotenv from 'dotenv';
dotenv.config();

const connectionString = process.env.DATABASE_URL;
const pool = new Pool({ connectionString });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
    try {
        console.log('Fetching a job...');
        const job = await prisma.job.findFirst();
        if (!job) {
            console.log('No jobs found.');
            return;
        }
        console.log('Found job:', job.id);
        console.log('Current isPublished:', (job as any).isPublished);

        console.log('Attempting to toggle isPublished...');
        const updatedJob = await prisma.job.update({
            where: { id: job.id },
            data: { isPublished: !(job as any).isPublished }
        });
        console.log('Success! New isPublished:', updatedJob.isPublished);
    } catch (e) {
        console.error('Error updating job:', e);
    } finally {
        await prisma.$disconnect();
    }
}

main();
