"""
Sistemas de Numeracion: Posicionales vs No Posicionales

Este modulo explora diferentes sistemas de numeracion y sus caracteristicas:

1. Sistemas no posicionales: Números Romanos
2. Sistemas posicionales por potencias: Base 5 (ejemplo)
3. Sistemas posicionales con bases variables: Notacion de tiempo
4. Conversiones entre ellos
"""

from typing import Dict, Tuple, List, Union, Callable, Any
from enum import Enum


# ============================================================================
# PARTE 0: CLASES BASE - ALFABETO Y LENGUAJE
# ============================================================================

class Alphabet:
    """
    Representa un alfabeto: conjunto ordenado y finito de símbolos.
    
    Un alfabeto es la base para construir palabras. Puede estar formado por:
    - Caracteres (strings): {'0', '1'}, {'a', 'b', 'c'}, etc.
    - Enteros: {0, 1, 2, 3, ...}
    - Booleanos: {False, True}
    - Enums personalizados
    
    Propiedades:
    - Finito y ordenado
    - Cada símbolo es único
    - El tamaño define la "base" para sistemas posicionales
    
    Convención de índices:
    - MSB (Most Significant Bit): índice n-1 (posición más a la izquierda)
    - LSB (Least Significant Bit): índice 0 (posición más a la derecha)
    
    Ejemplo:
        alphabet_binary = Alphabet(['0', '1'])
        alphabet_ternary = Alphabet([0, 1, 2])
    """
    
    def __init__(self, symbols: Union[List[str], List[int], List[bool]]):
        """
        Inicializa un alfabeto con símbolos dados.
        
        Args:
            symbols: Lista de símbolos (deben ser únicos y ordenados)
            
        Raises:
            ValueError: Si hay símbolos duplicados
        """
        if len(symbols) != len(set(symbols)):
            raise ValueError("El alfabeto contiene símbolos duplicados")
        
        self.symbols = list(symbols)  # Mantener orden
        self._symbol_to_index = {sym: idx for idx, sym in enumerate(self.symbols)}
    
    @property
    def size(self) -> int:
        """Retorna el tamaño del alfabeto (cardinalidad)."""
        return len(self.symbols)
    
    @property
    def base(self) -> int:
        """Alias para size, útil en contextos posicionales."""
        return self.size
    
    def __len__(self) -> int:
        return self.size
    
    def __getitem__(self, index: int) -> Any:
        """Accede a un símbolo por su índice."""
        return self.symbols[index]
    
    def __contains__(self, symbol: Any) -> bool:
        """Verifica si un símbolo está en el alfabeto."""
        return symbol in self._symbol_to_index
    
    def index_of(self, symbol: Any) -> int:
        """
        Retorna el índice de un símbolo en el alfabeto.
        
        Args:
            symbol: Símbolo a buscar
            
        Returns:
            int: Índice del símbolo
            
        Raises:
            ValueError: Si el símbolo no está en el alfabeto
        """
        if symbol not in self._symbol_to_index:
            raise ValueError(f"El símbolo '{symbol}' no está en el alfabeto")
        return self._symbol_to_index[symbol]
    
    def __iter__(self):
        """Itera sobre los símbolos del alfabeto."""
        return iter(self.symbols)
    
    def __repr__(self) -> str:
        return f"Alphabet{self.symbols}"


class FixedLengthLanguage:
    """
    Representa un lenguaje formal de longitud fija.
    
    Un lenguaje es un conjunto de palabras válidas construidas sobre un alfabeto,
    todas de la misma longitud, determinado por:
    1. Un alfabeto (Alphabet): símbolos disponibles
    2. Longitud: número de posiciones en cada palabra
    3. Predicado: función que verifica validez
    4. Siguiente: función que genera la siguiente palabra
    
    Convención de índices:
    - MSB (Most Significant Bit): índice n-1 (el más significativo)
    - LSB (Least Significant Bit): índice 0 (el menos significativo)
    
    En una palabra de longitud n:
    - palabra[n-1] es el MSB (posición más significativa)
    - palabra[0] es el LSB (posición menos significativa)
    
    Ejemplo:
        # Lenguaje binario de 4 bits
        alphabet = Alphabet(['0', '1'])
        language = FixedLengthLanguage(
            alphabet=alphabet,
            length=4,
            predicate=lambda p: True,  # Todas las palabras válidas
            zero_element='0000',
            next_function=lambda p: next_binary(p)
        )
    """
    
    def __init__(self, 
                 alphabet: Alphabet,
                 length: int,
                 predicate: Callable[[str], bool],
                 zero_element: Any = None,
                 next_function: Callable[[str], str] = None,
                 name: str = ''):
        """
        Inicializa un lenguaje.
        
        Args:
            alphabet: Objeto Alphabet que define los símbolos disponibles
            length: Longitud de cada palabra (n)
            predicate: Función que retorna True si palabra está en lenguaje
            zero_element: Símbolo/palabra de "inicio" (generalmente la más pequeña)
            next_function: Función que genera la siguiente palabra en el lenguaje
            name: Nombre descriptivo del lenguaje
            
        Raises:
            ValueError: Si length < 1
        """
        if length < 1:
            raise ValueError("La longitud debe ser al menos 1")
        
        self.alphabet = alphabet
        self.length = length
        self.predicate = predicate
        self.zero_element = zero_element
        self.next_function = next_function
        self.name = name
        
        # Cache de palabras (para lenguajes pequeños)
        self._words_cache = None
    
    def is_valid(self, word: str) -> bool:
        """
        Verifica si una palabra pertenece al lenguaje.
        
        Args:
            word: Palabra (string de símbolos)
            
        Returns:
            bool: True si la palabra es válida
            
        Raises:
            ValueError: Si la longitud no coincide
        """
        if len(word) != self.length:
            raise ValueError(
                f"Palabra '{word}' tiene longitud {len(word)}, "
                f"se esperaba {self.length}"
            )
        
        # Verificar que todos los caracteres están en el alfabeto
        if not all(c in self.alphabet for c in word):
            return False
        
        # Aplicar el predicado
        return self.predicate(word)
    
    def next_word(self, word: str) -> str:
        """
        Calcula la siguiente palabra en el lenguaje.
        
        Args:
            word: Palabra actual (debe ser válida)
            
        Returns:
            str: Siguiente palabra válida (con wrap-around al inicio)
            
        Raises:
            ValueError: Si la palabra no es válida o next_function no está definida
        """
        if not self.is_valid(word):
            raise ValueError(f"La palabra '{word}' no es válida en este lenguaje")
        
        if self.next_function is None:
            raise ValueError("La función 'next_function' no está definida")
        
        return self.next_function(word)
    
    def hamming_distance(self, word_a: str, word_b: str) -> int:
        """
        Calcula la distancia Hamming entre dos palabras.
        
        Args:
            word_a: Primera palabra (debe ser válida)
            word_b: Segunda palabra (debe ser válida)
            
        Returns:
            int: Distancia Hamming (número de posiciones diferentes)
            
        Raises:
            ValueError: Si alguna palabra no es válida
        """
        if not self.is_valid(word_a):
            raise ValueError(f"Palabra '{word_a}' no es válida")
        if not self.is_valid(word_b):
            raise ValueError(f"Palabra '{word_b}' no es válida")
        
        return distancia_hamming(word_a, word_b)
    
    def are_adjacent(self, word_a: str, word_b: str) -> bool:
        """
        Verifica si dos palabras son adyacentes (distancia Hamming = 1).
        
        Args:
            word_a: Primera palabra
            word_b: Segunda palabra
            
        Returns:
            bool: True si hamming_distance = 1
        """
        return self.hamming_distance(word_a, word_b) == 1
    
    def generate_all_words(self) -> List[str]:
        """
        Genera todas las palabras válidas del lenguaje.
        
        Para lenguajes pequeños, cachea el resultado.
        Para lenguajes grandes, advierte sobre complejidad.
        
        Returns:
            List[str]: Lista de todas las palabras válidas
        """
        if self._words_cache is not None:
            return self._words_cache
        
        # Generar todas las palabras posibles
        if self.alphabet.size ** self.length > 10000:
            print(f"⚠️  Lenguaje grande: {self.alphabet.size}^{self.length} palabras posibles")
        
        # Recursiva: generar todas las palabras de longitud n
        def generate_recursive(length_remaining):
            if length_remaining == 0:
                return ['']
            
            shorter = generate_recursive(length_remaining - 1)
            result = []
            for symbol in self.alphabet:
                for word in shorter:
                    candidate = str(symbol) + word
                    if self.is_valid(candidate):
                        result.append(candidate)
            return result
        
        words = generate_recursive(self.length)
        
        # Cache para lenguajes pequeños
        if len(words) <= 10000:
            self._words_cache = words
        
        return words
    
    def analyze_adjacency(self) -> Dict[str, Any]:
        """
        Analiza propiedades de adyacencia y ciclicidad del lenguaje.
        
        Returns:
            Dict con:
            - total_words: número de palabras válidas
            - is_adjacent: ¿todas las palabras sucesivas son adyacentes?
            - is_cyclic: ¿la última palabra es adyacente a la primera?
            - adjacency_graph: {palabra: palabras_adyacentes}
        """
        words = self.generate_all_words()
        
        if not words:
            return {'total_words': 0, 'error': 'Lenguaje vacío'}
        
        adjacency_graph = {}
        is_adjacent_all = True
        
        for i, word in enumerate(words):
            adjacents = []
            for j, other in enumerate(words):
                if i != j and self.are_adjacent(word, other):
                    adjacents.append(other)
            adjacency_graph[word] = adjacents
            
            # Check if successive words are adjacent
            next_word = words[(i + 1) % len(words)]
            if not self.are_adjacent(word, next_word):
                is_adjacent_all = False
        
        # Check ciclicity
        first = words[0]
        last = words[-1]
        is_cyclic = self.are_adjacent(last, first)
        
        return {
            'total_words': len(words),
            'is_adjacent': is_adjacent_all,
            'is_cyclic': is_cyclic,
            'adjacency_graph': adjacency_graph,
            'words': words
        }
    
    def __repr__(self) -> str:
        return f"FixedLengthLanguage({self.name}, |Σ|={self.alphabet.size}, n={self.length})"
    
    # ========================================================================
    # BACKWARD COMPATIBILITY METHODS (Spanish names from old Lenguaje class)
    # ========================================================================
    
    def es_valida(self, palabra: str) -> bool:
        """Alias para is_valid (compatibilidad hacia atrás)"""
        return self.is_valid(palabra)
    
    def siguiente_palabra(self, palabra: str) -> str:
        """Alias para next_word (compatibilidad hacia atrás)"""
        return self.next_word(palabra)
    
    def distancia_hamming(self, palabra_a: str, palabra_b: str) -> int:
        """Alias para hamming_distance (compatibilidad hacia atrás)"""
        return self.hamming_distance(palabra_a, palabra_b)
    
    def son_adyacentes(self, palabra_a: str, palabra_b: str) -> bool:
        """Alias para are_adjacent (compatibilidad hacia atrás)"""
        return self.are_adjacent(palabra_a, palabra_b)
    
    def generar_todas_palabras(self) -> List[str]:
        """Alias para generate_all_words (compatibilidad hacia atrás)"""
        return self.generate_all_words()
    
    def analizar_adyacencia(self) -> Dict:
        """Alias para analyze_adjacency (compatibilidad hacia atrás)"""
        return self.analyze_adjacency()
    
    # Aliases de propiedades
    @property
    def alfabeto(self) -> List:
        """Acceso compatible con código antiguo: lista de símbolos del alfabeto"""
        return self.alphabet.symbols
    
    @property
    def longitud(self) -> int:
        """Acceso compatible con código antiguo: longitud de palabras"""
        return self.length
    
    @property
    def predicado(self):
        """Acceso compatible con código antiguo: función de predicado"""
        return self.predicate
    
    @property
    def valor_cero(self):
        """Acceso compatible con código antiguo: elemento cero"""
        return self.zero_element
    
    @property
    def siguiente(self):
        """Acceso compatible con código antiguo: función siguiente"""
        return self.next_function
    
    @property
    def nombre(self) -> str:
        """Acceso compatible con código antiguo: nombre del lenguaje"""
        return self.name


