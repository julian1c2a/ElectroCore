# -*- coding: utf-8 -*-
"""
FASE 3: DETAILS - Demostracion completa

Muestra cómo fluye JSON a través del pipeline:
  JSON + Fase2 (Fase1DataValidator + Phase2StructureGenerator)
                        |
                Phase3Details.render()
                        |
        JSON + Fase3Details metadata + TEX estilizado
"""

import sys
if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 80)
print("FASE 3: DETAILS - Agregador de Estilos Visuales")
print("=" * 80)

# ============================================================================
# ENTRADA: JSON que viene de Fase 2
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
    },
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

print("\n[ENTRADA A FASE 3]")
print("  Metadata de Fase 1: PRESENTE (validación OK)")
print("  Metadata de Fase 2: PRESENTE (estructura OK)")
print("  num_rows: 1")
print("  num_cols: 6")
print("  is_solution: False (para enunciado)")

# ============================================================================
# FASE 3: Details
# ============================================================================

print("\n" + "=" * 80)
print("FASE 3: PROCESAMIENTO")
print("=" * 80)

print("""
[PASO 1] Extraer metadata de Fase 2
  - num_rows: 1
  - num_cols: 6
  - columns: ['Etiqueta', 'Decimal', 'Binario', 'C2', 'SM', 'BCD']

[PASO 2] Determinar color de celdas
  - is_solution: False -> PROBLEMA
  - Color RGB: 240,240,240 (gris muy claro)

[PASO 3] Definir estilos
  - Encabezado: color 230,230,230 (gris medio) + texto bold
  - Padding: 0.3em (espaciado dentro de celda)
  - Row height: 0.8em (altura minima de fila)
  - Fuente: monoespaciada (texttt) para alineacion correcta

[PASO 4] Generar LaTeX estilizado
  - usepackage xcolor para definir colores
  - definecolor: problema, solucion, encabezado
  - cellcolor para cada celda
  - texttt para fuente monoespaciada
  - Tabla compilable pero aun VACIA

[PASO 5] Agregar metadata de Fase 3
  - status: 'styled'
  - problema_color: RGB value
  - encabezado_color: RGB value
  - styles_applied: True
  - is_solution: False
""")

# ============================================================================
# TEX Output de Fase 3
# ============================================================================

fase3_latex = r"""
% ========================================
% FASE 3: DETALLES - Estilos visuales
% Tipo: ENUNCIADO
% ========================================

% Definición de colores (en RGB)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

% Tabla de conversión con estilos
% Estructura: 6 columnas x 1 filas
% Estilos: Colores, padding, alineación, fuente monoespaciada

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
\cellcolor{problema} \texttt{\cellpadding} & 
\cellcolor{problema} \texttt{\cellpadding} & 
\cellcolor{problema} \texttt{\cellpadding} & 
\cellcolor{problema} \texttt{\cellpadding} & 
\cellcolor{problema} \texttt{\cellpadding} & 
\cellcolor{problema} \texttt{\cellpadding} \\
\hline
\end{tabular}

% ========================================
% Salida de FASE 3
% ---
% Esta tabla está:
% [OK] Correctamente dimensionada (filas y columnas)
% [OK] Estructurada con bordes y encabezados
% [OK] Estilizada: colores, alineación, padding
% [OK] Compilable como TEX
% [NO] Sin contenido (se agrega en Fase 4)
% ========================================

% Notas de estilos aplicados:
% - Encabezados: fondo gris medio (230,230,230)
% - Celdas: fondo gris (240,240,240)
% - Padding: 0.3em
% - Altura mínima: 0.8em
% - Fuente: monoespaciada (\texttt) para alineación
% - Alineación: centrada (c) en todas las columnas
"""

print("\n[TEX OUTPUT] Salida de Fase 3 (compilable con colores):")
print(fase3_latex)

# ============================================================================
# JSON Output de Fase 3
# ============================================================================

print("[JSON OUTPUT] Metadata agregada para Fase 4:")
print("""
{
  'phase3_details': {
    'status': 'styled',
    'problema_color': '240,240,240',
    'solucion_color': None,
    'encabezado_color': '230,230,230',
    'cell_padding': '0.3em',
    'row_height': '0.8em',
    'font': 'ttfamily',
    'styles_applied': True,
    'is_solution': False
  }
}

Nota: Todo el JSON anterior (phase1_validation, phase2_structure, problem, solution, etc)
se pasa intacto a Fase 4 junto con esta nueva metadata de estilos.
""")

# ============================================================================
# Comparación: Fase 2 vs Fase 3
# ============================================================================

print("\n" + "=" * 80)
print("COMPARACION: FASE 2 vs FASE 3")
print("=" * 80)

print(r"""
FASE 2 (ESTRUCTURA):
  Tabla: estructura basica sin estilos
  \begin{tabular}{|c|c|c|c|c|c|}
  \hline
  Etiqueta & Decimal & Binario & ... \\
  \hline
   &  &  & ... \\
  \hline
  \end{tabular}
  
  Compilado: Tabla blanca, bordes basicos

FASE 3 (DETALLES):
  Tabla: estructura con estilos visuales
  \definecolor{problema}{RGB}{240,240,240}
  \usepackage{xcolor}
  
  \begin{tabular}{|c|c|c|c|c|c|}
  \hline
  \textbf{\cellcolor{encabezado} Etiqueta} & ... \\
  \hline
  \cellcolor{problema} \texttt{\cellpadding} & ... \\
  \hline
  \end{tabular}
  
  Compilado: Tabla con colores, encabezados negros, celdas grises

DIFERENCIAS:
  Fase 2: BLANCA        -> Fase 3: COLOREADA
  Fase 2: SIN PADDING   -> Fase 3: CON PADDING (0.3em)
  Fase 2: TEXTO NORMAL  -> Fase 3: TEXTO MONOESPACIADO
  Fase 2: ENCABEZADOS NORMALES  -> Fase 3: ENCABEZADOS NEGROS Y FONDO

SIMILITUDES:
  Ambas: TABLA VACIA (sin valores)
  Ambas: COMPILABLES
  Ambas: MISMA ESTRUCTURA (num_rows, num_cols)
""")

