# Sección 2.1.2 - Códigos BCD: Resumen Comparativo

**Comparación Completa de BCD Natural, Exceso-3 y Aiken**

---

## 📌 Introducción

Después de estudiar **4 sistemas para representar números enteros signados** (Magnitud y Signo, Complemento a Base-1, Complemento a Base, Exceso-K), exploramos ahora cómo representar **números decimales con signo**.

### Contexto

- Los números enteros signados (M&S, CB-1, CB) son para **aritmética binaria pura**
- En sistemas con **entrada/salida decimal**, se necesitan códigos que trabajen nativamente en base 10
- Los **códigos BCD** (Binary Coded Decimal) resuelven esto: **codifican cada dígito decimal en 4 bits binarios**

---

## 🔢 Tabla Maestra Comparativa

### Correspondencia de Códigos

```
┌──────────┬──────────────┬───────────┬──────────────┐
│ Decimal  │ BCD Natural  │ Exc-3     │ Aiken 2421   │
│          │ (8421)       │           │              │
├──────────┼──────────────┼───────────┼──────────────┤
│ 0        │ 0000         │ 0011      │ 0000         │
│ 1        │ 0001         │ 0100      │ 0001         │
│ 2        │ 0010         │ 0101      │ 0010         │
│ 3        │ 0011         │ 0110      │ 0011         │
│ 4        │ 0100         │ 0111      │ 0100         │
│ 5        │ 0101         │ 1000      │ 1011         │
│ 6        │ 0110         │ 1001      │ 1100         │
│ 7        │ 0111         │ 1010      │ 1101         │
│ 8        │ 1000         │ 1011      │ 1110         │
│ 9        │ 1001         │ 1100      │ 1111         │
└──────────┴──────────────┴───────────┴──────────────┘
```

### Propiedades Fundamentales

| Propiedad | BCD Natural | Exceso-3 | Aiken |
|---|---|---|---|
| **Bits por dígito** | 4 | 4 | 4 |
| **Rango** | 0-9 | 0-9 | 0-9 |
| **Eficacia** | 62.5% | 62.5% | 62.5% |
| **Codificación** | $d$ (directa) | $d + 3$ | Pesos 2-4-2-1 |
| **Tiene pesos** | ✅ SÍ (8,4,2,1) | ❌ NO | ✅ SÍ (2,4,2,1) |
| **Autocomplementario** | ❌ NO | ✅ SÍ | ✅ SÍ |
| **Suma simple** | ❌ NO | ❌ NO | ❌ NO |
| **Comparación directa** | **✅ SÍ** | **✅ SÍ** | **✅ SÍ** |

---

## 🎯 Características Detalladas

### 1. BCD Natural (8421)

**Codificación:** Cada dígito se codifica directamente en binario (pesos 8-4-2-1)

```
5 → 0101
27 → 0010 0111
```

**Operaciones Aritméticas:**

- **Suma:** Suma binaria + corrección (sumar 6 si resultado > 9)
- **Resta:** Requiere operación de resta separada
- **Comparación:** ✅ Directa (comparación binaria)

**Ventajas:**

- ✅ Comparación directa
- ✅ Conversión fácil a/desde decimal
- ✅ Un único cero
- ✅ Intuitivo

**Desventajas:**

- ❌ Suma requiere corrección compleja
- ❌ Números signados difíciles
- ❌ Multiplicación muy compleja

**Uso histórico:** Entrada/salida en sistemas decimales, calculadoras

---

### 2. BCD Exceso-3 (Excess-3)

**Codificación:** Suma 3 al dígito, luego codifica en BCD Natural

$$\text{Exc3}(d) = \text{BCD}(d + 3)$$

```
5 → 5 + 3 = 8 → 1000
7 → 7 + 3 = 10 → 1010
```

**Propiedad Clave - Autocomplementariedad:**

$$\text{Complemento a 9 de } d = \neg \text{Exc3}(d)$$

Es decir, invertir todos los bits da el complemento a 9.

**Operaciones Aritméticas:**

- **Suma:** Suma binaria + corrección (±3 según acarreo)
- **Resta:** Mediante complemento a 9 (invertir bits, luego sumar)
- **Comparación:** ❌ No directa

**Ventajas:**

