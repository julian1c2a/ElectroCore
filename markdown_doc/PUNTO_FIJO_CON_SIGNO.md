# Punto Fijo con Signo y Parte Fraccionaria

Implementación de representaciones de números con signo y parte fraccionaria en punto fijo Q(E,F).

## Dos Representaciones

### 1. Magnitud y Signo (M&S)

**Estructura:**

- MSD (dígito más significativo) = SIGNO
  - 0 → positivo (+)
  - 1..B-1 → negativo (-)
- Resto (E+F dígitos) = MAGNITUD del número

**Rango:**

```
[-( B^E - B^(-F) ), B^E - B^(-F) ]
```

**Ejemplo Q(4,4) base 2:**

```
Máximo positivo:  15.9375 = 2^4 - 2^(-4)
Mínimo negativo:  -15.9375 = -(2^4 - 2^(-4))
Rango: [-15.9375, 15.9375]
```

**Valores extremos:**

- Máximo: `B^E - B^(-F)`
- Mínimo: `-(B^E - B^(-F))`
- Positivo mínimo: `B^(-F)`
- Negativo máximo: `-B^(-F)`

**Propiedades:**
✓ Signo separado, fácil de identificar
✓ Magnitud es representación directa
✗ Cero tiene DOS representaciones (+0 y -0)
✗ Operaciones aritméticas requieren casos especiales

---

### 2. Complemento a la Base

**Estructura:**
Para positivos (valor ≥ 0):

```
M = valor × B^F
```

Para negativos (valor < 0):

```
M = B^(E+F+1) + valor × B^F
```

**Rango:**

```
[-B^E, B^E - B^(-F) ]
```

**Ejemplo Q(4,4) base 2:**

```
Máximo positivo:   15.9375 = 2^4 - 2^(-4)
Mínimo (negativo): -16 = -2^4
Rango: [-16, 15.9375]
```

**Valores extremos:**

- Máximo: `B^E - B^(-F)`
- Mínimo: `-B^E`  ← **El número más negativo**
- Positivo mínimo: `B^(-F)`
- Negativo máximo: `-B^(-F)`

**Propiedades:**
✓ Cero tiene representación ÚNICA
✓ Suma y resta son operaciones directas (sin casos especiales)
✓ Permite rango asimétrico (permite exactamente `-B^E`)
✗ Representación negativa menos intuitiva
✗ Requiere operación de complemento para negar

---

## Comparación M&S vs Complemento

| Aspecto | M&S | Complemento |
|---------|-----|------------|
| **Máximo positivo** | `B^E - B^(-F)` | `B^E - B^(-F)` |
| **Mínimo (más negativo)** | `-(B^E - B^(-F))` | `-B^E` |
| **Rango simétrico** | Sí | No |
| **Cero único** | No (±0) | Sí |
| **Suma/resta simple** | No | Sí |
| **Negación** | Invertir signo | M' = 2^(E+F+1) - M |

---

## Ejemplo Q(3,2) base 2

### M&S

```
Rango: [-7.75, 7.75]
```

| Valor | M (M&S) | Estructura |
|-------|---------|-----------|
| 7.75 | 31 | [0][111111] |
| 3.5 | 14 | [0][001110] |
| 0.0 | 0 | [0][000000] |
| -0.0 | 32 | [1][000000] |
| -3.5 | 46 | [1][001110] |
| -7.75 | 63 | [1][111111] |

### Complemento a Base

```
Rango: [-8, 7.75]
Módulo: 2^6 = 64
```

| Valor | M (Comp) | Binario | Interpretación |
|-------|----------|---------|----------------|
| 7.75 | 31 | 011111 | Positivo |
| 3.5 | 14 | 001110 | Positivo |
| 0.0 | 0 | 000000 | Cero único |
| -0.25 | 63 | 111111 | Complemento |
| -3.5 | 50 | 110010 | Complemento |
| -8.0 | 32 | 100000 | Mínimo |

---

## Operaciones Aritméticas

### En M&S

Requieren análisis de signos:

```
(+A) + (+B) = +(A + B)
(+A) + (-B) = +(A - B) si A ≥ B
             = -(B - A) si A < B
(-A) + (-B) = -(A + B)
```

### En Complemento a Base

Suma y resta directas (con manejo de overflow):

```
(+A) + (+B) = A + B (módulo B^(E+F+1))
(+A) + (-B) = A + B (módulo B^(E+F+1))
(-A) + (-B) = A + B (módulo B^(E+F+1))
```

**Ventaja computacional:** El complemento es más eficiente para aritmética.

---

## Clases Implementadas

### FixedPointSignedMS

Punto fijo con signo usando Magnitud y Signo.

```python
from core.punto_fijo_con_signo import FixedPointSignedMS

fp = FixedPointSignedMS(E=4, F=4, base=2)

# Codificar
M = fp.encode(5.25)      # → 84
M = fp.encode(-5.25)     # → 340

# Decodificar
value = fp.decode(84)    # → 5.25

# Propiedades
print(fp.max_value)      # 15.9375
print(fp.min_value)      # -15.9375
print(fp.epsilon)        # 0.0625
```

### FixedPointSignedComplement

Punto fijo con signo usando Complemento a Base.

```python
from core.punto_fijo_con_signo import FixedPointSignedComplement

fp = FixedPointSignedComplement(E=4, F=4, base=2)

# Codificar
M = fp.encode(5.25)      # → 84
M = fp.encode(-5.25)     # → 428

# Decodificar
value = fp.decode(84)    # → 5.25

# Negación (complemento)
M_comp = fp.complement(84)  # → 428

# Propiedades
print(fp.max_value)      # 15.9375
print(fp.min_value)      # -16
print(fp.modulo)         # 512
```

---

## Archivos

- **core/punto_fijo_con_signo.py** - Implementación de ambas clases (402 líneas)
- **demo_punto_fijo_con_signo.py** - Demostraciones detalladas (450+ líneas)

## Ejecución

```bash
# Demostracion basica
python -c "from core.punto_fijo_con_signo import *; demonstrate_ms(); demonstrate_complement()"

# Demostracion detallada
python demo_punto_fijo_con_signo.py
```

---

## Próximas Etapas

- [ ] Punto flotante: V = M × B^E
- [ ] Operaciones aritméticas optimizadas con manejo de overflow
- [ ] Conversión de signo entre representaciones
- [ ] Tests unitarios exhaustivos
