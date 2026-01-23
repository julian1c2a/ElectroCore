"""
Sistema de Expresiones Matemáticas

Define la sintaxis para expresiones matemáticas formales incluyendo:
- Variables y constantes
- Operadores binarios y unarios
- Funciones
- Cuantificadores
- Predicados

Autor: ElectroCore Project
"""

from typing import List, Dict, Set, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum


class ExpressionType(Enum):
    """Tipos de expresiones en el sistema."""
    VARIABLE = "var"
    CONSTANT = "const"
    BINARY_OP = "binop"
    UNARY_OP = "unop"
    FUNCTION = "func"
    QUANTIFIER = "quant"
    PREDICATE = "pred"


class Expression(ABC):
    """Clase base para todas las expresiones matemáticas."""
    
    @abstractmethod
    def __str__(self) -> str:
        """Representación en string de la expresión."""
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        """Igualdad estructural de expresiones."""
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        """Hash para usar en conjuntos y diccionarios."""
        pass
    
    @abstractmethod
    def free_variables(self) -> Set[str]:
        """Retorna el conjunto de variables libres."""
        pass
    
    @abstractmethod
    def substitute(self, var: str, expr: 'Expression') -> 'Expression':
        """Sustituye una variable por una expresión."""
        pass
    
    @abstractmethod
    def get_type(self) -> ExpressionType:
        """Retorna el tipo de expresión."""
        pass
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass(frozen=True)
class Variable(Expression):
    """Variable matemática."""
    name: str
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Variable) and self.name == other.name
    
    def __hash__(self) -> int:
        return hash(("var", self.name))
    
    def free_variables(self) -> Set[str]:
        return {self.name}
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        if self.name == var:
            return expr
        return self
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.VARIABLE


@dataclass(frozen=True)
class Constant(Expression):
    """Constante matemática."""
    value: Any
    name: Optional[str] = None
    
    def __str__(self) -> str:
        if self.name:
            return self.name
        return str(self.value)
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Constant) and self.value == other.value
    
    def __hash__(self) -> int:
        return hash(("const", self.value))
    
    def free_variables(self) -> Set[str]:
        return set()
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        return self
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.CONSTANT


@dataclass(frozen=True)
class BinaryOp(Expression):
    """Operador binario."""
    operator: str  # +, -, *, /, ∧, ∨, ⟹, ⟺, =, ≠, <, >, ≤, ≥, etc.
    left: Expression
    right: Expression
    precedence: int = 0
    
    def __str__(self) -> str:
        left_str = str(self.left)
        right_str = str(self.right)
        
        # Añadir paréntesis si es necesario
        if isinstance(self.left, BinaryOp) and self.left.precedence < self.precedence:
            left_str = f"({left_str})"
        if isinstance(self.right, BinaryOp) and self.right.precedence < self.precedence:
            right_str = f"({right_str})"
        
        return f"{left_str} {self.operator} {right_str}"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, BinaryOp) and 
                self.operator == other.operator and
                self.left == other.left and 
                self.right == other.right)
    
    def __hash__(self) -> int:
        return hash(("binop", self.operator, self.left, self.right))
    
    def free_variables(self) -> Set[str]:
        return self.left.free_variables() | self.right.free_variables()
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        return BinaryOp(
            self.operator,
            self.left.substitute(var, expr),
            self.right.substitute(var, expr),
            self.precedence
        )
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.BINARY_OP


@dataclass(frozen=True)
class UnaryOp(Expression):
    """Operador unario."""
    operator: str  # ¬, -, √, etc.
    operand: Expression
    
    def __str__(self) -> str:
        operand_str = str(self.operand)
        if isinstance(self.operand, BinaryOp):
            operand_str = f"({operand_str})"
        
        # Algunos operadores van después
        if self.operator in ["'", "†", "*"]:
            return f"{operand_str}{self.operator}"
        
        return f"{self.operator}{operand_str}"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, UnaryOp) and 
                self.operator == other.operator and
                self.operand == other.operand)
    
    def __hash__(self) -> int:
        return hash(("unop", self.operator, self.operand))
    
    def free_variables(self) -> Set[str]:
        return self.operand.free_variables()
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        return UnaryOp(self.operator, self.operand.substitute(var, expr))
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.UNARY_OP


@dataclass(frozen=True)
class Function(Expression):
    """Aplicación de función."""
    name: str
    arguments: tuple[Expression, ...]
    
    def __init__(self, name: str, *args: Expression):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'arguments', tuple(args))
    
    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Function) and 
                self.name == other.name and
                self.arguments == other.arguments)
    
    def __hash__(self) -> int:
        return hash(("func", self.name, self.arguments))
    
    def free_variables(self) -> Set[str]:
        result = set()
        for arg in self.arguments:
            result |= arg.free_variables()
        return result
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        new_args = [arg.substitute(var, expr) for arg in self.arguments]
        return Function(self.name, *new_args)
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.FUNCTION


