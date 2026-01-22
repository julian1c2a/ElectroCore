"""
alfabetos.py




























































































































































































    print("=" * 70)    print("✅ Demo completado")    print("=" * 70)        demo_codigo_hamming()    demo_palabras_como_simbolos()    demo_codigo_bcd_bytes()    demo_jerarquia_binaria()if __name__ == "__main__":    print()    print(f"\nTotal de mensajes de 2 palabras: {len(mensajes)}")            print(f"   {i}. {mensaje}")    for i, mensaje in enumerate(mensajes[:5], 1):    mensajes = alf_hamming.generar_palabras(2)    print("\nPrimeros 5 mensajes de 2 palabras de código:")    # Generar mensajes como secuencias de palabras de código        print(f"|Σ_Hamming| = {alf_hamming.cardinal}")    print(f"\nΣ_Hamming = {alf_hamming}")    alf_hamming = AlfabetoDesdeLegunaje(L_hamming, separador=" ")    # Usar palabras del código como símbolos        print(f"d_min = {L_hamming.distancia_minima()}")    print(f"|L_Hamming| = {L_hamming.cardinal()}")    print(f"\nL_Hamming = código de Hamming(7,4)")    L_hamming = LenguajeExplicitoLongitudFija(alf_bin, palabras_hamming, "Hamming(7,4)")        }        "1100110", "1101001", "1110000", "1111111"        "1000011", "1001100", "1010101", "1011010",        "0100101", "0101010", "0110011", "0111100",        "0000000", "0001111", "0010110", "0011001",    palabras_hamming = {    # (Simplificado - solo algunas palabras de código)    # Nivel 1: Código de Hamming(7,4) - 16 palabras válidas de 7 bits        alf_bin = AlfabetosPredefinidos.binario()    # Nivel 0: Binario        print("=" * 70)    print("ALFABETO DESDE CÓDIGO DE HAMMING")    print("=" * 70)    """Usar código de Hamming(7,4) como alfabeto."""def demo_codigo_hamming():    print()    print(f"\nTotal de frases de 3 palabras: {len(frases)}")            print(f"   {i}. {frase}")    for i, frase in enumerate(frases[:10], 1):    frases = alf_palabras.generar_palabras(3)    print("\nPrimeras 10 frases de 3 palabras:")    # Generar "frases" (secuencias de palabras)        print(f"\nΣ₂ (palabras): {alf_palabras}")    alf_palabras = AlfabetoDesdeLegunaje(L_vocabulario, separador=" ")    # Nivel 2: Alfabeto con palabras como símbolos        print(f"|L₁| = {L_vocabulario.cardinal()}")    print(f"\nL₁ (vocabulario) = {sorted(L_vocabulario.enumerar())}")    L_vocabulario = LenguajeExplicito(alf_ascii, vocabulario)        }        "gato", "perro", "casa", "coche"        "el", "la", "un", "una",    vocabulario = {    # Nivel 1: Pequeño vocabulario de palabras        print(f"\nΣ₀ (ASCII minúsculas): |Σ₀| = {alf_ascii.cardinal}")    alf_ascii = AlfabetosPredefinidos.ascii_minusculas()    # Nivel 0: Alfabeto ASCII        print("=" * 70)    print("ALFABETO DESDE PALABRAS DEL LENGUAJE NATURAL")    print("=" * 70)    """Usar palabras del lenguaje natural como símbolos."""def demo_palabras_como_simbolos():    print()    print(f"\nTotal de bytes BCD posibles: {len(bytes_bcd)}")            print(f"   {byte_val} = {dig1}{dig2} (decimal: {decimal})")        decimal = dig1 * 10 + dig2        dig2 = alf_bcd.simbolos.index(byte_val[4:])        dig1 = alf_bcd.simbolos.index(byte_val[:4])        # Interpretar como decimal    for i, byte_val in enumerate(bytes_bcd[:10]):    bytes_bcd = alf_byte.generar_palabras(2)    print("\nPrimeros 10 bytes BCD (2 dígitos):")    # Generar "bytes" BCD (2 dígitos BCD = 8 bits)        print(f"\nΣ₂ (bytes BCD) = {alf_byte}")    alf_byte = AlfabetoDesdeLegunaje(L_bcd, separador="")    # Nivel 2: Alfabeto con símbolos BCD (sin separador = concatenación)        print(f"|L_BCD| = {L_bcd.cardinal()}")    print(f"\nL_BCD = conjunto de códigos BCD")    L_bcd = LenguajeExplicito(alf_bin, set(alf_bcd.simbolos))    # Crear lenguaje con símbolos BCD        print(f"Símbolos: {alf_bcd.simbolos}")    print(f"\nΣ₁ (BCD) = {alf_bcd}")    alf_bcd = AlfabetosPredefinidos.bcd()    # Nivel 1: Alfabeto BCD (10 códigos de 4 bits)        print(f"\nΣ₀ = {alf_bin}")    alf_bin = AlfabetosPredefinidos.binario()    # Nivel 0: Alfabeto binario        print("=" * 70)    print("ALFABETO JERÁRQUICO: BCD → BYTES")    print("=" * 70)    """Usar alfabeto BCD para construir bytes (2 dígitos BCD)."""def demo_codigo_bcd_bytes():    print()        print(f"   |L₂| = {L2.cardinal()} = 4² = 16")    print(f"   L₂ = Σ₁² (todas las palabras de longitud 2 sobre Σ₁)")    L2 = LenguajeUniverso(alf1, longitud=2)    print("\n📍 NIVEL 3: Lenguaje sobre Σ₁")    # Nivel 3: Lenguaje sobre Σ₁        print(f"      ... ({len(palabras_nivel2)} palabras totales)")        print(f"      '{palabra}'")    for palabra in palabras_nivel2[:8]:    palabras_nivel2 = alf1.generar_palabras(2)    print("\n   Palabras de longitud 2 sobre Σ₁:")    # Generar palabras de longitud 2 sobre Σ₁        print(f"   Símbolos: {alf1.simbolos}")    print(f"   Σ₁ = L₁ = {alf1}")    alf1 = AlfabetoDesdeLegunaje(L1, separador=" ")    print("\n📍 NIVEL 2: Alfabeto desde L₁")    # Nivel 2: Alfabeto con símbolos = palabras de L1        print(f"   |L₁| = {L1.cardinal()}")    print(f"   L₁ = Σ₀² = {palabras_L1}")    palabras_L1 = L1.enumerar()    L1 = LenguajeUniverso(alf0, longitud=2)    print("\n📍 NIVEL 1: Lenguaje sobre Σ₀")    # Nivel 1: Lenguaje de palabras de 2 bits        print(f"   |Σ₀| = {alf0.cardinal}")    print(f"   Σ₀ = {alf0}")    alf0 = AlfabetosPredefinidos.binario()    print("\n📍 NIVEL 0: Alfabeto básico")    # Nivel 0: Alfabeto binario básico        print("=" * 70)    print("JERARQUÍA MULTINIVEL: ALFABETO BINARIO")    print("=" * 70)    """Demostración de jerarquía de 3 niveles con alfabeto binario."""def demo_jerarquia_binaria():)    LenguajeExplicitoLongitudFija    LenguajeExplicito,    LenguajeUniverso, from core.lenguajes import ()    AlfabetoExplicito    AlfabetoDesdeLegunaje,    AlfabetosPredefinidos, from core.alfabetos import (sys.path.insert(0, str(Path(__file__).parent.parent))from pathlib import Pathimport sys"""- Nivel 3+: Niveles adicionales de abstracción- Nivel 2: Palabras sobre palabras (usando L1 como alfabeto)- Nivel 1: Palabras sobre símbolos básicos- Nivel 0: Símbolos básicosEsto permite crear jerarquías multinivel:como símbolos de un nuevo alfabeto.Demostración de alfabetos jerárquicos: usar palabras de un lenguaje
