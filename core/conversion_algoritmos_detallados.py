"""
Algoritmos de Conversión entre Bases en Punto Fijo Q(E,F)

Este módulo implementa los dos enfoques para convertir números Q(E,F):

1. MÉTODO DE DESCOMPOSICIÓN:
   - Parte entera: divisiones sucesivas
   - Parte fraccionaria: multiplicaciones sucesivas
   - Combinar los resultados

2. MÉTODO HÍBRIDO (entero + desplazamiento):
   - Interpretar todo como entero: valor_entero = M × B^F
   - Convertir el valor entero a base B'
   - Interpretar resultado como Q(E',F') con desplazamiento

Ambos métodos respetan la regla: B'^F' >= B^F
"""

from decimal import Decimal, getcontext
from typing import Tuple, List, Dict
import math

getcontext().prec = 100


# ============================================================================
# MÉTODO 1: CONVERSIÓN POR DESCOMPOSICIÓN
# ============================================================================

def convert_integer_part(
    value_int: int,
    from_base: int,
    to_base: int
) -> Tuple[List[int], int]:
    """
    Convertir la parte entera usando divisiones sucesivas.
    
    Algoritmo clásico:
        while value_int > 0:
            dígito = value_int mod to_base
            value_int = value_int // to_base
            
    Args:
        value_int: Parte entera como entero natural
        from_base: Base origen (ignorado en este algoritmo)
        to_base: Base destino
        
    Returns:
        (dígitos en orden inverso, número de dígitos)
    
    Ejemplo:
        convert_integer_part(42, 10, 2)
        42 = 32 + 8 + 2 = 101010₂
        Pasos:
            42 mod 2 = 0, 42 // 2 = 21
            21 mod 2 = 1, 21 // 2 = 10
            10 mod 2 = 0, 10 // 2 = 5
            5 mod 2 = 1, 5 // 2 = 2
            2 mod 2 = 0, 2 // 2 = 1
            1 mod 2 = 1, 1 // 2 = 0
        Resultado: [0,1,0,1,0,1] → 101010₂ (invertido)
    """
    if value_int == 0:
        return [0], 1
    
    digits = []
    steps = []
    
    original = value_int
    while value_int > 0:
        remainder = value_int % to_base
        quotient = value_int // to_base
        steps.append((value_int, remainder, quotient))
        digits.append(remainder)
        value_int = quotient
    
    return digits[::-1], len(digits)


def convert_fractional_part(
    fraction: Decimal,
    from_base: int,
    to_base: int,
    num_digits: int
) -> Tuple[List[int], List[Decimal], List[Decimal]]:
    """
    Convertir la parte fraccionaria usando multiplicaciones sucesivas.
    
    Algoritmo:
        while información_pendiente > 0 and dígitos < num_digits:
            fracción = fracción × to_base
            dígito = floor(fracción)
            fracción = fracción - floor(fracción)
            
    Args:
        fraction: Parte fraccionaria como Decimal en (0,1)
        from_base: Base origen
        to_base: Base destino
        num_digits: Número máximo de dígitos a generar
        
    Returns:
        (dígitos, fracciones_parciales, información_transportada)
    
    Ejemplo:
        convert_fractional_part(0.625, 10, 2, 8)
        0.625 en binario:
            0.625 × 2 = 1.25 → dígito=1, fracción=0.25
            0.25 × 2 = 0.5 → dígito=0, fracción=0.5
            0.5 × 2 = 1.0 → dígito=1, fracción=0.0
        Resultado: [1,0,1] → .101₂ exacto
    """
    if fraction == 0:
        return [0] * num_digits, [fraction] * num_digits, []
    
    digits = []
    fractions = [fraction]
    steps = []
    
    current = fraction
    
    for i in range(num_digits):
        if current == 0:
            # Fracción terminante
            digits.extend([0] * (num_digits - len(digits)))
            break
        
        # Multiplicar por base destino
        product = current * Decimal(to_base)
        digit = int(product)
        remainder = product - Decimal(digit)
        
        digits.append(digit)
        steps.append({
            'iteration': i + 1,
            'fraction': current,
            'product': product,
            'digit': digit,
            'remainder': remainder
        })
        fractions.append(remainder)
        current = remainder
    
    return digits, fractions, steps


