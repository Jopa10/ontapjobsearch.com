// lib/db-utils.ts - Database utilities and health check functions
import prisma from './prisma';

/**
 * Check if database connection is healthy
 */
export async function checkDatabaseHealth(): Promise<boolean> {
    try {
        await prisma.$queryRaw`SELECT 1`;
        return true;
    } catch (error) {
        console.error('Database health check failed:', error);
        return false;
    }
}

/**
 * Initialize database - run migrations if needed
 */
export async function initializeDatabase(): Promise<void> {
    try {
        // Test connection
        await prisma.$connect();
        console.log('✅ Database connected successfully');
    } catch (error) {
        console.error('❌ Database connection failed:', error);
        throw new Error('Failed to connect to database');
    }
}

/**
 * Gracefully disconnect from database
 */
export async function disconnectDatabase(): Promise<void> {
    await prisma.$disconnect();
}