Módulo para la definición y manipulación de alfabetos en teoría de códigos
y lenguajes formales.

Un alfabeto es un conjunto finito no vacío de símbolos. Este módulo proporciona
clases y funciones para crear, validar y operar con alfabetos de diferentes tipos.

Classes:
    Alfabeto: Clase abstracta base para representar alfabetos
    AlfabetoExplicito: Alfabeto definido mediante lista explícita de símbolos
    AlfabetoEstandar: Alfabeto estándar basado en base numérica (2-36)
    AlfabetoBinario: Alfabeto binario especializado {0, 1}
    AlfabetoDesdeLenguaje: Alfabeto cuyos símbolos son palabras de un lenguaje
    
Functions:
    crear_alfabeto_explicito: Factory para crear alfabeto desde símbolos
    crear_alfabeto_estandar_desde_cardinal: Factory para alfabeto numérico
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Iterator
from collections import OrderedDict


# ============================================================================
# CLASE ABSTRACTA BASE
# ============================================================================

class Alfabeto(ABC):
    """
    Clase abstracta base para representar un alfabeto.
    
    Un alfabeto es un conjunto finito no vacío de símbolos.
    Esta clase define la interfaz común para todos los tipos de alfabetos.
    
    Attributes:
        simbolos: Lista ordenada de símbolos del alfabeto
        cardinal: Número de símbolos en el alfabeto
    """
    
    def __init__(self):
        """Inicializa un alfabeto vacío."""
        self._simbolos: List[str] = []
        self._indices: Dict[str, int] = {}
        self._cardinal: int = 0
    
    @abstractmethod
    def construir(self) -> None:
        """
        Construye el alfabeto.
        
        Método abstracto que debe ser implementado por las subclases
        para definir cómo se construye el alfabeto específico.
        """
        pass
    
    @property
    def simbolos(self) -> List[str]:
        """Retorna la lista ordenada de símbolos."""
        return self._simbolos.copy()
    
    @property
    def cardinal(self) -> int:
        """Retorna el cardinal (tamaño) del alfabeto."""
        return self._cardinal
    
    @property
    def indices(self) -> Dict[str, int]:
        """Retorna el diccionario de símbolos a índices."""
        return self._indices.copy()
    
    def contiene(self, simbolo: str) -> bool:
        """
        Verifica si un símbolo pertenece al alfabeto.
        
        Args:
            simbolo: Símbolo a verificar
            
        Returns:
            bool: True si el símbolo está en el alfabeto
        """
        return simbolo in self._indices
    
    def indice_de(self, simbolo: str) -> Optional[int]:
        """
        Obtiene el índice de un símbolo en el alfabeto.
        
        Args:
            simbolo: Símbolo del cual obtener el índice
            
        Returns:
            Optional[int]: Índice del símbolo, o None si no existe
        """
        return self._indices.get(simbolo)
    
    def simbolo_en(self, indice: int) -> Optional[str]:
        """
        Obtiene el símbolo en una posición específica.
        
        Args:
            indice: Posición del símbolo (0-indexed)
            
        Returns:
            Optional[str]: Símbolo en esa posición, o None si índice inválido
        """
        if 0 <= indice < self._cardinal:
            return self._simbolos[indice]
        return None
    
    def validar_palabra(self, palabra: str) -> bool:
        """
        Valida si una palabra está formada por símbolos del alfabeto.
        
        Args:
            palabra: Cadena a validar
            
        Returns:
            bool: True si todos los caracteres pertenecen al alfabeto
        """
        return all(char in self._indices for char in palabra)
    
    def comparar_simbolos(self, simbolo1: str, simbolo2: str) -> Optional[int]:
        """
        Compara dos símbolos del alfabeto según su orden.
        
        La comparación se basa en el índice de los símbolos en el alfabeto.
        
        Args:
            simbolo1: Primer símbolo a comparar
            simbolo2: Segundo símbolo a comparar
            
        Returns:
            Optional[int]: 
                -1 si simbolo1 < simbolo2
                 0 si simbolo1 = simbolo2
                 1 si simbolo1 > simbolo2
                None si algún símbolo no pertenece al alfabeto
                
        Example:
            >>> alf = AlfabetoEstandar(10)  # decimal
            >>> alf.comparar_simbolos('3', '7')
            -1
            >>> alf.comparar_simbolos('5', '5')
            0
            >>> alf.comparar_simbolos('9', '2')
            1
        """
        idx1 = self.indice_de(simbolo1)
        idx2 = self.indice_de(simbolo2)
        
        if idx1 is None or idx2 is None:
            return None
        
        if idx1 < idx2:
            return -1
        elif idx1 == idx2:
            return 0
        else:
            return 1
    
    def es_menor(self, simbolo1: str, simbolo2: str) -> bool:
        """
        Verifica si simbolo1 < simbolo2 en el orden del alfabeto.
        
        Args:
            simbolo1: Primer símbolo
            simbolo2: Segundo símbolo
            
        Returns:
            bool: True si simbolo1 está antes que simbolo2
            
        Raises:
            ValueError: Si algún símbolo no pertenece al alfabeto
        """
        resultado = self.comparar_simbolos(simbolo1, simbolo2)
        if resultado is None:
            raise ValueError(f"Uno o ambos símbolos no pertenecen al alfabeto")
        return resultado == -1
    
    def es_igual(self, simbolo1: str, simbolo2: str) -> bool:
        """
        Verifica si simbolo1 = simbolo2 (mismo símbolo).
        
        Args:
            simbolo1: Primer símbolo
            simbolo2: Segundo símbolo
            
        Returns:
            bool: True si son el mismo símbolo
            
        Raises:
            ValueError: Si algún símbolo no pertenece al alfabeto
        """
        resultado = self.comparar_simbolos(simbolo1, simbolo2)
        if resultado is None:
            raise ValueError(f"Uno o ambos símbolos no pertenecen al alfabeto")
        return resultado == 0
    
    def es_mayor(self, simbolo1: str, simbolo2: str) -> bool:
        """
        Verifica si simbolo1 > simbolo2 en el orden del alfabeto.
        
        Args:
            simbolo1: Primer símbolo
            simbolo2: Segundo símbolo
            
        Returns:
            bool: True si simbolo1 está después que simbolo2
            
        Raises:
            ValueError: Si algún símbolo no pertenece al alfabeto
        """
        resultado = self.comparar_simbolos(simbolo1, simbolo2)
        if resultado is None:
            raise ValueError(f"Uno o ambos símbolos no pertenecen al alfabeto")
        return resultado == 1
    
    def es_menor_o_igual(self, simbolo1: str, simbolo2: str) -> bool:
        """
        Verifica si simbolo1 <= simbolo2 en el orden del alfabeto.
        
        Args:
            simbolo1: Primer símbolo
            simbolo2: Segundo símbolo
            
        Returns:
            bool: True si simbolo1 está antes o es igual a simbolo2
            
        Raises:
            ValueError: Si algún símbolo no pertenece al alfabeto
        """
        resultado = self.comparar_simbolos(simbolo1, simbolo2)
        if resultado is None:
            raise ValueError(f"Uno o ambos símbolos no pertenecen al alfabeto")
        return resultado <= 0
    
    def es_mayor_o_igual(self, simbolo1: str, simbolo2: str) -> bool:
        """
        Verifica si simbolo1 >= simbolo2 en el orden del alfabeto.
        
        Args:
            simbolo1: Primer símbolo
            simbolo2: Segundo símbolo
            
        Returns:
            bool: True si simbolo1 está después o es igual a simbolo2
            
        Raises:
            ValueError: Si algún símbolo no pertenece al alfabeto
        """
        resultado = self.comparar_simbolos(simbolo1, simbolo2)
        if resultado is None:
            raise ValueError(f"Uno o ambos símbolos no pertenecen al alfabeto")
        return resultado >= 0
    
    def comparar_palabras_lexicografico(self, palabra1: str, palabra2: str) -> Optional[int]:
        """
        Compara dos palabras lexicográficamente según el orden del alfabeto.
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            Optional[int]:
                -1 si palabra1 < palabra2
                 0 si palabra1 = palabra2
                 1 si palabra1 > palabra2
                None si alguna palabra contiene símbolos no válidos
                
        Example:
            >>> alf = AlfabetoEstandar(2)  # binario
            >>> alf.comparar_palabras_lexicografico('101', '110')
            -1
            >>> alf.comparar_palabras_lexicografico('11', '11')
            0
        """
        # Validar que ambas palabras pertenecen al alfabeto
        if not self.validar_palabra(palabra1) or not self.validar_palabra(palabra2):
            return None
        
        # Comparar símbolo por símbolo
        for s1, s2 in zip(palabra1, palabra2):
            resultado = self.comparar_simbolos(s1, s2)
            if resultado != 0:
                return resultado
        
        # Si todos los símbolos coinciden, la más corta es menor
        if len(palabra1) < len(palabra2):
            return -1
        elif len(palabra1) > len(palabra2):
            return 1
        else:
            return 0
    
    def generar_palabras(self, longitud: int) -> List[str]:
        """
        Genera todas las palabras posibles de una longitud dada.
        
        Args:
            longitud: Longitud de las palabras a generar
            
        Returns:
            List[str]: Lista de todas las palabras posibles
            
        Example:
            >>> alf = AlfabetoEstandar(2)
            >>> alf.generar_palabras(2)
            ['00', '01', '10', '11']
        """
        if longitud == 0:
            return ['']
        
        if longitud == 1:
            return self._simbolos.copy()
        
        palabras = []
        
        def generar_recursivo(palabra_actual: str, long_restante: int):
            if long_restante == 0:
                palabras.append(palabra_actual)
                return
            
            for simbolo in self._simbolos:
                generar_recursivo(palabra_actual + simbolo, long_restante - 1)
        
        generar_recursivo('', longitud)
        return palabras
    
    def __len__(self) -> int:
        """Retorna el cardinal del alfabeto."""
        return self._cardinal
    
    def __contains__(self, simbolo: str) -> bool:
        """Permite usar 'simbolo in alfabeto'."""
        return self.contiene(simbolo)
    
    def __iter__(self) -> Iterator[str]:
        """Permite iterar sobre los símbolos del alfabeto."""
        return iter(self._simbolos)
    
    def __str__(self) -> str:
        """Representación en string del alfabeto."""
        simbolos_str = ', '.join(f"'{s}'" for s in self._simbolos)
        return f"Σ = {{{simbolos_str}}} (cardinal={self._cardinal})"
    
    def __repr__(self) -> str:
        """Representación técnica del alfabeto."""
        return f"{self.__class__.__name__}(cardinal={self._cardinal})"
    
    def __eq__(self, other) -> bool:
        """Compara dos alfabetos por igualdad."""
        if not isinstance(other, Alfabeto):
            return False
        return set(self._simbolos) == set(other._simbolos)


