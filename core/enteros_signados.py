"""
SECCIÓN 2.1.1.7: Números Enteros con Signo

Tema: Representación en Magnitud y Signo (M&S)

La representación más natural de números enteros con signo es la que usamos
en matemáticas desde niños: escribimos un signo (+/-) y una magnitud.

En binario de longitud fija, usamos:
- Bit MSB (índice n-1): Bit de signo
  - 0 = positivo (+)
  - 1 = negativo (-)
- Bits MSB-1 hasta LSB: Magnitud (valor absoluto)

Ejemplo: En 8 bits (M&S8)
┌─────────────────────────────────┐
│ 0 1 0 1 0 1 1 0 │  = +86 (decimal)
│ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
│ s m m m m m m m │  (s=signo, m=magnitud)
│ 7 6 5 4 3 2 1 0 │  (índices de bit)
└─────────────────────────────────┘

Bit 7 (MSB, signo) = 0 → positivo
Bits 6-0 (magnitud) = 1010110₂ = 86₁₀
Valor = +86

Otro ejemplo: En 8 bits (M&S8)
┌─────────────────────────────────┐
│ 1 1 0 1 0 1 1 0 │  = -86 (decimal)
│ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
│ s m m m m m m m │
│ 7 6 5 4 3 2 1 0 │
└─────────────────────────────────┘

Bit 7 (MSB, signo) = 1 → negativo
Bits 6-0 (magnitud) = 1010110₂ = 86₁₀
Valor = -86

PROPIEDADES FUNDAMENTALES:

1. RANGO DE REPRESENTACIÓN (n bits):
   - Números negativos: [-2^(n-1) + 1, -1]
   - Números positivos: [1, 2^(n-1) - 1]
   - Dos representaciones para 0: +0 (00...0) y -0 (10...0)
   - Rango total: [-2^(n-1) + 1, 2^(n-1) - 1]

2. CAPACIDAD:
   - Total de valores diferentes: 2^n - 1
   - (2^n combinaciones menos 1 por la duplicación del 0)

3. EFICACIA:
   - η = (2^n - 1) / 2^n = 1 - (1/2^n) ≈ 1 para n grande

4. VENTAJAS:
   - Intuitivo: como escribimos números a mano
   - Negación simple: invertir el bit de signo
   - Multiplicación/División: |A|·|B| con ajuste de signo

5. DESVENTAJAS:
   - Suma y resta requieren algoritmos diferentes
   - Comparación de negativos es invertida
   - Dos representaciones para el 0
   - Necesita validación de igualdad especial

CONVENCIÓN MSB/LSB:
- MSB (Most Significant Bit) = bit n-1 = bit de signo
- LSB (Least Significant Bit) = bit 0 = bit menos significativo de magnitud
"""

from typing import Dict, Tuple, List, Union
import math


# ============================================================================
# PARTE 1: ANÁLISIS DE RANGO Y CAPACIDAD
# ============================================================================

def rango_ms(n_bits: int) -> Dict[str, Union[int, Tuple[int, int]]]:
    """
    Calcula el rango de valores representables en M&S con n bits.
    
    Args:
        n_bits: Número total de bits (incluyendo bit de signo)
    
    Returns:
        Dict con:
        - min_negativo: Número más pequeño (más negativo)
        - max_negativo: -1 (número negativo más grande)
        - cero_positivo: 0
        - cero_negativo: 0 (representación alternativa)
        - min_positivo: 1
        - max_positivo: Número más grande
        - rango_negativos: Tupla (min_neg, max_neg)
        - rango_positivos: Tupla (min_pos, max_pos)
        - rango_total: Tupla (min_global, max_global)
        - magnitud_bits: Número de bits para magnitud (n-1)
        - capacidad: Total de valores diferentes (2^n - 1)
        - eficacia: Porcentaje de combinaciones usadas
    
    Ejemplo:
        rango_ms(8) retorna:
        {
            'min_negativo': -127,
            'max_negativo': -1,
            'min_positivo': 1,
            'max_positivo': 127,
            'rango_total': (-127, 127),
            'capacidad': 255,
            'eficacia': 0.9961 (99.61%)
        }
    """
    if n_bits < 2:
        raise ValueError("Se requieren al menos 2 bits (1 signo + 1 magnitud)")
    
    magnitud_bits = n_bits - 1
    max_magnitud = 2 ** magnitud_bits - 1
    
    min_negativo = -max_magnitud
    max_negativo = -1
    min_positivo = 1
    max_positivo = max_magnitud
    
    total_combinaciones = 2 ** n_bits
    capacidad = total_combinaciones - 1  # Menos 1 por la duplicación del 0
    eficacia = capacidad / total_combinaciones
    
    return {
        'min_negativo': min_negativo,
        'max_negativo': max_negativo,
        'cero': 0,
        'min_positivo': min_positivo,
        'max_positivo': max_positivo,
        'rango_negativos': (min_negativo, max_negativo),
        'rango_positivos': (min_positivo, max_positivo),
        'rango_total': (min_negativo, max_positivo),
        'magnitud_bits': magnitud_bits,
        'bits_totales': n_bits,
        'capacidad': capacidad,
        'total_combinaciones': total_combinaciones,
        'eficacia': eficacia,
        'porcentaje_eficacia': f"{eficacia*100:.2f}%"
    }


