"""
Módulo Core: Lenguajes Formales, Alfabetos y Semántica.

Implementa la arquitectura base para el Tema 4.1 del plan de estudios:
1. Alfabeto (Σ): Conjunto finito de símbolos.
2. Lenguaje (L): Conjunto de palabras sobre Σ (aquí acotado a L ⊆ Σ^n).
3. Semántica (S): Función que dota de significado o valor a las palabras.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Iterator, Dict, Generic, TypeVar
import itertools

# Tipo genérico para el valor semántico (puede ser int, float, str, objeto...)
T = TypeVar('T')


# ==============================================================================
# 1. NIVEL DE ALFABETO (Sintaxis Básica)
# ==============================================================================

class Alphabet(ABC):
    """
    Clase Abstracta: Representa un conjunto finito y no vacío de símbolos (Σ).
    """

    @property
    @abstractmethod
    def symbols(self) -> Tuple[str, ...]:
        """Devuelve la tupla ordenada de símbolos válidos."""
        pass

    @property
    def cardinality(self) -> int:
        """El número de símbolos en el alfabeto (|Σ| o Base)."""
        return len(self.symbols)

    def is_valid_symbol(self, char: str) -> bool:
        """Verifica si un carácter pertenece al alfabeto."""
        return char in self.symbols

    def is_valid_word(self, word: str) -> bool:
        """Verifica si una cadena está compuesta solo por símbolos del alfabeto."""
        return all(self.is_valid_symbol(c) for c in word)

    def index_of(self, symbol: str) -> int:
        """Obtiene el índice (valor intrínseco) de un símbolo."""
        try:
            return self.symbols.index(symbol)
        except ValueError:
            raise ValueError(f"Símbolo '{symbol}' no pertenece al alfabeto {self}")

    def __str__(self) -> str:
        return f"Σ = {{{', '.join(self.symbols)}}}"


class ExplicitAlphabet(Alphabet):
    """Alfabeto definido explícitamente por una lista de símbolos."""
    
    def __init__(self, symbols: List[str], name: str = "Custom"):
        if not symbols:
            raise ValueError("Un alfabeto no puede ser vacío.")
        # Aseguramos unicidad y orden inmutable
        # Nota: sorted() es importante para tener un orden canónico determinista
        self._symbols = tuple(sorted(list(set(symbols)))) 
        self.name = name

    @property
    def symbols(self) -> Tuple[str, ...]:
        return self._symbols

    def __repr__(self):
        return f"Alphabet({self.name}, size={self.cardinality})"


# Alfabetos Canónicos
ALPHABET_BINARY = ExplicitAlphabet(['0', '1'], "Binary")
ALPHABET_OCTAL = ExplicitAlphabet([str(i) for i in range(8)], "Octal")
ALPHABET_DECIMAL = ExplicitAlphabet([str(i) for i in range(10)], "Decimal")
ALPHABET_HEX = ExplicitAlphabet(list("0123456789ABCDEF"), "Hexadecimal")
ALPHABET_DNA = ExplicitAlphabet(['A', 'C', 'G', 'T'], "DNA")


# ==============================================================================
# 2. NIVEL DE LENGUAJE (Reglas de Formación)
# ==============================================================================

class Language(ABC):
    """
    Clase Abstracta: Un conjunto de palabras (L ⊆ Σ*).
    En electrónica digital, nos enfocamos principalmente en Σ^n (longitud fija).
    """

    def __init__(self, alphabet: Alphabet):
        self.alphabet = alphabet

    @abstractmethod
    def __contains__(self, word: str) -> bool:
        """Determina si una palabra pertenece al lenguaje (w ∈ L)."""
        pass

    @abstractmethod
    def generate_words(self) -> Iterator[str]:
        """Generador que produce las palabras del lenguaje."""
        pass
    
    @property
    @abstractmethod
    def size(self) -> int:
        """Cardinalidad del lenguaje (si es finito)."""
        pass


class FixedLengthLanguage(Language):
    """
    Lenguaje formal L = Σ^n.
    Conjunto de todas las palabras de longitud exacta n sobre Σ.
    Ejemplo: Todos los bytes de 8 bits (Σ=Binary, n=8).
    """

    def __init__(self, alphabet: Alphabet, length: int):
        super().__init__(alphabet)
        if length < 0:
            raise ValueError("La longitud no puede ser negativa")
        self.length = length

    def __contains__(self, word: str) -> bool:
        return len(word) == self.length and self.alphabet.is_valid_word(word)

    def generate_words(self) -> Iterator[str]:
        """
        Genera todas las combinaciones posibles (producto cartesiano).
        Advertencia: Crece exponencialmente con length.
        """
        for chars in itertools.product(self.alphabet.symbols, repeat=self.length):
            yield "".join(chars)
    
    @property
    def size(self) -> int:
        """Cardinalidad |L| = |Σ|^n."""
        return self.alphabet.cardinality ** self.length
    
    def __repr__(self):
        return f"Language(Σ={self.alphabet.name}, length={self.length})"


# ==============================================================================
# 3. NIVEL DE SEMÁNTICA (Significado y Orden)
# ==============================================================================

class Semantics(ABC, Generic[T]):
    """
    Clase Abstracta: Asigna significado a las palabras de un lenguaje.
    f: L -> D (Dominio de significado)
    """

    def __init__(self, language: Language):
        self.language = language

    @abstractmethod
    def evaluate(self, word: str) -> T:
        """Devuelve el valor/significado de la palabra."""
        pass
    
    @abstractmethod
    def describe(self) -> str:
        """Descripción pedagógica de la semántica."""
        pass
    
    def compare(self, word_a: str, word_b: str) -> int:
        """
        Compara dos palabras basándose en su significado semántico.
        Returns: <0 si a < b, 0 si a == b, >0 si a > b
        """
        val_a = self.evaluate(word_a)
        val_b = self.evaluate(word_b)
        
        if val_a < val_b: return -1
        if val_a > val_b: return 1
        return 0


class PositionalSemantics(Semantics[int]):
    """
    Semántica Numérica Posicional Estándar (Base N).
    Asigna el valor numérico interpretando la palabra como base N.
    Ej: "10" en binario -> 2.
    """
    
    def evaluate(self, word: str) -> int:
        if word not in self.language:
            # Validación laxa para permitir subcadenas si fuera necesario, 
            # pero estricta por defecto.
            if not self.language.alphabet.is_valid_word(word):
                 raise ValueError(f"Palabra '{word}' contiene símbolos inválidos")
        
        base = self.language.alphabet.cardinality
        value = 0
        for char in word:
            digit_val = self.language.alphabet.index_of(char)
            value = value * base + digit_val
        return value
    
    def describe(self) -> str:
        return f"Valor numérico posicional en Base {self.language.alphabet.cardinality} (Sin Signo)"


class LexicographicalSemantics(Semantics[str]):
    """
    Semántica de Orden de Diccionario.
    El 'valor' es la palabra misma, usada para ordenación alfabética.
    """
    
    def evaluate(self, word: str) -> str:
        return word

    def describe(self) -> str:
        return "Orden lexicográfico puro (basado en el orden de los símbolos en ASCII)"


class CustomMappingSemantics(Semantics[Any]):
    """
    Semántica arbitraria definida por un diccionario.
    Útil para códigos como Gray, códigos de error, o asignaciones aleatorias.
    """
    def __init__(self, language: Language, mapping: Dict[str, Any], description: str):
        super().__init__(language)
        self.mapping = mapping
        self.desc = description

    def evaluate(self, word: str) -> Any:
        return self.mapping.get(word, None)

    def describe(self) -> str:
        return self.desc


# ==============================================================================
# 4. FUNCIONES DE ANÁLISIS DE DISTANCIA DE HAMMING
# ==============================================================================

def hamming_distance(x: str, y: str) -> int:
    """
    Calcula la distancia de Hamming entre dos palabras de igual longitud.
    
    La distancia de Hamming es el número de posiciones en las que los símbolos
    de dos palabras de igual longitud son diferentes.
    
    Args:
        x: Primera palabra (cadena de caracteres)
        y: Segunda palabra (cadena de caracteres)
        
    Returns:
        int: Número de posiciones diferentes
        
    Raises:
        ValueError: Si las palabras tienen longitudes diferentes
        
    Ejemplo:
        >>> hamming_distance('1011', '1001')
        1
        >>> hamming_distance('0000', '1111')
        4
        >>> hamming_distance('1010', '1010')
        0
    """
    if len(x) != len(y):
        raise ValueError(
            f"Las palabras deben tener igual longitud. "
            f"Recibidas: {len(x)} vs {len(y)}"
        )
    
    return sum(c1 != c2 for c1, c2 in zip(x, y))


def hamming_weight(x: str, zero_symbol: str = '0') -> int:
    """
    Calcula el peso de Hamming de una palabra.
    
    El peso de Hamming es el número de posiciones no nulas (diferentes del
    símbolo cero del alfabeto). Para alfabetos binarios, es el número de unos.
    
    Args:
        x: Palabra (cadena de caracteres)
        zero_symbol: Símbolo que representa el cero (por defecto '0')
        
    Returns:
        int: Número de símbolos no-cero
        
    Ejemplo:
        >>> hamming_weight('0000')
        0
        >>> hamming_weight('1010')
        2
        >>> hamming_weight('1111')
        4
        >>> hamming_weight('10110101')
        5
    
    Nota:
        Para alfabetos binarios: hamming_weight(x) == hamming_distance(x, '0'*len(x))
    """
    return sum(c != zero_symbol for c in x)


def min_distance_of_language(code: List[str]) -> float:
    """
    Calcula la distancia mínima de un código (lenguaje).
    
    La distancia mínima es la menor distancia de Hamming entre cualquier par
    de palabras distintas del código. Determina la capacidad de detección y
    corrección de errores.
    
    Args:
        code: Lista de palabras-código (todas deben tener la misma longitud)
        
    Returns:
        float: Distancia mínima del código (inf si tiene menos de 2 palabras)
        
    Ejemplo:
        >>> min_distance_of_language(['000', '111'])
        3
        >>> min_distance_of_language(['000', '111', '101', '010'])
        2
    
    Nota:
        Un código con d_min puede:
        - Detectar hasta d_min - 1 errores
        - Corregir hasta ⌊(d_min - 1) / 2⌋ errores
    """
    if len(code) < 2:
        return float('inf')
    
    min_dist = float('inf')
    for i in range(len(code)):
        for j in range(i + 1, len(code)):
            dist = hamming_distance(code[i], code[j])
            min_dist = min(min_dist, dist)
    
    return min_dist


def hamming_sphere(center: str, radius: int, alphabet: str = '01') -> set:
    """
    Genera la esfera de Hamming de radio r centrada en una palabra.
    
    La esfera de Hamming B(x, r) es el conjunto de todas las palabras a
    distancia como máximo r de x.
    
    Args:
        center: Palabra central
        radius: Radio de la esfera (número máximo de diferencias)
        alphabet: Alfabeto a usar (por defecto binario '01')
        
    Returns:
        set: Conjunto de palabras en la esfera
        
    Ejemplo:
        >>> sorted(hamming_sphere('101', 1))
        ['001', '100', '101', '111']
        >>> len(hamming_sphere('000', 2))
        7  # C(3,0) + C(3,1) + C(3,2) = 1 + 3 + 3
    
    Nota:
        El volumen de la esfera es V(n, r) = Σᵢ₌₀ʳ C(n, i) · (|Σ| - 1)ⁱ
    """
    n = len(center)
    sphere = set()
    
    # Para cada número de posiciones a cambiar (de 0 a radius)
    for r in range(radius + 1):
        # Elegir qué posiciones cambiar
        for positions in itertools.combinations(range(n), r):
            # Para cada combinación de símbolos en esas posiciones
            for symbols in itertools.product(alphabet, repeat=r):
                word = list(center)
                for pos, sym in zip(positions, symbols):
                    if sym != center[pos]:  # Solo si realmente cambia
                        word[pos] = sym
                sphere.add(''.join(word))
    
    return sphere


def binomial_coefficient(n: int, k: int) -> int:
    """
    Calcula el coeficiente binomial C(n, k) = n! / (k! · (n-k)!).
    
    También conocido como "n choose k", representa el número de formas de
    elegir k elementos de un conjunto de n elementos sin importar el orden.
    
    Args:
        n: Tamaño del conjunto total
        k: Número de elementos a elegir
        
    Returns:
        int: Coeficiente binomial C(n, k)
        
    Ejemplo:
        >>> binomial_coefficient(5, 2)
        10
        >>> binomial_coefficient(7, 3)
        35
        >>> binomial_coefficient(5, 0)
        1
    
    Propiedades:
        - C(n, 0) = C(n, n) = 1
        - C(n, k) = C(n, n-k) (simetría)
        - C(n, k) = 0 si k < 0 o k > n
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Optimización: C(n, k) = C(n, n-k)
    k = min(k, n - k)
    
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result


def sphere_volume(n: int, r: int, alphabet_size: int = 2) -> int:
    """
    Calcula el volumen de una esfera de Hamming.
    
    El volumen V(n, r) es el número de palabras en la esfera B(x, r) de
    radio r en un espacio de palabras de longitud n sobre un alfabeto de
    tamaño dado.
    
    Args:
        n: Longitud de las palabras
        r: Radio de la esfera
        alphabet_size: Tamaño del alfabeto (por defecto 2 para binario)
        
    Returns:
        int: Volumen de la esfera V(n, r)
        
    Ejemplo:
        >>> sphere_volume(7, 1)
        8  # C(7,0) + C(7,1) = 1 + 7
        >>> sphere_volume(5, 2)
        16  # C(5,0) + C(5,1) + C(5,2) = 1 + 5 + 10
    
    Fórmula:
        V(n, r) = Σᵢ₌₀ʳ C(n, i) · (|Σ| - 1)ⁱ
    
    Aplicación:
        Usado en la Cota de Hamming: |C| ≤ |Σ|ⁿ / V(n, t) donde t es la
        capacidad de corrección del código.
    """
    volume = 0
    for i in range(r + 1):
        volume += binomial_coefficient(n, i) * ((alphabet_size - 1) ** i)
    return volume