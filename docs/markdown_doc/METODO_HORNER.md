# El Método de Horner: Evaluación Eficiente de Polinomios

## Introducción

El **método de Horner** es un algoritmo clásico e ingenioso para evaluar polinomios de manera eficiente. Es especialmente útil para conversiones de base numérica porque **evita calcular potencias explícitamente**, usando solo multiplicación y suma.

---

## El Problema

Cuando convertimos un número de base B a decimal, necesitamos evaluar:

```
N = d₀×B^n + d₁×B^(n-1) + ... + d_{n-1}×B^1 + d_n×B^0
```

**Ingenuamente**, esto requiere:

- `n` potencias (B^n, B^(n-1), ..., B^1, B^0)
- `n` multiplicaciones (dígito × potencia)
- `n-1` sumas

**Total: 2n-1 operaciones significativas** (potencias son muy costosas)

---

## La Solución de Horner

Horner observó que podemos **reordenar el polinomio** así:

```
N = (...((d₀×B + d₁)×B + d₂)×B + d₃)×B + ... + d_n
```

Nota los **paréntesis anidados**: empezamos con el primer dígito y vamos incorporando los demás.

**Ahora necesitamos:**

- `0` potencias (¡ninguna!)
- `n-1` multiplicaciones
- `n` sumas

**Total: 2n-1 operaciones**, pero **sin exponenciaciones costosas**

---

## Algoritmo

### Pseudocódigo

```
resultado = 0
PARA CADA dígito d en el número (de izquierda a derecha):
    resultado = resultado × base + valor(d)
RETORNAR resultado
```

### Implementación en Python

```python
def horner(numero_str, base):
    resultado = 0
    for digito_char in numero_str:
        valor_digito = obtener_valor(digito_char)
        resultado = resultado * base + valor_digito
    return resultado
```

---

## Ejemplo Paso a Paso

### Convertir 1101₂ a decimal

**Número binario: 1 1 0 1**

**Paso 1:** Tomar el primer dígito

```
resultado = 1
```

**Paso 2:** Siguiente dígito es '1'

```
resultado = 1 × 2 + 1 = 3
```

**Paso 3:** Siguiente dígito es '0'

```
resultado = 3 × 2 + 0 = 6
```

**Paso 4:** Siguiente dígito es '1'

```
resultado = 6 × 2 + 1 = 13
```

**Respuesta: 13₁₀**

---

## Comparación Visual

### Polinomio (Forma Estándar)

```
1101₂ = 1×2³ + 1×2² + 0×2¹ + 1×2⁰
      = 1×8 + 1×4 + 0×2 + 1×1
      = 8 + 4 + 0 + 1
      = 13
```

**Operaciones:**

- Calcular potencias: 2³, 2², 2¹, 2⁰ (4 exponenciaciones)
- Multiplicar: 1×8, 1×4, 0×2, 1×1 (4 multiplicaciones)
- Sumar: 8+4+0+1 (3 sumas)
- **Total: 11 operaciones**

### Horner (Forma Anidada)

```
1101₂ = ((1×2 + 1)×2 + 0)×2 + 1
      = (3×2 + 0)×2 + 1
      = 6×2 + 1
      = 13
```

**Operaciones:**

- Multiplicar: 1×2, 3×2, 6×2 (3 multiplicaciones)
- Sumar: 2+1, 6+0, 12+1 (3 sumas)
- **Total: 6 operaciones (¡45% menos!)**

---

## ¿Por Qué Importa?

### Escala Pequeña (4 dígitos)

| Método | Exponenciaciones | Multiplicaciones | Sumas | Total |
|--------|------------------|------------------|-------|-------|
| Polinomio | 4 | 4 | 3 | 11 |
| Horner | 0 | 3 | 3 | 6 |
| **Mejora** | -100% | -25% | 0% | **-45%** |

### Escala Mediana (8 dígitos)

| Método | Exponenciaciones | Multiplicaciones | Sumas | Total |
|--------|------------------|------------------|-------|-------|
| Polinomio | 8 | 8 | 7 | 23 |
| Horner | 0 | 7 | 8 | 15 |
| **Mejora** | -100% | -13% | +14% | **-35%** |

### Escala Grande (32 dígitos)

