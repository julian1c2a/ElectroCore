#!/usr/bin/env python3
"""
FASE B DEMO: Repository Pattern (Persistencia)

Demuestra:
1. Guardar Problem con FileProblemRepository
2. Cargar Problem desde ficheros
3. Listar con filtros
4. Actualizar y eliminar
5. Mismo codigo con SQLiteProblemRepository
6. Comparacion de backends
"""

import shutil
from pathlib import Path
from modules.numeracion.generators import ConversionRowGenerator
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers import get_mapper
from database import FileProblemRepository, SQLiteProblemRepository


def section(title: str, char: str = "="):
    """Imprime una seccion."""
    print(f"\n{char * 88}")
    print(f"  {title}")
    print(f"{char * 88}\n")


def generate_test_problems(count: int = 5) -> list:
    """Genera varios Problems para testing."""
    problems = []
    generator = ConversionRowGenerator()
    mapper = get_mapper(ProblemType.NUMERACION)
    
    for i in range(count):
        problem_params = {
            'label': chr(ord('a') + (i % 4)),
            'val_decimal': 50 + (i * 20),
            'target_col_idx': i % 4,
            'representable': True
        }
        
        exercise = generator.generate_from_problem(problem_params)
        problem = mapper.exercise_to_problem(exercise, seed=i)
        problem.set_difficulty(1 + (i % 5))
        problem.add_tag("test")
        
        problems.append(problem)
    
    return problems


def demo_file_repo():
    """Demo: FileProblemRepository"""
    section("DEMO 1: FileProblemRepository (JSON Files)", "-")
    
    # Limpiar cualquier repo anterior
    repo_path = "./test_problems_file"
    if Path(repo_path).exists():
        shutil.rmtree(repo_path)
    
    repo = FileProblemRepository(repo_path)
    
    print("1. GENERAR y GUARDAR Problems")
    print("   -------\n")
    
    problems = generate_test_problems(5)
    problem_ids = []
    
    for i, problem in enumerate(problems, 1):
        problem_id = repo.save(problem)
        problem_ids.append(problem_id)
        print(f"   [OK] Guardado: {problem.metadata.title}")
        print(f"        ID: {problem_id[:8]}...")
        print(f"        Dificultad: {problem.metadata.difficulty}\n")
    
    print("2. CARGAR Problem por ID")
    print("   -------\n")
    
    loaded = repo.load(problem_ids[0])
    print(f"   [OK] Cargado: {loaded.metadata.title}")
    print(f"        Valor: {loaded.statement.problem_fields['val_decimal']}")
    print(f"        Respuesta: {loaded.solution.solution_fields['target_val_str']}\n")
    
    print("3. LISTAR todos")
    print("   -------\n")
    
    all_problems = repo.list()
    print(f"   [OK] Total: {len(all_problems)} problems")
    for p in all_problems:
        print(f"        - {p.metadata.title} (dif: {p.metadata.difficulty})\n")
    
    print("4. LISTAR con filtros")
    print("   -------\n")
    
    dificiles = repo.list({"difficulty": 5})
    print(f"   [OK] Difficulty=5: {len(dificiles)} problems")
    
    easy = repo.list({"difficulty": 1})
    print(f"   [OK] Difficulty=1: {len(easy)} problems\n")
    
    print("5. ACTUALIZAR Problem")
    print("   -------\n")
    
    updated = repo.update(problem_ids[0], {
        "metadata.difficulty": 5,
        "metadata.tags": ["importante", "examen"]
    })
    print(f"   [OK] Actualizado: {updated.metadata.title}")
    print(f"        Dificultad: {updated.metadata.difficulty}")
    print(f"        Tags: {updated.metadata.tags}\n")
    
    print("6. ELIMINAR Problem")
    print("   -------\n")
    
    deleted = repo.delete(problem_ids[0])
    print(f"   [OK] Eliminado: {deleted}")
    
    remaining = repo.count()
    print(f"   [OK] Problemas restantes: {remaining}\n")
    
    print("7. INFORMACION del repositorio")
    print("   -------\n")
    
    info = repo.info()
    print(f"   Backend: {info['backend']}")
    print(f"   Ubicacion: {info['location']}")
    print(f"   Total: {info['total']}")
    print(f"   Por tipo: {info['by_type']}")
    print(f"   Por dificultad: {info['by_difficulty']}")
    print(f"   Tamano: {info['size_mb']} MB\n")
    
    return problem_ids


