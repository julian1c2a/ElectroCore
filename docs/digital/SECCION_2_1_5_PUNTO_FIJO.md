# Sección 2.1.5 - Representación de Fracciones en Punto Fijo

**Codificación de números fraccionarios con parte entera y fraccionaria fijas**

---

## 📌 Concepto Fundamental

### Definición

**Punto Fijo (Fixed Point)** es un sistema de representación numérica donde:

- **Estructura:** E bits para parte entera, F bits para parte fraccionaria
- **Total:** E + F bits
- **Rango:** $[-(2^{E-1} - 1), 2^{E-1} - 1]$ (con signo)
- **Precisión:** $2^{-F}$ (mínimo diferencial representable)

### Formato

```
Estructura general (con signo):
┌─────────────────────────────┬──────────────────────────┐
│ Parte Entera (E bits)       │ Parte Fraccionaria (F)   │
│ e₍E₋₁₎...e₁e₀             │ f₋₁f₋₂...f₍₋F₎           │
└─────────────────────────────┴──────────────────────────┘

Valor representado:
V = Σ(eᵢ × 2ⁱ) para i=0 a E-1  +  Σ(fⱼ × 2ʲ) para j=-1 a -F
```

### Ejemplo: Formato Q(3,4) en base 2

```
Q(3,4) significa:
- E = 3 bits para parte entera (rango: -4 a 3)
- F = 4 bits para parte fraccionaria (precisión: 1/16 = 0.0625)
- Total: 7 bits

Ejemplo de número: 0101.0110
├─ Parte entera: 0101 = 5 (se interpreta como 5 pero solo hasta 3 bits = 101)
├─ Parte fraccionaria: 0110 = 0.5 + 0.0 + 0.125 + 0 = 0.6875
└─ Valor total: 5.6875

Pero como solo tenemos 3 bits, rango es: -4 a 3, entonces 5 está fuera del rango
```

---

## 🔢 Representación en Base B Genérica

### Formato General en Base B

Para base B con E dígitos enteros y F dígitos fraccionarios:

$$V = \sum_{i=0}^{E-1} d_i \cdot B^i + \sum_{j=1}^{F} f_j \cdot B^{-j}$$

donde:

- $d_i$ ∈ {0, 1, ..., B-1} (dígitos enteros)
- $f_j$ ∈ {0, 1, ..., B-1} (dígitos fraccionarios)

### Ejemplos en Diferentes Bases

#### Base 10 (Decimal) - (3,2)

```
Formato: XXX.XX
Ejemplo: 123.45
├─ Parte entera: 123
├─ Parte fraccionaria: 45 → 0.45
├─ Precisión: 0.01
└─ Rango: -500 a 499 (con signo)
```

#### Base 2 (Binario) - (4,4)

```
Formato: XXXX.XXXX
Ejemplo: 1011.0110
├─ Parte entera: 1011 = 8 + 2 + 1 = 11
├─ Parte fraccionaria: 0110 = 0 + 1/4 + 1/8 + 0 = 0.375
├─ Valor total: 11.375
├─ Precisión: 1/16 = 0.0625
└─ Rango: -8 a 7 (con signo, 4 bits)
```

#### Base 16 (Hexadecimal) - (2,3)

```
Formato: XX.XXX
Ejemplo: 1F.8A4
├─ Parte entera: 1F = 31
├─ Parte fraccionaria: 8A4 = 8/16 + 10/256 + 4/4096 = 0.5391...
├─ Valor total: 31.5391...
├─ Precisión: 1/4096
└─ Rango: 0 a 255 (sin signo, 2 hex = 8 bits)
```

---

## 🔄 Conversión entre Bases

### Regla de Conservación: Mínimo de Dígitos Fraccionarios

**Problema:** Convertir un número con F dígitos en base B a base B' con F' dígitos

**Condición necesaria:**
$$B'^{F'} \geq B^F$$

**Para F' mínimo:**
$$F'_{min} = \lceil \log_{B'} B^F \rceil = \lceil F \cdot \log_{B'} B \rceil$$

### Demostración de la Regla

**Razón matemática:**

La precisión mínima representable es:

- En base B: $\Delta_B = B^{-F}$
- En base B': $\Delta_{B'} = B'^{-F'}$

Para no perder precisión: $\Delta_{B'} \leq \Delta_B$

$$B'^{-F'} \leq B^{-F}$$
$$B'^{F'} \geq B^F$$

### Ejemplos de Conversión

#### Caso 1: Base 2 a Base 10

**Dado:** F = 4 bits (base 2)
**Hallar:** F' para base 10

$$F'_{min} = \lceil 4 \cdot \log_{10} 2 \rceil = \lceil 4 \cdot 0.301 \rceil = \lceil 1.204 \rceil = 2$$

**Verificación:**

- Base 2 precisión: $2^{-4} = 0.0625$
- Base 10 con F'=1: $10^{-1} = 0.1 > 0.0625$ ❌ (pierde precisión)
- Base 10 con F'=2: $10^{-2} = 0.01 < 0.0625$ ✅ (conserva precisión)

