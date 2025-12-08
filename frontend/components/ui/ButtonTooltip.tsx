/**
 * ButtonTooltip Component
 * 
 * A tooltip that displays information about button requirements
 * Uses React Portal to render the tooltip at the document body level
 */

'use client';

import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import Image from 'next/image';
import { cn } from '@/lib/utils';

interface ButtonTooltipProps {
  /** Main tooltip text */
  text: string;
  /** Optional subtext (e.g., credit requirements) */
  subtext?: string;
  /** Optional image URL */
  image?: string;
  /** Whether to show the tooltip */
  show: boolean;
  /** Target element to position the tooltip relative to */
  targetElement?: HTMLElement | null;
}

export function ButtonTooltip({ text, subtext, image, show, targetElement }: ButtonTooltipProps) {
  const [mounted, setMounted] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (show && mounted) {
      // Small delay to trigger animation
      const timer = setTimeout(() => setIsVisible(true), 10);
      return () => clearTimeout(timer);
    } else {
      setIsVisible(false);
    }
  }, [show, mounted]);

  if (!show || !mounted || !targetElement) return null;

  const rect = targetElement.getBoundingClientRect();
  const top = rect.top + window.scrollY - 10;
  const left = rect.left + rect.width / 2 + window.scrollX;
  
  return createPortal(
    <div 
      className={cn(
        "fixed text-white shadow-2xl z-60 pointer-events-none",
        "transition-opacity duration-600 ease-out",
        isVisible ? "opacity-100" : "opacity-0",
        image 
          ? "bg-black rounded-4xl overflow-hidden p-3" 
          : "bg-gray-900 px-4 py-2.5 rounded-2xl whitespace-nowrap"
      )}
      style={{
        top: `${top}px`,
        left: `${left}px`,
        transform: 'translate(-50%, -100%)',
        width: image ? '220px' : 'auto',
      }}
    >
      {image && (
        <div className="relative w-full h-[120px] bg-linear-to-br from-teal-400 to-blue-200 rounded-3xl overflow-hidden mb-3">
          <Image 
            src={image} 
            alt=""
            fill
            className="object-cover"
          />
        </div>
      )}
      
      <div className={cn(
        "flex flex-col gap-0.5",
        image ? "px-1" : "items-center"
      )}>
        <span className={cn(
          "font-space-grotesk text-white",
          image ? "text-sm font-semibold mb-1" : "text-sm font-medium"
        )}>
          {text}
        </span>
        {subtext && (
          <span className={cn(
            "font-space-grotesk text-gray-300",
            image ? "text-[11px] leading-snug" : "text-xs"
          )}>
            {subtext}
          </span>
        )}
      </div>
      
      {!image && (
        <div 
          className="absolute w-0 h-0 border-l-[6px] border-r-[6px] border-t-[6px] border-transparent border-t-gray-900"
          style={{
            top: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            marginTop: '-1px',
          }}
        ></div>
      )}
    </div>,
    document.body
  );
}
