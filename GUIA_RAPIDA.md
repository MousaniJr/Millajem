# Guía Rápida - Millajem

**Uso diario y referencia rápida**

---

## Acceso Rápido

### URLs Principales
- **Dashboard**: http://localhost:3000/
- **Promociones**: http://localhost:3000/promotions
- **Recomendaciones**: http://localhost:3000/recommendations
- **Calculadora**: http://localhost:3000/calculator
- **Mis Saldos**: http://localhost:3000/balances
- **API Docs**: http://localhost:8000/docs

### Iniciar Servidores

**Backend:**
```bash
cd C:\Users\mousa\PycharmProjects\Millajem\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd C:\Users\mousa\PycharmProjects\Millajem\frontend
npm run dev
```

---

## Workflow Diario (5 minutos)

### 1. Revisar Promociones
1. Abrir http://localhost:3000/promotions
2. Aplicar filtros:
   - ☑️ Solo no leídas
   - Prioridad: High o Urgent
   - País: (tu país de interés)
3. Revisar 2-3 promociones top
4. Marcar favoritas (⭐) para después
5. Marcar como leídas (✓) las que no interesan

### 2. Actualizar Saldos (si aplicable)
1. Abrir http://localhost:3000/balances
2. Click "Actualizar" en programa con cambios
3. Ingresar nuevo balance
4. Ver conversión automática a Avios

---

## Filtros Útiles

### Por Urgencia
- Priority = Urgent
- Solo no leídas = ✓
→ Ver ofertas que expiran pronto

### Por País
- País = BR
- Related Program = Esfera
→ Ver ofertas Esfera específicamente

### Bonus de Transferencia
- Type = Bonus Transfer
- Priority = High
→ Ver bonos de transferencia buenos

### Error Fares
- Type = Error Fare
- Order by = Más recientes
→ Tarifas error antes de que desaparezcan

---

## Estrategia por País

### España 🇪🇸
**Objetivo**: Acumular Avios directamente

| Categoría | Acción | Earning |
|-----------|--------|---------|
| Compras diarias | Amex Gold España | 1 Avios/EUR |
| Combustible | Cepsa + Iberia | 2 Avios/litro |
| Transporte | Cabify vinculado Iberia | 1 Avios/EUR |
| Shopping | Iberia Shopping portal | 1-5 Avios/EUR |

**Tarjeta principal**: Amex Gold España (score 95)

### Brasil 🇧🇷
**Objetivo**: Acumular en Esfera → Transferir a Iberia

| Categoría | Acción | Earning |
|-----------|--------|---------|
| Compras | Santander Unique | 2.2 pts/BRL |
| Supermercado | Pão de Açúcar | 1 pt/BRL |
| Shopping | Livelo portal | 1-5 pts/BRL |
| Farmacia | Droga Raia/Drogasil | 1-2 pts/BRL |

**Conversión óptima**: Esfera → Iberia 2:1 (mejor que Livelo 3.5:1)
**Regla**: Solo transferir con bonus ≥30%

### Gibraltar 🇬🇮
**Objetivo**: Combinar earning + ahorro sin IVA

| Categoría | Acción | Beneficio |
|-----------|--------|-----------|
| Vuelos | BA GIB-LHR | 7-9 Avios/GBP ganados |
| Shopping | Main Street | ~20% ahorro (sin IVA) |
| Combustible | Cepsa GIB (verificar) | 2 Avios/litro + barato |
| Supermercado | Usar tarjeta rewards | Puntos de tarjeta |

**Pendiente verificar**:
- HSBC Premier WE MC (1.5 Avios/GBP)
- Cepsa Gibraltar acepta programa Avios
- Eroski Gibraltar acepta Club Card

**Alternativa**: Málaga AGP (130km) para vuelos largos - más destinos

---

## Ratios de Conversión

### A Avios (1:X)

| Programa | Ratio | Ejemplo |
|----------|-------|---------|
| Iberia Club | 1:1 | 10,000 = 10,000 Avios |
| BA Executive | 1:1 | 10,000 = 10,000 Avios |
| Amex MR España | 1:1 | 10,000 = 10,000 Avios |
| Esfera Brasil | 2:1 | 10,000 = 5,000 Avios |
| Livelo Brasil | 3.5:1 | 10,000 = 2,857 Avios |
| Smiles GOL | 4:1 | 10,000 = 2,500 Avios |
| Accor ALL | 1:1 | 10,000 = 10,000 Avios |
| Marriott Bonvoy | 2.4:1 | 10,000 = 4,167 Avios |

### Mejor Estrategia
1. **Acumular en España**: Directo en Avios (1:1)
2. **Acumular en Brasil**: Esfera primero (2:1), Livelo segundo (3.5:1)
3. **Hoteles**: Accor ALL mejor (1:1)

---

## Comandos Útiles

### Escanear Promociones Manualmente
```bash
curl -X POST http://localhost:8000/api/promotions/scan
```

### Ver Alertas por País
```bash
# España
curl "http://localhost:8000/api/alerts/?country=ES&limit=5"

# Brasil
curl "http://localhost:8000/api/alerts/?country=BR&limit=5"

# Gibraltar
curl "http://localhost:8000/api/alerts/?country=GI&limit=5"
```

### Ver Tarjetas Recomendadas
```bash
curl "http://localhost:8000/api/recommendations/cards"
```

### Backup Base de Datos
```bash
cd C:\Users\mousa\PycharmProjects\Millajem\backend
cp millajem.db millajem.db.backup_$(date +%Y%m%d)
```

---

## Checklist Semanal

### Lunes (10 min)
- [ ] Revisar promociones de fin de semana
- [ ] Filtrar Priority=Urgent o High
- [ ] Marcar favoritas las que requieren seguimiento
- [ ] Activar las que tengan buen ROI

