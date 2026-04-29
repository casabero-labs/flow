# Esquema de Base de Datos

> **Flow** — SQLite con SQLAlchemy 2.0 async.
> Documentación del esquema entidad-relación, tablas, columnas y relaciones.

---

## Diagrama ER

```
┌─────────────┐       ┌──────────────────┐       ┌──────────────────────┐
│   users     │1──N──>│    accounts       │       │   categories         │
│             │       │                  │       │                      │
│ id (PK)     │       │ id (PK)          │       │ id (PK)              │
│ email (UQ)  │       │ name             │       │ name                 │
│ hashed_pass │       │ account_type     │       │ icon (emoji)         │
│ name        │       │ currency (COP)   │       │ color (hex)          │
│ is_active   │       │ user_id (FK) ────┘       │ is_default           │
│ created_at  │       │ is_shared        │       │ user_id (FK) ────────┘
└──────┬──────┘       └──────────────────┘       └──────────┬───────────┐
       │                                                    │           │
       │1──────────────────┐                                │1          │1
       │                   │                                │           │
       │          ┌────────┴──────────┐                     │           │
       │          │   partnerships    │                     │           │
       │          │                  │                     │           │
       │          │ id (PK)          │                     │           │
       │          │ inviter_id (FK)──┼──┐                  │           │
       │          │ invitee_id (FK)──┼──┼──┐               │           │
       │          │ invite_code (UQ) │  │  │               │           │
       │          │ status           │  │  │               │           │
       │          │ created_at       │  │  │               │           │
       │          │ activated_at     │  │  │               │           │
       │          └──────────────────┘  │  │               │           │
       │                                │  │               │           │
       │1──N─────┐                      │  │               │           │
       │         │                      │  │               │           │
       │  ┌──────┴──────────┐           │  │               │           │
       │  │   transactions   │           │  │               │           │
       │  │                  │           │  │               │           │
       │  │ id (PK)          │           │  │               │           │
       │  │ type             │           │  │               │           │
       │  │ amount           │           │  │               │           │
       │  │ description      │           │  │               │           │
       │  │ payment_method   │           │  │               │           │
       │  │ category_id(FK)──┼───────────┼──┼───────────────┘           │
       │  │ account_id (FK)──┼───────────┼──┼───────────────────────┐   │
       │  │ user_id (FK) ────┼───────────┘  │                      │   │
       │  │ goal_id (FK) ────┼───────────┐   │                      │   │
       │  │ mood (enum)      │           │   │                      │   │
       │  │ is_auto_cat      │           │   │                      │   │
       │  │ ai_confidence    │           │   │                      │   │
       │  │ date             │           │   │                      │   │
       │  │ created_at       │           │   │                      │   │
       │  └──────────────────┘           │   │                      │   │
       │                                 │   │                      │   │
       │1──N─────┐                       │   │                      │   │
       │         │                       │   │                      │   │
       │  ┌──────┴──────────┐            │   │                      │   │
       │  │    budgets      │            │   │                      │   │
       │  │                 │            │   │                      │   │
       │  │ id (PK)         │            │   │                      │   │
       │  │ category_id(FK)─┼────────────┼───┘                      │   │
       │  │ user_id (FK) ───┘            │                          │   │
       │  │ month (YYYY-MM)              │                          │   │
       │  │ limit_amount                 │                          │   │
       │  │ alert_80_sent                │                          │   │
       │  │ alert_100_sent               │                          │   │
       │  │ created_at                   │                          │   │
       │  └──────────────────┘           │                          │   │
       │                                 │                          │   │
       │1──N─────┐                       │                          │   │
       │         │                       │                          │   │
       │  ┌──────┴──────────┐            │                          │   │
       │  │     goals       │            │                          │   │
       │  │                 │            │                          │   │
       │  │ id (PK)         │            │                          │   │
       │  │ name            │            │                          │   │
       │  │ emoji           │            │                          │   │
       │  │ target_amount   │            │                          │   │
       │  │ deadline        │            │                          │   │
       │  │ user_id (FK) ───┘            │                          │   │
       │  │ created_at                   │                          │   │
       │  └──────┬──────────┘            │                          │   │
       │         │1                      │                          │   │
       │         │N                      │                          │   │
       │  ┌──────┴──────────┐            │                          │   │
       │  │ goal_contrib   │            │                          │   │
       │  │                │            │                          │   │
       │  │ id (PK)        │            │                          │   │
       │  │ goal_id (FK) ──┼────────────┘                          │   │
       │  │ amount         │                                       │   │
       │  │ note           │                                       │   │
       │  │ date           │                                       │   │
       │  │ created_at     │                                       │   │
       │  └────────────────┘                                       │   │
       │                                                           │   │
       │  ┌──────────────────┐  ┌──────────────────┐               │   │
       │  │  telemetry_events│  │   insights       │               │   │
       │  │                  │  │                  │               │   │
       │  │ id (PK)          │  │ id (PK)          │               │   │
       │  │ event_type       │  │ type (enum)      │               │   │
       │  │ event_data (JSON)│  │ title            │               │   │
       │  │ user_id          │  │ description      │               │   │
       │  │ session_id       │  │ severity         │               │   │
       │  │ created_at       │  │ is_read          │               │   │
       │  └──────────────────┘  │ generated_at     │               │   │
       │                        └──────────────────┘               │   │
       │  ┌──────────────────┐                                     │   │
       │  │ monthly_summaries│                                     │   │
       │  │                  │                                     │   │
       │  │ id (PK)          │                                     │   │
       │  │ month (YYYY-MM)  │                                     │   │
       │  │ narrative (Text) │                                     │   │
       │  │ summary_data(JSON│                                     │   │
       │  │ generated_at     │                                     │   │
       │  └──────────────────┘                                     │   │
       └───────────────────────────────────────────────────────────┘
```

