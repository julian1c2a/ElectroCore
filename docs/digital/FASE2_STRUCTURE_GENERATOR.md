# FASE 2: Structure Generator (Generador de Estructura)

## Resumen Ejecutivo

**Fase 2** es el generador de marcos/estructura de tabla para ejercicios de numeración. Toma un JSON validado (de Fase 1) y genera:

1. **TEX compilable**: Tabla vacía pero correctamente dimensionada
2. **JSON enriquecido**: Con metadata de estructura para siguiente fase

## Responsabilidades

### Qué HACE

- ✅ Determina el número de filas basado en `exercise_type` y parámetros del problema
- ✅ Genera código LaTeX de tabla (`\begin{tabular}...\end{tabular}`)
- ✅ Define columnas estándar (Etiqueta, Decimal, Binario, C2, SM, BCD)
- ✅ Crea bordes básicos con `\hline`
- ✅ Produce TEX compilable (tabla vacía pero estructurada)
- ✅ Propaga JSON sin cambios (solo agrega metadata de `phase2_structure`)

### Qué NO HACE

- ❌ Agregar contenido/valores (eso es **Fase 4**)
- ❌ Agregar estilos visuales: colores, padding, alineación (eso es **Fase 3**)
- ❌ Validar JSON (eso fue **Fase 1**)
- ❌ Generar enunciados o explicaciones (eso es **Fase 5**)

## Arquitectura

### Entrada

```json
{
  "title": "Conversión Decimal a Múltiples Bases",
  "description": "Convierte 157 a binario, C2, SM y BCD",
  "metadata": {
    "exercise_type": "ConversionRow",
    "module": "modules.numeracion.models",
    "seed": 42
  },
  "problem": {
    "label": "a",
    "val_decimal": 157,
    "target_col_idx": 2,
    "representable": true
  },
  "solution": {...},
  "phase1_validation": {...}  // Metadata de Fase 1
}
```

### Procesamiento

```python
Phase2StructureGenerator.render(exercise_json, is_solution=False)
  |
  ├─ _extract_metadata(exercise_json)
  │  └─ Obtiene: exercise_type, module, seed
  │
  ├─ _extract_problem(exercise_json)
  │  └─ Obtiene: label, val_decimal, target_col_idx, representable
  │
  ├─ _determine_num_rows(exercise_type, problem)
  │  └─ Retorna: 1 para ConversionRow, 3 para ArithmeticOp, 1 por defecto
  │
  ├─ _generate_latex_table(num_rows, is_solution)
  │  └─ Genera: código LaTeX con estructura de tabla
  │
  └─ return PhaseOutput(
       latex_content = "% Fase 2\n\\begin{tabular}...",
       output_json = json + phase2_structure metadata,
       phase_name = "estructura",
       tex_filename = "02_fase2_estructura.tex"
     )
```

### Salida

**TEX Output** (`02_fase2_estructura.tex`):

```latex
% ========================================
% FASE 2: ESTRUCTURA - marcos y dimensiones de tabla
% Tipo: ENUNCIADO
% ========================================

% Tabla de conversion de bases numericas
% Estructura: 6 columnas x 1 filas

\begin{tabular}{|c|c|c|c|c|c|}
\hline
Etiqueta & Decimal & Binario & C2 & SM & BCD \\
\hline
 &  &  &  &  &  \\
\hline
\end{tabular}

% ========================================
% Salida de FASE 2
% ---
% Esta tabla está:
% [OK] Correctamente dimensionada (filas y columnas)
% [OK] Estructurada con bordes y encabezados
% [OK] Compilable como TEX
% [NO] Sin contenido (se agrega en Fase 3+)
% [NO] Sin estilos visuales (colores, padding, etc)
% ========================================
```

**JSON Output** (añade metadata):

```json
{
  ...JSON anterior...
  "phase2_structure": {
    "status": "generated",
    "table_type": "numeracion_conversion",
    "num_rows": 1,
    "num_cols": 6,
    "columns": ["Etiqueta", "Decimal", "Binario", "C2", "SM", "BCD"],
    "structure_defined": true,
    "is_solution": false
  }
}
```

## Lógica de Determinación de Filas

```python
def _determine_num_rows(exercise_type: str, problem: Dict) -> int:
    if exercise_type == 'ConversionRow':
        # Una fila para el número a convertir
        return 1
    
    elif exercise_type == 'ArithmeticOp':
        # Tipicamente 3 filas: operand1, operand2, result
        return 3
    
    else:
        # Default: una fila
        return 1
```

## Propiedades Clave

### Determinismo

- **Mismo JSON** → **Mismo TEX**
- No usa randomización
- Reproducible

### Agnósticismo

- Funciona tanto para **enunciado** como para **solución**
- Estructura de tabla idéntica
- Solo cambian dimensiones basadas en problem

### Composabilidad

