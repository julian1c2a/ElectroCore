"""
SECCIÓN 2.1.1.7.4: Exceso a K (Biased Representation)

Representación de números enteros usando un sesgo (bias) K.

Exceso a K permite:
- Representar números negativos sin bit de signo
- Flexibilidad en rango: [-K, B^l - K - 1]
- 100% de eficacia en cualquier base
- Operaciones aritméticas módulo B^l
- Usado en IEEE 754 para exponentes
"""

from typing import Dict, Tuple


def repr_ExcK(numero: int, base: int, longitud: int, K: int) -> str:
    """
    Representación en Exceso a K.
    
    ReprExcK(numero) = numero + K, si 0 <= numero + K <= B^l - 1
    
    Args:
        numero: Entero a representar (puede ser negativo)
        base: La base numérica
        longitud: Número de dígitos para la representación
        K: El sesgo (bias)
    
    Returns:
        str: La representación en Exceso a K con la longitud especificada
    
    Examples:
        repr_ExcK(0, 10, 2, 47)    -> '47'    (0 + 47 = 47)
        repr_ExcK(-47, 10, 2, 47)  -> '00'    (-47 + 47 = 0)
        repr_ExcK(52, 10, 2, 47)   -> '99'    (52 + 47 = 99)
        repr_ExcK(-5, 2, 8, 127)   -> '01111110'  (-5 + 127 = 122)
    """
    # Calcular la representación
    valor_exc = numero + K
    
    # Verificar que esté en rango [0, B^l - 1]
    max_val = base ** longitud
    if valor_exc < 0 or valor_exc >= max_val:
        raise ValueError(f"Número {numero} no representable en ExcK({base}, {K}, {longitud}): "
                        f"valor {valor_exc} fuera de rango [0, {max_val - 1}]")
    
    # Formatear resultado
    if base == 10:
        return str(valor_exc).zfill(longitud)
    elif base == 2:
        return format(valor_exc, f'0{longitud}b')
    else:
        return format(valor_exc, f'0{longitud}x')


def ExcK_a_decimal(palabra: str, base: int, K: int) -> int:
    """
    Conversión de Exceso a K a decimal.
    
    Interpreta una palabra en ExcK y devuelve su valor como entero decimal.
    
    Args:
        palabra: String de dígitos en ExcK
        base: La base numérica de la palabra
        K: El sesgo (bias)
    
    Returns:
        int: El valor decimal del número
    
    Examples:
        ExcK_a_decimal('47', 10, 47)  -> 0
        ExcK_a_decimal('00', 10, 47)  -> -47
        ExcK_a_decimal('99', 10, 47)  -> 52
    """
    # Interpretar palabra como valor natural en base B
    valor_natural = int(palabra, base)
    
    # Restar K para obtener el valor decimal
    return valor_natural - K


def suma_ExcK(palabra_a: str, palabra_b: str, base: int, K: int) -> dict:
    """
    Suma en Exceso a K.
    
    Si A = a + K y B = b + K, entonces:
    A + B = a + b + 2K
    
    Para obtener A '#' B (suma en ExcK):
    A '#' B = A + B - K = a + b + K
    
    Args:
        palabra_a: Primera palabra en ExcK
        palabra_b: Segunda palabra en ExcK
        base: La base numérica
        K: El sesgo (bias)
    
    Returns:
        dict: {
            'resultado': Resultado de la suma,
            'llevo': True si hubo carry/overflow,
            'valor_decimal': Valor decimal del resultado
        }
    
    Examples:
        suma_ExcK('47', '47', 10, 47) -> resultado='47', valor_decimal=0
        suma_ExcK('48', '49', 10, 47) -> resultado='50', valor_decimal=3 (1+2=3)
    """
    longitud = len(palabra_a)
    
    # Convertir a decimal
    val_a = ExcK_a_decimal(palabra_a, base, K)
    val_b = ExcK_a_decimal(palabra_b, base, K)
    
    # Suma decimal
    suma_decimal = val_a + val_b
    
    # Formatear resultado
    try:
        resultado = repr_ExcK(suma_decimal, base, longitud, K)
        llevo = False
    except ValueError:
        # Overflow: truncar con modulo
        max_val = base ** longitud
        valor_exc = (suma_decimal + K) % max_val
        if base == 10:
            resultado = str(valor_exc).zfill(longitud)
        elif base == 2:
            resultado = format(valor_exc, f'0{longitud}b')
        else:
            resultado = format(valor_exc, f'0{longitud}x')
        llevo = True
    
    valor_resultado = ExcK_a_decimal(resultado, base, K)
    
    return {
        'resultado': resultado,
        'llevo': llevo,
        'valor_decimal': valor_resultado,
        'valor_exacto': suma_decimal
    }


