# Refactorización V2: Soporte para Análógica Independiente

## Resumen Ejecutivo

Se ha completado una refactorización en **dos fases** que permite que **digital** y **análógica** sean completamente independientes y modulares:

### ✅ Fase 1: Organización por Tópicos

- Estructura separada: `build/latex/digital/` y `build/latex/analogica/`
- PDFs en `out/digital/` y `out/analogica/`
- Componentes organizados por módulo

### ✅ Fase 2: Independencia de Ejercicios

- Catálogos separados (`core/catalog.py` vs `core/analogica_catalog.py`)
- Renderers completamente independientes
- Configuración flexible para elegir tipo de examen

---

## Arquitectura de Digital + Análógica

```
┌─────────────────────────────────────────────────────────────┐
│               Generador de Exámenes V2                      │
│  (Ahora soporta Digital Y Análógica de forma independiente) │
└─────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  config/        │
                    │  work_type:     │
                    │  "digital" |    │
                    │  "analogica"    │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
      ┌─────▼──────┐   ┌────▼────┐   ┌──────▼──────┐
      │ Catálogo   │   │ExamBuild│   │Renderer     │
      │ Digital    │   │ (lógica)│   │Principal    │
      │ 5 ejercics │   └────┬────┘   └──────┬──────┘
      └────────────┘        │               │
                    ┌───────▼──────┐        │
                    │ Catálogo     │        │
                    │ Análógica     │        │
                    │ 3 ejercicios  │        │
                    └──────────────┘        │
                                      ┌─────▼─────────────┐
                                      │ Elige Renderer:   │
                                      │ Digital o Análógica│
                                      └───────────────────┘
```

---

## Archivos Creados (Fase 2)

### **modules/analogica/** (Nuevo)

- `__init__.py` - Inicializador del módulo
- `models.py` - Definiciones de datos
  - `AnalogicExerciseData`: Base
  - `TheveniCircuitData`: Thévenin
  - `DividerCircuitData`: Divisores
  - `RCCircuitData`: Circuitos RC
- `generators.py` - Generadores
  - `TheveniGenerator`
  - `DividerGenerator`
  - `RCCircuitGenerator`

### **renderers/latex/analogica_renderer.py** (Nuevo)

- Renderer completamente independiente
- Métodos específicos por tipo de ejercicio
- Genera componentes en `build/latex/analogica/componentes/`
- Placeholders TikZ listos para customizar

### **core/analogica_catalog.py** (Nuevo)

```python
ANALOGICA_EXERCISE_CATALOG = {
    "thevenin_analysis": TheveniGenerator(),
    "divider_circuit": DividerGenerator(),
    "rc_circuit_analysis": RCCircuitGenerator()
}
```

### **config/test_exam_analogica.json** (Nuevo)

```json
{
  "title": "Examen de Análógica V1",
  "work_type": "analogica",
  "seed": 54321,
  "exercises": [
    {"id": "thevenin_analysis", "qty": 1, "difficulty": 2},
    {"id": "divider_circuit", "qty": 1, "difficulty": 2},
    {"id": "rc_circuit_analysis", "qty": 1, "difficulty": 2}
  ]
}
```

---

## Archivos Modificados (Fase 2)

### **config/test_exam.json**

```json
{
  "title": "Examen de Prueba V2",
  "work_type": "digital",        // ✨ Nuevo campo
  "seed": 12345,
  "exercises": [...]
}
```

### **core/exam_builder.py**

- Lee `work_type` de config
- Elige catálogo (`EXERCISE_CATALOG` o `ANALOGICA_EXERCISE_CATALOG`)
- Compatible con versiones anteriores (default: digital)

### **renderers/latex/main_renderer.py**

- Parámetro adicional: `work_type`
- Inicializa renderers según tipo
- Métodos condicionales: `_render_digital_exercise()` / `_render_analogica_exercise()`

### **main_v2.py**

- Lee `work_type` de la configuración
- Crea estructura apropiada
- PDFs van al directorio correcto

---

## Comparativa: Digital vs Análógica

| Aspecto | Digital | Análógica |
|---------|---------|-----------|
| **Ubicación** | `modules/numeracion, combinacional, secuencial` | `modules/analogica/` |
| **Catálogo** | `core/catalog.py` | `core/analogica_catalog.py` |
| **Renderer** | Múltiples especializados | `analogica_renderer.py` único |
| **Build** | `build/latex/digital/{topic}/componentes/` | `build/latex/analogica/componentes/` |
| **Output** | `out/digital/` | `out/analogica/` |
| **Ejercicios** | 5 tipos | 3 tipos (extendible) |
| **Independencia** | ✓ Completa | ✓ Completa |

---

## Cómo Usar

### Examen Digital (Default)

```bash
# Editar main_v2.py para usar config/test_exam.json
# O dejar como está (default)
python main_v2.py
# Genera PDFs en out/digital/
```

### Examen Análógica

```bash
# Opción 1: Crear symlink en main_v2.py
# renderer_exam = LatexExamRenderer(
#     is_solution=False, 
#     base_build_path="build/latex/analogica", 
#     work_type="analogica"
# )

# Opción 2: Cambiar config en main_v2.py
config_file = "config/test_exam_analogica.json"  # ← cambiar esto

python main_v2.py
# Genera PDFs en out/analogica/
```

---

## Extensibilidad

### Agregar Nuevo Ejercicio de Análógica

1. **Crear modelo** en `modules/analogica/models.py`:

```python
@dataclass
class TransformerAnalysisData(AnalogicExerciseData):
    """Análisis de transformadores."""
    primary_voltage: float
    secondary_voltage: float
    # ...
```

1. **Crear generador** en `modules/analogica/generators.py`:

```python
class TransformerGenerator(ExerciseGenerator):
    def topic(self) -> str:
        return "Análisis de Transformadores"
    
    def generate(self, difficulty: int = 1):
        # ...
        return TransformerAnalysisData(...)
```

1. **Registrar en catálogo** en `core/analogica_catalog.py`:

```python
ANALOGICA_EXERCISE_CATALOG = {
    # ...
    "transformer_analysis": TransformerGenerator(),
}
```

1. **Agregar método en renderer** en `renderers/latex/analogica_renderer.py`:

```python
def _render_transformer(self, data: TransformerAnalysisData, index: int) -> str:
    # ...
```

1. **Usar en configuración**:

```json
{
  "exercises": [
    {"id": "transformer_analysis", "qty": 1, "difficulty": 2}
  ]
}
```

---

## Validación

Todas las pruebas pasan:
✓ Catálogos cargados correctamente  
✓ Examen digital genera 5 ejercicios  
✓ Examen análógica genera 3 ejercicios  
✓ Estructura de directorios correcta  
✓ Renderers independientes funcionan  
✓ Configuración se lee correctamente  

---

## Próximos Pasos Sugeridos

1. **Mejorar generadores análógica**: Lógica matemática más realista
2. **Agregar más tipos**: Fourier, Impedancia, Resonancia, Transformadores, etc.
3. **Exámenes mixtos**: Combinar digital + análógica en un mismo PDF
4. **Visualización**: Circuitos TikZ más realistas
5. **Sistema de puntuación**: Scoring diferenciado por tipo
6. **Portabilidad**: Permitir guardar/cargar configuraciones por usuario
