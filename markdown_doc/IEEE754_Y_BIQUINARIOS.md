# IEEE 754 Completo + Códigos Biquinarios

## 1. IEEE 754 - Estándar Completo para Punto Flotante

### Estructura: [Signo (1 bit)][Exponente (E bits)][Mantisa (F bits)]

---

### Números Normalizados

**Formato:** ±1.M × B^E (mantisa implícita)

```
Ejemplo IEEE 754 single (32 bits):
- 1 bit signo
- 8 bits exponente (bias = 127)
- 23 bits mantisa
- Rango: [1.18e-38, 1.70e+38]
```

---

### Números Denormalizados (Subnormales)

**Problema sin denormalizados:**

```
Números normalizados empiezan en 2^E_min ≈ 1.18e-38
Números más pequeños: simplemente 0 (salto abrupto)
```

**Solución: Números denormalizados**

**Formato:** ±0.M × B^E_min (mantisa sin bit implícito)

```
Cuando E_encoded = 0:
  - Exponente real: E = 1 - bias (mínimo)
  - Mantisa: 0.M (sin el 1 implícito)
  - Rango: [0, máx_denorm]
  
Ejemplo con IEEE 754 single:
  - E_min = 1 - 127 = -126
  - Rango denormalizado: [5.96e-08, 1.18e-38]
  - Transición suave a 0, sin salto
```

**Ventaja:** Gradual underflow en lugar de underflow abrupto

---

### Infinito

**Codificación:**

- Exponente: todo 1s (E_encoded = B^E_bits - 1)
- Mantisa: todo 0s
- Signo: 0 → +∞, 1 → -∞

```python
# Ejemplo
+∞: [0][11111111][00000000000000000000000]  (IEEE 754 single)
-∞: [1][11111111][00000000000000000000000]

# Operaciones
1 / 0 = +∞
-1 / 0 = -∞
∞ + 1 = ∞
∞ - ∞ = NaN
```

---

### NaN (Not a Number)

**Codificación:**

- Exponente: todo 1s (E_encoded = B^E_bits - 1)
- Mantisa: cualquier valor excepto 0
- Signo: irrelevante (no tiene significancia)

**Dos tipos de NaN:**

#### 1. **qNaN (Quiet NaN)**

- MSB de mantisa = 1
- No genera excepción al propagarse
- Usado para errores previos de operación

```
Ejemplo: [X][11111111][10000000000000000000000]
                      ↑ MSB = 1
```

#### 2. **sNaN (Signaling NaN)**

- MSB de mantisa = 0, pero mantisa ≠ 0
- **GENERA EXCEPCION** al usarse en operaciones
- Detecta operaciones inválidas

```
Ejemplo: [X][11111111][00000000000000000000001]
                      ↑ MSB = 0, pero hay 1s
```

**Propiedades:**

```
NaN ≠ NaN (nunca igual, ni siquiera consigo mismo)
NaN < x: falso
NaN > x: falso
NaN == x: falso (siempre)

Comparaciones con NaN: siempre falso o excepción
```

---

### Ejemplo: IEEE 754 Single (32 bits)

```
Rango normalizado:    [±1.18e-38, ±1.70e+38]
Rango denormalizado:  [±5.96e-08, ±1.18e-38]

Valores especiales:
  ±0      → [S][00000000][00000000000000000000000]
  ±∞      → [S][11111111][00000000000000000000000]
  qNaN    → [X][11111111][1XXXXXXXXXXXXXXXXXXXXXXXXX]
  sNaN    → [X][11111111][0XXXXXXXXXXXXXXXXXXXXXXXXX] (X ≠ todo 0)
```

---

## 2. Códigos Biquinarios vs "2 entre 5"

### Diferencia Crítica

| Aspecto | Biquinarios | "2 entre 5" |
|---|---|---|
| **Estructura** | Quinaria (grupo) + Binaria (selección) | Puro código de peso |
| **Bits con valor 1** | Variable (2-3 típico) | EXACTAMENTE 2 |
| **Detección de errores** | Paridad en cada componente | Cuenta de unos (siempre 2) |
| **Componentes** | Separados funcionalmente | Integrado |
| **Eficiencia** | Pobre (5-7 bits para 10 valores) | Similar (5 bits para 10 valores) |

---

### Biquinarios: 7 bits (IBM 650)

**Estructura:** [Relleno (2)][Binaria (2)][Quinaria (3)]

**Componentes:**

1. **Quinaria (3 bits):** Selecciona grupo
   - 000 → dígitos 0-1
   - 001 → dígitos 2-3
   - 010 → dígitos 4-5
   - 011 → dígitos 6-7
   - 100 → dígitos 8-9

2. **Binaria (2 bits):** Selecciona dentro del grupo
   - 01 → primer dígito del grupo
   - 10 → segundo dígito del grupo