- ✅ Autocomplementariedad (invertir bits = complemento a 9)
- ✅ Números signados naturales
- ✅ Resta fácil (mediante complemento)
- ✅ Un único cero

**Desventajas:**

- ❌ Sin pesos (dificulta cálculos)
- ❌ Suma aún requiere corrección
- ❌ Comparación no directa
- ❌ Menos intuitivo que BCD Natural

**Uso histórico:** Calculadoras electromecánicas (1940s-1970s), máquinas decimales tempranas

---

### 3. BCD Aiken (2-4-2-1)

**Codificación:** Pesos 2-4-2-1 (no 8-4-2-1)

$$\text{Valor} = 2b_3 + 4b_2 + 2b_1 + b_0$$

**Ejemplo:**

```
Dígito 5 en Aiken:
5 = 2(1) + 4(0) + 2(1) + 1(1) = 1011
```

**Propiedad Clave - Autocomplementariedad:**

$$\text{Complemento a 9 de } d = \neg \text{Aiken}(d)$$

Igual que Exceso-3: invertir bits = complemento a 9.

**Operaciones Aritméticas:**

- **Suma:** Suma binaria + corrección (compleja, específica)
- **Resta:** Mediante complemento a 9 (invertir bits, luego sumar)
- **Comparación:** ❌ No directa

**Ventajas:**

- ✅ Autocomplementariedad (invertir bits = complemento a 9)
- ✅ Tiene pesos (mejor que Exceso-3 para algunos cálculos)
- ✅ Números signados naturales
- ✅ Detección de errores (6 códigos inválidos: 0101-1010)

**Desventajas:**

- ❌ Pesos irregulares (2-4-2-1) menos intuitivos que 8-4-2-1
- ❌ Suma aún compleja
- ❌ Comparación no directa
- ❌ Menos estándar que BCD Natural

**Uso histórico:** Computadora Mark I de Harvard (1944), algunas máquinas tempranas

---

## 📊 Tabla Operacional

### Suma

| Código | Método | Complejidad | Requiere Conversión |
|---|---|---|---|
| **BCD Natural** | Suma binaria + corrección (+6 si >9) | Media | Dentro del rango |
| **Exceso-3** | Suma binaria + corrección (±3 según acarreo) | Media | Dentro del rango |
| **Aiken** | Suma binaria + corrección (específica) | Media-Alta | Valores específicos |

### Resta

| Código | Método | Complejidad |
|---|---|---|
| **BCD Natural** | Resta binaria ordinaria | Alta |
| **Exceso-3** | Complemento a 9 (invertir bits) + suma | Media |
| **Aiken** | Complemento a 9 (invertir bits) + suma | Media |

### Números Signados

| Código | Método | Facilidad |
|---|---|---|
| **BCD Natural** | Bit de signo separado o complemento complejo | Difícil |
| **Exceso-3** | Complemento a 9 de todo el número | Fácil |
| **Aiken** | Complemento a 9 de todo el número | Fácil |

---

## 🔄 Evolución: Búsqueda del Sistema Ideal

```
Objetivo inicial:
- Codificar dígitos decimales en binario
- Facilitar operaciones aritméticas
- Soportar números signados naturalmente
- Minimizar circuitería de corrección

        ↓

BCD Natural (8421)
├─ ✅ Tiene pesos
├─ ✅ Comparación directa
├─ ❌ Sin autocomplementariedad
└─ ❌ Números signados difíciles

        ↓ (Buscar autocomplementariedad)

Exceso-3
├─ ✅ Autocomplementariedad
├─ ✅ Números signados fáciles
├─ ✅ Comparación directa
├─ ❌ Sin pesos
└─ ❌ Códigos prohibidos

        ↓ (Buscar pesos + autocomplementariedad)

Aiken (2-4-2-1)
├─ ✅ Autocomplementariedad
├─ ✅ Tiene pesos
├─ ✅ Números signados fáciles
├─ ✅ Detección de errores
├─ ✅ Comparación directa
├─ ❌ Pesos irregulares
└─ ❌ Códigos prohibidos

        ↓ (Modern era)

Conclusión:
No hay un "mejor" código universal.
Cada uno es óptimo para ciertos escenarios.
```

---

