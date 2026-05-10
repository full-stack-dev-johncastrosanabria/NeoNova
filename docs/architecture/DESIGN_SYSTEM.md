# NeoNova AI - Design System Reference

## 🎨 Color Palette

### Primary Colors
```css
Primary (Sky Blue):
- 500: #0ea5e9
- 600: #0284c7
- 700: #0369a1

Secondary (Purple):
- 500: #a855f7
- 600: #9333ea
- 700: #7e22ce
```

### Background Colors
```css
Main Background: bg-gray-950
Sidebar: bg-gray-900/50 (with backdrop-blur-xl)
Cards/Surfaces: bg-white/5
Hover States: bg-white/10
Active States: bg-white/10
```

### Border Colors
```css
Default: border-white/10
Hover: border-white/20
Dividers: border-gray-800/30 or border-gray-800/50
```

### Text Colors
```css
Primary: text-gray-100
Secondary: text-gray-300
Tertiary: text-gray-400
Muted: text-gray-500
Very Muted: text-gray-600
```

---

## 📐 Spacing Scale

### Padding
```css
Tight: p-2 (8px)
Small: p-3 (12px)
Medium: p-4 (16px)
Large: p-6 (24px)
XLarge: p-8 (32px)
```

### Gaps
```css
Tight: gap-0.5 (2px)
Small: gap-1 (4px)
Medium: gap-2 (8px)
Large: gap-3 (12px)
XLarge: gap-4 (16px)
```

### Spacing Between Elements
```css
List items: space-y-0.5 (2px)
Sections: space-y-4 (16px)
Messages: space-y-6 (24px)
```

---

## 🔤 Typography

### Font Sizes
```css
XSmall: text-[11px] (Headers, labels)
Small: text-xs (12px) (Timestamps, meta)
Base: text-sm (14px) (Sidebar, buttons)
Medium: text-[15px] (Messages, input)
Large: text-lg (18px) (Descriptions)
XLarge: text-3xl (30px) (Headings)
```

### Line Heights
```css
Tight: leading-6 (1.5)
Normal: leading-7 (1.75)
Relaxed: leading-8 (2)
```

### Font Weights
```css
Normal: font-normal (400)
Medium: font-medium (500)
Semibold: font-semibold (600)
```

---

## 🎯 Component Patterns

### Glassmorphism Effect
```tsx
className="bg-white/5 backdrop-blur-xl border border-white/10"
```

### Gradient Buttons
```tsx
className="bg-gradient-to-br from-primary-500 to-secondary-500"
```

### Hover States
```tsx
// Subtle
className="hover:bg-white/5"

// Medium
className="hover:bg-white/10"

// With border
className="hover:border-white/20"

// With scale
className="hover:scale-105 transition-transform"
```

### Focus States
```tsx
className="focus-within:border-white/20 focus-within:bg-white/[0.07]"
```

---

## 🎭 Animation Patterns

### Fade In
```tsx
className="animate-fade-in"
// Duration: 0.5s
```

### Fade In Up
```tsx
className="animate-fade-in-up"
// Duration: 0.6s
// With delay:
style={{ animationDelay: '0.1s' }}
```

### Float
```tsx
className="animate-float"
// Duration: 3s infinite
```

### Staggered List Animations
```tsx
{items.map((item, index) => (
  <div
    key={item.id}
    className="animate-fade-in-up"
    style={{ animationDelay: `${index * 0.05}s` }}
  >
    {item.content}
  </div>
))}
```

---

## 🧩 Component Specifications

### Sidebar
```tsx
Width: w-64 (256px)
Background: bg-gray-900/50 backdrop-blur-xl
Border: border-r border-gray-800/50
Padding: p-2 to p-3
```

### Conversation Item
```tsx
Padding: px-2 py-1.5
Border Radius: rounded-md
Font Size: text-sm
Active: bg-white/10 text-gray-100
Hover: bg-white/5 text-gray-200
```

### Message Bubble (User)
```tsx
Background: bg-gradient-to-br from-primary-500 to-secondary-500
Text: text-white
Border Radius: rounded-2xl rounded-tr-sm
Padding: p-4
Max Width: max-w-[85%]
Alignment: Right
```

### Message Bubble (AI)
```tsx
Background: bg-white/5
Border: border-white/10
Text: text-gray-100
Border Radius: rounded-2xl rounded-tl-sm
Padding: p-4
Max Width: max-w-[85%]
Alignment: Left
```

### Avatar
```tsx
Size: w-8 h-8
Border Radius: rounded-full
Icon Size: w-4 h-4
User: bg-gradient-to-br from-gray-700 to-gray-800
AI: bg-gradient-to-br from-primary-500 to-secondary-500
```

