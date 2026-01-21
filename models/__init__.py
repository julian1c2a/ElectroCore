"""
Models: Clases agnósticas para persistencia.

Proporciona:
- Problem: Representación agnóstica de un ejercicio
- ProblemType: Enum de tipos soportados
- Mappers: Conversión ExerciseData ↔ Problem
"""

from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers import (
    get_mapper,
    ProblemMapper,
    ConversionRowMapper,
    KarnaughMapper,
    LogicProblemMapper,
    MSIMapper,
    SequentialMapper,
)

__all__ = [
    'Problem',
    'ProblemType',
    'get_mapper',
    'ProblemMapper',
    'ConversionRowMapper',
    'KarnaughMapper',
    'LogicProblemMapper',
    'MSIMapper',
    'SequentialMapper',
]
