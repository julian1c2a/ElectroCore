# Comparativa: Punto Fijo vs Punto Flotante

**Análisis detallado de ventajas, desventajas y casos de uso**

---

## 📊 Tabla Comparativa Completa

### Estructuras

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Formato** | [E bits enteros \| F bits fraccionarios] | [S(1) \| E bits exponente \| M bits mantisa] |
| **Ejemplo 32 bits** | Q(16,16) | IEEE 754 simple |
| **Posición decimal** | Fija (siempre en el mismo lugar) | Flota (varía con el exponente) |

### Rango de Representación

| Aspecto | Punto Fijo Q(16,16) | Punto Flotante (IEEE 754 simple) |
|---------|---|---|
| **Enteros positivos max** | 65,535 | 3.40 × 10^38 |
| **Enteros negativos min** | -65,536 | -3.40 × 10^38 |
| **Fracción más pequeña** | 0.0000153 (2^-16) | 1.18 × 10^-38 (subnormal) |
| **Rango dinámico** | ~50 billones (no existe) | ~10^76 ¡Enorme! |

### Precisión

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Tipo** | Absoluta (uniforme) | Relativa (uniforme) |
| **Error máximo** | 2^-F (constante) | ~2^-m (% del número) |
| **En número pequeño (0.001)** | 2^-16 = 0.0000153 | 0.001 × 2^-24 ≈ 5.96 × 10^-11 |
| **En número grande (1000000)** | 2^-16 = 0.0000153 | 1000000 × 2^-24 ≈ 0.0596 |
| **Ventaja** | Números pequeños son precisos | Números grandes son (relativamente) precisos |

### Operaciones Aritméticas

#### Suma / Resta

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Pasos** | 1. Sumar 2. Redondear | 1. Alinear exp. 2. Sumar 3. Normalizar 4. Redondear |
| **Complejidad** | Baja | Alta |
| **Velocidad** | Rápida | Más lenta |
| **Problemas** | Overflow/underflow | Pérdida de dígitos si Δ muy grande |

#### Multiplicación

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Pasos** | 1. Multiplicar 2. Descartar bits extras | 1. Multiplicar mantisas 2. Sumar exponentes 3. Normalizar |
| **Complejidad** | Alta (resultado es 2F bits) | Media (mantiene estructura) |
| **Velocidad** | Lenta | Más rápida que punto fijo |
| **Overflow** | Abrupto | Gradual (a infinito) |

### Hardware

| Aspecto | Punto Fijo | Punto Flotante |
|---------|-----------|-----------------|
| **Complejidad** | Simple | Muy complejo |
| **Área silicio** | Pequeña | Grande |
| **Consumo energía** | Bajo | Medio-Alto |
| **Velocidad** | Muy rápida | Rápida (pero más lenta que FX) |
| **Disponibilidad** | En todo microprocesador | FPU (no siempre presente) |

---

## 🔍 Análisis de Errores

### Error de Representación

#### Punto Fijo Q(E,F)

```
Cualquier número real x se redondea a:
x_repr = round(x × 2^F) / 2^F

Error absoluto:
ε_abs ∈ [0, 2^-F / 2]  (con redondeo)
ε_abs ∈ [0, 2^-F]      (con truncamiento)

Error relativo:
ε_rel = ε_abs / |x|

Ejemplo Q(16,16), x = 123.456:
├─ ε_abs = 2^-16 = 0.0000153
├─ ε_rel = 0.0000153 / 123.456 ≈ 0.00000012 (0.000012%)
└─ Muy pequeño para números grandes
  
Pero para x = 0.00001:
├─ ε_abs = 2^-16 = 0.0000153
├─ ε_rel = 0.0000153 / 0.00001 ≈ 1.53 (153%)
└─ ¡Error enorme para números pequeños!
```

#### Punto Flotante IEEE 754 Simple

```
Cualquier número real x se redondea a:
x_repr = M × 2^(E - 127)  donde M ∈ [1, 2)

Error absoluto:
ε_abs ∈ [0, (2^-24) × |x| / 2]

Error relativo:
ε_rel ≈ 2^-24 ≈ 5.96 × 10^-8  (uniforme)

Ejemplo x = 123.456:
├─ ε_abs ≈ 2^-24 × 123.456 ≈ 0.00000735
├─ ε_rel ≈ 5.96 × 10^-8 (constante)

Ejemplo x = 0.00001:
├─ ε_abs ≈ 2^-24 × 0.00001 ≈ 5.96 × 10^-13
├─ ε_rel ≈ 5.96 × 10^-8 (¡mismo error relativo!)
└─ Error relativo es predecible
```

