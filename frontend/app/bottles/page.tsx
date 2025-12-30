'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import BottleCard from '@/components/BottleCard';
import bottleService, { Bottle } from '@/lib/services/bottles';
import Link from 'next/link';

export default function MyBottlesPage() {
  const router = useRouter();
  const { user, initializeAuth } = useAuthStore();
  const [bottles, setBottles] = useState<Bottle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [spiritFilter, setSpiritFilter] = useState('');

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    const loadBottles = async () => {
      try {
        const data = await bottleService.getBottles(0, 50, spiritFilter || undefined);
        setBottles(data);
      } catch (error) {
        console.error('Failed to load bottles:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadBottles();
  }, [user, router, spiritFilter]);

  const handleDelete = async (id: string) => {
    try {
      await bottleService.deleteBottle(id);
      setBottles(bottles.filter(b => b.id !== id));
    } catch (error) {
      console.error('Failed to delete bottle:', error);
    }
  };

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
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-amber-400">My Bottles</h1>
          <Link href="/bottles/new" className="btn-primary">
            ➕ Add Bottle
          </Link>
        </div>

        {/* Filters */}
        <div className="card mb-8">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Filter by Spirit Type
              </label>
              <select
                value={spiritFilter}
                onChange={(e) => setSpiritFilter(e.target.value)}
                className="input-field w-full"
              >
                <option value="">All Types</option>
                <option value="whiskey">Whiskey</option>
                <option value="vodka">Vodka</option>
                <option value="tequila">Tequila</option>
                <option value="rum">Rum</option>
                <option value="gin">Gin</option>
                <option value="brandy">Brandy</option>
                <option value="wine">Wine</option>
              </select>
            </div>
          </div>
        </div>

        {/* Bottles Grid */}
        {bottles.length > 0 ? (
          <div>
            <p className="text-gray-400 mb-6">{bottles.length} bottles in your collection</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bottles.map((bottle) => (
                <BottleCard
                  key={bottle.id}
                  bottle={bottle}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          </div>
        ) : (
          <div className="card text-center">
            <p className="text-gray-400 mb-4">No bottles yet.</p>
            <Link href="/bottles/new" className="btn-primary">
              Add Your First Bottle
            </Link>
          </div>
        )}
      </div>
    </ClientLayout>
  );
}
