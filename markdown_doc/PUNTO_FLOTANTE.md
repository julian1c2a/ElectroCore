# Punto Flotante - V = M × B^E

Representación de números en **punto flotante** donde mantisa y exponente se almacenan por separado.

## Problema que Resuelve

Punto fijo tiene **error absoluto constante** pero **error relativo variable**:

```
Q(E,F) tiene epsilon = B^(-F)
Error relativo = epsilon / |valor|
```

Cuando cambias de escala:

- En valores pequeños (10^(-3)): error relativo ≈ 10^(-1)  ← MUY MALO
- En valores grandes (10^6): error relativo ≈ 10^(-10) ← MUY BUENO

**Resultado:** Punto fijo es ineficiente para valores que cambian de escala.

---

## Solución: Punto Flotante

**Formato:** V = M × B^E

Donde:

- **M** (mantisa): número **normalizado en [1, B)**
- **E** (exponente): escala el número
- **B** (base): típicamente 2 en sistemas reales

### Mantisa Normalizada en [1, B)

Para base 2, la mantisa está en **[1, 2)**:

- Esto significa: 1 bit entero (siempre 1) + bits fraccionarios
- En base 10: mantisa en [1, 10)

**Ventaja:** Al mantener M acotado, el error relativo es **constante**

```
Valor original: 0.001 = 1.024 × 2^(-10)   → mantisa = 1.024
Valor original: 1000   = 1.953 × 2^9      → mantisa = 1.953

Error relativo en ambos casos ≈ epsilon_mantisa = 2^(-F_M)
```

---

## Ejemplos de Normalización

| Valor Original | Mantisa | Exponente | Verificación |
|---|---|---|---|
| 5.25 | 1.3125 | 2 | 1.3125 × 2² = 5.25 ✓ |
| 0.125 | 1.0 | -3 | 1.0 × 2^(-3) = 0.125 ✓ |
| 100 | 1.5625 | 6 | 1.5625 × 2^6 = 100 ✓ |
| 0.001 | 1.024 | -10 | 1.024 × 2^(-10) ≈ 0.001 ✓ |

**✓ Verificado:** Todas las mantisas están en [1, 2)

---

## Comparación: Error Relativo

### Punto Fijo Q(8,4) base 10

| Escala | Error Relativo |
|---|---|
| 10^(-3) | 1.0e-01 |
| 10^(-1) | 1.0e-03 |
| 10^(0) | 1.0e-04 |
| 10^(2) | 1.0e-06 |
| 10^(6) | 1.0e-10 |

**Problema:** Error relativo varía 1000× según la escala

### Punto Flotante FP(F_M=4, E_bits=8) base 2

| Valor | Error Relativo |
|---|---|
| 0.001 | 0.0625 |
| 0.1 | 0.0625 |
| 1.0 | 0.0625 |
| 100 | 0.0625 |
| 1,000,000 | 0.0625 |

**Ventaja:** Error relativo es **CONSTANTE** independientemente de la escala

---

## Operaciones Aritméticas

### Suma

Requiere **igualar exponentes** antes de sumar mantisas:

```
Ejemplo: 1000000000 + 1

1. Normalizar:
   1000000000 = 1.863 × 2^29
   1          = 1.000 × 2^0

2. Igualar exponentes (usar el mayor):
   1000000000 = 1.863 × 2^29
   1          = 0.0000000019 × 2^29  ← muy pequeño

3. Sumar mantisas:
   1.863 + 0.0000000019 ≈ 1.863

4. Renormalizar (ya está en [1,2))
```

**Nota:** El número más pequeño puede "desaparecer" si su exponente es mucho menor.

### Multiplicación

Mucho más simple:

```
Ejemplo: 1000 × 0.001

1. Normalizar:
   1000   = 1.953 × 2^9
   0.001  = 1.024 × 2^(-10)

2. Multiplicar mantisas:
   1.953 × 1.024 = 2.000

3. Sumar exponentes:
   9 + (-10) = -1

4. Renormalizar (2.0 → 1.0 × 2^1):
   1.0 × 2^0 = 1.0  ✓
```

**Ventaja:** Solo hay que multiplicar mantisas y sumar exponentes.

### División

Similar a multiplicación:

```
Dividir mantisas, restar exponentes, renormalizar si es necesario.
```

---

## Propiedades

| Aspecto | Punto Fijo | Punto Flotante |
|---|---|---|
| **Error absoluto** | Constante | Variable (∝ valor) |
| **Error relativo** | Variable (depende escala) | Constante ✓ |
| **Rango dinámico** | Limitado | Enorme ✓ |
| **Precisión pequeños** | Mala | Buena ✓ |
| **Precisión grandes** | Mala | Buena ✓ |
| **Suma** | Directa | Requiere igualar exponentes |
| **Multiplicación** | Requiere reescalado | Directa ✓ |
| **Complejidad HW** | Simple ✓ | Compleja |
| **Velocidad** | Rápida ✓ | Más lenta |

---

## Clase FixedPointFloating

```python
from core.punto_flotante import FixedPointFloating

# Crear representación con:
# - F_M = 6 bits de precisión en mantisa
# - E_bits = 8 bits para exponente
fp = FixedPointFloating(F_M=6, E_bits=8, base=2)

# Normalizar un número
mantisa, exponent = fp.normalize(5.25)
# → mantisa = 1.3125, exponent = 2

# Reconstruir
valor = fp.denormalize(mantisa, exponent)
# → 5.25

# Operaciones
suma = fp.add(3.5, 2.25)          # → 5.75
resta = fp.subtract(10, 3)         # → 7.0
producto = fp.multiply(3.5, 2.25)  # → 7.875
cociente = fp.divide(15, 4)        # → 3.75

# Errores
epsilon = fp.epsilon_mantisa
abs_error = fp.absolute_error(valor)
rel_error = fp.relative_error(valor)
```

---

## Archivos

- **[core/punto_flotante.py](core/punto_flotante.py)** - Implementación básica
- **[demo_punto_flotante.py](demo_punto_flotante.py)** - Demostraciones y comparaciones

---

## Ejecución

```bash
# Demostraciones
python core/punto_flotante.py

# Comparación punto fijo vs flotante
python demo_punto_flotante.py
```

---

## Próximas Etapas

- [ ] **IEEE 754**: implementación del estándar
  - Números denormalizados
  - Infinito (±∞)
  - NaN (Not a Number)
  - Redondeo
- [ ] Operaciones en precisión doble (64 bits)
- [ ] Manejo de overflow/underflow
- [ ] Conversión de signo entre representaciones
