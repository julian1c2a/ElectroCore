# Sección 2.1.4 - Código Biquinario

**Código de Detección de Errores Basado en Dos Bits Encendidos**

---

## 📌 Concepto Fundamental

### Definición

**Biquinario** es un sistema de codificación de dígitos decimales (0-9) donde:

- **Cada palabra** tiene exactamente 7 bits
- **Exactamente 2 bits siempre están encendidos** (propiedad fundamental)
- **Excelente detección de errores:** si no hay exactamente 2 unos, hay error
- **Usado históricamente en computadoras antiguas** (IBM, máquinas contables)

### Estructura

El código está dividido en dos grupos:

- **5 bits de "quina":** representan grupo de 5 (0-4 o 5-9)
- **2 bits de "binario":** representan posición dentro del grupo

```
Estructura general:
┌─────────────────┬──────────┐
│ 5 bits (Quina)  │ 2 bits   │
│ Q₄ Q₃ Q₂ Q₁ Q₀ │ B₁ B₀    │
└─────────────────┴──────────┘

Propiedad: Q₄Q₃Q₂Q₁Q₀B₁B₀ siempre tiene exactamente 2 bits = 1
```

### Ejemplo: Codificación

```
Dígito 0: Grupo 0-4 + posición 0 → 0100001
Dígito 1: Grupo 0-4 + posición 1 → 0100010
Dígito 2: Grupo 0-4 + posición 2 → 0100100
Dígito 3: Grupo 0-4 + posición 3 → 0101000
Dígito 4: Grupo 0-4 + posición 4 → 0110000
Dígito 5: Grupo 5-9 + posición 0 → 1000001
Dígito 6: Grupo 5-9 + posición 1 → 1000010
Dígito 7: Grupo 5-9 + posición 2 → 1000100
Dígito 8: Grupo 5-9 + posición 3 → 1001000
Dígito 9: Grupo 5-9 + posición 4 → 1010000
```

---

## 🔢 Tabla Completa

| Decimal | Quina | Binario | Biquinario | Unos | Válido |
|---------|-------|---------|-----------|------|--------|
| 0 | 01000 | 01 | 0100001 | 2 | ✅ |
| 1 | 01000 | 10 | 0100010 | 2 | ✅ |
| 2 | 01000 | 01 | 0100100 | 2 | ✅ |
| 3 | 01000 | 01 | 0101000 | 2 | ✅ |
| 4 | 01000 | 01 | 0110000 | 2 | ✅ |
| 5 | 10000 | 01 | 1000001 | 2 | ✅ |
| 6 | 10000 | 10 | 1000010 | 2 | ✅ |
| 7 | 10000 | 01 | 1000100 | 2 | ✅ |
| 8 | 10000 | 01 | 1001000 | 2 | ✅ |
| 9 | 10000 | 01 | 1010000 | 2 | ✅ |

---

## ✅ Validación de Códigos Biquinario

### Regla Fundamental de Validación

Un código de 7 bits es válido en Biquinario si y solo si:

$$\text{VÁLIDO} = \begin{cases}
\text{SÍ} & \text{si } \sum_{i=0}^{6} b_i = 2 \text{ (exactamente 2 bits encendidos)} \\
\text{NO} & \text{en caso contrario}
\end{cases}$$

**En palabras:** El número de bits en 1 debe ser **exactamente 2**.

### Método Práctico

Para validar una palabra Biquinaria de 7 bits:

1. **Contar los bits en 1**
2. **¿Es exactamente 2?**
   - **SÍ** → ✅ Código válido
   - **NO** → ❌ Código inválido (error detectado)

### Ejemplos de Validación

#### Códigos Válidos (exactamente 2 unos)

```
0100001 → Conteo: 2 → ✅ VÁLIDO (representa 0)
0100010 → Conteo: 2 → ✅ VÁLIDO (representa 1)
0100100 → Conteo: 2 → ✅ VÁLIDO (representa 2)
0101000 → Conteo: 2 → ✅ VÁLIDO (representa 3)
0110000 → Conteo: 2 → ✅ VÁLIDO (representa 4)
1000001 → Conteo: 2 → ✅ VÁLIDO (representa 5)
1000010 → Conteo: 2 → ✅ VÁLIDO (representa 6)
1000100 → Conteo: 2 → ✅ VÁLIDO (representa 7)
1001000 → Conteo: 2 → ✅ VÁLIDO (representa 8)
1010000 → Conteo: 2 → ✅ VÁLIDO (representa 9)
```

#### Códigos Inválidos (número diferente de 2 unos)

```
0000000 → Conteo: 0 → ❌ INVÁLIDO (error: falta información)
0000001 → Conteo: 1 → ❌ INVÁLIDO (error de 1 bit)
0000011 → Conteo: 2 → ⚠️  Válido en forma (pero ¿representa qué?)
0100011 → Conteo: 3 → ❌ INVÁLIDO (error: 3 bits)
0101010 → Conteo: 3 → ❌ INVÁLIDO (error: 3 bits)
1111111 → Conteo: 7 → ❌ INVÁLIDO (error: todos bits)
1010101 → Conteo: 4 → ❌ INVÁLIDO (error: 4 bits)
0111111 → Conteo: 6 → ❌ INVÁLIDO (error: 6 bits)
```

---

## 🔍 Detección de Errores en Biquinario

### Capacidad de Detección

**Biquinario detecta:**

