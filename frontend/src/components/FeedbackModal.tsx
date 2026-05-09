import React, { useState, useEffect, useRef } from 'react';
import { apiClient } from '../api/client';

interface FeedbackModalProps {
  messageId: string;
  onClose: () => void;
}

const FeedbackModal: React.FC<FeedbackModalProps> = ({ messageId, onClose }) => {
  const [rating, setRating] = useState<number>(0);
  const [comment, setComment] = useState('');
  const [correction, setCorrection] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const dialogRef = useRef<HTMLDialogElement>(null);

  // Open the native dialog and focus it
  useEffect(() => {
    const dialog = dialogRef.current;
    if (dialog && !dialog.open) {
      dialog.showModal();
    }
  }, []);

  // Close on Escape key (native dialog handles this, but we sync state)
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    const handleCancel = (e: Event) => {
      e.preventDefault();
      onClose();
    };

    dialog.addEventListener('cancel', handleCancel);
    return () => dialog.removeEventListener('cancel', handleCancel);
  }, [onClose]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await apiClient.createFeedback(
        messageId,
        rating > 0 ? rating : undefined,
        comment.trim() || undefined,
        correction.trim() || undefined
      );
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby="feedback-modal-title"
      style={{
        border: 'none',
        borderRadius: '8px',
        padding: '1.5rem',
        width: '100%',
        maxWidth: '480px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.2)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 id="feedback-modal-title" style={{ margin: 0, fontSize: '1.125rem' }}>
          Submit Feedback
        </h2>
        <button
          type="button"
          onClick={onClose}
          aria-label="Close feedback modal"
          style={{
            background: 'none',
            border: 'none',
            fontSize: '1.25rem',
            cursor: 'pointer',
            color: '#7f8c8d',
            lineHeight: 1,
          }}
        >
          ✕
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Rating */}
        <fieldset style={{ border: 'none', padding: 0, marginBottom: '1rem' }}>
          <legend style={{ fontWeight: 500, marginBottom: '0.5rem', fontSize: '0.875rem' }}>
            Rating (optional)
          </legend>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star === rating ? 0 : star)}
                aria-label={`Rate ${star} out of 5`}
                aria-pressed={rating >= star}
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '1.5rem',
                  cursor: 'pointer',
                  color: rating >= star ? '#f39c12' : '#bdc3c7',
                  padding: '0.125rem',
                }}
              >
                ★
              </button>
            ))}
          </div>
        </fieldset>

        {/* Comment */}
        <div style={{ marginBottom: '1rem' }}>
          <label
            htmlFor="feedback-comment"
            style={{ display: 'block', fontWeight: 500, marginBottom: '0.25rem', fontSize: '0.875rem' }}
          >
            Comment (optional)
          </label>
          <textarea
            id="feedback-comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={3}
            placeholder="What did you think of this response?"
            aria-label="Feedback comment"
            style={{
              width: '100%',
              padding: '0.5rem 0.75rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '0.875rem',
              resize: 'vertical',
              boxSizing: 'border-box',
            }}
          />
        </div>

        {/* Correction */}
        <div style={{ marginBottom: '1.25rem' }}>
          <label
            htmlFor="feedback-correction"
            style={{ display: 'block', fontWeight: 500, marginBottom: '0.25rem', fontSize: '0.875rem' }}
          >
            Correction (optional)
          </label>
          <textarea
            id="feedback-correction"
            value={correction}
            onChange={(e) => setCorrection(e.target.value)}
            rows={3}
            placeholder="Provide a corrected version of the response…"
            aria-label="Feedback correction"
            style={{
              width: '100%',
              padding: '0.5rem 0.75rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '0.875rem',
              resize: 'vertical',
              boxSizing: 'border-box',
            }}
          />
        </div>

        {error && (
          <p role="alert" style={{ color: '#c0392b', fontSize: '0.8rem', marginBottom: '0.75rem' }}>
            {error}
          </p>
        )}

        <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            style={{
              padding: '0.5rem 1rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
              background: '#fff',
              cursor: 'pointer',
              fontSize: '0.875rem',
            }}
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            aria-label="Submit feedback"
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: loading ? '#95a5a6' : '#2c3e50',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 600,
              fontSize: '0.875rem',
            }}
          >
            {loading ? 'Submitting…' : 'Submit'}
          </button>
        </div>
      </form>
    </dialog>
  );
};

export default FeedbackModal;
