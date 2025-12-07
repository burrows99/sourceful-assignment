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
        "relative overflow-hidden appearance-none inline-flex items-center justify-center",
        "h-10 px-4 rounded-full",
        "bg-gradient-to-br from-[#8f00ff] from-10% to-[#0038ff] text-white",
        "disabled:from-gray-50 disabled:to-gray-50 disabled:text-gray-400",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500",
        "transition duration-200",
        "text-sm font-medium whitespace-nowrap",
        "before:opacity-0 hover:before:opacity-100 focus:before:opacity-100",
        "before:transition-opacity before:duration-200",
        "before:absolute before:inset-0",
        "before:bg-gradient-to-br before:from-[#8f00ff] before:from-40% before:to-[#0038ff]",
        "disabled:before:!bg-none",
        "w-full md:w-fit",
        className
      )}
      {...props}
    >
      <span className="font-space-grotesk tracking-normal text-inherit text-sm leading-5 md:text-sm md:leading-5 lg:text-[15px] lg:leading-5 xl:text-[15px] xl:leading-5 font-medium inline-flex px-0.5 relative">
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
        className="w-6 h-6 ml-2 relative"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <path d="m12 16 4-4-4-4" />
        <path d="M8 12h8" />
      </svg>
    </button>
  );
}
