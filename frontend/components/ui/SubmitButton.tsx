/**
 * SubmitButton Component
 * 
 * A gradient button with icon for submitting forms.
 * Features purple-to-blue gradient background with responsive text.
 * Displays different text based on authentication state.
 */

'use client';

import { type ButtonHTMLAttributes, useState } from 'react';
import { cn } from '@/lib/utils';
import { useButtonState } from '@/hooks/useButtonState';
import { ButtonTooltip } from './ButtonTooltip';

export interface PromptSubmitButton {
  buttonText: string;
  iconSide?: 'left' | 'right';
  shouldToggleDisabled?: boolean;
  forceDisabled?: boolean;
  isFeatureAvailable?: (credits: number) => boolean;
  requiredCredits?: number;
  buttonTextOverrideIfLowCredits?: string;
}

interface SubmitButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Prompt submit button configuration */
  promptSubmitButton?: PromptSubmitButton;
}

export function SubmitButton({ 
  promptSubmitButton,
  className,
  ...props 
}: SubmitButtonProps) {
  const { buttonText, iconSide, isDisabled, showCreditBadge, credits, featureAvailable, buttonTextOverride } = useButtonState(promptSubmitButton);
  const [showTooltip, setShowTooltip] = useState(false);
  
  const shouldShowTooltip = featureAvailable === false && buttonTextOverride;
  
  return (
    <div 
      className="relative inline-block w-full md:w-fit"
      onMouseEnter={() => shouldShowTooltip && setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <button
        type="submit"
        disabled={isDisabled}
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
        "[&>svg]:relative [&>svg]:w-6 [&>svg]:h-6",
        className
      )}
      {...props}
    >
      {iconSide === 'left' && (
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="1em" 
          height="1em" 
          fill="none" 
          viewBox="0 0 48 48"
          className="w-6 h-6 mr-2 relative"
          aria-hidden="true"
        >
          <g fill="currentColor">
            <path fillRule="evenodd" d="M8.56 22v4C16 26 22.72 33.645 22.72 44h4c0-10.355 6.722-18 14.16-18v-4c-7.438 0-14.16-7.645-14.16-18h-4c0 10.355-6.721 18-14.16 18Zm24.704 2c-3.73 2.083-6.715 5.644-8.544 9.974-1.828-4.33-4.813-7.891-8.543-9.974 3.73-2.083 6.715-5.644 8.544-9.974 1.828 4.33 4.813 7.891 8.543 9.974Z" clipRule="evenodd"/>
            <path d="M42.36 8.28a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM9 14.3a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM38.02 39.42a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
          </g>
        </svg>
      )}
      <span className="font-space-grotesk tracking-normal text-inherit text-sm leading-5 md:text-sm md:leading-5 lg:text-[15px] lg:leading-5 xl:text-[15px] xl:leading-5 font-medium inline-flex px-0.5 relative">
        {buttonText}
      </span>
      {iconSide === 'right' && !showCreditBadge && (
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
      )}
      {showCreditBadge && (
        <span className="inline-flex items-center border-2 rounded-full !pr-2 h-6 px-3 bg-white border-white mx-1 text-gray-950 disabled:opacity-100 disabled:pointer-events-auto relative z-10 flex-shrink-0">
          <span className="font-space-grotesk tracking-normal text-inherit text-sm leading-5 font-medium">
            {credits}
            <span className="sr-only">credits available</span>
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
            className="w-5 h-5 ml-0.5"
            aria-hidden="true"
          >
            <circle cx="8" cy="8" r="6" />
            <path d="M18.09 10.37A6 6 0 1 1 10.34 18" />
            <path d="M7 6h1v4" />
            <path d="m16.71 13.88.7.71-2.82 2.82" />
          </svg>
        </span>
      )}
      </button>
      
      {/* Tooltip */}
      <ButtonTooltip
        text={buttonTextOverride || ''}
        subtext={promptSubmitButton?.requiredCredits ? `${promptSubmitButton.requiredCredits} credits required` : undefined}
        show={shouldShowTooltip && showTooltip}
      />
    </div>
  );
}
