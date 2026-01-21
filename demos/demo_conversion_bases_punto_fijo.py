"""
Demostración Completa: Conversiones entre Bases en Punto Fijo

Este script muestra ejemplos prácticos de conversiones respetando
la regla fundamental: B'_F' >= B^F
"""

from core.punto_fijo import FixedPoint
from core.conversion_bases_punto_fijo import (
    convert_fixed_point_base,
    convert_multiple_bases,
    find_min_F_prime,
    verify_precision_rule
)
from decimal import Decimal


def print_header(title: str):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def print_conversion_details(original, converted, info):
    """Mostrar detalles de una conversión."""
    print(f"Original: {info['source_format']}")
    print(f"  Valor: {info['source_value']}")
    print(f"  M (valor crudo): {info['source_raw']}")
    print(f"\nDestino: {info['dest_format']}")
    print(f"  Valor: {info['dest_value']}")
    print(f"  M' (valor crudo): {info['dest_raw']}")
    print(f"\nRegla de precision: {info['rule_satisfied']}")
    print(f"Perdida de precision: {info['precision_loss']}")


# ============================================================================
# EJEMPLO 1: Conversion Simple - Base 2 a Base 10
# ============================================================================

print_header("EJEMPLO 1: Conversion Q(8,8)_2 a Q(8,F')_10")

# Crear numero en Q(8,8) base 2
fp = FixedPoint(8, 8, B=2, value=42.5625)
print(f"Numero original en binario:")
print(f"  {fp}\n  Formato: Q(8,8) base 2")
print(f"  Valor crudo M = {fp.raw_value}")
print(f"  Estructura: Parte entera (8 bits) | Parte fraccionaria (8 bits)")
print(f"  {bin(fp.raw_value)[2:].zfill(16)}")

# Calcular F' necesario
F_original = fp.F
F_prime = find_min_F_prime(F_original, 2, 10)
print(f"\nCalculando F' para base 10:")
print(f"  Necesitamos: 10^F' >= 2^{F_original} = {2**F_original}")
print(f"  F' minimo = {F_prime}")
print(f"  Verificacion: 10^{F_prime} = {10**F_prime} >= {2**F_original} OK")

# Realizar conversion
fp_decimal, info = convert_fixed_point_base(fp, 8, 10, F_prime)
print(f"\nResultado:")
print_conversion_details(fp, fp_decimal, info)


# ============================================================================
# EJEMPLO 2: Doble Conversion - Base 2 -> Base 10 -> Base 16
# ============================================================================

print_header("EJEMPLO 2: Doble Conversion 2 -> 10 -> 16")

# Comenzar con binario
fp_binary = FixedPoint(8, 8, B=2, value=12.375)
print(f"1. Original en base 2:")
print(f"  {fp_binary} (Q(8,8) base 2)")

# Convertir a base 10
F_10 = find_min_F_prime(8, 2, 10)
fp_decimal, info1 = convert_fixed_point_base(fp_binary, 8, 10, F_10)
print(f"\n2. Convertir a base 10:")
print(f"  Q(8,{F_10}) base 10")
print(f"  Valor: {fp_decimal.value}")

# Convertir el resultado decimal a hexadecimal
F_16 = find_min_F_prime(F_10, 10, 16)
fp_hex, info2 = convert_fixed_point_base(fp_decimal, 8, 16, F_16)
print(f"\n3. Convertir a base 16:")
print(f"  Q(8,{F_16}) base 16")
print(f"  Valor: {fp_hex.value}")

# Comparar con conversion directa
F_16_direct = find_min_F_prime(8, 2, 16)
fp_hex_direct, info3 = convert_fixed_point_base(fp_binary, 8, 16, F_16_direct)
print(f"\n4. Comparar con conversion directa 2 -> 16:")
print(f"  Q(8,{F_16_direct}) base 16")
print(f"  Valor: {fp_hex_direct.value}")
print(f"\nAmbas rutas llegan al mismo valor: {fp_hex.value == fp_hex_direct.value}")


# ============================================================================
# EJEMPLO 3: Precision en Diferentes Formatos
# ============================================================================

print_header("EJEMPLO 3: Analisis de Precision en Conversiones")

# Numero con muchos decimales
fp_original = FixedPoint(8, 8, B=2, value=100.123456)
print(f"Numero original: {fp_original}")
print(f"Valor exacto: {fp_original.value}")
print(f"Epsilon (minima diferencia representable): {fp_original.epsilon}")

# Conversiones a diferentes bases
bases = [2, 8, 10, 16]
print(f"\nConversiones:")
print(f"{'Base':<6} {'F_prime':<8} {'Valor':<25} {'Perdida':<20}")
print("-" * 65)

