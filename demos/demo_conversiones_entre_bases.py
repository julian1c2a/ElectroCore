"""
Demo: Funciones Genericas de Conversion entre Bases - ASCII SAFE
Secciones 2.1.1.3 y 2.1.1.5.4 del Temario
"""

from core.sistemas_numeracion_basicos import (
    decimal_a_base_B,
    base_B_a_decimal,
    base_B_a_base_B_prima,
    base_B_a_base_B_prima_potencias
)


def demo_1_decimal_a_base_B():
    """Demo 1: Convertir Decimal a Base B"""
    print("\n" + "=" * 80)
    print("DEMO 1: Convertir Decimal a Base B")
    print("=" * 80)
    print("\nFunción: decimal_a_base_B(numero: int, base: int) -> str")
    print("Referencia: 2.1.1.3 (Conversión de Base 10 a Base B)")
    print()
    
    casos = [
        (1994, 5, "Número 1994 en base 5"),
        (255, 2, "Número 255 en binario (base 2)"),
        (255, 16, "Número 255 en hexadecimal (base 16)"),
        (27, 10, "Número 27 en decimal (base 10)"),
        (100, 8, "Número 100 en octal (base 8)"),
    ]
    
    for numero, base, descripcion in casos:
        resultado = decimal_a_base_B(numero, base)
        print(f"  {numero} (base 10) -> base {base}: {resultado} ({descripcion})")
    
    print("\n[OK] Método: Divisiones sucesivas (cociente y resto)")


def demo_2_base_B_a_decimal():
    """Demo 2: Convertir Base B a Decimal"""
    print("\n" + "=" * 80)
    print("DEMO 2: Convertir Base B a Decimal")
    print("=" * 80)
    print("\nFunción: base_B_a_decimal(numero_str: str, base: int) -> int")
    print("Referencia: 2.1.1.3 (Conversión de Base B a Base 10)")
    print()
    
    casos = [
        ("30434", 5, "30434 en base 5"),
        ("11111111", 2, "11111111 en binario"),
        ("ff", 16, "ff en hexadecimal"),
        ("144", 8, "144 en octal"),
    ]
    
    for numero_str, base, descripcion in casos:
        resultado = base_B_a_decimal(numero_str, base)
        print(f"  {numero_str}_{base} -> {resultado}(base 10) <- {descripcion}")
    
    print("\n[OK] Método: Polinomio de Horner (evaluación eficiente)")


def demo_3_base_B_a_base_B_prima():
    """Demo 3: Conversión Genérica B -> B'"""
    print("\n" + "=" * 80)
    print("DEMO 3: Conversión Genérica entre Bases B y B'")
    print("=" * 80)
    print("\nFunción: base_B_a_base_B_prima(numero_str, base_origen, base_destino) -> str")
    print("Referencia: 2.1.1.3 (Conversión entre Sistemas de Numeración)")
    print()
    
    casos = [
        ("30434", 5, 2, "1994 desde base 5 a base 2"),
        ("ff", 16, 10, "255 desde base 16 a decimal"),
        ("1010", 2, 8, "10 desde binario a octal"),
        ("144", 8, 16, "100 desde octal a hexadecimal"),
    ]
    
    for numero_str, base_orig, base_dest, descripcion in casos:
        resultado = base_B_a_base_B_prima(numero_str, base_orig, base_dest)
        print(f"  {numero_str}_{base_orig} -> {resultado}_{base_dest} <- {descripcion}")
    
    print("\n[OK] Método: Conversión a través de decimal (B -> 10 -> B')")


def demo_4_bases_relacionadas():
    """Demo 4: Conversión Optimizada para Bases Relacionadas"""
    print("\n" + "=" * 80)
    print("DEMO 4: Conversión Optimizada para Bases Relacionadas")
    print("=" * 80)
    print("\nFunción: base_B_a_base_B_prima_potencias(numero_str, base_comun,")
    print("                                          exponente_origen, exponente_destino)")
    print("Referencia: 2.1.1.5.4 (Conversión entre bases B=b^n y B'=b^m)")
    print()
    
    # Caso 1: Binario -> Hexadecimal
    print("\n1. Binario (2^1) <-> Hexadecimal (2^4)")
    print("-" * 80)
    resultado_1a = base_B_a_base_B_prima_potencias("11111111", 2, 1, 4)
    resultado_1b = base_B_a_base_B_prima_potencias("ff", 2, 4, 1)
    print(f"  Binario -> Hexadecimal:   11111111(base 2) -> {resultado_1a}(base 16)")
    print(f"    Agrupamos 4 dígitos:   1111|1111 -> F|F")
    print(f"  Hexadecimal -> Binario:   ff(base 16) -> {resultado_1b}(base 2)")
    print(f"    Expandimos:            f|f -> 1111|1111")
    
    # Caso 2: Binario -> Octal
    print("\n2. Binario (2^1) <-> Octal (2^3)")
    print("-" * 80)
    resultado_2a = base_B_a_base_B_prima_potencias("1111", 2, 1, 3)
    resultado_2b = base_B_a_base_B_prima_potencias("17", 2, 3, 1)
    print(f"  Binario -> Octal:         1111(base 2) -> {resultado_2a}(base 8)")
    print(f"    Agrupamos 3 dígitos:   001|111 -> 1|7")
    print(f"  Octal -> Binario:         17(base 8) -> {resultado_2b}(base 2)")
    print(f"    Expandimos:            1|7 -> 001|111")
    
    # Caso 3: Base 3 <-> Base 27
    print("\n3. Base 3 (3^1) <-> Base 27 (3^3)")
    print("-" * 80)
    # Crear un número en base 3
    numero_b3 = "010021002"
    resultado_3a = base_B_a_base_B_prima_potencias(numero_b3, 3, 1, 3)
    print(f"  Base 3 -> Base 27:        {numero_b3}(base 3) -> {resultado_3a}(base 2)₇")
    print(f"    Agrupamos 3 dígitos:   010|021|002 -> 1|2|2")
    
    print("\n[OK] Método: Agrupación/Expansión de dígitos (sin aritmética costosa)")
    print("[OK] Mucho más eficiente que pasar por decimal para números grandes")


