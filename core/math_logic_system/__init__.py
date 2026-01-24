"""
Sistema de Lógica Matemática y Demostración Formal

Este módulo proporciona un sistema completo para:
- Definir axiomas y postulados
- Crear reglas de inferencia
- Construir demostraciones formales
- Verificar la validez de teoremas
- Derivar teoremas desde axiomas

Puede usarse para demostrar propiedades en:
- Álgebra de Boole (postulados de Huntington 1903)
- Teoría de conjuntos
- Teoría de números
- Espacios métricos
- Y cualquier sistema axiomático formal

Autor: ElectroCore Project
Fecha: Enero 2026
"""

from .expressions import (
    Expression, Variable, Constant, BinaryOp, UnaryOp,
    Function, Quantifier, Predicate,
    # Helper functions
    Var, Const, Func, Pred,
    And, Or, Not, Implies, Iff, Equals, NotEquals,
    Forall, Exists,
    Add, Mul, BinOp, UnOp, LessEq, GreaterEq
)

from .axioms import (
    Axiom, AxiomSystem, Postulate, Definition
)

from .inference_rules import (
    InferenceRule, ModusPonens, ModusTollens, Substitution,
    UniversalInstantiation, ExistentialGeneralization,
    Conjunction, Disjunction, Hypothetical,
    MathematicalInduction, StrongInduction, StructuralInduction
)

from .proof_system import (
    ProofStep, Proof, Theorem, Lemma, Corollary, JustificationType
)

from .verification import (
    ProofVerifier, ExpressionMatcher, Unifier
)

from .boolean_algebra import (
    BooleanAlgebra, HuntingtonPostulates,
    derive_boolean_theorems
)

from .natural_numbers import (
    PeanoArithmetic, create_peano_axioms
)

__all__ = [
    # Expresiones
    'Expression', 'Variable', 'Constant', 'BinaryOp', 'UnaryOp',
    'Function', 'Quantifier', 'Predicate',
    # Helper functions para expresiones
    'Var', 'Const', 'Func', 'Pred',
    'And', 'Or', 'Not', 'Implies', 'Iff', 'Equals', 'NotEquals',
    'Forall', 'Exists', 'Add', 'Mul', 'BinOp', 'UnOp', 'LessEq', 'GreaterEq',
    
    # Axiomas
    'Axiom', 'AxiomSystem', 'Postulate', 'Definition',
    
    # Reglas de inferencia
    'InferenceRule', 'ModusPonens', 'ModusTollens', 'Substitution',
    'UniversalInstantiation', 'ExistentialGeneralization',
    'Conjunction', 'Disjunction', 'Hypothetical',
    'MathematicalInduction', 'StrongInduction', 'StructuralInduction',
    
    # Sistema de pruebas
    'ProofStep', 'Proof', 'Theorem', 'Lemma', 'Corollary', 'JustificationType',
    
    # Verificación
    'ProofVerifier', 'ExpressionMatcher', 'Unifier',
    
    # Álgebra de Boole
    'BooleanAlgebra', 'HuntingtonPostulates', 'derive_boolean_theorems',
    
    # Números Naturales
    'PeanoArithmetic', 'create_peano_axioms'
]

__version__ = '1.0.0'
