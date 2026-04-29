# flow — Finanzas personales para pareja

> Joseph + Luz. Clarity in every transaction. 💸

<div align="center">

[![CI](https://github.com/casabero-labs/flow/actions/workflows/ci.yml/badge.svg)](https://github.com/casabero-labs/flow/actions/workflows/ci.yml)
[![Deploy Backend](https://github.com/casabero-labs/flow/actions/workflows/deploy-backend.yml/badge.svg)](https://github.com/casabero-labs/flow/actions/workflows/deploy-backend.yml)
[![Deploy Frontend](https://github.com/casabero-labs/flow/actions/workflows/deploy-frontend.yml/badge.svg)](https://github.com/casabero-labs/flow/actions/workflows/deploy-frontend.yml)
[![Tests](https://img.shields.io/badge/tests-74%20✔%20100%25-brightgreen)](https://github.com/casabero-labs/flow/tree/master/backend/tests)
[![Status](https://img.shields.io/badge/status-producci%C3%B3n-8A2BE2)](https://flow.casabero.com)

</div>

**flow** es una app de finanzas personales diseñada para que una pareja gestione sus finanzas compartidas con claridad, gráficos útiles e inteligencia artificial.

## 🌐 Estado

| Servicio    | URL                              | Estado     |
|------------|----------------------------------|-----------|
| Frontend   | [flow.casabero.com](https://flow.casabero.com) | 🟢 Producción |
| Backend    | `flow.casabero.com/api/v1`       | 🟢 Producción |
| API Docs   | [flow.casabero.com/docs](https://flow.casabero.com/docs) | 🟢 Swagger UI |
| Repo       | [casabero-labs/flow](https://github.com/casabero-labs/flow) | 🟢 GitHub |

## Stack

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![React](https://img.shields.io/badge/React_19-20232A?style=flat&logo=react)
![Vite](https://img.shields.io/badge/Vite_6-646CFF?style=flat&logo=vite)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
![Coolify](https://img.shields.io/badge/Coolify-0DB7ED?style=flat)

- **Backend**: FastAPI + SQLAlchemy 2.0 async + SQLite
- **Frontend**: React 19 + Vite 6 + Recharts + react-router-dom v7
- **IA**: MiniMax API (chat, resúmenes, categorización automática)
- **Estándares**: [casabero-standards](https://github.com/casabero-labs/casabero-standards)

## Features

- 💸 Registro de ingresos y gastos con mood tracking
- 📊 Dashboard con gráficos (torta, línea, barras)
- 🎯 Metas de ahorro con progreso visual
- 💰 Presupuestos mensuales por categoría + alertas
- 👫 Sistema de pareja (partnership) con datos compartidos
- 💬 Chat conversacional con IA
- 📝 Resumen mensual narrativo por IA
- 🔍 Detección de patrones (ánimo ↔ gastos, anomalías)
- 🤖 Categorización automática con aprendizaje

## Docs

- [SPEC.md](./SPEC.md) — Arquitectura técnica completa
- [docs/architecture/README.md](./docs/architecture/README.md) — Stack y decisiones de diseño
- [docs/architecture/database.md](./docs/architecture/database.md) — Esquema de base de datos
- [docs/qa_reports/001-backend-tests.md](./docs/qa_reports/001-backend-tests.md) — Reporte de tests
- [docs/](./docs/) — Documentación viva del proyecto

## Quick start (desarrollo local)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
SECRET_KEY=dev-secret MINIMAX_API_KEY=sk-test uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
source venv/bin/activate
SECRET_KEY=test MINIMAX_API_KEY=sk-test DATABASE_URL=sqlite+aiosqlite:///:memory: python -m pytest tests/ -v
```

✅ **74 tests** — 100% passing. Ver [docs/qa_reports/001-backend-tests.md](./docs/qa_reports/001-backend-tests.md).

## Deploy

Desplegado en Coolify. Ver [docs/deployments/](./docs/deployments/).

## CI/CD

| Pipeline | Descripción |
|---------|------------|
| [CI](.github/workflows/ci.yml) | Tests backend + lint/build frontend en cada push |
| [Deploy Backend](.github/workflows/deploy-backend.yml) | Tests → Docker → ghcr.io → Coolify (master, paths: backend/) |
| [Deploy Frontend](.github/workflows/deploy-frontend.yml) | Build → Docker → ghcr.io → Coolify (master, paths: frontend/) |

Deploy automático via GitHub Actions + ghcr.io + Coolify polling.

