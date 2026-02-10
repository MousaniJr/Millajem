# Programas Personalizados en Mis Saldos

**Fecha**: 9 de Febrero 2026
**Feature**: Crear programas de lealtad personalizados desde Mis Saldos

---

## ✅ Implementado

Ahora puedes crear programas de lealtad personalizados directamente desde la página de Mis Saldos para rastrear puntos que no están en la lista predefinida.

### Casos de Uso

**Programas que puedes añadir:**
- 💳 **Revolut Rev Points** - Tarjeta Revolut
- 🏪 **El Corte Inglés Club** - Programa de tienda
- ⭐ **Starbucks Rewards** - Café
- 🏦 **Banco Santander Puntos** - Programa bancario
- 🛍️ **Amazon Puntos** - Compras online
- ✈️ **Programas locales** - Aerolíneas pequeñas
- 🏨 **Hoteles boutique** - Programas independientes
- 🎯 **Cualquier otro** programa que uses

---

## 🎯 Cómo Usar

### 1. Acceder a Mis Saldos

1. Ir a http://localhost:3000/balances
2. Click en "➕ Añadir Saldo"

### 2. Crear Programa Personalizado

1. En el selector de "Programa", verás el link:
   ```
   ➕ ¿No encuentras tu programa? Crear uno nuevo
   ```

2. Click en el link → Se abre modal

3. Rellenar formulario:
   - **Nombre**: Ej. "Revolut Rev Points"
   - **Moneda/Unidad**: Ej. "Rev Points", "Puntos", "Estrellas"
   - **País**: Seleccionar país
   - **Ratio a Avios**: (Opcional) Solo si se convierte a Avios
   - **Notas**: (Opcional) Descripción

4. Click "Crear Programa"

5. El programa se crea y **se selecciona automáticamente** en el formulario

6. Continuar añadiendo el saldo normalmente

### 3. El Programa ya está Disponible

- Aparece en la lista de programas
- Se puede usar en futuros balances
- Se puede usar en la calculadora
- Se muestra en el dashboard

---

## 📝 Campos Explicados

### Nombre del Programa (Requerido)
```
Ejemplos:
- "Revolut Rev Points"
- "El Corte Inglés Club"
- "Starbucks Rewards"
- "American Airlines AAdvantage" (si no está en lista)
```

### Moneda/Unidad (Requerido)
```
Ejemplos:
- "Rev Points"
- "Puntos"
- "Estrellas"
- "Millas"
- "Créditos"
```

### País
```
Opciones:
- 🇪🇸 España
- 🇧🇷 Brasil
- 🇬🇮 Gibraltar
- 🇬🇧 Reino Unido
- 🇺🇸 Estados Unidos
- 🌍 Internacional (por defecto)
```

### Ratio de Conversión a Avios (Opcional)

**¿Qué es?**
- Cuántos puntos de TU programa equivalen a 1 Avios
- Solo si tu programa se puede convertir a Avios

**Ejemplos:**
```
Ratio = 1: 1 punto = 1 Avios (como Iberia)
Ratio = 2: 2 puntos = 1 Avios (como Esfera)
Ratio = 0: No se convierte a Avios (dejar en 0)
```

**¿Cuándo dejar en 0?**
- Si los puntos NO se convierten a Avios
- Ejemplos: Starbucks, Amazon, tiendas locales

**¿Cuándo poner un número?**
- Si los puntos SÍ se convierten a Avios
- Busca en la web del programa el ratio

### Notas (Opcional)
```
Ejemplos:
- "Programa de fidelidad de Revolut - 1 punto por libra"
- "Tarjeta de El Corte Inglés - acumulo en compras"
- "Programa local de mi banco - vencen a fin de año"
```

---

## 📊 Ejemplo Completo

### Crear Revolut Rev Points

