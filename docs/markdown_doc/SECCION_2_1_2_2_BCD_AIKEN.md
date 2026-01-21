# Sección 2.1.2.2 - BCD Aiken (2-4-2-1)

**Código Autocomplementario con Pesos**

---

## 📌 Concepto Fundamental

### Definición

**BCD Aiken** es un sistema de codificación de **dígitos decimales** donde cada dígito se representa mediante 4 bits con **pesos 2-4-2-1** (en lugar de los tradicionales 8-4-2-1).

La característica clave es que **es autocomplementario**: el complemento a 9 de un dígito se obtiene invirtiendo todos los bits.

### Historia

Fue inventado por **Howard Hathaway Aiken** en los años 1940 para la computadora **Mark I**, buscando un sistema que combinara:

- **Pesos definidos** (como BCD Natural)
- **Autocomplementariedad** (como Exceso-3)

---

## 🔢 Tabla de Correspondencia: BCD Aiken (2-4-2-1)

| Decimal | Pesos 2-4-2-1 | Binario Tradicional | Decimal | Pesos 2-4-2-1 | Binario Tradicional |
|---------|---|---|---------|---|---|
| 0 | **0000** | 0000 | 5 | ---- | 0101 |
| 1 | **0001** | 0001 | 6 | **1100** | 0110 |
| 2 | **0010** | 0010 | 7 | **1101** | 0111 |
| 3 | **0011** | 0011 | 8 | **1110** | 1000 |
| 4 | **0100** | 0100 | 9 | **1111** | 1001 |

**Observación:** Los dígitos 5-9 **no aparecen en la secuencia natural 0-4**.

### Pesos en Aiken

```
Bits: b3  b2  b1  b0
      |   |   |   |
Pesos: 2   4   2   1

Valor = b3×2 + b2×4 + b1×2 + b0×1
```

### Tabla Completa con Cálculos

| Decimal | $b_3$ | $b_2$ | $b_1$ | $b_0$ | Código Aiken | Cálculo: $2b_3 + 4b_2 + 2b_1 + b_0$ |
|---------|-------|-------|-------|-------|---|---|
| 0 | 0 | 0 | 0 | 0 | 0000 | 0 ✓ |
| 1 | 0 | 0 | 0 | 1 | 0001 | 1 ✓ |
| 2 | 0 | 0 | 1 | 0 | 0010 | 2 ✓ |
| 3 | 0 | 0 | 1 | 1 | 0011 | 3 ✓ |
| 4 | 0 | 1 | 0 | 0 | 0100 | 4 ✓ |
| 5 | 1 | 0 | 1 | 1 | 1011 | 2 + 2 + 1 = 5 ✓ |
| 6 | 1 | 1 | 0 | 0 | 1100 | 2 + 4 = 6 ✓ |
| 7 | 1 | 1 | 0 | 1 | 1101 | 2 + 4 + 1 = 7 ✓ |
| 8 | 1 | 1 | 1 | 0 | 1110 | 2 + 4 + 2 = 8 ✓ |
| 9 | 1 | 1 | 1 | 1 | 1111 | 2 + 4 + 2 + 1 = 9 ✓ |

**Nota:** Solo 10 combinaciones son válidas en Aiken (0000-0100, 1011-1111). Las 6 combinaciones 0101-1010 son "prohibidas".

---

## ✅ Validación de Códigos Aiken

### ¿Cómo Saber si un Código es Aiken Válido?

Dado un código de 4 bits: $d_3 d_2 d_1 d_0$

**Un código es Aiken ERRÓNEO basándose en:**

- **Si $d_3 = d_2$:** El código es **válido** (sin importar bits 1 y 0)
- **Si $d_3 \neq d_2$:** El código es válido **SOLO SI** $d_3 = d_1 = d_0$

En otras palabras:
$$\text{Válido} \iff [d_3 = d_2] \text{ O } [d_3 = d_1 = d_0]$$

**Ejemplos de validación:**

