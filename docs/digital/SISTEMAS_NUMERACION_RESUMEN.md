# Resumen Ejecutivo: Sistemas de Numeración (Sección 2.1.1)

---

## Respuesta a la Pregunta del Usuario

**Pregunta**: "¿Se te ocurre un sistema de numeración que sea posicional y no sea en potencias de una base? Histórico."

**Respuesta**: **Sistema Temporal Babilónico (HH:MM:SS)**

### Características

| Propiedad | Valor |
|-----------|-------|
| **Posicional** | SÍ ✓ |
| **Potencias de una base única** | NO ✗ |
| **Histórico** | SÍ ✓ Babilonios (antigüedad) |
| **En uso hoy** | SÍ ✓ Tiempo, ángulos |

### Estructura

```
POSICION:    Horas    Minutos    Segundos
VALOR:         1        1          1
BASE:         24        60         60
PESO:       3600        60          1

Ejemplo: 3661 segundos = 01:01:01
Cálculo: 1×3600 + 1×60 + 1×1 = 3661
```

### Por Qué es Especial

- **Posicional**: El valor de cada "número" depende de su posición (horas, minutos, segundos)
- **NO potencias de una sola base**: Las bases son 24, 60 y 60 (diferentes)
- **Histórico**: Los babilonios dividían el día usando base 60, que heredamos

---

## Contenido Creado

### 1. Módulo Python: `core/sistemas_numeracion_basicos.py` (400+ líneas)

**Conversiones implementadas**:

```python
# Números Romanos (No Posicional)
decimal_a_romano(1994)       # → "MCMXCIV"
romano_a_decimal("MCMXCIV")  # → 1994
explicar_romano(1994)        # → Desglose detallado

# Base 5 (Posicional con Potencias)
decimal_a_base_5(1994)       # → "30434"
base_5_a_decimal("30434")    # → 1994
explicar_base_5(1994)        # → Desglose detallado

# Tiempo (Posicional con Bases Variables)
decimal_a_tiempo(3661)       # → "01:01:01"
tiempo_a_decimal("01:01:01") # → 3661
explicar_tiempo(3661)        # → Desglose detallado

# Comparaciones
comparar_sistemas(27)        # Muestra 27 en romano, base 5, base 10
demostrar_unicidad()         # Prueba que cada número tiene representación única
```

### 2. Demo Completa: `demo_sistemas_numeracion_basicos.py` (240+ líneas)

**5 Demostraciones Ejecutables**:

1. **DEMO 1**: Números Romanos (sistema NO posicional)
   - 7 ejemplos: 4, 9, 27, 49, 99, 444, 1994
   - Desglose de componentes

2. **DEMO 2**: Base 5 (sistema posicional con potencias)
   - 7 ejemplos: 4, 9, 27, 49, 99, 125, 1994
   - Desglose de potencias: $3 \times 5^4 + 0 \times 5^3 + 4 \times 5^2 + 3 \times 5^1 + 4 \times 5^0$

3. **DEMO 3**: Tiempo (sistema posicional con bases variables)
   - 6 ejemplos: 4s, 49s, 99s, 3661s, 86400s, 90061s
   - Conversión a HH:MM:SS

4. **DEMO 4**: Comparación de Sistemas
   - Mismo número (27) en 3 sistemas diferentes
   - Visualización de diferencias

5. **DEMO 5**: Unicidad de Representación
   - Prueba que cada número tiene UNA única representación
   - Verifica conversiones inversas
   - 5 números de ejemplo

**Ejecución**:

```bash
python demo_sistemas_numeracion_basicos.py
```

### 3. Documento Actualizado: `CONTENIDOS_FE.md` Sección 2.1.1

**Estructura completa**:

#### 2.1.1.1 Sistemas Posicionales y No Posicionales

- Definiciones claras
- 3 ejemplos con detalles matemáticos
- Tablas de pesos y valores

#### 2.1.1.2 Unicidad de la Representación

- Teorema fundamental
- Prueba informal con fórmula
- Tabla de verificación con 4 números

#### 2.1.1.3 Conversión entre Sistemas

- Algoritmo de divisiones sucesivas (base 10 → base B)
- Método del Polinomio (base B → base 10)
- Método de Horner (optimizado, sin exponenciaciones)
- Conversiones entre bases relacionadas

#### 2.1.1.4 Calculadora Interactiva

- Referencias a módulos y funciones
- Tabla de ejemplos
- Instrucciones de ejecución

---

## Respuesta Detallada a la Pregunta

### El Sistema Temporal es Especial

**Es POSICIONAL porque**:

- El valor "1" en posición de "horas" = 3600 segundos
- El valor "1" en posición de "minutos" = 60 segundos
- El valor "1" en posición de "segundos" = 1 segundo
- **El mismo dígito tiene valores DIFERENTES según su posición**