### Miércoles (5 min)
- [ ] Quick check de nuevas promociones
- [ ] Verificar favoritas de lunes
- [ ] Actualizar saldos si hay cambios

### Viernes (15 min)
- [ ] Revisar todas las promociones de la semana
- [ ] Actualizar saldos en todos los programas
- [ ] Usar calculadora para planificar próximas transferencias
- [ ] Verificar vencimientos próximos

### Domingo (30 min)
- [ ] Auditoría completa de saldos
- [ ] Revisar recomendaciones para nuevas oportunidades
- [ ] Planificar estrategia de la semana siguiente
- [ ] Backup de base de datos

---

## Calculadora Rápida

### Uso Común

**Convertir Esfera a Avios:**
- Ir a /calculator
- Seleccionar "A Avios"
- From: Esfera Santander Brasil
- Cantidad: (tu cantidad)
- Ver resultado automático

**Comparar Valor:**
- Seleccionar "Comparar Valor"
- Programa: (tu programa)
- Cantidad: (tu cantidad)
- Ver en cuántos Avios equivale

**Convertir Todos:**
- Seleccionar "Todos a Avios"
- Ver total combinado en Avios
- Útil para saber poder adquisitivo total

---

## Rutas Populares en Avios

### MAD-GRU (Madrid-Sao Paulo)
- **Economy off-peak**: ~25,000 Avios one-way
- **Business off-peak**: ~50,500 Avios one-way
- **Truco**: Reservar GRU-MAD por separado (Brasil no cobra fuel surcharge)

### GIB-LHR (Gibraltar-Londres)
- **Economy off-peak**: 7,250 Avios one-way
- **Tasas mínimas**: ~£35
- **Ganas**: 7-9 Avios/GBP en vuelo pagado

### MAD-NYC (Madrid-Nueva York)
- **Economy off-peak**: ~26,000 Avios one-way
- **Business off-peak**: ~50,000 Avios one-way

### Familia Pooling
- **Iberia Club Family**: 7 miembros, requiere Silver
- **BA Household Account**: Hasta 6 miembros
- Compartir Avios gratis entre cuentas

---

## Cuentas Sociales Top 5

### España
1. **@puntosviajeros** (Instagram/Twitter) - Promociones Iberia/BA/Amex
2. **@millasymas** (Instagram/Twitter) - Noticias y consejos
3. **@iberiaclub** (Twitter) - Oficial Iberia

### Brasil
1. **@pontospravoar** (Instagram/Twitter) - Promociones Livelo/Smiles
2. **@passageirodeprimeira** (Instagram/Twitter) - Ofertas premium
3. **@livelobr** (Twitter) - Oficial Livelo

### UK/Gibraltar
1. **@headforpoints** (Instagram/Twitter) - Principal UK/Avios
2. **@british_airways** (Twitter) - Oficial BA
3. **@aviosclub** (Twitter) - Comunidad Avios

**Tip**: Activar notificaciones en las 3 primeras de cada país

---

## Problemas Comunes

### No aparecen promociones
```bash
# Solución rápida
curl -X POST http://localhost:8000/api/promotions/scan
```

### Backend caído
```bash
cd C:\Users\mousa\PycharmProjects\Millajem\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Frontend no carga
```bash
cd C:\Users\mousa\PycharmProjects\Millajem\frontend
npm run dev
```

### Error de base de datos
```bash
cd backend
cp millajem.db millajem.db.backup
rm millajem.db
python -m app.init_data
python -m app.init_recommendations
python -m app.add_gibraltar_data
```

---

## Tips Avanzados

### Maximizar Acumulación

1. **España**:
   - TODO con Amex Gold (1:1)
   - Combustible SIEMPRE en Cepsa (2 Avios/litro)
   - Usar Iberia Shopping antes de comprar online

2. **Brasil**:
   - Acumular en Esfera (mejor ratio 2:1)
   - Solo transferir con bonus ≥30%
   - Comprar en Pão de Açúcar cuando sea posible

3. **Gibraltar**:
   - Prioritizar BA GIB-LHR cuando vueles
   - Shopping en Main Street (ahorro 20% sin IVA)
   - Verificar opciones de earning local

### Evitar Errores

- ❌ NO transferir Livelo sin bonus (ratio 3.5:1 malo)
- ❌ NO dejar puntos vencer (monitorear vencimientos)
- ❌ NO acumular en múltiples programas sin plan
- ✅ SÍ centralizar en Avios cuando sea posible
- ✅ SÍ aprovechar bonos de transferencia ≥30%
- ✅ SÍ usar family pooling para combinar puntos

### Mejor ROI

1. **Cepsa España**: 2 Avios/litro (muy alto)
2. **Amex Gold España**: 1 Avios/EUR (todo gasto)
3. **BA GIB-LHR**: 7-9 Avios/GBP (vuelos + ganas)
4. **Esfera → Iberia**: 2:1 con bonos (mejor Brasil)
5. **Accor ALL → Avios**: 1:1 (mejor hoteles)

---

## Referencias Rápidas

### Documentación
- **Completa**: `DOCUMENTACION_PROYECTO.md`
- **Cobertura**: `COBERTURA_3_PAISES.md`
- **Research**: `docs/INVESTIGACION_MILLAJEM.md`

### Enlaces Útiles
- Iberia Club: https://www.iberia.com/es/iberia-plus/
- BA Executive: https://www.britishairways.com/travel/execclub/
- Livelo: https://www.livelo.com.br/
- Esfera: https://esferacard.com.br/

---

**Última actualización**: 9 de Febrero 2026
**Tip del día**: Revisa promociones ANTES de hacer compras grandes
