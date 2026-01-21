# 📝 Sección 2.1.1.7.2: Complemento a la Base Menos 1 (CB-1)

## Introducción: Una Operación, No una Representación

La **Complemento a la Base Menos 1** comienza como una **operación** sobre palabras de longitud fija. Aunque parezca abstracta al principio, esta operación es la clave para una forma alternativa (pero poco usada) de representar números negativos.

---

## Parte 1: La Operación opCBm1

### Operación sobre Dígitos

Para un dígito individual `d[i]` en una base `B`:

$$\text{opCBm1}(d[i]) = B - 1 - d[i]$$

**Propiedad fundamental:** Esta operación siempre devuelve un dígito válido en esa base.

**Ejemplos en diferentes bases:**

| Base | Dígito | Complemento | Cálculo |
|------|--------|------------|---------|
| 2    | 0      | 1          | 1 - 0 = 1 |
| 2    | 1      | 0          | 1 - 1 = 0 |
| 10   | 3      | 6          | 9 - 3 = 6 |
| 10   | 5      | 4          | 9 - 5 = 4 |
| 10   | 9      | 0          | 9 - 9 = 0 |

### Operación sobre Palabras

Dada una palabra `d[l-1:0]` de longitud `l` en base `B`:

$$\text{opCBm1}(d[l-1:0]) = \tilde{d}[l-1:0] = (B-1-d[i]):[l-1:0]$$

Es decir: **aplicar opCBm1 a cada dígito independientemente**.

**Característica especial:** No hay "carries" o "borrows". Cada dígito se procesa sin afectar a los demás.

**Ejemplo en base 10 con 5 dígitos:**

```
Palabra original:   A = 01239
                    ~A = 98760

Cálculo dígito a dígito:
  0 → 9-0 = 9
  1 → 9-1 = 8
  2 → 9-2 = 7
  3 → 9-3 = 6
  9 → 9-9 = 0

Resultado: 98760
```

**Ejemplo en binario (base 2):**

```
Palabra original:   0101
  Cada bit:         flip (0→1, 1→0)
Resultado:          1010

Es simplemente invertir cada bit (operación NOT en lógica digital)
```

### Propiedades de opCBm1

#### Propiedad 1: Involutiva (Aplicar dos veces = Identidad)

$$\text{opCBm1}(\text{opCBm1}(D)) = D$$

**Demostración:**

```
Si d[i] es un dígito:
  opCBm1(d[i]) = B - 1 - d[i]
  opCBm1(opCBm1(d[i])) = B - 1 - (B - 1 - d[i]) = d[i]  ✓
```

**Significado:** Como multiplicar por -1 dos veces (vuelves al número original).

#### Propiedad 2: Independencia de Dígitos

Cada dígito se procesa **completamente independiente** de los demás. No hay propagación de carry/borrow como en la suma tradicional.

#### Propiedad 3: Rango de Valores

Si interpretamos una palabra en opCBm1 como base B natural:

$$\text{eval}(\tilde{d}[l-1:0]) = B^l - 1 - \text{eval}(d[l-1:0])$$

**Ejemplo:** En base 10 con 2 dígitos:

```
Palabra:    01
eval(01) = 1
~01 = 98
eval(98) = 98 = 100 - 1 - 1 = 99 - 1  ✓
```

---

## Parte 2: Sumas Modulares con opCBm1

### Suma de Palabra A '+' Complemento de Palabra C

¿Qué ocurre cuando realizamos ReprCBm1(A) '+' ReprCBm1(C)?

**Nota importante:** El símbolo '+' (con comillas) denota la operación de suma en CB-1, que es diferente de la suma numérica (+) ordinaria.

Algebraicamente:
$$\text{ReprCBm1}(A) + \text{opCBm1}(\text{ReprCBm1}(C)) = A + (B^l - 1 - C) = A - C + B^l - 1$$

**En aritmética módulo B^l:**

$$\text{ReprCBm1}(A) '+' \text{ReprCBm1}(C) \equiv A - C - 1 \pmod{B^l}$$

**Ejemplo en base 10 con 5 dígitos:**

```
A = 03591
C = 01239
opCBm1(C) = ~01239 = 98760

A + opCBm1(C) = 03591 + 98760
Suma normal:    102351

Como trabajamos con 5 dígitos, B^5 = 100000
Carry final: 102351 mod 100000 = 02351
```

### Suma '+' de dos Complementos: ReprCBm1(-A) '+' ReprCBm1(-C)

Algebraicamente:
$$\text{opCBm1}(\text{ReprCBm1}(A)) '+' \text{opCBm1}(\text{ReprCBm1}(C)) = (B^l - 1 - A) + (B^l - 1 - C) = 2B^l - 2 - A - C$$

**Módulo B^l (con end-around carry):**

$$\text{ReprCBm1}(-A) '+' \text{ReprCBm1}(-C) \equiv -A - C - 1 \pmod{B^l}$$

*Nota: Con el end-around carry se suma 1, corrigiendo el -2 a -1*

### Tabla de Combinaciones (Base 10, 5 dígitos)

