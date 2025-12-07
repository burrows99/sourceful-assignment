/**
 * Icon Component
 * 
 * Loads and displays SVG icons from the /public/icons directory.
 * Uses Next.js Image component for optimization.
 * 
 * @example
 * <Icon name="package" />
 * <Icon name="logo-design" className="w-8 h-8" />
 */

import Image from 'next/image';

interface IconProps {
  /** Name of the icon file (without .svg extension) */
  name: string;
  /** Optional CSS classes to apply */
  className?: string;
}

export function Icon({ name, className = '' }: IconProps) {
  return (
    <Image
      src={`/icons/${name}.svg`}
      alt={`${name} icon`}
      width={30}
      height={30}
      className={className}
    />
  );
}
