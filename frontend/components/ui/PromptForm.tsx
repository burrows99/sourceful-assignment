/**
 * PromptForm Component
 * 
 * Form containing prompt textarea, file upload, and submit button
 */

'use client';

import { type FormEvent } from 'react';
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
  /** Button text for submit button */
  buttonText: string;
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
  buttonText,
  onFileSelect,
  onFileRemove,
  onSubmit
}: PromptFormProps) {
  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-4">
      {/* Reference File Preview */}
      {previewUrl && (
        <FilePreview previewUrl={previewUrl} onRemove={onFileRemove} />
      )}

      <div className="relative w-full">
        <PromptTextarea
          placeholder={placeholder}
          name="prompt"
          aria-label="Enter your prompt"
          required
        />
      </div>
      
      <div className="flex flex-row items-center justify-between gap-4">
        <div className="flex-1">
          <FileUploadButton onFileSelect={onFileSelect} />
        </div>
        
        {showSubmitButton && (
          <div>
            <SubmitButton extendedText={buttonText}>
              Start
            </SubmitButton>
          </div>
        )}
      </div>
    </form>
  );
}
