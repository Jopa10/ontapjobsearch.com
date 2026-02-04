// app/api/health/route.ts - Database health check endpoint
import { NextResponse } from 'next/server';
import { checkDatabaseHealth } from '@/lib/db-utils';

export async function GET() {
    try {
        const isHealthy = await checkDatabaseHealth();

        if (isHealthy) {
            return NextResponse.json(
                {
                    status: 'ok',
                    database: 'connected',
                    timestamp: new Date().toISOString(),
                },
                { status: 200 }
            );
        } else {
            return NextResponse.json(
                {
                    status: 'error',
                    database: 'disconnected',
                    timestamp: new Date().toISOString(),
                },
                { status: 503 }
            );
        }
    } catch (error) {
        return NextResponse.json(
            {
                status: 'error',
                message: 'Health check failed',
                timestamp: new Date().toISOString(),
            },
            { status: 500 }
        );
    }
}