- **Input**: JSON validado + compilable
- **Output**: JSON + TEX compilable
- Encadena perfectamente con Fase 1 y Fase 3

### Separación de Responsabilidades

```
Fase 1: Validación    → ¿Es correcto el JSON?
Fase 2: Estructura    → ¿Qué forma tiene la tabla?
Fase 3: Detalles      → ¿Qué estilos tiene la tabla?
Fase 4: Contenido     → ¿Qué valores llena la tabla?
Fase 5: Enunciados    → ¿Qué texto acompaña la tabla?
```

## Manejo de Errores

### Error 1: JSON no tiene `phase1_validation`

```python
# Indicador: JSON no procesado por Fase 1
# Solución: Pasar JSON a través de Fase 1 primero
```

### Error 2: `exercise_type` desconocido

```python
# Solución: Usar 1 fila por defecto + emitir warning
# "exercise_type no reconocido, usando 1 fila"
```

### Error 3: Fase 1 encontró validación fallida

```python
# Solución: Pipeline NO continua
# Error reportado en Fase 1, nunca llega a Fase 2
```

## Caso de Uso Completo

### 1. Crear Pipeline

```python
from renderers.latex.phase1_validator import Phase1DataValidator
from renderers.latex.phase2_structure import Phase2StructureGenerator
from renderers.latex.renderer_base import RendererPipeline

pipeline = RendererPipeline()
pipeline.add_phase(Phase1DataValidator())
pipeline.add_phase(Phase2StructureGenerator())
```

### 2. Renderizar

```python
output = pipeline.render(ejercicio_json, is_solution=False)
```

### 3. Acceder a resultados

```python
fase1_output = output.phases[0]
fase2_output = output.phases[1]

# TEX de estructura
print(fase2_output.latex_content)

# Metadata de estructura
print(fase2_output.output_json['phase2_structure'])
```

### 4. Guardar archivos

```python
pipeline.save_main_file('build/latex/main.tex')
# Resultado:
# - build/latex/00_fase1_validacion.tex
# - build/latex/02_fase2_estructura.tex
# - build/latex/main.tex (con \include de ambas)
```

## Relación con otras Fases

### Fase 1 → Fase 2

- **Entrada a Fase 2**: JSON validado + `phase1_validation` metadata
- **Salida de Fase 1**: Garantiza que JSON es estructuralmente correcto
- **Dependencia**: Fase 2 asume que Fase 1 ejecutó exitosamente

### Fase 2 → Fase 3

- **Entrada a Fase 3**: JSON + `phase2_structure` metadata
- **Salida de Fase 2**: Estructura de tabla definida
- **Dependencia**: Fase 3 usa `num_rows`, `num_cols` para aplicar estilos

## Característica: TEX Compilable en cada Fase

Cada fase produce TEX que es **independientemente compilable**:

```latex
% Fase 1: TEX de validación (comentarios)
% Fase 2: TEX de tabla vacía (compilable)
% Fase 3: TEX con estilos (compilable)
% Fase 4: TEX con contenido (compilable)
% Fase 5: TEX con enunciados (compilable, FINAL)
```

Permite debugging intermedio:

- Ver estructura sin contenido
- Ver estructura con estilos sin contenido
- Etc.

## Características Futuras

- [ ] Soporte para más tipos de ejercicio (ArithmeticOp, etc)
- [ ] Determinación dinámica de ancho de columna basada en valores
- [ ] Fusión de celdas para encabezados complejos
- [ ] Validación: verificar que num_rows es positivo

## Integración con Pipeline

```
ejercicio.json
    ↓
Phase1DataValidator
    ├─ 00_fase1_validacion.tex
    ├─ JSON + phase1_validation
    ↓
Phase2StructureGenerator  ←── ACTUAL
    ├─ 02_fase2_estructura.tex
    ├─ JSON + phase2_structure
    ↓
Phase3Details (PROXIMO)
    ├─ 03_fase3_detalles.tex
    ├─ JSON + phase3_details
    ↓
Phase4Content
    ├─ 04_fase4_contenido.tex
    ├─ JSON + phase4_content
    ↓
Phase5Text
    ├─ 05_fase5_texto.tex
    ├─ JSON: None
    ↓
RendererPipeline.save_main_file()
    └─ main.tex (composición final)
    ↓
[PDF OUTPUT]
```

## Archivos Implementados

- `renderers/latex/phase2_structure.py`: Implementación de Phase2StructureGenerator
- `FASE2_DEMO.py`: Demostración ejecutable del flujo Fase 1 → Fase 2

## Status

✅ **COMPLETADO**: Phase2StructureGenerator

- Análisis de problema
- Determinación de filas
- Generación de LaTeX compilable
- Metadata para siguiente fase

⏳ **PROXIMO**: Phase3Details

- Agregar colores
- Agregar alineación
- Agregar padding
- Mantener tabla vacía (sin valores)
