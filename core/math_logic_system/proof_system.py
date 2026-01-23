"""
Sistema de Pruebas Formales

Define la estructura para construir demostraciones formales
completas de teoremas, lemas y corolarios.

Autor: ElectroCore Project
"""

from typing import List, Optional, Set, Dict
from dataclasses import dataclass, field
from enum import Enum
from .expressions import Expression
from .axioms import Axiom, AxiomSystem
from .inference_rules import InferenceRule


class JustificationType(Enum):
    """Tipos de justificación para un paso de prueba."""
    AXIOM = "axiom"
    POSTULATE = "postulate"
    DEFINITION = "definition"
    PREMISE = "premise"
    HYPOTHESIS = "hypothesis"
    INFERENCE = "inference"
    THEOREM = "theorem"
    LEMMA = "lemma"
    PREVIOUS_STEP = "previous_step"


@dataclass
class ProofStep:
    """
    Un paso en una demostración formal.
    
    Atributos:
        statement: La expresión que se establece en este paso
        justification: Texto explicativo de por qué este paso es válido
        justification_type: Tipo de justificación
        depends_on: Números de pasos previos de los que depende
        rule: Regla de inferencia usada (si aplica)
        metadata: Información adicional
    """
    statement: Expression
    justification: str
    justification_type: JustificationType
    depends_on: List[int] = field(default_factory=list)
    rule: Optional[InferenceRule] = None
    metadata: Dict = field(default_factory=dict)
    
    def __str__(self) -> str:
        result = f"  {self.statement}"
        result += f"\n  [Justificación: {self.justification}"
        
        if self.rule:
            result += f", Regla: {self.rule.name()}"
        
        if self.depends_on:
            deps = ", ".join(str(d) for d in self.depends_on)
            result += f", Depende de: pasos {deps}"
        
        result += "]"
        return result


