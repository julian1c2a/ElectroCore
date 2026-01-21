"""
Jugar con diferentes representaciones numéricas en bases 2-36

Un explorador interactivo de cómo un número se ve en diferentes bases.
"""

from core.numeracion_utils import decimal_a_base_b_divisiones, obtener_digitos_para_base


def mostrar_numero_en_todas_bases(numero: int):
    """
    Muestra un número decimal en TODAS las bases soportadas (2-36).
    
    Args:
        numero: Número decimal a mostrar
    """
    print(f"\n{'═' * 80}")
    print(f"  NÚMERO {numero} EN TODAS LAS BASES (2-36)")
    print(f"{'═' * 80}\n")
    
    # Mostrar en grupo: bases pequeñas, medias, grandes
    grupos = [
        ("Bases Pequeñas (2-10)", range(2, 11)),
        ("Bases Medianas (11-20)", range(11, 21)),
        ("Bases Grandes (21-36)", range(21, 37))
    ]
    
    for nombre_grupo, bases in grupos:
        print(f"\n{nombre_grupo}:")
        print("─" * 80)
        
        for base in bases:
            resultado = decimal_a_base_b_divisiones(numero, base)
            digitos = obtener_digitos_para_base(base)
            
            # Alinear resultados
            print(f"  Base {base:2} ({nombre_base(base):12}): {resultado:20} "
                  f"(usa dígitos: {digitos})")


def nombre_base(base: int) -> str:
    """Retorna el nombre común de una base."""
    nombres = {
        2: "Binario",
        3: "Ternario",
        4: "Cuaternario",
        5: "Quinario",
        6: "Senario",
        7: "Septenary",
        8: "Octal",
        9: "Nonary",
        10: "Decimal",
        12: "Duodecimal",
        16: "Hexadecimal",
        20: "Vigesimal",
        36: "Alphanumeric"
    }
    return nombres.get(base, f"Base-{base}")


def comparar_numeros(numeros: list):
    """
    Compara múltiples números en múltiples bases.
    
    Args:
        numeros: Lista de números decimales a comparar
    """
    print(f"\n{'═' * 100}")
    print(f"  COMPARACIÓN: Múltiples números en múltiples bases")
    print(f"{'═' * 100}\n")
    
    bases_interes = [2, 8, 10, 12, 16, 20, 36]
    
    # Encabezado
    encabezado = "Decimal |"
    for base in bases_interes:
        encabezado += f" Base {base:2} |"
    
    print(encabezado)
    print("─" * 100)
    
    # Filas
    for numero in numeros:
        fila = f"{numero:7} |"
        for base in bases_interes:
            resultado = decimal_a_base_b_divisiones(numero, base)
            # Quitar el subíndice para mejor alineación
            resultado_limpio = resultado.replace(f"₍{base}₎", "").replace("₂", "").replace("₈", "").replace("₁₀", "").replace("₁₆", "").replace("₂₀", "").replace("₃₆", "")
            # En realidad voy a usar una forma más simple
            resultado_limpio = resultado[:-1]  # Quitar subíndice (último carácter)
            fila += f" {resultado_limpio:>8} |"
        print(fila)


def explorador_interactivo():
    """
    Explorador interactivo: El usuario elige un número y una base.
    """
    print(f"\n{'═' * 80}")
    print(f"  EXPLORADOR INTERACTIVO: Convierte números a cualquier base")
    print(f"{'═' * 80}\n")
    
    while True:
        try:
            numero = int(input("\nIngresa un número decimal (o 'q' para salir): "))
            
            print(f"\nNúmero {numero} en diferentes bases:")
            print("-" * 60)
            
            # Mostrar primero las bases comunes
            bases_comunes = {
                2: "Binario",
                8: "Octal",
                10: "Decimal",
                16: "Hexadecimal",
                36: "Base 36"
            }
            
            for base, nombre in bases_comunes.items():
                resultado = decimal_a_base_b_divisiones(numero, base)
                print(f"  {nombre:12}: {resultado}")
            
            # Preguntar si quiere más
            print("\n¿Quieres verlo en más bases? (ej: 3, 5, 12, 20)")
            respuesta = input("Ingresa bases separadas por comas (o 'n' para otro número): ").strip()
            
            if respuesta.lower() != 'n':
                try:
                    bases_extra = [int(b.strip()) for b in respuesta.split(',')]
                    print("\nBases adicionales:")
                    for base in bases_extra:
                        try:
                            resultado = decimal_a_base_b_divisiones(numero, base)
                            print(f"  Base {base:2}: {resultado}")
                        except ValueError as e:
                            print(f"  Base {base}: ✗ Error - {e}")
                except:
                    print("  Error al procesar las bases.")
        
        except ValueError:
            print("❌ Error: Ingresa un número válido")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  JUGANDO CON BASES NUMÉRICAS (2-36)".center(78) + "║")
    print("║" + "  Explora cómo un número se representa en diferentes sistemas".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝\n")
    
    while True:
        print("\nMENÚ DE OPCIONES:")
        print("─" * 60)
        print("1. Ver un número en TODAS las bases (2-36)")
        print("2. Comparar múltiples números en bases de interés")
        print("3. Explorador interactivo")
        print("4. Ejemplos predefinidos")
        print("5. Salir")
        print()
        
        opcion = input("Elige una opción (1-5): ").strip()
        
        if opcion == '1':
            try:
                numero = int(input("Ingresa un número decimal: "))
                mostrar_numero_en_todas_bases(numero)
            except ValueError:
                print("❌ Número inválido")
        
        elif opcion == '2':
            print("\nIngresa números separados por comas (ej: 10, 100, 255)")
            try:
                entrada = input("Números: ").strip()
                numeros = [int(n.strip()) for n in entrada.split(',')]
                comparar_numeros(numeros)
            except ValueError:
                print("❌ Error al procesar los números")
        
        elif opcion == '3':
            explorador_interactivo()
        
        elif opcion == '4':
            print("\n" + "═" * 80)
            print("  EJEMPLOS PREDEFINIDOS")
            print("═" * 80)
            
            ejemplos = [
                (13, "Número pequeño"),
                (42, "Respuesta a todo (Douglas Adams)"),
                (100, "Número redondo"),
                (255, "Máximo de 8 bits"),
                (1000, "Número grande"),
                (1295, "Máximo en base 36 con 2 dígitos (ZZ₃₆)")
            ]
            
            for numero, descripcion in ejemplos:
                print(f"\n► {numero}: {descripcion}")
                print("  " + "─" * 75)
                
                # Mostrar en bases principales
                bases = [2, 8, 16, 36]
                for base in bases:
                    resultado = decimal_a_base_b_divisiones(numero, base)
                    nombre = nombre_base(base)
                    print(f"    {nombre:12}: {resultado}")
        
        elif opcion == '5':
            print("\n¡Hasta luego! 👋")
            break
        
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()
