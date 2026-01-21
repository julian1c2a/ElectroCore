"""
================================================================================
DEMOSTRACIÓN COMPLETA: MAGNITUD Y SIGNO (M&S)
================================================================================

Este script demuestra todos los aspectos del sistema de Magnitud y Signo
para representación de números enteros con signo en binario.

Sección: 2.1.1.7.1 - Magnitud y Signo
Tema: Números Enteros con Signo
================================================================================
"""

from core.enteros_signados import (
    # Rango y Capacidad
    rango_ms,
    analizar_ms,
    
    # Conversión
    decimal_a_ms,
    ms_a_decimal,
    explicar_conversion_ms,
    
    # Operaciones
    negacion_ms,
    es_positivo_ms,
    es_negativo_ms,
    es_cero_ms,
    valor_absoluto_ms,
    comparar_ms,
    
    # Análisis
    validar_representacion_ms,
    analizar_representacion_ms,
    
    # Constructores
    crear_cero_positivo_ms,
    crear_cero_negativo_ms,
    generar_tabla_ms,
    mostrar_tabla_ms,
)


def print_titulo(texto, nivel=1):
    """Imprime un título formateado."""
    if nivel == 1:
        print("\n" + "=" * 80)
        print(f"  {texto}")
        print("=" * 80)
    elif nivel == 2:
        print(f"\n{texto}")
        print("-" * len(texto))
    else:
        print(f"\n  → {texto}")


def demo_1_conceptos_basicos():
    """Demo 1: Conceptos básicos de M&S"""
    print_titulo("DEMO 1: CONCEPTOS BASICOS", 2)
    
    print("""
En Magnitud y Signo:
  • Bit n-1 (MSB): Signo (0=positivo, 1=negativo)
  • Bits n-2...0: Magnitud (valor absoluto)
  
Ejemplos en M&S de 8 bits:
    """)
    
    ejemplos = [
        (86, 8, "Número positivo"),
        (-86, 8, "Número negativo"),
        (0, 8, "Cero positivo"),
        (127, 8, "Máximo positivo (M&S8)"),
        (-127, 8, "Mínimo negativo (M&S8)"),
    ]
    
    for decimal, n_bits, descripcion in ejemplos:
        ms = decimal_a_ms(decimal, n_bits)
        print(f"\n  {decimal:6} (dec) → {ms} (M&S{n_bits})  [{descripcion}]")
        
        # Mostrar estructura
        signo = "+" if ms[0] == '0' else "-"
        magnitud = int(ms[1:], 2)
        print(f"           Signo: {signo}  |  Magnitud: {magnitud} (dec), {ms[1:]} (bin)")


def demo_2_rango_y_capacidad():
    """Demo 2: Rango y capacidad para diferentes tamaños"""
    print_titulo("DEMO 2: RANGO Y CAPACIDAD", 2)
    
    print("\nAnálisis para diferentes tamaños:\n")
    
    for n_bits in [4, 8, 16, 32]:
        info = rango_ms(n_bits)
        print(f"M&S{n_bits}:")
        print(f"  Rango negativos:      [{info['min_negativo']:10}, {-1:10}]")
        print(f"  Rango positivos:      [{1:10}, {info['max_positivo']:10}]")
        print(f"  Valores únicos:       {info['capacidad']:10} (2^{n_bits} - 1)")
        print(f"  Eficacia:             {info['porcentaje_eficacia']:10.2f}%")
        print(f"  (Una combinación desperdiciada: +0 y -0)")
        print()


def demo_3_conversiones():
    """Demo 3: Conversiones paso a paso"""
    print_titulo("DEMO 3: CONVERSIONES PASO A PASO", 2)
    
    numeros = [42, -42, 0, 1, -1]
    
    for numero in numeros:
        print()
        print(f"Convertir {numero:4} a M&S8:")
        print("─" * 50)
        
        explicacion = explicar_conversion_ms(numero, 8)
        
        for paso in explicacion['pasos']:
            print(f"  {paso}")


def demo_4_operaciones():
    """Demo 4: Operaciones en M&S"""
    print_titulo("DEMO 4: OPERACIONES EN M&S", 2)
    
    # Negación
    print("\n4.1 NEGACIÓN (Multiplicar por -1)")
    print("─" * 50)
    print("En M&S, negación = flip del bit de signo\n")
    
    test_negacion = ['00101010', '10101010', '00000000', '10000000']
    for ms in test_negacion:
        valor_original = ms_a_decimal(ms)
        negado = negacion_ms(ms)
        valor_negado = ms_a_decimal(negado)
        print(f"  {ms} ({valor_original:4}) → flip bit signo → {negado} ({valor_negado:4})")
    
    # Predicados
    print("\n4.2 CONSULTAS SOBRE VALORES")
    print("─" * 50)
    
    test_valores = ['01010110', '11010110', '00000000', '10000000']
    for ms in test_valores:
        valor = ms_a_decimal(ms)
        es_pos = es_positivo_ms(ms)
        es_neg = es_negativo_ms(ms)
        es_cero = es_cero_ms(ms)
        
        print(f"\n  {ms} = {valor:4}")
        print(f"    Es positivo: {es_pos:5} | Es negativo: {es_neg:5} | Es cero: {es_cero}")
    
    # Comparación
    print("\n4.3 COMPARACION")
    print("─" * 50)
    print("En M&S, la comparación es compleja (invertida para negativos)\n")
    
    pares = [
        ('00101010', '00110010'),  # 42 vs 50
        ('10101010', '10110010'),  # -42 vs -50
        ('00000000', '10000000'),  # +0 vs -0
    ]
    
    for a, b in pares:
        val_a = ms_a_decimal(a)
        val_b = ms_a_decimal(b)
        resultado = comparar_ms(a, b)
        relacion = '<' if resultado < 0 else ('=' if resultado == 0 else '>')
        print(f"  {a} ({val_a:4}) {relacion} {b} ({val_b:4})")


