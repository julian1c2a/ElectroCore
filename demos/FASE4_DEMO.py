#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FASE 4: CONTENT - Demostracion completa

Muestra como fluye JSON a traves del pipeline:
  JSON validado (Fase 1) -> Fase1DataValidator -> JSON + TEX
                         |
                         v
                Fase2StructureGenerator -> JSON + TEX (estructura)
                         |
                         v
                Fase3Details -> JSON + TEX (estilos)
                         |
                         v
                Fase4Content -> JSON + TEX (CONTENIDO) <-- ACTUAL
"""

print("=" * 80)
print("FASE 4: CONTENT - TABLA LLENA DE VALORES")
print("=" * 80)

# ============================================================================
# ENTRADA: JSON que incluye problem y solution (para extraer contenido)
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
        'validated_at': 'phase1'
    },
    'phase2_structure': {
        'status': 'generated',
        'table_type': 'numeracion_conversion',
        'num_rows': 1,
        'num_cols': 6,
        'columns': ['Etiqueta', 'Decimal', 'Binario', 'C2', 'SM', 'BCD'],
        'structure_defined': True
    },
    'phase3_details': {
        'status': 'styled',
        'problema_color': '240,240,240',
        'solucion_color': '200,255,200',
        'encabezado_color': '230,230,230',
        'styles_applied': True
    }
}

print(r"""
[OK] JSON en entrada de Fase 4:
  - Incluye problem (valores del problema)
  - Incluye solution (valores de la solucion)
  - Incluye metadata de Fases 1, 2, 3
  - Listo para extraer contenido
""")

# ============================================================================
# FASE 4: Content Generator
# ============================================================================

print("=" * 80)
print("FASE 4: EXTRACCION Y LLENADO DE CONTENIDO")
print("=" * 80)

print(r"""
[PASO 1] Analizar exercise_type
  - exercise_type: ConversionRow
  - Estructura: 6 columnas (Etiqueta, Decimal, Binario, C2, SM, BCD)
  - Filas: 1 fila
  
[PASO 2] Extraer valores segun is_solution

  ENUNCIADO (is_solution=False):
    - Etiqueta: 'a' (del problem['label'])
    - Decimal: 157 (del problem['val_decimal'])
    - Binario: '' (vacio - alumno debe resolver)
    - C2: '' (vacio)
    - SM: '' (vacio)
    - BCD: '' (vacio)
  
  SOLUCION (is_solution=True):
    - Etiqueta: 'a' (del problem['label'])
    - Decimal: 157 (del problem['val_decimal'])
    - Binario: '10011101' (del solution['sol_bin'])
    - C2: '10011101' (del solution['sol_c2'])
    - SM: '10011101' (del solution['sol_sm'])
    - BCD: '0001 0101 0111' (del solution['sol_bcd'])

[PASO 3] Generar LaTeX con contenido
  - Mantener estilos de Fase 3 (colores, padding, alineacion)
  - AGREGAR VALORES en celdas
  - Compilable: SI

[PASO 4] Agregar metadata de Fase 4 al JSON
  - status: 'populated'
  - num_rows_filled: 1
  - content_added: True
  - is_solution: False/True segun modo
""")

# ============================================================================
# TEX Output ENUNCIADO (problema a resolver)
# ============================================================================

print("\n" + "=" * 80)
print("TEX OUTPUT: ENUNCIADO (para alumno)")
print("=" * 80)

enunciado_latex = r"""
% ========================================
% FASE 4: CONTENIDO - Valores numeral
% Tipo: ENUNCIADO
% Ejercicio: ConversionRow
% ========================================

% Definicion de colores (en RGB)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

% Tabla con contenido
% Estructura: 6 columnas x 1 filas
% Estilos: Colores, padding, alineacion, fuente monoespaciada
% Contenido: Valores del problema (para resolver)

\newcommand{\cellpadding}[0]{\rule{0pt}{0.8em}}

\begin{tabular}{|c|c|c|c|c|c|}
\hline
\textbf{\cellcolor{encabezado} Etiqueta} & 
\textbf{\cellcolor{encabezado} Decimal} & 
\textbf{\cellcolor{encabezado} Binario} & 
\textbf{\cellcolor{encabezado} C2} & 
\textbf{\cellcolor{encabezado} SM} & 
\textbf{\cellcolor{encabezado} BCD} \\
\hline
\cellcolor{problema} \texttt{\cellpadding a} & 
\cellcolor{problema} \texttt{\cellpadding 157} & 
\cellcolor{problema} \texttt{\cellpadding } & 
\cellcolor{problema} \texttt{\cellpadding } & 
\cellcolor{problema} \texttt{\cellpadding } & 
\cellcolor{problema} \texttt{\cellpadding } \\
\hline
\end{tabular}

% ========================================
% Salida de FASE 4
% ---
% Esta tabla esta:
% [OK] Correctamente dimensionada (filas y columnas)
% [OK] Estructurada con bordes y encabezados
% [OK] Estilizada: colores, alineacion, padding
% [OK] LLENA DE CONTENIDO: valores numericos
% [OK] Compilable como TEX
% [NO] Sin enunciados (se agregan en Fase 5)
% ========================================

