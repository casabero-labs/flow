# Arquitectura de Flow

> **Flow** — app de finanzas personales para pareja (Joseph + Luz).
> Documentación de arquitectura, decisiones de diseño y estructura del proyecto.

---

## Stack Overview

| Capa      | Tecnología                                      |
| --------- | ----------------------------------------------- |
| Backend   | **FastAPI** + **SQLAlchemy 2.0** (async)        |
| Base de datos | **SQLite** via `aiosqlite`                     |
| Frontend  | **React 19** + **Vite 6** + **Recharts**        |
| Router    | **react-router-dom v7**                         |
| HTTP      | **Axios**                                       |
| IA        | **MiniMax API** (chat, resúmenes, categorización) |
| Auth      | **JWT** (python-jose) + **bcrypt** (passlib)    |
| Despliegue | **Docker** + **Coolify** + **ghcr.io**          |
| CI/CD     | **GitHub Actions**                              |
| Secretos  | **Infisical** (self-hosted)                     |

---

## Decisiones de Diseño

### SQLite para simpleza

Elegimos SQLite en lugar de PostgreSQL porque:
- **Zero configuración**: no requiere servidor de base de datos externo.
- **Suficiente para el alcance**: la app es para una pareja, no millones de usuarios.
- **Portabilidad**: el archivo `.db` se respalda fácilmente.
- **Rendimiento**: con el tamaño de datos esperado, SQLite es más que suficiente.
- Migración futura a PostgreSQL posible via SQLAlchemy (cambiar URL nomás).

Se usa `aiosqlite` para operaciones asíncronas sin bloquear el event loop.

### Async SQLAlchemy

Toda la capa de datos usa `AsyncSession` con `async_sessionmaker`. Esto permite:
- Consultas concurrentes sin bloqueo.
- Mejor rendimiento bajo el modelo async de FastAPI.
- Fixtures de test con SQLite en memoria.

### JWT Auth

- Tokens JWT con algoritmo HS256.
- Expiración: 7 días (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).
- Contraseñas hasheadas con bcrypt via passlib.
- Dependencia `get_current_user` para proteger rutas.
- Sin sesiones server-side — stateless.

### Partnership Model

El modelo de pareja es único:
- `inviter_id` + `invite_code` (6 caracteres alfanuméricos) para invitar.
- `invitee_id` se asigna cuando el invitado acepta.
- `status`: `pending` → `active`.
- Restricción `UNIQUE` en `inviter_id` e `invitee_id`: una pareja activa por usuario.
- Las queries compartidas filtran por partnership: si estás en partnership activo, ves tus datos + los de tu pareja en dashboard y consultas.

### CORS Restringido

```python
allow_origins = [
    "https://flow.casabero.com",
    "http://localhost:5173",
]
```

Solo orígenes conocidos — no hay `allow_origins=["*"]`.

### Secretos en Infisical

- `FLOW_SECRET_KEY`, `FLOW_MINIMAX_API_KEY`, `FLOW_DATABASE_URL` desde Infisical.
- Prefijo `FLOW_` para namespace.
- Inyectados via `infisical run` en producción.

---

## Dependencias Principales

### Backend (`requirements.txt`)

| Dependencia | Versión | Propósito |
|------------|---------|-----------|
| fastapi | >=0.115.0 | Framework web |
| uvicorn | >=0.30.0 | Servidor ASGI |
| sqlalchemy | >=2.0.0 | ORM async |
| aiosqlite | >=0.20.0 | Driver SQLite async |
| alembic | >=1.13.0 | Migraciones (futuro) |
| python-jose | >=3.3.0 | JWT |
| passlib[bcrypt] | >=1.7.4 | Hashing de contraseñas |
| httpx | >=0.27.0 | Cliente HTTP para MiniMax |
| pydantic-settings | >=2.5.0 | Config desde env vars |

### Frontend (`package.json`)