# ============================================================================
# Flujo ENUNCIADO vs SOLUCION
# ============================================================================

print("\n" + "=" * 80)
print("FLUJO: ENUNCIADO vs SOLUCION")
print("=" * 80)

print("""
ENUNCIADO (is_solution=False):
  Fase 3 produce:
    - Encabezados: fondo gris medio + texto bold
    - Celdas: fondo GRIS (240,240,240) -> problema
    - Padding: 0.3em
    - Resultado: tabla con celdas grises para rellenar
    
SOLUCION (is_solution=True):
  Fase 3 produce:
    - Encabezados: fondo gris medio + texto bold
    - Celdas: fondo VERDE (200,255,200) -> solucion
    - Padding: 0.3em
    - Resultado: tabla con celdas verdes para mostrar

TEXTURA:
  - Encabezado siempre: gris medio + bold
  - Filas de problema: gris claro
  - Filas de solucion: verde claro
""")

# ============================================================================
# Pipeline completo hasta Fase 3
# ============================================================================

print("\n" + "=" * 80)
print("PIPELINE COMPLETO: FASE 1 + FASE 2 + FASE 3")
print("=" * 80)

print(r"""
Input: ejercicio.json (raw, no validado)
  |
  v
FASE 1: Validacion [OK]
  ├─ 00_fase1_validacion.tex
  ├─ JSON + phase1_validation metadata
  |
  v
FASE 2: Estructura [OK]
  ├─ 02_fase2_estructura.tex
  ├─ JSON + phase2_structure metadata
  |
  v
FASE 3: Detalles [OK]  <-- ACTUAL
  ├─ 03_fase3_detalles.tex (TABLA CON COLORES)
  ├─ JSON + phase3_details metadata
  |
  v
FASE 4: Contenido [PROXIMO]
  ├─ 04_fase4_contenido.tex (TABLA CON VALORES)
  ├─ JSON + phase4_content metadata
  |
  v
FASE 5: Enunciados
  ├─ 05_fase5_texto.tex (TEX FINAL)
  ├─ JSON: None (ultima fase)
  |
  v
main.tex (composicion con \include)
  |
  v
PDF OUTPUT
""")

# ============================================================================
# Características de Fase 3
# ============================================================================

print("\n" + "=" * 80)
print("CARACTERISTICAS DE FASE 3: DETAILS")
print("=" * 80)

print("""
[HACE]
  - Define colores (problema vs solucion)
  - Agrega padding y espaciado
  - Define altura minima de filas
  - Mejora encabezados (bold + color)
  - Usa fuente monoespaciada para alineacion

[NO HACE]
  - Agregar contenido/valores (eso es Fase 4)
  - Validar JSON (eso fue Fase 1)
  - Cambiar estructura (eso fue Fase 2)
  - Generar enunciados (eso es Fase 5)

[PROPIEDADES]
  - Determinista: Mismo JSON = Mismo TEX
  - Agnóstico: Funciona para enunciado y solucion
  - Compilable: TEX compilable con colores
  - Composable: JSON + TEX para siguiente
  - Incrementalista: Mejora Fase 2 sin destruir
""")

# ============================================================================
# Uso en código
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO: INTEGRACION EN CODIGO")
print("=" * 80)

print(r"""
from renderers.latex.phase1_validator import Phase1DataValidator
from renderers.latex.phase2_structure import Phase2StructureGenerator
from renderers.latex.phase3_details import Phase3Details
from renderers.latex.renderer_base import RendererPipeline

# Crear pipeline
pipeline = RendererPipeline()
pipeline.add_phase(Phase1DataValidator())
pipeline.add_phase(Phase2StructureGenerator())
pipeline.add_phase(Phase3Details())  # NUEVA

# Renderizar (Fase 1 -> Fase 2 -> Fase 3)
output = pipeline.render(ejercicio_json, is_solution=False)

# Acceder a resultados
fase3_output = output.phases[2]  # Phase3Details result
print(fase3_output.latex_content)  # TEX con colores
print(fase3_output.output_json['phase3_details'])  # Metadata

# Guardar todo
pipeline.save_main_file('build/latex/main.tex')
# Resultado:
#   build/latex/00_fase1_validacion.tex
#   build/latex/02_fase2_estructura.tex
#   build/latex/03_fase3_detalles.tex  <- CON COLORES
#   build/latex/main.tex  <- Incluye las tres
""")

print("\n" + "=" * 80)
print("PROXIMOS PASOS")
print("=" * 80)

print("""
FASE 4: Phase4Content
  Input: JSON + Fase3 TEX (tabla estilizada)
  Output: TEX con valores del problema
  Agrega: Numeros, conversiones, representaciones
  Ejemplo: Fila 1: [a] [157] [10011101] [10011101] [10011101] [0001...]
  
FASE 5: Phase5Text
  Input: JSON + Fase4 TEX (tabla llena)
  Output: TEX FINAL con explicaciones
  Agrega: Enunciados, pasos, notas, conclusiones

Status actual: Phase1DataValidator [OK]
               Phase2StructureGenerator [OK]
               Phase3Details [OK]
               Phase4Content [PROXIMO]
               Phase5Text [DESPUES]
""")

print("\n" + "=" * 80)
print("FIN DE DEMOSTRACION - FASE 3 LISTA")
print("=" * 80)
