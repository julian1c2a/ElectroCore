# JSON Intermedio Agnóstico

## Flujo de Generación

```
config.json (entrada)
    ↓
ExamBuilder.build()
    ├─ Genera List[ExerciseData] (objetos Python)
    └─ Serializa a List[Dict] (JSON agnóstico)
    ↓
ExamBuilder.save_intermediate_json()
    ├─ Guarda ejercicios.json (PRODUCTO PRINCIPAL)
    └─ Contiene metadata del examen + ejercicios
    ↓
Renderer agnóstico (LaTeX/DOCX/HTML/etc)
    ├─ Lee ejercicios.json
    ├─ No necesita conocer Python
    └─ Genera PDF/DOCX/HTML
```

## Ejemplo: JSON Intermedio Completo

```json
{
  "exam_metadata": {
    "title": "Examen de Sistemas Numéricos",
    "description": "Evaluación de conversión entre bases numéricas",
    "seed": 42,
    "total_exercises": 2
  },
  "exercises": [
    {
      "title": "Conversión Decimal a Múltiples Bases",
      "description": "Convertir el número decimal 157 a binario, complemento a 2, octal y BCD",
      "metadata": {
        "exercise_type": "ConversionRow",
        "module": "modules.numeracion.models"
      },
      "problem": {
        "label": "N1",
        "val_decimal": 157,
        "target_col_idx": 0,
        "representable": true
      },
      "solution": {
        "target_val_str": "10011101",
        "sol_bin": "10011101",
        "sol_c2": "10011101",
        "sol_sm": "10011101",
        "sol_bcd": "0001 0101 0111"
      }
    },
    {
      "title": "Operación Aritmética en Binario",
      "description": "Realizar suma en binario de dos números",
      "metadata": {
        "exercise_type": "ArithmeticOp",
        "module": "modules.numeracion.models"
      },
      "problem": {
        "op_type": "suma",
        "system": "binario",
        "operand1": 45,
        "operand2": 28,
        "operator_symbol": "+",
        "val1_dec": 45,
        "val2_dec": 28
      },
      "solution": {
        "result_dec": 73,
        "result_bin": "1001001",
        "overflow": false,
        "underflow": false,
        "carry_bits": "0001000"
      }
    }
  ]
}
```

## Características Clave

### 1. **Agnóstico de Renderer**

- El JSON NO contiene instrucciones de LaTeX, DOCX o HTML
- Solo contiene DATOS puros y estructurados
- Cualquier renderer en cualquier lenguaje puede consumirlo

### 2. **Separación Clara Problema/Solución**

- `"problem"`: Lo que el estudiante ve
- `"solution"`: Las respuestas correctas (ocultas en enunciado, visibles en soluciones)
- **No hay mezcla**: Cada campo está en una sola sección

### 3. **Metadata Descriptiva**

- `"exercise_type"`: Tipo de ejercicio (para el renderer saber cómo procesarlo)
- `"module"`: Ubicación Python del generador (para auditoría)
- `"exam_metadata"`: Info del examen completo

### 4. **Legible por Humanos**

- Indentación de 2 espacios
- Nombres de campos en snake_case
- Estructura jerárquica clara
- Sin caracteres escapados innecesarios

### 5. **Determinista**

- Misma `seed` → mismo JSON
- Ideal para reproducibilidad, testing, auditoría

## Cómo Usarlo

### Paso 1: Generar JSON Intermedio

```python
from core.exam_builder import ExamBuilder

builder = ExamBuilder("config/test_exam.json")
exercises = builder.build()
json_file = builder.save_intermediate_json()
# Output: build/json/test_exam_ejercicios.json
```

### Paso 2: Renderer Lee el JSON

```python
import json

# Renderer agnóstico (puede estar en Python, Node.js, C#, etc)
with open("build/json/test_exam_ejercicios.json") as f:
    data = json.load(f)

for exercise in data["exercises"]:
    ex_type = exercise["metadata"]["exercise_type"]
    problem_data = exercise["problem"]
    solution_data = exercise["solution"]
    
    # Render según tipo
    if ex_type == "ConversionRow":
        render_conversion_row(problem_data, solution_data)
    elif ex_type == "ArithmeticOp":
        render_arithmetic_op(problem_data, solution_data)
```

### Paso 3: Generar PDF (LaTeX Renderer consume JSON)

```python
from renderers.latex.main_renderer import LatexExamRenderer
import json

# Leer JSON intermedio (agnóstico)
with open("build/json/test_exam_ejercicios.json") as f:
    exercises_json = json.load(f)

# Renderer LaTeX procesa JSON
renderer = LatexExamRenderer(is_solution=False)
latex_code = renderer.render_from_json(exercises_json)
# Genera PDF enunciado
```

## Ventajas de esta Arquitectura

| Aspecto | Antes (Python → Renderer) | Ahora (Python → JSON → Renderer) |
|--------|---------------------------|----------------------------------|
| **Agnóstico** | ❌ Renderer debe conocer Python | ✅ Solo necesita leer JSON |
| **Reutilizable** | ❌ Código generador Python acoplado | ✅ JSON reutilizable en cualquier renderer |
| **Debuggable** | ❌ Debe inspeccionar objetos Python | ✅ Puede ver JSON limpio legible |
| **Reproducible** | ⚠️ Depende de versión Python | ✅ Versión independiente con seed |
| **Testeable** | ⚠️ Necesita instancia de generador | ✅ Puede testear JSON directo |
| **Mantenible** | ❌ Cambios generador → Cambios renderer | ✅ Contrato estable (JSON schema) |

## Próximos Pasos

1. **Definir JSON Schema**: Especificar estructura esperada para cada tipo
2. **Actualizar Renderers**: Implementar lectura desde JSON intermedio
3. **Crear Validadores**: Validar que JSON generado cumple schema
4. **Documentar Renderers Agnósticos**: Guía para implementar en otros lenguajes
