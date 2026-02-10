# Sistema de Monitoreo de Promociones - Millajem

## ✅ Implementado (9 de Febrero 2026)

### Funcionalidades

#### 1. Scraper RSS Automático
- **Scraping de blogs** de viajes españoles, portugueses y brasileños
- **Fuentes activas**:
  - 🇪🇸 España: Puntos Viajeros, Travel-Dealz
  - 🇧🇷 Brasil: Passageiro de Primeira, Pontos pra Voar, Melhores Destinos

#### 2. Detección Inteligente de Promociones
- **Palabras clave** detectadas automáticamente:
  - Bonus, bonificación, bónus
  - Avios, Iberia, British Airways, Vueling
  - Transferencia, conversión
  - Livelo, Esfera, Smiles
  - American Express, Membership Rewards
  - Error fare, precio error

#### 3. Sistema de Puntuación de Relevancia
- **Scoring automático** (0-100 puntos):
  - Avios: +30 puntos
  - Bonus: +25 puntos
  - Transferencia: +20 puntos
  - Livelo/Esfera: +20 puntos
  - Error Fare: +35 puntos (muy relevante)
  - Multiple keywords: +10 puntos bonus

#### 4. Clasificación Automática
- **Tipos de alerta**:
  - 🔄 **Bonus Transferencia**: Bonus en transferencia de puntos
  - 💰 **Bonus Compra**: Descuento en compra de puntos
  - 🎯 **Promoción**: Ofertas generales
  - ✈️ **Error Fare**: Tarifas error (muy urgentes)
  - ℹ️ **Info General**: Información relevante

- **Prioridades**:
  - 🔴 **Urgent** (score ≥90): Requiere acción inmediata
  - 🟠 **High** (score ≥70): Muy relevante
  - 🔵 **Normal** (score 40-69): Interesante
  - ⚪ **Low** (score <40): Informativo

#### 5. Monitoreo Automático
- **Scheduler (APScheduler)**: Escanea cada 2 horas automáticamente
- **Anti-duplicados**: No repite alertas en 48 horas
- **Filtrado**: Solo guarda promociones con relevancia ≥50

## 🎯 Promociones Detectadas (Ejemplo Real)

### Encontradas en el primer escaneo:

1. **🟠 Azul Fidelidade + Esfera: hasta 100% bonus**
   - País: 🇧🇷 Brasil
   - Tipo: Bonus Transferencia
   - Programa: Esfera
   - Prioridad: HIGH

2. **🟠 Esfera: hasta 5 puntos por real en Casas Bahia**
   - País: 🇧🇷 Brasil
   - Tipo: Promoción
   - Programa: Esfera
   - Prioridad: HIGH

3. **🟠 Hasta 52% descuento en compra de puntos Esfera**
   - País: 🇧🇷 Brasil
   - Tipo: Bonus Compra
   - Programa: Esfera
   - Prioridad: HIGH
   - **Precio**: Milheiro a R$ 33,60

4. **🔵 TAP: Salvador €493, Natal & Fortaleza €587**
   - País: 🇪🇸 España → 🇧🇷 Brasil
   - Tipo: Error Fare / Promoción
   - Prioridad: NORMAL

5. **🔵 Smiles: 20,000 millas bonus en Clube Smiles 2.000**
   - País: 🇧🇷 Brasil
   - Tipo: Bonus
   - Programa: Smiles
   - Prioridad: NORMAL

## 📡 API Endpoints

### Alertas
```
GET /api/alerts/ - Listar alertas (con filtros)
  ?unread_only=true - Solo no leídas
  ?country=ES - Filtrar por país
  ?alert_type=bonus_transfer - Filtrar por tipo

GET /api/alerts/{id} - Ver alerta específica
PATCH /api/alerts/{id}/read - Marcar como leída
PATCH /api/alerts/{id}/favorite - Alternar favorito
DELETE /api/alerts/{id} - Eliminar alerta
GET /api/alerts/stats/summary - Estadísticas
```

