"""
Mapper para problemas de Mapas de Karnaugh (KarnaughExerciseData).

Convierte entre:
- KarnaughExerciseData (ExerciseData Python)
- Problem (JSON agnóstico)
"""

from typing import Any, Dict
from dataclasses import asdict
from modules.combinacional.models import KarnaughExerciseData
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers.base import ProblemMapper


class KarnaughMapper(ProblemMapper):
    """
    Mapper para Karnaugh (mapas de Karnaugh y simplificación booleana).
    
    Responsabilidades:
    - KarnaughExerciseData → Problem agnóstico
    - Problem → KarnaughExerciseData
    """
    
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.KARNAUGH
    
    def _extract_statement(self, exercise: KarnaughExerciseData) -> Problem.Statement:
        """Extrae enunciado de Karnaugh."""
        problem_fields = {
            'vars_name': exercise.vars_name,
            'out_name': exercise.out_name,
            'truth_table_outputs': exercise.truth_table_outputs,
            'canon_type': exercise.canon_type,
            'gate_type': exercise.gate_type
        }
        
        text = (
            f"Dado un circuito combinacional con variables {', '.join(exercise.vars_name)} "
            f"y salida {exercise.out_name}, definido por la tabla de verdad proporcionada, "
            f"simplifica la función usando un Mapa de Karnaugh."
        )
        
        instructions = (
            f"Utilizando el método de Karnaugh:\n"
            f"1. Coloca los valores en el mapa según las coordenadas\n"
            f"2. Agrupa los unos (o ceros según {exercise.canon_type})\n"
            f"3. Extrae la expresión simplificada\n"
            f"4. Implementa con puertas {exercise.gate_type}"
        )
        
        return Problem.Statement(
            text=text,
            instructions=instructions,
            problem_fields=problem_fields
        )
    
    def _extract_solution(self, exercise: KarnaughExerciseData) -> Problem.Solution:
        """Extrae solución de Karnaugh."""
        explanation = (
            f"El mapa de Karnaugh para {exercise.canon_type} agrupa los valores "
            f"para obtener la expresión simplificada. La solución final implementada "
            f"con puertas {exercise.gate_type} es:"
        )
        
        steps = [
            f"1. Colocar {exercise.canon_type} en el mapa",
            f"2. Agrupar en rectángulos de potencia de 2",
            f"3. Expresión SOP: {exercise.simplified_sop}",
            f"4. Expresión POS: {exercise.simplified_pos}",
            f"5. Implementación {exercise.gate_type}: {getattr(exercise, f'simplified_{exercise.gate_type.lower()}', '...')}"
        ]
        
        solution_fields = {
            'minterms': exercise.minterms,
            'maxterms': exercise.maxterms,
            'simplified_sop': exercise.simplified_sop,
            'simplified_pos': exercise.simplified_pos,
            'simplified_nand': exercise.simplified_nand,
            'simplified_nor': exercise.simplified_nor
        }
        
        return Problem.Solution(
            explanation=explanation,
            steps=steps,
            solution_fields=solution_fields
        )
    
    def _serialize_exercise(self, exercise: KarnaughExerciseData) -> Dict[str, Any]:
        """Serializa KarnaughExerciseData como dict."""
        return asdict(exercise)
    
    def _reconstruct_from_problem_fields(self, problem: Problem) -> KarnaughExerciseData:
        """Reconstruye desde fields."""
        pf = problem.statement.problem_fields
        sf = problem.solution.solution_fields
        
        return KarnaughExerciseData(
            title=problem.metadata.title,
            description=problem.statement.text,
            vars_name=pf['vars_name'],
            out_name=pf['out_name'],
            truth_table_outputs=pf['truth_table_outputs'],
            canon_type=pf['canon_type'],
            gate_type=pf['gate_type'],
            minterms=sf['minterms'],
            maxterms=sf['maxterms'],
            simplified_sop=sf['simplified_sop'],
            simplified_pos=sf['simplified_pos'],
            simplified_nand=sf['simplified_nand'],
            simplified_nor=sf['simplified_nor']
        )
    
    def _deserialize_exercise(self, data: Dict[str, Any]) -> KarnaughExerciseData:
        """Deserializa desde dict."""
        return KarnaughExerciseData(**data)
