#!/usr/bin/env python3
"""
Demostracion de Complemento a la Base Menos 1 (CB-1)
Seccion 2.1.1.7.2

Ejemplos de la operacion opCBm1 y representacion ReprCBm1
"""

from core.enteros_signados import (
    opCBm1_digito,
    opCBm1_palabra,
    repr_CBm1,
    CBm1_a_decimal,
    ms_a_CBm1,
    CBm1_a_ms,
    suma_CBm1,
    analizar_representacion_CBm1,
    generar_tabla_CBm1,
    explicar_operacion_CBm1,
)


def demo_1_operacion_basica():
    """Demo 1: Operacion opCBm1 sobre digitos y palabras"""
    print("\n" + "=" * 80)
    print("DEMO 1: OPERACION opCBm1 BASICA")
    print("=" * 80)
    
    print("\n1a. Complemento de digitos individuales (Base 10):")
    digitos_base10 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for d in digitos_base10:
        comp = opCBm1_digito(d, 10)
        print(f"  opCBm1({d}) = {comp}   (9 - {d} = {comp})")
    
    print("\n1b. Complemento de digitos (Base 2):")
    for b in ['0', '1']:
        comp = opCBm1_digito(b, 2)
        print(f"  opCBm1({b}) = {comp}   (1 - {b} = {comp})")
    
    print("\n1c. Complemento de palabra completa (Base 10):")
    palabra = "01239"
    comp = opCBm1_palabra(palabra, 10)
    print(f"  Palabra original: {palabra}")
    print(f"  Complemento:     {comp}")
    print(f"  Calculo: 9-0=9, 9-1=8, 9-2=7, 9-3=6, 9-9=0")
    
    print("\n1d. Propiedad involutiva (aplicar dos veces = identidad):")
    comp1 = opCBm1_palabra(palabra, 10)
    comp2 = opCBm1_palabra(comp1, 10)
    print(f"  Original:     {palabra}")
    print(f"  Complemento:  {comp1}")
    print(f"  Doble compl:  {comp2}")
    print(f"  [OK] opCBm1(opCBm1({palabra})) = {comp2}")


def demo_2_representacion_CBm1():
    """Demo 2: Representacion en CB-1 de numeros positivos y negativos"""
    print("\n" + "=" * 80)
    print("DEMO 2: REPRESENTACION EN CB-1")
    print("=" * 80)
    
    print("\nRepresentacion en CB-1 (Base 10, 5 digitos):")
    numeros = [1239, -1239, 99999, -99999, 0, -0]
    for num in numeros:
        cb1 = repr_CBm1(num, 10, 5)
        valor = CBm1_a_decimal(cb1, 10)
        print(f"  {num:6d} -> CB-1: {cb1} -> Decimal: {valor}")
    
    print("\nRepresentacion en CB-1 (Base 2, 8 bits):")
    numeros_bin = [5, -5, 127, -127, 0, -0]
    for num in numeros_bin:
        cb1 = repr_CBm1(num, 2, 8)
        valor = CBm1_a_decimal(cb1, 2)
        print(f"  {num:4d} -> CB-1: {cb1} -> Decimal: {valor}")


def demo_3_tabla_valores():
    """Demo 3: Tabla de todos los valores representables"""
    print("\n" + "=" * 80)
    print("DEMO 3: TABLA DE VALORES CB-1")
    print("=" * 80)
    
    print("\nTabla CB-1 en Base 2 (4 bits):")
    tabla = generar_tabla_CBm1(2, 4)
    print(tabla[:1000])  # Primeros 1000 caracteres (para no saturar)
    
    print("\n\nTabla CB-1 en Base 10 (2 digitos):")
    tabla10 = generar_tabla_CBm1(10, 2)
    print(tabla10)


def demo_4_sumas_modulares():
    """Demo 4: Ejemplos del texto original - Sumas modulares"""
    print("\n" + "=" * 80)
    print("DEMO 4: SUMAS MODULARES (Del texto original)")
    print("=" * 80)
    
    print("\nEjemplos en Base 10, 5 digitos (M = 99999 = B^l - 1):")
    
    # Ejemplo del texto: A=01239, B=03591
    A = 1239
    B = 3591
    
    print(f"\n  A = {A:05d}")
    print(f"  B = {B:05d}")
    
    # Convertir a CB-1
    cb1_A = repr_CBm1(A, 10, 5)
    cb1_B = repr_CBm1(B, 10, 5)
    cb1_notA = opCBm1_palabra(cb1_A, 10)
    cb1_notB = opCBm1_palabra(cb1_B, 10)
    
    print(f"\n  ~A = {cb1_notA}")
    print(f"  ~B = {cb1_notB}")
    
    print(f"\nOperacion: A + B")
    resultado = suma_CBm1(cb1_A, cb1_B, 10)
    print(f"  {cb1_A} + {cb1_B} = {resultado['resultado']}")
    print(f"  Resultado decimal: {resultado['valor_decimal']} (correcto: {A+B})")
    
    print(f"\nOperacion: A + (~B)  [formula: A + ~C = A - C - 1 (mod B^l)]")
    resultado = suma_CBm1(cb1_A, cb1_notB, 10)
    print(f"  {cb1_A} + {cb1_notB} = {resultado['resultado']}")
    print(f"  Resultado decimal: {resultado['valor_decimal']} (correcto: {A-B-1})")
    if resultado['carry']:
        print(f"  (Sin carry final)")
    
    print(f"\nOperacion: (~A) + B  [formula: ~A + C = -A + C (mod B^l)]")
    resultado = suma_CBm1(cb1_notA, cb1_B, 10)
    print(f"  {cb1_notA} + {cb1_B} = {resultado['resultado']}")
    print(f"  Resultado decimal: {resultado['valor_decimal']} (correcto: {-A+B})")
    if resultado['carry']:
        print(f"  (Con end-around carry)")
    
    print(f"\nOperacion: (~A) + (~B)  [formula: ~A + ~B = -A - B - 2 (mod B^l), con carry: -A - B - 1]")
    resultado = suma_CBm1(cb1_notA, cb1_notB, 10)
    print(f"  {cb1_notA} + {cb1_notB} = {resultado['resultado']}")
    print(f"  Resultado decimal: {resultado['valor_decimal']} (correcto: {-A-B-1})")
    if resultado['carry']:
        print(f"  (Con end-around carry)")


