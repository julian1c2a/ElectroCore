"""
FASE 3: Details - Agrega estilos visuales a la tabla.

Responsabilidad: Agregar colores, alineación, padding, bordes mejorados.

Entrada: JSON + TEX de Fase 2 (tabla estructura)
Salida: 
  - TEX: Tabla con estilos visuales (aún sin contenido)
  - JSON: JSON con metadata de Fase3 para siguiente fase
  
Característica: Tabla compilable pero aún vacía (contenido viene en Fase 4).
"""

from typing import Dict, Any
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class Phase3Details(ExerciseRendererPhase):
    """
    FASE 3: Agregador de detalles visuales (estilos, colores, alineación).
    
    Responsabilidades:
    1. Definir colores para problema vs solución
    2. Agregar alineación vertical y horizontal
    3. Agregar padding y espaciado en celdas
    4. Mejorar bordes y líneas separadoras
    5. Generar TEX compilable con estilos
    
    Esta fase NO:
    - Agrega contenido/valores (eso es Fase 4)
    - Valida JSON (eso fue Fase 1)
    - Define estructura (eso fue Fase 2)
    - Genera enunciados (eso es Fase 5)
    
    La tabla sigue siendo VACÍA en esta fase, pero ESTILIZADA.
    """
    
    # Definición de colores (RGB)
    PROBLEMA_COLOR = "240,240,240"  # Gris muy claro
    SOLUCION_COLOR = "200,255,200"  # Verde muy claro
    ENCABEZADO_COLOR = "230,230,230"  # Gris medio
    
    # Definición de espaciado
    CELL_PADDING = "0.3em"  # Padding dentro de celda
    ROW_HEIGHT = "0.8em"  # Altura mínima de fila
    
    # Fuente monoespaciada para alineación
    FONT_FAMILY = "ttfamily"  # typewriter/monospace
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Genera LaTeX con estilos visuales (colores, alineación, padding).
        
        Args:
            exercise_json: JSON validado + Fase2 metadata
            is_solution: Si es enunciado o solución
        
        Returns:
            PhaseOutput con:
            - latex_content: TEX compilable con tabla estilizada
            - output_json: JSON con metadata de Fase3 para siguiente fase
            - phase_name: "detalles"
            - tex_filename: "03_fase3_detalles.tex"
        """
        
        # Extraer metadata de Fase 2
        metadata = self._extract_metadata(exercise_json)
        phase2_struct = exercise_json.get('phase2_structure', {})
        
        num_rows = phase2_struct.get('num_rows', 1)
        num_cols = phase2_struct.get('num_cols', 6)
        columns = phase2_struct.get('columns', [])
        
        # Determinar qué color usar para celdas
        cell_color = self._get_cell_color(is_solution)
        
        # Generar LaTeX con estilos
        latex = self._generate_styled_latex(
            num_rows=num_rows,
            num_cols=num_cols,
            columns=columns,
            is_solution=is_solution,
            cell_color=cell_color
        )
        
        # Preparar JSON para siguiente fase
        output_json = {
            **exercise_json,
            'phase3_details': {
                'status': 'styled',
                'problema_color': self.PROBLEMA_COLOR if not is_solution else None,
                'solucion_color': self.SOLUCION_COLOR if is_solution else None,
                'encabezado_color': self.ENCABEZADO_COLOR,
                'cell_padding': self.CELL_PADDING,
                'row_height': self.ROW_HEIGHT,
                'font': self.FONT_FAMILY,
                'styles_applied': True,
                'is_solution': is_solution
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=output_json,
            phase_name="detalles",
            tex_filename="03_fase3_detalles.tex"
        )
    
    def _get_cell_color(self, is_solution: bool) -> str:
        """Retorna color de celda según es enunciado o solución."""
        if is_solution:
            return self.SOLUCION_COLOR
        else:
            return self.PROBLEMA_COLOR
    
    def _generate_styled_latex(
        self,
        num_rows: int,
        num_cols: int,
        columns: list,
        is_solution: bool,
        cell_color: str
    ) -> str:
        """
        Genera LaTeX compilable con tabla estilizada.
        
        Incluye:
        - Definición de colores
        - Alineación centrada
        - Padding en celdas
        - Altura de filas
        - Fuente monoespaciada
        
        Args:
            num_rows: Número de filas de datos
            num_cols: Número de columnas
            columns: Lista de nombres de columna
            is_solution: Si es para solución o enunciado
            cell_color: Color RGB de celdas
        
        Returns:
            String con código LaTeX compilable
        """
        
        doc_type = "SOLUCION" if is_solution else "ENUNCIADO"
        
        latex = f"""% ========================================
% FASE 3: DETALLES - Estilos visuales
% Tipo: {doc_type}
% ========================================

% Definición de colores (en RGB)
\\usepackage[usenames,dvipsnames]{{xcolor}}
\\definecolor{{problema}}{{RGB}}{{{self.PROBLEMA_COLOR}}}
\\definecolor{{solucion}}{{RGB}}{{{self.SOLUCION_COLOR}}}
\\definecolor{{encabezado}}{{RGB}}{{{self.ENCABEZADO_COLOR}}}

% Tabla de conversión con estilos
% Estructura: {num_cols} columnas x {num_rows} filas
% Estilos: Colores, padding, alineación, fuente monoespaciada

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
        
        # Generar filas estilizadas (aún vacías)
        for i in range(num_rows):
            # Usar fuente monoespaciada para mantener alineación
            row_content = (
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} & "
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} & "
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} & "
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} & "
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} & "
                f"\\cellcolor{{{self._get_row_color(i, is_solution)}}} "
                f"\\texttt{{\\cellpadding}} "
                f"\\\\\n"
            )
            latex += row_content
            latex += "\\hline\n"
        
        latex += f"""\\end{{tabular}}

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
% - Encabezados: fondo gris medio ({self.ENCABEZADO_COLOR})
% - Celdas: fondo {'verde' if is_solution else 'gris'} ({cell_color})
% - Padding: {self.CELL_PADDING}
% - Altura mínima: {self.ROW_HEIGHT}
% - Fuente: monoespaciada (\\texttt) para alineación
% - Alineación: centrada (c) en todas las columnas
"""
        
        return latex
    
    def _get_row_color(self, row_index: int, is_solution: bool) -> str:
        """
        Retorna color para fila según índice e is_solution.
        
        En Fase 3, todas las filas tienen el mismo color (enunciado o solución).
        En versiones futuras podría variar por fila.
        """
        if is_solution:
            return "solucion"
        else:
            return "problema"
    
    @property
    def phase_name(self) -> str:
        """Nombre de esta fase en el pipeline."""
        return "detalles"
