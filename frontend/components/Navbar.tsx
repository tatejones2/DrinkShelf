'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store/auth-store';
import Link from 'next/link';

export default function Navbar() {
  const router = useRouter();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <nav className="bg-gray-950 border-b border-amber-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-amber-500">🍾</div>
            <span className="text-xl font-bold text-amber-500">DrinkShelf</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex space-x-6">
            <Link href="/search" className="hover:text-amber-400 transition-colors">
              Search
            </Link>
            {user ? (
              <>
                <Link href="/dashboard" className="hover:text-amber-400 transition-colors">
                  Dashboard
                </Link>
                <Link href="/bottles" className="hover:text-amber-400 transition-colors">
                  My Bottles
                </Link>
                <Link href="/collections" className="hover:text-amber-400 transition-colors">
                  Collections
                </Link>
                <Link href="/profile" className="hover:text-amber-400 transition-colors">
                  Profile
                </Link>
              </>
            ) : null}
          </div>

          {/* Auth Section */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-sm text-gray-400">{user.username}</span>
                <button
                  onClick={handleLogout}
                  className="btn-secondary text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/auth/login" className="hover:text-amber-400 transition-colors">
                  Login
                </Link>
                <Link href="/auth/register" className="btn-primary text-sm">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