### Promociones
```
POST /api/promotions/scan?min_relevance=50 - Escanear manualmente
POST /api/promotions/scan/{feed_name} - Escanear feed específico
GET /api/promotions/feeds - Listar feeds disponibles
GET /api/promotions/top?limit=10&country=BR - Top promociones
```

## 🖥️ Frontend

### Nueva Página: `/promotions`

**Características**:
- Lista de todas las promociones detectadas
- Filtros por país (ES, BR, INT) y tipo
- Botón "Escanear Ahora" para búsqueda manual
- Marcar como favorito ⭐
- Marcar como leída ✓
- Links directos a la oferta completa
- Indicadores visuales de prioridad
- Banderas por país 🇪🇸 🇧🇷 🌍

**UI**:
- Tarjetas con borde de color según prioridad
- Opacidad reducida para leídas
- Badges de tipo, prioridad y programa relacionado
- Fecha y hora de detección

## 🤖 Monitoreo Automático

### Configuración Actual
- **Frecuencia**: Cada 2 horas
- **Horarios**: 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00
- **Relevancia mínima**: 50 puntos
- **Anti-spam**: 48 horas

### Cómo funciona
1. Scheduler se inicia automáticamente con el backend
2. Cada 2 horas ejecuta el escaneo
3. Lee los feeds RSS de todos los blogs
4. Analiza cada entrada con IA de keywords
5. Calcula score de relevancia
6. Filtra por umbral mínimo (50)
7. Verifica duplicados
8. Guarda nuevas alertas en la base de datos
9. Disponibles inmediatamente en el frontend

## 💡 Cómo Usar

### Uso Manual (Inmediato)
1. Ve a http://localhost:3000/promotions
2. Haz clic en "🔄 Escanear Ahora"
3. Espera 3-5 segundos
4. Se mostrarán las promociones encontradas

### Uso Automático (Pasivo)
1. Deja el backend corriendo
2. Cada 2 horas se actualizará solo
3. Revisa las promociones cuando quieras
4. Marca como favoritas las que te interesen

### Aprovecha las Ofertas
1. **Esfera Brasil**: Cuando veas "52% descuento" en compra
   - R$ 33,60 por 1,000 puntos
   - Mejor ratio a Iberia (2:1)

2. **Bonus de Transferencia**: "100% bonus"
   - Transfiere 10,000 → recibes 20,000
   - Aprovecha para mover puntos

3. **Error Fares**: Actúa rápido
   - Duran pocas horas
   - Reserva primero, piensa después

4. **TAP a Brasil**: Ofertas recurrentes
   - €493-587 Europa-Brasil
   - Acumula millas TAP (Star Alliance)

## 🔮 Mejoras Futuras Posibles

- [ ] Notificaciones push vía Telegram bot
- [ ] Email diario con resumen de promociones
- [ ] Integración con más fuentes (Twitter, Instagram)
- [ ] Análisis de tendencias (cuándo suelen salir ofertas)
- [ ] Alertas personalizadas ("avísame si Iberia tiene >50% bonus")
- [ ] Histórico de promociones perdidas
- [ ] Calendario de promociones predecibles

## 📊 Estadísticas de Uso

Para ver estadísticas:
```bash
curl http://localhost:8000/api/alerts/stats/summary
```

Respuesta ejemplo:
```json
{
  "total": 5,
  "unread": 5,
  "favorites": 0,
  "by_type": {
    "promo_detected": 4,
    "bonus_transfer": 1
  }
}
```

## 🛠️ Archivos Clave

### Backend
- `app/models/alert.py` - Modelo de alertas
- `app/services/rss_scraper.py` - Scraper RSS con análisis IA
- `app/services/promotion_manager.py` - Gestor de promociones
- `app/scheduler.py` - Scheduler automático
- `app/api/alerts.py` - Endpoints de alertas
- `app/api/promotions.py` - Endpoints de escaneo

### Frontend
- `src/app/promotions/page.tsx` - Página de promociones
- `src/lib/api.ts` - Cliente API (alertsApi, promotionsApi)

---

**Estado**: ✅ Completamente funcional
**Última actualización**: 9 de Febrero 2026
**Promociones activas**: Consulta http://localhost:3000/promotions