```
0000 → d3=0, d2=0  → d3=d2 → ✅ VÁLIDO (0)
0001 → d3=0, d2=0  → d3=d2 → ✅ VÁLIDO (1)
0100 → d3=0, d2=1  → d3≠d2, ¿d3=d1=d0? (0=0=0?) NO → ❌ INVÁLIDO
1011 → d3=1, d2=0  → d3≠d2, ¿d3=d1=d0? (1=1=1?) SÍ → ✅ VÁLIDO (5)
1100 → d3=1, d2=1  → d3=d2 → ✅ VÁLIDO (6)
1111 → d3=1, d2=1  → d3=d2 → ✅ VÁLIDO (9)
0101 → d3=0, d2=1  → d3≠d2, ¿d3=d1=d0? (0=0=1?) NO → ❌ INVÁLIDO
1110 → d3=1, d2=1  → d3=d2 → ✅ VÁLIDO (8)
```

**Tabla de validación completa:**

| Código | d3 | d2 | d1 | d0 | d3=d2? | d3=d1=d0? | ¿Válido? |
|--------|----|----|----|----|--------|-----------|----------|
| 0000 | 0 | 0 | 0 | 0 | SÍ | - | ✅ |
| 0001 | 0 | 0 | 0 | 1 | SÍ | - | ✅ |
| 0010 | 0 | 0 | 1 | 0 | SÍ | - | ✅ |
| 0011 | 0 | 0 | 1 | 1 | SÍ | - | ✅ |
| 0100 | 0 | 1 | 0 | 0 | NO | NO | ❌ |
| 0101 | 0 | 1 | 0 | 1 | NO | NO | ❌ |
| 0110 | 0 | 1 | 1 | 0 | NO | NO | ❌ |
| 0111 | 0 | 1 | 1 | 1 | NO | NO | ❌ |
| 1000 | 1 | 0 | 0 | 0 | NO | NO | ❌ |
| 1001 | 1 | 0 | 0 | 1 | NO | NO | ❌ |
| 1010 | 1 | 0 | 1 | 0 | NO | NO | ❌ |
| 1011 | 1 | 0 | 1 | 1 | NO | SÍ | ✅ |
| 1100 | 1 | 1 | 0 | 0 | SÍ | - | ✅ |
| 1101 | 1 | 1 | 0 | 1 | SÍ | - | ✅ |
| 1110 | 1 | 1 | 1 | 0 | SÍ | - | ✅ |
| 1111 | 1 | 1 | 1 | 1 | SÍ | - | ✅ |

---

## 🎯 Propiedad Fundamental: Autocomplementariedad

### Verificación de Autocomplementariedad

En Aiken, el complemento a 9 de un dígito $d$ es:

$$\text{Aiken}(\overline{9-d}) = \neg \text{Aiken}(d)$$

**Tabla de verificación:**

| Dígito | Complemento a 9 | Aiken(d) | NOT Aiken(d) | Aiken(9-d) | ¿Iguales? |
|--------|----------------|-----------|-----------|-----------|----|
| 0 | 9 | 0000 | 1111 | 1111 | ✅ |
| 1 | 8 | 0001 | 1110 | 1110 | ✅ |
| 2 | 7 | 0010 | 1101 | 1101 | ✅ |
| 3 | 6 | 0011 | 1100 | 1100 | ✅ |
| 4 | 5 | 0100 | 1011 | 1011 | ✅ |
| 5 | 4 | 1011 | 0100 | 0100 | ✅ |
| 6 | 3 | 1100 | 0011 | 0011 | ✅ |
| 7 | 2 | 1101 | 0010 | 0010 | ✅ |
| 8 | 1 | 1110 | 0001 | 0001 | ✅ |
| 9 | 0 | 1111 | 0000 | 0000 | ✅ |

**Conclusión:** Aiken es **perfectamente autocomplementario** 🎯

### ¿Por Qué Funciona la Autocomplementariedad?

Matemáticamente en pesos 2-4-2-1:

$$\text{Aiken}(d) = 2b_3 + 4b_2 + 2b_1 + b_0 = d$$

