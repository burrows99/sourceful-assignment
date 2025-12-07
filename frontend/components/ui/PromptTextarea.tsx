/**
 * PromptTextarea Component
 * 
 * A textarea input for entering prompts with custom styling.
 * Features transparent background and placeholder text.
 */

'use client';

import { type TextareaHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface PromptTextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  /** Placeholder text to display */
  placeholder?: string;
}

export function PromptTextarea({ 
  placeholder = "Describe your vision...",
  className,
  ...props 
}: PromptTextareaProps) {
  return (
    <textarea
      placeholder={placeholder}
      className={cn(
        "w-full outline-none border-0 resize-none max-h-28 bg-transparent",
        "text-neutral-900 placeholder:text-neutral-400",
        className
      )}
      maxLength={10000}
      rows={4}
      {...props}
    />
  );
}
