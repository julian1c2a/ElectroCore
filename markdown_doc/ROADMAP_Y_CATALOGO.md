# ROADMAP Y ESTADO DEL CATÁLOGO - Sistemas de Numeración y Códigos

---

## 📊 RESUMEN EJECUTIVO

**Progreso Total**: 50% (4 de 8 fases completadas)

- ✅ FASES 1-4: 88 tests pasando (100%), ~2500 líneas de código
- ⏳ FASES 5-8: Detalladas en secciones siguientes
- 📈 Próximo: FASE 5 (Códigos Correctores - Hamming 7,4)

| Métrica | Valor |
|---------|-------|
| Tests Totales | 88 ✅ |
| Tests Pasando | 88 (100%) |
| Funciones Implementadas | 18 |
| Clases | 2 (Lenguaje, Códigos) |
| Líneas de Código | ~2500 |
| Documentación | ~2000 líneas |
| Archivos en CONTENIDOS_FE.md | 4 secciones (2.1.1.6.1.5-8) |

---

## Estado Actual (Completado)

### FASE 1: Eficacia de Empaquetado ✅

- Sección: **2.1.1.6.1.3-5** (CONTENIDOS_FE.md)
- Implementación: 5 funciones
- Tests: 45 (todas pasando)
- **Tópicos cubiertos:**
  - Eficacia de empaquetado simple
  - BCD vs DPD
  - IEEE 754 (punto flotante)
  - Teorema de empaquetado múltiple

### FASE 2: Códigos Especializados ✅

- Sección: **2.1.1.6.1.6-7** (CONTENIDOS_FE.md)
- Implementación: 6 funciones + 3 tablas de datos
- Tests: 47 (todas pasando)
- **Tópicos cubiertos:**
  - Código Biquinario (2 entre 5)
  - Código Johnson (cíclico adyacente)
  - Código Gray (reflejado)
  - Conversiones y análisis

### FASE 3: Teoría de Códigos ✅

- Sección: **2.1.1.6.1.5** (CONTENIDOS_FE.md)
- Implementación: Conceptual (sin código Python específico)
- **Tópicos cubiertos:**
  - Alfabeto, Lenguaje y Semántica
  - Definiciones formales
  - Comparativa de 5 códigos
  - Saturación, Adyacencia, Ciclicidad

### FASE 4: Distancia Hamming y Lenguajes ✅

- Sección: **2.1.1.6.1.8** (CONTENIDOS_FE.md)
- Implementación: 1 función + 1 clase + 4 constructores
- Tests: 41 (todas pasando)
- Demos: 6 (ejecutables)
- **Tópicos cubiertos:**
  - Distancia Hamming (fundamentación matemática)
  - Clase Lenguaje genérica
  - Análisis de adyacencia y ciclicidad
  - Propiedades métricas

---

## ¿Por Qué "Distancia" Hamming?

La función $d_H(a, b)$ cumple con **todas las propiedades de una métrica** en el sentido matemático:

### Axiomas de Métrica

Una función $d: X \times X \to \mathbb{R}$ es una **métrica** si cumple:

1. **No negatividad y separabilidad**:
   $$d_H(a, b) \geq 0, \quad d_H(a, b) = 0 \iff a = b$$
   ✓ Cumple: El número de diferencias es ≥ 0, e igual a 0 sólo si palabras son idénticas

2. **Simetría**:
   $$d_H(a, b) = d_H(b, a)$$
   ✓ Cumple: Las diferencias en las posiciones son las mismas en ambos sentidos

3. **Desigualdad triangular**:
   $$d_H(a, c) \leq d_H(a, b) + d_H(b, c)$$
   ✓ Cumple: Las diferencias entre a y c nunca pueden exceder la suma de caminos intermedios

### Consecuencias Teóricas

Por cumplir con axiomas de métrica:

- Define un **espacio métrico** sobre el conjunto de palabras-código
- Permite usar herramientas de análisis matemático: topología, geometría discreta
- Justifica términos como "distancia mínima", "bola de radio r", "código óptimo"
- Fundamenta teoría de códigos correctores de errores

### Ejemplo Práctico

