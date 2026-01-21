"""
FASE 2: Structure Generator - Genera marcos y estructura de tabla.

Responsabilidad: Crear la estructura LaTeX de la tabla (filas, columnas, dimensiones).

Entrada: JSON validado de Fase1DataValidator
Salida: 
  - TEX: Tabla vacía pero correctamente dimensionada y estructurada
  - JSON: JSON con metadata de Fase2 para siguiente fase
  
Característica: Output TEX es compilable (tabla vacía pero válida).
"""

from typing import Dict, Any, List
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class Phase2StructureGenerator(ExerciseRendererPhase):
    """
    FASE 2: Generador de estructura/marcos de tabla.
    
    Responsabilidades:
    1. Determinar número de filas basado en problema
    2. Crear estructura LaTeX de tabla (tabular environment)
    3. Definir encabezados (Etiqueta, Decimal, Binario, C2, SM, BCD)
    4. Generar filas vacías con estructura correcta
    5. Generar TEX compilable (tabla vacía)
    
    Esta fase NO:
    - Agrega colores o estilos visuales (eso es Fase 3)
    - Agrega contenido/valores de problema o solución (eso es Fase 4)
    - Agrega enunciados o explicaciones (eso es Fase 5)
    """
    
    # Ancho de celdas (em, unidades LaTeX)
    CELL_WIDTH = "2.5em"
    
    # Definición de columnas para tabla de conversión
    CONVERSION_COLUMNS = ["Etiqueta", "Decimal", "Binario", "C2", "SM", "BCD"]
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Genera la estructura LaTeX de tabla vacía pero bien dimensionada.
        
        Args:
            exercise_json: JSON validado con estructura {metadata, problem, solution, ...}
            is_solution: Si es enunciado o solución
        
        Returns:
            PhaseOutput con:
            - latex_content: TEX compilable con tabla vacía
            - output_json: JSON con metadata de Fase2 para siguiente fase
            - phase_name: "estructura"
            - tex_filename: "02_fase2_estructura.tex"
        """
        
        # Extraer metadata y problema
        metadata = self._extract_metadata(exercise_json)
        problem = self._extract_problem(exercise_json)
        
        # Determinar número de filas basado en ejercicio_type
        exercise_type = metadata.get('exercise_type', 'ConversionRow')
        num_rows = self._determine_num_rows(exercise_type, problem)
        
        # Generar LaTeX de tabla
        latex = self._generate_latex_table(num_rows, is_solution)
        
        # Preparar JSON para siguiente fase con metadata de Fase2
        output_json = {
            **exercise_json,
            'phase2_structure': {
                'status': 'generated',
                'table_type': 'numeracion_conversion',
                'num_rows': num_rows,
                'num_cols': len(self.CONVERSION_COLUMNS),
                'columns': self.CONVERSION_COLUMNS,
                'structure_defined': True,
                'is_solution': is_solution
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=output_json,
            phase_name="estructura",
            tex_filename="02_fase2_estructura.tex"
        )
    
    def _determine_num_rows(self, exercise_type: str, problem: Dict[str, Any]) -> int:
        """
        Determina número de filas de tabla basado en tipo de ejercicio y problema.
        
        Para ConversionRow: 1 fila de conversión
        Para ArithmeticOp: puede ser 2-3 filas (operandos + resultado)
        
        Args:
            exercise_type: Tipo de ejercicio (ConversionRow, ArithmeticOp, etc)
            problem: Diccionario con parámetros del problema
        
        Returns:
            Número de filas a generar en tabla
        """
        
        if exercise_type == 'ConversionRow':
            # Una fila para el número a convertir
            return 1
        
        elif exercise_type == 'ArithmeticOp':
            # Operandos + resultado: tipicamente 3 filas
            # operand1
            # operand2
            # result
            return 3
        
        else:
            # Default: una fila
            return 1
    
    def _generate_latex_table(self, num_rows: int, is_solution: bool) -> str:
        """
        Genera código LaTeX de tabla vacía pero estructurada.
        
        La tabla tiene:
        - Encabezados: Etiqueta, Decimal, Binario, C2, SM, BCD
        - Filas vacías: num_rows filas sin contenido
        - Bordes básicos: \hline para separación
        
        Args:
            num_rows: Número de filas a generar
            is_solution: Si es para enunciado o solución
        
        Returns:
            String con código LaTeX compilable de tabla
        """
        
        # Documentación inicial
        doc_type = "SOLUCIÓN" if is_solution else "ENUNCIADO"
        latex = f"""% ========================================
% FASE 2: ESTRUCTURA - marcos y dimensiones de tabla
% Tipo: {doc_type}
% ========================================

% Tabla de conversión de bases numéricas
% Estructura: {len(self.CONVERSION_COLUMNS)} columnas x {num_rows} filas

\\begin{{tabular}}{{|c|c|c|c|c|c|}}
\\hline
"""
        
        # Encabezados
        header = " & ".join(self.CONVERSION_COLUMNS) + " \\\\\n"
        latex += header + "\\hline\n"
        
        # Filas vacías (estructura)
        for i in range(num_rows):
            # Cada fila tiene 6 celdas vacías
            latex += " & " * (len(self.CONVERSION_COLUMNS) - 1) + " \\\\\n"
            latex += "\\hline\n"
        
        latex += """\\end{tabular}

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
        
        return latex
    
    @property
    def phase_name(self) -> str:
        """Nombre de esta fase en el pipeline."""
        return "estructura"
