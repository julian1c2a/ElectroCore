"""
Conversión entre Bases en Punto Fijo Q(E,F)

Este módulo implementa conversiones entre diferentes formatos de punto fijo,
respetando la regla fundamental: B'_F' >= B^F

Concepto clave:
    Para convertir un número de Q(E,F) base B a Q(E',F') base B':
    
    1. Obtener el valor en punto flotante: V = M × B^(-F)
    2. Determinar F' tal que B'^F' >= B^F (precisión no disminuya)
    3. Calcular M' = V × B'^F'
    
    La regla B'^F' >= B^F asegura que la precisión no se pierda en la
    conversión (aunque la representación sea diferente).
"""

from decimal import Decimal, getcontext
from typing import Tuple, Optional
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importes relativos
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.punto_fijo import FixedPoint

getcontext().prec = 100


class BaseConversionError(Exception):
    """Error en conversión entre bases."""
    pass


def log_base(value: Decimal, base: Decimal) -> Decimal:
    """Calcular log_base(value)."""
    if value <= 0 or base <= 0 or base == 1:
        raise ValueError(f"Parámetros inválidos: value={value}, base={base}")
    return (value.ln() / base.ln())


def find_min_F_prime(F: int, B: int, B_prime: int) -> int:
    """
    Encontrar F' mínimo tal que B'^F' >= B^F.
    
    Fórmula: F' = ceil(F × log_B'(B))
    
    Args:
        F: Bits fraccionarios del formato original
        B: Base original
        B_prime: Base destino
    
    Returns:
        F' mínimo que satisface la regla de precisión
    """
    F_decimal = Decimal(F)
    B_decimal = Decimal(B)
    B_prime_decimal = Decimal(B_prime)
    
    # F' = ceil(F × log_B'(B))
    exponent = F_decimal * log_base(B_decimal, B_prime_decimal)
    F_prime = int(exponent) + (1 if exponent % 1 != 0 else 0)
    
    return F_prime


def verify_precision_rule(F: int, B: int, F_prime: int, B_prime: int) -> bool:
    """
    Verificar que se cumple la regla: B'^F' >= B^F
    
    Returns:
        True si se cumple la regla, False en caso contrario
    """
    left_side = Decimal(B_prime) ** F_prime
    right_side = Decimal(B) ** F
    return left_side >= right_side


def convert_fixed_point_base(
    fp: FixedPoint,
    E_prime: int,
    B_prime: int,
    F_prime: Optional[int] = None
) -> Tuple[FixedPoint, dict]:
    """
    Convertir número Q(E,F)_B a Q(E',F')_B'
    
    Args:
        fp: Número en punto fijo original
        E_prime: Bits enteros del formato destino
        B_prime: Base destino
        F_prime: Bits fraccionarios destino (si None, se calcula automáticamente)
    
    Returns:
        Tupla (nuevo_FixedPoint, información_conversión)
    
    Raises:
        BaseConversionError: Si la conversión no es posible
    """
    
    # Si F' no se especifica, calcularlo automáticamente
    if F_prime is None:
        F_prime = find_min_F_prime(fp.F, fp.B, B_prime)
    
    # Verificar la regla de precisión
    if not verify_precision_rule(fp.F, fp.B, F_prime, B_prime):
        raise BaseConversionError(
            f"Regla de precisión violada: B'^F' < B^F "
            f"({B_prime}^{F_prime} < {fp.B}^{fp.F})"
        )
    
    # Obtener el valor exacto (en decimal de alta precisión)
    value = fp.value
    
    # Crear nuevo FixedPoint en formato destino
    try:
        fp_prime = FixedPoint(E_prime, F_prime, B_prime, value=float(value))
    except OverflowError as e:
        raise BaseConversionError(
            f"El valor {value} no cabe en Q({E_prime},{F_prime})_{B_prime}: {e}"
        )
    
    # Información de la conversión
    info = {
        'source_format': f"Q({fp.E},{fp.F})_{{{fp.B}}}",
        'dest_format': f"Q({E_prime},{F_prime})_{{{B_prime}}}",
        'source_value': float(fp.value),
        'dest_value': float(fp_prime.value),
        'precision_loss': float(abs(fp.value - fp_prime.value)),
        'source_raw': fp.raw_value,
        'dest_raw': fp_prime.raw_value,
        'rule_satisfied': f"{B_prime}^{F_prime} = {Decimal(B_prime)**F_prime} >= {Decimal(fp.B)**fp.F} = {fp.B}^{fp.F}",
    }
    
    return fp_prime, info


def convert_multiple_bases(
    fp: FixedPoint,
    E_prime: int,
    target_bases: list
) -> dict:
    """
    Convertir un número Q(E,F) a múltiples bases destino.
    
    Args:
        fp: Número en punto fijo original
        E_prime: Bits enteros para los formatos destino
        target_bases: Lista de bases destino
    
    Returns:
        Diccionario con conversiones para cada base
    """
    results = {}
    
    for B_prime in target_bases:
        try:
            F_prime = find_min_F_prime(fp.F, fp.B, B_prime)
            fp_prime, info = convert_fixed_point_base(fp, E_prime, B_prime, F_prime)
            results[B_prime] = {
                'success': True,
                'result': fp_prime,
                'info': info
            }
        except Exception as e:
            results[B_prime] = {
                'success': False,
                'error': str(e)
            }
    
    return results


