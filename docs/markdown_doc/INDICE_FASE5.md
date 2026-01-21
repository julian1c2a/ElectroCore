# INDICE FASE 5: Text (Enunciados)

## Estructura de Archivos

### 1. Código Principal

```
renderers/latex/
└── phase5_text.py
    ├── Class: Phase5Text(ExerciseRendererPhase)
    ├── Métodos:
    │   ├── __init__(self)
    │   ├── render(exercise_json, is_solution)
    │   ├── _extract_statement()
    │   ├── _extract_instructions()
    │   ├── _extract_explanation()
    │   ├── _extract_steps()
    │   ├── _regenerate_table()
    │   └── _generate_full_document_latex()
    ├── Líneas: 280+
    └── Imports:
        ├── ABC, abstractmethod
        ├── json
        ├── phase4_content
        └── typing
```

---

## 2. Demostración Ejecutable

```
FASE5_DEMO.py
├── Propósito: Demostrar pipeline completo (Fases 1-5)
├── Líneas: 600+
├── Secciones:
│   ├── Definición de ejercicio
│   │   ├── ConversionRow ejemplo
│   │   └── Campos problem + solution
│   ├── Comparación enunciado vs solución
│   │   ├── is_solution=False (estudiante)
│   │   └── is_solution=True (profesor)
│   ├── Salida LaTeX
│   │   ├── Estructura documentos
│   │   ├── Secciones y subsecciones
│   │   └── Tablas con/sin valores
│   ├── Manejo de errores
│   │   ├── Campos faltantes
│   │   └── Fallbacks
│   └── Casos de uso
│       ├── Generar examen
│       ├── Generar clave
│       └── Batch processing
└── Ejecución: `python FASE5_DEMO.py`
```

---

## 3. Documentación Técnica

### 3.1 FASE5_TEXT.md

```
Archivo: FASE5_TEXT.md
Líneas: 500+

Secciones:
├── Resumen Ejecutivo
│   └─ Qué es, para qué, por qué
├── Responsabilidades
│   ├─ Extracción de enunciado
│   ├─ Extracción de instrucciones
│   ├─ Extracción de explicación
│   ├─ Extracción de pasos
│   ├─ Regeneración de tabla
│   └─ Generación de documento
├── Arquitectura
│   ├─ Métodos principales
│   ├─ Flujo de datos
│   ├─ Estructura de clases
│   └─ Herencia
├── Flujo de Datos
│   ├─ Entrada (JSON + tabla Fase 4)
│   ├─ Procesamiento (extracción)
│   ├─ Salida (documento TEX)
│   └─ Metadata (JSON de auditoría)
├── Modos
│   ├─ Enunciado (is_solution=False)
│   │   └─ Estructura: Enunciado + Instrucciones + Tabla
│   └─ Solución (is_solution=True)
│       └─ Estructura: Enunciado + Instrucciones + Tabla + Explicación + Pasos
├── Características
│   ├─ Determinismo
│   ├─ Agnósticismo
│   ├─ Compilabilidad
│   ├─ Completitud
│   └─ Robustez
├── Ejemplos
│   ├─ Código de uso
│   ├─ JSON de entrada
│   └─ Salida LaTeX
├── Manejo de Errores
│   ├─ Campo faltante
│   ├─ Fallback logic
│   └─ Nunca falla (siempre compilable)
├── Validación Post-Fase 5
│   ├─ Checklist
│   ├─ Verificaciones
│   └─ Salud del documento
├── Integración
│   ├─ Con Fase 4
│   ├─ Con pipeline completo
│   └─ Casos de uso
└── Resumen Técnico
    └─ Tabla de referencia rápida
```

---

### 3.2 FASE5_SUMMARY.md