# ============================================================================
# ALFABETO EXPLÍCITO
# ============================================================================

class AlfabetoExplicito(Alfabeto):
    """
    Alfabeto definido mediante una lista explícita de símbolos.
    
    Los símbolos se proporcionan directamente y mantienen el orden
    en que fueron especificados. Cada símbolo tiene un índice asociado
    según su posición.
    
    Example:
        >>> alf = AlfabetoExplicito('0', '1', '2', '3')
        >>> alf.cardinal
        4
        >>> alf.indice_de('2')
        2
    """
    
    def __init__(self, *simbolos: str):
        """
        Inicializa un alfabeto con símbolos explícitos.
        
        Args:
            *simbolos: Símbolos del alfabeto (argumentos variables)
            
        Raises:
            ValueError: Si no se proporcionan símbolos o hay duplicados
        """
        super().__init__()
        
        if not simbolos:
            raise ValueError("El alfabeto debe tener al menos un símbolo")
        
        # Verificar duplicados
        if len(set(simbolos)) != len(simbolos):
            raise ValueError("El alfabeto no puede contener símbolos duplicados")
        
        self._simbolos_origen = list(simbolos)
        self.construir()
    
    def construir(self) -> None:
        """Construye el alfabeto con los símbolos proporcionados."""
        self._simbolos = self._simbolos_origen.copy()
        self._cardinal = len(self._simbolos)
        self._indices = {simbolo: idx for idx, simbolo in enumerate(self._simbolos)}