def analizar_ms(n_bits: int) -> str:
    """
    Análisis detallado de M&S para n bits.
    
    Retorna explicación en texto comprensible.
    """
    info = rango_ms(n_bits)
    
    texto = f"""
╔════════════════════════════════════════════════════════════════╗
║  ANÁLISIS: Magnitud y Signo con {info['bits_totales']} bits
╚════════════════════════════════════════════════════════════════╝

ESTRUCTURA:
  • Bit MSB (índice {info['magnitud_bits']}): Bit de signo (0=+, 1=-)
  • Bits {info['magnitud_bits']-1} hasta 0: Magnitud (valor absoluto)

RANGO DE VALORES:
  • Negativos: [{info['min_negativo']:6d}, {info['max_negativo']:6d}]
  • Positivos: [{info['min_positivo']:6d}, {info['max_positivo']:6d}]
  • Especial:  [0, -0] (dos representaciones del cero)
  
RANGO TOTAL: [{info['min_negativo']:6d}, {info['max_positivo']:6d}]

CAPACIDAD Y EFICIENCIA:
  • Combinaciones totales: 2^{info['bits_totales']} = {info['total_combinaciones']}
  • Valores representables: {info['capacidad']} (menos 1 por -0)
  • Eficacia: {info['porcentaje_eficacia']}

EJEMPLOS DE REPRESENTACIÓN:

Número +{info['max_positivo']}:
  Signo: 0 (positivo)
  Magnitud: {info['max_positivo']} en {info['magnitud_bits']} bits = {bin(info['max_positivo'])[2:].zfill(info['magnitud_bits'])}
  Representación: 0{bin(info['max_positivo'])[2:].zfill(info['magnitud_bits'])}

Número -{info['max_positivo']}:
  Signo: 1 (negativo)
  Magnitud: {info['max_positivo']} en {info['magnitud_bits']} bits = {bin(info['max_positivo'])[2:].zfill(info['magnitud_bits'])}
  Representación: 1{bin(info['max_positivo'])[2:].zfill(info['magnitud_bits'])}

Número +0:
  Representación: 0{'0' * info['magnitud_bits']}

Número -0:
  Representación: 1{'0' * info['magnitud_bits']}
"""
    return texto


# ============================================================================
# PARTE 2: CONVERSIÓN DECIMAL ↔ M&S
# ============================================================================

def decimal_a_ms(numero: int, n_bits: int) -> str:
    """
    Convierte un número decimal a M&S con n bits.
    
    Args:
        numero: Número decimal a convertir (int)
        n_bits: Número de bits total
    
    Returns:
        String con la representación en M&S
    
    Raises:
        ValueError: Si el número no cabe en el rango
    
    Ejemplo:
        decimal_a_ms(86, 8) → '01010110'
        decimal_a_ms(-86, 8) → '11010110'
        decimal_a_ms(0, 8) → '00000000' (+0)
    """
    info = rango_ms(n_bits)
    
    if numero < info['min_negativo'] or numero > info['max_positivo']:
        raise ValueError(
            f"Número {numero} fuera de rango [{info['min_negativo']}, {info['max_positivo']}] "
            f"para M&S con {n_bits} bits"
        )
    
    magnitud_bits = n_bits - 1
    
    if numero > 0:
        # Número positivo: bit de signo = 0
        signo_bit = '0'
        magnitud = numero
    elif numero < 0:
        # Número negativo: bit de signo = 1
        signo_bit = '1'
        magnitud = abs(numero)
    else:
        # Número cero: representación +0
        signo_bit = '0'
        magnitud = 0
    
    # Representar magnitud en binario con magnitud_bits dígitos
    magnitud_bin = bin(magnitud)[2:].zfill(magnitud_bits)
    
    return signo_bit + magnitud_bin


