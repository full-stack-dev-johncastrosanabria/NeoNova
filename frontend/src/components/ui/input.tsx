import { forwardRef, type InputHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, type = 'text', ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          type={type}
          className={cn(
            'flex h-10 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm',
            'placeholder:text-gray-400',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent focus:shadow-lg',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'transition-all duration-200',
            'hover:border-gray-400',
            error && 'border-red-500 focus:ring-red-500 animate-shake',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-red-600 animate-slide-down">{error}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
