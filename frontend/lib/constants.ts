/**
 * Constants
 * 
 * Application-wide constants and configuration
 */

export interface Category {
  id: string;
  name: string;
  icon: string;
  buttonText?: {
    authenticated: string;
    unauthenticated: string;
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
    buttonText: {
      authenticated: 'packaging design',
      unauthenticated: 'Start for free',
    },
    placeholder: 'Describe your ideal packaging vision...',
  },
  { 
    id: 'logo-design', 
    name: 'Logo design', 
    icon: 'logo-design', 
    buttonText: {
      authenticated: 'logo design',
      unauthenticated: 'for free',
    },
    placeholder: 'Describe your brand, target audience and any details about the logo you want...',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'create-image', 
    name: 'Create image', 
    icon: 'create-image', 
    buttonText: {
      authenticated: 'image creation',
      unauthenticated: 'for free',
    },
    placeholder: 'Describe the image you want to create...',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'edit-image', 
    name: 'Edit image', 
    icon: 'edit-image', 
    buttonText: {
      authenticated: 'image editing',
      unauthenticated: 'for free',
    },
    placeholder: 'Describe your ideal card or poster vision...',
    showDialog: true,
  },
  { 
    id: 'ai-photoshoot', 
    name: 'AI photoshoot', 
    icon: 'ai-photoshoot', 
    buttonText: {
      authenticated: 'photoshoot brief',
      unauthenticated: 'for free',
    },
    infoMessage: 'Click start photoshoot brief to add your specific shot details.',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'packaging-range', 
    name: 'Packaging range', 
    icon: 'packaging-rnge', 
    buttonText: {
      authenticated: 'packaging range',
      unauthenticated: 'for free',
    },
    infoMessage: 'Click start packaging range to add your reference design and choose your packaging types.',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'variant-range', 
    name: 'Variant range', 
    icon: 'variant-range', 
    buttonText: {
      authenticated: 'variant range',
      unauthenticated: 'for free',
    },
    infoMessage: 'Click start variant range to add your reference design and describe your variants.',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'social-ads', 
    name: 'Social ads', 
    icon: 'social-ads', 
    buttonText: {
      authenticated: 'social ads',
      unauthenticated: 'for free',
    },
    infoMessage: 'This tool is coming soon! Choose another tool to continue.',
    statusBadge: { text: 'Coming soon', color: 'orange' },
  },
  { 
    id: 'brand-moodboard', 
    name: 'Brand moodboard', 
    icon: 'brand-moodboard', 
    buttonText: {
      authenticated: 'brand moodboard',
      unauthenticated: 'for free',
    },
    infoMessage: 'Click start moodboard brief to add your brand and style details.',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'product-mockups', 
    name: 'Product mockups', 
    icon: 'product-mockups', 
    buttonText: {
      authenticated: 'product mockups',
      unauthenticated: 'for free',
    },
    infoMessage: 'Click start your new product mockup, supply your artwork and choose your desired product type.',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
  { 
    id: 'card-and-posters', 
    name: 'Card and posters', 
    icon: 'card-and-posters', 
    buttonText: {
      authenticated: 'card and posters',
      unauthenticated: 'for free',
    },
    placeholder: 'Describe your card or poster design...',
    statusBadge: { text: 'New!', color: 'gradient' },
  },
] as const;
