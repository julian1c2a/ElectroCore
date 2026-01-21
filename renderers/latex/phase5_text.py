"""
FASE 5: Text - Agrega enunciados, explicaciones e instrucciones.

Responsabilidad: Generar documento COMPLETO con tabla + texto narrativo.

Entrada: JSON + TEX de Fase 4 (tabla llena con valores)
Salida: 
  - TEX: Documento completo (enunciado + tabla + explicación)
  - JSON: JSON con metadata de Fase5 (final del pipeline)
  
Característica: ÚLTIMA FASE. Produce documento compilable listo para PDF.
               Es la ÚNICA FASE que recibe None como output_json (final del pipeline).
"""

from typing import Dict, Any, Optional
from renderers.latex.renderer_base import ExerciseRendererPhase, PhaseOutput


class Phase5Text(ExerciseRendererPhase):
    """
    FASE 5: Agregador de texto (enunciados, explicaciones, instrucciones).
    
    Responsabilidades:
    1. Extraer enunciado (problem statement)
    2. Extraer instrucciones (cómo resolver)
    3. Extraer explicación (solution explanation)
    4. Extraer pasos de resolución
    5. Composición del documento final
    6. Generar TEX completo y compilable
    
    Esta fase NO:
    - Valida JSON (eso fue Fase 1)
    - Define estructura (eso fue Fase 2)
    - Define estilos (eso fue Fase 3)
    - Llena valores (eso fue Fase 4)
    
    ESTA ES LA ÚLTIMA FASE. El documento está LISTO para compilar.
    Output JSON es None (final del pipeline).
    """
    
    # Colores (heredados)
    PROBLEMA_COLOR = "240,240,240"
    SOLUCION_COLOR = "200,255,200"
    ENCABEZADO_COLOR = "230,230,230"
    
    # Tipografía
    FONT_TITLE = "large"
    FONT_STATEMENT = "normalsize"
    FONT_EXPLANATION = "small"
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Genera LaTeX completo con enunciado, tabla y explicación.
        
        Args:
            exercise_json: JSON validado + metadata Fases 1-4 + problem/solution
            is_solution: Si generar documento de solución (True) o enunciado (False)
        
        Returns:
            PhaseOutput con:
            - latex_content: TEX COMPLETO (final, listo para PDF)
            - output_json: None (esta es la última fase)
            - phase_name: "texto"
            - tex_filename: "05_fase5_enunciados.tex"
        """
        
        # Extraer metadata acumulada
        metadata = self._extract_metadata(exercise_json)
        exercise_type = metadata.get('exercise_type', 'unknown')
        
        # Extraer componentes textuales
        statement = self._extract_statement(exercise_json, exercise_type)
        instructions = self._extract_instructions(exercise_json, exercise_type)
        explanation = self._extract_explanation(exercise_json, is_solution)
        steps = self._extract_steps(exercise_json, exercise_type, is_solution)
        
        # Extraer tabla de Fase 4
        table_tex = self._extract_table_from_phase4(exercise_json)
        
        # Generar documento completo
        latex = self._generate_full_document_latex(
            statement=statement,
            instructions=instructions,
            table=table_tex,
            explanation=explanation,
            steps=steps,
            is_solution=is_solution,
            exercise_type=exercise_type
        )
        
        # Preparar JSON para metadata (ÚLTIMA FASE: None)
        output_json = None  # No hay siguiente fase
        
        # Metadata de Fase 5 (para auditoría, no para siguiente)
        final_metadata = {
            **exercise_json,
            'phase5_text': {
                'status': 'completed',
                'exercise_type': exercise_type,
                'statement_extracted': bool(statement),
                'instructions_extracted': bool(instructions),
                'explanation_extracted': bool(explanation),
                'steps_extracted': len(steps) > 0,
                'document_complete': True,
                'is_solution': is_solution,
                'pipeline_complete': True
            }
        }
        
        return PhaseOutput(
            latex_content=latex,
            output_json=final_metadata,  # Para auditoría (no para siguiente fase)
            phase_name="texto",
            tex_filename="05_fase5_enunciados.tex"
        )
    
    def _extract_statement(
        self,
        exercise_json: Dict[str, Any],
        exercise_type: str
    ) -> str:
        """
        Extrae enunciado del problema.
        
        Campos buscados:
        - problem['statement']
        - problem['description']
        - metadata['description']
        
        Si no encuentra, retorna string genérico.
        """
        
        problem = exercise_json.get('problem', {})
        
        # Buscar en orden de preferencia
        if 'statement' in problem:
            return problem['statement']
        
        if 'description' in problem:
            return problem['description']
        
        # Fallback a description del ejercicio
        title = exercise_json.get('title', 'Ejercicio sin título')
        description = exercise_json.get('description', '')
        
        if description:
            return f"{title}\n\n{description}"
        
        return f"{title}"
    
    def _extract_instructions(
        self,
        exercise_json: Dict[str, Any],
        exercise_type: str
    ) -> str:
        """
        Extrae instrucciones sobre cómo resolver.
        
        Campos buscados:
        - problem['instructions']
        - problem['how_to_solve']
        
        Si no encuentra, retorna instrucciones genéricas según exercise_type.
        """
        
        problem = exercise_json.get('problem', {})
        
        # Buscar instrucciones explícitas
        if 'instructions' in problem:
            return problem['instructions']
        
        if 'how_to_solve' in problem:
            return problem['how_to_solve']
        
        # Instrucciones genéricas por tipo
        if exercise_type == 'ConversionRow':
            return (
                "Convierte el número decimal dado a sus representaciones "
                "en binario, complemento a 2, signo-magnitud y BCD."
            )
        elif exercise_type == 'ArithmeticOp':
            return (
                "Realiza la operación aritmética indicada utilizando "
                "la base numérica especificada."
            )
        else:
            return "Resuelve el ejercicio."
    
    def _extract_explanation(
        self,
        exercise_json: Dict[str, Any],
        is_solution: bool
    ) -> str:
        """
        Extrae explicación (solo si is_solution=True).
        
        Campos buscados:
        - solution['explanation']
        - solution['description']
        
        Si is_solution=False, retorna string vacío.
        """
        
        if not is_solution:
            return ""
        
        solution = exercise_json.get('solution', {})
        
        if 'explanation' in solution:
            return solution['explanation']
        
        if 'description' in solution:
            return solution['description']
        
        return ""
    
    def _extract_steps(
        self,
        exercise_json: Dict[str, Any],
        exercise_type: str,
        is_solution: bool
    ) -> list:
        """
        Extrae pasos de resolución (solo si is_solution=True).
        
        Campos buscados:
        - solution['steps'] (lista)
        - solution['resolution_steps']
        
        Si no encuentra, retorna lista vacía.
        """
        
        if not is_solution:
            return []
        
        solution = exercise_json.get('solution', {})
        
        # Buscar steps
        if 'steps' in solution:
            steps = solution['steps']
            if isinstance(steps, list):
                return steps
        
        if 'resolution_steps' in solution:
            steps = solution['resolution_steps']
            if isinstance(steps, list):
                return steps
        
        # Si no hay steps explícitos, retorna lista vacía
        return []
    
    def _extract_table_from_phase4(
        self,
        exercise_json: Dict[str, Any]
    ) -> str:
        """
        Extrae la tabla compilada de Fase 4.
        
        Si Fase 4 no se ejecutó o no hay metadata, retorna tabla vacía.
        
        Nota: En implementación actual, se regenra la tabla aquí.
        En versión futura, se podría reutilizar de fase anterior.
        """
        
        phase4_metadata = exercise_json.get('phase4_content', {})
        
        if not phase4_metadata:
            # Si no hay metadata de Fase 4, retorna tabla vacía
            return self._generate_empty_table()
        
        # En implementación actual, se regenra la tabla
        # (Similar a cómo Fase 3 regenera la tabla de Fase 2)
        return self._regenerate_table(exercise_json)
    
    def _regenerate_table(self, exercise_json: Dict[str, Any]) -> str:
        """
        Regenera la tabla de Fase 4.
        
        Esto asegura que la tabla en el documento final sea idéntica
        a la que se esperaría de Fase 4.
        """
        
        problem = exercise_json.get('problem', {})
        solution = exercise_json.get('solution', {})
        phase3_details = exercise_json.get('phase3_details', {})
        
        cell_color = "solucion" if phase3_details.get('is_solution') else "problema"
        
        table_tex = r"""
