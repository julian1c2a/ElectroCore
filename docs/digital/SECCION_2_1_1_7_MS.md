# 📝 Sección 2.1.1.7: Números Enteros con Signo

## Parte 1: Magnitud y Signo (M&S)

### Introducción

La representación en **Magnitud y Signo** es la forma más **intuitiva** de representar números enteros con signo en binario, porque es exactamente como escribimos números con lápiz y papel.

**Método manual:**

- Escribimos un signo: + o -
- Escribimos una magnitud (valor absoluto): 86
- Resultado: +86 o -86

**Método binario M&S:**

- Usamos un **bit de signo** (el MSB, índice n-1)
  - 0 = positivo (+)
  - 1 = negativo (-)
- Usamos los **bits restantes** para la magnitud (MSB-1 hasta LSB)
- Con n bits podemos representar: [-2^(n-1) + 1, 2^(n-1) - 1]

### Estructura en Memoria

Para un número de **8 bits** en M&S:

```
Número: +86 en decimal
┌─────────────────────────────────┐
│ 0 1 0 1 0 1 1 0 │  = +86
│ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
│ s m m m m m m m │  (s=signo, m=magnitud)
│ 7 6 5 4 3 2 1 0 │  (índices de bit, MSB...LSB)
└─────────────────────────────────┘

Bit 7 (MSB): 0 → positivo
Bits 6-0: 1010110₂ = 86₁₀
Valor = +86

Número: -86 en decimal
┌─────────────────────────────────┐
│ 1 1 0 1 0 1 1 0 │  = -86
│ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
│ s m m m m m m m │
│ 7 6 5 4 3 2 1 0 │
└─────────────────────────────────┘

Bit 7 (MSB): 1 → negativo
Bits 6-0: 1010110₂ = 86₁₀
Valor = -86
```

### Conversión: Decimal ↔ M&S

**Algoritmo: Decimal → M&S (n bits)**

```
1. Si número >= 0:
   - Bit de signo = 0
   - Magnitud = número en binario (n-1 bits)
2. Si número < 0:
   - Bit de signo = 1
   - Magnitud = |número| en binario (n-1 bits)
3. Concatenar: signo_bit + magnitud_bits
```

**Algoritmo: M&S → Decimal**

```
1. Extraer bit de signo (bit n-1)
2. Extraer bits de magnitud (bits n-2 a 0)
3. Convertir magnitud de binario a decimal
4. Si signo = 1, negamos el resultado
```

**Ejemplo:**

```
decimal_a_ms(86, 8):
  Número positivo → bit signo = 0
  Magnitud = 86₁₀ = 1010110₂ (7 bits)
  Resultado: 0 + 1010110 = 01010110

decimal_a_ms(-86, 8):
  Número negativo → bit signo = 1
  Magnitud = 86₁₀ = 1010110₂ (7 bits)
  Resultado: 1 + 1010110 = 11010110

ms_a_decimal('01010110'):
  Bit signo (índice 7) = 0 → positivo
  Magnitud (índices 6-0) = 1010110₂ = 86₁₀
  Resultado: +86

ms_a_decimal('11010110'):
  Bit signo (índice 7) = 1 → negativo
  Magnitud (índices 6-0) = 1010110₂ = 86₁₀
  Resultado: -86
```

### Rango de Representación

Para **n bits** en M&S:

| Aspecto | Fórmula | Valores (n=8) |
|---------|---------|---------------|
| Bits de magnitud | n - 1 | 7 |
| Número más negativo | -(2^(n-1) - 1) | -127 |
| -1 | -1 | -1 |
| Cero (dos veces) | 0 | +0 y -0 |
| +1 | 1 | 1 |
| Número más positivo | 2^(n-1) - 1 | 127 |
| Rango total | [-(2^(n-1) - 1), 2^(n-1) - 1] | [-127, 127] |
| Valores únicos | 2^n - 1 | 255 |
| Eficacia | 1 - (1/2^n) | 99.61% |

**Nota:** La capacidad es 2^n - 1, no 2^n, porque hay DOS representaciones para el 0:

- +0: 00000000 (signo 0, magnitud 0)
- -0: 10000000 (signo 1, magnitud 0)

### Operaciones en M&S

#### 1. Negación (Multiplicar por -1)

**Operación:** Invertir (flip) el bit de signo

```
+86 (01010110) → Flip bit 7 → 11010110 (-86)
-86 (11010110) → Flip bit 7 → 01010110 (+86)
+0  (00000000) → Flip bit 7 → 10000000 (-0, pero sigue siendo 0)
```