# Alias para backward compatibility
Lenguaje = FixedLengthLanguage


# ============================================================================
# PARTE 1: SISTEMA POSICIONAL NO NUMÉRICO (Números Romanos)
# ============================================================================

NUMEROS_ROMANOS_VALORES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
    'IV': 4,
    'IX': 9,
    'XL': 40,
    'XC': 90,
    'CD': 400,
    'CM': 900,
}

VALORES_ROMANOS_INVERSO = {
    1000: 'M',
    900: 'CM',
    500: 'D',
    400: 'CD',
    100: 'C',
    90: 'XC',
    50: 'L',
    40: 'XL',
    10: 'X',
    9: 'IX',
    5: 'V',
    4: 'IV',
    1: 'I',
}


def decimal_a_romano(numero: int) -> str:
    """
    Convierte un número decimal a números romanos.
    
    El sistema romano es NO POSICIONAL:
    - El valor no depende de la posicion, sino del simbolo
    - Cada simbolo tiene un valor fijo
    - Se puede escribir de múltiples formas (aunque la moderna respeta reglas)
    
    Ejemplo: 1994 = MCMXCIV
      M (1000) + CM (900) + XC (90) + IV (4) = 1994
    """
    resultado = ""
    
    for valor, simbolo in VALORES_ROMANOS_INVERSO.items():
        mientras_cantidad = numero // valor
        if mientras_cantidad:
            resultado += simbolo * mientras_cantidad
            numero -= valor * mientras_cantidad
    
    return resultado


def romano_a_decimal(romano_str: str) -> int:
    """
    Convierte números romanos a decimal.
    
    El sistema romano permite solo UNA representacion correcta para cada número
    (con las reglas modernas), pero historicamente habia variaciones.
    
    Reglas:
    - Los simbolos se suman de izquierda a derecha
    - I, X, C, M pueden aparecer hasta 3 veces seguidas
    - V, L, D aparecen como maximo una vez
    - Para restar: I antes de V o X, X antes de L o C, C antes de D o M
    """
    romano_str = romano_str.upper()
    
    # Reemplazar subtracciones por sus valores
    subtracciones = [
        ('IV', 'IIII'),
        ('IX', 'VIIII'),
        ('XL', 'XXXX'),
        ('XC', 'LXXXX'),
        ('CD', 'CCCC'),
        ('CM', 'DCCCC'),
    ]
    
    for resta, suma_equivalente in subtracciones:
        if resta in romano_str:
            romano_str = romano_str.replace(resta, suma_equivalente)
    
    resultado = 0
    for simbolo in romano_str:
        if simbolo in NUMEROS_ROMANOS_VALORES:
            resultado += NUMEROS_ROMANOS_VALORES[simbolo]
    
    return resultado


def explicar_romano(numero: int) -> Dict:
    """
    Explica la conversion de decimal a romano paso a paso.
    """
    romano = decimal_a_romano(numero)
    
    # Desglosar
    desglose = []
    numero_temp = numero
    
    for valor, simbolo in VALORES_ROMANOS_INVERSO.items():
        mientras_cantidad = numero_temp // valor
        if mientras_cantidad:
            desglose.append({
                'valor': valor,
                'simbolo': simbolo,
                'cantidad': mientras_cantidad,
                'representacion': simbolo * mientras_cantidad,
                'resta': valor * mientras_cantidad
            })
            numero_temp -= valor * mientras_cantidad
    
    return {
        'numero_decimal': numero,
        'romano': romano,
        'desglose': desglose,
        'explicacion': f"{numero} en romano = {' + '.join([d['representacion'] for d in desglose])}"
    }


# ============================================================================
# PARTE 2: SISTEMAS POSICIONALES POR POTENCIAS (Base 5)
# ============================================================================

