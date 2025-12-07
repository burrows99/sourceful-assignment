/**
 * Carousel Component
 * 
 * A general-purpose responsive carousel with scroll navigation.
 * Features:
 * - Responsive: Grid layout on mobile, horizontal scroll on desktop
 * - Dynamic scroll buttons based on scroll position
 * - Accepts any React children
 */

'use client';

import { useState, useRef, useEffect, type ReactNode } from 'react';
import { ScrollButton } from './ScrollButton';

interface CarouselProps {
  /** Content to display in the carousel */
  children: ReactNode;
  /** ARIA label for navigation */
  ariaLabel?: string;
  /** Show grid on mobile (default: true) */
  showMobileGrid?: boolean;
  /** Number of items to show in mobile grid (default: all) */
  mobileGridItems?: number;
}

export function Carousel({ 
  children,
  ariaLabel = 'Carousel navigation',
  showMobileGrid = true,
  mobileGridItems
}: CarouselProps) {
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Convert children to array for manipulation
  const childrenArray = Array.isArray(children) ? children : [children];
  const mobileItems = mobileGridItems 
    ? childrenArray.slice(0, mobileGridItems) 
    : childrenArray;

  const checkScroll = () => {
    if (!scrollRef.current) return;
    
    const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
    setCanScrollLeft(scrollLeft > 0);
    setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10);
  };

  useEffect(() => {
    checkScroll();
    const scrollElement = scrollRef.current;
    
    if (!scrollElement) return;

    scrollElement.addEventListener('scroll', checkScroll);
    window.addEventListener('resize', checkScroll);
    
    return () => {
      scrollElement.removeEventListener('scroll', checkScroll);
      window.removeEventListener('resize', checkScroll);
    };
  }, []);

  const scroll = (direction: 'left' | 'right') => {
    if (!scrollRef.current) return;
    
    // Width of one item (128px) + gap (20px = 5 * 4px in Tailwind)
    const itemWidth = 128 + 20;
    scrollRef.current.scrollBy({
      left: direction === 'left' ? -itemWidth : itemWidth,
      behavior: 'smooth',
    });
  };

  return (
    <nav className="relative" aria-label={ariaLabel}>
      {/* Mobile Grid */}
      {showMobileGrid && (
        <div className="grid grid-cols-2 gap-5 px-5 md:hidden">
          {mobileItems}
        </div>
      )}

      {/* Desktop Horizontal Carousel */}
      <div 
        ref={scrollRef}
        className={`${showMobileGrid ? 'hidden md:flex' : 'flex'} flex-row flex-nowrap gap-5 items-center overflow-x-auto py-1 snap-x snap-mandatory no-scrollbar scroll-pl-5 lg:scroll-pl-8`}
      >
        <div className="flex gap-5 px-5 lg:px-8">
          {childrenArray}
        </div>
      </div>

      {/* Scroll Navigation Buttons */}
      <div className="hidden md:block pointer-events-none">
        {canScrollLeft && (
          <ScrollButton
            direction="left"
            onClick={() => scroll('left')}
            className="absolute top-1/2 left-5 -translate-y-1/2 lg:left-8"
          />
        )}
        {canScrollRight && (
          <ScrollButton
            direction="right"
            onClick={() => scroll('right')}
            className="absolute top-1/2 right-5 -translate-y-1/2 lg:right-8"
          />
        )}
      </div>
    </nav>
  );
}
