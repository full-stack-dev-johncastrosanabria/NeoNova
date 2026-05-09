import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';

type Mode = 'login' | 'register';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'register') {
        await apiClient.register(email, password, displayName);
        // After registration, log in automatically
        const response = await apiClient.login(email, password);
        localStorage.setItem('token', response.token);
      } else {
        const response = await apiClient.login(email, password);
        localStorage.setItem('token', response.token);
      }
      navigate('/chat');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode((prev) => (prev === 'login' ? 'register' : 'login'));
    setError('');
  };

  const submitLabel = mode === 'login' ? 'Sign In' : 'Create Account';

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
      }}
    >
      <div
        style={{
          backgroundColor: '#fff',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          width: '100%',
          maxWidth: '400px',
        }}
      >
        <h1 style={{ marginBottom: '1.5rem', textAlign: 'center', fontSize: '1.5rem' }}>
          {mode === 'login' ? 'Sign In to NeoNova' : 'Create an Account'}
        </h1>

        <form onSubmit={handleSubmit} noValidate>
          {mode === 'register' && (
            <div style={{ marginBottom: '1rem' }}>
              <label htmlFor="displayName" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
                Display Name
              </label>
              <input
                id="displayName"
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                required
                aria-label="Display name"
                placeholder="Your name"
                style={{
                  width: '100%',
                  padding: '0.5rem 0.75rem',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  fontSize: '1rem',
                  boxSizing: 'border-box',
                }}
              />
            </div>
          )}

          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="email" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              aria-label="Email address"
              placeholder="you@example.com"
              autoComplete="email"
              style={{
                width: '100%',
                padding: '0.5rem 0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
                boxSizing: 'border-box',
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="password" style={{ display: 'block', marginBottom: '0.25rem', fontWeight: 500 }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              aria-label="Password"
              placeholder="••••••••"
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              style={{
                width: '100%',
                padding: '0.5rem 0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
                boxSizing: 'border-box',
              }}
            />
          </div>

          {error && (
            <p
              role="alert"
              style={{
                color: '#c0392b',
                marginBottom: '1rem',
                fontSize: '0.875rem',
                backgroundColor: '#fdecea',
                padding: '0.5rem 0.75rem',
                borderRadius: '4px',
              }}
            >
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            aria-label={mode === 'login' ? 'Sign in' : 'Create account'}
            style={{
              width: '100%',
              padding: '0.625rem',
              backgroundColor: loading ? '#95a5a6' : '#2c3e50',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              fontSize: '1rem',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 600,
            }}
          >
            {loading ? 'Please wait…' : submitLabel}
          </button>
        </form>

        <div style={{ marginTop: '1.25rem', textAlign: 'center' }}>
          <button
            type="button"
            onClick={toggleMode}
            aria-label={mode === 'login' ? 'Switch to register mode' : 'Switch to login mode'}
            style={{
              background: 'none',
              border: 'none',
              color: '#2980b9',
              cursor: 'pointer',
              fontSize: '0.875rem',
              textDecoration: 'underline',
            }}
          >
            {mode === 'login'
              ? "Don't have an account? Register"
              : 'Already have an account? Sign In'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