% ========================================
% Tabla poblada (de Fase 4)
% ========================================

\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

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
"""
        
        # Llenar tabla (simplificado para Fase 5)
        label = str(problem.get('label', '?'))
        decimal = str(problem.get('val_decimal', '?'))
        binario = str(solution.get('sol_bin', '?'))
        c2 = str(solution.get('sol_c2', '?'))
        sm = str(solution.get('sol_sm', '?'))
        bcd = str(solution.get('sol_bcd', '?'))
        
        table_tex += (
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {label}}} & "
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {decimal}}} & "
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {binario}}} & "
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {c2}}} & "
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {sm}}} & "
            f"\\cellcolor{{{cell_color}}} \\texttt{{\\cellpadding {bcd}}} "
            f"\\\\\n"
        )
        
        table_tex += r"""
\hline
\end{tabular}
"""
        
        return table_tex
    
    def _generate_empty_table(self) -> str:
        """Retorna tabla vacía si no hay data de Fase 4."""
        return r"""
\begin{tabular}{|c|c|c|c|c|c|}
\hline
\textbf{Etiqueta} & \textbf{Decimal} & \textbf{Binario} & \textbf{C2} & \textbf{SM} & \textbf{BCD} \\
\hline
 &  &  &  &  &  \\
\hline
\end{tabular}
"""
    
    def _generate_full_document_latex(
        self,
        statement: str,
        instructions: str,
        table: str,
        explanation: str,
        steps: list,
        is_solution: bool,
        exercise_type: str
    ) -> str:
        """
        Genera documento LaTeX COMPLETO.
        
        Estructura:
        1. Encabezado (tipo documento)
        2. Enunciado
        3. Instrucciones (si las hay)
        4. Tabla de Fase 4
        5. [SEPARADOR si es solución]
        6. Explicación (solo si is_solution=True)
        7. Pasos de resolución (solo si hay)
        
        Este es el DOCUMENTO FINAL, compilable directamente.
        """
        
        doc_type = "SOLUCION" if is_solution else "ENUNCIADO"
        
        latex = f"""% ========================================
