"""
Demo: Sistemas de Numeracion Posicionales vs No Posicionales

Este script muestra ejemplos concretos de:
1. Números romanos (no posicional)
2. Base 5 (posicional con potencias)
3. Tiempo (posicional con bases variables)
4. La unicidad de representacion en cada sistema
"""

from core.sistemas_numeracion_basicos import (
    decimal_a_romano, romano_a_decimal, explicar_romano,
    decimal_a_base_5, base_5_a_decimal, explicar_base_5,
    decimal_a_tiempo, tiempo_a_decimal, explicar_tiempo,
    comparar_sistemas, demostrar_unicidad
)


def demo_romanos():
    """Demostracion del sistema romano (No Posicional)."""
    print("\n" + "=" * 80)
    print("DEMO 1: Números Romanos (Sistema NO POSICIONAL)")
    print("=" * 80)
    print("""
?Posicional?  NO - El valor de cada simbolo NO depende de su posicion
Base única?   NO - No es una base única, sino simbolos con valores fijos
Historico?    SÍ - Usado en el Imperio Romano (siglo I a.C. - siglo VIII d.C.)

Caracteristica principal: Cada simbolo tiene el MISMO valor sin importar donde este.
I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000
""")
    
    números = [4, 9, 27, 49, 99, 444, 1994]
    
    print("Ejemplos de conversion decimal -> romano:")
    print("-" * 80)
    
    for num in números:
        romano = decimal_a_romano(num)
        print(f"  {num:4d}_1_0 = {romano:>10s} (inverso: {romano_a_decimal(romano)}_1_0)")
    
    print("\nDesglose detallado de 1994:")
    print("-" * 80)
    explicacion = explicar_romano(1994)
    for d in explicacion['desglose']:
        print(f"  {d['representacion']:4s} = {d['cantidad']}* {d['simbolo']} = {d['resta']}")
    print(f"\n  Total: {explicacion['romano']} = {sum(d['resta'] for d in explicacion['desglose'])}")


def demo_base_5():
    """Demostracion del sistema base 5 (Posicional con Potencias)."""
    print("\n" + "=" * 80)
    print("DEMO 2: Sistema Base 5 (POSICIONAL - Potencias de una Base)")
    print("=" * 80)
    print("""
?Posicional?  SÍ - El valor de cada digito DEPENDE de su posicion
Base única?   SÍ - Base 5 (digitos: 0, 1, 2, 3, 4)
Historico?    Menos común, pero conceptualmente similar a Babilonia (base 60)

Pesos de cada posicion: 5^0=1, 5^1=5, 5^2=25, 5^3=125, 5^4=625
""")
    
    números = [4, 9, 27, 49, 99, 125, 1994]
    
    print("Ejemplos de conversion decimal -> base 5:")
    print("-" * 80)
    
    for num in números:
        base5 = decimal_a_base_5(num)
        inverso = base_5_a_decimal(base5)
        print(f"  {num:4d}_1_0 = {base5:>10s}_5 (inverso: {inverso}_1_0)")
    
    print("\nDesglose detallado de 1994 (el mismo número):")
    print("-" * 80)
    explicacion = explicar_base_5(1994)
    print(f"  Numero en base 5: {explicacion['base_5']}")
    print(f"\n  Posicion | Digito | Potencia | Calculo  | Valor")
    print(f"  --------- -------- ---------- ---------- --------")
    for p in explicacion['potencias']:
        print(f"     {p['posicion']}    |   {p['digito']}    |  5^{p['posicion']}    | {p['calculo']:>8s} | {p['valor']:>4d}")
    print(f"\n  Suma: {' + '.join(str(p['valor']) for p in explicacion['potencias'])} = {explicacion['suma_final']}")


def demo_tiempo():
    """Demostracion del sistema de tiempo (Posicional con Bases Variables)."""
    print("\n" + "=" * 80)
    print("DEMO 3: Sistema de Tiempo (POSICIONAL - Bases VARIABLES)")
    print("=" * 80)
    print("""
?Posicional?   SÍ - El valor de cada número DEPENDE de su posicion
Base única?    NO - Bases variables: 24 (horas), 60 (minutos), 60 (segundos)
Historico?     SÍ - Babilonios usaban base 60 en astronomia

Pesos de cada posicion: horas*3600, minutos*60, segundos*1
Ejemplo historico: Los babilonios dividian el dia en partes basadas en 60.
""")
    
    segundos_totales = [
        4,          # 0:00:04
        49,         # 0:00:49
        99,         # 0:01:39
        3661,       # 1:01:01
        86400,      # 24:00:00 (un dia)
        90061,      # 25:01:01 (mas de un dia)
    ]
    
    print("Ejemplos de conversion segundos -> HH:MM:SS:")
    print("-" * 80)
    
    for seg in segundos_totales:
        tiempo = decimal_a_tiempo(seg)
        inverso = tiempo_a_decimal(tiempo)
        print(f"  {seg:6d}s = {tiempo} (inverso: {inverso}s)")
    
    print("\nDesglose detallado de 3661 segundos:")
    print("-" * 80)
    explicacion = explicar_tiempo(3661)
    print(f"  Tiempo: {explicacion['tiempo']}")
    print(f"\n  Posicion | Valor | Base | Calculo")
    print(f"  --------- ------- ------ ------------------")
    print(f"   Horas   |   1   |  24  |  3661 / 3600 = 1")
    print(f"  Minutos  |   1   |  60  |  (3661 % 3600) / 60 = 1")
    print(f"  Segundos |   1   |  60  |  3661 % 60 = 1")
    print(f"\n  Calculo inverso: {explicacion['calculo']}")


