# 📝 Sección 2.1.1.7.3: Complemento a la Base (CB)

## Introducción: La Representación Estándar

**Complemento a la Base (CB)** es la forma **estándar e industrial** de representar números enteros con signo en todos los computadores modernos.

A diferencia de:

- **M&S:** Dos representaciones para 0, comparación complicada
- **CB-1:** Dos representaciones para 0, suma requiere end-around carry
- **CB:** Una única representación para 0, suma = suma ordinaria

---

## Parte 1: La Operación opCB

### Definición

La operación **opCB(B, cadena)** tiene dos pasos:

**Paso 1: Flip cada dígito** (opCBm1)
$$d[i] \rightarrow B - 1 - d[i]$$

**Paso 2: Sumar 1 al resultado total**

### Equivalencia

$$\text{opCB}(B, \text{cadena}) = B^l - \text{eval}(\text{cadena})$$

Donde $l$ es la longitud de la cadena.

### Ejemplos

**Base 10, 5 dígitos:**

```
Paso 1 (flip):  01239 → 98760  (cada dígito: 0→9, 1→8, 2→7, 3→6, 9→0)
Paso 2 (suma 1): 98760 + 1 = 98761

Verificación: 100000 - 1239 = 98761  ✓
```

**Base 2, 4 bits:**

```
Paso 1 (flip):  0101 → 1010  (cada bit: 0→1, 1→0)
Paso 2 (suma 1): 1010 + 1 = 1011

Verificación: 16 - 5 = 11 = 1011₂  ✓
```

### Propiedades

**Propiedad 1: Identidad al aplicar dos veces**
$$\text{opCB}(\text{opCB}(D)) = D$$

**Demostración:**

```
opCB(opCB(d)) = opCB(B - 1 - d) 
              = (B - 1 - (B - 1 - d)) + 1 - 1
              = d  ✓
```

**Propiedad 2: Inversión exacta de valor**
Si interpretamos opCB(d) como número en base B:
$$\text{eval}(\text{opCB}(D)) \equiv -\text{eval}(D) \pmod{B^l}$$

---

## Parte 2: Representación en Complemento a la Base

### Definición

Una palabra de longitud $l$ en base $B$ representa un número entero mediante:

**Para número ≥ 0:**
Represéntalo directamente en $l$ dígitos

**Para número < 0:**
Representa como $B^l - |número|$ en $l$ dígitos

### Equivalencia Modular

$$\text{ReprCB}(número) = número \bmod B^l$$

Esta simple operación modular maneja automáticamente tanto positivos como negativos.

### Ejemplos

**Base 10, 5 dígitos:**

| Número | Operación | ReprCB | Verificación |
|--------|-----------|--------|--------------|
| +1239 | directo | 01239 | 1239 mod 100000 = 1239 |
| -1239 | 100000 - 1239 | 98761 | -1239 mod 100000 = 98761 |
| 0 | directo | 00000 | 0 mod 100000 = 0 |
| -100 | 100000 - 100 | 99900 | -100 mod 100000 = 99900 |

**Base 2, 8 bits:**

| Número | Operación | ReprCB | Verificación |
|--------|-----------|--------|--------------|
| +5 | directo | 00000101 | 5 mod 256 = 5 |
| -5 | 256 - 5 | 11111011 | -5 mod 256 = 251 |
| 0 | directo | 00000000 | 0 mod 256 = 0 |
| -128 | 256 - 128 | 10000000 | -128 mod 256 = 128 |

### Rango de Representación

Para una palabra de longitud $l$ en base $B$:

- **Mínimo:** $-B^{l-1}$
- **Máximo:** $B^{l-1} - 1$
- **Rango total:** $[-B^{l-1}, B^{l-1} - 1]$

**Ejemplos:**

- Base 2, 4 bits: [-8, 7]
- Base 2, 8 bits: [-128, 127]
- Base 10, 2 dígitos: [-50, 49]

### Capacidad y Eficacia

- **Total de representaciones:** $B^l$
- **Valores diferentes:** $B^l$ (todos los valores se usan)
- **Capacidad:** $B^l$ (máximo posible)
- **Eficacia:** $100\%$ (no hay desperdicio)

Esto es un GRAN avance sobre M&S y CB-1, que desperdician una representación en el cero doble.

---

## Parte 3: Conversión de Representaciones

### De decimal a CB

$$\text{ReprCB}(número) = número \bmod B^l$$

### De CB a decimal

**Interpretación:**

1. Interpretar la cadena como número en base $B$
2. Si el valor es > $B^{l-1} - 1$, restar $B^l$

