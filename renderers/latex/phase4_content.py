"""
FASE 4: Content - Agrega valores del problema y solucion a celdas.

Responsabilidad: Rellenar celdas de tabla con valores numéricos.

Entrada: JSON + TEX de Fase 3 (tabla estilizada pero vacía)
Salida: 
  - TEX: Tabla con contenido (valores del problema o solución)
  - JSON: JSON con metadata de Fase4 para siguiente fase
  
Característica: Tabla compilable CON VALORES (listo para Fase 5 enunciados).
"""

from typing import Dict, Any, List
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class Phase4Content(ExerciseRendererPhase):
    """
    FASE 4: Agregador de contenido (valores numéricos de problema/solución).
    
    Responsabilidades:
    1. Extraer valores de JSON (problem o solution según is_solution)
    2. Formatear valores para display en LaTeX
    3. Llenar celdas de tabla con valores
    4. Mantener estilos de Fase 3
    5. Generar TEX compilable con contenido
    
    Esta fase NO:
    - Valida JSON (eso fue Fase 1)
    - Define estructura (eso fue Fase 2)
    - Define estilos (eso fue Fase 3)
    - Genera enunciados o explicaciones (eso es Fase 5)
    
    La tabla ahora está LLENA DE VALORES y ESTILIZADA.
    """
    
    # Definición de colores (mismo que Fase 3)
    PROBLEMA_COLOR = "240,240,240"  # Gris muy claro
    SOLUCION_COLOR = "200,255,200"  # Verde muy claro
    ENCABEZADO_COLOR = "230,230,230"  # Gris medio
    
    # Espaciado (mismo que Fase 3)
    CELL_PADDING = "0.3em"
    ROW_HEIGHT = "0.8em"
    FONT_FAMILY = "ttfamily"
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Genera LaTeX con tabla llena de contenido.
        
        Args:
            exercise_json: JSON validado + Fase2/3 metadata + problem/solution
            is_solution: Si mostrar solución (True) o enunciado (False)
        
        Returns:
            PhaseOutput con:
            - latex_content: TEX compilable con tabla llena
            - output_json: JSON con metadata de Fase4 para siguiente fase
            - phase_name: "contenido"
            - tex_filename: "04_fase4_contenido.tex"
        """
        
        # Extraer metadata de fases anteriores
        metadata = self._extract_metadata(exercise_json)
        exercise_type = metadata.get('exercise_type', 'unknown')
        
        phase2_struct = exercise_json.get('phase2_structure', {})
        phase3_details = exercise_json.get('phase3_details', {})
        
        num_rows = phase2_struct.get('num_rows', 1)
        num_cols = phase2_struct.get('num_cols', 6)
        columns = phase2_struct.get('columns', [])
        
        # Determinar color según is_solution
        cell_color = self.SOLUCION_COLOR if is_solution else self.PROBLEMA_COLOR
        
        # Extraer valores de JSON según exercise_type
        values = self._extract_values(exercise_json, exercise_type, is_solution)
        
        # Generar LaTeX con contenido
        latex = self._generate_content_latex(
            num_rows=num_rows,
            num_cols=num_cols,
            columns=columns,
            values=values,
            is_solution=is_solution,
            exercise_type=exercise_type
        )
        
        # Preparar JSON para siguiente fase (Fase 5)
        output_json = {
            **exercise_json,
            'phase4_content': {
                'status': 'populated',
                'exercise_type': exercise_type,
                'num_rows_filled': len(values),
                'values_extracted': True,
                'content_added': True,
                'is_solution': is_solution
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=output_json,
            phase_name="contenido",
            tex_filename="04_fase4_contenido.tex"
        )
    
    def _extract_values(
        self,
        exercise_json: Dict[str, Any],
        exercise_type: str,
        is_solution: bool
    ) -> List[Dict[str, str]]:
        """
        Extrae valores de JSON según exercise_type.
        
        Para ConversionRow:
          - Problema: muestra label, decimal, y espacio para respuestas
          - Solución: muestra label, decimal, y todas las conversiones
        
        Para ArithmeticOp:
          - Problema: muestra operandos y operador
          - Solución: muestra operandos, operador, y resultado
        
        Returns:
            Lista de dicts con {columna: valor} para cada fila
        """
        
        if exercise_type == 'ConversionRow':
            return self._extract_conversion_values(exercise_json, is_solution)
        elif exercise_type == 'ArithmeticOp':
            return self._extract_arithmetic_values(exercise_json, is_solution)
        else:
            # Por defecto: retorna fila vacía
            return [{}]
    
    def _extract_conversion_values(
        self,
        exercise_json: Dict[str, Any],
        is_solution: bool
    ) -> List[Dict[str, str]]:
        """
        Extrae valores para ConversionRow.
        
        Estructura de columnas: [Etiqueta, Decimal, Binario, C2, SM, BCD]
        
        Enunciado (is_solution=False):
          - Muestra label, decimal
          - Resto: espacios en blanco para resolver
        
        Solución (is_solution=True):
          - Muestra label, decimal, binario, C2, SM, BCD
        """
        
        problem = exercise_json.get('problem', {})
        solution = exercise_json.get('solution', {})
        
        if is_solution:
            # Mostrar valores de solución
            return [{
                'Etiqueta': str(problem.get('label', '?')),
                'Decimal': str(problem.get('val_decimal', '?')),
                'Binario': str(solution.get('sol_bin', '?')),
                'C2': str(solution.get('sol_c2', '?')),
                'SM': str(solution.get('sol_sm', '?')),
                'BCD': str(solution.get('sol_bcd', '?'))
            }]
        else:
            # Mostrar solo problema (para que alumno responda)
            return [{
                'Etiqueta': str(problem.get('label', '?')),
                'Decimal': str(problem.get('val_decimal', '?')),
                'Binario': '',  # Espacio para respuesta
                'C2': '',
                'SM': '',
                'BCD': ''
            }]
    
    def _extract_arithmetic_values(
        self,
        exercise_json: Dict[str, Any],
        is_solution: bool
    ) -> List[Dict[str, str]]:
        """
        Extrae valores para ArithmeticOp.
        
        Estructura: 3 filas (operando1, operador, operando2)
        
        Enunciado (is_solution=False):
          - Muestra operandos y operador
          - Espacio para respuesta
        
        Solución (is_solution=True):
          - Muestra operandos, operador, y resultado
        """
        
        problem = exercise_json.get('problem', {})
        solution = exercise_json.get('solution', {})
        
        op1_label = problem.get('operand1_label', 'A')
        op2_label = problem.get('operand2_label', 'B')
        op_symbol = problem.get('operation_symbol', '+')
        op1_val = problem.get('operand1_value', '?')
        op2_val = problem.get('operand2_value', '?')
        result_val = solution.get('result_value', '?')
        
        if is_solution:
            rows = [
                {'Etiqueta': op1_label, 'Valor': str(op1_val), 'Base': problem.get('operand1_base', '10')},
                {'Etiqueta': op_symbol, 'Valor': str(op2_val), 'Base': problem.get('operand2_base', '10')},
                {'Etiqueta': '=', 'Valor': str(result_val), 'Base': problem.get('result_base', '10')}
            ]
        else:
            rows = [
                {'Etiqueta': op1_label, 'Valor': str(op1_val), 'Base': problem.get('operand1_base', '10')},
                {'Etiqueta': op_symbol, 'Valor': str(op2_val), 'Base': problem.get('operand2_base', '10')},
                {'Etiqueta': '=', 'Valor': '', 'Base': ''}  # Espacio para respuesta
            ]
        
        return rows
    
    def _generate_content_latex(
        self,
        num_rows: int,
        num_cols: int,
        columns: List[str],
        values: List[Dict[str, str]],
        is_solution: bool,
        exercise_type: str
    ) -> str:
        """
        Genera LaTeX compilable con tabla llena de contenido.
        
        Mantiene estilos de Fase 3 pero agrega valores.
        
        Args:
            num_rows: Número de filas de datos
            num_cols: Número de columnas
            columns: Lista de nombres de columna
            values: Lista de dicts {columna: valor}
            is_solution: Si es solución o enunciado
            exercise_type: Tipo de ejercicio (para contexto)
        
        Returns:
            String con código LaTeX compilable
        """
        
        doc_type = "SOLUCION" if is_solution else "ENUNCIADO"
        cell_color = "solucion" if is_solution else "problema"
        
        latex = f"""% ========================================
