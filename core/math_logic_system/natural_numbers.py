"""
Números Naturales - Axiomas de Peano

Implementa el sistema axiomático de los números naturales según
Giuseppe Peano (1889).

Los axiomas de Peano definen los números naturales con:
- 0 es un número natural
- Cada natural tiene un sucesor
- 0 no es sucesor de ningún número
- El sucesor es inyectivo
- Principio de inducción matemática

Autor: ElectroCore Project
Fecha: Enero 2026
"""

from typing import List, Dict
from .axioms import AxiomSystem, Axiom, Definition
from .expressions import *
from .proof_system import Proof, Theorem, ProofLibrary, JustificationType
from .inference_rules import MathematicalInduction


def create_peano_axioms() -> AxiomSystem:
    """
    Crea el sistema axiomático de los números naturales según Peano (1889).
    
    Returns:
        AxiomSystem con los axiomas de Peano
    """
    system = AxiomSystem(
        "Números Naturales (Axiomas de Peano)",
        "Sistema axiomático de los números naturales basado en Peano (1889)"
    )
    
    # Constantes y funciones
    zero = Const(0, "0")
    n = Var("n")
    m = Var("m")
    
    # AXIOMA P1: 0 es un número natural
    p1_zero = Axiom(
        "P1-Zero",
        Pred("∈", Const(0, "0"), Var("ℕ")),
        "0 es un número natural",
        {"peano", "base"}
    )
    system.add_axiom(p1_zero)
    
    # AXIOMA P2: Cada número natural tiene un sucesor único
    # ∀n ∈ ℕ: S(n) ∈ ℕ
    p2_successor = Axiom(
        "P2-Successor",
        Forall("n",
            Implies(
                Pred("∈", Var("n"), Var("ℕ")),
                Pred("∈", Func("S", Var("n")), Var("ℕ"))
            ),
            Var("ℕ")
        ),
        "El sucesor de un natural es natural",
        {"peano", "successor", "closure"}
    )
    system.add_axiom(p2_successor)
    
    # AXIOMA P3: 0 no es el sucesor de ningún número natural
    # ∀n ∈ ℕ: S(n) ≠ 0
    p3_zero_not_successor = Axiom(
        "P3-Zero-Not-Successor",
        Forall("n",
            Implies(
                Pred("∈", Var("n"), Var("ℕ")),
                NotEquals(Func("S", Var("n")), Const(0, "0"))
            ),
            Var("ℕ")
        ),
        "0 no es sucesor de ningún natural",
        {"peano", "zero", "successor"}
    )
    system.add_axiom(p3_zero_not_successor)
    
    # AXIOMA P4: El sucesor es inyectivo
    # ∀n,m ∈ ℕ: S(n) = S(m) ⟹ n = m
    p4_successor_injective = Axiom(
        "P4-Successor-Injective",
        Forall("n", Forall("m",
            Implies(
                And(
                    Pred("∈", Var("n"), Var("ℕ")),
                    Pred("∈", Var("m"), Var("ℕ"))
                ),
                Implies(
                    Equals(Func("S", Var("n")), Func("S", Var("m"))),
                    Equals(Var("n"), Var("m"))
                )
            ),
            Var("ℕ")
        ), Var("ℕ")),
        "El sucesor es inyectivo (diferentes naturales tienen diferentes sucesores)",
        {"peano", "successor", "injective"}
    )
    system.add_axiom(p4_successor_injective)
    
    # AXIOMA P5: Principio de Inducción Matemática
    # Si P(0) y (∀n ∈ ℕ: P(n) ⟹ P(S(n))), entonces ∀n ∈ ℕ: P(n)
    # 
    # Este es un esquema de axioma: una familia infinita de axiomas,
    # uno para cada predicado P
    p5_induction = Axiom(
        "P5-Induction",
        Forall("P",
            Implies(
                And(
                    Func("P", Const(0, "0")),
                    Forall("n",
                        Implies(
                            Func("P", Var("n")),
                            Func("P", Func("S", Var("n")))
                        ),
                        Var("ℕ")
                    )
                ),
                Forall("n", Func("P", Var("n")), Var("ℕ"))
            )
        ),
        "Principio de Inducción Matemática: Si P(0) y ∀n: P(n)⟹P(S(n)), entonces ∀n: P(n)",
        {"peano", "induction"}
    )
    system.add_axiom(p5_induction)
    
    # Definiciones derivadas
    
    # Definición de suma
    def_addition = Definition(
        "Addition",
        "+",
        And(
            # n + 0 = n
            Forall("n",
                Equals(
                    BinOp("+", Var("n"), Const(0, "0"), 4),
                    Var("n")
                ),
                Var("ℕ")
            ),
            # n + S(m) = S(n + m)
            Forall("n", Forall("m",
                Equals(
                    BinOp("+", Var("n"), Func("S", Var("m")), 4),
                    Func("S", BinOp("+", Var("n"), Var("m"), 4))
                ),
                Var("ℕ")
            ), Var("ℕ"))
        ),
        "Definición recursiva de la suma: n+0=n, n+S(m)=S(n+m)"
    )
    system.add_definition(def_addition)
    
    # Definición de multiplicación
    def_multiplication = Definition(
        "Multiplication",
        "·",
        And(
            # n · 0 = 0
            Forall("n",
                Equals(
                    BinOp("·", Var("n"), Const(0, "0"), 5),
                    Const(0, "0")
                ),
                Var("ℕ")
            ),
            # n · S(m) = n · m + n
            Forall("n", Forall("m",
                Equals(
                    BinOp("·", Var("n"), Func("S", Var("m")), 5),
                    BinOp("+", BinOp("·", Var("n"), Var("m"), 5), Var("n"), 4)
                ),
                Var("ℕ")
            ), Var("ℕ"))
        ),
        "Definición recursiva de la multiplicación: n·0=0, n·S(m)=n·m+n"
    )
    system.add_definition(def_multiplication)
    
    # Definición de orden
    def_less_than = Definition(
        "LessThan",
        "<",
        Forall("n", Forall("m",
            Iff(
                Pred("<", Var("n"), Var("m")),
                Exists("k",
                    And(
                        NotEquals(Var("k"), Const(0, "0")),
                        Equals(
                            BinOp("+", Var("n"), Var("k"), 4),
                            Var("m")
                        )
                    ),
                    Var("ℕ")
                )
            ),
            Var("ℕ")
        ), Var("ℕ")),
        "Definición de orden: n < m ⟺ ∃k≠0: n+k=m"
    )
    system.add_definition(def_less_than)
    
    return system


