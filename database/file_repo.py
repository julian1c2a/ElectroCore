"""
FileProblemRepository: Guardar Problems en ficheros JSON.

Estructura de directorios:
    problems_db/
    ├── numeracion/
    │   ├── uuid-1.json
    │   ├── uuid-2.json
    │   └── ...
    ├── karnaugh/
    │   ├── uuid-3.json
    │   └── ...
    ├── logic/
    ├── msi/
    ├── secuencial/
    └── _index.json  (metadata de búsqueda rápida)

Ventajas:
- Sin dependencias externas (solo Python)
- Versionable en Git
- Legible (JSON formateado)
- Fácil de debuguear
- Perfecto para desarrollo/testing

Desventajas:
- Lento para muchos Problems (> 10,000)
- Búsquedas lentas (lee todo el index)
- No escalable a múltiples procesos
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.problem import Problem
from models.problem_type import ProblemType
from database.repository import ProblemRepository


class FileProblemRepository(ProblemRepository):
    """
    Repositorio que guarda Problems en ficheros JSON.
    
    Uso:
        repo = FileProblemRepository("./problems_db")
        repo.save(problem)
        problem = repo.load(problem_id)
        all_problems = repo.list()
    """
    
    def __init__(self, base_path: str = "./problems_db"):
        """
        Inicializa el repositorio.
        
        Args:
            base_path: Ruta donde guardar los ficheros (default: ./problems_db)
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Crear subdirectorios por tipo
        for problem_type in ProblemType:
            type_dir = self.base_path / problem_type.value
            type_dir.mkdir(exist_ok=True)
        
        # Index para búsquedas rápidas
        self.index_path = self.base_path / "_index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Crea o restaura el index."""
        if not self.index_path.exists():
            self._rebuild_index()
    
    def _rebuild_index(self):
        """Reconstruye el index leyendo todos los ficheros."""
        index = {}
        
        # Recorrer todos los tipos
        for problem_type in ProblemType:
            type_dir = self.base_path / problem_type.value
            if not type_dir.exists():
                continue
            
            # Leer todos los JSON en este tipo
            for json_file in type_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        problem_data = json.load(f)
                        problem_id = problem_data.get('id')
                        
                        if problem_id:
                            index[problem_id] = {
                                'type': problem_type.value,
                                'file': str(json_file.relative_to(self.base_path)),
                                'metadata': problem_data.get('metadata', {}),
                                'difficulty': problem_data.get('metadata', {}).get('difficulty'),
                                'tags': problem_data.get('metadata', {}).get('tags', []),
                                'created_at': problem_data.get('metadata', {}).get('created_at')
                            }
                except Exception as e:
                    print(f"Error leyendo {json_file}: {e}")
        
        # Guardar index
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _load_index(self) -> Dict[str, Any]:
        """Carga el index desde disco."""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_index(self, index: Dict[str, Any]):
        """Guarda el index a disco."""
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def _get_problem_path(self, problem: Problem) -> Path:
        """Obtiene la ruta del fichero para un Problem."""
        type_dir = self.base_path / problem.type.value
        return type_dir / f"{problem.id}.json"
    
    # ==================== CRUD ====================
    
    def save(self, problem: Problem) -> str:
        """Guarda un Problem a fichero JSON."""
        if not self.validate_problem(problem):
            raise ValueError(f"Problem inválido: {problem}")
        
        # Guardar fichero
        file_path = self._get_problem_path(problem)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(problem.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Actualizar index
        index = self._load_index()
        index[problem.id] = {
            'type': problem.type.value,
            'file': str(file_path.relative_to(self.base_path)),
            'metadata': {k: v for k, v in problem.metadata.__dict__.items() if k != 'id'},
            'difficulty': problem.metadata.difficulty,
            'tags': problem.metadata.tags,
            'created_at': problem.metadata.created_at
        }
        self._save_index(index)
        
        return problem.id
    
    def load(self, problem_id: str) -> Problem:
        """Carga un Problem desde fichero JSON."""
        index = self._load_index()
        
        if problem_id not in index:
            raise FileNotFoundError(f"Problem {problem_id} no encontrado")
        
        file_info = index[problem_id]
        file_path = self.base_path / file_info['file']
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichero {file_path} no encontrado")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            problem_data = json.load(f)
        
        return Problem.from_dict(problem_data)
    
    def update(self, problem_id: str, data: Dict[str, Any]) -> Problem:
        """Actualiza campos de un Problem."""
        problem = self.load(problem_id)
        
        # Aplicar actualizaciones anidadas (ej: "metadata.difficulty": 5)
        for key, value in data.items():
            if '.' in key:
                parts = key.split('.')
                obj = problem
                for part in parts[:-1]:
                    obj = getattr(obj, part)
                setattr(obj, parts[-1], value)
            else:
                setattr(problem, key, value)
        
        problem.mark_updated()
        self.save(problem)
        return problem
    
    def delete(self, problem_id: str) -> bool:
        """Elimina un Problem."""
        index = self._load_index()
        
        if problem_id not in index:
            return False
        
        file_info = index[problem_id]
        file_path = self.base_path / file_info['file']
        
        if file_path.exists():
            file_path.unlink()
        
        del index[problem_id]
        self._save_index(index)
        
        return True
    
    # ==================== LECTURA ====================
    
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Problem]:
        """Lista Problems con filtros opcionales."""
        index = self._load_index()
        problems = []
        
        filters = filters or {}
        problem_type = filters.get('type')
        difficulty = filters.get('difficulty')
        tags = filters.get('tags', [])
        limit = filters.get('limit')
        offset = filters.get('offset', 0)
        
        # Filtrar
        for problem_id, info in index.items():
            # Filtrar por tipo
            if problem_type and info['type'] != problem_type:
                continue
            
            # Filtrar por dificultad
            if difficulty is not None and info['difficulty'] != difficulty:
                continue
            
            # Filtrar por tags (si se especificó alguno, debe estar en el problem)
            if tags and not any(tag in info['tags'] for tag in tags):
                continue
            
            # Cargar problem
            try:
                problem = self.load(problem_id)
                problems.append(problem)
            except Exception as e:
                print(f"Error cargando {problem_id}: {e}")
                continue
        
        # Paginación
        if offset:
            problems = problems[offset:]
        if limit:
            problems = problems[:limit]
        
        return problems
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta Problems con filtros."""
        return len(self.list(filters))
    
    def exists(self, problem_id: str) -> bool:
        """Verifica si un Problem existe."""
        index = self._load_index()
        return problem_id in index
    
    # ==================== LIMPIEZA ====================
    
    def clear(self) -> int:
        """Borra TODOS los Problems."""
        index = self._load_index()
        count = len(index)
        
        # Eliminar todos los ficheros
        for problem_type in ProblemType:
            type_dir = self.base_path / problem_type.value
            if type_dir.exists():
                for json_file in type_dir.glob("*.json"):
                    json_file.unlink()
        
        # Limpiar index
        self._save_index({})
        
        return count
    
    # ==================== INFORMACIÓN ====================
    
    def info(self) -> Dict[str, Any]:
        """Devuelve información del repositorio."""
        index = self._load_index()
        
        # Contar por tipo
        by_type = {}
        for problem_type in ProblemType:
            count = sum(1 for info in index.values() if info['type'] == problem_type.value)
            if count > 0:
                by_type[problem_type.value] = count
        
        # Contar por dificultad
        by_difficulty = {}
        for difficulty in range(1, 6):
            count = sum(1 for info in index.values() if info['difficulty'] == difficulty)
            if count > 0:
                by_difficulty[difficulty] = count
        
        # Tamaño
        total_size = sum(f.stat().st_size for f in self.base_path.rglob("*.json")) / (1024 * 1024)
        
        return {
            'backend': 'file',
            'location': str(self.base_path.absolute()),
            'total': len(index),
            'by_type': by_type,
            'by_difficulty': by_difficulty,
            'size_mb': round(total_size, 2)
        }
