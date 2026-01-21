#!/usr/bin/env python3
"""
Demostraciones de Eficacia de Empaquetado (Packing Efficiency)

Conceptos cubiertos:
1. Eficacia simple: (A/B)^n
2. Comparación BCD vs DPD
3. Empaquetado en bases relacionadas
4. Estándares IEEE 754
"""

from core.sistemas_numeracion_basicos import (
    eficacia_empaquetado_simple,
    eficacia_bcd_mejorada,
    comparar_eficacias_empaquetado,
    explicar_eficacia_empaquetado,
    explicar_ieee_754,
)


def demo_1_eficacia_simple():
    """Demo 1: Eficacia simple al representar diferentes bases en binario"""
    print("\n" + "=" * 80)
    print("DEMO 1: EFICACIA SIMPLE - Representar Bases Diversas en Binario")
    print("=" * 80)
    
    print("\nFórmula: Eficacia = (A/B)^n donde A=2 (binario nativo), B=base destino, n=dígitos")
    print("\nInterpretación:")
    print("  • Eficacia baja (< 0.7): Desperdicia mucho espacio")
    print("  • Eficacia media (0.7-0.9): Desperdicio moderado")
    print("  • Eficacia alta (> 0.9): Buen aprovechamiento")
    
    casos = [
        (2, 10, 1, "1 dígito decimal en binario"),
        (2, 10, 2, "2 dígitos decimales en binario"),
        (2, 10, 3, "3 dígitos decimales en binario"),
        (2, 16, 1, "1 dígito hexadecimal en binario"),
        (2, 8, 1, "1 dígito octal en binario"),
        (2, 5, 1, "1 dígito base-5 en binario"),
    ]
    
    print("\n{:<50} {:<15} {:<15} {:<15}".format(
        "Caso", "Capacidad", "Eficacia", "Porcentaje"))
    print("-" * 80)
    
    for base_nativa, base_destino, n_digitos, descripcion in casos:
        eficacia = eficacia_empaquetado_simple(base_nativa, base_destino, n_digitos)
        capacidad_nativa = base_nativa ** n_digitos
        capacidad_destino = base_destino ** n_digitos
        
        print("{:<50} {:<8} / {:<6} {:<15.6f} {:<15.2f}%".format(
            descripcion,
            capacidad_nativa,
            capacidad_destino,
            eficacia,
            eficacia * 100
        ))


def demo_2_bcd_vs_dpd():
    """Demo 2: Comparacion entre BCD clasico y DPD mejorado"""
    print("\n" + "=" * 80)
    print("DEMO 2: BCD CLASICO vs DPD (Dense Packed Decimal)")
    print("=" * 80)
    
    print("\nCOMPARACION DE EFICACIA:")
    print("-" * 80)
    
    # BCD Clásico
    print("\n[BCD CLASICO] (Binary Coded Decimal):")
    print("   * Codifica 1 digito decimal (0-9) en 4 bits")
    eficacia_bcd = eficacia_bcd_mejorada(10, 4)
    print(f"   * Valores representables: 10 (0-9)")
    print(f"   * Bits utilizados: 4")
    print(f"   * Capacidad en bits: 2^4 = 16")
    print(f"   * EFICACIA: 10/16 = {eficacia_bcd:.4f} ({eficacia_bcd*100:.2f}%)")
    print(f"   * DESPERDICIO: 6 combinaciones no usadas")
    
    # DPD
    print("\n[DPD] (Dense Packed Decimal - IEEE 754-2008):")
    print("   * Codifica 3 digitos decimales (0-999) en 10 bits")
    eficacia_dpd = eficacia_bcd_mejorada(1000, 10)
    print(f"   * Valores representables: 1000 (0-999)")
    print(f"   * Bits utilizados: 10")
    print(f"   * Capacidad en bits: 2^10 = 1024")
    print(f"   * EFICACIA: 1000/1024 = {eficacia_dpd:.4f} ({eficacia_dpd*100:.2f}%)")
    print(f"   * DESPERDICIO: 24 combinaciones no usadas")
    
    # Comparacion
    print("\nCONCLUSION:")
    mejora = (eficacia_dpd - eficacia_bcd) / eficacia_bcd * 100
    print(f"   * DPD es {mejora:.1f}% mas eficiente que BCD clasico")
    print(f"   * Por cada 1000 digitos decimales:")
    print(f"     - BCD: necesita 4000 bits")
    print(f"     - DPD: necesita ~3333 bits (25% menos espacio)")
    
    # Multiples digitos en BCD
    print("\nEXTENSION: Multiples digitos en BCD clasico:")
    for n_digitos in [1, 2, 3, 4]:
        valores = 10 ** n_digitos
        bits = 4 * n_digitos
        eficacia = eficacia_bcd_mejorada(valores, bits)
        print(f"   * {n_digitos} digito{'s' if n_digitos > 1 else ''} decimal{'es' if n_digitos > 1 else ''} en {bits} bits: {eficacia:.4f} ({eficacia*100:.2f}%)")


