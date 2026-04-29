# Fase 2 — Auth & Partnership

**Inicio**: 2026-04-28 23:00 COT  
**Estado**: En progreso 🚧  
**Agentes**: MiniMax M2.7 (ejecución), DeepSeek V4 (estrategia)

---

## Objetivo

Login/Register con sistema de pareja financiera. Dos usuarios se registran, se conectan mediante código de invitación, y comparten TODOS los datos (transacciones, cuentas, categorías, presupuestos, metas, insights).

## Estado actual del proyecto

### Backend ✅
- FastAPI + SQLAlchemy async + SQLite
- Auth: JWT (HS256), bcrypt, register/login/me funcionando
- CRUD: transactions, categories, accounts, budgets, goals
- AI: categorizer, chat, insights
- Modelo User con email, hashed_password, name
- No tiene sistema de pareja/partnership

### Frontend ✅
- React + TypeScript + Vite
- Páginas: Dashboard, Transactions, Budgets, Goals, Insights
- **Falta**: Login, Register, AuthContext, Protected Routes
- HelpMenu component existente
- Estilos globales con variables CSS

### Infra ✅
- Backend corriendo en `adt11irwuqprcupbkdgkrjei.casabero.com:8000`
- Frontend en `flow.casabero.com` (recién arreglado el ruteo)
- Sin CI/CD automático todavía
- Dockerfiles listos

---

## Estrategia de Partnership

### Modelo

```python
class Partnership(Base):
    __tablename__ = "partnerships"
    id: int (PK)
    inviter_id: int (FK → users, quien crea el código)
    invitee_id: int (FK → users, nullable, quien se une)
    invite_code: str (6 chars, unique)
    status: str ("pending" | "active" | "rejected")
    created_at: datetime
    activated_at: datetime (nullable)
```

### Flujo

1. **User A** se registra → obtiene JWT
2. **User A** genera un código de invitación (`POST /api/partnerships/invite`)
3. **User B** se registra → obtiene JWT
4. **User B** ingresa el código (`POST /api/partnerships/join`)
5. Partnership se activa → **AMBOS COMPARTEN DATOS**
6. Las queries existentes se adaptan: `WHERE user_id IN (user.id, partner.id)`

### Cambios necesarios

| Archivo | Cambio |
|---------|--------|
| `models/partnership.py` | **NUEVO** — modelo Partnership |
| `models/user.py` | Agregar relaciones a partnership |
| `api/partnership.py` | **NUEVO** — endpoints invite/join/status/leave |
| `api/deps.py` | Modificar `get_current_user` para inyectar `partnership_id` |
| `api/transactions.py` | Filtrar por partnership (user IN [self, partner]) |
| `api/accounts.py` | Idem |
| `api/categories.py` | Idem |
| `api/budgets.py` | Idem |
| `api/goals.py` | Idem |
| `api/dashboard.py` | Idem |
| `api/insights.py` | Idem |
| `api/router.py` | Agregar partnership router |
| `schemas/partnership.py` | **NUEVO** — schemas invite/join/status |
| `config.py` | Ajustar `access_token_expire_minutes` si necesario |

### Frontend — Nuevas páginas/componentes

| Archivo | Descripción |
|---------|-------------|
| `src/pages/Login.tsx` | Formulario login |
| `src/pages/Register.tsx` | Formulario register |
| `src/pages/PartnershipSetup.tsx` | Generar código / unirse con código |
| `src/contexts/AuthContext.tsx` | Contexto de autenticación |
| `src/components/ProtectedRoute.tsx` | Wrapper para rutas protegidas |
| `src/api/client.ts` | Axios/fetch wrapper con token JWT |
| `src/api/auth.ts` | Llamadas a login/register/me |
| `src/api/partnership.ts` | Llamadas a invite/join/status |

---

## Plan de ejecución (esta noche)

### Bloque 1: Backend (23:00 - 03:00)
- [ ] Crear modelo Partnership + migración
- [ ] Crear API partnership (invite, join, status)
- [ ] Modificar deps.py para inyectar partnership
- [ ] Modificar TODOS los endpoints existentes para filtrar por partnership
- [ ] Tests de partnership
- [ ] Deploy backend a Coolify

### Bloque 2: Frontend (03:00 - 06:00)
- [ ] Instalar dependencias (react-router-dom, axios)
- [ ] Crear AuthContext + ProtectedRoute
- [ ] Crear Login page
- [ ] Crear Register page
- [ ] Crear PartnershipSetup page
- [ ] Modificar App.tsx con rutas
- [ ] Conectar frontend al backend
- [ ] Deploy frontend a Coolify

### Bloque 3: Verificación (06:00 - 07:00)
- [ ] E2E manual: registrar 2 usuarios, match, ver datos compartidos
- [ ] Verificar dashboard muestra datos de ambos
- [ ] Reporte final a Casabero

---

## Notas

- **Regla**: MiniMax para TODO el desarrollo. DeepSeek SOLO para diseñar esta estrategia inicial.
- **Seguridad**: JWT con secret_key fuerte (usar Infisical para FLOW_SECRET_KEY)
- **UX**: El código de invitación se muestra en pantalla y se puede copiar. 6 caracteres alfanuméricos.
- **Limitación**: Solo 2 personas por partnership (pareja). No grupos.
