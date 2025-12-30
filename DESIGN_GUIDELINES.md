# DrinkShelf - UI/UX Design Guidelines

## Theme: Modern Heritage / Refined Speakeasy

### Design Philosophy
- **Elegance**: Sophisticated, upscale aesthetic
- **Heritage**: Vintage touches with modern clarity
- **Functionality**: Intuitive navigation and clear information hierarchy
- **Refinement**: Premium feel without excessive ornamentation
- **Approachability**: Welcoming despite the upscale theme

---

## Color Palette

### Primary Colors
```
Deep Charcoal: #1a1a1a (Primary background)
Rich Gold: #d4af37 (Accent, premium feel)
Warm Copper: #b87333 (Secondary accent)
Cream White: #f5f1e8 (Primary text, backgrounds for contrast)
```

### Secondary Colors
```
Amber: #ffd700 (Highlights, alerts)
Dark Brown: #3d2817 (Depth, shadows)
Sage Green: #6b8e5f (Subtle accents, balance)
Burgundy: #8b3a3a (Emphasis, premium spirits)
```

### Neutral Palette
```
Light Gray: #e8e8e8 (Borders, dividers)
Medium Gray: #a0a0a0 (Secondary text)
Dark Gray: #4a4a4a (Tertiary text)
```

### Semantic Colors
```
Success: #2d5a2d (Green)
Warning: #d4a537 (Gold/Amber)
Error: #a83a3a (Red/Burgundy)
Info: #4a7c9e (Blue)
```

