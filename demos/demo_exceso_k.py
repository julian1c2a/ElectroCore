#!/usr/bin/env python3
"""
DEMOSTRACION: Exceso a K (Biased Representation)
Seccion 2.1.1.7.4: Numeros Enteros con Signo

ExcK es la forma estándar para:
- Representar exponentes en IEEE 754
- Flexibilidad total: cualquier K, cualquier base
- 100% eficacia en cualquier base
- Rango simétrico o asimétrico según necesidad
"""

from core.exceso_k_representacion import (
    repr_ExcK, ExcK_a_decimal, suma_ExcK, resta_ExcK, multiplicacion_ExcK,
    analizar_representacion_ExcK, generar_tabla_ExcK, explicar_operacion_ExcK
)


def demo_1_conceptos_basicos():
    """Demo 1: Conceptos básicos de Exceso a K"""
    print("\n" + "=" * 80)
    print("DEMO 1: CONCEPTOS BASICOS DE EXCESO A K")
    print("=" * 80)
    
    print("\nExceso a K es una forma simple y flexible de representar números negativos.")
    print("Idea: desplazar (shift) todos los números por K")
    
    print("\n1a. Ejemplo: Base 10, 2 dígitos, K = 47")
    print("  (Rango natural: [0, 99])")
    print("  (Rango representado: [-47, 52])")
    
    ejemplos = [
        (-47, "00", "Minimo (00...0)"),
        (-46, "01", "-46"),
        (0, "47", "Cero se representa como K"),
        (1, "48", "+1"),
        (52, "99", "Maximo"),
    ]
    
    for numero, esperado, desc in ejemplos:
        repr_val = repr_ExcK(numero, 10, 2, 47)
        valor_back = ExcK_a_decimal(repr_val, 10, 47)
        print(f"  {numero:3d} -> ExcK: {repr_val} -> Decimal: {valor_back:3d}  ({desc})")
        if repr_val != esperado:
            print(f"    [WARNING] Esperado {esperado}, obtuvo {repr_val}")
    
    print("\n1b. Ejemplo: Base 2, 8 bits, K = 127")
    print("  (Estándar IEEE 754 para exponentes)")
    print("  (Rango natural: [0, 255])")
    print("  (Rango representado: [-127, 128])")
    
    ejemplos_bin = [
        (-127, "00000000", "Minimo"),
        (-1, "01111110", "-1"),
        (0, "01111111", "Cero"),
        (1, "10000000", "+1"),
        (128, "11111111", "Maximo"),
    ]
    
    for numero, esperado, desc in ejemplos_bin:
        repr_val = repr_ExcK(numero, 2, 8, 127)
        valor_back = ExcK_a_decimal(repr_val, 2, 127)
        print(f"  {numero:4d} -> ExcK: {repr_val} -> Decimal: {valor_back:4d}  ({desc})")


def demo_2_representacion():
    """Demo 2: Representación en ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 2: REPRESENTACION EN EXCESO A K")
    print("=" * 80)
    
    print("\nBase 10, 3 dígitos, K = 500:")
    print("(Rango: [-500, 499])")
    
    numeros = [-500, -100, 0, 100, 250, 499]
    for num in numeros:
        try:
            exc = repr_ExcK(num, 10, 3, 500)
            back = ExcK_a_decimal(exc, 10, 500)
            print(f"  {num:4d} -> ExcK: {exc} -> Decimal: {back:4d}")
        except ValueError as e:
            print(f"  {num:4d} -> ERROR: {e}")


def demo_3_tablas():
    """Demo 3: Tablas completas de ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 3: TABLA DE VALORES EXCESO A K")
    print("=" * 80)
    
    print("\nExceso a K (Base 2, 4 bits, K = 8):")
    print("(Rango: [-8, 7])")
    tabla = generar_tabla_ExcK(2, 4, 8)
    print(tabla)
    
    print("\n\nExceso a K (Base 10, 2 dígitos, K = 50):")
    print("(Rango: [-50, 49])")
    tabla = generar_tabla_ExcK(10, 2, 50)
    print(tabla)


