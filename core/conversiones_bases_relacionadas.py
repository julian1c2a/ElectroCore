"""
Conversión entre Bases Relacionadas (Potencias de la misma base)

Cuando tenemos un número en base B^l y queremos pasarlo a base B^k,
podemos usar un algoritmo optimizado basado en que ambas son potencias
de la misma base B.

Ejemplos:
- 2, 4, 8, 16, 32 (potencias de 2)
- 3, 9, 27 (potencias de 3)
- 5, 25 (potencias de 5)
- 6, 36 (potencias de 6)

El algoritmo:
1. Encontrar m = gcd(l, k) donde l = log_B(base_origen), k = log_B(base_destino)
2. Descomponer: l = l' × m, k = k' × m
3. Convertir de base B^l a base B^m (agrupamos cada l' dígitos de B)
4. Reagrupar de k' en k' los dígitos de B^m
5. Convertir cada grupo de k' a un dígito de B^k
"""

from math import gcd
from typing import List, Dict, Tuple, Union
from core.numeracion_utils import (
    valor_digito_en_base,
    validar_numero_en_base
)


def encontrar_base_primitiva(base1: int, base2: int) -> Tuple[int, int, int]:
    """
    Encuentra la base primitiva B y los exponentes l, k tales que:
    - base1 = B^l
    - base2 = B^k
    
    Retorna: (B, l, k) o None si no son potencias de la misma base
    """
    # Detectar patrones comunes
    # Formato: (base1, base2, B_primitiva, l, k)
    pares_potencias = [
        (2, 4, 2, 1, 2),    # 2=2^1, 4=2^2
        (2, 8, 2, 1, 3),    # 2=2^1, 8=2^3
        (2, 16, 2, 1, 4),   # 2=2^1, 16=2^4
        (2, 32, 2, 1, 5),   # 2=2^1, 32=2^5
        (4, 2, 2, 2, 1),    # 4=2^2, 2=2^1
        (4, 8, 2, 2, 3),    # 4=2^2, 8=2^3
        (4, 16, 2, 2, 4),   # 4=2^2, 16=2^4
        (8, 2, 2, 3, 1),    # 8=2^3, 2=2^1
        (8, 4, 2, 3, 2),    # 8=2^3, 4=2^2
        (8, 16, 2, 3, 4),   # 8=2^3, 16=2^4
        (16, 2, 2, 4, 1),   # 16=2^4, 2=2^1
        (16, 4, 2, 4, 2),   # 16=2^4, 4=2^2
        (16, 8, 2, 4, 3),   # 16=2^4, 8=2^3
        (32, 2, 2, 5, 1),   # 32=2^5, 2=2^1
        (3, 9, 3, 1, 2),    # 3=3^1, 9=3^2
        (3, 27, 3, 1, 3),   # 3=3^1, 27=3^3
        (9, 3, 3, 2, 1),    # 9=3^2, 3=3^1
        (9, 27, 3, 2, 3),   # 9=3^2, 27=3^3
        (27, 3, 3, 3, 1),   # 27=3^3, 3=3^1
        (27, 9, 3, 3, 2),   # 27=3^3, 9=3^2
        (5, 25, 5, 1, 2),   # 5=5^1, 25=5^2
        (25, 5, 5, 2, 1),   # 25=5^2, 5=5^1
        (6, 36, 6, 1, 2),   # 6=6^1, 36=6^2
        (36, 6, 6, 2, 1),   # 36=6^2, 6=6^1
    ]
    
    for b1, b2, B, l, k in pares_potencias:
        if base1 == b1 and base2 == b2:
            return B, l, k
    
    return None


def validar_conversion_bases_relacionadas(base1: int, base2: int) -> Tuple[bool, str]:
    """
    Valida si es posible hacer conversión optimizada entre dos bases.
    
    Retorna: (es_posible, mensaje)
    """
    if base1 < 2 or base2 < 2:
        return False, f"Bases deben ser >= 2"
    
    resultado = encontrar_base_primitiva(base1, base2)
    if resultado is None:
        return False, f"Las bases {base1} y {base2} no son potencias de la misma base"
    
    return True, "Conversión optimizada disponible"


