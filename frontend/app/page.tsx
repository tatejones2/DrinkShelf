'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();
  const { user, initializeAuth } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
    setIsLoading(false);
  }, [initializeAuth]);

  if (isLoading) {
    return (
      <ClientLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-400">Loading...</div>
        </div>
      </ClientLayout>
    );
  }

  return (
    <ClientLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4">
            <span className="text-amber-500">DrinkShelf</span>
          </h1>
          <p className="text-xl text-gray-400 mb-8">
            The ultimate spirit collector's platform. Organize, discover, and share your collection.
          </p>

          {!user ? (
            <div className="flex gap-4 justify-center">
              <Link href="/auth/login" className="btn-primary px-8 py-3">
                Log In
              </Link>
              <Link href="/auth/register" className="btn-secondary px-8 py-3">
                Create Account
              </Link>
            </div>
          ) : (
            <div className="flex gap-4 justify-center">
              <Link href="/dashboard" className="btn-primary px-8 py-3">
                Go to Dashboard
              </Link>
              <Link href="/search" className="btn-secondary px-8 py-3">
                Explore Catalog
              </Link>
            </div>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="card text-center">
            <div className="text-4xl mb-4">🍾</div>
            <h3 className="text-lg font-bold text-amber-400 mb-2">Manage Your Collection</h3>
            <p className="text-gray-400">
              Add bottles, track ratings, and organize your spirits into custom collections.
            </p>
          </div>

          <div className="card text-center">
            <div className="text-4xl mb-4">📝</div>
            <h3 className="text-lg font-bold text-amber-400 mb-2">Tasting Notes</h3>
            <p className="text-gray-400">
              Record your tasting experiences with detailed notes and ratings.
            </p>
          </div>

          <div className="card text-center">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-lg font-bold text-amber-400 mb-2">Discover</h3>
            <p className="text-gray-400">
              Search and filter by spirit type, region, price, and more to find your next bottle.
            </p>
          </div>
        </div>
      </div>
    </ClientLayout>
  );
}
