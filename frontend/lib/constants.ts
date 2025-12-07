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
  };
  unauthenticated: {
    promptSubmitButton?: PromptSubmitButton;
  };
  placeholder?: string;
  infoMessage?: string;
  showDialog?: boolean;
  statusBadge?: {
    text: string;
    color: 'gradient' | 'orange';
  };
}

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
  },
  { 
    id: 'create-image', 
    name: 'Create image', 
    icon: 'create-image', 
    authenticated: {
      promptSubmitButton: {
        buttonText: 'Start for free',
        iconSide: 'right',
      },
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
  },
  { 
    id: 'edit-image', 
    name: 'Edit image', 
    icon: 'edit-image', 
    authenticated: {},
    unauthenticated: {},
    placeholder: 'Describe your ideal card or poster vision...',
    showDialog: true,
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
  },
  { 
    id: 'social-ads', 
    name: 'Social ads', 
    icon: 'social-ads', 
    authenticated: {},
    unauthenticated: {},
    infoMessage: 'This tool is coming soon! Choose another tool to continue.',
    statusBadge: { text: 'Coming soon', color: 'orange' },
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
  },
] as const;