def dígito_base_b_a_dígitos_base_potencia(
    dígito: str,
    base_origen: int,
    base_destino: int
) -> List[str]:
    """
    Convierte un dígito en base_origen a dígitos en base_destino.
    
    Ejemplo: dígito 'F' en base 16 → dígitos en base 2: ['1','1','1','1']
    """
    # Obtener el valor del dígito
    valor = valor_digito_en_base(dígito, base_origen)
    
    # Convertir a base destino (lista de dígitos)
    if valor == 0:
        return ['0']
    
    dígitos = []
    while valor > 0:
        dígitos.append(str(valor % base_destino))
        valor //= base_destino
    
    # Invertir para obtener el orden correcto
    return dígitos[::-1]


def dígitos_base_b_a_dígito_base_potencia(
    dígitos: List[str],
    base_origen: int,
    base_destino: int
) -> str:
    """
    Convierte una lista de dígitos en base_origen a un dígito en base_destino.
    
    Ejemplo: ['1','1','1','1'] en base 2 → dígito 'F' en base 16
    """
    # Convertir lista de dígitos a valor decimal
    valor = 0
    for d in dígitos:
        valor = valor * base_origen + valor_digito_en_base(d, base_origen)
    
    # Convertir a dígito en base destino
    if valor < base_destino:
        if valor < 10:
            return str(valor)
        else:
            return chr(ord('A') + valor - 10)
    else:
        raise ValueError(f"Valor {valor} no cabe en un dígito de base {base_destino}")


def convertir_bases_relacionadas(
    numero_str: str,
    base_origen: int,
    base_destino: int,
    verbose: bool = False
) -> Dict:
    """
    Convierte un número de base_origen a base_destino cuando ambas
    son potencias de la misma base.
    
    Parámetros:
    - numero_str: Número como string en base_origen
    - base_origen: Base origen (ej: 2, 4, 8, 16, 32)
    - base_destino: Base destino (ej: 2, 4, 8, 16, 32)
    - verbose: Si True, incluye pasos intermedios
    
    Retorna: Dict con:
    - numero_original: número original
    - base_origen, base_destino
    - base_primitiva: B tal que base_origen = B^l, base_destino = B^k
    - exponentes: (l, k)
    - m: gcd(l, k)
    - resultado: número en base_destino
    - pasos: Lista de pasos intermedios (si verbose=True)
    """
    
    # Validar entrada
    valido, msg = validar_conversion_bases_relacionadas(base_origen, base_destino)
    if not valido:
        raise ValueError(msg)
    
    valido, msg = validar_numero_en_base(numero_str, base_origen)
    if not valido:
        raise ValueError(msg)
    
    # Obtener información de bases relacionadas
    B, l, k = encontrar_base_primitiva(base_origen, base_destino)
    m = gcd(l, k)
    l_prima = l // m
    k_prima = k // m
    
    pasos = [] if verbose else None
    
    if verbose:
        pasos.append({
            'paso': 'inicializacion',
            'descripcion': f'base_origen={base_origen}=B^l={B}^{l}, base_destino={base_destino}=B^k={B}^{k}',
            'gcd': m,
            'l_prima': l_prima,
            'k_prima': k_prima
        })
    
    # PASO 1: Convertir cada dígito de base_origen a l_prima dígitos de B
    dígitos_en_B = []
    for dígito in numero_str:
        grupo = dígito_base_b_a_dígitos_base_potencia(dígito, base_origen, B)
        # Rellenar a l_prima dígitos
        while len(grupo) < l_prima:
            grupo.insert(0, '0')
        dígitos_en_B.extend(grupo)
    
    if verbose:
        pasos.append({
            'paso': 1,
            'descripcion': f'Convertir cada dígito a {l_prima} dígitos en base {B}',
            'dígitos_originales': numero_str,
            'dígitos_en_B': ''.join(dígitos_en_B)
        })
    
    # PASO 2: Agrupar de k_prima en k_prima (empezando por la derecha)
    # Rellenar con ceros a la izquierda si es necesario
    while len(dígitos_en_B) % k_prima != 0:
        dígitos_en_B.insert(0, '0')
    
    grupos = []
    for i in range(0, len(dígitos_en_B), k_prima):
        grupos.append(dígitos_en_B[i:i+k_prima])
    
    if verbose:
        pasos.append({
            'paso': 2,
            'descripcion': f'Agrupar de {k_prima} en {k_prima} dígitos',
            'dígitos_en_B': ''.join(dígitos_en_B),
            'grupos': grupos
        })
    
    # PASO 3: Convertir cada grupo a un dígito en base_destino
    resultado_dígitos = []
    for grupo in grupos:
        dígito_destino = dígitos_base_b_a_dígito_base_potencia(grupo, B, base_destino)
        resultado_dígitos.append(dígito_destino)
        
        if verbose:
            valor_grupo = sum(
                valor_digito_en_base(d, B) * (B ** (len(grupo) - 1 - i))
                for i, d in enumerate(grupo)
            )
            pasos.append({
                'paso': 3,
                'grupo': ''.join(grupo),
                'valor_en_B': valor_grupo,
                'dígito_destino': dígito_destino
            })
    
    resultado = ''.join(resultado_dígitos)
    
    return {
        'numero_original': numero_str,
        'base_origen': base_origen,
        'base_destino': base_destino,
        'base_primitiva': B,
        'exponentes': (l, k),
        'gcd_exponentes': m,
        'l_prima': l_prima,
        'k_prima': k_prima,
        'resultado': resultado,
        'pasos': pasos if verbose else None
    }


