"""
Demostración: Distancia Hamming y Análisis de Lenguajes

Este script muestra las capacidades del sistema genérico de lenguajes:
- Cálculo de distancia Hamming
- Análisis de propiedades (adyacencia, ciclicidad)
- Comparación entre diferentes lenguajes
"""

from core.sistemas_numeracion_basicos import (
    distancia_hamming,
    crear_lenguaje_binario_saturado,
    crear_lenguaje_bcd,
    crear_lenguaje_johnson,
    crear_lenguaje_biquinario,
)


def demo_1_distancia_basica():
    """Demostración 1: Cálculo básico de distancia Hamming"""
    print("\n" + "="*80)
    print("DEMO 1: DISTANCIA HAMMING BASICA")
    print("="*80)
    
    ejemplos = [
        ('0000', '0000', "Identicas"),
        ('0000', '0001', "Una diferencia (adyacentes)"),
        ('0000', '0011', "Dos diferencias"),
        ('0111', '1000', "Cuatro diferencias (opuestas)"),
        ('1010', '0101', "Todas diferentes (complementarias)"),
    ]
    
    for p1, p2, descripcion in ejemplos:
        d = distancia_hamming(p1, p2)
        print(f"\n{p1} vs {p2}")
        print(f"  Distancia: {d}")
        print(f"  Descripcion: {descripcion}")


def demo_2_lenguaje_binario():
    """Demostración 2: Lenguaje Binario Natural"""
    print("\n" + "="*80)
    print("DEMO 2: LENGUAJE BINARIO NATURAL (4 bits)")
    print("="*80)
    
    lenguaje = crear_lenguaje_binario_saturado(4, "Binario Natural 4-bit")
    
    print(f"\nNombre: {lenguaje.nombre}")
    print(f"Alfabeto: {lenguaje.alfabeto}")
    print(f"Longitud: {lenguaje.longitud}")
    
    # Generar todas las palabras
    palabras = lenguaje.generar_todas_palabras()
    print(f"\nTotal de palabras: {len(palabras)}")
    print(f"Primeras 8: {palabras[:8]}")
    print(f"Ultimas 8: {palabras[-8:]}")
    
    # Mostrar transiciones de algunos valores
    print("\nTransiciones (cambios entre valores sucesivos):")
    transiciones = [
        (0, '0000', '0001'),
        (3, '0011', '0100'),
        (7, '0111', '1000'),
        (15, '1111', '0000'),
    ]
    
    for valor, actual, siguiente in transiciones:
        d = distancia_hamming(actual, siguiente)
        marca = "OK adyacente" if d == 1 else f"X {d} bits cambian"
        print(f"  {valor} -> {valor+1 if valor < 15 else 0}: {actual} -> {siguiente} ({marca})")
    
    # Análisis de adyacencia
    analisis = lenguaje.analizar_adyacencia()
    print(f"\nAnalisis de adyacencia:")
    print(f"  ?Adyacente? {analisis['es_adyacente']}")
    print(f"  ?Ciclico? {analisis['es_ciclico']}")
    print(f"  Pares adyacentes: {analisis['pares_adyacentes']}/15")
    print(f"  Distancia maxima: {analisis['max_distancia']} bits")


def demo_3_lenguaje_bcd():
    """Demostración 3: Lenguaje BCD"""
    print("\n" + "="*80)
    print("DEMO 3: LENGUAJE BCD (4 bits, digitos 0-9)")
    print("="*80)
    
    lenguaje = crear_lenguaje_bcd()
    
    print(f"\nNombre: {lenguaje.nombre}")
    print(f"Longitud: {lenguaje.longitud}")
    
    # Palabras válidas
    palabras = lenguaje.generar_todas_palabras()
    print(f"\nPalabras validas (10 total):")
    for i, palabra in enumerate(palabras):
        print(f"  {i}: {palabra}", end="  ")
        if (i + 1) % 5 == 0:
            print()
    print()
    
    # Palabras inválidas
    print(f"\nPalabras invalidas (1010-1111):")
    for i in range(10, 16):
        palabra = format(i, '04b')
        valida = lenguaje.es_valida(palabra)
        print(f"  {palabra}: {'OK valida' if valida else 'X invalida'}")
    
    # Análisis
    analisis = lenguaje.analizar_adyacencia()
    print(f"\nAnalisis:")
    print(f"  Eficacia: {len(palabras)}/16 = {len(palabras)/16:.1%}")
    print(f"  Adyacente: {analisis['es_adyacente']}")
    print(f"  Ciclico: {analisis['es_ciclico']}")


