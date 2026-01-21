# FASE 5: Text - Agregador de Enunciados y Explicaciones

## Resumen Ejecutivo

**Fase 5** es la **ÚLTIMA FASE** del pipeline. Toma la tabla llena de Fase 4 y la complementa con enunciados, instrucciones, explicaciones y pasos de resolución para generar un **documento COMPLETO listo para compilar a PDF**.

| Aspecto | Descripción |
|---------|-------------|
| **Entrada** | JSON validado + TEX compilado de Fase 4 |
| **Salida** | TEX COMPLETO (documento final) + metadata |
| **Archivo** | `renderers/latex/phase5_text.py` |
| **Clase** | `Phase5Text(ExerciseRendererPhase)` |
| **TEX Output** | `05_fase5_enunciados.tex` |
| **Especial** | ⚠️ output_json=None (última fase) |

---

## Responsabilidades

### 1. Extracción de Enunciado

**Objetivo**: Obtener el texto del problema a resolver.

Campos buscados (en orden):

- `problem['statement']` - Enunciado explícito
- `problem['description']` - Descripción del problema
- `title` + `description` - Fallback genérico

**Resultado**: String con enunciado compilable en LaTeX.

### 2. Extracción de Instrucciones

**Objetivo**: Obtener cómo resolver el problema.

Campos buscados:

- `problem['instructions']` - Instrucciones explícitas
- `problem['how_to_solve']` - Forma de resolver
- Default genérico según `exercise_type`

**Resultado**: String con instrucciones para el alumno.

### 3. Extracción de Explicación

**Objetivo**: Obtener explicación de la solución (solo si `is_solution=True`).

Campos buscados:

- `solution['explanation']` - Explicación de pasos
- `solution['description']` - Descripción de solución

**Especial**: Solo se extrae si `is_solution=True`.

**Resultado**: String con explicación detallada o vacío.

### 4. Extracción de Pasos

**Objetivo**: Obtener pasos de resolución (solo si `is_solution=True`).

Campos buscados:

- `solution['steps']` - Lista de pasos
- `solution['resolution_steps']` - Pasos de resolución

**Especial**: Solo se extrae si `is_solution=True` y existe lista.

**Resultado**: Lista de strings (cada uno es un paso).

### 5. Composición del Documento

**Objetivo**: Armar el documento final con todos los componentes.

Estructura:

1. Encabezado (tipo documento)
2. Definiciones (colores, comandos)
3. Enunciado
4. Instrucciones (si existen)
5. Tabla (de Fase 4)
6. [Si is_solution=True]:
   - Explicación
   - Pasos de resolución

**Resultado**: String con LaTeX completo y compilable.

---

## Arquitectura

### Clase Principal: `Phase5Text`

```python
class Phase5Text(ExerciseRendererPhase):
    """
    FASE 5: Agregador de texto (enunciados, explicaciones).
    ÚLTIMA FASE del pipeline.
    """
    
    # Colores (heredados)
    PROBLEMA_COLOR = "240,240,240"
    SOLUCION_COLOR = "200,255,200"
    ENCABEZADO_COLOR = "230,230,230"
    
    # Tipografía
    FONT_TITLE = "large"
    FONT_STATEMENT = "normalsize"
    FONT_EXPLANATION = "small"
```

### Métodos Principales

#### `render(exercise_json, is_solution)`

**Entrada**: JSON acumulado de Fases 1-4 + flag de solución
**Salida**: `PhaseOutput` con TEX completo

Flujo:

1. Extrae metadata de fases anteriores
2. Extrae statement, instructions, explanation, steps
3. Regenera tabla de Fase 4
4. Compone documento completo
5. Retorna `PhaseOutput(latex, output_json=None, ...)`

**Especial**: `output_json=None` porque es última fase.

#### `_extract_statement(exercise_json, exercise_type)`

Obtiene enunciado del problema.

#### `_extract_instructions(exercise_json, exercise_type)`

Obtiene instrucciones (o genéricas si no hay).

#### `_extract_explanation(exercise_json, is_solution)`

Obtiene explicación de solución (solo si `is_solution=True`).

#### `_extract_steps(exercise_json, exercise_type, is_solution)`

Obtiene lista de pasos (solo si `is_solution=True`).

#### `_generate_full_document_latex(...)`

Genera LaTeX compilable COMPLETO.

Estructura del documento:

