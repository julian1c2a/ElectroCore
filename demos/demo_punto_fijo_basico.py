"""
Demostración de Punto Fijo Q(E,F)

Este script muestra:
1. Propiedades fundamentales de Q(E,F): epsilon, máximo, rango
2. Operaciones aritméticas: suma, resta, multiplicación, división
3. Comparación de formatos diferentes
4. Conversión binaria
"""

from core.punto_fijo import FixedPoint
from decimal import Decimal


def print_section(title: str):
    """Imprimir título de sección."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


# ============================================================================
# 1. PROPIEDADES FUNDAMENTALES
# ============================================================================

print_section("1. PROPIEDADES FUNDAMENTALES DE Q(E,F)")

# Ejemplo 1: Q(8,8) en base 2
print("Q(8,8) base 2 (16 bits totales):")
print(FixedPoint.format_info(8, 8, B=2))

# Ejemplo 2: Q(16,16) en base 2
print("\nQ(16,16) base 2 (32 bits totales):")
print(FixedPoint.format_info(16, 16, B=2))

# Ejemplo 3: Base 10
print("\nQ(10,6) base 10 (16 dígitos totales):")
print(FixedPoint.format_info(10, 6, B=10))


# ============================================================================
# 2. CREACIÓN E INFORMACIÓN
# ============================================================================

print_section("2. CREACIÓN DE NÚMEROS Q(E,F)")

# Crear varios números en Q(8,8) base 2
fp1 = FixedPoint(8, 8, B=2, value=5.25)
fp2 = FixedPoint(8, 8, B=2, value=3.75)
fp3 = FixedPoint(8, 8, B=2, value=0.125)

print(f"fp1 = {fp1} (Q(8,8) base 2):")
print(fp1.info())

print(f"\nfp2 = {fp2} (Q(8,8) base 2):")
print(fp2.info())

print(f"\nfp3 = {fp3} (Q(8,8) base 2):")
print(fp3.info())


# ============================================================================
# 3. OPERACIONES ARITMÉTICAS
# ============================================================================

print_section("3. OPERACIONES ARITMÉTICAS")

print("Suma: 5.25 + 3.75 = 9.0")
result_sum = fp1 + fp2
print(f"Resultado: {result_sum}")
print(f"Valor crudo: M = {result_sum.raw_value}")
print(f"Verificación: {result_sum.raw_value} * 2^(-8) = {result_sum.value}\n")

print("Resta: 5.25 - 3.75 = 1.5")
result_sub = fp1 - fp2
print(f"Resultado: {result_sub}")
print(f"Valor crudo: M = {result_sub.raw_value}")
print(f"Verificación: {result_sub.raw_value} * 2^(-8) = {result_sub.value}\n")

print("Multiplicación: 5.25 * 3.75 = 19.6875")
result_mul = fp1 * fp2
print(f"Resultado: {result_mul}")
print(f"Valor crudo: M = {result_mul.raw_value}")
print(f"Verificación: {result_mul.raw_value} * 2^(-8) = {result_mul.value}\n")

print("División: 5.25 / 3.75 = 1.4")
result_div = fp1 / fp2
print(f"Resultado: {result_div}")
print(f"Valor crudo: M = {result_div.raw_value}")
print(f"Verificación: {result_div.raw_value} * 2^(-8) = {result_div.value}\n")


# ============================================================================
# 4. COMPARACIÓN
# ============================================================================

print_section("4. COMPARACIÓN DE NÚMEROS Q(E,F)")

print(f"fp1 = {fp1}")
print(f"fp2 = {fp2}")
print(f"fp3 = {fp3}\n")

print(f"fp1 == {fp1}: {fp1 == fp1}")
print(f"fp1 != fp2: {fp1 != fp2}")
print(f"fp1 > fp2: {fp1 > fp2}")
print(f"fp1 < fp2: {fp1 < fp2}")
print(f"fp3 < fp2: {fp3 < fp2}\n")

# Ordenamiento
numeros = [fp2, fp3, fp1]
numeros_ordenados = sorted(numeros)
print("Ordenamiento ascendente:")
for num in numeros_ordenados:
    print(f"  {num}")


# ============================================================================
# 5. EPSILON Y LÍMITES
# ============================================================================

print_section("5. ÉPSILON Y LÍMITES DE REPRESENTACIÓN")

print(f"Q(8,8) base 2:")
print(f"  Épsilon (mínimo no-cero): {fp1.epsilon}")
print(f"  Máximo representable: {fp1.max_value}")
print(f"  Rango: [{fp1.min_value}, {fp1.max_value}]\n")

# Crear número muy pequeño
fp_tiny = FixedPoint(8, 8, B=2, value=float(FixedPoint(8, 8, B=2).epsilon))
print(f"Número mínimo posible: {fp_tiny} (épsilon)")
print(f"Verificación: ε = 2^(-8) = 1/256 = {float(Decimal(1) / Decimal(256))}\n")

# Crear número cerca del máximo
fp_large = FixedPoint(8, 8, B=2, value=255.99609375)  # Cerca del máximo
print(f"Número próximo al máximo: {fp_large}")
print(f"Máximo real: {fp_large.max_value}")


# ============================================================================
# 6. DIFERENTES FORMATOS
# ============================================================================

print_section("6. COMPARACIÓN DE DIFERENTES FORMATOS Q(E,F)")

formats = [
    (4, 4, 2),
    (8, 8, 2),
    (16, 16, 2),
    (10, 6, 10),
    (12, 8, 2),
]

print("Formato      | Bits | Épsilon      | Máximo Valor | Rango (Bits) | Max Raw")
print("-" * 85)

for E, F, B in formats:
    fp = FixedPoint(E, F, B, value=0)
    eps = float(fp.epsilon)
    max_val = float(fp.max_value)
    max_raw = fp.max_raw_value
    print(f"Q({E:2},{F:2})₍{B}₎ | {E+F:4} | {eps:12.10f} | {max_val:12.2f} | {E+F:12} | {max_raw}")


# ============================================================================
# 7. OPERACIONES EN DIFERENTES BASES
# ============================================================================

print_section("7. OPERACIONES EN BASE 10")

# Números en Q(10,6) base 10
q_dec_1 = FixedPoint(10, 6, B=10, value=123.456789)
q_dec_2 = FixedPoint(10, 6, B=10, value=45.123456)

print(f"Número 1: {q_dec_1} (Q(10,6) base 10)")
print(f"Número 2: {q_dec_2} (Q(10,6) base 10)")
print(f"Épsilon en base 10: {q_dec_1.epsilon}\n")

suma_dec = q_dec_1 + q_dec_2
print(f"Suma: {q_dec_1} + {q_dec_2} = {suma_dec}")

mult_dec = q_dec_1 * q_dec_2
print(f"Multiplicación: {q_dec_1} * {q_dec_2} = {mult_dec}")


# ============================================================================
# 8. CASOS DE LÍMITE Y ERRORES
# ============================================================================

print_section("8. CASOS DE LÍMITE Y MANEJO DE ERRORES")

# Overflow
print("Test de Overflow:")
try:
    fp_max = FixedPoint(4, 4, B=2, value=15.93)
    print(f"  Número máximo Q(4,4): {fp_max}")
    fp_overflow = fp_max + FixedPoint(4, 4, B=2, value=0.1)
except OverflowError as e:
    print(f"  ✓ Capturado: {e}")

print("\nTest de Underflow (pérdida de precisión):")
fp_small = FixedPoint(8, 8, B=2, value=1.0)
fp_tiny_add = FixedPoint(8, 8, B=2, value=0.001)  # Menor que epsilon
print(f"  Número: {fp_small}")
print(f"  Sumando: {fp_tiny_add} (menor que épsilon = {fp_small.epsilon})")
result = fp_small + fp_tiny_add
print(f"  Resultado: {result} (pérdida de precisión)")

print("\nTest de División por cero:")
try:
    fp_zero = FixedPoint(8, 8, B=2, value=0)
    result = fp1 / fp_zero
except ZeroDivisionError as e:
    print(f"  ✓ Capturado: {e}")

print("\nTest de Representación de valor negativo:")
try:
    fp_neg = FixedPoint(8, 8, B=2, value=-5.0)
except ValueError as e:
    print(f"  ✓ Capturado: {e}")


# ============================================================================
# 9. REPRESENTACIÓN BINARIA
# ============================================================================

print_section("9. REPRESENTACIÓN BINARIA")

fp_demo = FixedPoint(8, 8, B=2, value=5.25)
print(f"Número: {fp_demo}")
print(f"Valor crudo: M = {fp_demo.raw_value}")
print(f"Binario: {fp_demo.to_binary()}")
print(f"Hexadecimal: {fp_demo.to_hex()}")
print(f"\nInterpretación:")
print(f"  M = {fp_demo.raw_value} = 0x{fp_demo.raw_value:04x}")
print(f"  Valor = M × 2^(-8) = {fp_demo.raw_value} × 1/256 = {fp_demo.value}")

# Mostrar estructura binaria
binary_str = bin(fp_demo.raw_value)[2:].zfill(16)
print(f"\nEstructura en Q(8,8):")
print(f"  {binary_str}")
print(f"  {' ' * 8}↑ Punto decimal (después de 8 bits)")
print(f"  Parte entera (8 bits): {binary_str[:8]}")
print(f"  Parte fraccionaria (8 bits): {binary_str[8:]}")


# ============================================================================
# 10. RESUMEN FINAL
# ============================================================================

print_section("10. RESUMEN DE PUNTO FIJO Q(E,F)")

print("""
CONCEPTOS CLAVE:

1. FORMATO Q(E,F):
   - E: número de dígitos para parte entera
   - F: número de dígitos para parte fraccionaria
   - L = E + F: longitud total

2. VALOR REPRESENTADO:
   - Valor = M × B^(-F), donde M es el valor crudo del registro
   - Ejemplo: Q(8,8) base 2: valor 5.25 → M = 1344 → 1344 × 2^(-8) = 5.25

3. ÉPSILON (Precisión):
   - ε = B^(-F) = mínimo valor no-cero representable
   - Ejemplo: Q(8,8) base 2: ε = 2^(-8) = 0.00390625

4. RANGO:
   - Positivos: [0, B^E - B^(-F)]
   - Ejemplo: Q(8,8) base 2: [0, 255.99609375]

5. OPERACIONES:
   - Suma/Resta: (M1 ± M2) × B^(-F)
   - Multiplicación: (M1 × M2) / B^F  (reescalado)
   - División: (M1 × B^F) / M2  (reescalado)

6. COMPARACIÓN:
   - Exacta comparando valores crudos M
   - Igual que con enteros hasta posición -F

7. EFICACIA:
   - 100%: no hay representaciones repetidas ni sin sentido
   - Cada combinación de L bits representa un valor único
""")

print("=" * 70)
