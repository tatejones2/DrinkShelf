'use client';

import { useState, useEffect } from 'react';
import ClientLayout from '@/components/ClientLayout';
import BottleCard from '@/components/BottleCard';
import bottleService, { Bottle } from '@/lib/services/bottles';
import Link from 'next/link';

export default function SearchPage() {
  const [bottles, setBottles] = useState<Bottle[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [spiritType, setSpiritType] = useState('');
  const [priceMin, setPriceMin] = useState('');
  const [priceMax, setPriceMax] = useState('');
  const [ratingMin, setRatingMin] = useState('');
  const [region, setRegion] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (query) {
        const results = await bottleService.searchBottles(query);
        setBottles(results);
      } else {
        const results = await bottleService.filterBottles({
          spirit_type: spiritType || undefined,
          price_min: priceMin ? parseFloat(priceMin) : undefined,
          price_max: priceMax ? parseFloat(priceMax) : undefined,
          rating_min: ratingMin ? parseFloat(ratingMin) : undefined,
          region: region || undefined,
          limit: 50,
        });
        setBottles(results.bottles);
      }
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ClientLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-4xl font-bold text-amber-400 mb-8">Explore Catalog</h1>

        {/* Search Form */}
        <div className="card mb-8">
          <form onSubmit={handleSearch} className="space-y-4">
            {/* Quick Search */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Quick Search
              </label>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search bottles by name, distillery..."
                className="input-field w-full"
              />
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Spirit Type
                </label>
                <select
                  value={spiritType}
                  onChange={(e) => setSpiritType(e.target.value)}
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

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Min Rating
                </label>
                <input
                  type="number"
                  min="0"
                  max="5"
                  step="0.5"
                  value={ratingMin}
                  onChange={(e) => setRatingMin(e.target.value)}
                  placeholder="3.0"
                  className="input-field w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Price Range ($)
                </label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    value={priceMin}
                    onChange={(e) => setPriceMin(e.target.value)}
                    placeholder="Min"
                    className="input-field w-1/2"
                  />
                  <input
                    type="number"
                    value={priceMax}
                    onChange={(e) => setPriceMax(e.target.value)}
                    placeholder="Max"
                    className="input-field w-1/2"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Region
                </label>
                <input
                  type="text"
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  placeholder="Scotland, Kentucky..."
                  className="input-field w-full"
                />
              </div>
            </div>

            <button type="submit" disabled={isLoading} className="btn-primary w-full">
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>

        {/* Results */}
        {bottles.length > 0 ? (
          <div>
            <p className="text-gray-400 mb-4">Found {bottles.length} bottles</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bottles.map((bottle) => (
                <BottleCard key={bottle.id} bottle={bottle} />
              ))}
            </div>
          </div>
        ) : (
          <div className="card text-center">
            <p className="text-gray-400">
              {isLoading ? 'Searching...' : 'No bottles found. Try different search criteria.'}
            </p>
          </div>
        )}
      </div>
    </ClientLayout>
  );
}