---

## Tablas y Columnas

### `users`

| Columna          | Tipo         | Restricciones             | Descripción                     |
|-----------------|--------------|--------------------------|---------------------------------|
| `id`            | Integer      | PK, autoincrement         | ID único del usuario             |
| `email`         | String(255)  | UNIQUE, NOT NULL, INDEX   | Email de login                   |
| `hashed_password` | String(255) | NOT NULL                  | Hash bcrypt de la contraseña     |
| `name`          | String(100)  | NOT NULL                  | Nombre visible                   |
| `is_active`     | Boolean      | DEFAULT True              | Cuenta activa/desactivada        |
| `created_at`    | DateTime     | DEFAULT utcnow            | Fecha de registro                |

**Relaciones:**
- 1:N → `accounts` (cascade delete)
- 1:N → `categories` (cascade delete)
- 1:N → `transactions` (cascade delete)
- 1:N → `budgets` (cascade delete)
- 1:N → `goals` (cascade delete)

---

### `accounts`

| Columna        | Tipo         | Restricciones              | Descripción                       |
|---------------|--------------|---------------------------|-----------------------------------|
| `id`          | Integer      | PK, autoincrement          | ID único                          |
| `name`        | String(100)  | NOT NULL                   | Nombre (Efectivo, Nequi, Banco)   |
| `account_type`| String(50)   | NOT NULL                   | `cash`, `bank`, `digital`         |
| `currency`    | String(3)    | DEFAULT "COP"              | Código ISO de moneda              |
| `user_id`     | Integer      | FK → users.id, ON DELETE CASCADE | Dueño de la cuenta          |
| `is_shared`   | Boolean      | DEFAULT False              | Compartida con la pareja           |
| `created_at`  | DateTime     | DEFAULT utcnow             |                                   |

**Relaciones:**
- N:1 → `users`
- 1:N → `transactions` (cascade delete)

---

### `categories`

| Columna      | Tipo         | Restricciones                  | Descripción                     |
|-------------|--------------|-------------------------------|---------------------------------|
| `id`        | Integer      | PK, autoincrement              | ID único                        |
| `name`      | String(100)  | NOT NULL                       | Nombre (Comida, Transporte...)  |
| `icon`      | String(10)   | DEFAULT "💰"                   | Emoji representativo            |
| `color`     | String(7)    | DEFAULT "#6B7280"              | Color hex                       |
| `is_default`| Boolean      | DEFAULT False                  | Categoría del sistema (no borrable) |
| `user_id`   | Integer|null | FK → users.id, ON DELETE CASCADE, NULLABLE | Dueño (NULL = global) |
| `created_at`| DateTime     | DEFAULT utcnow                 |                                 |

**Relaciones:**
- N:1 → `users` (nullable)
- 1:N → `transactions`
- 1:N → `budgets`

---

### `transactions`

