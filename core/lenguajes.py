"""
lenguajes.py

Módulo para lenguajes formales sobre alfabetos - Enfoque práctico.

Implementa lenguajes de longitud fija y casos especiales de longitud infinita,
con soporte para predicados, autómatas y operaciones sobre lenguajes.

Classes:
    EstadoDecision: Enum para estados de autómatas
    Lenguaje: Clase base para lenguajes
    LenguajeUniverso: Σ^l - todas las palabras de longitud l
    LenguajePredicado: Lenguaje definido por función predicado
    LenguajeAutomata: Lenguaje definido por máquina de estados
    LenguajeExplicito: Lenguaje con lista explícita de palabras
    LenguajeInfinito: Lenguajes de longitud infinita
"""

from abc import ABC, abstractmethod
from typing import Set, List, Optional, Callable, Union
from enum import Enum

from alfabetos import Alfabeto, AlfabetosPredefinidos


# ============================================================================
# ESTADO DE DECISIÓN
# ============================================================================

class EstadoDecision(Enum):
    """
    Estados posibles de decisión para autómatas.
    
    ACEPTAR: La palabra pertenece al lenguaje
    RECHAZAR: La palabra NO pertenece al lenguaje
    INDETERMINADO: No se puede decidir
    """
    ACEPTAR = "aceptar"
    RECHAZAR = "rechazar"
    INDETERMINADO = "indeterminado"


# ============================================================================
# CLASE BASE - LENGUAJE
# ============================================================================

class Lenguaje(ABC):
    """
    Clase abstracta base para representar lenguajes formales.
    
    Un lenguaje L sobre alfabeto Σ es un conjunto de palabras.
    """
    
    def __init__(self, alfabeto: Alfabeto, longitud_fija: bool = False, 
                 longitud: Optional[int] = None):
        self._alfabeto = alfabeto
        self._longitud_fija = longitud_fija
        self._longitud = longitud
    
    @property
    def alfabeto(self) -> Alfabeto:
        return self._alfabeto
    
    @property
    def longitud_fija(self) -> bool:
        return self._longitud_fija
    
    @property
    def longitud(self) -> Optional[int]:
        return self._longitud
    
    @abstractmethod
    def pertenece(self, palabra: str) -> bool:
        """Verifica si palabra ∈ L"""
        pass
    
    @abstractmethod
    def cardinal(self) -> Union[int, float]:
        """Retorna |L| (float('inf') si infinito)"""
        pass
    
    @abstractmethod
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        """Enumera palabras del lenguaje"""
        pass
    
    def es_vacio(self) -> bool:
        """Verifica si el lenguaje es vacío (L = ∅)"""
        return self.cardinal() == 0
    
    def es_sublenguaje_de(self, otro: 'Lenguaje') -> bool:
        """
        Verifica si este lenguaje es subconjunto de otro: L1 ⊆ L2
        
        Significa que todas las palabras de L1 están en L2.
        Solo funciona para lenguajes finitos.
        
        Args:
            otro: Lenguaje a comparar
            
        Returns:
            bool: True si L1 ⊆ L2
            
        Raises:
            ValueError: Si alguno de los lenguajes es infinito
        """
        if not self.es_finito() or not otro.es_finito():
            raise ValueError("Solo se puede verificar con lenguajes finitos")
        
        # Verificar que todos los elementos de self están en otro
        return all(otro.pertenece(palabra) for palabra in self.enumerar())
    
    def es_superlenguaje_de(self, otro: 'Lenguaje') -> bool:
        """
        Verifica si este lenguaje contiene a otro: L1 ⊇ L2
        Equivalente a: otro ⊆ self
        """
        return otro.es_sublenguaje_de(self)
    
    def es_igual_a(self, otro: 'Lenguaje') -> bool:
        """
        Verifica si dos lenguajes son iguales: L1 = L2
        Dos lenguajes son iguales si L1 ⊆ L2 y L2 ⊆ L1
        """
        if not self.es_finito() or not otro.es_finito():
            raise ValueError("Solo se puede verificar con lenguajes finitos")
        
        return (self.cardinal() == otro.cardinal() and 
                self.es_sublenguaje_de(otro))
    
    def es_finito(self) -> bool:
        """Verifica si el lenguaje es finito."""
        return self.cardinal() != float('inf')
    
    def __contains__(self, palabra: str) -> bool:
        return self.pertenece(palabra)
    
    def __len__(self) -> int:
        card = self.cardinal()
        if card == float('inf'):
            raise ValueError("El lenguaje es infinito")
        return int(card)
    
    def __le__(self, otro: 'Lenguaje') -> bool:
        """Operador <= para L1 ⊆ L2"""
        return self.es_sublenguaje_de(otro)
    
    def __ge__(self, otro: 'Lenguaje') -> bool:
        """Operador >= para L1 ⊇ L2"""
        return self.es_superlenguaje_de(otro)
    
    def __eq__(self, otro: object) -> bool:
        """Operador == para L1 = L2"""
        if not isinstance(otro, Lenguaje):
            return False
        try:
            return self.es_igual_a(otro)
        except:
            return False


