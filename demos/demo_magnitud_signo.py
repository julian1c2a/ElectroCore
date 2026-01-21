#!/usr/bin/env python3
"""
DEMO: Magnitud y Signo (M&S) - Sección 2.1.1.7

Demostración práctica de la representación de números enteros con signo
utilizando el método de Magnitud y Signo.
"""

from core.enteros_signados import (
    rango_ms,
    analizar_ms,
    decimal_a_ms,
    ms_a_decimal,
    explicar_conversion_ms,
    negacion_ms,
    es_positivo_ms,
    es_negativo_ms,
    es_cero_ms,
    valor_absoluto_ms,
    comparar_ms,
    analizar_representacion_ms,
    crear_cero_positivo_ms,
    crear_cero_negativo_ms,
    mostrar_tabla_ms
)


def demo_basico():
    """Demo básica: conceptos fundamentales"""
    print("=" * 80)
    print("DEMO 1: CONCEPTOS FUNDAMENTALES DE MAGNITUD Y SIGNO")
    print("=" * 80)
    
    print("\n[1] ESTRUCTURA DE UN NUMERO EN M&S (8 bits):")
    print("""
    Número: +86 en decimal
    ┌─────────────────────────────────┐
    │ 0 1 0 1 0 1 1 0 │ = +86
    │ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
    │ s m m m m m m m │
    │ 7 6 5 4 3 2 1 0 │
    └─────────────────────────────────┘
    
    • Bit 7 (MSB): bit de signo = 0 (positivo)
    • Bits 6-0: magnitud = 1010110₂ = 86₁₀
    • Valor = +86
    
    Número: -86 en decimal
    ┌─────────────────────────────────┐
    │ 1 1 0 1 0 1 1 0 │ = -86
    │ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ │
    │ s m m m m m m m │
    │ 7 6 5 4 3 2 1 0 │
    └─────────────────────────────────┘
    
    • Bit 7 (MSB): bit de signo = 1 (negativo)
    • Bits 6-0: magnitud = 1010110₂ = 86₁₀
    • Valor = -86
    """)
    
    print("\n[2] CONVERSION DECIMAL -> M&S:")
    para_convertir = [86, -86, 0, 1, -1, 127, -127]
    
    for numero in para_convertir:
        ms = decimal_a_ms(numero, 8)
        print(f"   {numero:4d} (decimal) → {ms} (M&S8)")


def demo_rango_y_capacidad():
    """Demo: Rango y capacidad de representación"""
    print("\n" + "=" * 80)
    print("DEMO 2: RANGO Y CAPACIDAD")
    print("=" * 80)
    
    for n_bits in [4, 8, 16]:
        info = rango_ms(n_bits)
        print(f"\n📊 M&S con {n_bits} bits:")
        print(f"   • Bits para magnitud: {info['magnitud_bits']}")
        print(f"   • Rango de valores: [{info['min_negativo']:6d}, {info['max_positivo']:6d}]")
        print(f"   • Capacidad: {info['capacidad']} valores (2^{n_bits} - 1)")
        print(f"   • Eficacia: {info['porcentaje_eficacia']}")
        print(f"   • Nota: Dos representaciones para 0 (+0 y -0)")


def demo_analisis_detallado():
    """Demo: Análisis detallado de M&S"""
    print("\n" + "=" * 80)
    print("DEMO 3: ANÁLISIS DETALLADO")
    print("=" * 80)
    
    print(analizar_ms(8))


def demo_conversiones():
    """Demo: Conversiones en detalle"""
    print("\n" + "=" * 80)
    print("DEMO 4: CONVERSIONES PASO A PASO")
    print("=" * 80)
    
    numeros_ejemplo = [42, -42, 0, 127, -127]
    
    for numero in numeros_ejemplo:
        print(f"\n{'─' * 70}")
        print(f"Convertir {numero:4d} a M&S (8 bits):")
        print(f"{'─' * 70}")
        
        explicacion = explicar_conversion_ms(numero, 8)
        
        print(f"✓ Signo:")
        print(f"  - Es {'positivo' if explicacion['es_positivo'] else 'negativo' if explicacion['es_negativo'] else 'cero'}")
        print(f"  - Bit de signo: {explicacion['paso_1_signo']['bit_signo']}")
        
        print(f"✓ Magnitud:")
        print(f"  - Valor absoluto: {explicacion['paso_2_magnitud']['magnitud']}")
        print(f"  - En binario: {explicacion['paso_2_magnitud']['conversion_binaria']['magnitud_binaria']}")
        
        print(f"✓ Resultado:")
        print(f"  - M&S8: {explicacion['resultado_final']['representacion']}")
        print(f"  - Verificación: {ms_a_decimal(explicacion['resultado_final']['representacion'])}")