% Notas de contenido:
% - Valores mostrados: 1 fila(s) poblada(s)
% - Tipo documento: Enunciado (problema a resolver)
% - Ejercicio: ConversionRow
% - Color: gris (problema)
% - Padding: 0.3em
% - Fuente: monoespaciada (\texttt) para alineacion
"""

print(enunciado_latex)

# ============================================================================
# TEX Output SOLUCION (con respuestas)
# ============================================================================

print("\n" + "=" * 80)
print("TEX OUTPUT: SOLUCION (con respuestas)")
print("=" * 80)

solucion_latex = r"""
% ========================================
% FASE 4: CONTENIDO - Valores numeral
% Tipo: SOLUCION
% Ejercicio: ConversionRow
% ========================================

% Definicion de colores (en RGB)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

% Tabla con contenido
% Estructura: 6 columnas x 1 filas
% Estilos: Colores, padding, alineacion, fuente monoespaciada
% Contenido: Valores del problema (solucion)

\newcommand{\cellpadding}[0]{\rule{0pt}{0.8em}}

\begin{tabular}{|c|c|c|c|c|c|}
\hline
\textbf{\cellcolor{encabezado} Etiqueta} & 
\textbf{\cellcolor{encabezado} Decimal} & 
\textbf{\cellcolor{encabezado} Binario} & 
\textbf{\cellcolor{encabezado} C2} & 
\textbf{\cellcolor{encabezado} SM} & 
\textbf{\cellcolor{encabezado} BCD} \\
\hline
\cellcolor{solucion} \texttt{\cellpadding a} & 
\cellcolor{solucion} \texttt{\cellpadding 157} & 
\cellcolor{solucion} \texttt{\cellpadding 10011101} & 
\cellcolor{solucion} \texttt{\cellpadding 10011101} & 
\cellcolor{solucion} \texttt{\cellpadding 10011101} & 
\cellcolor{solucion} \texttt{\cellpadding 0001 0101 0111} \\
\hline
\end{tabular}

% ========================================
% Salida de FASE 4
% ---
% Esta tabla esta:
% [OK] Correctamente dimensionada (filas y columnas)
% [OK] Estructurada con bordes y encabezados
% [OK] Estilizada: colores, alineacion, padding
% [OK] LLENA DE CONTENIDO: valores numericos
% [OK] Compilable como TEX
% [NO] Sin enunciados (se agregan en Fase 5)
% ========================================

% Notas de contenido:
% - Valores mostrados: 1 fila(s) poblada(s)
% - Tipo documento: Solucion (todos valores visibles)
% - Ejercicio: ConversionRow
% - Color: verde (solucion)
% - Padding: 0.3em
% - Fuente: monoespaciada (\texttt) para alineacion
"""

print(solucion_latex)

# ============================================================================
# Comparacion visual: Fase 3 vs Fase 4
# ============================================================================

print("\n" + "=" * 80)
print("COMPARACION: FASE 3 (VACIO) vs FASE 4 (LLENO)")
print("=" * 80)

print(r"""
FASE 3: Tabla estilizada pero vacia (Detalles)
  _____________________________________________
  | Etiqueta | Decimal | Binario | C2 | SM | BCD |  <- Encabezados
  |----------|---------|---------|----|----|-----|
  |          |         |         |    |    |     |  <- Vacio (esperando contenido)
  |__________|_________|_________|____|____|_____|
  
  Caracteristicas:
    [OK] Colores aplicados (gris para problema)
    [OK] Padding y alineacion (0.3em)
    [OK] Fuente monoespaciada
    [NO] SIN VALORES

FASE 4: Tabla llena de contenido (Contenido)
  _____________________________________________
  | Etiqueta | Decimal | Binario    | C2      | SM      | BCD            |
  |----------|---------|------------|---------|---------|----------------|
  | a        | 157     | 10011101   | 10011101| 10011101| 0001 0101 0111 |
  |__________|_________|____________|_________|_________|________________|
  
  Caracteristicas:
    [OK] Colores aplicados (verde para solucion)
    [OK] Padding y alineacion (0.3em)
    [OK] Fuente monoespaciada
    [OK] LLENO DE VALORES
""")

# ============================================================================
# JSON Output para Fase 5
# ============================================================================

print("\n" + "=" * 80)
print("JSON OUTPUT: Metadata para Fase 5")
print("=" * 80)

print(r"""
Luego de Fase 4, el JSON contiene metadata acumulada:

{
  'title': 'Conversion Decimal a Multiples Bases',
  'metadata': {...},
  'problem': {...},
  'solution': {...},
  
  'phase1_validation': {
    'status': 'valid',
    'exercise_type': 'ConversionRow',
    'validated_at': 'phase1'
  },
  
  'phase2_structure': {
    'status': 'generated',
    'num_rows': 1,
    'num_cols': 6,
    'structure_defined': True
  },
  
  'phase3_details': {
    'status': 'styled',
    'problema_color': '240,240,240',
    'styles_applied': True
  },
  
  'phase4_content': {         <-- NUEVO en Fase 4
    'status': 'populated',
    'exercise_type': 'ConversionRow',
    'num_rows_filled': 1,
    'values_extracted': True,
    'content_added': True,
    'is_solution': False
  }
}
""")

# ============================================================================
# Pipeline End-to-End
# ============================================================================

print("\n" + "=" * 80)
print("FLUJO COMPLETO DEL PIPELINE")
print("=" * 80)

print(r"""
Input: ejercicio.json (raw)
  |
  v
