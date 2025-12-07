/**
 * AuthTestButtons Component
 * 
 * Test buttons for signing in and out during development
 */

'use client';

import { useAuth } from '@/lib/auth-context';

export function AuthTestButtons() {
  const { user, isAuthenticated, credits, signIn, signOut, setCredits } = useAuth();

  const handleSignIn = async () => {
    await signIn('test@example.com', 'password123');
  };

  const handleCreditsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value)) {
      setCredits(value);
    }
  };

  return (
    <div className="flex items-center justify-end gap-4 p-4">
      {isAuthenticated ? (
        <div className="flex items-center gap-4">
          <span className="text-white text-sm">
            Signed in as: <strong>{user?.email}</strong>
          </span>
          <div className="flex items-center gap-2">
            <label htmlFor="credits-input" className="text-white text-sm">
              Credits:
            </label>
            <input
              id="credits-input"
              type="number"
              value={credits}
              onChange={handleCreditsChange}
              min="0"
              className="w-20 px-2 py-1 bg-white text-gray-900 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
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
