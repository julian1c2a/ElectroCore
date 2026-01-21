# Sección 2.1.6 - Representación de Números en Punto Flotante

**Formato generalizado para representación de números con rango dinámico**

---

## 📌 Concepto Fundamental

### Definición

**Punto Flotante (Floating Point)** es un sistema donde cada número se representa como:

$$V = M \times B^E$$

donde:

- **M (Mantisa):** Dígitos significativos (fraccionario normalizado)
- **B (Base):** Base del sistema (típicamente 2, 10, 16)
- **E (Exponente):** Potencia de B (escala del número)

### Estructura General

```
Formato genérico:
┌──────┬──────────────────┬──────────────────────┐
│ Signo│ Exponente (e bits)│ Mantisa (m bits)     │
│ 1 bit│                  │                      │
└──────┴──────────────────┴──────────────────────┘

Ejemplo: base 2, e=8 bits, m=23 bits (IEEE 754 simple)
```

### Componentes

#### 1. Signo (S)

```
S = 0  → número positivo
S = 1  → número negativo
```

#### 2. Exponente (E)

```
Propósito: Escalar la mantisa
Rango: Típicamente sesgado (biased)
Sesgo: 2^(e-1) - 1

Ejemplo (e=8):
├─ Rango sin sesgo: 0 a 255
├─ Sesgo: 127
├─ Exponente real: E_real = E - 127
├─ Rango real: -127 a 128
```

#### 3. Mantisa (M)

```
Propósito: Dígitos significativos
Formato: Número fraccionario normalizado: 1.xxx...x
Rango: [1, 2) en binario, [1, B) en base B

Ejemplo (m=23 bits):
├─ Representación: 1.xxxxx...xxxx (23 x's)
├─ Rango: [1.0, 2.0)
├─ Bit implícito: El "1." inicial se asume (no se almacena)
└─ Actual bits almacenados: 1 + 23 = 24 bits significativos
```

---

## 🔢 Formato Generalizado en Base B

### Definición Matemática

Para base B, exponente de e bits, mantisa de m bits:

$$V = (-1)^S \times M \times B^{E - Bias}$$

donde:

- **S ∈ {0,1}:** Signo (1 bit)
- **E ∈ [0, 2^e - 1]:** Exponente codificado (e bits)
- **M ∈ [1, B):** Mantisa normalizada (1 + m dígitos, pero m se almacenan)
- **Bias = $2^{e-1} - 1$:** Sesgo del exponente

### Normalización

Una mantisa está **normalizada** si tiene exactamente un dígito antes del punto decimal:

```
Base 2: 1.xxxxx...x
Base 10: d.xxxxx...x donde d ∈ {1,2,...,9}
Base 16: h.xxxxx...x donde h ∈ {1,2,...,F}

Ejemplos:
├─ Base 2: 1.0101 normalizado, 0.1101 NO normalizado
├─ Base 10: 3.14159 normalizado, 31.4159 NO normalizado
├─ Base 16: F.ABC normalizado, 1AB.C NO normalizado
```

### Ventaja de Normalización

```
Maximiza dígitos significativos (no desperdicia espacio)
Representación única (cada número tiene una sola forma)
Facilita comparación de números

Sin normalización:
├─ 1.0 × 2^2 = 4
├─ 0.1 × 2^3 = 4
├─ 0.01 × 2^4 = 4
└─ ¡Tres formas diferentes para el mismo número!
```

---

## 📋 Ejemplos en Diferentes Formatos

### IEEE 754 - Precisión Simple (32 bits)

```
Estructura: [S(1) | E(8) | M(23)]
├─ Signo: 1 bit
├─ Exponente: 8 bits, sesgo = 127
├─ Mantisa: 23 bits (+ 1 implícito) = 24 bits significativos
├─ Base: 2

Rango:
├─ Positivos: [1.18×10^-38, 3.40×10^38]
├─ Precisión: ~7 dígitos decimales

Ejemplo: 1.5 en IEEE 754 simple
├─ 1.5 = 1.1₂ × 2^0
├─ Signo: 0
├─ Exponente: 0 + 127 = 127 = 01111111₂
├─ Mantisa: 10000000000000000000000₂ (el 1. se asume)
└─ Resultado: 0 01111111 10000000000000000000000
```

### IEEE 754 - Precisión Doble (64 bits)