### Comparación Visual

```
Error relativo en función del número:

Punto Fijo Q(16,16):
│
│              ┌─────────────────────────
│              │ Error relativo = ε_abs / |x|
│              │ Decrece con x más grande
│        ┌─────┘
│        │
│    ┌───┘
│    │  Crece explosivamente para x pequeño
├────┼──────────────────────────────────
│    0.0001    0.01    1    100    10000
└─────────────────────────────────────

Punto Flotante:
│
│    ───────────────────────────────────
│ ε_rel ≈ cte = 2^-24
│    (línea plana)
│
├───────────────────────────────────
│
│    0.0001    0.01    1    100    10000
└─────────────────────────────────────
```

---

## 💾 Eficiencia de Almacenamiento

### Representación de Números en 32 bits

| Número | Punto Fijo Q(16,16) | Punto Flotante |
|--------|---|---|
| 0.0001 | 0.0001 ✅ | 1.00×10^-4 ✅ |
| 1.5 | 1.5 ✅ | 1.50×10^0 ✅ |
| 1000000 | 1000000 ✅ | 1.00×10^6 ✅ |
| 10^-38 | 0 ❌ | 1.00×10^-38 ✅ |
| 10^38 | Overflow ❌ | 1.00×10^38 ✅ |

---

## 🎯 Casos de Uso

### Punto Fijo: Cuándo Usar

#### ✅ Usar Punto Fijo cuando

1. **Hardware limitado:**
   - Microcontroladores (ARM Cortex-M0)
   - FPGA sin FPU
   - Procesadores vintage

2. **Velocidad crítica:**
   - Procesamiento de video en tiempo real
   - Audio digital (DSP)
   - Gráficos 3D (videojuegos)

3. **Rango conocido:**
   - Finanzas (siempre 0.01 a 999,999.99)
   - Sensores (rango físico limitado)
   - Imágenes (0 a 255 o 0.0 a 1.0)

4. **Determinismo:**
   - Sistemas embebidos críticos
   - Donde overflow abrupto es aceptable
   - Cálculos predecibles

#### ❌ Evitar Punto Fijo cuando

- Rango muy amplio (necesitas 10^-300 a 10^300)
- Cálculos científicos con errores acumulativos
- Interoperabilidad con otros sistemas
- Flexibilidad requerida

---

### Punto Flotante: Cuándo Usar

#### ✅ Usar Punto Flotante cuando

1. **Rango dinámico amplio:**
   - Astrofísica (tamaño universo)
   - Física de partículas (tamaño átomo)
   - Química molecular

2. **Cálculos científicos:**
   - Ecuaciones diferenciales
   - Métodos numéricos
   - Interpolación/extrapolación

3. **Generalidad:**
   - Lenguajes de programación
   - Herramientas (Excel, Matlab)
   - Transportabilidad de código

4. **Manejo de casos especiales:**
   - ±Infinito (division por cero)
   - NaN (operaciones inválidas)
   - Underflow gradual (números pequeños)

#### ❌ Evitar Punto Flotante cuando

- Velocidad máxima requerida (y hardware no tiene FPU)
- Determinismo crítico
- Recursos muy limitados
- Rango realmente limitado (desperdicia bits)

---

## 📈 Ejemplo Práctico: Procesamiento de Imagen

### Escenario: Convolver imagen 3x3

**Operación:** Aplicar filtro a cada pixel

```
Pixel = Σ(coef[i,j] × imagen[x+i, y+j])  para i,j ∈ {0,1,2}

Rango de valores:
├─ Entrada: pixels [0, 255]
├─ Coeficientes: [-1, 1]
└─ Resultado: [-765, 765] (overflow en 8 bits)
```

### Solución 1: Punto Fijo Q(10,8)

```
Almacenamiento: 2 bytes por valor
├─ Coeficientes: Q(2,6) con rango [-2, 1.98]
├─ Imagen: Q(8,0) con rango [0, 255]
├─ Resultado: Q(10,8) con rango [-512, 511.996]

Velocidad: Muy rápida (sin FPU)
Precisión: Suficiente para imagen

Ventajas:
├─ Rápido (ALU entera)
├─ Pequeño footprint
├─ Predecible

Desventajas:
├─ Requiere ajustar rango manualmente
├─ Overflow posible si coef > esperado
```

