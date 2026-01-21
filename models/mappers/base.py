"""
Clase base para mappers.

Un Mapper convierte entre:
- ExerciseData (objeto Python específico del tipo)
- Problem (JSON agnóstico para persistencia)

Cada tipo tiene su propio mapper que implementa esta interfaz.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from core.generator_base import ExerciseData
from models.problem import Problem
from models.problem_type import ProblemType


class ProblemMapper(ABC):
    """
    Base para mappers que convierten ExerciseData ↔ Problem.
    
    Un mapper es responsable de:
    1. Convertir ExerciseData → Problem (para persistencia)
    2. Convertir Problem → ExerciseData (para renderizado)
    3. Manejar la separación problema/solución
    4. Preservar todos los datos en ambas direcciones
    
    Implementación de método Template:
    - Subclases implementan métodos específicos del tipo
    - Esta clase orquesta el flujo
    
    Ejemplo:
        mapper = ConversionRowMapper()
        problem = mapper.exercise_to_problem(conversion_row_data)
        exercise = mapper.problem_to_exercise(problem)
    """
    
    @property
    @abstractmethod
    def problem_type(self) -> ProblemType:
        """Devuelve el ProblemType que este mapper maneja."""
        pass
    
    # ==================== CONVERSION EXERCISE → PROBLEM ====================
    
    def exercise_to_problem(
        self,
        exercise: ExerciseData,
        seed: int = None,
        generator_id: str = None
    ) -> Problem:
        """
        Convierte un ExerciseData → Problem.
        
        Template method que orquesta:
        1. Extrae metadata
        2. Extrae statement/solution específicos
        3. Crear Problem con toda la info
        
        Args:
            exercise: ExerciseData del tipo específico
            seed: Semilla usada para generar (si aplica)
            generator_id: ID del generador usado
        
        Returns:
            Problem agnóstico con toda la información
        """
        # 1. Extraer metadata
        metadata = self._extract_metadata(exercise)
        
        # 2. Extraer statement (problema)
        statement = self._extract_statement(exercise)
        
        # 3. Extraer solution (solución)
        solution = self._extract_solution(exercise)
        
        # 4. Crear Problem
        problem = Problem(
            type=self.problem_type,
            metadata=metadata,
            statement=statement,
            solution=solution,
            generator_params=Problem.GeneratorParams(
                seed=seed,
                generator_id=generator_id
            ),
            original_exercise_data=self._serialize_exercise(exercise)
        )
        
        return problem
    
    def _extract_metadata(self, exercise: ExerciseData) -> Problem.Metadata:
        """
        Extrae metadata común de cualquier ExerciseData.
        
        Args:
            exercise: ExerciseData
        
        Returns:
            Problem.Metadata
        """
        return Problem.Metadata(
            title=exercise.title,
            topic=self.problem_type.label,
            difficulty=getattr(exercise, 'difficulty', 1),
            author="system",
            source=self.problem_type.value
        )
    
    @abstractmethod
    def _extract_statement(self, exercise: ExerciseData) -> Problem.Statement:
        """
        Extrae el enunciado (problema) específico del tipo.
        
        Subclases deben implementar:
        - Acceder a campos específicos del exercise
        - Separar qué es "problem_fields" vs instrucciones
        - Crear texto del problema
        
        Args:
            exercise: ExerciseData específico del tipo
        
        Returns:
            Problem.Statement con problema y fields
        """
        pass
    
    @abstractmethod
    def _extract_solution(self, exercise: ExerciseData) -> Problem.Solution:
        """
        Extrae la solución específica del tipo.
        
        Subclases deben implementar:
        - Acceder a campos de solución del exercise
        - Generar explanation y steps si existen
        - Crear solution_fields
        
        Args:
            exercise: ExerciseData específico del tipo
        
        Returns:
            Problem.Solution con solución y fields
        """
        pass
    
    @abstractmethod
    def _serialize_exercise(self, exercise: ExerciseData) -> Dict[str, Any]:
        """
        Serializa el ExerciseData original como dict.
        
        Usado para guardar los datos originales en la DB.
        
        Args:
            exercise: ExerciseData
        
        Returns:
            Dict serializable
        """
        pass
    
    # ==================== CONVERSION PROBLEM → EXERCISE ====================
    
    def problem_to_exercise(self, problem: Problem) -> ExerciseData:
        """
        Convierte un Problem → ExerciseData.
        
        Template method que:
        1. Valida que sea del tipo correcto
        2. Reconstruye el ExerciseData desde Problem
        
        Args:
            problem: Problem agnóstico
        
        Returns:
            ExerciseData específico del tipo
        
        Raises:
            ValueError: Si el tipo del Problem no coincide
        """
        if problem.type != self.problem_type:
            raise ValueError(
                f"Tipo mismatch: Problem es {problem.type}, "
                f"pero este mapper maneja {self.problem_type}"
            )
        
        # Si tenemos los datos originales, usarlos
        if problem.original_exercise_data:
            return self._deserialize_exercise(problem.original_exercise_data)
        
        # Si no, reconstruir desde los fields
        return self._reconstruct_from_problem_fields(problem)
    
    @abstractmethod
    def _reconstruct_from_problem_fields(self, problem: Problem) -> ExerciseData:
        """
        Reconstruye un ExerciseData desde los fields del Problem.
        
        Usado cuando no tenemos los datos originales.
        
        Args:
            problem: Problem agnóstico
        
        Returns:
            ExerciseData reconstruido
        """
        pass
    
    @abstractmethod
    def _deserialize_exercise(self, data: Dict[str, Any]) -> ExerciseData:
        """
        Deserializa un ExerciseData desde dict.
        
        Args:
            data: Dict serializado con los datos
        
        Returns:
            ExerciseData reconstruido
        """
        pass
    
    # ==================== UTILIDADES ====================
    
    def validate_problem(self, problem: Problem) -> bool:
        """
        Valida que un Problem sea válido para este mapper.
        
        Args:
            problem: Problem a validar
        
        Returns:
            True si es válido, False si no
        """
        return problem.type == self.problem_type and \
               problem.statement.problem_fields and \
               problem.solution.solution_fields
    
    def __repr__(self) -> str:
        """Representación legible del mapper."""
        return f"{self.__class__.__name__}(handles={self.problem_type.value})"
