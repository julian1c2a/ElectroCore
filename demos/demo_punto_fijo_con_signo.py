"""
Demostracion de Punto Fijo con Signo - M&S vs Complemento a Base

Muestra ejemplos detallados de ambas representaciones con enfasis en los
valores extremos del rango.
"""

from core.punto_fijo_con_signo import FixedPointSignedMS, FixedPointSignedComplement
from decimal import Decimal


def demo_extreme_values():
    """Demostrar valores extremos en ambas representaciones."""
    print("\n" + "="*80)
    print("VALORES EXTREMOS EN PUNTO FIJO CON SIGNO")
    print("="*80)
    
    # Usar Q(4,4) para que sea claro
    E, F, base = 4, 4, 2
    
    ms = FixedPointSignedMS(E=E, F=F, base=base)
    comp = FixedPointSignedComplement(E=E, F=F, base=base)
    
    print(f"\nRepresentacion Q({E},{F}) base {base}")
    print(f"E = {E} (bits enteros)")
    print(f"F = {F} (bits fraccionarios)")
    print(f"\nUnidades basicas:")
    print(f"  B^E = {base}^{E} = {base**E}")
    print(f"  B^(-F) = {base}^(-{F}) = {base**(-F)}")
    
    print(f"\n--- MAGNITUD Y SIGNO ---")
    print(f"Rango: [-(B^E - B^(-F)), B^E - B^(-F)]")
    print(f"       [-({base**E} - {base**(-F)}), {base**E} - {base**(-F)}]")
    print(f"       [{ms.min_value}, {ms.max_value}]")
    
    print(f"\n  Maximo positivo:     B^E - B^(-F) = {ms.max_value}")
    print(f"  Minimo (negativo):   -(B^E - B^(-F)) = {ms.min_value}")
    print(f"  Positivo minimo:     B^(-F) = {ms.epsilon}")
    print(f"  Negativo maximo:     -B^(-F) = {-ms.epsilon}")
    
    print(f"\n--- COMPLEMENTO A BASE ---")
    print(f"Rango: [-B^E, B^E - B^(-F)]")
    print(f"       [-{base**E}, {base**E} - {base**(-F)}]")
    print(f"       [{comp.min_value}, {comp.max_value}]")
    
    print(f"\n  Maximo positivo:     B^E - B^(-F) = {comp.max_value}")
    print(f"  Minimo (mas negativo): -B^E = {comp.min_value}")
    print(f"  Positivo minimo:     B^(-F) = {comp.epsilon}")
    print(f"  Negativo maximo:     -B^(-F) = {-comp.epsilon}")
    
    print(f"\n--- COMPARACION ---")
    print(f"La representacion en complemento a base permite:")
    print(f"  - Un negativo adicional: -B^E vs -(B^E - B^(-F))")
    print(f"  - Diferencia: {abs(comp.min_value - ms.min_value)} unidades")
    print(f"  - Ventaja: Menor desperdicio de espacio de representacion")


def demo_ms_detailed():
    """Demostracion detallada de M&S."""
    print("\n" + "="*80)
    print("MAGNITUD Y SIGNO (M&S) - DETALLADO")
    print("="*80)
    
    E, F, base = 3, 2, 2
    fp = FixedPointSignedMS(E=E, F=F, base=base)
    
    print(f"\nRepresentacion: Q({E},{F}) base {base}")
    print(f"Total bits: {fp.total_bits}")
    print(f"Rango: [{fp.min_value}, {fp.max_value}]")
    
    print(f"\n--- ESTRUCTURA DE REPRESENTACION ---")
    print(f"Bit/Digito mas significativo (MSD): SIGNO")
    print(f"  0 → positivo (+)")
    print(f"  1 → negativo (-)")
    print(f"Resto ({E + F} bits): MAGNITUD")
    
    print(f"\n--- TABLA DE VALORES ---")
    print(f"{'M':<6} {'Signo':<8} {'Magnitud':<10} {'Valor':<8}")
    print("-" * 40)
    
    test_values = [
        fp.max_value,  # Maximo
        3.5,
        2.75,
        0.5,
        fp.epsilon,  # Minimo positivo
        0,  # Cero positivo
        -fp.epsilon,  # Maximo negativo (en magnitud)
        -0.5,
        -2.75,
        -3.5,
        fp.min_value  # Minimo
    ]
    
    for value in test_values:
        M = fp.encode(value)
        sign_digit = M // (base ** (E + F))
        magnitude_m = M % (base ** (E + F))
        sign_str = "+" if sign_digit == 0 else "-"
        print(f"{M:<6d} {sign_str:<8} {magnitude_m:<10d} {value:<8.4f}")
    
    print(f"\n--- PROPIEDADES DE M&S ---")
    print(f"✓ Signo separado facilita operaciones de signo")
    print(f"✓ Magnitud es representacion directa")
    print(f"✗ Cero tiene dos representaciones (+0 y -0)")
    print(f"✗ Requiere circuitos especiales para suma/resta")


