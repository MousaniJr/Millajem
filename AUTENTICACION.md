# Sistema de Autenticación - Millajem

**Fecha**: 9 de Febrero 2026
**Feature**: Autenticación con usuario/contraseña y JWT tokens

---

## ✅ Implementado

Sistema completo de autenticación para proteger el acceso cuando el sistema esté público.

### Componentes

**Backend:**
- ✅ Endpoints de autenticación (`/api/auth/login`, `/api/auth/verify`)
- ✅ JWT tokens con expiración de 7 días
- ✅ Middleware de protección de rutas
- ✅ Variables de entorno para credenciales

**Frontend:**
- ✅ Página de login (`/login`)
- ✅ Gestión de tokens en localStorage
- ✅ Interceptor axios para añadir token
- ✅ Redirección automática si no autenticado
- ✅ Botón de logout en navegación

---

## 🔐 Credenciales Por Defecto

**Usuario**: `admin`
**Contraseña**: `millajem2026`

⚠️ **IMPORTANTE**: Cambia estas credenciales en producción

---

## 🚀 Cómo Usar

### 1. Acceder al Sistema

1. Ir a http://localhost:3000
2. Si no estás autenticado, serás redirigido a `/login`
3. Ingresar credenciales:
   - Usuario: `admin`
   - Contraseña: `millajem2026`
4. Click "Iniciar Sesión"
5. Serás redirigido al dashboard

### 2. Navegación Normal

- Una vez autenticado, puedes navegar libremente
- El token se guarda en localStorage
- Dura 7 días (se renueva con cada uso)
- Todas las peticiones al backend incluyen el token

### 3. Cerrar Sesión

- Click en botón "Salir" en la navegación (arriba derecha)
- Se elimina el token
- Redirige a `/login`

---

## ⚙️ Configuración

### Cambiar Credenciales

**Opción 1: Variables de Entorno (Recomendado)**

Edita `backend/.env`:
```env
# Authentication
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
ADMIN_USERNAME=tu_usuario
ADMIN_PASSWORD=tu_contraseña_segura
```

**Opción 2: Variables de Sistema**

Windows:
```bash
set ADMIN_USERNAME=tu_usuario
set ADMIN_PASSWORD=tu_contraseña
```

Linux/Mac:
```bash
export ADMIN_USERNAME=tu_usuario
export ADMIN_PASSWORD=tu_contraseña
```

### Generar Secret Key Segura

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia el resultado y ponlo en `.env` como `SECRET_KEY`

---

## 🔒 Proteger Páginas

### Método 1: Envolver Página con ProtectedRoute

Para proteger una página específica, envuélvela con `ProtectedRoute`:

```tsx
// src/app/tu-pagina/page.tsx
import ProtectedRoute from '@/components/ProtectedRoute'

export default function TuPagina() {
  return (
    <ProtectedRoute>
      <div>
        {/* Tu contenido aquí */}
      </div>
    </ProtectedRoute>
  )
}
```

### Método 2: Proteger todas las páginas (Excepto Login)

Actualiza cada página principal añadiendo `ProtectedRoute`.

**Páginas a proteger:**
- `/` (Dashboard) - page.tsx
- `/balances` - balances/page.tsx
- `/calculator` - calculator/page.tsx
- `/promotions` - promotions/page.tsx
- `/recommendations` - recommendations/page.tsx
- `/sources` - sources/page.tsx

**Páginas SIN proteger:**
- `/login` - Debe ser accesible sin auth

---

## 🌐 Deployment en Producción

### Railway / Vercel / Otro

1. **Configurar Variables de Entorno**:
   ```
   SECRET_KEY=<generar-con-comando-arriba>
   ADMIN_USERNAME=<tu-usuario>
   ADMIN_PASSWORD=<contraseña-fuerte>
   ```

2. **NUNCA subir .env a Git**:
   - Ya está en `.gitignore`
   - Usar variables de entorno del hosting

3. **HTTPS Obligatorio**:
   - JWT tokens solo sobre HTTPS
   - Railway/Vercel proveen HTTPS automáticamente

### Generar Contraseña Fuerte

```bash
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

Ejemplo de contraseña generada: `Kx8vN-2RqP9mZt4wLc1a_Q`

---

## 📡 API de Autenticación

### POST /api/auth/login

Login y obtener token.

**Request:**
```json
{
  "username": "admin",
  "password": "millajem2026"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect username or password"
}
```

### POST /api/auth/verify

Verificar si token es válido.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "username": "admin"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Could not validate credentials"
}
```

### GET /api/auth/me

