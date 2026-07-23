# Design System

## Overview

- **UI type:** Web application (server-side rendered with Jinja2 + Tailwind CSS v3 via CDN)
- **Audience:** Medical professionals (radiologists, pulmonologists)
- **Tone:** Professional, clinical, trustworthy, modern
- **Density:** Moderate — information-dense but spaced for readability
- **Accessibility target:** WCAG 2.2 AA
- **Dark mode:** supported (via Tailwind `dark:` class + localStorage toggle)

### Visual Principles

| Principle | Meaning | Applies to |
|---|---|---|
| Clarity | Medical data must be unambiguous | Layout, typography, color coding |
| Trust | Interface must inspire confidence | Consistent blue/purple accents, clean forms |
| Efficiency | Minimize clicks to diagnosis | Dashboard layout, drag-and-drop upload |
| Accessibility | Readable under all conditions | Dark/light mode, sufficient contrast |

## Colors

Palette uses Tailwind CSS v3 utility classes applied directly in templates. No custom CSS variables. Note: "gray" palette is used (Tailwind v3 unified slate→gray).

| Token | Tailwind class | Hex (light) | Usage |
|---|---|---|---|
| `background` | `bg-gray-50` / `dark:bg-gray-900` | #f9fafb / #111827 | Page background |
| `surface` | `bg-white` / `dark:bg-gray-800` | #ffffff / #1f2937 | Cards, sidebar, modals |
| `foreground` | `text-gray-800` / `dark:text-white` | #1f2937 / #ffffff | Body text |
| `muted` | `text-gray-500` / `dark:text-gray-400` | #6b7280 / #9ca3af | Secondary text |
| `border` | `border-gray-200` / `dark:border-gray-700` | #e5e7eb / #374151 | Dividers, input borders |
| `primary` | `bg-blue-600` / `text-blue-600` | #2563eb | Buttons, links, active states |
| `primary-hover` | `hover:bg-blue-700` | #1d4ed8 | Button hover |
| `secondary` | `bg-purple-500/600` / `text-purple-400/500/600` | #a855f7 / #9333ea | Training page accents, gradients |
| `success` | `text-green-600` / `bg-green-50` | #16a34a / #f0fdf4 | Normal diagnosis |
| `danger` | `text-red-600` / `bg-red-50` | #dc2626 / #fef2f2 | Pneumonia diagnosis |
| `warning` | `text-yellow-600` / `bg-yellow-50` | #ca8a04 / #fefce8 | Pending/warning states |
| `focus` | `focus:ring-blue-500` | #3b82f6 | Input focus ring |

### Gradients

Used in training page cards and badges. Applied via `bg-gradient-to-r`:

| Gradient | Tailwind class | Usage |
|---|---|---|
| Purple → Blue | `from-purple-600 to-blue-600` | Training page hero/section headers |
| Purple → Indigo | `from-purple-500 to-indigo-600` | Secondary accent cards |
| Red → Rose | `from-red-500 to-rose-600` | Error/warning indicators |
| Green → Emerald | `from-green-500 to-emerald-600` | Success indicators |

Dark mode strategy: All backgrounds darken 3-4 stops (gray-50 → gray-900), text lightens (gray-800 → white), borders darken (gray-200 → gray-700). Gradients also darken accordingly. Toggled via `class="light"` on `<html>` and `darkMode: 'class'` Tailwind config. Preference persisted in `localStorage`.

## Typography

| Token | Font | Size | Weight | Line height | Usage |
|---|---|---|---|---|---|
| `body` | system-ui, sans-serif | 14px (text-sm) | 400 | 1.5 | Default body text |
| `heading` | system-ui, sans-serif | 18px (text-lg) | 700 | 1.4 | Section titles |
| `title` | system-ui, sans-serif | 24px (text-2xl) | 800-900 (font-black) | 1.3 | Page titles, hero text |
| `label` | system-ui, sans-serif | 12px (text-xs) | 600 | — | Form labels, stats |
| `monospace` | monospace | 13px | 400 | 1.5 | Logs, technical data |

