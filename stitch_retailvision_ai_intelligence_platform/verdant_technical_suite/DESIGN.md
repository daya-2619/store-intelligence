---
name: Verdant Technical Suite
colors:
  surface: '#e8fff0'
  surface-dim: '#b8e4cc'
  surface-bright: '#e8fff0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#d1fee5'
  surface-container: '#ccf8df'
  surface-container-high: '#c6f2da'
  surface-container-highest: '#c1ecd4'
  on-surface: '#002114'
  on-surface-variant: '#3f4943'
  inverse-surface: '#0e3727'
  inverse-on-surface: '#cffbe2'
  outline: '#6f7a72'
  outline-variant: '#bec9c0'
  surface-tint: '#116c4a'
  primary: '#0b6947'
  on-primary: '#ffffff'
  primary-container: '#30835f'
  on-primary-container: '#f5fff6'
  inverse-primary: '#86d7ad'
  secondary: '#2b694d'
  on-secondary: '#ffffff'
  secondary-container: '#b0f1cc'
  on-secondary-container: '#327053'
  tertiary: '#4a6150'
  on-tertiary: '#ffffff'
  tertiary-container: '#627a68'
  on-tertiary-container: '#f6fff4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#a1f4c8'
  primary-fixed-dim: '#86d7ad'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#b0f1cc'
  secondary-fixed-dim: '#94d4b1'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#0c5136'
  tertiary-fixed: '#cee9d3'
  tertiary-fixed-dim: '#b3cdb7'
  on-tertiary-fixed: '#092012'
  on-tertiary-fixed-variant: '#354c3b'
  background: '#e8fff0'
  on-background: '#002114'
  surface-variant: '#c1ecd4'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 56px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  margin: 32px
---

## Brand & Style

This design system is built for high-performance enterprise environments that prioritize clarity, cognitive ease, and a refreshing aesthetic. It moves away from the sterile "tech blue" standard, embracing a **light sea green ambiance** that suggests growth, stability, and vitality.

The style is a blend of **Corporate Modern** and **Minimalism**. It utilizes expansive white space—not as empty voids, but as breathing room—complemented by sophisticated tinted surfaces. The emotional response is one of "calm precision": the UI feels as organized as a code editor but as inviting as a modern architectural space. It targets professional users who spend hours in complex workflows, providing a visual environment that reduces eye strain through low-contrast surface transitions and an organic color palette.

## Colors

The palette is anchored by a refined **Sea Green (#40916C)**, used for primary actions and brand presence. Unlike traditional corporate palettes, this system eschews pure whites and neutral greys in favor of tinted neutrals.

- **Primary:** A versatile sea green that maintains high legibility against light backgrounds.
- **Surface & Background:** Surfaces use **#F0F7F4**, providing a soft, minty warmth that distinguishes container areas from the global background (**#F8FAF9**).
- **Typography & Neutrals:** Deep forest tones (**#1B4332**) replace standard blacks and greys for text, ensuring all content feels part of the same organic ecosystem while maintaining WCAG AA contrast ratios.
- **Accents:** Success states naturally harmonize with the palette, while warnings use a muted terracotta to remain distinct without clashing.

## Typography

The typography is powered exclusively by **Geist**, a typeface designed for technical precision and readability. 

The type scale is structured to emphasize hierarchy in data-heavy applications. Headlines utilize a tighter letter-spacing and heavier weights to feel impactful and grounded. Body text is set with generous line-height (1.6) to ensure long-form technical documentation is easily scannable. Label styles are set in medium or semi-bold weights to remain distinct even at small sizes (12px-14px). All type is rendered in the deep forest neutral to maintain the sea green ambiance.

## Layout & Spacing

This design system employs a **12-column fluid grid** for desktop and a **4-column fluid grid** for mobile. The layout philosophy centers on "clustered information," where related elements are grouped within containers to prevent visual sprawl.

Spacing is based on a **linear 8px scale**, ensuring mathematical harmony across all components. 
- **Desktop:** 32px outer margins with 24px gutters.
- **Tablet:** 24px outer margins with 16px gutters.
- **Mobile:** 16px outer margins with 12px gutters.

Horizontal rhythm is prioritized; alignment should follow the "hard-left" rule where text and icons are strictly aligned to the start of the column to maintain a clean, vertical scan-line.

## Elevation & Depth

Hierarchy is established through **tonal layering** and **colored shadows** rather than traditional grey-scale shadows. 

The system uses three primary tiers of depth:
1.  **Level 0 (Base):** The sea-tinted background (#F8FAF9).
2.  **Level 1 (Surface):** Elevated containers (#F0F7F4) with a very thin (1px) border in a slightly darker green tint.
3.  **Level 2 (Pop/Float):** Elements like menus or modals use a subtle ambient shadow. Shadows are not neutral; they are tinted with the primary color (e.g., `rgba(45, 106, 79, 0.08)`) to maintain the sea green personality even in the depth effects.

Backdrop blurs (12px–20px) are used on navigation bars and overlays to create a "glass-sea" effect, allowing the background colors to bleed through softly.

## Shapes

The shape language is defined by **Pill-shaped (Level 3)** roundedness. This extreme rounding softens the technical nature of the Geist typeface and the complexity of enterprise data.

Every interactive element—from buttons to input fields—utilizes large corner radii to create a friendly, approachable feel. Secondary containers and cards follow this logic with a minimum of 16px (`rounded-lg`) to 32px (`rounded-xl`) corner radii. This fluidity in shape represents the organic "sea green" theme, avoiding the harshness of sharp right angles.

## Components

### Buttons
Buttons are fully pill-shaped. **Primary buttons** use the Sea Green (#40916C) with white Geist Medium text. **Secondary buttons** use a ghost style with a 1.5px sea green border or a soft tinted fill (#D8F3DC).

### Input Fields
Inputs are rounded-xl (1rem) with a #F0F7F4 fill and a subtle border. On focus, the border transitions to the primary sea green with a soft, glowing outer ring tinted in the same hue.

### Cards
Cards are the primary container. They should have no visible shadow by default, instead using the #F0F7F4 surface color and a 1px border (#D8F3DC) to separate themselves from the background.

### Chips & Tags
Chips are small, fully pill-shaped elements using high-contrast combinations of the green palette (e.g., #1B4332 text on #D8F3DC background) to denote status or categories without overwhelming the layout.

### Data Tables
Tables should use "zebra-striping" with the surface tint (#F0F7F4) rather than horizontal lines to keep the UI clean and minimize visual noise.