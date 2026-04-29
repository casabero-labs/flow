# Fase 3 — Standards Compliance (Casabero Standards)

**Inicio**: 2026-04-29 07:00 COT
**Estado**: En progreso 🚧
**Agentes**: MiniMax M2.7 (ejecución), DeepSeek V4 (estrategia)
**Auditoría base**: AI_RULES.md + COOLIFY_DEPLOY_STANDARD.md + UX_UI_MANIFESTO.md

---

## Resumen de hallazgos

| Categoría | Estado |
|-----------|--------|
| UX/UI Manifesto | ✅ 100% |
| Arquitectura de código | ✅ 95% |
| Estructura docs/ | ⚠️ 60% (faltan architecture + qa_reports) |
| Tests y QA | ❌ 0% |
| CI/CD → Coolify real | ⚠️ 40% |
| Secrets/Infisical | ⚠️ 50% (defaults inseguros) |
| Data-Driven (telemetría) | ⚠️ 30% (modelo existe, sin implementar) |
| Partnership (core feature) | ❌ 0% |

---

## Bloques de trabajo

### 🔴 Bloque 1: Tests Backend (prioridad crítica)
**Archivos nuevos:**
- `backend/tests/__init__.py`
- `backend/tests/conftest.py` — fixtures: async client, test db, auth headers
- `backend/tests/test_auth.py` — register, login, token inválido, email duplicado
- `backend/tests/test_transactions.py` — CRUD, filtros, validación
- `backend/tests/test_categories.py` — CRUD
- `backend/tests/test_accounts.py` — CRUD
- `backend/tests/test_budgets.py` — CRUD, alertas
- `backend/tests/test_goals.py` — CRUD, contribuciones
- `backend/tests/test_dashboard.py` — datos agregados
- `backend/tests/test_security.py` — CORS headers, JWT expirado, SQL injection básico
- `backend/requirements-test.txt` — pytest, pytest-asyncio, httpx

**Resultado esperado**: 40+ tests pasando, reporte en `docs/qa_reports/001-backend-tests.md`

### 🔴 Bloque 2: CI/CD + Coolify Integration
**Archivos a modificar:**
- `.github/workflows/deploy-backend.yml` — agregar paso de tests, agregar POST a Coolify API con polling
- `.github/workflows/deploy-frontend.yml` — agregar paso de tests/lint
- `.github/workflows/ci.yml` — **NUEVO**: workflow de CI que corre tests sin deployar

**Unificar Dockerfiles:**
- Eliminar `./Dockerfile` raíz (redundante, CI usa `backend/Dockerfile`)
- Actualizar `docker-compose.prod.yml` para usar `backend/Dockerfile`

**Coolify webhook/deploy:**
- Investigar UUID de flow-backend y flow-frontend en Coolify
- Implementar POST `/api/v1/deploy?uuid=<UUID>` con polling
- Verificar health endpoint post-deploy

### 🟡 Bloque 3: Infisical Secrets + Seguridad
**Archivos a modificar:**
- `backend/app/config.py` — eliminar defaults inseguros, leer de Infisical
- `.env.example` — documentar variables requeridas sin valores

**Secretos a crear en Infisical:**
- `FLOW_SECRET_KEY` — token hex 32
- `FLOW_MINIMAX_API_KEY` — del .env existente
- `FLOW_DATABASE_URL` — sqlite path

**CORS fix:**
- `backend/app/main.py` — restringir `allow_origins` a `["https://flow.casabero.com", "http://localhost:5173"]`

### 🟡 Bloque 4: Documentación
**Crear:**
- `docs/architecture/README.md` — decisiones de diseño, stack, dependencias
- `docs/architecture/database.md` — esquema ER, migraciones
- `docs/qa_reports/` — directorio (se llena con Bloque 1)

**Actualizar:**
- `docs/AI_LOG.md` — registrar fase 3
- `README.md` — badges de CI, cobertura, estado

### 🟡 Bloque 5: Telemetry Implementation
**Backend:**
- `backend/app/api/telemetry.py` — `POST /api/v1/telemetry` (recibe eventos)
- Agregar a `router.py`

**Frontend:**
- `frontend/src/api/telemetry.ts` — cliente para enviar page_view, button_click
- Hook en App.tsx y páginas para rastrear navegación

### 🟡 Bloque 6: Partnership System
**Modelo:**
- `backend/app/models/partnership.py` — Partnership model
- Actualizar `models/__init__.py`

**API:**
- `backend/app/api/partnership.py` — endpoints invite, join, status, leave
- Actualizar `router.py`

**Schemas:**
- `backend/app/schemas/partnership.py`

**Modificar queries existentes:**
- `dept.py` — inyectar partnership_id
- Todos los endpoints CRUD — filtrar por household

**Frontend:**
- `src/pages/Login.tsx`
- `src/pages/Register.tsx`
- `src/pages/PartnershipSetup.tsx`
- `src/contexts/AuthContext.tsx`
- `src/components/ProtectedRoute.tsx`
- `src/api/client.ts`
- `src/api/auth.ts`
- `src/api/partnership.ts`

---

## Plan de ejecución

### Ronda 1 (paralelo — ahora)
1. **Subagente A**: Bloque 1 — Tests backend
2. **Subagente B**: Bloque 2 — CI/CD + Coolify
3. **Subagente C**: Bloque 3 — Infisical + seguridad

### Ronda 2 (paralelo — después de Ronda 1)
4. **Subagente D**: Bloque 4 — Documentación
5. **Subagente E**: Bloque 5 — Telemetry
6. **Subagente F**: Bloque 6 — Partnership (el más grande)

### Ronda 3 (verificación)
7. Correr todos los tests
8. Verificar CI/CD pasa
9. Reporte final a Casabero

---

## Criterios de salida

- [ ] 40+ tests backend pasando
- [ ] CI corre tests antes de deploy
- [ ] Deploy a Coolify verificado (health 200)
- [ ] Secretos en Infisical, sin defaults inseguros
- [ ] CORS restringido a flow.casabero.com
- [ ] docs/architecture/ creado
- [ ] docs/qa_reports/ con reporte de tests
- [ ] Telemetría funcional (endpoint + cliente)
- [ ] Partnership funcional (registro → código → match → datos compartidos)
