import { forwardRef, type ButtonHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
import { LoadingSpinner } from './loading-spinner'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    className, 
    variant = 'primary', 
    size = 'md', 
    isLoading = false,
    disabled,
    children,
    ...props 
  }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95'
    
    const variants = {
      primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 shadow-md hover:shadow-lg',
      secondary: 'bg-secondary-100 text-secondary-900 hover:bg-secondary-200 active:bg-secondary-300 shadow-sm hover:shadow-md',
      outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 active:bg-primary-100 hover:border-primary-700',
      ghost: 'text-gray-700 hover:bg-gray-100 active:bg-gray-200',
      danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 shadow-md hover:shadow-lg',
    }
    
    const sizes = {
      sm: 'h-8 px-3 text-sm gap-1.5',
      md: 'h-10 px-4 text-base gap-2',
      lg: 'h-12 px-6 text-lg gap-2.5',
    }

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && <LoadingSpinner size="sm" className="mr-2" />}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