**En hardware:** Una sola operación de XOR del MSB con 1

#### 2. Comparación

La comparación en M&S es compleja porque para números negativos la relación se invierte:

```
Para números positivos:
  Si |A| > |B| entonces A > B ✓

Para números negativos:
  Si |A| > |B| entonces A < B ✗ (INVERTIDO)

Ejemplo:
  -100 < -50, pero |−100| > |−50|
```

#### 3. Multiplicación y División

Se realiza sobre las magnitudes, ajustando el signo al final:

```
A × B:
  1. Calcular |A| × |B|
  2. Si signo(A) = signo(B) entonces signo resultado = 0 (+)
  3. Si signo(A) ≠ signo(B) entonces signo resultado = 1 (-)

Ejemplo:
  +5 × -3 = -(5 × 3) = -15
  -5 × -3 = +(5 × 3) = +15
```

### Ventajas y Desventajas

#### ✅ VENTAJAS

1. **Intuitivo:** Exactamente como escribimos números a mano
   - Signo explícito y visible
   - Fácil de reconocer por humanos

2. **Negación simple:** Una sola operación
   - Flip del bit MSB
   - Rapidísimo en hardware

3. **Multiplicación/División simples**
   - Operación sobre magnitudes
   - Ajuste de signo por regla simple

#### ❌ DESVENTAJAS

1. **DOS REPRESENTACIONES PARA CERO**
   - +0: 00000000
   - -0: 10000000
   - Ambas representan el número 0
   - Desperdicia una combinación
   - Comparación de igualdad es más compleja

2. **SUMA Y RESTA COMPLICADAS**
   - Positivo + Positivo → suma directa
   - Negativo + Negativo → suma de magnitudes, resultado negativo
   - Positivo + Negativo → necesita comparación y resta
   - Diferentes algoritmos según los signos
   - Mucho más lento que Complemento a 2

3. **COMPARACIÓN INVERTIDA PARA NEGATIVOS**
   - Para positivos: mayor magnitud = mayor número
   - Para negativos: mayor magnitud = MENOR número
   - Ejemplo: -100 < -50 pero |−100| > |−50|
   - Necesita lógica especial en comparador

4. **BAJA EFICIENCIA TEÓRICA**
   - Solo 2^n - 1 valores representables
   - Eficacia: (2^n - 1) / 2^n = 1 - 1/2^n
   - Siempre hay una combinación desperdiciada

### Implementación en Python

```python
from core.enteros_signados import (
    decimal_a_ms,           # Decimal → M&S
    ms_a_decimal,           # M&S → Decimal
    negacion_ms,            # Invertir signo
    rango_ms,               # Rango de representación
    explicar_conversion_ms, # Explicación paso a paso
)

# Conversiones
ms8 = decimal_a_ms(86, 8)      # '01010110'
valor = ms_a_decimal('11010110')  # -86

# Operaciones
negado = negacion_ms('01010110')   # '11010110' (+86 → -86)

# Análisis
info = rango_ms(8)
print(f"Rango: {info['rango_total']}")      # (-127, 127)
print(f"Capacidad: {info['capacidad']}")    # 255
print(f"Eficacia: {info['porcentaje_eficacia']}")  # 99.61%
```

### Demostración

Ejecutar:

```bash
python demo_ms_simple.py
```

Contiene 5 demostraciones:

1. Conceptos básicos
2. Rango y capacidad para diferentes tamaños
3. Conversiones paso a paso
4. Operaciones (negación, consultas)
5. Ventajas y desventajas

---

## Siguientes Temas

### 2.1.1.7.2 Complemento a la Base B (Complemento a 1 y Complemento a 2)

Los sistemas de **complemento** resuelven los problemas de M&S:

**Complemento a 1 (C1):**

- Negación: invertir TODOS los bits
- Sigue teniendo dos 0s

**Complemento a 2 (C2):**

- Negación: invertir todos los bits + sumar 1
- Una única representación para 0
- Suma y resta simples (mismo algoritmo)
- **ESTÁNDAR en sistemas modernos**

---

## Recursos

- **Módulo:** `core/enteros_signados.py`
- **Demo:** `demo_ms_simple.py`
- **Documentación:** Este archivo
- **Tests:** Próximamente

---

**Sección:** 2.1.1.7  
**Tema:** Números Enteros con Signo - Magnitud y Signo (M&S)  
**Estado:** ✅ IMPLEMENTADO  
**Próximo:** Complemento a la Base B
