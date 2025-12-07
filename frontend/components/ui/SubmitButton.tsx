/**
 * SubmitButton Component
 * 
 * A gradient button with icon for submitting forms.
 * Features purple-to-blue gradient background with responsive text.
 */

'use client';

import { type ButtonHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface SubmitButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button text label */
  children: string;
  /** Optional extended text visible on desktop */
  extendedText?: string;
}

export function SubmitButton({ 
  children,
  extendedText,
  className,
  ...props 
}: SubmitButtonProps) {
  return (
    <button
      type="submit"
      className={cn(
        "relative overflow-hidden inline-flex items-center justify-center",
        "h-10 px-4 rounded-full",
        "bg-linear-to-br from-purple-600 to-blue-600 text-white",
        "hover:from-purple-700 hover:to-blue-700",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500",
        "transition-all duration-200",
        "text-sm font-medium whitespace-nowrap",
        className
      )}
      {...props}
    >
      <span className="relative">
        {children}
        {extendedText && (
          <span className="hidden md:inline">&nbsp;{extendedText}</span>
        )}
      </span>
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
        className="w-6 h-6 ml-2"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="m12 16 4-4-4-4" />
        <path d="M8 12h8" />
      </svg>
    </button>
  );
}
