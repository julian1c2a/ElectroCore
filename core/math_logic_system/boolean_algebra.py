"""
Álgebra de Boole - Postulados de Huntington (1903)

Implementa el sistema axiomático del álgebra de Boole según
los postulados de E.V. Huntington publicados en 1903.

Los postulados de Huntington definen un álgebra de Boole como:
- Un conjunto B con al menos dos elementos
- Dos operaciones binarias: + (OR) y · (AND)
- Propiedades: conmutatividad, identidades, distributividad, complemento

Autor: ElectroCore Project
"""

from typing import List
from ..axioms import AxiomSystem, Postulate, Definition
from ..expressions import *
from ..proof_system import Proof, Theorem, Lemma, ProofLibrary, JustificationType
from ..inference_rules import Substitution, Conjunction


def create_huntington_system() -> AxiomSystem:
    """
    Crea el sistema axiomático del álgebra de Boole según Huntington (1903).
    
    Returns:
        AxiomSystem con los postulados de Huntington
    """
    system = AxiomSystem(
        "Álgebra de Boole (Huntington 1903)",
        "Sistema axiomático del álgebra de Boole basado en los postulados de Huntington"
    )
    
    # Variables para los postulados
    a = Var("a")
    b = Var("b")
    c = Var("c")
    zero = Const(0, "0")
    one = Const(1, "1")
    
    # POSTULADO I: Cierre
    # El sistema es cerrado bajo las operaciones + y ·
    p1_closure = Postulate(
        "P1-Closure",
        Forall("a", Forall("b",
            And(
                Pred("∈", BinOp("+", Var("a"), Var("b"), 4), Var("B")),
                Pred("∈", BinOp("·", Var("a"), Var("b"), 5), Var("B"))
            ),
            Var("B")
        ), Var("B")),
        "Cierre: Si a, b ∈ B, entonces a+b ∈ B y a·b ∈ B",
        {"closure", "binary-operations"}
    )
    system.add_postulate(p1_closure)
    
    # POSTULADO II: Conmutatividad
    # a + b = b + a
    # a · b = b · a
    p2_commutative_add = Postulate(
        "P2a-Commutative-OR",
        Forall("a", Forall("b",
            Equals(
                BinOp("+", Var("a"), Var("b"), 4),
                BinOp("+", Var("b"), Var("a"), 4)
            ),
            Var("B")
        ), Var("B")),
        "Conmutatividad de OR: a + b = b + a",
        {"commutative", "or"}
    )
    system.add_postulate(p2_commutative_add)
    
    p2_commutative_mul = Postulate(
        "P2b-Commutative-AND",
        Forall("a", Forall("b",
            Equals(
                BinOp("·", Var("a"), Var("b"), 5),
                BinOp("·", Var("b"), Var("a"), 5)
            ),
            Var("B")
        ), Var("B")),
        "Conmutatividad de AND: a · b = b · a",
        {"commutative", "and"}
    )
    system.add_postulate(p2_commutative_mul)
    
    # POSTULADO III: Identidades
    # Existe 0 tal que a + 0 = a
    # Existe 1 tal que a · 1 = a
    p3_identity_zero = Postulate(
        "P3a-Identity-Zero",
        Exists("0",
            Forall("a",
                Equals(
                    BinOp("+", Var("a"), Var("0"), 4),
                    Var("a")
                ),
                Var("B")
            ),
            Var("B")
        ),
        "Identidad aditiva: Existe 0 tal que a + 0 = a",
        {"identity", "zero", "or"}
    )
    system.add_postulate(p3_identity_zero)
    
    p3_identity_one = Postulate(
        "P3b-Identity-One",
        Exists("1",
            Forall("a",
                Equals(
                    BinOp("·", Var("a"), Var("1"), 5),
                    Var("a")
                ),
                Var("B")
            ),
            Var("B")
        ),
        "Identidad multiplicativa: Existe 1 tal que a · 1 = a",
        {"identity", "one", "and"}
    )
    system.add_postulate(p3_identity_one)
    
    # POSTULADO IV: Distributividad
    # a + (b · c) = (a + b) · (a + c)
    # a · (b + c) = (a · b) + (a · c)
    p4_distributive_or_over_and = Postulate(
        "P4a-Distributive-OR-over-AND",
        Forall("a", Forall("b", Forall("c",
            Equals(
                BinOp("+", Var("a"), BinOp("·", Var("b"), Var("c"), 5), 4),
                BinOp("·",
                    BinOp("+", Var("a"), Var("b"), 4),
                    BinOp("+", Var("a"), Var("c"), 4),
                    5
                )
            ),
            Var("B")
        ), Var("B")), Var("B")),
        "Distributividad de OR sobre AND: a + (b · c) = (a + b) · (a + c)",
        {"distributive", "or", "and"}
    )
    system.add_postulate(p4_distributive_or_over_and)
    
    p4_distributive_and_over_or = Postulate(
        "P4b-Distributive-AND-over-OR",
        Forall("a", Forall("b", Forall("c",
            Equals(
                BinOp("·", Var("a"), BinOp("+", Var("b"), Var("c"), 4), 5),
                BinOp("+",
                    BinOp("·", Var("a"), Var("b"), 5),
                    BinOp("·", Var("a"), Var("c"), 5),
                    4
                )
            ),
            Var("B")
        ), Var("B")), Var("B")),
        "Distributividad de AND sobre OR: a · (b + c) = (a · b) + (a · c)",
        {"distributive", "and", "or"}
    )
    system.add_postulate(p4_distributive_and_over_or)
    
    # POSTULADO V: Complemento
    # Para todo a, existe a' tal que a + a' = 1 y a · a' = 0
    p5_complement = Postulate(
        "P5-Complement",
        Forall("a",
            Exists("a'",
                And(
                    Equals(
                        BinOp("+", Var("a"), UnOp("'", Var("a")), 4),
                        Const(1, "1")
                    ),
                    Equals(
                        BinOp("·", Var("a"), UnOp("'", Var("a")), 5),
                        Const(0, "0")
                    )
                ),
                Var("B")
            ),
            Var("B")
        ),
        "Complemento: Para todo a existe a' tal que a + a' = 1 y a · a' = 0",
        {"complement"}
    )
    system.add_postulate(p5_complement)
    
    # POSTULADO VI: Existencia de al menos dos elementos distintos
    p6_distinct = Postulate(
        "P6-Distinct-Elements",
        Exists("a", Exists("b",
            NotEquals(Var("a"), Var("b")),
            Var("B")
        ), Var("B")),
        "Existen al menos dos elementos distintos en B",
        {"distinct", "non-trivial"}
    )
    system.add_postulate(p6_distinct)
    
    # Definiciones derivadas
    
    # Definición de NOT (complemento)
    def_not = Definition(
        "NOT",
        "¬a",
        Equals(UnOp("¬", a), UnOp("'", a)),
        "El operador NOT se define como el complemento: ¬a = a'"
    )
    system.add_definition(def_not)
    
    return system