# ============================================================================
# ALFABETO ESTÁNDAR
# ============================================================================

class AlfabetoEstandar(Alfabeto):
    """
    Alfabeto estándar basado en una base numérica.
    
    Para bases <= 10: usa dígitos '0' a 'base-1'
    Para bases > 10: usa '0'-'9' seguido de 'A'-'Z'
    
    El índice de cada símbolo coincide con su valor numérico.
    
    Example:
        >>> alf_bin = AlfabetoEstandar(2)
        >>> print(alf_bin)
        Σ = {'0', '1'} (cardinal=2)
        
        >>> alf_hex = AlfabetoEstandar(16)
        >>> alf_hex.cardinal
        16
        >>> alf_hex.simbolo_en(15)
        'F'
    """
    
    def __init__(self, base: int, mayusculas: bool = True):
        """
        Inicializa un alfabeto estándar para una base numérica.
        
        Args:
            base: Base numérica (2 <= base <= 36)
            mayusculas: Si True, usa A-Z; si False, usa a-z
            
        Raises:
            ValueError: Si la base está fuera del rango permitido
        """
        super().__init__()
        
        if base < 2:
            raise ValueError("La base debe ser >= 2")
        if base > 36:
            raise ValueError("La base debe ser <= 36 (0-9 + A-Z)")
        
        self._base = base
        self._mayusculas = mayusculas
        self.construir()
    
    def construir(self) -> None:
        """Construye el alfabeto estándar según la base."""
        self._simbolos = []
        letra_inicial = 'A' if self._mayusculas else 'a'
        
        for i in range(self._base):
            if i < 10:
                self._simbolos.append(str(i))
            else:
                self._simbolos.append(chr(ord(letra_inicial) + i - 10))
        
        self._cardinal = len(self._simbolos)
        self._indices = {simbolo: idx for idx, simbolo in enumerate(self._simbolos)}
    
    @property
    def base(self) -> int:
        """Retorna la base numérica del alfabeto."""
        return self._base
    
    def valor_numerico(self, simbolo: str) -> Optional[int]:
        """
        Obtiene el valor numérico de un símbolo.
        
        En alfabetos estándar, el valor numérico coincide con el índice.
        
        Args:
            simbolo: Símbolo del cual obtener el valor
            
        Returns:
            Optional[int]: Valor numérico del símbolo
        """
        return self.indice_de(simbolo)


