# Sourceful Frontend Architecture Knowledge Base

## Document Overview
This document serves as a comprehensive reference for implementing the Sourceful.com frontend in Next.js. It details the architecture, design system, animations, layouts, and components observed from the production website.

**Last Updated**: December 7, 2025  
**Source**: Sourceful.com (https://www.sourceful.com/home)  
**Purpose**: Reference for Next.js implementation

---

## Table of Contents
1. [Technology Stack](#technology-stack)
2. [Design System](#design-system)
3. [Layout Architecture](#layout-architecture)
4. [Component Breakdown](#component-breakdown)
5. [Animations & Transitions](#animations--transitions)
6. [Responsive Design](#responsive-design)
7. [Typography System](#typography-system)
8. [Color Palette](#color-palette)
9. [Implementation Recommendations](#implementation-recommendations)

---

## 1. Technology Stack

### Current Stack (Production)
- **Framework**: Next.js (App Router based on `__next` div structure)
- **Styling**: Tailwind CSS (extensive use of utility classes)
- **Font**: Space Grotesk (custom font family)
- **State Management**: React hooks (client-side)
- **Analytics**: 
  - Vercel Analytics (@vercel/analytics/next v1.5.0)
  - Vercel Speed Insights (@vercel/speed-insights/next v1.2.0)
  - Google Tag Manager
  - Facebook Pixel
  - Twitter Pixel

### Dependencies Identified
- `next`: 16.0.7
- `react`: 19.2.0
- `react-dom`: 19.2.0
- Tailwind CSS v4.x
- TypeScript

### Build Configuration
- Environment: Production
- Asset optimization: Enabled (image optimization, code splitting)
- Static Generation: Enabled (SSG)

---

## 2. Design System

### 2.1 Core Design Principles
1. **Glassmorphism**: Backdrop blur effects with transparency
2. **Gradient-Heavy**: Extensive use of multi-color gradients
3. **Rounded Corners**: Heavy use of `rounded-pill` (fully rounded) and `rounded-xl`
4. **Shadows**: Multiple shadow layers (shadow-mid, box-shadow variations)
5. **Spacing**: Consistent 4px/8px grid system

### 2.2 Custom Tailwind Configuration

#### Custom Classes Observed
```css
/* Gradient Backgrounds */
.bg-gradient-r-violet-blue-green-subtle
.bg-gradient-b-fade-transparent-to-white
.bg-gradient-to-br from-ui-violet-700 from-10% to-ui-blue-700
.bg-gradient-r-violet-blue-green

/* Text Gradients */
.text-transparent bg-clip-text bg-gradient-r-violet-blue-green

/* Focus States */
.focus-visible:focus-ring

/* Custom Sizes */
.h-40 (40px height)
.w-40 (40px width)
.size-24 (24x24px)
.size-32 (32x32px)

/* Z-Index Layers */
.z-sidebar-nav-mobile
.z-sidebar-nav-desktop
.z-platform-navigation
.z-toaster
```

### 2.3 Button Variants

#### Primary Gradient Button
```jsx
className="bg-gradient-to-br from-ui-violet-700 from-10% to-ui-blue-700 
           text-ui-lightest 
           disabled:from-ui-grey-50 disabled:to-ui-grey-50 
           disabled:text-ui-grey-400
           before:opacity-0 before:hover:opacity-100 
           before:transition-opacity before:duration-200 
           before:absolute before:inset-0 
           before:bg-gradient-to-br before:from-ui-violet-700 
           before:from-40% before:to-ui-blue-700"
```

#### Ghost Button
```jsx
className="bg-transparent text-brand-black 
           hover:bg-ui-grey-200 focus:bg-ui-grey-200
           disabled:text-ui-grey-400"
```

#### Icon Button
```jsx
className="rounded-pill w-40 h-40 
           justify-center !px-0
           [&>svg]:w-24 [&>svg]:h-24"
```

---

## 3. Layout Architecture

### 3.1 Page Structure

```
<html>
  └── <body>
      └── <div id="__next">
          └── Main App Container
              ├── Background Gradients Layer
              ├── Sidebar Navigation (Desktop/Mobile)
              ├── Header (Platform Navigation)
              └── Main Content Area
```

### 3.2 Grid System

#### Desktop Layout
```jsx
<div className="lg:grid lg:relative lg:grid-cols-[80px_1fr]">
  <nav className="lg:w-80">Sidebar</nav>
  <main className="lg:col-start-2">Content</main>
</div>
```

#### Content Container
```jsx
<div className="max-w-contained-xl mx-auto w-full">
  <div className="grid gap-16 md:gap-24 xl:gap-32 grid-cols-12">
    <div className="col-span-full lg:col-span-8 lg:col-start-3">
      {/* Centered content - 8 cols out of 12 */}
    </div>
  </div>
</div>
```

### 3.3 Background Layers

```jsx
{/* Layer 1: Gradient Background */}
<div className="fixed top-0 left-0 right-0 bg-gradient-r-violet-blue-green-subtle min-h-[700px]">
  {/* Layer 2: Fade Overlay */}
  <div className="bg-gradient-b-fade-transparent-to-white h-full w-full absolute inset-0" />
</div>
```

---

## 4. Component Breakdown

### 4.1 Sidebar Navigation

#### Structure
- Fixed position on desktop, overlay on mobile
- Width: 80px (desktop)
- Contains icon buttons with labels
- Sticky at top of viewport

#### Navigation Items
1. **Home** - House icon
2. **Create** - Plus circle icon
3. **Projects** - Folder icon
4. **Print-Ready** - Printer icon
5. **Playground** - Play circle icon
6. **Design Judge** - Scale icon
7. **Photoshoots** - Camera icon (hidden on desktop)

#### Bottom Actions
- **Help** - Question mark icon
- **Live Chat** - Messages icon (gradient button)

#### Mobile Behavior
```jsx
className="hidden fixed 
           max-lg:top-0 max-lg:left-0 max-lg:bottom-0 
           max-lg:w-full max-lg:z-sidebar-nav-mobile
           lg:flex lg:flex-col"
```

### 4.2 Platform Navigation (Header)

#### Position & Style
```jsx
className="fixed top-12 right-12 p-8 z-platform-navigation 
           bg-ui-lightest/80 backdrop-blur-strong rounded-pill"
```

#### Contents
- Notification bell icon
- Credits display (e.g., "40" with coins icon)
- User avatar/profile button

### 4.3 Prompt Box (Main Feature)

#### Container
```jsx
className="relative flex flex-col gap-20 
           bg-ui-lightest py-20 rounded-xl shadow-mid 
           lg:py-32"
```

#### Horizontal Scroll Navigation
- Tools selector (horizontal scrolling list)
- Scroll buttons appear/disappear based on scroll position
- Snap scrolling enabled: `snap-x snap-mandatory`

#### Tools Available
1. **Packaging Design** (Active/Blue highlight)
2. **Logo Design** (New!)
3. **Create Image** (New!)
4. **Edit Image**
5. **AI Photoshoot** (New!)
6. **Packaging Range** (New!)
7. **Variant Range** (New!)
8. **Social Ads** (Coming Soon)
9. **Brand Moodboard** (New!)
10. **Product Mockups** (New!)
11. **Cards & Posters** (New!)

#### Tool Button States
```jsx
// Active State
className="bg-ui-blue-100"

// Default State
className="bg-ui-lightest hover:bg-ui-grey-50"

// Structure
<button className="flex flex-col items-center justify-center 
                   gap-8 w-128 h-104 rounded-xl 
                   focus-visible:focus-ring [&_svg]:size-24 
                   transition-colors duration-200">
  <svg>Icon</svg>
  <span>Label</span>
  <span>Badge (New!/Coming Soon)</span>
</button>
```

#### Form Input Area
- Large textarea (max 10,000 characters)
- File upload button (logo image)
- Gradient CTA button
- Floating background images (decorative)

### 4.4 Background Decorative Images

#### Implementation Pattern
```jsx
<img className="rotate-12 object-cover 
                lg:ml-[-65%] lg:mt-[-25%] 
                xl:ml-[-65%] xl:mt-[-25%]
                hidden rounded-xl absolute 
                top-1/2 left-1/2 
                -translate-x-1/2 -translate-y-1/2 
                z-[-1]
                transition-all duration-1000 ease-in-out 
                lg:block opacity-100"
     src="..."
     alt=""
     width="362"
     height="207" />
```

**Positions**: 6 images positioned at various rotations and offsets:
- Image 1: `rotate-12, ml-[-65%], mt-[-25%]`
- Image 2: `-rotate-6, ml-[-70%], mt-[10%]`
- Image 3: `-rotate-12, ml-[70%], mt-[-20%]`
- Image 4: `rotate-6, ml-[65%], mt-[15%]`
- Image 5: `-rotate-3, ml-[-140%], mt-[0%]`
- Image 6: `-rotate-3, ml-[140%], mt-[0%]`

### 4.5 Video Resources Section

#### Layout
```jsx
<section className="px-16 lg:px-64 space-y-20">
  <h2>Introduction videos</h2>
  <div className="grid gap-16 md:gap-24 xl:gap-32 
                  grid-cols-1 md:grid-cols-2 
                  lg:grid-cols-3 xl:grid-cols-4">
    {/* YouTube iframes */}
  </div>
</section>
```

#### Video Count
9 introduction videos embedded via YouTube iframes

---

## 5. Animations & Transitions

### 5.1 Transition Patterns

#### Standard Transitions
```css
transition-duration: 200ms (0.2s)
transition-timing-function: ease-out
transition-property: background-color, color, opacity, transform
```

#### Long Transitions
```css
/* Dialog/Modal animations */
transition-duration: 700ms (fade)
transition-duration: 400ms (slide)

/* Image transitions */
transition-all duration-1000 ease-in-out
```

### 5.2 Transform Animations

#### Hover Scale
```css
.hover:scale-110
transform: scale(1.1)
```

#### Rotation
```css
transform: rotate(0deg)
hover: rotate(90deg) /* For close buttons */
```

#### Slide Animations
```css
/* Drawer/Sidebar */
transform: translateX(-100%) /* Hidden left */
transform: translateX(100%)  /* Hidden right */
transform: translateX(0)     /* Visible */
```

### 5.3 Opacity Transitions

#### Fade In/Out Pattern
```jsx
className="opacity-0 transition-delay-0ms transition-duration-700ms
           [visible]: opacity-100"
```

#### Hover Opacity
```jsx
className="before:opacity-0 before:hover:opacity-100 
           before:transition-opacity before:duration-200"
```

### 5.4 Scroll-Based Animations

#### Smooth Scroll Container
```jsx
className="overflow-x-auto snap-x snap-mandatory 
           scroll-pl-20 no-scrollbar"
```

#### Snap Points
```jsx
className="snap-center first:pl-20 last:pr-20 
           md:snap-start"
```

---

## 6. Responsive Design

### 6.1 Breakpoints

```javascript
// Tailwind Default Breakpoints Used
sm: '640px'   // Not heavily used
md: '768px'   // Major breakpoint
lg: '1024px'  // Major breakpoint
xl: '1280px'  // Major breakpoint
```

### 6.2 Mobile-First Patterns

#### Sidebar
```jsx
// Mobile: Overlay menu
className="max-lg:fixed max-lg:top-0 max-lg:left-0 
           max-lg:bottom-0 max-lg:w-full 
           max-lg:z-sidebar-nav-mobile max-lg:hidden"

// Desktop: Fixed sidebar
className="lg:flex lg:flex-col lg:w-80"
```

#### Grid Columns
```jsx
// Mobile: 1 column
// Tablet: 2 columns
// Desktop: 3-4 columns
className="grid-cols-1 md:grid-cols-2 
           lg:grid-cols-3 xl:grid-cols-4"
```

#### Spacing
```jsx
// Mobile: 16px
// Desktop: 32px or 64px
className="px-16 lg:px-32"
className="px-16 lg:px-64"
```

### 6.3 Visibility Classes

```jsx
// Hide on mobile
className="hidden lg:block"
className="hidden lg:flex"

// Hide on desktop
className="lg:hidden"
className="md:hidden"
```

---

## 7. Typography System

### 7.1 Font Family

**Primary Font**: Space Grotesk
```css
font-family: Space Grotesk
font-smooth: always
-webkit-font-smoothing: antialiased
-moz-osx-font-smoothing: auto
```

### 7.2 Text Sizing System

#### Utility Pattern
```jsx
data-text-body=""
data-text-label=""
```

#### Size Classes
```jsx
// Labels (Small)
className="text-10 leading-12 
           md:text-10 md:leading-12 
           lg:text-11 lg:leading-16 
           xl:text-12 xl:leading-16"

// Body Text
className="text-15 leading-24 
           md:text-16 md:leading-24 
           lg:text-16 lg:leading-24 
           xl:text-17 xl:leading-28"

// Headings (Large)
className="text-23 leading-28 
           md:text-26 md:leading-32 
           lg:text-30 lg:leading-36 
           xl:text-34 xl:leading-44"
```

### 7.3 Font Weights
- `font-regular` - 400
- `font-medium` - 500
- `font-bold` - 700 (less common)

### 7.4 Letter Spacing
```jsx
className="tracking-normal"  // Default
className="tracking-tight"   // For headings
```

---

## 8. Color Palette

### 8.1 Brand Colors

#### Primary Colors
```css
/* Violet */
--ui-violet-700: #5338ff (primary brand color)

/* Blue */
--ui-blue-700: #47a8d8
--ui-blue-100: #B3DCFF (light blue, active states)
--brand-blue: (specific blue for links)

/* Green (Accent) */
--ui-green: #3eed9a (used in gradients)

/* Black */
--brand-black: #222222
--ui-grey-950: (near black, text)
```

#### Neutral Colors
```css
/* Whites/Grays */
--ui-lightest: #FFFFFF or very light gray
--ui-grey-50: (very light gray)
--ui-grey-100: (light gray)
--ui-grey-200: (medium-light gray)
--ui-grey-400: (medium gray, disabled)
--ui-grey-600: (medium-dark gray, secondary text)
--ui-grey-900: (dark gray)

/* Amber */
--brand-amber: (for "Coming Soon" badges)
```

### 8.2 Semantic Colors

#### Interactive States
```css
/* Hover */
hover:bg-ui-grey-200
hover:bg-ui-grey-50

/* Focus */
focus:bg-ui-grey-200
focus-ring (custom outline)

/* Active */
bg-ui-blue-100 (active tab/button)

/* Disabled */
disabled:bg-ui-grey-100
disabled:text-ui-grey-400
```

### 8.3 Gradient Definitions

#### Multi-Stop Gradients
```css
/* Violet to Blue */
background: linear-gradient(to bottom right, 
  var(--ui-violet-700) 10%, 
  var(--ui-blue-700) 100%
);

/* Violet to Blue to Green */
background: linear-gradient(to right, 
  violet → blue → green
);

/* Fade to White */
background: linear-gradient(to bottom, 
  transparent 0%, 
  white 100%
);
```

#### Hover Gradient Overlay
```css
before:bg-gradient-to-br 
before:from-ui-violet-700 before:from-40% 
before:to-ui-blue-700
```

---

## 9. Implementation Recommendations

### 9.1 Project Structure

```
app/
├── (auth)/
│   ├── login/
│   └── signup/
├── (dashboard)/
│   ├── layout.tsx          # Sidebar + Header layout
│   ├── home/
│   ├── projects/
│   ├── playground/
│   └── print-ready/
├── layout.tsx              # Root layout
├── page.tsx                # Landing page
└── globals.css

components/
├── ui/                     # Base components
│   ├── button.tsx
│   ├── input.tsx
│   ├── avatar.tsx
│   ├── badge.tsx
│   └── icon.tsx
├── dashboard/
│   ├── sidebar.tsx
│   ├── platform-nav.tsx
│   ├── prompt-box.tsx
│   └── tool-selector.tsx
└── shared/
    ├── video-grid.tsx
    └── footer.tsx

lib/
├── utils.ts
└── constants.ts

public/
└── images/
    └── prompt-box/
```

### 9.2 Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          black: "#222222",
          blue: "#47a8d8",
          amber: "#FFA500",
        },
        ui: {
          lightest: "#FFFFFF",
          violet: {
            700: "#5338ff",
          },
          blue: {
            100: "#B3DCFF",
            700: "#47a8d8",
          },
          green: {
            DEFAULT: "#3eed9a",
          },
          grey: {
            50: "#F9FAFB",
            100: "#F3F4F6",
            200: "#E5E7EB",
            400: "#9CA3AF",
            600: "#4B5563",
            900: "#111827",
            950: "#030712",
          },
        },
      },
      fontFamily: {
        "space-grotesk": ["var(--font-space-grotesk)", "sans-serif"],
      },
      borderRadius: {
        pill: "9999px",
      },
      boxShadow: {
        mid: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
      },
      backdropBlur: {
        strong: "20px",
      },
      zIndex: {
        "sidebar-nav-mobile": "1000",
        "sidebar-nav-desktop": "900",
        "platform-navigation": "950",
        toaster: "1100",
      },
      maxWidth: {
        "contained-xl": "1280px",
      },
      transitionDuration: {
        "1000": "1000ms",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
  ],
};

export default config;
```

### 9.3 Component Patterns

#### Button Component Template
```tsx
// components/ui/button.tsx
import { cn } from "@/lib/utils";
import { ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "ghost" | "icon";
  size?: "sm" | "md" | "lg";
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "relative overflow-hidden appearance-none inline-flex items-center",
          "rounded-pill box-border transition duration-200",
          "[&>svg]:relative focus-visible:focus-ring",
          "disabled:cursor-not-allowed",
          {
            primary: `bg-gradient-to-br from-ui-violet-700 from-10% to-ui-blue-700 
                      text-ui-lightest disabled:from-ui-grey-50 disabled:to-ui-grey-50
                      before:opacity-0 before:hover:opacity-100 
                      before:transition-opacity before:duration-200
                      before:absolute before:inset-0
                      before:bg-gradient-to-br before:from-ui-violet-700 
                      before:from-40% before:to-ui-blue-700`,
            ghost: `bg-transparent text-brand-black 
                   hover:bg-ui-grey-200 focus:bg-ui-grey-200
                   disabled:text-ui-grey-400`,
            icon: `justify-center !px-0 w-40 h-40`,
          }[variant],
          {
            sm: "h-32 px-12 text-sm",
            md: "h-40 px-16",
            lg: "h-48 px-24 text-lg",
          }[size],
          className
        )}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button };
```

### 9.4 Animation Utilities

```typescript
// lib/animations.ts
export const transitions = {
  fast: "transition-all duration-200 ease-out",
  normal: "transition-all duration-300 ease-out",
  slow: "transition-all duration-700 ease-in-out",
  verySlow: "transition-all duration-1000 ease-in-out",
};

export const transforms = {
  scaleHover: "hover:scale-110 transition-transform duration-200",
  rotate90: "rotate-0 hover:rotate-90 transition-transform duration-200",
  slideLeft: "transform translateX(-100%)",
  slideRight: "transform translateX(100%)",
  slideNone: "transform translateX(0)",
};
```

### 9.5 Data Attributes Pattern

```typescript
// Use data attributes for styling hooks
<span data-text-body="" className="...">Text</span>
<span data-text-label="" className="...">Label</span>
<button data-button="" className="...">Button</button>
<div data-icon="" className="...">Icon</div>
```

### 9.6 Accessibility Considerations

```tsx
// Always include proper ARIA labels
<button 
  aria-label="Close menu"
  aria-labelledby="menu-item-id"
  aria-expanded="false"
  aria-controls="menu-content"
>
  <span className="sr-only">Close menu</span>
  <svg aria-hidden="true">...</svg>
</button>

// Focus states
className="focus-visible:focus-ring focus-visible:outline-none"

// Screen reader only content
className="sr-only"
```

### 9.7 Image Optimization

```tsx
// Use Next.js Image component
import Image from "next/image";

<Image
  src="/images/prompt-box/gi-3-1.jpg"
  alt="Descriptive alt text"
  width={362}
  height={207}
  priority // For above-fold images
  loading="lazy" // For below-fold images
  className="rounded-xl object-cover"
/>
```

### 9.8 Performance Optimizations

```typescript
// Preload critical resources
<link rel="preload" as="image" href="/images/hero.jpg" />
<link rel="preload" as="font" href="/fonts/space-grotesk.woff2" />

// Code splitting for heavy components
const HeavyComponent = dynamic(() => import("./HeavyComponent"), {
  loading: () => <LoadingSpinner />,
  ssr: false, // If client-side only
});

// Intersection Observer for lazy loading
const { ref, inView } = useInView({
  triggerOnce: true,
  threshold: 0.1,
});
```

---

## Key Features to Implement

### Priority 1 (Core Experience)
1. ✅ Sidebar navigation with icon + label pattern
2. ✅ Gradient background layers
3. ✅ Prompt box with tool selector
4. ✅ Horizontal scroll navigation
5. ✅ File upload component
6. ✅ Gradient CTA buttons

### Priority 2 (Enhanced UX)
1. ✅ Decorative floating images
2. ✅ Smooth scroll with snap points
3. ✅ Badge components (New! / Coming Soon)
4. ✅ Avatar with fallback initials
5. ✅ Notification system
6. ✅ Credits display

### Priority 3 (Polish)
1. ✅ Hover state animations
2. ✅ Loading states
3. ✅ Empty states
4. ✅ Error boundaries
5. ✅ Toast notifications
6. ✅ Modal/dialog system

---

## Testing Checklist

### Responsive Testing
- [ ] Mobile (< 768px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (> 1024px)
- [ ] Large Desktop (> 1280px)

### Browser Testing
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (macOS/iOS)

### Accessibility
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Color contrast (WCAG AA)
- [ ] Focus indicators
- [ ] ARIA labels

### Performance
- [ ] Lighthouse score > 90
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3.5s
- [ ] Core Web Vitals passing

---

## Additional Notes

### Animation Timing Philosophy
- **Fast interactions** (200ms): Hover states, clicks
- **Medium interactions** (300-400ms): Slides, fades
- **Slow interactions** (700-1000ms): Page transitions, decorative elements

### Gradient Strategy
- Use CSS variables for gradient stops
- Keep hover gradients more saturated (from-40% vs from-10%)
- Always provide fallback solid colors

### Z-Index Hierarchy
```
1100 - Toasts/Notifications
1000 - Mobile Navigation Overlay
950  - Platform Navigation
900  - Desktop Sidebar
10   - Default stacking context
0    - Base layer
-1   - Decorative/Background elements
```

### Mobile Menu Behavior
- Overlay: Full screen on mobile
- Backdrop: Semi-transparent with blur
- Animation: Slide in from left
- Close: X button or backdrop click

---

## Resources & References

### Design Inspiration
- Glassmorphism patterns
- Material Design 3
- Apple Human Interface Guidelines

### Code References
- Next.js App Router documentation
- Tailwind CSS v4 documentation
- Radix UI for accessible components
- Framer Motion for complex animations

---

## Change Log

### Version 1.0 (December 7, 2025)
- Initial documentation based on production site analysis
- Complete component breakdown
- Animation and transition specifications
- Responsive design patterns
- Color palette extraction
- Typography system documentation

---

**End of Document**
