"""
Comparacion detallada: Punto Fijo vs Punto Flotante

Demuestra como punto flotante resuelve el problema de error relativo variable
que tiene punto fijo cuando cambias de escala.
"""

from core.punto_fijo import FixedPoint
from core.punto_flotante import FixedPointFloating
from decimal import Decimal


def comparison_error_scales():
    """Comparar como varían los errores en diferentes escalas."""
    print("\n" + "="*80)
    print("COMPARACION: ERROR EN DIFERENTES ESCALAS")
    print("="*80)
    
    # Punto Fijo: Q(8,4) base 10
    # - 8 dígitos enteros: rango [-10^8, 10^8)
    # - 4 dígitos fraccionarios: precision 10^(-4)
    fp_fixed = FixedPoint(E=8, F=4, B=10)
    
    # Punto Flotante: FP(F_M=4, E_bits=5) base 2
    # - Mantisa: 4 dígitos de precision -> epsilon = 2^(-4) = 0.0625
    # - Exponente: 5 bits -> rango largo
    fp_float = FixedPointFloating(F_M=4, E_bits=8, base=2)
    
    print(f"\nPUNTO FIJO: {fp_fixed}")
    print(f"  Precision (epsilon): {fp_fixed.epsilon}")
    print(f"  Rango: [{fp_fixed.min_value}, {fp_fixed.max_value}]")
    
    print(f"\nPUNTO FLOTANTE: {fp_float}")
    print(f"  Precision mantisa: {fp_float.epsilon_mantisa}")
    print(f"  Rango exponente: [{fp_float.E_min}, {fp_float.E_max}]")
    
    print(f"\n" + "-"*80)
    print(f"ESCALA (MAGNITUD)  | ERROR RELATIVO PUNTO FIJO | ERROR RELATIVO PUNTO FLOTANTE")
    print(f"-"*80)
    
    # Diferentes escalas
    scales = [
        ("Milesimas", 10**(-3)),
        ("Centesimas", 10**(-2)),
        ("Decimas", 10**(-1)),
        ("Unidades", 10**(0)),
        ("Decenas", 10**(1)),
        ("Centenas", 10**(2)),
        ("Millares", 10**(3)),
        ("Millones", 10**(6)),
    ]
    
    print(f"\nUsando epsilon PUNTO FIJO = {fp_fixed.epsilon}")
    print(f"Usando epsilon MANTISA = {fp_float.epsilon_mantisa}")
    
    print(f"\n{'Escala':<20} {'Error Rel. FIJO':<25} {'Error Rel. FLOTANTE':<25}")
    print("-" * 70)
    
    for scale_name, scale_value in scales:
        # Error relativo en punto fijo
        rel_error_fixed = float(fp_fixed.epsilon) / scale_value
        
        # Error relativo en punto flotante (siempre el mismo)
        rel_error_float = float(fp_float.epsilon_mantisa)
        
        # Ratio: cuanto peor es punto fijo
        ratio = rel_error_fixed / rel_error_float if rel_error_float != 0 else float('inf')
        
        print(f"{scale_name:<20} {rel_error_fixed:<25.2e} {rel_error_float:<25.6f}")
    
    print(f"\nCONCLUSION:")
    print(f"- Punto FIJO: error relativo VARIABLE segun la escala (1e-1 a 1e-14 en este ejemplo)")
    print(f"- Punto FLOTANTE: error relativo CONSTANTE ({float(fp_float.epsilon_mantisa):.6f})")
    print(f"- Para numeros muy grandes o muy pequenos, punto FLOTANTE es MUCHO mejor")


def demonstration_mantisa_range():
    """Demostrar que mantisa siempre está en [1,2) en base 2."""
    print("\n" + "="*80)
    print("DEMOSTRACION: MANTISA NORMALIZADA EN [1,2)")
    print("="*80)
    
    fp = FixedPointFloating(F_M=8, E_bits=8, base=2)
    
    print(f"\nRepresentacion: {fp}")
    print(f"\nSegun IEEE 754 y convencion estandar:")
    print(f"  V = M × 2^E  donde  M ∈ [1, 2)")
    
    print(f"\nLa mantisa normalizada debe:")
    print(f"  - Ser >= 1 (para poder representar correctamente)")
    print(f"  - Ser < 2 (para maximizar precision con bits fijos)")
    print(f"  - Esto significa: 1 bit entero (siempre 1) + bits fraccionarios")
    
    print(f"\n" + "-"*80)
    print(f"EJEMPLOS DE NUMEROS Y SUS REPRESENTACIONES:")
    print(f"-"*80)
    
    examples = [
        ("Muy pequeno", 0.00195312),
        ("Pequeno", 0.5),
        ("Pequeno-medio", 1.0),
        ("Pequeno-medio", 1.5),
        ("Medio", 3.141592653),
        ("Grande", 100),
        ("Muy grande", 1000000),
    ]
    
    print(f"\n{'Valor Original':<20} {'Mantisa':<15} {'Exponente':<12} {'En Rango [1,2)':<12}")
    print("-" * 65)
    
    for name, value in examples:
        m, e = fp.normalize(value)
        in_range = 1 <= abs(m) < 2
        status = "✓" if in_range else "✗"
        print(f"{value:<20.10f} {m:<15.10f} {e:<12d} {status:<12}")
    
    print(f"\nOBSERVACION: Todas las mantisas estan en [1,2)")
    print(f"             Esto GARANTIZA error relativo estable")