def decimal_a_base_5(numero: int) -> str:
    """
    Convierte decimal a base 5.
    
    Sistema POSICIONAL: El valor de cada digito depende de su posicion.
    Posicion 0 = 5^0 = 1
    Posicion 1 = 5^1 = 5
    Posicion 2 = 5^2 = 25
    etc.
    
    Ejemplo: 1994 en decimal
    1994 / 5 = 398 resto 4
    398 / 5 = 79 resto 3
    79 / 5 = 15 resto 4
    15 / 5 = 3 resto 0
    3 / 5 = 0 resto 3
    
    Resultado: 30434_5 (leyendo los restos de abajo a arriba)
    Verificacion: 3*5^4 + 0*5^3 + 4*5^2 + 3*5^1 + 4*5^0 = 1875 + 0 + 100 + 15 + 4 = 1994
    """
    if numero == 0:
        return "0"
    
    digitos = []
    while numero > 0:
        digitos.append(str(numero % 5))
        numero //= 5
    
    return ''.join(digitos[::-1])


def base_5_a_decimal(base_5_str: str) -> int:
    """
    Convierte base 5 a decimal.
    
    El valor se calcula como:
    Número = d_n*5^n + d_(n-1)*5^(n-1) + ... + d_0*5^0
    """
    resultado = 0
    for i, digito in enumerate(reversed(base_5_str)):
        resultado += int(digito) * (5 ** i)
    
    return resultado


def explicar_base_5(numero: int) -> Dict:
    """
    Explica la conversion de decimal a base 5 paso a paso.
    """
    base_5 = decimal_a_base_5(numero)
    
    # Desglose por divisiones
    divisiones = []
    temp = numero
    while temp > 0:
        dividendo = temp
        divisor = 5
        cociente = temp // 5
        resto = temp % 5
        divisiones.append({
            'dividendo': dividendo,
            'divisor': divisor,
            'cociente': cociente,
            'resto': resto
        })
        temp = cociente
    
    # Desglose por potencias (de vuelta)
    potencias = []
    for i, digito in enumerate(reversed(base_5)):
        valor_posicion = 5 ** i
        valor_digito = int(digito)
        aporte = valor_digito * valor_posicion
        potencias.append({
            'posicion': i,
            'digito': digito,
            'potencia': valor_posicion,
            'calculo': f"{digito}*5^{i}",
            'valor': aporte
        })
    
    return {
        'número_decimal': numero,
        'base_5': base_5,
        'divisiones': divisiones,
        'potencias': potencias,
        'suma_final': sum(p['valor'] for p in potencias),
        'explicacion': f"{numero}_1_0 = {base_5}_5"
    }


# ============================================================================
# PARTE 3: SISTEMA POSICIONAL CON BASES VARIABLES (Notacion de Tiempo)
# ============================================================================

def decimal_a_tiempo(segundos_totales: int) -> str:
    """
    Convierte segundos a formato HH:MM:SS.
    
    Este es un sistema POSICIONAL pero CON BASES VARIABLES:
    - Base 24 para horas (max 23)
    - Base 60 para minutos (max 59)
    - Base 60 para segundos (max 59)
    
    NO es una base única, sino un sistema posicional MIXTO.
    
    Ejemplo: 3661 segundos
    3661 / 60 = 61 minutos, 1 segundo
    61 / 60 = 1 hora, 1 minuto
    
    Resultado: 01:01:01 (1 hora, 1 minuto, 1 segundo)
    """
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60
    
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def tiempo_a_decimal(tiempo_str: str) -> int:
    """
    Convierte HH:MM:SS a segundos.
    """
    partes = tiempo_str.split(':')
    if len(partes) != 3:
        raise ValueError("Formato debe ser HH:MM:SS")
    
    horas, minutos, segundos = map(int, partes)
    return horas * 3600 + minutos * 60 + segundos


def explicar_tiempo(segundos_totales: int) -> Dict:
    """
    Explica la conversion de segundos a tiempo paso a paso.
    """
    tiempo = decimal_a_tiempo(segundos_totales)
    
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60
    
    return {
        'segundos_totales': segundos_totales,
        'tiempo': tiempo,
        'desglose': {
            'horas': horas,
            'minutos': minutos,
            'segundos': segundos,
        },
        'calculo': f"{horas}*3600 + {minutos}*60 + {segundos} = {segundos_totales}",
        'explicacion': f"Sistema POSICIONAL con bases variables (24, 60, 60)"
    }


# ============================================================================
# PARTE 4: COMPARACIÓN Y EJEMPLOS
# ============================================================================

def comparar_sistemas(numero: int) -> Dict:
    """
    Muestra la representacion del mismo número en diferentes sistemas.
    """
    return {
        'número_decimal': numero,
        'sistemas': {
            'romano': {
                'representacion': decimal_a_romano(numero),
                'tipo': 'No Posicional',
                'descripcion': 'Cada simbolo tiene valor fijo'
            },
            'base_5': {
                'representacion': decimal_a_base_5(numero),
                'tipo': 'Posicional (potencias de 5)',
                'descripcion': 'Valor depende de posicion'
            },
            'base_10': {
                'representacion': str(numero),
                'tipo': 'Posicional (potencias de 10)',
                'descripcion': 'Sistema decimal moderno'
            }
        }
    }


def demostrar_unicidad() -> Dict:
    """
    Demuestra que cada sistema tiene representacion ÚNICA.
    
    Sistemas posicionales: Para cada número natural, existe UNA única
    representacion en una base dada (sin ceros a la izquierda).
    
    Sistema romano (moderno): Tambien existe una única representacion
    según las reglas de notacion.
    """
    números = [4, 9, 27, 99, 1994]
    
    ejemplos = []
    for num in números:
        rom = decimal_a_romano(num)
        b5 = decimal_a_base_5(num)
        b10 = str(num)
        
        # Verificar conversiones inversas
        rom_inverso = romano_a_decimal(rom)
        b5_inverso = base_5_a_decimal(b5)
        
        ejemplos.append({
            'número': num,
            'romano': rom,
            'base_5': b5,
            'base_10': b10,
            'verificacion': {
                'romano_inverso': rom_inverso == num,
                'base_5_inverso': b5_inverso == num
            }
        })
    
    return {
        'titulo': 'Unicidad de Representacion',
        'descripcion': 'Cada sistema posicional tiene UNA única representacion para cada número',
        'ejemplos': ejemplos,
        'conclusion': 'Todas las conversiones inversas son correctas: cada número tiene una única representacion en cada sistema'
    }


# ============================================================================
# PARTE 5: REPRESENTACIÓN EN LONGITUD FIJA (2.1.1.6)
# ============================================================================

def capacidad_representacion(base: int, longitud: int) -> int:
    """
    Calcula la capacidad de representación (2.1.1.6.1.1).
    
    La capacidad es el número total de valores diferentes que se pueden
    representar en una base dada con una longitud fija.
    
    Fórmula: capacidad(B, n) = B^n
    
    Args:
        base: Base del sistema de numeración (B)
        longitud: Número de dígitos disponibles (n)
    
    Returns:
        int: B^n = número de valores representables
        
    Ejemplos:
        capacidad_representacion(2, 3) = 8   (00 a 111 en binario)
        capacidad_representacion(2, 8) = 256 (00000000 a 11111111)
        capacidad_representacion(10, 3) = 1000 (000 a 999)
        capacidad_representacion(16, 2) = 256 (00 a FF)
    """
    return base ** longitud


def rango_representacion(base: int, longitud: int) -> Tuple[int, int]:
    """
    Calcula el rango de valores representables (2.1.1.6.1.2).
    
    Para una base B y longitud l, el rango es [0, B^l - 1] (cerrado).
    
    Args:
        base: Base del sistema de numeración (B)
        longitud: Número de dígitos disponibles (l)
    
    Returns:
        Tuple[int, int]: (mínimo, máximo) = (0, B^l - 1)
        
    Ejemplos:
        rango_representacion(2, 3) = (0, 7)
        rango_representacion(2, 8) = (0, 255)
        rango_representacion(10, 2) = (0, 99)
        rango_representacion(16, 2) = (0, 255)
    """
    capacidad = base ** longitud
    return (0, capacidad - 1)


