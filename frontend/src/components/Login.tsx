import React, { useState } from 'react';
import { api } from '../api';

interface LoginProps {
  onLoginSuccess: () => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('agent');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      if (isRegistering) {
        await api.register(username, password, role);
        setSuccessMsg('Registration successful! Please login.');
        setIsRegistering(false);
        setPassword('');
      } else {
        const response = await api.login(username, password);
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('username', response.username);
        localStorage.setItem('role', response.role);
        onLoginSuccess();
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card glass-panel">
        <div className="login-header">
          <div className="app-logo-circle">
            <span className="logo-spark">✦</span>
          </div>
          <h2>{isRegistering ? 'Create Account' : 'Support Console'}</h2>
          <p className="subtitle">
            {isRegistering 
              ? 'Register a new agent or administrator profile' 
              : 'Enter credentials to access the analytics workspace'}
          </p>
        </div>

        {error && (
          <div className="auth-alert alert-error">
            <span className="alert-icon">⚠</span>
            <p>{error}</p>
          </div>
        )}

        {successMsg && (
          <div className="auth-alert alert-success">
            <span className="alert-icon">✓</span>
            <p>{successMsg}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. agent_smith"
              required
              disabled={loading}
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
              autoComplete={isRegistering ? 'new-password' : 'current-password'}
            />
          </div>

          {isRegistering && (
            <div className="form-group">
              <label htmlFor="role">Assign Role</label>
              <select
                id="role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                disabled={loading}
              >
                <option value="agent">Support Agent</option>
                <option value="admin">System Administrator</option>
              </select>
            </div>
          )}

          <button type="submit" className="btn-primary auth-submit-btn" disabled={loading}>
            {loading 
              ? (isRegistering ? 'Creating...' : 'Authenticating...') 
              : (isRegistering ? 'Sign Up' : 'Log In')}
          </button>
        </form>

        <div className="login-footer">
          <button 
            type="button" 
            className="toggle-auth-mode-btn"
            onClick={() => {
              setIsRegistering(!isRegistering);
              setError(null);
              setSuccessMsg(null);
              setUsername('');
              setPassword('');
            }}
            disabled={loading}
          >
            {isRegistering 
              ? 'Already have an account? Sign In' 
              : "Don't have an account? Sign Up"}
          </button>
        </div>
      </div>
    </div>
  );
};
