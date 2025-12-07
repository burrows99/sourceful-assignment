/**
 * AuthTestButtons Component
 * 
 * Test buttons for signing in and out during development
 */

'use client';

import { useAuth } from '@/lib/auth-context';

export function AuthTestButtons() {
  const { user, isAuthenticated, credits, signIn, signOut } = useAuth();

  const handleSignIn = async () => {
    await signIn('test@example.com', 'password123');
  };

  return (
    <div className="flex items-center justify-end gap-4 p-4">
      {isAuthenticated ? (
        <div className="flex items-center gap-4">
          <span className="text-white text-sm">
            Signed in as: <strong>{user?.email}</strong> | Credits: <strong>{credits}</strong>
          </span>
          <button
            onClick={signOut}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Sign Out
          </button>
        </div>
      ) : (
        <button
          onClick={handleSignIn}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Sign In (Test)
        </button>
      )}
    </div>
  );
}