def demo_4_suma():
    """Demo 4: Suma en ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 4: SUMA EN EXCESO A K")
    print("=" * 80)
    
    print("\nSuma en ExcK (Base 10, 2 dígitos, K = 50):")
    print("Si A = a + K y B = b + K,")
    print("Entonces A + B = a + b + 2K")
    print("Pero en ExcK queremos: A '#' B = a + b + K")
    
    ejemplos = [
        (0, 0),
        (10, 20),
        (-10, 15),
        (-25, -10),
        (40, 40),
    ]
    
    for a, b in ejemplos:
        try:
            exc_a = repr_ExcK(a, 10, 2, 50)
            exc_b = repr_ExcK(b, 10, 2, 50)
            resultado = suma_ExcK(exc_a, exc_b, 10, 50)
            
            print(f"\n  {a:3d} + {b:3d} = {a + b:3d}")
            print(f"  ExcK({a:3d}) = {exc_a}")
            print(f"  ExcK({b:3d}) = {exc_b}")
            print(f"  Suma: {exc_a} + {exc_b} = {resultado['resultado']}")
            print(f"  Resultado decimal: {resultado['valor_decimal']}")
            
            if resultado['valor_decimal'] == a + b:
                print(f"  [OK] Correcto!")
            elif resultado['llevo']:
                print(f"  [OVERFLOW]")
        except ValueError as e:
            print(f"  ERROR: {e}")


def demo_5_resta():
    """Demo 5: Resta en ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 5: RESTA EN EXCESO A K")
    print("=" * 80)
    
    print("\nResta en ExcK (Base 10, 2 dígitos, K = 50):")
    
    ejemplos = [
        (20, 5),
        (0, 10),
        (-10, 20),
        (15, -15),
    ]
    
    for a, b in ejemplos:
        try:
            exc_a = repr_ExcK(a, 10, 2, 50)
            exc_b = repr_ExcK(b, 10, 2, 50)
            resultado = resta_ExcK(exc_a, exc_b, 10, 50)
            
            print(f"\n  {a:3d} - {b:3d} = {a - b:3d}")
            print(f"  ExcK({a:3d}) = {exc_a}")
            print(f"  ExcK({b:3d}) = {exc_b}")
            print(f"  Resta: {exc_a} - {exc_b} = {resultado['resultado']}")
            print(f"  Resultado decimal: {resultado['valor_decimal']}")
            
            if resultado['valor_decimal'] == a - b:
                print(f"  [OK] Correcto!")
        except ValueError as e:
            print(f"  ERROR: {e}")


def demo_6_multiplicacion():
    """Demo 6: Multiplicación en ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 6: MULTIPLICACION EN EXCESO A K")
    print("=" * 80)
    
    print("\nMultiplicacion en ExcK (Base 10, 2 dígitos, K = 50):")
    print("Algoritmo: (A - K) * (B - K) + K")
    
    ejemplos = [
        (2, 3),
        (5, -2),
        (-3, -4),
        (10, 0),
    ]
    
    for a, b in ejemplos:
        try:
            exc_a = repr_ExcK(a, 10, 2, 50)
            exc_b = repr_ExcK(b, 10, 2, 50)
            resultado = multiplicacion_ExcK(exc_a, exc_b, 10, 50)
            
            print(f"\n  {a:3d} * {b:3d} = {a * b:3d}")
            print(f"  ExcK({a:3d}) = {exc_a}")
            print(f"  ExcK({b:3d}) = {exc_b}")
            print(f"  Multiplicacion: {exc_a} * {exc_b} = {resultado['resultado']}")
            print(f"  Resultado decimal: {resultado['valor_decimal']}")
            
            if resultado['valor_decimal'] == a * b:
                print(f"  [OK] Correcto!")
            elif resultado['llevo']:
                print(f"  [OVERFLOW]")
        except ValueError as e:
            print(f"  ERROR: {e}")


def demo_7_ieee754_estandar():
    """Demo 7: IEEE 754 Estándar (K = 127 para 8 bits)"""
    print("\n" + "=" * 80)
    print("DEMO 7: IEEE 754 ESTANDAR (Exponente en ExcK)")
    print("=" * 80)
    
    print("\nEN IEEE 754 (precisión simple, 32 bits):")
    print("- Exponente: 8 bits en ExcK con K = 127")
    print("- Rango: [-127, 128]")
    print("- Cero se representa como 01111111 (127 en valor natural)")
    print("- Valores especiales: 00000000 y 11111111")
    
    print("\nEjemplos de exponentes comunes:")
    
    ejemplos_ieee = [
        (0, "Numero con exponente 0 (número normalizado)"),
        (-1, "Numero con exponente -1"),
        (1, "Numero con exponente 1"),
        (127, "Maximo exponente"),
        (-127, "Minimo exponente"),
    ]
    
    for exp, desc in ejemplos_ieee:
        try:
            exc = repr_ExcK(exp, 2, 8, 127)
            back = ExcK_a_decimal(exc, 2, 127)
            print(f"  Exp {exp:4d} -> {exc} -> {back:4d}  ({desc})")
        except ValueError:
            print(f"  Exp {exp:4d} -> [NO REPRESENTABLE]")


def demo_8_flexibilidad_K():
    """Demo 8: Flexibilidad de elegir K"""
    print("\n" + "=" * 80)
    print("DEMO 8: FLEXIBILIDAD DE EXCESO A K")
    print("=" * 80)
    
    print("\nBase 2, 8 bits con diferentes valores de K:")
    print("Total de valores representables: siempre 256")
    print("Pero el rango cambia según K\n")
    
    K_values = [0, 64, 127, 128, 255]
    
    for K in K_values:
        info = analizar_representacion_ExcK(2, 8, K)
        print(f"K = {K:3d}: Rango [{info['min_numero']:4d}, {info['max_numero']:4d}]  "
              f"Capacidad: {info['capacidad']}, Eficacia: {info['porcentaje_eficacia']}")


def demo_9_rango_y_capacidad():
    """Demo 9: Rango y capacidad de ExcK"""
    print("\n" + "=" * 80)
    print("DEMO 9: RANGO Y CAPACIDAD")
    print("=" * 80)
    
    configs = [
        (2, 4, 8, "Binario 4-bit, K=8"),
        (2, 8, 127, "Binario 8-bit (IEEE 754), K=127"),
        (10, 2, 50, "Decimal 2-digit, K=50"),
        (10, 3, 500, "Decimal 3-digit, K=500"),
    ]
    
    for base, longitud, K, desc in configs:
        info = analizar_representacion_ExcK(base, longitud, K)
        print(f"\n{desc}:")
        print(f"  Rango: [{info['min_numero']:6d}, {info['max_numero']:6d}]")
        print(f"  Capacidad: {info['capacidad']} valores")
        print(f"  Eficacia: {info['porcentaje_eficacia']}")


def demo_10_explicaciones():
    """Demo 10: Explicaciones paso a paso"""
    print("\n" + "=" * 80)
    print("DEMO 10: EXPLICACIONES PASO A PASO")
    print("=" * 80)
    
    print("\n--- Suma en ExcK ---")
    print(explicar_operacion_ExcK(15, 20, 'suma', 10, 2, 50))
    
    print("\n\n--- Resta en ExcK ---")
    print(explicar_operacion_ExcK(30, 10, 'resta', 10, 2, 50))
    
    print("\n\n--- Multiplicacion en ExcK ---")
    print(explicar_operacion_ExcK(5, 3, 'multiplicacion', 10, 2, 50))


def conclusiones():
    """Conclusiones sobre ExcK"""
    print("\n" + "=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    
    print("""
