'use client';

import { Bottle } from '@/lib/services/bottles';
import Link from 'next/link';
import { useState } from 'react';

interface BottleCardProps {
  bottle: Bottle;
  onDelete?: (id: string) => void;
}

export default function BottleCard({ bottle, onDelete }: BottleCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this bottle?')) return;
    setIsDeleting(true);
    try {
      await onDelete?.(bottle.id);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="card hover:border-amber-500 transition-all hover:shadow-xl">
      {bottle.image_url && (
        <div className="mb-4 h-48 bg-gray-800 rounded overflow-hidden">
          <img
            src={bottle.image_url}
            alt={bottle.name}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      <h3 className="text-lg font-bold text-amber-400 mb-2">{bottle.name}</h3>

      <div className="space-y-1 text-sm text-gray-300 mb-4">
        <p>
          <span className="text-amber-500">Distillery:</span> {bottle.distillery}
        </p>
        <p>
          <span className="text-amber-500">Region:</span> {bottle.region}, {bottle.country}
        </p>
        <p>
          <span className="text-amber-500">Type:</span> {bottle.spirit_type}
        </p>
        <p>
          <span className="text-amber-500">Proof:</span> {bottle.proof}
        </p>
      </div>

      {bottle.rating && (
        <div className="mb-4 pb-4 border-b border-gray-700">
          <div className="flex items-center">
            <span className="text-2xl font-bold text-amber-400">{bottle.rating}</span>
            <span className="text-gray-400 ml-2">/ 5.0</span>
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <Link
          href={`/bottles/${bottle.id}`}
          className="flex-1 btn-primary text-center text-sm"
        >
          View Details
        </Link>
        {onDelete && (
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="flex-1 btn-secondary text-sm opacity-70 hover:opacity-100"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        )}
      </div>
    </div>
  );
}