for base in bases:
    if base == 2:
        print(f"{base:<6} {8:<8} {float(fp_original.value):<25} {'0':<20}")
    else:
        F_p = find_min_F_prime(8, 2, base)
        fp_conv, info = convert_fixed_point_base(fp_original, 8, base, F_p)
        print(f"{base:<6} {F_p:<8} {float(fp_conv.value):<25} {info['precision_loss']:<20}")


# ============================================================================
# EJEMPLO 4: Casos Problematicos
# ============================================================================

print_header("EJEMPLO 4: Casos Problematicos y Manejo de Errores")

# Caso 1: Numero que no cabe en formato destino
print("Caso 1: Overflow al convertir")
fp_large = FixedPoint(6, 4, B=2, value=50.5)
print(f"  Numero original: {fp_large} (Q(6,4) base 2)")
print(f"  Maximo representable: {fp_large.max_value}")

try:
    # Intentar convertir a Q(4,8) que tiene rango mas pequeno
    F_p = find_min_F_prime(4, 2, 10)
    fp_converted, _ = convert_fixed_point_base(fp_large, 4, 10, F_p)
    print(f"  Conversion: {fp_converted}")
except Exception as e:
    print(f"  Error capturado: {e}")

# Caso 2: Perdida de precision significativa
print(f"\nCaso 2: Perdida de precision en conversion")
fp_precise = FixedPoint(10, 16, B=2, value=1000.123456789)
print(f"  Original: {fp_precise} (Q(10,16) base 2)")
print(f"  Epsilon: {fp_precise.epsilon}")

F_p = find_min_F_prime(16, 2, 8)
fp_8, info = convert_fixed_point_base(fp_precise, 10, 8, F_p)
print(f"  Convertido: {fp_8} (Q(10,{F_p}) base 8)")
print(f"  Epsilon nuevo: {fp_8.epsilon}")
print(f"  Perdida: {info['precision_loss']}")


# ============================================================================
# EJEMPLO 5: Tabla Comparativa de Formatos
# ============================================================================

print_header("EJEMPLO 5: Tabla Comparativa de Formatos")

print("Conversiones del numero 25.75 entre diferentes formatos:\n")
print(f"{'Formato':<20} {'Valor':<25} {'Max Raw Value':<20}")
print("-" * 65)

num_value = 25.75
formats = [
    (6, 4, 2),
    (8, 8, 2),
    (6, 4, 10),
    (6, 4, 16),
]

for E, F, B in formats:
    fp = FixedPoint(E, F, B=B, value=num_value)
    print(f"Q({E},{F})_{{{B:2}}}            {float(fp.value):<25} {fp.max_raw_value:<20}")


# ============================================================================
# EJEMPLO 6: Cadena de Conversiones
# ============================================================================

print_header("EJEMPLO 6: Cadena de Conversiones entre 4 Bases")

fp_start = FixedPoint(8, 8, B=2, value=33.5)
print(f"Punto de inicio: {fp_start} (Q(8,8) base 2)")
print(f"Valor: {fp_start.value}\n")

# Cadena: 2 -> 8 -> 10 -> 16 -> 2
conversions = [
    (8, 8),
    (8, 10),
    (8, 16),
    (8, 2),
]

current_fp = fp_start
path = f"2"

for target_B, target_E in conversions:
    current_B = current_fp.B
    current_F = current_fp.F
    
    F_prime = find_min_F_prime(current_F, current_B, target_B)
    current_fp, info = convert_fixed_point_base(current_fp, target_E, target_B, F_prime)
    
    path += f" -> {target_B}"
    print(f"Paso: {path}")
    print(f"  Q({target_E},{current_fp.F}) base {target_B}")
    print(f"  Valor: {current_fp.value}")
    print(f"  Perdida acumulada: {abs(current_fp.value - fp_start.value)}\n")


# ============================================================================
# EJEMPLO 7: Verificacion de la Regla en Caso Critico
# ============================================================================

print_header("EJEMPLO 7: Verificacion Critica de la Regla B'_F' >= B^F")

print("Examinar la regla en casos criticos:\n")

critical_cases = [
    (1, 2, 10),   # Caso: F=1, B=2, B'=10
    (4, 2, 10),   # Caso: F=4, B=2, B'=10
    (10, 2, 8),   # Caso: F=10, B=2, B'=8
    (6, 10, 2),   # Caso: F=6, B=10, B'=2
]

print(f"{'Original':<15} {'Destino':<15} {'F_prime calc':<15} {'Regla Satisfied':<20}")
print("-" * 70)

for F, B, B_prime in critical_cases:
    F_prime = find_min_F_prime(F, B, B_prime)
    satisfied = verify_precision_rule(F, B, F_prime, B_prime)
    
    print(f"Q(E,{F:2})_{{{B:2}}}        Q(E,{F_prime:2})_{{{B_prime:2}}}        "
          f"{F_prime:<15} {'SI' if satisfied else 'NO':<20}")


print("\n" + "=" * 80)
print("FIN DE LA DEMOSTRACION")
print("=" * 80)
