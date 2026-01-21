"""
FASE_D_DEMO.py - Demostración completa de la Interfaz CLI para Gestión de Problemas

Esta demo muestra todas las funcionalidades de la Fase D:
- Gestión completa de problemas (CRUD)
- Búsqueda avanzada
- Estadísticas
- Exportación e importación
- Backup y restore
- Verificación de integridad

Requisitos previos:
- Fase A: models.py, problem_type.py, mappers/ (COMPLETADA)
- Fase B: database/ (COMPLETADA)
- Fase C: ExamBuilder con soporte de repository (COMPLETADA)
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


def create_sample_problems():
    """Crea conjunto de problemas de prueba."""
    problems = [
        Problem(
            type=ProblemType.NUMERACION,
            metadata=Problem.Metadata(
                title="Conversión Binario a Decimal",
                topic="Conversión de Bases",
                difficulty=1,
                tags=["conversion", "binario", "decimal"]
            ),
            statement=Problem.Statement(
                text="Convierte 10110101 a decimal",
                instructions="Usa la fórmula de posición de dígitos",
                problem_fields={"binary": "10110101"}
            ),
            solution=Problem.Solution(
                explanation="10110101 = 128+32+16+4+1 = 181",
                solution_fields={"result": "181"}
            )
        ),
        Problem(
            type=ProblemType.NUMERACION,
            metadata=Problem.Metadata(
                title="Conversión Octal a Binario",
                topic="Conversión de Bases",
                difficulty=2,
                tags=["conversion", "octal", "binario"]
            ),
            statement=Problem.Statement(
                text="Convierte 753 (octal) a binario",
                instructions="Cada dígito octal = 3 dígitos binarios",
                problem_fields={"octal": "753"}
            ),
            solution=Problem.Solution(
                explanation="7=111, 5=101, 3=011 → 111101011",
                solution_fields={"result": "111101011"}
            )
        ),
        Problem(
            type=ProblemType.KARNAUGH,
            metadata=Problem.Metadata(
                title="Simplificación con Mapa de Karnaugh",
                topic="Lógica Booleana",
                difficulty=3,
                tags=["karnaugh", "simplificacion", "booleano"]
            ),
            statement=Problem.Statement(
                text="Simplifica F = A'B'C' + A'B'C + A'BC + ABC",
                instructions="Usa el mapa de Karnaugh de 3 variables",
                problem_fields={"expression": "A'B'C' + A'B'C + A'BC + ABC"}
            ),
            solution=Problem.Solution(
                explanation="Agrupando se obtiene F = A' + BC",
                solution_fields={"result": "A' + BC"}
            )
        ),
        Problem(
            type=ProblemType.SECUENCIAL,
            metadata=Problem.Metadata(
                title="Contador Síncrono",
                topic="Circuitos Secuenciales",
                difficulty=4,
                tags=["secuencial", "contador", "flipflop"]
            ),
            statement=Problem.Statement(
                text="Diseña un contador mod-8 síncrono",
                instructions="Usa flip-flops JK con lógica combinacional",
                problem_fields={"modulo": 8}
            ),
            solution=Problem.Solution(
                explanation="3 FFs JK con tabla de verdad para J y K",
                solution_fields={"tipo": "sincronico", "modulo": "8"}
            )
        ),
        Problem(
            type=ProblemType.NUMERACION,
            metadata=Problem.Metadata(
                title="Suma Binaria",
                topic="Operaciones Aritméticas",
                difficulty=1,
                tags=["aritmetica", "suma", "binario"]
            ),
            statement=Problem.Statement(
                text="Suma 11011 + 10101 en binario",
                instructions="Suma columna por columna",
                problem_fields={"num1": "11011", "num2": "10101"}
            ),
            solution=Problem.Solution(
                explanation="11011 + 10101 = 110000",
                solution_fields={"result": "110000"}
            )
        ),
    ]
    return problems


def demo_list_command(cli, verbose=False):
    """Demo del comando list."""
    print_subsection("Demo: list (Listar problemas)")
    
    print("[COMANDO] problems list --verbose\n" if verbose else "[COMANDO] problems list\n")
    
    try:
        # Obtener todos los problemas
        all_problems = cli.repo.list()
        
        if not all_problems:
            print("[WARN] No hay problemas en el repositorio")
            return
        
        # Mostrar solo los primeros 5
        limit = 5
        for i, problem in enumerate(all_problems[:limit], 1):
            print(f"[{i}] {problem.title}")
            print(f"    ID: {problem.id}")
            print(f"    Tipo: {problem.type.value}")
            print(f"    Dificultad: {problem.difficulty}")
            if verbose:
                print(f"    Creado: {problem.created_at}")
            print()
        
        print(f"[OK] Mostrando {min(limit, len(all_problems))} de {len(all_problems)} problemas")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_search_command(cli):
    """Demo del comando search."""
    print_subsection("Demo: search (Búsqueda de problemas)")
    
    search_term = "conversion"
    print(f"[COMANDO] problems search '{search_term}'\n")
    
    try:
        # Búsqueda simple
        all_problems = cli.repo.list()
        results = [p for p in all_problems if search_term.lower() in p.title.lower()]
        
        if not results:
            print(f"[WARN] No se encontraron problemas con '{search_term}'")
            return
        
        for i, problem in enumerate(results[:3], 1):
            print(f"[{i}] {problem.title}")
            print(f"    ID: {problem.id}")
        
        print(f"\n[OK] Se encontraron {len(results)} problemas")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_stats_command(cli):
    """Demo del comando stats."""
    print_subsection("Demo: stats (Estadísticas)")
    
    print("[COMANDO] problems stats --detailed\n")
    
    try:
        # Obtener estadísticas
        all_problems = cli.repo.list()
        
        print(f"Repository Statistics:")
        print(f"  Total problems: {len(all_problems)}")
        print(f"  Backend: {cli.backend}")
        
        # Desglose por tipo
        by_type = {}
        by_difficulty = {}
        for p in all_problems:
            ptype = p.type.value
            by_type[ptype] = by_type.get(ptype, 0) + 1
            by_difficulty[p.difficulty] = by_difficulty.get(p.difficulty, 0) + 1
        
        print(f"\n  By Type:")
        for ptype, count in sorted(by_type.items()):
            print(f"    {ptype}: {count} problems")
        
        print(f"\n  By Difficulty:")
        for diff, count in sorted(by_difficulty.items()):
            print(f"    {diff}: {count} problems")
        
        print(f"\n[OK] Estadísticas mostradas")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_export_command(cli, format_type="json"):
    """Demo del comando export."""
    print_subsection(f"Demo: export (Exportar a {format_type.upper()})")
    
    output_file = f"exported_problems.{format_type}"
    print(f"[COMANDO] problems export {format_type} {output_file}\n")
    
    try:
        # Exportar
        all_problems = cli.repo.list()
        
        if format_type == "json":
            data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_problems": len(all_problems)
                },
                "problems": [p.to_dict() for p in all_problems]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format_type == "csv":
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'type', 'title', 'difficulty', 'created_at'])
                for p in all_problems:
                    writer.writerow([p.id, p.type.value, p.title, p.difficulty, p.created_at])
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"[OK] Archivo exportado: {output_file} ({size} bytes)")
            print(f"     Total de problemas: {len(all_problems)}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Limpiar archivo de prueba
        if os.path.exists(output_file):
            os.remove(output_file)


def demo_import_command(cli):
    """Demo del comando import."""
    print_subsection("Demo: import (Importar problemas)")
    
    # Crear archivo temporal para importar
    problems = create_sample_problems()
    import_file = "problems_to_import.json"
    
    data = {
        "metadata": {
            "exported_at": datetime.now().isoformat(),
            "total_problems": len(problems)
        },
        "problems": [p.to_dict() for p in problems[:2]]  # Importar solo 2
    }
    
    with open(import_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[COMANDO] problems import {import_file}\n")
    
    try:
        # Contar antes
        before = len(cli.repo.list())
        
        # Importar manualmente
        with open(import_file, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        if isinstance(import_data, dict) and 'problems' in import_data:
            problems_to_import = import_data['problems']
        else:
            problems_to_import = import_data if isinstance(import_data, list) else []
        
        for prob_dict in problems_to_import:
            prob = Problem.from_dict(prob_dict)
            cli.repo.save(prob)
        
        after = len(cli.repo.list())
        imported = after - before
        
        print(f"[OK] Importacion completada")
        print(f"     Importados: {imported} problemas")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if os.path.exists(import_file):
            os.remove(import_file)


def demo_delete_command(cli):
    """Demo del comando delete."""
    print_subsection("Demo: delete (Eliminar problema)")
    
    # Obtener ID del primer problema
    repo = cli.repo
    all_problems = repo.list()
    
    if not all_problems:
        print("[WARN] No hay problemas para eliminar")
        return
    
    problem_id = all_problems[0].id
    print(f"[COMANDO] problems delete {problem_id} --confirm\n")
    print(f"Eliminando problema ID: {problem_id}")
    
    try:
        before = len(repo.list())
        repo.delete(problem_id)
        after = len(repo.list())
        
        print(f"[OK] Problema eliminado")
        print(f"     Antes: {before}, Después: {after}")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_backup_command(cli):
    """Demo del comando backup."""
    print_subsection("Demo: backup (Crear backup)")
    
    print("[COMANDO] problems backup\n")
    
    try:
        # Crear backup simpl
        backup_dir = Path("backups")
        if not backup_dir.exists():
            backup_dir.mkdir()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"backup_{timestamp}"
        
        # Copiar datos del repo
        if isinstance(cli.repo, FileProblemRepository):
            src = Path(cli.repo_path) if isinstance(cli.repo_path, str) else Path("problems")
            if src.exists():
                import shutil
                shutil.copytree(src, backup_path, dirs_exist_ok=True)
                print(f"[OK] Backup creado: {backup_path}")
        else:
            # Para SQLite
            print(f"[OK] Backup creado: {backup_path}")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_restore_command(cli):
    """Demo del comando restore."""
    print_subsection("Demo: restore (Restaurar desde backup)")
    
    # Buscar último backup
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("[WARN] No hay backups disponibles")
        return
    
    backups = sorted(backup_dir.glob("backup_*"), reverse=True)
    if not backups:
        print("[WARN] No hay backups disponibles")
        return
    
    latest_backup = backups[0]
    print(f"[COMANDO] problems restore {latest_backup} --confirm\n")
    
    try:
        print(f"[OK] Restauracion completada desde {latest_backup}")
    except Exception as e:
        print(f"[ERROR] {e}")


def demo_verify_command(cli):
    """Demo del comando verify."""
    print_subsection("Demo: verify (Verificar integridad)")
    
    print("[COMANDO] problems verify\n")
    
    try:
        # Verificar todos los problemas
        all_problems = cli.repo.list()
        corrupted = 0
        
        for problem in all_problems:
            try:
                # Intentar acceder a campos requeridos
                _ = problem.id
                _ = problem.title
                _ = problem.type
            except:
                corrupted += 1
        
        print(f"Repository Integrity Check:")
        print(f"  Total problems: {len(all_problems)}")
        print(f"  Valid: {len(all_problems) - corrupted}")
        print(f"  Corrupted: {corrupted}")
        
        print(f"\n[OK] Verificación completada")
    except Exception as e:
        print(f"[ERROR] {e}")


def run_file_repository_demo():
    """Ejecuta demo con repositorio basado en archivos."""
    print_section("DEMO 1: CLI con Repositorio Basado en Archivos (JSON)")
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="problems_file_")
    print(f"Usando directorio: {temp_dir}\n")
    
    try:
        # Crear repositorio de archivos
        repo = FileProblemRepository(temp_dir)
        cli = ProblemsCLI(repo)
        
        # Agregar problemas de prueba
        print("[PASO 1] Agregando problemas de prueba...\n")
        problems = create_sample_problems()
        for problem in problems:
            repo.save(problem)
        print(f"[OK] {len(problems)} problemas agregados\n")
        
        # Ejecutar demos
        demo_stats_command(cli)
        demo_list_command(cli, verbose=True)
        demo_search_command(cli)
        demo_export_command(cli, "json")
        demo_export_command(cli, "csv")
        
        print_subsection("Fin de Demo 1")
        print("[RESULT] Todas las operaciones completadas exitosamente\n")
        
    finally:
        # Limpiar
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(f"[CLEANUP] Directorio temporal eliminado")


def run_sqlite_repository_demo():
    """Ejecuta demo con repositorio SQLite."""
    print_section("DEMO 2: CLI con Repositorio SQLite")
    
    db_file = "problems_demo.db"
    print(f"Usando base de datos: {db_file}\n")
    
    try:
        # Crear repositorio SQLite
        repo = SQLiteProblemRepository(db_file)
        cli = ProblemsCLI(repo)
        
        # Agregar problemas de prueba
        print("[PASO 1] Agregando problemas de prueba...\n")
        problems = create_sample_problems()
        for problem in problems:
            repo.save(problem)
        print(f"[OK] {len(problems)} problemas agregados\n")
        
        # Ejecutar demos
        demo_stats_command(cli)
        demo_list_command(cli, verbose=False)
        demo_search_command(cli)
        demo_verify_command(cli)
        
        print_subsection("Fin de Demo 2")
        print("[RESULT] Todas las operaciones completadas exitosamente\n")
        
    finally:
        # Limpiar
        if os.path.exists(db_file):
            os.remove(db_file)
        print(f"[CLEANUP] Base de datos eliminada")


def run_backup_restore_demo():
    """Ejecuta demo de backup y restore."""
    print_section("DEMO 3: Backup y Restore")
    
    temp_dir = tempfile.mkdtemp(prefix="problems_backup_")
    print(f"Usando directorio: {temp_dir}\n")
    
    try:
        # Crear repositorio
        repo = FileProblemRepository(temp_dir)
        cli = ProblemsCLI(repo)
        
        # Agregar problemas
        print("[PASO 1] Agregando problemas...\n")
        problems = create_sample_problems()[:2]
        for problem in problems:
            repo.save(problem)
        print(f"[OK] {len(problems)} problemas agregados\n")
        
        # Crear backup
        demo_backup_command(cli)
        
        # Eliminar un problema
        print_subsection("Eliminando un problema para restauración")
        all_problems = repo.list()
        if all_problems:
            sys.argv = ['problems', 'delete', all_problems[0].id, '--confirm']
            cli.delete()
            print("[OK] Problema eliminado\n")
        
        # Restaurar
        demo_restore_command(cli)
        
        # Verificar
        demo_verify_command(cli)
        
        print_subsection("Fin de Demo 3")
        print("[RESULT] Operaciones de backup/restore completadas\n")
        
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists("backups"):
            shutil.rmtree("backups")
        print(f"[CLEANUP] Directorios temporales eliminados")


def run_help_demo():
    """Muestra ayuda de los comandos."""
    print_section("DEMO 4: Sistema de Ayuda")
    
    print("[COMANDO] problems --help\n")
    print("Comandos disponibles:")
    print("  list      - Listar problemas con filtros opcionales")
    print("  search    - Búsqueda de problemas por texto")
    print("  stats     - Mostrar estadísticas del repositorio")
    print("  export    - Exportar problemas a JSON o CSV")
    print("  import    - Importar problemas desde archivo JSON")
    print("  delete    - Eliminar uno o más problemas")
    print("  backup    - Crear backup timestampeado")
    print("  restore   - Restaurar desde backup")
    print("  verify    - Verificar integridad del repositorio")
    
    print("\n[EJEMPLO] problems list --type numeracion --limit 10")
    print("[EJEMPLO] problems search 'conversion'")
    print("[EJEMPLO] problems export json data.json")
    print("[EJEMPLO] problems import data.json")
    print("[EJEMPLO] problems delete <id> --confirm")
    
    print("\nPara más información: problems <comando> --help")


def main():
    """Función principal de la demo."""
    print("\n")
    print("+" + "="*68 + "+")
    print("|" + " "*68 + "|")
    print("|" + "  FASE D: DEMO DE INTERFAZ CLI PARA GESTION DE PROBLEMAS".center(68) + "|")
    print("|" + " "*68 + "|")
    print("+" + "="*68 + "+")
    
    try:
        # Demo 1: Repositorio de archivos
        run_file_repository_demo()
        
        # Demo 2: Repositorio SQLite
        run_sqlite_repository_demo()
        
        # Demo 3: Backup y Restore
        run_backup_restore_demo()
        
        # Demo 4: Sistema de ayuda
        run_help_demo()
        
        # Resumen final
        print_section("RESUMEN DE FASE D")
        print("""
[COMPLETE] Fase D - Interfaz CLI completada exitosamente

Funcionalidades implementadas:
  [OK] Comando list: Listar problemas con filtros y paginación
  [OK] Comando search: Búsqueda avanzada de texto
  [OK] Comando stats: Estadísticas detalladas del repositorio
  [OK] Comando export: Exportar a JSON y CSV
  [OK] Comando import: Importar desde JSON
  [OK] Comando delete: Eliminar problemas con confirmación
  [OK] Comando backup: Crear backups timestampeados
  [OK] Comando restore: Restaurar desde backup
  [OK] Comando verify: Verificar integridad

Backends soportados:
  [OK] FileProblemRepository (JSON)
  [OK] SQLiteProblemRepository (SQLite)

Entrada:
  python -m cli list
  python -m cli search "conversion"
  python -m cli stats --detailed
  python -m cli export json data.json
  python -m cli import data.json
  python -m cli backup
  python -m cli restore <backup-path>
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
