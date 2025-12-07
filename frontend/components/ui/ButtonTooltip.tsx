/**
 * ButtonTooltip Component
 * 
 * A tooltip that displays information about button requirements
 */

'use client';

interface ButtonTooltipProps {
  /** Main tooltip text */
  text: string;
  /** Optional subtext (e.g., credit requirements) */
  subtext?: string;
  /** Whether to show the tooltip */
  show: boolean;
}

export function ButtonTooltip({ text, subtext, show }: ButtonTooltipProps) {
  if (!show) return null;
  
  return (
    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-4 py-2.5 bg-gray-900 text-white rounded-lg whitespace-nowrap shadow-lg z-[60] pointer-events-none">
      <div className="flex flex-col items-center gap-0.5">
        <span className="font-space-grotesk text-sm font-medium">
          {text}
        </span>
        {subtext && (
          <span className="font-space-grotesk text-xs text-gray-300">
            {subtext}
          </span>
        )}
      </div>
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1 w-0 h-0 border-l-[6px] border-r-[6px] border-t-[6px] border-transparent border-t-gray-900"></div>
    </div>
  );
}
