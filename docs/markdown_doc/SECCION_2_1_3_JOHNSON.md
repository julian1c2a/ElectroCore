# Sección 2.1.3 - Código Johnson (Gray Modificado)

**Código Cíclico Adyacente para Aplicaciones Secuenciales**

---

## 📌 Concepto Fundamental

### Definición

**Johnson** (también conocido como **Código Reflejado de Johnson** o **Gray Modificado**) es un sistema de codificación de dígitos decimales (0-9) donde:

- **Cada palabra** tiene exactamente 5 bits
- **Todas las palabras sucesivas difieren en 1 bit** (adyacentes)
- **Es cíclico:** el último valor (9) es adyacente al primero (0)
- **Ideal para aplicaciones secuenciales** (contadores, máquinas de estado)

### Estructura

El código Johnson para valores 0-9 sigue un patrón de **unos progresivos**:

```
0 → 00000  (0 unos)
1 → 00001  (1 uno)
2 → 00011  (2 unos consecutivos desde la derecha)
3 → 00111  (3 unos consecutivos)
4 → 01111  (4 unos consecutivos)
5 → 11111  (5 unos, todos encendidos)
6 → 11110  (4 unos desde la izquierda)
7 → 11100  (3 unos desde la izquierda)
8 → 11000  (2 unos desde la izquierda)
9 → 10000  (1 uno)
```

---

## 🔢 Tabla Completa

| Decimal | Johnson | Descripción |
|---------|---------|-------------|
| 0 | 00000 | Todos ceros |
| 1 | 00001 | Un uno (derecha) |
| 2 | 00011 | Dos unos consecutivos |
| 3 | 00111 | Tres unos consecutivos |
| 4 | 01111 | Cuatro unos consecutivos |
| 5 | 11111 | Todos unos |
| 6 | 11110 | Cuatro unos (izquierda) |
| 7 | 11100 | Tres unos (izquierda) |
| 8 | 11000 | Dos unos (izquierda) |
| 9 | 10000 | Un uno (izquierda) |

**Códigos prohibidos (6 total):** 01000, 01001, 01010, 01011, 01100, 01101

---

## ✅ Validación de Códigos Johnson

### Regla de Validación

Un código de 5 bits es válido en Johnson si y solo si:

**"Es una secuencia de unos consecutivos (posiblemente vacía) o es el complemento de una secuencia de unos consecutivos"**

Matemáticamente: Una palabra es válida si, tras eliminar los bits iniciales en 0 y finales en 1 (o viceversa), obtenemos una secuencia válida.

**Más precisamente:**

$$\text{VÁLIDO} = \begin{cases}
\text{SÍ} & \text{si } b_4b_3b_2b_1b_0 \text{ es de la forma } 0^i 1^j 0^{5-i-j} \text{ ó } 1^i 0^j 1^{5-i-j} \\
\text{NO} & \text{en caso contrario}
\end{cases}$$

Es decir: **máximo una "transición" de 0→1 o de 1→0** (leyendo de izquierda a derecha o de derecha a izquierda).

### Método Práctico

Para validar una palabra Johnson de 5 bits:

1. **Contar transiciones:** ¿Cuántas veces cambia el valor del bit (0→1 o 1→0)?
2. **Resultado válido si:** Hay exactamente 2 transiciones (o 0 para 00000 o 11111)

### Ejemplos de Validación

#### Códigos Válidos

```
00000 → 0 transiciones → ✅ VÁLIDO (0)
00001 → 1 transición (0→1) → ✅ VÁLIDO (1)
00011 → 1 transición (0→1) → ✅ VÁLIDO (2)
00111 → 1 transición (0→1) → ✅ VÁLIDO (3)
01111 → 1 transición (0→1) → ✅ VÁLIDO (4)
11111 → 0 transiciones → ✅ VÁLIDO (5)
11110 → 1 transición (1→0) → ✅ VÁLIDO (6)
11100 → 1 transición (1→0) → ✅ VÁLIDO (7)
11000 → 1 transición (1→0) → ✅ VÁLIDO (8)
10000 → 1 transición (1→0) → ✅ VÁLIDO (9)
```

#### Códigos Inválidos

