/**
 * FileUploadButton Component
 * 
 * A circular button with a plus icon for uploading files.
 * Features black background with white icon.
 */

'use client';

import { useRef, type ChangeEvent } from 'react';
import { cn } from '@/lib/utils';

interface FileUploadButtonProps {
  /** Callback when file is selected */
  onFileSelect?: (file: File) => void;
  /** Optional custom class name */
  className?: string;
  /** Optional custom aria label */
  'aria-label'?: string;
}

export function FileUploadButton({ 
  onFileSelect,
  className,
  'aria-label': ariaLabel = "Upload reference image"
}: FileUploadButtonProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && onFileSelect) {
      onFileSelect(file);
    }
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
        aria-hidden="true"
      />
      <button
        type="button"
        onClick={handleClick}
        className={cn(
          "inline-flex items-center justify-center w-10 h-10 rounded-full",
          "bg-black text-white",
          "hover:bg-neutral-600",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-neutral-900",
          "transition-colors duration-200",
          "group/button",
          className
        )}
        aria-label={ariaLabel}
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
          className="w-6 h-6 transition-transform group-hover/button:scale-110"
          aria-hidden="true"
        >
          <path d="M5 12h14" />
          <path d="M12 5v14" />
        </svg>
      </button>
    </>
  );
}