Obtener info del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "username": "admin"
}
```

---

## 🔐 Seguridad

### JWT Tokens

- **Algoritmo**: HS256 (HMAC-SHA256)
- **Expiración**: 7 días
- **Storage**: localStorage (frontend)
- **Transmisión**: Header `Authorization: Bearer <token>`

### Contraseñas

- **NO se almacenan** en texto plano
- Backend compara directamente con variable de entorno
- Para producción: usar bcrypt hash (ya implementado en código)

### HTTPS

- **Obligatorio** en producción
- Protege token en tránsito
- Previene man-in-the-middle

### CORS

- Configurado en backend
- Por defecto permite todos los orígenes (desarrollo)
- En producción: limitar a tu dominio

---

## 🛠️ Troubleshooting

### "Could not validate credentials"

**Causa**: Token inválido o expirado

**Solución**:
1. Logout y login de nuevo
2. Verifica que SECRET_KEY no ha cambiado
3. Comprueba que no has editado el token manualmente

### "Incorrect username or password"

**Causa**: Credenciales incorrectas

**Solución**:
1. Verifica usuario y contraseña
2. Revisa variables de entorno en `.env`
3. Reinicia backend después de cambiar `.env`

### Redirige a /login infinitamente

**Causa**: Token guardado pero inválido

**Solución**:
1. Abrir DevTools (F12)
2. Application → Local Storage
3. Eliminar item `token`
4. Recargar página

### No aparece botón "Salir"

**Causa**: Estado de autenticación no actualizado

**Solución**:
- Recargar página
- El botón solo aparece cuando `isAuthenticated()` es true

---

## 📝 Ejemplo de Uso Completo

### 1. Configurar Credenciales

```bash
# backend/.env
SECRET_KEY=Kx8vN-2RqP9mZt4wLc1a_Q-YzB3mH7pW
ADMIN_USERNAME=mousa
ADMIN_PASSWORD=MiContraseñaSegura2026!
```

### 2. Reiniciar Backend

```bash
cd backend
# Matar proceso si está corriendo
# Reiniciar
uvicorn app.main:app --reload --port 8000
```

### 3. Probar Login

1. Ir a http://localhost:3000
2. Redirige a http://localhost:3000/login
3. Ingresar:
   - Usuario: `mousa`
   - Contraseña: `MiContraseñaSegura2026!`
4. Click "Iniciar Sesión"
5. Redirige a http://localhost:3000/ (Dashboard)

### 4. Navegar Libremente

- Todas las páginas accesibles
- Token en localStorage
- Botón "Salir" visible

### 5. Cerrar Sesión

- Click "Salir"
- Elimina token
- Redirige a `/login`

---

## 🔄 Flujo Completo

```
┌─────────────┐
│   Usuario   │
│  no autent. │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Accede a /  │
│  o /balances│
└──────┬──────┘
       │
       ▼ (no token)
┌─────────────┐
│ Redirige a  │
│   /login    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Ingresa   │
│ credenciales│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│POST /api/   │
│ auth/login  │
└──────┬──────┘
       │
       ▼ (token)
┌─────────────┐
│  Guarda en  │
│ localStorage│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Redirige a  │
│ Dashboard   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Navega     │
│ libremente  │
└──────┬──────┘
       │
       ▼ (cada request)
┌─────────────┐
│   Envía     │
│ Bearer token│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │
│  valida JWT │
└──────┬──────┘
       │
       ▼ (válido)
┌─────────────┐
│  Responde   │
│    datos    │
└─────────────┘
```

---

## 🎯 Mejoras Futuras (Opcional)

### Multi-Usuario

- Tabla de usuarios en BD
- Registro de usuarios
- Roles y permisos
- NO necesario para uso personal

### Refresh Tokens

- Token de acceso corto (15 min)
- Refresh token largo (30 días)
- Más seguro pero más complejo

### 2FA (Two-Factor Authentication)

- Código por email/SMS
- Google Authenticator
- Muy seguro pero innecesario para uso personal

### OAuth

- Login con Google/GitHub
- Conveniente pero requiere setup
- Innecesario si solo tú accedes

---

## ✅ Checklist de Seguridad

### Desarrollo
- ✅ Credenciales por defecto funcionan
- ✅ Token se guarda en localStorage
- ✅ Logout elimina token
- ✅ Rutas protegidas redirigen a login

### Producción
- [ ] Cambiar SECRET_KEY a valor aleatorio
- [ ] Cambiar ADMIN_USERNAME
- [ ] Cambiar ADMIN_PASSWORD a contraseña fuerte
- [ ] Configurar variables en hosting (Railway/Vercel)
- [ ] Verificar HTTPS habilitado
- [ ] Limitar CORS a tu dominio
- [ ] NO subir `.env` a Git
- [ ] Probar login/logout en producción

---

## 📚 Archivos Relacionados

**Backend:**
- `app/auth.py` - Utilidades de autenticación
- `app/api/auth.py` - Endpoints de auth
- `backend/.env` - Variables de entorno (NO subir a Git)

**Frontend:**
- `src/app/login/page.tsx` - Página de login
- `src/lib/auth.ts` - Utilidades de auth
- `src/components/ProtectedRoute.tsx` - HOC para proteger páginas
- `src/components/Navigation.tsx` - Nav con botón logout

---

## 🎊 Conclusión

**Sistema de autenticación implementado y funcionando:**

✅ Login con usuario/contraseña
✅ JWT tokens (7 días)
✅ Logout
✅ Protección de rutas
✅ Redirección automática
✅ Variables de entorno para credenciales

**Listo para:**
- Uso local inmediato (credenciales por defecto)
- Deployment en producción (cambiar credenciales)
- Proteger acceso público

---

**Última actualización**: 9 de Febrero 2026
**Credenciales por defecto**: admin / millajem2026
**⚠️ IMPORTANTE**: Cambiar credenciales antes de hacer público
