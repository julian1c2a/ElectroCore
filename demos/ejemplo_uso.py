#!/usr/bin/env python3
"""
Ejemplo de uso rápido: Conversión de Decimal a Binario
Muestra los 3 niveles de complejidad disponibles
"""

from core.numeracion_utils import (
    decimal_a_binario_divisiones,
    decimal_a_binario_con_pasos,
    decimal_a_binario_verbose
)


def main():
    numero = 173
    
    print("=" * 70)
    print(f"CONVERTIR {numero} A BINARIO - TRES FORMAS DIFERENTES")
    print("=" * 70)
    
    # NIVEL 1: Resultado simple
    print("\n[NIVEL 1] - Resultado Simple")
    print("-" * 70)
    print(f"Entrada: {numero}")
    print(f"Salida: {decimal_a_binario_divisiones(numero)}")
    print("\nUso: Cuando solo necesitas el resultado final")
    
    # NIVEL 2: Con datos intermedios
    print("\n" + "=" * 70)
    print("[NIVEL 2] - Con Datos Intermedios")
    print("-" * 70)
    
    resultado = decimal_a_binario_con_pasos(numero)
    
    print(f"Número: {resultado['numero']}")
    print(f"\nPasos de divisiones:")
    print(f"{'Dividendo':>10} | {'Cociente':>8} | {'Resto':>5}")
    print("-" * 30)
    for dividendo, cociente, resto in resultado['pasos']:
        print(f"{dividendo:>10} | {cociente:>8} | {resto:>5}")
    
    print(f"\nResultado: {resultado['binario']}")
    print("\nUso: Para mostrar tabla de divisiones en ejercicios")
    
    # NIVEL 3: Explicación completa
    print("\n" + "=" * 70)
    print("[NIVEL 3] - Explicación Completa")
    print("-" * 70)
    print(decimal_a_binario_verbose(numero))
    print("\nUso: Para ejercicios educativos detallados")
    
    # Casos de uso prácticos
    print("\n" + "=" * 70)
    print("CASOS DE USO PRÁCTICOS")
    print("=" * 70)
    
    print("\n1. Validar entrada del usuario:")
    from core.numeracion_utils import validar_numero_decimal
    
    entrada = "42"
    es_valido, msg = validar_numero_decimal(entrada)
    print(f"   Input: '{entrada}'")
    print(f"   Valido: {es_valido}")
    print(f"   Mensaje: {msg}")
    
    print("\n2. Converter con padding (8 bits):")
    print(f"   decimal_a_binario_divisiones(42, bits=8)")
    print(f"   → {decimal_a_binario_divisiones(42, bits=8)}")
    
    print("\n3. Diferentes bases:")
    from core.numeracion_utils import (
        decimal_a_octal_divisiones,
        decimal_a_hexadecimal_divisiones
    )
    
    num = 255
    print(f"   Número: {num}")
    print(f"   Binario: {decimal_a_binario_divisiones(num)}")
    print(f"   Octal: {decimal_a_octal_divisiones(num)}")
    print(f"   Hexadecimal: {decimal_a_hexadecimal_divisiones(num)}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
