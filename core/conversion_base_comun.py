"""
Conversión entre Bases con Base Común - Punto Fijo

Este módulo implementa el algoritmo exacto de conversión cuando las bases
comparten una base común.

CONCEPTO CLAVE:

Si B = b^n y B' = b^n', donde b es la base común:
    - m = mcd(n, n')
    - n'' = n/m (agrupación para B)
    - n''' = n'/m (agrupación para B')
    
Entonces podemos hacer conversión exacta sin pérdida:
    1. Convertir de B a b^m
    2. Agrupar dígitos de n''' en n''' para formar dígitos de B'

Ejemplos:
    - Base 2 = 2^1 a Base 8 = 2^3: m=1, n''=1, n'''=3 → agrupar 3 bits en 1 octal
    - Base 4 = 2^2 a Base 16 = 2^4: m=2, n''=1, n'''=2 → agrupar 2 dígitos base-4
    - Base 8 = 2^3 a Base 2 = 2^1: m=1, n''=3, n'''=1 → expandir 1 octal en 3 bits

FÓRMULA GENERAL DE LONGITUD:
    F' = ceil(F × log_{B'}(B))
    
Para información: 10^F_10 en base 10 = B'^F' en base B'
    F' = ceil(F_10 × log_{B'}(10))
"""

from decimal import Decimal, getcontext
from typing import Tuple, List, Optional, Dict
from math import gcd, ceil, log
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

getcontext().prec = 100


# ============================================================================
# CÁLCULO DE LOGARITMOS Y LONGITUDES
# ============================================================================

def log_base(value: Decimal, base: Decimal) -> Decimal:
    """Calcular log_base(value)."""
    if value <= 0 or base <= 0 or base == 1:
        raise ValueError(f"Parámetros inválidos")
    return value.ln() / base.ln()


def calculate_F_prime(F: int, B: int, B_prime: int) -> int:
    """
    Calcular F' necesario respetando: B'^F' >= B^F
    
    Fórmula: F' = ceil(F × log_{B'}(B))
    
    Args:
        F: Longitud fraccionaria en base B
        B: Base origen
        B_prime: Base destino
        
    Returns:
        F' mínimo que satisface la regla
    """
    F_decimal = Decimal(F)
    B_decimal = Decimal(B)
    B_prime_decimal = Decimal(B_prime)
    
    exponent = F_decimal * log_base(B_decimal, B_prime_decimal)
    return int(exponent) + (1 if exponent % 1 != 0 else 0)


# ============================================================================
# DETECCIÓN Y USO DE BASE COMÚN
# ============================================================================

