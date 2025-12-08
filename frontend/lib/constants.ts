/**
 * Constants
 * 
 * Application-wide constants and configuration
 */

import type { PromptSubmitButton } from '@/components/ui/SubmitButton';

export interface Category {
  id: string;
  name: string;
  icon: string;
  authenticated: {
    promptSubmitButton?: PromptSubmitButton;
    showVariationsSelector?: boolean;
  };
  unauthenticated: {
    promptSubmitButton?: PromptSubmitButton;
    showVariationsSelector?: boolean;
  };
  placeholder?: string;
  infoMessage?: string;
  showDialog?: boolean;
  statusBadge?: {
    text: string;
    color: 'gradient' | 'orange';
  };
  tooltipImage?: string;
  tooltipDescription?: string;
}

export const IMAGE_VARIATIONS_OPTIONS = [1, 2, 3, 4, 5] as const;
export type ImageVariationsCount = typeof IMAGE_VARIATIONS_OPTIONS[number];

export const categories: readonly Category[] = [
  { 
    id: 'packaging-design', 
    name: 'Packaging design', 
    icon: 'package', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start packaging design',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start packaging design',
        iconSide: 'right',
      },
    },
    placeholder: 'Describe your ideal packaging vision...',
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Design packaging that looks ready for the shelf.',
  },
  { 
    id: 'logo-design', 
    name: 'Logo design', 
    icon: 'logo-design', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start logo design',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start logo design',
        iconSide: 'right',
      },
    },
    placeholder: 'Describe your brand, target audience and any details about the logo you want...',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Create unique logos for your brand identity.',
  },
  { 
    id: 'create-image', 
    name: 'Create image', 
    icon: 'create-image', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start for free',
        iconSide: 'left',
        isFeatureAvailable: (credits) => credits >= 10,
        requiredCredits: 10,
        buttonTextOverrideIfLowCredits: 'Get credits',
      },
      showVariationsSelector: true,
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start for free',
        iconSide: 'left',
        shouldToggleDisabled: true,
      },
    },
    placeholder: 'Describe the image you want to create...',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Generate custom images with AI for any purpose.',
  },
  { 
    id: 'edit-image', 
    name: 'Edit image', 
    icon: 'edit-image', 
    authenticated: {},
    unauthenticated: {},
    placeholder: 'Describe your ideal card or poster vision...',
    showDialog: true,
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Edit and enhance your existing images with AI.',
  },
  { 
    id: 'ai-photoshoot', 
    name: 'AI photoshoot', 
    icon: 'ai-photoshoot', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start photoshoot brief',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start photoshoot brief',
        iconSide: 'right',
      },
    },
    infoMessage: 'Click start photoshoot brief to add your specific shot details.',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Create professional product photography with AI.',
  },
  { 
    id: 'packaging-range', 
    name: 'Packaging range', 
    icon: 'packaging-rnge', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start packaging range',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start packaging range',
        iconSide: 'right',
      },
    },
    infoMessage: 'Click start packaging range to add your reference design and choose your packaging types.',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Design consistent packaging across multiple products.',
  },
  { 
    id: 'variant-range', 
    name: 'Variant range', 
    icon: 'variant-range', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start variant range',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start variant range',
        iconSide: 'right',
      },
    },
    infoMessage: 'Click start variant range to add your reference design and describe your variants.',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Create multiple design variants from one concept.',
  },
  { 
    id: 'social-ads', 
    name: 'Social ads', 
    icon: 'social-ads', 
    authenticated: {},
    unauthenticated: {},
    infoMessage: 'This tool is coming soon! Choose another tool to continue.',
    statusBadge: { text: 'Coming soon', color: 'orange' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Create engaging ads for social media platforms.',
  },
  { 
    id: 'brand-moodboard', 
    name: 'Brand moodboard', 
    icon: 'brand-moodboard', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start brand moodboard',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start brand moodboard',
        iconSide: 'right',
      },
    },
    infoMessage: 'Click start moodboard brief to add your brand and style details.',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Build visual inspiration boards for your brand.',
  },
  { 
    id: 'product-mockups', 
    name: 'Product mockups', 
    icon: 'product-mockups', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start your new product mockups',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start your new product mockups',
        iconSide: 'right',
      },
    },
    infoMessage: 'Click start your new product mockup, supply your artwork and choose your desired product type.',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Showcase designs on realistic product mockups.',
  },
  { 
    id: 'card-and-posters', 
    name: 'Card and posters', 
    icon: 'card-and-posters', 
    authenticated: {
      promptSubmitButton: {
        forceDisabled: true,
        buttonText: 'Start packaging designs',
        iconSide: 'right',
      },
    },
    unauthenticated: {
      promptSubmitButton: {
        buttonText: 'Start packaging designs',
        iconSide: 'right',
        shouldToggleDisabled: true,
      },
    },
    placeholder: 'Describe your card or poster design...',
    statusBadge: { text: 'New!', color: 'gradient' },
    tooltipImage: 'https://www.sourceful.com/_next/image?url=%2Fimages%2Fprompt-box%2Fprompt-packaging-design.webp&w=640&q=75',
    tooltipDescription: 'Design beautiful cards and posters for any occasion.',
  },
] as const;