```
Archivo: FASE5_SUMMARY.md
Líneas: 400+

Propósito: RESUMEN EJECUTIVO
Tipo: Para gerentes, arquitectos, stakeholders

Secciones:
├── Visión General
│   └─ Qué es Fase 5, dónde encaja
├── Implementación
│   ├─ Archivo principal
│   ├─ Clase principal
│   └─ Métodos clave
├── Entrada y Salida
│   ├─ Entrada (JSON + tabla)
│   ├─ Salida (documento TEX)
│   └─ Formatos
├── Extracción de Componentes
│   ├─ Enunciado (búsqueda de campos)
│   ├─ Instrucciones (default por tipo)
│   ├─ Explicación (solo solución)
│   └─ Pasos (solo solución)
├── Estructura del Documento
│   ├─ Documento ENUNCIADO (1 sección)
│   ├─ Documento SOLUCIÓN (2 secciones)
│   └─ Comparación visual
├── Características
│   ├─ Determinismo
│   ├─ Agnósticismo
│   ├─ Compilabilidad
│   ├─ Completitud
│   └─ Agnósticismo de Exercise Type
├── Pipeline Completo (5 Fases)
│   └─ Diagrama: Entrada → Fases → PDF
├── Casos de Uso
│   ├─ Generar examen para estudiantes
│   ├─ Generar clave de respuestas
│   └─ Generar examen completo
├── Metadata JSON
│   ├─ Estructura
│   ├─ Campos clave
│   └─ output_json=None (especial)
├── Validación Post-Fase 5
│   ├─ Checklist
│   └─ Criterios de éxito
├── Manejo de Errores
│   ├─ Tabla con situaciones
│   └─ Principio NUNCA fallar
├── Estadísticas
│   ├─ Líneas de código
│   ├─ Métodos
│   ├─ Compilabilidad
│   └─ Status
└── Próximos Pasos
    ├─ Pipeline completado
    └─ Etapas futuras
```

---

## 4. Referencia Rápida

### 4.1 Archivos de Referencia Rápida

```
Archivo: FASE5_QUICK_REFERENCE.txt
Tipo: Cheat sheet
Propósito: Consulta rápida mientras programas

Contenidos:
├── Importar
│   └─ `from renderers.latex.phase5_text import Phase5Text`
├── Usar
│   └─ `phase5 = Phase5Text()`
│       `output = phase5.render(json, is_solution=False)`
├── Acceder
│   └─ `output.latex_content` (documento TEX)
│       `output.metadata` (JSON auditoría)
├── Guardar
│   └─ `with open('archivo.tex', 'w') as f: f.write(output.latex_content)`
├── Compilar
│   └─ `$ pdflatex archivo.tex`
├── Colores
│   ├─ Problema: (240, 240, 240) gris
│   └─ Solución: (200, 255, 200) verde
├── Métodos Privados
│   ├─ _extract_statement()
│   ├─ _extract_instructions()
│   ├─ _extract_explanation()
│   ├─ _extract_steps()
│   ├─ _regenerate_table()
│   └─ _generate_full_document_latex()
├── Campos Esperados (JSON)
│   ├─ problem.statement
│   ├─ problem.instructions
│   ├─ problem.description
│   ├─ problem.title
│   ├─ solution.explanation
│   ├─ solution.steps
│   └─ (todos opcionales, tiene fallbacks)
├── Output
│   ├─ 05_fase5_enunciados.tex (documento)
│   └─ metadata (JSON)
├── Validación
│   ├─ ✓ Enunciado extraído
│   ├─ ✓ Instrucciones presentes
│   ├─ ✓ Tabla regenerada
│   ├─ ✓ LaTeX compilable
│   ├─ Si is_solution:
│   │   ├─ ✓ Explicación
│   │   └─ ✓ Pasos enumerados
│   └─ ✓ Pipeline completo
└── Troubleshooting
    ├─ Documento vacío → Revisar statement/explanation
    ├─ LaTeX invalido → Verificar JSON encoding
    ├─ Tabla faltante → Verificar Fase 4 output
    └─ Pasos vacíos → Si no es solución, es normal
```

---

### 4.2 Completitud Fase 5