$$\text{Aiken}(\overline{9-d}) = 2\overline{b_3} + 4\overline{b_2} + 2\overline{b_1} + \overline{b_0}$$

donde $\overline{b_i}$ es el bit invertido.

$$= 2(1-b_3) + 4(1-b_2) + 2(1-b_1) + (1-b_0)$$
$$= 2 + 4 + 2 + 1 - (2b_3 + 4b_2 + 2b_1 + b_0)$$
$$= 9 - d \text{ ✓}$$

Por lo tanto: $\neg \text{Aiken}(d) = \text{Aiken}(9-d)$ 🎓

---

## ➕ Aritmética en Aiken

### Suma Básica

La suma en Aiken es más sencilla que en Exceso-3 porque **tiene pesos**, pero aún requiere corrección:

**Algoritmo:**

1. Sumar los códigos Aiken como binarios
2. Si el resultado es > 9 o hay acarreo involucrado, aplicar corrección
3. La corrección es específica según si hay acarreo

### Ejemplo 1: Suma sin acarreo (0-4 + 0-4)

```
Suma: 2 + 3 en Aiken

2 en Aiken: 0010
+ 3 en Aiken: 0011
-----------
           0101 (es una combinación prohibida)

Necesita corrección: 0101 + 0011 = 1000 (8 en Aiken)

Pero 2 + 3 = 5, no 8. Este cálculo es incorrecto.

Intento correcto:
2 + 3 = 5
5 en Aiken = 1011

Suma binaria: 0010 + 0011 = 0101
             0101 es "inválido" en Aiken
             Corrección: sumar 6 (0110)
             0101 + 0110 = 1011 ✓ (que es 5 en Aiken)
```

### Ejemplo 2: Suma con acarreo (dígitos 5-9)

```
Suma: 7 + 5 en Aiken

7 en Aiken: 1101
+ 5 en Aiken: 1011
-----------
          11000 (hay acarreo de 1)

Interpretación: Acarreo + 0000
La suma correcta sería 12 (7+5), que se representa como 1 (acarreo) y 2.

Corrección necesaria...
```

### Resta mediante Complemento a 9

Tal como en Exceso-3, la resta en Aiken se puede realizar mediante complemento a 9:

$$A - B = A + (\text{Complemento a 9 de } B) - 9$$

**Ventaja del complemento en Aiken:** Es simplemente invertir todos los bits ✓

---

## 📊 Propiedades de Aiken

| Propiedad | Valor |
|-----------|-------|
| **Bits por dígito** | 4 |
| **Rango por dígito** | 0-9 |
| **Eficacia** | 62.5% (10/16) |
| **Tiene pesos** | **SÍ (2-4-2-1)** |
| **Autocomplementario** | **SÍ** ✅ |
| **Valores válidos** | 0000-0100, 1011-1111 |
| **Valores inválidos** | 0101-1010 |
| **Suma directa** | NO (requiere corrección) |
| **Comparación directa** | Limitada (no es simple) |

---

## 🔢 Representación de Números Signados

### Mediante Complemento a 9

Para representar un número negativo $-d$, se usa su complemento a 9:

$$-d = \text{Aiken}(9-d)$$

**Ejemplo: -3 en Aiken**

```
3 en Aiken: 0011
Complemento a 9: 9 - 3 = 6
6 en Aiken: 1100

Por lo tanto: -3 se representa como 1100 en Aiken
(que es el código de +6)
```

### Números Multidígitos Signados

```
Número: -27

27 en Aiken: 0010 0111
           (2)   (7)

Complemento a 9:
- Dígito 2 → 9 - 2 = 7 → 1101
- Dígito 7 → 9 - 7 = 2 → 0010

-27 en Aiken: 1101 0010
```

---

## 🎯 Comparativa: BCD Natural vs Exceso-3 vs Aiken