**Fórmula:**
$$\text{Decimal} = \begin{cases}
valor & \text{si } valor \leq B^{l-1} - 1 \\
valor - B^l & \text{si } valor > B^{l-1} - 1
\end{cases}$$

### Ejemplo

**Base 10, 5 dígitos, palabra "98761":**

```
Interpretación como decimal: 98761
Punto de corte: 10^4 - 1 = 9999

¿98761 > 9999? SÍ
Aplicar: 98761 - 100000 = -1239  ✓
```

---

## Parte 4: Operaciones Aritméticas en CB

### Suma en CB

**LA OPERACIÓN MÁS IMPORTANTE: La suma en CB es la suma ordinaria modulo $B^l$**

No hay complicaciones. No hay end-around carry.

$$\text{ReprCB}(A) '+' \text{ReprCB}(B) = \text{ReprCB}(A + B) \bmod B^l$$

**Algoritmo:**
1. Sumar las representaciones como números en base $B$
2. Si hay carry fuera de $l$ dígitos, simplemente se descarta (modulo automático)
3. Truncar o tomar modulo para quedarse en $l$ dígitos

**Ejemplo en base 10, 5 dígitos:**

```
ReprCB(+1239) = 01239
ReprCB(-3591) = 96409  (100000 - 3591)

Suma: 01239 + 96409 = 97648

Verificación decimal: 1239 + (-3591) = -2352
Conversión: 97648 - 100000 = -2352  ✓
```

### Resta en CB

La resta se implementa como suma del complemento:

$$A '-' B = A '+' \text{opCB}(B) \bmod B^l$$

**Algoritmo:**
1. Calcular $\text{opCB}(B)$
2. Sumar $A '+' \text{opCB}(B)$ como suma ordinaria
3. Truncar/modulo para quedarse en $l$ dígitos

**Ejemplo en base 10, 5 dígitos:**

```
10 - 3 = 7

ReprCB(10) = 00010
ReprCB(3) = 00003
opCB(00003) = 99997  (100000 - 3)

Suma: 00010 + 99997 = 100007 → truncar → 00007
Decimal: 7  ✓
```

### Multiplicación en CB

La multiplicación en CB funciona correctamente sin complicaciones especiales:

**Para positivos a, b:**
$$\text{ReprCB}(a) \times \text{ReprCB}(b) = \text{ReprCB}(a \times b) \bmod B^l$$

**Para negativos:**
- $\text{ReprCB}(a) \times \text{ReprCB}(-b) = \text{ReprCB}(-a \times b) \bmod B^l$
- $\text{ReprCB}(-a) \times \text{ReprCB}(-b) = \text{ReprCB}(a \times b) \bmod B^l$

**Demostración algebraica (dos negativos):**

$$\text{opCB}(-a) \times \text{opCB}(-b) = (B^l - a)(B^l - b)$$
$$= B^{2l} - (a+b)B^l + ab$$
$$\equiv ab \pmod{B^l}$$
$$= \text{ReprCB}(ab) \bmod B^l$$  ✓

**Overflow:** Si $|a \times b|$ excede el rango $[-B^{l-1}, B^{l-1} - 1]$, el resultado se trunca.

### Comparación en CB

La comparación es muy simple: **el bit MSB determina el signo**

```
Bit MSB = 0 → número positivo (o cero)
Bit MSB = 1 → número negativo

Comparación:
- Si signos diferentes: positivo > negativo
- Si ambos positivos: comparar como naturales
- Si ambos negativos: comparar como naturales
  (el menor en valor natural = el más negativo)
```

---

## Parte 5: Ventajas de CB

### ✅ Una única representación para 0

```
ReprCB(0) = 00...0  (única)
ReprCB(-0) = 00...0  (la misma)
```

No hay desperdicio como en M&S y CB-1.

### ✅ Suma = suma ordinaria

$$\text{ReprCB}(A + B) = \text{ReprCB}(A) '+' \text{ReprCB}(B) \bmod B^l$$

Sin end-around carry, sin complicaciones.

### ✅ Resta sencilla

$$\text{ReprCB}(A - B) = \text{ReprCB}(A) '+' \text{opCB}(\text{ReprCB}(B))$$

Simple complemento y suma.

### ✅ Multiplicación correcta

La multiplicación funciona como multiplicación ordinaria modulo $B^l$.

### ✅ 100% de eficacia

Se usan todas las $B^l$ combinaciones. Ninguna se desperdicia.

### ✅ Comparación simple

El MSB determina el signo. Comparación directa igual que naturales.

### ✅ Estándar industrial

Es la ÚNICA representación usada en:
- Todos los procesadores (x86, ARM, MIPS, etc.)
- Todos los lenguajes de programación
- IEEE 754 para enteros
- Aritmética modular en criptografía

---