def demo_complement_detailed():
    """Demostracion detallada de complemento a base."""
    print("\n" + "="*80)
    print("COMPLEMENTO A BASE - DETALLADO")
    print("="*80)
    
    E, F, base = 3, 2, 2
    fp = FixedPointSignedComplement(E=E, F=F, base=base)
    
    print(f"\nRepresentacion: Q({E},{F}) base {base}")
    print(f"Total bits: {fp.total_bits}")
    print(f"Rango: [{fp.min_value}, {fp.max_value}]")
    print(f"Modulo: {base}^{E + F + 1} = {fp.modulo}")
    
    print(f"\n--- ESTRUCTURA DE REPRESENTACION ---")
    print(f"Positivos (valor >= 0):")
    print(f"  M = valor x base^F")
    print(f"Negativos (valor < 0):")
    print(f"  M = modulo + valor x base^F = base^(E+F+1) + valor x base^F")
    
    print(f"\n--- TABLA DE VALORES ---")
    print(f"{'Valor':<8} {'M':<6} {'Binario':<12} {'Interpretacion':<30}")
    print("-" * 60)
    
    test_values = [
        fp.max_value,  # Maximo
        3.5,
        2.75,
        0.5,
        fp.epsilon,  # Minimo positivo
        0,  # Cero (unico)
        -fp.epsilon,  # Maximo negativo
        -0.5,
        -2.75,
        -3.5,
        -4.0,
        fp.min_value  # Minimo (mas negativo)
    ]
    
    for value in test_values:
        try:
            M = fp.encode(value)
            binary = bin(M)[2:].zfill(fp.total_bits)
            
            # Interpretar
            if M >= int(fp.modulo) // 2:
                interp = f"Negativo (complemento)"
            elif value == 0:
                interp = "Cero (unico)"
            else:
                interp = "Positivo"
            
            print(f"{value:<8.4f} {M:<6d} {binary:<12} {interp:<30}")
        except ValueError:
            print(f"{value:<8.4f} ERROR: fuera de rango")
    
    print(f"\n--- PROPIEDADES DE COMPLEMENTO A BASE ---")
    print(f"✓ Cero tiene unica representacion")
    print(f"✓ Suma y resta son operaciones directas (sin casos especiales)")
    print(f"✓ Permite rango asimetrico: permite -B^E")
    print(f"✗ Representacion negativa menos intuitiva que M&S")
    print(f"✗ Requiere complemento para obtener el negativo")


def demo_operations():
    """Demostrar operaciones en ambas representaciones."""
    print("\n" + "="*80)
    print("OPERACIONES ARITMETICAS")
    print("="*80)
    
    E, F, base = 4, 4, 2
    ms = FixedPointSignedMS(E=E, F=F, base=base)
    comp = FixedPointSignedComplement(E=E, F=F, base=base)
    
    print(f"\nUsando Q({E},{F}) base {base}")
    
    # Pares de operandos
    test_cases = [
        (3.5, 2.25),
        (5.75, -3.5),
        (-4.0, -2.5),
        (0.5, -0.5),
        (-15.9375, 0.5625),
    ]
    
    print(f"\n--- EN M&S ---")
    for v1, v2 in test_cases:
        try:
            suma = ms.add(v1, v2)
            resta = ms.subtract(v1, v2)
            mult = ms.multiply(v1, v2)
            print(f"{v1:7.4f} + {v2:7.4f} = {suma:7.4f}")
            print(f"{v1:7.4f} - {v2:7.4f} = {resta:7.4f}")
            print(f"{v1:7.4f} x {v2:7.4f} = {mult:7.4f}")
            print()
        except Exception as e:
            print(f"  Operacion fallida: {e}\n")
    
    print(f"\n--- EN COMPLEMENTO A BASE ---")
    for v1, v2 in test_cases:
        try:
            suma = comp.add(v1, v2)
            resta = comp.subtract(v1, v2)
            mult = comp.multiply(v1, v2)
            print(f"{v1:7.4f} + {v2:7.4f} = {suma:7.4f}")
            print(f"{v1:7.4f} - {v2:7.4f} = {resta:7.4f}")
            print(f"{v1:7.4f} x {v2:7.4f} = {mult:7.4f}")
            print()
        except Exception as e:
            print(f"  Operacion fallida: {e}\n")


def demo_complementation():
    """Demostrar operacion de complemento (negacion)."""
    print("\n" + "="*80)
    print("NEGACION (COMPLEMENTO)")
    print("="*80)
    
    E, F, base = 4, 4, 2
    comp = FixedPointSignedComplement(E=E, F=F, base=base)
    
    print(f"\nEn complemento a base, para negar un numero:")
    print(f"  M_negado = modulo - M = {base}^(E+F+1) - M")
    
    test_values = [
        0,
        3.5,
        7.9375,
        -3.5,
        -8.0
    ]
    
    print(f"\n{'Valor':<8} {'M':<6} {'M_comp':<8} {'Negado':<8}")
    print("-" * 40)
    
    for value in test_values:
        try:
            M = comp.encode(value)
            M_comp = comp.complement(M)
            value_negated = comp.decode(M_comp)
            print(f"{value:<8.4f} {M:<6d} {M_comp:<8d} {value_negated:<8.4f}")
        except ValueError:
            print(f"{value:<8.4f} ERROR: fuera de rango")


if __name__ == "__main__":
    demo_extreme_values()
    demo_ms_detailed()
    demo_complement_detailed()
    demo_operations()
    demo_complementation()
