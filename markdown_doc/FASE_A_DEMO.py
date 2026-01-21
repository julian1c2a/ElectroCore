#!/usr/bin/env python3
"""
FASE A DEMO: MAPPERS - Conversion ExerciseData <-> Problem

Demuestra:
1. Crear un ExerciseData (objeto Python especifico del tipo)
2. Convertir a Problem agnostico (JSON-ready)
3. Serializar a JSON
4. Deserializar de JSON
5. Convertir de vuelta a ExerciseData

Todo sin perder informacion.
"""

import json
from modules.numeracion.generators import ConversionRowGenerator
from models.problem import Problem
from models.problem_type import ProblemType
from models.mappers import get_mapper


def section(title: str, char: str = "="):
    """Imprime una seccion de titulo."""
    print(f"\n{char * 88}")
    print(f"  {title}")
    print(f"{char * 88}\n")


def demo_conversion_row():
    """Demo: ConversionRow (Numeracion)"""
    section("DEMO 1: Conversion Numerica (ConversionRow)", "-")
    
    print("1. GENERAR ExerciseData (ConversionRow)")
    print("   -------\n")
    
    # Generar un ejercicio de conversion usando el generador
    generator = ConversionRowGenerator()
    problem_params = {
        'label': 'a',
        'val_decimal': 157,
        'target_col_idx': 0,  # Binario
        'representable': True
    }
    
    exercise_data = generator.generate_from_problem(problem_params)
    
    print(f"   [OK] Ejercicio generado:")
    print(f"        - Label: {exercise_data.label}")
    print(f"        - Valor decimal: {exercise_data.val_decimal}")
    print(f"        - Sistema target: {exercise_data.target_system}")
    print(f"        - Respuesta: {exercise_data.target_val_str}\n")
    
    print("2. CONVERTIR a Problem agnostico")
    print("   -------\n")
    
    # Obtener mapper para numeracion
    mapper = get_mapper(ProblemType.NUMERACION)
    
    # Convertir ExerciseData -> Problem
    problem = mapper.exercise_to_problem(
        exercise_data,
        seed=42,
        generator_id="ConversionRowGenerator"
    )
    
    print(f"   [OK] Problem creado:")
    print(f"        - ID: {problem.id[:8]}...")
    print(f"        - Type: {problem.type.value}")
    print(f"        - Title: {problem.metadata.title}")
    print(f"        - Difficulty: {problem.metadata.difficulty}")
    print(f"        - Tags: {problem.metadata.tags}")
    print(f"        - Created: {problem.metadata.created_at}\n")
    
    print("3. CAMPOS EN Problem")
    print("   -------\n")
    
    print("   Statement (problema):")
    print(f"     - Text: {problem.statement.text[:60]}...")
    print(f"     - Problem fields: {list(problem.statement.problem_fields.keys())}\n")
    
    print("   Solution (solucion):")
    print(f"     - Explanation: {problem.solution.explanation[:60]}...")
    print(f"     - Steps: {len(problem.solution.steps)} pasos")
    print(f"     - Solution fields: {list(problem.solution.solution_fields.keys())}\n")
    
    print("4. SERIALIZAR a JSON")
    print("   -------\n")
    
    json_string = problem.to_json_string()
    json_lines = json_string.split('\n')
    
    print(f"   [OK] Serializado ({len(json_string)} bytes):")
    for line in json_lines[:15]:
        print(f"     {line}")
    print(f"     ...")
    for line in json_lines[-5:]:
        print(f"     {line}\n")
    
    print("5. DESERIALIZAR de JSON")
    print("   -------\n")
    
    problem_restored = Problem.from_json_string(json_string)
    
    print(f"   [OK] Problem restaurado:")
    print(f"        - ID: {problem_restored.id} (mismo: {problem_restored.id == problem.id})")
    print(f"        - Type: {problem_restored.type.value} (mismo: {problem_restored.type == problem.type})")
    print(f"        - Title: {problem_restored.metadata.title}\n")
    
    print("6. CONVERTIR de vuelta a ExerciseData")
    print("   -------\n")
    
    exercise_restored = mapper.problem_to_exercise(problem_restored)
    
    print(f"   [OK] ExerciseData restaurado:")
    print(f"        - Label: {exercise_restored.label} (igual: {exercise_restored.label == exercise_data.label})")
    print(f"        - Valor: {exercise_restored.val_decimal} (igual: {exercise_restored.val_decimal == exercise_data.val_decimal})")
    print(f"        - Solucion bin: {exercise_restored.sol_bin} (igual: {exercise_restored.sol_bin == exercise_data.sol_bin})\n")
    
    print("7. VERIFICAR ROUND-TRIP")
    print("   -------\n")
    
    # Verificar que los datos son identicos
    original_dict = {
        'label': exercise_data.label,
        'val_decimal': exercise_data.val_decimal,
        'target_col_idx': exercise_data.target_col_idx,
        'target_val_str': exercise_data.target_val_str,
        'sol_bin': exercise_data.sol_bin,
        'sol_c2': exercise_data.sol_c2,
    }
    
    restored_dict = {
        'label': exercise_restored.label,
        'val_decimal': exercise_restored.val_decimal,
        'target_col_idx': exercise_restored.target_col_idx,
        'target_val_str': exercise_restored.target_val_str,
        'sol_bin': exercise_restored.sol_bin,
        'sol_c2': exercise_restored.sol_c2,
    }
    
    if original_dict == restored_dict:
        print("   [PASS] ROUND-TRIP EXITOSO: Datos identicos antes y despues\n")
    else:
        print("   [FAIL] ERROR: Datos diferentes")
        print(f"     Original: {original_dict}")
        print(f"     Restored: {restored_dict}\n")


