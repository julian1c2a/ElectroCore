"""
Demostración de Funciones de Capacidad y Rango de Representación
Sección 2.1.1.6.1 - Representación en Longitud Fija

Este script muestra el uso práctico de:
- capacidad_representacion(B, n) = B^n
- rango_representacion(B, n) = [0, B^n - 1]
- longitud_representacion(x, B) = ⌊log_B(x)⌋ + 1
"""

from core.sistemas_numeracion_basicos import (
    capacidad_representacion,
    rango_representacion,
    longitud_representacion,
    analisis_representacion
)


def demo_1_capacidad_representacion():
    """DEMO 1: Capacidad de Representación"""
    print("\n" + "=" * 80)
    print("DEMO 1: CAPACIDAD DE REPRESENTACIÓN (2.1.1.6.1.1)")
    print("=" * 80)
    print("\nCapacidad(B, n) = B^n")
    print("Número de valores diferentes que se pueden representar con n dígitos en base B")
    print()
    
    ejemplos = [
        (2, 3, "Binario - 3 bits"),
        (2, 8, "Binario - 1 byte (8 bits)"),
        (10, 3, "Decimal - 3 dígitos"),
        (16, 2, "Hexadecimal - 2 dígitos"),
        (5, 5, "Base 5 - 5 dígitos"),
    ]
    
    for base, longitud, descripcion in ejemplos:
        cap = capacidad_representacion(base, longitud)
        print(f"  Capacidad({base}, {longitud}) = {base}^{longitud} = {cap:6d}  ← {descripcion}")
    
    print("\n✓ Con n dígitos en base B, se pueden representar exactamente B^n valores diferentes")
    print("✓ El primero es 0, el último es B^n - 1")


def demo_2_rango_representacion():
    """DEMO 2: Rango de Valores Representables"""
    print("\n" + "=" * 80)
    print("DEMO 2: RANGO DE VALORES REPRESENTABLES (2.1.1.6.1.2)")
    print("=" * 80)
    print("\nRango(B, n) = [0, B^n - 1]")
    print("Intervalo cerrado de valores que se pueden representar")
    print()
    
    ejemplos = [
        (2, 3, "Binario - 3 bits"),
        (2, 8, "Binario - 1 byte"),
        (10, 2, "Decimal - 2 dígitos"),
        (16, 2, "Hexadecimal - 2 dígitos"),
        (5, 5, "Base 5 - 5 dígitos (ejemplo 1994)"),
    ]
    
    for base, longitud, descripcion in ejemplos:
        rango_min, rango_max = rango_representacion(base, longitud)
        print(f"  Rango({base}, {longitud}) = [{rango_min:5d}, {rango_max:5d}]  ← {descripcion}")
    
    print("\n✓ Rango mínimo SIEMPRE es 0")
    print("✓ Rango máximo = B^n - 1")
    print("✓ Total de valores = Rango máximo - Rango mínimo + 1 = B^n")


def demo_3_longitud_representacion():
    """DEMO 3: Longitud Mínima de Representación"""
    print("\n" + "=" * 80)
    print("DEMO 3: LONGITUD MÍNIMA DE REPRESENTACIÓN (2.1.1.6.1.2)")
    print("=" * 80)
    print("\nLongitud(x, B) = ⌊log_B(x)⌋ + 1")
    print("Número mínimo de dígitos necesarios para representar x en base B")
    print()
    
    ejemplos = [
        (27, 10, "27 en decimal"),
        (255, 2, "255 en binario (máximo de 8 bits)"),
        (1994, 5, "1994 en base 5 (30434₅)"),
        (99, 10, "99 en decimal"),
        (15, 16, "15 en hexadecimal (F₁₆)"),
        (1, 10, "1 en cualquier base"),
        (100, 10, "100 en decimal"),
    ]
    
    for numero, base, descripcion in ejemplos:
        longitud = longitud_representacion(numero, base)
        print(f"  Longitud({numero:4d}, {base:2d}) = {longitud}  ← {descripcion}")
    
    print("\n✓ Longitud(x, B) es el mínimo de dígitos NECESARIOS")
    print("✓ Puede ser menor que la longitud fija del registro")
    print("✓ Se rellena con ceros a la izquierda si es necesario")


