# IEEE754Gen + BiquinaryGen - Clases Genéricas Mejoradas

## 1. IEEE754Gen - Punto Flotante Completamente Genérico

### Características

```python
from core.ieee754 import IEEE754Gen

# Crear representación flotante personalizada
ieee = IEEE754Gen(E_bits=8, F_bits=23, base=2)
```

**Parámetros:**

- `E_bits`: bits para exponente (cualquier valor ≥ 1)
- `F_bits`: bits para mantisa fraccionaria (cualquier valor ≥ 1)
- `base`: base numérica (2, 10, 16, etc. - por defecto 2)

### Ejemplos de Uso

#### IEEE 754 Single (32 bits)

```python
ieee32 = IEEE754Gen(E_bits=8, F_bits=23, base=2)
# Sign (1) + Exponent (8) + Mantissa (23) = 32 bits
# Bias = 127, E_min = -126, E_max = 127

info = ieee32.info
# {
#   'E_bits': 8,
#   'F_bits': 23,
#   'total_bits': 32,
#   'bias': 127,
#   'E_min': -126,
#   'E_max': 127,
#   'epsilon': 1.1920929e-07,
#   'normalized_min': 1.1754944e-38,
#   'denormalized_min': 1.4012985e-45,
#   'max': 1.70141183e+38
# }

# Codificar número normalizado
sign, exponent, mantissa = ieee32.encode_normalized(1.5)
# sign=0, exponent=127, mantissa=4194304

# Decodificar
value = ieee32.decode(sign, exponent, mantissa)  # 1.5
```

#### IEEE 754 Double (64 bits)

```python
ieee64 = IEEE754Gen(E_bits=11, F_bits=52, base=2)
# Bias = 1023
# Rango: [2.225e-308, 8.988e+307]
```

#### Punto Flotante Decimal (Base 10)

```python
ieee_decimal = IEEE754Gen(E_bits=3, F_bits=5, base=10)
# Base 10 para sistemas decimales
# E_bits=3 → 1000 valores de exponente
# F_bits=5 → 5 dígitos decimales de precisión

sign, exp, mant = ieee_decimal.encode_normalized(12.34567)
decoded = ieee_decimal.decode(sign, exp, mant)
# decoded ≈ 12.3456 (redondeado a 5 dígitos)
```

#### Punto Flotante Hexadecimal (Base 16)

```python
ieee_hex = IEEE754Gen(E_bits=2, F_bits=4, base=16)
# Base 16 para representación hexadecimal
```

### API

#### Métodos de Codificación

```python
# Número normalizado: ±1.M × B^E
sign, E_enc, M_enc = ieee.encode_normalized(value)

# Número denormalizado: ±0.M × B^E_min
sign, E_enc, M_enc = ieee.encode_denormalized(value)

# Infinito: ±∞
sign, E_enc, M_enc = ieee.encode_infinity(positive=True)  # +∞
sign, E_enc, M_enc = ieee.encode_infinity(positive=False) # -∞

# NaN (quiet o signaling)
sign, E_enc, M_enc = ieee.encode_nan(quiet=True)   # qNaN
sign, E_enc, M_enc = ieee.encode_nan(quiet=False)  # sNaN
```

#### Decodificación Universal

```python
# Decodifica automáticamente cualquier combinación
result = ieee.decode(sign, E_encoded, M_encoded)
# Retorna: float (para valores normales/denormalizados)
#          "inf" (para +∞)
#          "-inf" (para -∞)
#          "qNaN" (para quiet NaN)
#          "sNaN" (para signaling NaN)
```

#### Utilidades

```python
# Información de la representación
info = ieee.info  # Diccionario con detalles

# Verificar tipos de valores
is_special = ieee.is_special(E_encoded, M_encoded)     # ¿Es infinito o NaN?
is_denorm = ieee.is_denormalized(E_encoded)             # ¿Es denormalizado?

# Rangos
min_norm, max_norm = ieee.get_range_normalized()        # Rango normalizado
min_denorm, max_denorm = ieee.get_range_denormalized()  # Rango denormalizado
```

### Estructura Interna

```
[Signo (1)][Exponente (E_bits)][Mantisa (F_bits)]

Exponente (formato exceso K):
  - Bias = B^(E_bits-1) - 1
  - E_min = 1 - bias (para denormalizados)
  - E_max = bias - 1 (para normalizados)
  - E_max_encoded = B^E_bits - 1 (para infinito/NaN)

Mantisa:
  - Normalizado: 1.M (bit implícito)
  - Denormalizado: 0.M (sin bit implícito)
  - Infinito: 0 (todo ceros)
  - NaN: ≠ 0 (qNaN: MSB=1, sNaN: MSB=0)
```

---

## 2. BiquinaryGen - Código Biquinario Genérico

### Arquitectura

```python
from core.biquinarios import BiquinaryGen, Biquinary7Bit, Biquinary5Bit, Biquinary6Bit

# Crear biquinario genérico personalizado
biq_custom = BiquinaryGen(
    total_bits=8,           # Bits totales
    quinaria_bits=3,        # Bits para componente quinaria
    binaria_bits=3,         # Bits para componente binaria
    encode_table={          # Tabla de codificación personalizada
        0: (0b00, 0b001),
        1: (0b00, 0b010),
        # ...
    }
)
```

**Componentes:**

- **Quinaria**: Selecciona grupo (0-4 o 5-9)
- **Binaria**: Selecciona posición dentro del grupo
- **Relleno**: Bits no utilizados (para alineación)

### Variantes Predefinidas

#### 1. Biquinario 7 bits (IBM 650)

