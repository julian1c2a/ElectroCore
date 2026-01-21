#!/usr/bin/env python3
"""
Demostración de IEEE 754 Genérico + Códigos Biquinarios Genéricos

Muestra:
1. IEEE754Gen - Punto flotante genérico con cualquier base, E_bits, F_bits
2. BiquinaryGen + variantes (7 bits, 5 bits, 6 bits)
"""

from core.ieee754 import IEEE754Gen
from core.biquinarios import BiquinaryGen, Biquinary7Bit, Biquinary5Bit, Biquinary6Bit


def demo_ieee754_gen():
    """Demostración de IEEE754Gen con diferentes configuraciones."""
    print("\n" + "="*80)
    print("IEEE754GEN - PUNTO FLOTANTE GENERICO")
    print("="*80)
    
    # Ejemplo 1: IEEE 754 Single (base 2, 8 bits expon, 23 bits mantisa)
    print("\n--- IEEE 754 Single (32 bits) ---")
    ieee_single = IEEE754Gen(E_bits=8, F_bits=23, base=2)
    print(f"Config: {ieee_single}")
    print(f"Total bits: {1 + ieee_single.E_bits + ieee_single.F_bits}")
    print(f"Bias: {ieee_single.bias}")
    
    info = ieee_single.info
    print(f"Rango normalizado: [{info['normalized_min']:.6e}, {info['max']:.6e}]")
    print(f"Rango denormalizado: [{info['denormalized_min']:.6e}, {info['max']:.6e}]")
    
    # Codificar algunos valores
    test_vals = [1.5, 100.5, 1e-40, 1e20]
    print(f"\n{'Valor':<15} {'Tipo':<15} {'Decodificado':<15}")
    print("-" * 45)
    
    for val in test_vals:
        try:
            s, e, m = ieee_single.encode_normalized(val)
            tipo = "Normalizado"
        except:
            try:
                s, e, m = ieee_single.encode_denormalized(val)
                tipo = "Denormalizado"
            except:
                tipo = "Infinito/NaN"
                continue
        
        decoded = ieee_single.decode(s, e, m)
        print(f"{val:<15.6e} {tipo:<15} {decoded:<15.6e}")
    
    # Infinito y NaN
    print(f"\nInfinito y NaN:")
    s, e, m = ieee_single.encode_infinity(positive=True)
    print(f"  +inf: {ieee_single.decode(s, e, m)}")
    
    s, e, m = ieee_single.encode_infinity(positive=False)
    print(f"  -inf: {ieee_single.decode(s, e, m)}")
    
    s, e, m = ieee_single.encode_nan(quiet=True)
    print(f"  qNaN (quiet): {ieee_single.decode(s, e, m)}")
    
    s, e, m = ieee_single.encode_nan(quiet=False)
    print(f"  sNaN (signaling): {ieee_single.decode(s, e, m)}")
    
    # Ejemplo 2: IEEE 754 Double (base 2, 11 bits expon, 52 bits mantisa)
    print("\n--- IEEE 754 Double (64 bits) ---")
    ieee_double = IEEE754Gen(E_bits=11, F_bits=52, base=2)
    print(f"Config: {ieee_double}")
    print(f"Total bits: {1 + ieee_double.E_bits + ieee_double.F_bits}")
    print(f"Bias: {ieee_double.bias}")
    
    info = ieee_double.info
    print(f"Rango normalizado: [{info['normalized_min']:.6e}, {info['max']:.6e}]")
    
    # Ejemplo 3: Punto flotante decimal (base 10)
    print("\n--- Punto Flotante Decimal (base 10, E=3, F=5) ---")
    ieee_decimal = IEEE754Gen(E_bits=3, F_bits=5, base=10)
    print(f"Config: {ieee_decimal}")
    print(f"Bias: {ieee_decimal.bias}")
    
    info = ieee_decimal.info
    print(f"Rango normalizado: [{info['normalized_min']:.2e}, {info['max']:.2e}]")
    
    val = 12.34567
    s, e, m = ieee_decimal.encode_normalized(val)
    decoded = ieee_decimal.decode(s, e, m)
    print(f"\nCodificación de {val}:")
    print(f"  Sign={s}, E={e}, M={m}")
    print(f"  Decodificado: {decoded}")
    
    # Ejemplo 4: Punto flotante base 16 (hexadecimal)
    print("\n--- Punto Flotante Hexadecimal (base 16, E=2, F=4) ---")
    ieee_hex = IEEE754Gen(E_bits=2, F_bits=4, base=16)
    print(f"Config: {ieee_hex}")
    print(f"Bias: {ieee_hex.bias}")
    
    info = ieee_hex.info
    print(f"Rango normalizado: [{info['normalized_min']:.2e}, {info['max']:.2e}]")
    
    val = 255.0
    s, e, m = ieee_hex.encode_normalized(val)
    decoded = ieee_hex.decode(s, e, m)
    print(f"\nCodificación de {val}:")
    print(f"  Sign={s}, E={e}, M={m}")
    print(f"  Decodificado: {decoded}")