class Proof:
    """
    Demostración formal completa.
    
    Una prueba consta de:
    - Un objetivo (teorema a demostrar)
    - Una secuencia de pasos lógicos
    - Referencias a axiomas y teoremas previos
    """
    
    def __init__(self, goal: Expression, description: str = ""):
        self.goal = goal
        self.description = description
        self.steps: List[ProofStep] = []
        self.premises: List[Expression] = []
        self.hypotheses: List[Expression] = []
        self.axiom_system: Optional[AxiomSystem] = None
        self._complete = False
    
    def set_axiom_system(self, system: AxiomSystem) -> None:
        """Establece el sistema axiomático usado en la prueba."""
        self.axiom_system = system
    
    def add_premise(self, premise: Expression) -> None:
        """Añade una premisa (hipótesis inicial)."""
        self.premises.append(premise)
    
    def add_hypothesis(self, hypothesis: Expression, description: str = "") -> int:
        """
        Añade una hipótesis temporal (para pruebas por contradicción o casos).
        Retorna el número del paso.
        """
        self.hypotheses.append(hypothesis)
        step = ProofStep(
            hypothesis,
            description or "Hipótesis",
            JustificationType.HYPOTHESIS
        )
        self.steps.append(step)
        return len(self.steps)
    
    def add_step(self,
                 statement: Expression,
                 justification: str,
                 justification_type: JustificationType,
                 depends_on: List[int] = None,
                 rule: Optional[InferenceRule] = None) -> int:
        """
        Añade un paso a la demostración.
        Retorna el número del paso (1-indexed).
        """
        step = ProofStep(
            statement,
            justification,
            justification_type,
            depends_on or [],
            rule
        )
        self.steps.append(step)
        return len(self.steps)
    
    def add_axiom_step(self, axiom_name: str) -> int:
        """Añade un paso citando un axioma."""
        if not self.axiom_system:
            raise ValueError("No se ha establecido un sistema axiomático")
        
        axiom = self.axiom_system.get_axiom(axiom_name)
        if not axiom:
            axiom = self.axiom_system.get_postulate(axiom_name)
        
        if not axiom:
            raise ValueError(f"Axioma/Postulado '{axiom_name}' no encontrado")
        
        return self.add_step(
            axiom.statement,
            f"Axioma: {axiom.description}",
            JustificationType.AXIOM
        )
    
    def add_inference_step(self,
                          conclusion: Expression,
                          rule: InferenceRule,
                          depends_on: List[int],
                          description: str = "") -> int:
        """Añade un paso usando una regla de inferencia."""
        justification = description or f"Por {rule.name()}"
        
        return self.add_step(
            conclusion,
            justification,
            JustificationType.INFERENCE,
            depends_on,
            rule
        )
    
    def mark_complete(self) -> None:
        """Marca la prueba como completa."""
        if not self.steps:
            raise ValueError("La prueba no tiene pasos")
        
        last_statement = self.steps[-1].statement
        if last_statement != self.goal:
            raise ValueError(
                f"El último paso no coincide con el objetivo.\n"
                f"Último paso: {last_statement}\n"
                f"Objetivo: {self.goal}"
            )
        
        self._complete = True
    
    def is_complete(self) -> bool:
        """Verifica si la prueba está completa."""
        return self._complete
    
    def show(self, title: str = "DEMOSTRACIÓN") -> str:
        """Genera una representación legible de la prueba."""
        lines = []
        lines.append("=" * 80)
        lines.append(title)
        lines.append("=" * 80)
        
        if self.description:
            lines.append(f"\n{self.description}\n")
        
        lines.append(f"OBJETIVO: {self.goal}\n")
        
        if self.axiom_system:
            lines.append(f"Sistema axiomático: {self.axiom_system.name}\n")
        
        if self.premises:
            lines.append("PREMISAS:")
            for i, premise in enumerate(self.premises, 1):
                lines.append(f"  P{i}: {premise}")
            lines.append("")
        
        lines.append("DEMOSTRACIÓN:\n")
        
        for i, step in enumerate(self.steps, 1):
            lines.append(f"Paso {i}:")
            lines.append(str(step))
            lines.append("")
        
        if self._complete:
            lines.append("□ Q.E.D. (Quod Erat Demonstrandum)")
        else:
            lines.append("⚠ DEMOSTRACIÓN INCOMPLETA")
        
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def __str__(self) -> str:
        status = "completa" if self._complete else "incompleta"
        return f"Proof({self.goal}) [{status}, {len(self.steps)} pasos]"


@dataclass
class Theorem:
    """
    Teorema: Proposición que ha sido demostrada.
    
    Atributos:
        name: Nombre del teorema
        statement: Expresión formal del teorema
        proof: Demostración del teorema
        description: Descripción en lenguaje natural
        tags: Etiquetas para clasificación
    """
    name: str
    statement: Expression
    proof: Proof
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    
    def __str__(self) -> str:
        return f"Theorem[{self.name}]: {self.statement}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def show(self) -> str:
        """Muestra el teorema con su demostración."""
        lines = []
        lines.append("\n" + "█" * 80)
        lines.append(f"█  TEOREMA: {self.name}")
        lines.append("█" * 80)
        lines.append(f"\nEnunciado: {self.statement}")
        if self.description:
            lines.append(f"Descripción: {self.description}")
        lines.append("")
        lines.append(self.proof.show(f"DEMOSTRACIÓN DEL TEOREMA: {self.name}"))
        return "\n".join(lines)


@dataclass
class Lemma:
    """
    Lema: Teorema auxiliar usado para demostrar otros teoremas.
    """
    name: str
    statement: Expression
    proof: Proof
    description: str = ""
    
    def __str__(self) -> str:
        return f"Lemma[{self.name}]: {self.statement}"
    
    def show(self) -> str:
        """Muestra el lema con su demostración."""
        lines = []
        lines.append("\n" + "▓" * 80)
        lines.append(f"▓  LEMA: {self.name}")
        lines.append("▓" * 80)
        lines.append(f"\nEnunciado: {self.statement}")
        if self.description:
            lines.append(f"Descripción: {self.description}")
        lines.append("")
        lines.append(self.proof.show(f"DEMOSTRACIÓN DEL LEMA: {self.name}"))
        return "\n".join(lines)


