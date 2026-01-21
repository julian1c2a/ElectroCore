# ÍNDICE: Sección 2.1.1.7 - Números Enteros Signados

**Documentación Completa de 4 Sistemas de Representación Numérica**

---

## 📚 Documentación Teórica

### 1. [SECCION_2_1_1_7_MS.md](SECCION_2_1_1_7_MS.md) - Magnitud y Signo

- **Líneas:** 284
- **Contenido:**
  - Concepto fundamental
  - Operación de negación
  - Representación en diferentes bases
  - Rango y capacidad
  - Operaciones aritméticas
  - Ventajas y desventajas
  - Casos especiales (dos ceros)
- **Nivel:** Principiante → Intermedio
- **Aplicación:** Educativa / Histórica

### 2. [SECCION_2_1_1_7_CB_MENOS_1.md](SECCION_2_1_1_7_CB_MENOS_1.md) - Complemento a la Base Menos 1

- **Líneas:** 425+
- **Contenido:**
  - Operación opCBm1(d) = B - 1 - d
  - Representación con end-around carry
  - Notación clarificada: '+' ≠ +
  - Suma modular con carry especial
  - Rango y capacidad (dos ceros)
  - Comparación con M&S
  - Análisis de eficacia
- **Nivel:** Intermedio
- **Aplicación:** Educativa / Histórica
- **Nota Especial:** Clarificación de notación +

### 3. [SECCION_2_1_1_7_CB.md](SECCION_2_1_1_7_CB.md) - Complemento a la Base

- **Líneas:** 300+
- **Contenido:**
  - Operación opCB = opCBm1 + 1
  - Representación = número mod B^l
  - Suma ordinaria módulo B^l
  - Multiplicación simple
  - Rango [-B^(l-1), B^(l-1) - 1]
  - 100% de eficacia
  - Comparación con M&S y CB-1
  - **ESTÁNDAR INDUSTRIAL**
- **Nivel:** Intermedio → Avanzado
- **Aplicación:** Standard - **TODOS LOS PROCESADORES**
- **Nota:** Demostrada la superioridad técnica

### 4. [SECCION_2_1_1_7_EXCESO_K.md](SECCION_2_1_1_7_EXCESO_K.md) - Exceso a K (Biased)

