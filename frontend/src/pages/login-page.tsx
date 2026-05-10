import { useState, Suspense } from 'react'
import { useTranslation } from 'react-i18next'
import { useLogin, useRegister } from '@/hooks/use-api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { LanguageSelector } from '@/components/ui/language-selector'
import { AnimatedBackground } from '@/components/ui/animated-background'
import { Sparkles, Mail, Lock, AlertCircle, User } from 'lucide-react'

export function LoginPage() {
  return (
    <Suspense fallback={<LoadingSpinner fullScreen />}>
      <LoginPageContent />
    </Suspense>
  )
}

function LoginPageContent() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [error, setError] = useState('')
  
  const { t } = useTranslation()
  
  const loginMutation = useLogin({
    onSuccess: (data) => {
      console.log('Login successful, token saved:', data.token.substring(0, 20) + '...')
      console.log('Token in localStorage:', localStorage.getItem('token')?.substring(0, 20) + '...')
      console.log('Reloading page to navigate to chat...')
      // Force a full page reload to /chat
      // This ensures the router re-evaluates the auth state
      window.location.replace('/chat')
    },
    onError: (err) => {
      console.error('Login error:', err)
      setError(err.message || 'Login failed')
    },
  })
  
  const registerMutation = useRegister({
    onSuccess: (data) => {
      console.log('Registration successful, token saved:', data.token.substring(0, 20) + '...')
      console.log('Token in localStorage:', localStorage.getItem('token')?.substring(0, 20) + '...')
      console.log('Reloading page to navigate to chat...')
      // Force a full page reload to /chat
      // This ensures the router re-evaluates the auth state
      window.location.replace('/chat')
    },
    onError: (err) => {
      console.error('Registration error:', err)
      setError(err.message || 'Registration failed')
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (!email || !password) {
      setError(t('auth.fillAllFields'))
      return
    }

    if (!isLogin && !displayName) {
      setError(t('auth.enterName'))
      return
    }

    if (isLogin) {
      loginMutation.mutate({ email, password })
    } else {
      registerMutation.mutate({ email, password, display_name: displayName })
    }
  }

  const isLoading = loginMutation.isPending || registerMutation.isPending

  return (
    <div className="min-h-screen relative">
      <AnimatedBackground />
      
      {/* Theme and Language Controls */}
      <div className="absolute top-4 right-4 flex gap-2 z-20">
        <LanguageSelector />
        <ThemeToggle />
      </div>

      <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
        <div className="w-full max-w-md">
          {/* Logo/Brand */}
          <div className="text-center mb-8 animate-fade-in-down">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-600 to-secondary-600 mb-4 shadow-lg animate-bounce-in hover:scale-110 transition-transform duration-300">
              <Sparkles className="w-8 h-8 text-white animate-pulse-slow" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white animate-fade-in-up">NeoNova AI</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              {t('footer.poweredBy')}
            </p>
          </div>

          <Card className="shadow-xl border-0 animate-scale-in backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 hover:shadow-2xl transition-shadow duration-300 dark:border-gray-700">
            <CardHeader>
              <CardTitle>{isLogin ? t('auth.welcomeBack') : t('auth.createAccount')}</CardTitle>
              <CardDescription>
                {isLogin 
                  ? t('auth.enterCredentials')
                  : t('auth.signUpMessage')}
              </CardDescription>
            </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Display Name Input (Register only) */}
              {!isLogin && (
                <div className="space-y-2 animate-slide-in-left">
                  <label htmlFor="displayName" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {t('auth.name')}
                  </label>
                  <div className="relative group">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
                    <Input
                      id="displayName"
                      type="text"
                      placeholder={t('auth.namePlaceholder')}
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      className="pl-10 transition-all duration-200 focus:scale-[1.02] dark:bg-gray-700 dark:text-white dark:border-gray-600"
                      disabled={isLoading}
                      autoComplete="name"
                    />
                  </div>
                </div>
              )}

              {/* Email Input */}
              <div className="space-y-2 animate-slide-in-left" style={{ animationDelay: !isLogin ? '0.1s' : '0s' }}>
                <label htmlFor="email" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {t('auth.email')}
                </label>
                <div className="relative group">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
                  <Input
                    id="email"
                    type="email"
                    placeholder={t('auth.emailPlaceholder')}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10 transition-all duration-200 focus:scale-[1.02] dark:bg-gray-700 dark:text-white dark:border-gray-600"
                    disabled={isLoading}
                    autoComplete="email"
                  />
                </div>
              </div>

              {/* Password Input */}
              <div className="space-y-2 animate-slide-in-left" style={{ animationDelay: !isLogin ? '0.2s' : '0.1s' }}>
                <label htmlFor="password" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {t('auth.password')}
                </label>
                <div className="relative group">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
                  <Input
                    id="password"
                    type="password"
                    placeholder={t('auth.passwordPlaceholder')}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10 transition-all duration-200 focus:scale-[1.02] dark:bg-gray-700 dark:text-white dark:border-gray-600"
                    disabled={isLoading}
                    autoComplete={isLogin ? 'current-password' : 'new-password'}
                  />
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 animate-shake">
                  <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 animate-bounce-subtle" />
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full group relative overflow-hidden"
                isLoading={isLoading}
              >
                <span className="relative z-10">{isLogin ? t('auth.login') : t('auth.register')}</span>
                <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-secondary-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </Button>

              {/* Debug: Manual navigation button */}
              {import.meta.env.DEV && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => {
                    console.log('Manual navigation to /chat')
                    window.location.replace('/chat')
                  }}
                >
                  [Debug] Go to Chat
                </Button>
              )}
            </form>

            {/* Toggle Login/Register */}
            <div className="mt-6 text-center animate-fade-in">
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin)
                  setError('')
                }}
                className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-all duration-200 hover:scale-105 inline-block"
                disabled={isLoading}
              >
                {isLogin 
                  ? t('auth.dontHaveAccount')
                  : t('auth.alreadyHaveAccount')}
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 dark:text-gray-400 mt-8 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          {t('footer.poweredBy')}
        </p>
        </div>
      </div>
    </div>
  )
}