def demo_biquinary_gen():
    """Demostración de BiquinaryGen y sus subclases."""
    print("\n" + "="*80)
    print("BIQUINARIOS - TODAS LAS VARIANTES")
    print("="*80)
    
    # Ejemplo 1: Biquinario 7 bits (IBM 650)
    print("\n--- Biquinario 7 bits (IBM 650) ---")
    bq7 = Biquinary7Bit()
    print(f"Config: {bq7}")
    
    print(f"\nTabla de codificación:")
    print(f"{'D':<3} {'Quina':<8} {'Bina':<8} {'Código':<10}")
    print("-" * 30)
    for d in range(10):
        q, b = bq7.encode_table[d]
        code = bq7.encode(d)
        print(f"{d:<3} {q:03b}     {b:02b}      {code:07b}")
    
    # Codificar números
    print(f"\nCodificacion de numeros:")
    for num_str in ["12345", "67890", "314159"]:
        codes = bq7.encode_number(num_str)
        codes_bin = ' '.join(f"{c:07b}" for c in codes)
        decoded = bq7.decode_number(codes)
        print(f"  {num_str} -> {codes_bin}")
        print(f"      OK Decodificado: {decoded}")
    
    # Ejemplo 2: Biquinario 5 bits (Univac 60/120)
    print("\n--- Biquinario 5 bits (Univac 60/120) ---")
    bq5 = Biquinary5Bit()
    print(f"Config: {bq5}")
    
    print(f"\nTabla de codificación:")
    print(f"{'D':<3} {'Quina':<8} {'Bina':<8} {'Código':<10}")
    print("-" * 30)
    for d in range(10):
        q, b = bq5.encode_table[d]
        code = bq5.encode(d)
        print(f"{d:<3} {q:02b}     {b:03b}      {code:05b}")
    
    # Codificar números
    print(f"\nCodificación de números:")
    for num_str in ["12345", "67890", "999999"]:
        codes = bq5.encode_number(num_str)
        codes_bin = ' '.join(f"{c:05b}" for c in codes)
        decoded = bq5.decode_number(codes)
        print(f"  {num_str} -> {codes_bin}")
        print(f"      OK Decodificado: {decoded}")
    
    # Ejemplo 3: Biquinario 6 bits (IBM 1401)
    print("\n--- Biquinario 6 bits (IBM 1401) ---")
    bq6 = Biquinary6Bit()
    print(f"Config: {bq6}")
    
    print(f"\nTabla de codificacion (primeros 5 digitos):")
    print(f"{'D':<3} {'Quina':<8} {'Bina':<8} {'Codigo':<10}")
    print("-" * 30)
    for d in range(5):
        q, b = bq6.encode_table[d]
        code = bq6.encode(d)
        print(f"{d:<3} {q:02b}     {b:03b}      {code:06b}")
    
    # Codificar números
    print(f"\nCodificacion de numeros:")
    for num_str in ["12345"]:
        codes = bq6.encode_number(num_str)
        codes_bin = ' '.join(f"{c:06b}" for c in codes)
        decoded = bq6.decode_number(codes)
        print(f"  {num_str} -> {codes_bin}")
        print(f"      OK Decodificado: {decoded}")


def demo_comparacion():
    """Comparación entre variantes de biquinarios."""
    print("\n" + "="*80)
    print("COMPARACION: EFICIENCIA DE BIQUINARIOS")
    print("="*80)
    
    variantes = [
        ("Biquinario 7 bits (IBM 650)", Biquinary7Bit()),
        ("Biquinario 5 bits (Univac)", Biquinary5Bit()),
        ("Biquinario 6 bits (IBM 1401)", Biquinary6Bit()),
    ]
    
    test_number = "123456789"
    
    print(f"\nCodificacion del numero: {test_number}")
    print(f"{'Variante':<30} {'Bits Totales':<15} {'Eficiencia':<15} {'Codigos':<50}")
    print("-" * 110)
    
    import math
    log2_10 = math.log2(10)  # ~3.322 bits ideales para un dígito
    
    for nombre, bq in variantes:
        codes = bq.encode_number(test_number)
        total_bits = len(test_number) * bq.total_bits
        ideal_bits = len(test_number) * log2_10
        efficiency = ideal_bits / bq.total_bits
        codes_str = ','.join(f"{c:0{bq.total_bits}b}" for c in codes[:3]) + "..."
        
        print(f"{nombre:<30} {total_bits:<15} {efficiency:>6.3f}x{'':<7} {codes_str:<50}")
    
    print(f"\nNota: Eficiencia ideal = {log2_10:.3f} bits/dígito")
    print(f"      Valores > 1.0 significan 'bits extra' por dígito (redundancia)")


if __name__ == "__main__":
    demo_ieee754_gen()
    demo_biquinary_gen()
    demo_comparacion()
