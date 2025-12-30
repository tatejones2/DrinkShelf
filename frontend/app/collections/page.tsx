'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import collectionService, { Collection } from '@/lib/services/collections';
import Link from 'next/link';

export default function CollectionsPage() {
  const router = useRouter();
  const { user, initializeAuth } = useAuthStore();
  const [collections, setCollections] = useState<Collection[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    const loadCollections = async () => {
      try {
        const data = await collectionService.getCollections();
        setCollections(data);
      } catch (error) {
        console.error('Failed to load collections:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadCollections();
  }, [user, router]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this collection?')) return;
    try {
      await collectionService.deleteCollection(id);
      setCollections(collections.filter(c => c.id !== id));
    } catch (error) {
      console.error('Failed to delete collection:', error);
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
          <h1 className="text-4xl font-bold text-amber-400">Collections</h1>
          <Link href="/collections/new" className="btn-primary">
            ➕ New Collection
          </Link>
        </div>

        {/* Collections Grid */}
        {collections.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {collections.map((collection) => (
              <Link
                key={collection.id}
                href={`/collections/${collection.id}`}
                className="card hover:border-amber-400 transition-all hover:shadow-xl"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-amber-400">{collection.name}</h3>
                  {collection.is_public && (
                    <span className="text-xs px-2 py-1 bg-amber-700/30 border border-amber-600 rounded text-amber-400">
                      Public
                    </span>
                  )}
                </div>

                {collection.description && (
                  <p className="text-gray-400 mb-4 line-clamp-3">{collection.description}</p>
                )}

                <div className="text-sm text-gray-500">
                  Created {new Date(collection.created_at).toLocaleDateString()}
                </div>

                <div className="mt-4 flex gap-2">
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      handleDelete(collection.id);
                    }}
                    className="btn-secondary text-sm flex-1"
                  >
                    Delete
                  </button>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="card text-center">
            <p className="text-gray-400 mb-4">No collections yet.</p>
            <Link href="/collections/new" className="btn-primary">
              Create Your First Collection
            </Link>
          </div>
        )}
      </div>
    </ClientLayout>
  );
}
