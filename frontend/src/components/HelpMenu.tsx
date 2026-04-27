import './HelpMenu.css'

interface Props {
  onClose: () => void
}

const HELP_ITEMS = [
  { icon: '💸', title: 'Registrar movimiento', desc: 'Tocá el botón + abajo, elegí ingreso o gasto, poné el monto y listo.' },
  { icon: '💬', title: 'Hablar con IA', desc: 'Andá a Insights y preguntale a Flow lo que quieras sobre tus finanzas.' },
  { icon: '🎯', title: 'Crear una meta', desc: 'En Metas, tocá + para crear una meta con nombre, monto y fecha.' },
  { icon: '💰', title: 'Presupuestos', desc: 'En Presupuesto, definí límites por categoría. Te avisamos al 80% y 100%.' },
  { icon: '📊', title: 'Gráficos', desc: 'El dashboard muestra tus gastos por categoría y la tendencia de los últimos 6 meses.' },
  { icon: '🌙', title: 'Modo oscuro', desc: 'Tocá el ícono de sol/luna arriba a la derecha para cambiar.' },
]

export default function HelpMenu({ onClose }: Props) {
  return (
    <div className="help-overlay" onClick={onClose}>
      <div className="help-panel" onClick={e => e.stopPropagation()}>
        <div className="help-header">
          <h2 className="help-title">¿Cómo usar Flow?</h2>
          <button className="btn-icon" onClick={onClose}>✕</button>
        </div>
        <div className="help-items">
          {HELP_ITEMS.map((item, i) => (
            <div key={i} className="help-item">
              <span className="help-icon">{item.icon}</span>
              <div>
                <div className="help-item-title">{item.title}</div>
                <div className="help-item-desc">{item.desc}</div>
              </div>
            </div>
          ))}
        </div>
        <div className="help-footer">
          <p>¿Más preguntas? Escribile a Flow en la pestaña de Insights 💬</p>
        </div>
      </div>
    </div>
  )
}