```
a = 1011
b = 1010  
c = 1100

d_H(a,b) = 1  (difieren en posición 3)
d_H(b,c) = 2  (difieren en posiciones 2,3)
d_H(a,c) = 2  (difieren en posiciones 2,3)

Verificar desigualdad: d_H(a,c) = 2 ≤ 1 + 2 = d_H(a,b) + d_H(b,c) ✓
```

---

## Próximas Fases (Planned)

### FASE 5: Códigos Correctores de Errores (Hamming y Reed-Solomon)

**Estimada:** Semana 2 de desarrollo
**Sección esperada:** 2.1.1.6.1.9

#### Hamming (7,4) - Código Clásico

- **Concepto:** Usa distancia mínima para corrección
- **Estructura:**
  - 4 bits de información
  - 3 bits de paridad
  - Capacidad: Corregir 1 error (t = 1)
  - Capacidad: Detectar 2 errores simultáneamente

- **Matriz generadora G** y **Matriz de paridad H**
  - Cálculo de síndrome para detección
  - Algoritmo de decodificación

- **Implementación Python:**

  ```python
  codificar_hamming_7_4(bits_info: str) -> str
  decodificar_hamming_7_4(codigo: str) -> Tuple[str, int, List[int]]
  # Retorna: (bits corregidos, error detectado?, posiciones de error)
  ```

#### Distancia Mínima y Capacidad Correctora

- **Definición:** $d_{min} = \min_{c_i \neq c_j} d_H(c_i, c_j)$
- **Capacidad correctora:** $t = \lfloor (d_{min} - 1) / 2 \rfloor$
- **Capacidad detectora:** $e = d_{min} - 1$
- Relación con Hamming: $d_{min}(7,4) = 3$, luego $t = 1$ error corregible

#### Reed-Solomon (Avanzado)

- Códigos sobre cuerpos finitos GF(2^m)
- Aplicaciones: QR codes, DVDs, comunicaciones satelitales
- Capacidad: Corregir múltiples errores

### FASE 6: Código Gray Generalizado para n bits

**Estimada:** Semana 2 de desarrollo
**Sección esperada:** 2.1.1.6.1.10

#### Propiedades del Gray

- Construcción recursiva: Gray(n) = 0·Gray(n-1) + 1·Gray_invertido(n-1)
- Reflexión/Especularidad: Primera mitad es negación de segunda mitad
- Adyacencia garantizada: Cambio de exactamente 1 bit

#### Implementación Python

```python
generar_gray_n_bits(n: int) -> List[str]
entero_a_gray_n_bits(valor: int, longitud: int) -> str
gray_n_bits_a_entero(codigo: str) -> int

# Ejemplos:
generar_gray_n_bits(3)  # ['000','001','011','010','110','111','101','100']
```

#### Verificación de Propiedades

- Comprobar adyacencia para cualquier n
- Verificar reflexión/especularidad
- Comparar con Binario Natural
- Casos de uso: Encoders multi-eje, control industrial

### FASE 7: Análisis de Distancia Mínima

**Estimada:** Semana 3 de desarrollo
**Sección esperada:** 2.1.1.6.1.11

#### Matriz de Distancias (All-Pairs)

```python
calcular_matriz_distancias(lenguaje: Lenguaje) -> np.ndarray
# Retorna matriz de tamaño NxN con todas las distancias Hamming

# Propiedades extraídas:
- d_min: Distancia mínima (crucial para corrección)
- d_max: Distancia máxima
- d_avg: Distancia promedio
- Distribución de distancias
```

#### Análisis Estadístico

- Histograma de distancias
- Distancia promedio vs. capacidad correctora
- Identificación de códigos óptimos

#### Benchmark de Códigos

```
Comparación: ¿Cuál es mejor para cada aplicación?
- Distancia mínima
- Eficacia (palabras válidas / posibles)
- Capacidad correctora
- Complejidad de implementación
```

### FASE 8: Visualización de Grafos de Transición

**Estimada:** Semana 3-4 de desarrollo
**Sección esperada:** 2.1.1.6.1.12

#### Grafo de Transición

