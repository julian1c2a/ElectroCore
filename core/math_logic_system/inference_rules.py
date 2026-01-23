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
