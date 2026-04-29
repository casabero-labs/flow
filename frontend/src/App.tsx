import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';

// Telemetry
import { sendTelemetryEvent } from './api/telemetry';

// Auth pages
import Login from './pages/Login';
import Register from './pages/Register';
import PartnershipSetup from './pages/PartnershipSetup';

// Protected pages
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import Goals from './pages/Goals';
import Budgets from './pages/Budgets';
import Insights from './pages/Insights';
import HelpMenu from './components/HelpMenu';

import { useState, useEffect } from 'react';
import './styles/app.css';


function PageViewTracker() {
  const location = useLocation();

  useEffect(() => {
    sendTelemetryEvent('page_view', {
      path: location.pathname,
      search: location.search,
      referrer: document.referrer || undefined,
      user_agent: navigator.userAgent.slice(0, 200),
    });
  }, [location]);

  return null;
}


function AppLayout({ children }: { children: React.ReactNode }) {
  const [darkMode, setDarkMode] = useState(true);
  const [showHelp, setShowHelp] = useState(false);

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <header className="app-header">
        <div className="header-left">
          <span className="logo">flow</span>
        </div>
        <div className="header-right">
          <button
            className="btn-icon"
            onClick={() => setDarkMode(d => !d)}
            title={darkMode ? 'Modo claro' : 'Modo oscuro'}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
          <button
            className="btn-icon"
            onClick={() => setShowHelp(h => !h)}
            title="Ayuda"
          >
            ❓
          </button>
        </div>
      </header>

      <main className="app-main">
        {children}
      </main>

      <nav className="bottom-nav">
        <button className="nav-btn active">
          <span className="nav-icon">🏠</span>
          <span className="nav-label">Inicio</span>
        </button>
        <button className="nav-btn">
          <span className="nav-icon">💸</span>
          <span className="nav-label">Movimientos</span>
        </button>
        <button className="nav-btn">
          <span className="nav-icon">🎯</span>
          <span className="nav-label">Metas</span>
        </button>
        <button className="nav-btn">
          <span className="nav-icon">💰</span>
          <span className="nav-label">Presupuesto</span>
        </button>
        <button className="nav-btn">
          <span className="nav-icon">🔍</span>
          <span className="nav-label">Insights</span>
        </button>
      </nav>

      {showHelp && <HelpMenu onClose={() => setShowHelp(false)} />}
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <PageViewTracker />
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Auth required, no partnership required */}
          <Route
            path="/setup"
            element={
              <ProtectedRoute requirePartnership={false}>
                <PartnershipSetup />
              </ProtectedRoute>
            }
          />

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Dashboard />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/transactions"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Transactions />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/budgets"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Budgets />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/goals"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Goals />
                </AppLayout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/insights"
            element={
              <ProtectedRoute>
                <AppLayout>
                  <Insights />
                </AppLayout>
              </ProtectedRoute>
            }
          />

          {/* Catch all - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