- **Vértices:** Palabras del código
- **Aristas:** Conexiones cuando distancia = 1
- **Propiedades:**
  - Grado de cada vértice (¿cuántos vecinos adyacentes?)
  - Conexidad (¿es un grafo conexo?)
  - Ciclos (¿tiene la estructura deseada?)

#### Visualización

```python
visualizar_grafo_transicion(lenguaje: Lenguaje) -> None
# Usa networkx + matplotlib
# Colorea nodos por propiedades
# Muestra aristas de adyacencia
```

#### Ejemplos Visualizables

- **Binario 4-bit:** 16 vértices, conectado pero no regular
- **Gray 4-bit:** 16 vértices, cíclico Hamiltoniano
- **Johnson 5-bit:** 10 vértices, ciclo perfecto
- **Biquinario 5-bit:** 10 vértices, varios componentes

---

## Secciones en CONTENIDOS_FE.md (Estado Actual)

```
2.1.1.6 Códigos Especializados
  ├── 2.1.1.6.1 Códigos Binarios
  │   ├── 2.1.1.6.1.3 Eficacia de Empaquetado ✅
  │   ├── 2.1.1.6.1.4 BCD vs DPD ✅
  │   ├── 2.1.1.6.1.5 Teoría de Códigos ✅
  │   ├── 2.1.1.6.1.6 Códigos Especializados de 5 Bits ✅
  │   ├── 2.1.1.6.1.7 Gray Reflejado ✅
  │   ├── 2.1.1.6.1.8 Distancia Hamming y Lenguajes ✅
  │   ├── 2.1.1.6.1.9 Códigos Correctores (Hamming, Reed-Solomon) ⏳ FASE 5
  │   ├── 2.1.1.6.1.10 Gray Generalizado para n bits ⏳ FASE 6
  │   ├── 2.1.1.6.1.11 Análisis de Distancia Mínima ⏳ FASE 7
  │   └── 2.1.1.6.1.12 Grafos de Transición ⏳ FASE 8
```

---

## Continuidad y Mañana

### Para Mañana (FASE 5)

1. **Implementar Hamming (7,4)**
   - Matriz generadora G (codificación)
   - Matriz de paridad H (detección)
   - Síndrome y corrección de errores
   - Tests exhaustivos

2. **Documentación:**
   - Teoría de distancia mínima
   - Deducción de capacidad correctora
   - Ejemplos paso a paso
   - Tabla comparativa: Hamming vs Gray vs Johnson

3. **Demos:**
   - Codificación de mensaje con paridad
   - Inyección de errores (simular)
   - Detección y corrección automática
   - Visualización de síndrome

---

## Archivos de Referencia

### Núcleo (Ya Completado)

- **core/sistemas_numeracion_basicos.py** - Distancia Hamming + Clase Lenguaje
- **tests/test_hamming_lenguaje.py** - 41 tests
- **demo_hamming_lenguaje.py** - 6 demostraciones

### Documentación

- **CONTENIDOS_FE.md** - Teoría y ejemplos completos
- **FASE_1_RESUMEN.md** - Eficacia de empaquetado
- **FASE_2_RESUMEN.md** - Códigos especializados
- **FASE_4_RESUMEN.md** - Hamming y lenguajes
- **Este archivo** - Roadmap y estado

---

## Métricas Globales (Hasta ahora)

| Métrica | Valor |
|---------|-------|
| **Fases Completadas** | 4 de 8 |
| **Secciones CONTENIDOS** | 6 de 12 |
| **Funciones Implementadas** | 18 |
| **Tests Totales** | 88 (100% pasando) |
| **Demostraciones** | 10+ |
| **Líneas de Código** | ~2500 |
| **Líneas de Documentación** | ~1500 |

---

## Próximo Paso (Acción Inmediata)

Cuando continúes mañana:

1. Leer esta sección de roadmap (para contexto)
2. Implementar **Hamming (7,4)** con matriz generadora
3. Agregar tests de corrección de errores
4. Documentar en CONTENIDOS_FE.md sección 2.1.1.6.1.9
5. Crear demo_hamming_correction.py

¡Excelente progreso! 🎯