def longitud_representacion(numero: int, base: int) -> int:
    """
    Calcula la longitud mínima de representación (2.1.1.6.1.2).
    
    Devuelve el mínimo número de dígitos necesarios para representar
    un número en una base dada.
    
    Fórmula: longitud(x, B) = ⌊log_B(x)⌋ + 1
    
    Esto es el logaritmo entero en base B + 1.
    
    Args:
        numero: Número a representar (x)
        base: Base del sistema de numeración (B)
    
    Returns:
        int: Número mínimo de dígitos necesarios
        
    Raises:
        ValueError: Si numero < 1 o base < 2
        
    Ejemplos:
        longitud_representacion(27, 10) = 2  (27 requiere 2 dígitos)
        longitud_representacion(255, 2) = 8  (255 = 11111111₂)
        longitud_representacion(1994, 5) = 5 (1994 = 30434₅)
        longitud_representacion(9, 10) = 1   (9 requiere 1 dígito)
    """
    import math
    
    if numero < 1:
        raise ValueError("El número debe ser positivo (≥ 1)")
    if base < 2:
        raise ValueError("La base debe ser ≥ 2")
    
    if numero == 0:
        return 1
    
    # ⌊log_B(x)⌋ + 1
    return math.floor(math.log(numero, base)) + 1


def analisis_representacion(numero: int, base: int, longitud: int = None) -> Dict:
    """
    Análisis completo de capacidad y rango de representación.
    
    Combina: capacidad(B, n), rango(B, n), y longitud(x, B).
    
    Args:
        numero: Número a analizar
        base: Base del sistema
        longitud: Longitud fija (opcional, si None se calcula automáticamente)
    
    Returns:
        Dict con análisis completo
    """
    if longitud is None:
        longitud = longitud_representacion(numero, base)
    
    capacidad = capacidad_representacion(base, longitud)
    rango_min, rango_max = rango_representacion(base, longitud)
    longitud_min = longitud_representacion(numero, base)
    
    está_en_rango = rango_min <= numero <= rango_max
    
    return {
        'número': numero,
        'base': base,
        'longitud_fija': longitud,
        'longitud_mínima': longitud_min,
        'capacidad': capacidad,
        'rango': f'[{rango_min}, {rango_max}]',
        'rango_min': rango_min,
        'rango_max': rango_max,
        'en_rango': está_en_rango,
        'fórmula_capacidad': f'{base}^{longitud} = {capacidad}',
        'fórmula_rango_máximo': f'{base}^{longitud} - 1 = {rango_max}'
    }


# ============================================================================
# EJEMPLOS Y EDUCACIÓN
# ============================================================================

# ============================================================================
# PARTE 6: CONVERSIONES GENÉRICAS ENTRE BASES
# ============================================================================

def decimal_a_base_B(numero: int, base: int) -> str:
    """
    Convierte un número decimal a cualquier base B (2-36).
    
    Algoritmo: Divisiones sucesivas
    - Dividir numero entre base, guardar el resto
    - El resto es un dígito en base B
    - Repetir con el cociente hasta que sea 0
    
    Parámetros:
        numero: Número decimal a convertir (>= 0)
        base: Base destino (2-36)
        
    Retorna:
        String con la representación en base B
        Usa dígitos 0-9 y letras A-Z para bases > 10
        
    Ejemplos:
        decimal_a_base_B(1994, 5) → "30434"
        decimal_a_base_B(255, 2) → "11111111"
        decimal_a_base_B(255, 16) → "ff"
        
    Referencias: 2.1.1.3 (Conversión de Base 10 a Base B)
    """
    if numero == 0:
        return "0"
    
    if not (2 <= base <= 36):
        raise ValueError("Base debe estar entre 2 y 36")
    
    digitos = "0123456789abcdefghijklmnopqrstuvwxyz"
    resultado = []
    
    while numero > 0:
        resultado.append(digitos[numero % base])
        numero //= base
    
    return ''.join(reversed(resultado))


def base_B_a_decimal(numero_str: str, base: int) -> int:
    """
    Convierte un número en base B a decimal.
    
    Algoritmo: Evaluación del polinomio
    Número_B = d_n * B^n + d_(n-1) * B^(n-1) + ... + d_0 * B^0
    
    Parámetros:
        numero_str: String con la representación en base B
        base: Base origen (2-36)
        
    Retorna:
        Número en decimal (base 10)
        
    Ejemplos:
        base_B_a_decimal("30434", 5) → 1994
        base_B_a_decimal("11111111", 2) → 255
        base_B_a_decimal("ff", 16) → 255
        
    Referencias: 2.1.1.3 (Conversión de Base B a Base 10)
    """
    if not (2 <= base <= 36):
        raise ValueError("Base debe estar entre 2 y 36")
    
    digitos = "0123456789abcdefghijklmnopqrstuvwxyz"
    numero_str = numero_str.lower()
    resultado = 0
    
    for i, digito in enumerate(reversed(numero_str)):
        if digito not in digitos[:base]:
            raise ValueError(f"Dígito '{digito}' inválido para base {base}")
        resultado += digitos.index(digito) * (base ** i)
    
    return resultado


def base_B_a_base_B_prima(numero_str: str, base_origen: int, base_destino: int) -> str:
    """
    Conversión genérica entre dos bases B y B' (2-36).
    
    Método: Conversión a través de decimal
    1. Convertir de base B a decimal
    2. Convertir de decimal a base B'
    
    Parámetros:
        numero_str: Número en base B
        base_origen: Base B (2-36)
        base_destino: Base B' (2-36)
        
    Retorna:
        String con la representación en base B'
        
    Ejemplos:
        base_B_a_base_B_prima("30434", 5, 2) → "11111001010"
        base_B_a_base_B_prima("ff", 16, 10) → "255"
        base_B_a_base_B_prima("1010", 2, 8) → "12"
        
    Referencias: 2.1.1.3 (Conversión entre Sistemas de Numeración)
    """
    decimal = base_B_a_decimal(numero_str, base_origen)
    return decimal_a_base_B(decimal, base_destino)


