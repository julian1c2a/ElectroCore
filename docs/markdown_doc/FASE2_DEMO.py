#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FASE 2: STRUCTURE GENERATOR - Demostración completa

Muestra cómo fluye JSON a través del pipeline:
  JSON validado (Fase 1) -> Phase1DataValidator -> JSON + TEX
                         |
                         v
                Phase2StructureGenerator -> JSON + TEX
"""

print("=" * 80)
print("FASE 2: STRUCTURE GENERATOR")
print("=" * 80)

# ============================================================================
# ENTRADA: JSON validado que sale de Fase 1
# ============================================================================

ejercicio_json = {
    'title': 'Conversion Decimal a Multiples Bases',
    'description': 'Convierte 157 a binario, C2, SM y BCD',
    'metadata': {
        'exercise_type': 'ConversionRow',
        'module': 'modules.numeracion.models',
        'seed': 42
    },
    'problem': {
        'label': 'a',
        'val_decimal': 157,
        'target_col_idx': 2,
        'representable': True
    },
    'solution': {
        'sol_bin': '10011101',
        'sol_c2': '10011101',
        'sol_sm': '10011101',
        'sol_bcd': '0001 0101 0111',
        'target_val_str': '10011101'
    },
    'phase1_validation': {
        'status': 'valid',
        'exercise_type': 'ConversionRow',
        'problem_fields': ['label', 'val_decimal', 'target_col_idx', 'representable'],
        'solution_fields': ['sol_bin', 'sol_c2', 'sol_sm', 'sol_bcd', 'target_val_str'],
        'validated_at': 'phase1'
    }
}

print("\n[OK] JSON Validado de Fase 1:")
print("  - Titulo: " + ejercicio_json['title'])
print("  - Tipo: " + ejercicio_json['metadata']['exercise_type'])
print("  - Campos problema: " + str(list(ejercicio_json['problem'].keys())))
print("  - Campos solucion: " + str(list(ejercicio_json['solution'].keys())))

# ============================================================================
# FASE 2: Structure Generator
# ============================================================================

print("\n" + "=" * 80)
print("FASE 2: ANALISIS Y GENERACION DE ESTRUCTURA")
print("=" * 80)

print("""
[PASO 1] Analizar problema
  - exercise_type: ConversionRow
  - num_rows determinado: 1 (una fila para convertir 157)
  
[PASO 2] Generar estructura LaTeX
  - Tabla: 6 columnas (Etiqueta, Decimal, Binario, C2, SM, BCD)
  - Filas: 1 fila vacia
  - Bordes: \\hline entre filas (estructura LaTeX estandar)
  - Compilable: SI (tabla valida pero vacia)

[PASO 3] Agregar metadata al JSON
  - table_type: numeracion_conversion
  - num_rows: 1
  - num_cols: 6
  - structure_defined: True
  - is_solution: False (para enunciado)
""")

# TEX Output de Fase 2
fase2_latex = r"""
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
"""

print("\n[TEX OUTPUT] Salida de Fase 2 (compilable):")
print(fase2_latex)

# ============================================================================
# OUTPUT: JSON para siguiente fase
# ============================================================================

print("[JSON OUTPUT] Metadata agregada para Fase 3:")
print("""
{
  'phase2_structure': {
    'status': 'generated',
    'table_type': 'numeracion_conversion',
    'num_rows': 1,
    'num_cols': 6,
    'columns': ['Etiqueta', 'Decimal', 'Binario', 'C2', 'SM', 'BCD'],
    'structure_defined': True,
    'is_solution': False
  }
}

Nota: Todo el JSON anterior (phase1_validation, problem, solution, etc)
se pasa intacto a Fase 3 junto con esta nueva metadata.
""")

# ============================================================================
# Pipeline End-to-End
# ============================================================================

print("\n" + "=" * 80)
print("FLUJO COMPLETO DEL PIPELINE")
print("=" * 80)

print("""
Input: ejercicio.json (raw, no validado)
  |
  v
