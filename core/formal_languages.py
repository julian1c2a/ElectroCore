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