def base_B_a_base_B_prima_potencias(numero_str: str, base_comun: int, 
                                    exponente_origen: int, 
                                    exponente_destino: int) -> str:
    """
    Conversión eficiente entre bases relacionadas B = b^n y B' = b^(n').
    
    Cuando la base origen B = b^n y la base destino B' = b^(n'),
    se puede convertir de manera más eficiente agrupando dígitos en la base común b.
    
    Método:
    1. Convertir B → b (agrupando/expandiendo n dígitos de base B)
    2. Convertir b → B' (agrupando n' dígitos de base b)
    
    Parámetros:
        numero_str: Número en base B (donde B = base_comun^exponente_origen)
        base_comun: Base b (2, 3, 5, etc.)
        exponente_origen: n tal que B = b^n
        exponente_destino: n' tal que B' = b^(n')
        
    Retorna:
        String con la representación en base B' (donde B' = b^(n'))
        
    Ejemplos:
        # Convertir binario (2^1) a hexadecimal (2^4)
        base_B_a_base_B_prima_potencias("11111111", 2, 1, 4) → "ff"
        
        # Convertir hexadecimal (2^4) a binario (2^1)
        base_B_a_base_B_prima_potencias("ff", 2, 4, 1) → "11111111"
        
        # Convertir binario (2^1) a octal (2^3)
        base_B_a_base_B_prima_potencias("1111", 2, 1, 3) → "17"
        
        # Convertir base 3 (3^1) a base 27 (3^3)
        base_B_a_base_B_prima_potencias("010021002", 3, 1, 3) → "122"
        
    Referencias: 2.1.1.5.4 (Sistema de conversión entre representación de bases relacionadas)
    
    Notas:
        - Si exponente_origen > exponente_destino: expandir dígitos y reagrupar
        - Si exponente_origen < exponente_destino: agrupar exponente_destino dígitos
        - Mucho más eficiente que pasar por decimal para bases grandes
    """
    if exponente_origen == exponente_destino:
        return numero_str
    
    # Primero: Convertir a base b (expandir exponente_origen dígitos en exponente_origen*log(base) dígitos)
    digitos_base_comun = []
    for digito_char in numero_str:
        # Convertir cada dígito de base B a su valor en base b
        digito_valor = int(digito_char, base_comun ** exponente_origen)
        
        # Expandir a exponente_origen dígitos en base b
        for _ in range(exponente_origen):
            digitos_base_comun.append(digito_valor % base_comun)
            digito_valor //= base_comun
        digitos_base_comun.reverse()
    
    # Segundo: Convertir de base b a base B' (agrupar exponente_destino dígitos)
    digitos_base_comun.reverse()  # Para procesar de derecha a izquierda
    resultado_digitos = []
    
    while digitos_base_comun:
        # Tomar exponente_destino dígitos de base b
        grupo = []
        for _ in range(exponente_destino):
            if digitos_base_comun:
                grupo.append(digitos_base_comun.pop())
        
        # Convertir grupo de base b a un dígito de base B'
        valor_digito = 0
        for digito in reversed(grupo):
            valor_digito = valor_digito * base_comun + digito
        
        resultado_digitos.append(valor_digito)
    
    # Convertir a string usando dígitos 0-9, a-z
    digitos_str = "0123456789abcdefghijklmnopqrstuvwxyz"
    resultado = ''.join(digitos_str[d] for d in reversed(resultado_digitos))
    
    return resultado if resultado else "0"


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SISTEMAS DE NUMERACIÓN: Posicionales vs No Posicionales")
    print("=" * 70)
    
    # Ejemplo 1: Número Romano
    print("\n1. SISTEMA ROMANO (No Posicional)")
    print("-" * 70)
    numero = 1994
    explicacion = explicar_romano(numero)
    print(f"Número: {numero}_1_0 = {explicacion['romano']}")
    print(f"Desglose:")
    for d in explicacion['desglose']:
        print(f"  {d['cantidad']}* {d['simbolo']} = {d['representacion']} ({d['resta']})")
    
    # Ejemplo 2: Base 5
    print("\n2. SISTEMA BASE 5 (Posicional - Potencias)")
    print("-" * 70)
    número_base5 = 1994
    explicacion_b5 = explicar_base_5(número_base5)
    print(f"Número: {número_base5}_1_0 = {explicacion_b5['base_5']}_5")
    print(f"Calculo:")
    for p in explicacion_b5['potencias']:
        print(f"  {p['calculo']} = {p['valor']}")
    print(f"  Suma: {explicacion_b5['suma_final']}")
    
    # Ejemplo 3: Tiempo
    print("\n3. SISTEMA DE TIEMPO (Posicional - Bases Variables)")
    print("-" * 70)
    segundos = 3661
    explicacion_tiempo = explicar_tiempo(segundos)
    print(f"Número: {segundos} segundos = {explicacion_tiempo['tiempo']}")
    print(f"Desglose: {explicacion_tiempo['calculo']}")
    
    print("\n" + "=" * 70)


# ============================================================================
# PARTE 7: EFICACIA DE EMPAQUETADO (Packing Efficiency)
# ============================================================================

def eficacia_empaquetado_simple(base_nativa: int, base_destino: int, n_digitos: int) -> float:
    """
    Calcula la eficacia de empaquetado simple al representar números en base B
    usando un sistema nativo de base A con n dígitos.
    
    Eficacia = (A/B)^n
    
    Si A < B: eficacia disminuye conforme n crece (representación ineficiente)
    Si A = B: eficacia = 1 (máxima)
    Si A > B: requiere múltiples dígitos nativos por dígito destino
    
    Args:
        base_nativa: Base del sistema nativo (A, típicamente 2 para computadoras)
        base_destino: Base en la que queremos representar (B)
        n_digitos: Número de dígitos en la base destino (n)
    
    Returns:
        float: Eficacia como número entre 0 y 1
        
    Ejemplo:
        # Sistema binario nativo (2) representando decimal (10)
        eficacia_empaquetado_simple(2, 10, 3) = (2/10)^3 = 0.008
        # Muy ineficiente porque 10^3 = 1000 > 2^3 = 8
    """
    if base_nativa <= 0 or base_destino <= 0 or n_digitos <= 0:
        raise ValueError("Bases y número de dígitos deben ser positivos")
    
    # Capacidad en sistema nativo: A^n
    capacidad_nativa = base_nativa ** n_digitos
    
    # Capacidad en base destino: B^n
    capacidad_destino = base_destino ** n_digitos
    
    # Eficacia = capacidad_nativa / capacidad_destino = (A/B)^n
    eficacia = capacidad_nativa / capacidad_destino
    
    return eficacia


def eficacia_bcd_mejorada(valores_representables: int, bits_utilizados: int) -> float:
    """
    Calcula la eficacia de empaquetado mejorada usando técnicas como
    Dense Packed Decimal (DPD) o BCD mejorado.
    
    Eficacia = valores_representables / (2^bits_utilizados)
    
    Ejemplo clásico BCD:
    - BCD simple: 1 dígito decimal (10 valores) en 4 bits (2^4 = 16)
      Eficacia = 10/16 = 0.625
    
    Ejemplo DPD (Dense Packed Decimal):
    - 3 dígitos decimales (1000 valores) en 10 bits (2^10 = 1024)
      Eficacia = 1000/1024 ≈ 0.977
    
    Args:
        valores_representables: Cantidad de valores únicos a representar
        bits_utilizados: Número de bits disponibles
    
    Returns:
        float: Eficacia como número entre 0 y 1
    """
    if valores_representables <= 0 or bits_utilizados <= 0:
        raise ValueError("Valores y bits deben ser positivos")
    
    capacidad_bits = 2 ** bits_utilizados
    
    if valores_representables > capacidad_bits:
        raise ValueError(
            f"No se pueden representar {valores_representables} valores "
            f"con solo {bits_utilizados} bits (capacidad: {capacidad_bits})"
        )
    
    eficacia = valores_representables / capacidad_bits
    return eficacia


def comparar_eficacias_empaquetado(base_nativa: int, opciones: List[Dict]) -> Dict:
    """
    Compara la eficacia de empaquetado de múltiples estrategias de representación.
    
    Cada opción puede ser:
    - {'tipo': 'simple', 'base_destino': B, 'n_digitos': n}
    - {'tipo': 'bcd', 'valores': N, 'bits': b}
    
    Retorna un diccionario con las comparaciones detalladas.
    
    Args:
        base_nativa: Base del sistema nativo (típicamente 2)
        opciones: Lista de opciones de empaquetado a comparar
    
    Returns:
        Dict: Información de todas las opciones con sus eficacias
        
    Ejemplo:
        comparar_eficacias_empaquetado(2, [
            {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 1},
            {'tipo': 'bcd', 'valores': 10, 'bits': 4},
            {'tipo': 'bcd', 'valores': 1000, 'bits': 10},
        ])
    """
    resultados = {
        'base_nativa': base_nativa,
        'opciones': []
    }
    
    for opcion in opciones:
        if opcion['tipo'] == 'simple':
            base_dest = opcion['base_destino']
            n_dig = opcion['n_digitos']
            
            eficacia = eficacia_empaquetado_simple(base_nativa, base_dest, n_dig)
            capacidad_nativa = base_nativa ** n_dig
            capacidad_destino = base_dest ** n_dig
            
            resultado = {
                'tipo': 'simple',
                'base_destino': base_dest,
                'n_digitos': n_dig,
                'capacidad_nativa': capacidad_nativa,
                'capacidad_destino': capacidad_destino,
                'eficacia': eficacia,
                'porcentaje': eficacia * 100,
                'description': f"Sistema nativo base {base_nativa} representando "
                               f"base {base_dest} con {n_dig} dígitos"
            }
            
        elif opcion['tipo'] == 'bcd':
            valores = opcion['valores']
            bits = opcion['bits']
            
            eficacia = eficacia_bcd_mejorada(valores, bits)
            capacidad_bits = 2 ** bits
            
            resultado = {
                'tipo': 'bcd',
                'valores_representables': valores,
                'bits_utilizados': bits,
                'capacidad_bits': capacidad_bits,
                'eficacia': eficacia,
                'porcentaje': eficacia * 100,
                'desperdicio': capacidad_bits - valores,
                'description': f"{valores} valores en {bits} bits "
                               f"(BCD mejorado)"
            }
        else:
            continue
        
        resultados['opciones'].append(resultado)
    
    # Ordenar por eficacia (mejor primero)
    resultados['opciones'].sort(key=lambda x: x['eficacia'], reverse=True)
    resultados['mejor'] = resultados['opciones'][0] if resultados['opciones'] else None
    
    return resultados


