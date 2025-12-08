/**
 * PromptBox Component
 * 
 * A comprehensive prompt input interface with category selection and form submission.
 * Composes CategoryCarousel, PromptTextarea, LogoUploadButton, and SubmitButton
 * into a unified prompt creation interface.
 */

'use client';

import { type FormEvent, useState } from 'react';
import { useAuth } from '@/lib/auth-context';
import { useCategorySelection, useFileUpload } from '@/hooks';
import { CategoryCarousel } from './CategoryCarousel';
import { PromptForm } from './PromptForm';
import { CategoryActionDialog } from './CategoryActionDialog';
import { categories, type ImageVariationsCount } from '@/lib/constants';

interface PromptBoxProps {
  initialCategory?: string;
}

export function PromptBox({ initialCategory = 'packaging-design' }: PromptBoxProps) {
  const { isAuthenticated } = useAuth();
  
  // Category selection and dialog management
  const {
    selectedCategory,
    dialogCategoryId,
    isActionDialogOpen,
    handleCategorySelect,
    closeDialog,
  } = useCategorySelection(initialCategory);
  
  // File upload management
  const {
    previewUrl,
    handleFileUpload,
    handleRemoveFile,
  } = useFileUpload();

  // Image variations state
  const [variationsCount, setVariationsCount] = useState<ImageVariationsCount>(5);

  // Get selected category data
  const selectedCategoryData = categories.find(c => c.id === selectedCategory);
  const dialogCategoryData = categories.find(c => c.id === dialogCategoryId);
  const placeholder = selectedCategoryData?.placeholder || 'Describe your vision...';
  const infoMessage = selectedCategoryData?.infoMessage;
  
  // Select auth-based configuration
  const authConfig = isAuthenticated 
    ? selectedCategoryData?.authenticated 
    : selectedCategoryData?.unauthenticated;
  
  const promptSubmitButton = authConfig?.promptSubmitButton;
  const showSubmitButton = !!promptSubmitButton;
  const showVariationsSelector = authConfig?.showVariationsSelector || false;

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const prompt = formData.get('prompt');
    
    // TODO: Implement form submission logic
    console.log('Selected category:', selectedCategory);
    console.log('Prompt:', prompt);
    console.log('Variations count:', variationsCount);
  };

  return (
    <div 
      id="prompt-box" 
      className="relative flex flex-col gap-5 bg-white py-5 rounded-4xl lg:py-8"
    >
      {/* Category Selection Carousel */}
      <CategoryCarousel 
        selectedCategory={selectedCategory}
        onCategorySelect={handleCategorySelect}
      />

      {/* Prompt Input Form */}
      <div className="flex flex-col px-5 lg:px-8">
        <PromptForm
          placeholder={placeholder}
          previewUrl={previewUrl}
          showSubmitButton={showSubmitButton}
          promptSubmitButton={promptSubmitButton}
          infoMessage={infoMessage}
          showVariationsSelector={showVariationsSelector}
          variationsCount={variationsCount}
          onVariationsChange={setVariationsCount}
          onFileSelect={handleFileUpload}
          onFileRemove={handleRemoveFile}
          onSubmit={handleSubmit}
        />
      </div>

      {/* Category Action Dialog */}
      <CategoryActionDialog
        isOpen={isActionDialogOpen}
        onClose={closeDialog}
        categoryName={dialogCategoryData?.name || ''}
      />
    </div>
  );
}
