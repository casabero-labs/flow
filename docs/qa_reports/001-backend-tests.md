# QA Report 001 — Backend Tests

> **Fecha**: 2026-04-29
> **Proyecto**: Flow (casabero-labs/flow)
> **Estado**: ✅ 74 tests pasando — 100%

---

## Resumen

| Métrica               | Valor       |
|----------------------|------------|
| Total tests           | 74         |
| Pasados               | 74         |
| Fallidos              | 0          |
| Cobertura de módulos  | 9 archivos |
| Duración              | ~27s       |
| Database              | SQLite :memory: |
| Python               | 3.11       |

---

## Cobertura por Módulo

| Módulo          | Tests | Archivo                | Escenarios cubiertos                                |
|-----------------|-------|------------------------|-----------------------------------------------------|
| Auth            | 10    | `test_auth.py`         | register (ok, no password, email inválido, duplicado), login (ok, wrong pass, nonexistent), /me (with token, without, invalid) |
| Accounts        | 8     | `test_accounts.py`     | CRUD (cash, bank, digital), list (empty, with data), delete (own, not found, other user's) |
| Transactions    | 15    | `test_transactions.py` | Create (income, expense, sin auth, invalid type), list (empty, with data, filter by category), get (ok, not found), update (ok, not found), delete (ok, not found), summary (empty, with data) |
| Budgets         | 9     | `test_budgets.py`      | Create, list (empty, with data, filter month), alerts (below 80%, at 80%, at 100%), delete (ok, not found) |
| Goals           | 9     | `test_goals.py`        | Create (basic, with deadline), list (empty, with progress), contribute (increments, not found), delete (own, not found, other user's) |
| Categories      | 8     | `test_categories.py`   | List (defaults created, without auth), create (full, minimal), delete (own, default fails, nonexistent, other user's) |
| Dashboard       | 4     | `test_dashboard.py`    | Empty (ceros, structure), with transactions (income, expense, balance), without auth, monthly_trend structure |
| Security        | 9     | `test_security.py`     | SQL injection (email, name), JWT (expired, tampered, wrong secret), CORS (headers present, allow origins), XSS (description, category name) |
| Main            | 2     | `test_main.py`         | Health endpoint, app title                         |

**Total**: 9 módulos, 74 tests.

---

## Herramientas

| Herramienta    | Propósito                         |
|---------------|-----------------------------------|
| **pytest**    | Test runner (v8+)                 |
| **pytest-asyncio** | Soporte async para tests     |
| **httpx**     | Cliente HTTP async (`AsyncClient`) |
| **ASGITransport** | Transporte directo ASGI sin HTTP real |
| **SQLite :memory:** | Base de datos temporal por test |

---

## Fixture Setup

Las fixtures están definidas en `backend/tests/conftest.py`:

### `event_loop` (session scope)
- Crea un event loop para toda la sesión de tests.
- Se cierra al finalizar la sesión.

### `setup_database` (autouse)
- **Antes de cada test**: crea todas las tablas en SQLite `:memory:`.
- **Después de cada test**: dropea todas las tablas.
- Garantiza estado limpio y aislado entre tests.

### `db_session`
- Retorna una `AsyncSession` directa para operaciones con la BD en tests.
- Útil para tests que necesitan acceso directo al session de SQLAlchemy.

### `async_client`
- Cliente HTTP asíncrono montado sobre la app FastAPI real.
- Usa `app.dependency_overrides[get_db]` para inyectar la sesión de test en lugar de la real.
- Transporte: `ASGITransport(app=app)` — no abre sockets reales.
- Base URL: `http://test`.

### `auth_headers`
- Registra un usuario de test (`test@example.com` / `***`).
- Hace login y retorna `{"Authorization": "Bearer <token>"}`.
- Usado en tests que requieren autenticación.

### `second_user_headers`
- Igual que `auth_headers` pero con un segundo usuario (`luz@example.com` / `***`).
- Útil para tests de permisos, partnership, y aislamiento entre usuarios.

---

## Cómo ejecutar los tests

```bash
cd backend
source venv/bin/activate

# Con variables de test directamente
SECRET_KEY=test-secret MINIMAX_API_KEY=sk-test DATABASE_URL=sqlite+aiosqlite:///:memory: python -m pytest tests/ -v

# Con Infisical (producción — cuidado con la DB real)
infisical run --env=prod -- python -m pytest tests/ -v

# Solo un módulo
python -m pytest tests/test_auth.py -v

# Con cobertura
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=term-missing
```