def ms_a_decimal(representacion_ms: str) -> int:
    """
    Convierte una representación M&S a decimal.
    
    Args:
        representacion_ms: String de 0s y 1s en M&S
    
    Returns:
        Número decimal equivalente
    
    Raises:
        ValueError: Si la representación no es válida
    
    Ejemplo:
        ms_a_decimal('01010110') → 86
        ms_a_decimal('11010110') → -86
        ms_a_decimal('00000000') → 0
        ms_a_decimal('10000000') → 0 (también -0)
    """
    if not representacion_ms:
        raise ValueError("Representación vacía")
    
    if not all(c in '01' for c in representacion_ms):
        raise ValueError(f"Caracteres inválidos en '{representacion_ms}'")
    
    n_bits = len(representacion_ms)
    magnitud_bits = n_bits - 1
    
    signo_bit = int(representacion_ms[0])
    magnitud_bits_str = representacion_ms[1:]
    magnitud = int(magnitud_bits_str, 2)
    
    if magnitud == 0:
        # El cero, independientemente del signo
        return 0
    
    # Si signo es 1, el número es negativo
    if signo_bit == 1:
        return -magnitud
    else:
        return magnitud


def explicar_conversion_ms(numero: int, n_bits: int) -> Dict[str, Union[int, str, Dict]]:
    """
    Explica paso a paso la conversión de decimal a M&S.
    
    Args:
        numero: Número decimal
        n_bits: Número de bits
    
    Returns:
        Dict con explicación detallada
    """
    info = rango_ms(n_bits)
    representacion = decimal_a_ms(numero, n_bits)
    
    magnitud_bits = n_bits - 1
    signo_bit = representacion[0]
    magnitud_bits_str = representacion[1:]
    magnitud = int(magnitud_bits_str, 2)
    
    return {
        'numero_decimal': numero,
        'n_bits': n_bits,
        'magnitud_bits': magnitud_bits,
        'en_rango': numero >= info['min_negativo'] and numero <= info['max_positivo'],
        'es_positivo': numero > 0,
        'es_negativo': numero < 0,
        'es_cero': numero == 0,
        'paso_1_signo': {
            'descripcion': 'Determinar el signo',
            'numero': numero,
            'signo': 'positivo (+)' if numero >= 0 else 'negativo (-)',
            'bit_signo': signo_bit,
            'significado': '0 = positivo, 1 = negativo'
        },
        'paso_2_magnitud': {
            'descripcion': 'Obtener la magnitud (valor absoluto)',
            'numero': numero,
            'magnitud': magnitud,
            'bits_disponibles': magnitud_bits,
            'conversion_binaria': {
                'magnitud_decimal': magnitud,
                'magnitud_binaria': magnitud_bits_str,
                'longitud': len(magnitud_bits_str)
            }
        },
        'paso_3_combinacion': {
            'descripcion': 'Combinar signo + magnitud',
            'signo_bit': signo_bit,
            'magnitud_bits': magnitud_bits_str,
            'representacion_final': representacion
        },
        'resultado_final': {
            'representacion': representacion,
            'formato': f"M&S{n_bits}",
            'valor_recuperado': ms_a_decimal(representacion)
        }
    }


# ============================================================================
# PARTE 3: OPERACIONES EN M&S
# ============================================================================

