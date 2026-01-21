"""
Cálculo de F' en Conversión entre Bases - Demostración Detallada

Este script demuestra cómo calcular F' de forma exacta en dos casos:

1. CASO GENERAL: Bases sin base común
   F' = ceil(F × log_{B'}(B))
   
2. CASO ESPECIAL: Bases con base común
   Si B = b^n y B' = b^n':
   F' = ceil(F × n' / n)
   
La fórmula se basa en la conservación de información:
   Información en base B: B^F
   Información en base B': B'^F'
   Para no perder información: B'^F' >= B^F
"""

from decimal import Decimal, getcontext
from math import log, ceil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.conversion_base_comun import find_common_base, log_base

getcontext().prec = 100


def explain_F_prime_calculation():
    """Explicar detalladamente el cálculo de F'."""
    
    print("\n" + "="*80)
    print("CÁLCULO DE F' EN CONVERSIÓN ENTRE BASES")
    print("="*80)
    
    print("""
PRINCIPIO FUNDAMENTAL:
    
    Cuando convertimos de Q(E,F) base B a Q(E',F') base B',
    necesitamos que la precisión NO disminuya:
    
    B^F <= B'^F'
    
    Donde:
    - B^F: cantidad de información fraccionaria en base B
    - B'^F': cantidad de información fraccionaria en base B'
    
DEMOSTRACIÓN:
    
    En base B: F dígitos fraccionarios representan (0, B^(-F)]
    Cada número diferente se diferencia por B^(-F) (epsilon)
    Total de representaciones: B^F
    
    En base B': F' dígitos fraccionarios representan (0, B'^(-F')]
    Cada número diferente se diferencia por B'^(-F') (epsilon)
    Total de representaciones: B'^F'
    
    Para que no haya pérdida: B'^F' >= B^F
    
    Tomando logaritmo base B':
        F' >= F × log_{B'}(B)
    
    Como F' debe ser entero:
        F' = ceil(F × log_{B'}(B))
""")


def example_2_to_10():
    """Ejemplo: Base 2 a Base 10."""
    print("\n" + "="*80)
    print("EJEMPLO 1: Base 2 to Base 10")
    print("="*80)
    
    B = 2
    F = 8
    B_prime = 10
    
    print(f"""
Datos:
    B = {B} (origen)
    F = {F} (fraccionarios en origen)
    B' = {B_prime} (destino)
    
Calculo de F':
    
    1. Formula: F' = ceil(F x log_B'(B))
    
    2. Sustituir:
       F' = ceil({F} x log_{B_prime}({B}))
       
    3. Calcular log_B'(B):
       log_B'(B) = ln(B) / ln(B')
                 = ln({B}) / ln({B_prime})
""")
    
    log_value = log(B) / log(B_prime)
    print(f"       log_10(2) = {log_value:.10f}")
    
    product = F * log_value
    F_prime = ceil(product)
    
    print(f"""
    4. Multiplicar:
       {F} x {log_value:.10f} = {product:.10f}
       
    5. Redondear hacia arriba:
       ceil({product:.10f}) = {F_prime}
       
Verificacion:
    B^F = {B}^{F} = {B**F}
    B'^F' = {B_prime}^{F_prime} = {B_prime**F_prime}
    {B_prime**F_prime} >= {B**F}: {B_prime**F_prime >= B**F} OK
    
Resultado: F' = {F_prime}
""")


def example_10_to_2():
    """Ejemplo: Base 10 a Base 2."""
    print("\n" + "="*80)
    print("EJEMPLO 2: Base 10 to Base 2")
    print("="*80)
    
    B = 10
    F = 6
    B_prime = 2
    
    print(f"""
Datos:
    B = {B} (origen)
    F = {F} (fraccionarios en origen)
    B' = {B_prime} (destino)
    
Cálculo de F':
    F' = ceil({F} × log_2({B}))
""")
    
    log_value = log(B) / log(B_prime)
    print(f"    log_2(10) = {log_value:.10f}")
    
    product = F * log_value
    F_prime = ceil(product)
    
    print(f"""
    {F} x {log_value:.10f} = {product:.10f}
    ceil({product:.10f}) = {F_prime}
    
Verificacion:
    10^6 = {B**F}
    2^{F_prime} = {B_prime**F_prime}
    {B_prime**F_prime} >= {B**F}: {B_prime**F_prime >= B**F} OK
    
Resultado: F' = {F_prime}
""")