| Tipo de Error | Detectable | Ejemplo |
|---|---|---|
| **Error de 1 bit** | ✅ SÍ | 0100001 → 0100011 (3 unos) |
| **Error de 2 bits (inversión)** | ✅ SÍ (a veces) | 0100001 → 0100010 (aún 2, pero diferente) |
| **Error de 3+ bits** | ✅ SÍ | 0100001 → 0101001 (3 unos) |
| **Pérdida total (todos 0)** | ✅ SÍ | 0100001 → 0000000 (0 unos) |

### Ejemplo de Detección

```
Transmisión sin error:
Envío: 0100001 (representa 0)
Recibo: 0100001
Validación: 2 unos ✅ CORRECTO

Transmisión con error de 1 bit:
Envío: 0100001 (representa 0)
Recibo: 0100011 (bit 0 se voltea)
Validación: 3 unos ❌ ERROR DETECTADO

Transmisión con error de 2 bits simultáneos:
Envío: 0100001 (representa 0)
Recibo: 0101010 (bits 1 y 2 se voltean)
Validación: 3 unos ❌ ERROR DETECTADO
```

---

## 🔗 Propiedades Clave

| Propiedad | Valor | Descripción |
|-----------|-------|-------------|
| **Bits por dígito** | 7 | Requiere 7 bits para codificar 0-9 |
| **Número de palabras** | 10 | Exactamente 10 códigos válidos |
| **Códigos prohibidos** | 118 | Total 128 posibles - 10 válidos = 118 prohibidos |
| **Bits siempre encendidos** | Exactamente 2 | Propiedad fundamental |
| **Detección de errores** | ✅ SÍ | Detecta cambios en número de unos |
| **Eficiencia** | Baja (7 bits) | Mucho overhead para solo 10 códigos |
| **Redundancia** | 70% | 7 bits para información de 3.32 bits (log₂ 10) |
| **Adyacencia** | ❌ NO | No todas las palabras vecinas son adyacentes |
| **Autocomplementario** | ❌ NO | El complemento no tiene significado especial |

---

## 📊 Análisis de Errores Detectables

### Matriz de Detección

```
Palabra válida: 0100001 (2 unos)

Errores de 1 bit (7 posibilidades):
├─ Voltear bit 0: 0100000 → 1 uno ❌ DETECTADO
├─ Voltear bit 1: 0100011 → 3 unos ❌ DETECTADO
├─ Voltear bit 2: 0100101 → 3 unos ❌ DETECTADO
├─ Voltear bit 3: 0101001 → 3 unos ❌ DETECTADO
├─ Voltear bit 4: 0110001 → 3 unos ❌ DETECTADO
├─ Voltear bit 5: 0000001 → 1 uno ❌ DETECTADO
└─ Voltear bit 6: 1100001 → 3 unos ❌ DETECTADO

Resultado: 100% de errores simples detectados
```

---

## 💡 Comparación con Otros Códigos

| Aspecto | Biquinario | Hamming | BCD | Johnson |
|--------|-----------|---------|-----|---------|
| **Bits requeridos** | 7 | 7 (para detectar) | 4 | 5 |
| **Palabras válidas** | 10 | 16-128 | 10 | 10 |
| **Detección errores** | Sí (simple) | Sí (Hamming) | No | No |
| **Corrección errores** | No | Sí | No | No |
| **Uso actual** | Histórico | Moderno | Común | Especializado |
| **Complejidad circuito** | Baja | Alta | Baja | Media |

---

## 🎯 Aplicaciones Prácticas

### Donde se usa Biquinario

1. **Computadoras antiguas:** IBM System, máquinas contables (1950-1970)
2. **Telefonía analógica:** Marcado por impulsos
3. **Telecomunicaciones:** Detección de errores en transmisión
4. **Histórico/Educativo:** Enseñanza de detección de errores
5. **Sistemas legacy:** Mantenimiento de máquinas antiguas

### Ventajas y Desventajas

**✅ VENTAJAS:**

- Detección de errores muy simple (contar unos)
- Detecta cualquier cambio de 1 bit
- Histórico (bien documentado)
- Fácil de implementar en hardware antiguo

**❌ DESVENTAJAS:**

- Muy ineficiente (7 bits para 10 valores)
- No permite corregir errores
- Superado por códigos Hamming y otros modernos
- Complejo para aritmética
- No tiene pesos

---

## 📈 Matriz de Validación Exhaustiva

**Estructura simplificada:** Muestra algunos ejemplos

| Palabra | Unos | Válido | Interpretación |
|---------|------|--------|----------------|
| 0000000 | 0 | ❌ | Error: información perdida |
| 0000001 | 1 | ❌ | Error de transmisión |
| 0000011 | 2 | ⚠️ | 2 unos, pero patrón inválido |
| 0100001 | 2 | ✅ | Dígito 0 |
| 0100010 | 2 | ✅ | Dígito 1 |
| 0100100 | 2 | ✅ | Dígito 2 |
| 0101000 | 2 | ✅ | Dígito 3 |
| 0110000 | 2 | ✅ | Dígito 4 |
| 0111000 | 3 | ❌ | Error: 3 unos |
| 1000001 | 2 | ✅ | Dígito 5 |
| 1010000 | 2 | ✅ | Dígito 9 |
| 1111111 | 7 | ❌ | Error total |

---

## 🎯 Resumen

**Biquinario es útil cuando:**
- Necesitas detección simple de errores
- Trabajas con hardware legacy/antiguo
- Simplicidad > eficiencia de bits
- Educación sobre códigos detectores de errores

**Usa algo mejor (Hamming, CRC, etc.) cuando:**
- Necesitas sistemas modernos
- Requieres corrección de errores
- La eficiencia de bits es importante
- Trabajas con transmisión confiable

**Conclusión:** Biquinario es principalmente histórico, pero conceptualmente importante para entender la evolución de los códigos detectores de errores.
