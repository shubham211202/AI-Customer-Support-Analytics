import React, { useState, useMemo } from 'react';
import type { TicketRead } from '../api';

interface TicketQueueProps {
  tickets: TicketRead[];
  onSelectTicket: (ticket: TicketRead) => void;
  onCreateTicketClick: () => void;
}

export const TicketQueue: React.FC<TicketQueueProps> = ({
  tickets,
  onSelectTicket,
  onCreateTicketClick,
}) => {
  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [sentimentFilter, setSentimentFilter] = useState<string>('all');

  // Filter logic
  const filteredTickets = useMemo(() => {
    return tickets.filter((ticket) => {
      // Search term
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch =
        ticket.subject.toLowerCase().includes(searchLower) ||
        ticket.description.toLowerCase().includes(searchLower) ||
        (ticket.customer_id && ticket.customer_id.toLowerCase().includes(searchLower));

      // Dropdown filters
      const matchesStatus = statusFilter === 'all' || ticket.status === statusFilter;
      const matchesPriority =
        priorityFilter === 'all' || ticket.prediction?.priority === priorityFilter;
      const matchesCategory =
        categoryFilter === 'all' || ticket.prediction?.category === categoryFilter;
      const matchesSentiment =
        sentimentFilter === 'all' || ticket.prediction?.sentiment === sentimentFilter;

      return matchesSearch && matchesStatus && matchesPriority && matchesCategory && matchesSentiment;
    });
  }, [tickets, searchTerm, statusFilter, priorityFilter, categoryFilter, sentimentFilter]);

  // Format date utility
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="ticket-queue-section">
      {/* Search and Filters Header Card */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1.25rem' }}>
        <div className="filters-bar">
          <div className="search-input-wrapper">
            <input
              type="text"
              className="form-control"
              placeholder="Search by subject, description, or customer..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', flex: 2, justifyContent: 'flex-end' }}>
            <select
              className="form-control"
              style={{ width: '130px' }}
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>

            <select
              className="form-control"
              style={{ width: '130px' }}
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
            >
              <option value="all">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>

            <select
              className="form-control"
              style={{ width: '140px' }}
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="all">All Categories</option>
              <option value="billing">Billing</option>
              <option value="technical_issue">Technical Issue</option>
              <option value="account_access">Account Access</option>
              <option value="refund">Refund</option>
              <option value="general_query">General Query</option>
            </select>

            <select
              className="form-control"
              style={{ width: '140px' }}
              value={sentimentFilter}
              onChange={(e) => setSentimentFilter(e.target.value)}
            >
              <option value="all">All Sentiments</option>
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
            </select>

            <button className="btn btn-primary" onClick={onCreateTicketClick}>
              + Create Ticket
            </button>
          </div>
        </div>
        
        <div style={{ fontSize: '0.8rem', color: 'hsl(var(--text-muted))', display: 'flex', justifyContent: 'space-between' }}>
          <span>Showing {filteredTickets.length} of {tickets.length} tickets</span>
          {searchTerm || statusFilter !== 'all' || priorityFilter !== 'all' || categoryFilter !== 'all' || sentimentFilter !== 'all' ? (
            <button 
              style={{ background: 'transparent', border: 'none', color: 'hsl(var(--accent))', cursor: 'pointer', fontWeight: 600 }}
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('all');
                setPriorityFilter('all');
                setCategoryFilter('all');
                setSentimentFilter('all');
              }}
            >
              Clear Filters
            </button>
          ) : null}
        </div>
      </div>

      {/* Tickets List */}
      <div className="tickets-list">
        {filteredTickets.length === 0 ? (
          <div className="card empty-state">
            <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>No tickets found matching filters</p>
            <p style={{ fontSize: '0.85rem', color: 'hsl(var(--text-dim))', marginTop: '0.5rem' }}>
              Try adjusting your filters, search term, or create a new ticket.
            </p>
          </div>
        ) : (
          filteredTickets.map((ticket) => (
            <div
              key={ticket.id}
              className="card ticket-item"
              onClick={() => onSelectTicket(ticket)}
            >
              <div className="ticket-item-main">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.35rem' }}>
                  <span className={`badge badge-status-${ticket.status}`}>
                    {ticket.status.replace('_', ' ')}
                  </span>
                  {ticket.prediction?.priority && (
                    <span className={`badge badge-priority-${ticket.prediction.priority}`}>
                      {ticket.prediction.priority}
                    </span>
                  )}
                  {ticket.prediction?.category && (
                    <span className="badge" style={{ backgroundColor: 'hsl(var(--primary-glow))', color: 'hsl(var(--primary-light))', borderColor: 'hsl(var(--primary-glow) * 2)' }}>
                      {ticket.prediction.category.replace('_', ' ')}
                    </span>
                  )}
                  {ticket.prediction?.sentiment && (
                    <span className={`badge badge-sentiment-${ticket.prediction.sentiment}`}>
                      {ticket.prediction.sentiment}
                    </span>
                  )}
                </div>
                <h4 className="ticket-subject">{ticket.subject}</h4>
                <p className="ticket-snippet">{ticket.description}</p>
              </div>

              <div className="ticket-item-meta">
                <div className="text-right">
                  <div className="ticket-date">{formatDate(ticket.created_at)}</div>
                  {ticket.customer_id && (
                    <div style={{ fontSize: '0.75rem', color: 'hsl(var(--text-dim))', marginTop: '0.25rem' }}>
                      Cust ID: {ticket.customer_id}
                    </div>
                  )}
                </div>
                <div style={{ color: 'hsl(var(--text-muted))', fontSize: '1.2rem', paddingLeft: '0.5rem' }}>
                  →
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