```
01000 → 2 transiciones (0→1→0) → ❌ INVÁLIDO
01001 → 3 transiciones (0→1→0→1) → ❌ INVÁLIDO
01010 → 4 transiciones (0→1→0→1→0) → ❌ INVÁLIDO
01011 → 3 transiciones (0→1→0→1→1) → ❌ INVÁLIDO
01100 → 2 transiciones (0→1→1→0) → ❌ INVÁLIDO
01101 → 3 transiciones (0→1→1→0→1) → ❌ INVÁLIDO
10101 → 4 transiciones (1→0→1→0→1) → ❌ INVÁLIDO
```

---

## 🔗 Propiedades Clave

| Propiedad | Valor | Descripción |
|-----------|-------|-------------|
| **Bits por dígito** | 5 | Necesita 5 bits para codificar 0-9 |
| **Número de palabras** | 10 | Exactamente 10 códigos válidos |
| **Códigos prohibidos** | 6 | Total 32 posibles - 10 válidos = 22 prohibidos |
| **Adyacencia** | ✅ SÍ | Valores sucesivos difieren en 1 bit |
| **Cíclico** | ✅ SÍ | 9→0 también difieren en 1 bit |
| **Autocomplementario** | ❌ NO | El complemento no es el siguiente valor |
| **Pesos** | ❌ NO | No tiene pesos fijos (similar a Gray) |
| **Detección de errores** | ✅ SÍ | Detecta múltiples errores en transiciones |

---

## 💡 Aplicaciones Prácticas

### Donde se usa Johnson

1. **Contadores secuenciales:** Hardware contador que avanza de 0-9
2. **Máquinas de estado:** Transiciones entre estados (cambio en 1 bit = cambio atómico)
3. **Codificadores rotativos:** Posiciones angulares (un bit de cambio por posición)
4. **Circuitos digitales síncronos:** Minimiza transiciones espurias (hazards)
5. **Detectores de velocidad:** Cambios de bit proporcionales a velocidad

### Ventajas y Desventajas

**✅ VENTAJAS:**

- Cambio de un bit entre valores sucesivos
- Cíclico (seguro para aplicaciones repetitivas)
- Fácil detectar errores (comprobar número de transiciones)
- Ideal para máquinas de estado

**❌ DESVENTAJAS:**

- Requiere 5 bits (menos eficiente que BCD de 4)
- No tiene pesos (no es aritmético)
- Menos conocido que BCD o Gray
- Conversión decimal ↔ Johnson no es directa

---

## 📊 Tabla de Validación Exhaustiva

| Palabra | Decimal | Transiciones | Válido | Razón |
|---------|---------|---|---|---|
| 00000 | 0 | 0 | ✅ | Especial: todos iguales |
| 00001 | 1 | 1 | ✅ | Unos progresivos |
| 00010 | - | 2 | ❌ | Transición duplicada |
| 00011 | 2 | 1 | ✅ | Unos progresivos |
| 00100 | - | 3 | ❌ | Patrón roto |
| 00101 | - | 3 | ❌ | Patrón roto |
| 00110 | - | 2 | ❌ | Transición duplicada |
| 00111 | 3 | 1 | ✅ | Unos progresivos |
| 01000 | - | 2 | ❌ | Transición en medio |
| 01111 | 4 | 1 | ✅ | Unos progresivos |
| 10000 | 9 | 1 | ✅ | Unos progresivos (inverso) |
| 11000 | 8 | 1 | ✅ | Unos progresivos (inverso) |
| 11100 | 7 | 1 | ✅ | Unos progresivos (inverso) |
| 11110 | 6 | 1 | ✅ | Unos progresivos (inverso) |
| 11111 | 5 | 0 | ✅ | Especial: todos iguales |

---

## 🎯 Resumen

**Johnson es ideal cuando:**
- Necesitas transiciones atómicas (1 bit)
- Cambios secuenciales y cíclicos
- Máquinas de estado simple
- Aplicaciones donde cambio = seguridad

**No usar Johnson cuando:**
- Necesitas aritmética (usa BCD)
- Necesitas eficiencia de bits (usa Gray)
- Necesitas autocomplementario (usa Exc3 o Aiken)
