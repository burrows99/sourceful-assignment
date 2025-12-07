/**
 * Constants
 * 
 * Application-wide constants and configuration
 */

export interface Category {
  id: string;
  name: string;
  icon: string;
  placeholder?: string;
  showDialog?: boolean;
  buttonText?: string;
  infoMessage?: string;
  statusBadge?: {
    text: string;
    color: 'gradient' | 'orange';
  };
}

export const categories: readonly Category[] = [
  { id: 'packaging-design', name: 'Packaging design', icon: 'package', placeholder: 'Describe your ideal packaging vision...', buttonText: 'packaging design' },
  { id: 'logo-design', name: 'Logo design', icon: 'logo-design', placeholder: 'Describe your brand, target audience and any details about the logo you want...', buttonText: 'logo design', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'create-image', name: 'Create image', icon: 'create-image', placeholder: 'Describe the image you want to create...', buttonText: 'image creation', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'edit-image', name: 'Edit image', icon: 'edit-image', placeholder: 'Describe your ideal card or poster vision...', buttonText: 'image editing', showDialog: true },
  { id: 'ai-photoshoot', name: 'AI photoshoot', icon: 'ai-photoshoot', buttonText: 'photoshoot brief', infoMessage: 'Click start photoshoot brief to add your specific shot details.', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'packaging-range', name: 'Packaging range', icon: 'packaging-rnge', buttonText: 'packaging range', infoMessage: 'Click start packaging range to add your reference design and choose your packaging types.', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'variant-range', name: 'Variant range', icon: 'variant-range', buttonText: 'variant range', infoMessage: 'Click start variant range to add your reference design and describe your variants.', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'social-ads', name: 'Social ads', icon: 'social-ads', buttonText: 'social ads', infoMessage: 'This tool is coming soon! Choose another tool to continue.', statusBadge: { text: 'Coming soon', color: 'orange' } },
  { id: 'brand-moodboard', name: 'Brand moodboard', icon: 'brand-moodboard', buttonText: 'brand moodboard', infoMessage: 'Click start moodboard brief to add your brand and style details.', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'product-mockups', name: 'Product mockups', icon: 'product-mockups', buttonText: 'product mockups', infoMessage: 'Click start your new product mockup, supply your artwork and choose your desired product type.', statusBadge: { text: 'New!', color: 'gradient' } },
  { id: 'card-and-posters', name: 'Card and posters', icon: 'card-and-posters', placeholder: 'Describe your card or poster design...', buttonText: 'card and posters', statusBadge: { text: 'New!', color: 'gradient' } },
] as const;