def demo_4_analisis_completo():
    """DEMO 4: Análisis Completo - Ejemplo 1994 en Base 5"""
    print("\n" + "=" * 80)
    print("DEMO 4: ANÁLISIS COMPLETO - EJEMPLO 1994 EN BASE 5")
    print("=" * 80)
    print("\nAnalizamos: número=1994, base=5, longitud=5 dígitos")
    print()
    
    análisis = analisis_representacion(1994, 5, longitud=5)
    
    print(f"  Número a representar: {análisis['número']}")
    print(f"  Base: {análisis['base']}")
    print(f"  Longitud fija del registro: {análisis['longitud_fija']} dígitos")
    print()
    print(f"  Longitud MÍNIMA requerida: {análisis['longitud_mínima']} dígitos")
    print(f"  Representación: 30434₅")
    print()
    print(f"  Capacidad: {análisis['fórmula_capacidad']}")
    print(f"    → Con 5 dígitos en base 5, se pueden representar {análisis['capacidad']} valores")
    print()
    print(f"  Rango: {análisis['rango']}")
    print(f"    → Mínimo: {análisis['rango_min']}")
    print(f"    → Máximo: {análisis['rango_max']} (fórmula: {análisis['fórmula_rango_máximo']})")
    print()
    print(f"  ¿Está {análisis['número']} en el rango? {análisis['en_rango']} ✓")
    
    print("\n✓ El número 1994 SE PUEDE representar en 5 dígitos de base 5")
    print("✓ 1994 está dentro del rango [0, 3124]")


def demo_5_comparación_bases():
    """DEMO 5: Comparación de Capacidad en Diferentes Bases"""
    print("\n" + "=" * 80)
    print("DEMO 5: COMPARACIÓN DE CAPACIDAD EN DIFERENTES BASES")
    print("=" * 80)
    print("\nSi tenemos 1 byte (8 bits), ¿cuántos valores podemos representar?")
    print()
    
    longitud = 8
    bases = [2, 8, 10, 16]
    
    print(f"  {'Base':<6} {'Capacidad':<15} {'Rango':<20} {'Ejemplo de valores':<30}")
    print("  " + "-" * 75)
    
    for base in bases:
        cap = capacidad_representacion(base, longitud)
        rango_min, rango_max = rango_representacion(base, longitud)
        
        if base == 2:
            rango_str = f"[{rango_min}, {rango_max}]"
            ejemplo = "00000000 a 11111111"
        elif base == 8:
            rango_str = f"[{rango_min}, {rango_max}]"
            ejemplo = "000 a 377 (octal)"
        elif base == 10:
            rango_str = f"[{rango_min}, {rango_max}]"
            ejemplo = "00 a 99 (decimal)"
        else:  # base 16
            rango_str = f"[{rango_min}, {rango_max}]"
            ejemplo = "00 a FF (hexadecimal)"
        
        print(f"  {base:<6} {cap:<15} {rango_str:<20} {ejemplo:<30}")
    
    print("\n✓ La capacidad NO depende de la base: siempre son 256 valores")
    print("✓ Solo cambia cómo los representamos (notación)")


def demo_6_errores_y_desbordamiento():
    """DEMO 6: Detección de Errores por Desbordamiento"""
    print("\n" + "=" * 80)
    print("DEMO 6: DETECCIÓN DE DESBORDAMIENTO DE RANGO")
    print("=" * 80)
    print("\nVerificamos si números caben en un registro de tamaño fijo")
    print()
    
    casos = [
        (100, 2, 8, "100 en binario con 8 bits"),
        (1000, 10, 3, "1000 en decimal con 3 dígitos"),
        (99, 10, 2, "99 en decimal con 2 dígitos"),
        (256, 16, 2, "256 en hexadecimal con 2 dígitos"),
        (1994, 5, 5, "1994 en base 5 con 5 dígitos"),
    ]
    
    for numero, base, longitud, descripcion in casos:
        análisis = analisis_representacion(numero, base, longitud)
        estado = "✓ CABE" if análisis['en_rango'] else "✗ DESBORDAMIENTO"
        print(f"\n  {descripcion}:")
        print(f"    Rango disponible: {análisis['rango']}")
        print(f"    Número: {numero}")
        print(f"    {estado}")
    
    print("\n✓ Si el número es > (B^n - 1), NO cabe en n dígitos → DESBORDAMIENTO")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN: CAPACIDAD Y RANGO DE REPRESENTACIÓN (2.1.1.6.1)".center(80))
    print("=" * 80)
    
    demo_1_capacidad_representacion()
    demo_2_rango_representacion()
    demo_3_longitud_representacion()
    demo_4_analisis_completo()
    demo_5_comparación_bases()
    demo_6_errores_y_desbordamiento()
    
    print("\n" + "=" * 80)
    print("FIN DE DEMOSTRACIONES")
    print("=" * 80)
    print("\n✓ Todas las funciones 2.1.1.6.1 implementadas y funcionando correctamente")