#### Caso 2: Base 10 a Base 2

**Dado:** F = 3 dígitos decimales
**Hallar:** F' para base 2

$$F'_{min} = \lceil 3 \cdot \log_2 10 \rceil = \lceil 3 \cdot 3.322 \rceil = \lceil 9.966 \rceil = 10$$

**Verificación:**

- Base 10 precisión: $10^{-3} = 0.001$
- Base 2 con F'=9: $2^{-9} = 0.00195 > 0.001$ ❌
- Base 2 con F'=10: $2^{-10} = 0.000977 < 0.001$ ✅

#### Caso 3: Base 8 a Base 16

**Dado:** F = 3 dígitos octal
**Hallar:** F' para hexadecimal

$$F'_{min} = \lceil 3 \cdot \log_{16} 8 \rceil = \lceil 3 \cdot \frac{\log 8}{\log 16} \rceil = \lceil 3 \cdot \frac{3}{4} \rceil = \lceil 2.25 \rceil = 3$$

**Verificación:**

- Base 8 precisión: $8^{-3} = 0.00195...$
- Base 16 con F'=2: $16^{-2} = 0.00391 > 0.00195$ ❌
- Base 16 con F'=3: $16^{-3} = 0.000244 < 0.00195$ ✅

---

## 📋 Algoritmos de Conversión

### Conversión de Número Fraccionario: Base B → Base B'

#### Algoritmo 1: Multiplicación Repetida

```
Entrada: número fraccionario 0.ddd...ddd en base B, F dígitos fraccionarios
Salida: número fraccionario en base B' con F' = ⌈F × log_B' B⌉ dígitos

Algoritmo:
1. Convertir el número de base B a decimal
   x = Σ(dᵢ × B^-i) para i=1 a F

2. Multiplicación repetida por B':
   para j = 1 a F':
       x = x × B'
       dígito_j = ⌊x⌋
       x = x - dígito_j
   
3. Resultado: 0.dígito₁dígito₂...dígito_F'
```

#### Algoritmo 2: Conversión Binaria ↔ Hexadecimal (Optimizada)

Para B=2 y B'=16 (o viceversa), usar conversión directa por grupos:

```
Binario → Hexadecimal: Agrupar cada 4 bits desde punto
Hexadecimal → Binario: Expandir cada hex a 4 bits

Ejemplo: 0.1011010 (binario) → hexadecimal
├─ Agrupar: 0.1011 | 010
├─ Rellenar: 0.1011 | 0100
├─ Convertir: 0.B4 (hexadecimal)
```

### Ejemplo Práctico: Convertir 0.625 (decimal) a Binario

**Objetivo:** Representar 0.625 en binario con F' dígitos mínimos

**Paso 1: Determinar F'**
$$F'_{min} = \lceil 3 \cdot \log_2 10 \rceil = \lceil 9.966 \rceil = 10$$

**Paso 2: Multiplicación repetida por 2**

```
0.625 × 2 = 1.25    → dígito₁ = 1
0.25 × 2 = 0.5     → dígito₂ = 0
0.5 × 2 = 1.0      → dígito₃ = 1
0.0 × 2 = 0.0      → dígito₄ = 0
(resto todos ceros)

Resultado: 0.101 en binario (exacto en 3 dígitos)
```

**Verificación:**

- 0.101₂ = 1/2 + 0/4 + 1/8 = 0.5 + 0.125 = 0.625 ✓

---

## 🔐 Punto Fijo con Signo

### Representación de Números Negativos

#### Opción 1: Magnitud y Signo (M&S)

```
Formato: [S | Parte Entera | Parte Fraccionaria]
├─ S: 0 = positivo, 1 = negativo
├─ Ejemplo (1,3,3): S=1, E=101, F=101
├─ Valor: -5.625
```

#### Opción 2: Complemento a la Base (más común)

```
Formato: Representación en complemento a 2 (para base 2)

Rango en Q(E,F):
├─ Máximo: 2^(E-1) - 2^(-F)
├─ Mínimo: -2^(E-1)
├─ Cero: 0

Ejemplo Q(4,4):
├─ Máximo: 7.9375 = 0111.1111
├─ Mínimo: -8.0000 = 1000.0000
├─ Cero: 0000.0000
```

---

## 📊 Características de Precisión

### Análisis de Error

#### Error Máximo Representable

Para un número fraccionario en Q(E,F):

$$\epsilon_{max} = 2^{-F} = B^{-F}$$

**Ejemplo:** Q(8,16) en binario

- Error máximo: $2^{-16} = 0.0000152587...$
- Precisión: ±0.00001526 unidades

#### Error de Redondeo

Al representar un número no exacto en punto fijo:

$$\epsilon_{round} \leq \frac{2^{-F}}{2} = \frac{\epsilon_{max}}{2}$$

**Método de redondeo:**

```
Truncamiento (suelo):    error ∈ [0, ε_max)
Redondeo (más próximo):  error ∈ [-ε_max/2, ε_max/2)
Techo:                   error ∈ (0, ε_max]
```

