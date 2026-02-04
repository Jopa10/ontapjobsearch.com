// Database seed script for Ontap Job Search Platform
import 'dotenv/config';
import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import { Pool } from 'pg';
import * as bcrypt from 'bcrypt';

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
    throw new Error('DATABASE_URL environment variable is not set');
}
const pool = new Pool({ connectionString, ssl: false });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
    console.log('🌱 Seeding database...');

    const adminEmail = process.env.ADMIN_EMAIL || 'admin@ontap.com';

    // Create default admin user
    const adminPassword = process.env.ADMIN_PASSWORD;
    if (!adminPassword) {
        console.warn('⚠️  ADMIN_PASSWORD not set in environment. Skipping admin user creation.');
        return;
    }
    const hashedPassword = await bcrypt.hash(adminPassword, 10);

    const admin = await prisma.admin.upsert({
        where: { email: adminEmail },
        update: {},
        create: {
            email: adminEmail,
            password: hashedPassword,
            name: 'Admin User',
            role: 'admin',
        },
    });

    console.log('✅ Created admin user:', admin.email);
    console.log('   Email:', adminEmail);
    console.log('   Password: [HIDDEN] (from ADMIN_PASSWORD env var)');

    console.log('🎉 Seeding completed!');
}

main()
    .catch((e) => {
        console.error('❌ Seeding failed:', e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
