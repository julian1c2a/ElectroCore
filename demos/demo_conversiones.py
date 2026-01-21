#!/usr/bin/env python3
"""
Demostración del módulo de conversiones numéricas.
Muestra cómo convertir números decimales a otras bases.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.numeracion_utils import (
    decimal_a_binario_divisiones,
    decimal_a_binario_con_pasos,
    decimal_a_binario_verbose,
    validar_numero_decimal,
    decimal_a_octal_divisiones,
    decimal_a_hexadecimal_divisiones
)


def demo_basico():
    """Demostración básica de conversiones."""
    print("=" * 80)
    print("CONVERSIONES BÁSICAS - Función decimal_a_binario_divisiones()")
    print("=" * 80)
    
    numeros = ["13", 42, "255", "0", 128]
    
    for num in numeros:
        try:
            binario = decimal_a_binario_divisiones(num)
            print(f"  {str(num):>3} → {binario}")
        except ValueError as e:
            print(f"  {str(num):>3} → ERROR: {e}")
    
    print("\nCon padding a 8 bits:")
    for num in [42, 13, 255]:
        binario = decimal_a_binario_divisiones(num, bits=8)
        print(f"  {num:>3} → {binario}")


def demo_con_pasos():
    """Demostración con pasos intermedios."""
    print("\n" + "=" * 80)
    print("CONVERSIÓN CON PASOS - decimal_a_binario_con_pasos()")
    print("=" * 80)
    
    numeros_prueba = [13, 42, 255]
    
    for numero in numeros_prueba:
        resultado = decimal_a_binario_con_pasos(numero)
        
        print(f"\nConvertir {resultado['numero']} a binario:")
        print("-" * 40)
        
        # Mostrar tabla de divisiones
        print(f"{'Dividendo':>10} | {'Cociente':>8} | {'Resto':>5}")
        print("-" * 40)
        
        for dividendo, cociente, resto in resultado['pasos']:
            print(f"{dividendo:>10} | {cociente:>8} | {resto:>5}")
        
        print("-" * 40)
        print(f"Restos en orden inverso: {resultado['binario']}")


def demo_verbose():
    """Demostración con explicación verbosa."""
    print("\n" + "=" * 80)
    print("CONVERSIÓN VERBOSA - decimal_a_binario_verbose()")
    print("=" * 80)
    
    numeros = [13, 42]
    
    for numero in numeros:
        print(f"\n{decimal_a_binario_verbose(numero)}\n")


def demo_validacion():
    """Demostración de validación."""
    print("\n" + "=" * 80)
    print("VALIDACIÓN - validar_numero_decimal()")
    print("=" * 80)
    
    inputs = ["42", 255, "abc", "-5", "0", "3.14", "  100  "]
    
    for inp in inputs:
        es_valido, mensaje = validar_numero_decimal(inp)
        estado = "[OK]" if es_valido else "[ERROR]"
        print(f"  {estado} {str(inp):>10} → {mensaje}")


def demo_otras_bases():
    """Demostración de conversiones a otras bases."""
    print("\n" + "=" * 80)
    print("OTRAS BASES - Octal y Hexadecimal")
    print("=" * 80)
    
    numeros = [42, 255, 1000]
    
    print("\nConversiones:")
    print(f"{'Decimal':>10} | {'Binario':>15} | {'Octal':>10} | {'Hexadecimal':>12}")
    print("-" * 60)
    
    for num in numeros:
        binario = decimal_a_binario_divisiones(num)
        octal = decimal_a_octal_divisiones(num)
        hexadecimal = decimal_a_hexadecimal_divisiones(num)
        
        print(f"{num:>10} | {binario:>15} | {octal:>10} | {hexadecimal:>12}")


def demo_tabla_conversion():
    """Tabla de conversión de 0 a 15."""
    print("\n" + "=" * 80)
    print("TABLA DE CONVERSIÓN (0 a 15)")
    print("=" * 80)
    
    print(f"{'Dec':>3} | {'Binario':>8} | {'Octal':>5} | {'Hex':>3}")
    print("-" * 35)
    
    for i in range(16):
        dec = str(i)
        binario = decimal_a_binario_divisiones(i, bits=4)
        octal = decimal_a_octal_divisiones(i)
        hexadecimal = decimal_a_hexadecimal_divisiones(i)
        
        print(f"{i:>3} | {binario:>8} | {octal:>5} | {hexadecimal:>3}")


def main():
    """Función principal."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "DEMOSTRACIÓN: CONVERSIONES NUMÉRICAS" + " " * 28 + "║")
    print("║" + " " * 20 + "Método de Divisiones Sucesivas" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Ejecutar demostraciones
    demo_basico()
    demo_con_pasos()
    demo_verbose()
    demo_validacion()
    demo_otras_bases()
    demo_tabla_conversion()
    
    # Ejemplo final
    print("\n" + "=" * 80)
    print("EJEMPLO PRÁCTICO FINAL")
    print("=" * 80)
    
    print("\nProbemos con 173:")
    print(decimal_a_binario_verbose("173"))


if __name__ == '__main__':
    main()
