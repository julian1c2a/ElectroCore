"""
Mappers: Conversión ExerciseData ↔ Problem.

Cada mapper es responsable de convertir entre:
- ExerciseData (objeto Python específico del tipo)
- Problem (JSON agnóstico para persistencia)

Uso:
    from models.mappers import get_mapper
    
    # Convertir ExerciseData → Problem (para guardar)
    mapper = get_mapper(ProblemType.NUMERACION)
    problem = mapper.exercise_to_problem(conversion_row_data)
    
    # Convertir Problem → ExerciseData (para renderizar)
    exercise = mapper.problem_to_exercise(problem)
"""

from models.mappers.base import ProblemMapper
from models.mappers.numeracion import ConversionRowMapper
from models.mappers.karnaugh import KarnaughMapper
from models.mappers.logic import LogicProblemMapper
from models.mappers.msi import MSIMapper
from models.mappers.secuencial import SequentialMapper
from models.problem_type import ProblemType


# Registro de mappers
MAPPERS = {
    ProblemType.NUMERACION: ConversionRowMapper(),
    ProblemType.KARNAUGH: KarnaughMapper(),
    ProblemType.LOGIC: LogicProblemMapper(),
    ProblemType.MSI: MSIMapper(),
    ProblemType.SECUENCIAL: SequentialMapper(),
}

# Alias para Fase C (ExamBuilder integration)
MAPPER_REGISTRY = MAPPERS


def get_mapper(problem_type: ProblemType) -> ProblemMapper:
    """
    Obtiene el mapper para un tipo de problema.
    
    Args:
        problem_type: ProblemType
    
    Returns:
        ProblemMapper correspondiente
    
    Raises:
        ValueError: Si el tipo no tiene mapper
    
    Ejemplo:
        mapper = get_mapper(ProblemType.NUMERACION)
        problem = mapper.exercise_to_problem(exercise_data)
    """
    if problem_type not in MAPPERS:
        raise ValueError(
            f"No hay mapper para {problem_type}. "
            f"Tipos soportados: {list(MAPPERS.keys())}"
        )
    return MAPPERS[problem_type]


__all__ = [
    'ProblemMapper',
    'ConversionRowMapper',
    'KarnaughMapper',
    'LogicProblemMapper',
    'MSIMapper',
    'SequentialMapper',
    'get_mapper',
    'MAPPERS',
]