def demo_3_comparar_multiples():
    """Demo 3: Comparar multiples estrategias de empaquetado"""
    print("\n" + "=" * 80)
    print("DEMO 3: COMPARACION DE MULTIPLES ESTRATEGIAS")
    print("=" * 80)
    
    opciones = [
        {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 1},
        {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 2},
        {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 3},
        {'tipo': 'simple', 'base_destino': 16, 'n_digitos': 1},
        {'tipo': 'bcd', 'valores': 10, 'bits': 4},
        {'tipo': 'bcd', 'valores': 100, 'bits': 8},
        {'tipo': 'bcd', 'valores': 1000, 'bits': 10},
    ]
    
    resultado = comparar_eficacias_empaquetado(2, opciones)
    
    print("\n" + "=" * 80)
    print(f"Sistema nativo: Base {resultado['base_nativa']} (Binario)")
    print("=" * 80)
    print("\n{:<5} {:<60} {:<15} {:<10}".format("Rank", "Descripción", "Eficacia", "Tipo"))
    print("-" * 80)
    
    for idx, opcion in enumerate(resultado['opciones'], 1):
        desc = opcion['description']
        eficacia = opcion['eficacia']
        tipo = opcion['tipo']
        
        # Indicador visual
        barra = "*" * int(eficacia * 20) + "-" * (20 - int(eficacia * 20))
        
        print(f"{idx:<5} {desc:<60} {eficacia:>7.4f} [{barra}] {tipo}")
    
    # Mejor opción
    print("\n" + "=" * 80)
    print(f"MEJOR OPCION: {resultado['mejor']['description']}")
    print(f"   Eficacia: {resultado['mejor']['eficacia']:.4f} ({resultado['mejor']['porcentaje']:.2f}%)")


def demo_4_explicacion_detallada():
    """Demo 4: Explicacion detallada de eficacia"""
    print("\n" + "=" * 80)
    print("DEMO 4: EXPLICACION DETALLADA DE EFICACIA")
    print("=" * 80)
    
    casos = [
        (2, 10, 1, "Binario representando 1 dígito decimal"),
        (2, 10, 3, "Binario representando 3 dígitos decimales"),
        (10, 2, 1, "Decimal representando 1 dígito binario"),
    ]
    
    for base_nativa, base_destino, n_digitos, titulo in casos:
        print(f"\n{'-' * 80}")
        print(f"Caso: {titulo}")
        print(f"{'-' * 80}")
        
        explicacion = explicar_eficacia_empaquetado(base_nativa, base_destino, n_digitos)
        
        print(f"Base nativa (A): {explicacion['base_nativa']}")
        print(f"Base destino (B): {explicacion['base_destino']}")
        print(f"Numero de digitos (n): {explicacion['n_digitos']}")
        print(f"\nCapacidad en base nativa: {base_nativa}^{n_digitos} = {explicacion['capacidad_nativa']}")
        print(f"Capacidad en base destino: {base_destino}^{n_digitos} = {explicacion['capacidad_destino']}")
        print(f"\nFormula: {explicacion['formula']}")
        print(f"Eficacia: {explicacion['porcentaje']:.2f}%")
        print(f"\nInterpretacion:")
        print(f"   {explicacion['interpretacion']}")
        
        if explicacion['digitos_nativos_por_destino'] is not None:
            print(f"\nNota adicional:")
            print(f"   Digitos nativos por digito destino: {explicacion['digitos_nativos_por_destino']}")
            print(f"   Eficacia fundamental: {explicacion['eficacia_fundamental']:.4f}")


def demo_5_ieee_754():
    """Demo 5: Estandares IEEE 754"""
    print("\n" + "=" * 80)
    print("DEMO 5: ESTANDARES IEEE 754 (Punto Flotante)")
    print("=" * 80)
    
    formatos = ['binary32', 'binary64', 'binary128', 'decimal128']
    
    for formato in formatos:
        info = explicar_ieee_754(formato)
        detalles = info['detalles']
        
        print(f"\n{'-' * 80}")
        print(f"Formato: {formato}")
        print(f"{'-' * 80}")
        print(f"Nombre: {detalles['nombre']}")
        print(f"Estructura: {info['estructura']}")
        
        if 'bits_totales' in detalles:
            print(f"\nBits totales: {detalles['bits_totales']}")
            print(f"  * Signo: {detalles.get('bits_signo', 'N/A')}")
            print(f"  * Exponente: {detalles.get('bits_exponente', 'N/A')}")
            print(f"  * Mantisa/Coeficiente: {detalles.get('bits_mantisa', 'N/A')}")
            print(f"  * Sesgo exponente: {detalles.get('sesgo_exponente', 'N/A')}")
        
        if 'rango_minimo' in detalles and 'rango_maximo' in detalles:
            print(f"\nRango de valores:")
            print(f"  * Minimo: +/- {detalles['rango_minimo']:.3e}")
            print(f"  * Maximo: +/- {detalles['rango_maximo']:.3e}")
        
        if 'digitos_decimales_precision' in detalles:
            print(f"\nPrecision: {detalles['digitos_decimales_precision']} digitos decimales")


def main():
    """Ejecuta todas las demostraciones"""
    print("\n" + "=" * 80)
    print("DEMOSTRACIONES: EFICACIA DE EMPAQUETADO")
    print("=" * 80)
    
    demo_1_eficacia_simple()
    demo_2_bcd_vs_dpd()
    demo_3_comparar_multiples()
    demo_4_explicacion_detallada()
    demo_5_ieee_754()
    
    print("\n" + "=" * 80)
    print("TODAS LAS DEMOSTRACIONES COMPLETADAS")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
