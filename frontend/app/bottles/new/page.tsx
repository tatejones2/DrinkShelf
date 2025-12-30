'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import bottleService, { Bottle } from '@/lib/services/bottles';

interface BottleFormData {
  name: string;
  spirit_type: string;
  distillery: string;
  region: string;
  country: string;
  proof: number;
  release_year?: number;
  batch_number?: string;
  price_paid?: number;
  price_current?: number;
  tasting_notes?: string;
  rating?: number;
  image_url?: string;
}

export default function BottleFormPage({ isEdit = false }: { isEdit?: boolean }) {
  const router = useRouter();
  const params = useParams();
  const { user, initializeAuth } = useAuthStore();
  const [formData, setFormData] = useState<BottleFormData>({
    name: '',
    spirit_type: 'whiskey',
    distillery: '',
    region: '',
    country: '',
    proof: 80,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    if (isEdit && params.id) {
      const loadBottle = async () => {
        try {
          const bottle = await bottleService.getBottle(params.id as string);
          setFormData({
            name: bottle.name,
            spirit_type: bottle.spirit_type,
            distillery: bottle.distillery,
            region: bottle.region,
            country: bottle.country,
            proof: bottle.proof,
            release_year: bottle.release_year,
            batch_number: bottle.batch_number,
            price_paid: bottle.price_paid,
            price_current: bottle.price_current,
            tasting_notes: bottle.tasting_notes,
            rating: bottle.rating,
            image_url: bottle.image_url,
          });
        } catch (err) {
          console.error('Failed to load bottle:', err);
          setError('Failed to load bottle');
        }
      };
      loadBottle();
    }
  }, [user, router, isEdit, params.id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || undefined : value || undefined,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isEdit && params.id) {
        await bottleService.updateBottle(params.id as string, formData);
        router.push(`/bottles/${params.id}`);
      } else {
        const newBottle = await bottleService.createBottle(formData);
        router.push(`/bottles/${newBottle.id}`);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save bottle');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) return null;

  return (
    <ClientLayout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-amber-400 mb-8">
          {isEdit ? 'Edit Bottle' : 'Add New Bottle'}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="card">
            <h2 className="text-xl font-bold text-amber-400 mb-4">Basic Information</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Bottle Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="input-field w-full"
                  placeholder="e.g., Macallan 18 Year Old"
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Spirit Type *
                  </label>
                  <select
                    name="spirit_type"
                    value={formData.spirit_type}
                    onChange={handleChange}
                    className="input-field w-full"
                    required
                  >
                    <option value="whiskey">Whiskey</option>
                    <option value="vodka">Vodka</option>
                    <option value="tequila">Tequila</option>
                    <option value="rum">Rum</option>
                    <option value="gin">Gin</option>
                    <option value="brandy">Brandy</option>
                    <option value="wine">Wine</option>
                    <option value="beer">Beer</option>
                    <option value="liqueur">Liqueur</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Proof *
                  </label>
                  <input
                    type="number"
                    name="proof"
                    value={formData.proof}
                    onChange={handleChange}
                    className="input-field w-full"
                    required
                    min="0"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Distillery *
                </label>
                <input
                  type="text"
                  name="distillery"
                  value={formData.distillery}
                  onChange={handleChange}
                  className="input-field w-full"
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Region *
                  </label>
                  <input
                    type="text"
                    name="region"
                    value={formData.region}
                    onChange={handleChange}
                    className="input-field w-full"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Country *
                  </label>
                  <input
                    type="text"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    className="input-field w-full"
                    required
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Additional Info */}
          <div className="card">
            <h2 className="text-xl font-bold text-amber-400 mb-4">Additional Information</h2>

            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Release Year
                  </label>
                  <input
                    type="number"
                    name="release_year"
                    value={formData.release_year || ''}
                    onChange={handleChange}
                    className="input-field w-full"
                    min="1900"
                    max={new Date().getFullYear()}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Batch Number
                  </label>
                  <input
                    type="text"
                    name="batch_number"
                    value={formData.batch_number || ''}
                    onChange={handleChange}
                    className="input-field w-full"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Price Paid ($)
                  </label>
                  <input
                    type="number"
                    name="price_paid"
                    value={formData.price_paid || ''}
                    onChange={handleChange}
                    className="input-field w-full"
                    step="0.01"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Current Value ($)
                  </label>
                  <input
                    type="number"
                    name="price_current"
                    value={formData.price_current || ''}
                    onChange={handleChange}
                    className="input-field w-full"
                    step="0.01"
                    min="0"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Your Rating (1-5)
                </label>
                <select
                  name="rating"
                  value={formData.rating || ''}
                  onChange={handleChange}
                  className="input-field w-full"
                >
                  <option value="">Not rated</option>
                  <option value="1">1 - Poor</option>
                  <option value="2">2 - Fair</option>
                  <option value="3">3 - Good</option>
                  <option value="4">4 - Very Good</option>
                  <option value="5">5 - Excellent</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Tasting Notes
                </label>
                <textarea
                  name="tasting_notes"
                  value={formData.tasting_notes || ''}
                  onChange={handleChange}
                  className="input-field w-full h-24"
                  placeholder="Describe the nose, palate, finish..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Image URL
                </label>
                <input
                  type="url"
                  name="image_url"
                  value={formData.image_url || ''}
                  onChange={handleChange}
                  className="input-field w-full"
                  placeholder="https://..."
                />
              </div>
            </div>
          </div>

          {error && (
            <div className="p-3 bg-red-900/30 border border-red-700 rounded text-red-400">
              {error}
            </div>
          )}

          <div className="flex gap-2">
            <button type="submit" disabled={isLoading} className="btn-primary flex-1">
              {isLoading ? 'Saving...' : isEdit ? 'Update Bottle' : 'Add Bottle'}
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