## Parte 6: Rango y Eficacia

### Tabla comparativa

| Aspecto | M&S | CB-1 | CB |
|---------|-----|------|-----|
| **Rango** | $[-2^{n-1}+1, 2^{n-1}-1]$ | $[-2^{n-1}+1, 2^{n-1}-1]$ | $[-2^{n-1}, 2^{n-1}-1]$ |
| **Capacidad** | $2^n - 1$ | $2^n - 1$ | $2^n$ |
| **Ceros** | 2 (+0, -0) | 2 (+0, -0) | 1 (0) |
| **Eficacia** | $1 - 1/2^n$ | $1 - 1/2^n$ | $1$ (100%) |
| **Suma** | Complicada | end-around carry | Ordinaria |
| **Resta** | Complicada | end-around carry | A + opCB(B) |
| **Multiplicación** | Complicada | Complicada | Ordinaria |
| **Uso industrial** | NO | NO | SÍ (100%) |

### Ejemplos de eficacia

**CB (Base 2):**
- 4 bits: Rango [-8, 7], Capacidad 16, Eficacia 100%
- 8 bits: Rango [-128, 127], Capacidad 256, Eficacia 100%

**CB (Base 10):**
- 2 dígitos: Rango [-50, 49], Capacidad 100, Eficacia 100%
- 3 dígitos: Rango [-500, 499], Capacidad 1000, Eficacia 100%

---

## Parte 7: Relación con opCB

### Negación de un número

Para obtener $-número$ a partir de su representación CB:

$$\text{ReprCB}(-número) = \text{opCB}(\text{ReprCB}(número))$$

**Ejemplo:**

```
ReprCB(5) = 00000101
opCB(00000101) = 11111011 = ReprCB(-5)

Verificación: -5 mod 256 = 251 = 11111011₂  ✓
```

### Número negativo no representable

Existe un caso especial: el negativo del mínimo del rango.

```
En 8 bits CB:
- Mínimo: -128 = 10000000
- opCB(10000000) = 01111111 + 1 = 10000000

ReprCB(-(-128)) = ReprCB(128) = ?
Pero 128 > 127, no cabe en 8 bits CB.

La operación opCB(10000000) = 10000000
Es decir: -(-128) ≡ -128 (mod 256)
```

Este es el único número que es su propio negativo en CB.

---

## Parte 8: Conclusiones

### CB es la representación estándar porque:

1. **Una única representación para 0** (no dos)
2. **Suma = suma ordinaria** modulo $B^l$
3. **No hay end-around carry** como en CB-1
4. **100% de eficacia** (no hay desperdicio)
5. **Multiplicación correcta** sin complicaciones
6. **Comparación simple** (MSB = signo)
7. **Usado en TODOS los computadores** del mundo

### En comparación:

- **M&S:** Intuitivo pero ineficiente (dos ceros, comparación complicada)
- **CB-1:** Elegante teóricamente pero poco práctico (dos ceros, end-around carry)
- **CB:** Estándar industrial, óptimo en todo

### Uso en la práctica:

Cuando ve `int`, `long`, `short`, `char` en cualquier lenguaje de programación (C, Java, Python, etc.), esos son enteros en **Complemento a la Base**.

```c
// En C
int x = -5;        // Internamente: complemento a la base
x = x + 3;         // Suma ordinaria modulo 2^32
if (x < 0) ...     // Comparación: compara MSB
```

Es la razón por la cual:
- $-1$ en binario es $111...111_2$ (todos 1s)
- $-1 + 1 = 0$ (overflow silencioso)
- El rango de `int` (32 bits) es $[-2^{31}, 2^{31} - 1]$, no simétrico

---

## Resumen de Fórmulas

| Operación | Fórmula |
|-----------|---------|
| **Representación** | ReprCB$(n) = n \bmod B^l$ |
| **Decodificación** | Dec $= n$ si $n \leq B^{l-1} - 1$ else $n - B^l$ |
| **Complemento** | opCB$(D) = B^l - D$ (mod $B^l$) |
| **Negación** | $-n \equiv$ opCB(ReprCB$(n)$) |
| **Suma** | ReprCB$(A + B) = $ ReprCB$(A)$ + ReprCB$(B)$ (mod $B^l$) |
| **Resta** | ReprCB$(A - B) = $ ReprCB$(A)$ + opCB(ReprCB$(B)$) (mod $B^l$) |
| **Multiplicación** | ReprCB$(A \times B) = $ ReprCB$(A)$ × ReprCB$(B)$ (mod $B^l$) |
| **Rango** | $[-B^{l-1}, B^{l-1} - 1]$ |
| **Eficacia** | $100\%$ (capacidad = $B^l$) |
