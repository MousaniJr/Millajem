# Gestión de Fuentes - Millajem

**Fecha**: 9 de Febrero 2026
**Feature**: Sistema completo de gestión de fuentes de información

---

## ✅ Implementado

### Backend

1. **Modelo `Source`** (`app/models/source.py`)
   - Almacena RSS feeds y cuentas de redes sociales
   - Campos: name, source_type, country, url, is_active, priority, description
   - Estadísticas: scrape_count, alert_count, last_scraped
   - Timestamps automáticos

2. **API REST completa** (`app/api/sources.py`)
   - `GET /api/sources/` - Listar con filtros
   - `GET /api/sources/{id}` - Obtener específica
   - `POST /api/sources/` - Crear nueva
   - `PUT /api/sources/{id}` - Actualizar
   - `DELETE /api/sources/{id}` - Eliminar
   - `POST /api/sources/{id}/toggle` - Activar/Desactivar
   - `GET /api/sources/stats/summary` - Estadísticas

3. **43 fuentes inicializadas** (`app/init_sources.py`)
   - 13 RSS feeds (activos por defecto)
   - 15 Instagram (inactivos, seguimiento manual)
   - 15 Twitter/X (inactivos, seguimiento manual)
   - 0 Telegram (reservado para futuro)

### Frontend

4. **Página de gestión** (`/sources`)
   - URL: http://localhost:3000/sources
   - Dashboard con estadísticas
   - Filtros por tipo, país, estado
   - Botones Activar/Desactivar/Editar/Eliminar
   - Modal para añadir/editar fuentes
   - Link añadido en navegación principal

---

## 📊 Fuentes Inicializadas

### Total: 43 fuentes

| Categoría | Activas | Inactivas | Total |
|-----------|---------|-----------|-------|
| RSS Feeds | 13 | 0 | 13 |
| Instagram | 0 | 15 | 15 |
| Twitter/X | 0 | 15 | 15 |
| **TOTAL** | **13** | **30** | **43** |

### Por País

| País | RSS | Instagram | Twitter | Total |
|------|-----|-----------|---------|-------|
| 🇪🇸 España | 2 | 4 | 3 | 9 |
| 🇧🇷 Brasil | 5 | 5 | 4 | 14 |
| 🇬🇮 Gibraltar | 3 | 3 | 5 | 11 |
| 🌍 Internacional | 3 | 3 | 3 | 9 |
| **TOTAL** | **13** | **15** | **15** | **43** |

---

## 🎯 Cómo Usar

### Acceder a la Gestión

1. Ir a http://localhost:3000/sources
2. Ver todas las fuentes con estadísticas

### Filtrar Fuentes

**Por Tipo:**
- 📰 RSS Feed
- 📸 Instagram
- 🐦 Twitter/X
- ✈️ Telegram

**Por País:**
- 🇪🇸 España
- 🇧🇷 Brasil
- 🇬🇮 Gibraltar
- 🌍 Internacional

**Por Estado:**
- ✅ Activas (usadas en scraping)
- ❌ Inactivas (solo referencia)

### Añadir Nueva Fuente

1. Click en "➕ Añadir Fuente"
2. Rellenar formulario:
   - **Nombre**: Ej. "Nuevo Blog Viajes"
   - **Tipo**: rss_feed/instagram/twitter/telegram
   - **País**: ES/BR/GI/INT
   - **URL**: URL del feed o perfil
   - **Prioridad**: 1-10 (mayor = más importante)
   - **Descripción**: Breve descripción
   - **Estado**: Activa/Inactiva
3. Click "Crear"

### Editar Fuente

1. Click en "Editar" en cualquier fuente
2. Modificar campos necesarios
3. Click "Actualizar"

### Activar/Desactivar

- Click en "Activar" o "Desactivar"
- Las fuentes activas se usan en scraping automático
- Las inactivas son solo referencia (redes sociales)

### Eliminar Fuente

1. Click en "Eliminar"
2. Confirmar eliminación
3. La fuente se elimina permanentemente

---

## 🔍 Campos Explicados

### Información Básica

**name**: Nombre descriptivo de la fuente
```
Ejemplo: "Puntos Viajeros", "Head for Points"
```

**source_type**: Tipo de fuente
```
- rss_feed: Feed RSS de blog
- instagram: Cuenta de Instagram
- twitter: Cuenta de Twitter/X
- telegram: Canal de Telegram (futuro)
```

**country**: País/región de la fuente
```
- ES: España
- BR: Brasil
- GI: Gibraltar/UK
- INT: Internacional
```

**url**: URL del feed o perfil
```
RSS: https://blog.com/feed/
Instagram: https://instagram.com/cuenta
Twitter: https://twitter.com/cuenta
```

**website_url**: (Opcional) URL del sitio principal
```
Ejemplo: https://blog.com
```

### Configuración

**is_active**: Si está activa para scraping
```
true: Se usa en scraping automático (RSS feeds)
false: Solo referencia manual (redes sociales)
```

**priority**: Prioridad 1-10
```
10: Máxima (ej: Head for Points)
7-9: Alta (ej: Puntos Viajeros)
5-6: Media
1-4: Baja
```

**description**: Descripción breve
```
"Principal blog UK de Avios, BA e Iberia"
```