def demo_operaciones():
    """Demo: Operaciones en M&S"""
    print("\n" + "=" * 80)
    print("DEMO 5: OPERACIONES EN M&S")
    print("=" * 80)
    
    print("\n1️⃣  NEGACIÓN (multiplicación por -1):")
    print("   Operación: Invertir el bit de signo")
    
    numeros = [42, -42, 0]
    for numero in numeros:
        ms = decimal_a_ms(numero, 8)
        negado = negacion_ms(ms)
        valor_negado = ms_a_decimal(negado)
        print(f"   {numero:4d} ({ms}) → {valor_negado:4d} ({negado})")
    
    print("\n2️⃣  CONSULTAS (predicados):")
    ejemplos = [
        ('01010110', 86),   # +86
        ('11010110', -86),  # -86
        ('00000000', 0),    # +0
        ('10000000', 0),    # -0
    ]
    
    for ms, valor_esperado in ejemplos:
        print(f"\n   {ms} (= {valor_esperado}):")
        print(f"   - ¿Positivo? {es_positivo_ms(ms)}")
        print(f"   - ¿Negativo? {es_negativo_ms(ms)}")
        print(f"   - ¿Es cero? {es_cero_ms(ms)}")
        print(f"   - Valor absoluto: {valor_absoluto_ms(ms)}")
    
    print("\n3️⃣  COMPARACIÓN:")
    pares = [
        ('01000101', '01010110'),  # +69 vs +86
        ('11000101', '11010110'),  # -69 vs -86
        ('01010110', '11010110'),  # +86 vs -86
    ]
    
    for ms_a, ms_b in pares:
        val_a = ms_a_decimal(ms_a)
        val_b = ms_a_decimal(ms_b)
        cmp = comparar_ms(ms_a, ms_b)
        
        if cmp < 0:
            symbol = '<'
        elif cmp > 0:
            symbol = '>'
        else:
            symbol = '='
        
        print(f"   {ms_a} ({val_a:4d}) {symbol} {ms_b} ({val_b:4d})")


def demo_tabla_completa():
    """Demo: Tabla completa para M&S de pocos bits"""
    print("\n" + "=" * 80)
    print("DEMO 6: TABLA COMPLETA (M&S 4 bits)")
    print("=" * 80)
    
    print(mostrar_tabla_ms(4))


def demo_ventajas_desventajas():
    """Demo: Ventajas y desventajas de M&S"""
    print("\n" + "=" * 80)
    print("DEMO 7: VENTAJAS Y DESVENTAJAS")
    print("=" * 80)
    
    print("""
✅ VENTAJAS:
   1. Intuitivo: Exactamente como escribimos números a mano
      • Signo explícito (0 = +, 1 = -)
      • Magnitud clara (bits 0 a n-2)
   
   2. Negación simple: Invertir bit de signo
      • -86 es solo flip del bit MSB de +86
      • Una operación: XOR(MSB, 1)
   
   3. Multiplicación/División simple
      • |A| * |B| = resultado (magnitudes)
      • Ajustar signo según regla: mismo signo → +, diferente → -
   
   4. Fácil interpretación
      • Rápido reconocer signo visualmente
      • Fácil de depurar

❌ DESVENTAJAS:
   1. DOS REPRESENTACIONES PARA CERO
      • +0 = 00000000₂
      • -0 = 10000000₂
      • Ambas son cero, pero diferentes códigos
      • Compara con: Binario natural y Complemento a 2 (solo una)
   
   2. SUMA Y RESTA REQUIEREN ALGORITMOS DIFERENTES
      • Positivo + Positivo → suma directa
      • Negativo + Negativo → suma de magnitudes, resultado negativo
      • Positivo + Negativo → comparar magnitudes, restar
      • Mucho más complejo que Complemento a 2
   
   3. COMPARACIÓN DE NEGATIVOS ES INVERTIDA
      • Para positivos: mayor magnitud → mayor número
      • Para negativos: mayor magnitud → MENOR número
      • Ejemplo: -100 < -50 pero |−100| > |−50|
      • Necesita lógica especial en comparador
   
   4. BAJA EFICACIA TEÓRICA
      • 2^n - 1 valores representables (menos 1 por -0)
      • Eficacia = (2^n - 1) / 2^n = 1 - 1/2^n
      • Para n grande: ≈ 1 (casi 100%)
      • Pero siempre hay una combinación desperdiciada

CONCLUSIÓN:
   M&S es intuitivo pero ineficiente para operaciones aritméticas.
   Por eso sistemas modernos usan Complemento a 2 (menos intuitivo,
   pero mucho más eficiente para suma/resta).
""")


def demo_comparacion_sistemas():
    """Demo: Comparación con otros sistemas (preview)"""
    print("\n" + "=" * 80)
    print("DEMO 8: PREVIEW - COMPARACIÓN CON OTROS SISTEMAS")
    print("=" * 80)
    
    print("""
NÚMERO: +5 en 4 bits

Magnitud y Signo (M&S):
   Representación: 0101
   Valor: +5
   Ventaja: Intuitivo
   Desventaja: Múltiples representaciones para 0

Complemento a 1 (C1) [próximo tema]:
   Representación: (similar a M&S pero con inversión)
   Valor: +5
   Ventaja: Negación es invertir todos los bits
   Desventaja: Sigue teniendo dos 0s

Complemento a 2 (C2) [próximo tema]:
   Representación: 0101
   Valor: +5
   Ventaja: Una única representación para 0
   Desventaja: Menos intuitivo (requiere cálculo)

NÚMERO: -5 en 4 bits

Magnitud y Signo (M&S):
   Representación: 1101
   (Signo 1, Magnitud 101=5)

Complemento a 1 (C1):
   Representación: 1010
   (Invertir todos los bits de +5)

Complemento a 2 (C2):
   Representación: 1011
   (Invertir todos + 1)

➜ Veremos que C2 es mucho más eficiente para hardware,
  pero M&S es más fácil de entender conceptualmente.
""")


def main():
    """Ejecuta todas las demostraciones"""
    demo_basico()
    demo_rango_y_capacidad()
    demo_analisis_detallado()
    demo_conversiones()
    demo_operaciones()
    demo_tabla_completa()
    demo_ventajas_desventajas()
    demo_comparacion_sistemas()
    
    print("\n" + "=" * 80)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == '__main__':
    main()
