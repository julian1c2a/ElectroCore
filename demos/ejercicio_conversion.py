#!/usr/bin/env python3
"""
Ejercicio educativo: Conversión de Decimal a Binario
Demuestra paso a paso el método de divisiones sucesivas.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.numeracion_utils import decimal_a_binario_verbose, decimal_a_binario_con_pasos
from modules.numeracion.models import ConversionRow
from modules.numeracion.generators import ConversionExerciseGenerator


def ejercicio_conversion_educativa():
    """
    Ejercicio educativo completo que muestra:
    1. Enunciado del problema
    2. Explicación del método
    3. Pasos detallados
    4. Solución final
    """
    
    print("=" * 80)
    print("EJERCICIO EDUCATIVO: CONVERSIÓN DE DECIMAL A BINARIO")
    print("=" * 80)
    print()
    
    # Datos del ejercicio
    numero_decimal = 173
    
    print("ENUNCIADO:")
    print("-" * 80)
    print(f"Convierte el número {numero_decimal} de decimal a binario utilizando el método")
    print("de divisiones sucesivas por 2.")
    print()
    
    print("MÉTODO:")
    print("-" * 80)
    print("""
El método de divisiones sucesivas consiste en:
  1. Dividir el número entre 2
  2. Anotar el resto (0 o 1)
  3. Tomar el cociente y repetir el proceso
  4. Continuar hasta que el cociente sea 0
  5. Leer los restos de abajo hacia arriba para obtener el número binario
    """)
    
    print("DESARROLLO PASO A PASO:")
    print("-" * 80)
    print(decimal_a_binario_verbose(numero_decimal))
    print()
    
    print("VERIFICACIÓN:")
    print("-" * 80)
    resultado = decimal_a_binario_con_pasos(numero_decimal)
    
    # Mostrar tabla formateada
    print("\nTabla de divisiones:")
    print(f"{'Paso':>5} | {'Dividendo':>9} | {'÷ 2':>3} | {'Cociente':>8} | {'Resto':>5}")
    print("-" * 50)
    
    for i, (dividendo, cociente, resto) in enumerate(resultado['pasos'], 1):
        print(f"{i:>5} | {dividendo:>9} | {' ':>3} | {cociente:>8} | {resto:>5}")
    
    print()
    print("Leyendo los restos de abajo hacia arriba (de atrás hacia adelante):")
    restos_invertidos = list(reversed(resultado['restos']))
    print(f"  {' '.join(str(r) for r in restos_invertidos)}")
    print()
    print(f"SOLUCIÓN: {numero_decimal}₁₀ = {resultado['binario']}")
    print()
    
    # Verificación matemática
    print("VERIFICACIÓN (convertir de vuelta a decimal):")
    print("-" * 80)
    binario_str = resultado['binario'].replace('₂', '')
    decimal_verificado = int(binario_str, 2)
    print(f"{resultado['binario']} = ", end="")
    
    # Mostrar cálculo posicional
    potencias = []
    for i, bit in enumerate(reversed(binario_str)):
        if bit == '1':
            potencias.append(f"2^{i}")
    
    print(" + ".join(potencias) + " = ", end="")
    
    suma_parcial = []
    for i, bit in enumerate(reversed(binario_str)):
        if bit == '1':
            suma_parcial.append(str(2**i))
    
    print(" + ".join(suma_parcial) + f" = {decimal_verificado}₁₀")
    print()
    
    if decimal_verificado == numero_decimal:
        print("[OK] VERIFICACION CORRECTA: El resultado es valido")
    else:
        print("[ERROR] La verificacion fallo")
    
    print()
    print("=" * 80)


def ejercicio_multiple():
    """Ejercicio con múltiples números para practicar."""
    
    print("\n" + "=" * 80)
    print("PRÁCTICA: CONVERSIONES MÚLTIPLES")
    print("=" * 80)
    print()
    
    numeros_practica = [7, 15, 32, 100, 256]
    
    print("Resuelve las siguientes conversiones de decimal a binario:\n")
    
    for i, num in enumerate(numeros_practica, 1):
        resultado = decimal_a_binario_con_pasos(num)
        
        print(f"\n{i}. {num}₁₀ = ?₂")
        print("-" * 40)
        
        # Mostrar tabla simplificada
        print(f"{'Dividendo':>10} | {'Cociente':>8} | {'Resto':>5}")
        print("-" * 40)
        for dividendo, cociente, resto in resultado['pasos']:
            print(f"{dividendo:>10} | {cociente:>8} | {resto:>5}")
        
        print("-" * 40)
        print(f"RESPUESTA: {resultado['binario']}\n")


def ejercicio_tabla_conversion():
    """Tabla de conversión para referencia rápida."""
    
    print("\n" + "=" * 80)
    print("TABLA DE REFERENCIA: CONVERSIONES DE 0 A 31")
    print("=" * 80)
    print()
    
    print(f"{'Decimal':>8} | {'Binario':>10} | {'Decimal':>8} | {'Binario':>10}")
    print("-" * 60)
    
    # Primera mitad (0-15)
    for i in range(16):
        resultado = decimal_a_binario_con_pasos(i)
        binario = resultado['binario']
        
        # Segunda mitad (16-31)
        j = i + 16
        resultado_j = decimal_a_binario_con_pasos(j)
        binario_j = resultado_j['binario']
        
        print(f"{i:>8} | {binario:>10} | {j:>8} | {binario_j:>10}")


def main():
    """Función principal."""
    
    print("\n")
    print("=" * 80)
    print("EJERCICIO EDUCATIVO DE NUMERACION")
    print("Conversion de Decimal a Binario")
    print("=" * 80)
    print("\n")
    
    # Ejercicio principal
    ejercicio_conversion_educativa()
    
    # Práctica múltiple
    ejercicio_multiple()
    
    # Tabla de referencia
    ejercicio_tabla_conversion()
    
    print("\n" + "=" * 80)
    print("FIN DEL EJERCICIO")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