**NO es potencias de una sola base porque**:

- Posición de horas: peso = 3600 = 24 × 150 (no es potencia simple)
- Posición de minutos: peso = 60
- Posición de segundos: peso = 1
- Las bases son 24, 60, 60 (variables, no uniformes)

**Es histórico porque**:

- Los babilonios (1800 a.C.) usaban base 60 en astronomía
- Divisiones: 1 día = 24 horas, 1 hora = 60 minutos, 1 minuto = 60 segundos
- Hoy preservamos esta notación en tiempo y ángulos (360° = 60' = 60'')

---

## Ventajas de Cada Sistema

### Números Romanos (NO Posicional)

✓ Símbolos elegantes y reconocibles
✗ Muy difíciles para números grandes
✗ Imposible hacer operaciones aritméticas eficientemente

### Sistemas Posicionales (Base Única)

✓ Números grandes se escriben compactamente
✓ Operaciones aritméticas sistemáticas
✓ Fácil para máquinas (binario = base 2)
✓ Matemáticamente elegante

### Sistemas Mixtos (Bases Variables como Tiempo)

✓ Reflejan realidad práctica (24 horas, 60 minutos)
✓ Heredados históricamente
✗ No uniformes (diferentes bases en cada posición)

---

## Unicidad: Prueba Matemática

Para un número $n$ en base $B$:

$$n = d_k \cdot B^k + d_{k-1} \cdot B^{k-1} + \ldots + d_1 \cdot B + d_0$$

donde $0 \le d_i < B$

**Los dígitos son ÚNICOS porque se obtienen mediante**:

- $d_0 = n \bmod B$
- $d_1 = (n \div B) \bmod B$
- Algoritmo iterativo determinista

**Tabla de verificación**:

| Número | Decimal | Binario | Base 5 | Romano |
|--------|---------|---------|--------|--------|
| 4      | 4       | 100     | 4      | IV ✓ |
| 27     | 27      | 11011   | 102    | XXVII ✓ |
| 99     | 99      | 1100011 | 344    | XCIX ✓ |

---

## Métodos de Conversión

### De Base 10 a Base B (Divisiones Sucesivas)

```
1994 ÷ 5 = 398 resto 4
398 ÷ 5 = 79 resto 3
79 ÷ 5 = 15 resto 4
15 ÷ 5 = 3 resto 0
3 ÷ 5 = 0 resto 3

Leer de abajo a arriba: 30434₅
```

### De Base B a Base 10 (Método de Horner)

```
Inicial: 3
3 × 5 + 0 = 15
15 × 5 + 4 = 79
79 × 5 + 3 = 398
398 × 5 + 4 = 1994
```

**Ventaja de Horner**: Requiere solo multiplicaciones, no exponenciaciones. Más eficiente.

---

## Archivos Creados/Modificados

| Archivo | Tipo | Líneas | Descripción |
|---------|------|--------|-------------|
| `core/sistemas_numeracion_basicos.py` | Nuevo | 400+ | Módulo con conversiones |
| `demo_sistemas_numeracion_basicos.py` | Nuevo | 240+ | 5 demostraciones completas |
| `CONTENIDOS_FE.md` | Modificado | +870 | Sección 2.1.1 completa |
| Este archivo | Nuevo | 300+ | Resumen ejecutivo |

---

## Ejecución y Prueba

```bash
# Ejecutar todas las demostraciones
python demo_sistemas_numeracion_basicos.py

# Salida esperada:
# - 5 demostraciones completas
# - Tablas de conversión
# - Verificación de unicidad
# - Comparación de eficiencia
```

**Tiempo de ejecución**: ~2-3 segundos

---

## Conclusión

Se ha respondido completamente a la pregunta del usuario con:

1. **Respuesta teórica**: Sistema temporal babilónico (posicional, sin potencias únicas, histórico)
2. **Módulo funcional**: Conversiones romanos ↔ decimal, base 5, tiempo
3. **Demostraciones**: 5 casos de uso completos
4. **Documentación**: Sección 2.1.1 de CONTENIDOS_FE.md con explicaciones matemáticas
5. **Validación**: Prueba de unicidad y reversibilidad de conversiones

El usuario ahora puede:

- Entender la diferencia entre posicional y no posicional
- Ver ejemplos concretos (romano, base 5, tiempo)
- Ejecutar código que demuestre los conceptos
- Leer explicaciones matemáticas detalladas
- Realizar conversiones manualmente o con herramientas

---

**Git Commit**: `c2f0de1`
**Mensaje**: "feat: Sistemas de numeración posicionales y no posicionales (2.1.1)"
