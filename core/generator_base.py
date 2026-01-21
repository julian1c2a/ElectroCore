from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Set, Dict, List

@dataclass
class ExerciseData:
    """Clase base para los datos de cualquier ejercicio."""
    title: str
    description: str
    # Los datos específicos se añadirán en las subclases


@dataclass
class ProblemSolutionExerciseData(ExerciseData, ABC):
    """
    INTERFAZ FORMAL: Separa explícitamente parámetros del problema vs solución.
    
    Similar a una clase virtual pura en C++, esta clase abstracta impone que:
    1. Cada subclase defina qué campos son del PROBLEMA
    2. Cada subclase defina qué campos son de la SOLUCIÓN
    3. Estos conjuntos sean DISJUNTOS (sin sobreposición)
    4. Todo campo debe estar en uno de estos dos conjuntos
    
    Ejemplo::
        @dataclass
        class MyExerciseData(ProblemSolutionExerciseData):
            # PROBLEMA
            input_value: int
            
            # SOLUCIÓN
            expected_output: str
            
            @classmethod
            def problem_field_names(cls) -> Set[str]:
                return {"input_value"}
            
            @classmethod
            def solution_field_names(cls) -> Set[str]:
                return {"expected_output"}
    """
    
    @classmethod
    @abstractmethod
    def problem_field_names(cls) -> Set[str]:
        """
        ABSTRACTO: Devuelve los nombres de campos que definen el PROBLEMA.
        
        Estos campos:
        - Aparecen en enunciados (is_solution=False)
        - NO contienen respuestas
        - Son invariantes (no cambian con la solución)
        
        Returns:
            Set de nombres de atributos que son del problema
        """
        pass
    
    @classmethod
    @abstractmethod
    def solution_field_names(cls) -> Set[str]:
        """
        ABSTRACTO: Devuelve los nombres de campos que contienen SOLUCIONES.
        
        Estos campos:
        - Aparecen SOLO en soluciones (is_solution=True), en rojo/resaltado
        - Contienen respuestas correctas
        - Son calculables a partir del problema
        
        Returns:
            Set de nombres de atributos que son soluciones
        """
        pass
    
    def __post_init__(self):
        """Valida que los campos estén correctamente separados."""
        super().__post_init__() if hasattr(super(), '__post_init__') else None
        
        # Obtener los conjuntos de campos
        problem_fields = self.problem_field_names()
        solution_fields = self.solution_field_names()
        
        # Validar que sean disjuntos
        overlap = problem_fields & solution_fields
        if overlap:
            raise ValueError(
                f"Campos en AMBAS categorías (problema y solución): {overlap}\n"
                f"Un campo no puede estar en ambas categorías simultáneamente."
            )
        
        # Obtener todos los campos de la dataclass (excepto title, description)
        all_class_fields = {f.name for f in fields(self) if f.name not in {'title', 'description'}}
        
        # Validar que todo campo esté categorizado
        categorized = problem_fields | solution_fields
        uncategorized = all_class_fields - categorized
        if uncategorized:
            raise ValueError(
                f"Campos no categorizados (no están en problema ni solución): {uncategorized}\n"
                f"Todo campo debe estar explícitamente en problem_field_names() o solution_field_names()."
            )
        
        # Validar que no hay campos extra en las categorías
        extra_problem = problem_fields - all_class_fields
        extra_solution = solution_fields - all_class_fields
        if extra_problem:
            raise ValueError(f"problem_field_names() menciona campos inexistentes: {extra_problem}")
        if extra_solution:
            raise ValueError(f"solution_field_names() menciona campos inexistentes: {extra_solution}")
    
    def to_problem_dict(self) -> Dict[str, Any]:
        """
        Extrae SOLO los parámetros del problema.
        
        Útil para:
        - Generar enunciados
        - Pasar al renderer con is_solution=False
        - Validar que no haya filtraciones
        
        Returns:
            Dict con solo los campos del problema
        """
        problem_fields = self.problem_field_names()
        return {field: getattr(self, field) for field in problem_fields}
    
    def to_solution_dict(self) -> Dict[str, Any]:
        """
        Extrae SOLO los parámetros de la solución.
        
        Útil para:
        - Generar PDFs de soluciones
        - Pasar al renderer con is_solution=True
        - Calificar respuestas del alumno
        
        Returns:
            Dict con solo los campos de solución
        """
        solution_fields = self.solution_field_names()
        return {field: getattr(self, field) for field in solution_fields}
    
    def to_full_dict(self) -> Dict[str, Any]:
        """Devuelve problema + solución (para depuración/logging)."""
        return {
            **self.to_problem_dict(),
            **self.to_solution_dict(),
            'title': self.title,
            'description': self.description
        }
    
    def asdict(self, include_metadata: bool = True) -> Dict[str, Any]:
        """
        Serializa el ejercicio a un Dict limpio, agnóstico y legible por humanos.
        
        Este método es la interfaz de serialización JSON intermedia. Los renderers
        consumen este dict, NO los objetos Python.
        
        La estructura generada es:
        {
            "metadata": { "type": "...", ... },
            "problem": { campos del problema },
            "solution": { campos de solución },
            "title": "...",
            "description": "..."
        }
        
        Args:
            include_metadata: Si incluir info de tipo (recomendado para agnóstico)
        
        Returns:
            Dict con estructura clara separando problema/solución
        """
        result = {
            "title": self.title,
            "description": self.description,
            "problem": self.to_problem_dict(),
            "solution": self.to_solution_dict(),
        }
        
        if include_metadata:
            result["metadata"] = {
                "exercise_type": self.__class__.__name__,
                "module": self.__class__.__module__,
            }
        
        return result


