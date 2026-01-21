# Sección 2.1.2.1 - BCD Exceso-3 (Excess-3)

**Código Autocomplementario para Aritmética Decimal Signada**

---

## 📌 Concepto Fundamental

### Definición

**BCD Exceso-3** es un sistema de codificación de **dígitos decimales** donde cada dígito se representa mediante:

$$\text{ReprExc3}(d) = \text{BCD Natural}(d + 3)$$

Es decir, se suma 3 al dígito decimal y luego se codifica el resultado en BCD Natural de 4 bits.

### Estructura

```
Dígito decimal: d
              ↓
Suma 3:       d + 3
              ↓
Codifica en BCD Natural (4 bits)
              ↓
Representación Exceso-3
```

### Ejemplo: Codificación de dígitos

```
Dígito 0: 0 + 3 = 3 → 0011 (Exc3 para 0)
Dígito 1: 1 + 3 = 4 → 0100 (Exc3 para 1)
Dígito 5: 5 + 3 = 8 → 1000 (Exc3 para 5)
Dígito 9: 9 + 3 = 12 → 1100 (Exc3 para 9)
```

---

## 🔢 Tabla de Correspondencia

| Decimal | BCD Natural | Exceso-3 | Decimal | BCD Natural | Exceso-3 |
|---------|------------|----------|---------|------------|----------|
| 0 | 0000 | **0011** | 5 | 0101 | 1000 |
| 1 | 0001 | **0100** | 6 | 0110 | 1001 |
| 2 | 0010 | **0101** | 7 | 0111 | 1010 |
| 3 | 0011 | **0110** | 8 | 1000 | 1011 |
| 4 | 0100 | **0111** | 9 | 1001 | 1100 |
| **Valores no usados** | 1010-1111 | 0000-0010, 1101-1111 | | |

**Observación clave:** Los 6 valores "no usados" (códigos prohibidos) son **exactamente complementarios** en Exceso-3:

- Códigos prohibidos: 0000-0010 y 1101-1111
- Estos son los complementos a 9 de sí mismos

---

## ✅ Validación de Códigos Exceso-3

### ¿Cómo Saber si un Código es Exceso-3 Válido?

Dado un código de 4 bits: $d_3 d_2 d_1 d_0$

**Un código es Exc3 ERRÓNEO si:**

$$d_3 = d_2 \text{ Y } (d_1 \neq d_0 \text{ O } d_2 = d_1)$$

En otras palabras: Si los bits 3 y 2 son iguales, es erróneo si además (bits 1 y 0 son diferentes) O (bits 2 y 1 son iguales).

**Ejemplos de validación:**

```
0011 (0) → d3=0, d2=0  → d3=d2=0, d1=1, d0=1 → d1=d0 y d2=d1? (0=1?) NO → ✅ VÁLIDO
0100 (1) → d3=0, d2=1  → d3≠d2 → NO se aplica restricción → ✅ VÁLIDO
1000 (5) → d3=1, d2=0  → d3≠d2 → NO se aplica restricción → ✅ VÁLIDO
1100 (9) → d3=1, d2=1  → d3=d2=1, d1=0, d0=0 → d1=d0 y d2=d1? (0=1?) NO → ✅ VÁLIDO
0000    → d3=0, d2=0  → d3=d2=0, d1=0, d0=0 → d1=d0 SI y d2=d1 SI → ❌ INVÁLIDO
1101    → d3=1, d2=1  → d3=d2=1, d1=0, d0=1 → d1≠d0 SÍ → ❌ INVÁLIDO
```

---

## 🎯 Propiedad Fundamental: Autocomplementariedad

### ¿Qué es Autocomplementariedad?

Un código es **autocomplementario** cuando el complemento a 9 de un dígito $d$ se obtiene invirtiendo todos los bits (NOT lógico) de la representación del dígito:

$$\text{ReprExc3}(\overline{9-d}) = \neg \text{ReprExc3}(d)$$

donde $\overline{9-d}$ es el complemento a 9 del dígito.

### Demostración de Autocomplementariedad

**Verificación para todos los dígitos:**

| Dígito | Complemento a 9 | Exc3(d) | NOT Exc3(d) | Exc3(9-d) | ¿Iguales? |
|--------|----------------|---------|-----------|-----------|-----------|
| 0 | 9 | 0011 | 1100 | 1100 | ✅ |
| 1 | 8 | 0100 | 1011 | 1011 | ✅ |
| 2 | 7 | 0101 | 1010 | 1010 | ✅ |
| 3 | 6 | 0110 | 1001 | 1001 | ✅ |
| 4 | 5 | 0111 | 1000 | 1000 | ✅ |
| 5 | 4 | 1000 | 0111 | 0111 | ✅ |
| 6 | 3 | 1001 | 0110 | 0110 | ✅ |
| 7 | 2 | 1010 | 0101 | 0101 | ✅ |
| 8 | 1 | 1011 | 0100 | 0100 | ✅ |
| 9 | 0 | 1100 | 0011 | 0011 | ✅ |