```
Estructura: [S(1) | E(11) | M(52)]
├─ Signo: 1 bit
├─ Exponente: 11 bits, sesgo = 1023
├─ Mantisa: 52 bits (+ 1 implícito) = 53 bits significativos
├─ Base: 2

Rango:
├─ Positivos: [2.23×10^-308, 1.80×10^308]
├─ Precisión: ~15-16 dígitos decimales
```

### Punto Flotante Genérico - Base 10, e=4, m=6

```
Estructura: [S(1) | E(4) | M(6)]
├─ Signo: 1 bit
├─ Exponente: 4 bits sin sesgo = [0, 15]
├─ Mantisa: 6 dígitos decimales
├─ Base: 10

Sesgo: 2^(4-1) - 1 = 7

Ejemplo: 123.456
├─ Normalizado: 1.23456 × 10^2
├─ Signo: 0
├─ Exponente: 2 + 7 = 9 = 1001₂
├─ Mantisa: 234560 (se asume el 1.)
└─ Resultado: 0 1001 234560
```

---

## 🔄 Números Especiales

### 1. Números Normalizados

Números con exponente **en rango válido** y mantisa **normalizada:**

```
Exponente E ∈ [1, 2^e - 2]  (excluye 0 y máximo)
Mantisa M = 1.xxxxx...x

Valor: (-1)^S × (1 + M_frac) × B^(E - Bias)

Ejemplo en IEEE 754 simple:
├─ E ∈ [1, 254]
├─ M normalizado: 1.xxxxx...x
└─ Rango de valores: [±1.18×10^-38, ±3.40×10^38]
```

### 2. Números Denormalizados

Números con exponente **E = 0** pero mantisa **≠ 0:**

```
Propósito: Llenar el "hueco" entre 0 y el número más pequeño normalizado
Mantisa: 0.xxxxx...x (sin el 1. inicial)

Valor: (-1)^S × (0 + M_frac) × B^(1 - Bias)
     = (-1)^S × M_frac × B^(1 - Bias)

Ejemplo en IEEE 754 simple:
├─ E = 0, M ≠ 0
├─ Valor: (-1)^S × 0.xxxxx...x × 2^-126
├─ Rango: [±1.4×10^-45, ±1.18×10^-38)

Ventaja: Gradual underflow en lugar de salto abrupto a 0
```

### 3. Cero

```
Exponente: E = 0
Mantisa: M = 0

Valor: (-1)^S × 0 = ±0

IEEE 754 permite ±0:
├─ +0: 0 00000000 00000000...
├─ -0: 1 00000000 00000000...
└─ Usualmente son equivalentes

Caso especial: En comparaciones, +0 = -0
```

### 4. Infinito

```
Exponente: E = 2^e - 1 (máximo)
Mantisa: M = 0

Valor: (-1)^S × ∞

Ejemplo IEEE 754 simple (e=8):
├─ +∞: 0 11111111 00000000...
├─ -∞: 1 11111111 00000000...

Operaciones:
├─ n + ∞ = ∞
├─ n × ∞ = ∞ (si n ≠ 0)
├─ 0 × ∞ = NaN (indefinido)
└─ ∞ / ∞ = NaN
```

### 5. NaN (Not a Number)

```
Exponente: E = 2^e - 1 (máximo)
Mantisa: M ≠ 0

Valor: No es un número válido

Ejemplo IEEE 754 simple:
├─ 0 11111111 00000001... (cualquier M ≠ 0)
├─ Puede ser "signaling NaN" o "quiet NaN"

Operaciones que generan NaN:
├─ 0 / 0
├─ ∞ / ∞
├─ √(-1)
├─ ∞ - ∞
├─ n + NaN = NaN
└─ Propiedad: NaN ≠ NaN (hasta NaN mismo)
```

---

## 📊 Tabla de Valores Especiales

| Exponente | Mantisa | Significado |
|-----------|---------|------------|
| 0 | 0 | ±0 (Cero) |
| 0 | ≠0 | ±Denormalizado |
| 1 a 2^e-2 | cualquiera | ±Normalizado |
| 2^e-1 | 0 | ±Infinito |
| 2^e-1 | ≠0 | NaN |

---

## ➕ Operaciones Aritméticas en Punto Flotante

### Suma / Resta

#### Algoritmo General

