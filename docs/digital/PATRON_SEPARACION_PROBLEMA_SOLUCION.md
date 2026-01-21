# Patrón Arquitectónico: Separación Problema ↔ Solución

## 🎯 Principio Fundamental

**Cada modelo de ejercicio debe separar explícitamente:**

1. **Parámetros del Problema** → Lo que el alumno ve (enunciado)
2. **Parámetros de la Solución** → Cálculos/respuestas (solo docente)

Esta separación debe estar **documentada en el código** y **respetada en los renderers**.

---

## 📊 Estructura General

```python
@dataclass
class EjercicioData(ExerciseData):
    # ══════════════════════════════════════════════════════════
    # PARÁMETROS DEL PROBLEMA (visible en enunciado)
    # ══════════════════════════════════════════════════════════
    
    # Contexto del problema
    title: str           # Título visible
    description: str     # Descripción del enunciado
    
    # Variables del problema
    problem_params: dict # Parámetros que definen el problema
    
    # ══════════════════════════════════════════════════════════
    # PARÁMETROS DE LA SOLUCIÓN (solo visible con is_solution=True)
    # ══════════════════════════════════════════════════════════
    
    # Respuestas calculadas
    solution_params: dict # Todo lo necesario para calcular respuestas
```

---

## 📝 Ejemplo 1: Numeración

### ❌ Problema Actual (Implícito)

```python
@dataclass
class ConversionRow:
    # Del problema
    label: str
    val_decimal: int
    target_col_idx: int  # ← Cuál es la columna que el alumno debe resolver
    target_val_str: str  # ← Indicador de si es representable
    
    # De la solución
    sol_bin: str   # Todas las soluciones
    sol_c2: str
    sol_sm: str
    sol_bcd: str
```

### ✅ Patrón Mejorado (Explícito)

```python
@dataclass
class ConversionRow:
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define el enunciado
    ════════════════════════════════════════════════════════════
    """
    label: str              # a), b), c)
    val_decimal: int        # Número a convertir
    target_col_idx: int     # Cuál sistema: 0=Bin, 1=C2, 2=SM, 3=BCD
    representable: bool     # ¿Se puede representar? (sí/no)
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    sol_bin: str   # Solución en Binario Natural
    sol_c2: str    # Solución en Complemento a 2
    sol_sm: str    # Solución en Signo-Magnitud
    sol_bcd: str   # Solución en BCD
```

**Renderer behavior:**

- `is_solution=False`: Solo muestra `target_col_idx` ← Alumno escribe aquí
- `is_solution=True`: Muestra todas las `sol_*` en rojo

---

## 📝 Ejemplo 2: Combinacional (Karnaugh)

### ❌ Problema Actual (Implícito)

```python
@dataclass
class KarnaughExerciseData(ExerciseData):
    truth_table_outputs: List[int]  # 16 valores (0 o 1)
    canon_type: str                  # "Minitérminos" o "Maxitérminos"
    gate_type: str                   # "NAND" o "NOR"
    vars_name: List[str]             # ["A", "B", "C", "D"]
    out_name: str                    # "F"
```

### ✅ Patrón Mejorado (Explícito)

```python
@dataclass
class KarnaughExerciseData(ExerciseData):
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define el enunciado
    ════════════════════════════════════════════════════════════
    """
    # Contexto
    title: str                  # "Mapa de Karnaugh (4 variables)"
    description: str            # "Simplifica la siguiente función"
    
    # Tabla de verdad (lo que el alumno ve)
    truth_table_outputs: List[int]  # [0, 1, 0, 1, 1, 0, ...] - 16 valores
    
    # Variables nombradas
    vars_name: List[str]        # ["A", "B", "C", "D"]
    out_name: str               # "F"
    
    # Especificación del problema
    canon_type: str             # "Minitérminos" (qué debe encontrar)
    gate_type: str              # "NAND" (restricción del problema)
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    # Mapa de Karnaugh (agrupamiento correcto)
    minterms: List[int]         # [1, 3, 4, 6, 8, 10, 12, 14]
    maxterms: List[int]         # [0, 2, 5, 7, 9, 11, 13, 15]
    
    # Soluciones simplificadas
    simplified_sop: str         # "F = A'BD + AC'D + ..." (SOP)
    simplified_pos: str         # "F = (A+B'+C)(A'+B+C) ..." (POS)
    simplified_nand: str        # "F = ((A'BD)' * (AC'D)'...)" (NAND)
    simplified_nor: str         # "F = ((A+B'C)' + ...)" (NOR)
    
    # Implementación
    gate_count_sop: int         # 5 puertas (para comparar soluciones)
    gate_count_nand: int        # 7 puertas
```

**Renderer behavior:**

- `is_solution=False`: Muestra tabla de verdad + vacío para respuesta
- `is_solution=True`: Muestra tabla + `simplified_sop` + `simplified_nand` (en rojo)

---

## 📝 Ejemplo 3: Secuencial (Flip-Flop)

### ❌ Problema Actual (Implícito)

```python
@dataclass
class SequentialExerciseData(ExerciseData):
    ff_type: str           # "JK", "D", "T"
    edge_type: str         # "Subida" o "Bajada"
    logic_type: str        # "SHIFT" o "COUNTER"
    has_async: bool
    async_type: str        # "Preset", "Clear"
    async_level: str       # "0" o "1"
    
    total_cycles: int
    clk_sequence: str
    async_sequence: str
    input_sequence: str
    output_placeholder: str
```

