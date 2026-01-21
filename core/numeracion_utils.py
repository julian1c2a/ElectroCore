"""
Utilidades para conversiones numéricas.
Funciones para convertir entre sistemas de numeración usando métodos explícitos.
"""

from typing import Union, Tuple, List


def decimal_a_binario_divisiones(numero: Union[int, str], bits: int = None) -> str:
    """
    Convierte un número decimal a binario usando sucesivas divisiones por 2.
    
    Método: 
        - Dividir el número entre 2
        - Guardar el resto (0 o 1)
        - Continuar con el cociente
        - Repetir hasta cociente = 0
        - Los restos en orden inverso forman el binario
    
    Args:
        numero: Número decimal (int o str). Si es str, se convierte a int.
        bits: (Opcional) Número mínimo de bits para padding con ceros.
    
    Returns:
        String con el binario en formato claro: "10101₂" o "0b10101"
        Si bits se especifica, retorna con ese ancho: "00010101₂"
    
    Raises:
        ValueError: Si el input no es un número válido o es negativo.
    
    Ejemplos:
        >>> decimal_a_binario_divisiones("13")
        '1101₂'
        
        >>> decimal_a_binario_divisiones(255, bits=8)
        '11111111₂'
        
        >>> decimal_a_binario_divisiones(42, bits=8)
        '00101010₂'
    """
    
    # Validar y convertir entrada
    try:
        if isinstance(numero, str):
            numero = int(numero.strip())
        else:
            numero = int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número entero")
    
    if numero < 0:
        raise ValueError(f"El número debe ser no-negativo, recibido: {numero}")
    
    # Caso especial: cero
    if numero == 0:
        resultado = "0"
    else:
        # Método de divisiones sucesivas por 2
        restos: List[str] = []
        dividendo = numero
        
        while dividendo > 0:
            resto = dividendo % 2  # Resto de la división por 2
            restos.append(str(resto))  # Guardar resto
            dividendo = dividendo // 2  # Cociente entero
        
        # Los restos están en orden inverso, así que los invertimos
        resultado = "".join(reversed(restos))
    
    # Padding con ceros si se especifica número de bits
    if bits is not None:
        if len(resultado) > bits:
            raise ValueError(f"El número requiere más de {bits} bits (necesita {len(resultado)})")
        resultado = resultado.zfill(bits)
    
    # Retornar con notación clara de base 2
    return f"{resultado}₂"


def decimal_a_binario_con_pasos(numero: Union[int, str]) -> dict:
    """
    Convierte decimal a binario mostrando todos los pasos de las divisiones.
    
    Útil para fines educativos y demostraciones.
    
    Args:
        numero: Número decimal (int o str)
    
    Returns:
        Dict con:
        - 'numero': Número original
        - 'pasos': Lista de pasos [(dividendo, cociente, resto), ...]
        - 'restos': Lista de restos en orden
        - 'binario': Resultado final con notación "xxxxx₂"
        - 'explicacion': Texto explicativo del proceso
    
    Ejemplos:
        >>> resultado = decimal_a_binario_con_pasos("13")
        >>> print(resultado['explicacion'])
        13 ÷ 2 = 6 resto 1
        6 ÷ 2 = 3 resto 0
        3 ÷ 2 = 1 resto 1
        1 ÷ 2 = 0 resto 1
        
        Leyendo los restos de abajo hacia arriba: 1101₂
    """
    
    # Validar y convertir
    try:
        if isinstance(numero, str):
            numero_int = int(numero.strip())
        else:
            numero_int = int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número entero")
    
    if numero_int < 0:
        raise ValueError(f"El número debe ser no-negativo")
    
    numero_original = numero_int
    pasos = []
    restos = []
    
    if numero_int == 0:
        pasos.append((0, 0, 0))
        restos.append(0)
        binario_resultado = "0₂"
    else:
        dividendo = numero_int
        while dividendo > 0:
            cociente = dividendo // 2
            resto = dividendo % 2
            
            pasos.append((dividendo, cociente, resto))
            restos.append(resto)
            dividendo = cociente
        
        # Invertir restos para obtener el binario
        binario_resultado = "".join(str(r) for r in reversed(restos)) + "₂"
    
    # Construir explicación paso a paso
    explicacion_lineas = []
    for dividendo, cociente, resto in pasos:
        explicacion_lineas.append(f"{dividendo} ÷ 2 = {cociente} resto {resto}")
    
    explicacion_lineas.append("")
    explicacion_lineas.append(f"Leyendo los restos de abajo hacia arriba: {binario_resultado}")
    
    explicacion = "\n".join(explicacion_lineas)
    
    return {
        'numero': numero_original,
        'pasos': pasos,
        'restos': restos,
        'binario': binario_resultado,
        'explicacion': explicacion
    }