```
Entrada: a = M_a × B^E_a, b = M_b × B^E_b
Salida: c = a + b

Pasos:
1. Alinear exponentes:
   Si E_a < E_b:
      M_a = M_a / B^(E_b - E_a)
      E_a = E_b
   
2. Sumar mantisas:
   M_c = M_a + M_b
   E_c = E_a

3. Normalizar resultado:
   Mientras M_c ≥ B:
      M_c = M_c / B
      E_c = E_c + 1
   Mientras M_c < 1:
      M_c = M_c × B
      E_c = E_c - 1

4. Redondear:
   Si M_c requiere más dígitos que m bits:
      Descartar dígitos extras (redondear)
```

#### Ejemplo: 1.25 + 0.0625 (base 2)

```
1.25 = 1.01₂ × 2^0
0.0625 = 1.0₂ × 2^-4

Alinear exponentes:
├─ 0.0001010₂ × 2^0  (movemos punto 4 posiciones)
├─ 1.01₂ × 2^0

Sumar mantisas:
├─ 1.01₂ + 0.00010₂ = 1.01010₂
├─ Resultado: 1.01010₂ × 2^0

Normalizar:
├─ Ya está normalizado

Valor: 1.01010₂ × 2^0 = 1.3125 ✓
```

### Multiplicación

#### Algoritmo General

```
Entrada: a = M_a × B^E_a, b = M_b × B^E_b
Salida: c = a × b

Pasos:
1. Multiplicar mantisas:
   M_c = M_a × M_b
   
2. Sumar exponentes:
   E_c = E_a + E_b

3. Normalizar (puede necesitar 1 o 2 dígitos):
   Si M_c ≥ B²:
      M_c = M_c / B
      E_c = E_c + 1

4. Redondear:
   Si M_c requiere más dígitos que m bits:
      Descartar dígitos extras
```

#### Ejemplo: 1.5 × 2.0 (base 2)

```
1.5 = 1.1₂ × 2^0
2.0 = 1.0₂ × 2^1

Multiplicar mantisas:
├─ 1.1₂ × 1.0₂ = 1.1₂ = 1.5

Sumar exponentes:
├─ E = 0 + 1 = 1

Normalizar:
├─ 1.1₂ × 2^1 ya está normalizado

Valor: 1.1₂ × 2^1 = 3.0 ✓
```

### División

#### Algoritmo General

```
Similar a multiplicación pero:
├─ Dividir mantisas: M_c = M_a / M_b
├─ Restar exponentes: E_c = E_a - E_b
└─ Normalizar resultado
```

---

## 🔍 Errores en Punto Flotante

### Error de Representación

**Problema:** No todo número real es representable exactamente

```
Ejemplo: 0.1 en base 2 (IEEE 754)
├─ 0.1₁₀ = 0.0001100110011...₂ (periódico)
├─ Se almacena con m bits: 0.00011001100110011...truncado
├─ Error: ~1.4 × 10^-17

Punto clave: El error es proporcional a la magnitud del número
```

### Error Relativo vs Absoluto

**Error Absoluto:**
$$\epsilon_{abs} = |valor\_real - valor\_representado|$$

**Error Relativo:**
$$\epsilon_{rel} = \frac{|valor\_real - valor\_representado|}{|valor\_real|}$$

```
Ventaja de punto flotante:
├─ Error relativo es UNIFORME (~2^-m)
├─ Para números grandes: error absoluto es mayor
├─ Para números pequeños: error absoluto es menor

Comparación:
├─ Punto fijo: Error absoluto uniforme (2^-F)
├─ Punto flotante: Error relativo uniforme (~2^-m)

Ejemplo (32 bits):
├─ Punto fijo Q(16,16): error máximo = 2^-16 = 0.0000153
├─ Punto flotante: error ~ 2^-24 = 0.0000000596 (más pequeño)
│  para números ≈ 1, pero crece para números grandes
```

### Pérdida de Dígitos Significativos

**Problema en Suma/Resta:** Cuando números tienen magnitudes muy diferentes

```
Ejemplo: 1000000 + 0.000001
├─ Se alinean exponentes
├─ 0.000001 se vuelve negligible
├─ Resultado: 1000000 (se pierden dígitos significativos)

Solución:
├─ Reorganizar cálculos
├─ Usar precisión extendida temporalmente
├─ Evitar restar números casi iguales
```

---

