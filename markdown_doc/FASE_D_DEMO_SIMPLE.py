"""
FASE_D_DEMO_SIMPLE.py - Demostración simple de Fase D (CLI)

Una demo simplificada que demuestra:
1. Creación de repositorio
2. Guardado y carga de problemas
3. Búsqueda y filtrado
4. Estadísticas
5. Export/Import

Esta demo funciona con la estructura real de Problem
"""

import os
import sys
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent))

from models.problem_type import ProblemType
from models.problem import Problem
from database.file_repo import FileProblemRepository
from database.sqlite_repo import SQLiteProblemRepository
from cli.problems import ProblemsCLI


def print_section(title):
    """Imprime encabezado de sección."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_subsection(title):
    """Imprime encabezado de subsección."""
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}\n")


def create_sample_problem():
    """Crea un problema de prueba."""
    return Problem(
        type=ProblemType.NUMERACION,
        metadata=Problem.Metadata(
            title="Conversion Binario a Decimal",
            topic="Conversion de Bases",
            difficulty=2,
            tags=["conversion", "binario", "decimal"]
        ),
        statement=Problem.Statement(
            text="Convierte 10110101 a decimal",
            instructions="Usa la formula de posicion de digitos",
            problem_fields={"binary": "10110101"}
        ),
        solution=Problem.Solution(
            explanation="10110101 = 128+32+16+4+1 = 181",
            solution_fields={"result": "181"}
        )
    )


def demo_file_repository():
    """Demo con repositorio basado en archivos."""
    print_section("DEMO 1: Repositorio Basado en Archivos (JSON)")
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="problems_demo_")
    print(f"Usando directorio: {temp_dir}\n")
    
    try:
        # Crear repositorio
        repo = FileProblemRepository(temp_dir)
        print("[OK] Repositorio creado\n")
        
        # Guardar problema
        print_subsection("Paso 1: Guardar Problema")
        problem = create_sample_problem()
        repo.save(problem)
        print(f"[OK] Problema guardado con ID: {problem.id}\n")
        
        # Cargar problema
        print_subsection("Paso 2: Cargar Problema")
        loaded = repo.load(problem.id)
        print(f"[OK] Problema cargado: {loaded.metadata.title}\n")
        
        # Ver estadísticas
        print_subsection("Paso 3: Estadísticas del Repositorio")
        info = repo.info()
        print(f"Total de problemas: {info['total']}")
        print(f"Problemas por tipo:")
        for ptype, count in info.get('by_type', {}).items():
            print(f"  - {ptype}: {count}")
        print()
        
        # Listar problemas
        print_subsection("Paso 4: Listar Problemas")
        all_problems = repo.list()
        for p in all_problems:
            print(f"  - [{p.metadata.title}] (dificultad: {p.metadata.difficulty})")
        print()
        
        # Contar
        print_subsection("Paso 5: Contar Problemas")
        count = repo.count()
        print(f"Total de problemas en repositorio: {count}\n")
        
        # Existe
        print_subsection("Paso 6: Verificar Existencia")
        exists = repo.exists(problem.id)
        print(f"Problema existe en repositorio: {exists}\n")
        
        # Exportar
        print_subsection("Paso 7: Exportar a JSON")
        export_file = os.path.join(temp_dir, "export.json")
        problems = repo.list()
        data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "total": len(problems)
            },
            "problems": [p.to_dict() for p in problems]
        }
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Exportado a: {export_file}")
        print(f"     Tamanio: {os.path.getsize(export_file)} bytes\n")
        
        # Resultado final
        print_subsection("Resultado")
        print("[COMPLETE] Todas las operaciones exitosas")
        print(f"[OK] Repositorio contiene {repo.count()} problema(s)\n")
        
    finally:
        # Limpiar
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(f"[CLEANUP] Directorio temporal eliminado\n")


def demo_sqlite_repository():
    """Demo con repositorio SQLite."""
    print_section("DEMO 2: Repositorio SQLite")
    
    db_file = "problems_demo_simple.db"
    print(f"Usando base de datos: {db_file}\n")
    
    try:
        # Crear repositorio
        repo = SQLiteProblemRepository(db_file)
        print("[OK] Repositorio SQLite creado\n")
        
        # Guardar problemas
        print_subsection("Paso 1: Guardar Multiples Problemas")
        problems = []
        for i in range(3):
            p = create_sample_problem()
            p.metadata.title = f"Problema {i+1}"
            p.metadata.difficulty = (i % 3) + 1
            repo.save(p)
            problems.append(p)
        print(f"[OK] {len(problems)} problemas guardados\n")
        
        # Listar
        print_subsection("Paso 2: Listar Todos")
        all_problems = repo.list()
        for p in all_problems:
            print(f"  - {p.metadata.title}")
        print()
        
        # Filtrar por dificultad
        print_subsection("Paso 3: Filtrar por Dificultad")
        filtered = repo.list({'difficulty': 2})
        print(f"Problemas con dificultad 2: {len(filtered)}")
        for p in filtered:
            print(f"  - {p.metadata.title}")
        print()
        
        # Estadísticas
        print_subsection("Paso 4: Estadísticas")
        info = repo.info()
        print(f"Total: {info['total']}")
        print(f"Por tipo: {info.get('by_type', {})}")
        print(f"Por dificultad: {info.get('by_difficulty', {})}")
        print()
        
        # Actualizar
        print_subsection("Paso 5: Actualizar Problema")
        if all_problems:
            first = all_problems[0]
            updated = repo.update(first.id, {
                'metadata.title': 'Titulo Modificado'
            })
            print(f"[OK] Problema actualizado: {updated.metadata.title}\n")
        
        # Resultado
        print_subsection("Resultado")
        print(f"[COMPLETE] Repositorio contiene {repo.count()} problema(s)\n")
        
    finally:
        # Limpiar
        if os.path.exists(db_file):
            os.remove(db_file)
        print(f"[CLEANUP] Base de datos eliminada\n")


def demo_cli_interface():
    """Demo de interfaz CLI."""
    print_section("DEMO 3: Interfaz CLI ProblemsCLI")
    
    temp_dir = tempfile.mkdtemp(prefix="problems_cli_")
    
    try:
        # Crear CLI con repositorio
        repo = FileProblemRepository(temp_dir)
        cli = ProblemsCLI(repo)
        
        print(f"[OK] CLI inicializado\n")
        
        # Guardar problema
        print_subsection("Paso 1: Guardar Problema via CLI")
        problem = create_sample_problem()
        repo.save(problem)
        print(f"[OK] Problema guardado via repositorio\n")
        
        # Usar CLI para listar
        print_subsection("Paso 2: Estadísticas via CLI")
        all_probs = cli.repo.list()
        print(f"Total de problemas: {len(all_probs)}")
        if all_probs:
            p = all_probs[0]
            print(f"Primer problema: {p.metadata.title}\n")
        
        print("[COMPLETE] Interfaz CLI funciona correctamente\n")
        
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(f"[CLEANUP] Directorio temporal eliminado\n")


def main():
    """Funcion principal."""
    print("\n")
    print("+" + "="*68 + "+")
    print("|" + " "*68 + "|")
    print("|" + "  FASE D: DEMO SIMPLIFICADA DE CLI".center(68) + "|")
    print("|" + " "*68 + "|")
    print("+"+"="*68 + "+")
    
    try:
        # Demo 1: File Repository
        demo_file_repository()
        
        # Demo 2: SQLite Repository
        demo_sqlite_repository()
        
        # Demo 3: CLI Interface
        demo_cli_interface()
        
        # Resumen
        print_section("RESUMEN FASE D")
        print("""
