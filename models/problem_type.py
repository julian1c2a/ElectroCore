"""
Enum de tipos de problemas soportados en el sistema.
"""
from enum import Enum


class ProblemType(Enum):
    """
    Enum que define todos los tipos de ejercicios soportados.
    
    Cada tipo corresponde a un módulo en modules/ y tiene:
    - Generador (módulos/[tipo]/generators.py)
    - Modelo (módulos/[tipo]/models.py)
    - Mapper (models/mappers/[tipo].py)
    
    Ejemplo:
        type = ProblemType.NUMERACION
        print(type.value)  # "numeracion"
        print(type.label)  # "Representación Numérica"
    """
    
    # NUMERACION: Conversiones entre bases y representaciones
    NUMERACION = "numeracion"
    
    # KARNAUGH: Mapas de Karnaugh y simplificación booleana
    KARNAUGH = "karnaugh"
    
    # LOGIC: Problemas de diseño lógico con contexto real
    LOGIC = "logic"
    
    # MSI: Circuitos Integrados Medianos (MUX, COMPARADOR, SUMADOR)
    MSI = "msi"
    
    # SECUENCIAL: Lógica secuencial (Flip-Flops, Contadores, Registros)
    SECUENCIAL = "secuencial"
    
    @property
    def label(self) -> str:
        """Devuelve el nombre legible del tipo de problema."""
        labels = {
            "numeracion": "Representación Numérica",
            "karnaugh": "Mapas de Karnaugh",
            "logic": "Diseño Lógico",
            "msi": "Circuitos MSI",
            "secuencial": "Lógica Secuencial"
        }
        return labels.get(self.value, "Desconocido")
    
    @classmethod
    def from_string(cls, value: str) -> "ProblemType":
        """
        Convierte un string a ProblemType.
        
        Args:
            value: String del tipo (ej: "numeracion")
        
        Returns:
            ProblemType correspondiente
        
        Raises:
            ValueError: Si el tipo no existe
        
        Ejemplo:
            type = ProblemType.from_string("numeracion")
        """
        for problem_type in cls:
            if problem_type.value == value:
                return problem_type
        raise ValueError(f"Tipo de problema desconocido: {value}. Valores válidos: {[p.value for p in cls]}")
    
    @classmethod
    def all_values(cls) -> list:
        """Devuelve lista de todos los valores válidos."""
        return [p.value for p in cls]
