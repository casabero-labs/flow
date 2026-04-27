# Flow — SPEC Técnica Completa

> **App:** Finanzas personales para pareja (Joseph + Luz)
> **Stack:** FastAPI (Python) + React (Vite) + SQLite
> **Estándares:** Casabero UX/UI Manifesto v1 | AI_RULES v1 | COOLIFY_DEPLOY v1
> **Estado:** Diseño arquitectónico v1.0

---

## Tabla de Contenidos

1. [Visión General](#1-visión-general)
2. [Estructura de Carpetas](#2-estructura-de-carpetas)
3. [Modelos de Datos](#3-modelos-de-datos)
4. [Diagrama Entidad-Relación](#4-diagrama-entidad-relación)
5. [Tablas SQLite (DDL)](#5-tablas-sqlite-ddl)
6. [Endpoints del API](#6-endpoints-del-api)
7. [Arquitectura Frontend](#7-arquitectura-frontend)
8. [Integración IA](#8-integración-ia)
9. [Flujo de Datos](#9-flujo-de-datos)
10. [Dependencias](#10-dependencias)
11. [Estructura docs/](#11-estructura-docs)
12. [Despliegue Coolify](#12-despliegue-coolify)

---

## 1. Visión General

Flow es una aplicación de finanzas personales diseñada para que **Joseph** y **Luz** gestionen sus finanzas compartidas e individuales. La app permite:

- Registrar **ingresos y gastos** categorizados por persona y por hogar
- Administrar **presupuestos mensuales** compartidos e individuales
- Gestionar **metas de ahorro** conjuntas
- Recibir **insights inteligentes** sobre patrones de gasto vía IA
- Visualizar **balances y tendencias** con gráficos claros
- **Sincronizar en tiempo real** entre ambos usuarios
- Funcionar con **modo offline** básico (PWA)

### Principios de Diseño (Casabero)

- **Transparencia de Estado**: Skeleton loaders, barras de progreso lineales, sin spinners
- **Minimalismo**: Paleta monocromática con 3 colores pastel de acento
- **Dark Mode**: Toggle obligatorio en header
- **"Dumb Components"**: React funcional + CSS vanilla por componente
- **Liquid Glass**: Animaciones suaves con `cubic-bezier(0.25, 0.46, 0.45, 0.94)`
- **Data-Driven**: Telemetría de uso desde el día 1

---

## 2. Estructura de Carpetas

```
flow/
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Tests + lint
│       └── cd.yml                  # Deploy Coolify
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Settings from env/Infisical
│   │   ├── database.py             # SQLite connection + migrations
│   │   │
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── account.py
│   │   │   ├── transaction.py
│   │   │   ├── category.py
│   │   │   ├── budget.py
│   │   │   ├── goal.py
│   │   │   └── insight.py
│   │   │
│   │   ├── schemas/                # Pydantic schemas (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── account.py
│   │   │   ├── transaction.py
│   │   │   ├── category.py
│   │   │   ├── budget.py
│   │   │   ├── goal.py
│   │   │   └── insight.py
│   │   │
│   │   ├── api/                    # Route handlers
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main router aggregator
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── accounts.py
│   │   │   ├── transactions.py
│   │   │   ├── categories.py
│   │   │   ├── budgets.py
│   │   │   ├── goals.py
│   │   │   └── insights.py
│   │   │
│   │   ├── services/              # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── transaction_service.py
│   │   │   ├── budget_service.py
│   │   │   ├── goal_service.py
│   │   │   ├── balance_service.py
│   │   │   ├── insight_service.py  # AI orchestration
│   │   │   └── analytics_service.py
│   │   │
│   │   ├── ai/                     # AI integration layer
│   │   │   ├── __init__.py
│   │   │   ├── client.py          # LLM client (OpenAI-compatible)
│   │   │   ├── prompts.py         # System prompts
│   │   │   ├── categorizer.py     # Auto-categorization
│   │   │   ├── insights.py        # Spending insights
│   │   │   ├── advisor.py         # Financial advice
│   │   │   └── summarizer.py      # Monthly summaries
│   │   │
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # JWT validation
│   │   │   ├── cors.py
│   │   │   └── telemetry.py       # Usage tracking
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── crypto.py          # Encryption helpers
│   │       ├── dates.py           # Date utilities
│   │       └── validators.py      # Custom validators
│   │
│   ├── migrations/
│   │   ├── 001_initial.sql
│   │   └── 002_seed_categories.sql
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_transactions.py
│   │   ├── test_budgets.py
│   │   ├── test_goals.py
│   │   ├── test_ai.py
│   │   └── test_security.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   ├── manifest.json          # PWA manifest
│   │   ├── sw.js                  # Service worker
│   │   ├── icons/
│   │   └── favicon.svg
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── routes.tsx             # React Router config
│   │   │
│   │   ├── assets/
│   │   │   ├── fonts/
│   │   │   └── images/
│   │   │
│   │   ├── styles/
│   │   │   ├── reset.css
│   │   │   ├── variables.css      # CSS Custom Properties (palette, spacing)
│   │   │   ├── global.css         # Base typography, layout
│   │   │   ├── animations.css     # Liquid glass keyframes
│   │   │   ├── dark.css           # Dark mode overrides
│   │   │   └── utilities.css      # Utility classes
│   │   │
│   │   ├── components/            # "Dumb components" — each has .tsx + .css
│   │   │   ├── ui/                # Atomic design system
│   │   │   │   ├── Button/
│   │   │   │   │   ├── Button.tsx
│   │   │   │   │   ├── Button.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Input/
│   │   │   │   │   ├── Input.tsx
│   │   │   │   │   ├── Input.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Card/
│   │   │   │   │   ├── Card.tsx
│   │   │   │   │   ├── Card.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Modal/
│   │   │   │   │   ├── Modal.tsx
│   │   │   │   │   ├── Modal.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Skeleton/
│   │   │   │   │   ├── Skeleton.tsx
│   │   │   │   │   ├── Skeleton.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── ProgressBar/
│   │   │   │   │   ├── ProgressBar.tsx
│   │   │   │   │   ├── ProgressBar.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Badge/
│   │   │   │   │   ├── Badge.tsx
│   │   │   │   │   ├── Badge.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Toggle/
│   │   │   │   │   ├── Toggle.tsx    # Dark mode toggle
│   │   │   │   │   ├── Toggle.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── EmptyState/
│   │   │   │   │   ├── EmptyState.tsx
│   │   │   │   │   ├── EmptyState.css
│   │   │   │   │   └── index.ts
│   │   │   │   └── HelpMenu/
│   │   │   │       ├── HelpMenu.tsx
│   │   │   │       ├── HelpMenu.css
│   │   │   │       └── index.ts
│   │   │   │
│   │   │   ├── layout/
│   │   │   │   ├── AppShell/
│   │   │   │   │   ├── AppShell.tsx      # Main layout wrapper
│   │   │   │   │   ├── AppShell.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Header/
│   │   │   │   │   ├── Header.tsx
│   │   │   │   │   ├── Header.css
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Sidebar/
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   ├── Sidebar.css
│   │   │   │   │   └── index.ts
│   │   │   │   └── BottomNav/         # Mobile bottom nav
│   │   │   │       ├── BottomNav.tsx
│   │   │   │       ├── BottomNav.css
│   │   │   │       └── index.ts
│   │   │   │
│   │   │   └── feature/             # Domain-specific components
│   │   │       ├── TransactionForm/
│   │   │       │   ├── TransactionForm.tsx
│   │   │       │   ├── TransactionForm.css
│   │   │       │   └── index.ts
│   │   │       ├── TransactionList/
│   │   │       │   ├── TransactionList.tsx
│   │   │       │   ├── TransactionList.css
│   │   │       │   ├── TransactionItem.tsx
│   │   │       │   ├── TransactionItem.css
│   │   │       │   └── index.ts
│   │   │       ├── BudgetCard/
│   │   │       │   ├── BudgetCard.tsx
│   │   │       │   ├── BudgetCard.css
│   │   │       │   └── index.ts
│   │   │       ├── GoalCard/
│   │   │       │   ├── GoalCard.tsx
│   │   │       │   ├── GoalCard.css
│   │   │       │   └── index.ts
│   │   │       ├── BalanceWidget/
│   │   │       │   ├── BalanceWidget.tsx
│   │   │       │   ├── BalanceWidget.css
│   │   │       │   └── index.ts
│   │   │       ├── SpendingChart/
│   │   │       │   ├── SpendingChart.tsx
│   │   │       │   ├── SpendingChart.css
│   │   │       │   └── index.ts
│   │   │       ├── InsightCard/
│   │   │       │   ├── InsightCard.tsx
│   │   │       │   ├── InsightCard.css
│   │   │       │   └── index.ts
│   │   │       ├── CatSelector/
│   │   │       │   ├── CatSelector.tsx
│   │   │       │   ├── CatSelector.css
│   │   │       │   └── index.ts
│   │   │       └── PersonSplit/
│   │   │           ├── PersonSplit.tsx
│   │   │           ├── PersonSplit.css
│   │   │           └── index.ts
│   │   │
│   │   ├── pages/                   # Route-level pages
│   │   │   ├── Dashboard/
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── Dashboard.css
│   │   │   │   └── index.ts
│   │   │   ├── Transactions/
│   │   │   │   ├── TransactionsPage.tsx
│   │   │   │   ├── TransactionsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Budgets/
│   │   │   │   ├── BudgetsPage.tsx
│   │   │   │   ├── BudgetsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Goals/
│   │   │   │   ├── GoalsPage.tsx
│   │   │   │   ├── GoalsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Insights/
│   │   │   │   ├── InsightsPage.tsx
│   │   │   │   ├── InsightsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Reports/
│   │   │   │   ├── ReportsPage.tsx
│   │   │   │   ├── ReportsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Settings/
│   │   │   │   ├── SettingsPage.tsx
│   │   │   │   ├── SettingsPage.css
│   │   │   │   └── index.ts
│   │   │   ├── Login/
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   ├── LoginPage.css
│   │   │   │   └── index.ts
│   │   │   └── Landing/
│   │   │       ├── LandingPage.tsx
│   │   │       ├── LandingPage.css
│   │   │       └── index.ts
│   │   │
│   │   ├── hooks/                   # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useTransactions.ts
│   │   │   ├── useBudgets.ts
│   │   │   ├── useGoals.ts
│   │   │   ├── useInsights.ts
│   │   │   ├── useBalance.ts
│   │   │   ├── useDarkMode.ts
│   │   │   ├── useMediaQuery.ts
│   │   │   └── useOnlineStatus.ts
│   │   │
│   │   ├── context/
│   │   │   ├── AuthContext.tsx
│   │   │   ├── ThemeContext.tsx
│   │   │   └── AppContext.tsx
│   │   │
│   │   ├── api/                     # API client layer
│   │   │   ├── client.ts           # Axios/fetch wrapper with JWT
│   │   │   ├── auth.ts
│   │   │   ├── transactions.ts
│   │   │   ├── budgets.ts
│   │   │   ├── goals.ts
│   │   │   ├── accounts.ts
│   │   │   ├── categories.ts
│   │   │   └── insights.ts
│   │   │
│   │   ├── lib/
│   │   │   ├── format.ts           # Currency, date formatters
│   │   │   ├── charts.ts           # Chart config helpers
│   │   │   └── validators.ts       # Client-side validation
│   │   │
│   │   └── types/
│   │       ├── models.ts           # Shared TypeScript interfaces
│   │       ├── api.ts              # API response types
│   │       └── common.ts           # Utility types
│   │
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf                  # Reverse proxy config
│   └── .env.example
│
├── docs/
│   ├── architecture/
│   │   ├── DECISIONS.md            # Architectural Decision Records
│   │   ├── DATA_FLOW.md            # Detailed data flow diagrams (ASCII)
│   │   ├── AI_INTEGRATION.md       # AI architecture deep-dive
│   │   └── SECURITY.md             # Security model
│   │
│   ├── phases/
│   │   ├── PHASE_001_SETUP.md
│   │   ├── PHASE_002_CORE.md
│   │   ├── PHASE_003_AI.md
│   │   └── PHASE_004_POLISH.md
│   │
│   ├── qa_reports/
│   │   └── README.md
│   │
│   ├── deployments/
│   │   ├── DEPLOYMENT.md
│   │   └── INCIDENTS.md
│   │
│   └── AI_LOG.md
│
├── docker-compose.yml              # Local dev setup
├── DEPLOYMENT.md                   # Coolify deploy manual
├── README.md
├── LICENSE
└── .env.example
```

---

## 3. Modelos de Datos

### 3.1 User

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | Identificador único |
| email | TEXT (UNIQUE) | Email de acceso |
| name | TEXT | Nombre visible (Joseph / Luz) |
| password_hash | TEXT | Hash bcrypt |
| avatar_url | TEXT | Avatar opcional |
| is_active | BOOLEAN | Cuenta activa |
| created_at | DATETIME | Fecha registro |
| updated_at | DATETIME | Última actualización |
| last_login | DATETIME | Último ingreso |
| onboarding_completed | BOOLEAN | Onboarding terminado |
| preferences | JSON | Preferencias de UI (tema, moneda, notificaciones) |

### 3.2 Account

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | Identificador único |
| user_id | UUID (FK → User) | Propietario (NULL si es compartida) |
| name | TEXT | Nombre de la cuenta (ej: "Bancolombia", "Efectivo", "Nequi") |
| type | TEXT | Tipo: `checking`, `savings`, `cash`, `investment` |
| currency | TEXT | Código ISO (ej: "COP", "USD") |
| balance | REAL | Balance actual |
| is_joint | BOOLEAN | TRUE si es cuenta compartida |
| icon | TEXT | Emoji o icono representativo |
| color | TEXT | Color de acento (hex) |
| is_archived | BOOLEAN | Cuenta archivada |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### 3.3 Category

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| name | TEXT | Ej: "Alimentos", "Transporte", "Salud" |
| icon | TEXT | Emoji representativo |
| color | TEXT | Color de acento (hex) |
| type | TEXT | `income` o `expense` |
| parent_id | UUID (FK → Category, NULL) | Categoría padre (subcategorías) |
| is_system | BOOLEAN | TRUE = categoría por defecto del sistema |
| sort_order | INTEGER | Orden de visualización |
| created_at | DATETIME | |

**Categorías del sistema (seed):**

```
Ingresos:
  ├── Salario
  ├── Freelance / Negocios
  ├── Inversiones
  ├── Regalos
  └── Otros Ingresos

Gastos:
  ├── Vivienda (Arriendo, Servicios, Mantenimiento)
  ├── Alimentos (Mercado, Comidas fuera, Delivery)
  ├── Transporte (Gasolina, Taxi/Uber, Parqueadero, Transporte público)
  ├── Salud (Médico, Medicinas, Seguro)
  ├── Educación (Cursos, Libros, Suscripciones)
  ├── Entretenimiento (Streaming, Salidas, Hobbies)
  ├── Tecnología (Internet, Celular, Software)
  ├── Ropa y Accesorios
  ├── Ahorro e Inversiones
  ├── Impuestos y Bancarios
  └── Otros Gastos
```

### 3.4 Transaction

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| account_id | UUID (FK → Account) | Cuenta origen/destino |
| category_id | UUID (FK → Category) | Categoría |
| user_id | UUID (FK → User) | Quien registró |
| amount | REAL | Monto (positivo = ingreso, negativo = gasto) |
| description | TEXT | Descripción libre |
| date | DATE | Fecha de la transacción |
| is_recurring | BOOLEAN | TRUE si es pago recurrente |
| recurring_id | UUID (FK → Recurring, NULL) | ID de recurrencia si aplica |
| tags | JSON | Array de tags libres |
| notes | TEXT | Notas internas |
| attachment_url | TEXT | URL de foto/comprobante |
| is_split | BOOLEAN | TRUE si es dividida entre Joseph y Luz |
| split_ratio | REAL | Proporción para Joseph (0.0-1.0). Ej: 0.5 = 50/50 |
| is_verified | BOOLEAN | TRUE si ambos confirmaron |
| verified_by | JSON | Array de user_ids que verificaron |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### 3.5 Recurring Transaction

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User) | |
| account_id | UUID (FK → Account) | |
| category_id | UUID (FK → Category) | |
| amount | REAL | |
| description | TEXT | |
| frequency | TEXT | `daily`, `weekly`, `biweekly`, `monthly`, `yearly` |
| interval | INTEGER | Cada N unidades (ej: cada 2 meses) |
| next_date | DATE | Próxima fecha de ejecución |
| end_date | DATE | NULL = indefinido |
| is_active | BOOLEAN | |
| created_at | DATETIME | |

### 3.6 Budget

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User, NULL) | NULL = presupuesto compartido |
| category_id | UUID (FK → Category) | |
| month | TEXT | Mes en formato "YYYY-MM" |
| limit_amount | REAL | Límite del presupuesto |
| spent_amount | REAL | Calculado automáticamente |
| is_joint | BOOLEAN | TRUE = presupuesto de pareja |
| rollover | BOOLEAN | TRUE = el sobrante se acumula al siguiente mes |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### 3.7 Goal

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User, NULL) | NULL = meta compartida |
| name | TEXT | Nombre de la meta |
| description | TEXT | Descripción |
| target_amount | REAL | Monto objetivo |
| current_amount | REAL | Monto actual ahorrado |
| currency | TEXT | |
| deadline | DATE | Fecha límite (NULL = sin fecha) |
| priority | TEXT | `low`, `medium`, `high` |
| category | TEXT | `savings`, `investment`, `debt_payment`, `travel`, `purchase`, `emergency`, `other` |
| icon | TEXT | |
| color | TEXT | |
| is_joint | BOOLEAN | TRUE = meta de pareja |
| is_completed | BOOLEAN | |
| completed_at | DATETIME | |
| auto_allocate | BOOLEAN | TRUE = asignar automático desde ingresos |
| auto_percentage | REAL | Porcentaje del ingreso a asignar (0.0-1.0) |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### 3.8 Goal Contribution

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| goal_id | UUID (FK → Goal) | |
| user_id | UUID (FK → User) | Quien contribuyó |
| amount | REAL | |
| date | DATE | |
| notes | TEXT | |
| created_at | DATETIME | |

### 3.9 Insight

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User, NULL) | NULL = para ambos |
| type | TEXT | `spending_alert`, `saving_tip`, `budget_warning`, `goal_milestone`, `monthly_summary`, `pattern_detected`, `anomaly`, `recommendation` |
| title | TEXT | Título corto |
| content | TEXT | Contenido del insight (generado por IA o reglas) |
| severity | TEXT | `info`, `warning`, `critical`, `success` |
| category_id | UUID (FK → Category, NULL) | Categoría relacionada |
| is_read | BOOLEAN | |
| is_dismissed | BOOLEAN | |
| metadata | JSON | Datos adicionales (monto, porcentaje, etc.) |
| created_at | DATETIME | |
| read_at | DATETIME | |

### 3.10 Sync Log

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User) | |
| action | TEXT | `create`, `update`, `delete` |
| entity_type | TEXT | `transaction`, `budget`, `goal`, etc. |
| entity_id | UUID | ID de la entidad afectada |
| payload | JSON | Snapshot del cambio |
| created_at | DATETIME | |

### 3.11 Telemetry Event

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID (PK) | |
| user_id | UUID (FK → User) | |
| event | TEXT | `page_view`, `feature_use`, `error`, `action` |
| page | TEXT | Ruta de la página |
| metadata | JSON | Datos contextuales |
| duration_ms | INTEGER | Tiempo en página |
| created_at | DATETIME | |

---

## 4. Diagrama Entidad-Relación

```
┌─────────────┐       ┌──────────────────┐
│    User     │1──N──▶│     Account      │
└─────────────┘       └──────────────────┘
       │1                    │1
       │                     │
       │                     │N
       │              ┌──────┴──────────┐
       │1             │  Transaction    │◀──┐
       │              │                 │   │
       │              └──────┬──────────┘   │
       │                     │N             │
       │               ┌─────┴──────┐       │
       │               │  Category  │1──────┘
       │               └────────────┘
       │1
       │              ┌──────────────┐
       ├─────────────▶│    Budget    │
       │              └──────────────┘
       │1
       │              ┌──────────────┐
       ├─────────────▶│     Goal     │
       │              └───┬──────────┘
       │                  │1
       │                  │
       │             ┌────┴───────────┐
       │             │GoalContribution│
       │             └────────────────┘
       │1
       │              ┌──────────────┐
       ├─────────────▶│   Insight    │
       │              └──────────────┘
       │1
       │              ┌──────────────┐
       ├─────────────▶│  SyncLog     │
       │              └──────────────┘
       │1
       │              ┌──────────────┐
       └─────────────▶│ Telemetry    │
                      └──────────────┘

Relaciones clave:
- User 1 ──N Transaction (quien registró)
- User 1 ──N Account (propietario)
- User 1 ──N Budget (propietario, NULL = compartido)
- User 1 ──N Goal (propietario, NULL = compartido)
- Account 1 ──N Transaction
- Category 1 ──N Transaction
- Category 1 ──N Budget
- Category 1 ──N Category (self: parent→children)
- Goal 1 ──N GoalContribution
```

---

## 5. Tablas SQLite (DDL)

```sql
-- ============================================================
-- FLOW — SQLite Schema v1
-- ============================================================
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -20000; -- 20MB cache

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    email           TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    password_hash   TEXT NOT NULL,
    avatar_url      TEXT,
    is_active       INTEGER NOT NULL DEFAULT 1,
    onboarding_completed INTEGER NOT NULL DEFAULT 0,
    preferences     TEXT DEFAULT '{}', -- JSON
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    last_login      TEXT
);

CREATE INDEX idx_users_email ON users(email);

-- ============================================================
-- ACCOUNTS
-- ============================================================
CREATE TABLE IF NOT EXISTS accounts (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT REFERENCES users(id) ON DELETE SET NULL,
    name            TEXT NOT NULL,
    type            TEXT NOT NULL CHECK(type IN ('checking','savings','cash','investment')),
    currency        TEXT NOT NULL DEFAULT 'COP',
    balance         REAL NOT NULL DEFAULT 0.0,
    is_joint        INTEGER NOT NULL DEFAULT 0,
    icon            TEXT,
    color           TEXT DEFAULT '#4A5568',
    is_archived     INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_accounts_user ON accounts(user_id);
CREATE INDEX idx_accounts_joint ON accounts(is_joint);

-- ============================================================
-- CATEGORIES
-- ============================================================
CREATE TABLE IF NOT EXISTS categories (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    name            TEXT NOT NULL,
    icon            TEXT,
    color           TEXT DEFAULT '#718096',
    type            TEXT NOT NULL CHECK(type IN ('income','expense')),
    parent_id       TEXT REFERENCES categories(id) ON DELETE SET NULL,
    is_system       INTEGER NOT NULL DEFAULT 0,
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_categories_type ON categories(type);
CREATE INDEX idx_categories_parent ON categories(parent_id);

-- ============================================================
-- TRANSACTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS transactions (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    account_id      TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    category_id     TEXT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount          REAL NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    date            TEXT NOT NULL,
    is_recurring    INTEGER NOT NULL DEFAULT 0,
    recurring_id    TEXT REFERENCES recurring_transactions(id) ON DELETE SET NULL,
    tags            TEXT DEFAULT '[]', -- JSON array
    notes           TEXT DEFAULT '',
    attachment_url  TEXT,
    is_split        INTEGER NOT NULL DEFAULT 0,
    split_ratio     REAL DEFAULT NULL CHECK(split_ratio IS NULL OR (split_ratio >= 0 AND split_ratio <= 1)),
    is_verified     INTEGER NOT NULL DEFAULT 0,
    verified_by     TEXT DEFAULT '[]', -- JSON array of user_ids
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_month ON transactions(substr(date,1,7));
CREATE INDEX idx_transactions_split ON transactions(is_split);

-- ============================================================
-- RECURRING TRANSACTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS recurring_transactions (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id      TEXT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    category_id     TEXT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    amount          REAL NOT NULL,
    description     TEXT NOT NULL DEFAULT '',
    frequency       TEXT NOT NULL CHECK(frequency IN ('daily','weekly','biweekly','monthly','yearly')),
    interval_value  INTEGER NOT NULL DEFAULT 1,
    next_date       TEXT NOT NULL,
    end_date        TEXT,
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_recurring_active ON recurring_transactions(is_active, next_date);

-- ============================================================
-- BUDGETS
-- ============================================================
CREATE TABLE IF NOT EXISTS budgets (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    category_id     TEXT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    month           TEXT NOT NULL,  -- 'YYYY-MM'
    limit_amount    REAL NOT NULL CHECK(limit_amount > 0),
    spent_amount    REAL NOT NULL DEFAULT 0.0,
    is_joint        INTEGER NOT NULL DEFAULT 0,
    rollover        INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, category_id, month)
);

CREATE INDEX idx_budgets_month ON budgets(month);
CREATE INDEX idx_budgets_user_month ON budgets(user_id, month);

-- ============================================================
-- GOALS
-- ============================================================
CREATE TABLE IF NOT EXISTS goals (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,
    description     TEXT DEFAULT '',
    target_amount   REAL NOT NULL CHECK(target_amount > 0),
    current_amount  REAL NOT NULL DEFAULT 0.0,
    currency        TEXT NOT NULL DEFAULT 'COP',
    deadline        TEXT,
    priority        TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low','medium','high')),
    category        TEXT NOT NULL DEFAULT 'savings' CHECK(category IN ('savings','investment','debt_payment','travel','purchase','emergency','other')),
    icon            TEXT,
    color           TEXT DEFAULT '#48BB78',
    is_joint        INTEGER NOT NULL DEFAULT 0,
    is_completed    INTEGER NOT NULL DEFAULT 0,
    completed_at    TEXT,
    auto_allocate   INTEGER NOT NULL DEFAULT 0,
    auto_percentage REAL DEFAULT NULL CHECK(auto_percentage IS NULL OR (auto_percentage > 0 AND auto_percentage <= 1)),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_goals_user ON goals(user_id);
CREATE INDEX idx_goals_active ON goals(is_completed);

-- ============================================================
-- GOAL CONTRIBUTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS goal_contributions (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    goal_id         TEXT NOT NULL REFERENCES goals(id) ON DELETE CASCADE,
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount          REAL NOT NULL CHECK(amount > 0),
    date            TEXT NOT NULL,
    notes           TEXT DEFAULT '',
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_goal_contrib_goal ON goal_contributions(goal_id);

-- ============================================================
-- INSIGHTS
-- ============================================================
CREATE TABLE IF NOT EXISTS insights (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT REFERENCES users(id) ON DELETE CASCADE,
    type            TEXT NOT NULL CHECK(type IN (
                        'spending_alert','saving_tip','budget_warning',
                        'goal_milestone','monthly_summary','pattern_detected',
                        'anomaly','recommendation'
                    )),
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,
    severity        TEXT NOT NULL DEFAULT 'info' CHECK(severity IN ('info','warning','critical','success')),
    category_id     TEXT REFERENCES categories(id) ON DELETE SET NULL,
    is_read         INTEGER NOT NULL DEFAULT 0,
    is_dismissed    INTEGER NOT NULL DEFAULT 0,
    metadata        TEXT DEFAULT '{}', -- JSON
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    read_at         TEXT
);

CREATE INDEX idx_insights_user ON insights(user_id);
CREATE INDEX idx_insights_unread ON insights(user_id, is_read, is_dismissed);

-- ============================================================
-- SYNC LOG
-- ============================================================
CREATE TABLE IF NOT EXISTS sync_log (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action          TEXT NOT NULL CHECK(action IN ('create','update','delete')),
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    payload         TEXT DEFAULT '{}', -- JSON snapshot
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_sync_user ON sync_log(user_id, created_at);

-- ============================================================
-- TELEMETRY
-- ============================================================
CREATE TABLE IF NOT EXISTS telemetry_events (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event           TEXT NOT NULL,
    page            TEXT,
    metadata        TEXT DEFAULT '{}',
    duration_ms     INTEGER,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_telemetry_user ON telemetry_events(user_id);
CREATE INDEX idx_telemetry_event ON telemetry_events(event);
CREATE INDEX idx_telemetry_date ON telemetry_events(created_at);

-- ============================================================
-- SESSIONS (for JWT refresh tracking)
-- ============================================================
CREATE TABLE IF NOT EXISTS sessions (
    id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id         TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash      TEXT NOT NULL,
    ip_address      TEXT,
    user_agent      TEXT,
    expires_at      TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_token ON sessions(token_hash);
```

---

## 6. Endpoints del API

### 6.1 Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/auth/register` | Registrar nuevo usuario | No |
| POST | `/api/v1/auth/login` | Iniciar sesión | No |
| POST | `/api/v1/auth/logout` | Cerrar sesión | Sí |
| POST | `/api/v1/auth/refresh` | Refrescar JWT | Sí |
| GET | `/api/v1/auth/me` | Obtener perfil actual | Sí |
| PATCH | `/api/v1/auth/me` | Actualizar perfil | Sí |
| PATCH | `/api/v1/auth/me/preferences` | Actualizar preferencias | Sí |
| POST | `/api/v1/auth/change-password` | Cambiar contraseña | Sí |

### 6.2 Usuarios (pareja)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/users` | Listar usuarios (para la pareja) | Sí |
| GET | `/api/v1/users/{id}` | Obtener usuario específico | Sí |
| GET | `/api/v1/users/partner` | Obtener datos del otro miembro | Sí |

### 6.3 Cuentas

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/accounts` | Listar cuentas del usuario | Sí |
| POST | `/api/v1/accounts` | Crear cuenta | Sí |
| GET | `/api/v1/accounts/{id}` | Obtener cuenta detalle | Sí |
| PATCH | `/api/v1/accounts/{id}` | Actualizar cuenta | Sí |
| DELETE | `/api/v1/accounts/{id}` | Archivar/eliminar cuenta | Sí |
| PATCH | `/api/v1/accounts/{id}/reorder` | Reordenar cuentas | Sí |
| GET | `/api/v1/accounts/{id}/balance-history` | Historial de balance | Sí |

### 6.4 Transacciones

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/transactions` | Listar transacciones (filtros: account, category, date_from, date_to, user, page, limit) | Sí |
| POST | `/api/v1/transactions` | Crear transacción | Sí |
| GET | `/api/v1/transactions/{id}` | Obtener transacción | Sí |
| PATCH | `/api/v1/transactions/{id}` | Actualizar transacción | Sí |
| DELETE | `/api/v1/transactions/{id}` | Eliminar transacción | Sí |
| POST | `/api/v1/transactions/batch` | Crear transacciones en lote | Sí |
| DELETE | `/api/v1/transactions/batch` | Eliminar transacciones en lote | Sí |
| POST | `/api/v1/transactions/{id}/verify` | Verificar transacción (split) | Sí |
| GET | `/api/v1/transactions/search` | Búsqueda avanzada | Sí |
| GET | `/api/v1/transactions/stats` | Estadísticas agregadas | Sí |

### 6.5 Categorías

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/categories` | Listar categorías | Sí |
| POST | `/api/v1/categories` | Crear categoría personalizada | Sí |
| GET | `/api/v1/categories/{id}` | Obtener categoría | Sí |
| PATCH | `/api/v1/categories/{id}` | Actualizar categoría | Sí |
| DELETE | `/api/v1/categories/{id}` | Eliminar categoría personalizada | Sí |

### 6.6 Presupuestos

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/budgets` | Listar presupuestos (filtro: month) | Sí |
| POST | `/api/v1/budgets` | Crear presupuesto | Sí |
| GET | `/api/v1/budgets/{id}` | Obtener presupuesto | Sí |
| PATCH | `/api/v1/budgets/{id}` | Actualizar presupuesto | Sí |
| DELETE | `/api/v1/budgets/{id}` | Eliminar presupuesto | Sí |
| GET | `/api/v1/budgets/monthly-summary` | Resumen del mes actual | Sí |
| POST | `/api/v1/budgets/clone` | Clonar presupuestos del mes anterior | Sí |

### 6.7 Metas

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/goals` | Listar metas | Sí |
| POST | `/api/v1/goals` | Crear meta | Sí |
| GET | `/api/v1/goals/{id}` | Obtener meta con progreso | Sí |
| PATCH | `/api/v1/goals/{id}` | Actualizar meta | Sí |
| DELETE | `/api/v1/goals/{id}` | Eliminar meta | Sí |
| POST | `/api/v1/goals/{id}/contribute` | Aportar a una meta | Sí |
| GET | `/api/v1/goals/{id}/contributions` | Historial de aportes | Sí |

### 6.8 Insights (IA)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/insights` | Listar insights del usuario | Sí |
| PATCH | `/api/v1/insights/{id}/read` | Marcar como leído | Sí |
| PATCH | `/api/v1/insights/{id}/dismiss` | Descartar insight | Sí |
| POST | `/api/v1/insights/generate` | Forzar generación de insights IA | Sí |
| GET | `/api/v1/insights/monthly-summary` | Resumen mensual por IA | Sí |
| POST | `/api/v1/insights/classify` | Clasificar transacción por IA | Sí |
| POST | `/api/v1/insights/advise` | Pedir consejo financiero | Sí |

### 6.9 Reportes y Analytics

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/reports/spending-by-category` | Gastos agrupados por categoría | Sí |
| GET | `/api/v1/reports/spending-by-person` | Gastos por persona | Sí |
| GET | `/api/v1/reports/spending-trend` | Tendencia de gastos mensual | Sí |
| GET | `/api/v1/reports/net-worth` | Patrimonio neto histórico | Sí |
| GET | `/api/v1/reports/cashflow` | Flujo de caja mensual | Sí |
| GET | `/api/v1/reports/comparison` | Comparación mes vs mes | Sí |
| GET | `/api/v1/reports/export` | Exportar datos (CSV/PDF) | Sí |

### 6.10 Sync (colaboración en tiempo real)

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/sync/changes` | Obtener cambios desde último sync | Sí |
| POST | `/api/v1/sync/push` | Enviar cambios locales | Sí |

### 6.11 Telemetría

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/telemetry/event` | Registrar evento | Sí |

### 6.12 Health & Status

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/health` | Health check | No |
| GET | `/api/v1/status` | Estado del sistema | No |
| GET | `/api/v1/version` | Versión de la app | No |

---

## 7. Arquitectura Frontend

### 7.1 Principios Arquitectónicos

1. **Dumb Components**: Cada componente es una función React pura, sin lógica de negocio. Recibe props, renderiza UI.
2. **CSS Vanilla**: Tailwind PROHIBIDO por defecto. Cada componente tiene su archivo `.css` homónimo. Variables globales en `variables.css`.
3. **Pages como orquestadoras**: Las páginas importan componentes "dumb" y hooks con lógica de negocio.
4. **API Layer**: Toda comunicación con backend pasa por `src/api/client.ts` que maneja JWT, refresh, errores y caché.
5. **Context mínimo**: Solo para auth y theme. El resto viaja por props o hooks.

### 7.2 Paleta de Colores (Monocromática + 3 Acentos)

Siguiendo el UX/UI Manifesto — máximo 3 colores de acento:

```
Variables CSS (variables.css):

--color-bg-light: #FFFFFF;
--color-bg-dark: #0F1117;
--color-surface-light: #F7F8FA;
--color-surface-dark: #1A1D27;
--color-border-light: #E5E7EB;
--color-border-dark: #2D3748;
--color-text-primary-light: #1A202C;
--color-text-primary-dark: #E2E8F0;
--color-text-secondary-light: #718096;
--color-text-secondary-dark: #A0AEC0;

--color-accent-1: #6C5CE7;  /* Púrpura pastel — balance general */
--color-accent-2: #48BB78;  /* Verde pastel — ahorro/metas */
--color-accent-3: #F6AD55;  /* Naranja pastel — alertas/gastos */

--color-success: #48BB78;
--color-warning: #F6AD55;
--color-danger: #FC8181;
--color-info: #63B3ED;

--font-display: 'Outfit', sans-serif;
--font-body: 'Inter', sans-serif;
--font-mono: 'Fira Code', monospace;

--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 16px;
--radius-xl: 24px;

--shadow-card: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
--shadow-card-hover: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.05);
--shadow-elevated: 0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04);

--transition-default: cubic-bezier(0.25, 0.46, 0.45, 0.94);
```

### 7.3 Layout y Navegación

```
Desktop (>1024px):
┌─────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────────────────────────┐ │
│  │  Sidebar │  │                              │ │
│  │          │  │          Header              │ │
│  │  📊 Dash │  │   💰 Balance    🌓 Toggle    │ │
│  │  💳 Trans│  │                              │ │
│  │  📋 Budget│  ├──────────────────────────────┤ │
│  │  🎯 Metas │  │                              │ │
│  │  💡 Insights│  │        Main Content         │ │
│  │  📈 Reports│  │                              │ │
│  │  ⚙️ Config│  │                              │ │
│  └──────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────┘

Mobile (<768px):
┌─────────────────┐
│     Header      │
│  🌓  💰 Flow   │
├─────────────────┤
│                 │
│   Main Content  │
│                 │
├─────────────────┤
│ 📊 │ 💳 │ 📋 │ 💡 │
└─────────────────┘
  Bottom Navigation
```

### 7.4 Árbol de Componentes por Página

**Dashboard (`/dashboard`)**:
```
<DashboardPage>
  ├── <AppShell>
  │   ├── <Sidebar /> | <BottomNav />
  │   ├── <Header>
  │   │   ├── <BalanceWidget />        ← Balance total + individial
  │   │   ├── <Toggle />               ← Dark mode
  │   │   └── <HelpMenu />
  │   └── <main>
  │       ├── <Card> <BalanceWidget expanded /> </Card>
  │       ├── <Card> <SpendingChart /> </Card>
  │       ├── <Card> <BudgetCard /> </Card>      ← Top 3 budgets
  │       ├── <Card> <GoalCard /> </Card>        ← Top metas
  │       └── <Card> <InsightCard /> </Card>     ← Último insight IA
  └── </AppShell>
```

**Transacciones (`/transactions`)**:
```
<TransactionsPage>
  ├── <AppShell>
  │   └── <main>
  │       ├── <Input search /> + <Button "Nueva" />
  │       ├── <FilterBar> (date, category, account, person) </FilterBar>
  │       └── <TransactionList>
  │           ├── <TransactionItem /> * N
  │           └── <Skeleton /> * 5  ← loading state
  └── <Modal "Nueva Transacción">
      └── <TransactionForm>
          ├── <Input amount (numeric mode) />
          ├── <CatSelector />
          ├── <PersonSplit />       ← toggle dividir con Luz
          ├── <Input description />
          ├── <Input date />
          └── <Button "Guardar" />
```

**Presupuestos (`/budgets`)**:
```
<BudgetsPage>
  ├── <AppShell>
  │   └── <main>
  │       ├── <ProgressBar /> (global: gastado/total)
  │       ├── <MonthSelector />
  │       └── <BudgetCard /> * N (por categoría)
  │           ├── <ProgressBar />
  │           ├── spent/limit text
  │           └── <Badge> (restante / excedido)
  └── <Modal "Nuevo Presupuesto">
      └── <Form>
```

**Metas (`/goals`)**:
```
<GoalsPage>
  ├── <AppShell>
  │   └── <main>
  │       └── <GoalCard /> * N
  │           ├── <ProgressBar />
  │           ├── current/target text
  │           ├── deadline countdown
  │           └── <Button "Aportar" />
  └── <Modal "Nueva Meta" / "Aportar">
```

**Insights (`/insights`)**:
```
<InsightsPage>
  ├── <AppShell>
  │   └── <main>
  │       ├── <Card "Resumen IA del mes" />
  │       └── <InsightCard /> * N (filterable by type)
  │           ├── <Badge severity>
  │           ├── title + content
  │           └── <Button dismiss>
```

### 7.5 Estados de UI (por componente)

Cada componente "dumb" maneja estos estados visuales:

| Estado | Implementación |
|--------|---------------|
| **Loading** | `<Skeleton />` con opacidad pulsante (breathe animation) |
| **Empty** | `<EmptyState icon message action />` |
| **Error** | Card con borde rojo, mensaje, botón reintentar |
| **Success** | Feedback sutil (green flash, checkmark) |
| **Offline** | Badge "Sin conexión" + datos cacheados |

---

## 8. Integración IA

### 8.1 Arquitectura de IA

```
┌──────────────┐     ┌─────────────────────┐     ┌───────────────┐
│  Frontend    │────▶│  Backend (FastAPI)  │────▶│  LLM Client   │
│  (React)     │     │                     │     │  (OpenAI-compat)│
└──────────────┘     │  services/          │     └───────┬───────┘
                     │  insight_service.py │             │
                     │  ai/                │     ┌───────┴───────┐
                     │  └─ client.py       │     │  Ollama /     │
                     │  └─ prompts.py      │     │  OpenAI /     │
                     │  └─ categorizer.py  │     │  DeepSeek     │
                     │  └─ insights.py     │     └───────────────┘
                     │  └─ advisor.py      │
                     │  └─ summarizer.py   │
                     └─────────────────────┘
```

### 8.2 Casos de Uso de IA

#### 8.2.1 Auto-clasificación de Transacciones

```python
# ai/categorizer.py
# Input: description, amount, known_categories
# Output: suggested category_id + confidence

PROMPT_SYSTEM = """
Eres un asistente financiero que clasifica transacciones personales.
Basado en la descripción y el monto, sugiere la categoría más apropiada
de la lista proporcionada. Responde SOLO con JSON.
"""

PROMPT_CLASSIFY = """
Descripción: {description}
Monto: {amount}
Categorías disponibles: {categories}
Responde: {{"category_id": "...", "confidence": 0.95, "reason": "..."}}
"""
```

#### 8.2.2 Generación de Insights

```python
# ai/insights.py
# Se ejecuta: diariamente (cron) + al agregar transacción significativa
# Genera insights basados en patrones detectados

TIPOS DE INSIGHT GENERADOS:
1. spending_alert:  "Gastaste 40% más en restaurantes este mes"
2. saving_tip:      "Podrías ahorrar $200K/mes si cocinas 3 veces más"
3. budget_warning:  "Tu presupuesto de 'Salud' está al 90%"
4. pattern_detected:"Compras en MercadoLibre cada viernes"
5. anomaly:         "Este gasto de $500K es atípico en tu historial"
6. recommendation:  "Basado en tu patrón, podrías invertir $X este mes"
```

#### 8.2.3 Resumen Mensual

```python
# ai/summarizer.py
# Input: todas las transacciones del mes
# Output: resumen narrativo + recomendaciones

PROMPT_SYSTEM = """
Eres un asesor financiero amigable para una pareja colombiana.
Genera un resumen mensual claro, útil y motivador.
Incluye: total gastado, categorías principales, comparación mes anterior,
y recomendaciones específicas para el próximo mes.
"""
```

#### 8.2.4 Chat/Consejo Financiero

```python
# ai/advisor.py
# Input: pregunta del usuario + contexto financiero
# Output: respuesta contextualizada

PROMPT_SYSTEM = """
Eres Flow, el asistente financiero de Joseph y Luz.
Tienes acceso a su contexto financiero actual: balance, gastos del mes,
metas activas, presupuestos. Respondes con consejos prácticos y realistas
para la realidad colombiana.
"""
```

### 8.3 Modelo de IA y Configuración

```yaml
# Configuración (config.py)
AI_PROVIDER: "ollama" | "openai" | "deepseek"
AI_MODEL: "deepseek-v4-flash"  # preferido por ecosistema Casabero
AI_ENDPOINT: "http://localhost:11434/v1"  # Ollama local
AI_TEMPERATURE: 0.3  # Bajo para clasificación consistente
AI_MAX_TOKENS: 500
AI_FALLBACK: "openai"  # Si Ollama no responde

# Estrategia de caché de insights
INSIGHT_CACHE_TTL: 3600  # 1 hora
INSIGHT_BATCH_SIZE: 10    # Procesar en lotes
INSIGHT_MIN_CONFIDENCE: 0.7  # Ignorar insights de baja confianza
```

### 8.4 Clasificación Offline (Reglas)

Cuando no hay conexión a IA (modo offline), se usa clasificación por reglas:

```python
# ai/categorizer.py — fallback rules
RULES = [
    (r'(mercadolibre|exito|carulla|olimpica|d1|ara|mercado)', 'Comida'),
    (r'(uber|taxi|transmilenio|gasolina|parqueadero)', 'Transporte'),
    (r'(netflix|spotify|youtube|disney|hbo|prime)', 'Suscripciones'),
    (r'(salud|eps|medico|farmacia|drogueria)', 'Salud'),
    # ...
]
```

---

## 9. Flujo de Datos

### 9.1 Flujo Principal: Registrar Gasto

```
[Usuario]                              [Frontend]                         [Backend]                            [SQLite]
    │                                       │                                │                                   │
    │  Abre modal "Nuevo Gasto"             │                                │                                   │
    │──────────────────────────────────────▶│                                │                                   │
    │                                       │                                │                                   │
    │  Llena formulario:                    │                                │                                   │
    │  - Monto: $150,000                    │                                │                                   │
    │  - Categoría: (auto-sugerida)         │                                │                                   │
    │  - Descripción: "Almuerzo"            │                                │                                   │
    │  - Dividir: Sí (50/50)                │                                │                                   │
    │──────────────────────────────────────▶│                                │                                   │
    │                                       │                                │                                   │
    │                                       │  Valida cliente                │                                   │
    │                                       │  ├─ Monto > 0                  │                                   │
    │                                       │  ├─ Categoría válida           │                                   │
    │                                       │  └─ Descripción no vacía      │                                   │
    │                                       │                                │                                   │
    │                                       │  POST /api/v1/transactions     │                                   │
    │                                       │───────────────────────────────▶│                                   │
    │                                       │                                │                                   │
    │                                       │                                │  Valida servidor                   │
    │                                       │                                │  ├─ JWT válido                     │
    │                                       │                                │  ├─ Account existe                 │
    │                                       │                                │  └─ Category existe                │
    │                                       │                                │                                   │
    │                                       │                                │  INSERT INTO transactions          │
    │                                       │                                │──────────────────────────────────▶│
    │                                       │                                │                                   │
    │                                       │                                │  UPDATE accounts.balance           │
    │                                       │                                │──────────────────────────────────▶│
    │                                       │                                │                                   │
    │                                       │                                │  ── Async ──                      │
    │                                       │                                │  ¿Actualizar budgets?             │
    │                                       │                                │  UPDATE budgets.spent_amount      │
    │                                       │                                │  ────────────────────────────────▶│
    │                                       │                                │                                   │
    │                                       │                                │  ¿Generar insights?               │
    │                                       │                                │  ── AI Client ──                  │
    │                                       │                                │  ├─ ¿Anomalía?                    │
    │                                       │                                │  ├─ ¿Budget cerca límite?         │
    │                                       │                                │  └─ ¿Patrón detectado?            │
    │                                       │                                │                                   │
    │                                       │  ◀── 201 Created ────          │                                   │
    │                                       │  { transaction, new_insights } │                                   │
    │                                       │                                │                                   │
    │  ◀── UI actualizada ───               │                                │                                   │
    │  - Lista recargada                    │                                │                                   │
    │  - Balance actualizado                │                                │                                   │
    │  - Insight nuevo (si aplica)          │                                │                                   │
    │                                       │                                │                                   │
    │  ── Sincronización ──                 │                                │                                   │
    │  (el otro miembro recibe cambio)      │                                │                                   │
    │  GET /api/v1/sync/changes             │                                │                                   │
    │  ←→ polling cada 30s / WebSocket      │                                │                                   │
```

### 9.2 Flujo de Insights Automáticos

```
[Cron: Cada 6 horas]        [Cron: Diario 9pm]        [On Transaction]
        │                        │                          │
        ▼                        ▼                          ▼
┌────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│ Check budgets  │    │ Monthly summary  │    │ Pattern detection │
│ near limit     │    │ (fin de mes)     │    │ (real-time)       │
└───────┬────────┘    └────────┬─────────┘    └────────┬───────────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  insight_service.py │
                    │                     │
                    │  ¿Usar IA o Reglas? │
                    │  ├─ Online → LLM    │
                    │  └─ Offline→ Reglas │
                    │                     │
                    │  Generar Insight    │
                    │  INSERT INTO        │
                    │  insights           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Notificar usuario  │
                    │  (UI badge + toast) │
                    └─────────────────────┘
```

### 9.3 Flujo de Sincronización (Pareja)

```
[Joseph]                          [Backend]                           [Luz]
   │                                  │                                 │
   │  Crea transacción                │                                 │
   │─────────────────────────────────▶│                                 │
   │                                  │  INSERT + sync_log              │
   │                                  │                                 │
   │  ◀── 201 ───────────────────────│                                 │
   │                                  │                                 │
   │                                  │   ── WebSocket / Polling ──     │
   │                                  │                                 │
   │                                  │◀─────────────────────────────── │
   │                                  │  GET /sync/changes?since=...    │
   │                                  │                                 │
   │                                  │  Return [new transaction]       │
   │                                  │────────────────────────────────▶│
   │                                  │                                 │
   │                                  │                                 │
   │                                  │  Luz ve el gasto en su UI      │
   │                                  │  Si es split, necesita verify   │
```

---

## 10. Dependencias

### 10.1 Backend (Python)

```txt
# requirements.txt — Producción
fastapi==0.115.*
uvicorn[standard]==0.34.*
pydantic==2.10.*
pydantic-settings==2.7.*
sqlalchemy==2.0.*
aiosqlite==0.20.*          # Async SQLite
python-jose[cryptography]==3.3.*  # JWT
passlib[bcrypt]==1.7.*     # Password hashing
httpx==0.28.*              # HTTP client (AI calls)
openai==1.58.*             # OpenAI-compatible LLM client
python-multipart==0.0.*
orjson==3.10.*             # Fast JSON
apscheduler==3.10.*        # Cron tasks (insights)
python-dateutil==2.9.*
bleach==6.2.*              # Sanitize user input

# requirements-dev.txt — Desarrollo
pytest==8.*
pytest-asyncio==0.25.*
pytest-cov==6.*
ruff==0.8.*
httpx-ws==0.6.*
```

### 10.2 Frontend (Node.js)

```json
{
  "name": "flow-frontend",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "tsc --noEmit && eslint src/",
    "test": "vitest run"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0",
    "recharts": "^2.15.0",
    "date-fns": "^4.1.0",
    "idb": "^8.0.0",
    "react-hot-toast": "^2.5.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.7.0",
    "vite": "^6.0.0",
    "vite-plugin-pwa": "^0.21.0",
    "vitest": "^2.1.0",
    "eslint": "^9.0.0"
  }
}
```

### 10.3 Infraestructura

| Componente | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.12+ | Runtime backend |
| Node.js | 22+ | Build frontend |
| SQLite | 3.45+ | Base de datos |
| Ollama | Última | LLM local (opcional) |
| Coolify | 4.x | Deploy y hosting |
| Docker | 24+ | Contenedores |
| Nginx | 1.26+ | Reverse proxy frontend |

---

## 11. Estructura docs/

```
docs/
├── architecture/
│   ├── DECISIONS.md          # ADRs: porque SQLite, porque Vanilla CSS, porque async
│   ├── DATA_FLOW.md          # Diagramas de flujo detallados (ASCII)
│   ├── AI_INTEGRATION.md     # Prompt engineering, modelos, fallbacks
│   └── SECURITY.md           # Modelo de seguridad: JWT, encriptación, validación
│
├── phases/
│   ├── PHASE_001_SETUP.md    # Repo, Docker, DB, auth básico
│   ├── PHASE_002_CORE.md     # CRUD transacciones, cuentas, categorías, budgets
│   ├── PHASE_003_AI.md       # Integración IA: clasificación, insights, resúmenes
│   └── PHASE_004_POLISH.md   # PWA, offline, telemetría, tests, deploy final
│
├── qa_reports/
│   └── README.md             # Formato de reportes de QA
│   # Se poblará con cada campaña de testing:
│   # Q1_2025_unit_tests.md
│   # Q1_2025_security_audit.md
│   # etc.
│
├── deployments/
│   ├── DEPLOYMENT.md         # Manual completo de deploy en Coolify
│   └── INCIDENTS.md          # Postmortem de incidencias
│
└── AI_LOG.md                 # Bitácora continua del agente
```

---

## 12. Despliegue Coolify

### 12.1 Dockerfiles

**Backend (`backend/Dockerfile`):**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend (`frontend/Dockerfile`):**
```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.26-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 12.2 docker-compose.yml (Desarrollo Local)

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - flow_data:/data  # SQLite persistente
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///data/flow.db
      - AI_PROVIDER=ollama
      - AI_ENDPOINT=http://host.docker.internal:11434/v1
    env_file:
      - .env

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

volumes:
  flow_data:
```

### 12.3 Secretos en Infisical

```yaml
# Path: /flow
# Env: prod
FLOW_JWT_SECRET: <auto-generado>
FLOW_JWT_ALGORITHM: HS256
FLOW_JWT_EXPIRE_MINUTES: 1440
FLOW_DATABASE_PATH: /data/flow.db
FLOW_AI_PROVIDER: openai
FLOW_AI_MODEL: deepseek-v4-flash
FLOW_AI_ENDPOINT: https://api.deepseek.com/v1
FLOW_AI_API_KEY: <desde Infisical>
FLOW_CORS_ORIGINS: https://flow.casabero.com
FLOW_LOG_LEVEL: INFO
```

### 12.4 Health Check Endpoint

```python
# GET /health
# Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "ai": "available",
  "uptime_seconds": 3600
}
```

### 12.5 Pipeline de Deploy (Coolify)

Siguiendo COOLIFY_DEPLOY_STANDARD:

1. Push a `main` → GitHub Action ejecuta `ci.yml` (tests + lint)
2. Coolify detecta push → encola deploy vía `POST /api/v1/deploy?uuid=<APP_UUID>`
3. Polling de `deployment_uuid` hasta `finished|failed|canceled`
4. Verificar `docker ps` con tag del SHA esperado
5. Verificar `GET /health` → HTTP 200
6. Verificar página pública responde con HTML

---

## Apéndice A: Estándares Casabero Aplicados

| Estándar | Aplicación en Flow |
|----------|-------------------|
| **UX/UI Manifesto §1** (State Clarity) | Skeleton loaders con breathe animation en listas y cards |
| **UX/UI Manifesto §2** (Inputs) | `inputmode="numeric"` en montos, auto-focus en modal de transacción |
| **UX/UI Manifesto §3** (Paleta) | 3 colores pastel: púrpura (balance), verde (metas), naranja (alertas) |
| **UX/UI Manifesto §4** (Dark Mode) | Toggle en header, variables CSS con `--color-*-dark` |
| **UX/UI Manifesto §5** (Ayuda) | `<HelpMenu />` en header con tour interactivo |
| **UX/UI Manifesto §6** (Animación) | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` en transiciones |
| **UX/UI Manifesto §7** (Arquitectura) | Vanilla CSS, "dumb components", Card premium |
| **UX/UI Manifesto §8** (Botones) | Variables CSS exactas para light/dark mode |
| **AI_RULES §1** (Código) | Tests obligatorios, seguridad desde el diseño |
| **AI_RULES §6** (QA) | docs/qa_reports/ para toda campaña de tests |
| **AI_RULES §7** (Docs) | docs/ con architecture/, phases/, qa_reports/, deployments/ |
| **AI_RULES §9** (Data-Driven) | Telemetría de eventos desde el día 1 |
| **COOLIFY_DEPLOY** | Docker multi-stage, health check, polling de deploy |

---

## Apéndice B: Glosario

| Término | Significado |
|---------|-------------|
| Split | División de un gasto entre Joseph y Luz (ej: 50/50, 70/30) |
| Joint | Recurso compartido por la pareja (cuenta, presupuesto, meta) |
| Insight | Recomendación/alerta generada por IA o reglas de negocio |
| Liquid Glass | Estilo de animación fluida tipo vidrio líquido de Apple |
| Breathe | Efecto de opacidad pulsante en skeleton loaders |
| Dumb Component | Componente React sin estado interno ni lógica de negocio |

---

> **Documento generado por Hermes Agent — 2026-04-26**
> **Próximo paso**: Crear repo `casabero-labs/flow`, inicializar backend con FastAPI + SQLite, deploy básico en Coolify.