Sea M = 99999 (que es B^l - 1 en 5 dígitos):

| Operación Aritmética | Representaciones CB-1 | Operación '+' en CB-1 | Resultado Decimal |
|-----------|---------|-----------------|------------------|
| A + B | ReprCBm1(3591) '+' ReprCBm1(1239) | 03591 '+' 01239 | +04830 |
| A - B | ReprCBm1(3591) '+' ReprCBm1(-1239) | 03591 '+' 98760 | -01352 |
| -A + B | ReprCBm1(-3591) '+' ReprCBm1(1239) | 96408 '+' 01239 | +01352 |
| -A - B | ReprCBm1(-3591) '+' ReprCBm1(-1239) | 96408 '+' 98760 | -04830 |

**Nótese sobre la operación '+' (suma en CB-1):**

- La operación '+' es **distinta** de la suma ordinaria (+)
- Requiere end-around carry: si hay carry final, se suma 1 al resultado
- **Importante:** ReprCBm1(A) '+' ReprCBm1(B) ≠ ReprCBm1(A + B) como operaciones simples
- La relación correcta: ReprCBm1(A) '+' ReprCBm1(B) = ReprCBm1(A + B) cuando se implementa completamente con end-around carry

---

## Parte 3: Representación en Complemento a la Base Menos 1

### Definición

Una palabra de longitud `l` en base `B` representa un número entero mediante:

- **Si número ≥ 0:** Represéntalo directamente en `l` dígitos
- **Si número < 0:** Representa como `B^l - 1 - número` en `l` dígitos

### Rango de Representación

El rango es idéntico al de Magnitud y Signo:

$$\text{Rango: } [-B^{l-1} + 1, B^{l-1} - 1]$$

**Para 8 bits en base 2:**

- Mínimo: -(2^7) + 1 = -127
- Máximo: 2^7 - 1 = 127

**Capacidad:** 2 × 2^(l-1) - 1 = 2^l - 1 valores

### El Problema del Cero Doble

CB-1 tiene **DOS representaciones para cero**:

1. **Cero positivo:** `00...0` (l dígitos)
   - Valor en CB-1: 0
   - Representa: +0

2. **Cero negativo:** `(B-1)(B-1)...(B-1)` (l dígitos)
   - Valor en CB-1: B^l - 1
   - Representa: -0 (pero sigue siendo 0)

**En base 10 con 2 dígitos:**

```
+0 se representa como: 00
-0 se representa como: 99  (porque 99 - 99 = 0)
```

**En binario con 8 bits:**

```
+0 se representa como: 00000000
-0 se representa como: 11111111
```

---

## Parte 4: Ejemplos Detallados

### Ejemplo 1: Decimal (Base 10, 2 dígitos)

**Tabla de representaciones:**

```
Valor decimal → Representación CB-9 → Interpretación
    +9        →        09           → positivo
    +8        →        08           → positivo
    +7        →        07           → positivo
    +6        →        06           → positivo
    +5        →        05           → positivo
    +4        →        04           → positivo
    +3        →        03           → positivo
    +2        →        02           → positivo
    +1        →        01           → positivo
    +0        →        00           → cero positivo
    -0        →        99           → cero negativo
    -1        →        98           → negativo
    -2        →        97           → negativo
    -3        →        96           → negativo
    -4        →        95           → negativo
    -5        →        94           → negativo
    -6        →        93           → negativo
    -7        →        92           → negativo
    -8        →        91           → negativo
    -9        →        90           → negativo
```

### Ejemplo 2: Binario (Base 2, 4 bits)

**CB-1 en 4 bits binarios:**

```
Valor decimal → CB-1 (4 bits) → Operación
    +7        →    0111       → directo
    +6        →    0110       → directo
    +5        →    0101       → directo
    +4        →    0100       → directo
    +3        →    0011       → directo
    +2        →    0010       → directo
    +1        →    0001       → directo
    +0        →    0000       → directo
    -0        →    1111       → flip todos (15-0=15)
    -1        →    1110       → flip todos (15-1=14)
    -2        →    1101       → flip todos (15-2=13)
    -3        →    1100       → flip todos (15-3=12)
    -4        →    1011       → flip todos (15-4=11)
    -5        →    1010       → flip todos (15-5=10)
    -6        →    1001       → flip todos (15-6=9)
    -7        →    1000       → flip todos (15-7=8)
```

**Observación:** En binario, opCBm1 = NOT (invertir cada bit).

---

## Parte 5: Operaciones en CB-1

### Negación (Multiplicar por -1)

Para negar un número en CB-1: **Aplicar opCBm1 a cada dígito.**

**En decimal:**

```
Número:   3591
Negación: ~3591 = 6408
```

**En binario:**

```
Número:   0101
Negación: ~0101 = 1010  (flip cada bit)
```

### Suma '+' en CB-1

La operación '+' (suma en CB-1) requiere "end-around carry":

1. Sumar las representaciones como en base B normal: ReprCBm1(A) '+' ReprCBm1(B)
2. Si hay carry final, sumarlo al resultado