def demo_5_dos_ceros():
    """Demo 5: Problema del cero doble en CB-1"""
    print("\n" + "=" * 80)
    print("DEMO 5: PROBLEMA DEL CERO DOBLE")
    print("=" * 80)
    
    print("\nEn CB-1 (Base 10, 2 digitos):")
    cb1_zero_pos = "00"
    cb1_zero_neg = "99"
    
    print(f"  +0 se representa como: {cb1_zero_pos}")
    print(f"     Valor decimal: {CBm1_a_decimal(cb1_zero_pos, 10)}")
    
    print(f"\n  -0 se representa como: {cb1_zero_neg}")
    print(f"     Valor decimal: {CBm1_a_decimal(cb1_zero_neg, 10)}")
    
    print(f"\n  Ambas representan el numero 0, pero son diferentes!")
    print(f"  Esto desperdicia una combinacion de los 100 valores posibles.")
    
    print("\nEn CB-1 (Base 2, 8 bits):")
    cb1_zero_pos_bin = "00000000"
    cb1_zero_neg_bin = "11111111"
    
    print(f"  +0 se representa como: {cb1_zero_pos_bin}")
    print(f"  -0 se representa como: {cb1_zero_neg_bin}")
    print(f"  Ambas representan 0, pero son diferentes en 256 valores posibles.")


def demo_6_rango_y_capacidad():
    """Demo 6: Rango y capacidad en diferentes bases y longitudes"""
    print("\n" + "=" * 80)
    print("DEMO 6: RANGO Y CAPACIDAD")
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
        info = analizar_representacion_CBm1(base, longitud)
        print(f"\nCB-1 (Base {base}, {longitud} digitos):")
        print(f"  Rango: [{info['min_negativo']:6d}, {info['max_positivo']:6d}]")
        print(f"  Capacidad: {info['capacidad']} valores")
        print(f"  Total posible: {info['total_posible']} combinaciones")
        print(f"  Eficacia: {info['porcentaje_eficacia']}")
        print(f"  Formula: {info['formula_eficacia']}")


def demo_7_explicaciones():
    """Demo 7: Explicaciones paso a paso"""
    print("\n" + "=" * 80)
    print("DEMO 7: EXPLICACIONES PASO A PASO")
    print("=" * 80)
    
    print("\n--- Complemento de un numero ---")
    explicacion = explicar_operacion_CBm1(42, 0, 'complemento', base=10, longitud=2)
    print(explicacion)
    
    print("\n--- Suma de dos numeros positivos ---")
    explicacion = explicar_operacion_CBm1(5, 3, 'suma', base=10, longitud=2)
    print(explicacion)
    
    print("\n--- Suma de numero positivo y negativo ---")
    explicacion = explicar_operacion_CBm1(5, -3, 'suma', base=10, longitud=2)
    print(explicacion)


def main():
    print("\n" + "=" * 80)
    print("DEMOSTRACION: COMPLEMENTO A LA BASE MENOS 1 (CB-1)")
    print("Seccion 2.1.1.7.2: Numeros Enteros con Signo")
    print("=" * 80)
    
    demo_1_operacion_basica()
    demo_2_representacion_CBm1()
    demo_3_tabla_valores()
    demo_4_sumas_modulares()
    demo_5_dos_ceros()
    demo_6_rango_y_capacidad()
    demo_7_explicaciones()
    
    print("\n" + "=" * 80)
    print("CONCLUSIONES")
    print("=" * 80)
    print("""
CB-1 es elegante teoricamente:
  - opCBm1 es una operacion simple (dígito a digito)
  - En binario, opCBm1 = NOT (invertir cada bit)
  - Rango igual a M&S

Pero tiene defectos practicos:
  - DOS CEROS: desperdicia una combinacion
  - END-AROUND CARRY: suma mas compleja
  - EFICACIA BAJA en bases grandes
  
Por eso los sistemas modernos prefieren COMPLEMENTO A 2 (C2).
""")


if __name__ == '__main__':
    main()