@dataclass
class Corollary:
    """
    Corolario: Teorema que se deduce fácilmente de otro teorema.
    """
    name: str
    statement: Expression
    from_theorem: str
    proof: Optional[Proof] = None
    description: str = ""
    
    def __str__(self) -> str:
        return f"Corollary[{self.name}] (de {self.from_theorem}): {self.statement}"
    
    def show(self) -> str:
        """Muestra el corolario con su demostración (si existe)."""
        lines = []
        lines.append("\n" + "░" * 80)
        lines.append(f"░  COROLARIO: {self.name}")
        lines.append(f"░  (Consecuencia del teorema: {self.from_theorem})")
        lines.append("░" * 80)
        lines.append(f"\nEnunciado: {self.statement}")
        if self.description:
            lines.append(f"Descripción: {self.description}")
        
        if self.proof:
            lines.append("")
            lines.append(self.proof.show(f"DEMOSTRACIÓN DEL COROLARIO: {self.name}"))
        else:
            lines.append("\n[Demostración trivial desde el teorema]")
        
        return "\n".join(lines)


class ProofLibrary:
    """
    Biblioteca de teoremas demostrados.
    
    Permite almacenar y consultar teoremas, lemas y corolarios.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.theorems: Dict[str, Theorem] = {}
        self.lemmas: Dict[str, Lemma] = {}
        self.corollaries: Dict[str, Corollary] = {}
    
    def add_theorem(self, theorem: Theorem) -> None:
        """Añade un teorema a la biblioteca."""
        if not theorem.proof.is_complete():
            raise ValueError(f"El teorema '{theorem.name}' no tiene una prueba completa")
        self.theorems[theorem.name] = theorem
    
    def add_lemma(self, lemma: Lemma) -> None:
        """Añade un lema a la biblioteca."""
        if not lemma.proof.is_complete():
            raise ValueError(f"El lema '{lemma.name}' no tiene una prueba completa")
        self.lemmas[lemma.name] = lemma
    
    def add_corollary(self, corollary: Corollary) -> None:
        """Añade un corolario a la biblioteca."""
        self.corollaries[corollary.name] = corollary
    
    def get_theorem(self, name: str) -> Optional[Theorem]:
        """Obtiene un teorema por nombre."""
        return self.theorems.get(name)
    
    def get_lemma(self, name: str) -> Optional[Lemma]:
        """Obtiene un lema por nombre."""
        return self.lemmas.get(name)
    
    def get_corollary(self, name: str) -> Optional[Corollary]:
        """Obtiene un corolario por nombre."""
        return self.corollaries.get(name)
    
    def list_all(self) -> str:
        """Lista todos los resultados en la biblioteca."""
        lines = []
        lines.append("=" * 80)
        lines.append(f"BIBLIOTECA DE TEOREMAS: {self.name}")
        lines.append("=" * 80)
        
        if self.theorems:
            lines.append(f"\nTEOREMAS ({len(self.theorems)}):")
            for name, thm in self.theorems.items():
                lines.append(f"  • {name}: {thm.statement}")
        
        if self.lemmas:
            lines.append(f"\nLEMAS ({len(self.lemmas)}):")
            for name, lem in self.lemmas.items():
                lines.append(f"  • {name}: {lem.statement}")
        
        if self.corollaries:
            lines.append(f"\nCOROLARIOS ({len(self.corollaries)}):")
            for name, cor in self.corollaries.items():
                lines.append(f"  • {name}: {cor.statement}")
        
        lines.append("=" * 80)
        return "\n".join(lines)