def decomposition_conversion(
    E: int,
    F: int,
    from_base: int,
    M: int,  # Valor crudo del registro
    to_base: int,
    E_prime: int,
    F_prime: int
) -> Dict:
    """
    Conversión por descomposición: separar parte entera y fraccionaria.
    
    Entrada:
        Número Q(E,F) con valor crudo M en base from_base
        Valor = M × from_base^(-F)
        
    Proceso:
        1. Extraer parte entera: int_part = M // from_base^F
        2. Extraer parte fraccionaria: frac_part = (M % from_base^F) / from_base^F
        3. Convertir parte entera usando divisiones
        4. Convertir parte fraccionaria usando multiplicaciones
        5. Ensamblar en base to_base
        
    Salida:
        Número Q(E',F') con valor crudo M' en base to_base
    """
    
    # Paso 1: Extraer partes
    base_power_F = from_base ** F
    int_part = M // base_power_F
    frac_numerator = M % base_power_F
    frac_part = Decimal(frac_numerator) / Decimal(base_power_F)
    
    # Paso 2: Convertir parte entera (divisiones)
    int_digits_origin, num_int_digits = convert_integer_part(int_part, from_base, to_base)
    
    # Paso 3: Convertir parte fraccionaria (multiplicaciones)
    frac_digits, frac_steps, _ = convert_fractional_part(frac_part, from_base, to_base, F_prime)
    
    # Paso 4: Ensamblar M' en base destino
    # M' = sum(d_i × to_base^i) para i desde 0 a E'+F'-1
    M_prime = 0
    for i, digit in enumerate(int_digits_origin):
        position = len(int_digits_origin) - 1 - i
        M_prime += digit * (to_base ** position)
    
    for i, digit in enumerate(frac_digits):
        position = -(i + 1)
        M_prime += digit * (to_base ** position)
    
    # Paso 5: Convertir M' a entero
    # Los dígitos fraccionarios representan posiciones 2^(-1), 2^(-2), etc.
    # Convertir a entero para almacenar en registro
    M_prime_int = 0
    for i, digit in enumerate(frac_digits):
        M_prime_int += digit * (to_base ** (F_prime - 1 - i))
    
    # Agregar parte entera
    for i, digit in enumerate(int_digits_origin):
        position = E_prime + F_prime - 1 - i
        if position >= F_prime:  # Solo si está dentro de la parte entera
            M_prime_int += digit * (to_base ** position)
    
    return {
        'method': 'descomposicion',
        'int_part_original': int_part,
        'frac_part_original': float(frac_part),
        'int_digits': int_digits_origin,
        'frac_digits': frac_digits,
        'M_prime': M_prime_int,
        'frac_steps': frac_steps,
    }


# ============================================================================
# MÉTODO 2: CONVERSIÓN HÍBRIDA (Entero + Desplazamiento)
# ============================================================================

