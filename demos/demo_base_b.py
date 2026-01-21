"""
Demostración de conversión de Base 10 a Base B (2-36)

Muestra cómo convertir números decimales a diferentes bases numéricas
usando el método de divisiones sucesivas.
"""

from core.numeracion_utils import (
    decimal_a_base_b_divisiones,
    decimal_a_base_b_con_pasos,
    decimal_a_base_b_verbose,
    validar_base,
    obtener_digitos_para_base
)


def separador(titulo=""):
    """Imprime un separador visual."""
    print("\n" + "=" * 70)
    if titulo:
        print(f"  {titulo}")
        print("=" * 70)
    print()


def demo_bases_basicas():
    """Demuestra conversiones a las bases más comunes."""
    separador("DEMO 1: Conversiones a Bases Comunes")
    
    numero = 173
    print(f"Número decimal: {numero}\n")
    
    bases = [2, 8, 10, 16]
    nombres = ["Binario", "Octal", "Decimal", "Hexadecimal"]
    
    for base, nombre in zip(bases, nombres):
        resultado = decimal_a_base_b_divisiones(numero, base)
        print(f"  {nombre:12} (Base {base:2}): {resultado}")


def demo_base_36():
    """Demuestra uso de base 36 (alfanumérica)."""
    separador("DEMO 2: Base 36 (Alfanumérica - El Máximo)")
    
    numeros = [100, 255, 1000, 1295]
    
    print("Ejemplos de conversión a Base 36:\n")
    for num in numeros:
        resultado = decimal_a_base_b_divisiones(num, 36)
        print(f"  {num:4} en base 36: {resultado}")
    
    print("\nNota: Base 36 usa dígitos 0-9 y letras A-Z")
    print("Máximo valor representable con 2 caracteres: ZZ₃₆ = 1295₁₀")


def demo_con_pasos():
    """Demuestra conversión con pasos intermedios."""
    separador("DEMO 3: Conversión con Pasos Intermedios")
    
    numero = 100
    base = 16
    
    print(f"Convertir {numero} a base {base} (Hexadecimal):\n")
    
    resultado = decimal_a_base_b_con_pasos(numero, base)
    
    print(resultado['explicacion'])


def demo_verbose():
    """Demuestra formato verboso completo."""
    separador("DEMO 4: Explicación Verbosa")
    
    numero = 42
    base = 2
    
    print(decimal_a_base_b_verbose(numero, base))


def demo_tabla_conversion_multiples_bases():
    """Demuestra una tabla con el mismo número en múltiples bases."""
    separador("DEMO 5: Tabla de Conversión - Un Número en Múltiples Bases")
    
    numero = 255
    print(f"Conversión del número {numero} a diferentes bases:\n")
    
    # Encabezado
    print("Base | Resultado | Dígitos Máx")
    print("-" * 45)
    
    for base in [2, 8, 10, 16, 20, 32, 36]:
        resultado = decimal_a_base_b_divisiones(numero, base)
        digitos_tabla = obtener_digitos_para_base(base)
        print(f"{base:4} | {resultado:15} | {digitos_tabla}")


def demo_tabla_conversion_rango():
    """Demuestra una tabla de conversión para un rango de números."""
    separador("DEMO 6: Tabla de Conversión - Rango 0-20 en Bases 2,8,16,36")
    
    print("Dec | Binario  | Octal  | Hex | Base36")
    print("-" * 50)
    
    for num in range(21):
        bin_val = decimal_a_base_b_divisiones(num, 2).replace("₂", "")
        oct_val = decimal_a_base_b_divisiones(num, 8).replace("₈", "")
        hex_val = decimal_a_base_b_divisiones(num, 16).replace("₁₆", "")
        b36_val = decimal_a_base_b_divisiones(num, 36).replace("₃₆", "")
        
        print(f"{num:3} | {bin_val:>8} | {oct_val:>6} | {hex_val:>3} | {b36_val:>6}")


def demo_validacion_bases():
    """Demuestra validación de bases."""
    separador("DEMO 7: Validación de Bases")
    
    bases_test = [1, 2, 8, 16, 36, 37, -5, 0]
    
    print("Validando bases:\n")
    for base in bases_test:
        es_valida = validar_base(base)
        estado = "✓ VÁLIDA" if es_valida else "✗ INVÁLIDA"
        print(f"  Base {base:2}: {estado}")


def demo_bases_intermedias():
    """Demuestra conversiones a bases menos comunes."""
    separador("DEMO 8: Bases Intermedias (5, 7, 12, 20, 27)")
    
    numero = 1000
    bases_especiales = [5, 7, 12, 20, 27]
    
    print(f"Convertir {numero} a diferentes bases:\n")
    
    for base in bases_especiales:
        resultado = decimal_a_base_b_divisiones(numero, base)
        nombre_base = {
            5: "Quinary (Base 5)",
            7: "Septenary (Base 7)",
            12: "Duodecimal (Base 12)",
            20: "Vigesimal (Base 20)",
            27: "Custom (Base 27)"
        }
        print(f"  {nombre_base[base]:25}: {resultado}")


def demo_padding():
    """Demuestra conversión con padding."""
    separador("DEMO 9: Conversión con Padding")
    
    numero = 42
    
    print(f"Número: {numero}\n")
    
    print("Sin padding:")
    print(f"  Binario:     {decimal_a_base_b_divisiones(numero, 2)}")
    print(f"  Hexadecimal: {decimal_a_base_b_divisiones(numero, 16)}")
    
    print("\nCon padding (8 dígitos):")
    print(f"  Binario:     {decimal_a_base_b_divisiones(numero, 2, bits=8)}")
    print(f"  Hexadecimal: {decimal_a_base_b_divisiones(numero, 16, bits=8)}")


def demo_caso_cero():
    """Demuestra manejo del caso especial: cero."""
    separador("DEMO 10: Caso Especial - El Número Cero")
    
    print("Conversión del número 0 a diferentes bases:\n")
    
    for base in [2, 8, 16, 36]:
        resultado = decimal_a_base_b_divisiones(0, base)
        print(f"  Base {base:2}: {resultado}")


if __name__ == "__main__":
    print("\n")
    print("█" * 70)
    print("█  DEMOSTRACIÓN: CONVERSIÓN DE BASE 10 A BASE B (2-36)")
    print("█" * 70)
    
    demo_bases_basicas()
    demo_base_36()
    demo_con_pasos()
    demo_verbose()
    demo_tabla_conversion_multiples_bases()
    demo_tabla_conversion_rango()
    demo_validacion_bases()
    demo_bases_intermedias()
    demo_padding()
    demo_caso_cero()
    
    print("\n" + "=" * 70)
    print("  FIN DE LAS DEMOSTRACIONES")
    print("=" * 70 + "\n")