class PeanoArithmetic:
    """
    Implementación computacional de la aritmética de Peano.
    
    Permite trabajar con números naturales y demostrar propiedades
    por inducción matemática.
    """
    
    def __init__(self):
        self.system = create_peano_axioms()
        self.library = ProofLibrary("Aritmética de Peano")
    
    def get_axioms(self) -> AxiomSystem:
        """Obtiene los axiomas de Peano."""
        return self.system
    
    def get_library(self) -> ProofLibrary:
        """Obtiene la biblioteca de teoremas."""
        return self.library
    
    def show_axioms(self) -> None:
        """Muestra todos los axiomas de Peano."""
        print(self.system.show_summary())
    
    def successor(self, n: int) -> int:
        """Función sucesor computacional."""
        return n + 1
    
    def add(self, n: int, m: int) -> int:
        """Suma de naturales (definición recursiva)."""
        if m == 0:
            return n
        return self.successor(self.add(n, m - 1))
    
    def multiply(self, n: int, m: int) -> int:
        """Multiplicación de naturales (definición recursiva)."""
        if m == 0:
            return 0
        return self.add(self.multiply(n, m - 1), n)
    
    def power(self, base: int, exp: int) -> int:
        """Exponenciación de naturales."""
        if exp == 0:
            return 1
        return self.multiply(self.power(base, exp - 1), base)


