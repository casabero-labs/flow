# docs/

Esta carpeta sigue los estándares Casabero AI_RULES — documentación viva del proyecto.

## Estructura

```
docs/
├── AI_LOG.md              # Bitácora del agente (ideas, bloqueos, resoluciones)
├── architecture/          # Decisiones de diseño, diagramas
├── phases/               # Bitácora de avances por fase
├── qa_reports/           # Resultados de tests ejecutados
└── deployments/           # Historial de despliegues
```

---

## Fases del proyecto

### Fase 0 — Setup ✅
- [x] Crear repo GitHub ✅
- [x] Estructura backend/frontend ✅
- [x] Configurar Infisical secrets ✅ (2026-04-29)
- [x] Configurar Coolify ✅
- [x] Deploy inicial ✅

### Fase 1 — Backend mínimo ✅
- [x] Auth (JWT) ✅
- [x] CRUD transactions ✅
- [x] CRUD categories ✅
- [x] CRUD accounts ✅
- [x] Dashboard API con gráficos ✅
- [x] Tests ✅ (2026-04-29 — 74 tests pasando)

### Fase 2 — Features completos ✅
- [x] CRUD budgets con alertas ✅
- [x] CRUD goals con contribuciones ✅
- [x] AI categorizer ✅
- [x] AI chat ✅
- [x] AI insights ✅
- [x] Monthly summary narrativo ✅
- [x] Partnership system ✅ (2026-04-29)

### Fase 3 — Standards Compliance ✅ (2026-04-29)
- [x] Tests backend (74 tests, 100% pass) ✅
- [x] CI/CD con tests + Coolify polling ✅
- [x] Secretos en Infisical ✅
- [x] CORS restringido ✅
- [x] Dockerfiles unificados ✅

### Fase 4 — UX premium ✅
- [x] Animaciones liquid glass ✅
- [x] Skeleton loaders ✅
- [x] Help menu ✅
- [x] Dark/light mode ✅
- [x] Touch-optimized ✅

### Fase 5 — Deploy producción ✅
- [x] Docker build ✅
- [x] Coolify setup ✅
- [x] Dominio flow.casabero.com ✅
- [x] Health check ✅
- [ ] QA tests completos (pendiente: frontend tests)

---

## Próximos pasos

- [ ] Tests frontend (Playwright + Vitest)
- [ ] Frontend: Login, Register, PartnershipSetup pages
- [ ] Frontend: AuthContext + ProtectedRoute
- [ ] End-to-end test (registro → partnership → datos compartidos)

---

## Log del agente

### 2026-04-29 07:00 — Standards Compliance Audit
- Auditoría completa de Flow vs casabero-standards
- 74 tests backend creados y pasando (100%)
- CI/CD integrado con Coolify (deploy + polling)
- Secretos migrados a Infisical (FLOW_SECRET_KEY, FLOW_MINIMAX_API_KEY, FLOW_DATABASE_URL)
- CORS restringido a flow.casabero.com
- Dockerfiles unificados (eliminado ./Dockerfile duplicado)
- Partnership model + API + queries compartidas implementado
- Bugs arreglados: orden de operaciones en cálculos %, .scalar() faltante en queries
- 3 subagentes MiniMax trabajando en paralelo

### 2026-04-29 08:00 — Fase 3 completada: Documentación de arquitectura y QA

**Fase 3: Standards Compliance — COMPLETA ✅**

Lo que se hizo:
- **docs/architecture/README.md** 🆕 — Stack overview (FastAPI + React 19 + Vite + SQLite), decisiones de diseño documentadas (SQLite para simpleza, async SQLAlchemy, JWT auth, partnership model, CORS restringido, Infisical), dependencias principales, estructura completa del proyecto con jerarquía de backend/frontend/docs.
- **docs/architecture/database.md** 🆕 — Diagrama ER descriptivo de las 11 tablas (users, accounts, categories, transactions, budgets, goals, goal_contributions, partnerships, telemetry_events, insights, monthly_summaries), columnas detalladas con tipos y restricciones, relaciones N:1, resumen de migraciones y plan para Alembic.
- **docs/qa_reports/001-backend-tests.md** 🆕 — Reporte completo: 74 tests pasando 100%, cobertura por módulo (auth 10, accounts 8, transactions 15, budgets 9, goals 9, categories 8, dashboard 4, security 9, main 2), herramientas (pytest + httpx + ASGITransport + asyncio), fixture setup detallado con conftest.py explicado.
- **README.md** actualizado — Badges de CI/CD (CI, Deploy Backend, Deploy Frontend, tests 74✔, status producción), tabla de estado de servicios, badges de stack, sección de tests, tabla de pipelines CI/CD, enlaces a nueva documentación.
- **docs/AI_LOG.md** — Bitácora actualizada con esta sesión.

CI/CD confirmado:
- `ci.yml`: Backend tests + frontend lint/build en cada push
- `deploy-backend.yml`: Tests → Docker build → ghcr.io → Coolify (master, paths: backend/)
- `deploy-frontend.yml`: Build → Docker → ghcr.io → Coolify (master, paths: frontend/)
- Dominio: flow.casabero.com 🟢 producción