| Columna            | Tipo            | Restricciones                       | Descripción                        |
|-------------------|-----------------|------------------------------------|-------------------------------------|
| `id`              | Integer         | PK, autoincrement                   | ID único                            |
| `type`            | Enum            | NOT NULL                            | `income` o `expense`                |
| `amount`          | Decimal         | NOT NULL                            | Monto siempre positivo              |
| `description`     | Text            | NULLABLE                            | Descripción libre                   |
| `payment_method`  | Enum            | DEFAULT "cash"                      | `cash`, `card`, `transfer`, `other` |
| `category_id`     | Integer|null    | FK → categories.id, ON DELETE SET NULL | Categoría asignada               |
| `account_id`      | Integer         | FK → accounts.id, ON DELETE CASCADE | Cuenta origen/destino               |
| `user_id`         | Integer         | FK → users.id, ON DELETE CASCADE    | Quien registró                      |
| `goal_id`         | Integer|null    | FK → goals.id, ON DELETE SET NULL   | Meta asociada (opcional)            |
| `mood`            | Enum|null       | NULLABLE                            | `happy`, `neutral`, `stressed`, `frustrated`, `anxious` |
| `is_auto_categorized` | Boolean    | DEFAULT False                       | Categorizada por IA                 |
| `ai_confidence`   | Float|null      | NULLABLE                            | Confianza de la IA (0.0 - 1.0)      |
| `date`            | DateTime        | DEFAULT utcnow                      | Fecha de la transacción             |
| `created_at`      | DateTime        | DEFAULT utcnow                      |                                   |

**Relaciones:**
- N:1 → `users`
- N:1 → `accounts`
- N:1 → `categories` (nullable)
- N:1 → `goals` (nullable)

---

### `budgets`

| Columna          | Tipo         | Restricciones                      | Descripción                    |
|-----------------|--------------|-----------------------------------|--------------------------------|
| `id`            | Integer      | PK, autoincrement                  | ID único                       |
| `category_id`   | Integer      | FK → categories.id, ON DELETE CASCADE | Categoría presupuestada     |
| `user_id`       | Integer      | FK → users.id, ON DELETE CASCADE   | Dueño del presupuesto          |
| `month`         | String(7)    | NOT NULL                           | Formato `YYYY-MM`              |
| `limit_amount`  | Decimal      | CHECK > 0                          | Límite del mes                  |
| `alert_80_sent` | Boolean      | DEFAULT False                      | Alerta de 80% ya enviada       |
| `alert_100_sent`| Boolean      | DEFAULT False                      | Alerta de 100% ya enviada      |
| `created_at`    | DateTime     | DEFAULT utcnow                     |                               |

**Restricciones:**
- `CHECK (limit_amount > 0)` — constraint `positive_limit`

**Relaciones:**
- N:1 → `users`
- N:1 → `categories`

---

### `goals`

| Columna         | Tipo         | Restricciones                    | Descripción                    |
|----------------|--------------|---------------------------------|--------------------------------|
| `id`           | Integer      | PK, autoincrement                | ID único                       |
| `name`         | String(200)  | NOT NULL                         | Nombre de la meta              |
| `emoji`        | String(10)   | DEFAULT "🎯"                     | Emoji representativo           |
| `target_amount`| Decimal      | NOT NULL                         | Meta total                     |
| `deadline`     | DateTime|null | NULLABLE                         | Fecha límite (opcional)        |
| `user_id`      | Integer      | FK → users.id, ON DELETE CASCADE | Dueño                          |
| `created_at`   | DateTime     | DEFAULT utcnow                   |                                |

**Relaciones:**
- N:1 → `users`
- 1:N → `transactions`
- 1:N → `goal_contributions` (cascade delete)

---

### `goal_contributions`

| Columna     | Tipo         | Restricciones                          | Descripción                    |
|------------|--------------|---------------------------------------|--------------------------------|
| `id`       | Integer      | PK, autoincrement                      | ID único                       |
| `goal_id`  | Integer      | FK → goals.id, ON DELETE CASCADE       | Meta a la que se contribuye    |
| `amount`   | Decimal      | NOT NULL                               | Monto de la contribución       |
| `note`     | String(255)  | NULLABLE                               | Nota opcional                  |
| `date`     | DateTime     | DEFAULT utcnow                         | Fecha de la contribución       |
| `created_at`| DateTime    | DEFAULT utcnow                         |                                |

**Relaciones:**
- N:1 → `goals`

El progreso de una meta se calcula como `SUM(goal_contributions.amount) / target_amount * 100`.

---

### `partnerships`

