"""
Mapper para Lógica Secuencial (SequentialExerciseData).

Convierte entre:
- SequentialExerciseData (ExerciseData Python)
- Problem (JSON agnóstico)
"""

from typing import Any, Dict
from dataclasses import asdict
from modules.secuencial.models import SequentialExerciseData
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers.base import ProblemMapper


class SequentialMapper(ProblemMapper):
    """
    Mapper para Lógica Secuencial (Flip-Flops, Contadores, Registros).
    """
    
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.SECUENCIAL
    
    def _extract_statement(self, exercise: SequentialExerciseData) -> Problem.Statement:
        """Extrae enunciado del circuito secuencial."""
        problem_fields = {
            'ff_type': exercise.ff_type,
            'edge_type': exercise.edge_type,
            'logic_type': exercise.logic_type,
            'has_async': exercise.has_async,
            'total_cycles': exercise.total_cycles,
            'clk_sequence': exercise.clk_sequence,
            'input_sequence': exercise.input_sequence
        }
        
        if exercise.has_async:
            problem_fields['async_sequence'] = exercise.async_sequence
        
        text = (
            f"Simula un circuito secuencial con flip-flops {exercise.ff_type}, "
            f"sensible al flanco de {exercise.logic_type.lower()}. "
            f"Dada la secuencia de entrada, calcula la salida en cada ciclo."
        )
        
        instructions = (
            f"Para cada ciclo del reloj:\n"
            f"1. Lee las entradas en el instante actual\n"
            f"2. Aplica las ecuaciones de próximo estado\n"
            f"3. Actualiza el estado después del flanco\n"
            f"4. Registra la salida (Q y Q')\n"
            f"5. Verifica posibles violaciones de setup/hold"
        )
        
        return Problem.Statement(
            text=text,
            instructions=instructions,
            problem_fields=problem_fields
        )
    
    def _extract_solution(self, exercise: SequentialExerciseData) -> Problem.Solution:
        """Extrae solución del circuito secuencial."""
        explanation = (
            f"La simulación del circuito {exercise.ff_type} "
            f"({exercise.logic_type.lower()}) genera la secuencia de salidas "
            f"según las transiciones de estado."
        )
        
        steps = [
            f"Circuito: {exercise.ff_type} (flanco de {exercise.logic_type})",
            f"Total de ciclos: {exercise.total_cycles}",
            f"Reloj: {exercise.clk_sequence}",
            f"Entrada: {exercise.input_sequence}",
            f"Salida Q: {exercise.output_sequence}",
            f"Salida Q': {exercise.output_bar_sequence}"
        ]
        
        if exercise.setup_time_violations:
            steps.append(f"Violaciones de setup: {exercise.setup_time_violations}")
        if exercise.hold_time_violations:
            steps.append(f"Violaciones de hold: {exercise.hold_time_violations}")
        
        solution_fields = {
            'output_sequence': exercise.output_sequence,
            'output_bar_sequence': exercise.output_bar_sequence,
            'state_transitions': exercise.state_transitions,
            'setup_time_violations': exercise.setup_time_violations,
            'hold_time_violations': exercise.hold_time_violations
        }
        
        return Problem.Solution(
            explanation=explanation,
            steps=steps,
            solution_fields=solution_fields
        )
    
    def _serialize_exercise(self, exercise: SequentialExerciseData) -> Dict[str, Any]:
        """Serializa SequentialExerciseData como dict."""
        return asdict(exercise)
    
    def _reconstruct_from_problem_fields(self, problem: Problem) -> SequentialExerciseData:
        """Reconstruye desde fields."""
        pf = problem.statement.problem_fields
        sf = problem.solution.solution_fields
        
        return SequentialExerciseData(
            title=problem.metadata.title,
            description=problem.statement.text,
            ff_type=pf['ff_type'],
            edge_type=pf['edge_type'],
            logic_type=pf['logic_type'],
            has_async=pf['has_async'],
            async_type=pf.get('async_type', 'Clear'),
            async_level=pf.get('async_level', '0'),
            total_cycles=pf['total_cycles'],
            clk_sequence=pf['clk_sequence'],
            async_sequence=pf.get('async_sequence', '0' * pf['total_cycles']),
            input_sequence=pf['input_sequence'],
            output_sequence=sf['output_sequence'],
            output_bar_sequence=sf['output_bar_sequence'],
            state_transitions=sf['state_transitions'],
            setup_time_violations=sf['setup_time_violations'],
            hold_time_violations=sf['hold_time_violations'],
            output_placeholder=""
        )
    
    def _deserialize_exercise(self, data: Dict[str, Any]) -> SequentialExerciseData:
        """Deserializa desde dict."""
        return SequentialExerciseData(**data)
