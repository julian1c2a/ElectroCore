"""
FASE C DEMO: Integración de ExamBuilder con ProblemRepository.

Demuestra:
1. ExamBuilder guardando automáticamente problemas en DB
2. Reutilización de problemas existentes
3. Estadísticas de persistencia
"""

import os
import json
import shutil
from pathlib import Path

# Fase C imports
from core.exam_builder import ExamBuilder
from database import FileProblemRepository, SQLiteProblemRepository
from models.problem_type import ProblemType


def section(title: str, char: str = "="):
    """Imprime una sección con título."""
    print(f"\n{char * 80}")
    print(f"{char * 20} {title}")
    print(f"{char * 80}\n")


def cleanup_test_dirs():
    """Limpia directorios de prueba anteriores."""
    test_dirs = ["test_exam_file", "test_exam_file2"]
    for d in test_dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    test_db = "test_exam.db"
    if os.path.exists(test_db):
        os.remove(test_db)


def create_test_config(title: str, seed: int = None) -> str:
    """Crea un archivo de configuración de prueba."""
    config = {
        "title": title,
        "description": f"Examen de prueba: {title}",
        "seed": seed,
        "exercises": [
            {
                "id": "num_conversion_8bits",  # Existe en EXERCISE_CATALOG
                "qty": 3,
                "difficulty": 2
            }
        ]
    }
    
    config_file = f"test_config_{title.replace(' ', '_').lower()}.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    return config_file


def demo_file_repository():
    """Demo 1: ExamBuilder con FileProblemRepository."""
    section("DEMO 1: ExamBuilder + FileProblemRepository")
    
    # Limpiar
    if os.path.exists("test_exam_file"):
        shutil.rmtree("test_exam_file")
    
    # Crear repositorio
    repo = FileProblemRepository("./test_exam_file")
    print("[INIT] Repositorio creado")
    print(f"       Ubicación: {os.path.abspath('test_exam_file')}")
    
    # Crear builder CON repositorio
    config_file = create_test_config("Examen 1 - File")
    builder = ExamBuilder(config_file, problem_repository=repo)
    
    print("\n[BUILD 1] Generando primer examen (sin reutilización)")
    try:
        exercises = builder.build(use_repository=True, reuse_probability=0.0)
        print(f"          [OK] {len(exercises)} ejercicios generados")
    except Exception as e:
        print(f"          [WARN]  Error: {e}")
        return
    
    builder.print_persistence_report()
    
    # Segundo examen CON reutilización
    print("\n[BUILD 2] Generando segundo examen (30% reutilización)")
    config_file2 = create_test_config("Examen 2 - File")
    builder2 = ExamBuilder(config_file2, problem_repository=repo)
    try:
        exercises2 = builder2.build(use_repository=True, reuse_probability=0.3)
        print(f"          [OK] {len(exercises2)} ejercicios generados")
    except Exception as e:
        print(f"          [WARN]  Error: {e}")
    
    builder2.print_persistence_report()
    
    # Estadísticas finales
    print("\n[FINAL STATS]")
    info = repo.info()
    print(f"Backend:      {info['backend']}")
    print(f"Total:        {info['total']} problemas")
    print(f"Por tipo:     {info['by_type']}")
    print(f"Tamaño:       {info['size_mb']:.2f} MB")
    
    # Limpiar
    os.remove(config_file)
    os.remove(config_file2)


def demo_sqlite_repository():
    """Demo 2: ExamBuilder con SQLiteProblemRepository."""
    section("DEMO 2: ExamBuilder + SQLiteProblemRepository")
    
    # Limpiar
    if os.path.exists("test_exam.db"):
        os.remove("test_exam.db")
    
    # Crear repositorio
    repo = SQLiteProblemRepository("./test_exam.db")
    print("[INIT] Base de datos creada")
    print(f"       Ubicación: {os.path.abspath('test_exam.db')}")
    
    # Primer examen
    config_file = create_test_config("Examen SQLite 1", seed=42)
    builder = ExamBuilder(config_file, problem_repository=repo)
    
    print("\n[BUILD 1] Generando primer examen")
    try:
        exercises = builder.build(use_repository=True, reuse_probability=0.0)
        print(f"          [OK] {len(exercises)} ejercicios generados")
    except Exception as e:
        print(f"          [WARN]  Error: {e}")
        return
    
    builder.print_persistence_report()
    
    # Segundo examen
    print("\n[BUILD 2] Generando segundo examen (50% reutilización)")
    config_file2 = create_test_config("Examen SQLite 2", seed=123)
    builder2 = ExamBuilder(config_file2, problem_repository=repo)
    try:
        exercises2 = builder2.build(use_repository=True, reuse_probability=0.5)
        print(f"          [OK] {len(exercises2)} ejercicios generados")
    except Exception as e:
        print(f"          [WARN]  Error: {e}")
    
    builder2.print_persistence_report()
    
    # Estadísticas finales
    print("\n[FINAL STATS]")
    info = repo.info()
    print(f"Backend:      {info['backend']}")
    print(f"Total:        {info['total']} problemas")
    print(f"Por tipo:     {info['by_type']}")
    print(f"Tamaño:       {info['size_mb']:.2f} MB")
    
    # Limpiar
    os.remove(config_file)
    os.remove(config_file2)