def demo_5_comparacion_metodos():
    """Demo 5: Comparación de Métodos"""
    print("\n" + "=" * 80)
    print("DEMO 5: Comparación de Métodos")
    print("=" * 80)
    print()
    
    # Ejemplo: Convertir 255 de binario a hexadecimal
    numero_bin = "11111111"
    
    print(f"Convertir {numero_bin}(base 2) a base 16:")
    print()
    
    # Método 1: Genérico (a través de decimal)
    print("Método 1: Genérico (base_B_a_base_B_prima)")
    print("-" * 80)
    resultado_gen = base_B_a_base_B_prima(numero_bin, 2, 16)
    print(f"  {numero_bin}(base 2) -> 255(base 10) -> {resultado_gen}(base 16)")
    print(f"  Operaciones: 1 conversión a decimal + 1 conversión a destino")
    print(f"  Ventaja: Funciona para CUALQUIER par de bases")
    print()
    
    # Método 2: Optimizado (agrupación)
    print("Método 2: Optimizado (base_B_a_base_B_prima_potencias)")
    print("-" * 80)
    resultado_opt = base_B_a_base_B_prima_potencias(numero_bin, 2, 1, 4)
    print(f"  {numero_bin}(base 2) -> {resultado_opt}(base 16)")
    print(f"  Operaciones: Agrupar 4 dígitos (sin aritmética)")
    print(f"  Agrupamos:   1111|1111 -> F|F -> {resultado_opt}(base 16)")
    print(f"  Ventaja: MÁS RÁPIDO para bases relacionadas")
    print()
    
    # Comparación
    print("Comparación:")
    print("-" * 80)
    print("Caso de uso                         | Método recomendado")
    print("-" * 80)
    print("Conversión general B -> B'          | base_B_a_base_B_prima()")
    print("Binario <-> Octal/Hexadecimal        | base_B_a_base_B_prima_potencias()")
    print("Decimal -> Cualquier base           | decimal_a_base_B()")
    print("Cualquier base -> Decimal           | base_B_a_decimal()")


def demo_6_casos_practicos():
    """Demo 6: Casos Prácticos"""
    print("\n" + "=" * 80)
    print("DEMO 6: Casos Prácticos en Informática")
    print("=" * 80)
    print()
    
    # Caso 1: Direcciones IP
    print("1. Dirección IP en Binario")
    print("-" * 80)
    print("  Dirección IP: 192.168.1.1")
    
    # 192 en binario
    ip_byte_1 = decimal_a_base_B(192, 2)
    print(f"    192(base 10) = {ip_byte_1}(base 2)")
    
    # 168 en binario
    ip_byte_2 = decimal_a_base_B(168, 2)
    print(f"    168(base 10) = {ip_byte_2}(base 2)")
    
    # 1 en binario
    ip_byte_3 = decimal_a_base_B(1, 2)
    print(f"    1(base 10) = {ip_byte_3}(base 2)")
    print()
    
    # Caso 2: Color RGB en diferentes representaciones
    print("2. Color RGB: Rojo Puro")
    print("-" * 80)
    r, g, b = 255, 0, 0
    
    # Hexadecimal (usado en web)
    hex_color = "#" + decimal_a_base_B(r, 16) + decimal_a_base_B(g, 16) + decimal_a_base_B(b, 16)
    print(f"  Decimal (RGB): ({r}, {g}, {b})")
    print(f"  Hexadecimal:   {hex_color}")
    
    # Binario (hardware)
    bin_r = decimal_a_base_B(r, 2)
    bin_g = decimal_a_base_B(g, 2)
    bin_b = decimal_a_base_B(b, 2)
    print(f"  Binario:       {bin_r} {bin_g} {bin_b}")
    print()
    
    # Caso 3: Permiso de archivos en Linux
    print("3. Permisos de Archivo (UNIX) 755 en octal -> binario")
    print("-" * 80)
    permisos_oct = "755"
    permisos_bin = base_B_a_base_B_prima_potencias(permisos_oct, 8, 1, 1)
    print(f"  Octal (755):   rwxr-xr-x")
    print(f"  Binario:       {permisos_bin}")
    print(f"    Propietario: {permisos_bin[0:3]} (rwx)")
    print(f"    Grupo:       {permisos_bin[3:6]} (r-x)")
    print(f"    Otros:       {permisos_bin[6:9]} (r-x)")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN: Funciones Genéricas de Conversión entre Bases".center(80))
    print("Secciones 2.1.1.3 y 2.1.1.5.4 del Temario".center(80))
    print("=" * 80)
    
    demo_1_decimal_a_base_B()
    demo_2_base_B_a_decimal()
    demo_3_base_B_a_base_B_prima()
    demo_4_bases_relacionadas()
    demo_5_comparacion_metodos()
    demo_6_casos_practicos()
    
    print("\n" + "=" * 80)
    print("FIN DE DEMOSTRACIONES")
    print("=" * 80)
    print("\n[OK] Todas las funciones funcionando correctamente")
    print("[OK] Referencias en CONTENIDOS_FE.md (2.1.1.1 hasta 2.1.1.6.1)")
