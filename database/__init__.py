"""
Database: Capa de persistencia agnóstica.

Proporciona:
- ProblemRepository (ABC)
- FileProblemRepository (JSON files)
- SQLiteProblemRepository (SQLite)

Uso:
    from database import ProblemRepository, FileProblemRepository, SQLiteProblemRepository
    
    # File-based
    repo = FileProblemRepository("./problems_db")
    
    # o SQLite
    repo = SQLiteProblemRepository("./problems.db")
    
    # API es identica
    repo.save(problem)
    problem = repo.load(problem_id)
    problems = repo.list({"type": "numeracion"})
"""

from database.repository import ProblemRepository
from database.file_repo import FileProblemRepository
from database.sqlite_repo import SQLiteProblemRepository

__all__ = [
    'ProblemRepository',
    'FileProblemRepository',
    'SQLiteProblemRepository',
]
