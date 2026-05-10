import { Moon, Sun } from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'
import { Button } from './button'
import { useTranslation } from 'react-i18next'

export function ThemeToggle() {
  const { theme, setTheme, actualTheme } = useTheme()
  const { t } = useTranslation()

  const toggleTheme = () => {
    if (theme === 'system') {
      setTheme('light')
    } else if (theme === 'light') {
      setTheme('dark')
    } else {
      setTheme('system')
    }
  }

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={toggleTheme}
      className="relative group"
      title={t('theme.toggleTheme')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">{t('theme.toggleTheme')}</span>
    </Button>
  )
}
