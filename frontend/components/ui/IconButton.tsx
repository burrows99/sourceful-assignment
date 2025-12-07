/**
 * IconButton Component
 * 
 * A button component with an icon and text label, used for category selection.
 * Supports selected state with different visual styling.
 */

'use client';

import { type ReactNode, type ButtonHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Icon element to display */
  icon: ReactNode;
  /** Text label below the icon */
  text: string;
  /** Whether this button is currently selected */
  isSelected?: boolean;
  /** Status badge configuration */
  statusBadge?: {
    text: string;
    color: 'gradient' | 'orange';
  };
}

const baseStyles = `
  flex flex-col items-center justify-center gap-2
  w-32 h-26 rounded-[32px]
  text-base leading-6 font-normal
  cursor-pointer appearance-none
  transition-colors duration-200
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-300
`;

const iconStyles = `
  [&_svg]:w-[30px] [&_svg]:h-[30px] 
  [&_svg]:block [&_svg]:stroke-2
`;

const selectedStyles = `
  bg-blue-100 
  active:bg-blue-200
`;

const defaultStyles = `
  bg-[rgb(248,248,248)]
  active:bg-neutral-100
`;

export function IconButton({
  icon,
  text,
  isSelected = false,
  statusBadge,
  className,
  ...props
}: IconButtonProps) {
  const badgeColorClass = statusBadge?.color === 'orange'
    ? 'text-orange-500'
    : 'text-transparent bg-clip-text bg-gradient-to-r from-violet-500 via-blue-500 to-green-500';

  return (
    <button
      type="button"
      data-state={isSelected ? 'selected' : 'default'}
      className={cn(
        baseStyles,
        iconStyles,
        isSelected ? selectedStyles : defaultStyles,
        className
      )}
      {...props}
    >
      <div className="w-[30px] h-[30px] flex items-center justify-center">
        {icon}
      </div>

      <span className="text-[10px] md:text-[10px] lg:text-[11px] xl:text-xs leading-3 md:leading-3 lg:leading-4 xl:leading-4 text-center text-neutral-800">
        {text}
      </span>

      {statusBadge && (
        <span 
          data-text-label="" 
          className={cn(
            "font-space-grotesk tracking-tighter text-[10px] leading-3 md:text-[10px] md:leading-3 lg:text-[11px] lg:leading-4 xl:text-xs xl:leading-4 font-semibold",
            badgeColorClass
          )}
        >
          {statusBadge.text}
        </span>
      )}
    </button>
  );
}
