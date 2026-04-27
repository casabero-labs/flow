# Deployment — flow.casabero.com

**Fecha:** 2026-04-27
**Ambiente:** Coolify (192.168.1.7)
**Dominio:** flow.casabero.com

## DNS (Cloudflare)

| Subdominio | Tipo | IP | Proxy |
|---|---|---|---|
| `flow.casabero.com` | A | 190.60.62.82 | ✅ Cloudflare Proxy |
| `api.flow.casabero.com` | A | 190.60.62.82 | ✅ Cloudflare Proxy |

Creados el 2026-04-27.

## Secrets requeridos (Infisical)

En `prod /` path:

```
SECRET_KEY=<generar-256bits>
MINIMAX_API_KEY=<token-minimax>
```

## Coolify — Backend

1. New Application → `casabero-labs/flow`
2. Build Pack: Dockerfile
3. Dockerfile: `Dockerfile` (root)
4. Port: `8000`
5. Env vars:
   - `DATABASE_URL=sqlite+aiosqlite:///./flow.db`
   - `SECRET_KEY=<生成>`
   - `MINIMAX_API_KEY=<token>`
6. Deploy

## Coolify — Frontend

1. New Application → `casabero-labs/flow`
2. Build Pack: Dockerfile
3. Dockerfile: `frontend/Dockerfile`
4. Port: `3000`
5. Domain: `flow.casabero.com`
6. Nginx proxy para `/api/` → `api.flow.casabero.com:8000`

## Verificación post-deploy

```bash
# Health check
curl https://api.flow.casabero.com/health

# Expected: {"status":"ok","app":"flow"}

# Registro
curl -X POST https://api.flow.casabero.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"joseph@casabero.com","password":"...","name":"Joseph"}'

# Login
curl -X POST https://api.flow.casabero.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"joseph@casabero.com","password":"..."}'
```

## Rollback

Si algo falla: Coolify → Deploy → seleccionar commit anterior → Deploy.
