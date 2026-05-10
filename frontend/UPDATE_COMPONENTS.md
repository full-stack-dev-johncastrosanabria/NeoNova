# Quick Component Update Guide

## Files Created ✅
1. `/src/i18n/config.ts` - i18n setup
2. `/src/i18n/locales/en.ts` - English translations
3. `/src/i18n/locales/es.ts` - Spanish translations
4. `/src/contexts/ThemeContext.tsx` - Theme provider
5. `/src/components/ui/theme-toggle.tsx` - Theme switcher
6. `/src/components/ui/language-selector.tsx` - Language switcher
7. `/src/components/ui/animated-background.tsx` - Advanced background
8. `tailwind.config.ts` - Converted from JS, added dark mode
9. `postcss.config.ts` - Converted from JS

## Quick Updates Needed

### 1. Login Page - Add to imports:
```tsx
import { useTranslation } from 'react-i18next'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { LanguageSelector } from '@/components/ui/language-selector'
import { AnimatedBackground } from '@/components/ui/animated-background'
```

### 2. Login Page - Add in component:
```tsx
const { t } = useTranslation()
```

### 3. Login Page - Replace background div:
```tsx
<div className="min-h-screen relative">
  <AnimatedBackground />
  
  {/* Add controls */}
  <div className="absolute top-4 right-4 flex gap-2 z-20">
    <LanguageSelector />
    <ThemeToggle />
  </div>
  
  <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
    {/* Rest of your content */}
  </div>
</div>
```

### 4. Replace Text Strings:
```tsx
// Title
{t('auth.welcomeBack')} or {t('auth.createAccount')}

// Subtitle  
{t('auth.enterCredentials')} or {t('auth.signUpMessage')}

// Labels
{t('auth.name')}
{t('auth.email')}
{t('auth.password')}

// Buttons
{isLogin ? t('auth.login') : t('auth.register')}

// Toggle text
{isLogin ? t('auth.dontHaveAccount') : t('auth.alreadyHaveAccount')}

// Footer
{t('footer.poweredBy')}
```

### 5. Chat Page - Add to Sidebar:
```tsx
// In sidebar header, add:
<div className="flex gap-1">
  <LanguageSelector />
  <ThemeToggle />
</div>
```

### 6. Add Dark Mode Classes:
Replace all color classes with dark variants:
```tsx
// Backgrounds
bg-white → bg-white dark:bg-gray-800
bg-gray-50 → bg-gray-50 dark:bg-gray-900

// Text
text-gray-900 → text-gray-900 dark:text-gray-100
text-gray-700 → text-gray-700 dark:text-gray-300

// Borders
border-gray-200 → border-gray-200 dark:border-gray-700
```

## Test Checklist
- [ ] Theme toggle works (light/dark/system)
- [ ] Language switcher works (EN/ES)
- [ ] Animated background displays
- [ ] All text is translated
- [ ] Dark mode colors look good
- [ ] Animations work in both themes