# ============================================================================
# EJEMPLOS Y CASOS DE USO
# ============================================================================

if __name__ == "__main__":
    from decimal import Decimal
    
    print("=" * 80)
    print("CONVERSIÓN ENTRE BASES EN PUNTO FIJO")
    print("=" * 80)
    
    # Ejemplo 1: Base 2 a Base 10
    print("\n" + "=" * 80)
    print("Ejemplo 1: Q(8,8)_2 -> Q(8,F')_10")
    print("=" * 80)
    
    fp_binary = FixedPoint(8, 8, B=2, value=5.25)
    print(f"\nNúmero original: {fp_binary}")
    print(f"Formato: Q(8,8) base 2")
    print(f"Valor: {fp_binary.value}")
    
    # Calcular F' automáticamente
    F_prime = find_min_F_prime(8, 2, 10)
    print(f"\nCalcular F' tal que 10^F' >= 2^8:")
    print(f"  F' = ceil(8 × log_10(2)) = ceil(8 × {float(log_base(Decimal(2), Decimal(10))):.6f})")
    print(f"  F' = {F_prime}")
    print(f"  Verificación: 10^{F_prime} = {10**F_prime} >= {2**8} = 2^8 ✓")
    
    fp_decimal, info = convert_fixed_point_base(fp_binary, 8, 10, F_prime)
    print(f"\nResultado: Q(8,{F_prime}) base 10")
    print(f"Valor: {fp_decimal.value}")
    print(f"Pérdida de precisión: {info['precision_loss']}")
    
    
    # Ejemplo 2: Base 10 a Base 2
    print("\n" + "=" * 80)
    print("Ejemplo 2: Q(10,6)_10 -> Q(10,F')_2")
    print("=" * 80)
    
    fp_decimal = FixedPoint(10, 6, B=10, value=123.456789)
    print(f"\nNúmero original: {fp_decimal}")
    print(f"Formato: Q(10,6) base 10")
    print(f"Valor: {fp_decimal.value}")
    
    F_prime = find_min_F_prime(6, 10, 2)
    print(f"\nCalcular F' tal que 2^F' >= 10^6:")
    print(f"  F' = ceil(6 × log_2(10)) = ceil(6 × {float(log_base(Decimal(10), Decimal(2))):.6f})")
    print(f"  F' = {F_prime}")
    print(f"  Verificación: 2^{F_prime} = {2**F_prime} >= {10**6} = 10^6 ✓")
    
    fp_binary, info = convert_fixed_point_base(fp_decimal, 10, 2, F_prime)
    print(f"\nResultado: Q(10,{F_prime}) base 2")
    print(f"Valor: {fp_binary.value}")
    print(f"Pérdida de precisión: {info['precision_loss']}")
    
    
    # Ejemplo 3: Conversión a múltiples bases
    print("\n" + "=" * 80)
    print("Ejemplo 3: Conversión de Q(8,8)_2 a múltiples bases")
    print("=" * 80)
    
    fp = FixedPoint(8, 8, B=2, value=10.5)
    print(f"\nNúmero original: {fp}")
    print(f"Formato: Q(8,8) base 2")
    print(f"Valor: {fp.value}")
    
    results = convert_multiple_bases(fp, 8, [2, 8, 10, 16])
    
    print("\nConversiones:")
    for base, result in results.items():
        if result['success']:
            fp_converted = result['result']
            info = result['info']
            F_prime = find_min_F_prime(8, 2, base)
            print(f"\n  Base {base}:")
            print(f"    Formato destino: Q(8,{F_prime})_{{{base}}}")
            print(f"    Valor: {fp_converted.value}")
            print(f"    Pérdida: {info['precision_loss']}")
        else:
            print(f"\n  Base {base}: ERROR - {result['error']}")
    
    
    # Ejemplo 4: Demostrar la regla de precisión
    print("\n" + "=" * 80)
    print("Ejemplo 4: Demostración de la Regla B'^F' >= B^F")
    print("=" * 80)
    
    examples = [
        (8, 2, 10),
        (6, 10, 2),
        (4, 16, 2),
        (10, 2, 8),
    ]
    
    print("\nFormato Original | Formato Destino | Regla B'^F' >= B^F")
    print("-" * 80)
    
    for F, B, B_prime in examples:
        F_prime = find_min_F_prime(F, B, B_prime)
        left = Decimal(B_prime) ** F_prime
        right = Decimal(B) ** F
        satisfied = left >= right
        
        print(f"Q(E,{F:2})_{{{B:2}}}      | Q(E,{F_prime:2})_{{{B_prime:2}}}       | "
              f"{B_prime}^{F_prime} = {left} >= {right} = {B}^{F} {'✓' if satisfied else '✗'}")
    
    
    print("\n" + "=" * 80)
