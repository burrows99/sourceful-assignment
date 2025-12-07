/**
 * CategoryDialog Component
 * 
 * A modal dialog for selecting categories on mobile devices.
 * Features full-screen overlay with grid of category options.
 */

'use client';

import { useEffect, type ReactNode } from 'react';
import { IconButton } from './IconButton';
import { Icon } from './Icon';
import { categories } from '@/lib/constants';

interface CategoryDialogProps {
  /** Whether the dialog is open */
  isOpen: boolean;
  /** Callback to close the dialog */
  onClose: () => void;
  /** Currently selected category ID */
  selectedCategory: string;
  /** Callback when category is selected */
  onCategorySelect: (categoryId: string) => void;
}

export function CategoryDialog({
  isOpen,
  onClose,
  selectedCategory,
  onCategorySelect
}: CategoryDialogProps) {
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

  const handleSelect = (categoryId: string) => {
    onCategorySelect(categoryId);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Full-screen Dialog */}
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="category-dialog-title"
        className="fixed inset-0 z-50 bg-white overflow-y-auto md:hidden"
      >
        {/* Header */}
        <div className="flex items-center justify-end p-6">
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

        {/* Category Grid */}
        <div className="px-6 pb-6">
          <div className="grid grid-cols-2 gap-4">
            {categories.map((category) => (
              <IconButton
                key={category.id}
                icon={<Icon name={category.icon} />}
                text={category.name}
                isSelected={selectedCategory === category.id}
                onClick={() => handleSelect(category.id)}
                className="w-full"
                aria-label={`Select ${category.name}`}
              />
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