**Conclusión:** Exceso-3 es **perfectamente autocomplementario** 🎯

### ¿Por Qué Funciona?

Matemáticamente:

$$\text{Exc3}(\overline{9-d}) = (9-d) + 3 = 12 - d = 15 - (d + 3) = \text{NOT}[\text{Exc3}(d)]$$

porque $15 - x$ es el complemento bit a bit de $x$ en 4 bits.

---

## ➕ Aritmética: Suma en Exceso-3

### Suma de un número signado con Complemento a 9

Para representar números con signo usando complementación a base 10 (complemento a 9), Exceso-3 es ideal.

### Algoritmo de Suma

**Para sumar $A$ y $B$ en Exceso-3:**

1. Sumar los códigos Exceso-3 como si fueran binarios ordinarios
2. Si hay acarreo final, sumar 3 al resultado
3. Si no hay acarreo final, restar 3 del resultado

### Ejemplo 1: Suma sin acarreo

```
Suma: 5 + 3 en Exceso-3

5 en Exc3:  1000
+ 3 en Exc3: 0110
-----------
           1110

Acarreo final: NO → Restar 3
1110 - 0011 = 1011 (que es 8 en Exc3)

Verificación: 5 + 3 = 8 ✅
```

### Ejemplo 2: Suma con acarreo

```
Suma: 7 + 6 en Exceso-3

7 en Exc3:  1010
+ 6 en Exc3: 1001
-----------
          10011

Acarreo final: SÍ (el 1 de la izquierda) → Sumar 3
0011 + 0011 = 0110

Pero interpretamos con el acarreo anterior, resulta 1 0110, que sería...
Interpretación: Necesitamos procesarlo correctamente.

Método alternativo: Procesar digito a dígito como en BCD Natural
```

### Resta en Exceso-3

Para restar $B$ de $A$:

1. Obtener el complemento a 9 de $B$ (invertir todos los bits)
2. Sumar $A$ con el complemento a 9 de $B$
3. Aplicar la regla de acarreo anterior

**Ventaja:** No necesitamos una operación de resta separada, solo complementación (que es trivial: invertir bits).

---

## 📊 Propiedades de Exceso-3

| Propiedad | Valor |
|-----------|-------|
| **Bits por dígito** | 4 |
| **Rango por dígito** | 0-9 |
| **Eficacia** | 62.5% (10/16) |
| **Tiene pesos** | NO |
| **Autocomplementario** | **SÍ ✅** |
| **Suma directa** | NO (requiere corrección) |
| **Resta** | Mediante complemento a 9 |
| **Comparación directa** | **SÍ ✅** (igual a binario natural) |
| **Códigos válidos** | 10 (0011-0111, 1000-1100) |
| **Códigos prohibidos** | 6 (0000-0010, 1101-1111) |

---

## 🔢 Representación de Números Signados en Exceso-3

### Estructura para Números Signados

```
Número signado: -5 en base 10

Usando complemento a 9:
Complemento a 9 de 5: 9 - 5 = 4

Representación de -5:
- Signo: negativo → usar complemento
- Dígitos: 5 → Exc3(5) = 1000
- Complemento: NOT(1000) = 0111 → Que es Exc3(4) ✅

Por lo tanto: -5 = 0111 (cuatro en Exc3)
```

### Ejemplo Completo: Número Negativo

```
Número: -37 (tres dígitos)

Paso 1: Complemento a 9
9 - 37 = 62 (aunque verbosamente: 9-3=6, 9-7=2)

Paso 2: Codificar 62 en Exceso-3
6: 6+3=9 → 1001
2: 2+3=5 → 0101

Representación de -37: 1001 0101

Verificación:
Si sumamos 37 + (-37) con complemento, debería dar 99 (o 0 con acarreo)
```

---

## 🎯 Comparativa: BCD Natural vs Exceso-3

| Característica | BCD Natural | Exceso-3 |
|---|---|---|
| **Codificación** | $d$ en BCD | $d+3$ en BCD |
| **Eficacia** | 62.5% | 62.5% |
| **Autocomplementario** | NO | **SÍ** |
| **Pesos** | SÍ (8,4,2,1) | NO |
| **Suma** | Corrección (+6 si >9) | Corrección (+3 o -3) |
| **Números signados** | Difícil (requiere bit sign) | Fácil (complemento a 9) |
| **Comparación** | Directa | NO |
| **Uso** | Entrada/salida | Aritmética signada |