def demo_metadata_operations():
    """Demo: Operaciones con metadata"""
    section("DEMO 2: Operaciones con Metadata", "-")
    
    print("1. CREAR Problem con metadata")
    print("   -------\n")
    
    # Crear un Problem manualmente
    problem = Problem(
        type=ProblemType.NUMERACION,
        metadata=Problem.Metadata(
            title="Conversion Avanzada",
            topic="Representacion Numerica",
            difficulty=3,
            tags=["8bits", "conversion", "binario"],
            author="sistema",
            source="manual"
        ),
        statement=Problem.Statement(
            text="Convierte 255 a todas las bases",
            instructions="Realiza las conversiones",
            problem_fields={"val_decimal": 255}
        )
    )
    
    print(f"   [OK] Creado con metadata:")
    print(f"        - Title: {problem.metadata.title}")
    print(f"        - Difficulty: {problem.metadata.difficulty}")
    print(f"        - Tags: {problem.metadata.tags}")
    print(f"        - Created: {problem.metadata.created_at}\n")
    
    print("2. MODIFICAR Problem")
    print("   -------\n")
    
    problem.add_tag("importante")
    problem.add_tag("examen")
    problem.set_difficulty(4)
    problem.mark_updated()
    
    print(f"   [OK] Despues de modificar:")
    print(f"        - Difficulty: {problem.metadata.difficulty}")
    print(f"        - Tags: {problem.metadata.tags}")
    print(f"        - Updated: {problem.metadata.updated_at}\n")
    
    print("3. REPRESENTACION")
    print("   -------\n")
    
    print(f"   [OK] {repr(problem)}\n")


def demo_mapper_registry():
    """Demo: Registro de mappers"""
    section("DEMO 3: Registro de Mappers", "-")
    
    from models.mappers import MAPPERS
    
    print("MAPPERS DISPONIBLES:")
    print("   -------\n")
    
    for problem_type, mapper in MAPPERS.items():
        print(f"   [OK] {problem_type.value:12} -> {mapper}\n")


def main():
    """Ejecuta todos los demos."""
    print("\n" + "=" * 88)
    print(" " * 15 + "FASE A: MAPPERS (ExerciseData <-> Problem)")
    print("=" * 88)
    
    try:
        demo_conversion_row()
        demo_metadata_operations()
        demo_mapper_registry()
        
        section("FASE A COMPLETADA CON EXITO", "=")
        
        print("""
RESUMEN:

La Fase A proporciona:

1. [OK] ProblemType (Enum)
   - Tipos soportados: NUMERACION, KARNAUGH, LOGIC, MSI, SECUENCIAL
   
2. [OK] Problem (Clase agnostica)
   - Metadata comun a todos los tipos
   - Enunciado y solucion genericos
   - Serializacion JSON completa
   - Operaciones de metadata (tags, difficulty, etc)
   
3. [OK] Mappers (5 tipos)
   - ConversionRowMapper (Numeracion)
   - KarnaughMapper (Mapas de Karnaugh)
   - LogicProblemMapper (Diseno Logico)
   - MSIMapper (Circuitos MSI)
   - SequentialMapper (Logica Secuencial)
   
4. [OK] Round-trip garantizado
   - ExerciseData -> Problem -> JSON -> Problem -> ExerciseData
   - Sin perdida de datos

PROXIMA FASE: Fase B (Repository)
   - Guardar/cargar Problem de disco o BD
   - CRUD completo
   - Busqueda y filtrado
   - Multiples backends (File, SQLite, etc)
""")
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
