export function AnimatedBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 animate-gradient bg-200%" />
      
      {/* Animated blobs */}
      <div className="absolute top-0 -left-4 w-72 h-72 bg-primary-300 dark:bg-primary-900 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-xl opacity-70 dark:opacity-30 animate-blob" />
      <div className="absolute top-0 -right-4 w-72 h-72 bg-secondary-300 dark:bg-secondary-900 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-xl opacity-70 dark:opacity-30 animate-blob animation-delay-2000" style={{ animationDelay: '2s' }} />
      <div className="absolute -bottom-8 left-20 w-72 h-72 bg-primary-300 dark:bg-primary-900 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-xl opacity-70 dark:opacity-30 animate-blob animation-delay-4000" style={{ animationDelay: '4s' }} />
      
      {/* Grid pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-[0.02] dark:opacity-[0.05]" />
      
      {/* Floating particles */}
      <div className="absolute inset-0">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-primary-400 dark:bg-primary-600 rounded-full animate-float opacity-20"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${3 + Math.random() * 4}s`,
            }}
          />
        ))}
      </div>
      
      {/* Glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-400/20 dark:bg-primary-600/10 rounded-full filter blur-3xl animate-glow" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary-400/20 dark:bg-secondary-600/10 rounded-full filter blur-3xl animate-glow" style={{ animationDelay: '1s' }} />
    </div>
  )
}

// Add this to your global CSS for the grid pattern
// .bg-grid-pattern {
//   background-image: 
//     linear-gradient(to right, currentColor 1px, transparent 1px),
//     linear-gradient(to bottom, currentColor 1px, transparent 1px);
//   background-size: 40px 40px;
// }
