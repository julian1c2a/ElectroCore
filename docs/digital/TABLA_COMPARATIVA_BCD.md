# Tabla de Comparación: BCD Natural, Exceso-3 y Aiken

**Referencia rápida de los 3 códigos BCD más importantes**

---

## 📋 Tabla Completa (16-valor binario: 0-15)

```
┌──────────┬──────────┬────────────┬───────────────┐
│ Binario  │ Natural  │ Exceso-3   │ Aiken (2-4-2-1│
│ (0-15)   │ (8421)   │            │ )             │
├──────────┼──────────┼────────────┼───────────────┤
│ 0000     │ 0        │ ----       │ 0             │
│ 0001     │ 1        │ ----       │ 1             │
│ 0010     │ 2        │ ----       │ 2             │
│ 0011     │ 3        │ 0          │ 3             │
│ 0100     │ 4        │ 1          │ 4             │
│ 0101     │ 5        │ 2          │ ----          │
│ 0110     │ 6        │ 3          │ ----          │
│ 0111     │ 7        │ 4          │ ----          │
│ 1000     │ 8        │ 5          │ ----          │
│ 1001     │ 9        │ 6          │ ----          │
│ 1010     │ ----     │ 7          │ ----          │
│ 1011     │ ----     │ 8          │ 5             │
│ 1100     │ ----     │ 9          │ 6             │
│ 1101     │ ----     │ ----       │ 7             │
│ 1110     │ ----     │ ----       │ 8             │
│ 1111     │ ----     │ ----       │ 9             │
└──────────┴──────────┴────────────┴───────────────┘

Nota: ---- indica códigos no válidos o no utilizados
```

---

## 🔢 Tabla de Codificación (Dígitos 0-9 Válidos)

| Dígito | BCD Natural (8421) | BCD Exceso-3 | BCD Aiken (2-4-2-1) |
|--------|---|---|---|
| **0** | 0000 | 0011 | 0000 |
| **1** | 0001 | 0100 | 0001 |
| **2** | 0010 | 0101 | 0010 |
| **3** | 0011 | 0110 | 0011 |
| **4** | 0100 | 0111 | 0100 |
| **5** | 0101 | 1000 | 1011 |
| **6** | 0110 | 1001 | 1100 |
| **7** | 0111 | 1010 | 1101 |
| **8** | 1000 | 1011 | 1110 |
| **9** | 1001 | 1100 | 1111 |

---

## 🎯 Propiedades Comparativas

| Propiedad | BCD Natural | Exceso-3 | Aiken |
|-----------|---|---|---|
| **Codificación** | d (directo) | d + 3 | Pesos 2-4-2-1 |
| **Bits por dígito** | 4 | 4 | 4 |
| **Rango** | 0-9 | 0-9 | 0-9 |
| **Códigos válidos** | 10 | 10 | 10 |
| **Códigos inválidos** | 6 | 6 | 6 |
| **Eficacia** | 62.5% | 62.5% | 62.5% |
| **Pesos** | 8-4-2-1 ✅ | NO ❌ | 2-4-2-1 ✅ |
| **Autocomplementario** | NO ❌ | SÍ ✅ | SÍ ✅ |
| **Comparación directa** | **SÍ ✅** (binaria) | **SÍ ✅** (binaria) | **SÍ ✅** (binaria) |
| **Suma simple** | NO ❌ | NO ❌ | NO ❌ |
| **Números signados** | Difícil | Fácil | Fácil |
| **Complemento a 9** | Complejo | Invertir bits ✅ | Invertir bits ✅ |

---

## ✨ Características Especiales

### BCD Natural (8-4-2-1)

**✅ Fortalezas:**

- Pesos estándar (8-4-2-1)
- Comparación directa (binaria)
- Intuitivo para conversión decimal
- Un único cero
- Estándar para entrada/salida

**❌ Debilidades:**

- Suma requiere corrección (+6 si > 9)
- Sin autocomplementariedad
- Números signados difíciles
- Multiplicación compleja

**🎯 Mejor para:**

