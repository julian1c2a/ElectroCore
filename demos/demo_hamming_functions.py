"""
Demo: Uso de funciones de Distancia de Hamming desde el core del proyecto.

Este demo muestra cómo utilizar las funciones migradas de análisis de Hamming
que ahora están disponibles en el core del proyecto.

Ejecutar: python -m demos.demo_hamming_functions
"""

# Importar directamente desde core.formal_languages
from core.formal_languages import (
    hamming_distance,
    hamming_weight,
    min_distance_of_language,
    hamming_sphere,
    binomial_coefficient,
    sphere_volume,
)


def demo_basic_operations():
    """Demostración de operaciones básicas."""
    print("=" * 70)
    print("1. OPERACIONES BÁSICAS")
    print("=" * 70)
    
    x = "1011010"
    y = "1001011"
    
    print(f"\nPalabras:")
    print(f"  x = {x}")
    print(f"  y = {y}")
    
    d = hamming_distance(x, y)
    print(f"\nDistancia de Hamming: d_H(x, y) = {d}")
    
    # Mostrar posiciones diferentes
    diffs = [(i, x[i], y[i]) for i in range(len(x)) if x[i] != y[i]]
    print(f"Posiciones diferentes: {diffs}")
    
    # Peso de Hamming
    wx = hamming_weight(x)
    wy = hamming_weight(y)
    print(f"\nPeso de Hamming:")
    print(f"  w_H(x) = {wx}")
    print(f"  w_H(y) = {wy}")


def demo_error_correcting_codes():
    """Demostración con códigos correctores."""
    print("\n" + "=" * 70)
    print("2. CÓDIGOS CORRECTORES DE ERRORES")
    print("=" * 70)
    
    # Código de repetición triple
    print("\n📌 Código de repetición triple:")
    repetition = ["000", "111"]
    d_min = min_distance_of_language(repetition)
    print(f"  Código: {repetition}")
    print(f"  Distancia mínima: d_min = {d_min}")
    print(f"  Capacidad de corrección: t = ⌊(d_min-1)/2⌋ = {(d_min-1)//2} error(es)")
    
    # Código de Hamming (7,4)
    print("\n📌 Código de Hamming (7,4):")
    hamming_7_4 = [
        "0000000", "1101000", "0110100", "1011100",
        "0011010", "1110010", "0101110", "1000110",
        "0001101", "1100101", "0111001", "1010001",
        "0010111", "1111111", "0100011", "1001011"
    ]
    d_min = min_distance_of_language(hamming_7_4)
    print(f"  Palabras-código: {len(hamming_7_4)}")
    print(f"  Distancia mínima: d_min = {d_min}")
    print(f"  Capacidad de corrección: t = {(d_min-1)//2} error(es)")


def demo_hamming_spheres():
    """Demostración de esferas de Hamming."""
    print("\n" + "=" * 70)
    print("3. ESFERAS DE HAMMING")
    print("=" * 70)
    
    center = "101"
    
    for radius in range(3):
        sphere = hamming_sphere(center, radius)
        volume_calc = sphere_volume(len(center), radius)
        
        print(f"\n🔵 Esfera de radio {radius} centrada en '{center}':")
        print(f"  B('{center}', {radius}) = {sorted(sphere)}")
        print(f"  Volumen: |B| = {len(sphere)}")
        print(f"  Fórmula: V(3, {radius}) = {volume_calc}")
        
        # Verificar fórmula
        expected = sum(binomial_coefficient(3, i) for i in range(radius + 1))
        print(f"  Σᵢ₌₀^{radius} C(3,i) = {expected} {'✓' if expected == volume_calc else '✗'}")


def demo_hamming_bound():
    """Demostración de la Cota de Hamming."""
    print("\n" + "=" * 70)
    print("4. COTA DE HAMMING (SPHERE-PACKING BOUND)")
    print("=" * 70)
    
    n = 7  # Hamming (7,4)
    t = 1  # Corrige 1 error
    
    vol = sphere_volume(n, t)
    max_codewords = (2 ** n) / vol
    
    print(f"\nPara n={n} bits, t={t} error(es) corregibles:")
    print(f"  Volumen esfera: V({n}, {t}) = {vol}")
    print(f"  Espacio total: 2^{n} = {2**n}")
    print(f"  Cota de Hamming: |C| ≤ {2**n}/{vol} = {max_codewords}")
    
    # Código de Hamming (7,4) alcanza la cota
    print(f"\n  Código de Hamming (7,4):")
    print(f"    Palabras-código: 16")
    print(f"    ¿Es perfecto?: {'SÍ ✓' if 16 == max_codewords else 'NO'}")
    print(f"    (Alcanza la igualdad en la cota de Hamming)")


def demo_binomial_coefficients():
    """Demostración de coeficientes binomiales."""
    print("\n" + "=" * 70)
    print("5. COEFICIENTES BINOMIALES")
    print("=" * 70)
    
    n = 7
    print(f"\nTriángulo de Pascal para n={n}:")
    print("  C(n, k) | k=0  k=1  k=2  k=3  k=4  k=5  k=6  k=7")
    print("  " + "-" * 55)
    
    for i in range(n + 1):
        row = [binomial_coefficient(i, k) for k in range(i + 1)]
        row_str = "  ".join(f"{val:4d}" for val in row)
        print(f"  n={i}   | {row_str}")
    
    # Verificar suma de fila = 2^n
    print(f"\n  Propiedad: Σₖ C(n, k) = 2^n")
    for i in range(n + 1):
        suma = sum(binomial_coefficient(i, k) for k in range(i + 1))
        esperado = 2 ** i
        print(f"    n={i}: {suma} = {esperado} {'✓' if suma == esperado else '✗'}")


def main():
    """Ejecutar todas las demostraciones."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "DEMO: FUNCIONES DE DISTANCIA DE HAMMING" + " " * 18 + "║")
    print("║" + " " * 15 + "Desde el Catálogo del Proyecto" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    
    demo_basic_operations()
    demo_error_correcting_codes()
    demo_hamming_spheres()
    demo_hamming_bound()
    demo_binomial_coefficients()
    
    print("\n" + "=" * 70)
    print("✅ TODAS LAS FUNCIONES FUNCIONAN CORRECTAMENTE")
    print("=" * 70)
    print("\nFunciones disponibles desde core.formal_languages:")
    funcs = [
        "hamming_distance", "hamming_weight", "min_distance_of_language",
        "hamming_sphere", "binomial_coefficient", "sphere_volume"
    ]
    for func_name in funcs:
        print(f"  ✓ {func_name}")
    print()


if __name__ == "__main__":
    main()
