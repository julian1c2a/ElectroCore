"""
Demostración: Conversión de Base B a Base 10
Con Polinomio, Método de Horner y Comparación

Muestra cómo convertir números de cualquier base a decimal,
usando dos métodos diferentes para enseñar eficiencia algorítmica.
"""

from core.numeracion_utils import (
    base_b_a_decimal_simple,
    base_b_a_decimal_con_polinomio,
    base_b_a_decimal_con_horner,
    comparar_metodos_conversion,
    validar_numero_en_base
)


def separador(titulo=""):
    """Imprime un separador visual."""
    print("\n" + "=" * 80)
    if titulo:
        print(f"  {titulo}")
        print("=" * 80)
    print()


def demo_conversion_simple():
    """Demostración: Conversión simple de múltiples bases a decimal."""
    separador("DEMO 1: Conversión Simple (Resultado Directo)")
    
    ejemplos = [
        ("1101", 2),
        ("377", 8),
        ("FF", 16),
        ("4T", 36),
        ("110110", 2),
        ("255", 10),
        ("1A2B", 16),
    ]
    
    print("Conversiones rápidas (sin detalles):\n")
    
    for numero_str, base in ejemplos:
        try:
            decimal = base_b_a_decimal_simple(numero_str, base)
            print(f"  {numero_str:>8} (Base {base:2}) = {decimal:6}")
        except ValueError as e:
            print(f"  {numero_str:>8} (Base {base:2}) = ERROR: {e}")


def demo_polinomio():
    """Demostración: Método polinomio (forma estándar)."""
    separador("DEMO 2: Método del Polinomio (Forma Estándar)")
    
    ejemplos = [
        ("1101", 2, "Binario"),
        ("377", 8, "Octal"),
        ("FF", 16, "Hexadecimal"),
    ]
    
    for numero_str, base, nombre in ejemplos:
        print(f"\n{nombre}: {numero_str} (Base {base})")
        print("-" * 80)
        
        resultado = base_b_a_decimal_con_polinomio(numero_str, base)
        
        print(f"Polinomio: {resultado['polinomio_str']}\n")
        print("Cálculos:")
        for calc in resultado['calculos']:
            print(f"  {calc}")
        
        print(f"\nResultado: {resultado['decimal']}")


def demo_horner():
    """Demostración: Método de Horner (más eficiente)."""
    separador("DEMO 3: Método de Horner (Más Eficiente)")
    
    ejemplos = [
        ("1101", 2, "Binario"),
        ("377", 8, "Octal"),
        ("FF", 16, "Hexadecimal"),
    ]
    
    for numero_str, base, nombre in ejemplos:
        print(f"\n{nombre}: {numero_str} (Base {base})")
        print("-" * 80)
        
        resultado = base_b_a_decimal_con_horner(numero_str, base)
        
        print(f"Forma de Horner: {resultado['forma_horner']}\n")
        print("Pasos del algoritmo (resultado = resultado × base + dígito):\n")
        
        for paso in resultado['pasos_horner']:
            print(f"Paso {paso['paso']}: Dígito '{paso['digito']}' (valor {paso['valor_digito']})")
            print(f"         {paso['resultado_anterior']} × {paso['base']} + {paso['valor_digito']} = {paso['resultado_actual']}")
        
        print(f"\nResultado: {resultado['decimal']}")


def demo_comparacion():
    """Demostración: Comparación de métodos."""
    separador("DEMO 4: Comparación Polinomio vs Horner")
    
    ejemplos = [
        ("1101", 2),
        ("10101010", 2),
        ("ABCDEF", 16),
        ("12345", 8),
    ]
    
    for numero_str, base in ejemplos:
        print(f"\nNúmero: {numero_str} (Base {base})")
        print("-" * 80)
        
        resultado = comparar_metodos_conversion(numero_str, base)
        print(resultado['explicacion'])


def demo_tabla_conversion_multiple():
    """Demostración: Tabla de conversión desde múltiples bases."""
    separador("DEMO 5: Tabla de Conversión - Mismo Número desde Diferentes Bases")
    
    print("Número '100' convertido desde diferentes bases:\n")
    print(f"{'Base':<6} | {'Número':<10} | {'Decimal':<10} | {'Verificación'}")
    print("-" * 65)
    
    for base in [2, 3, 5, 8, 10, 16, 20, 36]:
        numero_str = "100"
        try:
            decimal = base_b_a_decimal_simple(numero_str, base)
            verificacion = f"{base}² = {base**2}"
            print(f"{base:<6} | {numero_str:<10} | {decimal:<10} | {verificacion}")
        except ValueError:
            print(f"{base:<6} | {numero_str:<10} | ERROR    |")