FASE 1: Phase1DataValidator.render()
  |- Validar estructura
  |- Validar campos requeridos
  |- Validar tipos de datos
  |- Output:
  |  |- 00_fase1_validacion.tex (documentacion)
  |  |- JSON + phase1_validation metadata
  |
  v
FASE 2: Phase2StructureGenerator.render()  <-- ACTUAL
  |- Determinar num_rows (1 para ConversionRow)
  |- Generar tabla vacia pero dimensionada
  |- Output:
  |  |- 02_fase2_estructura.tex (tabla compilable)
  |  |- JSON + phase2_structure metadata
  |
  v
FASE 3: Phase3Details.render() [PROXIMO]
  |- Agregar colores (problema=gris, solucion=verde)
  |- Agregar estilos visuales
  |- Output:
  |  |- 03_fase3_detalles.tex (tabla con estilos)
  |  |- JSON + phase3_details metadata
  |
  v
FASE 4: Phase4Content.render()
  |- Agregar valores del problema
  |- Output:
  |  |- 04_fase4_contenido.tex (tabla con datos)
  |  |- JSON + phase4_content metadata
  |
  v
FASE 5: Phase5Text.render()
  |- Agregar enunciados y explicaciones
  |- Output:
  |  |- 05_fase5_texto.tex (TEX FINAL)
  |  |- JSON: None (ultima fase)
  |
  v
RendererPipeline.save_main_file()
  |- main.tex con \\include{00_fase1...}
  |               \\include{02_fase2...}
  |               \\include{03_fase3...}
  |               \\include{04_fase4...}
  |               \\include{05_fase5...}
  |
  v
[PDF OUTPUT]
""")

# ============================================================================
# Manejo de Errores
# ============================================================================

print("\n" + "=" * 80)
print("MANEJO DE ERRORES EN FASE 2")
print("=" * 80)

print("""
[ERROR 1] JSON no tiene phase1_validation
  Razon: JSON no fue procesado por Fase 1
  Solucion: Pasar JSON a traves de Fase 1 primero
  
[ERROR 2] exercise_type no reconocido
  Razon: Tipo de ejercicio no mapeado en _determine_num_rows
  Solucion: Usar 1 fila por defecto, emitir warning

[ERROR 3] Fase 1 encontro validacion fallida
  Razon: JSON tiene errores de validacion
  Solucion: Pipeline no continua (detiene en Fase 1)
""")

# ============================================================================
# Características clave
# ============================================================================

print("\n" + "=" * 80)
print("CARACTERISTICAS CLAVE DE FASE 2")
print("=" * 80)

print("""
[HACE]
  - Define marcos y estructura de tabla
  - Determina dimensiones basadas en tipo ejercicio
  - Genera codigo LaTeX compilable
  - Pasa JSON sin cambios (solo agrega metadata)

[NO HACE]
  - Agregar contenido/valores (eso es Fase 4)
  - Agregar colores/estilos (eso es Fase 3)
  - Validar JSON (eso fue Fase 1)
  - Generar enunciados (eso es Fase 5)

[PROPIEDADES]
  - Determinista: Mismo JSON = Mismo TEX
  - Agnóstico: Funciona para enunciado y solucion
  - Composable: TEX compilable + JSON para siguiente
  - Independiente: No depende de contenido, solo estructura
""")

# ============================================================================
# Ejemplo de uso en código
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO: INTEGRACION EN CODIGO")
print("=" * 80)

print("""
# 1. Importar fases
from renderers.latex.phase1_validator import Phase1DataValidator
from renderers.latex.phase2_structure import Phase2StructureGenerator
from renderers.latex.renderer_base import RendererPipeline

# 2. Crear pipeline
pipeline = RendererPipeline()
pipeline.add_phase(Phase1DataValidator())
pipeline.add_phase(Phase2StructureGenerator())
# ... agregar Fase 3, 4, 5 ...