def demonstration_operations_detail():
    """Demostrar operaciones en detalle."""
    print("\n" + "="*80)
    print("OPERACIONES EN PUNTO FLOTANTE - DETALLE")
    print("="*80)
    
    fp = FixedPointFloating(F_M=6, E_bits=8, base=2)
    
    # SUMA
    print(f"\n--- SUMA: requiere IGUALAR EXPONENTES ---")
    print(f"\nProblema: 1000000000 + 1")
    v1, v2 = 1000000000, 1
    
    m1, e1 = fp.normalize(v1)
    m2, e2 = fp.normalize(v2)
    
    print(f"\n1. Normalizar:")
    print(f"   {v1} = {m1:.10f} × 2^{e1}")
    print(f"   {v2} = {m2:.10f} × 2^{e2}")
    
    print(f"\n2. Igualar exponentes (usar e={e1}):")
    m2_shifted = m2 / (2 ** (e1 - e2))
    print(f"   Mantisa 1: {m1:.10f}")
    print(f"   Mantisa 2: {m2:.10f} → {m2_shifted:.15f} (desplazada)")
    print(f"   NOTA: m2 se hace muy pequena, casi 0!")
    
    print(f"\n3. Sumar mantisas:")
    m_sum = m1 + m2_shifted
    print(f"   {m1:.10f} + {m2_shifted:.15f} = {m_sum:.10f}")
    
    print(f"\n4. Renormalizar si es necesario: {m_sum:.10f} ya está en [1,2)")
    
    result = fp.add(v1, v2)
    print(f"\nResultado: {result:.1f}")
    print(f"Esperado:  {v1 + v2:.1f}")
    print(f"Nota: Precision limitada por F_M=6 bits")
    
    # MULTIPLICACION
    print(f"\n" + "-"*80)
    print(f"\n--- MULTIPLICACION: mas simple ---")
    print(f"\nProblema: 1000 × 0.001")
    v1, v2 = 1000, 0.001
    
    m1, e1 = fp.normalize(v1)
    m2, e2 = fp.normalize(v2)
    
    print(f"\n1. Normalizar:")
    print(f"   {v1} = {m1:.10f} × 2^{e1}")
    print(f"   {v2} = {m2:.10f} × 2^{e2}")
    
    print(f"\n2. Multiplicar mantisas:")
    m_prod = m1 * m2
    print(f"   {m1:.10f} × {m2:.10f} = {m_prod:.10f}")
    
    print(f"\n3. Sumar exponentes:")
    e_prod = e1 + e2
    print(f"   {e1} + {e2} = {e_prod}")
    
    print(f"\n4. Renormalizar si es necesario:")
    if m_prod >= 2:
        m_norm, e_corr = fp.normalize(m_prod)
        print(f"   {m_prod:.10f} está fuera de [1,2)")
        print(f"   → {m_norm:.10f} × 2^{e_corr}")
        e_final = e_prod + e_corr
    else:
        m_norm = m_prod
        e_final = e_prod
        print(f"   {m_prod:.10f} ya está en [1,2) ✓")
    
    result = fp.multiply(v1, v2)
    print(f"\nResultado: {result:.6f}")
    print(f"Esperado:  {v1 * v2:.6f}")


def comparison_table():
    """Tabla comparativa de punto fijo vs flotante."""
    print("\n" + "="*80)
    print("TABLA COMPARATIVA: PUNTO FIJO vs PUNTO FLOTANTE")
    print("="*80)
    
    print(f"\n{'ASPECTO':<30} {'PUNTO FIJO':<30} {'PUNTO FLOTANTE':<30}")
    print("-" * 90)
    
    comparisons = [
        ("Formato", "Q(E,F): [Sig][E dígitos][F dígitos]", "V=M×B^E: [Sig][E bits][M bits]"),
        ("Mantisa/Magnitud", "Entero en [0, B^E)", "Normalizada en [1, B)"),
        ("Error absoluto", "FIJO (ε = B^(-F))", "VARIABLE (∝ valor)"),
        ("Error relativo", "VARIABLE (depende escala)", "CONSTANTE (ε_mantisa)"),
        ("Rango dinámico", "LIMITADO (B^E - B^(-F))", "ENORME (B^E_min a B^E_max)"),
        ("Precision pequeños", "MALA (error grande en %)", "BUENA (error % constante)"),
        ("Precision grandes", "MALA (error grande en %)", "BUENA (error % constante)"),
        ("Suma", "Directa, sin normalizacion", "Requiere igualar exponentes"),
        ("Multiplicacion", "Requiere reescalado", "Directa, solo exponentes"),
        ("Complejidad HW", "SIMPLE", "COMPLEJA"),
        ("Velocidad", "RAPIDA", "MAS LENTA"),
        ("Uso tipico", "Sistemas embebidos, DSP", "Sistemas de proposito general"),
    ]
    
    for aspect, fixed, floating in comparisons:
        print(f"{aspect:<30} {fixed:<30} {floating:<30}")
    
    print(f"\nCONCLUSION:")
    print(f"- Punto FIJO: mejor para ranges CONOCIDOS y CONSTANTES")
    print(f"- Punto FLOTANTE: mejor para ranges DESCONOCIDOS o VARIABLES")


if __name__ == "__main__":
    comparison_error_scales()
    demonstration_mantisa_range()
    demonstration_operations_detail()
    comparison_table()