class HuntingtonPostulates:
    """
    Clase auxiliar para trabajar con los postulados de Huntington.
    """
    
    def __init__(self):
        self.system = create_huntington_system()
    
    def get_system(self) -> AxiomSystem:
        """Obtiene el sistema axiomático."""
        return self.system
    
    def show_postulates(self) -> None:
        """Muestra todos los postulados."""
        print(self.system.show_summary())


def derive_boolean_theorems() -> ProofLibrary:
    """
    Deriva teoremas fundamentales del álgebra de Boole
    a partir de los postulados de Huntington.
    
    Returns:
        ProofLibrary con los teoremas derivados
    """
    library = ProofLibrary("Teoremas del Álgebra de Boole")
    system = create_huntington_system()
    
    # ========================================================================
    # TEOREMA 1: Idempotencia
    # a + a = a
    # a · a = a
    # ========================================================================
    
    # Teorema 1a: Idempotencia de OR
    proof_1a = Proof(
        Equals(
            BinOp("+", Var("a"), Var("a"), 4),
            Var("a")
        ),
        "Idempotencia de OR: a + a = a"
    )
    proof_1a.set_axiom_system(system)
    
    # Demostración:
    # a = a + 0                           (P3a: Identidad de 0)
    # a = a + (a · a')                    (P5: a · a' = 0)
    # a = (a + a) · (a + a')              (P4a: Distributividad)
    # a = (a + a) · 1                     (P5: a + a' = 1)
    # a = a + a                           (P3b: Identidad de 1)
    
    proof_1a.add_step(
        Equals(Var("a"), BinOp("+", Var("a"), Const(0, "0"), 4)),
        "Por P3a (Identidad de 0): a = a + 0",
        JustificationType.AXIOM
    )
    
    proof_1a.add_step(
        Equals(
            BinOp("+", Var("a"), Const(0, "0"), 4),
            BinOp("+", Var("a"), BinOp("·", Var("a"), UnOp("'", Var("a")), 5), 4)
        ),
        "Por P5 (Complemento): 0 = a · a'",
        JustificationType.AXIOM
    )
    
    proof_1a.add_step(
        Equals(
            BinOp("+", Var("a"), BinOp("·", Var("a"), UnOp("'", Var("a")), 5), 4),
            BinOp("·",
                BinOp("+", Var("a"), Var("a"), 4),
                BinOp("+", Var("a"), UnOp("'", Var("a")), 4),
                5
            )
        ),
        "Por P4a (Distributividad): a + (a · a') = (a + a) · (a + a')",
        JustificationType.AXIOM
    )
    
    proof_1a.add_step(
        Equals(
            BinOp("+", Var("a"), UnOp("'", Var("a")), 4),
            Const(1, "1")
        ),
        "Por P5 (Complemento): a + a' = 1",
        JustificationType.AXIOM
    )
    
    proof_1a.add_step(
        Equals(
            BinOp("·",
                BinOp("+", Var("a"), Var("a"), 4),
                Const(1, "1"),
                5
            ),
            BinOp("+", Var("a"), Var("a"), 4)
        ),
        "Por P3b (Identidad de 1): (a + a) · 1 = a + a",
        JustificationType.AXIOM
    )
    
    proof_1a.add_step(
        Equals(BinOp("+", Var("a"), Var("a"), 4), Var("a")),
        "Por transitividad de las igualdades anteriores",
        JustificationType.PREVIOUS_STEP,
        [1, 2, 3, 4, 5]
    )
    
    proof_1a.mark_complete()
    
    theorem_1a = Theorem(
        "T1a-Idempotence-OR",
        Equals(BinOp("+", Var("a"), Var("a"), 4), Var("a")),
        proof_1a,
        "Idempotencia de OR: a + a = a",
        {"idempotence", "or"}
    )
    
    library.add_theorem(theorem_1a)
    
    # ========================================================================
    # TEOREMA 2: Absorción
    # a + (a · b) = a
    # a · (a + b) = a
    # ========================================================================
    
    # Se pueden añadir más teoremas siguiendo el mismo patrón...
    
    return library