def negacion_ms(representacion_ms: str) -> str:
    """
    Obtiene el negativo de un número en M&S (multiplicación por -1).
    
    Operación: Invertir el bit de signo (flip)
    - 0 → 1 (positivo a negativo)
    - 1 → 0 (negativo a positivo)
    
    Args:
        representacion_ms: String en M&S
    
    Returns:
        String con la negación
    
    Ejemplo:
        negacion_ms('01010110') → '11010110'  (+86 → -86)
        negacion_ms('11010110') → '01010110'  (-86 → +86)
        negacion_ms('00000000') → '10000000'  (+0 → -0)
    """
    signo_bit = int(representacion_ms[0])
    magnitud_bits = representacion_ms[1:]
    
    nuevo_signo = 1 - signo_bit  # Flip del bit
    
    return str(nuevo_signo) + magnitud_bits


def es_positivo_ms(representacion_ms: str) -> bool:
    """¿El número es positivo o cero en M&S?"""
    return representacion_ms[0] == '0'


def es_negativo_ms(representacion_ms: str) -> bool:
    """¿El número es negativo en M&S?"""
    return representacion_ms[0] == '1'


def es_cero_ms(representacion_ms: str) -> bool:
    """¿El número es cero (en cualquier representación)?"""
    magnitud_bits = representacion_ms[1:]
    return all(c == '0' for c in magnitud_bits)


def valor_absoluto_ms(representacion_ms: str) -> int:
    """
    Obtiene el valor absoluto de un número en M&S.
    
    Ejemplo:
        valor_absoluto_ms('11010110') → 86
    """
    magnitud_bits = representacion_ms[1:]
    return int(magnitud_bits, 2)


def comparar_ms(rep_a: str, rep_b: str) -> int:
    """
    Compara dos números en M&S.
    
    Returns:
        -1 si A < B
         0 si A = B
         1 si A > B
    
    Nota: La comparación de números negativos es "invertida" en M&S.
    Ejemplo: -100 < -50, pero en M&S la magnitud de -100 es mayor.
    Por eso necesitamos este algoritmo especial.
    """
    val_a = ms_a_decimal(rep_a)
    val_b = ms_a_decimal(rep_b)
    
    if val_a < val_b:
        return -1
    elif val_a > val_b:
        return 1
    else:
        return 0


# ============================================================================
# PARTE 4: VALIDACIÓN Y ANÁLISIS
# ============================================================================

def validar_representacion_ms(representacion_ms: str, n_bits_esperado: int = None) -> Dict[str, Union[bool, str]]:
    """
    Valida que una representación sea válida en M&S.
    
    Args:
        representacion_ms: String a validar
        n_bits_esperado: Número de bits esperado (opcional)
    
    Returns:
        Dict con validación
    """
    errores = []
    
    # Validar caracteres
    if not all(c in '01' for c in representacion_ms):
        errores.append("Contiene caracteres que no son 0 o 1")
    
    # Validar longitud
    if len(representacion_ms) < 2:
        errores.append("Debe tener al menos 2 bits (1 signo + 1 magnitud)")
    
    # Validar longitud esperada
    if n_bits_esperado and len(representacion_ms) != n_bits_esperado:
        errores.append(f"Longitud {len(representacion_ms)}, se esperaba {n_bits_esperado}")
    
    return {
        'valida': len(errores) == 0,
        'errores': errores,
        'longitud': len(representacion_ms),
        'es_binario': all(c in '01' for c in representacion_ms) if representacion_ms else False
    }


def analizar_representacion_ms(representacion_ms: str) -> Dict:
    """
    Análisis completo de una representación en M&S.
    """
    validacion = validar_representacion_ms(representacion_ms)
    
    if not validacion['valida']:
        return {
            'valida': False,
            'errores': validacion['errores']
        }
    
    n_bits = len(representacion_ms)
    magnitud_bits = n_bits - 1
    
    signo_bit = int(representacion_ms[0])
    magnitud_bits_str = representacion_ms[1:]
    magnitud = int(magnitud_bits_str, 2)
    
    valor = ms_a_decimal(representacion_ms)
    
    rango_info = rango_ms(n_bits)
    
    return {
        'valida': True,
        'representacion': representacion_ms,
        'n_bits': n_bits,
        'estructura': {
            'bit_signo': f"bit {magnitud_bits} = {signo_bit}",
            'bits_magnitud': f"bits {magnitud_bits-1} a 0 = {magnitud_bits_str}",
            'signo_significado': 'positivo (+)' if signo_bit == 0 else 'negativo (-)'
        },
        'valor_decimal': valor,
        'magnitud': magnitud,
        'en_rango': valor >= rango_info['min_negativo'] and valor <= rango_info['max_positivo'],
        'es_positivo': valor > 0,
        'es_negativo': valor < 0,
        'es_cero': valor == 0,
        'es_positivo_cero': representacion_ms == '0' * n_bits,
        'es_negativo_cero': representacion_ms == '1' + '0' * magnitud_bits,
        'rango_disponible': rango_info['rango_total'],
        'negacion': negacion_ms(representacion_ms)
    }


