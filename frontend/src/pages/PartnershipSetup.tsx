import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { createInvite, joinWithCode } from '../api/partnership';

export default function PartnershipSetup() {
  const [mode, setMode] = useState<'create' | 'join'>('create');
  const [inviteCode, setInviteCode] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const { partnership, refreshPartnership } = useAuth();
  const navigate = useNavigate();

  // If partnership is already active, redirect to dashboard
  useEffect(() => {
    if (partnership?.status === 'active') {
      navigate('/');
    }
  }, [partnership, navigate]);

  const handleCreateInvite = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await createInvite();
      setInviteCode(response.code);
      // Poll for partnership status changes
      pollPartnershipStatus();
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error al crear invitación');
    } finally {
      setLoading(false);
    }
  };

  const pollPartnershipStatus = () => {
    const interval = setInterval(async () => {
      await refreshPartnership();
      if (partnership?.status === 'active') {
        clearInterval(interval);
        navigate('/');
      }
    }, 3000);
  };

  const handleJoin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (joinCode.length !== 6) {
      setError('El código debe tener 6 caracteres');
      return;
    }

    setLoading(true);
    try {
      await joinWithCode(joinCode.toUpperCase());
      await refreshPartnership();
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Código inválido o expirado');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyCode = async () => {
    if (inviteCode) {
      await navigator.clipboard.writeText(inviteCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="setup-page">
      <div className="setup-container">
        <div className="setup-header">
          <h1 className="setup-title">Conectar con tu pareja</h1>
          <p className="setup-subtitle">Compartan finanzas en pareja</p>
        </div>

        <div className="setup-tabs">
          <button
            className={`tab ${mode === 'create' ? 'active' : ''}`}
            onClick={() => setMode('create')}
          >
            Crear invitación
          </button>
          <button
            className={`tab ${mode === 'join' ? 'active' : ''}`}
            onClick={() => setMode('join')}
          >
            Unirse con código
          </button>
        </div>

        {error && <div className="setup-error">{error}</div>}

        {mode === 'create' && (
          <div className="setup-content">
            {!inviteCode ? (
              <div className="invite-create">
                <p className="setup-description">
                  Genera un código de invitación y compártelo con tu pareja.
                </p>
                <button
                  className="btn-create"
                  onClick={handleCreateInvite}
                  disabled={loading}
                >
                  {loading ? 'Generando...' : 'Generar código'}
                </button>
              </div>
            ) : (
              <div className="invite-code-display">
                <p className="code-label">Comparte este código:</p>
                <div className="code-display">
                  <span className="code">{inviteCode}</span>
                  <button className="btn-copy" onClick={handleCopyCode}>
                    {copied ? '✓' : '📋'}
                  </button>
                </div>
                <p className="waiting-text">
                  Esperando a que tu pareja ingrese el código...
                </p>
                <div className="pulse-indicator" />
              </div>
            )}
          </div>
        )}

        {mode === 'join' && (
          <form className="setup-content" onSubmit={handleJoin}>
            <p className="setup-description">
              Ingresa el código de 6 caracteres que te compartió tu pareja.
            </p>
            <div className="form-group">
              <input
                type="text"
                value={joinCode}
                onChange={(e) => setJoinCode(e.target.value.toUpperCase().slice(0, 6))}
                placeholder="XXXXXX"
                maxLength={6}
                className="code-input"
                autoFocus
              />
            </div>
            <button
              type="submit"
              className="btn-join"
              disabled={loading || joinCode.length !== 6}
            >
              {loading ? 'Uniendo...' : 'Unirse'}
            </button>
          </form>
        )}
      </div>

      <style>{`
        .setup-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: var(--space-4);
          background: var(--bg-primary);
        }

        .setup-container {
          width: 100%;
          max-width: 400px;
        }

        .setup-header {
          text-align: center;
          margin-bottom: var(--space-6);
        }

        .setup-title {
          font-family: var(--font-heading);
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--text-primary);
        }

        .setup-subtitle {
          color: var(--text-muted);
          font-size: 0.875rem;
          margin-top: var(--space-1);
        }

        .setup-tabs {
          display: flex;
          gap: var(--space-2);
          background: var(--bg-secondary);
          padding: var(--space-1);
          border-radius: var(--radius-lg);
          margin-bottom: var(--space-4);
        }

        .tab {
          flex: 1;
          padding: 10px 16px;
          font-size: 0.875rem;
          font-weight: 500;
          color: var(--text-muted);
          background: transparent;
          border: none;
          border-radius: var(--radius-md);
          cursor: pointer;
          transition: all var(--transition-fast);
        }

        .tab.active {
          background: var(--bg-card);
          color: var(--text-primary);
          box-shadow: var(--shadow-sm);
        }

        .setup-error {
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid rgba(239, 68, 68, 0.3);
          color: #EF4444;
          padding: var(--space-3);
          border-radius: var(--radius-md);
          font-size: 0.875rem;
          text-align: center;
          margin-bottom: var(--space-4);
        }

        .setup-content {
          background: var(--bg-card);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-lg);
          padding: var(--space-6);
        }

        .setup-description {
          color: var(--text-secondary);
          font-size: 0.875rem;
          text-align: center;
          margin-bottom: var(--space-6);
        }

        .btn-create, .btn-join {
          width: 100%;
          padding: 12px 16px;
          font-size: 1rem;
          font-weight: 600;
          color: white;
          background: linear-gradient(135deg, #8B5CF6, #6366F1);
          border: none;
          border-radius: var(--radius-md);
          cursor: pointer;
          transition: opacity var(--transition-fast), transform var(--transition-fast);
        }

        .btn-create:hover:not(:disabled), .btn-join:hover:not(:disabled) {
          opacity: 0.9;
          transform: translateY(-1px);
        }

        .btn-create:disabled, .btn-join:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .invite-code-display {
          text-align: center;
        }

        .code-label {
          color: var(--text-muted);
          font-size: 0.875rem;
          margin-bottom: var(--space-3);
        }

        .code-display {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--space-3);
          margin-bottom: var(--space-4);
        }

        .code {
          font-family: var(--font-mono);
          font-size: 2rem;
          font-weight: 700;
          letter-spacing: 0.25em;
          color: var(--accent-purple);
        }

        .btn-copy {
          width: 48px;
          height: 48px;
          border-radius: var(--radius-md);
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          font-size: 1.25rem;
          cursor: pointer;
          transition: background var(--transition-fast);
        }

        .btn-copy:hover {
          background: var(--bg-tertiary);
        }

        .waiting-text {
          color: var(--text-muted);
          font-size: 0.875rem;
        }

        .pulse-indicator {
          width: 12px;
          height: 12px;
          background: var(--accent-green);
          border-radius: 50%;
          margin: var(--space-4) auto 0;
          animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 0.4; transform: scale(0.9); }
          50% { opacity: 1; transform: scale(1.1); }
        }

        .code-input {
          text-align: center;
          font-family: var(--font-mono);
          font-size: 1.5rem;
          font-weight: 600;
          letter-spacing: 0.25em;
          text-transform: uppercase;
        }
      `}</style>
    </div>
  );
}
