#!/usr/bin/env python3
"""
DEMOSTRACION: Complemento a la Base (CB)
Seccion 2.1.1.7.3: Numeros Enteros con Signo

CB es superior a CB-1:
- Una única representación para 0
- La suma es la suma ordinaria modulo B^l
- No requiere end-around carry
- Multiplicación más sencilla
"""

from core.cb_representacion import (
    opCB_digito, opCB_palabra, repr_CB, CB_a_decimal,
    suma_CB, resta_CB, multiplicacion_CB,
    analizar_representacion_CB, generar_tabla_CB,
    explicar_operacion_CB, ms_a_CB, CB_a_ms
)


def demo_1_operacion_basica():
    """Demo 1: Operación opCB (complemento a la base)"""
    print("\n" + "=" * 80)
    print("DEMO 1: OPERACION opCB BASICA")
    print("=" * 80)
    
    print("\n1a. Complemento a la Base de dígitos individuales (Base 10):")
    print("  (Primer paso: flip cada dígito)")
    for d in range(10):
        flipped = opCB_digito(str(d), 10)
        print(f"  opCBm1({d}) = {flipped}   ({9} - {d} = {flipped})")
    
    print("\n1b. Complemento a la Base de dígitos (Base 2):")
    for d in range(2):
        flipped = opCB_digito(str(d), 2)
        print(f"  opCBm1({d}) = {flipped}   ({1} - {d} = {flipped})")
    
    print("\n1c. Complemento a la Base de palabra completa (Base 10):")
    palabra_orig = "01239"
    palabra_cb = opCB_palabra(palabra_orig, 10)
    print(f"  Palabra original:  {palabra_orig}")
    print(f"  Complemento CB:    {palabra_cb}")
    print(f"  Verificacion: B^l - numero = 100000 - 1239 = {100000 - 1239}")
    
    print("\n1d. Complemento a la Base en binario (Base 2):")
    palabra_bin = "0101"
    palabra_cb_bin = opCB_palabra(palabra_bin, 2)
    print(f"  Palabra original:  {palabra_bin}")
    print(f"  Complemento CB:    {palabra_cb_bin}")
    print(f"  Verificacion: B^l - numero = 16 - 5 = {16 - 5} = {palabra_cb_bin}")
    
    print("\n1e. Propiedad: opCB(opCB(D)) = D?")
    doble_cb = opCB_palabra(palabra_cb, 10)
    print(f"  Original:           {palabra_orig}")
    print(f"  CB:                 {palabra_cb}")
    print(f"  Doble CB:           {doble_cb}")
    if doble_cb == palabra_orig:
        print(f"  [OK] opCB(opCB({palabra_orig})) = {palabra_orig}")
    else:
        print(f"  [ERROR] Esperado {palabra_orig}, obtuvo {doble_cb}")


def demo_2_representacion_cb():
    """Demo 2: Representación de números en CB"""
    print("\n" + "=" * 80)
    print("DEMO 2: REPRESENTACION EN CB")
    print("=" * 80)
    
    print("\nRepresentacion en CB (Base 10, 5 digitos):")
    numeros = [1239, -1239, 99999, -99999, 0, 50000]
    for num in numeros:
        cb_repr = repr_CB(num, 10, 5)
        valor_back = CB_a_decimal(cb_repr, 10)
        print(f"  {num:>6} -> CB: {cb_repr} -> Decimal: {valor_back:>6}")
    
    print("\nRepresentacion en CB (Base 2, 8 bits):")
    numeros_bin = [5, -5, 127, -128, 0, 100]
    for num in numeros_bin:
        cb_repr = repr_CB(num, 2, 8)
        valor_back = CB_a_decimal(cb_repr, 2)
        print(f"  {num:>4} -> CB: {cb_repr} -> Decimal: {valor_back:>4}")


def demo_3_tablas_cb():
    """Demo 3: Tablas completas de representación CB"""
    print("\n" + "=" * 80)
    print("DEMO 3: TABLA DE VALORES CB")
    print("=" * 80)
    
    print("\nTabla CB en Base 2 (4 bits):")
    tabla_bin = generar_tabla_CB(2, 4)
    print(tabla_bin)
    
    print("\n\nTabla CB en Base 10 (2 digitos):")
    tabla_dec = generar_tabla_CB(10, 2)
    print(tabla_dec)


