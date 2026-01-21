# Interfaz Formal: ProblemSolutionExerciseData

## 🎯 Concepto (C++ → Python)

En C++, usarías una clase virtual pura (abstract class):

```cpp
// C++ (hypothetical)
class ProblemSolutionExerciseData {
  virtual Set<string> problem_field_names() = 0;  // Puro
  virtual Set<string> solution_field_names() = 0; // Puro
};

class ConversionRow : public ProblemSolutionExerciseData {
  Set<string> problem_field_names() override {
    return {"label", "val_decimal", "target_col_idx", "representable"};
  }
  Set<string> solution_field_names() override {
    return {"target_val_str", "sol_bin", "sol_c2", "sol_sm", "sol_bcd"};
  }
};
```

En Python, hacemos equivalente con **ABC (Abstract Base Classes)**:

```python
from abc import ABC, abstractmethod

class ProblemSolutionExerciseData(ExerciseData, ABC):
    @classmethod
    @abstractmethod
    def problem_field_names(cls) -> Set[str]:
        """Implementar en subclases."""
        pass
    
    @classmethod
    @abstractmethod
    def solution_field_names(cls) -> Set[str]:
        """Implementar en subclases."""
        pass
```

---

## 📋 Interfaz Formal

### Métodos Abstractos (DEBEN Implementar)

```python
@classmethod
@abstractmethod
def problem_field_names(cls) -> Set[str]:
    """
    Devuelve los nombres de campos que definen el PROBLEMA.
    
    Estos campos:
    - Aparecen en enunciados (is_solution=False)
    - NO contienen respuestas
    - Son invariantes (no cambian con la solución)
    
    Example:
        class MyExercise(ProblemSolutionExerciseData):
            input_value: int
            expected_output: str
            
            @classmethod
            def problem_field_names(cls) -> Set[str]:
                return {"input_value"}
    """
```

```python
@classmethod
@abstractmethod
def solution_field_names(cls) -> Set[str]:
    """
    Devuelve los nombres de campos que contienen SOLUCIONES.
    
    Estos campos:
    - Aparecen SOLO en soluciones (is_solution=True), en rojo
    - Contienen respuestas correctas
    - Son calculables a partir del problema
    
    Example:
        @classmethod
        def solution_field_names(cls) -> Set[str]:
            return {"expected_output"}
    """
```

### Métodos Proporcionados (GRATIS)

```python
def to_problem_dict(self) -> Dict[str, Any]:
    """Extrae SOLO los parámetros del problema."""
    
def to_solution_dict(self) -> Dict[str, Any]:
    """Extrae SOLO los parámetros de la solución."""
    
def to_full_dict(self) -> Dict[str, Any]:
    """Extrae problema + solución (para depuración)."""
```

### Validaciones Automáticas (en `__post_init__`)

1. **Disjunción**: Problema ∩ Solución = ∅
   - Ningun campo puede estar en ambas categorías

2. **Exhaustividad**: (Problema ∪ Solución) = Campos reales
   - Todo campo debe estar categorizado

3. **Consistencia**: Los nombres mencionados existen
   - Sin typos en los nombres de campos

---

## 🔧 Cómo Implementar

### Paso 1: Heredar de ProblemSolutionExerciseData

```python
from core.generator_base import ProblemSolutionExerciseData

@dataclass
class MyExerciseData(ProblemSolutionExerciseData):
    # Tu código aquí
```

### Paso 2: Definir campos

```python
@dataclass
class MyExerciseData(ProblemSolutionExerciseData):
    # PROBLEMA
    input_value: int
    num_operations: int
    
    # SOLUCIÓN
    expected_result: str
    detailed_steps: List[str]
```

### Paso 3: Implementar métodos abstractos

```python
@classmethod
def problem_field_names(cls) -> Set[str]:
    return {"input_value", "num_operations"}

@classmethod
def solution_field_names(cls) -> Set[str]:
    return {"expected_result", "detailed_steps"}
```

### Paso 4: Listo

La clase automáticamente:

- ✅ Valida en `__post_init__` que no hay overlaps
- ✅ Valida que todo campo está categorizado
- ✅ Proporciona `to_problem_dict()` y `to_solution_dict()`

---

## 📊 Ejemplo Real: ConversionRow

```python
@dataclass
class ConversionRow(ProblemSolutionExerciseData):
    # PROBLEMA (5 campos)
    label: str
    val_decimal: int
    target_col_idx: int
    representable: bool
    
    # SOLUCIÓN (5 campos)
    target_val_str: str
    sol_bin: str
    sol_c2: str
    sol_sm: str
    sol_bcd: str
    
    @classmethod
    def problem_field_names(cls) -> Set[str]:
        return {
            "label",
            "val_decimal",
            "target_col_idx",
            "representable"
        }
    
    @classmethod
    def solution_field_names(cls) -> Set[str]:
        return {
            "target_val_str",
            "sol_bin",
            "sol_c2",
            "sol_sm",
            "sol_bcd"
        }
```

### Uso

```python
row = ConversionRow(
    label="a)",
    val_decimal=154,
    target_col_idx=0,
    representable=True,
    target_val_str="10011010",
    sol_bin="10011010",
    sol_c2="01100110",
    sol_sm="10011010",
    sol_bcd="0001 0101 0100",
    title="Numeración",
    description="Convierte..."
)

# Extrae solo el problema
problem = row.to_problem_dict()
# → {"label": "a)", "val_decimal": 154, "target_col_idx": 0, "representable": True}

# Extrae solo la solución
solution = row.to_solution_dict()
# → {"target_val_str": "10011010", "sol_bin": "10011010", ...}
```