- Entrada/salida decimal
- Displays numéricos
- Conversión decimal ↔ BCD
- Comparación de valores

---

### BCD Exceso-3

**✅ Fortalezas:**

- Autocomplementario (invertir bits = complemento a 9) 🔑
- Números signados naturales
- Resta por suma
- Comparación directa (como binario natural de 4 bits) ✅
- Un único cero

**❌ Debilidades:**

- Sin pesos (dificulta cálculos rápidos)
- Suma requiere corrección
- Menos intuitivo
- Menos estándar que BCD Natural

**🎯 Mejor para:**

- Aritmética decimal signada
- Máquinas electromecánicas antiguas
- Sistemas sin multiplicación
- Estudio histórico

**🔑 Característica Clave:**

```
Complemento a 9 de n = ~Exc3(n)
                      (invertir todos los bits)

Ejemplo: Complemento a 9 de 5
Exc3(5) = 1000
~1000 = 0111 = Exc3(4) = complemento a 9 de 5 ✓
```

---

### BCD Aiken (2-4-2-1)

**✅ Fortalezas:**

- Autocomplementario (invertir bits = complemento a 9) 🔑
- Tiene pesos (mejor que Exceso-3)
- Números signados naturales
- Detección de errores (6 códigos prohibidos)
- Solución "balanceada"

**❌ Debilidades:**

- Pesos irregulares (2-4-2-1)
- Suma aún requiere corrección
- Comparación no directa
- Menos estándar/conocido
- Menos intuitivo que BCD Natural

**🎯 Mejor para:**

- Balance entre eficiencia y funcionalidad
- Hardware con limitaciones
- Sistemas que detectan errores
- Estudio histórico (Mark I, 1944)

**🔑 Característica Clave:**

```
Pesos: 2-4-2-1 en lugar de 8-4-2-1
Valor = 2·b3 + 4·b2 + 2·b1 + b0

Ejemplo: Aiken(5) = 1011
Valor = 2(1) + 4(0) + 2(1) + 1(1) = 2 + 2 + 1 = 5 ✓

Complemento a 9:
~1011 = 0100 = Aiken(4) ✓
```

---

## 📊 Matriz de Decisión: ¿Cuál Usar?

### Pregunta 1: ¿Necesitas Autocomplementariedad?

```
    ├─→ SÍ: Uso 1: Exceso-3 o Aiken
    │       └─ Fácil complemento a 9
    │       └─ Números signados sin bit adicional
    │
    └─→ NO: Uso 2: BCD Natural
            └─ Pesos estándar
            └─ Comparación fácil
```

### Pregunta 2: Si Sí (autocomplementario), ¿Necesitas Pesos?

```
    ├─→ SÍ: Uso 1: BCD Aiken
    │       └─ Balance óptimo
    │       └─ Mejor que Exceso-3 para cálculos
    │
    └─→ NO: Uso 2: BCD Exceso-3
            └─ Más simple
            └─ Menos bits de overhead
```

### Pregunta 3: ¿Aplicación Histórica/Educativa?

```
    ├─→ Máquinas antiguas (1940-70s): BCD Exceso-3
    │   └─ Usado en calculadoras electromecánicas
    │
    ├─→ Harvard Mark I (1944): BCD Aiken
    │   └─ Diseñado específicamente por Aiken
    │
    └─→ Sistemas I/O modernos: BCD Natural
        └─ Estándar de facto
```

---

## 📈 Tabla Histórica

| Época | Sistema | Uso | Contexto |
|-------|---------|-----|---------|
| **1940s** | Excesoparticipa-3 | Calculadoras electromecánicas | Máquinas de relés |
| **1944** | BCD Aiken | Computadora Mark I (Harvard) | Búsqueda de balance |
| **1950s-60s** | BCD Natural | COBOL, Fortran | Entrada/salida |
| **1970s-80s** | Binarios puros | Computadoras modernas | Velocidad |
| **Hoy** | BCD (especializado) | Finanzas, IEEE 754 Decimal | Precisión decimal |

---

