"""
Ejemplo de uso práctico: Conversión de Base 10 a Base B

Muestra los 3 niveles de complejidad de la API generalizada.
"""

from core.numeracion_utils import (
    decimal_a_base_b_divisiones,
    decimal_a_base_b_con_pasos,
    decimal_a_base_b_verbose
)


def main():
    print("\n" + "=" * 70)
    print("  CONVERSIÓN DE BASE 10 A BASE B - NIVELES DE USO")
    print("=" * 70 + "\n")
    
    # Caso de uso: Convertir el número 173 a diferentes bases
    numero = 173
    
    # ========================================================================
    # NIVEL 1: RESULTADO SIMPLE
    # ========================================================================
    print("[NIVEL 1] - Resultado Simple (Solo el resultado)")
    print("-" * 70)
    print(f"Número a convertir: {numero}\n")
    
    bases_ejemplos = [2, 8, 16, 20, 36]
    print("Conversiones rápidas:")
    
    for base in bases_ejemplos:
        resultado = decimal_a_base_b_divisiones(numero, base)
        print(f"  {numero} en base {base:2} = {resultado}")
    
    # ========================================================================
    # NIVEL 2: CON TABLA DE DIVISIONES (Datos intermedios)
    # ========================================================================
    print("\n" + "=" * 70)
    print("[NIVEL 2] - Con Tabla de Divisiones (Para ejercicios)")
    print("-" * 70)
    
    numero_nivel2 = 173
    base_nivel2 = 16
    
    resultado = decimal_a_base_b_con_pasos(numero_nivel2, base_nivel2)
    
    print(f"\nConvertir {numero_nivel2} a base {base_nivel2} (Hexadecimal):\n")
    print(f"{'Dividendo':<10} | {'Cociente':<8} | {'Resto':<10}")
    print("-" * 35)
    
    for dividendo, cociente, digito in resultado['pasos']:
        print(f"{dividendo:<10} | {cociente:<8} | {digito:<10}")
    
    print(f"\nResultado: {resultado['resultado']}")
    print(f"\n(Leer los restos de abajo hacia arriba)")
    
    # Acceder a los datos estructurados para procesamiento
    print(f"\nDatos disponibles en el diccionario:")
    print(f"  - número original: {resultado['numero']}")
    print(f"  - base destino: {resultado['base']}")
    print(f"  - pasos: {len(resultado['pasos'])} divisiones")
    print(f"  - dígitos en orden: {resultado['digitos']}")
    print(f"  - resultado final: {resultado['resultado']}")
    
    # ========================================================================
    # NIVEL 3: EXPLICACIÓN COMPLETA (Educativo)
    # ========================================================================
    print("\n" + "=" * 70)
    print("[NIVEL 3] - Explicación Completa (Educativo detallado)")
    print("-" * 70)
    
    numero_nivel3 = 100
    base_nivel3 = 2
    
    print(f"\n{decimal_a_base_b_verbose(numero_nivel3, base_nivel3)}")
    
    # ========================================================================
    # CASOS PRÁCTICOS
    # ========================================================================
    print("\n" + "=" * 70)
    print("  CASOS PRÁCTICOS DE USO")
    print("=" * 70)
    
    # Caso 1: Conversión a múltiples bases al mismo tiempo
    print("\n[Caso 1] Convertir 255 a todas las bases importantes:")
    print("-" * 70)
    
    num = 255
    bases = {
        2: "Binario (informática)",
        8: "Octal (legacy)",
        10: "Decimal (natural)",
        16: "Hexadecimal (colors, memoria)",
        36: "Base 36 (URL-safe alphanumeric)"
    }
    
    for base, descripcion in bases.items():
        resultado = decimal_a_base_b_divisiones(num, base)
        print(f"  {descripcion:35}: {resultado}")
    
    # Caso 2: Validar entrada y convertir si es válida
    print("\n[Caso 2] Entrada de usuario con validación:")
    print("-" * 70)
    
    entrada = "42"
    base_entrada = 16
    
    try:
        resultado = decimal_a_base_b_divisiones(entrada, base_entrada)
        print(f"  Entrada: '{entrada}' (string)")
        print(f"  Base destino: {base_entrada}")
        print(f"  Resultado: {resultado}")
        print(f"  ✓ Conversión exitosa")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    
    # Caso 3: Padding para ancho fijo (importante en sistemas embebidos)
    print("\n[Caso 3] Padding para ancho fijo (8 bits):")
    print("-" * 70)
    
    numeros_padding = [0, 1, 15, 42, 127, 255]
    print(f"\n{'Dec':<4} | {'Binario (8 bits)':<18} | {'Hex (4 bits)':<14}")
    print("-" * 40)
    
    for num in numeros_padding:
        bin_padded = decimal_a_base_b_divisiones(num, 2, bits=8)
        hex_padded = decimal_a_base_b_divisiones(num, 16, bits=4)
        
        bin_str = bin_padded.replace("₂", "")
        hex_str = hex_padded.replace("₁₆", "")
        
        print(f"{num:<4} | {bin_str:>16}  | {hex_str:>12}")
    
    # Caso 4: Base 36 para compresión de URLs o IDs
    print("\n[Caso 4] Base 36 para compresión (Bases de datos, URLs):")
    print("-" * 70)
    
    ids_largos = [100, 1000, 10000, 100000, 1000000]
    
    print(f"\n{'ID Decimal':<15} | {'Base 36':<12} | {'Ahorro':<10}")
    print("-" * 42)
    
    for id_num in ids_largos:
        b10 = str(id_num)
        b36 = decimal_a_base_b_divisiones(id_num, 36).replace("₃₆", "")
        ahorro = f"{len(b10) - len(b36)} dígitos"
        
        print(f"{id_num:<15} | {b36:>10}  | {ahorro:<10}")
    
    # ========================================================================
    # RESUMEN
    # ========================================================================
    print("\n" + "=" * 70)
    print("  RESUMEN DE LA API")
    print("=" * 70 + "\n")
    
    print("3 Niveles de Complejidad:")
    print("""
1. decimal_a_base_b_divisiones(numero, base, bits=None)
   → Uso: Cuando solo necesitas el resultado final
   → Retorna: String con el número en la base especificada
   → Ejemplo: decimal_a_base_b_divisiones(42, 16) → "2A₁₆"

2. decimal_a_base_b_con_pasos(numero, base)
   → Uso: Para generar ejercicios con pasos visibles
   → Retorna: Dict con pasos, dígitos, resultado y explicación
   → Ejemplo: Para mostrar tabla de divisiones

3. decimal_a_base_b_verbose(numero, base)
   → Uso: Para ejercicios educativos con explicación completa
   → Retorna: String con explicación visual del proceso
   → Ejemplo: Para mostrar cómo se hace la conversión paso a paso

Bases soportadas: 2-36
  - Base 2-36: Usa dígitos 0-9 y letras A-Z
  - Máximo: Base 36 (alfanumérica completa)
  - Común: Binario (2), Octal (8), Decimal (10), Hexadecimal (16)
""")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
