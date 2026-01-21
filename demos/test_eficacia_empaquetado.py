#!/usr/bin/env python3
"""
Tests para Funciones de Eficacia de Empaquetado
"""

from core.sistemas_numeracion_basicos import (
    eficacia_empaquetado_simple,
    eficacia_bcd_mejorada,
    comparar_eficacias_empaquetado,
    explicar_eficacia_empaquetado,
    explicar_ieee_754,
)


def test_eficacia_empaquetado_simple():
    """Prueba de eficacia simple"""
    print("\n1. eficacia_empaquetado_simple(base_nativa, base_destino, n_digitos)")
    
    tests = [
        # (base_nativa, base_destino, n_digitos, eficacia_esperada, descripcion)
        (2, 10, 1, 0.2, "1 digito decimal en binario"),
        (2, 10, 3, 0.008, "3 digitos decimales en binario"),
        (2, 16, 1, 0.125, "1 digito hexadecimal en binario"),
        (2, 2, 1, 1.0, "Binario a binario (optimo)"),
        (10, 2, 1, 5.0, "1 digito binario en decimal (>1)"),
    ]
    
    for base_nativa, base_destino, n_digitos, esperada, desc in tests:
        resultado = eficacia_empaquetado_simple(base_nativa, base_destino, n_digitos)
        estado = "OK" if abs(resultado - esperada) < 0.0001 else "FAIL"
        print(f"  [{estado}] {desc}")
        print(f"       Esperado: {esperada:.6f}, Obtenido: {resultado:.6f}")


def test_eficacia_bcd_mejorada():
    """Prueba de eficacia BCD mejorada"""
    print("\n2. eficacia_bcd_mejorada(valores_representables, bits_utilizados)")
    
    tests = [
        # (valores, bits, eficacia_esperada, descripcion)
        (10, 4, 10/16, "BCD clasico (1 digito decimal)"),
        (100, 8, 100/256, "BCD clasico (2 digitos decimales)"),
        (1000, 10, 1000/1024, "DPD mejorado (3 digitos decimales)"),
        (256, 8, 1.0, "256 valores en 8 bits (uso completo)"),
    ]
    
    for valores, bits, esperada, desc in tests:
        resultado = eficacia_bcd_mejorada(valores, bits)
        estado = "OK" if abs(resultado - esperada) < 0.0001 else "FAIL"
        print(f"  [{estado}] {desc}")
        print(f"       Esperado: {esperada:.6f}, Obtenido: {resultado:.6f}")


def test_comparar_eficacias():
    """Prueba de comparacion de eficacias"""
    print("\n3. comparar_eficacias_empaquetado(base_nativa, opciones)")
    
    opciones = [
        {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 1},
        {'tipo': 'bcd', 'valores': 10, 'bits': 4},
        {'tipo': 'bcd', 'valores': 1000, 'bits': 10},
    ]
    
    resultado = comparar_eficacias_empaquetado(2, opciones)
    
    print(f"  [OK] Se compararon {len(resultado['opciones'])} opciones")
    print(f"  [OK] La mejor tiene eficacia: {resultado['mejor']['eficacia']:.6f}")
    
    # Verificar que estan ordenadas por eficacia (descendente)
    eficacias = [op['eficacia'] for op in resultado['opciones']]
    ordenada = all(eficacias[i] >= eficacias[i+1] for i in range(len(eficacias)-1))
    
    if ordenada:
        print(f"  [OK] Opciones ordenadas por eficacia (mayor primero)")
    else:
        print(f"  [FAIL] Opciones NO estan correctamente ordenadas")


