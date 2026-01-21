"""
Tests para funciones genéricas de conversión entre bases
"""

from core.sistemas_numeracion_basicos import (
    decimal_a_base_B,
    base_B_a_decimal,
    base_B_a_base_B_prima,
    base_B_a_base_B_prima_potencias
)

print("=" * 80)
print("TEST: Conversiones Genéricas entre Bases")
print("=" * 80)

# Test 1: Decimal a Base B
print("\n1. decimal_a_base_B(numero, base) -> str")
print("-" * 80)

test_cases_1 = [
    (1994, 5, "30434"),
    (255, 2, "11111111"),
    (255, 16, "ff"),
    (27, 10, "27"),
    (100, 8, "144"),
]

for numero, base, esperado in test_cases_1:
    resultado = decimal_a_base_B(numero, base)
    estado = "[OK]" if resultado == esperado else "[FAIL]"
    print(f"{estado} decimal_a_base_B({numero}, {base}) = {resultado} (esperado: {esperado})")

# Test 2: Base B a Decimal
print("\n2. base_B_a_decimal(numero_str, base) -> int")
print("-" * 80)

test_cases_2 = [
    ("30434", 5, 1994),
    ("11111111", 2, 255),
    ("ff", 16, 255),
    ("27", 10, 27),
    ("144", 8, 100),
]

for numero_str, base, esperado in test_cases_2:
    resultado = base_B_a_decimal(numero_str, base)
    estado = "[OK]" if resultado == esperado else "[FAIL]"
    print(f"{estado} base_B_a_decimal('{numero_str}', {base}) = {resultado} (esperado: {esperado})")

# Test 3: Base B a Base B' (genérico)
print("\n3. base_B_a_base_B_prima(numero_str, base_origen, base_destino) -> str")
print("-" * 80)

test_cases_3 = [
    ("30434", 5, 2, "11111001010"),
    ("ff", 16, 10, "255"),
    ("1010", 2, 8, "12"),
    ("144", 8, 16, "64"),
]

for numero_str, base_orig, base_dest, esperado in test_cases_3:
    resultado = base_B_a_base_B_prima(numero_str, base_orig, base_dest)
    estado = "[OK]" if resultado == esperado else "[FAIL]"
    print(f"{estado} base_B_a_base_B_prima('{numero_str}', {base_orig}, {base_dest}) = {resultado} (esperado: {esperado})")

# Test 4: Base B a Base B' (potencias)
print("\n4. base_B_a_base_B_prima_potencias(numero_str, base_comun, exp_origen, exp_destino) -> str")
print("-" * 80)

test_cases_4 = [
    ("11111111", 2, 1, 4, "ff"),  # Binario a Hexadecimal
    ("ff", 2, 4, 1, "11111111"),  # Hexadecimal a Binario
    ("1111", 2, 1, 3, "17"),      # Binario a Octal
]

for numero_str, base_comun, exp_orig, exp_dest, esperado in test_cases_4:
    try:
        resultado = base_B_a_base_B_prima_potencias(numero_str, base_comun, exp_orig, exp_dest)
        estado = "[OK]" if resultado == esperado else "[FAIL]"
        print(f"{estado} base_B_a_base_B_prima_potencias('{numero_str}', {base_comun}, {exp_orig}, {exp_dest}) = {resultado} (esperado: {esperado})")
    except Exception as e:
        print(f"[FAIL] Error en base_B_a_base_B_prima_potencias('{numero_str}', {base_comun}, {exp_orig}, {exp_dest}): {e}")

print("\n" + "=" * 80)
print("Tests completados")
print("=" * 80)
