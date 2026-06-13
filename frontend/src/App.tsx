import { useState, useEffect, useCallback } from 'react';
import { api } from './api';
import type { TicketRead } from './api';
import { Dashboard } from './components/Dashboard';
import { TicketQueue } from './components/TicketQueue';
import { TicketDetailModal } from './components/TicketDetailModal';
import { CreateTicketModal } from './components/CreateTicketModal';
import { ModelControl } from './components/ModelControl';

type Tab = 'dashboard' | 'queue' | 'model';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('dashboard');
  const [tickets, setTickets] = useState<TicketRead[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<TicketRead | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Toast notifications
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = useCallback((msg: string) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage(null);
    }, 4000);
  }, []);

  // Fetch all tickets on mount
  const fetchTickets = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.getTickets({ limit: 100 });
      setTickets(response.items);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to retrieve tickets from server.';
      setError(errorMessage);
      showToast('Error fetching tickets.');
    } finally {
      setIsLoading(false);
    }
  }, [showToast]);

  useEffect(() => {
    /* eslint-disable-next-line react-hooks/set-state-in-effect */
    fetchTickets();
  }, [fetchTickets]);

  // Event Handlers for child components
  const handleTicketCreated = (newTicket: TicketRead) => {
    setTickets((prev) => [newTicket, ...prev]);
    showToast('New ticket created successfully with AI predictions!');
  };

  const handleTicketUpdated = (updatedTicket: TicketRead) => {
    setTickets((prev) =>
      prev.map((t) => (t.id === updatedTicket.id ? updatedTicket : t))
    );
    if (selectedTicket && selectedTicket.id === updatedTicket.id) {
      setSelectedTicket(updatedTicket);
    }
    showToast('Ticket updated successfully.');
  };

  const handleTicketDeleted = (id: string) => {
    setTickets((prev) => prev.filter((t) => t.id !== id));
    showToast('Ticket deleted successfully.');
  };

  return (
    <div className="app-container">
      {/* Toast Alert */}
      {toastMessage && <div className="toast">{toastMessage}</div>}

      {/* App Header */}
      <header className="header">
        <div className="header-title-container">
          <h1>Customer Support Analytics</h1>
          <p className="header-subtitle">
            AI-Driven Auto-Prioritization & Classification Dashboard
          </p>
        </div>

        {/* Tab Navigation */}
        <nav className="nav-tabs">
          <button
            className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Analytics
          </button>
          <button
            className={`tab-btn ${activeTab === 'queue' ? 'active' : ''}`}
            onClick={() => setActiveTab('queue')}
          >
            📋 Ticket Queue
          </button>
          <button
            className={`tab-btn ${activeTab === 'model' ? 'active' : ''}`}
            onClick={() => setActiveTab('model')}
          >
            ⚙️ MLflow Sync
          </button>
        </nav>
      </header>

      {/* Main Content Area */}
      <main>
        {isLoading && tickets.length === 0 ? (
          <div className="card empty-state">
            <div style={{ display: 'inline-block', width: '30px', height: '30px', border: '3px solid hsl(var(--primary-light))', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            <p style={{ marginTop: '1rem' }}>Loading ticket metrics and classification data...</p>
          </div>
        ) : error && tickets.length === 0 ? (
          <div className="card empty-state" style={{ borderColor: 'hsl(var(--sentiment-negative) / 0.3)' }}>
            <p style={{ color: 'hsl(var(--sentiment-negative))', fontWeight: 600 }}>Connection Error</p>
            <p style={{ fontSize: '0.85rem', color: 'hsl(var(--text-muted))', marginTop: '0.5rem' }}>{error}</p>
            <button className="btn btn-secondary" style={{ marginTop: '1.25rem' }} onClick={fetchTickets}>
              🔄 Try Reconnecting
            </button>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && <Dashboard tickets={tickets} />}
            {activeTab === 'queue' && (
              <TicketQueue
                tickets={tickets}
                onSelectTicket={setSelectedTicket}
                onCreateTicketClick={() => setIsCreateModalOpen(true)}
              />
            )}
            {activeTab === 'model' && <ModelControl onShowToast={showToast} />}
          </>
        )}
      </main>

      {/* Modals */}
      {selectedTicket && (
        <TicketDetailModal
          ticket={selectedTicket}
          onClose={() => setSelectedTicket(null)}
          onTicketUpdated={handleTicketUpdated}
          onTicketDeleted={handleTicketDeleted}
        />
      )}

      {isCreateModalOpen && (
        <CreateTicketModal
          onClose={() => setIsCreateModalOpen(false)}
          onTicketCreated={handleTicketCreated}
        />
      )}

      {/* Footer Info */}
      <footer style={{ marginTop: '4rem', borderTop: '1px solid hsl(var(--card-border))', paddingTop: '1.5rem', textAlign: 'center', fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
        AI Support Analytics Portal &bull; MLflow Registry Integration &bull; FastAPI + React TS
      </footer>
    </div>
  );
}

export default App;
