/**
 * CategoryCarousel Component
 * 
 * A specialized carousel for category selection.
 * Mobile: Shows selected category + "More tools" button that opens dialog
 * Desktop: Wraps the general-purpose Carousel component
 */

'use client';

import { useState, useRef } from 'react';
import { Carousel } from './Carousel';
import { IconButton } from './IconButton';
import { Icon } from './Icon';
import { CategoryDialog } from './CategoryDialog';
import { categories } from '@/lib/constants';

interface CategoryCarouselProps {
  /** Currently selected category ID */
  selectedCategory: string;
  /** Callback when category is selected */
  onCategorySelect: (categoryId: string) => void;
}

export function CategoryCarousel({ 
  selectedCategory, 
  onCategorySelect 
}: CategoryCarouselProps) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const buttonRefs = useRef<{ [key: string]: HTMLButtonElement | null }>({});
  
  const selectedCategoryData = categories.find(c => c.id === selectedCategory);

  const handleCategoryClick = (categoryId: string) => {
    // Scroll the clicked button into view
    const buttonElement = buttonRefs.current[categoryId];
    if (buttonElement) {
      buttonElement.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center'
      });
    }
    
    onCategorySelect(categoryId);
  };

  return (
    <>
      {/* Mobile: Show selected category + More tools button */}
      <div className="grid grid-cols-2 gap-5 px-5 md:hidden">
        <IconButton
          icon={<Icon name={selectedCategoryData?.icon || 'package'} />}
          text={selectedCategoryData?.name || 'Category'}
          isSelected={true}
          onClick={() => setIsDialogOpen(true)}
          className="w-full"
          aria-label="Selected category"
        />
        <IconButton
          icon={
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="30" 
              height="30" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="1" />
              <circle cx="19" cy="12" r="1" />
              <circle cx="5" cy="12" r="1" />
            </svg>
          }
          text="More tools"
          isSelected={false}
          onClick={() => setIsDialogOpen(true)}
          className="w-full"
          aria-label="Open more tools"
        />
      </div>

      {/* Desktop: Show carousel */}
      <div className="hidden md:block">
        <Carousel 
          ariaLabel="Category selection"
          showMobileGrid={false}
        >
          {categories.map((category) => (
            <IconButton
              key={category.id}
              ref={(el) => { buttonRefs.current[category.id] = el; }}
              icon={<Icon name={category.icon} />}
              text={category.name}
              isSelected={selectedCategory === category.id}
              statusBadge={category.statusBadge}
              tooltipImage={category.tooltipImage}
              tooltipDescription={category.tooltipDescription}
              onClick={() => handleCategoryClick(category.id)}
              aria-label={`Select ${category.name}`}
            />
          ))}
        </Carousel>
      </div>

      <CategoryDialog
        isOpen={isDialogOpen}
        onClose={() => setIsDialogOpen(false)}
        selectedCategory={selectedCategory}
        onCategorySelect={onCategorySelect}
      />
    </>
  );
}