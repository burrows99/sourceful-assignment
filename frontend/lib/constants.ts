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
  status?: {
    text: string;
    color: 'gradient' | 'orange';
  };
}

export const categories: readonly Category[] = [
  { id: 'packaging-design', name: 'Packaging design', icon: 'package', placeholder: 'Describe your ideal packaging vision...', buttonText: 'packaging design' },
  { id: 'logo-design', name: 'Logo design', icon: 'logo-design', placeholder: 'Describe your brand, target audience and any details about the logo you want...', buttonText: 'logo design', status: { text: 'New!', color: 'gradient' } },
  { id: 'brand-moodboard', name: 'Brand moodboard', icon: 'brand-moodboard', placeholder: 'Describe the image you want to create', buttonText: 'brand moodboard', status: { text: 'New!', color: 'gradient' } },
  { id: 'product-mockups', name: 'Product mockups', icon: 'product-mockups', showDialog: true, status: { text: 'New!', color: 'gradient' } },
  { id: 'ai-photoshoot', name: 'AI photoshoot', icon: 'ai-photoshoot', showDialog: true, status: { text: 'New!', color: 'gradient' } },
  { id: 'social-ads', name: 'Social ads', icon: 'social-ads', placeholder: 'What social media ad do you want to create?', buttonText: 'social ads', status: { text: 'Coming soon', color: 'orange' } },
  { id: 'card-and-posters', name: 'Card and posters', icon: 'card-and-posters', placeholder: 'Describe your card or poster design...', buttonText: 'card and posters', status: { text: 'New!', color: 'gradient' } },
  { id: 'variant-range', name: 'Variant range', icon: 'variant-range', placeholder: 'Describe the product variants you need...', buttonText: 'variant range', status: { text: 'New!', color: 'gradient' } },
  { id: 'packaging-range', name: 'Packaging range', icon: 'packaging-rnge', placeholder: 'Describe your packaging range requirements...', buttonText: 'packaging range', status: { text: 'New!', color: 'gradient' } },
  { id: 'create-image', name: 'Create image', icon: 'create-image', placeholder: 'Describe the image you want to create...', buttonText: 'image creation', status: { text: 'New!', color: 'gradient' } },
  { id: 'edit-image', name: 'Edit image', icon: 'edit-image', placeholder: 'Describe your ideal card or poster vision...', buttonText: 'image editing' },
] as const;
