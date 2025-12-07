/**
 * PromptForm Component
 * 
 * Form containing prompt textarea, file upload, and submit button
 */

'use client';

import { type FormEvent } from 'react';
import { useAuth } from '@/lib/auth-context';
import { PromptTextarea } from './PromptTextarea';
import { FileUploadButton } from './FileUploadButton';
import { SubmitButton } from './SubmitButton';
import { FilePreview } from './FilePreview';

interface PromptFormProps {
  /** Placeholder text for textarea */
  placeholder: string;
  /** Preview URL for uploaded file */
  previewUrl: string | null;
  /** Whether to show submit button */
  showSubmitButton: boolean;
  /** Button text for submit button when authenticated */
  authenticatedButtonText: string;
  /** Button text for submit button when not authenticated */
  unauthenticatedButtonText: string;
  /** Info message to display instead of textarea */
  infoMessage?: string;
  /** Callback when file is selected */
  onFileSelect: (file: File) => void;
  /** Callback when file is removed */
  onFileRemove: () => void;
  /** Callback when form is submitted */
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
}

export function PromptForm({
  placeholder,
  previewUrl,
  showSubmitButton,
  authenticatedButtonText,
  unauthenticatedButtonText,
  infoMessage,
  onFileSelect,
  onFileRemove,
  onSubmit
}: PromptFormProps) {
  const { isAuthenticated } = useAuth();
  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-4 min-h-[168px] lg:gap-6">
      {/* Reference File Preview */}
      {previewUrl && (
        <FilePreview previewUrl={previewUrl} onRemove={onFileRemove} />
      )}

      {/* Info Message or Textarea */}
      {infoMessage ? (
        <span className="inline-flex items-center border-2 rounded-full px-3 bg-gray-100 border-gray-100 text-gray-950 m-0 !pl-1 !pr-2 w-fit h-fit">
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
            className="w-5 h-5 text-blue-600 !mr-1 shrink-0"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="10" />
            <path d="M12 16v-4" />
            <path d="M12 8h.01" />
          </svg>
          <span className="font-space-grotesk tracking-normal text-inherit text-xs leading-4 md:text-xs md:leading-4 lg:text-[13px] lg:leading-4 xl:text-[13px] xl:leading-4 font-medium">
            {infoMessage}
          </span>
        </span>
      ) : (
        <div className="relative w-full">
          <PromptTextarea
            placeholder={placeholder}
            name="prompt"
            aria-label="Enter your prompt"
            required
          />
        </div>
      )}
      
      <div className="flex flex-row items-center justify-between gap-4 mt-auto">
        <div className="flex-1">
          <FileUploadButton onFileSelect={onFileSelect} />
        </div>
        
        {showSubmitButton && (
          <div>
            <SubmitButton 
              authenticatedText={authenticatedButtonText}
              unauthenticatedText={unauthenticatedButtonText}
              isAuthenticated={isAuthenticated}
            >
              Start
            </SubmitButton>
          </div>
        )}
      </div>
    </form>
  );
}
