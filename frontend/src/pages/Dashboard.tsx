import { useState, useEffect } from 'react'
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import './Dashboard.css'

const ACCENT_COLORS = ['#A78BFA', '#34D399', '#FB923C', '#60A5FA', '#F472B6', '#FBBF24', '#10B981', '#6B7280']

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    fetch('/api/v1/dashboard')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="dashboard">
        <div className="skeleton" style={{ height: 80, marginBottom: 16 }} />
        <div className="skeleton" style={{ height: 200, marginBottom: 16 }} />
        <div className="skeleton" style={{ height: 200 }} />
      </div>
    )
  }

  const fmt = (n: number) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(n)

  return (
    <div className="dashboard">
      <h1 className="page-title">Resumen</h1>

      {/* Balance cards */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-label">Ingresos</div>
          <div className="stat-value income">{fmt(Number(data?.income_this_month || 0))}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Gastos</div>
          <div className="stat-value expense">{fmt(Number(data?.expense_this_month || 0))}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Balance</div>
          <div className="stat-value balance">{fmt(Number(data?.balance_this_month || 0))}</div>
        </div>
      </div>

      {/* Gastos por categoría — torta */}
      {data?.category_totals?.length > 0 && (
        <div className="section">
          <div className="section-title">Gastos por categoría</div>
          <div className="card chart-card">
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={data.category_totals}
                  dataKey="total"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={2}
                >
                  {data.category_totals.map((_: any, i: number) => (
                    <Cell key={i} fill={ACCENT_COLORS[i % ACCENT_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: number) => fmt(v)} />
              </PieChart>
            </ResponsiveContainer>
            <div className="pie-legend">
              {data.category_totals.map((cat: any, i: number) => (
                <div key={i} className="legend-item">
                  <span className="legend-dot" style={{ background: ACCENT_COLORS[i % ACCENT_COLORS.length] }} />
                  <span className="legend-icon">{cat.icon}</span>
                  <span className="legend-name">{cat.category}</span>
                  <span className="legend-pct">{cat.percentage.toFixed(0)}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tendencia mensual — línea */}
      {data?.monthly_trend?.length > 0 && (
        <div className="section">
          <div className="section-title">Tendencia</div>
          <div className="card">
            <ResponsiveContainer width="100%" height={180}>
              <LineChart data={data.monthly_trend}>
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: 'var(--text-muted)' }} />
                <YAxis tick={{ fontSize: 11, fill: 'var(--text-muted)' }} width={60} tickFormatter={(v: number) => `${(v/1000000).toFixed(1)}M`} />
                <Tooltip formatter={(v: number) => fmt(v)} />
                <Line type="monotone" dataKey="income" stroke="#34D399" strokeWidth={2} dot={false} name="Ingresos" />
                <Line type="monotone" dataKey="expense" stroke="#EF4444" strokeWidth={2} dot={false} name="Gastos" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Sin datos */}
      {!data?.category_totals?.length && (
        <div className="empty-state">
          <div className="empty-state-icon">📊</div>
          <div className="empty-state-title">Sin datos todavía</div>
          <p>Registrá tu primer movimiento para ver el dashboard</p>
        </div>
      )}
    </div>
  )
}