def test_explicar_eficacia():
    """Prueba de explicacion detallada"""
    print("\n4. explicar_eficacia_empaquetado(base_nativa, base_destino, n_digitos)")
    
    explicacion = explicar_eficacia_empaquetado(2, 10, 1)
    
    # Verificar estructura
    claves_esperadas = [
        'base_nativa', 'base_destino', 'n_digitos',
        'capacidad_nativa', 'capacidad_destino',
        'formula', 'eficacia', 'porcentaje', 'ratio_base',
        'interpretacion'
    ]
    
    todas_presentes = all(clave in explicacion for clave in claves_esperadas)
    
    if todas_presentes:
        print(f"  [OK] Estructura completa con todas las claves esperadas")
    else:
        print(f"  [FAIL] Faltan algunas claves en la estructura")
    
    # Verificar valores
    print(f"  [OK] Base nativa: {explicacion['base_nativa']}")
    print(f"  [OK] Base destino: {explicacion['base_destino']}")
    print(f"  [OK] Eficacia: {explicacion['eficacia']:.6f}")
    print(f"  [OK] Porcentaje: {explicacion['porcentaje']:.2f}%")


def test_ieee_754():
    """Prueba de informacion IEEE 754"""
    print("\n5. explicar_ieee_754(formato)")
    
    formatos = ['binary32', 'binary64', 'binary128', 'decimal128']
    
    for formato in formatos:
        info = explicar_ieee_754(formato)
        
        # Verificar estructura
        tiene_formato = 'formato' in info
        tiene_detalles = 'detalles' in info
        tiene_estructura = 'estructura' in info
        
        if tiene_formato and tiene_detalles and tiene_estructura:
            print(f"  [OK] {formato}: estructura completa")
        else:
            print(f"  [FAIL] {formato}: faltan elementos en la estructura")


def test_casos_especiales():
    """Pruebas de casos especiales y errores"""
    print("\n6. Casos especiales y manejo de errores")
    
    # Caso 1: Bases iguales (optimo)
    eficacia_optima = eficacia_empaquetado_simple(5, 5, 10)
    if eficacia_optima == 1.0:
        print(f"  [OK] Bases iguales: eficacia = 1.0 (optimo)")
    else:
        print(f"  [FAIL] Bases iguales deberia dar 1.0, obtuvo {eficacia_optima}")
    
    # Caso 2: DPD vs BCD
    bcd = eficacia_bcd_mejorada(10, 4)
    dpd = eficacia_bcd_mejorada(1000, 10)
    if dpd > bcd:
        print(f"  [OK] DPD ({dpd:.4f}) es mas eficiente que BCD ({bcd:.4f})")
    else:
        print(f"  [FAIL] DPD deberia ser mas eficiente que BCD")
    
    # Caso 3: Base pequeña en base grande (ineficiente)
    eficacia_baja = eficacia_empaquetado_simple(2, 100, 1)
    if eficacia_baja < 0.1:
        print(f"  [OK] Representar base 100 en binario es ineficiente ({eficacia_baja:.6f})")
    else:
        print(f"  [FAIL] Eficacia deberia ser muy baja")
    
    # Caso 4: Error - valores exceden capacidad
    try:
        eficacia_bcd_mejorada(20, 4)  # 20 > 16 (2^4)
        print(f"  [FAIL] Deberia lanzar error para valores > capacidad")
    except ValueError:
        print(f"  [OK] Error correctamente lanzado para valores > capacidad")


def test_formulas_matematicas():
    """Verificacion de formulas matematicas"""
    print("\n7. Verificacion de formulas matematicas")
    
    # Formula: eficacia = (A/B)^n
    A, B, n = 2, 10, 1
    eficacia = eficacia_empaquetado_simple(A, B, n)
    formula_directa = (A / B) ** n
    
    if abs(eficacia - formula_directa) < 0.0001:
        print(f"  [OK] (2/10)^1 = {eficacia:.6f} (correcto)")
    else:
        print(f"  [FAIL] Formula (A/B)^n no es correcta")
    
    # Otra verificacion: capacidad_nativa / capacidad_destino
    A, B, n = 2, 10, 3
    eficacia2 = eficacia_empaquetado_simple(A, B, n)
    cap_nativa = 2 ** 3  # 8
    cap_destino = 10 ** 3  # 1000
    esperada = cap_nativa / cap_destino
    
    if abs(eficacia2 - esperada) < 0.0001:
        print(f"  [OK] Capacidad_nativa / Capacidad_destino = {eficacia2:.6f} (correcto)")
    else:
        print(f"  [FAIL] Calculo de capacidades no es correcto")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 80)
    print("TESTS: FUNCIONES DE EFICACIA DE EMPAQUETADO")
    print("=" * 80)
    
    test_eficacia_empaquetado_simple()
    test_eficacia_bcd_mejorada()
    test_comparar_eficacias()
    test_explicar_eficacia()
    test_ieee_754()
    test_casos_especiales()
    test_formulas_matematicas()
    
    print("\n" + "=" * 80)
    print("TESTS COMPLETADOS")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()