---

## 💡 Ventajas y Desventajas

### ✅ Ventajas

1. **Autocomplementariedad:** Complemento a 9 es simplemente invertir bits
2. **Números signados:** Facilita representación sin bit de signo separado
3. **Resta como suma:** Mediante complemento, reduce lógica aritmética
4. **Simetría:** Los dígitos 0-4 y 5-9 son perfectamente complementarios
5. **Previene errores:** Estructura autocomplementaria detecta ciertos errores

### ❌ Desventajas

1. **Sin pesos:** Dificulta ciertas operaciones aritméticas rápidas
2. **Suma compleja:** Requiere corrección como BCD Natural
3. **Multiplicación muy compleja:** No trivial
4. **Sin comparación directa:** No puedes comparar números directamente
5. **Menos intuitivo:** Requiere entender complementación a 9

---

## 🔗 Relación con Complemento a 9

### ¿Cómo Usar Exceso-3 para Complementación?

Si tenemos un número $N$ de múltiples dígitos en Exceso-3, su complemento a 9 se obtiene:

$$\text{Complemento a 9 de } N_{\text{Exc3}} = \neg N_{\text{Exc3}} \text{ (invertir todos los bits)}$$

**Ejemplo:**

```
Número: 42

Exc3(4) = 0111
Exc3(2) = 0101
Exc3(42) = 0111 0101

Complemento a 9:
NOT(0111 0101) = 1000 1010
                = Exc3(5) Exc3(7) = Exc3(57)

Verificación: 9 - 42 = 57 ✓
Complemento a 9 de 42 es 57 ✓
```

---

## 📍 Casos Especiales

### 1. El cero en Exceso-3

```
0 en Exceso-3: 0 + 3 = 3 → 0011
(Un único cero, sin ambigüedad)
```

### 2. Números negativos (complemento a 9)

```
-5 en Exceso-3:
Complemento a 9 de 5 = 9 - 5 = 4
4 en Exc3 = 0111

Por lo tanto: -5 se representa como 0111 en Exc3
(que es el código de +4)
```

### 3. Acarreos en suma

En suma de números múltiples dígitos, el acarreo requiere procesamiento especial para mantener el código Exceso-3.

---

## 🎓 Historia y Contexto

### ¿Por Qué fue Importante Exceso-3?

En **calculadoras analógicas y máquinas de computo electromecánicas**, Exceso-3 fue crucial porque:

1. Permitía **representar números negativos sin bit de signo separado**
2. La operación de complemento era **trivial** (invertir conductores/switches)
3. Facilitaba construcción de circuitos para **suma y resta uniformes**

### Época de Uso

- **1940s-1960s:** Estándar en calculadoras electromecánicas
- **1960s-1970s:** Usado en algunas computadoras decimales
- **Hoy:** Principalmente histórico/educativo, pero conceptualmente valioso

---

## 🔄 Evolución de Códigos BCD

```
Números Naturales (Binarios 8-4-2-1)
        ↓ (Codificar por dígitos)
BCD Natural (8-4-2-1 para cada dígito)
        ↓ (Buscar autocomplementariedad)
Exceso-3 (8-4-2-1 + 3 para cada dígito)
        ↓ (Buscar pesos + autocomplementariedad)
BCD Aiken (2-4-2-1, autocomplementario con pesos)
```

---

## 📝 Resumen

| Característica | Exceso-3 |
|---|---|
| **Nombre** | BCD Exceso-3 (Excess-3) |
| **Codificación** | Dígito + 3, luego BCD Natural |
| **Bits por dígito** | 4 |
| **Rango** | 0-9 por dígito |
| **Eficacia** | 62.5% |
| **Pesos** | NO |
| **Autocomplementario** | **SÍ** ✅ |
| **Suma** | Requiere corrección |
| **Números signados** | Mediante complemento a 9 |
| **Época de uso** | 1940s-1970s (electromecánica) |
| **Uso actual** | Principalmente educativo |

---

## 🚀 Siguiente Paso

Una vez entendido Exceso-3, exploraremos **[BCD Aiken](SECCION_2_1_2_BCD_AIKEN.md)** que intenta combinar:

- Pesos (como BCD Natural)
- Autocomplementariedad (como Exceso-3)

---

**Comparación de los 3 Códigos BCD:**

- [BCD Natural (8421)](SECCION_2_1_2_BCD_NATURAL.md)
- [BCD Exceso-3 (este archivo)](SECCION_2_1_2_1_BCD_EXC3.md) ← Aquí estás
- [BCD Aiken (2-4-2-1)](SECCION_2_1_2_BCD_AIKEN.md)