def decimal_a_binario_verbose(numero: Union[int, str]) -> str:
    """
    Convierte decimal a binario retornando tanto el resultado como los pasos.
    
    Formato retornado es un string con todos los pasos de forma visual.
    
    Args:
        numero: Número decimal (int o str)
    
    Returns:
        String con explicación completa del proceso de conversión
    
    Ejemplo:
        >>> print(decimal_a_binario_verbose("13"))
        Convertir 13 a binario (sucesivas divisiones por 2):
        
        13 ÷ 2 = 6 resto 1
         6 ÷ 2 = 3 resto 0
         3 ÷ 2 = 1 resto 1
         1 ÷ 2 = 0 resto 1
        
        Resultado: 1101₂
        
        (Leer los restos de abajo hacia arriba)
    """
    resultado = decimal_a_binario_con_pasos(numero)
    
    lineas = [
        f"Convertir {resultado['numero']} a binario (sucesivas divisiones por 2):",
        ""
    ]
    
    # Agregar pasos con indentación visual
    for i, (dividendo, cociente, resto) in enumerate(resultado['pasos']):
        espacios = " " * (1 if dividendo >= 10 else 0)
        lineas.append(f"{espacios}{dividendo} ÷ 2 = {cociente} resto {resto}")
    
    lineas.extend([
        "",
        f"Resultado: {resultado['binario']}",
        "",
        "(Leer los restos de abajo hacia arriba)"
    ])
    
    return "\n".join(lineas)


def validar_numero_decimal(numero: Union[int, str, float]) -> Tuple[bool, str]:
    """
    Valida si un input es un número decimal válido para conversiones.
    
    Args:
        numero: Input a validar
    
    Returns:
        Tupla (es_valido: bool, mensaje: str)
    
    Ejemplos:
        >>> validar_numero_decimal("42")
        (True, "42 es un número decimal válido")
        
        >>> validar_numero_decimal("-5")
        (False, "El número debe ser no-negativo")
    """
    try:
        if isinstance(numero, str):
            num = int(numero.strip())
        else:
            num = int(numero)
        
        if num < 0:
            return False, "El número debe ser no-negativo"
        
        return True, f"{num} es un número decimal válido"
    
    except (ValueError, TypeError):
        return False, f"'{numero}' no es un número decimal válido"


# Funciones adicionales para otras bases
def decimal_a_octal_divisiones(numero: Union[int, str], bits: int = None) -> str:
    """Convierte decimal a octal usando divisiones sucesivas por 8."""
    try:
        num = int(numero) if isinstance(numero, str) else int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número")
    
    if num < 0:
        raise ValueError("El número debe ser no-negativo")
    
    if num == 0:
        resultado = "0"
    else:
        digitos = []
        while num > 0:
            digitos.append(str(num % 8))
            num //= 8
        resultado = "".join(reversed(digitos))
    
    if bits is not None:
        resultado = resultado.zfill(bits)
    
    return f"{resultado}₈"


def decimal_a_hexadecimal_divisiones(numero: Union[int, str], bits: int = None) -> str:
    """Convierte decimal a hexadecimal usando divisiones sucesivas por 16."""
    try:
        num = int(numero) if isinstance(numero, str) else int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número")
    
    if num < 0:
        raise ValueError("El número debe ser no-negativo")
    
    digitos_hex = "0123456789ABCDEF"
    
    if num == 0:
        resultado = "0"
    else:
        digitos = []
        while num > 0:
            digitos.append(digitos_hex[num % 16])
            num //= 16
        resultado = "".join(reversed(digitos))
    
    if bits is not None:
        resultado = resultado.zfill(bits)
    
    return f"{resultado}₁₆"


