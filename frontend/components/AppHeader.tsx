/**
 * AppHeader Component
 * 
 * Transparent header for app navigation and auth controls
 */

'use client';

import { AuthTestButtons } from './AuthTestButtons';

export function AppHeader() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-transparent">
      <div className="container mx-auto px-4">
        <AuthTestButtons />
      </div>
    </header>
  );
}
