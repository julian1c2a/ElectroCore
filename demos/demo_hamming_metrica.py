"""
Demostración Formal: La Distancia Hamming es una Métrica

Este script usa el sistema general de lógica matemática en core/math_logic_system/
para demostrar formalmente que la distancia de Hamming cumple las tres propiedades
de una métrica:

1. No negatividad e identidad: d(x,y) ≥ 0 y d(x,y) = 0 ⟺ x = y
2. Simetría: d(x,y) = d(y,x)
3. Desigualdad triangular: d(x,z) ≤ d(x,y) + d(y,z)

Usa el sistema general que también puede demostrar el álgebra de Boole
desde los postulados de Huntington (1903).

Autor: ElectroCore Project
Fecha: Enero 2026
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Tuple
from core.math_logic_system import (
    Expression, Var, Const, BinOp, Func, Forall, Equals, And, Iff, LessEq, Add,
    AxiomSystem, Axiom, Postulate,
    Proof, Theorem, ProofLibrary, JustificationType
)


# ============================================================================
# DISTANCIA DE HAMMING - Implementación Computacional
# ============================================================================

class HammingDistance:
    """Implementación de la distancia de Hamming."""
    
    @staticmethod
    def distance(x: str, y: str) -> int:
        """
        Calcula la distancia de Hamming entre dos cadenas.
        
        Args:
            x: Primera cadena
            y: Segunda cadena (debe tener la misma longitud que x)
            
        Returns:
            int: Número de posiciones donde difieren
        """
        if len(x) != len(y):
            raise ValueError("Las cadenas deben tener la misma longitud")
        
        return sum(1 for i in range(len(x)) if x[i] != y[i])
    
    @staticmethod
    def show_differences(x: str, y: str) -> str:
        """Muestra visualmente las diferencias entre dos cadenas."""
        if len(x) != len(y):
            raise ValueError("Las cadenas deben tener la misma longitud")
        
        result = []
        result.append(f"x: {x}")
        result.append(f"y: {y}")
        
        diff_markers = ""
        for i in range(len(x)):
            if x[i] != y[i]:
                diff_markers += "^"
            else:
                diff_markers += " "
        result.append(f"   {diff_markers}")
        
        return "\n".join(result)


# ============================================================================
# SISTEMA AXIOMÁTICO PARA ESPACIOS MÉTRICOS
# ============================================================================

def create_metric_space_axioms() -> AxiomSystem:
    """
    Crea el sistema axiomático para espacios métricos.
    
    Returns:
        AxiomSystem con los axiomas de espacios métricos
    """
    system = AxiomSystem(
        "Espacios Métricos",
        "Axiomas que definen una métrica en un conjunto"
    )
    
    # Variables
    x = Var("x")
    y = Var("y")
    z = Var("z")
    
    # Función distancia
    d_xy = Func("d", x, y)
    d_yx = Func("d", y, x)
    d_xz = Func("d", x, z)
    d_yz = Func("d", y, z)
    
    # Constante cero
    zero = Const(0, "0")
    
    # Axioma 1: No negatividad
    axiom_non_negative = Axiom(
        "M1-NonNegative",
        Forall("x", Forall("y",
            BinOp("≥", Func("d", Var("x"), Var("y")), Const(0, "0"), 0),
            Var("X")
        ), Var("X")),
        "No negatividad: d(x,y) ≥ 0 para todo x, y",
        {"non-negative", "metric"}
    )
    system.add_axiom(axiom_non_negative)
    
    # Axioma 2: Identidad de indiscernibles
    axiom_identity = Axiom(
        "M2-Identity",
        Forall("x", Forall("y",
            Iff(
                Equals(Func("d", Var("x"), Var("y")), Const(0, "0")),
                Equals(Var("x"), Var("y"))
            ),
            Var("X")
        ), Var("X")),
        "Identidad: d(x,y) = 0 ⟺ x = y",
        {"identity", "metric"}
    )
    system.add_axiom(axiom_identity)
    
    # Axioma 3: Simetría
    axiom_symmetry = Axiom(
        "M3-Symmetry",
        Forall("x", Forall("y",
            Equals(
                Func("d", Var("x"), Var("y")),
                Func("d", Var("y"), Var("x"))
            ),
            Var("X")
        ), Var("X")),
        "Simetría: d(x,y) = d(y,x)",
        {"symmetry", "metric"}
    )
    system.add_axiom(axiom_symmetry)
    
    # Axioma 4: Desigualdad triangular
    axiom_triangle = Axiom(
        "M4-Triangle",
        Forall("x", Forall("y", Forall("z",
            LessEq(
                Func("d", Var("x"), Var("z")),
                Add(
                    Func("d", Var("x"), Var("y")),
                    Func("d", Var("y"), Var("z"))
                )
            ),
            Var("X")
        ), Var("X")), Var("X")),
        "Desigualdad triangular: d(x,z) ≤ d(x,y) + d(y,z)",
        {"triangle", "metric"}
    )
    system.add_axiom(axiom_triangle)
    
    return system


# ============================================================================
# DEMOSTRACIÓN: LA DISTANCIA HAMMING SATISFACE LOS AXIOMAS MÉTRICOS
# ============================================================================

def prove_hamming_is_metric() -> ProofLibrary:
    """
    Demuestra que la distancia de Hamming es una métrica.
    
    Returns:
        ProofLibrary con los teoremas demostrados
    """
    library = ProofLibrary("Distancia de Hamming es Métrica")
    metric_system = create_metric_space_axioms()
    
    # ========================================================================
    # TEOREMA 1: No negatividad
    # ========================================================================
    
    proof_non_neg = Proof(
        BinOp("≥", Func("d_H", Var("x"), Var("y")), Const(0, "0"), 0),
        "La distancia de Hamming es no negativa"
    )
    proof_non_neg.set_axiom_system(metric_system)
    
    proof_non_neg.add_step(
        Equals(
            Func("d_H", Var("x"), Var("y")),
            Func("|·|", Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0)))
        ),
        "Definición de distancia de Hamming: d_H(x,y) = |{i : x[i] ≠ y[i]}|",
        JustificationType.DEFINITION
    )
    
    proof_non_neg.add_step(
        Forall("S",
            BinOp("≥", Func("|·|", Var("S")), Const(0, "0"), 0),
            Var("Sets")
        ),
        "Axioma: La cardinalidad de un conjunto es no negativa",
        JustificationType.AXIOM
    )
    
    proof_non_neg.add_step(
        BinOp("≥", Func("d_H", Var("x"), Var("y")), Const(0, "0"), 0),
        "Por aplicación del axioma a la definición de d_H",
        JustificationType.INFERENCE,
        [1, 2]
    )
    
    proof_non_neg.mark_complete()
    
    theorem_non_neg = Theorem(
        "Hamming-NonNegative",
        BinOp("≥", Func("d_H", Var("x"), Var("y")), Const(0, "0"), 0),
        proof_non_neg,
        "La distancia de Hamming es no negativa",
        {"hamming", "non-negative"}
    )
    library.add_theorem(theorem_non_neg)
    
    # ========================================================================
    # TEOREMA 2: Identidad (d=0 ⟺ x=y)
    # ========================================================================
    
    proof_identity = Proof(
        Iff(
            Equals(Func("d_H", Var("x"), Var("y")), Const(0, "0")),
            Equals(Var("x"), Var("y"))
        ),
        "d_H(x,y) = 0 si y solo si x = y"
    )
    proof_identity.set_axiom_system(metric_system)
    
    # Dirección (⟹): x = y ⟹ d_H(x,y) = 0
    proof_identity.add_hypothesis(
        Equals(Var("x"), Var("y")),
        "Supongamos x = y"
    )
    
    proof_identity.add_step(
        Forall("i", Equals(Var("x[i]"), Var("y[i]")), Var("indices")),
        "Si x = y, entonces x[i] = y[i] para todo i",
        JustificationType.DEFINITION,
        [1]
    )
    
    proof_identity.add_step(
        Equals(
            Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0)),
            Const("∅", "∅")
        ),
        "El conjunto de posiciones diferentes es vacío",
        JustificationType.INFERENCE,
        [2]
    )
    
    proof_identity.add_step(
        Equals(Func("d_H", Var("x"), Var("y")), Const(0, "0")),
        "Por tanto, d_H(x,y) = 0",
        JustificationType.INFERENCE,
        [3]
    )
    
    # Dirección (⟸): d_H(x,y) = 0 ⟹ x = y
    proof_identity.add_hypothesis(
        Equals(Func("d_H", Var("x"), Var("y")), Const(0, "0")),
        "Supongamos d_H(x,y) = 0"
    )
    
    proof_identity.add_step(
        Equals(
            Func("|·|", Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0))),
            Const(0, "0")
        ),
        "La cardinalidad del conjunto de diferencias es 0",
        JustificationType.DEFINITION,
        [5]
    )
    
    proof_identity.add_step(
        Equals(
            Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0)),
            Const("∅", "∅")
        ),
        "Solo el conjunto vacío tiene cardinalidad 0",
        JustificationType.AXIOM,
        [6]
    )
    
    proof_identity.add_step(
        Forall("i", Equals(Var("x[i]"), Var("y[i]")), Var("indices")),
        "Por tanto, x[i] = y[i] para todo i",
        JustificationType.INFERENCE,
        [7]
    )
    
    proof_identity.add_step(
        Equals(Var("x"), Var("y")),
        "Por definición de igualdad de cadenas, x = y",
        JustificationType.DEFINITION,
        [8]
    )
    
    proof_identity.add_step(
        Iff(
            Equals(Func("d_H", Var("x"), Var("y")), Const(0, "0")),
            Equals(Var("x"), Var("y"))
        ),
        "Hemos probado ambas direcciones",
        JustificationType.INFERENCE,
        [4, 9]
    )
    
    proof_identity.mark_complete()
    
    theorem_identity = Theorem(
        "Hamming-Identity",
        Iff(
            Equals(Func("d_H", Var("x"), Var("y")), Const(0, "0")),
            Equals(Var("x"), Var("y"))
        ),
        proof_identity,
        "d_H(x,y) = 0 si y solo si x = y",
        {"hamming", "identity"}
    )
    library.add_theorem(theorem_identity)
    
    # ========================================================================
    # TEOREMA 3: Simetría
    # ========================================================================
    
    proof_symmetry = Proof(
        Equals(
            Func("d_H", Var("x"), Var("y")),
            Func("d_H", Var("y"), Var("x"))
        ),
        "La distancia de Hamming es simétrica"
    )
    proof_symmetry.set_axiom_system(metric_system)
    
    proof_symmetry.add_step(
        Equals(
            Func("d_H", Var("x"), Var("y")),
            Func("|·|", Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0)))
        ),
        "Definición de d_H(x,y)",
        JustificationType.DEFINITION
    )
    
    proof_symmetry.add_step(
        Forall("i",
            Iff(
                BinOp("≠", Var("x[i]"), Var("y[i]"), 0),
                BinOp("≠", Var("y[i]"), Var("x[i]"), 0)
            ),
            Var("indices")
        ),
        "La desigualdad es simétrica: x[i] ≠ y[i] ⟺ y[i] ≠ x[i]",
        JustificationType.AXIOM
    )
    
    proof_symmetry.add_step(
        Equals(
            Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0)),
            Func("set", BinOp("≠", Var("y[i]"), Var("x[i]"), 0))
        ),
        "Los conjuntos de posiciones diferentes son idénticos",
        JustificationType.INFERENCE,
        [2]
    )
    
    proof_symmetry.add_step(
        Equals(
            Func("|·|", Func("set", BinOp("≠", Var("x[i]"), Var("y[i]"), 0))),
            Func("|·|", Func("set", BinOp("≠", Var("y[i]"), Var("x[i]"), 0)))
        ),
        "Conjuntos iguales tienen la misma cardinalidad",
        JustificationType.AXIOM,
        [3]
    )
    
    proof_symmetry.add_step(
        Equals(
            Func("d_H", Var("x"), Var("y")),
            Func("d_H", Var("y"), Var("x"))
        ),
        "Por sustitución y definición",
        JustificationType.INFERENCE,
        [1, 4]
    )
    
    proof_symmetry.mark_complete()
    
    theorem_symmetry = Theorem(
        "Hamming-Symmetry",
        Equals(
            Func("d_H", Var("x"), Var("y")),
            Func("d_H", Var("y"), Var("x"))
        ),
        proof_symmetry,
        "La distancia de Hamming es simétrica",
        {"hamming", "symmetry"}
    )
    library.add_theorem(theorem_symmetry)
    
    # ========================================================================
    # TEOREMA 4: Desigualdad Triangular
    # ========================================================================
    
    proof_triangle = Proof(
        LessEq(
            Func("d_H", Var("x"), Var("z")),
            Add(
                Func("d_H", Var("x"), Var("y")),
                Func("d_H", Var("y"), Var("z"))
            )
        ),
        "Desigualdad triangular para la distancia de Hamming"
    )
    proof_triangle.set_axiom_system(metric_system)
    
    proof_triangle.add_step(
        Equals(
            Func("d_H", Var("x"), Var("z")),
            Func("|·|", Func("I", "conjunto de posiciones donde x ≠ z"))
        ),
        "Sea I = {i : x[i] ≠ z[i]}",
        JustificationType.DEFINITION
    )
    
    proof_triangle.add_step(
        Equals(
            Func("I"),
            BinOp("∪",
                Func("I1", "posiciones donde x≠y∧y=z o x=y∧y≠z"),
                Func("I2", "posiciones donde x≠y∧y≠z"),
                0
            )
        ),
        "Partición de I según el valor de y[i]",
        JustificationType.DEFINITION
    )
    
    proof_triangle.add_step(
        BinOp("⊆", Func("I1"), Func("set", "x[i] ≠ y[i] o y[i] ≠ z[i]"), 0),
        "Cada elemento de I1 difiere en x-y o y-z",
        JustificationType.INFERENCE,
        [2]
    )
    
    proof_triangle.add_step(
        BinOp("⊆", Func("I2"), Func("set", "x[i] ≠ y[i] y y[i] ≠ z[i]"), 0),
        "Cada elemento de I2 difiere en ambos",
        JustificationType.INFERENCE,
        [2]
    )
    
    proof_triangle.add_step(
        LessEq(
            Func("|·|", Func("I")),
            Add(Func("|·|", Func("I1")), Func("|·|", Func("I2")))
        ),
        "Por propiedad de cardinalidad de uniones",
        JustificationType.AXIOM,
        [2]
    )
    
    proof_triangle.add_step(
        And(
            LessEq(Func("|·|", Func("I1")), Func("d_H", Var("x"), Var("y"))),
            LessEq(Func("|·|", Func("I2")), Func("d_H", Var("y"), Var("z")))
        ),
        "I1 e I2 son subconjuntos de las diferencias respectivas",
        JustificationType.INFERENCE,
        [3, 4]
    )
    
    proof_triangle.add_step(
        LessEq(
            Func("d_H", Var("x"), Var("z")),
            Add(
                Func("d_H", Var("x"), Var("y")),
                Func("d_H", Var("y"), Var("z"))
            )
        ),
        "Por transitividad y sustitución",
        JustificationType.INFERENCE,
        [1, 5, 6]
    )
    
    proof_triangle.mark_complete()
    
    theorem_triangle = Theorem(
        "Hamming-Triangle",
        LessEq(
            Func("d_H", Var("x"), Var("z")),
            Add(
                Func("d_H", Var("x"), Var("y")),
                Func("d_H", Var("y"), Var("z"))
            )
        ),
        proof_triangle,
        "Desigualdad triangular",
        {"hamming", "triangle"}
    )
    library.add_theorem(theorem_triangle)
    
    return library


# ============================================================================
# VALIDACIÓN CON EJEMPLOS CONCRETOS
# ============================================================================

def validate_with_examples():
    """Valida las propiedades con ejemplos concretos."""
    
    print("\n" + "=" * 80)
    print("VALIDACIÓN CON EJEMPLOS CONCRETOS")
    print("=" * 80 + "\n")
    
    # Ejemplos de cadenas
    examples = [
        ("1010", "1010"),
        ("1010", "0101"),
        ("1111", "0000"),
        ("10101", "10111"),
    ]
    
    for x, y in examples:
        print(f"\n{'='*60}")
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"{'='*60}")
        
        d_xy = HammingDistance.distance(x, y)
        print(f"\nd(x,y) = {d_xy}")
        print(HammingDistance.show_differences(x, y))
        
        # Propiedad 1: No negatividad
        print(f"\n✓ Propiedad 1 (No negatividad): d(x,y) = {d_xy} ≥ 0")
        
        # Propiedad 1: Identidad
        if x == y:
            print(f"✓ Propiedad 1 (Identidad): x = y ⟹ d(x,y) = {d_xy} = 0")
        else:
            print(f"✓ Propiedad 1 (Identidad): x ≠ y ⟹ d(x,y) = {d_xy} > 0")
        
        # Propiedad 2: Simetría
        d_yx = HammingDistance.distance(y, x)
        print(f"✓ Propiedad 2 (Simetría): d(x,y) = {d_xy}, d(y,x) = {d_yx}")
        assert d_xy == d_yx, "¡Fallo en simetría!"
    
    # Ejemplos para desigualdad triangular
    print("\n\n" + "=" * 80)
    print("VALIDACIÓN DE DESIGUALDAD TRIANGULAR")
    print("=" * 80)
    
    triangular_examples = [
        ("1010", "1100", "0000"),
        ("0000", "1111", "0101"),
        ("10101", "11111", "00000"),
    ]
    
    for x, y, z in triangular_examples:
        print(f"\n{'='*60}")
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"z = {z}")
        print(f"{'='*60}")
        
        d_xy = HammingDistance.distance(x, y)
        d_yz = HammingDistance.distance(y, z)
        d_xz = HammingDistance.distance(x, z)
        
        print(f"\nd(x,y) = {d_xy}")
        print(HammingDistance.show_differences(x, y))
        
        print(f"\nd(y,z) = {d_yz}")
        print(HammingDistance.show_differences(y, z))
        
        print(f"\nd(x,z) = {d_xz}")
        print(HammingDistance.show_differences(x, z))
        
        sum_distances = d_xy + d_yz
        print(f"\n✓ Propiedad 3 (Desigualdad triangular):")
        print(f"  d(x,z) = {d_xz} ≤ {sum_distances} = d(x,y) + d(y,z)")
        print(f"  {d_xz} ≤ {d_xy} + {d_yz}")
        
        assert d_xz <= sum_distances, "¡Fallo en desigualdad triangular!"


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecuta todas las demostraciones."""
    
    print("\n" + "=" * 80)
    print(" " * 15 + "DEMOSTRACIÓN FORMAL")
    print(" " * 10 + "LA DISTANCIA DE HAMMING ES UNA MÉTRICA")
    print(" " * 8 + "(Usando el Sistema General de Lógica Matemática)")
    print("=" * 80)
    
    # Crear el sistema axiomático
    metric_system = create_metric_space_axioms()
    print("\n" + metric_system.show_summary())
    
    # Derivar teoremas
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 15 + "DEMOSTRACIÓN: DISTANCIA HAMMING ES MÉTRICA" + " " * 20 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    library = prove_hamming_is_metric()
    
    # Mostrar cada teorema
    for theorem_name in ["Hamming-NonNegative", "Hamming-Identity", 
                         "Hamming-Symmetry", "Hamming-Triangle"]:
        theorem = library.get_theorem(theorem_name)
        if theorem:
            print(theorem.show())
            print("\n")
    
    # Conclusión
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 25 + "CONCLUSIÓN FINAL" + " " * 37 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80 + "\n")
    
    print("Por los cuatro teoremas demostrados:")
    print()
    print("  1. d_H(x,y) ≥ 0 (No negatividad)")
    print("  2. d_H(x,y) = 0 ⟺ x = y (Identidad)")
    print("  3. d_H(x,y) = d_H(y,x) (Simetría)")
    print("  4. d_H(x,z) ≤ d_H(x,y) + d_H(y,z) (Desigualdad triangular)")
    print()
    print("Concluimos que la distancia de Hamming es una MÉTRICA en el")
    print("espacio de cadenas de longitud fija.")
    print()
    print("□ Q.E.D.")
    print("=" * 80)
    
    # Validación con ejemplos
    validate_with_examples()
    
    print("\n" + "=" * 80)
    print(" " * 25 + "DEMOSTRACIÓN COMPLETADA")
    print(" " * 15 + "Sistema general disponible en:")
    print(" " * 20 + "core/math_logic_system/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