# ============================================================================
# LENGUAJE VACÍO
# ============================================================================

class LenguajeVacio(Lenguaje):
    """
    Lenguaje vacío ∅: no contiene ninguna palabra.
    
    Es único para cada alfabeto y longitud.
    
    Propiedades:
    - |∅| = 0
    - ∅ ⊆ L para todo lenguaje L
    - ∅ ∪ L = L
    - ∅ ∩ L = ∅
    
    Example:
        >>> alf = AlfabetosPredefinidos.binario()
        >>> vacio = LenguajeVacio(alf, longitud=3)
        >>> vacio.cardinal()
        0
        >>> '000' in vacio
        False
    """
    
    # Singleton pattern: un solo lenguaje vacío por (alfabeto, longitud)
    _instancias: dict = {}
    
    def __new__(cls, alfabeto: Alfabeto, longitud: Optional[int] = None):
        """Implementa singleton por alfabeto y longitud."""
        clave = (id(alfabeto), longitud)
        if clave not in cls._instancias:
            instancia = super().__new__(cls)
            cls._instancias[clave] = instancia
        return cls._instancias[clave]
    
    def __init__(self, alfabeto: Alfabeto, longitud: Optional[int] = None):
        """
        Inicializa el lenguaje vacío.
        
        Args:
            alfabeto: Alfabeto del lenguaje
            longitud: Longitud fija (None para cualquier longitud)
        """
        if not hasattr(self, '_inicializado'):
            super().__init__(alfabeto, longitud_fija=(longitud is not None), 
                           longitud=longitud)
            self._inicializado = True
    
    def pertenece(self, palabra: str) -> bool:
        """Ninguna palabra pertenece al lenguaje vacío."""
        return False
    
    def cardinal(self) -> int:
        """El cardinal del lenguaje vacío es 0."""
        return 0
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        """No hay palabras para enumerar."""
        return []
    
    def __str__(self) -> str:
        """Representación del lenguaje vacío."""
        return "∅ (lenguaje vacío)"
    
    def __repr__(self) -> str:
        return "LenguajeVacio()"


# ============================================================================
# LENGUAJE UNIVERSO - Σ^l
# ============================================================================

class LenguajeUniverso(Lenguaje):
    """
    Lenguaje universo Σ^l: todas las palabras de longitud l.
    Cardinal: n^l donde n = |Σ|
    """
    
    def __init__(self, alfabeto: Alfabeto, longitud: int):
        if longitud < 0:
            raise ValueError("La longitud debe ser >= 0")
        super().__init__(alfabeto, longitud_fija=True, longitud=longitud)
        self._palabras: Optional[List[str]] = None
    
    def pertenece(self, palabra: str) -> bool:
        return (len(palabra) == self._longitud and 
                self._alfabeto.validar_palabra(palabra))
    
    def cardinal(self) -> int:
        return len(self._alfabeto) ** self._longitud
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        if self._palabras is None:
            self._palabras = self._alfabeto.generar_palabras(self._longitud)
        return self._palabras[:limite] if limite else self._palabras.copy()


# ============================================================================
# LENGUAJE PREDICADO
# ============================================================================

