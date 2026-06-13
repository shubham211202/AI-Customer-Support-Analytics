import React, { useState } from 'react';
import { api } from '../api';
import type { TicketRead, TicketStatus } from '../api';

interface TicketDetailModalProps {
  ticket: TicketRead;
  onClose: () => void;
  onTicketUpdated: (updatedTicket: TicketRead) => void;
  onTicketDeleted: (id: string) => void;
}

export const TicketDetailModal: React.FC<TicketDetailModalProps> = ({
  ticket,
  onClose,
  onTicketUpdated,
  onTicketDeleted,
}) => {
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [isRerunningPredict, setIsRerunningPredict] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Status Change Handler
  const handleStatusChange = async (newStatus: TicketStatus) => {
    setIsUpdatingStatus(true);
    setError(null);
    try {
      const updated = await api.updateTicketStatus(ticket.id, newStatus);
      onTicketUpdated(updated);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update status.';
      setError(errorMessage);
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  // Re-run prediction Handler
  const handleRerunPrediction = async () => {
    setIsRerunningPredict(true);
    setError(null);
    try {
      const updated = await api.rerunPrediction(ticket.id);
      onTicketUpdated(updated);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to re-run AI prediction.';
      setError(errorMessage);
    } finally {
      setIsRerunningPredict(false);
    }
  };

  // Delete handler
  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this ticket?')) return;
    setIsDeleting(true);
    setError(null);
    try {
      await api.deleteTicket(ticket.id);
      onTicketDeleted(ticket.id);
      onClose();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete ticket.';
      setError(errorMessage);
      setIsDeleting(false);
    }
  };

  // Format date utility
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString(undefined, {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  };

  const hasPrediction = !!ticket.prediction;

  return (
    <div className="modal-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal-content">
        <div className="modal-header">
          <h3 className="modal-title">Ticket Details</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        {error && (
          <div className="card btn-danger" style={{ padding: '0.75rem', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Main Info */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
                ID: {ticket.id}
              </span>
              <span className="ticket-date">Created: {formatDate(ticket.created_at)}</span>
            </div>
            
            <h2 style={{ fontFamily: 'var(--font-title)', fontSize: '1.4rem', fontWeight: 800, color: 'hsl(var(--text-main))', marginBottom: '1rem' }}>
              {ticket.subject}
            </h2>

            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '1.25rem' }}>
              <span className="form-label" style={{ margin: 0, paddingRight: '0.5rem' }}>Status:</span>
              <select
                className="form-control"
                style={{ width: '150px', padding: '0.4rem 2rem 0.4rem 0.65rem' }}
                value={ticket.status}
                disabled={isUpdatingStatus}
                onChange={(e) => handleStatusChange(e.target.value as TicketStatus)}
              >
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>

              <span className="form-label" style={{ margin: '0 0 0 1rem', paddingRight: '0.5rem' }}>Source:</span>
              <span className="badge" style={{ background: 'hsl(var(--text-main) / 0.05)', color: 'hsl(var(--text-main))', textTransform: 'capitalize' }}>
                {ticket.source}
              </span>

              {ticket.customer_id && (
                <>
                  <span className="form-label" style={{ margin: '0 0 0 1rem', paddingRight: '0.5rem' }}>Customer ID:</span>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{ticket.customer_id}</span>
                </>
              )}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <span className="form-label">Description</span>
              <div 
                className="card" 
                style={{ 
                  background: 'hsl(var(--bg-dark))', 
                  fontSize: '0.9rem', 
                  lineHeight: '1.5', 
                  whiteSpace: 'pre-wrap',
                  maxHeight: '200px',
                  overflowY: 'auto'
                }}
              >
                {ticket.description}
              </div>
            </div>
          </div>

          {/* AI Prediction Visualizer */}
          <div className="prediction-card">
            <div className="prediction-title">
              <span>AI Classification Insights</span>
              {hasPrediction && ticket.prediction?.model_version && (
                <span className="prediction-version">
                  MLflow Version: <strong>{ticket.prediction.model_version}</strong>
                </span>
              )}
            </div>

            {!hasPrediction ? (
              <div className="empty-state" style={{ padding: '1rem' }}>
                No prediction payload found for this ticket.
              </div>
            ) : (
              <div className="prediction-metrics">
                {/* Category */}
                <div className="metric-item">
                  <div className="metric-label">Category</div>
                  <div className="metric-val" style={{ color: 'hsl(var(--primary-light))' }}>
                    {ticket.prediction!.category.replace('_', ' ')}
                  </div>
                  <div className="confidence-bar-wrapper">
                    <div 
                      className="confidence-bar" 
                      style={{ 
                        width: `${ticket.prediction!.category_confidence * 100}%`,
                        backgroundColor: 'hsl(var(--primary-light))'
                      }}
                    />
                  </div>
                  <div style={{ fontSize: '0.75rem', marginTop: '0.35rem', color: 'hsl(var(--text-muted))' }}>
                    Confidence: {(ticket.prediction!.category_confidence * 100).toFixed(0)}%
                  </div>
                </div>

                {/* Priority */}
                <div className="metric-item">
                  <div className="metric-label">Priority</div>
                  <div className="metric-val" style={{ color: `hsl(var(--priority-${ticket.prediction!.priority}))` }}>
                    {ticket.prediction!.priority}
                  </div>
                  <div className="confidence-bar-wrapper">
                    <div 
                      className="confidence-bar" 
                      style={{ 
                        width: `${ticket.prediction!.priority_confidence * 100}%`,
                        backgroundColor: `hsl(var(--priority-${ticket.prediction!.priority}))`
                      }}
                    />
                  </div>
                  <div style={{ fontSize: '0.75rem', marginTop: '0.35rem', color: 'hsl(var(--text-muted))' }}>
                    Confidence: {(ticket.prediction!.priority_confidence * 100).toFixed(0)}%
                  </div>
                </div>

                {/* Sentiment */}
                <div className="metric-item">
                  <div className="metric-label">Sentiment</div>
                  <div className="metric-val" style={{ color: `hsl(var(--sentiment-${ticket.prediction!.sentiment}))` }}>
                    {ticket.prediction!.sentiment}
                  </div>
                  <div className="confidence-bar-wrapper">
                    <div 
                      className="confidence-bar" 
                      style={{ 
                        width: `${ticket.prediction!.sentiment_confidence * 100}%`,
                        backgroundColor: `hsl(var(--sentiment-${ticket.prediction!.sentiment}))`
                      }}
                    />
                  </div>
                  <div style={{ fontSize: '0.75rem', marginTop: '0.35rem', color: 'hsl(var(--text-muted))' }}>
                    Confidence: {(ticket.prediction!.sentiment_confidence * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            )}

            <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'flex-end' }}>
              <button
                className="btn btn-secondary"
                disabled={isRerunningPredict}
                onClick={handleRerunPrediction}
              >
                {isRerunningPredict ? 'Running ML Inference...' : '⚡ Rerun AI Analysis'}
              </button>
            </div>
          </div>

          {/* Action Row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid hsl(var(--card-border))', paddingTop: '1.25rem', marginTop: '0.5rem' }}>
            <button
              className="btn btn-danger"
              disabled={isDeleting}
              onClick={handleDelete}
            >
              {isDeleting ? 'Deleting...' : 'Delete Ticket'}
            </button>
            <button className="btn btn-secondary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
