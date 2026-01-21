"""
SECCIÓN 2.1.1.7.3: Complemento a la Base (CB)

Representación de números enteros con signo usando Complemento a la Base.

CB es superior a CB-1:
- Una única representación para 0
- La suma es la suma ordinaria modulo B^l
- No requiere end-around carry
- Rango: [-B^(l-1), B^(l-1) - 1]

Operación opCB(B, cadena) = opCBm1(B, cadena) + 1
                           = (flip cada dígito) + 1
"""

from typing import Dict, Tuple, List


def opCB_digito(digito: str, base: int) -> str:
    """
    Complemento a la Base de un dígito individual (sin suma de 1).
    
    Este es el primer paso: opCBm1(d) = B - 1 - d
    El paso de sumar 1 se hace en opCB_palabra().
    
    Args:
        digito: Un carácter de dígito en la base dada
        base: La base numérica (2, 10, 16, etc.)
    
    Returns:
        str: El dígito complementado
    
    Examples:
        opCB_digito('0', 2)  -> '1'
        opCB_digito('5', 10) -> '4'  (9 - 5 = 4)
    """
    valor = int(digito, base)
    resultado = (base - 1) - valor
    if base <= 10:
        return str(resultado)
    else:
        return format(resultado, 'x')


def opCB_palabra(palabra: str, base: int) -> str:
    """
    Complemento a la Base de una palabra completa.
    
    Operación en dos pasos:
    1. opCBm1: flip cada dígito (d → B-1-d)
    2. Sumar 1 al resultado completo
    
    Equivalencia: opCB(palabra) = B^l - eval(palabra)
    
    Args:
        palabra: String de dígitos en la base dada
        base: La base numérica
    
    Returns:
        str: La palabra en complemento a la base
    
    Examples:
        opCB_palabra('01239', 10) -> '98761'  (99999 - 01239 + 1)
        opCB_palabra('0101', 2)   -> '1011'   (1111 - 0101 + 1)
    """
    longitud = len(palabra)
    
    # Paso 1: flip cada dígito (opCBm1)
    flipped = ''.join(opCB_digito(d, base) for d in palabra)
    
    # Paso 2: sumar 1 al resultado
    valor = int(flipped, base)
    valor_cb = valor + 1
    
    # Manejar overflow (si la suma causa desbordamiento, truncar)
    max_val = base ** longitud
    valor_cb = valor_cb % max_val
    
    # Formatear resultado
    if base == 10:
        return str(valor_cb).zfill(longitud)
    elif base == 2:
        return format(valor_cb, f'0{longitud}b')
    else:
        return format(valor_cb, f'0{longitud}x')


def repr_CB(numero: int, base: int, longitud: int) -> str:
    """
    Representación en Complemento a la Base (CB).
    
    Para una palabra de longitud l en base B:
    - Si numero >= 0: representa numero directamente en l dígitos
    - Si numero < 0: representa como B^l - |numero| en l dígitos
    
    Equivalencia: ReprCB(numero) = numero mod B^l
                 (funciona automáticamente para negativos)
    
    Args:
        numero: Entero a representar (puede ser positivo o negativo)
        base: La base numérica
        longitud: Número de dígitos para la representación
    
    Returns:
        str: La representación en CB con la longitud especificada
    
    Examples:
        repr_CB(5, 10, 2)   -> '05'
        repr_CB(-5, 10, 2)  -> '95'     (100 - 5 = 95)
        repr_CB(3, 2, 4)    -> '0011'
        repr_CB(-3, 2, 4)   -> '1101'   (16 - 3 = 13)
    """
    max_val = base ** longitud
    
    # Mantener numero en rango [0, max_val)
    valor_cb = numero % max_val
    
    # Formatear resultado
    if base == 10:
        return str(valor_cb).zfill(longitud)
    elif base == 2:
        return format(valor_cb, f'0{longitud}b')
    else:
        return format(valor_cb, f'0{longitud}x')


def CB_a_decimal(palabra: str, base: int) -> int:
    """
    Conversión de Complemento a la Base a decimal.
    
    Interpreta una palabra en CB y devuelve su valor como entero decimal.
    
    Args:
        palabra: String de dígitos en CB
        base: La base numérica de la palabra
    
    Returns:
        int: El valor decimal del número
    
    Examples:
        CB_a_decimal('05', 10)   -> 5
        CB_a_decimal('95', 10)   -> -5
        CB_a_decimal('0011', 2)  -> 3
        CB_a_decimal('1101', 2)  -> -3
    """
    longitud = len(palabra)
    valor = int(palabra, base)
    
    # Punto de separación entre positivos y negativos
    punto_separacion = (base ** (longitud - 1)) - 1
    
    if valor <= punto_separacion:
        # Es positivo o cero
        return valor
    else:
        # Es negativo: aplicar conversión
        max_val = base ** longitud
        return valor - max_val


