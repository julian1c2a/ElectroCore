#!/usr/bin/env python3
"""
Demo de Fase 6: FixedPointUnified, Comparador y Validador

Demuestra:
1. Clase unificada FixedPointUnified
2. Comparativa de variantes
3. Validacion universal
4. Renderizacion en multiples formatos
"""

import sys
from pathlib import Path

# Agregar core al path
sys.path.insert(0, str(Path(__file__).parent))

from core.punto_fijo_unified import FixedPointUnified
from core.punto_fijo_comparator import FixedPointComparator
from core.representation_validator import RepresentationValidator, batch_validate


def demo_1_fixedpoint_unified():
    """Demo 1: FixedPointUnified"""
    print("\n" + "="*70)
    print("DEMO 1: FixedPointUnified - Clase Unificada")
    print("="*70)
    
    # Sin signo
    print("\n[1] SIN SIGNO (FixedPointUnified)")
    fp_unsigned = FixedPointUnified(E=4, F=4, base=2, signed=False)
    print(fp_unsigned.info())
    
    print("\nOperaciones:")
    print(f"  encode(5.25) = {fp_unsigned.encode(5.25)}")
    print(f"  decode(84) = {fp_unsigned.decode(84)}")
    print(f"  5.25 + 3.75 = {fp_unsigned.add(5.25, 3.75)}")
    
    # Con signo - M&S
    print("\n[2] CON SIGNO - MAGNITUD Y SIGNO (M&S)")
    fp_ms = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms')
    print(fp_ms.info())
    
    print("\nOperaciones:")
    print(f"  encode(5.25) = {fp_ms.encode(5.25)}")
    print(f"  encode(-5.25) = {fp_ms.encode(-5.25)}")
    print(f"  decode(84) = {fp_ms.decode(84)}")
    print(f"  decode({fp_ms.encode(-5.25)}) = {fp_ms.decode(fp_ms.encode(-5.25))}")
    
    # Con signo - Complemento (RECOMENDADO)
    print("\n[3] CON SIGNO - COMPLEMENTO A BASE [RECOMENDADO]")
    fp_complement = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')
    print(fp_complement.info())
    
    print("\nOperaciones:")
    print(f"  encode(5.25) = {fp_complement.encode(5.25)}")
    print(f"  encode(-5.25) = {fp_complement.encode(-5.25)}")
    print(f"  decode(84) = {fp_complement.decode(84)}")
    print(f"  decode({fp_complement.encode(-5.25)}) = {fp_complement.decode(fp_complement.encode(-5.25))}")
    print(f"  5.25 - 3.75 = {fp_complement.subtract(5.25, 3.75)}")


def demo_2_comparador():
    """Demo 2: Comparador"""
    print("\n" + "="*70)
    print("DEMO 2: FixedPointComparator - Comparativas")
    print("="*70)
    
    # Crear las 3 variantes
    fps = [
        FixedPointUnified(E=4, F=4, base=2, signed=False),
        FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms'),
        FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement'),
    ]
    
    comparator = FixedPointComparator()
    
    # Renderizar en texto
    print("\n[TABLE] TABLA EN TEXTO PLANO:")
    print(comparator.render_text(fps))
    
    # Renderizar LaTeX (mostrar parte)
    print("\n[TEX] TABLA EN LaTeX (primeras 10 lineas):")
    latex = comparator.render_latex(fps)
    print("\n".join(latex.split("\n")[:10]))
    print("  ...")
    
    # Exportar a archivos
    output_dir = Path("build")
    output_dir.mkdir(exist_ok=True)
    
    comparator.export_latex_file(fps, str(output_dir / "comparison.tex"))
    comparator.export_html_file(fps, str(output_dir / "comparison.html"))
    comparator.export_json_file(fps, str(output_dir / "comparison.json"))


def demo_3_validador():
    """Demo 3: Validador Universal"""
    print("\n" + "="*70)
    print("DEMO 3: RepresentationValidator - Validacion Universal")
    print("="*70)
    
    # Crear representaciones
    fp_unsigned = FixedPointUnified(E=4, F=4, base=2, signed=False)
    fp_ms = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms')
    fp_complement = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')
    
    validator = RepresentationValidator()
    
    # Validar cada una
    print("\n[1] VALIDACION SIN SIGNO:")
    report_unsigned = validator.validate_fixed_point(fp_unsigned)
    print(report_unsigned.summary())
    
    print("[2] VALIDACION MAGNITUD-SIGNO:")
    report_ms = validator.validate_fixed_point(fp_ms)
    print(report_ms.summary())
    
    print("[3] VALIDACION COMPLEMENTO [RECOMENDADO]:")
    report_complement = validator.validate_fixed_point(fp_complement)
    print(report_complement.summary())
    
    # Comparar errores
    print("\n[4] COMPARACION DE ERRORES:")
    print("\nRepresentando el valor 5.5 en las 3 variantes:")
    
    value = 5.5
    comparison = validator.compare_error(value, fp_unsigned, fp_complement)
    
    print(f"\nValor original: {comparison['value']}")
    print(f"\nSin signo ({comparison['fp1']['name']}):")
    print(f"  Decodificado: {comparison['fp1']['decoded']}")
    print(f"  Error absoluto: {comparison['fp1']['error_absolute']}")
    print(f"  Error relativo: {comparison['fp1']['error_relative']:.6%}")
    
    print(f"\nComplemento ({comparison['fp2']['name']}):")
    print(f"  Decodificado: {comparison['fp2']['decoded']}")
    print(f"  Error absoluto: {comparison['fp2']['error_absolute']}")
    print(f"  Error relativo: {comparison['fp2']['error_relative']:.6%}")
    
    print(f"\n[WINNER] Ganador: {comparison['winner']}")


def demo_4_batch_validation():
    """Demo 4: Validacion por lotes"""
    print("\n" + "="*70)
    print("DEMO 4: Validacion por Lotes")
    print("="*70)
    
    # Crear varias representaciones
    representations = [
        FixedPointUnified(E=4, F=4, base=2, signed=False),
        FixedPointUnified(E=8, F=8, base=2, signed=True, representation='complement'),
        FixedPointUnified(E=16, F=16, base=10, signed=True, representation='ms'),
    ]
    
    reports = batch_validate(representations)
    
    print(f"\n[OK] Se validaron {len(reports)} representaciones:\n")
    for i, report in enumerate(reports, 1):
        status = "[OK] VALIDO" if report.is_valid else "[ERROR] INVALIDO"
        print(f"{i}. {report.representation_type}: {status}")
        print(f"   Chequeos: {report.checks_passed}/{report.checks_total}")


def main():
    """Ejecutar todos los demos."""
    print("\n" + "="*70)
    print("DEMO DE FASE 6: PUNTO FIJO UNIFICADO")
    print("="*70)
    
    try:
        demo_1_fixedpoint_unified()
        demo_2_comparador()
        demo_3_validador()
        demo_4_batch_validation()
        
        print("\n" + "="*70)
        print("[OK] DEMO COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\nArchivos generados en build/:")
        print("  - comparison.tex (LaTeX)")
        print("  - comparison.html (HTML)")
        print("  - comparison.json (JSON)")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
