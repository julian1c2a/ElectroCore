---
# REFERENCIA RÁPIDA: FUNCIONES DE REPRESENTACIÓN EN LONGITUD FIJA (2.1.1.6.1)

## 📋 Tabla de Funciones Python Disponibles

| Función | Fórmula Matemática | Retorna | Uso |
|---------|-------------------|---------|-----|
| `capacidad_representacion(B, n)` | $B^n$ | `int` | Número total de valores representables |
| `rango_representacion(B, n)` | $[0, B^n-1]$ | `Tuple[int, int]` | Mínimo y máximo representables |
| `longitud_representacion(x, B)` | $\lfloor \log_B(x) \rfloor + 1$ | `int` | Dígitos mínimos necesarios para x |
| `analisis_representacion(x, B, n)` | Todas las anteriores | `Dict` | Análisis completo con todas las métricas |

---

## 🎯 Ejemplos Prácticos Rápidos

### Ejemplo 1: ¿Cuántos valores con 8 bits? (Base 2, 8 dígitos)

```python
from core.sistemas_numeracion_basicos import capacidad_representacion, rango_representacion

cap = capacidad_representacion(2, 8)      # 256
rango = rango_representacion(2, 8)        # (0, 255)

print(f"Con 8 bits: {cap} valores, rango {rango}")
# Salida: Con 8 bits: 256 valores, rango (0, 255)
```

### Ejemplo 2: ¿Cuántos dígitos para representar 1994 en base 5?

```python
from core.sistemas_numeracion_basicos import longitud_representacion

digitos = longitud_representacion(1994, 5)  # 5
print(f"1994 en base 5 necesita {digitos} dígitos")
# 1994 = 30434₅  ✓ 5 dígitos
```

### Ejemplo 3: Análisis Completo

```python
from core.sistemas_numeracion_basicos import analisis_representacion

datos = analisis_representacion(1994, 5, longitud=5)
print(f"Capacidad: {datos['capacidad']}")        # 3125
print(f"Rango: {datos['rango']}")                 # (0, 3124)
print(f"¿Cabe 1994? {datos['en_rango']}")        # True
```

---

## 📊 Tabla de Capacidades Comunes

| Longitud | Base 2 | Base 8 | Base 10 | Base 16 |
|----------|--------|--------|---------|---------|
| 3 dígitos | 8 | 512 | 1,000 | 4,096 |
| 4 dígitos | 16 | 4,096 | 10,000 | 65,536 |
| **8 dígitos** | **256** | **16M** | **100M** | **4G** |
| 16 dígitos | 65,536 | 281T | $10^{16}$ | $2^{64}$ |

---

## 🔍 Detección de Desbordamiento

```python
def cabe_en_registro(numero, base, longitud):
    """¿Cabe el número en n dígitos de la base dada?"""
    from core.sistemas_numeracion_basicos import rango_representacion
    rango_min, rango_max = rango_representacion(base, longitud)
    return rango_min <= numero <= rango_max

# Uso:
print(cabe_en_registro(100, 2, 8))    # True  - 100 cabe en 8 bits
print(cabe_en_registro(1000, 10, 3))  # False - 1000 NO cabe en 3 dígitos decimales
print(cabe_en_registro(1994, 5, 5))   # True  - 1994 cabe en 5 dígitos base-5
```

---

## 📝 Relaciones Importantes

### 1. Capacidad vs Rango

- **Capacidad = B^n** → cantidad total de valores
- **Rango = [0, B^n-1]** → intervalo de valores
- **Relación**: Total de valores = Rango_máximo - Rango_mínimo + 1 = B^n

### 2. Longitud Mínima

- Para representar x en base B: $\text{dígitos} = \lfloor \log_B(x) \rfloor + 1$
- Ejemplo: 1994 en base 5
  - $\log_5(1994) \approx 4.77$
  - $\lfloor 4.77 \rfloor + 1 = 5$ dígitos ✓

### 3. Desbordamiento

- Si numero > B^n - 1, **NO cabe** en n dígitos
- Ejemplo: 256 en 2 dígitos hexadecimales (máx: 255)

---

## 🧮 Conversión Rápida: 1994 en Base 5

### Usando las funciones

```python
from core.sistemas_numeracion_basicos import (
    longitud_representacion,
    rango_representacion,
    analisis_representacion
)

# ¿Cuántos dígitos?
digs = longitud_representacion(1994, 5)  # 5

# ¿Cabe en longitud 5?
rango_min, rango_max = rango_representacion(5, 5)  # (0, 3124)
cabe = rango_min <= 1994 <= rango_max  # True ✓

# Análisis completo
análisis = analisis_representacion(1994, 5)
print(análisis)
```

**Verificación manual:**

- $1994 = 1 \times 5^4 + 9 \times 5^3 + 9 \times 5^2 + 3 \times 5 + 4$
- $= 1 \times 625 + 9 \times 125 + 9 \times 25 + 3 \times 5 + 4$
- $= 625 + 1125 + 225 + 15 + 4 = 1994$ ✓
- **Resultado: 1994₁₀ = 30434₅**

---

## 🚀 Caso de Uso: Sistema de Puntos

Un videojuego usa un registro de 16 bits sin signo para guardar la puntuación.

```python
from core.sistemas_numeracion_basicos import rango_representacion, analisis_representacion

# Rango de puntos posibles
rango_min, rango_max = rango_representacion(2, 16)
print(f"Puntuación máxima: {rango_max:,}")  # 65,535

# Análisis de una puntuación específica
puntos = 50000
datos = analisis_representacion(puntos, 2, 16)

if datos['en_rango']:
    print(f"Puntuación {puntos:,} es VÁLIDA")
    print(f"En binario: {'0' * (16 - datos['longitud_mínima'])} + {bin(puntos)[2:]}")
else:
    print(f"ERROR: Puntuación {puntos:,} DESBORDAMIENTO")
```

---

## 📌 Notas Importantes

1. **Capacidad NO depende de la base**: 8 bits = 256 valores en cualquier base
2. **Rango mínimo SIEMPRE es 0**: [0, B^n-1]
3. **Longitud mínima es una cota inferior**: Puede necesitar padding con ceros
4. **Desbordamiento**: Se produce cuando numero > B^n - 1

---

## 🔗 Secciones Relacionadas

- **2.1.1.6**: Representación en longitud fija
- **2.1.1.6.1.1**: Capacidad de representación (B^n)
- **2.1.1.6.1.2**: Rango de representación ([0, B^n-1])
- **2.1.1.6.1.3**: (futura) Desbordamiento y detección de errores
