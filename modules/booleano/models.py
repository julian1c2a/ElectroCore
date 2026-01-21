"""
Modelos de datos para ejercicios de Álgebra Booleana.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class TruthTable:
    """Tabla de verdad para una función booleana."""
    inputs: List[str]  # Nombres de variables de entrada (p.ej., ['A', 'B', 'C'])
    outputs: List[str]  # Nombres de variables de salida
    rows: List[Dict[str, bool]]  # Cada fila es un diccionario {var: valor}


@dataclass
class BooleanFunction:
    """Representación de una función booleana."""
    expression: str  # Expresión algebraica (p.ej., "A·B + A'·C")
    truth_table: TruthTable
    minterms: List[int]  # Índices de minterms
    maxterms: List[int]  # Índices de maxterms
    simplified_form: Optional[str] = None
    dnf: Optional[str] = None  # Forma normal disyuntiva (suma de productos)
    cnf: Optional[str] = None  # Forma normal conjuntiva (producto de sumas)


@dataclass
class KarnaughMap:
    """Mapa de Karnaugh para simplificación booleana."""
    variables: List[str]
    size: int  # 2^n (donde n es número de variables)
    cells: List[List[int]]  # Matriz con los valores
    minterms_grouped: List[List[int]]  # Grupos identificados
    simplified_expression: str


@dataclass
class LogicGate:
    """Definición de una puerta lógica."""
    type: str  # 'AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR'
    inputs: int  # Número de entradas
    truth_table: TruthTable
    logic_equations: List[str]  # Ecuaciones de la puerta
    timing_delay: float  # Retardo en ns


@dataclass
class LogicCircuit:
    """Circuito lógico compuesto de puertas."""
    name: str
    gates: List[LogicGate]
    connections: List[tuple]  # (from_gate, from_pin, to_gate, to_pin)
    inputs: List[str]
    outputs: List[str]
    expression: str


@dataclass
class BooleanPropertiesExercise:
    """Ejercicio sobre propiedades del Álgebra de Boole."""
    title: str
    description: str
    property_name: str  # 'idempotencia', 'complemento', 'absorción', etc.
    expression_problem: str  # Expresión a simplificar
    law_to_apply: str  # Ley específica a aplicar
    solution: str
    steps: List[str]  # Pasos de simplificación