def hybrid_conversion(
    E: int,
    F: int,
    from_base: int,
    M: int,  # Valor crudo
    to_base: int,
    E_prime: int,
    F_prime: int
) -> Dict:
    """
    Conversión híbrida: interpretar como entero + desplazamiento.
    
    Estrategia:
        1. Interpretar M como entero puro (sin fracción)
        2. Convertir M a base destino usando divisiones
        3. El resultado se interpreta en Q(E',F') con desplazamiento
        
    Ejemplo:
        Q(4,4) base 2: valor=5.25, M=84, binario=0101 0100
        Interpretar como entero: 84₁₀ = 1010100₂
        Convertir a base 8: 84₁₀ = 124₈
        Interpretar como Q(4,3) base 8: valor = 124₈ × 8^(-3)
        
    Esta es la interpretación más pura del registro de bits.
    """
    
    # Paso 1: Convertir M como entero puro
    int_result = []
    temp = M
    
    if temp == 0:
        int_result = [0]
    else:
        while temp > 0:
            int_result.append(temp % to_base)
            temp //= to_base
        int_result = int_result[::-1]
    
    # Paso 2: Reconstruir M' como entero en base destino
    M_prime = 0
    for i, digit in enumerate(int_result):
        position = len(int_result) - 1 - i
        M_prime += digit * (to_base ** position)
    
    # Paso 3: Calcular valor en nuevo formato
    # El valor se calcula como: M_prime × to_base^(-F_prime)
    value_new = Decimal(M_prime) * (Decimal(to_base) ** (-F_prime))
    
    return {
        'method': 'hibrido',
        'M_original': M,
        'digits': int_result,
        'M_prime': M_prime,
        'value_new': float(value_new),
    }


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def digits_to_string(digits: List[int], base: int) -> str:
    """Convertir lista de dígitos a string."""
    if base <= 10:
        return ''.join(str(d) for d in digits)
    else:
        # Para bases > 10, usar A=10, B=11, etc.
        hex_chars = '0123456789ABCDEF'
        return ''.join(hex_chars[d] if d < 16 else str(d) for d in digits)


def integer_to_digits(value: int, base: int) -> List[int]:
    """Convertir entero a lista de dígitos en cualquier base."""
    if value == 0:
        return [0]
    
    digits = []
    while value > 0:
        digits.append(value % base)
        value //= base
    return digits[::-1]


def digits_to_integer(digits: List[int], base: int) -> int:
    """Convertir lista de dígitos a entero."""
    result = 0
    for d in digits:
        result = result * base + d
    return result


# ============================================================================
# INFORMACIÓN Y ANÁLISIS
# ============================================================================

