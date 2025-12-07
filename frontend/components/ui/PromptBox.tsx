/**
 * PromptBox Component
 * 
 * A comprehensive prompt input interface with category selection and form submission.
 * Composes CategoryCarousel, PromptTextarea, LogoUploadButton, and SubmitButton
 * into a unified prompt creation interface.
 */

'use client';

import { useState, type FormEvent } from 'react';
import { CategoryCarousel } from './CategoryCarousel';
import { PromptForm } from './PromptForm';
import { CategoryActionDialog } from './CategoryActionDialog';
import { categories } from '@/lib/constants';

export function PromptBox() {
  const [selectedCategory, setSelectedCategory] = useState<string>('packaging-design');
  const [isActionDialogOpen, setIsActionDialogOpen] = useState(false);
  const [dialogCategoryId, setDialogCategoryId] = useState<string>('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Get selected category data
  const selectedCategoryData = categories.find(c => c.id === selectedCategory);
  const dialogCategoryData = categories.find(c => c.id === dialogCategoryId);
  const placeholder = selectedCategoryData?.placeholder || 'Describe your vision...';
  const showSubmitButton = !!selectedCategoryData?.placeholder && !!selectedCategoryData?.buttonText;

  // Handle category selection - open dialog if needed
  const handleCategorySelect = (categoryId: string) => {
    const category = categories.find(c => c.id === categoryId);
    if (category?.showDialog) {
      // Don't change selection, just open dialog
      setDialogCategoryId(categoryId);
      setIsActionDialogOpen(true);
    } else {
      // Normal selection
      setSelectedCategory(categoryId);
    }
  };

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
    
    // Create preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    
    // Cleanup old URL if exists
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  };

  const handleRemoveFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setUploadedFile(null);
    setPreviewUrl(null);
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const prompt = formData.get('prompt');
    
    // TODO: Implement form submission logic
    console.log('Selected category:', selectedCategory);
    console.log('Prompt:', prompt);
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
          buttonText={selectedCategoryData?.buttonText || 'design'}
          onFileSelect={handleFileUpload}
          onFileRemove={handleRemoveFile}
          onSubmit={handleSubmit}
        />
      </div>

      {/* Category Action Dialog */}
      <CategoryActionDialog
        isOpen={isActionDialogOpen}
        onClose={() => setIsActionDialogOpen(false)}
        categoryName={dialogCategoryData?.name || ''}
      />
    </div>
  );
}
