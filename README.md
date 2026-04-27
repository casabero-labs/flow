# flow — Finanzas personales para pareja

> Joseph + Luz. Clarity in every transaction. 💸

**flow** es una app de finanzas personales diseñada para que una pareja gestione sus finanzas compartidas con claridad, gráficos útiles e inteligencia artificial.

## 🚀 En desarrollo

La app está siendo construida. Seguila en: **flow.casabero.com**

## Stack

- **Backend**: FastAPI + SQLite
- **Frontend**: React 19 + Vite + Recharts
- **IA**: MiniMax API (chat, resúmenes, categorización automática)
- **Estándares**: [casabero-standards](https://github.com/casabero-labs/casabero-standards)

## Features

- 💸 Registro de ingresos y gastos con mood tracking
- 📊 Dashboard con gráficos (torta, línea, barras)
- 🎯 Metas de ahorro con progreso visual
- 💰 Presupuestos mensuales por categoría + alertas
- 💬 Chat conversacional con IA
- 📝 Resumen mensual narrativo por IA
- 🔍 Detección de patrones (ánimo ↔ gastos, anomalías)
- 🤖 Categorización automática con aprendizaje

## Docs

- [SPEC.md](./SPEC.md) — Arquitectura técnica completa
- [docs/](./docs/) — Documentación viva del proyecto

## Quick start (desarrollo local)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Deploy

Desplegado en Coolify. Ver [docs/deployments/](./docs/deployments/).

## CI/CD

Deploy automático via GitHub Actions + ghcr.io

