/**
 * CategoryTooltip Component
 * 
 * A hover tooltip that displays category preview information
 * with an image and description.
 */

'use client';

interface CategoryTooltipProps {
  /** Category name/title */
  title: string;
  /** Preview image URL */
  image: string;
  /** Category description */
  description: string;
}

export function CategoryTooltip({
  title,
  image,
  description
}: CategoryTooltipProps) {
  return (
    <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 z-[9999] w-[280px] bg-black rounded-[32px] p-4 shadow-2xl pointer-events-none animate-in fade-in duration-200">
      {/* Preview Image */}
      <div className="w-full aspect-video rounded-[24px] overflow-hidden mb-4 bg-gradient-to-br from-teal-400 to-blue-300">
        <img 
          src={image} 
          alt={title}
          className="w-full h-full object-cover"
          onError={(e) => {
            // Fallback to gradient background if image fails to load
            e.currentTarget.style.display = 'none';
          }}
        />
      </div>
      
      {/* Title */}
      <h3 className="text-white font-semibold text-lg mb-2">
        {title}
      </h3>
      
      {/* Description */}
      <p className="text-gray-400 text-sm leading-relaxed">
        {description}
      </p>
    </div>
  );
}