### Representabilidad

Un número real $x$ es representable en Q(E,F) si:

$$x = \frac{n}{2^F}$$

donde $n$ es un entero tal que:

$$-2^{E-1} \leq n < 2^{E-1}$$

**Ejemplos en Q(4,4) con base 2:**

```
0.0625 = 1/16 ✅ (representable)
0.625 = 10/16 ✅ (representable)
0.6 = 9.6/16 ❌ (no representable: requiere infinitos bits)
```

---

## ➕ Errores en Operaciones

### Error de Operación: Suma/Resta

#### Problema: Overflow/Underflow

```
Ejemplo en Q(4,4):
├─ 7.9375 + 1.0000 = 8.9375 (fuera del rango)
├─ Resultado truncado: -7.0625 (desbordamiento)

Problema: Pérdida de datos y resultados incorrectos
```

#### Soluciones

1. **Saturación:** Limitar al máximo/mínimo representable
2. **Envolvimiento (Wrapping):** Permitir overflow con aritmética modular
3. **Mayor precisión:** Usar más bits temporalmente

### Error de Operación: Multiplicación

#### Problema: Expansión de bits

```
Cuando multiplicamos dos números en Q(E,F):
resultado ∈ Q(2E, 2F)  ← ¡Necesita el doble de bits!

Ejemplo:
├─ Q(4,4) × Q(4,4) = Q(8,8)
├─ 7.9375 × 7.9375 = 62.89...
├─ Requiere reducir back a Q(4,4)
└─ Pérdida de precisión inevitable
```

#### Manejo del Error

```
Opciones:
1. Redondear/Truncar resultado a Q(E,F)
   └─ Pérdida de precisión en bits bajos

2. Normalizar resultado
   └─ Escalar mantisa y exponente (punto flotante)

3. Usar aritmética extendida
   └─ Mantener bits extra temporalmente
```

---

## 📈 Tabla Comparativa de Formatos Q

| Formato | E | F | Total Bits | Rango (Signo) | Precisión | Uso |
|---------|---|---|-----------|---|---|---|
| Q(4,4) | 4 | 4 | 8 | [-8, 7.9375) | 0.0625 | Embedded systems |
| Q(8,8) | 8 | 8 | 16 | [-256, 255.996) | 0.00391 | DSP, filtros |
| Q(16,16) | 16 | 16 | 32 | [-32768, 32767.9) | 0.0000153 | Precisión media |
| Q(24,8) | 24 | 8 | 32 | [-8M, 8M) | 0.00391 | Audio |

---

## 🎯 Ventajas y Desventajas

### ✅ Ventajas de Punto Fijo

1. **Operaciones rápidas:** Sin lógica de normalización
2. **Predecible:** Error siempre acotado por $2^{-F}$
3. **Hardware simple:** Circuitos aritméticos estándar
4. **Rango homogéneo:** Precisión igual en todo el rango
5. **No hay Inf/NaN:** Comportamiento determinista

### ❌ Desventajas de Punto Fijo

1. **Rango limitado:** Sin "escala automática"
2. **Problemas con escala:** Overflow fácil en cálculos
3. **Eficiencia de bits:** Desperdicia espacio en números pequeños
4. **Multiplicación compleja:** Resultado requiere bits extra
5. **Programador debe controlar:** Necesita estar atento a ranges

---

## 💡 Cuándo Usar Punto Fijo

**✅ Usar punto fijo cuando:**

- Hardware limitado (microcontroladores)
- Necesitas velocidad máxima
- Rango de números es conocido y limitado
- Aplicaciones financieras (dinero: siempre 2 decimales)
- Procesamiento digital de señales con punto fijo

**❌ No usar punto fijo cuando:**

- Rango muy amplio (necesitas desde 0.0001 hasta 1000000)
- Cálculos científicos (errores acumulativos)
- Números muy grandes y muy pequeños en el mismo cálculo
- Precisión relativa (porcentaje de error) es importante

---

## 🔗 Siguiente: Punto Flotante

Una solución a los problemas de rango limitado es **Punto Flotante**, donde:

- El punto decimal "flota" (se ajusta automáticamente)
- Cada número tiene un exponente que escala su valor
- Mayor rango, pero menor precisión en números pequeños

Ver: [SECCION_2_1_6_PUNTO_FLOTANTE.md](SECCION_2_1_6_PUNTO_FLOTANTE.md)

---

## 📝 Resumen

**Punto Fijo = (Parte Entera: E bits) + (Parte Fraccionaria: F bits)**

| Aspecto | Características |
|---------|-----------------|
| **Estructura** | Posición del punto decimal es fija |
| **Precisión** | Uniforme: siempre $2^{-F}$ |
| **Rango** | Limitado: $[-2^{E-1}, 2^{E-1})$ |
| **Operaciones** | Rápidas, sin normalización |
| **Error máximo** | Acotado y predecible |
| **Overflow** | Requiere manejo explícito |
| **Uso** | Sistemas embebidos, DSP, finanzas |
