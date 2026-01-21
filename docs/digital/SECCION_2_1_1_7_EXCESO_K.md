# Sección 2.1.1.7.4: Exceso a K (Biased Representation)

## 1. Introducción a Exceso a K

**Exceso a K** (Biased o Excess-K representation) es una representación numérica que desplaza todos los números por una constante $K$.

### 1.1 Idea Fundamental

La idea es muy simple: en lugar de representar un número $a$ como sí mismo, representamos:

$$\text{ReprExcK}(a) = a + K$$

Por ejemplo, en **Exceso a 50** con 2 dígitos decimales:

- El número $0$ se representa como $0 + 50 = 50$ → `"50"`
- El número $10$ se representa como $10 + 50 = 60$ → `"60"`
- El número $-10$ se representa como $-10 + 50 = 40$ → `"40"`

### 1.2 ¿Por qué es útil?

Exceso a K es especialmente útil porque:

1. **No necesita bit de signo especial** - todos los bits se usan para representar magnitud
2. **Flexibilidad total** - podemos elegir cualquier $K$, en cualquier base, con cualquier longitud
3. **100% eficacia** - en cualquier base $B$ con longitud $l$, siempre representamos exactamente $B^l$ números
4. **Rango configurable** - eligiendo $K$ podemos determinar exactamente qué rango queremos representar
5. **Usado en IEEE 754** - los exponentes en punto flotante se representan en Exceso a 127 (binario 8-bit)

## 2. Definición Formal

### 2.1 Representación en Exceso a K

Dado:

- Base $B$
- Longitud en dígitos: $l$
- Desplazamiento (bias): $K$
- Número decimal a representar: $a$

La representación es:

$$\text{ReprExcK}(B, l, K, a) = \text{representación en base B de } (a + K) \text{ con } l \text{ dígitos}$$

### 2.2 Rango Representable

Con Exceso a K en base $B$ con longitud $l$:

- **Mínimo valor natural en cadena**: $0$ (cuando todos los dígitos son 0)
  - Representa el número: $0 - K = -K$
  
- **Máximo valor natural en cadena**: $B^l - 1$ (cuando todos los dígitos son $B-1$)
  - Representa el número: $(B^l - 1) - K = B^l - 1 - K$

**Rango de números representables**: $[-K, B^l - 1 - K]$

**Número de valores representables**: exactamente $B^l$ (100% eficacia)

### 2.3 Ejemplos de Rango

#### Ejemplo 1: Base 10, 2 dígitos, K = 50

- Cadenas posibles: `"00"` a `"99"` (100 valores)
- Valores naturales: 0 a 99
- Números representados: -50 a 49
- El `"00"` representa -50
- El `"50"` representa 0
- El `"99"` representa 49

#### Ejemplo 2: Base 2, 8 bits, K = 127 (IEEE 754)

- Cadenas posibles: `00000000` a `11111111` (256 valores)
- Valores naturales: 0 a 255
- Números representados: -127 a 128
- El `00000000` representa -127
- El `01111111` representa 0
- El `11111111` representa 128

#### Ejemplo 3: Base 2, 4 bits, K = 8

- Cadenas posibles: `0000` a `1111` (16 valores)
- Valores naturales: 0 a 15
- Números representados: -8 a 7
- El `0000` representa -8
- El `1000` representa 0
- El `1111` representa 7

## 3. Operaciones Aritméticas en Exceso a K

### 3.1 Suma

Si $A$ representa al número $a$ en ExcK y $B$ representa a $b$ en ExcK, entonces:

$$A = a + K$$
$$B = b + K$$

Si simplemente sumamos las representaciones:
$$A + B = (a + K) + (b + K) = a + b + 2K$$

Esto representa al número $a + b + K$, **no es lo que queremos**.

Para obtener la suma correcta $a + b$, necesitamos restar $K$ una vez:

