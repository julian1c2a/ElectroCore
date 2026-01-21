# 📖 REFERENCIA: Funciones Genéricas de Conversión entre Bases

## 🎯 Descripción General

Cuatro funciones para convertir números entre **cualquier par de bases** (2-36):

| Función | Para | Ejemplo |
|---------|------|---------|
| `decimal_a_base_B()` | Decimal → Base B | 1994₁₀ → 30434₅ |
| `base_B_a_decimal()` | Base B → Decimal | 30434₅ → 1994₁₀ |
| `base_B_a_base_B_prima()` | Base B → Base B' | 30434₅ → 11111001010₂ |
| `base_B_a_base_B_prima_potencias()` | Bases relacionadas (optimizado) | 11111111₂ ↔ ff₁₆ |

---

## 1️⃣ `decimal_a_base_B(numero, base) -> str`

Convierte un número **decimal a cualquier base B** (2-36).

### Firma Completa

```python
from core.sistemas_numeracion_basicos import decimal_a_base_B

decimal_a_base_B(numero: int, base: int) -> str
```

### Parámetros

- `numero` (int): Número decimal ≥ 0
- `base` (int): Base destino (2-36)

### Retorna

- `str`: Representación en base B
  - Usa dígitos 0-9 para valores 0-9
  - Usa letras a-z para valores 10-35

### Ejemplos

```python
# Base 5
decimal_a_base_B(1994, 5)   # → "30434"

# Base 2 (Binario)
decimal_a_base_B(255, 2)    # → "11111111"

# Base 16 (Hexadecimal)
decimal_a_base_B(255, 16)   # → "ff"

# Base 8 (Octal)
decimal_a_base_B(100, 8)    # → "144"

# Base 36 (Máxima)
decimal_a_base_B(1295, 36)  # → "zz"
```

### Algoritmo: Divisiones Sucesivas

```
1994 ÷ 5 = 398 resto 4  →  d₀ = 4
398 ÷ 5 = 79 resto 3   →  d₁ = 3
79 ÷ 5 = 15 resto 4    →  d₂ = 4
15 ÷ 5 = 3 resto 0     →  d₃ = 0
3 ÷ 5 = 0 resto 3      →  d₄ = 3

Resultado: 30434₅ (leyendo de abajo a arriba)
```

### Referencias en Temario

- **2.1.1.3**: Conversión de Base 10 a Base B

---

## 2️⃣ `base_B_a_decimal(numero_str, base) -> int`

Convierte un número **en base B a decimal**.

### Firma Completa

```python
from core.sistemas_numeracion_basicos import base_B_a_decimal

base_B_a_decimal(numero_str: str, base: int) -> int
```

### Parámetros

- `numero_str` (str): Representación en base B
- `base` (int): Base origen (2-36)

### Retorna

- `int`: Valor en decimal (base 10)

### Ejemplos

```python
# Base 5
base_B_a_decimal("30434", 5)    # → 1994

# Base 2 (Binario)
base_B_a_decimal("11111111", 2) # → 255

# Base 16 (Hexadecimal)
base_B_a_decimal("ff", 16)      # → 255

# Base 8 (Octal)
base_B_a_decimal("144", 8)      # → 100
```

### Algoritmo: Polinomio de Horner

```python
# Método tradicional (potencias):
# Número = d₄×5⁴ + d₃×5³ + d₂×5² + d₁×5¹ + d₀×5⁰
# = 3×625 + 0×125 + 4×25 + 3×5 + 4×1 = 1994

# Método Horner (más eficiente):
((((3 × 5 + 0) × 5 + 4) × 5 + 3) × 5 + 4) = 1994
```

### Referencias en Temario

- **2.1.1.3**: Conversión de Base B a Base 10

---

## 3️⃣ `base_B_a_base_B_prima(numero_str, base_origen, base_destino) -> str`

Conversión **genérica entre dos bases B y B'** cualquiera.

### Firma Completa

```python
from core.sistemas_numeracion_basicos import base_B_a_base_B_prima

base_B_a_base_B_prima(numero_str: str, base_origen: int, base_destino: int) -> str
```

### Parámetros