### Input Container
```tsx
Background: bg-white/5
Border: border-white/10
Border Radius: rounded-2xl
Padding: p-3
Focus: border-white/20 bg-white/[0.07]
```

### Textarea
```tsx
Background: bg-transparent
Text: text-gray-100
Placeholder: placeholder-gray-500
Font Size: text-[15px]
Line Height: leading-6
Max Height: max-h-[200px]
```

### Send Button (Active)
```tsx
Background: bg-gradient-to-br from-primary-500 to-secondary-500
Hover: from-primary-600 to-secondary-600
Shadow: shadow-lg hover:shadow-xl
Scale: hover:scale-105
Padding: p-2
Border Radius: rounded-lg
```

### Send Button (Disabled)
```tsx
Background: bg-white/5
Text: text-gray-600
Cursor: cursor-not-allowed
```

### Suggested Prompt Card
```tsx
Background: bg-white/5 hover:bg-white/10
Border: border-white/10 hover:border-white/20
Border Radius: rounded-xl
Padding: p-4
Icon Container: w-10 h-10 rounded-lg
Icon: w-5 h-5
```

---

## 🎨 Gradient Presets

### Primary Gradient
```tsx
className="bg-gradient-to-br from-primary-500 to-secondary-500"
```

### Icon Gradients
```tsx
// Blue
className="bg-gradient-to-br from-blue-500 to-cyan-500"

// Purple
className="bg-gradient-to-br from-purple-500 to-pink-500"

// Green
className="bg-gradient-to-br from-green-500 to-emerald-500"

// Orange
className="bg-gradient-to-br from-orange-500 to-yellow-500"
```

---

## 🔧 Utility Patterns

### Truncate Text
```tsx
className="truncate"
// Or with flex:
className="flex-1 min-w-0"
<p className="truncate">Long text...</p>
```

### Center Content
```tsx
className="flex items-center justify-center"
```

### Flex with Gap
```tsx
className="flex items-center gap-2"
```

### Sticky Bottom
```tsx
className="sticky bottom-0"
```

### Backdrop Blur
```tsx
className="backdrop-blur-xl"
```

### Pointer Events None
```tsx
className="pointer-events-none"
```

---

## ♿ Accessibility Patterns

### Button with ARIA Label
```tsx
<button
  aria-label="Send message"
  className="..."
>
  <Send className="w-5 h-5" />
</button>
```

### Keyboard Navigation
```tsx
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit()
  }
}
```

### Focus Visible
```tsx
className="focus-visible:ring-2 focus-visible:ring-primary-500"
```

---

## 📱 Responsive Patterns

### Max Width Container
```tsx
className="max-w-3xl mx-auto"
// 768px max width, centered
```

### Responsive Padding
```tsx
className="px-4 md:px-6 lg:px-8"
```

### Responsive Grid
```tsx
className="grid grid-cols-1 md:grid-cols-2 gap-3"
```

---

## 🎯 Best Practices

### DO ✅
- Use glassmorphism for overlays
- Keep opacity values consistent (5%, 10%, 20%)
- Use subtle animations (0.3-0.6s)
- Maintain proper contrast ratios
- Use semantic HTML
- Add ARIA labels
- Use proper TypeScript types
- Keep components focused and small

### DON'T ❌
- Use heavy borders
- Overuse animations
- Mix opacity scales randomly
- Use divs for interactive elements
- Forget keyboard navigation
- Use array indices as keys
- Create overly complex components
- Ignore accessibility

---

## 📚 Component Library

### Core Components Used
- `Button` - From UI library
- `LoadingSpinner` - From UI library
- `ThemeToggle` - Theme switcher
- `LanguageSelector` - i18n selector
- `AnimatedBackground` - Subtle background

### Icons (Lucide React)
- `Sparkles` - Logo, AI branding
- `MessageSquarePlus` - New chat
- `Send` - Send message
- `Trash2` - Delete
- `LogOut` - Sign out
- `User` - User avatar
- `Bot` - AI avatar
- `AlertCircle` - Errors
- `Paperclip` - Attachments
- `Code`, `Mail`, `FileText`, `Lightbulb` - Suggested prompts

---

## 🎨 Design Principles

1. **Minimalism** - Remove unnecessary elements
2. **Hierarchy** - Clear visual structure
3. **Consistency** - Systematic patterns
4. **Accessibility** - Inclusive design
5. **Performance** - Optimized animations
6. **Clarity** - Obvious interactions
7. **Polish** - Attention to detail
8. **Focus** - Conversation-first

---

**Version:** 1.0.0  
**Last Updated:** 2026-05-09
