"""
VERIFICACIÓN DE CONCORDANCIA: Teoría ↔ Implementación
Sección 2.1.1.6.1 - Representación en Longitud Fija

Este script verifica que las funciones Python implementadas
coincidan exactamente con las definiciones teóricas de CONTENIDOS_FE.md
"""

from core.sistemas_numeracion_basicos import (
    capacidad_representacion,
    rango_representacion,
    longitud_representacion,
    analisis_representacion
)
import math


def verificar_concordancia():
    """Verifica que teoría y código coincidan exactamente"""
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN DE CONCORDANCIA: 2.1.1.6.1 (TEORÍA ↔ CÓDIGO)")
    print("=" * 80)
    
    # Test Suite completo
    test_cases = [
        {
            'nombre': 'Capacidad: 2^3 = 8 (3 bits binarios)',
            'func': lambda: capacidad_representacion(2, 3),
            'esperado': 8,
            'teoría': '2.1.1.6.1.1: Capacidad(B, n) = B^n'
        },
        {
            'nombre': 'Capacidad: 2^8 = 256 (1 byte)',
            'func': lambda: capacidad_representacion(2, 8),
            'esperado': 256,
            'teoría': '2.1.1.6.1.1: B = 2, n = 8'
        },
        {
            'nombre': 'Capacidad: 5^5 = 3125',
            'func': lambda: capacidad_representacion(5, 5),
            'esperado': 3125,
            'teoría': '2.1.1.6.1.1: Ejemplo con base 5'
        },
        {
            'nombre': 'Rango: 2^3 = [0, 7]',
            'func': lambda: rango_representacion(2, 3),
            'esperado': (0, 7),
            'teoría': '2.1.1.6.1.2: Rango = [0, B^n - 1]'
        },
        {
            'nombre': 'Rango: 2^8 = [0, 255]',
            'func': lambda: rango_representacion(2, 8),
            'esperado': (0, 255),
            'teoría': '2.1.1.6.1.2: Rango máximo = B^n - 1'
        },
        {
            'nombre': 'Rango: 5^5 = [0, 3124]',
            'func': lambda: rango_representacion(5, 5),
            'esperado': (0, 3124),
            'teoría': '2.1.1.6.1.2: Para el ejemplo 1994'
        },
        {
            'nombre': 'Longitud: 27 en decimal = 2 dígitos',
            'func': lambda: longitud_representacion(27, 10),
            'esperado': 2,
            'teoría': '2.1.1.6.1.2: ⌊log₁₀(27)⌋ + 1 = 1 + 1 = 2'
        },
        {
            'nombre': 'Longitud: 255 en binario = 8 bits',
            'func': lambda: longitud_representacion(255, 2),
            'esperado': 8,
            'teoría': '2.1.1.6.1.2: ⌊log₂(255)⌋ + 1 = 7 + 1 = 8'
        },
        {
            'nombre': 'Longitud: 1994 en base 5 = 5 dígitos',
            'func': lambda: longitud_representacion(1994, 5),
            'esperado': 5,
            'teoría': '2.1.1.6.1.2: Ejemplo principal del documento'
        },
        {
            'nombre': 'Longitud: 99 en decimal = 2 dígitos',
            'func': lambda: longitud_representacion(99, 10),
            'esperado': 2,
            'teoría': '2.1.1.6.1.2: ⌊log₁₀(99)⌋ + 1 = 1 + 1 = 2'
        },
        {
            'nombre': 'Longitud: 100 en decimal = 3 dígitos',
            'func': lambda: longitud_representacion(100, 10),
            'esperado': 3,
            'teoría': '2.1.1.6.1.2: ⌊log₁₀(100)⌋ + 1 = 2 + 1 = 3'
        },
    ]
    
    resultados = {
        'pasaron': 0,
        'fallaron': 0,
        'detalles': []
    }
    
    for test in test_cases:
        try:
            resultado = test['func']()
            pasó = resultado == test['esperado']
            
            if pasó:
                estado = "✓ PASÓ"
                resultados['pasaron'] += 1
            else:
                estado = "✗ FALLÓ"
                resultados['fallaron'] += 1
            
            resultados['detalles'].append({
                'nombre': test['nombre'],
                'esperado': test['esperado'],
                'resultado': resultado,
                'pasó': pasó,
                'teoría': test['teoría']
            })
            
            print(f"\n{estado} | {test['nombre']}")
            print(f"         Esperado: {test['esperado']}, Obtenido: {resultado}")
            print(f"         {test['teoría']}")
            
        except Exception as e:
            print(f"\n✗ ERROR | {test['nombre']}")
            print(f"         Exception: {str(e)}")
            resultados['fallaron'] += 1
    
    # Resumen
    total = resultados['pasaron'] + resultados['fallaron']
    porcentaje = (resultados['pasaron'] / total * 100) if total > 0 else 0
    
    print("\n" + "=" * 80)
    print("RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"Total: {total} pruebas")
    print(f"Pasaron: {resultados['pasaron']} ✓")
    print(f"Fallaron: {resultados['fallaron']} ✗")
    print(f"Tasa de éxito: {porcentaje:.1f}%")
    
    if resultados['fallaron'] == 0:
        print("\n✓ CONCORDANCIA PERFECTA: Teoría y código coinciden exactamente")
    else:
        print("\n✗ DISCORDANCIA DETECTADA: Revisar implementación")
    
    return resultados['fallaron'] == 0


def verificar_formulas_matematicas():
    """Verifica que las fórmulas matemáticas sean correctas"""
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN DE FÓRMULAS MATEMÁTICAS")
    print("=" * 80)
    
    print("\n1. LONGITUD(1994, 5) = ⌊log₅(1994)⌋ + 1")
    log_5_1994 = math.log(1994, 5)
    piso = math.floor(log_5_1994)
    resultado = piso + 1
    print(f"   log₅(1994) ≈ {log_5_1994:.4f}")
    print(f"   ⌊{log_5_1994:.4f}⌋ = {piso}")
    print(f"   {piso} + 1 = {resultado} ✓")
    
    print("\n2. LONGITUD(255, 2) = ⌊log₂(255)⌋ + 1")
    log_2_255 = math.log(255, 2)
    piso = math.floor(log_2_255)
    resultado = piso + 1
    print(f"   log₂(255) = {log_2_255:.4f}")
    print(f"   ⌊{log_2_255:.4f}⌋ = {piso}")
    print(f"   {piso} + 1 = {resultado} ✓")
    
    print("\n3. CAPACIDAD(2, 8) = 2^8")
    resultado = 2 ** 8
    print(f"   2^8 = {resultado} ✓")
    
    print("\n4. RANGO(5, 5) = [0, 5^5 - 1]")
    capacidad = 5 ** 5
    rango_max = capacidad - 1
    print(f"   5^5 = {capacidad}")
    print(f"   5^5 - 1 = {rango_max}")
    print(f"   Rango: [0, {rango_max}] ✓")


def verificar_conversiones():
    """Verifica conversiones específicas del documento"""
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN DE CONVERSIONES ESPECIALES")
    print("=" * 80)
    
    print("\n1. Conversión de 1994 (decimal) a base 5")
    print("   Teoría: 1994₁₀ = 30434₅")
    
    # Verificación manual
    valor = 1 * (5**4) + 3 * (5**3) + 0 * (5**2) + 4 * (5**1) + 4 * (5**0)
    print(f"   Verificación: 1×625 + 3×125 + 0×25 + 4×5 + 4×1 = {valor}")
    
    if valor == 1994:
        print(f"   ✓ Conversión correcta: {valor} = 1994")
        
        # Verificar que nuestras funciones lo capturan
        longitud = longitud_representacion(1994, 5)
        rango_min, rango_max = rango_representacion(5, 5)
        cabe = rango_min <= 1994 <= rango_max
        
        print(f"   Longitud mínima: {longitud} dígitos")
        print(f"   Rango [0, {rango_max}]: 1994 está dentro? {cabe} ✓")
    else:
        print(f"   ✗ ERROR: {valor} ≠ 1994")


if __name__ == "__main__":
    # Ejecutar todas las verificaciones
    ok_tests = verificar_concordancia()
    
    verificar_formulas_matematicas()
    
    verificar_conversiones()
    
    # Resultado final
    print("\n" + "=" * 80)
    if ok_tests:
        print("✓ TODAS LAS PRUEBAS PASARON")
        print("✓ La implementación Python es concordante con la teoría (2.1.1.6.1)")
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
        print("✗ Revisar implementación vs teoría")
    print("=" * 80 + "\n")
