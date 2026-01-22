"""
demo_hamming.py

Demostración de distancia de Hamming en lenguajes de longitud fija.

Muestra:
- Distancia de Hamming entre pares de palabras
- Distancia mínima de códigos
- Peso de Hamming
- Capacidad de detección/corrección de errores
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.alfabetos import AlfabetosPredefinidos
from core.lenguajes import (
    LenguajeLongitudFija, 
    LenguajeExplicito,
    LenguajeExplicitoLongitudFija,
    LenguajeUniverso
)


def demo_distancia_hamming():
    """Demuestra el cálculo de distancia de Hamming."""
    print("=" * 70)
    print("DISTANCIA DE HAMMING")
    print("=" * 70)
    
    palabras = [
        ("000", "000"),
        ("000", "001"),
        ("000", "111"),
        ("101", "110"),
        ("1010", "0101")
    ]
    
    for w1, w2 in palabras:
        d = LenguajeLongitudFija.distancia_hamming(w1, w2)
        print(f"d_H({w1}, {w2}) = {d}")
    
    print()


def demo_codigo_paridad():
    """Código de paridad simple (1 bit de paridad par)."""
    print("=" * 70)
    print("CÓDIGO DE PARIDAD (4 bits datos + 1 bit paridad)")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    
    # Código de paridad: palabras de 4 bits con paridad par
    # Solo las palabras con número par de unos
    palabras_paridad = {
        "0000", "0011", "0101", "0110",
        "1001", "1010", "1100", "1111"
    }
    
    codigo = LenguajeExplicitoLongitudFija(alf, palabras_paridad, "Paridad-4")
    
    print(f"Alfabeto: {alf}")
    print(f"Longitud: {codigo.longitud}")
    print(f"Cardinal: {codigo.cardinal()}")
    print(f"Palabras válidas: {sorted(codigo.enumerar())}")
    print()
    
    # Calcular distancia mínima
    d_min = codigo.distancia_minima()
    print(f"Distancia mínima d_min = {d_min}")
    print()
    
    # Capacidad de detección/corrección
    if d_min >= 2:
        print(f"✓ Puede detectar {d_min - 1} error(es)")
    if d_min >= 3:
        t = (d_min - 1) // 2
        print(f"✓ Puede corregir {t} error(es)")
    
    print()


def demo_codigo_repeticion():
    """Código de repetición triple."""
    print("=" * 70)
    print("CÓDIGO DE REPETICIÓN TRIPLE")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    
    # Solo dos palabras: 000 y 111
    codigo = LenguajeExplicitoLongitudFija(alf, {"000", "111"}, "Rep-3")
    
    print(f"Palabras válidas: {codigo.enumerar()}")
    
    d_min = codigo.distancia_minima()
    print(f"Distancia mínima d_min = {d_min}")
    
    t = (d_min - 1) // 2
    print(f"✓ Puede detectar {d_min - 1} errores")
    print(f"✓ Puede corregir {t} error(es)")
    print()
    
    # Ejemplo de corrección de errores
    print("Ejemplo de corrección:")
    palabra_recibida = "001"  # Error en última posición
    
    distancias = []
    for palabra_valida in codigo.enumerar():
        d = codigo.distancia_hamming(palabra_recibida, palabra_valida)
        distancias.append((d, palabra_valida))
    
    distancias.sort()
    
    print(f"Palabra recibida: {palabra_recibida}")
    for d, palabra in distancias:
        print(f"  d_H({palabra_recibida}, {palabra}) = {d}")
    
    palabra_corregida = distancias[0][1]
    print(f"→ Palabra corregida: {palabra_corregida}")
    print()


def demo_peso_hamming():
    """Demuestra el peso de Hamming."""
    print("=" * 70)
    print("PESO DE HAMMING")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    L = LenguajeUniverso(alf, longitud=4)
    
    palabras = ["0000", "0001", "0011", "0111", "1111"]
    
    for palabra in palabras:
        peso = L.peso_hamming(palabra)
        print(f"w_H({palabra}) = {peso}")
    
    print()


def demo_factory_automatico():
    """Demuestra el factory automático de LenguajeExplicito."""
    print("=" * 70)
    print("FACTORY AUTOMÁTICO: LenguajeExplicito")
    print("=" * 70)
    
    alf = AlfabetosPredefinidos.binario()
    
    # Caso 1: Longitud fija (se convierte a LenguajeExplicitoLongitudFija)
    print("1. Palabras de longitud fija:")
    L1 = LenguajeExplicito(alf, {"00", "11"})
    print(f"   Tipo: {type(L1).__name__}")
    print(f"   Longitud fija: {L1.longitud_fija}")
    print(f"   Longitud: {L1.longitud}")
    
    if isinstance(L1, LenguajeLongitudFija):
        print(f"   ✓ Tiene método distancia_hamming")
        print(f"   d_H(00, 11) = {L1.distancia_hamming('00', '11')}")
    
    print()
    
    # Caso 2: Longitud variable (mantiene LenguajeExplicito)
    print("2. Palabras de longitud variable:")
    L2 = LenguajeExplicito(alf, {"0", "11", "101"})
    print(f"   Tipo: {type(L2).__name__}")
    print(f"   Longitud fija: {L2.longitud_fija}")
    print(f"   Longitud: {L2.longitud}")
    
    print()


if __name__ == "__main__":
    demo_distancia_hamming()
    demo_codigo_paridad()
    demo_codigo_repeticion()
    demo_peso_hamming()
    demo_factory_automatico()
    
    print("=" * 70)
    print("✅ Demo completado")
    print("=" * 70)
