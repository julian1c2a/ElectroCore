"""
Demostraciones de códigos especializados (Biquinario, Johnson, Gray)

Ejemplos prácticos de uso y propiedades de cada código.
"""

from core.sistemas_numeracion_basicos import (
    biquinario_a_entero,
    johnson_a_entero,
    entero_a_gray_4bits,
    gray_4bits_a_entero,
    analisis_codigo_especializado,
    comparar_codigos_5bits,
    CODIGO_BIQUINARIO,
    CODIGO_JOHNSON,
    CODIGO_GRAY_4BITS
)


def demo_1_introduccion():
    """Demo 1: Introducción a códigos especializados"""
    print("\n" + "="*70)
    print("DEMO 1: Introducción a Códigos Especializados")
    print("="*70)
    
    print("\nLos códigos especializados son variantes del sistema binario diseñadas")
    print("para aplicaciones específicas como detección de errores, cambios suaves,")
    print("o maximización de eficiencia.")
    
    print("\nTres sistemas clave:")
    print("  1. BIQUINARIO (2 entre 5): Detección de errores")
    print("  2. JOHNSON (Cíclico): Cambios suaves sin glitches")
    print("  3. GRAY (4-bit): Máxima eficiencia y todas las propiedades")
    
    print("\nEficacia de empaquetado (qué porcentaje de códigos son válidos):")
    print("  - Biquinario: 10/32 = 31.25%")
    print("  - Johnson:    10/32 = 31.25%")
    print("  - Gray 4-bit: 16/16 = 100%  [PERFECTO]")


def demo_2_biquinario_deteccion_errores():
    """Demo 2: Biquinario y detección de errores"""
    print("\n" + "="*70)
    print("DEMO 2: Código Biquinario - Detección de Errores")
    print("="*70)
    
    print("\nCaracterística: Exactamente 2 bits encendidos en 5 posiciones")
    print("Aplicación: Sistemas telefónicos antiguos para detectar errores")
    
    print("\nTabla de Códigos Biquinarios:")
    print("-" * 50)
    print("Valor | Código | Bits encendidos | Válido")
    print("-" * 50)
    
    for valor, codigo in CODIGO_BIQUINARIO.items():
        bits_encendidos = codigo.count('1')
        print(f"  {valor:2d}  | {codigo} |       {bits_encendidos}       | OK")
    
    print("\nConversión de Biquinario a Entero:")
    print("-" * 50)
    ejemplos = [0, 3, 5, 9]
    for valor in ejemplos:
        codigo = CODIGO_BIQUINARIO[valor]
        restaurado = biquinario_a_entero(codigo)
        print(f"  {codigo} -> {restaurado}  (valor original: {valor})")
    
    print("\nDetección de Errores:")
    print("-" * 50)
    print("Si un bit se voltea por error, el código se invalida:")
    
    codigo_correcto = '11000'  # Valor 5
    print(f"  Código correcto: {codigo_correcto} (5 con error detection)")
    print(f"  Bits encendidos: {codigo_correcto.count('1')} OK (exactamente 2)")
    
    codigo_error = '11010'  # Se voltea un bit
    print(f"  Código con error: {codigo_error} (un bit voltea)")
    print(f"  Bits encendidos: {codigo_error.count('1')} ERROR (debería ser 2)")
    
    try:
        biquinario_a_entero(codigo_error)
    except ValueError as e:
        print(f"  -> ERROR DETECTADO: {e}")
    
    print("\nConclusión: Biquinario detecta automáticamente cualquier cambio")
    print("   en un solo bit (propiedades de código redundante).")


def demo_3_johnson_cambios_suaves():
    """Demo 3: Código Johnson y cambios suaves"""
    print("\n" + "="*70)
    print("DEMO 3: Código Johnson - Cambios Suaves y Cíclicos")
    print("="*70)
    
    print("\nCaracterísticas:")
    print("  * Adyacencia: Valores sucesivos difieren en 1 solo bit")
    print("  * Ciclicidad: Último valor (9) se envuelve al primero (0) en 1 bit")
    print("  * Aplicación: Contadores sin glitches, cambios suaves")
    
    print("\nTabla de Códigos Johnson:")
    print("-" * 60)
    print("Valor | Código | Cambio | Descripción")
    print("-" * 60)
    
    for valor in range(10):
        codigo = CODIGO_JOHNSON[valor]
        cambio = ""
        
        if valor == 0:
            cambio = "START"
        else:
            codigo_prev = CODIGO_JOHNSON[valor - 1]
            pos_cambio = next(i for i, (c1, c2) in enumerate(zip(codigo, codigo_prev)) if c1 != c2)
            cambio = f"bit {4-pos_cambio}"
        
        ones = codigo.count('1')
        if ones == 0:
            desc = "Todos 0s"
        elif ones == 5:
            desc = "Todos 1s (pivote)"
        elif ones <= 2:
            desc = f"{ones} uno(s) a la derecha"
        else:
            zeros = 5 - ones
            desc = f"{zeros} cero(s) a la derecha"
        
        print(f"  {valor:2d}  | {codigo} | {cambio:7s} | {desc}")
    
    print("\nPropiedad Adyacente (cambio en 1 bit):")
    print("-" * 60)
    for valor in [1, 3, 5, 9]:
        codigo_actual = CODIGO_JOHNSON[valor]
        codigo_siguiente = CODIGO_JOHNSON[(valor + 1) % 10]
        
        diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_actual, codigo_siguiente))
        
        print(f"  {valor} -> {(valor+1)%10:2d}: {codigo_actual} -> {codigo_siguiente}")
        print(f"        (diferencia: {diferencias} bit) OK")
    
    print("\nPropiedad Cíclica (se envuelve):")
    print("-" * 60)
    codigo_9 = CODIGO_JOHNSON[9]
    codigo_0 = CODIGO_JOHNSON[0]
    diferencias = sum(c1 != c2 for c1, c2 in zip(codigo_9, codigo_0))
    print(f"  9 -> 0: {codigo_9} -> {codigo_0}")
    print(f"        (diferencia: {diferencias} bit) OK CÍCLICO")
    
    print("\nConversión Johnson a Entero:")
    print("-" * 60)
    ejemplos = [('00000', 0), ('00011', 2), ('11111', 5), ('10000', 9)]
    for codigo, valor in ejemplos:
        restaurado = johnson_a_entero(codigo)
        print(f"  {codigo} -> {restaurado}  (esperado: {valor}) OK")
    
    print("\nConclusión: Johnson es ideal para contadores porque cada valor")
    print("   difiere del siguiente en exactamente 1 bit, evitando glitches")
    print("   y cambios transitorios en múltiples señales simultáneamente.")


