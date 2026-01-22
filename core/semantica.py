"""
semantica.py

Módulo para definir semántica como orden parcial sobre lenguajes.

La semántica asocia significado a las palabras mediante un orden parcial
con elemento máximo, elemento mínimo y sin partes desconectadas.

Classes:
    Semantica: Clase abstracta base para órdenes semánticos
    SemanticaLexicografica: Orden lexicográfico según alfabeto
    SemanticaPesoHamming: Orden por peso de Hamming
    SemanticaLongitud: Orden por longitud de palabras
    SemanticaPersonalizada: Orden definido por función de comparación
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Set, Callable, Tuple
from enum import Enum

from core.alfabetos import Alfabeto
from core.lenguajes import Lenguaje, LenguajeLongitudFija


# ============================================================================
# ENUMERACIÓN - RELACIÓN DE ORDEN
# ============================================================================

class RelacionOrden(Enum):
    """
    Resultado de comparar dos elementos en un orden parcial.
    
    MENOR: a < b (a es estrictamente menor que b)
    IGUAL: a = b (a y b son equivalentes)
    MAYOR: a > b (a es estrictamente mayor que b)
    INCOMPARABLE: a ⊥ b (a y b no son comparables)
    """
    MENOR = -1
    IGUAL = 0
    MAYOR = 1
    INCOMPARABLE = None


# ============================================================================
# CLASE BASE - SEMÁNTICA
# ============================================================================

class Semantica(ABC):
    """
    Clase abstracta base para definir semántica como orden parcial.
    
    Una semántica es un orden parcial (L, ≤) donde:
    - L es un lenguaje formal
    - ≤ es una relación de orden parcial reflexiva, antisimétrica y transitiva
    - Existe elemento mínimo ⊥ (bottom)
    - Existe elemento máximo ⊤ (top)
    - El orden es conexo (no hay partes desconectadas)
    
    Attributes:
        lenguaje: Lenguaje sobre el que se define el orden
    """
    
    def __init__(self, lenguaje: Lenguaje):
        """
        Inicializa la semántica sobre un lenguaje.
        
        Args:
            lenguaje: Lenguaje formal sobre el que se define el orden
        """
        self._lenguaje = lenguaje
        self._cache_minimo: Optional[str] = None
        self._cache_maximo: Optional[str] = None
    
    @property
    def lenguaje(self) -> Lenguaje:
        """Retorna el lenguaje sobre el que se define la semántica."""
        return self._lenguaje
    
    @abstractmethod
    def comparar(self, palabra1: str, palabra2: str) -> RelacionOrden:
        """
        Compara dos palabras según el orden semántico.
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            RelacionOrden indicando la relación entre las palabras
            
        Raises:
            ValueError: Si alguna palabra no pertenece al lenguaje
        """
        pass
    
    def es_menor_o_igual(self, palabra1: str, palabra2: str) -> bool:
        """
        Verifica si palabra1 ≤ palabra2.
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            True si palabra1 ≤ palabra2
        """
        rel = self.comparar(palabra1, palabra2)
        return rel in (RelacionOrden.MENOR, RelacionOrden.IGUAL)
    
    def es_menor(self, palabra1: str, palabra2: str) -> bool:
        """
        Verifica si palabra1 < palabra2 (estrictamente menor).
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            True si palabra1 < palabra2
        """
        return self.comparar(palabra1, palabra2) == RelacionOrden.MENOR
    
    def es_igual(self, palabra1: str, palabra2: str) -> bool:
        """
        Verifica si palabra1 = palabra2 según el orden.
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            True si palabra1 = palabra2
        """
        return self.comparar(palabra1, palabra2) == RelacionOrden.IGUAL
    
    def es_mayor(self, palabra1: str, palabra2: str) -> bool:
        """
        Verifica si palabra1 > palabra2 (estrictamente mayor).
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            True si palabra1 > palabra2
        """
        return self.comparar(palabra1, palabra2) == RelacionOrden.MAYOR
    
    def es_comparable(self, palabra1: str, palabra2: str) -> bool:
        """
        Verifica si dos palabras son comparables.
        
        Args:
            palabra1: Primera palabra
            palabra2: Segunda palabra
            
        Returns:
            True si las palabras son comparables
        """
        return self.comparar(palabra1, palabra2) != RelacionOrden.INCOMPARABLE
    
    def minimo(self) -> str:
        """
        Retorna el elemento mínimo ⊥ (bottom) del orden.
        
        El mínimo es la palabra w tal que w ≤ v para toda v ∈ L.
        
        Returns:
            Palabra mínima del lenguaje
            
        Raises:
            ValueError: Si el lenguaje es infinito o no tiene mínimo
        """
        if self._cache_minimo is not None:
            return self._cache_minimo
        
        if self._lenguaje.cardinal() == float('inf'):
            raise ValueError("No se puede calcular mínimo de lenguaje infinito")
        
        palabras = self._lenguaje.enumerar()
        
        if not palabras:
            raise ValueError("El lenguaje vacío no tiene elemento mínimo")
        
        # Buscar palabra que sea menor o igual a todas
        for candidato in palabras:
            es_minimo = True
            for palabra in palabras:
                if not self.es_menor_o_igual(candidato, palabra):
                    es_minimo = False
                    break
            
            if es_minimo:
                self._cache_minimo = candidato
                return candidato
        
        raise ValueError("El lenguaje no tiene elemento mínimo")
    
    def maximo(self) -> str:
        """
        Retorna el elemento máximo ⊤ (top) del orden.
        
        El máximo es la palabra w tal que v ≤ w para toda v ∈ L.
        
        Returns:
            Palabra máxima del lenguaje
            
        Raises:
            ValueError: Si el lenguaje es infinito o no tiene máximo
        """
        if self._cache_maximo is not None:
            return self._cache_maximo
        
        if self._lenguaje.cardinal() == float('inf'):
            raise ValueError("No se puede calcular máximo de lenguaje infinito")
        
        palabras = self._lenguaje.enumerar()
        
        if not palabras:
            raise ValueError("El lenguaje vacío no tiene elemento máximo")
        
        # Buscar palabra que sea mayor o igual a todas
        for candidato in palabras:
            es_maximo = True
            for palabra in palabras:
                if not self.es_menor_o_igual(palabra, candidato):
                    es_maximo = False
                    break
            
            if es_maximo:
                self._cache_maximo = candidato
                return candidato
        
        raise ValueError("El lenguaje no tiene elemento máximo")
    
    def supremo(self, conjunto: Set[str]) -> Optional[str]:
        """
        Calcula el supremo (menor cota superior) de un conjunto.
        
        El supremo de S es la menor palabra w tal que s ≤ w para todo s ∈ S.
        
        Args:
            conjunto: Conjunto de palabras del lenguaje
            
        Returns:
            Supremo del conjunto, o None si no existe
        """
        if not conjunto:
            return self.minimo()
        
        palabras = self._lenguaje.enumerar()
        
        # Encontrar cotas superiores
        cotas_superiores = []
        for candidato in palabras:
            es_cota = True
            for elemento in conjunto:
                if not self.es_menor_o_igual(elemento, candidato):
                    es_cota = False
                    break
            
            if es_cota:
                cotas_superiores.append(candidato)
        
        if not cotas_superiores:
            return None
        
        # Encontrar la menor cota superior
        for cota in cotas_superiores:
            es_minima = True
            for otra_cota in cotas_superiores:
                if self.es_menor(otra_cota, cota):
                    es_minima = False
                    break
            
            if es_minima:
                return cota
        
        return None
    
    def infimo(self, conjunto: Set[str]) -> Optional[str]:
        """
        Calcula el ínfimo (mayor cota inferior) de un conjunto.
        
        El ínfimo de S es la mayor palabra w tal que w ≤ s para todo s ∈ S.
        
        Args:
            conjunto: Conjunto de palabras del lenguaje
            
        Returns:
            Ínfimo del conjunto, o None si no existe
        """
        if not conjunto:
            return self.maximo()
        
        palabras = self._lenguaje.enumerar()
        
        # Encontrar cotas inferiores
        cotas_inferiores = []
        for candidato in palabras:
            es_cota = True
            for elemento in conjunto:
                if not self.es_menor_o_igual(candidato, elemento):
                    es_cota = False
                    break
            
            if es_cota:
                cotas_inferiores.append(candidato)
        
        if not cotas_inferiores:
            return None
        
        # Encontrar la mayor cota inferior
        for cota in cotas_inferiores:
            es_maxima = True
            for otra_cota in cotas_inferiores:
                if self.es_mayor(otra_cota, cota):
                    es_maxima = False
                    break
            
            if es_maxima:
                return cota
        
        return None
    
    def ordenar(self, palabras: List[str]) -> List[str]:
        """
        Ordena una lista de palabras según el orden semántico.
        
        Args:
            palabras: Lista de palabras a ordenar
            
        Returns:
            Lista ordenada (solo palabras comparables)
        """
        # Usar ordenamiento de burbuja adaptado para orden parcial
        resultado = palabras.copy()
        n = len(resultado)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                rel = self.comparar(resultado[j], resultado[j + 1])
                if rel == RelacionOrden.MAYOR:
                    resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
        
        return resultado


# ============================================================================
# SEMÁNTICA LEXICOGRÁFICA
# ============================================================================

class SemanticaLexicografica(Semantica):
    """
    Orden lexicográfico según el orden del alfabeto.
    
    Compara palabras símbolo por símbolo de izquierda a derecha.
    Si una palabra es prefijo de otra, la más corta es menor.
    
    Example:
        >>> alf = AlfabetosPredefinidos.binario()
        >>> L = LenguajeUniverso(alf, longitud=2)
        >>> sem = SemanticaLexicografica(L, alf)
        >>> sem.comparar("00", "01")
        RelacionOrden.MENOR
        >>> sem.minimo()
        '00'
        >>> sem.maximo()
        '11'
    """
    
    def __init__(self, lenguaje: Lenguaje, alfabeto: Alfabeto):
        """
        Inicializa semántica lexicográfica.
        
        Args:
            lenguaje: Lenguaje sobre el que se define
            alfabeto: Alfabeto que define el orden de símbolos
        """
        super().__init__(lenguaje)
        self._alfabeto = alfabeto
    
    def comparar(self, palabra1: str, palabra2: str) -> RelacionOrden:
        """Compara lexicográficamente."""
        if not self._lenguaje.pertenece(palabra1):
            raise ValueError(f"'{palabra1}' no pertenece al lenguaje")
        if not self._lenguaje.pertenece(palabra2):
            raise ValueError(f"'{palabra2}' no pertenece al lenguaje")
        
        resultado = self._alfabeto.comparar_palabras_lexicografico(palabra1, palabra2)
        
        if resultado < 0:
            return RelacionOrden.MENOR
        elif resultado > 0:
            return RelacionOrden.MAYOR
        else:
            return RelacionOrden.IGUAL


# ============================================================================
# SEMÁNTICA POR PESO DE HAMMING
# ============================================================================

class SemanticaPesoHamming(Semantica):
    """
    Orden por peso de Hamming (número de símbolos no nulos).
    
    Solo aplicable a lenguajes de longitud fija.
    Palabras con menor peso son menores en el orden.
    Palabras con mismo peso son incomparables.
    
    Example:
        >>> alf = AlfabetosPredefinidos.binario()
        >>> L = LenguajeUniverso(alf, longitud=3)
        >>> sem = SemanticaPesoHamming(L)
        >>> sem.comparar("000", "001")  # peso 0 < peso 1
        RelacionOrden.MENOR
        >>> sem.comparar("001", "010")  # mismo peso
        RelacionOrden.INCOMPARABLE
    """
    
    def __init__(self, lenguaje: LenguajeLongitudFija):
        """
        Inicializa semántica por peso de Hamming.
        
        Args:
            lenguaje: Lenguaje de longitud fija
            
        Raises:
            TypeError: Si el lenguaje no es de longitud fija
        """
        if not isinstance(lenguaje, LenguajeLongitudFija):
            raise TypeError("SemanticaPesoHamming requiere LenguajeLongitudFija")
        
        super().__init__(lenguaje)
    
    def comparar(self, palabra1: str, palabra2: str) -> RelacionOrden:
        """Compara por peso de Hamming."""
        if not self._lenguaje.pertenece(palabra1):
            raise ValueError(f"'{palabra1}' no pertenece al lenguaje")
        if not self._lenguaje.pertenece(palabra2):
            raise ValueError(f"'{palabra2}' no pertenece al lenguaje")
        
        peso1 = self._lenguaje.peso_hamming(palabra1)
        peso2 = self._lenguaje.peso_hamming(palabra2)
        
        if peso1 < peso2:
            return RelacionOrden.MENOR
        elif peso1 > peso2:
            return RelacionOrden.MAYOR
        elif palabra1 == palabra2:
            return RelacionOrden.IGUAL
        else:
            # Mismo peso pero palabras diferentes → incomparables
            return RelacionOrden.INCOMPARABLE


# ============================================================================
# SEMÁNTICA POR LONGITUD
# ============================================================================

class SemanticaLongitud(Semantica):
    """
    Orden por longitud de palabras.
    
    Palabras más cortas son menores.
    Palabras de misma longitud son incomparables.
    
    Example:
        >>> alf = AlfabetosPredefinidos.binario()
        >>> L = LenguajeExplicito(alf, {"0", "00", "000", "01", "10"})
        >>> sem = SemanticaLongitud(L)
        >>> sem.comparar("0", "00")
        RelacionOrden.MENOR
        >>> sem.comparar("00", "01")  # misma longitud
        RelacionOrden.INCOMPARABLE
    """
    
    def comparar(self, palabra1: str, palabra2: str) -> RelacionOrden:
        """Compara por longitud."""
        if not self._lenguaje.pertenece(palabra1):
            raise ValueError(f"'{palabra1}' no pertenece al lenguaje")
        if not self._lenguaje.pertenece(palabra2):
            raise ValueError(f"'{palabra2}' no pertenece al lenguaje")
        
        len1 = len(palabra1)
        len2 = len(palabra2)
        
        if len1 < len2:
            return RelacionOrden.MENOR
        elif len1 > len2:
            return RelacionOrden.MAYOR
        elif palabra1 == palabra2:
            return RelacionOrden.IGUAL
        else:
            # Misma longitud pero diferentes → incomparables
            return RelacionOrden.INCOMPARABLE


# ============================================================================
# SEMÁNTICA PERSONALIZADA
# ============================================================================

class SemanticaPersonalizada(Semantica):
    """
    Orden definido por función de comparación personalizada.
    
    Permite definir cualquier orden parcial mediante una función.
    
    Example:
        >>> def comparar_suma_digitos(w1, w2):
        ...     s1 = sum(int(c) for c in w1)
        ...     s2 = sum(int(c) for c in w2)
        ...     if s1 < s2: return RelacionOrden.MENOR
        ...     elif s1 > s2: return RelacionOrden.MAYOR
        ...     elif w1 == w2: return RelacionOrden.IGUAL
        ...     else: return RelacionOrden.INCOMPARABLE
        >>> 
        >>> sem = SemanticaPersonalizada(L, comparar_suma_digitos)
    """
    
    def __init__(self, lenguaje: Lenguaje, 
                 funcion_comparacion: Callable[[str, str], RelacionOrden]):
        """
        Inicializa semántica personalizada.
        
        Args:
            lenguaje: Lenguaje sobre el que se define
            funcion_comparacion: Función que compara dos palabras
        """
        super().__init__(lenguaje)
        self._funcion_comparacion = funcion_comparacion
    
    def comparar(self, palabra1: str, palabra2: str) -> RelacionOrden:
        """Compara usando la función personalizada."""
        if not self._lenguaje.pertenece(palabra1):
            raise ValueError(f"'{palabra1}' no pertenece al lenguaje")
        if not self._lenguaje.pertenece(palabra2):
            raise ValueError(f"'{palabra2}' no pertenece al lenguaje")
        
        return self._funcion_comparacion(palabra1, palabra2)


if __name__ == "__main__":
    # Ejemplos de uso
    from core.alfabetos import AlfabetosPredefinidos
    from core.lenguajes import LenguajeUniverso
    
    print("=" * 70)
    print("EJEMPLOS DE USO - Módulo semantica.py")
    print("=" * 70)
    
    # Semántica lexicográfica
    print("\n1. Semántica lexicográfica:")
    alf = AlfabetosPredefinidos.binario()
    L = LenguajeUniverso(alf, longitud=2)
    sem_lex = SemanticaLexicografica(L, alf)
    
    print(f"   Lenguaje: {L.enumerar()}")
    print(f"   Mínimo: {sem_lex.minimo()}")
    print(f"   Máximo: {sem_lex.maximo()}")
    print(f"   '00' < '01': {sem_lex.es_menor('00', '01')}")
    print(f"   '11' > '10': {sem_lex.es_mayor('11', '10')}")
    
    # Semántica por peso de Hamming
    print("\n2. Semántica por peso de Hamming:")
    L3 = LenguajeUniverso(alf, longitud=3)
    sem_peso = SemanticaPesoHamming(L3)
    
    print(f"   '000' vs '001': {sem_peso.comparar('000', '001')}")
    print(f"   '001' vs '010': {sem_peso.comparar('001', '010')}")
    print(f"   Mínimo: {sem_peso.minimo()}")
    print(f"   Máximo: {sem_peso.maximo()}")
    
    print("\n" + "=" * 70)
