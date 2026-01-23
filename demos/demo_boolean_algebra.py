"""
Demostración: Álgebra de Boole desde los Postulados de Huntington (1903)

Este script usa el sistema general de lógica matemática en core/math_logic_system/
para demostrar teoremas del álgebra de Boole partiendo de los postulados de
Edward V. Huntington publicados en 1903.

Los postulados de Huntington definen axiomáticamente el álgebra de Boole con:
- Un conjunto B con al menos dos elementos
- Dos operaciones binarias: + (OR) y · (AND)
- Propiedades: conmutatividad, identidades, distributividad, complemento

Autor: ElectroCore Project
Fecha: Enero 2026
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.math_logic_system.boolean_algebra import (
    BooleanAlgebra, HuntingtonPostulates, derive_boolean_theorems
)


def main():
    """Ejecuta la demostración del álgebra de Boole."""
    
    print("\n" + "=" * 80)
    print(" " * 15 + "ÁLGEBRA DE BOOLE")
    print(" " * 10 + "POSTULADOS DE HUNTINGTON (1903)")
    print(" " * 8 + "(Usando el Sistema General de Lógica Matemática)")
    print("=" * 80)
    
    # Crear el sistema de álgebra de Boole
    boolean_algebra = BooleanAlgebra()
    
    # Mostrar los postulados
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 25 + "POSTULADOS DE HUNTINGTON" + " " * 29 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    system = boolean_algebra.get_postulates()
    print(system.show_summary())
    
    # Derivar teoremas
    print("\n\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "TEOREMAS DERIVADOS DEL ÁLGEBRA DE BOOLE" + " " * 19 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    library = boolean_algebra.derive_theorems()
    
    # Mostrar el teorema de idempotencia
    theorem = library.get_theorem("T1a-Idempotence-OR")
    if theorem:
        print(theorem.show())
    
    # Resumen de teoremas disponibles
    print("\n\n" + "=" * 80)
    print("BIBLIOTECA DE TEOREMAS")
    print("=" * 80)
    print(library.list_all())
    
    # Ejemplos de evaluación
    print("\n\n" + "=" * 80)
    print("EVALUACIÓN DE EXPRESIONES BOOLEANAS")
    print("=" * 80)
    
    from core.math_logic_system import Var, BinOp, UnOp
    
    # Ejemplo 1: a + a = a (idempotencia)
    a = Var("a")
    expr1 = BinOp("+", a, a, 4)
    
    print(f"\nEjemplo 1: {expr1}")
    print("Valores:")
    for a_val in [False, True]:
        result = boolean_algebra.evaluate(expr1, {"a": a_val})
        print(f"  a = {a_val} → {expr1} = {result}")
    print(f"Verifica la idempotencia: a + a = a")
    
    # Ejemplo 2: a · (a + b) = a (absorción)
    b = Var("b")
    expr2 = BinOp("·", a, BinOp("+", a, b, 4), 5)
    
    print(f"\nEjemplo 2: {expr2}")
    print("Tabla de verdad:")
    print("  a | b | a+(b) | a·(a+b)")
    print("  --|---|-------|--------")
    for a_val in [False, True]:
        for b_val in [False, True]:
            or_result = a_val or b_val
            and_result = a_val and or_result
            print(f"  {int(a_val)} | {int(b_val)} |   {int(or_result)}   |    {int(and_result)}")
    print(f"Verifica la absorción: a · (a + b) = a")
    
    # Ejemplo 3: a + a' = 1 (complemento)
    expr3 = BinOp("+", a, UnOp("'", a), 4)
    
    print(f"\nEjemplo 3: {expr3}")
    print("Valores:")
    for a_val in [False, True]:
        not_a = not a_val
        result = a_val or not_a
        print(f"  a = {a_val}, a' = {not_a} → {expr3} = {result}")
    print(f"Verifica el complemento: a + a' = 1")
    
    # Ejemplo 4: Ley de De Morgan: (a · b)' = a' + b'
    expr4_left = UnOp("'", BinOp("·", a, b, 5))
    expr4_right = BinOp("+", UnOp("'", a), UnOp("'", b), 4)
    
    print(f"\nEjemplo 4 (Ley de De Morgan):")
    print(f"  {expr4_left} = {expr4_right}")
    print("Tabla de verdad:")
    print("  a | b | a·b | (a·b)' | a' | b' | a'+b'")
    print("  --|---|-----|--------|----|----|------")
    for a_val in [False, True]:
        for b_val in [False, True]:
            and_result = a_val and b_val
            not_and = not and_result
            not_a = not a_val
            not_b = not b_val
            or_not = not_a or not_b
            print(f"  {int(a_val)} | {int(b_val)} |  {int(and_result)}  |   {int(not_and)}    | {int(not_a)}  | {int(not_b)}  |   {int(or_not)}")
    print(f"Verifica la Ley de De Morgan: (a · b)' = a' + b'")
    
    # Conclusión
    print("\n\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 25 + "CONCLUSIÓN" + " " * 43 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    print("El sistema axiomático de Huntington (1903) define completamente")
    print("el álgebra de Boole. A partir de sus 6 postulados fundamentales:")
    print()
    print("  P1. Cierre bajo + y ·")
    print("  P2. Conmutatividad de + y ·")
    print("  P3. Existencia de identidades 0 y 1")
    print("  P4. Distributividad de + sobre · y · sobre +")
    print("  P5. Existencia de complementos")
    print("  P6. Existencia de al menos dos elementos distintos")
    print()
    print("Podemos derivar TODOS los teoremas del álgebra de Boole, incluyendo:")
    print("  • Idempotencia")
    print("  • Absorción")
    print("  • Leyes de De Morgan")
    print("  • Involución del complemento")
    print("  • Y muchos más...")
    print()
    print("□ Q.E.D.")
    print()
    print("=" * 80)
    print(" " * 20 + "SISTEMA DISPONIBLE EN:")
    print(" " * 20 + "core/math_logic_system/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