EXCESO A K (Biased Representation) es flexible y poderoso:

VENTAJAS:
  1. Representacion de negativos SIN bit de signo especial
  2. Flexibilidad total: elegir cualquier K segun necesidad
  3. 100% eficacia en CUALQUIER base
  4. Rango configurable: [-K, B^l - K - 1]
  5. Operaciones aritmeticas directas (suma, resta, multiplicacion)
  6. Comparacion simple para exponentes en punto flotante
  7. Usado en IEEE 754 para exponentes (K=127 en 8 bits)

USO ACTUAL:
  - IEEE 754 (punto flotante): exponentes en ExcK
  - Sin uso en enteros puros (CB es estandar)
  - Importante para representaciones de base arbitraria

FLEXIBILIDAD DE K:
  - K = 0: Numeros naturales puros (B^l valores desde 0 a B^l-1)
  - K = B^l/2: Rango casi simetrico
  - K = B^l-1: Maxima extension hacia positivos
  - K = 127: IEEE 754 (8 bits, binario)
  
OPERACIONES EN ExcK:
  - Suma:          A '#' B = (A-K) + (B-K) + K
  - Resta:         A '#' B = (A-K) - (B-K) + K
  - Multiplicacion: A '*' B = (A-K) * (B-K) + K
  - Comparacion:   directa (el representacion natural es igual al valor real)

NOTA IMPORTANTE:
  En ExcK, el numero "mas pequeno" en valor natural (00...0) representa
  el numero MAS NEGATIVO (-K). Esto es opuesto a CB (complemento a la base).
  
  Ejemplo:
    Binary 8-bit en CB:   00000000 = 0,   10000000 = -128
    Binary 8-bit en ExcK: 00000000 = -127, 10000000 = 1
    """)


def main():
    """Ejecutar todas las demostraciones"""
    demo_1_conceptos_basicos()
    demo_2_representacion()
    demo_3_tablas()
    demo_4_suma()
    demo_5_resta()
    demo_6_multiplicacion()
    demo_7_ieee754_estandar()
    demo_8_flexibilidad_K()
    demo_9_rango_y_capacidad()
    demo_10_explicaciones()
    conclusiones()
    
    print("\n" + "=" * 80)
    print("FIN DE DEMOSTRACIONES")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
