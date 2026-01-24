"""
Reglas de Inferencia

Define las reglas lógicas que permiten derivar nuevas
proposiciones a partir de otras ya establecidas.

Autor: ElectroCore Project
"""

from typing import List, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .expressions import Expression, BinaryOp, UnaryOp, Quantifier, Variable


class InferenceRule(ABC):
    """Clase base para reglas de inferencia."""
    
    @abstractmethod
    def apply(self, *premises: Expression) -> Optional[Expression]:
        """
        Aplica la regla de inferencia a las premisas dadas.
        Retorna la conclusión si la regla es aplicable, None en caso contrario.
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Nombre de la regla."""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Descripción de la regla."""
        pass
    
    def __str__(self) -> str:
        return f"{self.name()}: {self.description()}"


class ModusPonens(InferenceRule):
    """
    Modus Ponens: De P y P ⟹ Q, derivar Q.
    """
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 2:
            return None
        
        p, implication = premises
        
        # Verificar que la segunda premisa es una implicación
        if not isinstance(implication, BinaryOp) or implication.operator != "⟹":
            return None
        
        # Verificar que P coincide con el antecedente
        if p == implication.left:
            return implication.right
        
        return None
    
    def name(self) -> str:
        return "Modus Ponens"
    
    def description(self) -> str:
        return "De P y P ⟹ Q, derivar Q"


class ModusTollens(InferenceRule):
    """
    Modus Tollens: De ¬Q y P ⟹ Q, derivar ¬P.
    """
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 2:
            return None
        
        not_q, implication = premises
        
        # Verificar que la primera premisa es una negación
        if not isinstance(not_q, UnaryOp) or not_q.operator != "¬":
            return None
        
        # Verificar que la segunda premisa es una implicación
        if not isinstance(implication, BinaryOp) or implication.operator != "⟹":
            return None
        
        # Verificar que ¬Q coincide con la negación del consecuente
        if not_q.operand == implication.right:
            return UnaryOp("¬", implication.left)
        
        return None
    
    def name(self) -> str:
        return "Modus Tollens"
    
    def description(self) -> str:
        return "De ¬Q y P ⟹ Q, derivar ¬P"


class Substitution(InferenceRule):
    """
    Sustitución: Reemplazar una variable por una expresión.
    """
    
    def __init__(self, var: str, replacement: Expression):
        self.var = var
        self.replacement = replacement
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        return premises[0].substitute(self.var, self.replacement)
    
    def name(self) -> str:
        return "Substitution"
    
    def description(self) -> str:
        return f"Sustituir {self.var} por {self.replacement}"


class UniversalInstantiation(InferenceRule):
    """
    Instanciación Universal: De ∀x: P(x), derivar P(t) para cualquier término t.
    """
    
    def __init__(self, term: Expression):
        self.term = term
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        premise = premises[0]
        
        # Verificar que la premisa es un cuantificador universal
        if not isinstance(premise, Quantifier) or premise.type != "∀":
            return None
        
        # Sustituir la variable cuantificada por el término
        return premise.body.substitute(premise.variable, self.term)
    
    def name(self) -> str:
        return "Universal Instantiation"
    
    def description(self) -> str:
        return f"De ∀x: P(x), derivar P({self.term})"


class ExistentialGeneralization(InferenceRule):
    """
    Generalización Existencial: De P(t), derivar ∃x: P(x).
    """
    
    def __init__(self, term: Expression, var: str):
        self.term = term
        self.var = var
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        premise = premises[0]
        
        # Reemplazar el término por la variable en la premisa
        generalized = premise.substitute(str(self.term), Variable(self.var))
        
        return Quantifier("∃", self.var, None, generalized)
    
    def name(self) -> str:
        return "Existential Generalization"
    
    def description(self) -> str:
        return f"De P({self.term}), derivar ∃{self.var}: P({self.var})"


class Conjunction(InferenceRule):
    """
    Introducción de Conjunción: De P y Q, derivar P ∧ Q.
    """
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 2:
            return None
        
        p, q = premises
        return BinaryOp("∧", p, q, 2)
    
    def name(self) -> str:
        return "Conjunction Introduction"
    
    def description(self) -> str:
        return "De P y Q, derivar P ∧ Q"


class Disjunction(InferenceRule):
    """
    Introducción de Disyunción: De P, derivar P ∨ Q para cualquier Q.
    """
    
    def __init__(self, q: Expression):
        self.q = q
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        p = premises[0]
        return BinaryOp("∨", p, self.q, 1)
    
    def name(self) -> str:
        return "Disjunction Introduction"
    
    def description(self) -> str:
        return f"De P, derivar P ∨ {self.q}"


class Hypothetical(InferenceRule):
    """
    Silogismo Hipotético: De P ⟹ Q y Q ⟹ R, derivar P ⟹ R.
    """
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 2:
            return None
        
        impl1, impl2 = premises
        
        # Verificar que ambas son implicaciones
        if (not isinstance(impl1, BinaryOp) or impl1.operator != "⟹" or
            not isinstance(impl2, BinaryOp) or impl2.operator != "⟹"):
            return None
        
        # Verificar que el consecuente de la primera coincide con el antecedente de la segunda
        if impl1.right == impl2.left:
            return BinaryOp("⟹", impl1.left, impl2.right, 0)
        
        return None
    
    def name(self) -> str:
        return "Hypothetical Syllogism"
    
    def description(self) -> str:
        return "De P ⟹ Q y Q ⟹ R, derivar P ⟹ R"


class ConjunctionElimination(InferenceRule):
    """
    Eliminación de Conjunción: De P ∧ Q, derivar P (o Q).
    """
    
    def __init__(self, left: bool = True):
        self.left = left
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        premise = premises[0]
        
        if not isinstance(premise, BinaryOp) or premise.operator != "∧":
            return None
        
        return premise.left if self.left else premise.right
    
    def name(self) -> str:
        side = "izquierda" if self.left else "derecha"
        return f"Conjunction Elimination ({side})"
    
    def description(self) -> str:
        side = "P" if self.left else "Q"
        return f"De P ∧ Q, derivar {side}"


class DoubleNegation(InferenceRule):
    """
    Doble Negación: De ¬¬P, derivar P (y viceversa).
    """
    
    def __init__(self, eliminate: bool = True):
        self.eliminate = eliminate
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        if len(premises) != 1:
            return None
        
        premise = premises[0]
        
        if self.eliminate:
            # Eliminar doble negación: ¬¬P → P
            if (isinstance(premise, UnaryOp) and premise.operator == "¬" and
                isinstance(premise.operand, UnaryOp) and premise.operand.operator == "¬"):
                return premise.operand.operand
        else:
            # Introducir doble negación: P → ¬¬P
            return UnaryOp("¬", UnaryOp("¬", premise))
        
        return None
    
    def name(self) -> str:
        return "Double Negation"
    
    def description(self) -> str:
        if self.eliminate:
            return "De ¬¬P, derivar P"
        return "De P, derivar ¬¬P"


class MathematicalInduction(InferenceRule):
    """
    Inducción Matemática sobre ℕ:
    De P(0) y ∀n: P(n) ⟹ P(S(n)), derivar ∀n: P(n)
    
    Donde S(n) es el sucesor de n.
    """
    
    def __init__(self, variable: str = "n", predicate_name: str = "P"):
        self.variable = variable
        self.predicate_name = predicate_name
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        """
        Espera dos premisas:
        1. P(0) - Caso base
        2. ∀n: P(n) ⟹ P(S(n)) - Paso inductivo
        
        Retorna: ∀n: P(n)
        """
        if len(premises) != 2:
            return None
        
        base_case = premises[0]
        inductive_step = premises[1]
        
        # Verificar que el paso inductivo es un cuantificador universal
        if not isinstance(inductive_step, Quantifier) or inductive_step.type != "∀":
            return None
        
        # Verificar que el cuerpo del paso inductivo es una implicación
        if not isinstance(inductive_step.body, BinaryOp) or inductive_step.body.operator != "⟹":
            return None
        
        # El resultado es ∀n: P(n)
        # Extraemos P(n) del antecedente del paso inductivo
        p_n = inductive_step.body.left
        
        return Quantifier("∀", self.variable, None, p_n)
    
    def name(self) -> str:
        return "Mathematical Induction"
    
    def description(self) -> str:
        return f"De P(0) y ∀{self.variable}: P({self.variable}) ⟹ P(S({self.variable})), derivar ∀{self.variable}: P({self.variable})"


class StrongInduction(InferenceRule):
    """
    Inducción Fuerte (Completa) sobre ℕ:
    De ∀n: (∀k<n: P(k)) ⟹ P(n), derivar ∀n: P(n)
    
    Esta es una forma más fuerte de inducción donde asumimos que
    P(k) es verdadera para todos los k < n, no solo para n-1.
    """
    
    def __init__(self, variable: str = "n", predicate_name: str = "P"):
        self.variable = variable
        self.predicate_name = predicate_name
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        """
        Espera una premisa:
        ∀n: (∀k<n: P(k)) ⟹ P(n)
        
        Retorna: ∀n: P(n)
        """
        if len(premises) != 1:
            return None
        
        premise = premises[0]
        
        # Verificar que es un cuantificador universal
        if not isinstance(premise, Quantifier) or premise.type != "∀":
            return None
        
        # Verificar que el cuerpo es una implicación
        if not isinstance(premise.body, BinaryOp) or premise.body.operator != "⟹":
            return None
        
        # El consecuente es P(n)
        p_n = premise.body.right
        
        return Quantifier("∀", self.variable, None, p_n)
    
    def name(self) -> str:
        return "Strong Induction"
    
    def description(self) -> str:
        return f"De ∀{self.variable}: (∀k<{self.variable}: P(k)) ⟹ P({self.variable}), derivar ∀{self.variable}: P({self.variable})"


class StructuralInduction(InferenceRule):
    """
    Inducción Estructural:
    Generalización de la inducción para estructuras recursivas
    (listas, árboles, expresiones, etc.)
    
    De P(base) y ∀x: P(x) ⟹ P(constructor(x)), derivar ∀x: P(x)
    """
    
    def __init__(self, variable: str = "x", predicate_name: str = "P"):
        self.variable = variable
        self.predicate_name = predicate_name
    
    def apply(self, *premises: Expression) -> Optional[Expression]:
        """
        Espera al menos dos premisas:
        1. P(base_1), P(base_2), ... - Casos base
        n. ∀x: P(x) ⟹ P(constructor(x)) - Casos recursivos
        
        Retorna: ∀x: P(x)
        """
        if len(premises) < 2:
            return None
        
        # La última premisa debería ser el caso inductivo
        inductive_case = premises[-1]
        
        # Verificar que es un cuantificador universal con implicación
        if not isinstance(inductive_case, Quantifier) or inductive_case.type != "∀":
            return None
        
        if not isinstance(inductive_case.body, BinaryOp) or inductive_case.body.operator != "⟹":
            return None
        
        # El consecuente es P(constructor(x))
        # Extraemos P(x) del antecedente
        p_x = inductive_case.body.left
        
        return Quantifier("∀", self.variable, None, p_x)
    
    def name(self) -> str:
        return "Structural Induction"
    
    def description(self) -> str:
        return f"De casos base y ∀{self.variable}: P({self.variable}) ⟹ P(constructor({self.variable})), derivar ∀{self.variable}: P({self.variable})"