def example_common_base_2_8():
    """Ejemplo: Base 2 a Base 8 (base común = 2)."""
    print("\n" + "="*80)
    print("EJEMPLO 3: Base 2 to Base 8 (Base Comun)")
    print("="*80)
    
    B = 2
    B_prime = 8
    F = 8
    
    result = find_common_base(B, B_prime)
    if result:
        b, n, n_prime, m, n_pp, n_ppp = result
        
        print(f"""
Bases con base comun:
    B = {B} = {b}^{n}
    B' = {B_prime} = {b}^{n_prime}
    
Parametros:
    Base comun: b = {b}
    n = {n}, n' = {n_prime}
    m = mcd({n}, {n_prime}) = {m}
    n'' = {n} / {m} = {n_pp}
    n''' = {n_prime} / {m} = {n_ppp}
    
En este caso, la conversion es EXACTA:
    
    Informacion original: {B}^{F} = {B**F} valores diferentes
    Informacion destino: {B_prime}^F' = {B_prime}^? 
    
    Como F' = ceil(F x n' / n) = ceil({F} x {n_prime} / {n})
               = ceil({F * n_prime / n})
               = {ceil(F * n_prime / n)}
    
    Verificacion:
    {B_prime}^{ceil(F * n_prime / n)} = {B_prime**ceil(F * n_prime / n)} >= {B**F} OK
    
Resultado: F' = {ceil(F * n_prime / n)} (exacto, sin perdida)

Explicacion:
    - 1 digito en base {B_prime} = {n_prime} digitos en base {b}
    - 1 digito en base {B} = {n_pp} digitos en base {b}
    - Agrupar {n_ppp} bits binarios = 1 digito octal
""")


def example_common_base_16_2():
    """Ejemplo: Base 16 a Base 2 (base común = 2)."""
    print("\n" + "="*80)
    print("EJEMPLO 4: Base 16 to Base 2 (Base Comun)")
    print("="*80)
    
    B = 16
    B_prime = 2
    F = 4
    
    result = find_common_base(B, B_prime)
    if result:
        b, n, n_prime, m, n_pp, n_ppp = result
        
        print(f"""
Bases con base comun:
    B = {B} = {b}^{n}
    B' = {B_prime} = {b}^{n_prime}
    
Parametros:
    Base comun: b = {b}
    n = {n}, n' = {n_prime}
    m = mcd({n}, {n_prime}) = {m}
    n'' = {n} / {m} = {n_pp}
    n''' = {n_prime} / {m} = {n_ppp}
    
Conversion exacta con F' = {ceil(F * n_prime / n)}:
    
    1 digito hexadecimal = {n} bits
    Expandir cada digito en {n} bits individuales
    
    Cada {n_pp} bits hexadecimales = {n_ppp} digitos binarios
    (En este caso 1:1, cada digito = 4 bits)
""")


def example_base_8_4():
    """Ejemplo: Base 8 a Base 4."""
    print("\n" + "="*80)
    print("EJEMPLO 5: Base 8 to Base 4")
    print("="*80)
    
    B = 8
    B_prime = 4
    F = 6
    
    # Base 8 = 2^3, Base 4 = 2^2, base común = 2
    result = find_common_base(B, B_prime)
    if result:
        b, n, n_prime, m, n_pp, n_ppp = result
        
        print(f"""
Caso especial: Base comun = 2
    
    B = {B} = 2^{n}
    B' = {B_prime} = 2^{n_prime}
    
    F' exacta = ceil({F} x {n_prime} / {n})
              = ceil({F * n_prime / n})
              = {ceil(F * n_prime / n)}
    
Conversion exacta sin perdida de informacion.
""")


def table_F_prime_values():
    """Mostrar tabla de F' para conversiones comunes."""
    print("\n" + "="*80)
    print("TABLA: F' PARA CONVERSIONES COMUNES")
    print("="*80)
    
    conversions = [
        (2, 8, 4),
        (2, 8, 8),
        (2, 10, 8),
        (2, 10, 10),
        (2, 16, 4),
        (8, 2, 4),
        (8, 10, 6),
        (10, 2, 6),
        (10, 8, 4),
        (16, 2, 4),
    ]
    
    print(f"\n{'B->B_prime':<15} {'F':<5} {'F_prime':<10} {'Exacta':<10} {'Info Original':<20} {'Info Nueva':<20}")
    print("-" * 85)
    
    for B, B_prime, F in conversions:
        # Calcular F'
        log_val = log(B) / log(B_prime)
        F_prime = ceil(F * log_val)
        
        # Verificar si es exacta
        is_exact = False
        result = find_common_base(B, B_prime)
        if result:
            b, n, n_p, m, n_pp, n_ppp = result
            F_prime_exact = ceil(F * n_p / n)
            is_exact = True
        
        info_orig = B ** F
        info_new = B_prime ** F_prime
        
        print(f"{B}->{B_prime:<13} {F:<5} {F_prime:<10} {'Si' if is_exact else 'No':<10} "
              f"{info_orig:<20} {info_new:<20}")


if __name__ == "__main__":
    explain_F_prime_calculation()
    example_2_to_10()
    example_10_to_2()
    example_common_base_2_8()
    example_common_base_16_2()
    example_base_8_4()
    table_F_prime_values()
    
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    print("""
FORMULAS CLAVE:

1. Caso general (sin base comun):
   F' = ceil(F x log_B'(B))
   
2. Caso especial (con base comun):
   Si B = b^n y B' = b^n', entonces:
   F' = ceil(F x n' / n)
   
   Esta segunda es mas eficiente computacionalmente y da
   conversiones exactas sin perdida de informacion.

REGLA FUNDAMENTAL:
   B'^F' >= B^F
   
   Esto asegura que no hay perdida de precision al convertir.
""")