def prove_sum_formula() -> Theorem:
    """
    Demuestra por inducción: ∑(i=0 to n) i = n(n+1)/2
    
    O en términos de Peano: 0+1+2+...+n = n·(n+1)/2
    """
    peano = create_peano_axioms()
    
    # Objetivo: ∀n: sum(n) = n(n+1)/2
    # Donde sum(n) = 0 + 1 + 2 + ... + n
    
    goal = Forall("n",
        Equals(
            Func("sum", Var("n")),
            BinOp("·",
                Var("n"),
                BinOp("+", Var("n"), Const(1, "1"), 4),
                5
            )
        ),
        Var("ℕ")
    )
    
    proof = Proof(goal, "Fórmula de la suma: ∑(i=0 to n) i = n(n+1)/2")
    proof.set_axiom_system(peano)
    
    # Caso base: n = 0
    proof.add_step(
        Equals(Func("sum", Const(0, "0")), Const(0, "0")),
        "Caso base: sum(0) = 0",
        JustificationType.DEFINITION
    )
    
    proof.add_step(
        Equals(
            BinOp("·",
                Const(0, "0"),
                BinOp("+", Const(0, "0"), Const(1, "1"), 4),
                5
            ),
            Const(0, "0")
        ),
        "0·(0+1) = 0·1 = 0",
        JustificationType.DEFINITION
    )
    
    proof.add_step(
        Equals(
            Func("sum", Const(0, "0")),
            BinOp("·",
                Const(0, "0"),
                BinOp("+", Const(0, "0"), Const(1, "1"), 4),
                5
            )
        ),
        "Por tanto, P(0) es verdadero",
        JustificationType.INFERENCE,
        [1, 2]
    )
    
    # Paso inductivo: Asumimos P(n), demostramos P(n+1)
    proof.add_hypothesis(
        Equals(
            Func("sum", Var("n")),
            BinOp("·",
                Var("n"),
                BinOp("+", Var("n"), Const(1, "1"), 4),
                5
            )
        ),
        "Hipótesis inductiva: sum(n) = n(n+1)/2"
    )
    
    proof.add_step(
        Equals(
            Func("sum", Func("S", Var("n"))),
            BinOp("+",
                Func("sum", Var("n")),
                Func("S", Var("n")),
                4
            )
        ),
        "Por definición: sum(n+1) = sum(n) + (n+1)",
        JustificationType.DEFINITION
    )
    
    proof.add_step(
        Equals(
            BinOp("+",
                Func("sum", Var("n")),
                Func("S", Var("n")),
                4
            ),
            BinOp("+",
                BinOp("·",
                    Var("n"),
                    BinOp("+", Var("n"), Const(1, "1"), 4),
                    5
                ),
                Func("S", Var("n")),
                4
            )
        ),
        "Sustituimos la hipótesis inductiva",
        JustificationType.INFERENCE,
        [4, 5]
    )
    
    proof.add_step(
        Equals(
            BinOp("+",
                BinOp("·",
                    Var("n"),
                    BinOp("+", Var("n"), Const(1, "1"), 4),
                    5
                ),
                Func("S", Var("n")),
                4
            ),
            BinOp("·",
                Func("S", Var("n")),
                BinOp("+", Func("S", Var("n")), Const(1, "1"), 4),
                5
            )
        ),
        "Álgebra: n(n+1)/2 + (n+1) = (n+1)(n+2)/2",
        JustificationType.INFERENCE,
        [6]
    )
    
    proof.add_step(
        Equals(
            Func("sum", Func("S", Var("n"))),
            BinOp("·",
                Func("S", Var("n")),
                BinOp("+", Func("S", Var("n")), Const(1, "1"), 4),
                5
            )
        ),
        "Por tanto, P(n+1) es verdadero",
        JustificationType.INFERENCE,
        [5, 6, 7]
    )
    
    # Aplicar inducción
    proof.add_step(
        Forall("n",
            Implies(
                Equals(
                    Func("sum", Var("n")),
                    BinOp("·",
                        Var("n"),
                        BinOp("+", Var("n"), Const(1, "1"), 4),
                        5
                    )
                ),
                Equals(
                    Func("sum", Func("S", Var("n"))),
                    BinOp("·",
                        Func("S", Var("n")),
                        BinOp("+", Func("S", Var("n")), Const(1, "1"), 4),
                        5
                    )
                )
            ),
            Var("ℕ")
        ),
        "Hemos demostrado el paso inductivo",
        JustificationType.INFERENCE,
        [4, 8]
    )
    
    proof.add_step(
        goal,
        "Por el principio de inducción matemática (P5)",
        JustificationType.INFERENCE,
        [3, 9]
    )
    
    proof.mark_complete()
    
    theorem = Theorem(
        "Sum-Formula",
        goal,
        proof,
        "Fórmula de la suma de los primeros n naturales",
        {"peano", "induction", "sum"}
    )
    
    return theorem


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 80)
    print("NÚMEROS NATURALES - AXIOMAS DE PEANO (1889)")
    print("=" * 80)
    
    peano = PeanoArithmetic()
    peano.show_axioms()
    
    print("\n\n" + "=" * 80)
    print("EJEMPLOS COMPUTACIONALES")
    print("=" * 80)
    
    print("\nFunción sucesor:")
    for i in range(5):
        print(f"  S({i}) = {peano.successor(i)}")
    
    print("\nSuma (definición recursiva):")
    print(f"  3 + 4 = {peano.add(3, 4)}")
    print(f"  5 + 0 = {peano.add(5, 0)}")
    
    print("\nMultiplicación (definición recursiva):")
    print(f"  3 · 4 = {peano.multiply(3, 4)}")
    print(f"  5 · 2 = {peano.multiply(5, 2)}")
    
    print("\nExponenciación:")
    print(f"  2³ = {peano.power(2, 3)}")
    print(f"  3² = {peano.power(3, 2)}")
    
    print("\n\n" + "=" * 80)
    print("TEOREMA: FÓRMULA DE LA SUMA (Demostración por Inducción)")
    print("=" * 80)
    
    theorem = prove_sum_formula()
    print(theorem.show())
    
    print("\n" + "=" * 80)
