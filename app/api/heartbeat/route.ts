// app/api/heartbeat/route.ts - Server heartbeat endpoint
import { NextResponse } from 'next/server';

export async function GET() {
    return NextResponse.json({
        status: 'alive',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
    });
}