**notes**: Notas adicionales
```
"Publicar promociones solo los lunes"
```

### Estadísticas (Automáticas)

**last_scraped**: Última vez scrapeada
**scrape_count**: Veces scrapeada
**alert_count**: Alertas generadas
**created_at**: Fecha de creación
**updated_at**: Última actualización

---

## 📡 Estado Actual

### RSS Feeds (13 activos)

**España (2):**
1. Puntos Viajeros - Priority 9
2. Travel-Dealz - Priority 8

**Brasil (5):**
3. Melhores Destinos - Priority 9
4. Passageiro de Primeira - Priority 10 ⭐
5. Pontos pra Voar - Priority 9
6. Mil Milhas - Priority 7
7. Blog MaxMilhas - Priority 7

**Gibraltar/UK (3):**
8. Head for Points - Priority 10 ⭐
9. InsideFlyer UK - Priority 8
10. Turning Left for Less - Priority 8

**Internacional (3):**
11. One Mile at a Time - Priority 8
12. The Points Guy - Priority 9
13. Frequent Miler - Priority 8

### Instagram (15 inactivos)

Por defecto inactivos - seguimiento manual recomendado

### Twitter/X (15 inactivos)

Por defecto inactivos - seguimiento manual recomendado

---

## 🔄 Integración con Scraping

### RSS Feeds Activos

Los RSS feeds marcados como **activos** se usan automáticamente en:
- Scraping cada 2 horas (APScheduler)
- Endpoint `/api/promotions/scan`
- Generación de alertas

### Redes Sociales Inactivas

Instagram y Twitter están **inactivos** por defecto porque:
1. No hay APIs públicas gratuitas
2. Requieren aprobación de Meta/Twitter
3. O servicios pagados (Apify, RapidAPI)

**Solución actual**: Seguimiento manual
- Seguir cuentas directamente
- Activar notificaciones
- Revisar diariamente

---

## 🚀 Próximas Mejoras

### Scraping Automático de Redes Sociales

Para activar scraping de Instagram/Twitter necesitarías:

1. **Instagram**:
   - API oficial de Meta (requiere app aprobada)
   - O servicio como Apify ($)
   - Implementar en `social_scraper.py`

2. **Twitter/X**:
   - Twitter API v2 (free tier muy limitado)
   - O servicio como RapidAPI ($)
   - Implementar en `social_scraper.py`

3. **Telegram**:
   - Telegram Bot API (gratis)
   - Monitorear canales públicos
   - Más fácil de implementar

### Estadísticas Avanzadas

- Gráficos de scraping por fuente
- Mejor fuente por alertas generadas
- Tendencias de promociones por país
- ROI de cada fuente

### Validación Automática

- Verificar URLs funcionan
- Detectar feeds rotos
- Alertar si fuente no responde
- Auto-desactivar fuentes caídas

---

## 📝 Comandos Útiles

### Listar todas las fuentes
```bash
curl http://localhost:8000/api/sources/
```

### Filtrar RSS feeds activos
```bash
curl "http://localhost:8000/api/sources/?source_type=rss_feed&is_active=true"
```

### Estadísticas
```bash
curl http://localhost:8000/api/sources/stats/summary
```

### Crear nueva fuente (ejemplo)
```bash
curl -X POST http://localhost:8000/api/sources/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nuevo Blog",
    "source_type": "rss_feed",
    "country": "ES",
    "url": "https://nuevoblog.com/feed/",
    "is_active": true,
    "priority": 7,
    "description": "Blog nuevo de viajes"
  }'
```

### Activar/Desactivar fuente
```bash
curl -X POST http://localhost:8000/api/sources/1/toggle
```

### Eliminar fuente
```bash
curl -X DELETE http://localhost:8000/api/sources/1
```

---

## ✅ Checklist de Uso

### Setup Inicial (Ya hecho)
- ✅ Modelo Source creado
- ✅ API endpoints implementados
- ✅ Página frontend creada
- ✅ 43 fuentes inicializadas
- ✅ Link en navegación añadido

### Uso Diario
- [ ] Revisar fuentes activas semanalmente
- [ ] Añadir nuevas fuentes cuando las descubras
- [ ] Desactivar fuentes que no funcionan
- [ ] Ajustar prioridades según calidad

### Mantenimiento
- [ ] Verificar URLs no rotas mensualmente
- [ ] Evaluar ROI de cada fuente
- [ ] Considerar añadir Telegram cuando sea necesario
- [ ] Backup de fuentes antes de cambios grandes

---

## 🎊 Conclusión

El sistema de gestión de fuentes está **100% funcional** y permite:

✅ **Ver todas las fuentes** en un solo lugar
✅ **Filtrar** por tipo, país, estado
✅ **Añadir nuevas fuentes** fácilmente
✅ **Editar** fuentes existentes
✅ **Activar/Desactivar** según necesidad
✅ **Eliminar** fuentes obsoletas
✅ **Estadísticas** en tiempo real

**Total fuentes gestionadas**: 43 (13 RSS activos + 30 social referencia)

---

**Última actualización**: 9 de Febrero 2026
**Acceso**: http://localhost:3000/sources
**API Docs**: http://localhost:8000/docs#/sources