class LenguajePredicado(Lenguaje):
    """
    Sublenguaje de Σ^l definido por predicado: L = {w ∈ Σ^l | P(w) = True}
    """
    
    def __init__(self, alfabeto: Alfabeto, longitud: int, 
                 predicado: Callable[[str], bool], nombre: str = ""):
        super().__init__(alfabeto, longitud_fija=True, longitud=longitud)
        self._predicado = predicado
        self._nombre = nombre
        self._universo = LenguajeUniverso(alfabeto, longitud)
        self._palabras: Optional[List[str]] = None
    
    def pertenece(self, palabra: str) -> bool:
        return (self._universo.pertenece(palabra) and 
                self._predicado(palabra))
    
    def cardinal(self) -> int:
        return len(self.enumerar())
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        if self._palabras is None:
            self._palabras = [w for w in self._universo.enumerar() 
                            if self._predicado(w)]
        return self._palabras[:limite] if limite else self._palabras.copy()


# ============================================================================
# LENGUAJE AUTÓMATA
# ============================================================================

class LenguajeAutomata(Lenguaje):
    """
    Lenguaje definido por autómata que retorna EstadoDecision.
    """
    
    def __init__(self, alfabeto: Alfabeto, 
                 automata: Callable[[str], EstadoDecision],
                 longitud: Optional[int] = None, nombre: str = ""):
        super().__init__(alfabeto, longitud_fija=(longitud is not None), 
                        longitud=longitud)
        self._automata = automata
        self._nombre = nombre
        
        if longitud is not None:
            self._universo = LenguajeUniverso(alfabeto, longitud)
    
    def pertenece(self, palabra: str) -> bool:
        if not self._alfabeto.validar_palabra(palabra):
            return False
        if self._longitud_fija and len(palabra) != self._longitud:
            return False
        return self._automata(palabra) == EstadoDecision.ACEPTAR
    
    def decidir(self, palabra: str) -> EstadoDecision:
        """Retorna el estado de decisión completo."""
        if not self._alfabeto.validar_palabra(palabra):
            return EstadoDecision.RECHAZAR
        if self._longitud_fija and len(palabra) != self._longitud:
            return EstadoDecision.RECHAZAR
        return self._automata(palabra)
    
    def combinar_con(self, otro_automata: Callable[[str], EstadoDecision]) -> 'LenguajeAutomata':
        """
        Combina este autómata con otro para reducir casos INDETERMINADO.
        
        Estrategia:
        - Si este autómata retorna ACEPTAR o RECHAZAR, usar ese resultado
        - Si retorna INDETERMINADO, consultar el otro autómata
        
        Args:
            otro_automata: Segundo autómata a consultar
            
        Returns:
            LenguajeAutomata: Nuevo lenguaje con autómata combinado
        """
        def automata_combinado(palabra: str) -> EstadoDecision:
            resultado1 = self._automata(palabra)
            if resultado1 != EstadoDecision.INDETERMINADO:
                return resultado1
            return otro_automata(palabra)
        
        nombre = f"{self._nombre}_combinado" if self._nombre else "combinado"
        return LenguajeAutomata(self._alfabeto, automata_combinado, 
                               self._longitud, nombre)
    
    def cardinal(self) -> Union[int, float]:
        if not self._longitud_fija:
            return float('inf')
        return len(self.enumerar())
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        if not self._longitud_fija:
            raise ValueError("No se puede enumerar sin longitud fija")
        palabras = [w for w in self._universo.enumerar()
                   if self._automata(w) == EstadoDecision.ACEPTAR]
        return palabras[:limite] if limite else palabras


# ============================================================================
# LENGUAJE EXPLÍCITO
# ============================================================================

class LenguajeExplicito(Lenguaje):
    """
    Lenguaje definido por lista explícita de palabras.
    """
    
    def __init__(self, alfabeto: Alfabeto, palabras: Set[str], nombre: str = ""):
        longitudes = {len(p) for p in palabras}
        longitud_fija = len(longitudes) <= 1
        longitud = longitudes.pop() if longitud_fija and longitudes else None
        
        super().__init__(alfabeto, longitud_fija, longitud)
        
        for palabra in palabras:
            if not alfabeto.validar_palabra(palabra):
                raise ValueError(f"Palabra '{palabra}' no válida")
        
        self._palabras = set(palabras)
        self._nombre = nombre
    
    def pertenece(self, palabra: str) -> bool:
        return palabra in self._palabras
    
    def cardinal(self) -> int:
        return len(self._palabras)
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        palabras = sorted(list(self._palabras))
        return palabras[:limite] if limite else palabras