# ============================================================================
# PARTE 5: CONSTRUCTORES Y UTILIDADES
# ============================================================================

def crear_cero_positivo_ms(n_bits: int) -> str:
    """
    Crea la representación de +0 en M&S.
    
    Ejemplo:
        crear_cero_positivo_ms(8) → '00000000'
    """
    return '0' * n_bits


def crear_cero_negativo_ms(n_bits: int) -> str:
    """
    Crea la representación de -0 en M&S.
    
    Ejemplo:
        crear_cero_negativo_ms(8) → '10000000'
    """
    magnitud_bits = n_bits - 1
    return '1' + '0' * magnitud_bits


def generar_tabla_ms(n_bits: int) -> List[Dict]:
    """
    Genera tabla completa de valores representables en M&S.
    
    Retorna lista de dicts con:
    - decimal: valor decimal
    - ms_representation: representación en M&S
    - signo: + o -
    - magnitud: valor absoluto
    """
    info = rango_ms(n_bits)
    tabla = []
    
    # Negativos
    for i in range(info['min_negativo'], 0):
        tabla.append({
            'decimal': i,
            'ms': decimal_a_ms(i, n_bits),
            'signo': '-',
            'magnitud': abs(i)
        })
    
    # Ceros
    tabla.append({
        'decimal': 0,
        'ms': crear_cero_positivo_ms(n_bits),
        'signo': '+',
        'magnitud': 0,
        'nota': '+0'
    })
    
    tabla.append({
        'decimal': 0,
        'ms': crear_cero_negativo_ms(n_bits),
        'signo': '-',
        'magnitud': 0,
        'nota': '-0 (duplicado)'
    })
    
    # Positivos
    for i in range(1, info['max_positivo'] + 1):
        tabla.append({
            'decimal': i,
            'ms': decimal_a_ms(i, n_bits),
            'signo': '+',
            'magnitud': i
        })
    
    return tabla


def mostrar_tabla_ms(n_bits: int) -> str:
    """
    Muestra tabla de M&S en formato legible.
    """
    tabla = generar_tabla_ms(n_bits)
    
    lineas = [
        f"╔ Tabla de Magnitud y Signo ({n_bits} bits) ╗",
        "┌──────────┬────────────┬──────┬───────────┐",
        "│ Decimal  │ M&S Repr.  │ Sign │ Magnitud  │",
        "├──────────┼────────────┼──────┼───────────┤"
    ]
    
    for entrada in tabla:
        decimal = entrada['decimal']
        ms = entrada['ms']
        signo = entrada['signo']
        magnitud = entrada['magnitud']
        nota = entrada.get('nota', '')
        
        linea = f"│ {decimal:8d} │ {ms:10s} │  {signo}   │ {magnitud:9d} │"
        if nota:
            linea += f"  {nota}"
        lineas.append(linea)
    
    lineas.append("└──────────┴────────────┴──────┴───────────┘")
    
    return "\n".join(lineas)


# ============================================================================
# PARTE 2: COMPLEMENTO A LA BASE MENOS 1 (CB-1 o C1)
# ============================================================================

