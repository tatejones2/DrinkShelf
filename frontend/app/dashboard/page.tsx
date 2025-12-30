'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import BottleCard from '@/components/BottleCard';
import bottleService, { Bottle, BottleStats } from '@/lib/services/bottles';
import tastingNoteService, { UserFlavorProfile } from '@/lib/services/tasting-notes';
import Link from 'next/link';

export default function DashboardPage() {
  const router = useRouter();
  const { user, initializeAuth } = useAuthStore();
  const [bottles, setBottles] = useState<Bottle[]>([]);
  const [stats, setStats] = useState<BottleStats | null>(null);
  const [profile, setProfile] = useState<UserFlavorProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    const loadData = async () => {
      try {
        const [bottlesList, bottleStats, userProfile] = await Promise.all([
          bottleService.getBottles(0, 6),
          bottleService.getBottleStats(),
          tastingNoteService.getUserStatistics().catch(() => null),
        ]);

        setBottles(bottlesList);
        setStats(bottleStats);
        setProfile(userProfile);
      } catch (error) {
        console.error('Failed to load dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [user, router]);

  if (isLoading) {
    return (
      <ClientLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-gray-400">Loading...</div>
        </div>
      </ClientLayout>
    );
  }

  if (!user) return null;

  return (
    <ClientLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-amber-400">
            Welcome, {user.display_name || user.username}! 🍾
          </h1>
          <p className="text-gray-400 mt-2">Manage your spirit collection</p>
        </div>

        {/* Stats Section */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="card">
              <div className="text-3xl font-bold text-amber-400">{stats.total_bottles}</div>
              <p className="text-gray-400">Total Bottles</p>
            </div>
            <div className="card">
              <div className="text-3xl font-bold text-amber-400">
                {stats.average_rating.toFixed(1)}/5
              </div>
              <p className="text-gray-400">Average Rating</p>
            </div>
            <div className="card">
              <div className="text-3xl font-bold text-amber-400">
                {Object.keys(stats.spirit_breakdown).length}
              </div>
              <p className="text-gray-400">Spirit Types</p>
            </div>
          </div>
        )}

        {/* User Flavor Profile */}
        {profile && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-amber-400 mb-4">Your Flavor Profile</h2>
            <div className="space-y-4">
              <div>
                <p className="text-gray-400">Average Rating: {profile.average_rating.toFixed(1)}/5</p>
              </div>
              {profile.most_tasted_spirits.length > 0 && (
                <div>
                  <p className="font-semibold text-gray-300 mb-2">Most Tasted Spirits:</p>
                  <div className="flex flex-wrap gap-2">
                    {profile.most_tasted_spirits.map((s) => (
                      <span key={s.spirit} className="px-3 py-1 bg-amber-900/30 border border-amber-700 rounded">
                        {s.spirit} ({s.count})
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {profile.common_descriptors.length > 0 && (
                <div>
                  <p className="font-semibold text-gray-300 mb-2">Common Descriptors:</p>
                  <div className="flex flex-wrap gap-2">
                    {profile.common_descriptors.slice(0, 5).map((d) => (
                      <span key={d} className="px-3 py-1 bg-gray-700 rounded text-sm">
                        {d}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link href="/bottles/new" className="card text-center hover:border-amber-400">
            <div className="text-4xl mb-4">➕</div>
            <h3 className="font-bold text-amber-400 mb-2">Add Bottle</h3>
            <p className="text-gray-400">Add a new bottle to your collection</p>
          </Link>
          <Link href="/collections" className="card text-center hover:border-amber-400">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="font-bold text-amber-400 mb-2">Collections</h3>
            <p className="text-gray-400">View and manage your collections</p>
          </Link>
          <Link href="/search" className="card text-center hover:border-amber-400">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="font-bold text-amber-400 mb-2">Discover</h3>
            <p className="text-gray-400">Explore the spirit catalog</p>
          </Link>
        </div>

        {/* Recent Bottles */}
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-amber-400">Recent Bottles</h2>
            <Link href="/bottles" className="text-amber-400 hover:text-amber-300">
              View All →
            </Link>
          </div>

          {bottles.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bottles.map((bottle) => (
                <BottleCard key={bottle.id} bottle={bottle} />
              ))}
            </div>
          ) : (
            <div className="card text-center">
              <p className="text-gray-400 mb-4">No bottles yet. Start building your collection!</p>
              <Link href="/bottles/new" className="btn-primary">
                Add Your First Bottle
              </Link>
            </div>
          )}
        </div>
      </div>
    </ClientLayout>
  );
}
