import React, { useEffect, useState, useCallback } from 'react';
import { apiClient } from '../api/client';
import type { Conversation } from '../types';

interface ConversationListProps {
  selectedId: string | null;
  onSelect: (id: string) => void;
}

const ConversationList: React.FC<ConversationListProps> = ({ selectedId, onSelect }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchConversations = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.listConversations();
      setConversations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversations');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchConversations();
  }, [fetchConversations]);

  const handleNewConversation = async () => {
    const title = globalThis.prompt('Enter a title for the new conversation:');
    if (!title?.trim()) return;

    try {
      await apiClient.createConversation(title.trim());
      await fetchConversations();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create conversation');
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        padding: '1rem',
        boxSizing: 'border-box',
      }}
    >
      <button
        type="button"
        onClick={handleNewConversation}
        aria-label="New conversation"
        style={{
          padding: '0.5rem 0.75rem',
          backgroundColor: '#2c3e50',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontWeight: 600,
          marginBottom: '1rem',
          fontSize: '0.875rem',
        }}
      >
        + New Conversation
      </button>

      {error && (
        <p role="alert" style={{ color: '#c0392b', fontSize: '0.8rem', marginBottom: '0.5rem' }}>
          {error}
        </p>
      )}

      {loading && (
        <p style={{ color: '#7f8c8d', fontSize: '0.875rem' }}>Loading…</p>
      )}

      <ul
        style={{
          listStyle: 'none',
          margin: 0,
          padding: 0,
          overflowY: 'auto',
          flex: 1,
        }}
      >
        {conversations.map((conv) => {
          const isSelected = conv.id === selectedId;
          return (
            <li key={conv.id}>
              <button
                type="button"
                onClick={() => onSelect(conv.id)}
                aria-current={isSelected ? 'true' : undefined}
                aria-label={`Conversation: ${conv.title}`}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '0.625rem 0.75rem',
                  marginBottom: '0.25rem',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  backgroundColor: isSelected ? '#2c3e50' : 'transparent',
                  color: isSelected ? '#fff' : '#2c3e50',
                  fontWeight: isSelected ? 600 : 400,
                  fontSize: '0.875rem',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {conv.title}
              </button>
            </li>
          );
        })}
      </ul>

      {!loading && conversations.length === 0 && (
        <p style={{ color: '#95a5a6', fontSize: '0.8rem', textAlign: 'center', marginTop: '1rem' }}>
          No conversations yet.
        </p>
      )}
    </div>
  );
};

export default ConversationList;