# ============================================================================
# ALFABETO BINARIO
# ============================================================================

class AlfabetoBinario(AlfabetoEstandar):
    """
    Alfabeto binario: {0, 1}
    
    Clase especializada para el alfabeto binario más común en sistemas digitales.
    Garantiza que siempre contiene exactamente '0' con índice 0 y '1' con índice 1.
    
    Example:
        >>> alf = AlfabetoBinario()
        >>> alf.simbolos
        ['0', '1']
        >>> alf.indices
        {'0': 0, '1': 1}
        >>> alf.valor_numerico('1')
        1
    """
    
    def __init__(self):
        """Inicializa el alfabeto binario con símbolos '0' y '1'."""
        super().__init__(base=2, mayusculas=True)
    
    def __repr__(self) -> str:
        """Representación técnica del alfabeto binario."""
        return "AlfabetoBinario()"


# ============================================================================
# ALFABETO DESDE LENGUAJE
# ============================================================================

class AlfabetoDesdeLenguaje(Alfabeto):
    """
    Alfabeto cuyos símbolos son las palabras de un lenguaje.
    
    Esto permite crear jerarquías multinivel:
    - Nivel 0: Alfabeto básico Σ₀ = {0, 1}
    - Nivel 1: Lenguaje L₁ sobre Σ₀ = {00, 01, 10, 11}
    - Nivel 2: Alfabeto Σ₁ = L₁ (usando palabras como símbolos)
    - Nivel 3: Lenguaje L₂ sobre Σ₁
    
    Los símbolos del alfabeto son las palabras del lenguaje proporcionado.
    El lenguaje debe ser finito y estar completamente enumerado.
    
    Example:
        >>> # Nivel 0: alfabeto binario
        >>> alf_bin = AlfabetosPredefinidos.binario()
        >>> 
        >>> # Nivel 1: lenguaje de palabras de 2 bits
        >>> from lenguajes import LenguajeUniverso
        >>> L1 = LenguajeUniverso(alf_bin, longitud=2)
        >>> L1.enumerar()
        ['00', '01', '10', '11']
        >>> 
        >>> # Nivel 2: alfabeto con símbolos = palabras de L1
        >>> alf_nivel2 = AlfabetoDesdeLenguaje(L1)
        >>> alf_nivel2.simbolos
        ['00', '01', '10', '11']
        >>> 
        >>> # Nivel 3: palabras sobre el nuevo alfabeto
        >>> alf_nivel2.generar_palabras(2)
        ['00 00', '00 01', '00 10', '00 11', '01 00', ...]
    
    Attributes:
        lenguaje_fuente: Lenguaje de donde se toman las palabras
        separador: String para separar símbolos al formar palabras
    """
    
    def __init__(self, lenguaje, separador: str = " "):
        """
        Crea alfabeto usando palabras de un lenguaje como símbolos.
        
        Args:
            lenguaje: Lenguaje fuente (debe ser finito)
            separador: Separador entre símbolos al generar palabras
                      (por defecto espacio para distinguir símbolos)
        
        Raises:
            ValueError: Si el lenguaje es infinito o vacío
            ImportError: Si el módulo lenguajes no está disponible
        
        Example:
            >>> # Usar alfabeto BCD como lenguaje de símbolos
            >>> alf_bcd = AlfabetosPredefinidos.bcd()
            >>> L_bcd = LenguajeExplicito(alf_bin, set(alf_bcd.simbolos))
            >>> alf_byte = AlfabetoDesdeLenguaje(L_bcd, separador="")
            >>> # Ahora cada "símbolo" es un grupo de 4 bits
        """
        super().__init__()
        
        # Importación tardía para evitar dependencia circular
        try:
            from core.lenguajes import Lenguaje
        except ImportError:
            from lenguajes import Lenguaje
        
        if not isinstance(lenguaje, Lenguaje):
            raise TypeError(
                f"Se esperaba un Lenguaje, recibido: {type(lenguaje).__name__}"
            )
        
        # Verificar que el lenguaje sea finito
        cardinal = lenguaje.cardinal()
        if cardinal == float('inf'):
            raise ValueError(
                "No se puede crear alfabeto desde lenguaje infinito. "
                "El lenguaje debe ser finito y enumerarble."
            )
        
        if cardinal == 0:
            raise ValueError("No se puede crear alfabeto desde lenguaje vacío")
        
        self._lenguaje_fuente = lenguaje
        self._separador = separador
        self.construir()
    
    def construir(self) -> None:
        """Construye el alfabeto enumerando las palabras del lenguaje."""
        # Los símbolos son las palabras del lenguaje
        palabras = self._lenguaje_fuente.enumerar()
        
        self._simbolos = palabras
        self._cardinal = len(palabras)
        self._indices = {simbolo: idx for idx, simbolo in enumerate(palabras)}
    
    @property
    def lenguaje_fuente(self):
        """Retorna el lenguaje fuente del alfabeto."""
        return self._lenguaje_fuente
    
    @property
    def separador(self) -> str:
        """Retorna el separador usado entre símbolos."""
        return self._separador
    
    def generar_palabras(self, longitud: int) -> List[str]:
        """
        Genera todas las palabras de longitud dada sobre este alfabeto.
        
        Como los símbolos son palabras, usa el separador para unirlas.
        
        Args:
            longitud: Número de símbolos en cada palabra
            
        Returns:
            Lista de palabras del alfabeto jerárquico
            
        Example:
            >>> # Si símbolos = ['00', '01', '10', '11']
            >>> alf.generar_palabras(2)
            ['00 00', '00 01', '00 10', '00 11', '01 00', ...]
        """
        if longitud == 0:
            return ['']
        
        if longitud == 1:
            return self._simbolos.copy()
        
        # Generación recursiva
        palabras_cortas = self.generar_palabras(longitud - 1)
        resultado = []
        
        for palabra_corta in palabras_cortas:
            for simbolo in self._simbolos:
                if palabra_corta:
                    nueva = palabra_corta + self._separador + simbolo
                else:
                    nueva = simbolo
                resultado.append(nueva)
        
        return resultado
    
    def validar_palabra(self, palabra: str) -> bool:
        """
        Valida si una palabra es válida sobre este alfabeto jerárquico.
        
        Divide la palabra usando el separador y verifica que cada parte
        sea un símbolo válido.
        
        Args:
            palabra: Palabra a validar
            
        Returns:
            True si la palabra es válida
            
        Example:
            >>> # Si símbolos = ['00', '01', '10', '11'] y separador = ' '
            >>> alf.validar_palabra('00 01 11')
            True
            >>> alf.validar_palabra('00 02')  # '02' no es símbolo
            False
        """
        if not palabra:
            return True  # Palabra vacía es válida
        
        if self._separador:
            partes = palabra.split(self._separador)
        else:
            # Sin separador, debe dividir por longitud de símbolos
            # Asume que todos los símbolos tienen la misma longitud
            if not self._simbolos:
                return False
            
            long_simbolo = len(self._simbolos[0])
            if len(palabra) % long_simbolo != 0:
                return False
            
            partes = [
                palabra[i:i+long_simbolo] 
                for i in range(0, len(palabra), long_simbolo)
            ]
        
        return all(parte in self._indices for parte in partes)
    
    def __str__(self) -> str:
        """Representación textual del alfabeto jerárquico."""
        if self._cardinal <= 10:
            simbolos_str = ', '.join(f"'{s}'" for s in self._simbolos)
            return f"Σ = {{{simbolos_str}}} (desde lenguaje, |Σ| = {self._cardinal})"
        else:
            primeros = ', '.join(f"'{s}'" for s in self._simbolos[:3])
            ultimos = ', '.join(f"'{s}'" for s in self._simbolos[-2:])
            return f"Σ = {{{primeros}, ..., {ultimos}}} (desde lenguaje, |Σ| = {self._cardinal})"
    
    def __repr__(self) -> str:
        """Representación técnica del alfabeto jerárquico."""
        return f"AlfabetoDesdeLenguaje(lenguaje={self._lenguaje_fuente!r}, separador={self._separador!r})"


