"""
Sistema de Axiomas y Postulados

Define axiomas, postulados y definiciones que forman la base
de un sistema axiomático formal.

Autor: ElectroCore Project
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field
from .expressions import Expression


@dataclass
class Axiom:
    """
    Axioma: Proposición aceptada como verdadera sin demostración.
    
    Atributos:
        name: Nombre del axioma
        statement: Expresión formal del axioma
        description: Descripción en lenguaje natural
        tags: Etiquetas para clasificación
    """
    name: str
    statement: Expression
    description: str
    tags: Set[str] = field(default_factory=set)
    
    def __str__(self) -> str:
        return f"Axiom[{self.name}]: {self.statement}"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Postulate(Axiom):
    """
    Postulado: Tipo específico de axioma.
    
    En matemáticas clásicas, axiomas y postulados son equivalentes,
    pero históricamente los postulados se usaban más en geometría.
    """
    pass


@dataclass
class Definition:
    """
    Definición: Introduce nuevos términos o símbolos.
    
    Atributos:
        name: Nombre de lo que se define
        symbol: Símbolo o notación
        statement: Expresión formal de la definición
        description: Descripción en lenguaje natural
    """
    name: str
    symbol: str
    statement: Expression
    description: str
    
    def __str__(self) -> str:
        return f"Definition[{self.name}] ({self.symbol}): {self.statement}"
    
    def __repr__(self) -> str:
        return self.__str__()


class AxiomSystem:
    """
    Sistema axiomático completo.
    
    Contiene axiomas, postulados, definiciones y permite
    derivar teoremas a partir de ellos.
    """
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.axioms: Dict[str, Axiom] = {}
        self.postulates: Dict[str, Postulate] = {}
        self.definitions: Dict[str, Definition] = {}
        self.tags_index: Dict[str, Set[str]] = {}
    
    def add_axiom(self, axiom: Axiom) -> None:
        """Añade un axioma al sistema."""
        self.axioms[axiom.name] = axiom
        for tag in axiom.tags:
            if tag not in self.tags_index:
                self.tags_index[tag] = set()
            self.tags_index[tag].add(axiom.name)
    
    def add_postulate(self, postulate: Postulate) -> None:
        """Añade un postulado al sistema."""
        self.postulates[postulate.name] = postulate
        for tag in postulate.tags:
            if tag not in self.tags_index:
                self.tags_index[tag] = set()
            self.tags_index[tag].add(postulate.name)
    
    def add_definition(self, definition: Definition) -> None:
        """Añade una definición al sistema."""
        self.definitions[definition.name] = definition
    
    def get_axiom(self, name: str) -> Optional[Axiom]:
        """Obtiene un axioma por nombre."""
        return self.axioms.get(name)
    
    def get_postulate(self, name: str) -> Optional[Postulate]:
        """Obtiene un postulado por nombre."""
        return self.postulates.get(name)
    
    def get_definition(self, name: str) -> Optional[Definition]:
        """Obtiene una definición por nombre."""
        return self.definitions.get(name)
    
    def get_by_tag(self, tag: str) -> List[Axiom]:
        """Obtiene todos los axiomas/postulados con una etiqueta."""
        if tag not in self.tags_index:
            return []
        
        result = []
        for name in self.tags_index[tag]:
            if name in self.axioms:
                result.append(self.axioms[name])
            elif name in self.postulates:
                result.append(self.postulates[name])
        return result
    
    def list_axioms(self) -> List[Axiom]:
        """Lista todos los axiomas."""
        return list(self.axioms.values())
    
    def list_postulates(self) -> List[Postulate]:
        """Lista todos los postulados."""
        return list(self.postulates.values())
    
    def list_definitions(self) -> List[Definition]:
        """Lista todas las definiciones."""
        return list(self.definitions.values())
    
    def show_summary(self) -> str:
        """Muestra un resumen del sistema axiomático."""
        lines = []
        lines.append("=" * 80)
        lines.append(f"Sistema Axiomático: {self.name}")
        if self.description:
            lines.append(f"Descripción: {self.description}")
        lines.append("=" * 80)
        lines.append(f"\nTotal de axiomas: {len(self.axioms)}")
        lines.append(f"Total de postulados: {len(self.postulates)}")
        lines.append(f"Total de definiciones: {len(self.definitions)}")
        
        if self.axioms:
            lines.append("\n--- AXIOMAS ---")
            for axiom in self.axioms.values():
                lines.append(f"\n{axiom.name}:")
                lines.append(f"  {axiom.statement}")
                if axiom.description:
                    lines.append(f"  ({axiom.description})")
        
        if self.postulates:
            lines.append("\n--- POSTULADOS ---")
            for postulate in self.postulates.values():
                lines.append(f"\n{postulate.name}:")
                lines.append(f"  {postulate.statement}")
                if postulate.description:
                    lines.append(f"  ({postulate.description})")
        
        if self.definitions:
            lines.append("\n--- DEFINICIONES ---")
            for definition in self.definitions.values():
                lines.append(f"\n{definition.name} ({definition.symbol}):")
                lines.append(f"  {definition.statement}")
                if definition.description:
                    lines.append(f"  ({definition.description})")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return f"AxiomSystem[{self.name}]: {len(self.axioms)} axioms, {len(self.postulates)} postulates"
    
    def __repr__(self) -> str:
        return self.__str__()