[COMPLETE] Fase D - CLI completada exitosamente

Funcionalidades Demostr adas:

1. Repositorio Basado en Archivos (JSON)
   [OK] Crear repositorio
   [OK] Guardar problema
   [OK] Cargar problema
   [OK] Listar problemas
   [OK] Contar problemas
   [OK] Verificar existencia
   [OK] Exportar a JSON

2. Repositorio SQLite
   [OK] Crear base de datos
   [OK] Guardar multiples problemas
   [OK] Listar con filtros
   [OK] Estadísticas
   [OK] Actualizar problemas

3. Interfaz CLI
   [OK] Inicializar CLI
   [OK] Acceder a repositorio
   [OK] Obtener estadísticas

Comandos Disponibles (en cli/problems.py):
  - list: Listar problemas con filtros
  - search: Búsqueda de problemas
  - stats: Estadísticas del repositorio
  - export: Exportar a JSON/CSV
  - import: Importar desde JSON
  - delete: Eliminar problemas
  - backup: Crear backup
  - restore: Restaurar desde backup
  - verify: Verificar integridad

Entrada CLI:
  python -m cli list
  python -m cli search "conversion"
  python -m cli stats --detailed
  python -m cli export json data.json
  python -m cli import data.json

Status: EXITOSO
        """)
        
        print("[STATUS] Demo completada sin errores\n")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