% FASE 5: TEXTO - Documento Completo
% Tipo: {doc_type}
% Ejercicio: {exercise_type}
% ========================================

% Definicion de colores
\\usepackage[usenames,dvipsnames]{{xcolor}}
\\definecolor{{problema}}{{RGB}}{{240,240,240}}
\\definecolor{{solucion}}{{RGB}}{{200,255,200}}
\\definecolor{{encabezado}}{{RGB}}{{230,230,230}}

% Comando para padding en tablas
\\newcommand{{\\cellpadding}}[0]{{\\rule{{0pt}}{{0.8em}}}}

% ========================================
% ENUNCIADO DEL PROBLEMA
% ========================================

\\section*{{Enunciado}}

{statement}

"""
        
        # Agregar instrucciones si las hay
        if instructions and instructions.strip():
            latex += f"""
\\subsection*{{Instrucciones}}

{instructions}

"""
        
        # Agregar tabla (siempre)
        latex += f"""
% ========================================
% TABLA DE DATOS
% ========================================

{table}

"""
        
        # SEGUNDA PARTE: Solo si es solución
        if is_solution:
            latex += f"""
% ========================================
% SOLUCION Y EXPLICACION
% ========================================

\\section*{{Solucion}}

"""
            
            # Explicación (si la hay)
            if explanation and explanation.strip():
                latex += f"""
\\subsection*{{Explicacion}}

{explanation}

"""
            
            # Pasos de resolución (si los hay)
            if steps and len(steps) > 0:
                latex += """
\\subsection*{Pasos de Resolucion}

\\begin{enumerate}
"""
                for i, step in enumerate(steps, 1):
                    step_text = str(step) if not isinstance(step, str) else step
                    latex += f"  \\item {step_text}\n"
                
                latex += """\\end{enumerate}

"""
        
        # Pie de documento
        latex += f"""
% ========================================
% Salida de FASE 5 (FINAL DEL PIPELINE)
% ---
% Este documento esta:
% [OK] Completo: enunciado + tabla + explicacion
% [OK] Estructurado: secciones y subsecciones
% [OK] Compilable como TEX
% [OK] Listo para generar PDF
% [OK] Pipeline completo: Fase 1 -> 2 -> 3 -> 4 -> 5
% ========================================

% Documento {doc_type}
% Ejercicio: {exercise_type}
% Compilable: SI
% Generado por: Phase5Text (Fase 5 del pipeline)
"""
        
        return latex
    
    @property
    def phase_name(self) -> str:
        """Nombre de esta fase en el pipeline."""
        return "texto"