Font stack: `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

## Layout

- **Layout strategy:** Fixed sidebar + scrollable main content (dashboard). Full-page centered forms (login, register).
- **Max content width:** 1024px (max-w-4xl) to 1152px (max-w-5xl), depending on section
- **Breakpoints:**
  - sm: 640px (mobile landscape)
  - md: 768px (tablet; sidebar expands from 64px to 288px)
  - lg: 1024px (desktop)
  - xl: 1280px (wide desktop)

### Sidebar

| State | Width | Tailwind class |
|---|---|---|
| Collapsed (mobile) | 64px | `w-16` |
| Expanded (md+) | 288px | `w-72` |
| Expanded (xl+) | 320px | `w-80` |

### Dashboard Layout
```
+-- sidebar (64/288px) --+-- main content (flex-1, overflow-y-auto) --+
| User info + avatar     | Header / breadcrumb                       |
| Navigation (Diagnóstico)| Drop zone / results grid                 |
| History panel          | XAI heatmap 1x4 grid                     |
+------------------------+-------------------------------------------+
```

### Training Layout
```
+-- sidebar (64/288px) --+-- main content (flex-1) -------------------+
| Same sidebar           | Chatbot interface (max-w-3xl centered)     |
|                        | Training controls + progress               |
|                        | Results tabs: Sessions/Models/Ranking/Ext   |
+------------------------+-------------------------------------------+
```

## Components

### Interactive States

| State | Visual rule | Accessibility rule |
|---|---|---|
| Default | Solid background or outline | Minimum contrast 4.5:1 |
| Hover | Background darkens 1 shade; `group-hover` effects | Do not rely on hover-only affordances |
| Focus | Ring-2 with blue-500 | Must be visible for keyboard users |
| Disabled | Opacity 75%, cursor not-allowed | Must communicate unavailable state |
| Error | Red border + red text message | Must include text, not color alone |

### Component Catalog

| Component | Variants | States | Notes |
|---|---|---|---|
| Button | Primary (blue gradient), Ghost (transparent) | Default, hover, active, disabled | Rounded-xl, px-4 py-2, shadow |
| Input | Text, file (hidden), select, file drag-drop | Default, focus, error, disabled | Rounded-lg, border, shadow-sm |
| Card | Dashboard card, result card, training card | Default, hover (group-hover) | Rounded-2xl, shadow, border, bg-white |
| Modal | Image modal (fullscreen overlay) | Open, closed | Centered, backdrop-blur, cursor-zoom |
| Sidebar | Collapsed (w-16), expanded (w-72/w-80) | — | Fixed, scrollable, dark bg (slate-800/900) |
| Drop zone | File upload area | Default, drag-over, success, error | Dashed border, centered icon, rounded-2xl |
| Chat bubble | User (right, blue), AI (left, gray) | Default, typing indicator | Rounded-2xl, max-w-sm / max-w-3xl / max-w-[85%] |
| Tabs | Sessions, Models, Ranking, External | Active (underline/border-b-2), inactive | Horizontal tab bar, divide-x |
| Badge | Status indicator | In Progress (yellow), Completed (green), Failed (red) | Rounded-full, colored bg, text-xs |

### Custom CSS Classes

Defined in `<style>` blocks within templates:

| Class | Properties | Usage |
|---|---|---|
| `.chat-bubble-ai` | bg-white/gray-100, rounded-2xl, rounded-bl | AI chat messages |
| `.chat-bubble-user` | bg-blue-600, rounded-2xl, rounded-br, text-white | User chat messages |
| Custom scrollbar | ::-webkit-scrollbar width 6-8px | Scrollable panels |

## Do's and Don'ts

- **Update** when a reusable token, component variant, layout rule, or accessibility rule changes.
- **Do not update** for normal use of existing components or one-off visual details.

### Known Exceptions

| Exception | Reason | Scope |
|---|---|---|
| None | — | — |
