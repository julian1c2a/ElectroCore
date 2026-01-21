"""
Mapper para Circuitos Integrados Medianos (MSI).

Convierte entre:
- MSIExerciseData (ExerciseData Python)
- Problem (JSON agnóstico)
"""

from typing import Any, Dict
from dataclasses import asdict
from modules.combinacional.models import MSIExerciseData
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers.base import ProblemMapper


class MSIMapper(ProblemMapper):
    """
    Mapper para Circuitos MSI (Multiplexor, Comparador, Sumador).
    """
    
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.MSI
    
    def _extract_statement(self, exercise: MSIExerciseData) -> Problem.Statement:
        """Extrae enunciado del circuito MSI."""
        problem_fields = {
            'block_type': exercise.block_type,
            'params': exercise.params
        }
        
        text = (
            f"Analiza el circuito {exercise.block_type} con los parámetros dados. "
            f"Determina las salidas para las entradas especificadas."
        )
        
        instructions = (
            f"Para el circuito {exercise.block_type}:\n"
            f"1. Comprende la función y comportamiento\n"
            f"2. Aplica las entradas dadas\n"
            f"3. Calcula las salidas esperadas\n"
            f"4. Verifica con la tabla de verdad"
        )
        
        return Problem.Statement(
            text=text,
            instructions=instructions,
            problem_fields=problem_fields
        )
    
    def _extract_solution(self, exercise: MSIExerciseData) -> Problem.Solution:
        """Extrae solución del circuito MSI."""
        explanation = (
            f"El circuito {exercise.block_type} genera las salidas siguiendo "
            f"su tabla de verdad característica."
        )
        
        steps = [
            f"1. Circuito: {exercise.block_type}",
            f"2. Entradas: {exercise.params}",
            f"3. Salidas esperadas: {exercise.expected_outputs}",
            f"4. Verificación en tabla de verdad"
        ]
        
        solution_fields = {
            'expected_outputs': exercise.expected_outputs,
            'truth_table': exercise.truth_table
        }
        
        return Problem.Solution(
            explanation=explanation,
            steps=steps,
            solution_fields=solution_fields
        )
    
    def _serialize_exercise(self, exercise: MSIExerciseData) -> Dict[str, Any]:
        """Serializa MSIExerciseData como dict."""
        return asdict(exercise)
    
    def _reconstruct_from_problem_fields(self, problem: Problem) -> MSIExerciseData:
        """Reconstruye desde fields."""
        pf = problem.statement.problem_fields
        sf = problem.solution.solution_fields
        
        return MSIExerciseData(
            title=problem.metadata.title,
            description=problem.statement.text,
            block_type=pf['block_type'],
            params=pf['params'],
            expected_outputs=sf['expected_outputs'],
            truth_table=sf['truth_table']
        )
    
    def _deserialize_exercise(self, data: Dict[str, Any]) -> MSIExerciseData:
        """Deserializa desde dict."""
        return MSIExerciseData(**data)
