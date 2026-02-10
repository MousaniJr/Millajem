# 🚀 Deployment Guide - Millajem en Railway

## ✅ Estado del Deployment

**Última actualización:** Febrero 2026

- ✅ **Backend**: Desplegado y funcionando
- ✅ **Frontend**: Desplegado y funcionando
- ✅ **Autenticación**: JWT funcionando correctamente
- ✅ **Base de datos**: SQLite (funcionando)

---

## 🏗️ Arquitectura en Railway

```
┌─────────────────────────────────────┐
│         Railway Project             │
├─────────────────────────────────────┤
│                                     │
│  ┌────────────────────────────┐    │
│  │  Backend Service           │    │
│  │  - FastAPI + Python 3.9    │    │
│  │  - Dockerfile custom       │    │
│  │  - Puerto: Variable ($PORT)│    │
│  │  - URL: Railway domain     │    │
│  └────────────────────────────┘    │
│                                     │
│  ┌────────────────────────────┐    │
│  │  Frontend Service          │    │
│  │  - Next.js 14.2.35         │    │
│  │  - Nixpacks build          │    │
│  │  - Puerto: Variable ($PORT)│    │
│  │  - URL: Railway domain     │    │
│  └────────────────────────────┘    │
│                                     │
│  ┌────────────────────────────┐    │
│  │  (Opcional) PostgreSQL     │    │
│  │  - Managed by Railway      │    │
│  │  - Auto DATABASE_URL       │    │
│  └────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔧 Configuración del Backend

### Archivos clave para Railway:
- `backend/Dockerfile` - Build del contenedor Python
- `backend/start.sh` - Script de inicio que maneja $PORT
- `backend/railway.json` - Configuración de Railway
- `backend/requirements.txt` - Dependencias Python

### Variables de entorno requeridas:
```env
SECRET_KEY=tu-clave-secreta-larga-y-aleatoria
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_contraseña_segura
```

### Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x start.sh
CMD ["./start.sh"]
```

### start.sh:
```bash
#!/bin/bash
PORT=${PORT:-8000}
echo "Starting uvicorn on port $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🌐 Configuración del Frontend

### Archivos clave para Railway:
- `frontend/package.json` - Scripts npm
- `frontend/railway.json` - Configuración de Railway
- `frontend/tsconfig.json` - TypeScript config

### Variables de entorno requeridas:
```env
NEXT_PUBLIC_API_URL=https://[backend-url].up.railway.app
```

### Railway Settings:
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Start Command**: `npm start`
- **Install Command**: `npm ci`

---

## 🔐 Seguridad

### Medidas implementadas:
- ✅ JWT con tokens de 7 días
- ✅ Variables de entorno nunca en código
- ✅ `.env` excluido de Git
- ✅ CORS configurado
- ✅ Next.js actualizado a 14.2.35 (sin vulnerabilidades)
- ✅ Dependencias de autenticación: python-jose, passlib

### Generar SECRET_KEY segura:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🔄 Proceso de Deployment

### Deployment automático:
1. Hacer cambios localmente
2. Commit a Git:
   ```bash
   git add .
   git commit -m "Descripción"
   git push origin main
   ```
3. Railway detecta el push automáticamente
4. Build y deploy automático
5. ~2-3 minutos hasta estar activo

### Verificar deployment:
```bash
# Backend
curl https://[backend-url].up.railway.app/docs

# Frontend
curl https://[frontend-url].up.railway.app
```

---

## 🐛 Troubleshooting

### Build del Backend falla

**Error: pip command not found**
- ✅ Resuelto: Usar Dockerfile en lugar de Nixpacks
- Archivo: `backend/railway.json` especifica `DOCKERFILE`

**Error: PORT variable**
- ✅ Resuelto: Script `start.sh` maneja $PORT correctamente

**Error: Missing dependencies (jose, passlib)**
- ✅ Resuelto: Añadidas a `requirements.txt`

### Build del Frontend falla

**Error: Security vulnerabilities**
- ✅ Resuelto: Next.js actualizado a 14.2.35

**Error: Module not found @/lib/api**
- ✅ Resuelto: Archivos lib/ añadidos a Git (estaban en .gitignore)

**Error: TypeScript downlevelIteration**
- ✅ Resuelto: Añadido `downlevelIteration: true` en tsconfig.json

**Error: Type null not assignable**
- ✅ Resuelto: Type guards en filtros

### Runtime issues

**Login no funciona**
- Verificar `NEXT_PUBLIC_API_URL` en frontend
- Debe apuntar a URL de backend en Railway
- Debe usar `https://` no `http://`

**CORS errors**
- Backend tiene CORS configurado para todos los orígenes en desarrollo
- Para producción, actualizar en `backend/app/main.py`

---

## 📊 Monitoreo

### Logs en Railway:
1. Click en el servicio (backend o frontend)
2. Ver pestaña "Deployments"
3. Click en el deployment activo
4. Ver logs en tiempo real

### Endpoints útiles:
```bash
# Health check backend
GET /docs

# Verificar autenticación
POST /api/auth/login

# Listar programas
GET /api/programs/
```

---

## 🔄 Actualizaciones Futuras

### Para añadir PostgreSQL:
1. En Railway: + New → Database → PostgreSQL
2. Railway configura `DATABASE_URL` automáticamente
3. Backend detecta y usa PostgreSQL
4. Migrar datos de SQLite si necesario

### Para configurar dominios personalizados:
1. Railway: Settings → Domains → + Add Domain
2. Añadir CNAMEs en Cloudflare:
   - `millajem.mousani.com` → Frontend
   - `api.millajem.mousani.com` → Backend
3. Proxy status: DNS only inicialmente
4. Esperar propagación (5-30 min)

---

## 📝 Checklist de Deployment

- [x] Backend build exitoso
- [x] Frontend build exitoso
- [x] Variables de entorno configuradas
- [x] Autenticación funcionando
- [x] Login funciona con admin/password
- [x] Frontend conecta al backend
- [x] Dashboard carga correctamente
- [ ] PostgreSQL añadido (opcional)
- [ ] Dominios personalizados configurados (opcional)
- [ ] Monitoring configurado (opcional)

---

## 🆘 Soporte

**Railway Docs:** https://docs.railway.app
**Next.js Deployment:** https://nextjs.org/docs/deployment
**FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

**Issues del proyecto:** https://github.com/MousaniJr/Millajem/issues
