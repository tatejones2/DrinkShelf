'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import bottleService, { Bottle } from '@/lib/services/bottles';
import tastingNoteService, { TastingNote, BottleReviewSummary } from '@/lib/services/tasting-notes';
import Link from 'next/link';

export default function BottleDetailPage() {
  const router = useRouter();
  const params = useParams();
  const { user, initializeAuth } = useAuthStore();
  const [bottle, setBottle] = useState<Bottle | null>(null);
  const [tastingNotes, setTastingNotes] = useState<TastingNote[]>([]);
  const [summary, setSummary] = useState<BottleReviewSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleting, setIsDeleting] = useState(false);

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
        const bottleId = params.id as string;
        const [bottleData, notesData, summaryData] = await Promise.all([
          bottleService.getBottle(bottleId),
          tastingNoteService.getTastingNotes(bottleId),
          tastingNoteService.getBottleStats(bottleId),
        ]);
        setBottle(bottleData);
        setTastingNotes(notesData);
        setSummary(summaryData);
      } catch (error) {
        console.error('Failed to load bottle:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [user, router, params]);

  const handleDelete = async () => {
    if (!bottle || !confirm('Are you sure you want to delete this bottle?')) return;
    setIsDeleting(true);
    try {
      await bottleService.deleteBottle(bottle.id);
      router.push('/bottles');
    } catch (error) {
      console.error('Failed to delete bottle:', error);
      setIsDeleting(false);
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

  if (!bottle) {
    return (
      <ClientLayout>
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="card text-center">
            <p className="text-gray-400 mb-4">Bottle not found</p>
            <Link href="/bottles" className="btn-primary">
              Back to My Bottles
            </Link>
          </div>
        </div>
      </ClientLayout>
    );
  }

  return (
    <ClientLayout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <div className="mb-6">
          <Link href="/bottles" className="text-amber-400 hover:text-amber-300">
            ← Back to My Bottles
          </Link>
        </div>

        {/* Bottle Header */}
        <div className="card mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-4xl font-bold text-amber-400 mb-2">{bottle.name}</h1>
              <p className="text-xl text-gray-300">{bottle.distillery}</p>
            </div>
            <div className="text-right">
              {bottle.rating && (
                <div className="text-center">
                  <div className="text-5xl font-bold text-amber-400">{bottle.rating}</div>
                  <div className="text-gray-400">Your Rating</div>
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div>
              <p className="text-gray-400 text-sm">Spirit Type</p>
              <p className="text-white font-semibold">{bottle.spirit_type}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Proof</p>
              <p className="text-white font-semibold">{bottle.proof}°</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Region</p>
              <p className="text-white font-semibold">{bottle.region}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Country</p>
              <p className="text-white font-semibold">{bottle.country}</p>
            </div>
          </div>

          {bottle.release_year && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div>
                <p className="text-gray-400 text-sm">Release Year</p>
                <p className="text-white font-semibold">{bottle.release_year}</p>
              </div>
              {bottle.batch_number && (
                <div>
                  <p className="text-gray-400 text-sm">Batch Number</p>
                  <p className="text-white font-semibold">{bottle.batch_number}</p>
                </div>
              )}
              {bottle.price_paid && (
                <div>
                  <p className="text-gray-400 text-sm">Price Paid</p>
                  <p className="text-white font-semibold">${bottle.price_paid}</p>
                </div>
              )}
              {bottle.price_current && (
                <div>
                  <p className="text-gray-400 text-sm">Current Value</p>
                  <p className="text-white font-semibold">${bottle.price_current}</p>
                </div>
              )}
            </div>
          )}

          <div className="flex gap-2">
            <Link href={`/bottles/${bottle.id}/edit`} className="btn-primary">
              ✏️ Edit
            </Link>
            <button onClick={handleDelete} disabled={isDeleting} className="btn-secondary">
              {isDeleting ? 'Deleting...' : '🗑️ Delete'}
            </button>
          </div>
        </div>

        {/* Community Reviews */}
        {summary && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-amber-400 mb-4">Community Reviews</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded">
                <p className="text-gray-400 text-sm">Average Rating</p>
                <p className="text-3xl font-bold text-amber-400">
                  {summary.average_rating.toFixed(1)}/5
                </p>
              </div>
              <div className="bg-gray-800 p-4 rounded">
                <p className="text-gray-400 text-sm">Total Ratings</p>
                <p className="text-3xl font-bold text-amber-400">{summary.total_ratings}</p>
              </div>
              <div className="bg-gray-800 p-4 rounded">
                <p className="text-gray-400 text-sm">Rating Distribution</p>
                <div className="flex gap-1 mt-2">
                  {[5, 4, 3, 2, 1].map((rating) => (
                    <div key={rating} className="text-xs">
                      {summary.rating_distribution[rating] || 0}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tasting Notes */}
        <div className="card mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-amber-400">Tasting Notes</h2>
            <Link href={`/bottles/${bottle.id}/tasting-note/new`} className="btn-primary text-sm">
              ➕ Add Note
            </Link>
          </div>

          {tastingNotes.length > 0 ? (
            <div className="space-y-4">
              {tastingNotes.map((note) => (
                <div key={note.id} className="bg-gray-800 p-4 rounded border border-gray-700">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex gap-2">
                      <div className="text-3xl font-bold text-amber-400">{note.rating}</div>
                      <div>
                        <p className="text-white font-semibold">Your Rating</p>
                        <p className="text-gray-400 text-sm">{new Date(note.tasted_date).toLocaleDateString()}</p>
                      </div>
                    </div>
                    <Link
                      href={`/bottles/${bottle.id}/tasting-note/${note.id}`}
                      className="text-amber-400 hover:text-amber-300 text-sm"
                    >
                      Edit
                    </Link>
                  </div>
                  <div className="space-y-2 text-gray-300">
                    {note.nose && (
                      <p>
                        <span className="font-semibold text-amber-400">Nose:</span> {note.nose}
                      </p>
                    )}
                    {note.palate && (
                      <p>
                        <span className="font-semibold text-amber-400">Palate:</span> {note.palate}
                      </p>
                    )}
                    {note.finish && (
                      <p>
                        <span className="font-semibold text-amber-400">Finish:</span> {note.finish}
                      </p>
                    )}
                    {note.overall_notes && (
                      <p>
                        <span className="font-semibold text-amber-400">Overall:</span> {note.overall_notes}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 mb-4">No tasting notes yet. Be the first to add one!</p>
          )}
        </div>
      </div>
    </ClientLayout>
  );
}