def ms_a_CB(ms_palabra: str, base: int) -> str:
    """
    Conversión de Magnitud y Signo a Complemento a la Base.
    
    Args:
        ms_palabra: Palabra en M&S
        base: La base numérica
    
    Returns:
        str: La misma palabra en CB
    """
    from enteros_signados import ms_a_decimal
    
    longitud = len(ms_palabra)
    valor_decimal = ms_a_decimal(ms_palabra, base)
    return repr_CB(valor_decimal, base, longitud)


def CB_a_ms(cb_palabra: str, base: int) -> str:
    """
    Conversión de Complemento a la Base a Magnitud y Signo.
    
    Args:
        cb_palabra: Palabra en CB
        base: La base numérica
    
    Returns:
        str: La misma palabra en M&S
    """
    from enteros_signados import decimal_a_ms
    
    longitud = len(cb_palabra)
    valor_decimal = CB_a_decimal(cb_palabra, base)
    return decimal_a_ms(valor_decimal, base, longitud)


def CB_a_CBm1(cb_palabra: str, base: int) -> str:
    """
    Conversión de Complemento a la Base a Complemento a la Base Menos 1.
    
    Args:
        cb_palabra: Palabra en CB
        base: La base numérica
    
    Returns:
        str: La misma palabra en CB-1
    """
    from enteros_signados import repr_CBm1
    
    longitud = len(cb_palabra)
    valor_decimal = CB_a_decimal(cb_palabra, base)
    return repr_CBm1(valor_decimal, base, longitud)


def CBm1_a_CB(cbm1_palabra: str, base: int) -> str:
    """
    Conversión de Complemento a la Base Menos 1 a Complemento a la Base.
    
    Args:
        cbm1_palabra: Palabra en CB-1
        base: La base numérica
    
    Returns:
        str: La misma palabra en CB
    """
    from enteros_signados import CBm1_a_decimal
    
    longitud = len(cbm1_palabra)
    valor_decimal = CBm1_a_decimal(cbm1_palabra, base)
    return repr_CB(valor_decimal, base, longitud)


