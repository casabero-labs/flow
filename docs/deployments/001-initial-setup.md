# flow — Deploy Guide

## Arquitectura

```
GitHub (master) ──push──► GitHub Actions ──build+push──► ghcr.io
                                                         │
                                          Coolify ◄─── pull imagen
                                              │
                                          flow.casabero.com (frontend)
                                          api.flow.casabero.com (backend)
```

## Setup inicial en Coolify (una sola vez)

### 1. Agregar ghcr.io como Private Registry

1. Ir a **panel.casabero.com** → Settings → **Registries**
2. Agregar nuevo registry:
   - **Name**: `ghcr`
   - **Registry URL**: `https://ghcr.io`
   - **Username**: `casabero-labs` (o tu usuario de GitHub)
   - **Password**: GitHub Personal Access Token con permisos `packages:write`

   > Para crear el token: GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens → Generar uno con `packages:write`

### 2. Crear app flow-backend

1. **Project**: `flow` (ya existe)
2. **New Application** → **Private Registry**
3. Seleccionar registry `ghcr.io`
4. **Image**: `ghcr.io/casabero-labs/casabero-labs/flow/flow-backend`
5. **Tag strategy**: `latest` + pull always
6. **Port**: `8000`
7. **Health Check**: Type `http`, Path `/health`, Port `8000`
8. **Environment Variables**:
   - `DATABASE_URL=sqlite:///./flow.db`
   - `SECRET_KEY=<generar con: python3 -c "import secrets; print(secrets.token_hex(32))">`
   - `MINIMAX_API_KEY=<del archivo ~/.hermes/.env o de Infisical>`

### 3. Crear app flow-frontend

1. **Project**: `flow` (ya existe)
2. **New Application** → **Private Registry**
3. Seleccionar registry `ghcr.io`
4. **Image**: `ghcr.io/casabero-labs/casabero-labs/flow/flow-frontend`
5. **Tag strategy**: `latest` + pull always
6. **Port**: `3000`
7. **Health Check**: Type `http`, Path `/`, Port `3000`
8. **Environment Variables**:
   - `BACKEND_URL=https://api.flow.casabero.com`

## Deploy automático (después del setup)

Cada vez que hacés push a `master`:

1. GitHub Actions buildea la imagen (backend o frontend)
2. Push a ghcr.io con tag `sha-<commit>` + `latest`
3. Coolify detecta imagen nueva → redeploya automáticamente

## Endpoints

| Servicio | URL | Props |
|---|---|---|
| Frontend | https://flow.casabero.com | Público, usa Traefik |
| Backend API | https://api.flow.casabero.com | Interno + Cloudflare |
| Health | https://api.flow.casabero.com/health | GET sin auth |

## Notas técnicas

- **Backend**: FastAPI en puerto 8000, SQLite en `/app/flow.db`
- **Frontend**: Nginx en puerto 3000, proxy `/api/` a `BACKEND_URL`
- **Auth**: JWT, tokens en headers `Authorization: Bearer <token>`
- **CORS**: Configurado para `flow.casabero.com` y `http://localhost:5173`
- **ghcr.io**: Container Registry de GitHub Packages. Las imágenes son públicas por defecto con este setup.

## Solución de problemas

### Coolify no detecta nueva imagen
Si Coolify no hace redeploy automático, hay dos opciones:

1. **Manual via API** (si la app ya está creada):
   ```bash
   curl -X POST \
     -H "Authorization: Bearer $COOLIFY_API_KEY" \
     http://192.168.1.7:8000/api/v1/applications/<uuid>/restart
   ```

2. **Manual via UI**: Entrar a panel.casabero.com → flow-backend → Redeploy

### La imagen no existe en ghcr.io
Verificar que el workflow de GitHub Actions terminó exitosamente:
- Repo → Actions → debería mostrar "Deploy Backend" o "Deploy Frontend" en verde

### Error 500 en /api/
Revisar logs del backend en Coolify (botón "Logs" en la app).
Causas comunes:
- `SECRET_KEY` no configurado
- `DATABASE_URL` mal formado
- `MINIMAX_API_KEY` faltante