**Formulario:**
```
Nombre: Revolut Rev Points
Moneda: Rev Points
País: Reino Unido
Ratio a Avios: 0 (no se convierten)
Notas: Tarjeta Revolut - 1 punto por libra gastada
```

**Resultado:**
- Programa creado ✅
- ID: 13
- Se selecciona automáticamente
- Listo para añadir balance

**Añadir Saldo:**
```
Programa: Revolut Rev Points (ya seleccionado)
Cantidad: 15000
Notas: Saldo acumulado de compras del mes
```

**En Dashboard:**
```
Revolut Rev Points: 15,000 Rev Points
Equiv. Avios: N/A (no convertible)
```

---

## 🔄 Integración con el Sistema

### Dashboard
- Los programas personalizados aparecen en el dashboard
- Se agrupan por país
- Si no tienen conversión a Avios, muestra "N/A"

### Calculadora
- Disponibles en la calculadora
- Si tienen ratio a Avios, se pueden convertir
- Si ratio = 0, muestra mensaje "No convertible a Avios"

### Mis Saldos
- Aparecen en la lista de programas
- Se pueden editar/eliminar balances normalmente
- Última actualización se registra

---

## ⚠️ Consideraciones

### Ratio a Avios

**Si no estás seguro del ratio:**
1. Deja en 0 por ahora
2. Investiga en la web del programa
3. Edita el programa después si encuentras el ratio

**Cómo encontrar el ratio:**
- Busca en la web: "[Programa] convert to Avios"
- Busca en la web: "[Programa] transfer to Iberia"
- Pregunta en foros de viajes/puntos
- Si no existe conversión, deja en 0

### Programas Duplicados

**Antes de crear:**
- Revisa que NO esté ya en la lista
- Programas como Iberia, BA, Livelo ya existen
- Solo crea si es realmente nuevo

### Categoría

Por ahora la categoría se pone automáticamente como "other" (otros).

---

## 🎯 Programas Comunes a Añadir

### Reino Unido 🇬🇧
- Revolut Rev Points (0 ratio - no convierte)
- Tesco Clubcard (0 ratio - descuentos)
- Nectar (0 ratio - tiendas)

### España 🇪🇸
- El Corte Inglés Club (0 ratio - descuentos)
- Carrefour Puntos (0 ratio - descuentos)
- IKEA Family (0 ratio - programa familiar)

### Brasil 🇧🇷
- Magazine Luiza (0 ratio - tienda)
- Ponto Frio (0 ratio - tienda)
- Casas Bahia (0 ratio - tienda)

### Estados Unidos 🇺🇸
- Starbucks Rewards (0 ratio - café)
- Amazon Puntos (0 ratio - compras)
- Target Circle (0 ratio - tienda)

### Internacional 🌍
- Uber Rewards (0 ratio - transporte)
- Airbnb Puntos (0 ratio - alojamiento)
- PayPal Rewards (0 ratio - pagos)

---

## 🚀 Ventajas

### Centralización
✅ Todos tus puntos en un solo lugar
✅ Un dashboard para ver todo
✅ No necesitas apps múltiples

### Flexibilidad
✅ Añade CUALQUIER programa
✅ Programas locales, pequeños, raros
✅ No estás limitado a la lista predefinida

### Tracking
✅ Registra balances manualmente
✅ Ve última actualización
✅ Añade notas sobre vencimientos

### Conversión (si aplica)
✅ Si el programa convierte a Avios, calcula automáticamente
✅ Ve todo en equivalente Avios
✅ Compara valor real

---

## 📝 Comandos API (Avanzado)

### Crear programa vía API

```bash
curl -X POST http://localhost:8000/api/programs/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Revolut Rev Points",
    "currency": "Rev Points",
    "country": "UK",
    "category": "other",
    "avios_ratio": 0,
    "notes": "Programa de fidelidad de Revolut"
  }'
```

### Ver todos los programas

```bash
curl http://localhost:8000/api/programs/
```

### Ver programas "other"