@dataclass(frozen=True)
class Quantifier(Expression):
    """Cuantificador (∀ o ∃)."""
    type: str  # "∀" o "∃"
    variable: str
    domain: Optional[Expression]
    body: Expression
    
    def __str__(self) -> str:
        if self.domain:
            return f"{self.type}{self.variable} ∈ {self.domain}: {self.body}"
        return f"{self.type}{self.variable}: {self.body}"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Quantifier) and 
                self.type == other.type and
                self.variable == other.variable and
                self.domain == other.domain and
                self.body == other.body)
    
    def __hash__(self) -> int:
        return hash(("quant", self.type, self.variable, self.domain, self.body))
    
    def free_variables(self) -> Set[str]:
        result = self.body.free_variables() - {self.variable}
        if self.domain:
            result |= self.domain.free_variables()
        return result
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        if var == self.variable:
            # No sustituir variables ligadas
            return self
        
        # Evitar captura de variables
        if self.variable in expr.free_variables():
            # Renombrar variable ligada
            new_var = self._fresh_variable(expr.free_variables() | self.free_variables())
            new_body = self.body.substitute(self.variable, Variable(new_var))
            return Quantifier(
                self.type,
                new_var,
                self.domain.substitute(var, expr) if self.domain else None,
                new_body.substitute(var, expr)
            )
        
        return Quantifier(
            self.type,
            self.variable,
            self.domain.substitute(var, expr) if self.domain else None,
            self.body.substitute(var, expr)
        )
    
    def _fresh_variable(self, used: Set[str]) -> str:
        """Genera una variable fresca no usada."""
        base = self.variable.rstrip("0123456789'")
        i = 1
        while f"{base}{i}" in used or f"{base}'" * i in used:
            i += 1
        return f"{base}{i}"
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.QUANTIFIER


@dataclass(frozen=True)
class Predicate(Expression):
    """Predicado (relación)."""
    name: str
    arguments: tuple[Expression, ...]
    
    def __init__(self, name: str, *args: Expression):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'arguments', tuple(args))
    
    def __str__(self) -> str:
        if len(self.arguments) == 2 and self.name in ["=", "≠", "<", ">", "≤", "≥", "∈", "⊆", "⊂"]:
            return f"{self.arguments[0]} {self.name} {self.arguments[1]}"
        
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Predicate) and 
                self.name == other.name and
                self.arguments == other.arguments)
    
    def __hash__(self) -> int:
        return hash(("pred", self.name, self.arguments))
    
    def free_variables(self) -> Set[str]:
        result = set()
        for arg in self.arguments:
            result |= arg.free_variables()
        return result
    
    def substitute(self, var: str, expr: Expression) -> Expression:
        new_args = [arg.substitute(var, expr) for arg in self.arguments]
        return Predicate(self.name, *new_args)
    
    def get_type(self) -> ExpressionType:
        return ExpressionType.PREDICATE


# Funciones auxiliares para construir expresiones comunes

def Var(name: str) -> Variable:
    """Crea una variable."""
    return Variable(name)

def Const(value: Any, name: Optional[str] = None) -> Constant:
    """Crea una constante."""
    return Constant(value, name)

def BinOp(operator: str, left: Expression, right: Expression, precedence: int = 0) -> BinaryOp:
    """Crea un operador binario."""
    return BinaryOp(operator, left, right, precedence)

def UnOp(operator: str, operand: Expression) -> UnaryOp:
    """Crea un operador unario."""
    return UnaryOp(operator, operand)

def Func(name: str, *args: Expression) -> Function:
    """Crea una función."""
    return Function(name, *args)

def Forall(variable: str, body: Expression, domain: Optional[Expression] = None) -> Quantifier:
    """Crea un cuantificador universal."""
    return Quantifier("∀", variable, domain, body)

def Exists(variable: str, body: Expression, domain: Optional[Expression] = None) -> Quantifier:
    """Crea un cuantificador existencial."""
    return Quantifier("∃", variable, domain, body)

def Pred(name: str, *args: Expression) -> Predicate:
    """Crea un predicado."""
    return Predicate(name, *args)

# Operadores comunes

def Equals(left: Expression, right: Expression) -> Predicate:
    """Igualdad."""
    return Predicate("=", left, right)

def NotEquals(left: Expression, right: Expression) -> Predicate:
    """Desigualdad."""
    return Predicate("≠", left, right)

def And(left: Expression, right: Expression) -> BinaryOp:
    """Conjunción lógica."""
    return BinaryOp("∧", left, right, 2)

def Or(left: Expression, right: Expression) -> BinaryOp:
    """Disyunción lógica."""
    return BinaryOp("∨", left, right, 1)

def Implies(left: Expression, right: Expression) -> BinaryOp:
    """Implicación."""
    return BinaryOp("⟹", left, right, 0)

def Iff(left: Expression, right: Expression) -> BinaryOp:
    """Doble implicación."""
    return BinaryOp("⟺", left, right, 0)

def Not(operand: Expression) -> UnaryOp:
    """Negación."""
    return UnaryOp("¬", operand)

def Add(left: Expression, right: Expression) -> BinaryOp:
    """Suma."""
    return BinaryOp("+", left, right, 4)

def Mul(left: Expression, right: Expression) -> BinaryOp:
    """Multiplicación."""
    return BinaryOp("·", left, right, 5)

def LessEq(left: Expression, right: Expression) -> Predicate:
    """Menor o igual."""
    return Predicate("≤", left, right)

def GreaterEq(left: Expression, right: Expression) -> Predicate:
    """Mayor o igual."""
    return Predicate("≥", left, right)
