'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import ClientLayout from '@/components/ClientLayout';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter();
  const { user, login, error, isLoading } = useAuthStore();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState('');

  useEffect(() => {
    if (user) {
      router.push('/dashboard');
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError('');

    try {
      await login(username, password);
      router.push('/dashboard');
    } catch (err: any) {
      setLocalError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <ClientLayout>
      <div className="flex items-center justify-center min-h-screen py-12 px-4">
        <div className="card w-full max-w-md">
          <h1 className="text-3xl font-bold text-amber-400 mb-8 text-center">Login</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Username or Email
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field w-full"
                placeholder="Enter your username or email"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field w-full"
                placeholder="Enter your password"
                required
              />
            </div>

            {(localError || error) && (
              <div className="p-3 bg-red-900/30 border border-red-700 rounded text-red-400 text-sm">
                {localError || error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? 'Logging in...' : 'Log In'}
            </button>
          </form>

          <div className="mt-6 text-center text-gray-400">
            Don't have an account?{' '}
            <Link href="/auth/register" className="text-amber-400 hover:text-amber-300">
              Sign up
            </Link>
          </div>
        </div>
      </div>
    </ClientLayout>
  );
}