# ============================================================================
# LENGUAJE INFINITO
# ============================================================================

class LenguajeInfinito(Lenguaje):
    """
    Lenguaje de longitud infinita - casos especiales.
    """
    
    def __init__(self, alfabeto: Alfabeto, nombre: str = ""):
        super().__init__(alfabeto, longitud_fija=False, longitud=None)
        self._nombre = nombre
    
    def cardinal(self) -> float:
        return float('inf')
    
    @abstractmethod
    def generar_hasta(self, n: int) -> List[str]:
        """Genera las primeras n palabras."""
        pass
    
    def enumerar(self, limite: Optional[int] = None) -> List[str]:
        return self.generar_hasta(limite if limite else 100)


class LenguajeNaturalesBinario(LenguajeInfinito):
    """
    Lenguaje de naturales en binario sin ceros a la izquierda.
    """
    
    def __init__(self):
        super().__init__(AlfabetosPredefinidos.binario(), "Naturales Binario")
    
    def pertenece(self, palabra: str) -> bool:
        if not self._alfabeto.validar_palabra(palabra):
            return False
        if palabra == '' or palabra == '0':
            return True
        return palabra[0] == '1'
    
    def generar_hasta(self, n: int) -> List[str]:
        return [bin(i)[2:] for i in range(n)]


# ============================================================================
# OPERACIONES SOBRE LENGUAJES
# ============================================================================

