"""
SQLiteProblemRepository: Guardar Problems en base de datos SQLite.

Ventajas:
- Rápido para búsquedas
- Soporte para queries complejas
- Sin dependencias externas (SQLite está en Python)
- Scalable a millones de Problems
- Transacciones ACID

Esquema:
    problems (tabla)
    ├── id (TEXT PRIMARY KEY)
    ├── type (TEXT)
    ├── data (TEXT) - JSON blob
    ├── difficulty (INTEGER)
    ├── created_at (TEXT)
    ├── updated_at (TEXT)
    └── índices para búsqueda rápida

Uso:
    repo = SQLiteProblemRepository("./problems.db")
    repo.save(problem)
    repo.load(problem_id)
    repo.list({"type": "numeracion", "difficulty": 4})
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from models.problem import Problem
from models.problem_type import ProblemType
from database.repository import ProblemRepository


class SQLiteProblemRepository(ProblemRepository):
    """
    Repositorio que guarda Problems en base de datos SQLite.
    
    Uso:
        repo = SQLiteProblemRepository("./problems.db")
        repo.save(problem)
        problem = repo.load(problem_id)
        all_problems = repo.list()
    """
    
    def __init__(self, db_path: str = "./problems.db"):
        """
        Inicializa el repositorio SQLite.
        
        Args:
            db_path: Ruta de la base de datos SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_schema()
    
    def _get_connection(self):
        """Obtiene una conexión a la BD."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_schema(self):
        """Crea el esquema de la BD si no existe."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tabla principal
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS problems (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                data TEXT NOT NULL,
                difficulty INTEGER,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        # Índices para búsqueda rápida
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON problems(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_difficulty ON problems(difficulty)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON problems(created_at)")
        
        conn.commit()
        conn.close()
    
    # ==================== CRUD ====================
    
    def save(self, problem: Problem) -> str:
        """Guarda un Problem en la BD."""
        if not self.validate_problem(problem):
            raise ValueError(f"Problem inválido: {problem}")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        problem_json = json.dumps(problem.to_dict(), ensure_ascii=False)
        
        cursor.execute("""
            INSERT OR REPLACE INTO problems
            (id, type, data, difficulty, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            problem.id,
            problem.type.value,
            problem_json,
            problem.metadata.difficulty,
            problem.metadata.created_at,
            problem.metadata.updated_at
        ))
        
        conn.commit()
        conn.close()
        
        return problem.id
    
    def load(self, problem_id: str) -> Problem:
        """Carga un Problem de la BD."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM problems WHERE id = ?", (problem_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise FileNotFoundError(f"Problem {problem_id} no encontrado")
        
        problem_data = json.loads(row['data'])
        return Problem.from_dict(problem_data)
    
    def update(self, problem_id: str, data: Dict[str, Any]) -> Problem:
        """Actualiza campos de un Problem."""
        problem = self.load(problem_id)
        
        # Aplicar actualizaciones anidadas
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
        """Elimina un Problem de la BD."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
        affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return affected > 0
    
    # ==================== LECTURA ====================
    
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[Problem]:
        """Lista Problems con filtros opcionales."""
        filters = filters or {}
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Construir query
        query = "SELECT data FROM problems WHERE 1=1"
        params = []
        
        if 'type' in filters:
            query += " AND type = ?"
            params.append(filters['type'])
        
        if 'difficulty' in filters:
            query += " AND difficulty = ?"
            params.append(filters['difficulty'])
        
        # Orden
        query += " ORDER BY created_at DESC"
        
        # Paginación
        limit = filters.get('limit')
        offset = filters.get('offset', 0)
        
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Cargar Problems
        problems = []
        for row in rows:
            try:
                problem_data = json.loads(row['data'])
                problem = Problem.from_dict(problem_data)
                
                # Filtrar por tags si es necesario
                tags_filter = filters.get('tags', [])
                if tags_filter and not any(tag in problem.metadata.tags for tag in tags_filter):
                    continue
                
                problems.append(problem)
            except Exception as e:
                print(f"Error cargando problem: {e}")
                continue
        
        return problems
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta Problems con filtros."""
        filters = filters or {}
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) as cnt FROM problems WHERE 1=1"
        params = []
        
        if 'type' in filters:
            query += " AND type = ?"
            params.append(filters['type'])
        
        if 'difficulty' in filters:
            query += " AND difficulty = ?"
            params.append(filters['difficulty'])
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        
        return row['cnt'] if row else 0
    
    def exists(self, problem_id: str) -> bool:
        """Verifica si un Problem existe."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM problems WHERE id = ?", (problem_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    # ==================== LIMPIEZA ====================
    
    def clear(self) -> int:
        """Borra TODOS los Problems."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as cnt FROM problems")
        count = cursor.fetchone()['cnt']
        
        cursor.execute("DELETE FROM problems")
        conn.commit()
        conn.close()
        
        return count
    
    # ==================== INFORMACIÓN ====================
    
    def info(self) -> Dict[str, Any]:
        """Devuelve información del repositorio."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total
        cursor.execute("SELECT COUNT(*) as cnt FROM problems")
        total = cursor.fetchone()['cnt']
        
        # Por tipo
        cursor.execute("""
            SELECT type, COUNT(*) as cnt 
            FROM problems 
            GROUP BY type
        """)
        by_type = {row['type']: row['cnt'] for row in cursor.fetchall()}
        
        # Por dificultad
        cursor.execute("""
            SELECT difficulty, COUNT(*) as cnt 
            FROM problems 
            GROUP BY difficulty
        """)
        by_difficulty = {row['difficulty']: row['cnt'] for row in cursor.fetchall()}
        
        conn.close()
        
        # Tamaño
        size_mb = self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0
        
        return {
            'backend': 'sqlite',
            'location': str(self.db_path.absolute()),
            'total': total,
            'by_type': by_type,
            'by_difficulty': by_difficulty,
            'size_mb': round(size_mb, 2)
        }
