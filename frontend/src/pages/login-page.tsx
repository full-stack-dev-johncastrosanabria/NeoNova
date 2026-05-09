import { useState, Suspense } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { useLogin, useRegister } from '@/hooks/use-api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
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
  
  const navigate = useNavigate()
  
  const loginMutation = useLogin({
    onSuccess: (data) => {
      console.log('Login successful, token saved:', data.token.substring(0, 20) + '...')
      console.log('Navigating to /chat...')
      // Use window.location as fallback if navigate doesn't work
      try {
        navigate({ to: '/chat' })
        console.log('Navigate called successfully')
      } catch (error) {
        console.error('Navigate error:', error)
        window.location.href = '/chat'
      }
    },
    onError: (err) => {
      console.error('Login error:', err)
      setError(err.message || 'Login failed')
    },
  })
  
  const registerMutation = useRegister({
    onSuccess: (data) => {
      console.log('Registration successful, token saved:', data.token.substring(0, 20) + '...')
      console.log('Navigating to /chat...')
      // Use window.location as fallback if navigate doesn't work
      try {
        navigate({ to: '/chat' })
        console.log('Navigate called successfully')
      } catch (error) {
        console.error('Navigate error:', error)
        window.location.href = '/chat'
      }
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
      setError('Please fill in all fields')
      return
    }

    if (!isLogin && !displayName) {
      setError('Please enter your name')
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
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md animate-fade-in">
        {/* Logo/Brand */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-600 to-secondary-600 mb-4 shadow-lg">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">NeoNova AI</h1>
          <p className="text-gray-600 mt-2">Your intelligent assistant</p>
        </div>

        <Card className="shadow-xl border-0 animate-slide-up">
          <CardHeader>
            <CardTitle>{isLogin ? 'Welcome back' : 'Create account'}</CardTitle>
            <CardDescription>
              {isLogin 
                ? 'Enter your credentials to access your account' 
                : 'Sign up to start your AI journey'}
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Display Name Input (Register only) */}
              {!isLogin && (
                <div className="space-y-2">
                  <label htmlFor="displayName" className="text-sm font-medium text-gray-700">
                    Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <Input
                      id="displayName"
                      type="text"
                      placeholder="Your name"
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      className="pl-10"
                      disabled={isLoading}
                      autoComplete="name"
                    />
                  </div>
                </div>
              )}

              {/* Email Input */}
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium text-gray-700">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-10"
                    disabled={isLoading}
                    autoComplete="email"
                  />
                </div>
              </div>

              {/* Password Input */}
              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium text-gray-700">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    disabled={isLoading}
                    autoComplete={isLogin ? 'current-password' : 'new-password'}
                  />
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200 animate-slide-down">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full"
                isLoading={isLoading}
              >
                {isLogin ? 'Sign in' : 'Create account'}
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
                    window.location.href = '/chat'
                  }}
                >
                  [Debug] Go to Chat
                </Button>
              )}
            </form>

            {/* Toggle Login/Register */}
            <div className="mt-6 text-center">
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin)
                  setError('')
                }}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors"
                disabled={isLoading}
              >
                {isLogin 
                  ? "Don't have an account? Sign up" 
                  : 'Already have an account? Sign in'}
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-8">
          Powered by advanced AI technology
        </p>
      </div>
    </div>
  )
}