def union(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado:
    """L1 ∪ L2"""
    if L1.alfabeto != L2.alfabeto or L1.longitud != L2.longitud:
        raise ValueError("Alfabetos y longitudes deben coincidir")
    predicado = lambda w: L1.pertenece(w) or L2.pertenece(w)
    return LenguajePredicado(L1.alfabeto, L1.longitud, predicado, "L1 ∪ L2")

def interseccion(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado:
    """L1 ∩ L2"""
    if L1.alfabeto != L2.alfabeto or L1.longitud != L2.longitud:
        raise ValueError("Alfabetos y longitudes deben coincidir")
    predicado = lambda w: L1.pertenece(w) and L2.pertenece(w)
    return LenguajePredicado(L1.alfabeto, L1.longitud, predicado, "L1 ∩ L2")

def complemento(L: Lenguaje) -> LenguajePredicado:
    r"""L̄ = Σ^l \ L"""
    if not L.longitud_fija:
        raise ValueError("Solo para longitud fija")
    predicado = lambda w: not L.pertenece(w)
    return LenguajePredicado(L.alfabeto, L.longitud, predicado, "L̄")

def diferencia(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado:
    r"""L1 \ L2 = L1 - L2 = {w | w ∈ L1 y w ∉ L2}"""
    if L1.alfabeto != L2.alfabeto or L1.longitud != L2.longitud:
        raise ValueError("Alfabetos y longitudes deben coincidir")
    predicado = lambda w: L1.pertenece(w) and not L2.pertenece(w)
    return LenguajePredicado(L1.alfabeto, L1.longitud, predicado, r"L1 \ L2")

def diferencia_simetrica(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado:
    r"""L1 △ L2 = (L1 \ L2) ∪ (L2 \ L1) = {w | w ∈ L1 XOR w ∈ L2}"""
    if L1.alfabeto != L2.alfabeto or L1.longitud != L2.longitud:
        raise ValueError("Alfabetos y longitudes deben coincidir")
    predicado = lambda w: L1.pertenece(w) != L2.pertenece(w)
    return LenguajePredicado(L1.alfabeto, L1.longitud, predicado, "L1 △ L2")

def concatenacion(L1: Lenguaje, L2: Lenguaje) -> 'LenguajeExplicito':
    """
    Concatenación de lenguajes: L1 · L2 = {w1w2 | w1 ∈ L1, w2 ∈ L2}
    
    Solo funciona para lenguajes finitos.
    """
    if not L1.es_finito() or not L2.es_finito():
        raise ValueError("Solo se puede concatenar lenguajes finitos")
    
    if L1.alfabeto != L2.alfabeto:
        raise ValueError("Los alfabetos deben coincidir")
    
    palabras_concat = {w1 + w2 for w1 in L1.enumerar() for w2 in L2.enumerar()}
    return LenguajeExplicito(L1.alfabeto, palabras_concat, "L1·L2")

def potencia(L: Lenguaje, n: int) -> 'LenguajeExplicito':
    """
    Potencia de un lenguaje: L^n = L · L · ... · L (n veces)
    
    L^0 = {ε} (cadena vacía)
    L^1 = L
    L^2 = L · L
    ...
    
    Solo funciona para lenguajes finitos.
    """
    if not L.es_finito():
        raise ValueError("Solo se puede calcular potencia de lenguajes finitos")
    
    if n < 0:
        raise ValueError("El exponente debe ser >= 0")
    
    if n == 0:
        return LenguajeExplicito(L.alfabeto, {''}, "L^0")
    
    if n == 1:
        return LenguajeExplicito(L.alfabeto, set(L.enumerar()), "L^1")
    
    # Calcular L^n mediante concatenaciones sucesivas
    resultado = LenguajeExplicito(L.alfabeto, set(L.enumerar()), "L")
    for i in range(n - 1):
        resultado = concatenacion(resultado, L)
    
    return LenguajeExplicito(L.alfabeto, set(resultado.enumerar()), f"L^{n}")

def producto_cartesiano(L1: Lenguaje, L2: Lenguaje, 
                        separador: str = ',') -> 'LenguajeExplicito':
    """
    Producto cartesiano de lenguajes: L1 × L2 = {(w1, w2) | w1 ∈ L1, w2 ∈ L2}
    
    Representado como palabras con separador.
    """
    if not L1.es_finito() or not L2.es_finito():
        raise ValueError("Solo se puede calcular producto de lenguajes finitos")
    
    palabras_producto = {f"{w1}{separador}{w2}" 
                         for w1 in L1.enumerar() 
                         for w2 in L2.enumerar()}
    
    # Crear alfabeto extendido que incluye el separador
    simbolos_L1 = set(''.join(L1.enumerar()))
    simbolos_L2 = set(''.join(L2.enumerar()))
    # Nota: esto es una simplificación, en teoría necesitaríamos un alfabeto más complejo
    
    return LenguajeExplicito(L1.alfabeto, palabras_producto, "L1×L2")


# ============================================================================
# EJEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EJEMPLOS - Lenguajes Formales")
    print("=" * 70)
    
    alf_bin = AlfabetosPredefinidos.binario()
    
    # Universo
    print("\n1. Lenguaje Universo Σ^3:")
    L_univ = LenguajeUniverso(alf_bin, 3)
    print(f"   Cardinal: {L_univ.cardinal()}")
    print(f"   Palabras: {L_univ.enumerar()}")
    
    # Predicado
    print("\n2. Lenguaje con Predicado (paridad par):")
    L_par = LenguajePredicado(alf_bin, 4, lambda w: w.count('1') % 2 == 0)
    print(f"   Cardinal: {L_par.cardinal()}")
    print(f"   Palabras: {L_par.enumerar()}")
    
    # Explícito
    print("\n3. Lenguaje Explícito (BCD parcial):")
    L_bcd = LenguajeExplicito(alf_bin, {'0000', '0001', '0010', '0011'})
    print(f"   Cardinal: {L_bcd.cardinal()}")
    print(f"   Palabras: {L_bcd.enumerar()}")
    
    # Infinito
    print("\n4. Lenguaje Infinito (Naturales):")
    L_nat = LenguajeNaturalesBinario()
    print(f"   Primeras 10: {L_nat.generar_hasta(10)}")
    
    # Lenguaje vacío
    print("\n5. Lenguaje Vacío:")
    L_vacio = LenguajeVacio(alf_bin, longitud=3)
    print(f"   {L_vacio}")
    print(f"   Cardinal: {L_vacio.cardinal()}")
    print(f"   '000' ∈ ∅: {'000' in L_vacio}")
    print(f"   ¿Es vacío?: {L_vacio.es_vacio()}")
    
    # Relaciones entre lenguajes
    print("\n6. Relaciones entre lenguajes:")
    L1 = LenguajeExplicito(alf_bin, {'00', '01'}, "L1")
    L2 = LenguajeExplicito(alf_bin, {'00', '01', '10'}, "L2")
    L3 = LenguajeUniverso(alf_bin, 2)
    
    print(f"   L1 = {L1.enumerar()}")
    print(f"   L2 = {L2.enumerar()}")
    print(f"   L3 (universo) = {L3.enumerar()}")
    print(f"   L1 ⊆ L2: {L1.es_sublenguaje_de(L2)}")
    print(f"   L2 ⊆ L1: {L2.es_sublenguaje_de(L1)}")
    print(f"   L1 ⊆ L3: {L1.es_sublenguaje_de(L3)}")
    print(f"   ∅ ⊆ L1: {L_vacio.es_sublenguaje_de(L1)}")
    print(f"   L1 = L2: {L1.es_igual_a(L2)}")
    
    # Operadores
    print("\n7. Usando operadores (<=, >=, ==):")
    print(f"   L1 <= L2: {L1 <= L2}")
    print(f"   L2 >= L1: {L2 >= L1}")
    
    # Combinación de autómatas
    print("\n8. Combinación de autómatas:")
    
    def automata1(w: str) -> EstadoDecision:
        """Acepta si tiene número par de unos, indeterminado si > 5 bits"""
        if len(w) > 5:
            return EstadoDecision.INDETERMINADO
        return (EstadoDecision.ACEPTAR if w.count('1') % 2 == 0 
                else EstadoDecision.RECHAZAR)
    
    def automata2(w: str) -> EstadoDecision:
        """Acepta si empieza con 0"""
        if not w:
            return EstadoDecision.RECHAZAR
        return (EstadoDecision.ACEPTAR if w[0] == '0' 
                else EstadoDecision.RECHAZAR)
    
    L_auto1 = LenguajeAutomata(alf_bin, automata1, longitud=3, nombre="paridad")
    L_auto2 = LenguajeAutomata(alf_bin, automata2, longitud=3, nombre="empieza_0")
    L_combinado = L_auto1.combinar_con(automata2)
    
    print(f"   L_auto1 (paridad par): {L_auto1.enumerar()}")
    print(f"   L_auto2 (empieza con 0): {L_auto2.enumerar()}")
    
    # Pertenencia de palabras
    print("\n9. Pertenencia de palabras:")
    palabra = "101"
    print(f"   '{palabra}' ∈ L1: {palabra in L1}")
    print(f"   '{palabra}' ∈ L_auto1: {palabra in L_auto1}")
    print(f"   '{palabra}' ∈ L_vacio: {palabra in L_vacio}")
    print(f"   '{palabra}' ∈ L3 (universo): {palabra in L3}")
    
    # Operaciones adicionales
    print("\n10. Operaciones: Diferencia y Diferencia Simétrica:")
    L_dif = diferencia(L2, L1)
    L_sim = diferencia_simetrica(L1, L2)
    print(f"   L2 \\ L1: {L_dif.enumerar()}")
    print(f"   L1 △ L2: {L_sim.enumerar()}")
    
    # Concatenación
    print("\n11. Operación: Concatenación:")
    L_a = LenguajeExplicito(alf_bin, {'0', '1'}, "L_a")
    L_b = LenguajeExplicito(alf_bin, {'0', '1'}, "L_b")
    L_concat = concatenacion(L_a, L_b)
    print(f"   L_a: {L_a.enumerar()}")
    print(f"   L_b: {L_b.enumerar()}")
    print(f"   L_a · L_b: {L_concat.enumerar()}")
    
    # Potencia
    print("\n12. Operación: Potencia:")
    L_base = LenguajeExplicito(alf_bin, {'0', '1'}, "L")
    L_pot0 = potencia(L_base, 0)
    L_pot1 = potencia(L_base, 1)
    L_pot2 = potencia(L_base, 2)
    print(f"   L: {L_base.enumerar()}")
    print(f"   L^0: {L_pot0.enumerar()}")
    print(f"   L^1: {L_pot1.enumerar()}")
    print(f"   L^2: {L_pot2.enumerar()}")
    
    print("\n" + "=" * 70)
    print("✅ Todas las operaciones ejecutadas correctamente")
    print("=" * 70)