# ============================================================================
# ALFABETOS PREDEFINIDOS
# ============================================================================

class AlfabetosPredefinidos:
    """Colección de alfabetos estándar comúnmente usados."""
    
    @staticmethod
    def binario() -> AlfabetoBinario:
        """Alfabeto binario: {0, 1}"""
        return AlfabetoBinario()
    
    @staticmethod
    def octal() -> AlfabetoEstandar:
        """Alfabeto octal: {0, 1, 2, 3, 4, 5, 6, 7}"""
        return AlfabetoEstandar(8)
    
    @staticmethod
    def decimal() -> AlfabetoEstandar:
        """Alfabeto decimal: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}"""
        return AlfabetoEstandar(10)
    
    @staticmethod
    def hexadecimal(mayusculas: bool = True) -> AlfabetoEstandar:
        """Alfabeto hexadecimal: {0-9, A-F} o {0-9, a-f}"""
        return AlfabetoEstandar(16, mayusculas)
    
    @staticmethod
    def bcd() -> AlfabetoExplicito:
        """Alfabeto BCD (Binary Coded Decimal): 4 bits"""
        return AlfabetoExplicito(
            '0000', '0001', '0010', '0011', '0100',
            '0101', '0110', '0111', '1000', '1001'
        )
    
    @staticmethod
    def ascii_minusculas() -> AlfabetoExplicito:
        """Alfabeto de letras minúsculas a-z"""
        return AlfabetoExplicito(*[chr(i) for i in range(ord('a'), ord('z') + 1)])
    
    @staticmethod
    def ascii_mayusculas() -> AlfabetoExplicito:
        """Alfabeto de letras mayúsculas A-Z"""
        return AlfabetoExplicito(*[chr(i) for i in range(ord('A'), ord('Z') + 1)])


