"""
demo_semantica.py

Demostración de semántica como orden parcial sobre lenguajes.

Muestra diferentes tipos de órdenes semánticos:
- Orden lexicográfico
- Orden por peso de Hamming
- Orden por longitud
- Orden personalizado
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.alfabetos import AlfabetosPredefinidos
from core.lenguajes import LenguajeUniverso, LenguajeExplicito
from core.semantica import (
    SemanticaLexicografica,
    SemanticaPesoHamming,
    SemanticaLongitud,
    SemanticaPersonalizada,
    RelacionOrden
)


def demo_semantica_lexicografica():
    """Orden lexicográfico sobre palabras binarias."""
    print("=" * 70)
    print("SEMÁNTICA LEXICOGRÁFICA")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    L = LenguajeUniverso(alf, longitud=3)
    sem = SemanticaLexicografica(L, alf)
    
    print(f"\nLenguaje: {L.enumerar()}")
    print(f"Orden: lexicográfico según alfabeto {alf.simbolos}")
    
    # Elementos extremos
    print(f"\n⊥ (mínimo): {sem.minimo()}")
    print(f"⊤ (máximo): {sem.maximo()}")
    
    # Comparaciones
    print("\nComparaciones:")
    pares = [
        ("000", "001"),
        ("001", "010"),
        ("101", "110"),
        ("110", "111")
    ]
    
    for w1, w2 in pares:
        rel = sem.comparar(w1, w2)
        simbolo = "<" if rel == RelacionOrden.MENOR else ">" if rel == RelacionOrden.MAYOR else "="
        print(f"   {w1} {simbolo} {w2}")
    
    # Ordenar palabras
    palabras_desordenadas = ["111", "000", "010", "101"]
    palabras_ordenadas = sem.ordenar(palabras_desordenadas)
    print(f"\nOrdenar {palabras_desordenadas}:")
    print(f"   → {palabras_ordenadas}")
    
    print()


def demo_semantica_peso_hamming():
    """Orden por peso de Hamming."""
    print("=" * 70)
    print("SEMÁNTICA POR PESO DE HAMMING")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    L = LenguajeUniverso(alf, longitud=4)
    sem = SemanticaPesoHamming(L)
    
    print(f"\nLenguaje: palabras de longitud 4 sobre {alf.simbolos}")
    print(f"Orden: por peso de Hamming w_H(w)")
    
    # Elementos extremos
    print(f"\n⊥ (mínimo): {sem.minimo()} (peso 0)")
    print(f"⊤ (máximo): {sem.maximo()} (peso 4)")
    
    # Comparaciones
    print("\nComparaciones:")
    comparaciones = [
        ("0000", "0001", "peso 0 < peso 1"),
        ("0001", "0011", "peso 1 < peso 2"),
        ("0101", "1001", "mismo peso → incomparables"),
        ("1111", "0111", "peso 4 > peso 3"),
    ]
    
    for w1, w2, desc in comparaciones:
        rel = sem.comparar(w1, w2)
        peso1 = L.peso_hamming(w1)
        peso2 = L.peso_hamming(w2)
        
        if rel == RelacionOrden.MENOR:
            simbolo = "<"
        elif rel == RelacionOrden.MAYOR:
            simbolo = ">"
        elif rel == RelacionOrden.IGUAL:
            simbolo = "="
        else:
            simbolo = "⊥"  # incomparables
        
        print(f"   {w1} (w={peso1}) {simbolo} {w2} (w={peso2})  # {desc}")
    
    # Supremo e ínfimo
    print("\nSupremo e ínfimo:")
    conjunto = {"0001", "0010", "0100"}
    sup = sem.supremo(conjunto)
    inf = sem.infimo(conjunto)
    
    print(f"   Conjunto: {conjunto}")
    print(f"   Supremo (menor cota superior): {sup}")
    print(f"   Ínfimo (mayor cota inferior): {inf}")
    
    print()


def demo_semantica_longitud():
    """Orden por longitud de palabras."""
    print("=" * 70)
    print("SEMÁNTICA POR LONGITUD")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    palabras = {"0", "1", "00", "01", "10", "11", "000", "111"}
    L = LenguajeExplicito(alf, palabras)
    sem = SemanticaLongitud(L)
    
    print(f"\nLenguaje: {sorted(L.enumerar(), key=len)}")
    print(f"Orden: por longitud |w|")
    
    # Elementos extremos
    print(f"\n⊥ (mínimo): {sem.minimo()} (longitud 1)")
    print(f"⊤ (máximo): {sem.maximo()} (longitud 3)")
    
    # Comparaciones
    print("\nComparaciones:")
    comparaciones = [
        ("0", "00", "|0| = 1 < |00| = 2"),
        ("00", "000", "|00| = 2 < |000| = 3"),
        ("00", "01", "misma longitud → incomparables"),
        ("111", "10", "|111| = 3 > |10| = 2"),
    ]
    
    for w1, w2, desc in comparaciones:
        rel = sem.comparar(w1, w2)
        
        if rel == RelacionOrden.MENOR:
            simbolo = "<"
        elif rel == RelacionOrden.MAYOR:
            simbolo = ">"
        elif rel == RelacionOrden.IGUAL:
            simbolo = "="
        else:
            simbolo = "⊥"
        
        print(f"   {w1} {simbolo} {w2}  # {desc}")
    
    print()


def demo_semantica_personalizada():
    """Orden personalizado: suma de dígitos."""
    print("=" * 70)
    print("SEMÁNTICA PERSONALIZADA: SUMA DE DÍGITOS")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.decimal()
    L = LenguajeUniverso(alf, longitud=2)
    
    # Definir orden por suma de dígitos
    def comparar_suma_digitos(w1: str, w2: str) -> RelacionOrden:
        """Compara por suma de dígitos."""
        suma1 = sum(int(c) for c in w1)
        suma2 = sum(int(c) for c in w2)
        
        if suma1 < suma2:
            return RelacionOrden.MENOR
        elif suma1 > suma2:
            return RelacionOrden.MAYOR
        elif w1 == w2:
            return RelacionOrden.IGUAL
        else:
            # Misma suma pero palabras diferentes → incomparables
            return RelacionOrden.INCOMPARABLE
    
    sem = SemanticaPersonalizada(L, comparar_suma_digitos)
    
    print(f"\nLenguaje: números de 2 dígitos (00-99)")
    print(f"Orden: por suma de dígitos Σ(w)")
    
    # Elementos extremos
    minimo = sem.minimo()
    maximo = sem.maximo()
    print(f"\n⊥ (mínimo): {minimo} (suma = {sum(int(c) for c in minimo)})")
    print(f"⊤ (máximo): {maximo} (suma = {sum(int(c) for c in maximo)})")
    
    # Comparaciones
    print("\nComparaciones:")
    comparaciones = [
        "00", "11", "23", "45", "99"
    ]
    
    for w in comparaciones:
        suma = sum(int(c) for c in w)
        print(f"   {w}: suma = {suma}")
    
    print("\nRelaciones de orden:")
    pares = [
        ("00", "11"),
        ("11", "23"),
        ("12", "21"),  # misma suma → incomparables
        ("45", "99"),
    ]
    
    for w1, w2 in pares:
        rel = sem.comparar(w1, w2)
        s1 = sum(int(c) for c in w1)
        s2 = sum(int(c) for c in w2)
        
        if rel == RelacionOrden.MENOR:
            simbolo = "<"
        elif rel == RelacionOrden.MAYOR:
            simbolo = ">"
        elif rel == RelacionOrden.IGUAL:
            simbolo = "="
        else:
            simbolo = "⊥"
        
        print(f"   {w1} (Σ={s1}) {simbolo} {w2} (Σ={s2})")
    
    print()


def demo_diagrama_hasse():
    """Visualización conceptual del diagrama de Hasse."""
    print("=" * 70)
    print("DIAGRAMA DE HASSE (CONCEPTUAL)")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    L = LenguajeUniverso(alf, longitud=3)
    sem = SemanticaPesoHamming(L)
    
    print("\nLenguaje: palabras binarias de longitud 3")
    print("Orden: por peso de Hamming")
    print("\nDiagrama de Hasse (niveles por peso):")
    
    # Agrupar por peso
    palabras = L.enumerar()
    por_peso = {}
    
    for palabra in palabras:
        peso = L.peso_hamming(palabra)
        if peso not in por_peso:
            por_peso[peso] = []
        por_peso[peso].append(palabra)
    
    # Mostrar de mayor a menor
    for peso in sorted(por_peso.keys(), reverse=True):
        nivel = por_peso[peso]
        print(f"\nPeso {peso}: {', '.join(nivel)}")
        if peso > 0:
            print("   " + "  ↑  " * len(nivel))
    
    print()


if __name__ == "__main__":
    demo_semantica_lexicografica()
    demo_semantica_peso_hamming()
    demo_semantica_longitud()
    demo_semantica_personalizada()
    demo_diagrama_hasse()
    
    print("=" * 70)
    print("✅ Demo completado")
    print("=" * 70)