### Solución 2: Punto Flotante IEEE 754

```
Almacenamiento: 4 bytes por valor
├─ Coeficientes: Float directo
├─ Imagen: Float con rango [0, 255]
├─ Resultado: Float con rango [-765, 765]

Velocidad: Más lenta (usa FPU)
Precisión: Sobrada (24 bits vs 10 bits necesarios)

Ventajas:
├─ Automático (sin escalar manualmente)
├─ Sin preocuparse por overflow
├─ Código simple y transportable

Desventajas:
├─ 2x más memoria
├─ Más lento si no hay FPU
└─ Overkill de precisión
```

### Recomendación

```
Punto fijo: ✅ Mejor opción (más rápido, eficiente)
Punto flotante: Aceptable pero con overhead innecesario
```

---

## 🔬 Ejemplo Científico: Integración Numérica

### Método: Simpson's Rule

```
∫ f(x)dx ≈ Σ (f(x_i) + 4f(x_i+1/2) + f(x_i+1)) × h/3
```

### Escenario: Integrar sin(x) de 0 a π

```
Rango de valores:
├─ x: [0, π] ≈ [0, 3.14159]
├─ f(x) = sin(x): [-1, 1]
├─ Acumulador: [0, π] ≈ [0, 3.14159]

Iteraciones: 10^6 (millones de operaciones)
```

### Solución 1: Punto Fijo Q(2,30)

```
Almacenamiento: 4 bytes
Rango: [-2, 1.99]
Precisión: 2^-30 ≈ 9.3 × 10^-10

Problemas:
├─ Necesita aritmética de 64 bits temporalmente
├─ Muy lento (sin hardware especializado)
├─ Error acumulativo aún problemático

Resultado después 10^6 iter: Error ≈ 10^-4 (mediocre)
```

### Solución 2: Punto Flotante IEEE 754 Doble

```
Almacenamiento: 8 bytes
Rango: [±10^-308, ±10^308]
Precisión: 2^-53 ≈ 1.1 × 10^-16

Ventajas:
├─ Totalmente automático
├─ Manejable rangos completamente diferentes
├─ Error bien caracterizado

Resultado después 10^6 iter: Error ≈ 10^-11 (excelente)
```

### Recomendación

```
Punto fijo: ❌ Inadecuado (error acumulativo, complejo)
Punto flotante: ✅ Mejor opción (simple, preciso)
```

---

## 🏆 Resumen Decisional

```
¿Qué usar?

┌─────────────────────────────────────┐
│ ¿Rango dinámico amplio necesario?  │
└─────────┬───────────────────────────┘
          │
     NO   │   SÍ
     ┌────┴────────┐
     │             │
     ▼             ▼
┌──────────────┐   ┌──────────────────┐
│ Punto Fijo   │   │ Punto Flotante   │
│              │   │                  │
│ Más rápido   │   │ Más flexible     │
│ Predecible   │   │ Mejor precisión  │
│ Eficiente    │   │ Estándar         │
└──────────────┘   └──────────────────┘
```

### Matriz de Decisión Final

| Requisito | Punto Fijo | Punto Flotante |
|-----------|-----------|---|
| Velocidad máxima | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Eficiencia memoria | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Rango amplio | ⭐ | ⭐⭐⭐⭐⭐ |
| Precisión relativa | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Facilidad uso | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Determinismo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Hardware requerido | Simple | FPU necesario |

---

## 📚 Referencias Cruzadas

- [Punto Fijo](SECCION_2_1_5_PUNTO_FIJO.md) - Detalles técnicos
- [Punto Flotante](SECCION_2_1_6_PUNTO_FLOTANTE.md) - Detalles técnicos
- IEEE 754 - Standard floating point
- Goldberg, D. "What Every Computer Scientist Should Know About Floating-Point Arithmetic"

---

## ✅ Conclusión

**No hay "mejor" en absoluto - depende del contexto:**

- **Punto Fijo:** El rey en sistemas embebidos y tiempo real
- **Punto Flotante:** Imprescindible en cálculo científico

En duda: **Usa Punto Flotante** (es más seguro y flexible)
