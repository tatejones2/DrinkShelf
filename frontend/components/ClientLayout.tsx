'use client';

import { ReactNode } from 'react';
import Navbar from '@/components/Navbar';

interface LayoutProps {
  children: ReactNode;
}

export default function ClientLayout({ children }: LayoutProps) {
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-950">
        {children}
      </main>
    </>
  );
}