def opCBm1_digito(digito: str, base: int) -> str:
    """
    Operación de complemento a la base menos 1 de un dígito.
    
    Para un dígito d en base B:
    opCBm1(d) = B - 1 - d
    
    Esto convierte cada dígito a su complemento en esa base.
    
    Args:
        digito: Un carácter que representa un dígito en la base dada
        base: La base numérica (2, 10, 16, etc.)
    
    Returns:
        str: El dígito complementado
        
    Examples:
        opCBm1_digito('3', 10) -> '6'  (porque 9-3=6)
        opCBm1_digito('1', 2)  -> '0'  (porque 1-1=0)
        opCBm1_digito('0', 2)  -> '1'  (porque 1-0=1)
        opCBm1_digito('5', 10) -> '4'  (porque 9-5=4)
    """
    # Convertir carácter a valor
    if digito.isdigit():
        valor = int(digito)
    else:
        # Para bases > 10 (hexadecimal, etc.)
        valor = int(digito, base)
    
    # Aplicar fórmula: B - 1 - d
    resultado = (base - 1) - valor
    
    # Convertir de vuelta a carácter
    if base <= 10:
        return str(resultado)
    else:
        return format(resultado, 'x')  # Para hex


def opCBm1_palabra(palabra: str, base: int) -> str:
    """
    Operación de complemento a la base menos 1 de una palabra completa.
    
    Dada una palabra d[l-1:0] en base B:
    opCBm1(d) = ~d = (B-1-d[i]) para cada posición i
    
    El complemento se aplica dígito a dígito, sin llevar nada de una posición a otra.
    
    Args:
        palabra: String de dígitos en la base dada
        base: La base numérica (2, 10, 16, etc.)
    
    Returns:
        str: La palabra con cada dígito complementado
        
    Examples:
        opCBm1_palabra('01239', 10) -> '98760'  (9-0=9, 9-1=8, 9-2=7, 9-3=6, 9-9=0)
        opCBm1_palabra('1010', 2)   -> '0101'   (flip de cada bit)
        
    Propiedades:
        - opCBm1(opCBm1(d)) = d  (aplicar dos veces vuelve al original)
        - No hay carries ni borrows
        - Cada dígito se procesa independientemente
    """
    return ''.join(opCBm1_digito(d, base) for d in palabra)


def repr_CBm1(numero: int, base: int, longitud: int) -> str:
    """
    Representación en Complemento a la Base Menos 1 (CB-1).
    
    Dada una palabra de longitud l en base B:
    - Si numero >= 0: representa numero directamente en l dígitos
    - Si numero < 0: representa como B^l - 1 - numero (en l dígitos)
    
    Args:
        numero: Entero a representar (puede ser positivo o negativo)
        base: La base numérica (2, 10, 16, etc.)
        longitud: Número de dígitos para la representación
    
    Returns:
        str: La representación en CB-1 con la longitud especificada
        
    Examples:
        repr_CBm1(5, 10, 2)   -> '05'     (+5 en 2 dígitos)
        repr_CBm1(-5, 10, 2)  -> '94'     (-5 como 99-5=94)
        repr_CBm1(3, 2, 4)    -> '0011'   (+3 en 4 bits)
        repr_CBm1(-3, 2, 4)   -> '1100'   (-3 como 15-3=12=1100)
    """
    if numero >= 0:
        # Número positivo: convertir directamente
        return format(numero, f'0{longitud}d' if base == 10 else f'0{longitud}b' if base == 2 else f'0{longitud}x')
    else:
        # Número negativo: B^l - 1 - numero
        max_val = (base ** longitud) - 1
        valor_cb1 = max_val + numero  # +numero porque numero es negativo
        
        if base == 10:
            return str(valor_cb1).zfill(longitud)
        elif base == 2:
            return format(valor_cb1, f'0{longitud}b')
        else:
            return format(valor_cb1, f'0{longitud}x')


def CBm1_a_decimal(palabra: str, base: int) -> int:
    """
    Conversión de Complemento a la Base Menos 1 a decimal.
    
    Interpreta una palabra en CB-1 y devuelve su valor como entero decimal.
    
    Args:
        palabra: String de dígitos en CB-1
        base: La base numérica de la palabra
    
    Returns:
        int: El valor decimal del número
        
    Examples:
        CBm1_a_decimal('01239', 10) -> 1239
        CBm1_a_decimal('98760', 10) -> -1239  (porque ~01239)
        CBm1_a_decimal('0011', 2)   -> 3
        CBm1_a_decimal('1100', 2)   -> -3
    """
    longitud = len(palabra)
    # Convertir palabra a valor decimal
    valor = int(palabra, base)
    
    # Punto de separación entre positivos y negativos
    punto_separacion = (base ** (longitud - 1)) - 1
    
    if valor <= punto_separacion:
        # Es positivo o cero
        return valor
    else:
        # Es negativo: aplicar CB-1
        max_val = (base ** longitud) - 1
        return valor - max_val - 1


