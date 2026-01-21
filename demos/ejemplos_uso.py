#!/usr/bin/env python3
"""
Ejemplos rápidos de uso: IEEE754Gen + Biquinarios
"""

from core.ieee754 import IEEE754Gen
from core.biquinarios import Biquinary7Bit, Biquinary5Bit, Biquinary6Bit


# ============================================================================
# EJEMPLO 1: IEEE754Gen con diferentes configuraciones
# ============================================================================

print("\n" + "="*70)
print("EJEMPLO 1: IEEE754Gen - Punto Flotante Genérico")
print("="*70)

# IEEE 754 Single (32 bits)
ieee32 = IEEE754Gen(E_bits=8, F_bits=23, base=2)
print(f"\nIEEE 754 Single: {ieee32}")

# Codificar número normalizado
sign, exp, mant = ieee32.encode_normalized(3.14159)
decoded = ieee32.decode(sign, exp, mant)
print(f"  Codificación de 3.14159: sign={sign}, exp={exp}, mant={mant}")
print(f"  Decodificado: {decoded:.6f}")

# IEEE 754 Double (64 bits)
ieee64 = IEEE754Gen(E_bits=11, F_bits=52, base=2)
print(f"\nIEEE 754 Double: {ieee64}")
info = ieee64.info
print(f"  Bias: {info['bias']}")
print(f"  Rango: [{info['normalized_min']:.2e}, {info['max']:.2e}]")

# Punto Flotante Decimal (Base 10)
ieee_decimal = IEEE754Gen(E_bits=3, F_bits=5, base=10)
print(f"\nPunto Flotante Decimal: {ieee_decimal}")
sign, exp, mant = ieee_decimal.encode_normalized(123.456)
decoded = ieee_decimal.decode(sign, exp, mant)
print(f"  Codificación de 123.456: sign={sign}, exp={exp}, mant={mant}")
print(f"  Decodificado: {decoded}")

# Casos especiales
print(f"\nCasos especiales (IEEE 754 Single):")
s, e, m = ieee32.encode_infinity(positive=True)
print(f"  +infinity: {ieee32.decode(s, e, m)}")

s, e, m = ieee32.encode_infinity(positive=False)
print(f"  -infinity: {ieee32.decode(s, e, m)}")

s, e, m = ieee32.encode_nan(quiet=True)
print(f"  qNaN: {ieee32.decode(s, e, m)}")

s, e, m = ieee32.encode_nan(quiet=False)
print(f"  sNaN: {ieee32.decode(s, e, m)}")


# ============================================================================
# EJEMPLO 2: Códigos Biquinarios - Todas las Variantes
# ============================================================================

print("\n" + "="*70)
print("EJEMPLO 2: Códigos Biquinarios")
print("="*70)

test_number = "123456789"

# Biquinario 7 bits (IBM 650)
print(f"\nBiquinario 7 bits (IBM 650):")
bq7 = Biquinary7Bit()
codes = bq7.encode_number(test_number)
decoded = bq7.decode_number(codes)
print(f"  Número: {test_number}")
print(f"  Códigos: {' '.join(f'{c:07b}' for c in codes[:3])}... ({len(codes)} códigos)")
print(f"  Decodificado: {decoded}")
print(f"  Bits totales: {len(codes) * 7}")

# Biquinario 5 bits (Univac 60/120)
print(f"\nBiquinario 5 bits (Univac 60/120):")
bq5 = Biquinary5Bit()
codes = bq5.encode_number(test_number)
decoded = bq5.decode_number(codes)
print(f"  Número: {test_number}")
print(f"  Códigos: {' '.join(f'{c:05b}' for c in codes[:3])}... ({len(codes)} códigos)")
print(f"  Decodificado: {decoded}")
print(f"  Bits totales: {len(codes) * 5}")

# Biquinario 6 bits (IBM 1401)
print(f"\nBiquinario 6 bits (IBM 1401):")
bq6 = Biquinary6Bit()
codes = bq6.encode_number(test_number)
decoded = bq6.decode_number(codes)
print(f"  Número: {test_number}")
print(f"  Códigos: {' '.join(f'{c:06b}' for c in codes[:3])}... ({len(codes)} códigos)")
print(f"  Decodificado: {decoded}")
print(f"  Bits totales: {len(codes) * 6}")


# ============================================================================
# EJEMPLO 3: Codificar/Decodificar Dígitos Individuales
# ============================================================================

print("\n" + "="*70)
print("EJEMPLO 3: Dígitos Individuales")
print("="*70)

bq7 = Biquinary7Bit()

print(f"\nBiquinario 7 bits (primeros 5 dígitos):")
print(f"{'Dígito':<8} {'Código 7 bits':<20} {'Decodificado':<15}")
print("-" * 45)

for digit in range(5):
    code = bq7.encode(digit)
    decoded = bq7.decode(code)
    print(f"{digit:<8} {code:07b}         {decoded:<15}")

# El resto
for digit in range(5, 10):
    code = bq7.encode(digit)
    decoded = bq7.decode(code)
    print(f"{digit:<8} {code:07b}         {decoded:<15}")


# ============================================================================
# EJEMPLO 4: Tabla Comparativa de Eficiencia
# ============================================================================

print("\n" + "="*70)
print("EJEMPLO 4: Comparación de Eficiencia")
print("="*70)

import math

test_numbers = ["12345", "67890", "314159", "123456789"]
log2_10 = math.log2(10)

for num_str in test_numbers:
    print(f"\nNúmero: {num_str}")
    print(f"{'Variante':<30} {'Bits Totales':<15} {'vs Ideal':<15}")
    print("-" * 60)
    
    ideal_bits = len(num_str) * log2_10
    print(f"{'Ideal (log2(10))':<30} {ideal_bits:.1f}{'':<8} {1.0:<15}")
    
    variants = [
        ("Biquinario 7 bits", Biquinary7Bit()),
        ("Biquinario 5 bits", Biquinary5Bit()),
        ("Biquinario 6 bits", Biquinary6Bit()),
    ]
    
    for nombre, bq in variants:
        codes = bq.encode_number(num_str)
        total_bits = len(codes) * bq.total_bits
        ratio = total_bits / ideal_bits
        print(f"{nombre:<30} {total_bits:<15} {ratio:.2f}x")


# ============================================================================
# EJEMPLO 5: Manejo de Errores
# ============================================================================

print("\n" + "="*70)
print("EJEMPLO 5: Manejo de Errores")
print("="*70)

bq7 = Biquinary7Bit()

print("\nIntentar codificar dígito inválido:")
try:
    code = bq7.encode(15)  # Fuera de rango
except ValueError as e:
    print(f"  Error capturado: {e}")

print("\nIntentar decodificar código inválido:")
try:
    digit = bq7.decode(0b1111111)  # Código inválido
except ValueError as e:
    print(f"  Error capturado: {e}")

print("\nIntentar codificar carácter no numérico:")
try:
    codes = bq7.encode_number("12A45")  # Contiene 'A'
except ValueError as e:
    print(f"  Error capturado: {e}")


print("\n" + "="*70)
print("FIN DE EJEMPLOS")
print("="*70)
