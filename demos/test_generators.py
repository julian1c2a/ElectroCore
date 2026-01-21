#!/usr/bin/env python3
"""
Script de prueba para validar que todos los generadores están disponibles y funcionan.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.generator_factory import GeneratorFactory
from core.exercise_mapper import ExerciseMapper


def test_generator_availability():
    """Prueba qué generadores están disponibles."""
    print("=" * 80)
    print("PRUEBA DE DISPONIBILIDAD DE GENERADORES")
    print("=" * 80)
    
    results = GeneratorFactory.test_generator_availability()
    
    available = {k: v for k, v in results.items() if v['status'] == 'available'}
    missing = {k: v for k, v in results.items() if v['status'] == 'missing'}
    
    print(f"\n[OK] DISPONIBLES: {len(available)}")
    for topic_id, info in available.items():
        config = ExerciseMapper.get_generator_config(topic_id)
        print(f"  {topic_id:15} -> {info['class']:45} ({config.description[:40]}...)")
    
    if missing:
        print(f"\n[FALTA] FALTANTES: {len(missing)}")
        for topic_id, info in missing.items():
            config = ExerciseMapper.get_generator_config(topic_id)
            print(f"  {topic_id:15} -> {config.class_name:45} (FALTA IMPLEMENTACION)")
            print(f"    Error: {info['error']}")
    
    print(f"\nRESUMEN: {len(available)} generadores disponibles, {len(missing)} pendientes")
    return available, missing


def test_generator_execution():
    """Prueba que los generadores generen ejercicios correctamente."""
    print("\n" + "=" * 80)
    print("PRUEBA DE EJECUCION DE GENERADORES")
    print("=" * 80)
    
    # Probar algunos generadores clave
    test_topics = [
        "2.1.1.1.3",  # Conversión
        "2.1.1.5.2",  # Punto Fijo
        "2.1.1.5.3",  # Punto Flotante
        "2.2.2",      # Propiedades Booleanas
        "2.2.4",      # Puertas Lógicas
        "2.3.2",      # Flip-Flops
        "1.1.2",      # Ley de Ohm
    ]
    
    for topic_id in test_topics:
        config = ExerciseMapper.get_generator_config(topic_id)
        if not config:
            print(f"\n[AVISO] {topic_id}: No tiene configuracion")
            continue
        
        try:
            generator = GeneratorFactory.create_generator(topic_id)
            if not generator:
                print(f"\n[ERROR] {topic_id}: No se pudo crear generador")
                continue
            
            # Intentar generar ejercicio
            if hasattr(generator, 'generate_from_problem'):
                exercise = generator.generate_from_problem({})
            elif hasattr(generator, 'generate'):
                exercise = generator.generate()
            else:
                print(f"\n[AVISO] {topic_id}: Generador no tiene metodo de generacion")
                continue
            
            print(f"\n[OK] {topic_id:15} EXITOSO")
            print(f"  Generador: {type(generator).__name__}")
            print(f"  Descripcion: {config.description}")
            
            # Mostrar resultado si es un dict
            if isinstance(exercise, dict):
                if 'title' in exercise:
                    print(f"  Titulo: {exercise['title']}")
                if 'problem' in exercise:
                    problem_text = str(exercise['problem'])[:60] + ("..." if len(str(exercise['problem'])) > 60 else "")
                    print(f"  Problema: {problem_text}")
        
        except Exception as e:
            print(f"\n[ERROR] {topic_id}: FALLO")
            print(f"  Clase: {config.class_name}")
            print(f"  Error: {str(e)}")


def test_builder():
    """Prueba el builder de ejercicios."""
    print("\n" + "=" * 80)
    print("PRUEBA DE BUILDER DE EJERCICIOS")
    print("=" * 80)
    
    from core.generator_factory import ExerciseGeneratorBuilder
    
    # Probar construcción de un ejercicio
    try:
        builder = ExerciseGeneratorBuilder("2.1.1.1.3")
        builder.with_difficulty(2)
        builder.with_params(target_base=16)
        
        exercise = builder.build()
        
        print("\n[OK] Builder EXITOSO para 2.1.1.1.3")
        print(f"  Titulo: {exercise.get('title', 'N/A')}")
        print(f"  Problema: {str(exercise.get('problem', 'N/A'))[:60]}...")
    
    except Exception as e:
        print(f"\n[ERROR] Builder FALLO: {str(e)}")


def main():
    """Función principal."""
    print("\nINICIANDO PRUEBAS DE GENERADORES...\n")
    
    # Prueba 1: Disponibilidad
    available, missing = test_generator_availability()
    
    # Prueba 2: Ejecución
    test_generator_execution()
    
    # Prueba 3: Builder
    test_builder()
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    print(f"Generadores disponibles: {len(available)}")
    print(f"Generadores faltantes: {len(missing)}")
    
    if missing:
        print("\nGENERADORES FALTANTES POR IMPLEMENTAR:")
        for topic_id in missing:
            config = ExerciseMapper.get_generator_config(topic_id)
            print(f"  - {topic_id}: {config.class_name} ({config.description})")


if __name__ == '__main__':
    main()
