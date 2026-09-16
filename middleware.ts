// middleware.ts - Route protection middleware for admin pages
import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
    function middleware(req) {
        const token = req.nextauth.token;
        const isAdminPath = req.nextUrl.pathname.startsWith('/admin');
        const isAuthPath =
            req.nextUrl.pathname.startsWith('/admin/login') ||
            req.nextUrl.pathname.startsWith('/admin/recover');

        // Allow access to login and recover pages without authentication
        if (isAuthPath) {
            return NextResponse.next();
        }

        // Protect admin routes - redirect to login if not authenticated
        if (isAdminPath && !token) {
            const loginUrl = new URL('/admin/login', req.url);
            loginUrl.searchParams.set('callbackUrl', req.nextUrl.pathname);
            return NextResponse.redirect(loginUrl);
        }

        return NextResponse.next();
    },
    {
        callbacks: {
            authorized: ({ token, req }) => {
                const isAuthPath =
                    req.nextUrl.pathname.startsWith('/admin/login') ||
                    req.nextUrl.pathname.startsWith('/admin/recover');

                // Always allow auth pages
                if (isAuthPath) {
                    return true;
                }

                // For other admin pages, require token
                if (req.nextUrl.pathname.startsWith('/admin')) {
                    return !!token;
                }

                // Allow all other pages
                return true;
            },
        },
    }
);

export const config = {
    matcher: ['/admin/:path*'],
};