- `numero_str` (str): Número en base B
- `base_origen` (int): Base B (2-36)
- `base_destino` (int): Base B' (2-36)

### Retorna

- `str`: Representación en base B'

### Ejemplos

```python
# Base 5 → Base 2
base_B_a_base_B_prima("30434", 5, 2)  # → "11111001010"

# Base 16 → Base 10
base_B_a_base_B_prima("ff", 16, 10)   # → "255"

# Base 2 → Base 8
base_B_a_base_B_prima("1010", 2, 8)   # → "12"

# Base 8 → Base 16
base_B_a_base_B_prima("144", 8, 16)   # → "64"
```

### Algoritmo: Conversión a través de Decimal

```
1. Base B → Decimal:  "30434"₅ → 1994₁₀
2. Decimal → Base B': 1994₁₀ → "11111001010"₂
```

### Ventajas y Desventajas

| Aspecto | Valor |
|---------|-------|
| **Simplicidad** | ✅ Alta |
| **Eficiencia** | ⚠️ Media (pasa por decimal) |
| **Uso** | ✅ General (cualquier par de bases) |
| **Precisión** | ✅ Exacta para enteros |

### Referencias en Temario

- **2.1.1.3**: Conversión entre Sistemas de Numeración

---

## 4️⃣ `base_B_a_base_B_prima_potencias(numero_str, base_comun, exponente_origen, exponente_destino) -> str`

Conversión **optimizada para bases relacionadas** donde:

- Base origen: $B = b^n$
- Base destino: $B' = b^{n'}$

### Firma Completa

```python
from core.sistemas_numeracion_basicos import base_B_a_base_B_prima_potencias

base_B_a_base_B_prima_potencias(numero_str: str, 
                                base_comun: int, 
                                exponente_origen: int, 
                                exponente_destino: int) -> str
```

### Parámetros

