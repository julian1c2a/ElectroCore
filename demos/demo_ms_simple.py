#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: Magnitud y Signo (M&S) - Seccion 2.1.1.7
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
)


def demo_1_basico():
    """Demo 1: Conceptos basicos"""
    print("\n" + "=" * 70)
    print("DEMO 1: CONCEPTOS BASICOS")
    print("=" * 70)
    
    print("\nEstructura de M&S (Magnitud y Signo) con 8 bits:")
    print("  Bit 7 (MSB):    Bit de signo (0=positivo, 1=negativo)")
    print("  Bits 6-0:       Magnitud (valor absoluto)")
    
    print("\nEjemplos:")
    ejemplos = [86, -86, 0, 1, -1, 127, -127]
    
    for numero in ejemplos:
        ms = decimal_a_ms(numero, 8)
        recuperado = ms_a_decimal(ms)
        print(f"  {numero:4d} (dec) -> {ms} (M&S8) -> {recuperado:4d} (dec)")


def demo_2_rango_capacidad():
    """Demo 2: Rango y capacidad"""
    print("\n" + "=" * 70)
    print("DEMO 2: RANGO Y CAPACIDAD")
    print("=" * 70)
    
    for n_bits in [4, 8, 16]:
        info = rango_ms(n_bits)
        print(f"\nM&S{n_bits}:")
        print(f"  Bits para magnitud:   {info['magnitud_bits']}")
        print(f"  Rango negativos:      [{info['min_negativo']:6d}, {info['max_negativo']:6d}]")
        print(f"  Rango positivos:      [{info['min_positivo']:6d}, {info['max_positivo']:6d}]")
        print(f"  Capacidad total:      {info['capacidad']} valores (2^{n_bits} - 1)")
        print(f"  Eficacia:             {info['porcentaje_eficacia']}")
        print(f"  Nota:                 Dos representaciones para 0 (+0 y -0)")


def demo_3_conversiones():
    """Demo 3: Conversiones paso a paso"""
    print("\n" + "=" * 70)
    print("DEMO 3: CONVERSIONES PASO A PASO")
    print("=" * 70)
    
    numeros = [42, -42, 0]
    
    for numero in numeros:
        print(f"\nConvertir {numero} a M&S8:")
        explicacion = explicar_conversion_ms(numero, 8)
        
        print(f"  Paso 1 - Signo:")
        print(f"    Valor: {numero}")
        print(f"    Tipo: {'positivo' if explicacion['es_positivo'] else 'negativo' if explicacion['es_negativo'] else 'cero'}")
        print(f"    Bit de signo: {explicacion['paso_1_signo']['bit_signo']}")
        
        print(f"  Paso 2 - Magnitud:")
        print(f"    Valor absoluto: {explicacion['paso_2_magnitud']['magnitud']}")
        mag_bin = explicacion['paso_2_magnitud']['conversion_binaria']['magnitud_binaria']
        print(f"    En binario (7 bits): {mag_bin}")
        
        print(f"  Paso 3 - Resultado:")
        resultado = explicacion['resultado_final']['representacion']
        print(f"    M&S8: {resultado}")
        print(f"    Verificacion: {ms_a_decimal(resultado)}")


def demo_4_operaciones():
    """Demo 4: Operaciones"""
    print("\n" + "=" * 70)
    print("DEMO 4: OPERACIONES EN M&S")
    print("=" * 70)
    
    print("\n[A] NEGACION (invertir bit de signo):")
    for numero in [42, -42, 0]:
        ms = decimal_a_ms(numero, 8)
        negado = negacion_ms(ms)
        valor_negado = ms_a_decimal(negado)
        print(f"  {numero:4d} ({ms}) -> {valor_negado:4d} ({negado})")
    
    print("\n[B] CONSULTAS:")
    ejemplos_consulta = [
        ('01010110', 86),
        ('11010110', -86),
        ('00000000', 0),
        ('10000000', 0),
    ]
    
    for ms, val_esperado in ejemplos_consulta:
        print(f"\n  {ms} = {val_esperado}:")
        print(f"    - Positivo?  {es_positivo_ms(ms)}")
        print(f"    - Negativo?  {es_negativo_ms(ms)}")
        print(f"    - Es cero?   {es_cero_ms(ms)}")
        print(f"    - Valor abs: {valor_absoluto_ms(ms)}")


def demo_5_ventajas_desventajas():
    """Demo 5: Ventajas y desventajas"""
    print("\n" + "=" * 70)
    print("DEMO 5: VENTAJAS Y DESVENTAJAS")
    print("=" * 70)
    
    print("""
VENTAJAS (+):
  1. Intuitivo: Exactamente como escribimos numeros a mano
  2. Negacion simple: Solo flip del bit MSB
  3. Multiplicacion facil: |A| * |B| con ajuste de signo

DESVENTAJAS (-):
  1. DOS CEROS: +0 y -0 son diferentes codigos (00000000 vs 10000000)
  2. Suma/Resta complicada: Algoritmos diferentes para diferentes casos
  3. Comparacion invertida para negativos: x < y pero |x| > |y|
  4. Ineficacia: Una combinacion desperdiciada (-0)

CONCLUSION:
  M&S es intuitivo pero ineficiente para hardware.
  Los sistemas modernos usan Complemento a 2 (C2) que es mas eficiente.
""")


def main():
    """Ejecuta todas las demos"""
    print("\n" + "=" * 70)
    print("DEMOSTRACION: MAGNITUD Y SIGNO (M&S)")
    print("Seccion 2.1.1.7: Numeros Enteros con Signo")
    print("=" * 70)
    
    demo_1_basico()
    demo_2_rango_capacidad()
    demo_3_conversiones()
    demo_4_operaciones()
    demo_5_ventajas_desventajas()
    
    print("\n" + "=" * 70)
    print("DEMOSTRACION COMPLETADA")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