```
Archivo: FASE5_COMPLETADA.txt
Propósito: Confirmación de completitud
Tipo: Checklist de éxito

Verificaciones:
├── ✓ CÓDIGO
│   ├─ phase5_text.py creado
│   ├─ Clase Phase5Text definida
│   ├─ 8 métodos implementados
│   ├─ Herencia de ExerciseRendererPhase
│   └─ Sin errores de sintaxis
├── ✓ DEMOS
│   ├─ FASE5_DEMO.py creado (600+ líneas)
│   ├─ Cubre pipeline 1-5
│   ├─ Enunciado vs Solución
│   ├─ Manejo de errores
│   ├─ Casos de uso
│   └─ Ejecutable sin errores
├── ✓ DOCUMENTACIÓN
│   ├─ FASE5_TEXT.md creado (500+ líneas)
│   ├─ FASE5_SUMMARY.md creado (400+ líneas)
│   ├─ Ejemplos de código incluidos
│   ├─ Diagrama de flujo incluido
│   ├─ Manejo de errores documentado
│   └─ Validación documentada
├── ✓ INTEGRACIÓN
│   ├─ Hereda de ExerciseRendererPhase
│   ├─ Usa phase4_content para tabla
│   ├─ Sigue patrón Pipe & Filter
│   ├─ JSON acumula metadata
│   └─ output_json=None (marca fin)
├── ✓ CARACTERÍSTICAS
│   ├─ Determinismo garantizado
│   ├─ Agnóstico a exercise type
│   ├─ 100% compilable
│   ├─ Robusto (nunca falla)
│   ├─ Dos modos (enunciado/solución)
│   └─ Manejo de campos faltantes
├── ✓ TESTING
│   ├─ FASE5_DEMO.py pasó ejecución
│   ├─ Output verificado
│   ├─ Modo enunciado funciona
│   ├─ Modo solución funciona
│   ├─ Errores manejados
│   └─ LaTeX compilable
└── ✓ PIPELINE COMPLETO
    ├─ Fase 1: COMPLETADA
    ├─ Fase 2: COMPLETADA
    ├─ Fase 3: COMPLETADA
    ├─ Fase 4: COMPLETADA
    ├─ Fase 5: COMPLETADA
    └─ STATUS: 100% COMPLETADO
```

---

## 5. Estructura de Clases

```
phase5_text.py:

class Phase5Text(ExerciseRendererPhase):
    
    # Constantes de Colores (heredadas de Fase 3)
    PROBLEMA_COLOR = (240, 240, 240)      # Gris
    SOLUCION_COLOR = (200, 255, 200)      # Verde
    ENCABEZADO_COLOR = (200, 200, 200)    # Gris medio
    
    # Constantes de Tipografía
    FONT_TITLE = "\\textbf{}"              # Negrita
    FONT_STATEMENT = "\\textit{}"          # Itálica
    FONT_EXPLANATION = "\\texttt{}"        # Monoespaciado
    
    # Métodos Públicos
    def render(exercise_json, is_solution=False) → RendererOutput
    
    # Métodos Privados
    def _extract_statement() → str
    def _extract_instructions() → str
    def _extract_explanation() → str
    def _extract_steps() → list[str]
    def _regenerate_table() → str
    def _generate_full_document_latex() → str
```

---

## 6. Flujo de Datos

```
INPUT:
┌─────────────────────────────────┐
│ exercise_json                   │
│ ├─ exercise_type                │
│ ├─ title                        │
│ ├─ problem                      │
│ │  ├─ statement                 │
│ │  ├─ description               │
│ │  ├─ instructions              │
│ │  └─ [otros campos]            │
│ ├─ solution                     │
│ │  ├─ explanation               │
│ │  ├─ steps                     │
│ │  └─ [otros campos]            │
│ └─ is_solution (flag)           │
└─────────────────────────────────┘
        ↓
    render()
        ↓
    _extract_statement()
    _extract_instructions()
    _extract_explanation()
    _extract_steps()
    _regenerate_table()
    _generate_full_document_latex()
        ↓
OUTPUT:
┌────────────────────────────────────┐
│ RendererOutput                     │
│ ├─ latex_content (documento TEX)   │
│ └─ metadata (JSON auditoría)       │
│    ├─ phase5_text: {               │
│    │   "status": "completed",      │
│    │   "statement_extracted": ..., │
│    │   ... más campos ...          │
│    │   "output_json": null         │  ← ÚLTIMO
│    │ }                             │
│    └─ [metadata de fases 1-4]      │
└────────────────────────────────────┘
```

