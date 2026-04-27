import { useState } from 'react'
import './styles/app.css'

// Páginas (se implementan después)
import Dashboard from './pages/Dashboard'
import Transactions from './pages/Transactions'
import Goals from './pages/Goals'
import Budgets from './pages/Budgets'
import Insights from './pages/Insights'
import HelpMenu from './components/HelpMenu'

type Page = 'dashboard' | 'transactions' | 'goals' | 'budgets' | 'insights'

export default function App() {
  const [page, setPage] = useState<Page>('dashboard')
  const [darkMode, setDarkMode] = useState(true)
  const [showHelp, setShowHelp] = useState(false)

  const navItems: { id: Page; label: string; icon: string }[] = [
    { id: 'dashboard', label: 'Inicio', icon: '🏠' },
    { id: 'transactions', label: 'Movimientos', icon: '💸' },
    { id: 'goals', label: 'Metas', icon: '🎯' },
    { id: 'budgets', label: 'Presupuesto', icon: '💰' },
    { id: 'insights', label: 'Insights', icon: '🔍' },
  ]

  const toggleDark = () => setDarkMode(d => !d)

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <span className="logo">flow</span>
        </div>
        <div className="header-right">
          <button
            className="btn-icon"
            onClick={toggleDark}
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

      {/* Main content */}
      <main className="app-main">
        {page === 'dashboard' && <Dashboard />}
        {page === 'transactions' && <Transactions />}
        {page === 'goals' && <Goals />}
        {page === 'budgets' && <Budgets />}
        {page === 'insights' && <Insights />}
      </main>

      {/* Bottom nav (mobile-first) */}
      <nav className="bottom-nav">
        {navItems.map(item => (
          <button
            key={item.id}
            className={`nav-btn ${page === item.id ? 'active' : ''}`}
            onClick={() => setPage(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Help overlay */}
      {showHelp && <HelpMenu onClose={() => setShowHelp(false)} />}
    </div>
  )
}