class ExerciseRandomizer(ABC):
    """
    ALEATORIZADOR: Genera parámetros del PROBLEMA de forma aleatoria.
    
    Esta clase es ESTOCÁSTICA: genera valores diferentes según seed.
    RESPONSABILIDADES:
    - Generar valores aleatorios para los campos del problema
    - Respetar la seed para reproducibilidad
    
    IMPORTANTE: NO calcula la solución. Solo genera el problema.
    """
    
    @abstractmethod
    def randomize(self, seed: int | None = None) -> Dict[str, Any]:
        """
        Genera parámetros del problema de forma aleatoria.
        
        Args:
            seed: Semilla para reproducibilidad. Si es None, usa aleatorio del SO.
        
        Returns:
            Dict con los parámetros del problema (SIN solución).
            
        Ejemplo:
            {
                'val_decimal': 157,
                'target_col_idx': 0,
                'representable': True,
                'label': 'N1'
            }
        """
        pass
    
    @property
    @abstractmethod
    def topic(self) -> str:
        """Devuelve el nombre del tema (ej: 'Numeración')."""
        pass


class ExerciseGenerator(ABC):
    """
    GENERADOR: Calcula la SOLUCIÓN a partir de parámetros del PROBLEMA.
    
    Esta clase es DETERMINISTA: mismo problema → misma solución.
    RESPONSABILIDADES:
    - Recibir parámetros del problema (ya definidos)
    - Calcular solución basada en esos parámetros
    - Devolver ejercicio completo (problema + solución)
    
    IMPORTANTE: NO genera valores aleatorios. Los recibe como entrada.
    """
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> ExerciseData:
        """
        MÉTODO PRINCIPAL: Genera ejercicio completo desde parámetros del problema.
        
        ARQUITECTURA ORTOGONAL:
        - El problema viene definido (no se genera aquí)
        - El generador SOLO calcula la solución
        - Es 100% determinista
        
        Args:
            problem_dict: Parámetros del problema ya definidos.
                         Ejemplo: {'val_decimal': 157, 'target_col_idx': 0, ...}
        
        Returns:
            ExerciseData: Ejercicio completo (problema + solución calculada).
        
        Raises:
            ValueError: Si falta algún campo requerido del problema.
            
        NOTA: Por defecto usa generate(). Subclases pueden sobrescribir si necesitan.
        """
        # Default implementation: fallback to legacy generate()
        # Subclases pueden sobrescribir si necesitan comportamiento específico
        return self.generate(difficulty=1)
    
    def generate(self, difficulty: int = 1) -> ExerciseData:
        """
        MÉTODO LEGACY: Compatible hacia atrás.
        
        Por defecto, usa aleatorizador con seed=None.
        Subclases pueden sobrescribir para compatibilidad.
        
        Args:
            difficulty: Nivel de dificultad (1-3).
        
        Returns:
            ExerciseData: Ejercicio generado aleatoriamente.
        """
        # Por defecto: si no hay aleatorizador, error
        raise NotImplementedError(
            f"{self.__class__.__name__} debe implementar generate() "
            "o proporcionar un aleatorizador en ExamBuilder."
        )
    
    @property
    @abstractmethod
    def topic(self) -> str:
        """Devuelve el nombre del tema (ej: 'Numeración')."""
        pass
