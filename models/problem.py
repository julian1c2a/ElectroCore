"""
Clase Problem: Representación agnóstica de un ejercicio.

Esta clase es AGNÓSTICA respecto al tipo de problema:
- Puede serializar/deserializar a/desde JSON
- Contiene metadata común a todos los tipos
- Mantiene el JSON específico del tipo en campos separados
- Es la "moneda común" del sistema de persistencia

Ventajas:
- Independiente del tipo específico
- Fácil guardar/cargar de bases de datos
- Versioning automático
- Trazabilidad completa
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4
from models.problem_type import ProblemType


@dataclass
class Problem:
    """
    Representación agnóstica de un ejercicio.
    
    Estructura:
    - metadata: Información común a todos los tipos
    - statement: Enunciado (problema a resolver)
    - solution: Solución (respuesta correcta)
    - generator_params: Parámetros usados para generar el problema
    - original_data: Datos Python originales (si aplica)
    
    Ejemplo JSON guardado en DB:
    {
      "id": "uuid-1234",
      "type": "numeracion",
      "metadata": {
        "title": "Conversión Decimal a Bases",
        "topic": "Representación Numérica",
        "difficulty": 1,
        "tags": ["8bits", "conversión"],
        "created_at": "2026-01-15T10:30:00",
        "version": "1.0"
      },
      "statement": {
        "text": "Convierte 157 a binario...",
        "instructions": "Para cada base realiza...",
        "problem_fields": {
          "label": "a",
          "val_decimal": 157,
          "target_col_idx": 0
        }
      },
      "solution": {
        "explanation": "El 157 se convierte dividiendo...",
        "steps": ["157/2=78 r1", ...],
        "solution_fields": {
          "sol_bin": "10011101",
          "sol_c2": "10011101",
          ...
        }
      },
      "generator_params": {
        "seed": 42,
        "config": {...}
      }
    }
    """
    
    # IDENTIDAD
    id: str = field(default_factory=lambda: str(uuid4()))
    type: ProblemType = field(default=None)
    
    # METADATA (común a todos los tipos)
    @dataclass
    class Metadata:
        """Información común a todos los problemas."""
        title: str                           # "Conversión Decimal a Bases"
        topic: str                           # "Representación Numérica"
        difficulty: int = 1                  # 1-5 (1=fácil, 5=difícil)
        tags: list = field(default_factory=list)  # ["8bits", "conversión", "decimal"]
        created_at: str = field(default_factory=lambda: datetime.now().isoformat())
        updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
        version: str = "1.0"
        author: Optional[str] = None         # Quién creó el problema
        source: Optional[str] = None         # De dónde viene (generador, importado, etc)
    
    metadata: Metadata = field(default_factory=Metadata)
    
    # ENUNCIADO (problema a resolver)
    @dataclass
    class Statement:
        """El problema que el alumno debe resolver."""
        text: str                            # "Convierte 157 a binario..."
        instructions: Optional[str] = None   # "Para cada base realiza..."
        hints: list = field(default_factory=list)  # ["Divide entre 2", "Recuerda el complemento a 2"]
        
        # Campos específicos del tipo (agnósticos)
        problem_fields: Dict[str, Any] = field(default_factory=dict)  # {"label": "a", "val_decimal": 157, ...}
    
    statement: Statement = field(default_factory=Statement)
    
    # SOLUCION (respuesta correcta)
    @dataclass
    class Solution:
        """La solución correcta del problema."""
        explanation: Optional[str] = None    # "El 157 se convierte dividiendo..."
        steps: list = field(default_factory=list)  # ["157/2=78 r1", "78/2=39 r0", ...]
        
        # Campos específicos del tipo (agnósticos)
        solution_fields: Dict[str, Any] = field(default_factory=dict)  # {"sol_bin": "10011101", ...}
    
    solution: Solution = field(default_factory=Solution)
    
    # PARÁMETROS DEL GENERADOR (para reproducibilidad)
    @dataclass
    class GeneratorParams:
        """Información sobre cómo se generó este problema."""
        seed: Optional[int] = None           # Semilla para reproducibilidad
        generator_id: Optional[str] = None   # ID del generador usado
        randomizer_config: Dict[str, Any] = field(default_factory=dict)  # Config específica
    
    generator_params: GeneratorParams = field(default_factory=GeneratorParams)
    
    # DATOS PYTHON ORIGINALES (para compatibilidad)
    original_exercise_data: Optional[Dict[str, Any]] = None  # ExerciseData serializado como dict
    
    # ==================== MÉTODOS ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el Problem a diccionario (para JSON).
        
        Returns:
            Dict serializable a JSON
        """
        data = asdict(self)
        # Convertir enum type a string para que sea serializable
        data['type'] = self.type.value if self.type else None
        return data
    
    def to_json_string(self) -> str:
        """
        Convierte el Problem a JSON string.
        
        Returns:
            String JSON
        """
        import json
        
        # Crear dict pero con enums convertidos a strings
        data = asdict(self)
        data['type'] = self.type.value if self.type else None
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Problem":
        """
        Crea un Problem desde un diccionario.
        
        Args:
            data: Dict con estructura Problem
        
        Returns:
            Problem reconstructido
        """
        # Convertir type string → enum
        if isinstance(data.get('type'), str):
            data['type'] = ProblemType.from_string(data['type'])
        
        # Convertir nested dicts → dataclasses
        if isinstance(data.get('metadata'), dict):
            data['metadata'] = cls.Metadata(**data['metadata'])
        
        if isinstance(data.get('statement'), dict):
            data['statement'] = cls.Statement(**data['statement'])
        
        if isinstance(data.get('solution'), dict):
            data['solution'] = cls.Solution(**data['solution'])
        
        if isinstance(data.get('generator_params'), dict):
            data['generator_params'] = cls.GeneratorParams(**data['generator_params'])
        
        return cls(**data)
    
    @classmethod
    def from_json_string(cls, json_string: str) -> "Problem":
        """
        Crea un Problem desde un JSON string.
        
        Args:
            json_string: String JSON
        
        Returns:
            Problem reconstructido
        """
        import json
        data = json.loads(json_string)
        return cls.from_dict(data)
    
    # ==================== UTILIDADES ====================
    
    def add_tag(self, tag: str) -> None:
        """Agrega un tag al problema."""
        if tag not in self.metadata.tags:
            self.metadata.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remueve un tag del problema."""
        if tag in self.metadata.tags:
            self.metadata.tags.remove(tag)
    
    def set_difficulty(self, difficulty: int) -> None:
        """Establece la dificultad (1-5)."""
        if not 1 <= difficulty <= 5:
            raise ValueError(f"Dificultad debe estar entre 1-5, recibió {difficulty}")
        self.metadata.difficulty = difficulty
    
    def mark_updated(self) -> None:
        """Actualiza el timestamp de última modificación."""
        self.metadata.updated_at = datetime.now().isoformat()
    
    def __repr__(self) -> str:
        """Representación legible del Problem."""
        return (
            f"Problem("
            f"id={self.id[:8]}..., "
            f"type={self.type.value}, "
            f"title={self.metadata.title!r}, "
            f"difficulty={self.metadata.difficulty})"
        )