**Ejemplo verificando ReprCBm1(1239) '+' ReprCBm1(-1239) = ReprCBm1(0):**

```
  ReprCBm1(+1239) = 01239
+ ReprCBm1(-1239) = 98760
                = -------
           carry 1 00999  (hay carry final)
         +     1  (end-around carry)
           -------
             01000 = 00000 (después de truncar)

Resultado decimal: ReprCBm1^(-1)(00000) = 0  ✓
```

**Conclusión:** ReprCBm1(1239) '+' ReprCBm1(-1239) = ReprCBm1(0), verificando que la operación '+' funciona correctamente.

- La suma numérica: 1239 + (-1239) = 0
- La operación '+': ReprCBm1(1239) '+' ReprCBm1(-1239) = ReprCBm1(0) ✓

### Resta '-' en CB-1

La operación '-' (resta en CB-1) se implementa usando la operación '+':

$$\text{ReprCBm1}(A) '-' \text{ReprCBm1}(C) = \text{ReprCBm1}(A) '+' \text{opCBm1}(\text{ReprCBm1}(C))$$

Es decir: para restar ReprCBm1(C), se complementa con opCBm1 y luego se suma usando la operación '+' con end-around carry.

### Comparación

La comparación en CB-1 es más consistente que en M&S:

- **Dos números positivos:** Compara como naturales
- **Dos números negativos:** Compara como naturales (porque el bit más alto determina el signo)
- **Uno positivo, uno negativo:** El positivo es mayor

---

## Parte 6: Ventajas y Desventajas de CB-1

### ✅ VENTAJAS

1. **Operación simple en binario**
   - opCBm1 = NOT (invertir cada bit)
   - Muy rápido en hardware

2. **Operación de dígitos independientes**
   - No hay propagación de carry
   - Cada dígito se procesa en paralelo

3. **Comparación uniforme**
   - Más consistente que M&S
   - Reglas similares para positivos y negativos

### ❌ DESVENTAJAS

1. **DOS REPRESENTACIONES PARA CERO**
   - +0: `00...0`
   - -0: `(B-1)(B-1)...(B-1)`
   - Desperdicia una combinación

2. **SUMA Y RESTA COMPLICADAS POR END-AROUND CARRY**
   - Requiere detector de carry
   - Requiere sumador adicional para el carry final
   - Más lento que suma binaria simple

3. **BAJA EFICACIA EN BASES GRANDES**
   - Eficacia: (2/B) - (1/B^l)
   - Cuando B crece, eficacia disminuye
   - En base 2: eficacia = 1 - (1/2^l) ✓
   - En base 10: eficacia = 0.2 - (1/10^l) ✗ (¡muy baja!)

4. **NO ESTÁNDAR EN SISTEMAS MODERNOS**
   - Complemento a 2 (C2) es preferido
   - C2 tiene una sola representación para 0
   - C2 no requiere end-around carry

---

## Parte 7: Eficacia de CB-1

### Fórmula General

Para base B y longitud l:

$$\text{Eficacia} = \frac{2 \times B^{l-1} - 1}{B^l} = \frac{2}{B} - \frac{1}{B^l}$$

**Casos específicos:**

| Base | Longitud | Capacidad | Posible | Eficacia |
|------|----------|-----------|---------|----------|
| 2    | 4        | 15        | 16      | 93.75%   |
| 2    | 8        | 255       | 256     | 99.61%   |
| 2    | 16       | 65535     | 65536   | 99.998%  |
| 10   | 2        | 19        | 100     | 19.00%   |
| 10   | 3        | 199       | 1000    | 19.90%   |
| 10   | 4        | 1999      | 10000   | 19.99%   |

**Observación:** En base 2, eficacia es excelente. En base 10, ¡es muy mala! Por eso CB-1 no se usa en sistemas decimales.

---

## Parte 8: Comparación M&S vs CB-1

| Aspecto | M&S | CB-1 |
|---------|-----|------|
| Bit de signo | SÍ (MSB) | NO |
| Operación negación | Flip MSB | opCBm1 todos |
| Suma | Compleja | Con end-around carry |
| Dos ceros | SÍ | SÍ |
| Eficacia (base 2) | 1 - 1/2^l | 1 - 1/2^l |
| Rango | [-2^(l-1)+1, 2^(l-1)-1] | [-2^(l-1)+1, 2^(l-1)-1] |
| Hardware | Más simple | Más simple (AND gates) |
| Usado actualmente | NO | NO (Complemento a 2 es estándar) |

---

## Conclusión

CB-1 es una representación elegante teóricamente, especialmente en binario donde opCBm1 es simplemente NOT. Sin embargo, tiene un defecto fatal: **dos representaciones para cero**, que causa ineficiencia y complejidad adicional.

Por eso en sistemas modernos se prefiere **Complemento a 2 (C2)**, que resolve este problema con una simple suma adicional de 1.

---

**Sección:** 2.1.1.7.2  
**Tema:** Complemento a la Base Menos 1  
**Estado:** ✅ IMPLEMENTADO  
**Próximo:** Complemento a 2 (C2) - El estándar industrial