def ms_a_CBm1(ms_palabra: str, base: int) -> str:
    """
    Conversión de Magnitud y Signo a Complemento a la Base Menos 1.
    
    Args:
        ms_palabra: Palabra en M&S
        base: La base numérica
    
    Returns:
        str: La misma palabra en CB-1
    """
    longitud = len(ms_palabra)
    valor_decimal = ms_a_decimal(ms_palabra, base)
    return repr_CBm1(valor_decimal, base, longitud)


def CBm1_a_ms(cb1_palabra: str, base: int) -> str:
    """
    Conversión de Complemento a la Base Menos 1 a Magnitud y Signo.
    
    Args:
        cb1_palabra: Palabra en CB-1
        base: La base numérica
    
    Returns:
        str: La misma palabra en M&S
    """
    longitud = len(cb1_palabra)
    valor_decimal = CBm1_a_decimal(cb1_palabra, base)
    return decimal_a_ms(valor_decimal, base, longitud)


def suma_CBm1(palabra_a: str, palabra_b: str, base: int) -> dict:
    """
    Suma de dos palabras en Complemento a la Base Menos 1.
    
    La suma en CB-1 tiene una característica especial: si hay carry final,
    se suma 1 al resultado (end-around carry).
    
    Args:
        palabra_a: Primera palabra en CB-1
        palabra_b: Segunda palabra en CB-1
        base: La base numérica
    
    Returns:
        dict: {
            'resultado': Resultado de la suma,
            'carry': True si hubo carry,
            'carry_suma_uno': True si se sumó 1 por carry final,
            'valor_decimal': Valor decimal del resultado
        }
    """
    longitud = len(palabra_a)
    
    # Convertir a decimal
    val_a = int(palabra_a, base)
    val_b = int(palabra_b, base)
    
    # Sumar
    suma_total = val_a + val_b
    
    # Capacidad máxima
    max_val = base ** longitud
    
    # Verificar carry
    carry = suma_total >= max_val
    
    # Aplicar end-around carry si es necesario
    if carry:
        suma_total = (suma_total % max_val) + 1
    
    # Formatear resultado
    if base == 10:
        resultado = str(suma_total).zfill(longitud)
    elif base == 2:
        resultado = format(suma_total, f'0{longitud}b')
    else:
        resultado = format(suma_total, f'0{longitud}x')
    
    return {
        'resultado': resultado,
        'carry': carry,
        'carry_suma_uno': carry,
        'valor_decimal': CBm1_a_decimal(resultado, base)
    }


def analizar_representacion_CBm1(base: int, longitud: int) -> dict:
    """
    Análisis completo de la representación en CB-1.
    
    Args:
        base: La base numérica
        longitud: Número de dígitos
    
    Returns:
        dict: Información sobre el rango, capacidad y eficacia
    """
    max_positivo = (base ** (longitud - 1)) - 1
    min_negativo = -(base ** (longitud - 1)) + 1
    
    # Capacidad
    capacidad = 2 * (base ** (longitud - 1)) - 1
    total_posible = base ** longitud
    
    # Eficacia
    eficacia = capacidad / total_posible
    
    return {
        'base': base,
        'longitud': longitud,
        'rango_total': [min_negativo, max_positivo],
        'min_negativo': min_negativo,
        'max_positivo': max_positivo,
        'capacidad': capacidad,
        'total_posible': total_posible,
        'eficacia': eficacia,
        'porcentaje_eficacia': f"{eficacia * 100:.2f}%",
        'dos_ceros': True,  # CB-1 siempre tiene dos representaciones para 0
        'formula_eficacia': f"(2/{base}) - (1/{base}^{longitud})",
        'nota': 'CB-1 tiene dos representaciones para 0, no es muy usado actualmente'
    }