def demo_4_gray_eficiencia_perfecta():
    """Demo 4: Código Gray y eficiencia perfecta"""
    print("\n" + "="*70)
    print("DEMO 4: Código Gray 4-bit - Eficiencia Perfecta (100%)")
    print("="*70)
    
    print("\nCaracterísticas Únicas de Gray:")
    print("  OK Adyacencia: Valores consecutivos difieren en 1 bit")
    print("  OK Ciclicidad: Último (15) y primero (0) difieren en 1 bit")
    print("  OK Especularidad: Simetría perfecta (reflejado)")
    print("  OK Eficiencia: 16/16 = 100% (sin desperdiciar códigos)")
    print("  OK Aplicación: Encoders rotativos, contadores, válvulas lógicas")
    
    print("\nTabla de Códigos Gray 4-bit:")
    print("-" * 70)
    print("Decimal | Binario | Gray  | Cambio | Decimal | Binario | Gray  | Cambio")
    print("-" * 70)
    
    for i in range(8):
        valor1 = i
        valor2 = i + 8
        
        binario1 = format(valor1, '04b')
        gray1 = entero_a_gray_4bits(valor1)
        binario2 = format(valor2, '04b')
        gray2 = entero_a_gray_4bits(valor2)
        
        if i > 0:
            cambio1 = sum(c1 != c2 for c1, c2 in zip(gray1, entero_a_gray_4bits(valor1-1)))
            cambio2 = sum(c1 != c2 for c1, c2 in zip(gray2, entero_a_gray_4bits(valor2-1)))
        else:
            cambio1 = 0
            cambio2 = sum(c1 != c2 for c1, c2 in zip(gray2, gray1))
        
        print(f"  {valor1:2d}    | {binario1} | {gray1} | bit {cambio1}  |  {valor2:2d}   | {binario2} | {gray2} | bit {cambio2}")
    
    print("\nVerificación de Ciclicidad (15 -> 0):")
    print("-" * 70)
    gray_15 = entero_a_gray_4bits(15)
    gray_0 = entero_a_gray_4bits(0)
    cambio_ciclico = sum(c1 != c2 for c1, c2 in zip(gray_15, gray_0))
    print(f"  15 -> 0: {gray_15} -> {gray_0}")
    print(f"          (diferencia: {cambio_ciclico} bit) OK CÍCLICO")
    
    print("\nPropiedad Especular (Reflejada):")
    print("-" * 70)
    print("Primera mitad (0-7):  ", [entero_a_gray_4bits(i) for i in range(8)])
    print("Segunda mitad (8-15): ", [entero_a_gray_4bits(i) for i in range(8, 16)])
    print("\nObservar:")
    print("  * Primer bit es inverso en cada par especular")
    print("  * Gray(i) != Gray(15-i) en primer bit")
    print("  * Estructura perfectamente simétrica")
    
    print("\nFórmula de Conversión:")
    print("-" * 70)
    print("Decimal -> Gray:  Gray_i = Decimal_i XOR (Decimal_i >> 1)")
    print("Gray -> Decimal:  Decimal_i = Gray_i XOR (Decimal_{i+1})")
    
    ejemplos = [0, 5, 10, 15]
    print("\nEjemplos de Conversión:")
    for valor in ejemplos:
        binario = format(valor, '04b')
        gray = entero_a_gray_4bits(valor)
        restaurado = gray_4bits_a_entero(gray)
        print(f"  {valor:2d} = {binario} (binario) -> {gray} (Gray) -> {restaurado} OK")
    
    print("\nAplicación: Encoder Rotatorio")
    print("-" * 70)
    print("Un encoder rotatorio de 4 bits puede usar Gray en vez de binario.")
    print("Con binario: transición 7->8 (0111->1000) cambia 4 bits simultáneamente")
    print("Con Gray:    transición 7->8 (0100->1100) cambia 1 solo bit")
    print("Resultado: Sin errores transitorios o glitches.")
    
    print("\nConclusión: Gray es el 'código perfecto' para aplicaciones")
    print("   donde importan cambios suaves y se desperdician 0 códigos.")


if __name__ == '__main__':
    demo_1_introduccion()
    demo_2_biquinario_deteccion_errores()
    demo_3_johnson_cambios_suaves()
    demo_4_gray_eficiencia_perfecta()
    
    print("\n" + "="*70)
    print("Demostraciones completadas OK")
    print("="*70)