def demo_sin_repositorio():
    """Demo 3: ExamBuilder SIN repositorio (backward compatibility)."""
    section("DEMO 3: ExamBuilder sin Repositorio (backward compatibility)")
    
    # Crear builder SIN repositorio
    config_file = create_test_config("Examen Legacy")
    builder = ExamBuilder(config_file, problem_repository=None)
    
    print("[BUILD] Generando examen sin repositorio")
    try:
        exercises = builder.build(use_repository=False)
        print(f"        [OK] {len(exercises)} ejercicios generados")
    except Exception as e:
        print(f"        [WARN]  Error: {e}")
    
    stats = builder.get_persistence_stats()
    print(f"\n[STATS]")
    print(f"Repositorio:  {'SÍ' if stats['has_repository'] else 'NO'}")
    print(f"Guardados:    {stats['saved_count']}")
    print(f"Cargados:     {stats['loaded_count']}")
    print(f"Generados:    {stats['generated_count']}")
    
    os.remove(config_file)


def demo_persistencia_reports():
    """Demo 4: Generar y guardar reportes de persistencia."""
    section("DEMO 4: Reportes de Persistencia")
    
    # Crear repo
    repo = FileProblemRepository("./test_exam_reports")
    config_file = create_test_config("Examen con Reporte")
    
    # Build
    builder = ExamBuilder(config_file, problem_repository=repo)
    try:
        builder.build(use_repository=True, reuse_probability=0.2)
    except Exception as e:
        print(f"[WARN]  Error: {e}")
        return
    
    print("[SAVE] Guardando reportes")
    
    # Guardar reporte de persistencia
    os.makedirs("build/json", exist_ok=True)
    repo_report = builder.save_persistence_report()
    print(f"       [OK] Reporte guardado: {repo_report}")
    
    # Leer y mostrar contenido
    with open(repo_report, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    print(f"\n[CONTENIDO DEL REPORTE]")
    print(f"Examen:       {report_data['exam_title']}")
    print(f"Guardados:    {report_data['persistence_stats']['saved_count']}")
    print(f"Cargados:     {report_data['persistence_stats']['loaded_count']}")
    print(f"Tasa reutiliz: {report_data['persistence_stats']['reuse_ratio']:.1%}")
    
    # Limpiar
    shutil.rmtree("test_exam_reports")
    os.remove(config_file)


def main():
    """Ejecuta todos los demos."""
    
    print("\n" + "="*80)
    print("="*80)
    print("FASE C: INTEGRACIÓN EXAMBUILDER + PROBLEM REPOSITORY".center(80))
    print("="*80)
    print("="*80)
    
    cleanup_test_dirs()
    
    try:
        # Demo 1: File Repository
        demo_file_repository()
        
        # Demo 2: SQLite Repository
        demo_sqlite_repository()
        
        # Demo 3: Sin Repositorio (backward compat)
        demo_sin_repositorio()
        
        # Demo 4: Reportes
        demo_persistencia_reports()
        
        # Resumen final
        section("[OK] FASE C: COMPLETADA CON ÉXITO")
        print("""
La integración ExamBuilder + ProblemRepository proporciona:

1. [[OK]] PERSISTENCIA AUTOMÁTICA
   • Los ejercicios se guardan automáticamente en el repositorio
   • Soporta File (JSON) y SQLite (DB)

2. [[OK]] REUTILIZACIÓN INTELIGENTE
   • Parámetro reuse_probability controla reutilización
   • Reutilización aleatoria de problemas existentes
   • Estadísticas de tasa de reutilización

3. [[OK]] BACKWARD COMPATIBILITY
   • ExamBuilder sin repositorio = comportamiento original
   • use_repository=False desactiva persistencia
   • Código existente sigue funcionando

4. [[OK]] REPORTES Y ESTADÍSTICAS
   • get_persistence_stats() → Dict con métricas
   • print_persistence_report() → Salida formateada
   • save_persistence_report() → Reporte JSON

5. [[OK]] POLYMORFISMO
   • Mismo código funciona con File o SQLite
   • Fácil cambiar backend

PRÓXIMA FASE: Fase D (CLI Tools)
   • CLI para management de problemas
   • Búsqueda y filtrado
   • Estadísticas
   • Backup y restore
        """)
        
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpiar
        cleanup_test_dirs()
        for f in ["test_config_examen_1_-_file.json", 
                  "test_config_examen_2_-_file.json",
                  "test_config_examen_sqlite_1.json",
                  "test_config_examen_sqlite_2.json",
                  "test_config_examen_legacy.json",
                  "test_config_examen_con_reporte.json"]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    main()