# ============================================================================
# FUNCIONES FACTORY
# ============================================================================

def crear_alfabeto_explicito(*simbolos: str) -> AlfabetoExplicito:
    """
    Crea un alfabeto con símbolos explícitos.
    
    Args:
        *simbolos: Símbolos del alfabeto
        
    Returns:
        AlfabetoExplicito: Alfabeto creado
        
    Example:
        >>> alf = crear_alfabeto_explicito('0', '1', '2', '3')
        >>> alf.cardinal
        4
        >>> alf.indices
        {'0': 0, '1': 1, '2': 2, '3': 3}
    """
    return AlfabetoExplicito(*simbolos)


def crear_alfabeto_estandar_desde_cardinal(
    base: int, 
    mayusculas: bool = True
) -> AlfabetoEstandar:
    """
    Crea un alfabeto estándar desde una base numérica.
    
    Args:
        base: Base numérica (2-36)
        mayusculas: Si usar mayúsculas para letras
        
    Returns:
        AlfabetoEstandar: Alfabeto creado
        
    Example:
        >>> alf = crear_alfabeto_estandar_desde_cardinal(16)
        >>> alf.simbolos
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F']
    """
    return AlfabetoEstandar(base, mayusculas)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def obtener_alfabeto_desde_lista(simbolos: List[str]) -> Dict[str, int]:
    """
    Convierte una lista de símbolos en un diccionario símbolo→índice.
    
    Args:
        simbolos: Lista de símbolos
        
    Returns:
        Dict[str, int]: Diccionario {símbolo: índice}
        
    Example:
        >>> obtener_alfabeto_desde_lista(['a', 'b', 'c'])
        {'a': 0, 'b': 1, 'c': 2}
    """
    return {simbolo: idx for idx, simbolo in enumerate(simbolos)}