- **Líneas:** 300+
- **Contenido:**
  - Concepto de desplazamiento por K
  - Representación: ReprExcK(a) = a + K
  - Rango flexible: [-K, B^l - K - 1]
  - 100% de eficacia en cualquier base
  - Operaciones: Suma (#), Resta, Multiplicación
  - Comparación directa
  - IEEE 754 contexto (K=127 para exponentes)
  - Flexibilidad de elección de K
- **Nivel:** Avanzado
- **Aplicación:** Standard - **IEEE 754 EXPONENTES**
- **Nota:** Flexible y poderoso para cualquier base

### 5. [RESUMEN_ENTEROS_SIGNADOS.md](RESUMEN_ENTEROS_SIGNADOS.md) - Resumen Ejecutivo

- **Líneas:** 360
- **Contenido:**
  - Resumen de lo implementado
  - Tabla comparativa de características
  - Archivos generados
  - Validación completada
  - Resultados clave
  - Commits realizados
  - Tabla visual binario 4-bit
  - Insights principales
  - Próximos pasos
  - Conclusión y status
- **Nivel:** Resumen / Gerencial
- **Audiencia:** Supervisores, gestores, revisores

### 6. [CONCLUSIONES.md](CONCLUSIONES.md) - Análisis Final

- **Líneas:** 345
- **Contenido:**
  - Resumen de trabajo realizado
  - Análisis comparativo exhaustivo
  - Descubrimientos clave
  - Validación completada
  - Calidad del código
  - Valor educativo
  - Próximos pasos sugeridos
  - Status final
- **Nivel:** Ejecutivo
- **Audiencia:** Decisión makers, revisores de código, educadores

---

## 📚 Sección 2.1.2 - Códigos BCD (Decimal)

**Representación de Dígitos Decimales Usando 4 Bits Binarios**

### Introducción: BCD

Después de resolver la representación de **números enteros signados en binario** (M&S, CB-1, CB, ExcK), exploramos cómo representar **números decimales con signo**.

Los **códigos BCD** (Binary Coded Decimal) codifican cada dígito decimal (0-9) en 4 bits binarios, permitiendo:

- ✅ Interfacing con sistemas decimales (entrada/salida)
- ✅ Aritmética nativa en base 10
- ✅ Facilitar sistemas de números signados

### Documentación de 3 Códigos BCD

#### 1. [SECCION_2_1_2_BCD_NATURAL.md](SECCION_2_1_2_BCD_NATURAL.md) - BCD Natural (8421)

- **Líneas:** 280+
- **Codificación:** Cada dígito = BCD Natural directo
  - $\text{Repr}(d) = d$ (en 4 bits, pesos 8-4-2-1)
- **Ejemplo:** 5 = 0101, 27 = 0010 0111
- **Propiedades:**
  - ✅ Comparación directa (binaria)
  - ❌ Autocomplementario: NO
  - ❌ Suma compleja (requiere corrección +6 si >9)
  - ✅ Un único cero
  - ✅ Intuitivo (cada 4 bits = 1 dígito decimal)
- **Eficacia:** 62.5% (10/16)
- **Nivel:** Principiante → Intermedio
- **Uso:** Entrada/salida decimal, calculadoras, displays
- **Época:** Ampliamente usado en sistemas con I/O decimal

#### 2. [SECCION_2_1_2_1_BCD_EXC3.md](SECCION_2_1_2_1_BCD_EXC3.md) - BCD Exceso-3

- **Líneas:** 240+
- **Codificación:** Suma 3, luego BCD Natural
  - $\text{Exc3}(d) = \text{BCD}(d + 3)$
- **Ejemplo:** 5 = 1000 (porque 5+3=8), 7 = 1010
- **Propiedades Clave:**
  - ✅ **Autocomplementario:** Complemento a 9 = invertir bits
  - ❌ Sin pesos (dificulta cálculos rápidos)
  - ❌ Suma compleja (requiere corrección ±3)
  - ✓ Números signados naturales
  - ✅ Un único cero
- **Eficacia:** 62.5% (10/16)
- **Nivel:** Intermedio
- **Uso:** Máquinas electromecánicas (1940s-1970s), aritmética signada
- **Ventaja:** Resta por suma mediante complemento a 9

#### 3. [SECCION_2_1_2_2_BCD_AIKEN.md](SECCION_2_1_2_2_BCD_AIKEN.md) - BCD Aiken (2-4-2-1)

- **Líneas:** 280+
- **Codificación:** Pesos 2-4-2-1 (no 8-4-2-1)
  - $\text{Valor} = 2b_3 + 4b_2 + 2b_1 + b_0 = d$
- **Ejemplo:** 5 = 1011, 9 = 1111
- **Propiedades Clave:**
  - ✅ **Autocomplementario:** Complemento a 9 = invertir bits
  - ✅ Tiene pesos (mejor que Exceso-3)
  - ❌ Pesos irregulares (2-4-2-1)
  - ✅ Números signados naturales
  - ✅ Detección de errores (6 códigos "prohibidos": 0101-1010)
  - ✅ Un único cero
- **Eficacia:** 62.5% (10/16)
- **Nivel:** Intermedio → Avanzado
- **Uso:** Computadora Mark I (1944), balance entre BCD Natural y Exc3
- **Inventor:** Howard Hathaway Aiken (1944)
- **Ventaja:** Combina pesos + autocomplementariedad

#### 4. [SECCION_2_1_2_RESUMEN_BCD.md](SECCION_2_1_2_RESUMEN_BCD.md) - Comparativa Completa

- **Líneas:** 380+
- **Contenido:**
  - Tabla maestra comparativa
  - Propiedades de los 3 códigos
  - Matriz de decisión (cuál usar)
  - Ejemplos operacionales (suma 47+35)
  - Timeline histórico
  - Análisis de eficacia
  - Ventajas comparativas por aspecto
  - Relación con sistemas anteriores (M&S, CB, ExcK)
  - IEEE 754 Decimal (DPD)
- **Nivel:** Resumen / Gerencial
- **Audiencia:** Decisión makers, educadores, arquitectos

---

### Tabla Maestra: Los 3 Códigos BCD

```
Dígito  │ BCD Natural │ Exceso-3 │ Aiken (2-4-2-1)
        │  (8421)     │          │
────────┼─────────────┼──────────┼────────────────
0       │ 0000        │ 0011     │ 0000
1       │ 0001        │ 0100     │ 0001
2       │ 0010        │ 0101     │ 0010
3       │ 0011        │ 0110     │ 0011
4       │ 0100        │ 0111     │ 0100
5       │ 0101        │ 1000     │ 1011
6       │ 0110        │ 1001     │ 1100
7       │ 0111        │ 1010     │ 1101
8       │ 1000        │ 1011     │ 1110
9       │ 1001        │ 1100     │ 1111
────────┴─────────────┴──────────┴────────────────
Pesos   │ 8-4-2-1 ✅  │ NO ❌    │ 2-4-2-1 ✅
Autocomp│ NO ❌       │ SÍ ✅    │ SÍ ✅
Comparac│ SÍ ✅       │ NO ❌    │ NO ❌
```

### Propiedades Comparadas

| Propiedad | BCD Natural | Exceso-3 | Aiken |
|-----------|-------------|----------|--------|
| **Bits/dígito** | 4 | 4 | 4 |
| **Eficacia** | 62.5% | 62.5% | 62.5% |
| **Pesos** | 8-4-2-1 | NO | 2-4-2-1 |
| **Autocomplementario** | NO | SÍ | SÍ |
| **Suma simple** | NO | NO | NO |
| **Comparación** | SÍ | NO | NO |
| **Números signados** | Difícil | Fácil | Fácil |
| **Uso** | I/O decimal | Aritmética | Mark I |
| **Época** | Estándar | 1940s-70s | 1944+ |

### Matriz de Decisión

**¿BCD Natural?**

- ✅ Para entrada/salida decimal
- ✅ Para comparación de valores
- ✅ Para conversión fácil decimal ↔ BCD

**¿Exceso-3?**

- ✅ Para aritmética decimal signada
- ✅ Cuando autocomplementariedad es crítica
- ✅ Para máquinas electromecánicas antiguas

**¿Aiken?**

- ✅ Para balance: pesos + autocomplementariedad
- ✅ Para detección de errores (códigos prohibidos)
- ✅ Estudio histórico (Mark I)

---

## 💻 Implementación de Código

### 1. [core/enteros_signados.py](core/enteros_signados.py) - M&S y CB-1

- **Líneas:** 1,001
- **Funciones principales:**
  - **M&S:**
    - `repr_MS(numero, base, longitud)`
    - `MS_a_decimal(palabra, base)`
    - `negacion_MS(palabra)`
    - `suma_MS(palabra_a, palabra_b, base)`
    - `es_negativo_MS(palabra)`
  - **CB-1:**
    - `opCBm1_digito(digito, base)`
    - `opCBm1_palabra(palabra, base)`
    - `repr_CBm1(numero, base, longitud)`
    - `CBm1_a_decimal(palabra, base)`
    - `suma_CBm1(palabra_a, palabra_b, base)` (con end-around carry)
    - `analizar_representacion_CBm1(base, longitud)`
    - `generar_tabla_CBm1(base, longitud)`
    - `explicar_operacion_CBm1()`
- **Características:**
  - Type hints completos
  - Error handling robusto
  - Docstrings exhaustivos
  - Ejemplos en docstrings

### 2. [core/exceso_k_representacion.py](core/exceso_k_representacion.py) - ExcK

- **Líneas:** 350+
- **Funciones principales:**
  - `repr_ExcK(numero, base, longitud, K)`
  - `ExcK_a_decimal(palabra, base, K)`
  - `suma_ExcK(palabra_a, palabra_b, base, K)` (A + B - K)
  - `resta_ExcK(palabra_a, palabra_b, base, K)` (A - B + K)
  - `multiplicacion_ExcK(palabra_a, palabra_b, base, K)`
  - `analizar_representacion_ExcK(base, longitud, K)`
  - `generar_tabla_ExcK(base, longitud, K)`
  - `explicar_operacion_ExcK()`
- **Características:**
  - Soporte para cualquier base
  - Soporte para cualquier K
  - Manejo de overflow
  - Verificación de rango

---

## 🎯 Demostraciones Interactivas

### 1. [demo_ms_simple.py](demo_ms_simple.py) - Magnitud y Signo

- **Demostraciones:**
  1. Conceptos básicos
  2. Rango y capacidad
  3. Conversiones paso a paso
  4. Operaciones en M&S
  5. Ventajas y desventajas
- **Ejecución:** `python demo_ms_simple.py`
- **Status:** ✅ Completo y probado

### 2. [demo_cb1.py](demo_cb1.py) - Complemento a la Base Menos 1

- **Demostraciones:** 7
  1. Operación opCBm1 básica
  2. Representación en CB-1
  3. Tablas de valores
  4. Sumas modulares
  5. Dos ceros
  6. Rango y capacidad
  7. Explicaciones paso a paso
- **Ejecución:** `python demo_cb1.py`
- **Status:** ✅ Completo con notación clarificada

### 3. [demo_cb.py](demo_cb.py) - Complemento a la Base

- **Demostraciones:** 9
  1. Operación opCB básica
  2. Representación en CB
  3. Tablas de valores
  4. Suma ordinaria (sin end-around carry)
  5. Resta
  6. Multiplicación
  7. Comparación directa
  8. Superioridad vs CB-1
  9. Comparación con todas las representaciones
- **Ejecución:** `python demo_cb.py`
- **Status:** ✅ Completo y probado

### 4. [demo_exceso_k.py](demo_exceso_k.py) - Exceso a K

- **Demostraciones:** 10
  1. Conceptos básicos
  2. Representación con diferentes K
  3. Tablas de valores
  4. Suma (A + B - K)
  5. Resta (A - B + K)
  6. Multiplicación ((A-K)*(B-K)+K)
  7. IEEE 754 estándar (K=127)
  8. Flexibilidad de K
  9. Rango y capacidad
  10. Explicaciones paso a paso
- **Ejecución:** `python demo_exceso_k.py`
- **Status:** ✅ Completo y probado

---

## 📊 Análisis y Comparativas

### [generar_tabla_comparativa.py](generar_tabla_comparativa.py)

- **Contenido:**
  - Tabla lado a lado de 4 representaciones
  - Estadísticas de eficacia
  - Análisis operacional (suma, multiplicación, comparación, rango)
- **Ejecución:** `python generar_tabla_comparativa.py`
- **Status:** ✅ Completo

### [verificar_demostraciones.py](verificar_demostraciones.py)

- **Propósito:**
  - Script de verificación automatizada
  - Ejecuta todas las demostraciones
  - Reporta status de éxito/fallo
  - Resumen final
- **Ejecución:** `python verificar_demostraciones.py`
- **Status:** ✅ Completo

---

## 📖 Guía de Lectura Recomendada

### Para Principiantes

1. Empezar con `SECCION_2_1_1_7_MS.md`
2. Ejecutar `demo_ms_simple.py`
3. Leer `SECCION_2_1_1_7_CB_MENOS_1.md`
4. Ejecutar `demo_cb1.py`

### Para Desarrolladores

1. Leer `SECCION_2_1_1_7_CB.md` (relevancia industrial)
2. Estudiar `core/enteros_signados.py` (código)
3. Ejecutar `demo_cb.py`
4. Revisar `generar_tabla_comparativa.py`

### Para Especialistas en Punto Flotante

1. Leer `SECCION_2_1_1_7_EXCESO_K.md` (IEEE 754)
2. Estudiar `core/exceso_k_representacion.py`
3. Ejecutar `demo_exceso_k.py` (especialmente Demo 7)
4. Consultar `CONCLUSIONES.md`

### Para Gerentes/Supervisores

1. Leer `RESUMEN_ENTEROS_SIGNADOS.md` (quick overview)
2. Revisar `CONCLUSIONES.md` (análisis estratégico)
3. Consultar tabla comparativa en `generar_tabla_comparativa.py`

---

## 🔗 Relaciones entre Documentos

```
CONCLUSIONES.md ← Análisis final de todo
    ↓
RESUMEN_ENTEROS_SIGNADOS.md ← Síntesis ejecutiva
    ↓
M&S ← CB-1 ← CB ← ExcK
    ↓      ↓     ↓     ↓
  demo    demo   demo   demo
    ↓      ↓     ↓     ↓
generar_tabla_comparativa.py ← Análisis visual
```

---

## 📊 Estadísticas

| Aspecto | Cantidad |
|---------|----------|
| Documentos de Teoría | 6 |
| Líneas de Documentación | 1,300+ |
| Módulos Python | 2 |
| Líneas de Código | 1,350+ |
| Funciones Implementadas | 30+ |
| Demostraciones | 30+ |
| Commits | 11 |
| Status | ✅ COMPLETO |

---

## 🎓 Conceptos Cubiertos

- ✅ Sistemas de numeración con signo
- ✅ Representación binaria y en otras bases
- ✅ Rango y capacidad de representación
- ✅ Eficacia y desperdicio de combinaciones
- ✅ Operaciones aritméticas (suma, resta, multiplicación)
- ✅ End-around carry en CB-1
- ✅ Overflow y underflow
- ✅ Estándares industriales (CB en procesadores, ExcK en IEEE 754)
- ✅ Análisis comparativo y justificación técnica
- ✅ Aplicaciones prácticas

---

## 🔗 Proyectos Relacionados

Esta sección es la base para:

- Sección 2.1.2: Números en Punto Flotante (IEEE 754)
- Sección 2.1.3: Códigos Especiales (BCD, Gray, etc.)
- Sección 2.1.4: Operaciones Aritméticas
- Módulos de simulación de ALU
- Ejercicios interactivos

---

## 📞 Preguntas Frecuentes

**P: ¿Cuál es la mejor representación?**
A: Depende del contexto:

- Enteros → CB (estándar industrial)
- Exponentes → ExcK (IEEE 754)
- Educación → Cualquiera (cada una enseña algo)

**P: ¿Por qué CB-1 aún existe?**
A: Valor histórico y educativo. Ayuda a entender el desarrollo hacia CB.

**P: ¿ExcK se usa en enteros?**
A: No en sistemas estándar. CB es superior para enteros. ExcK brilla en exponentes.

**P: ¿Todos los procesadores usan CB?**
A: Sí. x86, ARM, MIPS, PowerPC, todos usan Complemento a Dos (CB).

**P: ¿IEEE 754 usa solo ExcK?**
A: El exponente usa ExcK, pero la mantisa usa otra representación (significand).

---

## 📝 Notas

- Toda la documentación puede compilarse a PDF usando Pandoc
- Todo el código es Python 3.6+
- Todos los ejemplos son ejecutables
- Todos los conceptos están respaldados matemáticamente
- Todos los algoritmos han sido validados

---

**Última actualización:** 2024
**Status:** ✅ COMPLETO Y LISTO PARA PRODUCCIÓN