def resta_ExcK(palabra_a: str, palabra_b: str, base: int, K: int) -> dict:
    """
    Resta en Exceso a K.
    
    Si A = a + K y B = b + K, entonces:
    A '-' B = A + (-B operación) - K + K = A - B
    
    Pero en ExcK, la resta se calcula como:
    - Obtener -b (negativo de b)
    - Convertir a ExcK: ReprExcK(-b) = -b + K
    - Sumar: A '#' ReprExcK(-b)
    
    O más simple: a - b = a + b - 2K, pero en representaciones:
    A - B = (A - K) - (B - K) + K = A - B + K
    
    Args:
        palabra_a: Primera palabra (minuendo)
        palabra_b: Segunda palabra (sustraendo)
        base: La base numérica
        K: El sesgo (bias)
    
    Returns:
        dict: Resultado de la resta
    """
    longitud = len(palabra_a)
    
    # Convertir a decimal
    val_a = ExcK_a_decimal(palabra_a, base, K)
    val_b = ExcK_a_decimal(palabra_b, base, K)
    
    # Resta decimal
    resta_decimal = val_a - val_b
    
    # Formatear resultado
    try:
        resultado = repr_ExcK(resta_decimal, base, longitud, K)
        llevo = False
    except ValueError:
        # Overflow: truncar con modulo
        max_val = base ** longitud
        valor_exc = (resta_decimal + K) % max_val
        if base == 10:
            resultado = str(valor_exc).zfill(longitud)
        elif base == 2:
            resultado = format(valor_exc, f'0{longitud}b')
        else:
            resultado = format(valor_exc, f'0{longitud}x')
        llevo = True
    
    valor_resultado = ExcK_a_decimal(resultado, base, K)
    
    return {
        'resultado': resultado,
        'llevo': llevo,
        'valor_decimal': valor_resultado,
        'valor_exacto': resta_decimal
    }


def multiplicacion_ExcK(palabra_a: str, palabra_b: str, base: int, K: int) -> dict:
    """
    Multiplicación en Exceso a K.
    
    Si A = a + K y B = b + K, entonces:
    A * B = (a + K)(b + K) = ab + aK + bK + K^2
    
    Pero queremos ReprExcK(a*b) = a*b + K
    
    Algoritmo:
    1. Restar K a ambas representaciones: a = A - K, b = B - K
    2. Multiplicar: a * b
    3. Sumar K al resultado: a*b + K
    
    Args:
        palabra_a: Primera palabra
        palabra_b: Segunda palabra
        base: La base numérica
        K: El sesgo (bias)
    
    Returns:
        dict: {
            'resultado': Resultado truncado a longitud,
            'llevo': True si hay overflow,
            'valor_decimal': Valor decimal del resultado,
            'valor_exacto': Valor decimal sin truncar
        }
    """
    longitud = len(palabra_a)
    
    # Convertir a decimal
    val_a = ExcK_a_decimal(palabra_a, base, K)
    val_b = ExcK_a_decimal(palabra_b, base, K)
    
    # Multiplicar
    producto = val_a * val_b
    
    # Formatear resultado (truncado a l dígitos)
    try:
        resultado = repr_ExcK(producto, base, longitud, K)
        llevo = False
    except ValueError:
        # Overflow: truncar con modulo
        max_val = base ** longitud
        valor_exc = (producto + K) % max_val
        if base == 10:
            resultado = str(valor_exc).zfill(longitud)
        elif base == 2:
            resultado = format(valor_exc, f'0{longitud}b')
        else:
            resultado = format(valor_exc, f'0{longitud}x')
        llevo = True
    
    valor_resultado = ExcK_a_decimal(resultado, base, K)
    
    return {
        'resultado': resultado,
        'llevo': llevo,
        'valor_decimal': valor_resultado,
        'valor_exacto': producto
    }


