import React, { useState } from 'react';
import { api } from '../api';
import type { TicketCreate, TicketSource, TicketRead } from '../api';

interface CreateTicketModalProps {
  onClose: () => void;
  onTicketCreated: (newTicket: TicketRead) => void;
}

export const CreateTicketModal: React.FC<CreateTicketModalProps> = ({
  onClose,
  onTicketCreated,
}) => {
  const [subject, setSubject] = useState('');
  const [description, setDescription] = useState('');
  const [customerId, setCustomerId] = useState('');
  const [source, setSource] = useState<TicketSource>('web');
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Quick validation
    if (subject.trim().length < 3) {
      setError('Subject must be at least 3 characters long.');
      return;
    }
    if (description.trim().length < 10) {
      setError('Description must be at least 10 characters long.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const payload: TicketCreate = {
        subject: subject.trim(),
        description: description.trim(),
        source,
      };

      if (customerId.trim()) {
        payload.customer_id = customerId.trim();
      }

      const newTicket = await api.createTicket(payload);
      onTicketCreated(newTicket);
      onClose();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit ticket.';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal-content" style={{ maxWidth: '550px' }}>
        <div className="modal-header">
          <h3 className="modal-title">New Support Ticket</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        {error && (
          <div className="card btn-danger" style={{ padding: '0.75rem', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Subject */}
          <div className="form-group">
            <label className="form-label" htmlFor="subject">Subject *</label>
            <input
              id="subject"
              type="text"
              className="form-control"
              placeholder="e.g. Trouble accessing billing invoice"
              value={subject}
              required
              min={3}
              max={255}
              disabled={isSubmitting}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>

          {/* Customer ID & Source Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="customerId">Customer ID</label>
              <input
                id="customerId"
                type="text"
                className="form-control"
                placeholder="e.g. CUST-9876"
                value={customerId}
                disabled={isSubmitting}
                onChange={(e) => setCustomerId(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="source">SourceChannel *</label>
              <select
                id="source"
                className="form-control"
                value={source}
                required
                disabled={isSubmitting}
                onChange={(e) => setSource(e.target.value as TicketSource)}
              >
                <option value="web">Web Portal</option>
                <option value="email">Email</option>
                <option value="chat">Live Chat</option>
                <option value="phone">Phone Support</option>
              </select>
            </div>
          </div>

          {/* Description */}
          <div className="form-group">
            <label className="form-label" htmlFor="description">Detailed Description *</label>
            <textarea
              id="description"
              className="form-control"
              style={{ minHeight: '120px', resize: 'vertical' }}
              placeholder="Please provide full details of your inquiry. AI will automatically prioritize and categorize your text."
              value={description}
              required
              minLength={10}
              disabled={isSubmitting}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '0.5rem', borderTop: '1px solid hsl(var(--card-border))', paddingTop: '1.25rem' }}>
            <button
              type="button"
              className="btn btn-secondary"
              disabled={isSubmitting}
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Submitting & Predicting...' : 'Submit Ticket'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