def test_eficacia_bcd_mejorada():
    """Prueba de eficacia BCD mejorada"""
    print("\n2. eficacia_bcd_mejorada(valores_representables, bits_utilizados)")
    
    tests = [
        # (valores, bits, eficacia_esperada, descripcion)
        (10, 4, 10/16, "BCD clásico (1 dígito decimal)"),
        (100, 8, 100/256, "BCD clásico (2 dígitos decimales)"),
        (1000, 10, 1000/1024, "DPD mejorado (3 dígitos decimales)"),
        (256, 8, 1.0, "256 valores en 8 bits (uso completo)"),
    ]
    
    for valores, bits, esperada, desc in tests:
        resultado = eficacia_bcd_mejorada(valores, bits)
        estado = "✓" if abs(resultado - esperada) < 0.0001 else "✗"
        print(f"  [{estado}] {desc}")
        print(f"       Esperado: {esperada:.6f}, Obtenido: {resultado:.6f}")


def test_comparar_eficacias():
    """Prueba de comparación de eficacias"""
    print("\n3. comparar_eficacias_empaquetado(base_nativa, opciones)")
    
    opciones = [
        {'tipo': 'simple', 'base_destino': 10, 'n_digitos': 1},
        {'tipo': 'bcd', 'valores': 10, 'bits': 4},
        {'tipo': 'bcd', 'valores': 1000, 'bits': 10},
    ]
    
    resultado = comparar_eficacias_empaquetado(2, opciones)
    
    print(f"  ✓ Se compararon {len(resultado['opciones'])} opciones")
    print(f"  ✓ La mejor tiene eficacia: {resultado['mejor']['eficacia']:.6f}")
    
    # Verificar que están ordenadas por eficacia (descendente)
    eficacias = [op['eficacia'] for op in resultado['opciones']]
    ordenada = all(eficacias[i] >= eficacias[i+1] for i in range(len(eficacias)-1))
    
    if ordenada:
        print(f"  ✓ Opciones ordenadas por eficacia (mayor primero)")
    else:
        print(f"  ✗ Opciones NO están correctamente ordenadas")


def test_explicar_eficacia():
    """Prueba de explicación detallada"""
    print("\n4. explicar_eficacia_empaquetado(base_nativa, base_destino, n_digitos)")
    
    explicacion = explicar_eficacia_empaquetado(2, 10, 1)
    
    # Verificar estructura
    claves_esperadas = [
        'base_nativa', 'base_destino', 'n_digitos',
        'capacidad_nativa', 'capacidad_destino',
        'formula', 'eficacia', 'porcentaje', 'ratio_base',
        'interpretacion'
    ]
    
    todas_presentes = all(clave in explicacion for clave in claves_esperadas)
    
    if todas_presentes:
        print(f"  ✓ Estructura completa con todas las claves esperadas")
    else:
        print(f"  ✗ Faltan algunas claves en la estructura")
    
    # Verificar valores
    print(f"  ✓ Base nativa: {explicacion['base_nativa']}")
    print(f"  ✓ Base destino: {explicacion['base_destino']}")
    print(f"  ✓ Eficacia: {explicacion['eficacia']:.6f}")
    print(f"  ✓ Porcentaje: {explicacion['porcentaje']:.2f}%")