| Característica | BCD Natural | Exceso-3 | Aiken |
|---|---|---|---|
| **Codificación** | $d$ | $d+3$ | Pesos 2-4-2-1 |
| **Pesos** | SÍ (8,4,2,1) | NO | **SÍ (2,4,2,1)** |
| **Eficacia** | 62.5% | 62.5% | 62.5% |
| **Autocomplementario** | NO | SÍ | **SÍ** |
| **Suma simple** | NO | NO | NO |
| **Comparación** | **SÍ** | NO | NO |
| **Números signados** | Difícil | Fácil | **Fácil** |
| **Multiplicación** | Compleja | Compleja | **Ligeramente menos** |
| **Época de uso** | Entrada/salida | Electromecánica | **Computadoras Mark I** |

---

## 💡 Ventajas y Desventajas

### ✅ Ventajas

1. **Autocomplementariedad:** Complemento a 9 es invertir bits (trivial)
2. **Pesos definidos:** Permite ciertas operaciones aritméticas más directas
3. **Números signados:** Fácil representación mediante complemento
4. **Mejor balance:** Intenta combinar lo mejor de BCD Natural y Exceso-3
5. **Detección de errores:** Valores inválidos (0101-1010) pueden indicar errores

### ❌ Desventajas

1. **Suma aún compleja:** Requiere corrección similar a otros códigos BCD
2. **Pesos irregulares:** 2-4-2-1 son menos intuitivos que 8-4-2-1
3. **Sin comparación directa:** A diferencia de BCD Natural
4. **Menos histórico:** BCD Natural (8-4-2-1) fue más estándar
5. **Multiplicación compleja:** Como todos los códigos BCD

---

## 📊 Eficacia y Capacidad

### Comparativa de Eficacia

Los tres códigos BCD tienen la **misma eficacia** (62.5%) porque todos usan 4 bits para 10 dígitos:

$$\text{Eficacia} = \frac{10}{16} = 62.5\%$$

**Comparación con Números Naturales Binarios:**

| Sistema | Rango | Bits | Eficacia |
|---------|-------|------|----------|
| Binarios naturales | 0-9 | 4 | 100% (10/10) |
| BCD Natural | 0-9 | 4 | 62.5% (10/16) |
| BCD Exc3 | 0-9 | 4 | 62.5% (10/16) |
| BCD Aiken | 0-9 | 4 | 62.5% (10/16) |

---

## 🔗 Relación con Complementación a 9

**Ventaja única de Aiken y Exceso-3:** La complementación a 9 es **trivial**

```
Para restar B de A en Aiken:
1. Obtener 9 - B: Invertir todos los bits de B
2. Sumar A + (9 - B) con correcciones
3. Ajustar resultado

Compare con números signados tradicionales:
- Debe calcular 9 - B manualmente
- Luego convertir a representación signada
- Mucho más complejo
```

---

## 📍 Casos Especiales

### 1. Códigos Válidos vs Inválidos

En Aiken, exactamente **6 combinaciones son inválidas**:

```
Válidos:   0000-0100, 1011-1111 (10 códigos)
Inválidos: 0101-1010 (6 códigos)
```

Esto permite **detección de errores simple**: si aparece un código inválido, hay error de transmisión o corrupción.

### 2. Conversión a/desde BCD Natural

```
BCD Natural 5 = 0101

Buscar equivalente en Aiken:
5 en Aiken = 1011

Conversion necesaria:
0101 (BCD) → Se interpreta como 5 → Buscar 5 en Aiken = 1011
```

### 3. Números muy grandes

```
Número: 9876543210

Cada dígito en Aiken (4 bits):
9 → 1111
8 → 1110
7 → 1101
6 → 1100
5 → 1011
4 → 0100
3 → 0011
2 → 0010
1 → 0001
0 → 0000

Representación completa (40 bits):
1111 1110 1101 1100 1011 0100 0011 0010 0001 0000
```

---

## 🎓 Historia: ¿Por Qué Aiken?

### El Problema que Resolvía

En los años 1940, **Howard Aiken** buscaba un sistema numérico para la **Mark I** que fuera:

