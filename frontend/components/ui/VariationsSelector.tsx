/**
 * VariationsSelector Component
 * 
 * A button with popover that allows selecting the number of image variations (1-5)
 * Uses Radix UI Popover for accessible dropdown functionality
 */

'use client';

import { useState } from 'react';
import * as Popover from '@radix-ui/react-popover';
import { IMAGE_VARIATIONS_OPTIONS, type ImageVariationsCount } from '@/lib/constants';
import { cn } from '@/lib/utils';
import { ButtonTooltip } from './ButtonTooltip';

interface VariationsSelectorProps {
  /** Current selected variation count */
  value: ImageVariationsCount;
  /** Callback when variation count changes */
  onChange: (count: ImageVariationsCount) => void;
}

export function VariationsSelector({ value, onChange }: VariationsSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  const [buttonElement, setButtonElement] = useState<HTMLButtonElement | null>(null);

  const handleSelect = (count: ImageVariationsCount) => {
    onChange(count);
    setIsOpen(false);
  };

  return (
    <Popover.Root open={isOpen} onOpenChange={setIsOpen}>
      <Popover.Trigger asChild>
        <button
          ref={setButtonElement}
          type="button"
          onMouseEnter={() => !isOpen && setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          className="h-10 px-4 min-w-16 shrink-0 inline-flex items-center justify-center rounded-full bg-transparent text-neutral-900 hover:bg-neutral-200 transition duration-200 cursor-pointer"
        >
          <span className="font-space-grotesk text-sm lg:text-[15px] font-medium pr-2">
            {value}
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
            className="w-6 h-6"
          >
            <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
            <circle cx="9" cy="9" r="2" />
            <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
          </svg>
        </button>
      </Popover.Trigger>

      <Popover.Portal>
        <Popover.Content
          side="top"
          align="start"
          sideOffset={8}
          className="p-6 rounded-4xl bg-white lg:bg-neutral-50/80 backdrop-blur-md border border-neutral-200 shadow-lg w-[270px] z-50 animate-in fade-in-0 zoom-in-95"
        >
          <div role="radiogroup" className="flex flex-col gap-4">
            {IMAGE_VARIATIONS_OPTIONS.map((count) => (
              <div key={count} className="flex items-center justify-between gap-3">
                <div
                  onClick={() => handleSelect(count)}
                  className="flex items-center gap-3 cursor-pointer flex-1"
                >
                  <span className="font-space-grotesk text-sm lg:text-[15px] font-medium text-neutral-950">
                    {count}
                  </span>
                  <div className="flex gap-0.5">
                    {Array.from({ length: count }, (_, i) => (
                      <svg
                        key={i}
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        className="lucide lucide-image"
                      >
                        <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
                        <circle cx="9" cy="9" r="2" />
                        <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
                      </svg>
                    ))}
                  </div>
                </div>
                <button
                  type="button"
                  role="radio"
                  aria-checked={value === count}
                  aria-label={`Select ${count} image${count > 1 ? 's' : ''}`}
                  onClick={() => handleSelect(count)}
                  className={cn(
                    "w-5 h-5 rounded-full border-2 flex items-center justify-center transition",
                    value === count
                      ? "border-blue-700 bg-blue-700 text-white"
                      : "border-neutral-600 bg-white hover:border-neutral-700"
                  )}
                >
                  {value === count && (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            ))}
          </div>
        </Popover.Content>
      </Popover.Portal>

      <ButtonTooltip
        text="Number of images"
        subtext="Choose the number of images to generate"
        show={showTooltip && !isOpen}
        targetElement={buttonElement}
      />
    </Popover.Root>
  );
}