def generar_tabla_CBm1(base: int, longitud: int) -> str:
    """
    Genera una tabla de todas las representaciones en CB-1 para una base y longitud.
    
    Args:
        base: La base numérica (recomendado: 2 o 10)
        longitud: Número de dígitos
    
    Returns:
        str: Tabla formateada mostrando todas las representaciones
    """
    if base == 10 and longitud > 4:
        return f"Tabla muy grande para B={base}, L={longitud}. Use base 2 o menor longitud."
    
    if base == 2 and longitud > 8:
        return f"Tabla muy grande para B={base}, L={longitud}. Use longitud <= 8."
    
    total_combinaciones = base ** longitud
    
    lineas = []
    lineas.append(f"Tabla de representacion en CB-{base-1} (base {base}, {longitud} digitos)")
    lineas.append("=" * 80)
    
    lineas.append(f"{'Decimal':>8} | {'CB-{0}':>15} | Significado".format(base-1, ''))
    lineas.append("-" * 80)
    
    for i in range(total_combinaciones):
        # Convertir a representación
        if base == 10:
            cb1_str = str(i).zfill(longitud)
        elif base == 2:
            cb1_str = format(i, f'0{longitud}b')
        else:
            cb1_str = format(i, f'0{longitud}x')
        
        # Obtener valor decimal
        valor = CBm1_a_decimal(cb1_str, base)
        
        linea = f"{valor:8d} | {cb1_str:>15} | "
        
        # Agregar notas especiales
        max_pos = (base ** (longitud - 1)) - 1
        if valor == 0 and cb1_str == '0' * longitud:
            linea += "Cero positivo (+0)"
        elif valor == 0 and cb1_str == str(base-1) * longitud:
            linea += "Cero negativo (-0)"
        elif valor == max_pos:
            linea += "Maximo positivo"
        elif valor == -(max_pos):
            linea += "Minimo negativo"
        
        lineas.append(linea)
    
    lineas.append("=" * 80)
    
    return "\n".join(lineas)


def explicar_operacion_CBm1(numero_a: int, numero_b: int, operacion: str, base: int = 10, longitud: int = None) -> str:
    """
    Explicación paso a paso de operaciones en CB-1.
    
    Args:
        numero_a: Primer número
        numero_b: Segundo número
        operacion: 'suma', 'resta', 'complemento'
        base: La base numérica (default: 10)
        longitud: Número de dígitos (si None, se calcula automáticamente)
    
    Returns:
        str: Explicación detallada
    """
    if longitud is None:
        longitud = len(str(max(abs(numero_a), abs(numero_b)))) + 1
    
    pasos = []
    pasos.append(f"Operacion: {operacion.upper()}")
    pasos.append(f"Base: {base}, Longitud: {longitud} digitos")
    pasos.append("=" * 60)
    
    if operacion == 'complemento':
        pasos.append(f"Numero original: {numero_a}")
        cb1_original = repr_CBm1(numero_a, base, longitud)
        pasos.append(f"Representacion en CB-{base-1}: {cb1_original}")
        
        cb1_complementado = opCBm1_palabra(cb1_original, base)
        pasos.append(f"Complemento digit a digito: {cb1_complementado}")
        
        valor_resultado = CBm1_a_decimal(cb1_complementado, base)
        pasos.append(f"Valor decimal del resultado: {valor_resultado}")
        
        if valor_resultado == -numero_a:
            pasos.append("✓ Propiedad verificada: opCBm1(opCBm1(A)) = A")
    
    elif operacion == 'suma':
        cb1_a = repr_CBm1(numero_a, base, longitud)
        cb1_b = repr_CBm1(numero_b, base, longitud)
        
        pasos.append(f"Numero A: {numero_a} -> CB-{base-1}: {cb1_a}")
        pasos.append(f"Numero B: {numero_b} -> CB-{base-1}: {cb1_b}")
        
        resultado_suma = suma_CBm1(cb1_a, cb1_b, base)
        pasos.append(f"Suma en CB-{base-1}: {cb1_a} + {cb1_b} = {resultado_suma['resultado']}")
        
        if resultado_suma['carry']:
            pasos.append("  (Con end-around carry: suma 1 al resultado)")
        
        pasos.append(f"Valor decimal del resultado: {resultado_suma['valor_decimal']}")
        pasos.append(f"Esperado: {numero_a} + {numero_b} = {numero_a + numero_b}")
        
        if resultado_suma['valor_decimal'] == numero_a + numero_b:
            pasos.append("✓ Resultado correcto!")
    
    return "\n".join(pasos)