$$A \mathbin{\#} B = A + B - K = (a + K) + (b + K) - K = a + b + K$$

Que es la representación correcta de $a + b$ en ExcK.

**Algoritmo de suma en ExcK:**

1. Sumar las dos representaciones como números naturales
2. Restar $K$ del resultado
3. Si hay desbordamiento, se trunca a $l$ dígitos

### 3.2 Resta

Análogamente, para restar:

$$A \mathbin{\#} B = A - B + K$$

**Algoritmo de resta en ExcK:**

1. Restar la segunda representación de la primera
2. Sumar $K$ al resultado
3. Si hay desbordamiento o subdesbordamiento, se ajusta con módulo

### 3.3 Multiplicación

Para multiplicar dos números en ExcK:

$$A \times B \text{ en representaciones} = (a + K) \times (b + K)$$
$$= ab + aK + bK + K^2$$

Pero queremos representar $ab$, que en ExcK es:
$$\text{ReprExcK}(ab) = ab + K$$

Entonces, necesitamos:
$$\text{Resultado} = (a + K) \times (b + K) - aK - bK - K^2 + K$$
$$= ab + K$$

O de forma más práctica:

1. Convertir representaciones a decimales: $a = A - K$, $b = B - K$
2. Multiplicar: $a \times b$
3. Convertir resultado a representación: $(a \times b) + K$

**Algoritmo de multiplicación en ExcK:**

1. Convertir $A$ y $B$ a decimales: $a = A - K$, $b = B - K$
2. Multiplicar: $producto = a \times b$
3. Convertir a representación: $resultado = producto + K$
4. Si el resultado no cabe en $l$ dígitos, se trunca

### 3.4 Comparación

Una ventaja importante de ExcK es que **la comparación es directa**:

Si queremos saber si $a < b$:

- En ExcK: $a + K < b + K$ ⟺ $a < b$
- Es decir: comparar directamente los valores naturales de las cadenas

Esto es especialmente útil para exponentes en punto flotante.

## 4. Ejemplos Detallados

### 4.1 Suma: $5 + 7 = 12$ en ExcK (Base 10, 2 dígitos, K=50)

**Paso 1: Representar en ExcK**

- $A = \text{ReprExcK}(5) = 5 + 50 = 55$ → `"55"`
- $B = \text{ReprExcK}(7) = 7 + 50 = 57$ → `"57"`

**Paso 2: Sumar las representaciones**

- `"55"` + `"57"` = 55 + 57 = 112 (en valores naturales)

**Paso 3: Restar K**

- $112 - 50 = 62$
- Como cadena: `"62"`

**Verificación:**

- `"62"` representa al número: $62 - 50 = 12$ ✓

### 4.2 Resta: $15 - 8 = 7$ en ExcK (Base 10, 2 dígitos, K=50)

**Paso 1: Representar en ExcK**

- $A = \text{ReprExcK}(15) = 15 + 50 = 65$ → `"65"`
- $B = \text{ReprExcK}(8) = 8 + 50 = 58$ → `"58"`

**Paso 2: Restar las representaciones**

- `"65"` - `"58"` = 65 - 58 = 7 (en valores naturales)

**Paso 3: Sumar K**

- $7 + 50 = 57$
- Como cadena: `"57"`

**Verificación:**

- `"57"` representa al número: $57 - 50 = 7$ ✓

### 4.3 Multiplicación: $4 \times 3 = 12$ en ExcK (Base 10, 2 dígitos, K=50)

**Paso 1: Representar en ExcK**

- $A = \text{ReprExcK}(4) = 4 + 50 = 54$ → `"54"`
- $B = \text{ReprExcK}(3) = 3 + 50 = 53$ → `"53"`

**Paso 2: Convertir a decimales**

- $a = 54 - 50 = 4$
- $b = 53 - 50 = 3$

**Paso 3: Multiplicar**

- $4 \times 3 = 12$

**Paso 4: Convertir resultado a representación**

- $\text{ReprExcK}(12) = 12 + 50 = 62$ → `"62"`

**Verificación:**

- `"62"` representa al número: $62 - 50 = 12$ ✓

## 5. Casos Especiales con Números Negativos

### 5.1 Suma: $(-10) + 15 = 5$ en ExcK (Base 10, 2 dígitos, K=50)

**Paso 1: Representar en ExcK**

- $A = \text{ReprExcK}(-10) = -10 + 50 = 40$ → `"40"`
- $B = \text{ReprExcK}(15) = 15 + 50 = 65$ → `"65"`

**Paso 2: Sumar las representaciones**

- `"40"` + `"65"` = 40 + 65 = 105

**Paso 3: Restar K**

- $105 - 50 = 55$
- Como cadena: `"55"`

**Verificación:**

- `"55"` representa: $55 - 50 = 5$ ✓

### 5.2 Multiplicación: $(-3) \times 4 = -12$ en ExcK (Base 10, 2 dígitos, K=50)

**Paso 1: Representar en ExcK**

- $A = \text{ReprExcK}(-3) = -3 + 50 = 47$ → `"47"`
- $B = \text{ReprExcK}(4) = 4 + 50 = 54$ → `"54"`

**Paso 2: Convertir a decimales**

- $a = 47 - 50 = -3$
- $b = 54 - 50 = 4$

**Paso 3: Multiplicar**

- $(-3) \times 4 = -12$

**Paso 4: Convertir resultado a representación**

- $\text{ReprExcK}(-12) = -12 + 50 = 38$ → `"38"`

**Verificación:**

- `"38"` representa: $38 - 50 = -12$ ✓

## 6. IEEE 754 y Exceso a K

En el estándar IEEE 754 para números en punto flotante:

### 6.1 Estructura de un número de precisión simple (32 bits)

```
[Signo: 1 bit][Exponente: 8 bits][Mantisa: 23 bits]
```

El exponente se representa en **Exceso a 127** (binario, 8 bits).

### 6.2 Rango del Exponente

Con 8 bits en Exceso a 127:

- Valor mínimo natural: $0$ (cadena `00000000`) → representa $-127$
- Valor máximo natural: $255$ (cadena `11111111`) → representa $+128$
- Rango de exponentes: $[-127, 128]$

**Valores especiales:**

- `00000000` (exponente -127): números desnormalizados (muy pequeños)
- `11111111` (exponente +128): infinito o NaN (números no válidos)
- `01111111` (exponente 0): la mantisa está en el rango $[1, 2)$

### 6.3 ¿Por qué Exceso a K en punto flotante?

1. **Comparación fácil**: Los números en punto flotante se pueden comparar usando comparación de enteros si tratamos el bit de signo especialmente
2. **Sin complicaciones de complemento a dos**: La representación es más regular
3. **Orden correcto**: La representación binaria mantiene el orden correcto para números positivos
4. **Rango asimétrico**: Podemos representar más positivos grandes que negativos pequeños (típicamente util)

## 7. Comparación de Todas las Representaciones

### 7.1 Tabla Comparativa: Binario, 8 bits

| Representación | -128 | -127 | -1 | 0 | 1 | 127 | 128 | Capacidad | Eficacia | Operaciones |
|---|---|---|---|---|---|---|---|---|---|---|
| **Magnitud y Signo** | 10000000 | 11111111 | 10000001 | 00000000 | 00000001 | 01111111 | ❌ | 255 | 99.6% | suma(+carry) |
| **CB-1** | 10000000 | 10000001 | 11111110 | 00000000 | 00000001 | 01111110 | ❌ | 255 | 99.6% | suma(+end-carry) |
| **CB (Std)** | 10000000 | 10000001 | 11111111 | 00000000 | 00000001 | 01111111 | ❌ | 256 | 100% | suma(simple) |
| **ExcK (K=127)** | 00000000 | 00000001 | 01111110 | 01111111 | 10000000 | 11111110 | 11111111 | 256 | 100% | suma(-K) |

### 7.2 Observaciones

1. **M&S y CB-1** tienen dos representaciones para 0 (ineficientes)
2. **CB y ExcK** usan 100% del espacio disponible
3. **CB** es el estándar industrial para enteros en todos los procesadores
4. **ExcK** es flexible: eligiendo K podemos ajustar el rango según necesidad
5. **ExcK vs CB** en punto flotante: ExcK es mejor para exponentes (comparación directa)

## 8. Flexibilidad de Exceso a K

Una característica poderosa de ExcK es que siempre tiene 100% eficacia **independientemente de K**.

### 8.1 Ejemplos con diferentes K (Base 2, 8 bits)

| K | Rango | Significado |
|---|---|---|
| 0 | [0, 255] | Enteros naturales (sin negativos) |
| 64 | [-64, 191] | Rango asimétrico |
| 127 | [-127, 128] | IEEE 754 estándar |
| 128 | [-128, 127] | Rango casi simétrico |
| 255 | [-255, 0] | Solo negativos |

### 8.2 Seleccionar K según necesidad

- **Si queremos máxima precisión positiva**: elegir $K$ pequeño
- **Si queremos máxima precisión negativa**: elegir $K$ grande
- **Si queremos rango simétrico**: elegir $K \approx B^l / 2$
- **Si queremos rango específico**: elegir $K$ tal que $-K$ sea el mínimo deseado

## 9. Algoritmos Implementados

### 9.1 Conversiones

**Decimal a ExcK:**

```
ReprExcK(numero, base, longitud, K):
    valor_natural = numero + K
    si valor_natural < 0 o valor_natural >= base^longitud:
        error "número fuera de rango"
    retorna representacion_en_base(valor_natural, base, longitud)
```

**ExcK a Decimal:**

```
ExcK_a_decimal(palabra, base, K):
    valor_natural = int(palabra, base)
    retorna valor_natural - K
```

### 9.2 Operaciones

**Suma:**

```
suma_ExcK(A, B, base, K):
    suma_natural = int(A, base) + int(B, base)
    resultado = suma_natural - K
    retorna resultado mod base^longitud
```

**Resta:**

```
resta_ExcK(A, B, base, K):
    resta_natural = int(A, base) - int(B, base)
    resultado = resta_natural + K
    retorna resultado mod base^longitud
```

**Multiplicación:**

```
multiplicacion_ExcK(A, B, base, K):
    a = int(A, base) - K
    b = int(B, base) - K
    producto = a * b
    resultado = producto + K
    retorna resultado mod base^longitud
```

## 10. Resumen y Conclusiones

### 10.1 Ventajas de Exceso a K

✓ Representación sin bit de signo separado
✓ 100% eficacia en cualquier base
✓ Flexibilidad total en la elección de rango
✓ Operaciones aritméticas correctas y consistentes
✓ Comparación directa de cadenas (en ciertos casos)
✓ Estándar para exponentes en IEEE 754
✓ Aplicable a cualquier base, no solo binario

### 10.2 Desventajas

✗ Menos común que Complemento a Base para enteros
✗ Requiere sumar/restar K en cada operación
✗ No hay un "valor especial" para detectar desbordamiento
✗ La comparación directa solo funciona bien sin signo en el bit más significativo

### 10.3 Cuándo usar Exceso a K

| Caso | Por qué |
|---|---|
| Exponentes en punto flotante | Comparación y rango flexible |
| Bases arbitrarias | 100% eficacia garantizada |
| Rango asimétrico deseado | K configurable |
| Sistemas donde se prefiere el bias | Convención de diseño |

### 10.4 Jerarquía de Representaciones para Enteros Signados

1. **Magnitud y Signo**: Histórica, educativa, ya no se usa
2. **Complemento a la Base Menos 1**: Educativa, raramente usada
3. **Complemento a la Base (CB/Two's Complement)**: **ESTÁNDAR** para enteros signados en procesadores
4. **Exceso a K**: **ESTÁNDAR** para exponentes en punto flotante

## 11. Referencias y Lecturas Adicionales

- IEEE 754-2019: Standard for Floating-Point Arithmetic
- "Computer Arithmetic" - Behrooz Parhami
- Arquitectura de Computadores: Representaciones numéricas

---

**Documentación generada como parte de: Sección 2.1.1.7 - Números Enteros con Signo**