def demo_4_lenguaje_johnson():
    """Demostración 4: Lenguaje Johnson (adyacente y cíclico)"""
    print("\n" + "="*80)
    print("DEMO 4: CODIGO JOHNSON (5 bits, adyacente y ciclico)")
    print("="*80)
    
    lenguaje = crear_lenguaje_johnson()
    
    print(f"\nNombre: {lenguaje.nombre}")
    print(f"Longitud: {lenguaje.longitud}")
    
    # Mostrar todas las palabras con estructura
    palabras = lenguaje.generar_todas_palabras()
    print(f"\nTodas las palabras (estructura de 1s desplazados):")
    for i, palabra in enumerate(palabras):
        num_unos = palabra.count('1')
        patron = "0"*i + "1"*(5-i) if i < 5 else "1"*(10-i) + "0"*(i-5)
        print(f"  {i}: {palabra}  (patron: {num_unos} unos)")
    
    # Verificar adyacencia
    print(f"\nVerificacion de adyacencia (cada valor difiere en 1 bit del siguiente):")
    for i in range(len(palabras)):
        actual = palabras[i]
        siguiente = palabras[(i + 1) % len(palabras)]
        d = distancia_hamming(actual, siguiente)
        marca = "OK" if d == 1 else "X"
        transicion = f"{i}->{(i+1) % len(palabras)}" if i < len(palabras)-1 else f"{i}->0"
        print(f"  {marca} {transicion}: {actual} -> {siguiente} (distancia={d})")
    
    # Análisis
    analisis = lenguaje.analizar_adyacencia()
    print(f"\nAnalisis:")
    print(f"  Eficacia: {len(palabras)}/32 = {len(palabras)/32:.1%}")
    print(f"  Adyacente: {analisis['es_adyacente']}")
    print(f"  Ciclico: {analisis['es_ciclico']}")
    print(f"  Distancia de ciclicidad: {analisis['distancia_ciclica']} bit")


def demo_5_lenguaje_biquinario():
    """Demostración 5: Código Biquinario (detección de errores)"""
    print("\n" + "="*80)
    print("DEMO 5: CODIGO BIQUINARIO (5 bits, exactamente 2 encendidos)")
    print("="*80)
    
    lenguaje = crear_lenguaje_biquinario()
    
    print(f"\nNombre: {lenguaje.nombre}")
    print(f"Longitud: {lenguaje.longitud}")
    
    # Palabras válidas
    palabras = lenguaje.generar_todas_palabras()
    print(f"\nPalabras validas (10 total, exactamente 2 bits encendidos):")
    for i, palabra in enumerate(palabras):
        bits_encendidos = palabra.count('1')
        posiciones = [str(j) for j in range(5) if palabra[j] == '1']
        print(f"  {i}: {palabra}  (posiciones: {','.join(posiciones)})")
    
    # Detección de errores
    print(f"\nDeteccion de errores:")
    ejemplos = [
        ('00110', True, "Valida (2 bits encendidos)"),
        ('00111', False, "Error: 3 bits encendidos"),
        ('00100', False, "Error: 1 bit encendido"),
        ('00000', False, "Error: 0 bits encendidos"),
        ('11111', False, "Error: 5 bits encendidos"),
    ]
    
    for palabra, debe_ser_valida, descripcion in ejemplos:
        es_valida = lenguaje.es_valida(palabra)
        marca = "OK" if es_valida == debe_ser_valida else "X"
        bits = palabra.count('1')
        print(f"  {marca} {palabra} ({bits} bits): {descripcion}")
    
    # Análisis
    analisis = lenguaje.analizar_adyacencia()
    print(f"\nAnalisis:")
    print(f"  Eficacia: {len(palabras)}/32 = {len(palabras)/32:.1%}")
    print(f"  Adyacente: {analisis['es_adyacente']}")
    print(f"  Ciclico: {analisis['es_ciclico']}")
    print(f"  !Pero detecta errores! (cualquier desviacion es detectable)")


def demo_6_comparacion_completa():
    """Demostración 6: Comparación de todos los lenguajes"""
    print("\n" + "="*80)
    print("DEMO 6: COMPARACION COMPLETA DE LENGUAJES")
    print("="*80)
    
    lenguajes = {
        'Binario 4-bit': crear_lenguaje_binario_saturado(4),
        'BCD 4-bit': crear_lenguaje_bcd(),
        'Johnson 5-bit': crear_lenguaje_johnson(),
        'Biquinario 5-bit': crear_lenguaje_biquinario(),
    }
    
    print("\nTabla comparativa:\n")
    print(f"{'Lenguaje':<20} {'Palabras':<10} {'Posibles':<10} {'Eficacia':<10} {'Adyacente':<12} {'Ciclico':<10}")
    print("-" * 80)
    
    for nombre, lenguaje in lenguajes.items():
        palabras = lenguaje.generar_todas_palabras()
        n_palabras = len(palabras)
        n_posibles = len(lenguaje.alfabeto) ** lenguaje.longitud
        eficacia = n_palabras / n_posibles
        
        analisis = lenguaje.analizar_adyacencia()
        adyacente = "Si OK" if analisis['es_adyacente'] else "No X"
        ciclico = "Si OK" if analisis['es_ciclico'] else "No X"
        
        print(f"{nombre:<20} {n_palabras:<10} {n_posibles:<10} {eficacia:>8.1%}  {adyacente:<12} {ciclico:<10}")
    
    print("\nRecomendaciones de uso:")
    print("  * Binario Natural: Aritmetica general, maxima eficacia")
    print("  * BCD: Conversion directa de digitos, displays")
    print("  * Johnson: Contadores sin glitches, maquinas de estado")
    print("  * Biquinario: Comunicaciones criticas, deteccion de errores")


if __name__ == '__main__':
    demo_1_distancia_basica()
    demo_2_lenguaje_binario()
    demo_3_lenguaje_bcd()
    demo_4_lenguaje_johnson()
    demo_5_lenguaje_biquinario()
    demo_6_comparacion_completa()
    
    print("\n" + "="*80)
    print("DEMOSTRACIONES COMPLETADAS")
    print("="*80)
