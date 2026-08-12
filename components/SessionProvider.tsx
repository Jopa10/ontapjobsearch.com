// components/SessionProvider.tsx - Client component for NextAuth session
'use client';

import { SessionProvider as NextAuthSessionProvider } from 'next-auth/react';
import type { Session } from 'next-auth';

export default function SessionProvider({
    children,
    session,
}: {
    children: React.ReactNode;
    session?: Session | null;
}) {
    if (session === undefined) {
        return <NextAuthSessionProvider>{children}</NextAuthSessionProvider>;
    }

    return <NextAuthSessionProvider session={session}>{children}</NextAuthSessionProvider>;
}
