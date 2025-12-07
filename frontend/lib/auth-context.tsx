/**
 * Auth Context Provider
 * 
 * Client-side authentication context for managing user session state
 */

'use client';

import { createContext, useContext, useState, type ReactNode } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  credits: number;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  credits: number;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const signIn = async (email: string, password: string) => {
    // Stub: In production, this would call your authentication API
    // For now, we'll just set a mock user
    const mockUser: User = {
      id: '1',
      name: 'Test User',
      email: email,
      credits: 10,
    };
    setUser(mockUser);
  };

  const signOut = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        credits: user?.credits ?? 0,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