def explicar_eficacia_empaquetado(base_nativa: int, base_destino: int, 
                                   n_digitos: int) -> Dict:
    """
    Explicación detallada del cálculo de eficacia de empaquetado.
    
    Incluye:
    - Capacidades en ambas bases
    - Fórmula de eficacia
    - Análisis de la relación A/B
    - Interpretación
    
    Args:
        base_nativa: Base del sistema nativo (A)
        base_destino: Base de destino (B)
        n_digitos: Número de dígitos (n)
    
    Returns:
        Dict: Explicación completa con cálculos paso a paso
    """
    eficacia = eficacia_empaquetado_simple(base_nativa, base_destino, n_digitos)
    capacidad_nativa = base_nativa ** n_digitos
    capacidad_destino = base_destino ** n_digitos
    ratio_base = base_nativa / base_destino
    
    # Análisis de la relación A/B
    if base_nativa < base_destino:
        interpretacion = (
            f"A < B: Sistema INEFICIENTE. Con {n_digitos} dígitos base {base_destino}, "
            f"solo se pueden usar {capacidad_nativa} de {capacidad_destino} "
            f"combinaciones posibles ({eficacia*100:.2f}% de eficacia)"
        )
    elif base_nativa == base_destino:
        interpretacion = (
            f"A = B: Sistema ÓPTIMO. Eficacia = 1.0 (100%). "
            f"Perfecto aprovechamiento del espacio."
        )
    else:  # base_nativa > base_destino
        interpretacion = (
            f"A > B: Sistema requiere múltiples dígitos nativos. "
            f"Para mejorar eficacia, se pueden empaquetar "
            f"múltiples dígitos de base {base_destino} en dígitos de base {base_nativa}."
        )
    
    # Calcular número de dígitos nativos requeridos para almacenar un dígito destino
    if base_nativa > base_destino:
        import math
        digitos_nativos_por_destino = math.ceil(math.log(base_destino, base_nativa))
        eficacia_fundamental = base_destino / (base_nativa ** digitos_nativos_por_destino)
    else:
        digitos_nativos_por_destino = None
        eficacia_fundamental = None
    
    return {
        'base_nativa': base_nativa,
        'base_destino': base_destino,
        'n_digitos': n_digitos,
        'capacidad_nativa': capacidad_nativa,
        'capacidad_destino': capacidad_destino,
        'formula': f"({base_nativa}/{base_destino})^{n_digitos} = {eficacia:.6f}",
        'eficacia': eficacia,
        'porcentaje': eficacia * 100,
        'ratio_base': ratio_base,
        'interpretacion': interpretacion,
        'digitos_nativos_por_destino': digitos_nativos_por_destino,
        'eficacia_fundamental': eficacia_fundamental,
    }


# Estándar IEEE 754 (Punto Flotante)
IEEE_754_STANDARDS = {
    'binary32': {
        'nombre': 'Single Precision (float)',
        'bits_totales': 32,
        'bits_signo': 1,
        'bits_exponente': 8,
        'bits_mantisa': 23,
        'sesgo_exponente': 127,
        'rango_minimo': 1.175e-38,
        'rango_maximo': 3.402e38,
        'digitos_decimales_precision': 6,
    },
    'binary64': {
        'nombre': 'Double Precision (double)',
        'bits_totales': 64,
        'bits_signo': 1,
        'bits_exponente': 11,
        'bits_mantisa': 52,
        'sesgo_exponente': 1023,
        'rango_minimo': 2.225e-308,
        'rango_maximo': 1.798e308,
        'digitos_decimales_precision': 15,
    },
    'binary128': {
        'nombre': 'Quadruple Precision (long double)',
        'bits_totales': 128,
        'bits_signo': 1,
        'bits_exponente': 15,
        'bits_mantisa': 112,
        'sesgo_exponente': 16383,
        'rango_minimo': 3.36e-4932,
        'rango_maximo': 1.19e4932,
        'digitos_decimales_precision': 34,
    },
    'decimal128': {
        'nombre': 'Decimal Floating Point',
        'bits_totales': 128,
        'digitos_significativos': 34,
        'rango_exponente': [-6143, 6144],
        'descripcion': 'Punto flotante decimal (IEEE 754-2008)',
        'uso': 'Aplicaciones financieras y comerciales',
    },
}


def explicar_ieee_754(formato: str) -> Dict:
    """
    Proporciona información detallada sobre los estándares IEEE 754.
    
    Args:
        formato: Uno de 'binary32', 'binary64', 'binary128', 'decimal128'
    
    Returns:
        Dict: Información completa del formato
        
    Ejemplo:
        explicar_ieee_754('binary64')  # Double precision
    """
    if formato not in IEEE_754_STANDARDS:
        raise ValueError(f"Formato desconocido: {formato}. "
                        f"Opciones: {list(IEEE_754_STANDARDS.keys())}")
    
    return {
        'formato': formato,
        'detalles': IEEE_754_STANDARDS[formato],
        'estructura': _estructura_ieee(formato),
    }


def _estructura_ieee(formato: str) -> str:
    """Describe la estructura de bits del formato IEEE 754."""
    if formato == 'binary32':
        return "32 bits: [1 signo | 8 exponente | 23 mantisa]"
    elif formato == 'binary64':
        return "64 bits: [1 signo | 11 exponente | 52 mantisa]"
    elif formato == 'binary128':
        return "128 bits: [1 signo | 15 exponente | 112 mantisa]"
    elif formato == 'decimal128':
        return "128 bits: [3 bits signo | 8 bits combinación | 120 bits coeficiente]"
    return "Formato desconocido"


# ============================================================================
# PARTE 8: CODIGOS ESPECIALIZADOS (5 bits y Gray)
# ============================================================================

# Tablas de códigos de 5 bits
CODIGO_BIQUINARIO = {
    0: '00110',  # 2 bits encendidos (posiciones 2 y 1)
    1: '01010',  # 2 bits encendidos (posiciones 3 y 1)
    2: '01100',  # 2 bits encendidos (posiciones 3 y 2)
    3: '10010',  # 2 bits encendidos (posiciones 4 y 1)
    4: '10100',  # 2 bits encendidos (posiciones 4 y 2)
    5: '11000',  # 2 bits encendidos (posiciones 4 y 3)
    6: '01001',  # 2 bits encendidos (posiciones 3 y 0)
    7: '10001',  # 2 bits encendidos (posiciones 4 y 0)
    8: '00101',  # 2 bits encendidos (posiciones 2 y 0)
    9: '00011',  # 2 bits encendidos (posiciones 1 y 0)
}

CODIGO_JOHNSON = {
    0: '00000',
    1: '00001',
    2: '00011',
    3: '00111',
    4: '01111',
    5: '11111',
    6: '11110',
    7: '11100',
    8: '11000',
    9: '10000',
}

CODIGO_GRAY_4BITS = {
    0: '0000',
    1: '0001',
    2: '0011',
    3: '0010',
    4: '0110',
    5: '0111',
    6: '0101',
    7: '0100',
    8: '1100',
    9: '1101',
    10: '1111',
    11: '1110',
    12: '1010',
    13: '1011',
    14: '1001',
    15: '1000',
}


