"""
ProblemRepository: Interfaz abstracta para persistencia agnóstica.

Un repositorio es responsable de:
1. CREAR: Guardar un nuevo Problem
2. LEER: Cargar un Problem por ID
3. ACTUALIZAR: Modificar un Problem existente
4. ELIMINAR: Borrar un Problem
5. LISTAR: Recuperar Problems según filtros

La implementación es agnóstica: puede ser File, SQLite, MongoDB, etc.
El código cliente nunca conoce detalles de la persistencia.

Ejemplo:
    repo = FileProblemRepository("./problems_db")
    # o
    repo = SQLiteProblemRepository("./problems.db")
    # o
    repo = MongoDBProblemRepository("mongodb://...")
    
    # El código es IDÉNTICO para todos los backends:
    problem_id = repo.save(problem)
    problem = repo.load(problem_id)
    problems = repo.list({"type": "numeracion", "difficulty": 3})
    repo.delete(problem_id)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from models.problem import Problem
from models.problem_type import ProblemType


class ProblemRepository(ABC):
    """
    Interfaz abstracta para repositorios de Problems.
    
    Define el contrato que TODA implementación debe cumplir.
    """
    
    # ==================== CRUD ====================
    
    @abstractmethod
    def save(self, problem: Problem) -> str:
        """
        Guarda un Problem (nuevo o actualización).
        
        Si el Problem tiene ID vacío, genera uno nuevo.
        Si tiene ID, actualiza el existente.
        
        Args:
            problem: Problem a guardar
        
        Returns:
            ID del problem guardado (str UUID)
        
        Raises:
            IOError: Si hay error al guardar
            ValueError: Si el Problem es inválido
        
        Ejemplo:
            problem_id = repo.save(problem)
            print(f"Guardado con ID: {problem_id}")
        """
        pass
    
    @abstractmethod
    def load(self, problem_id: str) -> Problem:
        """
        Carga un Problem por ID.
        
        Args:
            problem_id: ID del Problem (UUID string)
        
        Returns:
            Problem completo
        
        Raises:
            FileNotFoundError: Si el Problem no existe
            IOError: Si hay error al leer
        
        Ejemplo:
            problem = repo.load("uuid-1234")
        """
        pass
    
    @abstractmethod
    def update(self, problem_id: str, data: Dict[str, Any]) -> Problem:
        """
        Actualiza campos específicos de un Problem.
        
        Args:
            problem_id: ID del Problem
            data: Dict con campos a actualizar
                 {"metadata.difficulty": 4, "metadata.tags": [...]}
        
        Returns:
            Problem actualizado
        
        Raises:
            FileNotFoundError: Si el Problem no existe
            IOError: Si hay error al actualizar
        
        Ejemplo:
            problem = repo.update(
                "uuid-1234",
                {"metadata.difficulty": 5, "metadata.tags": ["importante"]}
            )
        """
        pass
    
    @abstractmethod
    def delete(self, problem_id: str) -> bool:
        """
        Elimina un Problem por ID.
        
        Args:
            problem_id: ID del Problem
        
        Returns:
            True si se eliminó, False si no existía
        
        Raises:
            IOError: Si hay error al eliminar
        
        Ejemplo:
            deleted = repo.delete("uuid-1234")
        """
        pass
    
    # ==================== LECTURA ====================
    
    @abstractmethod
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Problem]:
        """
        Lista Problems según filtros opcionales.
        
        Args:
            filters: Dict de filtros (opcional)
                {
                    "type": "numeracion",
                    "difficulty": 3,
                    "tags": ["importante"],
                    "limit": 10,
                    "offset": 0
                }
        
        Returns:
            Lista de Problems (puede estar vacía)
        
        Raises:
            IOError: Si hay error al listar
        
        Ejemplo:
            # Todos los problemas
            all_problems = repo.list()
            
            # Filtradores
            numeracion = repo.list({"type": "numeracion"})
            dificiles = repo.list({"difficulty": 5})
            ambos = repo.list({"type": "karnaugh", "difficulty": 4})
            
            # Con paginación
            page1 = repo.list({"limit": 10, "offset": 0})
            page2 = repo.list({"limit": 10, "offset": 10})
        """
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Cuenta Problems según filtros opcionales.
        
        Args:
            filters: Dict de filtros (mismo formato que list())
        
        Returns:
            Cantidad de Problems que coinciden
        
        Raises:
            IOError: Si hay error al contar
        
        Ejemplo:
            total = repo.count()
            numeracion_count = repo.count({"type": "numeracion"})
        """
        pass
    
    @abstractmethod
    def exists(self, problem_id: str) -> bool:
        """
        Verifica si un Problem existe.
        
        Args:
            problem_id: ID a verificar
        
        Returns:
            True si existe, False si no
        
        Ejemplo:
            if repo.exists("uuid-1234"):
                print("El problema existe")
        """
        pass
    
    # ==================== LIMPIEZA ====================
    
    @abstractmethod
    def clear(self) -> int:
        """
        Borra TODOS los Problems del repositorio.
        
        ¡PELIGROSO! Úsalo solo para testing.
        
        Returns:
            Cantidad de Problems eliminados
        
        Ejemplo:
            deleted_count = repo.clear()
            print(f"Se eliminaron {deleted_count} problemas")
        """
        pass
    
    # ==================== INFORMACIÓN ====================
    
    @abstractmethod
    def info(self) -> Dict[str, Any]:
        """
        Devuelve información del repositorio.
        
        Returns:
            Dict con información:
            {
                "backend": "file" | "sqlite" | "mongodb",
                "location": "/path/to/db" o "mongodb://...",
                "total": 42,
                "by_type": {"numeracion": 15, "karnaugh": 10, ...},
                "by_difficulty": {1: 5, 2: 10, 3: 15, ...},
                "size_mb": 1.23
            }
        
        Ejemplo:
            info = repo.info()
            print(f"Total de problemas: {info['total']}")
        """
        pass
    
    # ==================== UTILIDADES ====================
    
    def validate_problem(self, problem: Problem) -> bool:
        """
        Valida que un Problem sea válido para guardar.
        
        Implementación por defecto (puede ser overrideada).
        
        Args:
            problem: Problem a validar
        
        Returns:
            True si es válido, False si no
        """
        return (
            problem.type is not None and
            problem.metadata.title and
            problem.statement.text and
            problem.statement.problem_fields
        )
    
    def get_by_type(self, problem_type: ProblemType) -> List[Problem]:
        """
        Obtiene todos los Problems de un tipo específico.
        
        Implementación por defecto usando list().
        
        Args:
            problem_type: ProblemType a filtrar
        
        Returns:
            Lista de Problems del tipo
        """
        return self.list({"type": problem_type.value})
    
    def get_by_difficulty(self, difficulty: int) -> List[Problem]:
        """
        Obtiene todos los Problems con dificultad específica.
        
        Implementación por defecto usando list().
        
        Args:
            difficulty: 1-5
        
        Returns:
            Lista de Problems con esa dificultad
        """
        return self.list({"difficulty": difficulty})
    
    def get_by_tag(self, tag: str) -> List[Problem]:
        """
        Obtiene todos los Problems con un tag específico.
        
        Implementación por defecto usando list().
        
        Args:
            tag: Tag a buscar
        
        Returns:
            Lista de Problems con ese tag
        """
        return self.list({"tags": [tag]})
    
    def __repr__(self) -> str:
        """Representación legible del repositorio."""
        info = self.info()
        return (
            f"{self.__class__.__name__}("
            f"backend={info['backend']}, "
            f"location={info['location']}, "
            f"total={info['total']})"
        )