---

## 7. Estrategia de Extracción

### 7.1 Enunciado

```
Búsqueda en orden:
1. problem['statement']
   └─ Si existe → Usar
2. problem['description']
   └─ Si existe → Usar
3. title + description combinados
   └─ Si existen → Usar ambos
4. "Statement not found"
   └─ Si nada → Mensaje genérico
```

### 7.2 Instrucciones

```
Búsqueda en orden:
1. problem['instructions']
   └─ Si existe → Usar
2. problem['how_to_solve']
   └─ Si existe → Usar
3. Genéricas por exercise_type
   ├─ ConversionRow: "Convierte el número a..."
   ├─ ArithmeticOp: "Realiza la operación..."
   └─ Otros: "Resuelve el siguiente problema..."
```

### 7.3 Explicación (Solo si is_solution=True)

```
Búsqueda en orden:
1. solution['explanation']
   └─ Si existe → Usar
2. solution['description']
   └─ Si existe → Usar
3. (vacío)
   └─ Si nada → Omitir subsección
```

### 7.4 Pasos (Solo si is_solution=True)

```
Búsqueda en orden:
1. solution['steps'] (lista)
   └─ Si existe y es lista → Usar
2. solution['resolution_steps']
   └─ Si existe → Usar
3. (lista vacía)
   └─ Si nada → \begin{enumerate} vacío
```

---

## 8. Validación Post-Fase 5

```
CHECKLIST DE VALIDACION:

Componentes Extraídos:
├─ ✓ statement_extracted (boolean)
├─ ✓ instructions_extracted (boolean)
├─ ✓ explanation_extracted (boolean si solución)
└─ ✓ steps_extracted (boolean si solución)

Componentes en Documento:
├─ ✓ Enunciado presente
├─ ✓ Instrucciones presentes
├─ ✓ Tabla regenerada (con Fase 4 content)
├─ ✓ Si is_solution=True:
│  ├─ ✓ Explicación presente (sección)
│  └─ ✓ Pasos enumerados (lista)
└─ ✓ Estructura LaTeX correcta

Compilabilidad:
├─ ✓ Sintaxis LaTeX válida
├─ ✓ Paquetes definidos
├─ ✓ Colores definidos
├─ ✓ Comandos personalizados válidos
└─ ✓ Compilable con pdflatex

Pipeline:
├─ ✓ Metadata de Fase 1 presente
├─ ✓ Metadata de Fase 2 presente
├─ ✓ Metadata de Fase 3 presente
├─ ✓ Metadata de Fase 4 presente
├─ ✓ Metadata de Fase 5 presente
└─ ✓ output_json=None (marca fin)
```

---

## 9. Casos de Uso Completos

### 9.1 Generar Examen Único

```python
from renderers.latex.phase5_text import Phase5Text

# Cargar ejercicio
with open('ejercicio.json', 'r') as f:
    ejercicio = json.load(f)

# Generar enunciado
phase5 = Phase5Text()
output = phase5.render(ejercicio, is_solution=False)

# Guardar y compilar
with open('ejercicio.tex', 'w') as f:
    f.write(output.latex_content)

os.system('pdflatex ejercicio.tex')
# Resultado: ejercicio.pdf
```

### 9.2 Generar Examen Completo (Múltiples Ejercicios)

```python
from renderers.latex.phase5_text import Phase5Text

ejercicios = cargar_lista_ejercicios()

# Generar todos
output_texts = []
for i, ej in enumerate(ejercicios):
    phase5 = Phase5Text()
    output = phase5.render(ej, is_solution=False)
    
    # Nombre único
    nombre = f'ejercicio_{i:03d}.tex'
    with open(nombre, 'w') as f:
        f.write(output.latex_content)
    
    output_texts.append((nombre, output))

# Compilar todos
for nombre, output in output_texts:
    os.system(f'pdflatex {nombre}')
```

