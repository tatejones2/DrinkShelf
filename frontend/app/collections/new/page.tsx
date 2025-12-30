'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import collectionService from '@/lib/services/collections';

interface CollectionFormData {
  name: string;
  description?: string;
  is_public: boolean;
}

export default function NewCollectionPage() {
  const router = useRouter();
  const { user, initializeAuth } = useAuthStore();
  const [formData, setFormData] = useState<CollectionFormData>({
    name: '',
    description: '',
    is_public: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
    }
  }, [user, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const collection = await collectionService.createCollection(formData);
      router.push(`/collections/${collection.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create collection');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) return null;

  return (
    <ClientLayout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-amber-400 mb-8">Create Collection</h1>

        <form onSubmit={handleSubmit} className="card space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Collection Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="input-field w-full"
              placeholder="e.g., Rare Whiskeys, Tequila Collection"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description || ''}
              onChange={handleChange}
              className="input-field w-full h-24"
              placeholder="Describe your collection..."
            />
          </div>

          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              name="is_public"
              checked={formData.is_public}
              onChange={handleChange}
              className="w-4 h-4 rounded"
            />
            <label className="text-gray-300">
              Make this collection public
            </label>
          </div>

          {error && (
            <div className="p-3 bg-red-900/30 border border-red-700 rounded text-red-400">
              {error}
            </div>
          )}

          <div className="flex gap-2">
            <button type="submit" disabled={isLoading} className="btn-primary flex-1">
              {isLoading ? 'Creating...' : 'Create Collection'}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </ClientLayout>
  );
}