def demo_comparacion():
    """Comparacion del mismo número en diferentes sistemas."""
    print("\n" + "=" * 80)
    print("DEMO 4: El Número 27 en Diferentes Sistemas")
    print("=" * 80)
    
    comparacion = comparar_sistemas(27)
    
    print(f"\nNúmero original: {comparacion['número_decimal']}_1_0\n")
    
    for sistema, datos in comparacion['sistemas'].items():
        print(f"{sistema.upper():12s}: {datos['representacion']:>15s}")
        print(f"  Tipo: {datos['tipo']}")
        print(f"  {datos['descripcion']}\n")
    
    print(f"\n?Notas la diferencia?")
    print(f"  • El número romano usa SÍMBOLOS con valores fijos")
    print(f"  • Base 5 y 10 usan POSICIONES con pesos diferentes")


def demo_unicidad():
    """Demostracion de la unicidad de representacion."""
    print("\n" + "=" * 80)
    print("DEMO 5: UNICIDAD DE REPRESENTACIÓN")
    print("=" * 80)
    print("""
Propiedad fundamental: En cada sistema, existe UNA ÚNICA representacion
para cada número natural.

Esto significa:
  • Si se el número decimal, se exactamente que es en romano, base 5, etc.
  • No hay ambigüedad: 1994_1_0 = MCMXCIV = 30434_5 (siempre)
  • La conversion inversa siempre funciona y es única
""")
    
    unicidad = demostrar_unicidad()
    
    print("Ejemplos verificados:")
    print("-" * 80)
    print(f"{'Decimal':<10} {'Romano':<15} {'Base 5':<15} {'Verificacion':<20}")
    print("-" * 80)
    
    for ejemplo in unicidad['ejemplos']:
        verif = "✓" if (ejemplo['verificacion']['romano_inverso'] and 
                        ejemplo['verificacion']['base_5_inverso']) else "✗"
        print(f"{ejemplo['número']:<10} {ejemplo['romano']:<15} {ejemplo['base_5']:<15} {verif:<20}")
    
    print(f"\nConclusion: Todas las conversiones son REVERSIBLES y ÚNICAS")


def demo_comparacion_notacion():
    """Muestra por que los sistemas posicionales son mejores."""
    print("\n" + "=" * 80)
    print("COMPARACIÓN: Notacion Romana vs Sistemas Posicionales")
    print("=" * 80)
    
    print("""
Ventajas del sistema ROMANO (No Posicional):
  + Simbolos reconocibles y elegantes
  + Facil de entender (cada simbolo tiene un valor)
  - Dificil de escribir números grandes (MMMMMMMMM = 9000000)
  - Muy dificil para operaciones aritmeticas (?cuanto es MCMXCIV * XLII?)
  - No hay representacion eficiente para números muy grandes

Ventajas de sistemas POSICIONALES (como Base 10, Base 5):
  + Números grandes se escriben de forma compacta (9000000 = 9*10^6)
  + Operaciones aritmeticas son sistematicas (algoritmos claros)
  + Facil de calcular con maquinas (solo 0 y 1 en binario)
  + Matematicamente elegante y eficiente
  - Requiere dominar el concepto de "valor posicional"

Ventajas de sistemas MIXTOS (como el tiempo):
  + Reflejan nuestra realidad (24 horas, 60 minutos, 60 segundos)
  + Historicamente establecidos
  - No son uniformes (diferentes bases en cada posicion)
""")
    
    ejemplos = [
        (99, "Número moderadamente grande"),
        (1994, "Año reciente"),
        (999999, "Número grande")
    ]
    
    print("\nComparacion de notaciones:")
    print("-" * 80)
    
    for num, desc in ejemplos:
        rom = decimal_a_romano(num) if num <= 3999 else "IIII (limite romano)"
        b5 = decimal_a_base_5(num)
        b10 = str(num)
        
        print(f"\n{desc}: {num}")
        print(f"  Decimal (Base 10): {b10:15s} (cifras: {len(b10)})")
        print(f"  Base 5:           {b5:15s} (cifras: {len(b5)})")
        if num <= 3999:
            print(f"  Romano:           {rom:15s} (simbolos: {len(rom)})")
        else:
            print(f"  Romano:           ['imposible de escribir eficientemente']")


if __name__ == "__main__":
    demo_romanos()
    demo_base_5()
    demo_tiempo()
    demo_comparacion()
    demo_unicidad()
    demo_comparacion_notacion()
    
    print("\n" + "=" * 80)
    print("FIN DE LAS DEMOSTRACIONES")
    print("=" * 80)
    print("\nResumen:")
    print("  ✓ Sistemas NO posicionales: Números romanos")
    print("  ✓ Sistemas posicionales con base única: Base 5, Base 10, Base 2")
    print("  ✓ Sistemas posicionales con bases variables: Tiempo (HH:MM:SS)")
    print("  ✓ Cada sistema tiene representacion ÚNICA para cada número")
    print("=" * 80 + "\n")