# 3. Renderizar (Fase 1 -> Fase 2 -> ...)
output = pipeline.render(ejercicio_json, is_solution=False)

# 4. Resultado accesible
phase2_output = output.phases[1]  # Phase2StructureGenerator result
print(phase2_output.latex_content)  # TEX de estructura
print(phase2_output.output_json['phase2_structure'])  # Metadata

# 5. Guardar todo
pipeline.save_main_file('build/latex/main.tex')
# Resultado:
#   build/latex/00_fase1_validacion.tex
#   build/latex/02_fase2_estructura.tex
#   build/latex/main.tex  <- Incluye ambas
""")

print("\n" + "=" * 80)
print("PROXIMOS PASOS")
print("=" * 80)

print("""
IMPLEMENTACION SIGUIENTE:

Fase 3 - Phase3Details:
  - Agregar colores
  - Agregar alineacion
  - Agregar padding
  - Mantener tabla vacia (sin valores)
  
Fase 4 - Phase4Content:
  - Agregar valores del problema (columna problema)
  - Agregar valores de solucion (columna solucion)
  
Fase 5 - Phase5Text:
  - Agregar enunciados
  - Agregar explicaciones
  - Agregar pasos de resolucion

Status actual: Phase1DataValidator [OK]
               Phase2StructureGenerator [OK]
               Phase3Details [PROXIMO]
""")

print("\n" + "=" * 80)
print("FIN DE DEMOSTRACION")
print("=" * 80)

print("=" * 80)
print("FASE 2: STRUCTURE GENERATOR - Demo Completo")
print("=" * 80)

# JSON validado que sale de Fase 1
ejercicio_json = {
    'title': 'Conversión Decimal a Múltiples Bases',
    'description': 'Convierte 157 a binario, C2, SM y BCD',
    'metadata': {
        'exercise_type': 'ConversionRow',
        'module': 'modules.numeracion.models',
        'seed': 42
    },
    'problem': {
        'label': 'a',
        'val_decimal': 157,
        'target_col_idx': 2,
        'representable': True
    },
    'solution': {
        'sol_bin': '10011101',
        'sol_c2': '10011101',
        'sol_sm': '10011101',
        'sol_bcd': '0001 0101 0111',
        'target_val_str': '10011101'
    },
    # Metadata añadida por Fase 1
    'phase1_validation': {
        'status': 'valid',
        'exercise_type': 'ConversionRow',
        'problem_fields': ['label', 'val_decimal', 'target_col_idx', 'representable'],
        'solution_fields': ['sol_bin', 'sol_c2', 'sol_sm', 'sol_bcd', 'target_val_str'],
        'validated_at': 'phase1'
    }
}

print("\n✓ JSON Validado de Fase 1")
print(f"  - Título: {ejercicio_json['title']}")
print(f"  - Tipo: {ejercicio_json['metadata']['exercise_type']}")
print(f"  - Campos problema: {list(ejercicio_json['problem'].keys())}")
print(f"  - Campos solución: {list(ejercicio_json['solution'].keys())}")

# ============================================================================
# Fase 1 (repaso rápido)
# ============================================================================

print("\n" + "=" * 80)
print("FASE 1: Validación y Metadata Extraction")
print("=" * 80)

print("""
✓ Validación de estructura
  - title: ✓ presente
  - description: ✓ presente
  - problem: ✓ presente
  - solution: ✓ presente
  - metadata: ✓ presente

✓ Validación de campos requeridos (ConversionRow)
  - problem.label: ✓ 'a'
  - problem.val_decimal: ✓ 157
  - problem.target_col_idx: ✓ 2
  - problem.representable: ✓ True
  - solution.sol_bin: ✓ '10011101'
  - solution.sol_c2: ✓ '10011101'
  - solution.sol_sm: ✓ '10011101'
  - solution.sol_bcd: ✓ '0001 0101 0111'
  - solution.target_val_str: ✓ '10011101'