```latex
% Encabezado
% Definiciones de color
% Comando \cellpadding

\section*{Enunciado}
[statement aquí]

\subsection*{Instrucciones}
[instructions aquí]

[tabla de Fase 4]

% SI is_solution=True:
\section*{Solucion}

\subsection*{Explicacion}
[explanation aquí]

\subsection*{Pasos de Resolucion}
\begin{enumerate}
  \item paso 1
  \item paso 2
  ...
\end{enumerate}
```

---

## Flujo de Datos

### Entrada de Fase 5

```
ejercicio.json (contiene problem + solution + metadata de Fases 1-4)
{
  'title': '...',
  'metadata': {'exercise_type': 'ConversionRow'},
  'problem': {
    'statement': 'Convierte 157 a...',
    'instructions': 'Para cada base...',
    ...
  },
  'solution': {
    'explanation': 'El numero 157...',
    'steps': ['Paso 1...', 'Paso 2...'],
    ...
  },
  'phase1_validation': {...},
  'phase2_structure': {...},
  'phase3_details': {...},
  'phase4_content': {...}
}
```

### Procesamiento

```
1. Leer statement → "Convierte 157..."
2. Leer instructions → "Para cada base..."
3. Leer explanation → "El numero 157..." (si is_solution=True)
4. Leer steps → ['Paso 1', 'Paso 2'] (si is_solution=True)
5. Regenerar tabla de Fase 4
6. Componer documento completo
```

### Salida de Fase 5

```
05_fase5_enunciados.tex:
  % Documento completo, compilable directamente
  \usepackage[usenames,dvipsnames]{xcolor}
  \section*{Enunciado}
  ...
  \begin{tabular}{...}
  ...
  \end{tabular}
  ...
  % Si es solución:
  \section*{Solucion}
  ...

ejercicio_fase5.json:
  Contiene metadata de auditoría (no para siguiente fase)
  {
    'phase5_text': {
      'status': 'completed',
      'document_complete': True,
      'pipeline_complete': True
    }
  }
```

---

## Modos de Operación

### Modo Enunciado (`is_solution=False`)

**Propósito**: Documento para que estudiante resuelva.

**Contenido**:

- Enunciado completo
- Instrucciones claras
- Tabla con espacios en blanco
- **NO** explicación
- **NO** pasos

**Estructura**:

```
ENUNCIADO
=========
Convierte 157 a binario, C2, SM y BCD.

INSTRUCCIONES
==============
Para cada base...

[Tabla GRIS con espacios]
```

**Uso**: Imprimir para examen, distribuir a estudiantes.

### Modo Solución (`is_solution=True`)

**Propósito**: Documento con respuestas para profesor.

**Contenido**:

- Enunciado completo (igual que enunciado)
- Instrucciones claras (igual)
- Tabla con TODAS las respuestas
- Explicación de la solución
- Pasos de resolución

**Estructura**:

```
SOLUCION
========
Convierte 157 a binario, C2, SM y BCD.

INSTRUCCIONES
==============
Para cada base...

[Tabla VERDE con todas respuestas]

EXPLICACION
============
El numero 157 en decimal se convierte a binario...

PASOS DE RESOLUCION
====================
1. 157 / 2 = 78 resto 1
2. 78 / 2 = 39 resto 0
...
```

**Uso**: Clave de respuestas, evaluación, documentación.

---

## Características Clave

### ✓ Determinismo

- Mismo JSON → Siempre mismo TEX
- Sin variabilidad
- Reproducible

### ✓ Agnósticismo

- Un JSON, dos documentos (enunciado/solución)
- Lógica condicional según `is_solution`

### ✓ Compilabilidad

- TEX siempre válido y compilable
- Listo para `pdflatex`
- Produce PDF directamente

### ✓ Completitud

- Documento FINAL del pipeline
- No requiere más fases
- Listo para uso

### ✓ Agnósticismo

- Funciona para ConversionRow, ArithmeticOp, otros
- Exercise type genérico

---

## Ejemplo: Conversión de Número

### Entrada JSON

```json
{
  "title": "Conversión de 157",
  "problem": {
    "statement": "Convierte 157 a binario, C2, SM y BCD",
    "instructions": "Realiza la conversión para cada base"
  },
  "solution": {
    "explanation": "157 = 10011101 en binario...",
    "steps": [
      "157 / 2 = 78 resto 1",
      "78 / 2 = 39 resto 0",
      "...",
      "Resultado: 10011101"
    ]
  }
}
```

