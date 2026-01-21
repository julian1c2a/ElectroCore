# 📝 Expansión de Sección 2.1.1.6.1

**Fecha**: 15 de enero de 2026  
**Commit**: ce64733  
**Cambios**: Definiciones formales de capacidad y rango de representación

---

## ✅ Lo Que Se Agregó

### 2.1.1.6.1.1 - Capacidad de Representación

**Definición formal**:

```
capacidad(B, n) = B^n
```

Donde:

- **B** es la base del sistema de numeración
- **n** es la longitud (número de dígitos)
- El resultado es el **número total de representaciones distintas posibles**

**Tabla de ejemplos incluida**:

| Base | Longitud | Capacidad | Rango |
|------|----------|-----------|-------|
| 2    | 3        | 8         | 0-7 |
| 2    | 8        | 256       | 0-255 |
| 10   | 3        | 1000      | 0-999 |
| 16   | 2        | 256       | 0-255 |

---

### 2.1.1.6.1.2 - Rango de Valores Representables

**Definición formal**:

```
Rango = [0, B^l - 1]  (intervalo cerrado)
```

**Justificación matemática** incluida:

- **Mínimo**: Todos los dígitos = 0 → suma = 0
- **Máximo**: Todos los dígitos = (B-1) → suma = $B^l - 1$

**Función de Longitud de Representación**:

```
longitud(x, B) = ⌊log_B(x)⌋ + 1
```

Esto es el **logaritmo entero** del número en base B (mínimo de dígitos necesarios).

**Ejemplos con verificación**:

- 27₁₀: log₁₀(27) ≈ 1.43 → 2 dígitos ✓
- 255₂: log₂(255) ≈ 7.99 → 8 dígitos ✓
- 1994₅: log₅(1994) ≈ 4.72 → 5 dígitos (= 30434₅) ✓

**Tabla de rangos incluida**:

| Base | Longitud | Rango        | Capacidad |
|------|----------|--------------|-----------|
| 2    | 3        | [0, 7]       | 8 |
| 2    | 8        | [0, 255]     | 256 |
| 10   | 2        | [0, 99]      | 100 |
| 16   | 2        | [0, 255]     | 256 |
| 5    | 5        | [0, 3124]    | 3125 |

**Verificación del ejemplo 1994 en base 5 con 5 dígitos**:

```
Capacidad: 5^5 = 3125 ✓
Rango: [0, 3124] ✓
1994 ∈ [0, 3124] ✓
Representación: 30434₅ ✓
```

---

## 📊 Cambios en Documentos

### CONTENIDOS_FE.md

- **Líneas agregadas**: 108
- **Secciones expandidas**: 2.1.1.6.1
- **Nuevas subsecciones**: 2.1.1.6.1.1, 2.1.1.6.1.2
- **Tablas añadidas**: 3 (capacidades, rangos, verificación)
- **Ecuaciones LaTeX**: 5

### INDICE_COMPLETO_SECCION_2_1_1.md

- **Líneas modificadas**: 13
- **Niveles añadidos**: Ampliación de 2.1.1.6.1.1 y 2.1.1.6.1.2
- **Nuevas subsecciones**: 2.1.1.6.1.1.1, 2.1.1.6.1.1.2, 2.1.1.6.1.1.3, 2.1.1.6.1.2.1, 2.1.1.6.1.2.2, 2.1.1.6.1.2.3, 2.1.1.6.1.2.4

### MAPA_NAVEGACION_2_1_1.md

- **Descripción actualizada**: Más detallada
- **Referencias de línea**: Actualizadas
- **Subsecciones expandidas**: Ahora muestra 5 niveles (2.1.1.6.1.1 a 2.1.1.6.1.5)

---

## 🔗 Referencias Cruzadas

**Conceptos relacionados ya existentes**:

- 2.1.1.3 - Conversión entre sistemas (usa capacidad implícitamente)
- 2.1.1.5 - Binario/Octal/Hex (casos especiales de esta sección)
- 2.1.1.8 - Operaciones (necesita entender rango para desbordamiento)

**Conceptos que usarán estas definiciones**:

- 2.1.1.7 - Números con signo (usa rango para definir espacios)
- 2.1.1.9 - Punto flotante (usa capacidad y rango para IEEE 754)

---

## 📌 Notas Importantes

✅ **Concordancia verificada** en todos los documentos
✅ **Fórmulas LaTeX** correctas y renderizadas
✅ **Tablas** con formato markdown estándar
✅ **Ejemplos** verificables matemáticamente
✅ **Notación consistente** con el resto de la sección

---

## 🎯 Ahora Puedes Referenciar

- **2.1.1.6.1.1.1** - Definición de capacidad $B^n$
- **2.1.1.6.1.1.2** - Función capacidad(B, n)
- **2.1.1.6.1.1.3** - Ejemplos de capacidades
- **2.1.1.6.1.2.1** - Definición de rango [0, $B^n - 1$]
- **2.1.1.6.1.2.2** - Justificación matemática
- **2.1.1.6.1.2.3** - Tabla de rangos
- **2.1.1.6.1.2.4** - Función de longitud de representación

**Ejemplo de cita precisa**:

> "Según 2.1.1.6.1.1.2, la capacidad de representación se calcula con la función capacidad(B, n) = $B^n$"

> "El rango máximo es $B^l - 1$ (ver 2.1.1.6.1.2.1)"

---

**Estado**: ✅ LISTO PARA USAR

Commit: ce64733
