import React from 'react';
import type { TicketRead } from '../api';

interface DashboardProps {
  tickets: TicketRead[];
}

export const Dashboard: React.FC<DashboardProps> = ({ tickets }) => {
  const total = tickets.length;
  
  // Status breakdown
  const statusCounts = tickets.reduce((acc, t) => {
    acc[t.status] = (acc[t.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Priority breakdown
  const priorityCounts = tickets.reduce((acc, t) => {
    if (t.prediction?.priority) {
      acc[t.prediction.priority] = (acc[t.prediction.priority] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Sentiment breakdown
  const sentimentCounts = tickets.reduce((acc, t) => {
    if (t.prediction?.sentiment) {
      acc[t.prediction.sentiment] = (acc[t.prediction.sentiment] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Category breakdown
  const categoryCounts = tickets.reduce((acc, t) => {
    if (t.prediction?.category) {
      acc[t.prediction.category] = (acc[t.prediction.category] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Calculate percentage helper
  const getPercent = (count: number) => {
    if (total === 0) return 0;
    return Math.round((count / total) * 100);
  };

  // Status values
  const openCount = statusCounts['open'] || 0;
  const inProgressCount = statusCounts['in_progress'] || 0;
  const resolvedCount = statusCounts['resolved'] || 0;
  const closedCount = statusCounts['closed'] || 0;

  // Sentiment averages / confidence metrics
  const avgConfidence = total > 0
    ? tickets.reduce((acc, t) => {
        if (t.prediction) {
          const sumConf = (t.prediction.category_confidence + t.prediction.sentiment_confidence + t.prediction.priority_confidence) / 3;
          return acc + sumConf;
        }
        return acc;
      }, 0) / tickets.filter(t => t.prediction).length
    : 0;

  return (
    <div className="dashboard-content">
      {/* Stat Cards Grid */}
      <div className="dashboard-grid">
        <div className="card stat-card" style={{ borderLeft: '4px solid hsl(var(--primary))' }}>
          <div className="stat-header">
            <span className="stat-label">Total Tickets</span>
          </div>
          <span className="stat-value">{total}</span>
          <div className="stat-trend neutral">All time registered tickets</div>
        </div>

        <div className="card stat-card" style={{ borderLeft: '4px solid hsl(var(--status-open))' }}>
          <div className="stat-header">
            <span className="stat-label">Open</span>
            <span className="badge badge-status-open">{openCount}</span>
          </div>
          <span className="stat-value">{openCount}</span>
          <div className="stat-trend positive">Requires developer triage</div>
        </div>

        <div className="card stat-card" style={{ borderLeft: '4px solid hsl(var(--status-in_progress))' }}>
          <div className="stat-header">
            <span className="stat-label">In Progress</span>
            <span className="badge badge-status-in_progress">{inProgressCounts()}</span>
          </div>
          <span className="stat-value">{inProgressCount}</span>
          <div className="stat-trend neutral">Currently being handled</div>
        </div>

        <div className="card stat-card" style={{ borderLeft: '4px solid hsl(var(--status-resolved))' }}>
          <div className="stat-header">
            <span className="stat-label">Resolved / Closed</span>
            <span className="badge badge-status-resolved">{resolvedCount + closedCount}</span>
          </div>
          <span className="stat-value">{resolvedCount + closedCount}</span>
          <div className="stat-trend positive">Success resolution rate: {getPercent(resolvedCount + closedCount)}%</div>
        </div>
      </div>

      {/* Breakdowns Grid */}
      <div className="breakdown-grid">
        {/* Category Breakdown */}
        <div className="card">
          <h3 className="breakdown-title">Predicted Categories</h3>
          {total === 0 ? (
            <div className="empty-state">No predictions available yet.</div>
          ) : (
            Object.entries(categoryCounts).map(([cat, count]) => (
              <div className="breakdown-row" key={cat}>
                <div className="breakdown-info">
                  <span className="breakdown-label" style={{ textTransform: 'capitalize' }}>
                    {cat.replace('_', ' ')}
                  </span>
                  <span className="breakdown-count">
                    {count} tickets ({getPercent(count)}%)
                  </span>
                </div>
                <div className="progress-container">
                  <div 
                    className="progress-bar" 
                    style={{ 
                      width: `${getPercent(count)}%`,
                      background: 'linear-gradient(90deg, hsl(var(--primary)), hsl(var(--accent)))'
                    }}
                  />
                </div>
              </div>
            ))
          )}
        </div>

        {/* Priority & Sentiment Column */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {/* Priority Breakdown */}
          <div>
            <h3 className="breakdown-title" style={{ marginBottom: '1rem' }}>AI Prioritization Ratios</h3>
            {total === 0 ? (
              <div className="empty-state">No prioritization stats.</div>
            ) : (
              ['low', 'medium', 'high', 'urgent'].map((prio) => {
                const count = priorityCounts[prio] || 0;
                return (
                  <div className="breakdown-row" key={prio}>
                    <div className="breakdown-info">
                      <span className="breakdown-label" style={{ textTransform: 'capitalize' }}>
                        {prio}
                      </span>
                      <span className="breakdown-count">
                        {count} ({getPercent(count)}%)
                      </span>
                    </div>
                    <div className="progress-container">
                      <div 
                        className="progress-bar" 
                        style={{ 
                          width: `${getPercent(count)}%`,
                          backgroundColor: `hsl(var(--priority-${prio}))`
                        }}
                      />
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Sentiment Breakdown */}
          <div>
            <h3 className="breakdown-title" style={{ marginBottom: '1rem' }}>Customer Sentiment</h3>
            {total === 0 ? (
              <div className="empty-state">No sentiment data.</div>
            ) : (
              ['positive', 'neutral', 'negative'].map((sent) => {
                const count = sentimentCounts[sent] || 0;
                return (
                  <div className="breakdown-row" key={sent}>
                    <div className="breakdown-info">
                      <span className="breakdown-label" style={{ textTransform: 'capitalize' }}>
                        {sent}
                      </span>
                      <span className="breakdown-count">
                        {count} ({getPercent(count)}%)
                      </span>
                    </div>
                    <div className="progress-container">
                      <div 
                        className="progress-bar" 
                        style={{ 
                          width: `${getPercent(count)}%`,
                          backgroundColor: `hsl(var(--sentiment-${sent}))`
                        }}
                      />
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* AI Confidence summary */}
      {total > 0 && !isNaN(avgConfidence) && (
        <div className="card text-center" style={{ padding: '1.25rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h4 style={{ fontFamily: 'var(--font-title)', fontWeight: 700, color: 'hsl(var(--text-main))' }}>
              Average Model Prediction Confidence
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'hsl(var(--text-muted))', marginTop: '0.25rem' }}>
              Mean probability score across category, priority, and sentiment classifications
            </p>
          </div>
          <div>
            <span style={{ 
              fontSize: '2.5rem', 
              fontFamily: 'var(--font-title)', 
              fontWeight: 800, 
              color: 'hsl(var(--accent))',
              textShadow: '0 0 15px hsl(var(--accent) / 0.3)'
            }}>
              {(avgConfidence * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      )}
    </div>
  );

  // Simple helper to avoid type compilation issues with return value inside JSX expression
  function inProgressCounts() {
    return inProgressCount;
  }
};
