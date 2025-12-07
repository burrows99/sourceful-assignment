/**
 * PromptSubmitButton Component
 * 
 * A reusable gradient purple button with enabled/disabled states
 */

'use client';

import { type ButtonHTMLAttributes, type ReactNode } from 'react';

interface PromptSubmitButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Text to display when authenticated */
  authenticatedText: string;
  /** Text to display when not authenticated */
  unauthenticatedText: string;
  /** Whether user is authenticated */
  isAuthenticated: boolean;
  /** Whether the button is enabled */
  enabled?: boolean;
  /** Icon to display (optional) */
  icon?: ReactNode;
  /** Credit cost badge content (optional, only shown when authenticated) */
  creditBadge?: {
    amount: number;
    icon?: ReactNode;
  };
  /** Whether to show full width on mobile */
  fullWidthMobile?: boolean;
}

export function PromptSubmitButton({
  authenticatedText,
  unauthenticatedText,
  isAuthenticated,
  enabled = true,
  icon,
  creditBadge,
  fullWidthMobile = true,
  className = '',
  type = 'submit',
  ...props
}: PromptSubmitButtonProps) {
  const displayText = isAuthenticated ? authenticatedText : unauthenticatedText;
  
  return (
    <button
      data-button=""
      className={`relative overflow-hidden appearance-none inline-flex items-center rounded-pill justify-center box-border transition duration-200 [&>svg]:relative focus-visible:focus-ring disabled:cursor-not-allowed h-40 [&>svg]:w-24 [&>svg]:h-24 [&>svg:first-child]:mr-8 [&>svg:last-child]:ml-8 px-16 bg-gradient-to-br from-ui-violet-700 from-10% to-ui-blue-700 text-ui-lightest disabled:from-ui-grey-50 disabled:to-ui-grey-50 disabled:text-ui-grey-400 dark:disabled:from-transparent dark:disabled:to-transparent dark:disabled:text-ui-grey-600 before:opacity-0 before:hover:opacity-100 before:focus:opacity-100 before:transition-opacity before:duration-200 before:absolute before:inset-0 before:bg-gradient-to-br before:from-ui-violet-700 before:from-40% before:to-ui-blue-700 ${fullWidthMobile ? 'w-full md:w-fit' : 'w-fit'} disabled:before:!bg-none ${className}`}
      type={type}
      disabled={!enabled}
      data-state="closed"
      {...props}
    >
      {/* Icon */}
      {icon}
      
      {/* Button Text - Hidden on mobile if full width */}
      <span
        className="font-space-grotesk tracking-normal text-inherit text-14 leading-20 md:text-14 md:leading-20 lg:text-15 lg:leading-20 xl:text-15 xl:leading-20 font-medium px-2 relative hidden md:block"
        data-text-label=""
        data-button-text=""
      >
        {displayText}
      </span>
      
      {/* Credit Badge - Only shown when authenticated */}
      {isAuthenticated && creditBadge && (
        <span className="inline-flex items-center border-2 rounded-pill !pr-2 h-24 px-12 [&>svg]:w-20 [&>svg]:h-20 bg-ui-lightest border-ui-lightest mx-4 [&>svg:first-child]:mr-2 [&>svg:last-child]:ml-2 !text-ui-grey-950 disabled:opacity-100 disabled:pointer-events-auto relative z-10 flex-shrink-0">
          <span
            className="font-space-grotesk tracking-normal text-inherit text-14 leading-20 md:text-14 md:leading-20 lg:text-15 lg:leading-20 xl:text-15 xl:leading-20 font-medium"
            data-text-label=""
          >
            {creditBadge.amount}
            <span className="sr-only">credits required</span>
          </span>
          {creditBadge.icon || (
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
              className="lucide lucide-coins"
              aria-hidden="true"
            >
              <circle cx="8" cy="8" r="6" />
              <path d="M18.09 10.37A6 6 0 1 1 10.34 18" />
              <path d="M7 6h1v4" />
              <path d="m16.71 13.88.7.71-2.82 2.82" />
            </svg>
          )}
        </span>
      )}
    </button>
  );
}