# ============================================================================
# FUNCIONES GENERALIZADAS PARA CUALQUIER BASE (2-36)
# ============================================================================

def validar_base(base: int) -> bool:
    """
    Valida que una base esté en el rango permitido (2-36).
    
    Bases soportadas:
    - 2-10: Dígitos 0-9
    - 11-36: Dígitos 0-9 + Letras A-Z
    
    Args:
        base: Base numérica a validar
    
    Returns:
        True si la base es válida, False en caso contrario
    """
    return isinstance(base, int) and 2 <= base <= 36


def obtener_digitos_para_base(base: int) -> str:
    """
    Obtiene el conjunto de dígitos válidos para una base.
    
    Para bases 2-10: '0123456789'
    Para bases 11-36: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    Args:
        base: Base numérica (2-36)
    
    Returns:
        String con los dígitos válidos para esa base
    
    Raises:
        ValueError: Si la base no está en rango 2-36
    """
    if not validar_base(base):
        raise ValueError(f"Base debe estar entre 2 y 36, recibido: {base}")
    
    return "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]


def decimal_a_base_b_divisiones(numero: Union[int, str], base: int, bits: int = None) -> str:
    """
    Convierte un número decimal a una base B (2-36) usando divisiones sucesivas.
    
    Método:
        - Dividir el número entre la base
        - Guardar el resto (dígito en la nueva base)
        - Continuar con el cociente
        - Repetir hasta cociente = 0
        - Los restos en orden inverso forman el resultado
    
    Args:
        numero: Número decimal (int o str)
        base: Base destino (2-36)
            - 2: Binario
            - 8: Octal
            - 10: Decimal (sin cambio)
            - 16: Hexadecimal
            - 36: Alphanumeric (máximo soportado)
        bits: (Opcional) Número mínimo de dígitos para padding
    
    Returns:
        String con el número en la base especificada, con subíndice
        Ej: "1A5₁₆", "373₈", "10101₂"
    
    Raises:
        ValueError: Si el input no es válido o base está fuera de rango
    
    Ejemplos:
        >>> decimal_a_base_b_divisiones(173, 2)  # Binario
        '10101101₂'
        
        >>> decimal_a_base_b_divisiones(255, 16)  # Hexadecimal
        'FF₁₆'
        
        >>> decimal_a_base_b_divisiones(100, 36)  # Base 36
        '2S₃₆'
        
        >>> decimal_a_base_b_divisiones(42, 8)  # Octal
        '52₈'
    """
    # Validar base
    if not validar_base(base):
        raise ValueError(f"Base debe estar entre 2 y 36, recibido: {base}")
    
    # Validar y convertir número
    try:
        if isinstance(numero, str):
            num = int(numero.strip())
        else:
            num = int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número entero")
    
    if num < 0:
        raise ValueError(f"El número debe ser no-negativo, recibido: {num}")
    
    # Obtener dígitos permitidos para esta base
    digitos = obtener_digitos_para_base(base)
    
    # Caso especial: cero
    if num == 0:
        resultado = "0"
    else:
        # Algoritmo de divisiones sucesivas
        digitos_resultado = []
        while num > 0:
            resto = num % base  # Dígito en la nueva base
            digitos_resultado.append(digitos[resto])  # Convertir a carácter
            num //= base  # Dividir entre la base
        
        # Los dígitos están en orden inverso
        resultado = "".join(reversed(digitos_resultado))
    
    # Padding si se especifica
    if bits is not None:
        if len(resultado) > bits:
            raise ValueError(f"Resultado requiere más de {bits} dígitos (necesita {len(resultado)})")
        resultado = resultado.zfill(bits)
    
    # Crear subíndice para la base
    # Convertir números de base > 9 a subíndice (ej: 16 → ₁₆)
    base_str = str(base)
    subindices = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
    }
    base_subindice = ''.join(subindices.get(d, d) for d in base_str)
    
    return f"{resultado}{base_subindice}"


