from dataclasses import dataclass
from typing import List, Set
from core.generator_base import ProblemSolutionExerciseData, ExerciseData

# Mapeo de índices a tipos de representación
COLUMN_NAMES = {
    0: "Binario Natural",
    1: "Complemento a 2",
    2: "Signo-Magnitud",
    3: "BCD"
}

@dataclass
class ConversionRow(ProblemSolutionExerciseData):
    """
    IMPLEMENTACIÓN DE LA INTERFAZ: Separación Problema ↔ Solución.
    
    Hereda de ProblemSolutionExerciseData, que impone:
    - Definir qué campos son del problema
    - Definir qué campos son de la solución
    - Validar que no se solapen
    - Validar que todo campo esté categorizado
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define lo que el alumno debe resolver
    ════════════════════════════════════════════════════════════
    """
    label: str                  # Identificador (ej: 'a)', 'b)', 'c)')
    val_decimal: int            # Valor decimal que debe convertir
    target_col_idx: int         # Columna activa: 0=Binario, 1=C2, 2=SM, 3=BCD
    representable: bool         # ¿Se puede representar en el sistema target?
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    target_val_str: str         # Respuesta esperada ('10011010' o 'NR')
    
    # Soluciones precalculadas para todas las columnas
    sol_bin: str                # Solución en Binario Natural
    sol_c2: str                 # Solución en Complemento a 2
    sol_sm: str                 # Solución en Signo-Magnitud
    sol_bcd: str                # Solución en BCD
    
    @classmethod
    def problem_field_names(cls) -> Set[str]:
        """Define qué campos son del PROBLEMA."""
        return {"label", "val_decimal", "target_col_idx", "representable"}
    
    @classmethod
    def solution_field_names(cls) -> Set[str]:
        """Define qué campos son de la SOLUCIÓN."""
        return {"target_val_str", "sol_bin", "sol_c2", "sol_sm", "sol_bcd"}
    
    def __post_init__(self):
        """Valida separación + validaciones específicas de numeración."""
        super().__post_init__()
        
        if not 0 <= self.target_col_idx < 4:
            raise ValueError(f"target_col_idx debe estar entre 0-3, recibió {self.target_col_idx}")
        
        # Validar consistencia: representable ↔ target_val_str
        if self.representable and self.target_val_str == 'NR':
            raise ValueError(f"Inconsistencia: representable=True pero target_val_str='NR'")
        if not self.representable and self.target_val_str != 'NR':
            raise ValueError(f"Inconsistencia: representable=False pero target_val_str='{self.target_val_str}'")
    
    @property
    def target_system(self) -> str:
        """Devuelve el nombre del sistema de representación target."""
        return COLUMN_NAMES.get(self.target_col_idx, "Desconocido")

@dataclass
class ArithmeticOp(ProblemSolutionExerciseData):
    """
    IMPLEMENTACIÓN DE LA INTERFAZ: Separación Problema ↔ Solución.
    
    Representa una operación aritmética en el ejercicio de numeración.
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define lo que el alumno ve
    ════════════════════════════════════════════════════════════
    """
    op_type: str                # "Suma" o "Resta"
    system: str                 # "Binario Natural" o "Complemento a 2"
    operand1: str               # Etiqueta de la fila (ej: 'a)', 'b)')
    operand2: str               # Etiqueta de la fila
    operator_symbol: str        # "+" o "-"
    
    # Valores decimales de referencia
    val1_dec: int               # Valor decimal del operando 1
    val2_dec: int               # Valor decimal del operando 2
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    result_dec: int             # Resultado en decimal
    result_bin: str             # Resultado en binario (N bits)
    overflow: bool              # ¿Hubo desbordamiento?
    underflow: bool             # ¿Hubo desbordamiento por defecto?
    carry_bits: str             # Bits de acarreo intermedios ('0110')
    
    @classmethod
    def problem_field_names(cls) -> Set[str]:
        """Define qué campos son del PROBLEMA."""
        return {"op_type", "system", "operand1", "operand2", "operator_symbol", "val1_dec", "val2_dec"}
    
    @classmethod
    def solution_field_names(cls) -> Set[str]:
        """Define qué campos son de la SOLUCIÓN."""
        return {"result_dec", "result_bin", "overflow", "underflow", "carry_bits"}

@dataclass
class ConversionExerciseData(ExerciseData):
    n_bits: int
    rows: List[ConversionRow]
    operations: List[ArithmeticOp]