class BooleanAlgebra:
    """
    Implementación computacional del álgebra de Boole.
    
    Permite evaluar expresiones booleanas y verificar identidades.
    """
    
    def __init__(self):
        self.system = create_huntington_system()
        self.library = None
    
    def get_postulates(self) -> AxiomSystem:
        """Obtiene los postulados de Huntington."""
        return self.system
    
    def derive_theorems(self) -> ProofLibrary:
        """Deriva teoremas del álgebra de Boole."""
        if self.library is None:
            self.library = derive_boolean_theorems()
        return self.library
    
    def show_all(self) -> None:
        """Muestra todos los postulados y teoremas."""
        print(self.system.show_summary())
        print("\n")
        
        if self.library is None:
            self.library = derive_boolean_theorems()
        
        print(self.library.list_all())
    
    def evaluate(self, expr: Expression, values: dict) -> bool:
        """
        Evalúa una expresión booleana con valores concretos.
        
        Args:
            expr: Expresión a evaluar
            values: Diccionario con valores de variables
            
        Returns:
            Resultado de la evaluación
        """
        if isinstance(expr, Variable):
            if expr.name not in values:
                raise ValueError(f"Variable {expr.name} no tiene valor asignado")
            return values[expr.name]
        
        if isinstance(expr, Constant):
            return bool(expr.value)
        
        if isinstance(expr, BinaryOp):
            left_val = self.evaluate(expr.left, values)
            right_val = self.evaluate(expr.right, values)
            
            if expr.operator == "+":  # OR
                return left_val or right_val
            elif expr.operator == "·":  # AND
                return left_val and right_val
            elif expr.operator == "=":  # Equals
                return left_val == right_val
            else:
                raise ValueError(f"Operador desconocido: {expr.operator}")
        
        if isinstance(expr, UnaryOp):
            operand_val = self.evaluate(expr.operand, values)
            
            if expr.operator in ["¬", "'"]:  # NOT
                return not operand_val
            else:
                raise ValueError(f"Operador unario desconocido: {expr.operator}")
        
        raise ValueError(f"Tipo de expresión no soportado: {type(expr)}")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear el sistema de álgebra de Boole
    boolean_algebra = BooleanAlgebra()
    
    # Mostrar los postulados de Huntington
    print("=" * 80)
    print("ÁLGEBRA DE BOOLE - POSTULADOS DE HUNTINGTON (1903)")
    print("=" * 80)
    print()
    
    boolean_algebra.show_all()
    
    # Derivar y mostrar teoremas
    print("\n\n")
    library = boolean_algebra.derive_theorems()
    
    # Mostrar un teorema específico
    theorem = library.get_theorem("T1a-Idempotence-OR")
    if theorem:
        print(theorem.show())