def unir_alfabetos(alf1: Alfabeto, alf2: Alfabeto) -> AlfabetoExplicito:
    """
    Crea un nuevo alfabeto como unión de dos alfabetos.
    
    Args:
        alf1: Primer alfabeto
        alf2: Segundo alfabeto
        
    Returns:
        AlfabetoExplicito: Alfabeto unión (sin duplicados)
        
    Example:
        >>> a1 = crear_alfabeto_explicito('0', '1')
        >>> a2 = crear_alfabeto_explicito('1', '2')
        >>> union = unir_alfabetos(a1, a2)
        >>> union.simbolos
        ['0', '1', '2']
    """
    simbolos_unidos = list(dict.fromkeys(alf1.simbolos + alf2.simbolos))
    return AlfabetoExplicito(*simbolos_unidos)


if __name__ == "__main__":
    # Ejemplos de uso
    print("=" * 70)
    print("EJEMPLOS DE USO - Módulo alfabetos.py")
    print("=" * 70)
    
    # Alfabeto explícito
    print("\n1. Alfabeto explícito:")
    alf_exp = crear_alfabeto_explicito('a', 'b', 'c', 'd')
    print(f"   {alf_exp}")
    print(f"   Índices: {alf_exp.indices}")
    
    # Alfabeto estándar binario
    print("\n2. Alfabeto binario:")
    alf_bin = AlfabetosPredefinidos.binario()
    print(f"   {alf_bin}")
    print(f"   Palabras de longitud 3: {alf_bin.generar_palabras(3)}")
    
    # Alfabeto hexadecimal
    print("\n3. Alfabeto hexadecimal:")
    alf_hex = AlfabetosPredefinidos.hexadecimal()
    print(f"   {alf_hex}")
    print(f"   Símbolo en posición 15: {alf_hex.simbolo_en(15)}")
    
    # Validación de palabras
    print("\n4. Validación de palabras:")
    palabra = "CAFE"
    es_valida = alf_hex.validar_palabra(palabra)
    print(f"   ¿'{palabra}' es válida en hexadecimal? {es_valida}")
    
    # Comparación de símbolos
    print("\n5. Comparación de símbolos:")
    alf_dec = AlfabetosPredefinidos.decimal()
    print(f"   Alfabeto: {alf_dec}")
    print(f"   ¿'3' < '7'? {alf_dec.es_menor('3', '7')}")
    print(f"   ¿'5' = '5'? {alf_dec.es_igual('5', '5')}")
    print(f"   ¿'9' > '2'? {alf_dec.es_mayor('9', '2')}")
    print(f"   comparar_simbolos('4', '6'): {alf_dec.comparar_simbolos('4', '6')}")
    
    # Comparación lexicográfica
    print("\n6. Comparación lexicográfica de palabras:")
    print(f"   comparar_palabras('123', '456'): {alf_dec.comparar_palabras_lexicografico('123', '456')}")
    print(f"   comparar_palabras('999', '999'): {alf_dec.comparar_palabras_lexicografico('999', '999')}")
    print(f"   comparar_palabras('789', '123'): {alf_dec.comparar_palabras_lexicografico('789', '123')}")
    
    # Comparación binaria
    print("\n7. Comparación en binario:")
    print(f"   Alfabeto: {alf_bin}")
    print(f"   comparar_palabras('101', '110'): {alf_bin.comparar_palabras_lexicografico('101', '110')}")
    print(f"   comparar_palabras('1111', '10'): {alf_bin.comparar_palabras_lexicografico('1111', '10')}")
    
    print("\n" + "=" * 70)
