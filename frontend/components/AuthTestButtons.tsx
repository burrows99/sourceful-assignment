/**
 * AuthTestButtons Component
 * 
 * Test buttons for signing in and out during development
 */

'use client';

import { useAuth } from '@/lib/auth-context';
import { cn } from '@/lib/utils';

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
    <div className="flex items-center justify-end gap-4 py-4">
      <div className="flex items-center gap-3 bg-transparent backdrop-blur-sm rounded-full px-5 py-2.5">
        {isAuthenticated ? (
          <>
            <span className="font-space-grotesk text-sm font-medium text-gray-900">
              {user?.email}
            </span>
            <div className="flex items-center gap-2">
              <label htmlFor="credits-input" className="font-space-grotesk text-sm font-medium text-gray-700">
                Credits:
              </label>
              <input
                id="credits-input"
                type="number"
                value={credits}
                onChange={handleCreditsChange}
                min="0"
                className={cn(
                  "w-20 h-8 px-3 rounded-full border border-gray-200",
                  "bg-white text-gray-900 font-space-grotesk text-sm",
                  "focus:outline-none focus:ring-2 focus:ring-[#8f00ff] focus:border-transparent",
                  "transition duration-200"
                )}
              />
            </div>
            <button
              onClick={signOut}
              className={cn(
                "relative overflow-hidden appearance-none inline-flex items-center justify-center",
                "h-8 px-4 rounded-full",
                "bg-gradient-to-br from-red-500 to-red-600 text-white",
                "hover:from-red-600 hover:to-red-700",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-red-500",
                "transition duration-200",
                "font-space-grotesk text-sm font-medium whitespace-nowrap"
              )}
            >
              Sign Out
            </button>
          </>
        ) : (
          <button
            onClick={handleSignIn}
            className={cn(
              "relative overflow-hidden appearance-none inline-flex items-center justify-center",
              "h-8 px-4 rounded-full",
              "bg-gradient-to-br from-[#8f00ff] from-10% to-[#0038ff] text-white",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500",
              "transition duration-200",
              "font-space-grotesk text-sm font-medium whitespace-nowrap",
              "before:opacity-0 hover:before:opacity-100 focus:before:opacity-100",
              "before:transition-opacity before:duration-200",
              "before:absolute before:inset-0",
              "before:bg-gradient-to-br before:from-[#8f00ff] before:from-40% before:to-[#0038ff]"
            )}
          >
            <span className="relative">Sign In</span>
          </button>
        )}
      </div>
    </div>
  );
}
