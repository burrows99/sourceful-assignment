/**
 * useCategorySelection Hook
 * 
 * Custom hook to manage category selection, URL updates, and dialog state
 */

import { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { categories } from '@/lib/constants';

export function useCategorySelection(initialCategory: string = 'packaging-design') {
  const router = useRouter();
  const pathname = usePathname();
  
  // Validate initial category
  const validInitialCategory = initialCategory && categories.find(c => c.id === initialCategory) 
    ? initialCategory 
    : 'packaging-design';
  
  const [selectedCategory, setSelectedCategory] = useState<string>(validInitialCategory);
  const [isActionDialogOpen, setIsActionDialogOpen] = useState(false);
  const [dialogCategoryId, setDialogCategoryId] = useState<string>('');

  // Handle category selection - open dialog if needed
  const handleCategorySelect = (categoryId: string) => {
    const category = categories.find(c => c.id === categoryId);
    
    // Always update the URL
    router.push(`${pathname}?category=${categoryId}`, { scroll: false });
    
    if (category?.showDialog) {
      // Open dialog but don't change selection
      setDialogCategoryId(categoryId);
      setIsActionDialogOpen(true);
    } else {
      // Normal selection
      setSelectedCategory(categoryId);
    }
  };

  const closeDialog = () => setIsActionDialogOpen(false);

  return {
    selectedCategory,
    dialogCategoryId,
    isActionDialogOpen,
    handleCategorySelect,
    closeDialog,
  };
}
