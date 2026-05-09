import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import ConversationList from '../components/ConversationList';
import Chat from '../components/Chat';

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);

  const handleLogout = () => {
    localStorage.removeItem('token');
    apiClient.clearToken();
    navigate('/login');
  };

  return (
    <div
      style={{
        display: 'flex',
        height: '100vh',
        overflow: 'hidden',
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      {/* Sidebar */}
      <nav
        aria-label="Conversations"
        style={{
          width: '260px',
          minWidth: '260px',
          borderRight: '1px solid #ecf0f1',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: '#fafafa',
        }}
      >
        {/* Sidebar header */}
        <div
          style={{
            padding: '1rem',
            borderBottom: '1px solid #ecf0f1',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <span style={{ fontWeight: 700, fontSize: '1rem', color: '#2c3e50' }}>NeoNova</span>
          <button
            type="button"
            onClick={handleLogout}
            aria-label="Log out"
            style={{
              background: 'none',
              border: '1px solid #ccc',
              borderRadius: '4px',
              padding: '0.25rem 0.5rem',
              cursor: 'pointer',
              fontSize: '0.75rem',
              color: '#7f8c8d',
            }}
          >
            Logout
          </button>
        </div>

        {/* Conversation list */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          <ConversationList
            selectedId={selectedConversationId}
            onSelect={setSelectedConversationId}
          />
        </div>
      </nav>

      {/* Main chat area */}
      <main
        aria-label="Chat area"
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {selectedConversationId ? (
          <Chat conversationId={selectedConversationId} />
        ) : (
          <div
            style={{
              flex: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#95a5a6',
              fontSize: '1rem',
            }}
          >
            Select a conversation or create a new one to get started.
          </div>
        )}
      </main>
    </div>
  );
};

export default ChatPage;