## 🔄 Autocomplementariedad: Detalles

### Concepto

Un código es **autocomplementario** si:

$$\text{Código}(\text{complemento a 9 de } d) = \neg \text{Código}(d)$$

Es decir: invirtiendo todos los bits obtienes el complemento a 9.

### En BCD Exceso-3

```
Dígito d = 5
Exc3(5) = 5 + 3 = 8 = 1000

Complemento a 9 de 5 = 4
Exc3(4) = 4 + 3 = 7 = 0111

¿Coinciden 0111 = ~1000?
~1000 = 0111 ✓ SÍ
```

**Matemática:**

```
Exc3(d) = d + 3 (en 4 bits)
Exc3(9-d) = (9-d) + 3 = 12 - d = 15 - (d+3) = ~(d+3) = ~Exc3(d)
            porque 15 es el complemento en 4 bits
```

### En BCD Aiken

```
Dígito d = 5
Aiken(5) = 1011 (valor = 2(1)+4(0)+2(1)+1(1) = 5)

Complemento a 9 de 5 = 4  
Aiken(4) = 0100 (valor = 2(0)+4(1)+2(0)+0 = 4)

¿Coinciden 0100 = ~1011?
~1011 = 0100 ✓ SÍ
```

**Matemática:**

```
Aiken(d) = 2b3 + 4b2 + 2b1 + b0 = d
Aiken(9-d) = 2(1-b3) + 4(1-b2) + 2(1-b1) + (1-b0)
           = 9 - (2b3 + 4b2 + 2b1 + b0)
           = 9 - d ✓
           = ~(2b3 + 4b2 + 2b1 + b0) en 4 bits
           = ~Aiken(d)
```

---

## 🚀 Ejemplos Prácticos

### Ejemplo 1: Representar 247

**BCD Natural:**

```
2 → 0010
4 → 0100
7 → 0111
Resultado: 0010 0100 0111
```

**BCD Exceso-3:**

```
2 → 0010 + 0011 = 0101
4 → 0100 + 0011 = 0111
7 → 0111 + 0011 = 1010
Resultado: 0101 0111 1010
```

**BCD Aiken:**

```
2 → 0010
4 → 0100
7 → 1101
Resultado: 0010 0100 1101
```

### Ejemplo 2: Complemento a 9 de 247

**BCD Exceso-3 (Invertir bits):**

```
Original: 0101 0111 1010
Invertir: 1010 1000 0101
Verificación: Debe ser complemento a 9 de 247 = 752
Exc3(7)=1010, Exc3(5)=1000, Exc3(2)=0101 ✓
```

**BCD Aiken (Invertir bits):**

```
Original: 0010 0100 1101
Invertir: 1101 1011 0010
Verificación: Debe ser Aiken de 752
Aiken(7)=1101, Aiken(5)=1011, Aiken(2)=0010 ✓
```

---

## 💡 Conclusión

**No hay un "mejor" código universal.** Cada uno es óptimo para diferentes escenarios:

- **BCD Natural:** Mejor para conversión y comparación
- **BCD Exceso-3:** Mejor para aritmética signada simple
- **BCD Aiken:** Mejor para balance entre características

La elección depende de:

1. ¿Qué operaciones son dominantes?
2. ¿Se necesita aritmética signada?
3. ¿Hay limitaciones de hardware?
4. ¿Cuál es el contexto histórico?

---

## 📚 Referencias

- [BCD Natural (8-4-2-1)](SECCION_2_1_2_BCD_NATURAL.md)
- [BCD Exceso-3](SECCION_2_1_2_1_BCD_EXC3.md)
- [BCD Aiken (2-4-2-1)](SECCION_2_1_2_2_BCD_AIKEN.md)
- [Resumen Comparativo BCD](SECCION_2_1_2_RESUMEN_BCD.md)
- [Transición: De Enteros a BCD](TRANSICION_ENTEROS_A_BCD.md)
- [Demo Comparativa](demo_bcd_comparativo.py)

---

*Tabla de referencia rápida para comparar los 3 códigos BCD principales*