### 9.3 Generar Clave de Respuestas

```python
from renderers.latex.phase5_text import Phase5Text

ejercicio = cargar_ejercicio()

# Generar con explicaciones
phase5 = Phase5Text()
output = phase5.render(ejercicio, is_solution=True)

# Guardar
with open('solucion.tex', 'w') as f:
    f.write(output.latex_content)

# Compilar
os.system('pdflatex solucion.tex')
# Resultado: solucion.pdf (con explicación y pasos)
```

---

## 10. Mapa de Navegación

```
FASE 5 DOCUMENTATION TREE:

FASE5_SUMMARY.md ←─── Inicio (resumen ejecutivo)
├─ ¿Qué es?
├─ ¿Cómo funciona?
├─ ¿Qué produce?
└─ Casos de uso

FASE5_TEXT.md ←────── Profundidad técnica
├─ Responsabilidades (5 funciones)
├─ Arquitectura (8 métodos)
├─ Flujo de datos
├─ Modos (enunciado/solución)
├─ Características
├─ Manejo de errores
├─ Validación
└─ Integración

INDICE_FASE5.md ←──── Referencia estructural
├─ Archivos
├─ Clases
├─ Métodos
├─ Flujo
└─ Validación

FASE5_QUICK_REFERENCE.txt ←─ Cheat sheet
├─ Importar
├─ Usar
├─ Guardar
├─ Compilar
└─ Troubleshooting

FASE5_COMPLETADA.txt ←─ Checklist
├─ Código ✓
├─ Demos ✓
├─ Documentación ✓
├─ Integración ✓
└─ Status ✓

phase5_text.py ←────── Código
├── Class Phase5Text
├── 8 métodos
└── 280+ líneas

FASE5_DEMO.py ←────── Ejecución
├─ Pipeline 1-5
├─ Enunciado vs Solución
└─ Compilable
```

---

## 11. Ruta de Lectura Recomendada

### Para Principiantes

1. **FASE5_SUMMARY.md** (resumen)
2. **FASE5_DEMO.py** (ver en acción)
3. **FASE5_QUICK_REFERENCE.txt** (usar)

### Para Desarrolladores

1. **FASE5_TEXT.md** (detalles técnicos)
2. **phase5_text.py** (código fuente)
3. **FASE5_DEMO.py** (ejemplos)
4. **INDICE_FASE5.md** (esta referencia)

### Para Arquitectos

1. **RESUMEN_GENERAL_FASES_1_2_3_4_5.md** (pipeline completo)
2. **FASE5_SUMMARY.md** (Fase 5 en contexto)
3. **INDICE_FASE5.md** (estructura)

---

## 12. Tabla de Referencia Rápida

| Aspecto | Detalle |
|---------|---------|
| **Archivo Principal** | `renderers/latex/phase5_text.py` |
| **Clase** | `Phase5Text(ExerciseRendererPhase)` |
| **Líneas** | 280+ |
| **Métodos** | 8 (1 público, 7 privados) |
| **Input** | JSON exercise + is_solution flag |
| **Output** | TEX document + metadata |
| **Responsabilidad** | Composición de documento final |
| **Especial** | output_json=None (última fase) |
| **Compilabilidad** | 100% LaTeX válido |
| **Agnósticismo** | Cualquier exercise_type |
| **Error Handling** | Nunca falla (siempre compilable) |
| **Modos** | Enunciado (1 sección) / Solución (2 secciones) |
| **Demo** | `FASE5_DEMO.py` (600+ líneas) |
| **Status** | ✓ COMPLETADA |

---

**FIN DE INDICE FASE 5**

Este documento es una **referencia estructural** de todos los componentes de Fase 5.

Para información detallada, consulta:

- **Técnico**: FASE5_TEXT.md
- **Ejecutivo**: FASE5_SUMMARY.md
- **Rápida**: FASE5_QUICK_REFERENCE.txt