def decimal_a_base_b_con_pasos(numero: Union[int, str], base: int) -> dict:
    """
    Convierte decimal a base B mostrando todos los pasos de las divisiones.
    
    Útil para fines educativos y demostraciones.
    
    Args:
        numero: Número decimal (int o str)
        base: Base destino (2-36)
    
    Returns:
        Dict con:
        - 'numero': Número original
        - 'base': Base destino
        - 'pasos': Lista de pasos [(dividendo, cociente, resto_digito), ...]
        - 'digitos': Lista de dígitos en orden inverso
        - 'resultado': Resultado final con notación "xxxxx_base"
        - 'explicacion': Texto explicativo del proceso
    
    Ejemplos:
        >>> resultado = decimal_a_base_b_con_pasos(255, 16)
        >>> print(resultado['resultado'])
        'FF₁₆'
    """
    # Validar base
    if not validar_base(base):
        raise ValueError(f"Base debe estar entre 2 y 36, recibido: {base}")
    
    # Validar y convertir
    try:
        if isinstance(numero, str):
            numero_int = int(numero.strip())
        else:
            numero_int = int(numero)
    except (ValueError, TypeError):
        raise ValueError(f"No se puede convertir '{numero}' a número entero")
    
    if numero_int < 0:
        raise ValueError("El número debe ser no-negativo")
    
    digitos_tabla = obtener_digitos_para_base(base)
    numero_original = numero_int
    pasos = []
    digitos = []
    
    if numero_int == 0:
        pasos.append((0, 0, "0"))
        digitos.append("0")
        base_str = str(base)
        subindices = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        base_subindice = ''.join(subindices.get(d, d) for d in base_str)
        resultado_final = f"0{base_subindice}"
    else:
        dividendo = numero_int
        while dividendo > 0:
            cociente = dividendo // base
            resto = dividendo % base
            digito_char = digitos_tabla[resto]
            
            pasos.append((dividendo, cociente, digito_char))
            digitos.append(digito_char)
            dividendo = cociente
        
        # Invertir dígitos para obtener el resultado
        resultado = "".join(reversed(digitos))
        
        base_str = str(base)
        subindices = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        base_subindice = ''.join(subindices.get(d, d) for d in base_str)
        resultado_final = f"{resultado}{base_subindice}"
    
    # Construir explicación paso a paso
    explicacion_lineas = []
    explicacion_lineas.append(f"Convirtiendo {numero_original} a base {base}:")
    explicacion_lineas.append("")
    
    for dividendo, cociente, digito in pasos:
        explicacion_lineas.append(f"{dividendo} ÷ {base} = {cociente} resto {digito}")
    
    explicacion_lineas.append("")
    explicacion_lineas.append(f"Leyendo los restos de abajo hacia arriba: {resultado_final}")
    
    explicacion = "\n".join(explicacion_lineas)
    
    return {
        'numero': numero_original,
        'base': base,
        'pasos': pasos,
        'digitos': digitos,
        'resultado': resultado_final,
        'explicacion': explicacion
    }


def decimal_a_base_b_verbose(numero: Union[int, str], base: int) -> str:
    """
    Convierte decimal a base B retornando explicación visual completa.
    
    Args:
        numero: Número decimal (int o str)
        base: Base destino (2-36)
    
    Returns:
        String con explicación completa del proceso de conversión
    """
    resultado = decimal_a_base_b_con_pasos(numero, base)
    
    lineas = [
        f"Convertir {resultado['numero']} a base {resultado['base']} (divisiones sucesivas):",
        ""
    ]
    
    # Agregar pasos con indentación visual
    for dividendo, cociente, digito in resultado['pasos']:
        espacios = " " * (len(str(dividendo)) - 2) if dividendo >= 10 else ""
        lineas.append(f"{espacios}{dividendo} ÷ {base} = {cociente} resto {digito}")
    
    lineas.extend([
        "",
        f"Resultado: {resultado['resultado']}",
        "",
        "(Leer los restos de abajo hacia arriba)"
    ])
    
    return "\n".join(lineas)


