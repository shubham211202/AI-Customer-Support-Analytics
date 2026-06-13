import React, { useState } from 'react';
import { api } from '../api';

interface ModelControlProps {
  onShowToast: (message: string) => void;
}

export const ModelControl: React.FC<ModelControlProps> = ({ onShowToast }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeModelVersion, setActiveModelVersion] = useState<string | null>(null);

  const handleReloadModel = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.reloadModels();
      setActiveModelVersion(result.model_version);
      onShowToast(`Successfully reloaded MLflow model version ${result.model_version || 'latest'}`);
    } catch (err: any) {
      setError(err.message || 'Failed to sync with MLflow registry.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="model-control-layout">
      {/* Sync Card */}
      <div className="card" style={{ borderLeft: '4px solid hsl(var(--accent))' }}>
        <h3 className="breakdown-title" style={{ color: 'hsl(var(--accent))', borderColor: 'hsl(var(--card-border))' }}>
          MLflow Model Hot-Sync
        </h3>
        
        <p style={{ fontSize: '0.9rem', lineHeight: '1.6', color: 'hsl(var(--text-muted))', marginBottom: '1.5rem' }}>
          Trigger a reload on the FastAPI backend to fetch and cache the latest registered models 
          (priority, category, sentiment classifier) from the local MLflow Model Registry. 
          New support tickets will instantly use the synchronized model.
        </p>

        {error && (
          <div className="card btn-danger" style={{ padding: '0.75rem', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            <strong>Sync Failure:</strong> {error}
          </div>
        )}

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))', display: 'block' }}>
              Active Model Version:
            </span>
            <span style={{ fontSize: '1.1rem', fontWeight: 700, color: 'hsl(var(--text-main))' }}>
              {activeModelVersion ? `Version ${activeModelVersion}` : 'Default (Pre-loaded / Cache)'}
            </span>
          </div>

          <button
            className="btn btn-primary"
            style={{ 
              background: 'linear-gradient(135deg, hsl(var(--accent)), hsl(190 80% 40%))',
              boxShadow: '0 4px 15px -4px hsl(var(--accent) / 0.4)'
            }}
            disabled={isLoading}
            onClick={handleReloadModel}
          >
            {isLoading ? 'Syncing with MLflow...' : '⚡ Reload Latest Model'}
          </button>
        </div>
      </div>

      {/* Architecture Visual Aid Card */}
      <div className="card">
        <h3 className="breakdown-title">Data Pipeline Flow</h3>
        
        <p style={{ fontSize: '0.85rem', color: 'hsl(var(--text-muted))', marginBottom: '1.5rem' }}>
          Our AI analytics engine orchestrates data, training, registry, and service delivery across four layers:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Step 1 */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
            <div style={{ 
              background: 'hsl(var(--primary-glow))', 
              color: 'hsl(var(--primary-light))', 
              borderRadius: '50%', 
              width: '24px', 
              height: '24px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '0.8rem',
              flexShrink: 0
            }}>
              1
            </div>
            <div>
              <h5 style={{ fontWeight: 700, fontSize: '0.9rem', marginBottom: '0.2rem' }}>Apache Airflow (Scheduler)</h5>
              <p style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
                Runs ETL pipelines to ingest customer support data, validate features, retrain the models, and publish updates.
              </p>
            </div>
          </div>

          {/* Step 2 */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
            <div style={{ 
              background: 'hsl(var(--primary-glow))', 
              color: 'hsl(var(--primary-light))', 
              borderRadius: '50%', 
              width: '24px', 
              height: '24px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '0.8rem',
              flexShrink: 0
            }}>
              2
            </div>
            <div>
              <h5 style={{ fontWeight: 700, fontSize: '0.9rem', marginBottom: '0.2rem' }}>MLflow Registry (Repository)</h5>
              <p style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
                Tracks parameters, validation metrics, model artifacts, and manages stage promotions (Staging/Production).
              </p>
            </div>
          </div>

          {/* Step 3 */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
            <div style={{ 
              background: 'hsl(var(--primary-glow))', 
              color: 'hsl(var(--primary-light))', 
              borderRadius: '50%', 
              width: '24px', 
              height: '24px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '0.8rem',
              flexShrink: 0
            }}>
              3
            </div>
            <div>
              <h5 style={{ fontWeight: 700, fontSize: '0.9rem', marginBottom: '0.2rem' }}>FastAPI Backend (Serving)</h5>
              <p style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
                Serves endpoints, interacts with PostgreSQL, and hot-swaps active ML pipelines on-demand.
              </p>
            </div>
          </div>

          {/* Step 4 */}
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
            <div style={{ 
              background: 'hsl(var(--primary-glow))', 
              color: 'hsl(var(--primary-light))', 
              borderRadius: '50%', 
              width: '24px', 
              height: '24px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '0.8rem',
              flexShrink: 0
            }}>
              4
            </div>
            <div>
              <h5 style={{ fontWeight: 700, fontSize: '0.9rem', marginBottom: '0.2rem' }}>React Dashboard (Analytics Interface)</h5>
              <p style={{ fontSize: '0.8rem', color: 'hsl(var(--text-dim))' }}>
                Queries FastAPI, renders prediction outcomes, triggers re-evaluation, and controls system-wide models.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