✓ Validación de tipos
  - val_decimal: ✓ int (158)
  - representable: ✓ bool (True)
  - target_col_idx: ✓ int (2)

✓ Salida:
  - output.latex_content: TEX con documentación de validación
  - output.output_json: JSON limpio + phase1_validation metadata
  - output.phase_name: 'validador'
  - output.tex_filename: '00_fase1_validacion.tex'
""")

print("\nJSON sale de Fase 1 con metadata añadida:")
print(f"  phase1_validation: {ejercicio_json.get('phase1_validation', {})}")

# ============================================================================
# Fase 2: Structure Generator
# ============================================================================

print("\n" + "=" * 80)
print("FASE 2: STRUCTURE GENERATOR")
print("=" * 80)

print("""
✓ Análisis de problema
  - exercise_type: 'ConversionRow'
  - num_rows determinado: 1 (una fila para convertir 157)

✓ Generación de estructura LaTeX
  - Tabla: 6 columnas (Etiqueta, Decimal, Binario, C2, SM, BCD)
  - Filas: 1 fila vacía (estructura, sin contenido)
  - Bordes: \\hline entre filas (estructura LaTeX estándar)
  - Compilable: SÍ (tabla válida pero vacía)

✓ Metadata añadida al JSON
  - table_type: 'numeracion_conversion'
  - num_rows: 1
  - num_cols: 6
  - structure_defined: True
""")

# Simulación de salida de Fase 2
fase2_latex = r"""
% ========================================
% FASE 2: ESTRUCTURA - marcos y dimensiones de tabla
% Tipo: ENUNCIADO
% ========================================

% Tabla de conversión de bases numéricas
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
% ✓ Correctamente dimensionada (filas y columnas)
% ✓ Estructurada con bordes y encabezados
% ✓ Compilable como TEX
% ✗ Sin contenido (se agrega en Fase 3+)
% ✗ Sin estilos visuales (colores, padding, etc)
% ========================================
"""

print("\n? TEX Output de Fase 2 (compilable):")
print(fase2_latex)

# JSON actualizado después de Fase 2
fase2_json = {
    **ejercicio_json,
    'phase2_structure': {
        'status': 'generated',
        'table_type': 'numeracion_conversion',
        'num_rows': 1,
        'num_cols': 6,
        'columns': ['Etiqueta', 'Decimal', 'Binario', 'C2', 'SM', 'BCD'],
        'structure_defined': True,
        'is_solution': False
    }
}

print("\n? JSON Output de Fase 2 (para Fase 3):")
print("""
{
  'title': '...',
  'metadata': {...},
  'problem': {...},
  'solution': {...},
  'phase1_validation': {...},
  'phase2_structure': {
    'status': 'generated',
    'table_type': 'numeracion_conversion',
    'num_rows': 1,
    'num_cols': 6,
    'columns': ['Etiqueta', 'Decimal', 'Binario', 'C2', 'SM', 'BCD'],
    'structure_defined': True,
    'is_solution': False
  }
}
""")

# ============================================================================
# Pipeline: Fase 1 → Fase 2
# ============================================================================

print("\n" + "=" * 80)
print("FLUJO COMPLETO: FASE 1 → FASE 2")
print("=" * 80)

print("""
Input: ejercicio.json (raw, no validado)

    ↓

FASE 1: Phase1DataValidator.render()
  ├─ Validar estructura
  ├─ Validar campos requeridos
  ├─ Validar tipos
  ├─ Output:
  │  ├─ 00_fase1_validacion.tex (documentación)
  │  └─ JSON + phase1_validation metadata
  
    ↓

FASE 2: Phase2StructureGenerator.render()
  ├─ Determinar num_rows (1 para ConversionRow)
  ├─ Generar tabla vacía pero dimensionada
  ├─ Output:
  │  ├─ 02_fase2_estructura.tex (tabla compilable)
  │  └─ JSON + phase2_structure metadata
  
    ↓