## 🎯 Matriz de Decisión: ¿Cuál Usar?

### Para Entrada/Salida Decimal

**Usar BCD Natural:**

- Conversión fácil a/desde decimal
- Comparación de valores
- Entrada desde teclado numérico

### Para Aritmética Decimal Signada

**Usar Exceso-3 o Aiken:**

- Complementación a 9 trivial (invertir bits)
- Resta por suma
- Números negativos naturales

### Para Detectar Errores de Transmisión

**Usar Aiken:**

- 6 códigos "prohibidos" (0101-1010)
- Cualquier otro código indica corrupción
- Aplicable si confiabilidad es crítica

### Para Máquinas Antiguas (Educativo)

**Toda la triada:**

- Mark I → Aiken
- Calculadoras electromecánicas → Exceso-3
- Sistemas I/O → BCD Natural

---

## 📈 Tabla de Eficacia

Todos los códigos BCD tienen la **misma eficacia**:

$$\text{Eficacia} = \frac{10 \text{ valores}}{16 \text{ combinaciones}} = 62.5\%$$

**Comparación con otros sistemas:**

| Sistema | Rango | Bits Necesarios | Eficacia |
|---------|-------|---|---|
| Naturales binarios | 0-9 | 4 | 100% (óptimo) |
| BCD Natural | 0-9 | 4 | 62.5% |
| BCD Exc3 | 0-9 | 4 | 62.5% |
| BCD Aiken | 0-9 | 4 | 62.5% |
| Números naturales | 0-99 | 7 | 100% |
| BCD x2 | 0-99 | 8 | 62.5% |

**Conclusión:** BCD es 20% menos eficiente que binarios puros, pero facilita interfacing con sistemas decimales.

---

## 🔗 Relación con Sistemas de Enteros Signados

### Revisión de Sistemas Anteriores

```
Para ENTEROS SIGNADOS (binarios):
- M&S (Magnitud y Signo) → IEEE 754 mantisa
- CB-1 (Complemento a B-1) → Histórico/educativo
- CB (Complemento a Base) → Todos los procesadores
- ExcK (Exceso-K) → IEEE 754 exponentes

Para DECIMALES SIGNADOS (decimales):
- BCD Natural → I/O, sin signo
- BCD Exc3 → Números signados
- BCD Aiken → Números signados + pesos
```

### Combinación: IEEE 754 Decimal (DPD)

Basándose en BCD, IEEE 754 define **Decimal Floating Point**:

- Mantisa en BCD densamente empaquetado (Densely Packed Decimal)
- Exponente en Exceso-K
- Más eficiente que BCD simple

---

## 💡 Ventajas Comparativas

### BCD Natural

```
✅ MEJOR EN:
  - Conversión decimal ↔ BCD
  - Comparación de valores
  - Legibilidad (cada 4 bits = 1 dígito)
  - Entrada de datos

❌ PEOR EN:
  - Operaciones signadas
  - Suma/resta
  - Números negativos
```

### Exceso-3

```
✅ MEJOR EN:
  - Suma y resta (con corrección)
  - Complemento a 9 (trivial)
  - Números signados
  - Detectar sobre/desbordamiento

❌ PEOR EN:
  - Conversión desde decimal
  - Intuitividad
  - Pesos para operaciones rápidas
  - Códigos prohibidos (6 inválidos)
```

### Aiken

```
✅ MEJOR EN:
  - Suma y resta (con corrección)
  - Complemento a 9 (trivial)
  - Números signados
  - Tiene pesos (mejor que Exc3)
  - Detección de errores (6 inválidos)

❌ PEOR EN:
  - Pesos no estándar (2-4-2-1)
  - Conversión desde decimal
  - Menos conocido
  - Códigos prohibidos (6 inválidos)
```

---

## 📝 Ejemplos Operacionales

### Ejemplo 1: Sumar 47 + 35 = 82

#### En BCD Natural

```
4 → 0100      3 → 0011
7 → 0111      5 → 0101

  0100 0111  (47)
+ 0011 0101  (35)
-----------
  0111 1100  (Resultado parcial, dígito inferior inválido)

Corrección dígito inferior: 1100 > 9
  1100 + 0110 = 10010 (Acarreo 1, dígito 0010=2)

Dígito superior + acarreo:
  0111 + 0001 = 1000 (8)

Resultado final: 1000 0010 (82) ✅
```