def demo_5_ventajas_desventajas():
    """Demo 5: Resumen de ventajas y desventajas"""
    print_titulo("DEMO 5: VENTAJAS Y DESVENTAJAS", 2)
    
    print("""
VENTAJAS:
  + Intuitivo (como escribimos números a mano)
  + Negacion es simple (solo flip del bit de signo)
  + Facil de entender conceptualmente
  + Multiplicacion/division directa sobre magnitudes

DESVENTAJAS:
  - DOS REPRESENTACIONES PARA CERO (+0 y -0)
    -> Desperdicia una combinacion
    -> Comparacion de igualdad mas compleja
  
  - SUMA Y RESTA COMPLICADAS
    -> Requieren diferentes algoritmos segun signos
    -> Mucho mas lento que Complemento a 2
  
  - COMPARACION INVERTIDA PARA NEGATIVOS
    -> Mas compleja y lenta
    -> Requiere logica especial en hardware
  
  - BAJA EFICIENCIA TEORICA
    -> Capacidad = 2^n - 1 (no 2^n)
    -> Eficacia = 1 - (1/2^n)

CONCLUSION:
  M&S es pedagogicamente util para ENTENDER el concepto,
  pero NO es usado en hardware moderno.
  
  -> Los procesadores usan Complemento a 2 (C2)
  -> C2 resuelve todos estos problemas
    """)
    
    # Mostrar tabla comparativa de los dos ceros
    print("\nEjemplo: Los dos ceros en M&S8")
    print("─" * 50)
    
    cero_positivo = crear_cero_positivo_ms(8)
    cero_negativo = crear_cero_negativo_ms(8)
    
    print(f"\n  Representacion de +0: {cero_positivo}")
    print(f"  Representacion de -0: {cero_negativo}")
    print(f"\n  Ambas se interpretan como: {ms_a_decimal(cero_positivo)}")
    print(f"  iDos combinaciones diferentes para el mismo valor!")


def demo_6_tablas_pequenas():
    """Demo 6: Tablas para valores pequeños"""
    print_titulo("DEMO 6: TABLAS DE VALORES", 2)
    
    print("\nTabla completa M&S4 (rango [-7, 7]):")
    print(mostrar_tabla_ms(4, show_all=True))
    
    print("\n\nTabla de M&S8 (muestra parcial):")
    print(mostrar_tabla_ms(8, show_all=False))


def demo_7_analisis_completo():
    """Demo 7: Análisis completo de una representación"""
    print_titulo("DEMO 7: ANALISIS COMPLETO", 2)
    
    representaciones = ['01010110', '11010110', '00000000']
    
    for rep in representaciones:
        print(f"\nAnalizando: {rep}")
        print("─" * 50)
        
        analisis = analizar_representacion_ms(rep)
        
        if analisis['valido']:
            print(f"  Estructura:")
            print(f"    Bit de signo (índice {analisis['estructura']['indice_signo']}): {analisis['estructura']['bit_signo']}")
            print(f"    Bits de magnitud (índices {analisis['estructura']['indices_magnitud']}): {analisis['estructura']['bits_magnitud']}")
            
            print(f"\n  Interpretación:")
            print(f"    Positivo: {analisis['interpretacion']['es_positivo']}")
            print(f"    Negativo: {analisis['interpretacion']['es_negativo']}")
            print(f"    Es cero: {analisis['interpretacion']['es_cero']}")
            print(f"    Magnitud: {analisis['interpretacion']['magnitud_decimal']}")
            print(f"    Valor decimal: {analisis['interpretacion']['valor_decimal']}")




def main():
    """Ejecuta todas las demostraciones"""
    
    print("""
    
================================================================================
                   DEMOSTRACION: MAGNITUD Y SIGNO (M&S)
                                                                      
  Seccion 2.1.1.7.1: Numeros Enteros con Signo
                                                                      
  Este script demuestra TODOS los aspectos del sistema M&S:
   * Conceptos basicos
   * Rango y capacidad
   * Conversiones paso a paso
   * Operaciones (negacion, comparacion)
   * Ventajas y desventajas
   * Tablas de valores
   * Analisis completo

================================================================================
    """)
    
    # Ejecutar demostraciones
    demo_1_conceptos_basicos()
    demo_2_rango_y_capacidad()
    demo_3_conversiones()
    demo_4_operaciones()
    demo_5_ventajas_desventajas()
    demo_6_tablas_pequenas()
    demo_7_analisis_completo()
    
    # Conclusión
    print_titulo("CONCLUSIÓN", 1)
    print("""
M&S es la forma MAS INTUITIVA de representar números con signo:
  + Conceptualmente clara: signo separado de magnitud
  + Facil de entender para principiantes
  + Base conceptual para otros sistemas

PERO tiene PROBLEMAS PRACTICOS:
  - Dos ceros (desperdicio)
  - Suma/resta complicadas
  - Comparacion invertida para negativos

POR ESO, en HARDWARE MODERNO se usa:
  --> COMPLEMENTO A 2 (C2)
  --> Que resuelve todos estos problemas

La progresion pedagogica es:
  1. M&S (entender concepto) --> 
  2. C1 (transicion) --> 
  3. C2 (moderno)

iProximo: Complemento a 1 (C1)!
    """)


if __name__ == "__main__":
    main()