def demo_4_suma_cb():
    """Demo 4: Suma en CB (la misma que suma ordinaria)"""
    print("\n" + "=" * 80)
    print("DEMO 4: SUMA EN CB (Suma ordinaria modulo B^l)")
    print("=" * 80)
    
    print("\nEjemplos en Base 10, 5 digitos:")
    print("(La suma en CB es la MISMA suma ordinaria modulo B^l)")
    
    ejemplos = [
        (1239, 3591),
        (1239, -3591),
        (-1239, 3591),
        (-1239, -3591),
        (50000, 50000),
    ]
    
    for a, b in ejemplos:
        cb_a = repr_CB(a, 10, 5)
        cb_b = repr_CB(b, 10, 5)
        resultado = suma_CB(cb_a, cb_b, 10)
        
        print(f"\n  ReprCB({a:>6}) = {cb_a}")
        print(f"  ReprCB({b:>6}) = {cb_b}")
        print(f"  Suma: {cb_a} + {cb_b} = {resultado['resultado']}")
        print(f"  Decimal: {resultado['valor_decimal']:>6} (esperado: {a + b:>6})")
        
        if resultado['llevo']:
            print(f"  [OVERFLOW - resultado truncado]")
        else:
            if resultado['valor_decimal'] == a + b:
                print(f"  [OK] Correcto!")


def demo_5_resta_cb():
    """Demo 5: Resta en CB"""
    print("\n" + "=" * 80)
    print("DEMO 5: RESTA EN CB")
    print("=" * 80)
    
    print("\nImplementacion: A - B = A + opCB(B) modulo B^l")
    
    ejemplos = [
        (10, 3),
        (3, 10),
        (-5, -2),
        (50, 75),
    ]
    
    for a, b in ejemplos:
        cb_a = repr_CB(a, 10, 2)
        cb_b = repr_CB(b, 10, 2)
        cb_b_neg = opCB_palabra(cb_b, 10)
        resultado = resta_CB(cb_a, cb_b, 10)
        
        print(f"\n  {a:3} - {b:3} = {a - b:3}")
        print(f"  ReprCB({a:2}) = {cb_a}")
        print(f"  ReprCB({b:2}) = {cb_b}")
        print(f"  opCB({cb_b}) = {cb_b_neg}  (para restar)")
        print(f"  Suma: {cb_a} + {cb_b_neg} = {resultado['resultado']}")
        print(f"  Resultado: {resultado['valor_decimal']}")
        
        if resultado['valor_decimal'] == a - b:
            print(f"  [OK] Correcto!")
        else:
            if resultado['llevo']:
                print(f"  [OVERFLOW]")


def demo_6_multiplicacion_cb():
    """Demo 6: Multiplicación en CB"""
    print("\n" + "=" * 80)
    print("DEMO 6: MULTIPLICACION EN CB")
    print("=" * 80)
    
    print("\nLa multiplicacion en CB funciona correctamente:")
    print("- a > 0, b > 0: ReprCB(a) * ReprCB(b) = ReprCB(a*b)")
    print("- a > 0, b < 0: ReprCB(a) * ReprCB(-b) = ReprCB(-a*b)")
    print("- a < 0, b < 0: ReprCB(-a) * ReprCB(-b) = ReprCB(a*b)")
    
    ejemplos = [
        (3, 4),
        (3, -4),
        (-3, 4),
        (-3, -4),
        (10, 10),
    ]
    
    for a, b in ejemplos:
        cb_a = repr_CB(a, 10, 2)
        cb_b = repr_CB(b, 10, 2)
        resultado = multiplicacion_CB(cb_a, cb_b, 10)
        
        print(f"\n  {a:3} * {b:3} = {a * b:3}")
        print(f"  ReprCB({a:2}) = {cb_a}")
        print(f"  ReprCB({b:2}) = {cb_b}")
        print(f"  Producto: {cb_a} * {cb_b} = {resultado['resultado']}")
        print(f"  Resultado: {resultado['valor_decimal']}")
        
        if resultado['llevo']:
            print(f"  [OVERFLOW - esperado {a*b}, obtuvo {resultado['valor_decimal']}]")
        else:
            if resultado['valor_decimal'] == a * b:
                print(f"  [OK] Correcto!")