# ============================================================================
# FUNCIONES PARA CONVERSIÓN INVERSA: BASE B → DECIMAL (CON POLINOMIO Y HORNER)
# ============================================================================

def validar_numero_en_base(numero_str: str, base: int) -> Tuple[bool, str]:
    """
    Valida si un string representa un número válido en una base específica.
    
    Args:
        numero_str: String representando el número en la base
        base: Base numérica (2-36)
    
    Returns:
        Tupla (es_válido: bool, mensaje: str)
    
    Ejemplos:
        >>> validar_numero_en_base("1010", 2)
        (True, "1010 es un número binario válido")
        
        >>> validar_numero_en_base("FF", 16)
        (True, "FF es un número en base 16 válido")
        
        >>> validar_numero_en_base("G", 16)
        (False, "G no es un dígito válido en base 16")
    """
    if not validar_base(base):
        return False, f"Base inválida: {base}"
    
    digitos_validos = obtener_digitos_para_base(base)
    numero_upper = numero_str.strip().upper()
    
    if not numero_upper:
        return False, "El número no puede estar vacío"
    
    for digito in numero_upper:
        if digito not in digitos_validos:
            return False, f"'{digito}' no es un dígito válido en base {base}"
    
    return True, f"{numero_upper} es un número en base {base} válido"


def valor_digito_en_base(digito_char: str, base: int) -> int:
    """
    Obtiene el valor numérico de un dígito en una base específica.
    
    Ejemplos:
        >>> valor_digito_en_base('5', 10)
        5
        
        >>> valor_digito_en_base('F', 16)
        15
        
        >>> valor_digito_en_base('Z', 36)
        35
    """
    digitos_tabla = obtener_digitos_para_base(base)
    digito_upper = digito_char.upper()
    
    if digito_upper not in digitos_tabla:
        raise ValueError(f"'{digito_char}' no es un dígito válido en base {base}")
    
    return digitos_tabla.index(digito_upper)


def base_b_a_decimal_simple(numero_str: str, base: int) -> int:
    """
    Convierte un número de base B a decimal (simple).
    
    Usa el algoritmo directo: suma de (dígito × base^posición)
    
    Args:
        numero_str: String con el número en la base especificada
        base: Base numérica (2-36)
    
    Returns:
        int: Número en base 10
    
    Raises:
        ValueError: Si el número no es válido para la base
    
    Ejemplos:
        >>> base_b_a_decimal_simple("1101", 2)
        13
        
        >>> base_b_a_decimal_simple("FF", 16)
        255
        
        >>> base_b_a_decimal_simple("377", 8)
        255
    """
    # Validar
    es_valido, msg = validar_numero_en_base(numero_str, base)
    if not es_valido:
        raise ValueError(msg)
    
    numero_upper = numero_str.strip().upper()
    resultado = 0
    
    # Calcular: suma de (dígito × base^posición)
    for posicion, digito_char in enumerate(reversed(numero_upper)):
        valor_digito = valor_digito_en_base(digito_char, base)
        potencia = base ** posicion
        resultado += valor_digito * potencia
    
    return resultado


