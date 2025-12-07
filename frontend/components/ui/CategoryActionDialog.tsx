/**
 * CategoryActionDialog Component
 * 
 * Mock dialog that shows when certain categories are selected.
 * Simple placeholder for demonstration purposes.
 */

'use client';

import { useEffect } from 'react';

interface CategoryActionDialogProps {
  /** Whether the dialog is open */
  isOpen: boolean;
  /** Callback to close the dialog */
  onClose: () => void;
  /** Category name to display */
  categoryName: string;
}

export function CategoryActionDialog({
  isOpen,
  onClose,
  categoryName
}: CategoryActionDialogProps) {
  // Close on escape key
  useEffect(() => {
    if (!isOpen) return;
    
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Prevent body scroll when dialog is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <>
      {/* Mobile: Full-screen Dialog */}
      <div
        role="dialog"
        aria-modal="true"
        className="fixed inset-0 z-50 bg-white/95 backdrop-blur-md overflow-y-auto md:hidden"
      >
        <div className="flex items-center justify-between p-6">
          <h2 className="text-lg font-semibold text-neutral-900">
            {categoryName}
          </h2>
          <button
            onClick={onClose}
            className="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-neutral-100 transition-colors"
            aria-label="Close dialog"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-5 h-5"
            >
              <path d="M18 6 6 18" />
              <path d="m6 6 12 12" />
            </svg>
          </button>
        </div>

        <div className="px-6 pb-6">
          <p className="text-neutral-600">Mock dialog content for {categoryName}</p>
        </div>
      </div>

      {/* Desktop: Centered Dialog */}
      <div className="hidden md:block">
        <div
          className="fixed inset-0 backdrop-blur-md bg-black/30 z-40"
          onClick={onClose}
          aria-hidden="true"
        />

        <div
          role="dialog"
          aria-modal="true"
          className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-white rounded-4xl p-8 w-full max-w-2xl"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-neutral-900">
              {categoryName}
            </h2>
            <button
              onClick={onClose}
              className="inline-flex items-center justify-center w-10 h-10 rounded-full hover:bg-neutral-100 transition-colors"
              aria-label="Close dialog"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-5 h-5"
              >
                <path d="M18 6 6 18" />
                <path d="m6 6 12 12" />
              </svg>
            </button>
          </div>

          <p className="text-neutral-600">Mock dialog content for {categoryName}</p>
        </div>
      </div>
    </>
  );
}