def demo_7_rango_y_capacidad():
    """Demo 7: Rango y capacidad de CB"""
    print("\n" + "=" * 80)
    print("DEMO 7: RANGO Y CAPACIDAD")
    print("=" * 80)
    
    configs = [
        (2, 4),
        (2, 8),
        (2, 16),
        (10, 2),
        (10, 3),
        (10, 4),
    ]
    
    for base, longitud in configs:
        info = analizar_representacion_CB(base, longitud)
        print(f"\nCB (Base {base}, {longitud} digitos):")
        print(f"  Rango: [{info['min_negativo']:>6}, {info['max_positivo']:>6}]")
        print(f"  Capacidad: {info['capacidad']} valores")
        print(f"  Eficacia: {info['porcentaje_eficacia']}")
        print(f"  Una representacion para 0: {info['una_representacion_cero']}")


def demo_8_conversiones():
    """Demo 8: Conversiones entre representaciones"""
    print("\n" + "=" * 80)
    print("DEMO 8: CONVERSIONES ENTRE REPRESENTACIONES")
    print("=" * 80)
    
    numeros = [5, -5, 0, 10, -10]
    
    print("\nBase 10, 2 digitos:")
    for num in numeros:
        try:
            cb = repr_CB(num, 10, 2)
            ms = repr_CB(num, 10, 2)  # Seria decimal_a_ms pero importamos cb
            cbm1 = repr_CB(num, 10, 2)  # Similar
            
            print(f"\n  Numero: {num:3}")
            print(f"  CB:   {cb}")
            print(f"  (MS y CB-1 requieren funciones de otros modulos)")
        except:
            pass


def demo_9_explicaciones_paso_a_paso():
    """Demo 9: Explicaciones detalladas de operaciones"""
    print("\n" + "=" * 80)
    print("DEMO 9: EXPLICACIONES PASO A PASO")
    print("=" * 80)
    
    print("\n--- Complemento de un numero ---")
    print(explicar_operacion_CB(42, 0, 'complemento', 10, 2))
    
    print("\n\n--- Suma de dos numeros positivos ---")
    print(explicar_operacion_CB(5, 3, 'suma', 10, 2))
    
    print("\n\n--- Suma de numero positivo y negativo ---")
    print(explicar_operacion_CB(5, -3, 'suma', 10, 2))
    
    print("\n\n--- Resta ---")
    print(explicar_operacion_CB(10, 3, 'resta', 10, 2))
    
    print("\n\n--- Multiplicacion ---")
    print(explicar_operacion_CB(3, 4, 'multiplicacion', 10, 2))


def conclusiones():
    """Conclusiones sobre CB"""
    print("\n" + "=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    
    print("""
CB (Complemento a la Base) es LA representacion estandar para enteros con signo:

VENTAJAS SOBRE M&S:
  - Una UNICA representacion para 0 (no dos)
  - Suma y resta como suma ordinaria modulo B^l
  - No hay complicaciones de end-around carry
  - Multiplicacion y division mas simples

VENTAJAS SOBRE CB-1:
  - Una UNICA representacion para 0 (CB-1 tiene dos)
  - No requiere end-around carry
  - Suma y resta identicas a aritmetica ordinaria
  - Multiplicacion correcta sin truncaje especial

RANGO:
  - [-B^(l-1), B^(l-1) - 1]
  - Utiliza TODA la capacidad B^l

EFICACIA:
  - 100% (se usan todas las B^l combinaciones)
  - En contraste: M&S = 1 - (1/2^l), CB-1 = (2/B) - (1/B^l)

RAZON DE USO:
  CB es la representacion universal para numeros enteros con signo en:
  - Computadores (todos los procesadores)
  - Lenguajes de programacion (int, long, etc.)
  - Estandares (IEEE, ISO, POSIX)
  - Aritmetica modular en criptografia
    """)


def main():
    """Ejecutar todas las demostraciones"""
    demo_1_operacion_basica()
    demo_2_representacion_cb()
    demo_3_tablas_cb()
    demo_4_suma_cb()
    demo_5_resta_cb()
    demo_6_multiplicacion_cb()
    demo_7_rango_y_capacidad()
    demo_8_conversiones()
    demo_9_explicaciones_paso_a_paso()
    conclusiones()
    
    print("\n" + "=" * 80)
    print("FIN DE DEMOSTRACIONES")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