def base_b_a_decimal_con_polinomio(numero_str: str, base: int) -> dict:
    """
    Convierte de base B a decimal mostrando el polinomio de evaluación.
    
    Muestra cómo se calcula el número usando el método estándar:
    d_n × base^n + d_(n-1) × base^(n-1) + ... + d_1 × base^1 + d_0 × base^0
    
    Args:
        numero_str: String con el número en la base especificada
        base: Base numérica (2-36)
    
    Returns:
        Dict con:
        - 'numero_original': El string original
        - 'base': La base usada
        - 'decimal': Resultado en base 10
        - 'polinomio_terminos': Lista de términos del polinomio
        - 'polinomio_str': Representación en string del polinomio
        - 'calculos': Lista de cálculos paso a paso
        - 'explicacion': Texto explicativo completo
    
    Ejemplos:
        >>> resultado = base_b_a_decimal_con_polinomio("1101", 2)
        >>> print(resultado['polinomio_str'])
        1×2³ + 1×2² + 0×2¹ + 1×2⁰
    """
    # Validar
    es_valido, msg = validar_numero_en_base(numero_str, base)
    if not es_valido:
        raise ValueError(msg)
    
    numero_upper = numero_str.strip().upper()
    n_digitos = len(numero_upper)
    
    # Calcular términos del polinomio
    terminos = []
    calculos = []
    total = 0
    
    for posicion, digito_char in enumerate(reversed(numero_upper)):
        valor_digito = valor_digito_en_base(digito_char, base)
        exponente = n_digitos - 1 - posicion
        potencia = base ** exponente
        termino_valor = valor_digito * potencia
        
        terminos.append({
            'digito': digito_char,
            'valor_digito': valor_digito,
            'exponente': exponente,
            'base': base,
            'potencia': potencia,
            'termino_valor': termino_valor
        })
        
        # Crear notación
        calculos.append(f"{valor_digito}×{base}^{exponente} = {termino_valor}")
        total += termino_valor
    
    # Construir polinomio
    polinomio_partes = []
    for termino in terminos:
        polinomio_partes.append(f"{termino['digito']}×{termino['base']}^{termino['exponente']}")
    
    polinomio_str = " + ".join(polinomio_partes)
    
    # Explicación
    explicacion_lineas = [
        f"Convertir {numero_upper} desde base {base} a decimal (Polinomio):",
        "",
        f"Polinomio: {polinomio_str}",
        ""
    ]
    
    for calc in calculos:
        explicacion_lineas.append(f"  {calc}")
    
    explicacion_lineas.extend([
        "",
        f"Resultado: {total}"
    ])
    
    return {
        'numero_original': numero_upper,
        'base': base,
        'decimal': total,
        'polinomio_terminos': terminos,
        'polinomio_str': polinomio_str,
        'calculos': calculos,
        'explicacion': '\n'.join(explicacion_lineas)
    }


def base_b_a_decimal_con_horner(numero_str: str, base: int) -> dict:
    """
    Convierte de base B a decimal usando el método de Horner.
    
    El método de Horner es más eficiente pues transforma:
    d_n × base^n + d_(n-1) × base^(n-1) + ... + d_0 × base^0
    
    En:
    (...((d_n × base + d_(n-1)) × base + d_(n-2)) × ... × base + d_0)
    
    Esto reduce operaciones de potencias a simples multiplicaciones.
    
    Args:
        numero_str: String con el número en la base especificada
        base: Base numérica (2-36)
    
    Returns:
        Dict con:
        - 'numero_original': El string original
        - 'base': La base usada
        - 'decimal': Resultado en base 10
        - 'pasos_horner': Lista de pasos del algoritmo
        - 'forma_horner': Representación con paréntesis anidados
        - 'explicacion': Texto explicativo completo
    
    Ejemplos:
        >>> resultado = base_b_a_decimal_con_horner("1101", 2)
        >>> print(resultado['forma_horner'])
        ((1×2 + 1)×2 + 0)×2 + 1
    """
    # Validar
    es_valido, msg = validar_numero_en_base(numero_str, base)
    if not es_valido:
        raise ValueError(msg)
    
    numero_upper = numero_str.strip().upper()
    
    # Algoritmo de Horner
    pasos = []
    resultado = 0
    
    for i, digito_char in enumerate(numero_upper):
        valor_digito = valor_digito_en_base(digito_char, base)
        
        # Paso: resultado = resultado × base + digito
        resultado_anterior = resultado
        resultado = resultado * base + valor_digito
        
        pasos.append({
            'paso': i + 1,
            'digito': digito_char,
            'valor_digito': valor_digito,
            'base': base,
            'resultado_anterior': resultado_anterior,
            'multiplicacion': resultado_anterior * base,
            'suma': valor_digito,
            'resultado_actual': resultado,
            'formula': f"({resultado_anterior} × {base}) + {valor_digito} = {resultado}"
        })
    
    # Construir forma de Horner (paréntesis anidados)
    forma_horner_partes = []
    for digito_char in numero_upper:
        forma_horner_partes.append(digito_char)
    
    # Construir manualmente la forma de Horner
    if len(numero_upper) == 1:
        forma_horner = numero_upper[0]
    else:
        forma_horner = f"(({numero_upper[0]}"
        for digito in numero_upper[1:]:
            forma_horner += f")×{base} + {digito}"
        forma_horner += ")"
    
    # Explicación
    explicacion_lineas = [
        f"Convertir {numero_upper} desde base {base} a decimal (Horner):",
        "",
        f"Forma de Horner: {forma_horner}",
        "",
        "Pasos del algoritmo (resultado = resultado × base + dígito):",
        ""
    ]
    
    for paso in pasos:
        explicacion_lineas.append(
            f"Paso {paso['paso']}: Dígito {paso['digito']} (valor {paso['valor_digito']})"
        )
        explicacion_lineas.append(
            f"        {paso['resultado_anterior']} × {base} + {paso['valor_digito']} = {paso['resultado_actual']}"
        )
    
    explicacion_lineas.extend([
        "",
        f"Resultado: {resultado}"
    ])
    
    return {
        'numero_original': numero_upper,
        'base': base,
        'decimal': resultado,
        'pasos_horner': pasos,
        'forma_horner': forma_horner,
        'explicacion': '\n'.join(explicacion_lineas)
    }