def demo_sqlite_repo():
    """Demo: SQLiteProblemRepository"""
    section("DEMO 2: SQLiteProblemRepository (SQLite)", "-")
    
    # Limpiar DB anterior
    db_path = "./test_problems.db"
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    repo = SQLiteProblemRepository(db_path)
    
    print("1. GENERAR y GUARDAR Problems")
    print("   -------\n")
    
    problems = generate_test_problems(5)
    problem_ids = []
    
    for i, problem in enumerate(problems, 1):
        problem_id = repo.save(problem)
        problem_ids.append(problem_id)
        print(f"   [OK] Guardado: {problem.metadata.title}")
        print(f"        ID: {problem_id[:8]}...")
        print(f"        Dificultad: {problem.metadata.difficulty}\n")
    
    print("2. CARGAR Problem por ID")
    print("   -------\n")
    
    loaded = repo.load(problem_ids[0])
    print(f"   [OK] Cargado: {loaded.metadata.title}")
    print(f"        Valor: {loaded.statement.problem_fields['val_decimal']}")
    print(f"        Respuesta: {loaded.solution.solution_fields['target_val_str']}\n")
    
    print("3. LISTAR con filtros")
    print("   -------\n")
    
    by_difficulty = {}
    for d in range(1, 6):
        count = repo.count({"difficulty": d})
        if count > 0:
            by_difficulty[d] = count
            print(f"   [OK] Difficulty={d}: {count} problems")
    
    print()
    
    print("4. VERIFICAR existencia")
    print("   -------\n")
    
    exists1 = repo.exists(problem_ids[0])
    exists2 = repo.exists("no-existe")
    
    print(f"   [OK] {problem_ids[0][:8]}... existe: {exists1}")
    print(f"   [OK] 'no-existe' existe: {exists2}\n")
    
    print("5. INFORMACION del repositorio")
    print("   -------\n")
    
    info = repo.info()
    print(f"   Backend: {info['backend']}")
    print(f"   Ubicacion: {info['location']}")
    print(f"   Total: {info['total']}")
    print(f"   Por tipo: {info['by_type']}")
    print(f"   Por dificultad: {info['by_difficulty']}")
    print(f"   Tamano: {info['size_mb']} MB\n")
    
    return repo


def demo_comparison():
    """Demo: Comparacion de backends"""
    section("DEMO 3: Comparacion File vs SQLite", "-")
    
    print("Ambos backends tienen la MISMA API:")
    print("   -------\n")
    
    file_repo = FileProblemRepository("./test_problems_file")
    sqlite_repo = SQLiteProblemRepository("./test_problems.db")
    
    print(f"   File repo:      {file_repo}")
    print(f"   SQLite repo:    {sqlite_repo}\n")
    
    print("Mismo codigo funciona en ambos:")
    print("   -------\n")
    
    code = """
    repo = FileProblemRepository("./problems")
    # o
    repo = SQLiteProblemRepository("./problems.db")
    
    # Codigo IDENTICO para ambos:
    repo.save(problem)
    problem = repo.load(problem_id)
    problems = repo.list({"type": "numeracion"})
    repo.delete(problem_id)
    info = repo.info()
    """
    
    for line in code.split('\n'):
        print(f"   {line}")
    
    print()


def main():
    """Ejecuta todos los demos."""
    print("\n" + "=" * 88)
    print(" " * 15 + "FASE B: REPOSITORY PATTERN (Persistencia)")
    print("=" * 88)
    
    try:
        demo_file_repo()
        demo_sqlite_repo()
        demo_comparison()
        
        section("FASE B COMPLETADA CON EXITO", "=")
        
        print("""
RESUMEN:

La Fase B proporciona:

1. [OK] ProblemRepository (ABC)
   - Interface agnóstica para persistencia
   - Métodos: save, load, update, delete, list, count, exists, clear, info
   - Validación integrada
   
2. [OK] FileProblemRepository
   - Guardar en JSON files
   - Estructura: problems_db/tipo/uuid.json
   - Index para búsquedas rápidas
   - Perfecto para desarrollo/testing
   
3. [OK] SQLiteProblemRepository
   - Guardar en SQLite DB
   - Índices para búsqueda rápida
   - Escalable a millones de Problems
   - Queries SQL nativos
   
4. [OK] API Uniforme
   - Mismo código para File y SQLite
   - Fácil cambiar de backend
   - Extensible: agregar MongoDB, PostgreSQL, etc
   
5. [OK] Filtros y Búsquedas
   - Por tipo
   - Por dificultad
   - Por tags
   - Con paginación
   - Con conteos

PROXIMA FASE: Fase C (Integracion con ExamBuilder)
   - ExamBuilder.build() guarda Problems automáticamente
   - Opcion de cargar desde DB
   - Reutilización de problemas
""")
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