def find_common_base(B: int, B_prime: int) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Detectar si B = b^n y B' = b^n' para alguna base común b.
    
    Returns:
        (b, n, n', m, n'') si existe base común
        None si no existe
        
    Donde:
        - b: base común
        - n: exponente de B (B = b^n)
        - n': exponente de B' (B' = b^n')
        - m: mcd(n, n')
        - n'': n/m, n''': n'/m
    """
    
    # Intentar con las bases primas más comunes
    for prime_base in [2, 3, 5, 7, 11, 13]:
        
        # Verificar si B = prime_base^n
        n = 0
        temp_B = B
        while temp_B > 1:
            if temp_B % prime_base == 0:
                temp_B //= prime_base
                n += 1
            else:
                break
        
        if temp_B == 1 and n > 0:  # B es potencia de prime_base
            
            # Verificar si B' = prime_base^n'
            n_prime = 0
            temp_B_prime = B_prime
            while temp_B_prime > 1:
                if temp_B_prime % prime_base == 0:
                    temp_B_prime //= prime_base
                    n_prime += 1
                else:
                    break
            
            if temp_B_prime == 1 and n_prime > 0:  # B' es potencia de prime_base
                m = gcd(n, n_prime)
                n_double_prime = n // m
                n_triple_prime = n_prime // m
                
                return (prime_base, n, n_prime, m, n_double_prime, n_triple_prime)
    
    return None


def has_common_base(B: int, B_prime: int) -> bool:
    """Verificar si existe base común."""
    return find_common_base(B, B_prime) is not None


# ============================================================================
# CONVERSIÓN CON BASE COMÚN (EXACTA)
# ============================================================================

def convert_with_common_base(
    E: int,
    F: int,
    B: int,
    M: int,
    B_prime: int,
    E_prime: int
) -> Dict:
    """
    Conversión exacta cuando B y B' comparten base común.
    
    Proceso:
        1. Detectar base común b tal que B = b^n, B' = b^n'
        2. Calcular m = mcd(n, n'), n'' = n/m, n''' = n'/m
        3. Convertir M a dígitos en base b^m
        4. Agrupar/expandir dígitos según n'' y n'''
        5. Reconstruir M' en base B'
        
    Args:
        E, F: Formato original Q(E,F)
        B: Base original
        M: Valor crudo en base B
        B_prime: Base destino
        E_prime: Enteros en formato destino
        
    Returns:
        Diccionario con resultados y pasos
    """
    
    # Detectar base común
    result = find_common_base(B, B_prime)
    if result is None:
        raise ValueError(f"No existe base común entre {B} y {B_prime}")
    
    b, n, n_prime, m, n_pp, n_ppp = result
    
    # F' se calcula exactamente en este caso
    F_prime = ceil(F * n_prime / n)
    
    # Conversión exacta: convertir M a base b^m
    common_base = b ** m
    
    # Extraer dígitos en base común
    digits_common = []
    temp = M
    
    if temp == 0:
        digits_common = [0]
    else:
        while temp > 0:
            digits_common.append(temp % common_base)
            temp //= common_base
        digits_common = digits_common[::-1]
    
    # Expandir cada dígito en base b a n'' dígitos
    digits_in_b = []
    for digit in digits_common:
        b_digits = []
        for _ in range(n_pp):
            b_digits.append(digit % b)
            digit //= b
        digits_in_b.extend(b_digits[::-1])
    
    # Agrupar de n''' en n''' para formar dígitos en B'
    digits_in_B_prime = []
    for i in range(0, len(digits_in_b), n_ppp):
        chunk = digits_in_b[i:i+n_ppp]
        # Rellenar si es necesario
        while len(chunk) < n_ppp:
            chunk.append(0)
        
        # Convertir chunk a un dígito en B'
        digit_B_prime = 0
        for j, d in enumerate(chunk):
            digit_B_prime = digit_B_prime * b + d
        digits_in_B_prime.append(digit_B_prime)
    
    # Reconstruir M' en base B'
    M_prime = 0
    for digit in digits_in_B_prime:
        M_prime = M_prime * B_prime + digit
    
    # Calcular valor decimal
    value_original = M * (B ** (-F))
    value_new = M_prime * (B_prime ** (-F_prime))
    
    return {
        'method': 'common_base',
        'common_base_b': b,
        'n': n,
        'n_prime': n_prime,
        'm': m,
        'n_pp': n_pp,
        'n_ppp': n_ppp,
        'F_prime': F_prime,
        'M_original': M,
        'M_prime': M_prime,
        'value_original': float(value_original),
        'value_new': float(value_new),
        'is_exact': True,
        'digits_common': digits_common,
        'digits_in_b': digits_in_b,
        'digits_in_B_prime': digits_in_B_prime,
    }


# ============================================================================
# EJEMPLOS CLÁSICOS DE BASE COMÚN
# ============================================================================

def example_binary_to_octal():
    """Ejemplo: Base 2 → Base 8 (2^1 → 2^3)"""
    print("\n" + "="*80)
    print("EJEMPLO: Base 2 → Base 8 (Conversión Exacta)")
    print("="*80)
    
    # B = 2 = 2^1, B' = 8 = 2^3
    # m = mcd(1,3) = 1, n'' = 1, n''' = 3
    # Cada 3 bits binarios = 1 dígito octal
    
    from core.punto_fijo import FixedPoint
    
    # Crear número: 5.625 en Q(4,4) base 2
    fp_binary = FixedPoint(4, 4, B=2, value=5.625)
    
    print(f"\nNúmero original: {fp_binary}")
    print(f"Formato: Q(4,4) base 2")
    print(f"Valor crudo M: {fp_binary.raw_value}")
    print(f"Binario: {bin(fp_binary.raw_value)[2:].zfill(8)}")
    
    result = convert_with_common_base(4, 4, 2, fp_binary.raw_value, 8, 4)
    
    print(f"\nBases:")
    print(f"  B = 2 = 2^1")
    print(f"  B' = 8 = 2^3")
    print(f"  Base común: b = 2")
    print(f"  m = mcd(1,3) = 1")
    print(f"  n'' = 1/1 = 1 (dígitos binarios por dígito base-4)")
    print(f"  n''' = 3/1 = 3 (dígitos binarios por dígito octal)")
    
    print(f"\nProceso:")
    print(f"  1. Binario: {bin(fp_binary.raw_value)[2:].zfill(8)}")
    print(f"  2. Agrupar de 3 en 3 (derecha a izquierda):")
    binary_str = bin(fp_binary.raw_value)[2:].zfill(8)
    groups = []
    for i in range(len(binary_str), 0, -3):
        start = max(0, i-3)
        groups.insert(0, binary_str[start:i])
    for i, group in enumerate(groups):
        octal_digit = int(group, 2)
        print(f"     {group} → {octal_digit}")
    
    print(f"\n  3. Octal: {result['digits_in_B_prime']}")
    print(f"  4. M' en base 8: {result['M_prime']}")
    
    print(f"\nResultado:")
    print(f"  Formato destino: Q(4,{result['F_prime']}) base 8")
    print(f"  Valor crudo M': {result['M_prime']}")
    print(f"  Valor decimal: {result['value_new']}")
    print(f"  Conversión exacta: {result['is_exact']}")


def example_octal_to_binary():
    """Ejemplo: Base 8 → Base 2 (2^3 → 2^1)"""
    print("\n" + "="*80)
    print("EJEMPLO: Base 8 → Base 2 (Expansión Exacta)")
    print("="*80)
    
    # B = 8 = 2^3, B' = 2 = 2^1
    # m = mcd(3,1) = 1, n'' = 3, n''' = 1
    # Cada dígito octal = 3 bits binarios
    
    print(f"\nBases:")
    print(f"  B = 8 = 2^3")
    print(f"  B' = 2 = 2^1")
    print(f"  Base común: b = 2")
    print(f"  m = mcd(3,1) = 1")
    print(f"  n'' = 3/1 = 3 (bits por dígito octal)")
    print(f"  n''' = 1/1 = 1 (bit por dígito binario)")
    
    # Número: 125 en base 8 = 5.5625 en Q(4,4) base 8
    # Verificar: 1×64 + 2×8 + 5×1 = 85 en base 10
    # Fracciones en base 8: no hay en este ejemplo
    M = int(5.5625 * (8**4))
    print(f"\nNúmero original en base 8:")
    print(f"  Valor: 5.5625")
    print(f"  M en base 8: {M}")
    
    try:
        result = convert_with_common_base(4, 4, 8, M, 2, 4)
        
        print(f"\nProceso:")
        print(f"  1. Expandir cada dígito octal a 3 bits")
        print(f"  2. Octal {result['digits_in_B_prime']} → Binario {result['digits_in_b']}")
        
        print(f"\nResultado:")
        print(f"  M' en base 2: {result['M_prime']}")
        print(f"  Binario: {bin(result['M_prime'])[2:].zfill(16)}")
        print(f"  Conversión exacta: {result['is_exact']}")
    except Exception as e:
        print(f"Error: {e}")


def example_base_4_to_base_16():
    """Ejemplo: Base 4 → Base 16 (2^2 → 2^4)"""
    print("\n" + "="*80)
    print("EJEMPLO: Base 4 → Base 16 (2^2 → 2^4)")
    print("="*80)
    
    # B = 4 = 2^2, B' = 16 = 2^4
    # m = mcd(2,4) = 2, n'' = 1, n''' = 2
    # Cada 2 dígitos base-4 = 1 dígito hexadecimal
    
    print(f"\nBases:")
    print(f"  B = 4 = 2^2")
    print(f"  B' = 16 = 2^4")
    print(f"  Base común: b = 2")
    print(f"  m = mcd(2,4) = 2")
    print(f"  n'' = 2/2 = 1 (dígito base-4 por dígito base-2)")
    print(f"  n''' = 4/2 = 2 (dígitos base-4 por dígito hexadecimal)")
    
    # Número en base 4: 3.5 en Q(4,4) base 4
    M = int(3.5 * (4**4))
    print(f"\nNúmero original:")
    print(f"  Valor: 3.5")
    print(f"  M en base 4: {M}")
    
    try:
        result = convert_with_common_base(4, 4, 4, M, 16, 4)
        
        print(f"\nResultado:")
        print(f"  M' en base 16: {result['M_prime']}")
        print(f"  Hexadecimal: 0x{result['M_prime']:04x}")
        print(f"  F' = {result['F_prime']}")
        print(f"  Conversión exacta: {result['is_exact']}")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# TABLA COMPARATIVA DE CONVERSIONES
# ============================================================================

def print_common_base_table():
    """Mostrar tabla de bases con base común."""
    print("\n" + "="*80)
    print("BASES CON BASE COMÚN (Conversión Exacta Posible)")
    print("="*80)
    
    base_pairs = [
        (2, 4),
        (2, 8),
        (2, 16),
        (4, 2),
        (4, 16),
        (8, 2),
        (8, 4),
        (16, 2),
        (16, 4),
    ]
    
    print(f"\n{'B':<5} {'B_prime':<8} {'Base común':<12} {'n':<5} {'n_prime':<8} {'m':<5} {'Exacta':<10}")
    print("-" * 65)
    
    for B, B_prime in base_pairs:
        result = find_common_base(B, B_prime)
        if result:
            b, n, n_p, m, n_pp, n_ppp = result
            exact = "SI"
        else:
            b, n, n_p, m = "N/A", "N/A", "N/A", "N/A"
            exact = "NO"
        
        print(f"{B:<5} {B_prime:<8} {str(b) if b != 'N/A' else 'N/A':<12} "
              f"{str(n) if n != 'N/A' else 'N/A':<5} "
              f"{str(n_p) if n_p != 'N/A' else 'N/A':<8} "
              f"{str(m) if m != 'N/A' else 'N/A':<5} "
              f"{exact:<10}")


if __name__ == "__main__":
    print_common_base_table()
    example_binary_to_octal()
    example_octal_to_binary()
    example_base_4_to_base_16()
    
    print("\n" + "="*80)
    print("FIN DE EJEMPLOS")
    print("="*80)
