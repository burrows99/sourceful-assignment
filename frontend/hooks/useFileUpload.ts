/**
 * useFileUpload Hook
 * 
 * Custom hook to manage file upload state and preview URL cleanup
 */

import { useState, useEffect } from 'react';

export function useFileUpload() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Cleanup preview URL when component unmounts
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileUpload = (file: File) => {
    // Cleanup old URL if exists
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    
    setUploadedFile(file);
    
    // Create new preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleRemoveFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setUploadedFile(null);
    setPreviewUrl(null);
  };

  return {
    uploadedFile,
    previewUrl,
    handleFileUpload,
    handleRemoveFile,
  };
}