1. **Eficiente computacionalmente:** Pesos definidos para cálculos
2. **Eficiente en complementación:** Para restar (fácil con números negativos)
3. **Universalmente válido:** Trabajar con complemento a 9 de forma natural

BCD Natural tenía pesos pero no autocomplementariedad.
Exceso-3 tenía autocomplementariedad pero sin pesos.

**Aiken = Solución intermedia: Los mejores de ambos mundos**

### Computadora Mark I (1944)

```
Mark I specifications:
- Máquina electromecánica
- Calculadora decimal
- ~3 metros de largo
- 5 toneladas
- Usaba relés electromagnéticos
- Requería operaciones aritmét.
  eficientes

Aiken BCD (2-4-2-1) fue
la solución elegida
```

### Evolución Histórica

```
1940: BCD Natural (8-4-2-1) → Entrada/salida
1940: Exceso-3 → Algunas máquinas con complementación
1944: BCD Aiken (2-4-2-1) → Mark I de Harvard
1950s: Computadoras decimales tempranas
1960s-70s: COBOL usa BCD Natural
1980s+: Prefieren binarios puros, BCD relegado a I/O
```

---

## 📝 Resumen

| Característica | Aiken (2-4-2-1) |
|---|---|
| **Nombre** | BCD Aiken |
| **Pesos** | 2-4-2-1 |
| **Bits por dígito** | 4 |
| **Eficacia** | 62.5% |
| **Autocomplementario** | **SÍ** ✅ |
| **Códigos válidos** | 10 (0000-0100, 1011-1111) |
| **Códigos inválidos** | 6 (0101-1010) |
| **Suma** | Requiere corrección |
| **Complemento a 9** | Invertir bits |
| **Números signados** | Mediante complemento a 9 |
| **Uso histórico** | Mark I (1944) |
| **Uso actual** | Principalmente educativo |
| **Inventor** | Howard Hathaway Aiken |
| **Año** | 1944 |

---

## 🔄 Tabla Comparativa: Los 3 Códigos BCD

```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│   Dígito        │ BCD Natural  │ Exceso-3     │ Aiken (2421) │
│                 │   (8421)     │              │              │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 0               │ 0000         │ 0011         │ 0000         │
│ 1               │ 0001         │ 0100         │ 0001         │
│ 2               │ 0010         │ 0101         │ 0010         │
│ 3               │ 0011         │ 0110         │ 0011         │
│ 4               │ 0100         │ 0111         │ 0100         │
│ 5               │ 0101         │ 1000         │ 1011         │
│ 6               │ 0110         │ 1001         │ 1100         │
│ 7               │ 0111         │ 1010         │ 1101         │
│ 8               │ 1000         │ 1011         │ 1110         │
│ 9               │ 1001         │ 1100         │ 1111         │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Autocomplementario │ NO        │ SÍ           │ SÍ           │
│ Tiene pesos     │ SÍ (8,4,2,1) │ NO           │ SÍ (2,4,2,1) │
│ Comparación     │ Directa      │ NO           │ NO           │
│ Suma simple     │ NO           │ NO           │ NO           │
│ Época uso       │ Entrada/sal. │ 1940s-1970s  │ Mark I (44)  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 🚀 Conclusión

BCD Aiken fue un esfuerzo brillante por **combinar los mejores atributos** de BCD Natural y Exceso-3:

- ✅ Pesos definidos (como BCD Natural)
- ✅ Autocomplementariedad (como Exceso-3)
- ⚠️ Pero sacrificando comparación directa y manteniendo suma compleja

Hoy es principalmente **histórico/educativo**, pero conceptualmente importante para entender la evolución de sistemas numéricos.

---

**Documentación Relacionada:**

- [BCD Natural (8421)](SECCION_2_1_2_BCD_NATURAL.md)
- [BCD Exceso-3](SECCION_2_1_2_1_BCD_EXC3.md)
- [Números Enteros Signados](SECCION_2_1_1_7_MS.md) ← Ver cómo Aiken facilita aritmética signada