### Color Usage
- **Backgrounds**: Deep Charcoal (#1a1a1a) with Cream White (#f5f1e8) accents
- **Buttons**: Rich Gold (#d4af37) primary, Warm Copper (#b87333) secondary
- **Hover States**: Increase brightness by 10-15%
- **Text**: Cream White on dark backgrounds, Dark Gray/Charcoal on light
- **Accents**: Rich Gold for premium/rare items, Burgundy for high-value bottles

---

## Typography

### Font Family
- **Headlines**: "Playfair Display" or similar serif (luxury feel)
- **Body**: "Inter" or "Roboto" (modern, readable)
- **Monospace**: "Fira Code" or "Consolas" (data/code display)

### Font Sizes & Weights
```
H1: 48px, 700 weight (page titles)
H2: 36px, 700 weight (section headers)
H3: 24px, 600 weight (subsection headers)
H4: 20px, 600 weight (component headers)
Body: 16px, 400 weight (regular text)
Small: 14px, 400 weight (metadata, secondary info)
Captions: 12px, 400 weight (hints, help text)
```

### Line Height
- Headlines: 1.2
- Body: 1.6
- Compact: 1.4

---

## Layout & Spacing

### Grid System
- Base unit: 8px
- 12-column responsive grid
- Breakpoints:
  - Mobile: 320px - 640px (single column)
  - Tablet: 641px - 1024px (2-3 columns)
  - Desktop: 1025px+ (3-4 columns)

### Spacing Scale
```
xs: 4px
sm: 8px
md: 16px
lg: 24px
xl: 32px
xxl: 48px
```

### Component Spacing
- Padding: 16px - 24px for most components
- Margin: 24px - 32px between sections
- Gap (flex/grid): 16px - 24px

---

## Components

### Bottles Card
```
┌─────────────────────────────┐
│  [Image placeholder]        │
│  ▲                          │ (Rating stars)
├─────────────────────────────┤
│  Bottle Name                │ (Bold, 18px)
│  Distillery · Proof %       │ (14px, secondary)
├─────────────────────────────┤
│ $XX.XX                      │ (Price, 16px, bold)
│ ⭐⭐⭐⭐⭐ (4.2)             │ (Rating)
├─────────────────────────────┤
│  [View] [Edit] [Delete]     │ (Action buttons)
└─────────────────────────────┘
```

**Styling:**
- Background: #2a2a2a (slightly lighter than page background)
- Border: 1px solid #d4af37
- Border-radius: 8px
- Padding: 16px
- Hover: Slight shadow increase, border glow
- Transition: 0.3s ease-in-out

### Button Styles

#### Primary Button
```
Background: #d4af37
Color: #1a1a1a
Padding: 12px 24px
Border-radius: 6px
Font-weight: 600
Border: none
Cursor: pointer
Transition: 0.2s
Hover: Background #e5c158, box-shadow: 0 4px 12px rgba(212,175,55,0.3)
```

#### Secondary Button
```
Background: transparent
Color: #d4af37
Padding: 12px 24px
Border: 2px solid #d4af37
Border-radius: 6px
Font-weight: 600
Transition: 0.2s
Hover: Background: #d4af37, Color: #1a1a1a
```

#### Ghost Button
```
Background: transparent
Color: #d4af37
Padding: 12px 24px
Border: none
Font-weight: 600
Transition: 0.2s
Hover: Color: #e5c158
```

### Input Fields
```
Background: #2a2a2a
Border: 1px solid #4a4a4a
Color: #f5f1e8
Padding: 12px 16px
Border-radius: 6px
Font-size: 16px
Focus: Border-color: #d4af37, Box-shadow: 0 0 0 3px rgba(212,175,55,0.2)
```

### Form Labels
```
Font-size: 14px
Font-weight: 600
Color: #d4af37
Margin-bottom: 8px
```

### Modal/Overlay
```
Background: rgba(0, 0, 0, 0.8)
Backdrop-filter: blur(4px)
Content Background: #1a1a1a
Border: 1px solid #d4af37
Border-radius: 12px
Padding: 32px
Box-shadow: 0 20px 60px rgba(0,0,0,0.6)
```

### Navigation
```
Background: #0f0f0f (darker than main background)
Height: 64px
Border-bottom: 2px solid #d4af37
Position: sticky/fixed at top
Items: Flexbox, spaced 24px apart
Active item: Color #d4af37, underline
Hover: Color #d4af37 with 0.2s transition
```

### Shelf Visualization
```
Grid Layout: 3-4 columns
Card Ratio: 3:4 (portrait)
Cards: Rotated slightly (-1° to 1°) for visual interest
Spacing: 16px gap
Hover: Scale 1.05, rotate 0°, shadow increase
Animation: 0.3s ease-out
```

---

## Page Layouts

### Dashboard / Collection View
```
┌────────────────────────────────────────┐
│  DrinkShelf Logo      [Search] [Menu]  │ Navigation
├────────────────────────────────────────┤
│                                        │
│  Welcome Back, Username!               │ Hero Section
│  You have XX bottles in your collection│
│                                        │
├────────────────────────────────────────┤
│  Collection Stats (4 columns)          │
│  [Total] [Value] [Avg Rating] [Types]  │
├────────────────────────────────────────┤
│                                        │
│  Filters: [Type ▼] [Proof ▼] [Sort ▼] │ Filtering
│                                        │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ ▶️  │ │Bottle│ │Bottle│ │Bottle│    │ Shelf View
│  │     │ │     │ │     │ │     │    │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                        │
│  [< Previous] [1][2][3][4][5] [Next >]│ Pagination
└────────────────────────────────────────┘
```

### Add/Edit Bottle Form
```
┌────────────────────────────────────────┐
│  Add New Bottle                    [×] │ Header
├────────────────────────────────────────┤
│                                        │
│  Bottle Name *                         │ Form Section
│  [_________________] [AI Research]    │
│                                        │
│  Spirit Type *                         │
│  [Whiskey ▼]                          │
│                                        │
│  [Two-column layout for next fields]   │
│  Proof        │  Age Statement         │
│  [_____]      │  [_____]              │
│                                        │
│  Distillery              Region        │
│  [_______________]  [_______________]  │
│                                        │
│  [Additional Fields...]                │
│                                        │
│  ┌─────────────────────────────────┐   │
│  │ Notes & Additional Details      │   │
│  │                                 │   │
│  │ [Large text area for notes]    │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                        │
│  Image Upload: [Choose File] [Preview] │
│                                        │
│  [Cancel]                   [Save]    │ Actions
└────────────────────────────────────────┘
```

### Search Results
```
┌────────────────────────────────────────┐
│  Search Results for "bourbon"      [×] │
├────────────────────────────────────────┤
│  Filters: [Whiskey] [Proof: 80-100]   │
│  Sort: [Relevance ▼]                  │
├────────────────────────────────────────┤
│                                        │
│  Showing 1-20 of 247 results           │
│                                        │
│  Search Result List:                   │
│  ┌──────────────────────────────────┐  │
│  │ ▶️ 1792 Small Batch               │ Result Item
│  │    Proof: 100  |  $25.99          │
│  │    Barton 1792 Distillery · KY    │ Full Row Click
│  │    ⭐⭐⭐⭐☆ (4.2/5)              │
│  │    [Add to Collection] [Details]  │
│  └──────────────────────────────────┘  │
│                                        │
│  [< Previous] [1][2][3]...[24] [Next >]│ Pagination
└────────────────────────────────────────┘
```

---

## Interactions & Animations

### Transitions
- Default: 0.2s - 0.3s ease-out
- Slower: 0.5s ease-out (modals, major layout shifts)
- Instant: Interactions that don't need animation

### Hover Effects
- Buttons: Color shift + subtle shadow
- Cards: Scale 1.02 + shadow increase
- Links: Color change + underline
- Shelf items: Slight rotation correction + scale

### Loading States
- Spinner: Rotating gold circle with dark outline
- Skeleton screens: Pulsing gradient placeholders
- Progress bar: Gold gradient bar at top of form
- Submit button: "Loading..." text with spinner

### Empty States
- Icon: Large, centered, in secondary color
- Message: "No bottles yet" or similar
- CTA: Clear call-to-action button
- Background: Subtle pattern or gradient

---

## Accessibility (A11y)

### Color Contrast
- Text on background: Minimum 4.5:1 ratio for normal text
- Text on background: Minimum 3:1 ratio for large text
- Use color + additional visual indicators (icons, text)

### Focus States
- All interactive elements must have visible focus
- Focus indicator: 2px solid border in gold (#d4af37)
- Focus outline: Offset 2px from element

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate buttons
- Arrow keys for list navigation
- Escape to close modals/overlays

### Semantic HTML
- Use proper heading hierarchy (H1 → H2 → H3)
- Buttons are `<button>` not `<div>`
- Forms use `<label>` for accessibility
- Images have descriptive `alt` text

### Screen Reader Support
- ARIA labels for icon-only buttons
- `aria-expanded` for collapse/expand
- `aria-selected` for tabs
- Role attributes where semantics aren't clear

---

## Responsive Design Breakpoints

### Mobile (320px - 640px)
- Single column layout
- Full-width cards
- Larger touch targets (48px minimum)
- Simplified navigation (hamburger menu)
- Shelf: 1-2 column grid
- Font sizes: 18px for buttons/headers

### Tablet (641px - 1024px)
- 2-3 column grid
- Optimized spacing
- Side navigation
- Shelf: 2-3 column grid
- Font sizes: Standard

### Desktop (1025px+)
- 3-4 column grid
- Full-featured layout
- Top/side navigation
- Shelf: 3-4 column grid
- Font sizes: Standard

---

## Dark Mode (Default)

The interface is designed for dark mode by default to fit the "Refined Speakeasy" theme:
- Deep backgrounds (charcoal, near-black)
- Light text (cream, white)
- Warm accents (gold, copper)
- Reduced eye strain for evening use

---

## Component States

### Bottle Card States
- **Default**: Normal appearance
- **Hover**: Scale up slightly, increase shadow
- **Selected**: Gold border, checkmark overlay
- **Disabled**: Opacity 0.5, no hover effect
- **Loading**: Skeleton screen

### Button States
- **Default**: Normal styling
- **Hover**: Darker shade, shadow
- **Active/Pressed**: Slightly inset appearance
- **Disabled**: Opacity 0.5, no cursor pointer
- **Loading**: Disabled state + spinner

---

## Visual Hierarchy

1. **H1 Titles**: 48px, 700, top-level pages
2. **H2 Titles**: 36px, 700, major sections
3. **Important Data**: 24px, 600, bottle names, key details
4. **Body Text**: 16px, 400, descriptions
5. **Secondary**: 14px, 400, metadata, timestamps
6. **Tertiary**: 12px, 400, helper text, captions

---

## Marketing Copy & Tone

- **Headlines**: Sophisticated, aspirational ("Your Collection, Refined")
- **Body**: Knowledgeable, welcoming ("Track, discover, and celebrate")
- **CTAs**: Action-oriented, premium ("Explore Your Shelf", "Add to Collection")
- **Error Messages**: Helpful, not blaming ("Let's try that again", "We couldn't find that bottle")