```python
bq7 = Biquinary7Bit()

# Estructura: [Relleno (2)][Binaria (2)][Quinaria (3)]
# Eficiencia: 0.427 bits/dígito

# Codificar
code = bq7.encode(7)  # 0010011 (binario)

# Decodificar
digit = bq7.decode(code)  # 7

# Número completo
codes = bq7.encode_number("314159")
decoded = bq7.decode_number(codes)  # "314159"
```

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

#### 2. Biquinario 5 bits (Univac 60/120)

```python
bq5 = Biquinary5Bit()

# Estructura: [Quinaria (2)][Binaria (3)]
# Eficiencia: 0.664 bits/dígito

# Codificar números largos
codes = bq5.encode_number("67890")
# → [10010, 10100, 11001, 11010, 00001]

decoded = bq5.decode_number(codes)  # "67890"
```

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

#### 3. Biquinario 6 bits (IBM 1401)

```python
bq6 = Biquinary6Bit()

# Estructura: [Relleno (1)][Quinaria (2)][Binaria (3)]
# Eficiencia: 0.555 bits/dígito
# Adaptado a máquinas de 6 bits

codes = bq6.encode_number("12345")
decoded = bq6.decode_number(codes)
```

### API Común (BiquinaryGen)

```python
# Codificar dígito individual
code = bq.encode(digit)          # int → int (7/5/6 bits)

# Decodificar código
digit = bq.decode(code)          # int → int (dígito 0-9)

# Codificar número completo
codes = bq.encode_number("12345")  # str → List[int]

# Decodificar lista de códigos
number = bq.decode_number(codes)   # List[int] → str

# Información
repr(bq)                           # "Biquinary7Bit(IBM 650 style)"
```

### Propiedades de BiquinaryGen

```python
bq.total_bits          # Bits totales (7, 5, 6, etc.)
bq.quinaria_bits       # Bits para quinaria
bq.binaria_bits        # Bits para binaria
bq.encode_table        # Diccionario de codificación
bq.decode_table        # Diccionario inverso
```

---

## 3. Comparación: Biquinarios vs "2 entre 5"

### Diferencias Críticas

| Aspecto | Biquinarios | "2 entre 5" |
|---|---|---|
| **Estructura** | Quinaria + Binaria (componentes separados) | Código de peso integrado |
| **Unos en código** | Variable (2-3 típico) | **EXACTAMENTE 2** |
| **Detección de errores** | Paridad por componente | Conteo de unos (siempre 2) |
| **Componentes** | Separados funcionalmente | Código único |
| **Implementación** | IBM 650, Univac 60/120 | Weitzman, variantes |

### Ejemplo

```python
# BIQUINARIO 7 BITS (IBM 650)
# Dígito 7: quinaria=011 (grupo), binaria=10 (selección)
# Código: 0010011

# "2 ENTRE 5" (5-4-2-1-0)
# Dígito 7: exactamente 2 unos en 5 bits
# Código: 10010 (pesos 4 + 2 = 6 ✗)
#      o: 01010 (pesos 4 + 1 = 5 ✗)
#      o: 10100 (pesos 4 + 2 = 6 ✗)
```

---

## 4. Ejemplo Completo Integrado

```python
from core.ieee754 import IEEE754Gen
from core.biquinarios import Biquinary7Bit, Biquinary5Bit

# 1. Crear representación IEEE 754 personalizada
ieee = IEEE754Gen(E_bits=8, F_bits=23, base=2)

# 2. Codificar un número flotante
num_float = 3.14159
sign, exp, mant = ieee.encode_normalized(num_float)
decoded = ieee.decode(sign, exp, mant)
print(f"Flotante {num_float} → {decoded}")

# 3. Usar biquinarios para almacenar datos
bq7 = Biquinary7Bit()
bq5 = Biquinary5Bit()

# 4. Codificar número decimal
num_dec = "31415926"
codes7 = bq7.encode_number(num_dec)
codes5 = bq5.encode_number(num_dec)

print(f"\nNúmero: {num_dec}")
print(f"  7 bits: {len(codes7)} códigos, {len(codes7)*7} bits totales")
print(f"  5 bits: {len(codes5)} códigos, {len(codes5)*5} bits totales")

# 5. Verificar decodificación
assert bq7.decode_number(codes7) == num_dec
assert bq5.decode_number(codes5) == num_dec

print(f"  ✓ Verificación OK")
```

### Salida Esperada

```
Flotante 3.14159 → 3.1415901184082

Número: 31415926
  7 bits: 8 códigos, 56 bits totales
  5 bits: 8 códigos, 40 bits totales
  ✓ Verificación OK
```

---

## 5. Archivos Implementados

| Archivo | Contenido | Líneas |
|---|---|---|
| [core/ieee754.py](core/ieee754.py) | IEEE754Gen + alias IEEE754 + métodos especiales | 377 |
| [core/biquinarios.py](core/biquinarios.py) | BiquinaryGen + 3 variantes predefinidas | 322 |
| [demo_ieee754_biquinarios.py](demo_ieee754_biquinarios.py) | Demostración completa de ambas clases | 217 |

---

## 6. Commit

```
0eea3cb - refactor: IEEE754Gen generico + BiquinaryGen + 3 variantes (7,5,6 bits) + demostracion completa
```

---

**Estado:** ✅ **COMPLETO Y FUNCIONAL**

Ambas clases son:

- ✅ Genéricas y personalizables
- ✅ Totalmente documentadas
- ✅ Con ejemplos de uso
- ✅ Validadas con pruebas de demostración
