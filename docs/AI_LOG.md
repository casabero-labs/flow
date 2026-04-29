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
- [ ] docs/architecture/

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
