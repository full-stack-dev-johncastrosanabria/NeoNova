# NeoNova Frontend

Modern React TypeScript frontend for the NeoNova AI Assistant with Vite build tooling.

## 🏗️ Architecture

**Modern React Stack:**
- **React 18** with TypeScript for type safety
- **Vite** for fast development and optimized builds
- **React Router** for client-side routing
- **Axios** for HTTP API communication
- **Component-based architecture** with reusable UI components

**Key Features:**
- Responsive design for desktop and mobile
- Real-time chat interface with AI assistant
- User authentication and session management
- Conversation history and memory management
- Feedback system for AI responses
- Modern UI/UX with clean design

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your backend URL

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/          # Generic components (Button, Input, etc.)
│   │   ├── chat/            # Chat-specific components
│   │   ├── auth/            # Authentication components
│   │   └── layout/          # Layout components (Header, Sidebar)
│   ├── pages/               # Page components
│   │   ├── Home.tsx         # Landing page
│   │   ├── Chat.tsx         # Main chat interface
│   │   ├── Login.tsx        # Login page
│   │   ├── Register.tsx     # Registration page
│   │   └── Profile.tsx      # User profile page
│   ├── services/            # API services
│   │   ├── api.ts           # Axios configuration
│   │   ├── auth.ts          # Authentication API
│   │   ├── chat.ts          # Chat API
│   │   └── memory.ts        # Memory API
│   ├── types/               # TypeScript type definitions
│   │   ├── auth.ts          # Authentication types
│   │   ├── chat.ts          # Chat types
│   │   └── api.ts           # API response types
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts       # Authentication hook
│   │   ├── useChat.ts       # Chat functionality hook
│   │   └── useLocalStorage.ts # Local storage hook
│   ├── utils/               # Utility functions
│   │   ├── constants.ts     # Application constants
│   │   ├── helpers.ts       # Helper functions
│   │   └── validation.ts    # Form validation
│   ├── styles/              # CSS and styling
│   │   ├── globals.css      # Global styles
│   │   └── components/      # Component-specific styles
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── vite-env.d.ts        # Vite type definitions
├── public/                  # Static assets
├── dist/                    # Production build output
├── package.json             # Node.js dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
└── .env.example             # Environment template
```

## 🔧 Development

### Code Style
- **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** for code formatting
- **Consistent naming conventions**

```bash
# Format code
npm run format

# Check types
npm run type-check

# Run all quality checks
npm run lint && npm run type-check
```

### Component Development

**Functional Components with TypeScript:**
```typescript
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

**Custom Hooks:**
```typescript
import { useState, useEffect } from 'react';
import { authService } from '../services/auth';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  return { user, loading };
};
```

### API Integration

**Service Layer:**
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// Request interceptor for auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Environment Configuration

Create `.env` file with:

```env
# Backend API
VITE_API_BASE_URL=http://localhost:8000

# Application
VITE_APP_NAME=NeoNova AI Assistant
VITE_APP_VERSION=0.1.0

# Features
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

## 🎨 Styling & UI

### CSS Architecture
- **CSS Modules** for component-scoped styles
- **CSS Variables** for theming
- **Responsive design** with mobile-first approach
- **Consistent spacing** and typography

```css
/* globals.css */
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  
  --font-family: 'Inter', sans-serif;
  --font-size-base: 16px;
  --line-height-base: 1.5;
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 3rem;
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .container {
    padding: var(--spacing-sm);
  }
}
```

### Component Styling
```typescript
// Button.module.css
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: 4px;
  font-family: var(--font-family);
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary {
  background-color: var(--primary-color);
  color: white;
}

.primary:hover {
  background-color: var(--primary-color-dark);
}
```

## 🧪 Testing Strategy

### Unit Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  test('renders button with text', () => {
    render(<Button onClick={() => {}}>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  test('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Integration Testing
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ChatPage } from './ChatPage';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('ChatPage Integration', () => {
  test('loads and displays chat interface', async () => {
    renderWithRouter(<ChatPage />);
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    });
  });
});
```

## 🚀 Build & Deployment

### Development Build
```bash
# Start development server with HMR
npm run dev

# Development server with specific port
npm run dev -- --port 3000

# Development server with host binding
npm run dev -- --host 0.0.0.0
```

### Production Build
```bash
# Build for production
npm run build

# Preview production build locally
npm run preview

# Analyze bundle size
npm run build -- --analyze
```

### Deployment Options

**Static Hosting (Netlify, Vercel):**
```bash
# Build and deploy
npm run build
# Upload dist/ folder to hosting service
```

**Docker Deployment:**
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Handle client-side routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional)
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔍 Performance Optimization

### Code Splitting
```typescript
import { lazy, Suspense } from 'react';

const ChatPage = lazy(() => import('./pages/ChatPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </Suspense>
  );
}
```

### Bundle Optimization
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          utils: ['axios', 'date-fns']
        }
      }
    }
  }
});
```

## 🛠️ Troubleshooting

### Common Issues

**Build Errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+

# Clear Vite cache
rm -rf node_modules/.vite
```

**TypeScript Errors:**
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Update type definitions
npm update @types/react @types/react-dom
```

**Development Server Issues:**
```bash
# Check port availability
lsof -i :5173

# Start with different port
npm run dev -- --port 3000

# Clear browser cache and restart
```

**API Connection Issues:**
```bash
# Check environment variables
echo $VITE_API_BASE_URL

# Test API endpoint
curl http://localhost:8000/health

# Check network tab in browser dev tools
```

### Performance Issues

**Slow Development Server:**
- Exclude unnecessary files from Vite watching
- Use `--host 0.0.0.0` only when needed
- Check for large files in src/ directory

**Large Bundle Size:**
- Analyze bundle with `npm run build -- --analyze`
- Implement code splitting for large components
- Remove unused dependencies

**Memory Issues:**
- Increase Node.js memory limit: `NODE_OPTIONS="--max-old-space-size=4096"`
- Check for memory leaks in components
- Use React DevTools Profiler