---
name: Obsidian Intel
colors:
  surface: '#10131b'
  surface-dim: '#10131b'
  surface-bright: '#363942'
  surface-container-lowest: '#0b0e16'
  surface-container-low: '#181b24'
  surface-container: '#1c1f28'
  surface-container-high: '#272a32'
  surface-container-highest: '#32353d'
  on-surface: '#e0e2ee'
  on-surface-variant: '#c4c6d0'
  inverse-surface: '#e0e2ee'
  inverse-on-surface: '#2d3039'
  outline: '#8e909a'
  outline-variant: '#44474f'
  surface-tint: '#adc6ff'
  primary: '#d8e2ff'
  on-primary: '#122f5f'
  primary-container: '#adc6ff'
  on-primary-container: '#385283'
  inverse-primary: '#455e90'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00b47d'
  on-secondary-container: '#003e28'
  tertiary: '#ffdbcc'
  on-tertiary: '#51240d'
  tertiary-container: '#ffb595'
  on-tertiary-container: '#7a442b'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#2c4677'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdbcd'
  tertiary-fixed-dim: '#ffb596'
  on-tertiary-fixed: '#360f00'
  on-tertiary-fixed-variant: '#6c3921'
  background: '#10131b'
  on-background: '#e0e2ee'
  surface-variant: '#32353d'
  background-deep: '#030303'
  surface-glass: rgba(255, 255, 255, 0.03)
  border-glass: rgba(255, 255, 255, 0.08)
  glow-primary: rgba(173, 198, 255, 0.05)
  error-red: '#ffb4ab'
  warning-yellow: '#fcd667'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Geist
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-desktop: 40px
  sidebar-width: 256px
  header-height: 64px
---

## Brand & Style

Obsidian Intel represents the pinnacle of Enterprise AI surveillance and analytics. The brand personality is **technical, high-fidelity, and authoritative**, designed for security operations centers and retail executive suites. 

The visual style is a sophisticated blend of **Glassmorphism** and **Minimalism**. It utilizes deep obsidian backgrounds, vibrant data-driven accents, and translucent layers to create a sense of infinite depth. The interface feels like a "digital command center"—precise, real-time, and futuristic, yet highly functional and corporate.

## Colors
The palette is centered on a **true black background (#030303)** to maximize contrast for the glass effects. 

- **Primary (Blue-Grey #adc6ff):** Used for main interactive elements, primary metrics, and system status.
- **Secondary (Mint #4edea3):** Signifies "Health," "Live" status, and positive growth trends.
- **Tertiary (Peach #ffb595):** Reserved for warnings, loss prevention alerts, and heatmaps.
- **Surface Strategy:** Backgrounds utilize `surface-container` variants, but the primary aesthetic driver is the translucent glass card, which uses low-opacity white fills and high-blur backdrops to separate content layers.

## Typography
The system uses a tri-font approach to balance technical precision with readability:
- **Geist** for headlines and display values, providing a clean, modern, and slightly technical "developer-tool" feel.
- **Inter** for all body copy and standard UI text to ensure maximum legibility at small sizes.
- **JetBrains Mono** for metadata, system IDs (e.g., STORE_042), and secondary metrics. This reinforces the "intelligence data" aspect of the brand.

Large data numbers (KPIs) should use `headline-md` or `display-lg` with Geist to emphasize numerical impact.

## Layout & Spacing
The layout follows a **structured 12-column fluid grid** with generous 24px gutters. 

- **Navigation:** A fixed 256px (64 units) sidebar on the left and a 64px fixed header.
- **Margins:** Desktop views use a 40px outer margin for breathability.
- **Responsibility:** On tablet, the 12-column grid collapses to 6 columns. On mobile, cards stack vertically into a single column with 16px margins. 
- **Rhythm:** All spacing and padding are multiples of the 4px base unit.

## Elevation & Depth
Depth is not communicated through shadows, but through **material properties and light simulation**:

- **Glassmorphism:** Components use `backdrop-filter: blur(20px)` and a thin 1px border. The top border is slightly more opaque than the others to simulate a top-down light source hitting the "edge" of the glass.
- **Layering:** The base background is #030303. Level 1 surfaces are `surface-container` (translucent). Level 2 surfaces (hover states) increase border opacity and brightness.
- **Glow Effects:** Critical components utilize subtle radial gradients (`glow-primary` or `glow-secondary`) positioned behind the cards to create a "bloom" effect, suggesting the screen is emitting high-energy light.

## Shapes
The system uses **Soft (Level 1)** roundedness to maintain a professional, slightly sharp edge.

- **Standard Cards:** 12px (rounded-xl) for main dashboard components.
- **Buttons & Inputs:** 8px (rounded-lg) or full pill-shape for search bars and tags.
- **Visuals:** Circular elements are used exclusively for progress rings and status indicators to contrast against the predominantly rectangular grid.

## Components

- **Glass Cards:** The primary container. Must have a 1px border (`white/10`) and a subtle inner glow on hover.
- **Action Buttons:** Active states should use the secondary color (#4edea3) with a low-opacity background and a 2px left border for navigation items.
- **Inputs:** Search fields are fully rounded (pill), using a `white/5` background and expanding/glowing on focus.
- **KPI Metrics:** Large numerical display using Geist, paired with a small SVG sparkline and a mono-spaced label.
- **Status Indicators:** Small 8px circles with a "subtle pulse" animation to denote live data streams or active system health.
- **Data Funnels:** Horizontal bars with `origin-left` scale-in animations and 20% opacity fills of the primary or secondary color.