Ready para FASE 3: Detalles Visuales (colores, estilos)
  - Entrada: JSON con phase1_validation + phase2_structure
  - Salida: TEX con estilos + JSON para siguiente
  
    ↓
    
Ready para FASE 4: Contenido (números, valores)
  - Entrada: JSON + TEX con estructura y estilos
  - Salida: TEX con valores del problema
  
    ↓
    
Ready para FASE 5: Enunciados (texto, explicaciones)
  - Entrada: Completamente estructurado
  - Salida: TEX final compilable + PDF
""")

# ============================================================================
# Casos de Error
# ============================================================================

print("\n" + "=" * 80)
print("MANEJO DE ERRORES EN FASE 2")
print("=" * 80)

print("""
❌ CASO 1: JSON no validado (falta phase1_validation)
   → Fase 2 debería rechazarlo con error claro
   → "JSON debe ser validado por Fase 1 primero"

❌ CASO 2: exercise_type desconocido
   → Fase 2 usa 1 fila por defecto
   → Emite warning: "exercise_type desconocido"

❌ CASO 3: Fase 1 encontró errores
   → Fase 2 nunca recibe el JSON (pipeline detiene)
   → Error reportado en Fase 1, no continúa
""")

# ============================================================================
# Características de Fase 2
# ============================================================================

print("\n" + "=" * 80)
print("CARACTERÍSTICAS DE FASE 2: STRUCTURE GENERATOR")
print("=" * 80)

print("""
✓ RESPONSABILIDADES CLARAS
  - Define marcos y estructura de tabla
  - Determina dimensiones basadas en tipo de ejercicio
  - Genera código LaTeX compilable

✗ NO HACE:
  - Agregar contenido/valores (eso es Fase 3+)
  - Agregar colores/estilos (eso es Fase 3)
  - Validar JSON (eso es Fase 1)

✓ DETERMINISTA
  - Mismo JSON → Mismo TEX output
  - Reproducible
  - No usa randomización

✓ AGNÓSTICO DE SOLUCIÓN
  - Tabla vacía tanto para enunciado como para solución
  - Estructura idéntica
  - Solo cambia dimensiones basadas en problema

✓ COMPOSABLE
  - Output TEX compilable
  - Output JSON para siguiente fase
  - Encadena perfectamente con Fase 1 y Fase 3
""")

# ============================================================================
# Ejemplo de uso en código
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO: USO EN CÓDIGO")
print("=" * 80)

print("""
from renderers.latex.phase1_validator import Phase1DataValidator
from renderers.latex.phase2_structure import Phase2StructureGenerator
from renderers.latex.renderer_base import RendererPipeline

# Crear pipeline
pipeline = RendererPipeline()
pipeline.add_phase(Phase1DataValidator())
pipeline.add_phase(Phase2StructureGenerator())

# Renderizar (Fase 1 → Fase 2)
output = pipeline.render(ejercicio_json, is_solution=False)

# Resultado:
# - output.phases[0].latex_content: TEX de validación (Fase 1)
# - output.phases[1].latex_content: TEX de estructura (Fase 2)
# - output.phases[1].output_json: JSON con metadatas de Fase1 + Fase2

# Guardar
pipeline.save_main_file('build/latex/main.tex')
# Genera: main.tex con \\include{00_fase1_validacion.tex}
#                        \\include{02_fase2_estructura.tex}
""")

print("\n" + "=" * 80)
print("PRÓXIMO PASO: FASE 3 - Detalles Visuales")
print("=" * 80)

print("""
Fase 3 agregará:
  - Colores: problema (gris) vs solución (verde)
  - Alineación: centrado vertical
  - Padding: espaciado de celdas
  - Fuentes: monoespaciada para alineación

Input: JSON + TEX de Fase 2
Output: TEX con estilos + JSON con phase3_details metadata
""")