| Dependencia | Versión | Propósito |
|------------|---------|-----------|
| react | ^19.0.0 | UI framework |
| react-router-dom | ^7.14.2 | Routing SPA |
| recharts | ^2.15.0 | Gráficos (torta, línea, barras) |
| axios | ^1.15.2 | HTTP client |
| date-fns | ^4.0.0 | Manejo de fechas |
| vite | ^6.0.0 | Build tool |

---

## Estructura del Proyecto

```
flow/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── accounts.py        # CRUD cuentas
│   │   │   ├── auth.py            # register, login, /me
│   │   │   ├── budgets.py         # CRUD presupuestos + alertas
│   │   │   ├── categories.py      # CRUD categorías + defaults
│   │   │   ├── chat.py            # Chat con IA
│   │   │   ├── dashboard.py       # Dashboard agregado
│   │   │   ├── deps.py            # Dependencias (auth, db)
│   │   │   ├── goals.py           # CRUD metas + contribuciones
│   │   │   ├── insights.py        # Insights IA
│   │   │   ├── partnership.py     # Sistema de pareja
│   │   │   ├── router.py          # Router principal
│   │   │   ├── telemetry.py       # Telemetría
│   │   │   └── transactions.py    # CRUD transacciones
│   │   ├── models/
│   │   │   ├── user.py            # User model
│   │   │   ├── account.py         # Account model
│   │   │   ├── category.py        # Category model
│   │   │   ├── transaction.py     # Transaction model (types, mood, payment)
│   │   │   ├── budget.py          # Budget model (con alertas)
│   │   │   ├── goal.py            # Goal model
│   │   │   ├── goal_contribution.py # GoalContribution model
│   │   │   ├── partnership.py     # Partnership model
│   │   │   ├── insight.py         # Insight model (IA)
│   │   │   ├── monthly_summary.py # MonthlySummary model
│   │   │   ├── telemetry.py       # TelemetryEvent model
│   │   │   └── __init__.py        # Re-exporta todos los modelos
│   │   ├── schemas/               # Pydantic models (request/response)
│   │   ├── services/
│   │   │   ├── auth_service.py    # Lógica de auth
│   │   │   ├── ai_categorizer.py  # Categorización con IA
│   │   │   └── ai_chat.py         # Chat con MiniMax
│   │   ├── config.py              # Settings via pydantic-settings
│   │   ├── database.py            # Engine + session async
│   │   └── main.py                # FastAPI app entry point
│   ├── tests/
│   │   ├── conftest.py            # Fixtures (SQLite en memoria, auth headers)
│   │   ├── test_accounts.py       # 8 tests
│   │   ├── test_auth.py           # 10 tests
│   │   ├── test_budgets.py        # 9 tests
│   │   ├── test_categories.py     # 8 tests
│   │   ├── test_dashboard.py      # 4 tests
│   │   ├── test_goals.py          # 9 tests
│   │   ├── test_main.py           # 2 tests
│   │   ├── test_security.py       # 9 tests
│   │   └── test_transactions.py   # 15 tests
│   ├── requirements.txt           # Producción
│   ├── requirements-test.txt      # Tests
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # Root component
│   │   ├── main.tsx               # Entry point
│   │   └── vite-env.d.ts
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── nginx.conf                 # Nginx para SPA routing
│   └── Dockerfile
├── docs/
│   ├── AI_LOG.md                  # Bitácora del agente
│   ├── architecture/
│   │   ├── README.md              ← Este archivo
│   │   └── database.md            # Esquema ER detallado
│   ├── phases/                    # Bitácora por fase
│   ├── qa_reports/                # Reportes de tests
│   └── deployments/               # Historial de deploys
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI: tests backend + lint/build frontend
│       ├── deploy-backend.yml     # Deploy backend → Coolify
│       └── deploy-frontend.yml    # Deploy frontend → Coolify
├── docker-compose.yml             # Desarrollo local
├── docker-compose.prod.yml        # Producción
└── README.md
```