def biquinario_a_entero(codigo_biquinario: str) -> int:
    """
    Convierte un código biquinario (2 entre 5) a su valor entero.
    
    El código biquinario tiene exactamente 2 bits encendidos en 5 posiciones,
    lo que permite representar 10 valores (0-9).
    
    Tabla de búsqueda:
    0: 00110, 1: 01010, 2: 01100, 3: 10010, 4: 10100
    5: 11000, 6: 01001, 7: 10001, 8: 00101, 9: 00011
    
    Args:
        codigo_biquinario: String de 5 caracteres '0' y '1' con exactamente 2 unos
    
    Returns:
        int: Valor entero 0-9
        
    Ejemplo:
        biquinario_a_entero('00110') -> 0
        biquinario_a_entero('01010') -> 1
        biquinario_a_entero('11000') -> 5
        biquinario_a_entero('00011') -> 9
    """
    if not isinstance(codigo_biquinario, str):
        raise ValueError("Código debe ser string")
    
    if len(codigo_biquinario) != 5:
        raise ValueError("Código biquinario debe tener 5 bits")
    
    # Validar caracteres
    if not all(c in '01' for c in codigo_biquinario):
        raise ValueError("Código biquinario debe contener solo '0' y '1'")
    
    if codigo_biquinario.count('1') != 2:
        raise ValueError("Código biquinario debe tener exactamente 2 bits encendidos")
    
    # Tabla inversa para lookup
    tabla_inversa = {v: k for k, v in CODIGO_BIQUINARIO.items()}
    
    if codigo_biquinario in tabla_inversa:
        return tabla_inversa[codigo_biquinario]
    else:
        raise ValueError("Código biquinario inválido")


def johnson_a_entero(codigo_johnson: str) -> int:
    """
    Convierte un código Johnson (cíclico) a su valor entero.
    
    El código Johnson es un código cíclico donde:
    - Cada valor sucesivo difiere en un solo bit (propiedad adyacente/cíclica)
    - Contiene una secuencia de 0s seguida de una secuencia de 1s
    - Se envuelve cíclicamente (último y primer valor también difieren en 1 bit)
    
    Tabla de Johnson:
    0: 00000, 1: 00001, 2: 00011, 3: 00111, 4: 01111,
    5: 11111, 6: 11110, 7: 11100, 8: 11000, 9: 10000
    
    Args:
        codigo_johnson: String de 5 caracteres '0' y '1'
    
    Returns:
        int: Valor entero 0-9
        
    Ejemplo:
        johnson_a_entero('00000') -> 0
        johnson_a_entero('00001') -> 1
        johnson_a_entero('11111') -> 5
        johnson_a_entero('10000') -> 9
    """
    if not isinstance(codigo_johnson, str):
        raise ValueError("Código debe ser string")
    
    if len(codigo_johnson) != 5:
        raise ValueError("Código Johnson debe tener 5 bits")
    
    # Validar caracteres
    if not all(c in '01' for c in codigo_johnson):
        raise ValueError("Código Johnson debe contener solo '0' y '1'")
    
    # Tabla inversa para lookup
    tabla_inversa = {v: k for k, v in CODIGO_JOHNSON.items()}
    
    if codigo_johnson in tabla_inversa:
        return tabla_inversa[codigo_johnson]
    else:
        raise ValueError("Código Johnson inválido: no es un código Johnson válido")


def entero_a_gray_4bits(valor: int) -> str:
    """
    Convierte un entero (0-15) a código Gray de 4 bits.
    
    Código Gray: código reflejado donde valores sucesivos difieren en un solo bit.
    Ventaja: ideal para encoders rotativos y contadores sin glitches.
    
    Fórmula: Gray = valor ^ (valor >> 1)
    
    Args:
        valor: Entero 0-15
    
    Returns:
        str: Código Gray de 4 bits
        
    Ejemplo:
        entero_a_gray_4bits(0)  -> '0000'
        entero_a_gray_4bits(1)  -> '0001'
        entero_a_gray_4bits(2)  -> '0011'
        entero_a_gray_4bits(15) -> '1000'
    """
    if not 0 <= valor <= 15:
        raise ValueError("Valor debe estar entre 0 y 15")
    
    gray = valor ^ (valor >> 1)
    return format(gray, '04b')


def gray_4bits_a_entero(codigo_gray: str) -> int:
    """
    Convierte un código Gray de 4 bits a su valor entero.
    
    El proceso es invertir la transformación XOR:
    valor = gray ^ (gray >> 1) ^ (gray >> 2) ^ (gray >> 3)
    
    Args:
        codigo_gray: String de 4 caracteres '0' y '1'
    
    Returns:
        int: Valor entero 0-15
        
    Ejemplo:
        gray_4bits_a_entero('0000') -> 0
        gray_4bits_a_entero('0001') -> 1
        gray_4bits_a_entero('0011') -> 2
        gray_4bits_a_entero('1000') -> 15
    """
    if len(codigo_gray) != 4:
        raise ValueError("Código Gray debe tener 4 bits")
    
    gray = int(codigo_gray, 2)
    
    # Invertir la transformación Gray
    valor = gray
    gray >>= 1
    while gray:
        valor ^= gray
        gray >>= 1
    
    return valor


def analisis_codigo_especializado(codigo: str, tipo: str) -> Dict:
    """
    Análisis completo de un código especializado.
    
    Args:
        codigo: String del código
        tipo: Uno de 'biquinario', 'johnson', 'gray'
    
    Returns:
        Dict: Análisis con conversión y características
        
    Ejemplo:
        analisis_codigo_especializado('00100', 'biquinario')
    """
    if tipo == 'biquinario':
        if len(codigo) != 5 or codigo.count('1') != 2:
            raise ValueError("Código biquinario inválido")
        
        valor = biquinario_a_entero(codigo)
        
        return {
            'tipo': 'biquinario',
            'codigo': codigo,
            'valor': valor,
            'bits_encendidos': 2,
            'capacidad': 10,
            'bits_utilizados': 5,
            'eficacia': 10 / 32,
            'caracteristicas': [
                'Exactamente 2 bits encendidos en 5 posiciones',
                'Detección de errores: 1 bit encendido == error',
                '3 bits encendidos == error'
            ]
        }
    
    elif tipo == 'johnson':
        if len(codigo) != 5:
            raise ValueError("Código Johnson debe tener 5 bits")
        
        valor = johnson_a_entero(codigo)
        
        return {
            'tipo': 'johnson',
            'codigo': codigo,
            'valor': valor,
            'capacidad': 10,
            'bits_utilizados': 5,
            'eficacia': 10 / 32,
            'caracteristicas': [
                'Código cíclico: valores sucesivos difieren en 1 bit',
                'Adyacente: transición suave sin glitches',
                'Envolvimiento cíclico: 9→0 también difiere en 1 bit'
            ]
        }
    
    elif tipo == 'gray':
        if len(codigo) != 4:
            raise ValueError("Código Gray debe tener 4 bits")
        
        valor = gray_4bits_a_entero(codigo)
        
        return {
            'tipo': 'gray',
            'codigo': codigo,
            'valor': valor,
            'capacidad': 16,
            'bits_utilizados': 4,
            'eficacia': 16 / 16,
            'caracteristicas': [
                'Código reflejado (especular): valores sucesivos difieren en 1 bit',
                'Óptimo para encoders rotativos',
                'Evita glitches en transiciones',
                'Envolvimiento cíclico perfecto'
            ]
        }
    
    else:
        raise ValueError(f"Tipo de código desconocido: {tipo}")


