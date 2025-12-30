'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import authService, { User } from '@/lib/services/auth';

export default function ProfilePage() {
  const router = useRouter();
  const { user, initializeAuth, setUser } = useAuthStore();
  const [profile, setProfile] = useState<User | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    display_name: '',
    bio: '',
  });

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (!user) {
      router.push('/auth/login');
      return;
    }

    const loadProfile = async () => {
      try {
        const data = await authService.getCurrentUser();
        setProfile(data);
        setFormData({
          display_name: data.display_name || '',
          bio: data.bio || '',
        });
      } catch (err) {
        console.error('Failed to load profile:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, [user, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile) return;

    setError('');
    setIsSaving(true);

    try {
      const updated = await authService.updateProfile(profile.id, formData);
      setProfile(updated);
      setUser(updated);
      setIsEditing(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save profile');
    } finally {
      setIsSaving(false);
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

  if (!profile) return null;

  return (
    <ClientLayout>
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-amber-400 mb-8">My Profile</h1>

        <div className="card mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-2xl font-bold text-white">{profile.display_name || profile.username}</h2>
              <p className="text-gray-400">@{profile.username}</p>
            </div>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="btn-primary text-sm"
            >
              {isEditing ? '✕ Cancel' : '✏️ Edit'}
            </button>
          </div>

          <div className="space-y-4 border-t border-gray-700 pt-4">
            <div>
              <p className="text-gray-400 text-sm">Email</p>
              <p className="text-white">{profile.email}</p>
            </div>

            <div>
              <p className="text-gray-400 text-sm">Member Since</p>
              <p className="text-white">
                {new Date(profile.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </p>
            </div>

            {!isEditing && profile.bio && (
              <div>
                <p className="text-gray-400 text-sm">Bio</p>
                <p className="text-white">{profile.bio}</p>
              </div>
            )}
          </div>
        </div>

        {isEditing && (
          <form onSubmit={handleSave} className="card space-y-6">
            <h3 className="text-xl font-bold text-amber-400">Edit Profile</h3>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Display Name
              </label>
              <input
                type="text"
                name="display_name"
                value={formData.display_name}
                onChange={handleChange}
                className="input-field w-full"
                placeholder="How you want to be called"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Bio
              </label>
              <textarea
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                className="input-field w-full h-24"
                placeholder="Tell us about your spirit interests..."
              />
            </div>

            {error && (
              <div className="p-3 bg-red-900/30 border border-red-700 rounded text-red-400">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isSaving}
              className="btn-primary w-full"
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        )}

        {/* Account Info */}
        <div className="card">
          <h3 className="text-xl font-bold text-amber-400 mb-4">Account Information</h3>
          <div className="space-y-3 text-sm text-gray-400">
            <p>Username: <span className="text-white">{profile.username}</span></p>
            <p>Email: <span className="text-white">{profile.email}</span></p>
            <p>User ID: <span className="text-white font-mono text-xs">{profile.id}</span></p>
            <p>Last Updated: <span className="text-white">{new Date(profile.updated_at).toLocaleDateString()}</span></p>
          </div>
        </div>
      </div>
    </ClientLayout>
  );
}