def convertir_bases_relacionadas_tabla(
    numero_str: str,
    base_origen: int,
    base_destino: int
) -> Dict:
    """
    Conversión con tabla detallada paso a paso.
    """
    return convertir_bases_relacionadas(numero_str, base_origen, base_destino, verbose=True)


def comparar_conversiones_bases_relacionadas(
    numero_str: str,
    base_origen: int,
    base_destino: int
) -> Dict:
    """
    Compara la conversión optimizada con el método tradicional.
    """
    # Método optimizado
    optimizado = convertir_bases_relacionadas(numero_str, base_origen, base_destino)
    
    # Método tradicional (Base A → Base 10 → Base B)
    # Primero: Base A → Base 10
    valor_decimal = 0
    for d in numero_str:
        valor_decimal = valor_decimal * base_origen + valor_digito_en_base(d, base_origen)
    
    # Segundo: Base 10 → Base B
    resultado_decimal = []
    if valor_decimal == 0:
        resultado_decimal = ['0']
    else:
        while valor_decimal > 0:
            dígito = valor_decimal % base_destino
            if dígito < 10:
                resultado_decimal.append(str(dígito))
            else:
                resultado_decimal.append(chr(ord('A') + dígito - 10))
            valor_decimal //= base_destino
        resultado_decimal = resultado_decimal[::-1]
    
    resultado_tradicional = ''.join(resultado_decimal)
    
    return {
        'numero_original': numero_str,
        'base_origen': base_origen,
        'base_destino': base_destino,
        'resultado_optimizado': optimizado['resultado'],
        'resultado_tradicional': resultado_tradicional,
        'coinciden': optimizado['resultado'] == resultado_tradicional,
        'explicacion': f"""
Conversión Optimizada (Bases Relacionadas):
  • Aprovecha que {base_origen} = {optimizado['base_primitiva']}^{optimizado['exponentes'][0]}
                   y {base_destino} = {optimizado['base_primitiva']}^{optimizado['exponentes'][1]}
  • Evita conversión a decimal intermedia
  • Usa agrupación de dígitos

Conversión Tradicional:
  • {numero_str}₍{base_origen}₎ → decimal → base {base_destino}
  • Siempre funciona pero menos eficiente para bases relacionadas

Resultado: Ambas dan {optimizado['resultado']} ✓
        """
    }


# Ejemplos de uso
if __name__ == "__main__":
    print("Conversión entre Bases Relacionadas\n")
    
    # Ejemplo 1: Binario a Hexadecimal (2 → 16, es decir 2^1 → 2^4)
    print("=" * 60)
    print("Ejemplo 1: Binario (2) a Hexadecimal (16)")
    print("=" * 60)
    
    numero = "11111111"
    resultado = convertir_bases_relacionadas(numero, 2, 16, verbose=True)
    print(f"Número: {numero}₂")
    print(f"Resultado: {resultado['resultado']}₁₆")
    print(f"Base primitiva: {resultado['base_primitiva']}")
    print(f"Exponentes: {resultado['exponentes'][0]} y {resultado['exponentes'][1]}")
    print()