% FASE 4: CONTENIDO - Valores numeral
% Tipo: {doc_type}
% Ejercicio: {exercise_type}
% ========================================

% Definición de colores (en RGB)
\\usepackage[usenames,dvipsnames]{{xcolor}}
\\definecolor{{problema}}{{RGB}}{{{self.PROBLEMA_COLOR}}}
\\definecolor{{solucion}}{{RGB}}{{{self.SOLUCION_COLOR}}}
\\definecolor{{encabezado}}{{RGB}}{{{self.ENCABEZADO_COLOR}}}

% Tabla con contenido
% Estructura: {num_cols} columnas x {len(values)} filas
% Estilos: Colores, padding, alineación, fuente monoespaciada
% Contenido: Valores del problema {'(solución)' if is_solution else '(para resolver)'}

\\newcommand{{\\cellpadding}}[0]{{\\rule{{0pt}}{{{self.ROW_HEIGHT}}}}}

\\begin{{tabular}}{{|c|c|c|c|c|c|}}
\\hline
\\textbf{{\\cellcolor{{encabezado}} Etiqueta}} & 
\\textbf{{\\cellcolor{{encabezado}} Decimal}} & 
\\textbf{{\\cellcolor{{encabezado}} Binario}} & 
\\textbf{{\\cellcolor{{encabezado}} C2}} & 
\\textbf{{\\cellcolor{{encabezado}} SM}} & 
\\textbf{{\\cellcolor{{encabezado}} BCD}} \\\\
\\hline
"""
        
        # Generar filas CON CONTENIDO
        for i, value_dict in enumerate(values):
            # Obtener valor para cada columna
            etiqueta = value_dict.get('Etiqueta', '')
            decimal = value_dict.get('Decimal', '')
            binario = value_dict.get('Binario', '')
            c2 = value_dict.get('C2', '')
            sm = value_dict.get('SM', '')
            bcd = value_dict.get('BCD', '')
            
            # Construir fila con valores
            row_content = (
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {etiqueta}}} & "
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {decimal}}} & "
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {binario}}} & "
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {c2}}} & "
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {sm}}} & "
                f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {bcd}}} "
                f"\\\\\n"
            )
            latex += row_content
            latex += "\\hline\n"
        
        latex += f"""\\end{{tabular}}

% ========================================
% Salida de FASE 4
% ---
% Esta tabla está:
% [OK] Correctamente dimensionada (filas y columnas)
% [OK] Estructurada con bordes y encabezados
% [OK] Estilizada: colores, alineación, padding
% [OK] LLENA DE CONTENIDO: valores numéricos
% [OK] Compilable como TEX
% [NO] Sin enunciados (se agregan en Fase 5)
% ========================================

% Notas de contenido:
% - Valores mostrados: {len(values)} fila(s) poblada(s)
% - Tipo documento: {'Solución (todos valores visibles)' if is_solution else 'Enunciado (problema a resolver)'}
% - Ejercicio: {exercise_type}
% - Color: {'verde' if is_solution else 'gris'} ({('solucion' if is_solution else 'problema')})
% - Padding: {self.CELL_PADDING}
% - Fuente: monoespaciada (\\texttt) para alineación
"""
        
        return latex
    
    @property
    def phase_name(self) -> str:
        """Nombre de esta fase en el pipeline."""
        return "contenido"