### Salida ENUNCIADO

```latex
\section*{Enunciado}
Convierte 157 a binario, C2, SM y BCD

\subsection*{Instrucciones}
Realiza la conversión para cada base

\begin{tabular}{|c|c|c|c|c|c|}
...
| a | 157 | ___ | ___ | ___ | ___ |
...
\end{tabular}
```

### Salida SOLUCION

```latex
\section*{Enunciado}
Convierte 157 a binario, C2, SM y BCD

\subsection*{Instrucciones}
Realiza la conversión para cada base

\begin{tabular}{|c|c|c|c|c|c|}
...
| a | 157 | 10011101 | 10011101 | 10011101 | 0001 0101 0111 |
...
\end{tabular}

\section*{Solucion}

\subsection*{Explicacion}
157 = 10011101 en binario...

\subsection*{Pasos de Resolucion}
\begin{enumerate}
  \item 157 / 2 = 78 resto 1
  \item 78 / 2 = 39 resto 0
  ...
  \item Resultado: 10011101
\end{enumerate}
```

---

## Manejo de Errores

### Error: Campo faltante

- **Causa**: No hay `problem['statement']`
- **Acción**: Usa `title` como fallback
- **Resultado**: Documento con título genérico
- **Severidad**: INFO

### Error: No hay explanation

- **Causa**: `is_solution=True` pero falta `solution['explanation']`
- **Acción**: Omite subsección de explicación
- **Resultado**: Documento sin explicación pero compilable
- **Severidad**: INFO

### Error: No hay steps

- **Causa**: `is_solution=True` pero falta `solution['steps']`
- **Acción**: Omite lista de pasos
- **Resultado**: Documento sin pasos pero compilable
- **Severidad**: INFO

**Principio General**: NUNCA fallar. Siempre generar TEX compilable.

---

## Validación de Salida

### Checklist de Fase 5

```
[OK] Enunciado extraído
[OK] Instrucciones presentes (genéricas o explícitas)
[OK] Tabla regenerada de Fase 4
[OK] LaTeX compilable
[OK] Documento estructurado (secciones/subsecciones)
[OK] Colores aplicados (gris/verde)
[OK] Si is_solution=True:
      [OK] Explicación presente
      [OK] Pasos enumerados
[OK] Metadata de auditoría en JSON
```

---

## Integración con Pipeline

### Entrada desde Fase 4

```
Phase4Content.render() 
  ↓ retorna PhaseOutput
    - latex_content: tabla con valores
    - output_json: JSON + phase4_content
```

### Fase 5 consume

```
Phase5Text.render(output_json)
  - Lee JSON completo con statement, explanation, steps
  - Regenera tabla de Fase 4
  - Compone documento final
  ↓ retorna PhaseOutput
    - latex_content: DOCUMENTO COMPLETO
    - output_json: metadata de auditoría (None como siguiente)
```

### Salida final

```
05_fase5_enunciados.tex
  ↓
pdflatex 05_fase5_enunciados.tex
  ↓
05_fase5_enunciados.pdf
```

---

## Resumen Técnico

| Aspecto | Detalle |
|---------|---------|
| **Líneas de Código** | ~280 |
| **Métodos Principales** | 8 (render + 7 extract/generate) |
| **Exercise Types** | Cualquiera (agnóstico) |
| **Colores Usados** | 3 (heredados) |
| **Estructura Enunciado** | 1 sección + tabla |
| **Estructura Solución** | 2 secciones + tabla + explicación + pasos |
| **Output JSON** | None (última fase) |
| **Compilabilidad** | 100% |
| **Especial** | ⚠️ output_json=None indica fin del pipeline |

---

## Próximas Etapas

**Después de Fase 5**:

- ❌ No hay Fase 6 (Fase 5 es la última)
- ✓ Pipeline de 5 fases está **COMPLETO**

**Siguientes pasos** (fuera del pipeline):

1. Integración con `main_v2.py`
2. Creación de RendererPipeline (orchestrador)
3. Batch processing (múltiples ejercicios)
4. Tests unitarios
5. Documentación final

---

## Conclusión

Fase 5 es la **CULMINACIÓN** del pipeline de 5 fases:

✓ Toma tablas compiladas  
✓ Agrega contexto y explicación  
✓ Produce documentos completos  
✓ Listo para PDF  

**Pipeline**: Validación → Estructura → Detalles → Contenido → **Texto** ✓

**Estado**: COMPLETADA