def analizar_representacion_ExcK(base: int, longitud: int, K: int) -> dict:
    """
    Análisis completo de la representación en Exceso a K.
    
    Args:
        base: La base numérica
        longitud: Número de dígitos
        K: El sesgo (bias)
    
    Returns:
        dict: Información sobre el rango, capacidad y eficacia
    """
    # Rango
    min_numero = -K
    max_numero = (base ** longitud) - 1 - K
    
    # Capacidad
    capacidad = base ** longitud
    
    # Eficacia
    eficacia = 1.0  # ExcK usa TODA la capacidad
    
    return {
        'base': base,
        'longitud': longitud,
        'K': K,
        'rango_total': [min_numero, max_numero],
        'min_numero': min_numero,
        'max_numero': max_numero,
        'capacidad': capacidad,
        'total_posible': capacidad,
        'eficacia': eficacia,
        'porcentaje_eficacia': f"{eficacia * 100:.2f}%",
        'representacion_cero': 'K',
        'representacion_minimo': '0' * longitud,
        'nota': 'ExcK utiliza toda la capacidad: flexibilidad total en rango'
    }


def generar_tabla_ExcK(base: int, longitud: int, K: int) -> str:
    """
    Genera una tabla de todas las representaciones en ExcK.
    
    Args:
        base: La base numérica (recomendado: 2 o 10)
        longitud: Número de dígitos
        K: El sesgo (bias)
    
    Returns:
        str: Tabla formateada
    """
    if base == 10 and longitud > 3:
        return f"Tabla muy grande para B={base}, L={longitud}. Use longitud <= 3."
    
    if base == 2 and longitud > 8:
        return f"Tabla muy grande para B={base}, L={longitud}. Use longitud <= 8."
    
    total_combinaciones = base ** longitud
    
    lineas = []
    lineas.append(f"Tabla de representacion en ExcK (base {base}, {longitud} digitos, K={K})")
    lineas.append("=" * 100)
    lineas.append(f"{'Decimal':>8} | {'Repr. ExcK':>15} | {'Valor Natural':>15} | Significado")
    lineas.append("-" * 100)
    
    for i in range(total_combinaciones):
        # Convertir a representación
        if base == 10:
            exc_str = str(i).zfill(longitud)
        elif base == 2:
            exc_str = format(i, f'0{longitud}b')
        else:
            exc_str = format(i, f'0{longitud}x')
        
        # Obtener valor decimal
        valor = ExcK_a_decimal(exc_str, base, K)
        
        linea = f"{valor:8d} | {exc_str:>15} | {i:>15d} | "
        
        # Agregar notas especiales
        if valor == -K:
            linea += "Minimo (00...0)"
        elif valor == 0:
            linea += "Cero (representa 0)"
        elif valor == (base ** longitud) - 1 - K:
            linea += "Maximo"
        
        lineas.append(linea)
    
    lineas.append("=" * 100)
    
    return "\n".join(lineas)