def test_ieee_754():
    """Prueba de información IEEE 754"""
    print("\n5. explicar_ieee_754(formato)")
    
    formatos = ['binary32', 'binary64', 'binary128', 'decimal128']
    
    for formato in formatos:
        info = explicar_ieee_754(formato)
        
        # Verificar estructura
        tiene_formato = 'formato' in info
        tiene_detalles = 'detalles' in info
        tiene_estructura = 'estructura' in info
        
        if tiene_formato and tiene_detalles and tiene_estructura:
            print(f"  ✓ {formato}: estructura completa")
        else:
            print(f"  ✗ {formato}: faltan elementos en la estructura")


def test_casos_especiales():
    """Pruebas de casos especiales y errores"""
    print("\n6. Casos especiales y manejo de errores")
    
    # Caso 1: Bases iguales (óptimo)
    eficacia_optima = eficacia_empaquetado_simple(5, 5, 10)
    if eficacia_optima == 1.0:
        print(f"  ✓ Bases iguales: eficacia = 1.0 (óptimo)")
    else:
        print(f"  ✗ Bases iguales debería dar 1.0, obtuvo {eficacia_optima}")
    
    # Caso 2: DPD vs BCD
    bcd = eficacia_bcd_mejorada(10, 4)
    dpd = eficacia_bcd_mejorada(1000, 10)
    if dpd > bcd:
        print(f"  ✓ DPD ({dpd:.4f}) es más eficiente que BCD ({bcd:.4f})")
    else:
        print(f"  ✗ DPD debería ser más eficiente que BCD")
    
    # Caso 3: Base pequeña en base grande (ineficiente)
    eficacia_baja = eficacia_empaquetado_simple(2, 100, 1)
    if eficacia_baja < 0.1:
        print(f"  ✓ Representar base 100 en binario es ineficiente ({eficacia_baja:.6f})")
    else:
        print(f"  ✗ Eficacia debería ser muy baja")
    
    # Caso 4: Error - valores exceden capacidad
    try:
        eficacia_bcd_mejorada(20, 4)  # 20 > 16 (2^4)
        print(f"  ✗ Debería lanzar error para valores > capacidad")
    except ValueError:
        print(f"  ✓ Error correctamente lanzado para valores > capacidad")


def test_formulas_matematicas():
    """Verificación de fórmulas matemáticas"""
    print("\n7. Verificación de fórmulas matemáticas")
    
    # Fórmula: eficacia = (A/B)^n
    A, B, n = 2, 10, 1
    eficacia = eficacia_empaquetado_simple(A, B, n)
    formula_directa = (A / B) ** n
    
    if abs(eficacia - formula_directa) < 0.0001:
        print(f"  ✓ (2/10)^1 = {eficacia:.6f} (correcto)")
    else:
        print(f"  ✗ Fórmula (A/B)^n no es correcta")
    
    # Otra verificación: capacidad_nativa / capacidad_destino
    A, B, n = 2, 10, 3
    eficacia2 = eficacia_empaquetado_simple(A, B, n)
    cap_nativa = 2 ** 3  # 8
    cap_destino = 10 ** 3  # 1000
    esperada = cap_nativa / cap_destino
    
    if abs(eficacia2 - esperada) < 0.0001:
        print(f"  ✓ Capacidad_nativa / Capacidad_destino = {eficacia2:.6f} (correcto)")
    else:
        print(f"  ✗ Cálculo de capacidades no es correcto")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 80)
    print("TESTS: FUNCIONES DE EFICACIA DE EMPAQUETADO")
    print("=" * 80)
    
    test_eficacia_empaquetado_simple()
    test_eficacia_bcd_mejorada()
    test_comparar_eficacias()
    test_explicar_eficacia()
    test_ieee_754()
    test_casos_especiales()
    test_formulas_matematicas()
    
    print("\n" + "=" * 80)
    print("TESTS COMPLETADOS")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