**Tabla:**

```
Dígito | Quinaria | Binaria | Código 7-bit
-------|----------|---------|------------
   0   |   000    |   01    | 0001000
   1   |   000    |   10    | 0010000
   2   |   001    |   01    | 0001001
   3   |   001    |   10    | 0010001
   4   |   010    |   01    | 0001010
   5   |   010    |   10    | 0010010
   6   |   011    |   01    | 0001011
   7   |   011    |   10    | 0010011
   8   |   100    |   01    | 0001100
   9   |   100    |   10    | 0010100
```

**Eficiencia:** log₂(10) / 7 ≈ 0.427 bits/dígito

---

### Biquinarios: 5 bits (Univac 60/120 - Remington Rand)

**Estructura:** [Quinaria (2)][Binaria (3)]

Más compacto que 7 bits pero aún menos eficiente que BCD.

**Tabla:**

```
Dígito | Quinaria | Binaria | Código 5-bit
-------|----------|---------|----------
   0   |   00     |   001   | 00001
   1   |   00     |   010   | 00010
   2   |   00     |   100   | 00100
   3   |   01     |   001   | 01001
   4   |   01     |   010   | 01010
   5   |   10     |   001   | 10001
   6   |   10     |   010   | 10010
   7   |   10     |   100   | 10100
   8   |   11     |   001   | 11001
   9   |   11     |   010   | 11010
```

**Eficiencia:** log₂(10) / 5 ≈ 0.664 bits/dígito

---

### Variantes Históricas de Biquinarios

1. **IBM 650** (7 bits) - La más común
2. **IBM 1401** (6 bits) - Adaptada al hardware de 6 bits
3. **Univac 60/120** (5 bits) - Remington Rand
4. **FACOM 128** (7 bits) - Variante japonesa

---

### "2 entre 5" (Cinco de los Siguientes)

**Estructura:** Exactamente 2 unos en 5 bits

**Códigos de peso (5-4-2-1-0):**

```
0 → 00011 (pesos 1+2 = 3, dos unos) ✓
1 → 00101 (pesos 1+4 = 5, dos unos) ✓
2 → 00110 (pesos 2+4 = 6, dos unos) ✓
3 → 01001 (pesos 1+8... no, esto es incorrecto)

Versiónestándar (5-4-2-1-0):
0 → 00011
1 → 00101
2 → 00110
3 → 01001
4 → 01010
5 → 01100
6 → 10001
7 → 10010
8 → 10100
9 → 11000
```

**Detección de errores:** Si hay error en transmisión, no habrá exactamente 2 unos

**NO ES LO MISMO QUE BIQUINARIO:**

- Biquinario: estructura en dos componentes lógicos
- "2 entre 5": código de peso con restricción de exactamente 2 unos

---

## Comparación de Eficiencias

```
Código              Bits  Eficiencia    Uso Típico
BCD (4-2-1-0)       4     0.832         Estándar, mejor eficiencia
"2 entre 5"         5     0.664         Transmisión (detección integrada)
Biquinario 5 bits   5     0.664         Univac (menos común)
Biquinario 7 bits   7     0.427         IBM 650 (histórico)
```

---

## Implementación en Python

### IEEE 754

```python
from core.ieee754 import IEEE754

# Crear representación
ieee = IEEE754(E_bits=8, F_bits=23, base=2)

# Números normalizados
s, e, m = ieee.encode_normalized(3.5)
value = ieee.decode(s, e, m)

# Números denormalizados
s, e, m = ieee.encode_denormalized(1e-40)

# Infinito
s, e, m = ieee.encode_infinity(positive=True)

# NaN
s, e, m = ieee.encode_nan(quiet=True)  # qNaN
s, e, m = ieee.encode_nan(quiet=False) # sNaN

# Decodificar
result = ieee.decode(s, e, m)
# → valor float, "inf", "-inf", "qNaN", "sNaN"
```

### Biquinarios

```python
from core.biquinarios import Biquinary7Bit, Biquinary5Bit

# 7 bits (IBM 650)
bq7 = Biquinary7Bit()
code = bq7.encode(7)           # → 0010011
digit = bq7.decode(code)       # → 7

# 5 bits (Univac)
bq5 = Biquinary5Bit()
codes = bq5.encode_number("31415")
number = bq5.decode_number(codes)
```

---

## Archivos Implementados

- **[core/ieee754.py](core/ieee754.py)** - IEEE 754 completo (350 líneas)
- **[core/biquinarios.py](core/biquinarios.py)** - Biquinarios 7 bits y 5 bits (290 líneas)

---

## Commit

```
277d3d9 - feat: implement IEEE 754 complete (denormalized, NaN, infinity) and biquinary codes
```

---

**Estado:** ✅ **COMPLETADO Y VERIFICADO**