## 📈 Tabla Comparativa: Punto Fijo vs Punto Flotante

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Estructura** | Posición decimal fija | Exponente variable |
| **Rango** | Limitado | Muy amplio |
| **Precisión** | Uniforme (absoluta) | Uniforme (relativa) |
| **Operaciones** | Rápidas | Más lentas |
| **Normalización** | No requerida | Requerida post-operación |
| **Overflow** | Abrupto | Gradual (desnormalizado) |
| **Números especiales** | Ninguno | 0, ±∞, NaN |
| **Hardware** | Simple | Complejo |
| **Rango 32 bits** | [-2M, 2M) | [±1.18×10^-38, ±3.40×10^38] |
| **Precisión 32 bits** | 2^-F (variable) | ~7 dígitos decimales |
| **Mejor para** | DSP, finanzas, embebidos | Científica, cálculos amplios |

---

## 🎯 Necesidad de Normalización

### ¿Por qué normalizar?

```
Problema: Mantener precisión máxima y forma única

Ejemplo sin normalización (base 2, m=4):
├─ 0.0101 × 2^3 = 5
├─ 0.1010 × 2^2 = 5  ← Misma mantisa pero desplazada
├─ 1.0100 × 2^1 = 5  ← Otra forma

Solución: Forzar mantisa = 1.xxxxx...
├─ 1.0100 × 2^1 = 5  ← Forma única y máxima precisión
```

### Normalización Post-Operación

**Después de suma/resta:**

```
La mantisa puede no estar normalizada
└─ Requiere renormalizar antes de almacenar

Después de multiplicación:
└─ Puede crecer a B dígitos (requiere escalar)
```

---

## 💡 Ventajas de Punto Flotante

### ✅ Ventajas

1. **Rango dinamático enorme:** Desde 10^-308 a 10^308 (IEEE doble)
2. **Error relativo constante:** Precisión relativa uniforme
3. **Números pequeños y grandes:** Sin reescalado manual
4. **Estándar universal:** IEEE 754 es reconocido internacionalmente
5. **Hardware eficiente:** FPU (Floating Point Unit) optimizado
6. **Números especiales:** Manejo de ±∞, NaN

### ❌ Desventajas

1. **Complejidad:** Hardware/software más complicado
2. **Errores acumulativos:** Redondeos se suman en cálculos largos
3. **Comportamiento no intuitivo:** Pérdida de precisión con diferencias pequeñas
4. **No es asociativo:** (a + b) + c ≠ a + (b + c)
5. **Más lento:** Operaciones más costosas que punto fijo
6. **Debugging difícil:** Errores pueden ser sutiles

---

## 🔗 Relación Punto Fijo vs Punto Flotante

```
Punto Fijo:
└─ Mejor para: Sistemas con rango limitado
└─ Más rápido, más simple, predecible

Punto Flotante:
└─ Mejor para: Sistemas con rango dinámico amplio
└─ Más versátil, estándar, maneja números especiales

Decisión:
├─ ¿Rango conocido y limitado? → Punto Fijo
├─ ¿Rango dinámico o muy amplio? → Punto Flotante
└─ ¿Duda? → Punto Flotante (es más seguro)
```

---

## 📚 Referencia Rápida IEEE 754

### Simple (32 bits)

```
[S(1) | E(8, sesgo=127) | M(23)]
Rango: [1.18×10^-38, 3.40×10^38]
Precisión: 7 dígitos decimales
```

### Doble (64 bits)

```
[S(1) | E(11, sesgo=1023) | M(52)]
Rango: [2.23×10^-308, 1.80×10^308]
Precisión: 15-16 dígitos decimales
```

### Extendida (80 bits)

```
[S(1) | E(15, sesgo=16383) | M(64)]
Rango: [3.36×10^-4932, 1.19×10^4932]
Precisión: 19 dígitos decimales
```

---

## 📝 Resumen

**Punto Flotante = (Signo) × (Mantisa) × Base^(Exponente)**

| Aspecto | Características |
|---------|-----------------|
| **Estructura** | Signo (1), Exponente (e), Mantisa (m) |
| **Normalización** | Mantisa ∈ [1, B) con 1 dígito antes del punto |
| **Rango** | Enormemente amplio gracias al exponente |
| **Precisión** | Relativa y uniforme: ~2^-m |
| **Especiales** | ±0, ±∞, NaN, denormalizados |
| **Operaciones** | Requieren normalización post-operación |
| **Error** | Acumulativo, requiere cuidado |
| **Uso** | Científico, ingeniería, cálculos amplios |
