from dataclasses import dataclass
from typing import List, Set, Optional
from core.generator_base import ProblemSolutionExerciseData

@dataclass
class LanguageExerciseData(ProblemSolutionExerciseData):
    """
    Datos para ejercicios de Lenguajes Formales (Tema 4.1).
    """
    # --- PROBLEMA (Lo que ve el alumno) ---
    alphabet_symbols: List[str]
    word_length: int
    problem_type: str  # 'counting', 'listing', 'ordering'
    words_to_order: Optional[List[str]] = None
    
    # --- SOLUCIÓN (Lo que ve el profesor) ---
    total_words: int
    valid_words: List[str]
    ordered_words: Optional[List[str]] = None
    explanation: str = ""

    @classmethod
    def problem_field_names(cls) -> Set[str]:
        return {"alphabet_symbols", "word_length", "problem_type", "words_to_order"}

    @classmethod
    def solution_field_names(cls) -> Set[str]:
        return {"total_words", "valid_words", "ordered_words", "explanation"}