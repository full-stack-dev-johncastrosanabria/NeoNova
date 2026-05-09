import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { apiClient } from './api/client';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';

// Restore token from localStorage on app load
const storedToken = localStorage.getItem('token');
if (storedToken) {
  apiClient.setToken(storedToken);
}

/** Guard that redirects to /login when no token is present */
const ProtectedRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
};

const App: React.FC = () => {
  const token = localStorage.getItem('token');

  return (
    <BrowserRouter>
      <Routes>
        {/* Root: redirect based on auth state */}
        <Route
          path="/"
          element={<Navigate to={token ? '/chat' : '/login'} replace />}
        />

        {/* Login / Register page */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected chat page */}
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <ChatPage />
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
