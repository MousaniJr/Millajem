# Millajem

Sistema personal de gestión y monitoreo de puntos de lealtad, millas y Avios. Optimizado para maximizar beneficios en programas de España, Brasil y Gibraltar.

## 🚀 Características

- **Dashboard centralizado** de todos tus saldos de puntos y millas
- **Calculadora de conversión** a Avios
- **Monitoreo automático de promociones** vía RSS y redes sociales
- **Recomendaciones personalizadas** de tarjetas y oportunidades
- **Sistema de alertas** para no perder promociones importantes
- **Gestión de fuentes** de información (blogs, Instagram, Twitter, Telegram)

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos (PostgreSQL en producción)
- **APScheduler** - Scraping automático de promociones
- **BeautifulSoup & Feedparser** - Web scraping

### Frontend
- **Next.js 14** - Framework React con App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Estilos

## 📋 Requisitos Previos

- **Python 3.9+**
- **Node.js 18+**
- **npm** o **yarn**

## 🔧 Instalación Local

### 1. Clonar el repositorio

\`\`\`bash
git clone https://github.com/MousaniJr/Millajem.git
cd Millajem
\`\`\`

### 2. Configurar Backend

\`\`\`bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales
\`\`\`

**Importante**: Edita el archivo \`.env\` y configura:
- \`SECRET_KEY\` - Una clave secreta larga y aleatoria
- \`ADMIN_USERNAME\` - Tu nombre de usuario
- \`ADMIN_PASSWORD\` - Tu contraseña segura

### 3. Configurar Frontend

\`\`\`bash
cd ../frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local
\`\`\`

### 4. Iniciar servidores

**Backend** (puerto 8000):
\`\`\`bash
cd backend
uvicorn app.main:app --reload
\`\`\`

**Frontend** (puerto 3000):
\`\`\`bash
cd frontend
npm run dev
\`\`\`

Accede a **http://localhost:3000** e inicia sesión con tus credenciales.

## 🚂 Deploy en Railway

### 1. Preparar proyecto

\`\`\`bash
# Asegúrate de que todos los cambios están commiteados
git add .
git commit -m "Preparado para deploy"
git push origin main
\`\`\`

### 2. Deploy Backend

1. Ve a [Railway.app](https://railway.app)
2. Crea nuevo proyecto → Deploy from GitHub
3. Selecciona el repositorio \`Millajem\`
4. Configura las variables de entorno:
   - \`SECRET_KEY\`
   - \`ADMIN_USERNAME\`
   - \`ADMIN_PASSWORD\`
   - \`DATABASE_URL\` (Railway lo configurará automáticamente si añades PostgreSQL)
5. Railway detectará automáticamente que es Python y lo desplegará

### 3. Deploy Frontend

1. En el mismo proyecto de Railway, añade un nuevo servicio
2. Selecciona el mismo repositorio
3. Configura:
   - Root directory: \`frontend\`
   - Build command: \`npm run build\`
   - Start command: \`npm start\`
4. Variables de entorno:
   - \`NEXT_PUBLIC_API_URL\` - URL del backend de Railway (ej: \`https://millajem-backend.up.railway.app\`)

### 4. Configurar PostgreSQL (Recomendado para producción)

1. En Railway, añade PostgreSQL al proyecto
2. Railway configurará automáticamente \`DATABASE_URL\`
3. El backend detectará y usará PostgreSQL en lugar de SQLite

## 🔐 Seguridad

- ✅ Autenticación JWT con tokens de 7 días
- ✅ Contraseñas nunca hardcodeadas en el código
- ✅ Variables de entorno para todos los secretos
- ✅ \`.env\` excluido de Git
- ✅ CORS configurado para producción
- ⚠️ **Importante**: Cambia todas las credenciales por defecto antes de desplegar

## 📂 Estructura del Proyecto

\`\`\`
Millajem/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints REST
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── services/     # Lógica de negocio
│   │   ├── auth.py       # Autenticación JWT
│   │   └── main.py       # Aplicación FastAPI
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/          # Páginas Next.js
│   │   ├── components/   # Componentes React
│   │   └── lib/          # Utilidades y API client
│   ├── package.json
│   └── .env.example
│
└── README.md
\`\`\`

## 📝 Uso

### Añadir un nuevo saldo

1. Ve a **Mis Saldos**
2. Haz clic en **Añadir Saldo**
3. Selecciona el programa o crea uno personalizado
4. Introduce los puntos y guarda

### Ver promociones

1. Ve a **Promociones**
2. Filtra por país, tipo o fuente
3. Las promociones se actualizan automáticamente cada 2 horas

### Gestionar fuentes

1. Ve a **Fuentes**
2. Activa/desactiva fuentes de información
3. Añade nuevos feeds RSS o cuentas sociales

## 🤝 Contribuciones

Este es un proyecto personal, pero si encuentras bugs o tienes sugerencias, siéntete libre de abrir un issue.

## 📄 Licencia

Uso personal - No redistribuir

## 👤 Autor

**Mousa Jr**

---

**Nota**: Este proyecto está optimizado para uso personal. Las credenciales y datos son privados y no deben compartirse.