def comparar_codigos_5bits() -> Dict:
    """
    Comparación completa de códigos de 5 bits.
    
    Returns:
        Dict: Comparación de características, eficacias y propiedades
    """
    return {
        'biquinario': {
            'nombre': 'Código Biquinario (2 entre 5)',
            'capacidad': 10,
            'bits': 5,
            'eficacia': 10 / 32,
            'porcentaje_eficacia': (10 / 32) * 100,
            'bits_encendidos': 2,
            'adyacente': False,
            'ciclico': False,
            'especular': False,
            'error_detection': True,
            'caracteristicas': [
                'Detecta errores simples',
                'Patrón fijo: exactamente 2 bits encendidos',
                'Usado en viejos sistemas telefónicos'
            ]
        },
        'johnson': {
            'nombre': 'Código Johnson (Cíclico)',
            'capacidad': 10,
            'bits': 5,
            'eficacia': 10 / 32,
            'porcentaje_eficacia': (10 / 32) * 100,
            'adyacente': True,
            'ciclico': True,
            'especular': False,
            'error_detection': False,
            'caracteristicas': [
                'Adyacente: cambio de 1 bit entre valores',
                'Cíclico: envolvimiento perfecto',
                'Ideal para contadores y máquinas de estados'
            ]
        },
        'gray_4bits': {
            'nombre': 'Código Gray (4 bits)',
            'capacidad': 16,
            'bits': 4,
            'eficacia': 16 / 16,
            'porcentaje_eficacia': 100.0,
            'adyacente': True,
            'ciclico': True,
            'especular': True,
            'error_detection': False,
            'caracteristicas': [
                'Reflejado/Especular: simetría perfecta',
                'Adyacente: cambio de 1 bit entre valores',
                'Cíclico: transición suave sin glitches',
                'Óptimo para encoders rotativos'
            ]
        }
    }


# ============================================================================
# PARTE 6: DISTANCIA HAMMING Y LENGUAJES DE LONGITUD FIJA
# ============================================================================

def distancia_hamming(palabra_a: str, palabra_b: str) -> int:
    """
    Calcula la distancia Hamming entre dos palabras de igual longitud.
    
    La distancia Hamming es el número de posiciones en las que los símbolos
    de dos palabras de igual longitud son diferentes.
    
    Args:
        palabra_a: Primera palabra (cadena de caracteres)
        palabra_b: Segunda palabra (cadena de caracteres)
        
    Returns:
        int: Número de posiciones diferentes
        
    Raises:
        ValueError: Si las palabras tienen longitudes diferentes
        
    Ejemplo:
        distancia_hamming('1011', '1001') -> 1  (difieren en posición 2)
        distancia_hamming('0000', '1111') -> 4  (difieren en todas)
        distancia_hamming('1010', '1010') -> 0  (idénticas)
    """
    if len(palabra_a) != len(palabra_b):
        raise ValueError(
            f"Las palabras deben tener igual longitud. "
            f"Recibidas: {len(palabra_a)} vs {len(palabra_b)}"
        )
    
    return sum(1 for a, b in zip(palabra_a, palabra_b) if a != b)



# ============================================================================
# CONSTRUCTORES DE LENGUAJES (usando FixedLengthLanguage)
# ============================================================================

def crear_lenguaje_binario_saturado(longitud: int, nombre='') -> FixedLengthLanguage:
    """
    Crea un lenguaje binario saturado (todas las 2^L palabras son válidas).
    
    Args:
        longitud: Longitud de las palabras
        nombre: Nombre descriptivo (ej: "Binario Natural 4-bit")
        
    Returns:
        FixedLengthLanguage: Instancia del lenguaje binario
    """
    def siguiente_binario(palabra: str) -> str:
        """Incrementa palabra binaria con wrap-around."""
        # Convertir a entero, incrementar, convertir back
        valor = int(palabra, 2)
        valor = (valor + 1) % (2 ** longitud)
        return format(valor, f'0{longitud}b')
    
    return FixedLengthLanguage(
        alphabet=Alphabet(['0', '1']),
        length=longitud,
        predicate=lambda p: True,  # Todas las palabras son válidas
        zero_element='0' * longitud,
        next_function=siguiente_binario,
        name=nombre or f"Binario Saturado {longitud}-bit"
    )


def crear_lenguaje_bcd() -> FixedLengthLanguage:
    """
    Crea el lenguaje BCD (Binary Coded Decimal).
    
    BCD válido: representa dígitos 0-9
    - Total posible: 2^4 = 16 palabras
    - Total válido: 10 palabras (0000-1001)
    
    Returns:
        FixedLengthLanguage: Instancia del lenguaje BCD
    """
    # Palabras válidas: 0000 a 1001 (0-9 en decimal)
    palabras_validas = {format(i, '04b') for i in range(10)}
    
    def siguiente_bcd(palabra: str) -> str:
        """Incrementa BCD con wrap-around a 0."""
        valor = int(palabra, 2)
        valor = (valor + 1) % 10
        return format(valor, '04b')
    
    def predicado_bcd(palabra: str) -> bool:
        return palabra in palabras_validas
    
    return FixedLengthLanguage(
        alphabet=Alphabet(['0', '1']),
        length=4,
        predicate=predicado_bcd,
        zero_element='0000',
        next_function=siguiente_bcd,
        name="BCD (Binary Coded Decimal)"
    )


def crear_lenguaje_johnson() -> FixedLengthLanguage:
    """
    Crea el lenguaje Johnson (código cíclico adyacente de 5 bits).
    
    Johnson: Código adyacente donde cada valor difiere en 1 bit
    - Total posible: 2^5 = 32 palabras
    - Total válido: 10 palabras (para dígitos 0-9)
    
    Returns:
        FixedLengthLanguage: Instancia del lenguaje Johnson
    """
    palabras_johnson = [
        '00000',  # 0
        '00001',  # 1
        '00011',  # 2
        '00111',  # 3
        '01111',  # 4
        '11111',  # 5
        '11110',  # 6
        '11100',  # 7
        '11000',  # 8
        '10000',  # 9
    ]
    
    palabras_johnson_set = set(palabras_johnson)
    
    def siguiente_johnson(palabra: str) -> str:
        """Incrementa Johnson con wrap-around."""
        idx = palabras_johnson.index(palabra)
        return palabras_johnson[(idx + 1) % 10]
    
    def predicado_johnson(palabra: str) -> bool:
        return palabra in palabras_johnson_set
    
    # Crear lenguaje pero sobrescribir generar_todas_palabras para mantener orden
    lenguaje = FixedLengthLanguage(
        alphabet=Alphabet(['0', '1']),
        length=5,
        predicate=predicado_johnson,
        zero_element='00000',
        next_function=siguiente_johnson,
        name="Código Johnson (Cíclico Adyacente)"
    )
    
    # Cache directo para mantener el orden correcto
    lenguaje._words_cache = palabras_johnson
    
    return lenguaje


def crear_lenguaje_biquinario() -> FixedLengthLanguage:
    """
    Crea el lenguaje Biquinario (2 entre 5).
    
    Biquinario: Exactamente 2 bits encendidos
    - Total posible: 2^5 = 32 palabras
    - Total válido: C(5,2) = 10 palabras
    
    Returns:
        FixedLengthLanguage: Instancia del lenguaje Biquinario
    """
    palabras_biquinarias = [
        '00110',  # 0 (posiciones 2,1)
        '00101',  # 1 (posiciones 2,0)
        '01001',  # 2 (posiciones 3,0)
        '01010',  # 3 (posiciones 3,1)
        '01100',  # 4 (posiciones 3,2)
        '10001',  # 5 (posiciones 4,0)
        '10010',  # 6 (posiciones 4,1)
        '10100',  # 7 (posiciones 4,2)
        '11000',  # 8 (posiciones 4,3)
        '00011',  # 9 (posiciones 1,0)  <- FALTABA ESTA
    ]
    
    palabras_biquinarias_set = set(palabras_biquinarias)
    
    def siguiente_biquinario(palabra: str) -> str:
        """Incrementa biquinario con wrap-around."""
        idx = palabras_biquinarias.index(palabra)
        return palabras_biquinarias[(idx + 1) % len(palabras_biquinarias)]
    
    def predicado_biquinario(palabra: str) -> bool:
        """Verifica que exactamente 2 bits estén encendidos."""
        return palabra.count('1') == 2 and palabra in palabras_biquinarias_set
    
    # Crear lenguaje pero sobrescribir generar_todas_palabras para mantener orden
    lenguaje = FixedLengthLanguage(
        alphabet=Alphabet(['0', '1']),
        length=5,
        predicate=predicado_biquinario,
        zero_element='00110',
        next_function=siguiente_biquinario,
        name="Código Biquinario (2 entre 5)"
    )
    
    # Cache directo para mantener el orden correcto
    lenguaje._words_cache = palabras_biquinarias
    
    return lenguaje