def comparar_metodos_conversion(numero_str: str, base: int) -> dict:
    """
    Compara los dos métodos de conversión: Polinomio vs Horner.
    
    Muestra ambos métodos lado a lado para demostrar que, aunque
    llegan al mismo resultado, Horner es más eficiente.
    
    Args:
        numero_str: String con el número en la base especificada
        base: Base numérica (2-36)
    
    Returns:
        Dict con:
        - 'polinomio': Dict de resultado polinomio
        - 'horner': Dict de resultado Horner
        - 'comparacion': Análisis comparativo
        - 'explicacion': Texto comparativo
    """
    resultado_polinomio = base_b_a_decimal_con_polinomio(numero_str, base)
    resultado_horner = base_b_a_decimal_con_horner(numero_str, base)
    
    # Contar operaciones
    n = len(numero_str)
    
    # Polinomio: (n-1) multiplicaciones (para potencias) + n multiplicaciones
    # Realmente: n exponenciaciones + n multiplicaciones
    ops_polinomio = {
        'multiplicaciones': n,
        'exponenciaciones': n,
        'sumas': n - 1,
        'total_operaciones_significativas': n + (n - 1)
    }
    
    # Horner: n-1 multiplicaciones + n sumas
    ops_horner = {
        'multiplicaciones': n - 1,
        'exponenciaciones': 0,
        'sumas': n,
        'total_operaciones_significativas': (n - 1) + n
    }
    
    # Explicación
    explicacion = f"""
COMPARACIÓN DE MÉTODOS
═══════════════════════════════════════════════════════════

Número: {numero_str} (Base {base})
Resultado decimal: {resultado_polinomio['decimal']}

MÉTODO 1: POLINOMIO (Forma Estándar)
──────────────────────────────────────
{resultado_polinomio['polinomio_str']}

Operaciones:
  • Multiplicaciones: {ops_polinomio['multiplicaciones']}
  • Exponenciaciones: {ops_polinomio['exponenciaciones']}
  • Sumas: {ops_polinomio['sumas']}
  • Total significativo: {ops_polinomio['total_operaciones_significativas']}

MÉTODO 2: HORNER (Más Eficiente)
─────────────────────────────────
{resultado_horner['forma_horner']}

Operaciones:
  • Multiplicaciones: {ops_horner['multiplicaciones']}
  • Exponenciaciones: {ops_horner['exponenciaciones']}
  • Sumas: {ops_horner['sumas']}
  • Total significativo: {ops_horner['total_operaciones_significativas']}

CONCLUSIÓN
──────────
Polinomio requiere {ops_polinomio['exponenciaciones']} exponenciaciones.
Horner requiere 0 exponenciaciones.

¡Horner es más eficiente porque evita calcular potencias!
Especialmente importante con números muy grandes o bases inusuales.
"""
    
    return {
        'polinomio': resultado_polinomio,
        'horner': resultado_horner,
        'operaciones_polinomio': ops_polinomio,
        'operaciones_horner': ops_horner,
        'explicacion': explicacion.strip()
    }
