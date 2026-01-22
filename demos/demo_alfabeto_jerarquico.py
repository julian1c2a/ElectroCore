"""
demo_alfabeto_jerarquico.py

Demostración de alfabetos jerárquicos: usar palabras de un lenguaje
como símbolos de un nuevo alfabeto.

Esto permite crear jerarquías multinivel:
- Nivel 0: Símbolos básicos
- Nivel 1: Palabras sobre símbolos básicos
- Nivel 2: Palabras sobre palabras (usando L1 como alfabeto)
- Nivel 3+: Niveles adicionales de abstracción
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.alfabetos import (
    AlfabetosPredefinidos, 
    AlfabetoDesdeLenguaje,
    AlfabetoExplicito
)
from core.lenguajes import (
    LenguajeUniverso, 
    LenguajeExplicito,
    LenguajeExplicitoLongitudFija
)


def demo_jerarquia_binaria():
    """Demostración de jerarquía de 3 niveles con alfabeto binario."""
    print("=" * 70)
    print("JERARQUÍA MULTINIVEL: ALFABETO BINARIO")
    print("=" * 70)
    
    # Nivel 0: Alfabeto binario básico
    print("\n📍 NIVEL 0: Alfabeto básico")
    alf0 = AlfabetosPredefinidos.binario()
    print(f"   Σ₀ = {alf0}")
    print(f"   |Σ₀| = {alf0.cardinal}")
    
    # Nivel 1: Lenguaje de palabras de 2 bits
    print("\n📍 NIVEL 1: Lenguaje sobre Σ₀")
    L1 = LenguajeUniverso(alf0, longitud=2)
    palabras_L1 = L1.enumerar()
    print(f"   L₁ = Σ₀² = {palabras_L1}")
    print(f"   |L₁| = {L1.cardinal()}")
    
    # Nivel 2: Alfabeto con símbolos = palabras de L1
    print("\n📍 NIVEL 2: Alfabeto desde L₁")
    alf1 = AlfabetoDesdeLenguaje(L1, separador=" ")
    print(f"   Σ₁ = L₁ = {alf1}")
    print(f"   Símbolos: {alf1.simbolos}")
    
    # Generar palabras de longitud 2 sobre Σ₁
    print("\n   Palabras de longitud 2 sobre Σ₁:")
    palabras_nivel2 = alf1.generar_palabras(2)
    for palabra in palabras_nivel2[:8]:
        print(f"      '{palabra}'")
    print(f"      ... ({len(palabras_nivel2)} palabras totales)")
    
    # Nivel 3: Lenguaje sobre Σ₁
    print("\n📍 NIVEL 3: Lenguaje sobre Σ₁")
    L2 = LenguajeUniverso(alf1, longitud=2)
    print(f"   L₂ = Σ₁² (todas las palabras de longitud 2 sobre Σ₁)")
    print(f"   |L₂| = {L2.cardinal()} = 4² = 16")
    
    print()


def demo_codigo_bcd_bytes():
    """Usar alfabeto BCD para construir bytes (2 dígitos BCD)."""
    print("=" * 70)
    print("ALFABETO JERÁRQUICO: BCD → BYTES")
    print("=" * 70)
    
    # Nivel 0: Alfabeto binario
    alf_bin = AlfabetosPredefinidos.binario()
    print(f"\nΣ₀ = {alf_bin}")
    
    # Nivel 1: Alfabeto BCD (10 códigos de 4 bits)
    alf_bcd = AlfabetosPredefinidos.bcd()
    print(f"\nΣ₁ (BCD) = {alf_bcd}")
    print(f"Símbolos: {alf_bcd.simbolos}")
    
    # Crear lenguaje con símbolos BCD
    L_bcd = LenguajeExplicito(alf_bin, set(alf_bcd.simbolos))
    print(f"\nL_BCD = conjunto de códigos BCD")
    print(f"|L_BCD| = {L_bcd.cardinal()}")
    
    # Nivel 2: Alfabeto con símbolos BCD (sin separador = concatenación)
    alf_byte = AlfabetoDesdeLenguaje(L_bcd, separador="")
    print(f"\nΣ₂ (bytes BCD) = {alf_byte}")
    
    # Generar "bytes" BCD (2 dígitos BCD = 8 bits)
    print("\nPrimeros 10 bytes BCD (2 dígitos):")
    bytes_bcd = alf_byte.generar_palabras(2)
    for i, byte_val in enumerate(bytes_bcd[:10]):
        # Interpretar como decimal
        dig1 = alf_bcd.simbolos.index(byte_val[:4])
        dig2 = alf_bcd.simbolos.index(byte_val[4:])
        decimal = dig1 * 10 + dig2
        print(f"   {byte_val} = {dig1}{dig2} (decimal: {decimal})")
    
    print(f"\nTotal de bytes BCD posibles: {len(bytes_bcd)}")
    print()


def demo_palabras_como_simbolos():
    """Usar palabras del lenguaje natural como símbolos."""
    print("=" * 70)
    print("ALFABETO DESDE PALABRAS DEL LENGUAJE NATURAL")
    print("=" * 70)
    
    # Nivel 0: Alfabeto ASCII
    alf_ascii = AlfabetosPredefinidos.ascii_minusculas()
    print(f"\nΣ₀ (ASCII minúsculas): |Σ₀| = {alf_ascii.cardinal}")
    
    # Nivel 1: Pequeño vocabulario de palabras
    vocabulario = {
        "el", "la", "un", "una",
        "gato", "perro", "casa", "coche"
    }
    
    L_vocabulario = LenguajeExplicito(alf_ascii, vocabulario)
    print(f"\nL₁ (vocabulario) = {sorted(L_vocabulario.enumerar())}")
    print(f"|L₁| = {L_vocabulario.cardinal()}")
    
    # Nivel 2: Alfabeto con palabras como símbolos
    alf_palabras = AlfabetoDesdeLenguaje(L_vocabulario, separador=" ")
    print(f"\nΣ₂ (palabras): {alf_palabras}")
    
    # Generar "frases" (secuencias de palabras)
    print("\nPrimeras 10 frases de 3 palabras:")
    frases = alf_palabras.generar_palabras(3)
    for i, frase in enumerate(frases[:10], 1):
        print(f"   {i}. {frase}")
    
    print(f"\nTotal de frases de 3 palabras: {len(frases)}")
    print()


def demo_codigo_hamming():
    """Usar código de Hamming(7,4) como alfabeto."""
    print("=" * 70)
    print("ALFABETO DESDE CÓDIGO DE HAMMING")
    print("=" * 70)
    
    # Nivel 0: Binario
    alf_bin = AlfabetosPredefinidos.binario()
    
    # Nivel 1: Código de Hamming(7,4) - 16 palabras válidas de 7 bits
    # (Simplificado - solo algunas palabras de código)
    palabras_hamming = {
        "0000000", "0001111", "0010110", "0011001",
        "0100101", "0101010", "0110011", "0111100",
        "1000011", "1001100", "1010101", "1011010",
        "1100110", "1101001", "1110000", "1111111"
    }
    
    L_hamming = LenguajeExplicitoLongitudFija(alf_bin, palabras_hamming, "Hamming(7,4)")
    print(f"\nL_Hamming = código de Hamming(7,4)")
    print(f"|L_Hamming| = {L_hamming.cardinal()}")
    print(f"d_min = {L_hamming.distancia_minima()}")
    
    # Usar palabras del código como símbolos
    alf_hamming = AlfabetoDesdeLenguaje(L_hamming, separador=" ")
    print(f"\nΣ_Hamming = {alf_hamming}")
    print(f"|Σ_Hamming| = {alf_hamming.cardinal}")
    
    # Generar mensajes como secuencias de palabras de código
    print("\nPrimeros 5 mensajes de 2 palabras de código:")
    mensajes = alf_hamming.generar_palabras(2)
    for i, mensaje in enumerate(mensajes[:5], 1):
        print(f"   {i}. {mensaje}")
    
    print(f"\nTotal de mensajes de 2 palabras: {len(mensajes)}")
    print()


if __name__ == "__main__":
    demo_jerarquia_binaria()
    demo_codigo_bcd_bytes()
    demo_palabras_como_simbolos()
    demo_codigo_hamming()
    
    print("=" * 70)
    print("✅ Demo completado")
    print("=" * 70)
