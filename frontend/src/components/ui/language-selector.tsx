import { Languages } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { Button } from './button'
import { useState } from 'react'
import { cn } from '@/lib/utils'

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
]

export function LanguageSelector() {
  const { i18n, t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng)
    setIsOpen(false)
  }

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0]

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="gap-2"
        title={t('language.changeLanguage')}
      >
        <Languages className="h-5 w-5" />
        <span className="text-sm">{currentLanguage.flag}</span>
      </Button>

      {isOpen && (
        <>
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 mt-2 w-48 rounded-lg bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 z-50 animate-scale-in">
            <div className="p-2">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  onClick={() => changeLanguage(lang.code)}
                  className={cn(
                    'w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                    i18n.language === lang.code
                      ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  )}
                >
                  <span className="text-xl">{lang.flag}</span>
                  <span>{lang.name}</span>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