def print_conversion_steps(
    E: int, F: int, from_base: int, M: int,
    to_base: int, E_prime: int, F_prime: int
):
    """Mostrar pasos detallados de conversión."""
    
    print(f"\n{'='*80}")
    print(f"CONVERSIÓN DETALLADA: Q({E},{F})_{{{from_base}}} → Q({E_prime},{F_prime})_{{{to_base}}}")
    print(f"{'='*80}\n")
    
    # Valor original
    value_original = M * (from_base ** (-F))
    print(f"ENTRADA:")
    print(f"  Formato original: Q({E},{F}) base {from_base}")
    print(f"  Valor crudo M: {M}")
    print(f"  Valor decimal: {value_original}")
    
    # Extraer partes
    base_power_F = from_base ** F
    int_part = M // base_power_F
    frac_numerator = M % base_power_F
    frac_part = Decimal(frac_numerator) / Decimal(base_power_F)
    
    print(f"\nPASO 1: EXTRAER PARTES")
    print(f"  Parte entera: {M} // {from_base}^{F} = {M} // {base_power_F} = {int_part}")
    print(f"  Parte fraccionaria: ({M} % {base_power_F}) / {base_power_F} = {frac_numerator} / {base_power_F} = {frac_part}")
    
    # Convertir parte entera
    print(f"\nPASO 2: CONVERTIR PARTE ENTERA (divisiones sucesivas)")
    print(f"  {int_part}₁₀ → ?₍{to_base}₎")
    
    temp = int_part
    divisions = []
    while temp > 0:
        rem = temp % to_base
        quot = temp // to_base
        divisions.append((temp, rem, quot))
        temp = quot
    
    for val, rem, quot in divisions:
        print(f"    {val} ÷ {to_base} = {quot} residuo {rem}")
    
    int_digits = [d[1] for d in divisions[::-1]]
    print(f"  Resultado (invertido): {digits_to_string(int_digits, to_base)}")
    
    # Convertir parte fraccionaria
    print(f"\nPASO 3: CONVERTIR PARTE FRACCIONARIA (multiplicaciones sucesivas)")
    print(f"  {float(frac_part)} → ?₍{to_base}₎")
    
    current = frac_part
    frac_digits = []
    for i in range(F_prime):
        product = current * Decimal(to_base)
        digit = int(product)
        remainder = product - Decimal(digit)
        frac_digits.append(digit)
        print(f"    {float(current):.10f} × {to_base} = {float(product):.10f} → dígito={digit}, residuo={float(remainder):.10f}")
        current = remainder
        if current == 0:
            print(f"    (fracción terminante)")
            break
    
    print(f"  Resultado: {digits_to_string(frac_digits, to_base)}")
    
    # Ensamblar
    print(f"\nPASO 4: ENSAMBLAR EN Q({E_prime},{F_prime})_{{{to_base}}}")
    print(f"  Tenemos:")
    print(f"    - {len(int_digits)} dígitos de parte entera: {digits_to_string(int_digits, to_base)}")
    print(f"    - {len(frac_digits)} dígitos de parte fraccionaria: {digits_to_string(frac_digits, to_base)}")
    print(f"    - Capacidad: E'={E_prime} posiciones enteras + F'={F_prime} posiciones fraccionarias")
    
    # Reconstruir M'
    # Los dígitos enteros ocupan las posiciones altas: desde len(int_digits)-1 hasta F_prime
    # Los dígitos fraccionarios ocupan las posiciones bajas: desde F_prime-1 hasta 0
    M_prime = 0
    
    # Parte entera: los dígitos van en orden de mayor a menor significancia
    # Posición más alta para el primer dígito (más significativo)
    for i, digit in enumerate(int_digits):
        # Primer dígito → posición = F_prime + len(int_digits) - 1
        # Último dígito → posición = F_prime
        position = F_prime + len(int_digits) - 1 - i
        contribution = digit * (to_base ** position)
        M_prime += contribution
        print(f"  Dígito entero[{i}]={digit} en posición {position}: {digit} × {to_base}^{position} = {contribution}")
    
    # Parte fraccionaria: los dígitos van en orden de mayor a menor significancia
    # Primer dígito → posición = F_prime - 1
    # Último dígito → posición = F_prime - len(frac_digits)
    for i, digit in enumerate(frac_digits):
        position = F_prime - 1 - i
        contribution = digit * (to_base ** position)
        M_prime += contribution
        print(f"  Dígito frac[{i}]={digit} en posición {position}: {digit} × {to_base}^{position} = {contribution}")
    
    print(f"\n  M' = {M_prime}")
    
    # Valor resultante
    value_result = Decimal(M_prime) * (Decimal(to_base) ** (-F_prime))
    print(f"\nSALIDA:")
    print(f"  Formato destino: Q({E_prime},{F_prime}) base {to_base}")
    print(f"  Valor crudo M': {M_prime}")
    print(f"  Valor decimal: {float(value_result)}")
    print(f"  Pérdida: {abs(Decimal(str(value_original)) - value_result)}")


if __name__ == "__main__":
    # Demostración con ejemplos
    
    # Ejemplo 1: Q(4,4) base 2 → Q(4,2) base 10
    print("\n" + "="*80)
    print("EJEMPLO 1: Q(4,4) base 2 → Q(4,2) base 10")
    print("="*80)
    M_origin = int(5.25 * (2**4))  # 5.25 en Q(4,4) base 2
    print_conversion_steps(4, 4, 2, M_origin, 10, 4, 2)
    
    # Ejemplo 2: Q(8,8) base 2 → Q(8,3) base 10
    print("\n" + "="*80)
    print("EJEMPLO 2: Q(8,8) base 2 → Q(8,3) base 10")
    print("="*80)
    M_origin = int(42.5625 * (2**8))
    print_conversion_steps(8, 8, 2, M_origin, 10, 8, 3)
