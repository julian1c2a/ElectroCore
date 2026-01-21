"""
Mapper para Problemas de Diseño Lógico (LogicProblemExerciseData).

Convierte entre:
- LogicProblemExerciseData (ExerciseData Python)
- Problem (JSON agnóstico)
"""

from typing import Any, Dict
from dataclasses import asdict
from modules.combinacional.models import LogicProblemExerciseData
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers.base import ProblemMapper


class LogicProblemMapper(ProblemMapper):
    """
    Mapper para Problemas de Diseño Lógico.
    
    Responsabilidades:
    - LogicProblemExerciseData → Problem agnóstico
    - Problem → LogicProblemExerciseData
    """
    
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.LOGIC
    
    def _extract_statement(self, exercise: LogicProblemExerciseData) -> Problem.Statement:
        """Extrae enunciado del problema lógico."""
        problem_fields = {
            'context_title': exercise.context_title,
            'variables_desc': exercise.variables_desc,
            'output_desc': exercise.output_desc,
            'logic_description': exercise.logic_description,
            'vars_clean': exercise.vars_clean,
            'out_clean': exercise.out_clean
        }
        
        # Construir texto con contexto
        vars_text = "\n".join(f"  {var}" for var in exercise.variables_desc)
        text = (
            f"{exercise.context_title}\n\n"
            f"Variables de entrada:\n{vars_text}\n\n"
            f"Salida: {exercise.output_desc}\n\n"
            f"Lógica requerida:\n{exercise.logic_description}"
        )
        
        instructions = (
            f"Diseña un circuito combinacional que implemente la lógica descrita. "
            f"Representa la solución como:\n"
            f"1. Tabla de verdad para las variables {', '.join(exercise.vars_clean)}\n"
            f"2. Expresión booleana simplificada\n"
            f"3. Esquema del circuito (opcional)"
        )
        
        return Problem.Statement(
            text=text,
            instructions=instructions,
            problem_fields=problem_fields
        )
    
    def _extract_solution(self, exercise: LogicProblemExerciseData) -> Problem.Solution:
        """Extrae solución del problema lógico."""
        explanation = (
            f"La solución del problema \"{exercise.context_title}\" "
            f"requiere implementar la lógica especificada usando puertas lógicas."
        )
        
        # Generar tabla de verdad en texto
        num_vars = len(exercise.vars_clean)
        steps = [
            f"Tabla de verdad para {num_vars} variables:",
            f"Se definen {2**num_vars} filas combinando todos los valores posibles",
            f"Solución simplificada: {exercise.simplified_solution}"
        ]
        
        solution_fields = {
            'truth_table_outputs': exercise.truth_table_outputs,
            'simplified_solution': exercise.simplified_solution,
            'vars_clean': exercise.vars_clean,
            'out_clean': exercise.out_clean
        }
        
        return Problem.Solution(
            explanation=explanation,
            steps=steps,
            solution_fields=solution_fields
        )
    
    def _serialize_exercise(self, exercise: LogicProblemExerciseData) -> Dict[str, Any]:
        """Serializa LogicProblemExerciseData como dict."""
        return asdict(exercise)
    
    def _reconstruct_from_problem_fields(self, problem: Problem) -> LogicProblemExerciseData:
        """Reconstruye desde fields."""
        pf = problem.statement.problem_fields
        sf = problem.solution.solution_fields
        
        return LogicProblemExerciseData(
            title=problem.metadata.title,
            description=problem.statement.text,
            context_title=pf['context_title'],
            variables_desc=pf['variables_desc'],
            output_desc=pf['output_desc'],
            logic_description=pf['logic_description'],
            vars_clean=pf['vars_clean'],
            out_clean=pf['out_clean'],
            truth_table_outputs=sf['truth_table_outputs'],
            simplified_solution=sf['simplified_solution']
        )
    
    def _deserialize_exercise(self, data: Dict[str, Any]) -> LogicProblemExerciseData:
        """Deserializa desde dict."""
        return LogicProblemExerciseData(**data)
