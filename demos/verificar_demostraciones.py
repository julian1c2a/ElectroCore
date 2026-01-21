#!/usr/bin/env python3
"""
VERIFICACIÓN FINAL: Ejecutar todas las demostraciones
Asegura que todo funciona correctamente
"""

import subprocess
import sys
from pathlib import Path


def run_demo(demo_file, description):
    """Ejecutar un archivo de demostración"""
    print(f"\n{'='*80}")
    print(f"EJECUTANDO: {description}")
    print(f"{'='*80}")
    print(f"Archivo: {demo_file}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, demo_file],
            capture_output=False,
            text=True,
            timeout=30,
            encoding='utf-8'
        )
        if result.returncode == 0:
            print(f"\n[OK] {description} - COMPLETADO EXITOSAMENTE")
            return True
        else:
            print(f"\n[FAIL] {description} - FALLÓ (código: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print(f"\n[FAIL] {description} - TIEMPO AGOTADO")
        return False
    except Exception as e:
        print(f"\n[FAIL] {description} - ERROR: {e}")
        return False


def main():
    """Ejecutar todas las verificaciones"""
    print("\n" + "="*80)
    print("VERIFICACIÓN FINAL: SECCIÓN 2.1.1.7 - NÚMEROS ENTEROS SIGNADOS")
    print("="*80)
    
    # Cambiar al directorio del proyecto
    project_dir = Path(__file__).parent
    import os
    os.chdir(project_dir)
    
    demos = [
        ("demo_ms_simple.py", "DEMO 1: Magnitud y Signo (M&S)"),
        ("demo_cb1.py", "DEMO 2: Complemento a la Base Menos 1 (CB-1)"),
        ("demo_cb.py", "DEMO 3: Complemento a la Base (CB)"),
        ("demo_exceso_k.py", "DEMO 4: Exceso a K (Biased)"),
        ("generar_tabla_comparativa.py", "DEMO 5: Tablas Comparativas"),
    ]
    
    results = []
    for demo_file, description in demos:
        success = run_demo(demo_file, description)
        results.append((description, success))
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    
    print(f"\nTotal de demostraciones: {total}")
    print(f"Exitosas: {passed} [OK]")
    print(f"Fallidas: {failed} [FAIL]")
    
    print("\n" + "─"*80)
    print("Detalles:")
    print("─"*80)

    
    for description, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"{status:8} - {description}")
    
    print("\n" + "="*80)
    
    if failed == 0:
        print("SUCCESS: TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*80)
        print("\nLa implementación de Sección 2.1.1.7 está LISTA PARA PRODUCCIÓN [OK]")
        return 0
    else:
        print(f"WARNING: {failed} PRUEBA(S) FALLARON")
        print("="*80)
        return 1


if __name__ == "__main__":
    sys.exit(main())