def demo_binario_educativo():
    """Demostración educativa: Convertir número binario con ambos métodos."""
    separador("DEMO 6: Educativo - Convertir 10110 desde Binario (Todo Detallado)")
    
    numero = "10110"
    base = 2
    
    print(f"Convertir {numero}₂ a decimal\n")
    
    # Método 1: Polinomio
    print("MÉTODO 1: POLINOMIO (Forma Estándar)")
    print("─" * 80)
    resultado_poli = base_b_a_decimal_con_polinomio(numero, base)
    print(f"\nPolinomio:")
    print(f"  {resultado_poli['polinomio_str']}\n")
    print("Cálculos:")
    for i, calc in enumerate(resultado_poli['calculos'], 1):
        print(f"  {i}. {calc}")
    print(f"\nPaso final: Suma de todos los términos = {resultado_poli['decimal']}")
    
    # Método 2: Horner
    print("\n" + "=" * 80)
    print("MÉTODO 2: HORNER (Más Eficiente)")
    print("─" * 80)
    resultado_horner = base_b_a_decimal_con_horner(numero, base)
    print(f"\nForma de Horner:")
    print(f"  {resultado_horner['forma_horner']}\n")
    print("Evaluación paso a paso:\n")
    
    for paso in resultado_horner['pasos_horner']:
        print(f"Paso {paso['paso']}: {paso['digito']}")
        if paso['paso'] == 1:
            print(f"       = {paso['valor_digito']}")
        else:
            print(f"       Anterior: {paso['resultado_anterior']}")
            print(f"       {paso['resultado_anterior']} × {paso['base']} = {paso['multiplicacion']}")
            print(f"       {paso['multiplicacion']} + {paso['valor_digito']} = {paso['resultado_actual']}")
    
    print(f"\nRespuesta final: {resultado_horner['decimal']}")


def demo_validacion():
    """Demostración: Validación de entrada."""
    separador("DEMO 7: Validación de Entrada")
    
    pruebas = [
        ("1010", 2, "Binario válido"),
        ("10102", 2, "Binario inválido (contiene 2)"),
        ("FF", 16, "Hexadecimal válido"),
        ("GG", 16, "Hexadecimal inválido (G>F)"),
        ("377", 8, "Octal válido"),
        ("388", 8, "Octal inválido (8>7)"),
        ("1A2B", 36, "Base 36 válido"),
        ("1Z", 35, "Base 35 inválido (Z no existe)"),
    ]
    
    print("Validación de números en diferentes bases:\n")
    
    for numero_str, base, descripcion in pruebas:
        es_valido, msg = validar_numero_en_base(numero_str, base)
        estado = "✓" if es_valido else "✗"
        print(f"{estado} {descripcion:35} → {msg}")


def demo_aplicacion_practica():
    """Demostración: Aplicación práctica real."""
    separador("DEMO 8: Aplicación Práctica - Decodificar Código Hexadecimal")
    
    print("Escenario: Decodificar valores hexadecimales comunes:\n")
    
    valores = {
        "FF": "Máximo de 8 bits",
        "0A": "Salto de línea (LF)",
        "1F": "Separador de unidad",
        "AA": "Patrón de prueba",
        "DEAD": "Código de error (DEADBEEF)",
        "BEEF": "Código de error (DEADBEEF)",
    }
    
    for hex_num, descripcion in valores.items():
        decimal = base_b_a_decimal_simple(hex_num, 16)
        print(f"  {hex_num:>6}₁₆ = {decimal:6} en decimal  ({descripcion})")


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print("  DEMOSTRACIÓN: CONVERSIÓN DE BASE B A DECIMAL")
    print("  Polinomio, Método de Horner y Comparación")
    print("=" * 80)
    
    demo_conversion_simple()
    demo_polinomio()
    demo_horner()
    demo_comparacion()
    demo_tabla_conversion_multiple()
    demo_binario_educativo()
    demo_validacion()
    demo_aplicacion_practica()
    
    print("\n" + "=" * 80)
    print("  FIN DE LAS DEMOSTRACIONES")
    print("=" * 80 + "\n")