def explicar_operacion_ExcK(numero_a: int, numero_b: int, operacion: str, 
                             base: int = 10, longitud: int = 2, K: int = None) -> str:
    """
    Explicación paso a paso de operaciones en ExcK.
    
    Args:
        numero_a: Primer número
        numero_b: Segundo número
        operacion: 'suma', 'resta', 'multiplicacion'
        base: La base numérica (default: 10)
        longitud: Número de dígitos
        K: El sesgo (si None, se usa B^l / 2)
    
    Returns:
        str: Explicación detallada
    """
    if K is None:
        # Por defecto, usar K = B^l / 2 para simetría
        K = (base ** longitud) // 2
    
    pasos = []
    pasos.append(f"Operacion: {operacion.upper()}")
    pasos.append(f"Base: {base}, Longitud: {longitud} digitos, K: {K}")
    pasos.append("=" * 70)
    
    if operacion == 'suma':
        try:
            exc_a = repr_ExcK(numero_a, base, longitud, K)
            exc_b = repr_ExcK(numero_b, base, longitud, K)
            
            pasos.append(f"Numero A: {numero_a:3d} -> ExcK: {exc_a}")
            pasos.append(f"Numero B: {numero_b:3d} -> ExcK: {exc_b}")
            
            resultado_suma = suma_ExcK(exc_a, exc_b, base, K)
            pasos.append(f"Suma en ExcK: {exc_a} + {exc_b} = {resultado_suma['resultado']}")
            
            if resultado_suma['llevo']:
                pasos.append("  (Con overflow)")
            
            pasos.append(f"Valor decimal del resultado: {resultado_suma['valor_decimal']}")
            pasos.append(f"Esperado: {numero_a} + {numero_b} = {numero_a + numero_b}")
            
            if resultado_suma['valor_decimal'] == numero_a + numero_b:
                pasos.append("[OK] Resultado correcto!")
        except ValueError as e:
            pasos.append(f"ERROR: {e}")
    
    elif operacion == 'resta':
        try:
            exc_a = repr_ExcK(numero_a, base, longitud, K)
            exc_b = repr_ExcK(numero_b, base, longitud, K)
            
            pasos.append(f"Numero A: {numero_a:3d} -> ExcK: {exc_a}")
            pasos.append(f"Numero B: {numero_b:3d} -> ExcK: {exc_b}")
            
            resultado_resta = resta_ExcK(exc_a, exc_b, base, K)
            pasos.append(f"Resta en ExcK: {exc_a} - {exc_b} = {resultado_resta['resultado']}")
            
            if resultado_resta['llevo']:
                pasos.append("  (Con overflow)")
            
            pasos.append(f"Valor decimal del resultado: {resultado_resta['valor_decimal']}")
            pasos.append(f"Esperado: {numero_a} - {numero_b} = {numero_a - numero_b}")
            
            if resultado_resta['valor_decimal'] == numero_a - numero_b:
                pasos.append("[OK] Resultado correcto!")
        except ValueError as e:
            pasos.append(f"ERROR: {e}")
    
    elif operacion == 'multiplicacion':
        try:
            exc_a = repr_ExcK(numero_a, base, longitud, K)
            exc_b = repr_ExcK(numero_b, base, longitud, K)
            
            pasos.append(f"Numero A: {numero_a:3d} -> ExcK: {exc_a}")
            pasos.append(f"Numero B: {numero_b:3d} -> ExcK: {exc_b}")
            
            resultado_mult = multiplicacion_ExcK(exc_a, exc_b, base, K)
            pasos.append(f"Multiplicacion exacta: {numero_a} * {numero_b} = {resultado_mult['valor_exacto']}")
            pasos.append(f"Resultado en ExcK (truncado a {longitud} digitos): {resultado_mult['resultado']}")
            pasos.append(f"Valor decimal del resultado: {resultado_mult['valor_decimal']}")
            
            if resultado_mult['llevo']:
                pasos.append("  (Con overflow - resultado truncado)")
        except ValueError as e:
            pasos.append(f"ERROR: {e}")
    
    return "\n".join(pasos)