### ✅ Patrón Mejorado (Explícito)

```python
@dataclass
class SequentialExerciseData(ExerciseData):
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define el enunciado
    ════════════════════════════════════════════════════════════
    """
    # Contexto
    title: str                  # "Flip-Flop JK (contador asincrónico)"
    description: str            # "Simula el siguiente circuito"
    
    # Componentes del circuito
    ff_type: str               # "JK", "D", "T"
    edge_type: str             # "Subida" (qué edge dispara)
    
    # Lógica del circuito
    logic_type: str            # "SHIFT" o "COUNTER"
    has_async: bool            # ¿Tiene entrada asincrónica?
    async_type: str            # "Preset" o "Clear"
    async_level: str           # "0" o "1" (nivel activo)
    
    # Secuencias de entrada (lo que el alumno ve)
    total_cycles: int          # Número de ciclos a simular
    clk_sequence: str          # "0101010101..." (reloj)
    async_sequence: str        # "0000011000..." (entrada async)
    input_sequence: str        # "1010101010..." (J o D o T)
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    # Salidas calculadas por simulación
    output_sequence: str       # "1010101010..." (Q en cada ciclo)
    output_bar_sequence: str   # "0101010101..." (Q' en cada ciclo)
    
    # Tabla de transiciones
    state_transitions: List[dict]  # [
                                   #   {"t": 0, "J": 1, "K": 0, "CLK": 0, "Q": 0},
                                   #   {"t": 1, "J": 1, "K": 0, "CLK": 1, "Q": 1},
                                   #   ...
                                   # ]
    
    # Información de timing
    setup_time_met: bool       # ¿Se respetan los tiempos?
    hold_time_met: bool
    timing_violations: List[str]  # [] o ["Setup violation at t=5", ...]
```

**Renderer behavior:**

- `is_solution=False`: Muestra `clk_sequence`, `input_sequence`, tabla vacía para `output_sequence`
- `is_solution=True`: Muestra todo incluyendo `output_sequence` y transiciones

---

## 🔍 Patrón General

### Estructura de Comentarios en Código

```python
@dataclass
class TuExerciseData(ExerciseData):
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA
    ════════════════════════════════════════════════════════════
    Estos campos definen QUÉ PROBLEMA se le presenta al alumno.
    Deben ser visibles en is_solution=False.
    """
    param1: type  # Descripción del parámetro
    param2: type
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN
    ════════════════════════════════════════════════════════════
    Estos campos contienen LAS RESPUESTAS CORRECTAS.
    Solo visibles en is_solution=True (en rojo o resaltado).
    """
    solution1: type  # Descripción de la solución
    solution2: type
```

---

## 🎨 Impacto en Renderers

### Antes (Confuso)

```python
# ¿Cuál es el enunciado? ¿Cuál es la solución?
renderer.render(exercise_data, is_solution=False)
```

### Después (Claro)

```python
# Es obvio qué mostrar
if is_solution:
    # Mostrar todo, soluciones en rojo
    for field in exercise_data.SOLUTION_PARAMS:
        show_in_red(field)
else:
    # Mostrar solo el problema
    for field in exercise_data.PROBLEM_PARAMS:
        show_in_black(field)
```

---

## 📋 Checklist de Implementación

Para cada modelo `XyzExerciseData`:

- [ ] Documentación clara de parámetros del problema
- [ ] Documentación clara de parámetros de la solución
- [ ] Separación visual con comentarios `════════`
- [ ] Validación: problema debe ser completo sin soluciones
- [ ] Validación: soluciones deben ser calculables del problema
- [ ] Renderer: `is_solution=False` solo muestra problema
- [ ] Renderer: `is_solution=True` muestra problema + soluciones en rojo
- [ ] Tests: verificar que problema es siempre igual, soluciones varían

---

## 🔧 Cambios Necesarios por Módulo

| Módulo | Clase | Cambios Necesarios |
|--------|-------|-------------------|
| **numeracion** | `ConversionRow` | ✅ Ya hecho (añadir `representable`) |
| **numeracion** | `ArithmeticOp` | Separar params: problema vs solución |
| **combinacional** | `KarnaughExerciseData` | Añadir `simplified_sop`, `simplified_pos`, etc. |
| **combinacional** | `LogicProblemExerciseData` | Añadir soluciones de circuito |
| **combinacional** | `MSIExerciseData` | Separar especificación vs evaluación |
| **secuencial** | `SequentialExerciseData` | Añadir `output_sequence`, `state_transitions` |

---

## 💡 Beneficios

1. **Claridad** → Evidente qué muestra cada renderer
2. **Robustez** → Impossible mostrar soluciones en enunciado por error
3. **Extensibilidad** → Fácil agregar nuevas soluciones (NOR, NAND, etc.)
4. **Testing** → Fácil verificar que problema es invariante
5. **Documentación** → El código es autodocumentado

---

## 📚 Referencias en Código

Usar esta sintaxis en todos los modelos:

```python
"""
════════════════════════════════════════════════════════════
PARÁMETROS DEL PROBLEMA
════════════════════════════════════════════════════════════
"""

"""
════════════════════════════════════════════════════════════
PARÁMETROS DE LA SOLUCIÓN
════════════════════════════════════════════════════════════
"""
```

Esto permite búsqueda rápida: `grep "PARÁMETROS DEL PROBLEMA"`
