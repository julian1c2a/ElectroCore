"""
Mapper para problemas de Representación Numérica (ConversionRow).

Convierte entre:
- ConversionRow (ExerciseData Python)
- Problem (JSON agnóstico)
"""

from typing import Any, Dict
from dataclasses import asdict
from modules.numeracion.models import ConversionRow, COLUMN_NAMES
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers.base import ProblemMapper


class ConversionRowMapper(ProblemMapper):
    """
    Mapper para ConversionRow (conversiones de bases numéricas).
    
    Responsabilidades:
    - ExerciseData ConversionRow → Problem agnóstico
    - Problem agnóstico → ExerciseData ConversionRow
    - Preservar todos los campos específicos del problema
    - Generar explicaciones legibles
    """
    
    @property
    def problem_type(self) -> ProblemType:
        return ProblemType.NUMERACION
    
    # ==================== EXERCISE → PROBLEM ====================
    
    def _extract_statement(self, exercise: ConversionRow) -> Problem.Statement:
        """
        Extrae el enunciado de un ConversionRow.
        
        El enunciado incluye:
        - Texto describiendo el problema
        - Instrucciones
        - Campos específicos del problema
        
        Args:
            exercise: ConversionRow
        
        Returns:
            Problem.Statement
        """
        # Extraer campos del problema
        problem_fields = {
            'label': exercise.label,
            'val_decimal': exercise.val_decimal,
            'target_col_idx': exercise.target_col_idx,
            'representable': exercise.representable
        }
        
        # Generar texto descriptivo
        target_system = exercise.target_system
        text = (
            f"Convierte el valor decimal {exercise.val_decimal} "
            f"a su representación en {target_system}."
        )
        
        instructions = (
            f"Realizando la conversión del número decimal {exercise.val_decimal} "
            f"hacia el sistema {target_system}, escribe el resultado usando "
            f"únicamente dígitos válidos para dicha base."
        )
        
        return Problem.Statement(
            text=text,
            instructions=instructions,
            problem_fields=problem_fields
        )
    
    def _extract_solution(self, exercise: ConversionRow) -> Problem.Solution:
        """
        Extrae la solución de un ConversionRow.
        
        Args:
            exercise: ConversionRow
        
        Returns:
            Problem.Solution con explicación y solución
        """
        # Generar explicación
        target_system = exercise.target_system
        explanation = (
            f"Para convertir {exercise.val_decimal} a {target_system}, "
            f"se utilizan divisiones sucesivas u otros métodos según el sistema. "
            f"El resultado es: {exercise.target_val_str}"
        )
        
        # Steps (proceso de conversión)
        steps = self._generate_conversion_steps(exercise)
        
        # Soluciones para todas las columnas
        solution_fields = {
            'target_val_str': exercise.target_val_str,
            'sol_bin': exercise.sol_bin,
            'sol_c2': exercise.sol_c2,
            'sol_sm': exercise.sol_sm,
            'sol_bcd': exercise.sol_bcd
        }
        
        return Problem.Solution(
            explanation=explanation,
            steps=steps,
            solution_fields=solution_fields
        )
    
    def _generate_conversion_steps(self, exercise: ConversionRow) -> list:
        """
        Genera pasos detallados de la conversión.
        
        Args:
            exercise: ConversionRow
        
        Returns:
            Lista de strings describiendo los pasos
        """
        steps = []
        val = abs(exercise.val_decimal)
        
        if exercise.target_col_idx == 0:  # Binario Natural
            steps.append(f"Dividir {val} entre 2 sucesivamente:")
            while val > 0:
                remainder = val % 2
                val //= 2
                steps.append(f"  {val} × 2 + {remainder}")
            steps.append(f"Leer restos de abajo a arriba: {exercise.target_val_str}")
        
        elif exercise.target_col_idx == 1:  # C2
            if exercise.val_decimal >= 0:
                steps.append(f"Como {exercise.val_decimal} >= 0, usar representación binaria positiva")
                steps.append(f"Resultado: {exercise.target_val_str}")
            else:
                steps.append(f"Como {exercise.val_decimal} < 0, usar complemento a 2")
                steps.append(f"1. Binario de {abs(exercise.val_decimal)}: {bin(abs(exercise.val_decimal))[2:].zfill(8)}")
                steps.append(f"2. Invertir bits y sumar 1")
                steps.append(f"Resultado: {exercise.target_val_str}")
        
        elif exercise.target_col_idx == 2:  # Signo-Magnitud
            steps.append(f"Bit de signo: {'1' if exercise.val_decimal < 0 else '0'}")
            steps.append(f"Magnitud: {exercise.target_val_str[1:] if exercise.val_decimal < 0 else exercise.target_val_str[1:]}")
            steps.append(f"Resultado: {exercise.target_val_str}")
        
        elif exercise.target_col_idx == 3:  # BCD
            steps.append(f"BCD: cada dígito decimal → 4 bits binarios")
            steps.append(f"Resultado: {exercise.target_val_str}")
        
        return steps
    
    def _serialize_exercise(self, exercise: ConversionRow) -> Dict[str, Any]:
        """Serializa ConversionRow como dict."""
        return asdict(exercise)
    
    # ==================== PROBLEM → EXERCISE ====================
    
    def _reconstruct_from_problem_fields(self, problem: Problem) -> ConversionRow:
        """
        Reconstruye un ConversionRow desde los fields del Problem.
        
        Args:
            problem: Problem agnóstico
        
        Returns:
            ConversionRow reconstruido
        """
        problem_fields = problem.statement.problem_fields
        solution_fields = problem.solution.solution_fields
        
        return ConversionRow(
            # Heredados
            title=problem.metadata.title,
            description=problem.statement.text,
            
            # Problema
            label=problem_fields['label'],
            val_decimal=problem_fields['val_decimal'],
            target_col_idx=problem_fields['target_col_idx'],
            representable=problem_fields['representable'],
            
            # Solución
            target_val_str=solution_fields['target_val_str'],
            sol_bin=solution_fields['sol_bin'],
            sol_c2=solution_fields['sol_c2'],
            sol_sm=solution_fields['sol_sm'],
            sol_bcd=solution_fields['sol_bcd']
        )
    
    def _deserialize_exercise(self, data: Dict[str, Any]) -> ConversionRow:
        """
        Deserializa un ConversionRow desde dict.
        
        Args:
            data: Dict con los datos
        
        Returns:
            ConversionRow reconstruido
        """
        return ConversionRow(**data)