#### En Exceso-3

```
4 → 0111      3 → 0110
7 → 1010      5 → 1000

  0111 1010  (47 en Exc3)
+ 0110 1000  (35 en Exc3)
-----------
  1110 0010  (Resultado parcial)

Acarreo final: NO
Corrección: Restar 3 (0011) a cada dígito
  1110 - 0011 = 1011 (Dígito 8 en Aiken? No...)

Este proceso es más complejo en Exc3, requiere lógica especial.
```

#### En Aiken

```
4 → 0100      3 → 0011
7 → 1101      5 → 1011

  0100 1101  (47 en Aiken)
+ 0011 1011  (35 en Aiken)
-----------
  1000 1000  (Resultado parcial)

Interpretación: Dígitos 8 y 8 ✓
Resultado final: 1000 1000 (82 en Aiken) ✅

(Aiken maneja mejor algunas sumas sin corrección)
```

---

## 🎓 Contexto Histórico

### Timeline

```
1940
│  BCD Natural (8-4-2-1) ← Estándar para entrada/salida
│
├─→ Exceso-3 ← Máquinas electromecánicas tempranas
│   (1940s)   ✓ Autocomplementario
│             ✓ Facilitaba resta por complementación
│
├─→ BCD Aiken (2-4-2-1) ← Computadora Mark I (Harvard)
│   (1944)                ✓ Pesos + autocomplementario
│                         ✓ Solución intermedia óptima
│
└─→ COBOL, Fortran ← Decimales en software
    (1950s-60s)     ✓ BCD Natural para I/O
                    ✓ Binarios para cómputo

1980+: Procesadores binarios puros
       BCD relegado a interfacing/legado
```

---

## 🚀 Conclusiones

### Resumen de la Triada BCD

| Aspecto | Conclusión |
|---|---|
| **Mejor para I/O** | BCD Natural (8-4-2-1) |
| **Mejor para Aritmética Signada** | Exceso-3 o Aiken |
| **Mejor balance** | Aiken (2-4-2-1) |
| **Menos complejo** | BCD Natural |
| **Más versátil** | Depende del contexto |

### Principio de Diseño

La elección de código BCD refleja un **trade-off fundamental**:

- **BCD Natural:** Optimizado para conversión ↔ decimal
- **Exceso-3:** Optimizado para aritmética signada (sin pesos)
- **Aiken:** Optimizado para balance (pesos + autocomplementario)

No existe un "mejor" código universal. La elección depende de:

1. **Operaciones dominantes** (¿suma, comparación, conversión?)
2. **Arquitectura del hardware** (¿necesita pesos?)
3. **Necesidad de números signados** (¿sí o no?)
4. **Requerimientos de error-detection** (¿detección necesaria?)

---

## 📚 Documentación Relacionada

### BCD Específicos

- [BCD Natural (8-4-2-1)](SECCION_2_1_2_BCD_NATURAL.md)
- [BCD Exceso-3](SECCION_2_1_2_1_BCD_EXC3.md)
- [BCD Aiken (2-4-2-1)](SECCION_2_1_2_2_BCD_AIKEN.md)

### Números Enteros Signados (Binarios)

- [Magnitud y Signo (M&S)](SECCION_2_1_1_7_MS.md)
- [Complemento a Base-1 (CB-1)](SECCION_2_1_1_7_CB_MENOS_1.md)
- [Complemento a Base (CB)](SECCION_2_1_1_7_CB.md)
- [Exceso-K (ExcK)](SECCION_2_1_1_7_EXCESO_K.md)

### IEEE 754 (Contexto)

- Mantisa: M&S (magnitud con signo separado)
- Exponentes: ExcK (Exceso-127 para 32-bit)
- Decimales: DPD (Densely Packed Decimal, basado en BCD)

---

**Conclusión Final:** Los códigos BCD representan un paso intermedio importante en la historia de la computación: después de resolver representación de enteros signados en binario, surgen los BCD para facilitar sistemas que operan nativamente en decimal. Hoy son principalmente históricos/educativos, pero conceptualmente vitales para entender arquitectura digital.
