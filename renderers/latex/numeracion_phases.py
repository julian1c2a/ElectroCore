"""
Implementación del pipeline de renderers para Numeración.

3 Fases:
1. Structure: Define marcos y estructura de la tabla
2. Details: Agrega detalles visuales (bordes, colores, alineación)
3. Text: Agrega texto, enunciados, explicaciones
"""

from typing import Dict, Any
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class NumeracionPhase1Structure(ExerciseRendererPhase):
    """Fase 1: Estructura y marcos de la tabla."""
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Renderiza SOLO la estructura/marcos de la tabla de conversión.
        
        Responsabilidad: Definir filas, columnas, tamaños
        No: Colores, bordes, texto detallado
        """
        problem = self._extract_problem(exercise_json)
        solution = self._extract_solution(exercise_json)
        
        # Crear estructura LaTeX básica
        latex = """% ========================================
% FASE 1: ESTRUCTURA - marcos y dimensiones
% ========================================

\\begin{tabular}{|c|c|c|c|c|c|}
\\hline
Etiqueta & Decimal & Binario & C2 & SM & BCD \\\\
\\hline
"""
        
        # Estructura de tabla (sin valores aún)
        for i in range(4):
            latex += " & & & & & \\\\\n\\hline\n"
        
        latex += "\\end{tabular}\n"
        
        # JSON intermedio: pasar todo para la siguiente fase
        output_json = {
            **exercise_json,
            'phase1_state': {
                'table_structure_defined': True,
                'rows': 4,
                'columns': 6
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=output_json,
            phase_name="estructura",
            tex_filename="01_numeracion_estructura.tex"
        )


class NumeracionPhase2Details(ExerciseRendererPhase):
    """Fase 2: Detalles visuales (bordes, colores, alineación)."""
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Renderiza DETALLES VISUALES: colores, alineación, estilos.
        
        Responsabilidad: Mejorar presentación visual
        No: Agregar contenido/texto significativo
        """
        problem = self._extract_problem(exercise_json)
        solution = self._extract_solution(exercise_json)
        
        latex = """% ========================================
% FASE 2: DETALLES - colores, estilos, alineación
% ========================================

% Definir colores para problema/solución
\\definecolor{problema}{RGB}{240,240,240}  % gris claro
\\definecolor{solucion}{RGB}{255,200,200}  % rosa claro

% Tabla con detalles visuales
\\begin{tabular}{|c|c|c|c|c|c|}
\\hline
\\textbf{Etiqueta} & \\textbf{Decimal} & \\textbf{Binario} & \\textbf{C2} & \\textbf{SM} & \\textbf{BCD} \\\\
\\hline
"""
        
        # Agregar filas con colores alternados
        label = problem.get('label', 'a')
        val_decimal = problem.get('val_decimal', 0)
        
        for i in range(4):
            if i == 0:
                # Primera fila: el problema actual
                latex += f"\\cellcolor{{problema}}{label} & \\cellcolor{{problema}}{val_decimal} & & & & \\\\\n\\hline\n"
            else:
                # Otras filas vacías pero estilizadas
                latex += " & & & & & \\\\\n\\hline\n"
        
        latex += "\\end{tabular}\n\n"
        latex += "% Nota: Colores definidos, estructura lista para contenido\n"
        
        # JSON intermedio
        output_json = {
            **exercise_json,
            'phase2_state': {
                'colors_defined': True,
                'styling_applied': True
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=output_json,
            phase_name="detalles",
            tex_filename="02_numeracion_detalles.tex"
        )


class NumeracionPhase3Text(ExerciseRendererPhase):
    """Fase 3 (ÚLTIMA): Texto, enunciados, soluciones."""
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Renderiza CONTENIDO FINAL: valores, soluciones, explicaciones.
        
        Esta es la ÚLTIMA FASE: solo produce LaTeX, NO JSON.
        """
        problem = self._extract_problem(exercise_json)
        solution = self._extract_solution(exercise_json)
        
        label = problem.get('label', 'a')
        val_decimal = problem.get('val_decimal', 0)
        
        if is_solution:
            # Mostrar soluciones
            sol_bin = solution.get('sol_bin', 'NR')
            sol_c2 = solution.get('sol_c2', 'NR')
            sol_sm = solution.get('sol_sm', 'NR')
            sol_bcd = solution.get('sol_bcd', 'NR')
            
            latex = f"""% ========================================
% FASE 3: TEXTO - Contenido y soluciones
% ========================================

\\section*{{Soluciones - Conversión de Bases}}

Para el número decimal \\textbf{{{val_decimal}}} (etiqueta {label}):

\\begin{{itemize}}
  \\item Binario: \\textbf{{{sol_bin}}}
  \\item Complemento a 2: \\textbf{{{sol_c2}}}
  \\item Signo-Magnitud: \\textbf{{{sol_sm}}}
  \\item BCD: \\textbf{{{sol_bcd}}}
\\end{{itemize}}

"""
        else:
            # Mostrar solo problema
            latex = f"""% ========================================
% FASE 3: TEXTO - Enunciado
% ========================================

\\section*{{Conversión de Bases Numéricas}}

\\textbf{{Pregunta:}} Convierte el número decimal \\textbf{{{val_decimal}}} a los siguientes sistemas:

\\begin{{itemize}}
  \\item Binario Natural
  \\item Complemento a 2 (8 bits)
  \\item Signo-Magnitud (8 bits)
  \\item BCD (Decimal Codificado en Binario)
\\end{{itemize}}

Completa la tabla anterior con los valores correspondientes.

"""
        
        # ÚLTIMA FASE: No devolvemos JSON (es None)
        return PhaseOutput(
            latex_content=latex,
            output_json=None,  # ÚLTIMO = no hay siguiente
            phase_name="texto",
            tex_filename="03_numeracion_texto.tex"
        )