def suma_CB(palabra_a: str, palabra_b: str, base: int) -> dict:
    """
    Suma de dos palabras en Complemento a la Base.
    
    La GRAN ventaja de CB: la suma es la suma ordinaria modulo B^l.
    No hay complicaciones de end-around carry como en CB-1.
    
    Args:
        palabra_a: Primera palabra en CB
        palabra_b: Segunda palabra en CB
        base: La base numérica
    
    Returns:
        dict: {
            'resultado': Resultado de la suma,
            'llevo': True si hubo carry/overflow,
            'valor_decimal': Valor decimal del resultado
        }
    
    Examples:
        suma_CB('05', '03', 10)  -> resultado='08', valor_decimal=8
        suma_CB('95', '03', 10)  -> resultado='98', valor_decimal=-2 (pq -5+3=-2)
    """
    longitud = len(palabra_a)
    
    # Convertir a decimal (valores en rango [-B^(l-1), B^(l-1)-1])
    val_a = CB_a_decimal(palabra_a, base)
    val_b = CB_a_decimal(palabra_b, base)
    
    # Suma normal
    suma_total = val_a + val_b
    
    # Formatear resultado (el modulo B^l se maneja automáticamente en repr_CB)
    resultado = repr_CB(suma_total, base, longitud)
    
    # Detectar overflow: si suma_total está fuera de rango
    max_val = base ** longitud
    rango_min = -(max_val // 2)
    rango_max = (max_val // 2) - 1
    llevo = suma_total < rango_min or suma_total > rango_max
    
    return {
        'resultado': resultado,
        'llevo': llevo,
        'valor_decimal': CB_a_decimal(resultado, base)
    }


def resta_CB(palabra_a: str, palabra_b: str, base: int) -> dict:
    """
    Resta de dos palabras en Complemento a la Base.
    
    Implementación: A - B = A + opCB(B) modulo B^l
    
    Args:
        palabra_a: Primera palabra (minuendo)
        palabra_b: Segunda palabra (sustraendo)
        base: La base numérica
    
    Returns:
        dict: {
            'resultado': Resultado de la resta,
            'llevo': True si hubo carry/overflow,
            'valor_decimal': Valor decimal del resultado
        }
    """
    # Negar palabra_b
    palabra_b_negada = opCB_palabra(palabra_b, base)
    
    # Sumar A + (-B)
    return suma_CB(palabra_a, palabra_b_negada, base)


def multiplicacion_CB(palabra_a: str, palabra_b: str, base: int) -> dict:
    """
    Multiplicación de dos palabras en Complemento a la Base.
    
    En CB, la multiplicación funciona directamente:
    - Si a,b > 0: ReprCB(a) * ReprCB(b) = ReprCB(a*b)
    - Si a > 0, b < 0: ReprCB(a) * ReprCB(-b) = ReprCB(-a*b)
    - Si a < 0, b < 0: ReprCB(-a) * ReprCB(-b) = ReprCB(a*b)
    
    Args:
        palabra_a: Primera palabra
        palabra_b: Segunda palabra
        base: La base numérica
    
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
    val_a = CB_a_decimal(palabra_a, base)
    val_b = CB_a_decimal(palabra_b, base)
    
    # Multiplicar
    producto = val_a * val_b
    
    # Formato resultado (truncado a l dígitos)
    resultado = repr_CB(producto, base, longitud)
    valor_resultado = CB_a_decimal(resultado, base)
    
    # Detectar overflow
    max_val = base ** longitud
    rango_min = -(max_val // 2)
    rango_max = (max_val // 2) - 1
    llevo = producto < rango_min or producto > rango_max
    
    return {
        'resultado': resultado,
        'llevo': llevo,
        'valor_decimal': valor_resultado,
        'valor_exacto': producto
    }


def analizar_representacion_CB(base: int, longitud: int) -> dict:
    """
    Análisis completo de la representación en CB.
    
    Args:
        base: La base numérica
        longitud: Número de dígitos
    
    Returns:
        dict: Información sobre el rango, capacidad y eficacia
    """
    max_positivo = (base ** (longitud - 1)) - 1
    min_negativo = -(base ** (longitud - 1))
    
    # Capacidad
    capacidad = base ** longitud
    
    # Eficacia
    eficacia = 1.0  # CB usa TODA la capacidad
    
    return {
        'base': base,
        'longitud': longitud,
        'rango_total': [min_negativo, max_positivo],
        'min_negativo': min_negativo,
        'max_positivo': max_positivo,
        'capacidad': capacidad,
        'total_posible': capacidad,
        'eficacia': eficacia,
        'porcentaje_eficacia': f"{eficacia * 100:.2f}%",
        'una_representacion_cero': True,
        'nota': 'CB utiliza toda la capacidad: no hay representaciones duplicadas'
    }


def generar_tabla_CB(base: int, longitud: int) -> str:
    """
    Genera una tabla de todas las representaciones en CB.
    
    Args:
        base: La base numérica (recomendado: 2 o 10)
        longitud: Número de dígitos
    
    Returns:
        str: Tabla formateada
    """
    if base == 10 and longitud > 3:
        return f"Tabla muy grande para B={base}, L={longitud}. Use longitud <= 3."
    
    if base == 2 and longitud > 8:
        return f"Tabla muy grande para B={base}, L={longitud}. Use longitud <= 8."
    
    total_combinaciones = base ** longitud
    
    lineas = []
    lineas.append(f"Tabla de representacion en CB (base {base}, {longitud} digitos)")
    lineas.append("=" * 80)
    lineas.append(f"{'Decimal':>8} | {'Repr. CB':>15} | Significado")
    lineas.append("-" * 80)
    
    for i in range(total_combinaciones):
        # Convertir a representación
        if base == 10:
            cb_str = str(i).zfill(longitud)
        elif base == 2:
            cb_str = format(i, f'0{longitud}b')
        else:
            cb_str = format(i, f'0{longitud}x')
        
        # Obtener valor decimal
        valor = CB_a_decimal(cb_str, base)
        
        linea = f"{valor:8d} | {cb_str:>15} | "
        
        # Agregar notas especiales
        max_pos = (base ** (longitud - 1)) - 1
        min_neg = -(base ** (longitud - 1))
        
        if valor == 0:
            linea += "Cero (unica representacion)"
        elif valor == max_pos:
            linea += "Maximo positivo"
        elif valor == min_neg:
            linea += "Minimo negativo"
        
        lineas.append(linea)
    
    lineas.append("=" * 80)
    
    return "\n".join(lineas)


def explicar_operacion_CB(numero_a: int, numero_b: int, operacion: str, 
                          base: int = 10, longitud: int = None) -> str:
    """
    Explicación paso a paso de operaciones en CB.
    
    Args:
        numero_a: Primer número
        numero_b: Segundo número
        operacion: 'suma', 'resta', 'multiplicacion', 'complemento'
        base: La base numérica (default: 10)
        longitud: Número de dígitos (si None, se calcula automáticamente)
    
    Returns:
        str: Explicación detallada
    """
    if longitud is None:
        longitud = max(len(str(abs(numero_a))), len(str(abs(numero_b)))) + 1
        if base == 2:
            longitud = max(longitud, numero_a.bit_length() + 1)
    
    pasos = []
    pasos.append(f"Operacion: {operacion.upper()}")
    pasos.append(f"Base: {base}, Longitud: {longitud} digitos")
    pasos.append("=" * 60)
    
    if operacion == 'complemento':
        pasos.append(f"Numero original: {numero_a}")
        cb_original = repr_CB(numero_a, base, longitud)
        pasos.append(f"Representacion en CB: {cb_original}")
        
        cb_complementado = opCB_palabra(cb_original, base)
        pasos.append(f"Complemento a la base: {cb_complementado}")
        
        valor_resultado = CB_a_decimal(cb_complementado, base)
        pasos.append(f"Valor decimal del resultado: {valor_resultado}")
        
        if valor_resultado == -numero_a:
            pasos.append("[OK] Resultado correcto: opCB(ReprCB(a)) = ReprCB(-a)")
    
    elif operacion == 'suma':
        cb_a = repr_CB(numero_a, base, longitud)
        cb_b = repr_CB(numero_b, base, longitud)
        
        pasos.append(f"Numero A: {numero_a} -> CB: {cb_a}")
        pasos.append(f"Numero B: {numero_b} -> CB: {cb_b}")
        
        resultado_suma = suma_CB(cb_a, cb_b, base)
        pasos.append(f"Suma en CB: {cb_a} + {cb_b} = {resultado_suma['resultado']}")
        
        if resultado_suma['llevo']:
            pasos.append("  (Con overflow)")
        
        pasos.append(f"Valor decimal del resultado: {resultado_suma['valor_decimal']}")
        pasos.append(f"Esperado: {numero_a} + {numero_b} = {numero_a + numero_b}")
        
        if resultado_suma['valor_decimal'] == numero_a + numero_b:
            pasos.append("[OK] Resultado correcto!")
    
    elif operacion == 'resta':
        cb_a = repr_CB(numero_a, base, longitud)
        cb_b = repr_CB(numero_b, base, longitud)
        
        pasos.append(f"Numero A: {numero_a} -> CB: {cb_a}")
        pasos.append(f"Numero B: {numero_b} -> CB: {cb_b}")
        
        resultado_resta = resta_CB(cb_a, cb_b, base)
        cb_b_neg = opCB_palabra(cb_b, base)
        pasos.append(f"opCB({cb_b}) = {cb_b_neg}  (complemento de B)")
        pasos.append(f"Resta en CB: {cb_a} + {cb_b_neg} = {resultado_resta['resultado']}")
        
        pasos.append(f"Valor decimal del resultado: {resultado_resta['valor_decimal']}")
        pasos.append(f"Esperado: {numero_a} - {numero_b} = {numero_a - numero_b}")
        
        if resultado_resta['valor_decimal'] == numero_a - numero_b:
            pasos.append("[OK] Resultado correcto!")
    
    elif operacion == 'multiplicacion':
        cb_a = repr_CB(numero_a, base, longitud)
        cb_b = repr_CB(numero_b, base, longitud)
        
        pasos.append(f"Numero A: {numero_a} -> CB: {cb_a}")
        pasos.append(f"Numero B: {numero_b} -> CB: {cb_b}")
        
        resultado_mult = multiplicacion_CB(cb_a, cb_b, base)
        pasos.append(f"Multiplicacion exacta: {numero_a} * {numero_b} = {resultado_mult['valor_exacto']}")
        pasos.append(f"Resultado en CB (truncado a {longitud} digitos): {resultado_mult['resultado']}")
        pasos.append(f"Valor decimal del resultado: {resultado_mult['valor_decimal']}")
        
        if resultado_mult['llevo']:
            pasos.append("  (Con overflow - resultado truncado)")
        else:
            pasos.append("[OK] Sin overflow")
    
    return "\n".join(pasos)