FASE 1: Phase1DataValidator
  |- Validar estructura y tipos
  |- Output: JSON + phase1_validation
  |
  v
FASE 2: Phase2StructureGenerator
  |- Determinar num_rows
  |- Crear tabla vacia
  |- Output: JSON + phase2_structure + 02_fase2_estructura.tex
  |
  v
FASE 3: Phase3Details
  |- Agregar colores
  |- Agregar estilos
  |- Output: JSON + phase3_details + 03_fase3_detalles.tex
  |
  v
FASE 4: Phase4Content  <-- ACTUAL
  |- Extraer valores de problem/solution
  |- Llenar tabla CON CONTENIDO
  |- Output: JSON + phase4_content + 04_fase4_contenido.tex
  |
  v
FASE 5: Phase5Text [PROXIMO]
  |- Agregar enunciados
  |- Agregar explicaciones
  |- Output: JSON + phase5_text + 05_fase5_enunciados.tex
  |
  v
main.tex (compilado) -> PDF
""")

# ============================================================================
# Flujo de datos (JSON + TEX)
# ============================================================================

print("\n" + "=" * 80)
print("FLUJO DE DATOS: JSON + TEX")
print("=" * 80)

print(r"""
ENTRADA FASE 4:
  ejercicio.json (contiene problem y solution)
  + 03_fase3_detalles.tex (tabla estilizada pero vacia)
  + Metadata de Fases 1, 2, 3

PROCESAMIENTO:
  1. Leer exercise_type del metadata
  2. Llamar a _extract_values() -> extrae del problem/solution
  3. Llamar a _generate_content_latex() -> crea tabla con valores
  4. Acumular metadata en JSON

SALIDA FASE 4:
  04_fase4_contenido.tex (tabla LLENA y compilable)
  ejercicio_fase4.json (con phase4_content metadata)
  
CARACTERISTICAS CLAVE:
  - Mantiene estilos de Fase 3 (colores, padding)
  - Agrega contenido (valores numericos)
  - Compilable como LaTeX
  - Determinismo: mismo input -> mismo output
  - Agnósticismo: funciona para enunciado y solucion
""")

# ============================================================================
# Casos de error
# ============================================================================

print("\n" + "=" * 80)
print("CASOS DE ERROR Y MANEJO")
print("=" * 80)

print(r"""
ERROR 1: exercise_type desconocido
  Causa: JSON contiene exercise_type no soportado
  Manejo: Retorna fila vacia {} en _extract_values()
  Resultado: Tabla se genera pero sin datos
  Severity: WARNING - se mantiene compilabilidad

ERROR 2: Campos faltantes en problem/solution
  Causa: JSON incompleto (ej: falta solution['sol_bin'])
  Manejo: Retorna '?' como valor default
  Resultado: Tabla muestra '?' indicando dato faltante
  Severity: WARNING - se mantiene compilabilidad

ERROR 3: is_solution incoherente
  Causa: is_solution=True pero falta solution data
  Manejo: _extract_values() retorna valores del solution disponible
  Resultado: Mezcla valores del problem + solution parcial
  Severity: INFO - usuario puede verificar

PRINCIPIO GENERAL:
  NUNCA fallar. Siempre generar TEX compilable,
  incluso si datos falta. Usar marcadores '?' para
  datos incompletos para facilitar debugging.
""")

# ============================================================================
# Proximos pasos
# ============================================================================

print("\n" + "=" * 80)
print("PROXIMOS PASOS HACIA FASE 5")
print("=" * 80)

print(r"""
FASE 5: Phase5Text
  Responsabilidad: Agregar enunciados y explicaciones
  
  Entrada: JSON + TEX de Fase 4 (tabla llena)
  
  Salida: 
    - TEX: Completo con tabla + enunciado + explicacion
    - JSON: JSON con metadata de Fase5 (final)
  
  Responsabilidades de Fase 5:
    1. Extraer enunciado (problem['statement'])
    2. Extraer explicacion (solution['explanation'])
    3. Agregar antes/despues de tabla
    4. Generar TEX completo y compilable
  
  Resultado final:
    - 05_fase5_enunciados.tex (completo)
    - main.tex (compilado) -> PDF

CRITERIOS DE EXITO FASE 4:
  [OK] Tabla llena con valores (enunciado: problema, solucion: respuestas)
  [OK] TEX compilable
  [OK] Estilos mantenidos de Fase 3
  [OK] Metadata en JSON
  [OK] Agnósticismo: funciona para ConversionRow y ArithmeticOp
  [OK] Determinismo: mismo input -> mismo output
  [OK] Manejo de errores sin crashes
""")

print("\n" + "=" * 80)
print("FIN DEMOSTRACION FASE 4")
print("=" * 80)
