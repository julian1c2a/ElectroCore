#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demostraciones: Conversión entre Bases Relacionadas

Cuando tenemos un número en base B^l y queremos pasarlo a base B^k,
podemos usar un algoritmo optimizado que:

1. Reconoce que ambas bases son potencias de la misma base B
2. Agrupa dígitos inteligentemente
3. Convierte sin pasar por decimal intermedio

Ejemplos: 2↔4↔8↔16↔32, 3↔9↔27, 5↔25, 6↔36
"""

from core.conversiones_bases_relacionadas import (
    convertir_bases_relacionadas,
    convertir_bases_relacionadas_tabla,
    comparar_conversiones_bases_relacionadas,
    encontrar_base_primitiva
)


def demo_1_basico():
    """Demo 1: Conversiones básicas binario ↔ hexadecimal"""
    print("\n" + "=" * 70)
    print("DEMO 1: Conversiones Binario ↔ Hexadecimal")
    print("=" * 70)
    print("\nBinario (2) ↔ Hexadecimal (16)")
    print("Porque 2 = 2^1 y 16 = 2^4, ambas son potencias de 2")
    print()
    
    ejemplos = [
        ("1111", 2, 16),      # F
        ("11111111", 2, 16),  # FF
        ("10101010", 2, 16),  # AA
    ]
    
    for numero, base_orig, base_dest in ejemplos:
        resultado = convertir_bases_relacionadas(numero, base_orig, base_dest)
        print(f"  {numero}₂ = {resultado['resultado']}₁₆")


def demo_2_binario_octal():
    """Demo 2: Binario a Octal (2 → 8)"""
    print("\n" + "=" * 70)
    print("DEMO 2: Conversión Binario a Octal")
    print("=" * 70)
    print("\nBinario (2) → Octal (8)")
    print("Porque 2 = 2^1 y 8 = 2^3, ambas son potencias de 2")
    print("Agrupamos cada 3 dígitos binarios en 1 octal")
    print()
    
    numero = "101101010"
    print(f"Número: {numero}₂")
    print(f"Agrupamos: (101)(101)(010) = 5,5,2")
    
    resultado = convertir_bases_relacionadas(numero, 2, 8)
    print(f"Resultado: {resultado['resultado']}₈")
    print()


def demo_3_potencias_tres():
    """Demo 3: Conversiones con potencias de 3"""
    print("\n" + "=" * 70)
    print("DEMO 3: Conversiones con Potencias de 3")
    print("=" * 70)
    print("\n3 = 3^1, 9 = 3^2, 27 = 3^3 (todas potencias de 3)")
    print()
    
    ejemplos = [
        ("12101", 3, 9),       # Base 3 → Base 9
        ("102", 9, 3),         # Base 9 → Base 3
        ("21212", 3, 27),      # Base 3 → Base 27
    ]
    
    for numero, base_orig, base_dest in ejemplos:
        resultado = convertir_bases_relacionadas(numero, base_orig, base_dest)
        B, l, k = encontrar_base_primitiva(base_orig, base_dest)
        print(f"  {numero}_{base_orig} → {resultado['resultado']}_{base_dest}")
        print(f"    (Base primitiva: {B}, exponentes: {l} y {k})")


def demo_4_pasos_detallados():
    """Demo 4: Paso a paso detallado de conversión"""
    print("\n" + "=" * 70)
    print("DEMO 4: Paso a Paso Detallado")
    print("=" * 70)
    print("\nConversión: 1010₂ → ₁₆")
    print()
    
    numero = "1010"
    print(f"Número original: {numero}₂")
    print()
    
    resultado = convertir_bases_relacionadas_tabla(numero, 2, 16)
    
    print(f"Base primitiva: {resultado['base_primitiva']} (porque 2 = 2^1, 16 = 2^4)")
    print(f"Exponentes: l={resultado['exponentes'][0]}, k={resultado['exponentes'][1]}")
    print(f"GCD(l, k) = {resultado['gcd_exponentes']}")
    print(f"l' = {resultado['exponentes'][0]}/{resultado['gcd_exponentes']} = {resultado['l_prima']}")
    print(f"k' = {resultado['exponentes'][1]}/{resultado['gcd_exponentes']} = {resultado['k_prima']}")
    print()
    
    print("Proceso:")
    for paso in resultado['pasos']:
        if paso.get('paso') == 'inicializacion':
            print(f"  Paso 0: {paso['descripcion']}")
        elif paso.get('paso') == 1:
            print(f"  Paso 1: Convertir cada dígito a {paso['descripcion'].split()[-1]} dígitos en base 2")
            print(f"         {paso['dígitos_originales']}₂ → {paso['dígitos_en_B']}₂")
        elif paso.get('paso') == 2:
            print(f"  Paso 2: Agrupar de 4 en 4 (k'={resultado['k_prima']})")
            for i, grupo in enumerate(paso['grupos']):
                print(f"         Grupo {i+1}: {' '.join(grupo)}")
        elif paso.get('paso') == 3:
            print(f"         {paso['grupo']}₂ = {paso['valor_en_B']}₁₀ = {paso['dígito_destino']}₁₆")
    
    print()
    print(f"Resultado final: {resultado['resultado']}₁₆")
    print()


def demo_5_comparacion():
    """Demo 5: Comparación de métodos"""
    print("\n" + "=" * 70)
    print("DEMO 5: Comparación Método Optimizado vs Tradicional")
    print("=" * 70)
    print()
    
    numero = "11111111"
    comparacion = comparar_conversiones_bases_relacionadas(numero, 2, 16)
    
    print(f"Número: {numero}₂")
    print(f"Destino: Base 16")
    print()
    
    print(f"Método Optimizado:  {comparacion['resultado_optimizado']}₁₆")
    print(f"Método Tradicional: {comparacion['resultado_tradicional']}₁₆")
    print(f"Coinciden: {comparacion['coinciden']} ✓")
    print()
    print("Ventajas del método optimizado:")
    print("  • No necesita conversión a decimal")
    print("  • Agrupa dígitos inteligentemente")
    print("  • Más rápido para bases relacionadas")


def demo_6_tabla_completa():
    """Demo 6: Tabla de conversiones entre potencias de 2"""
    print("\n" + "=" * 70)
    print("DEMO 6: Tabla de Conversiones (Potencias de 2)")
    print("=" * 70)
    print()
    print("Tabla: Número 255 en diferentes bases (potencias de 2)")
    print()
    
    numero = 255
    bases = [2, 4, 8, 16, 32]
    
    # Convertir de base 10 a cada base (método tradicional)
    representaciones = {}
    for base in bases:
        dígitos = []
        n = numero
        if n == 0:
            dígitos = [0]
        else:
            while n > 0:
                dígitos.append(n % base)
                n //= base
            dígitos = dígitos[::-1]
        
        # Convertir a string
        resultado_str = ""
        for d in dígitos:
            if d < 10:
                resultado_str += str(d)
            else:
                resultado_str += chr(ord('A') + d - 10)
        
        representaciones[base] = resultado_str
    
    print(f"{'Base':<6} | {'Representación':<20} | {'Observación'}")
    print("-" * 60)
    for base in bases:
        obs = f"(2^{bases.index(base)+1})" if base > 2 else "(base primitiva)"
        print(f"{base:<6} | {representaciones[base]:<20} | {obs}")
    
    print()
    print("Ahora vamos a convertir entre estas bases usando el algoritmo optimizado:")
    print()
    
    # Demostrar conversiones optimizadas
    ejemplos = [
        (representaciones[2], 2, 8),
        (representaciones[8], 8, 16),
        (representaciones[16], 16, 2),
    ]
    
    for numero_str, base_orig, base_dest in ejemplos:
        resultado = convertir_bases_relacionadas(numero_str, base_orig, base_dest)
        print(f"  {numero_str}_{base_orig} → {resultado['resultado']}_{base_dest} ✓")


def demo_7_errores():
    """Demo 7: Manejo de errores"""
    print("\n" + "=" * 70)
    print("DEMO 7: Validación y Manejo de Errores")
    print("=" * 70)
    print()
    
    casos = [
        ("1010", 2, 3, "Bases no relacionadas (2 no es potencia de 3)"),
        ("1010", 2, 5, "Bases no relacionadas (2 no es potencia de 5)"),
        ("102", 2, 8, "Dígito inválido en base 2"),
    ]
    
    for numero, base_orig, base_dest, descripcion in casos:
        print(f"Caso: {descripcion}")
        print(f"  Intento: {numero}_{base_orig} → base {base_dest}")
        try:
            resultado = convertir_bases_relacionadas(numero, base_orig, base_dest)
            print(f"  Resultado: {resultado['resultado']}")
        except ValueError as e:
            print(f"  Error (esperado): {e}")
        print()


def demo_8_base_6_36():
    """Demo 8: Conversión entre base 6 y 36"""
    print("\n" + "=" * 70)
    print("DEMO 8: Conversión Base 6 ↔ Base 36")
    print("=" * 70)
    print()
    print("Base 6 = 6^1 y Base 36 = 6^2")
    print("Cada dígito en base 36 representa 2 dígitos en base 6")
    print()
    
    numero = "123454"  # En base 6
    print(f"Número: {numero} (base 6)")
    
    resultado = convertir_bases_relacionadas(numero, 6, 36)
    print(f"Resultado: {resultado['resultado']} (base 36)")
    print()
    
    # Inversa
    print(f"Inversa: {resultado['resultado']}₃₆ → base 6")
    resultado_inv = convertir_bases_relacionadas(resultado['resultado'], 36, 6)
    print(f"Resultado: {resultado_inv['resultado']} (base 6)")
    print(f"Coincide con original: {resultado_inv['resultado'] == numero} ✓")


if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("Conversión entre Bases Relacionadas (Potencias de misma base)".center(70))
    print("=" * 70)
    
    demo_1_basico()
    demo_2_binario_octal()
    demo_3_potencias_tres()
    demo_4_pasos_detallados()
    demo_5_comparacion()
    demo_6_tabla_completa()
    demo_7_errores()
    demo_8_base_6_36()
    
    print("\n" + "=" * 70)
    print("Todas las demostraciones completadas")
    print("=" * 70 + "\n")