```bash
curl http://localhost:8000/api/programs/ | grep -A 5 '"category": "other"'
```

---

## ✅ Checklist de Uso

### Crear Programa Personalizado
- [ ] Ir a /balances
- [ ] Click "Añadir Saldo"
- [ ] Click "¿No encuentras tu programa?"
- [ ] Rellenar nombre (requerido)
- [ ] Rellenar moneda (requerido)
- [ ] Seleccionar país
- [ ] Ratio a Avios (0 si no convierte)
- [ ] Notas descriptivas
- [ ] Click "Crear Programa"

### Añadir Balance
- [ ] Programa ya seleccionado automáticamente
- [ ] Ingresar cantidad de puntos
- [ ] Notas opcionales
- [ ] Click "Guardar"

### Verificar
- [ ] Aparece en Mis Saldos
- [ ] Aparece en Dashboard
- [ ] Si tiene ratio, muestra equiv. Avios
- [ ] Última actualización correcta

---

## 🎊 Ejemplo de Uso Real

### Situación
Tienes una tarjeta Revolut y acumulas Rev Points, pero no están en la lista de programas.

### Solución
1. Ir a /balances
2. Click "Añadir Saldo"
3. Click "¿No encuentras tu programa?"
4. Crear programa:
   ```
   Nombre: Revolut Rev Points
   Moneda: Rev Points
   País: Reino Unido
   Ratio: 0 (no convierte a Avios)
   Notas: Acumulo 1 punto por libra gastada
   ```
5. Click "Crear"
6. Programa se selecciona automáticamente
7. Añadir saldo:
   ```
   Programa: Revolut Rev Points
   Cantidad: 15000
   Notas: Acumulado en febrero
   ```
8. Click "Guardar"

### Resultado
```
Dashboard muestra:
┌─────────────────────────┐
│ Revolut Rev Points      │
│ 15,000 Rev Points       │
│ Equiv. Avios: N/A       │
│ UK                      │
└─────────────────────────┘
```

---

## 🔧 Troubleshooting

### "Error al crear programa"
- Verifica que el nombre no esté duplicado
- Asegúrate de rellenar campos requeridos
- Comprueba que el backend esté corriendo

### "No aparece en la lista"
- Refresca la página
- El programa se crea correctamente pero necesita reload

### "No se selecciona automáticamente"
- Cierra y abre el formulario de nuevo
- El programa está creado, búscalo en la lista

### "Ratio a Avios incorrecto"
- Puedes editarlo después (pendiente implementar)
- Por ahora, crea el programa de nuevo con ratio correcto

---

## 💡 Tips

1. **Nombres Descriptivos**
   - Usa nombres claros: "Revolut Rev Points" mejor que "Revolut"
   - Incluye el tipo de puntos si es necesario

2. **Ratio = 0 por Defecto**
   - Si no sabes el ratio, pon 0
   - Mejor que poner un ratio incorrecto
   - Puedes investigar y actualizarlo después

3. **Notas Útiles**
   - Anota vencimientos: "Vencen 31 dic 2026"
   - Anota earning: "1 punto por libra"
   - Anota restricciones: "Mínimo 5000 para canjear"

4. **País Correcto**
   - Facilita agrupación en dashboard
   - Si es global, usa "Internacional"

---

## 🎯 Conclusión

Ahora tienes **total flexibilidad** para rastrear CUALQUIER programa de puntos:

✅ Programas grandes (Iberia, BA) → Ya en la lista
✅ Programas medianos (Revolut, tiendas) → Créalos tú
✅ Programas pequeños (locales, raros) → Créalos tú
✅ Todo en un solo dashboard
✅ Conversión a Avios cuando aplique

**No más apps múltiples, todo centralizado en Millajem.**

---

**Última actualización**: 9 de Febrero 2026
**Acceso**: http://localhost:3000/balances
**API Docs**: http://localhost:8000/docs#/programs