---

## ✅ Validaciones Automáticas

### Validación 1: Sin Overlaps

```python
# ❌ ERROR: "label" está en ambos
@dataclass
class BadExample(ProblemSolutionExerciseData):
    label: str
    
    @classmethod
    def problem_field_names(cls):
        return {"label"}  # ← aquí
    
    @classmethod
    def solution_field_names(cls):
        return {"label"}  # ← y aquí → ERROR!
```

```
ValueError: Campos en AMBAS categorías (problema y solución): {'label'}
Un campo no puede estar en ambas categorías simultáneamente.
```

### Validación 2: Exhaustividad

```python
# ❌ ERROR: "description" no está categorizado
@dataclass
class BadExample(ProblemSolutionExerciseData):
    label: str
    description: str  # ← No mencionado en los métodos
    
    @classmethod
    def problem_field_names(cls):
        return {"label"}
    
    @classmethod
    def solution_field_names(cls):
        return set()  # Sin mencionar "description"
```

```
ValueError: Campos no categorizados (no están en problema ni solución): {'description'}
Todo campo debe estar explícitamente en problem_field_names() o solution_field_names().
```

### Validación 3: Sin Typos

```python
# ❌ ERROR: Typo en el nombre
@classmethod
def problem_field_names(cls):
    return {"labeel"}  # ← Typo: "labeel" vs "label"
```

```
ValueError: problem_field_names() menciona campos inexistentes: {'labeel'}
```

---

## 🎨 Integración con Renderers

```python
# renderer.py
def render(self, data: ProblemSolutionExerciseData, is_solution: bool) -> str:
    if is_solution:
        # Mostrar PROBLEMA + SOLUCIÓN
        problem_dict = data.to_problem_dict()
        solution_dict = data.to_solution_dict()
        
        latex = self._render_problem(problem_dict)
        latex += self._render_solution_in_red(solution_dict)
    else:
        # Mostrar SOLO PROBLEMA
        problem_dict = data.to_problem_dict()
        latex = self._render_problem(problem_dict)
    
    return latex
```

---

## 🔍 Búsqueda en Código

Para encontrar rápidamente qué campos son del problema:

```bash
# Grep para encontrar implementations
grep -A 3 "def problem_field_names" modules/*/models.py

# Resultado:
# modules/numeracion/models.py
# ConversionRow:
#     return {"label", "val_decimal", "target_col_idx", "representable"}
# ArithmeticOp:
#     return {"op_type", "system", ...}
```

---

## 📈 Evolución del Código

### Antes (Implícito, confuso)

```python
@dataclass
class ConversionRow:
    # ¿Cuál es del problema? ¿Cuál es de la solución?
    label: str
    val_decimal: int
    target_col_idx: int
    representable: bool
    target_val_str: str
    sol_bin: str
    sol_c2: str
    sol_sm: str
    sol_bcd: str
    
    # No hay validación
    # Renderer debe adivinar qué mostrar
```

### Después (Explícito, validado, seguro)

```python
@dataclass
class ConversionRow(ProblemSolutionExerciseData):
    # PROBLEMA
    label: str
    val_decimal: int
    target_col_idx: int
    representable: bool
    
    # SOLUCIÓN
    target_val_str: str
    sol_bin: str
    sol_c2: str
    sol_sm: str
    sol_bcd: str
    
    @classmethod
    def problem_field_names(cls):
        return {"label", "val_decimal", "target_col_idx", "representable"}
    
    @classmethod
    def solution_field_names(cls):
        return {"target_val_str", "sol_bin", "sol_c2", "sol_sm", "sol_bcd"}
    
    # Validaciones automáticas ✅
    # Métodos to_problem_dict() y to_solution_dict() gratis ✅
    # Renderer sabe exactamente qué mostrar ✅
```

---

## 🎓 Próximos Pasos

### Para Desarrolladores

1. Todas las nuevas dataclasses que representen ejercicios deben heredar de `ProblemSolutionExerciseData`
2. Implementar `problem_field_names()` y `solution_field_names()`
3. La interfaz se encarga del resto

### Para Renderers

1. Usar `data.to_problem_dict()` cuando `is_solution=False`
2. Usar `data.to_full_dict()` cuando `is_solution=True`
3. No adivinar qué mostrar → está en el código

### Para Testing

```python
def test_conversion_row_separation():
    """Valida que problema y solución están bien separados."""
    assert ConversionRow.problem_field_names().isdisjoint(
        ConversionRow.solution_field_names()
    )
    
    row = ConversionRow(...)  # Si hay error, salta aquí en __post_init__
    
    problem = row.to_problem_dict()
    assert "sol_bin" not in problem  # No debe haber soluciones
    
    solution = row.to_solution_dict()
    assert "target_col_idx" not in solution  # No debe haber problema
```

---

## 🏆 Beneficios Conseguidos

| Aspecto | Resultado |
|---------|-----------|
| **Type Safety** | ABC asegura que cada subclase implemente métodos |
| **Runtime Validation** | `__post_init__` valida invariantes |
| **Self-Documenting** | El código es la documentación |
| **Utility Methods** | `to_problem_dict()` gratis |
| **No Hidden State** | Todo problema y solución está explícito |
| **Easy Testing** | Fácil verificar la separación |
| **Refactor-Safe** | Cambiar estructura → validación lo atrapa |
