import React, { useState, useEffect, useRef, useCallback } from 'react';
import { apiClient } from '../api/client';
import type { Message } from '../types';
import FeedbackModal from './FeedbackModal';

interface ChatProps {
  conversationId: string;
}

const Chat: React.FC<ChatProps> = ({ conversationId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [feedbackMessageId, setFeedbackMessageId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = useCallback(async () => {
    setError('');
    try {
      const data = await apiClient.listMessages(conversationId);
      setMessages(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load messages');
    }
  }, [conversationId]);

  useEffect(() => {
    setMessages([]);
    void fetchMessages();
  }, [fetchMessages]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    setInput('');
    setLoading(true);
    setError('');

    try {
      const newMessages = await apiClient.sendMessage(conversationId, trimmed);
      setMessages((prev) => [...prev, ...newMessages]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void handleSend();
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        boxSizing: 'border-box',
      }}
    >
      {/* Messages area */}
      <div
        aria-live="polite"
        aria-label="Conversation messages"
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '1rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem',
        }}
      >
        {messages.map((msg) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={msg.id}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: isUser ? 'flex-end' : 'flex-start',
              }}
            >
              <div
                style={{
                  maxWidth: '70%',
                  padding: '0.625rem 0.875rem',
                  borderRadius: isUser ? '12px 12px 2px 12px' : '12px 12px 12px 2px',
                  backgroundColor: isUser ? '#2c3e50' : '#ecf0f1',
                  color: isUser ? '#fff' : '#2c3e50',
                  fontSize: '0.9rem',
                  lineHeight: 1.5,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                }}
              >
                {msg.content}
              </div>

              {msg.role === 'assistant' && (
                <button
                  type="button"
                  onClick={() => setFeedbackMessageId(msg.id)}
                  aria-label="Submit feedback for this message"
                  style={{
                    marginTop: '0.25rem',
                    background: 'none',
                    border: 'none',
                    color: '#7f8c8d',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                    textDecoration: 'underline',
                    padding: 0,
                  }}
                >
                  Feedback
                </button>
              )}
            </div>
          );
        })}

        {loading && (
          <div style={{ display: 'flex', alignItems: 'flex-start' }}>
            <div
              aria-label="Waiting for response"
              style={{
                padding: '0.625rem 0.875rem',
                borderRadius: '12px 12px 12px 2px',
                backgroundColor: '#ecf0f1',
                color: '#7f8c8d',
                fontSize: '0.9rem',
              }}
            >
              <span aria-hidden="true">●●●</span>
            </div>
          </div>
        )}

        {error && (
          <p role="alert" style={{ color: '#c0392b', fontSize: '0.8rem', textAlign: 'center' }}>
            {error}
          </p>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div
        style={{
          borderTop: '1px solid #ecf0f1',
          padding: '0.75rem 1rem',
          display: 'flex',
          gap: '0.5rem',
          alignItems: 'flex-end',
        }}
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          rows={1}
          aria-label="Message input. Press Enter to send, Shift+Enter for a new line."
          placeholder="Type a message… (Enter to send, Shift+Enter for newline)"
          style={{
            flex: 1,
            padding: '0.5rem 0.75rem',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '0.9rem',
            resize: 'none',
            lineHeight: 1.5,
            maxHeight: '120px',
            overflowY: 'auto',
            boxSizing: 'border-box',
          }}
        />
        <button
          type="button"
          onClick={() => void handleSend()}
          disabled={loading || !input.trim()}
          aria-label="Send message"
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: loading || !input.trim() ? '#95a5a6' : '#2c3e50',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
            fontWeight: 600,
            fontSize: '0.875rem',
            whiteSpace: 'nowrap',
          }}
        >
          Send
        </button>
      </div>

      {/* Feedback modal */}
      {feedbackMessageId && (
        <FeedbackModal
          messageId={feedbackMessageId}
          onClose={() => setFeedbackMessageId(null)}
        />
      )}
    </div>
  );
};

export default Chat;