- `numero_str` (str): Número en base B = b^n
- `base_comun` (int): Base b (2, 3, 5, etc.)
- `exponente_origen` (int): n tal que B = b^n
- `exponente_destino` (int): n' tal que B' = b^(n')

### Retorna

- `str`: Representación en base B'

### Ejemplos

#### Binario ↔ Hexadecimal (b=2, B=2¹, B'=2⁴)

```python
# Binario (2¹) → Hexadecimal (2⁴)
base_B_a_base_B_prima_potencias("11111111", 2, 1, 4)
# → "ff"
# Agrupa 4 dígitos binarios: 1111|1111 = F|F = FF₁₆

# Hexadecimal (2⁴) → Binario (2¹)
base_B_a_base_B_prima_potencias("ff", 2, 4, 1)
# → "11111111"
```

#### Binario ↔ Octal (b=2, B=2¹, B'=2³)

```python
# Binario (2¹) → Octal (2³)
base_B_a_base_B_prima_potencias("1111", 2, 1, 3)
# → "17"
# Agrupa 3 dígitos: 001|111 = 1|7 = 17₈

# Octal (2³) → Binario (2¹)
base_B_a_base_B_prima_potencias("17", 2, 3, 1)
# → "1111" (o "001111" con padding)
```

#### Base 3 ↔ Base 27 (b=3, B=3¹, B'=3³)

```python
# Base 3 (3¹) → Base 27 (3³)
base_B_a_base_B_prima_potencias("010021002", 3, 1, 3)
# → "122"
# Agrupa 3 dígitos: 010|021|002 = 1|2|2
```

### Algoritmo: Agrupación de Dígitos

#### Caso: Binario → Hexadecimal

```
1. Expandir: "ff"₁₆ → cada dígito hex a 4 dígitos binarios
   f = 1111, f = 1111
   Resultado: "11111111"₂

2. Agrupar (inversión): "11111111"₂ → agrupar en 4
   1111|1111 → f|f → "ff"₁₆
```

#### Proceso General

```
Paso 1: B → b (expandir exponente_origen dígitos)
        Cada dígito de base B = b^n se expande a n dígitos de base b

Paso 2: b → B' (agrupar exponente_destino dígitos)
        Se agrupan n' dígitos de base b para formar un dígito de base B' = b^(n')
```

### Ventajas y Desventajas

| Aspecto | Valor |
|---------|-------|
| **Simplicidad** | ⚠️ Media |
| **Eficiencia** | ✅ Alta (sin aritmética) |
| **Uso** | ⚠️ Solo bases relacionadas |
| **Precisión** | ✅ Exacta |
| **Casos de uso** | Binario↔Hex, Binario↔Octal, etc. |

### Casos de Uso Comunes

**Sistemas Digitales**:

```python
# En electrónica digital es muy común
# convertir entre estas bases:

# 1 byte en hexadecimal
base_B_a_base_B_prima_potencias("ff", 2, 4, 1)  # → Binario

# 3 bits en octal
base_B_a_base_B_prima_potencias("377", 2, 3, 1)  # → Binario
```

### Referencias en Temario

- **2.1.1.5.3**: Conversión entre binario, octal y hexadecimal
- **2.1.1.5.4**: Sistema de conversión entre representación de bases relacionadas

---

## 📊 Comparación de Métodos

| Aspecto | `base_B_a_base_B_prima()` | `base_B_a_base_B_prima_potencias()` |
|---------|--------------------------|-------------------------------------|
| **Bases soportadas** | Cualquier par (2-36) | Solo relacionadas (b^n ↔ b^m) |
| **Algoritmo** | Decimal intermedio | Agrupación de dígitos |
| **Eficiencia** | ⚠️ Media | ✅ Alta |
| **Precisión** | ✅ Exacta | ✅ Exacta |
| **Implementación** | Simple | Más compleja |
| **Mejor para** | Conversiones generales | Bases 2, 8, 16, etc. |

---

## 🧪 Test Suite Completo

Todos los tests pasados (15/15):

```
Test 1: decimal_a_base_B
  ✓ 1994 → base 5
  ✓ 255 → base 2
  ✓ 255 → base 16

Test 2: base_B_a_decimal
  ✓ "30434" en base 5
  ✓ "11111111" en base 2
  ✓ "ff" en base 16

Test 3: base_B_a_base_B_prima
  ✓ "30434"₅ → base 2
  ✓ "ff"₁₆ → base 10
  ✓ "1010"₂ → base 8

Test 4: base_B_a_base_B_prima_potencias
  ✓ "11111111"₂ → base 16
  ✓ "ff"₁₆ → base 2
  ✓ "1111"₂ → base 8
```

---

## 📌 Guía Rápida de Elección

¿Qué función usar?

```
¿Necesitas convertir de decimal?
├─ SÍ → decimal_a_base_B()

¿Necesitas convertir a decimal?
├─ SÍ → base_B_a_decimal()

¿Necesitas convertir entre dos bases B y B'?
├─ ¿Son bases relacionadas (2-8, 2-16, 3-9, etc.)?
│  ├─ SÍ → base_B_a_base_B_prima_potencias() (más rápido)
│  └─ NO → base_B_a_base_B_prima() (general)
```

---

## 🔗 Referencias en el Temario

- **2.1.1.1**: Sistemas Posicionales y No Posicionales
- **2.1.1.2**: Unicidad de la Representación
- **2.1.1.3**: Conversión entre Sistemas de Numeración
- **2.1.1.5.3**: Conversión entre binario, octal y hexadecimal
- **2.1.1.5.4**: Sistema de conversión entre representación de bases relacionadas
- **2.1.1.6.1**: Representación en Longitud Fija

---

## 💻 Ubicación en el Código

**Archivo**: [core/sistemas_numeracion_basicos.py](core/sistemas_numeracion_basicos.py)

**Sección**: PARTE 6: CONVERSIONES GENÉRICAS ENTRE BASES

**Líneas**: Aproximadamente líneas 503-700

---

## 📚 Recursos Adicionales

- **Demo**: [demo_conversiones_entre_bases.py](demo_conversiones_entre_bases.py) (si existe)
- **Tests**: [test_conversiones_genericas.py](test_conversiones_genericas.py)
- **Teoría**: Ver secciones 2.1.1.3 y 2.1.1.5 en [CONTENIDOS_FE.md](CONTENIDOS_FE.md)