| Método | Exponenciaciones | Multiplicaciones | Sumas | Total |
|--------|------------------|------------------|-------|-------|
| Polinomio | 32 | 32 | 31 | 95 |
| Horner | 0 | 31 | 32 | 63 |
| **Mejora** | -100% | -3% | +3% | **-34%** |

**Con números grandes, las exponenciaciones son EXTREMADAMENTE costosas.**

---

## Propiedades del Método de Horner

### ✅ Ventajas

1. **Evita exponenciaciones** - Las más costosas computacionalmente
2. **Menos multiplicaciones** - Solo n-1 en lugar de n
3. **Estable numéricamente** - Con aritmética de punto flotante
4. **Fácil de implementar** - Solo un bucle simple
5. **Usa menos memoria** - No necesita almacenar potencias

### ⚠️ Consideraciones

1. **Orden específico** - DEBE ir de izquierda a derecha
2. **Válido para cualquier base** - Binario, octal, hex, etc.
3. **Generalizable** - Funciona para cualquier polinomio

---

## Generalización: Evaluación de Polinomios

El método de Horner NO es solo para conversiones numéricas. Es un método general para evaluar **cualquier polinomio**:

### Polinomio General

```
P(x) = a₀×x^n + a₁×x^(n-1) + ... + a_{n-1}×x + a_n
```

### Con Horner

```
P(x) = (...((a₀×x + a₁)×x + a₂)×x + ... + a_n)
```

### Ejemplo: P(x) = 2x³ + 3x² - 5x + 7 evaluado en x=3

**Polinomio directo:**

```
P(3) = 2×3³ + 3×3² - 5×3 + 7
     = 2×27 + 3×9 - 15 + 7
     = 54 + 27 - 15 + 7
     = 73
```

**Horner:**

```
P(3) = ((2×3 + 3)×3 - 5)×3 + 7
     = (9×3 - 5)×3 + 7
     = 22×3 + 7
     = 73
```

**Mismo resultado, pero más eficiente.**

---

## Historia

El método es conocido como:

- **Método de Horner** (por William George Horner, 1819)
- **Esquema de Horner**
- **División sintética** (en álgebra)
- **Evaluación Ruffini** (en algunos países)

Aunque Horner recibió crédito, el método ya era conocido en China y Persia mucho antes.

---

## Aplicaciones Prácticas

### 1. Conversiones de Base (Primary)

```python
def binary_to_decimal(binary_str):
    result = 0
    for bit in binary_str:
        result = result * 2 + int(bit)
    return result
```

### 2. Evaluación de Polinomios

```python
def evaluate_polynomial(coefficients, x):
    result = coefficients[0]
    for coef in coefficients[1:]:
        result = result * x + coef
    return result
```

### 3. Hashing (Polinomial Rolling Hash)

```python
def polynomial_hash(string, prime=31):
    hash_value = 0
    power = 1
    for char in string:
        hash_value += (ord(char) - ord('a') + 1) * power
        power *= prime  # Equivalente a aplicar Horner
    return hash_value
```

### 4. Procesamiento de Dígitos

Cualquier problema que involucre procesar dígitos secuencialmente.

---

## Conclusión

El **método de Horner** es un ejemplo perfecto de cómo un pequeño cambio en el orden de las operaciones puede resultar en una **mejora significativa de eficiencia**.

Es una lección importante en programación:

- **No siempre el método obvio es el mejor**
- **La creatividad algorítmica importa**
- **Pequeñas optimizaciones pueden escalar enormemente**

### Puntos Clave

1. ✅ Horner evita exponenciaciones
2. ✅ Funciona para cualquier base
3. ✅ Se generaliza a cualquier polinomio
4. ✅ Simple de implementar
5. ✅ Parte de los algoritmos "clásicos" que todo programador debería conocer

---

## Referencias

- William George Horner: "A New Method of Solving Numerical Equations of All Orders, by Continuous Approximation" (1819)
- Donald Knuth: "The Art of Computer Programming", Vol. 2
- Método conocido en China (SongDynasty) y Persia mucho antes

---

**Reflexión:** Este es un buen recordatorio de que los algoritmos más útiles son a menudo los más simples en concepto, pero requieren un poco de creatividad matemática para descubrir.