| Columna         | Tipo         | Restricciones                           | Descripción                        |
|----------------|--------------|----------------------------------------|------------------------------------|
| `id`           | Integer      | PK, autoincrement                       | ID único                           |
| `inviter_id`   | Integer      | FK → users.id, UNIQUE, INDEX            | Quien crea la invitación           |
| `invitee_id`   | Integer|null | FK → users.id, UNIQUE, INDEX, NULLABLE  | Quien acepta (NULL mientras pending) |
| `invite_code`  | String(6)    | UNIQUE, INDEX, NOT NULL                 | Código de 6 caracteres             |
| `status`       | String(20)   | DEFAULT "pending"                       | `pending` o `active`               |
| `created_at`   | DateTime     | DEFAULT utcnow                          |                                    |
| `activated_at` | DateTime|null | NULLABLE                                | Cuándo se activó la pareja         |

**Restricciones:**
- `UNIQUE(inviter_id)` — un usuario solo puede invitar a una persona
- `UNIQUE(invitee_id)` — un usuario solo puede ser invitado una vez
- `UNIQUE(invite_code)` — código único de 6 chars

---

### `telemetry_events`

| Columna       | Tipo         | Restricciones        | Descripción                     |
|--------------|--------------|---------------------|---------------------------------|
| `id`         | Integer      | PK, autoincrement    | ID único                        |
| `event_type` | String(100)  | NOT NULL             | `page_view`, `button_click`, etc |
| `event_data` | Text         | NOT NULL             | JSON con datos del evento       |
| `user_id`    | Integer|null | DEFAULT NULL         | Usuario (si está autenticado)   |
| `session_id` | String(100)| NULLABLE             | ID de sesión anónima            |
| `created_at` | DateTime     | DEFAULT utcnow       |                                 |

---

### `insights`

| Columna        | Tipo         | Restricciones        | Descripción                             |
|---------------|--------------|---------------------|-----------------------------------------|
| `id`          | Integer      | PK, autoincrement    | ID único                                |
| `type`        | Enum         | NOT NULL             | `mood_correlation`, `anomaly`, `goal_alert`, `budget_alert`, `spending_trend` |
| `title`       | String(255)  | NOT NULL             | Título del insight                      |
| `description` | Text         | NOT NULL             | Descripción detallada                   |
| `severity`    | String(20)   | DEFAULT "info"       | `low`, `medium`, `high`                 |
| `is_read`     | Boolean      | DEFAULT False        | Marcado como leído                      |
| `generated_at`| DateTime     | DEFAULT utcnow       |                                         |

---

### `monthly_summaries`

| Columna        | Tipo         | Restricciones        | Descripción                             |
|---------------|--------------|---------------------|-----------------------------------------|
| `id`          | Integer      | PK, autoincrement    | ID único                                |
| `month`       | String(7)    | NOT NULL             | Formato `YYYY-MM`                       |
| `narrative`   | Text         | NOT NULL             | Resumen narrativo generado por IA       |
| `summary_data`| Text         | NOT NULL             | JSON con totales, comparativas          |
| `generated_at`| DateTime     | DEFAULT utcnow       |                                         |

---

## Resumen de Relaciones

| Tabla Origen        | Tabla Destino        | Tipo | Campo FK                | On Delete       |
|--------------------|---------------------|------|------------------------|-----------------|
| accounts           | users               | N:1  | user_id                | CASCADE         |
| categories         | users               | N:1  | user_id                | CASCADE         |
| transactions       | users               | N:1  | user_id                | CASCADE         |
| transactions       | accounts            | N:1  | account_id             | CASCADE         |
| transactions       | categories          | N:1  | category_id            | SET NULL        |
| transactions       | goals               | N:1  | goal_id                | SET NULL        |
| budgets            | users               | N:1  | user_id                | CASCADE         |
| budgets            | categories          | N:1  | category_id            | CASCADE         |
| goals              | users               | N:1  | user_id                | CASCADE         |
| goal_contributions | goals               | N:1  | goal_id                | CASCADE         |
| partnerships       | users (inviter)     | N:1  | inviter_id             | — (no espec.)   |
| partnerships       | users (invitee)     | N:1  | invitee_id             | — (no espec.)   |

---

## Migraciones

Actualmente **no hay migraciones formales** con Alembic. El esquema se crea en el startup via:

```python
# backend/app/database.py
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

Para producción, se planea:

```bash
cd backend
alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head
```

Por ahora, el esquema evoluciona directamente — SQLite permite agregar columnas con `ALTER TABLE`. Para cambios mayores se implementará Alembic.
