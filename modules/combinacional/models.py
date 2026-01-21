from dataclasses import dataclass
from typing import List, Dict, Any
from core.generator_base import ExerciseData

@dataclass
class KarnaughExerciseData(ExerciseData):
    """
    Ejercicio de Mapa de Karnaugh y simplificación booleana.
    Separa explícitamente PARÁMETROS DEL PROBLEMA vs SOLUCIÓN.
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define lo que el alumno ve
    ════════════════════════════════════════════════════════════
    """
    # Variables y estructura
    vars_name: List[str]            # ["A", "B", "C", "D"]
    out_name: str                   # "F" o "Y"
    
    # Tabla de verdad (lo que el alumno ve)
    truth_table_outputs: List[int]  # 16 valores (0 o 1) para 4 variables
    
    # Especificación del problema
    canon_type: str                 # "Minitérminos" o "Maxitérminos"
    gate_type: str                  # "NAND" o "NOR" (restricción del problema)
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    # Mapa de Karnaugh (índices de casillas agrupadas)
    minterms: List[int]             # [1, 3, 4, 6, 8, 10, 12, 14] para minitérminos
    maxterms: List[int]             # [0, 2, 5, 7, 9, 11, 13, 15] para maxitérminos
    
    # Soluciones simplificadas en diferentes formas
    simplified_sop: str             # "F = A'BD + AC'D + ..." (Suma de Productos)
    simplified_pos: str             # "F = (A+B'+C)(A'+B+C)..." (Producto de Sumas)
    simplified_nand: str            # Implementación con puertas NAND
    simplified_nor: str             # Implementación con puertas NOR


@dataclass
class LogicProblemExerciseData(ExerciseData):
    """
    Ejercicio de problema lógico (contexto real → función booleana).
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA
    ════════════════════════════════════════════════════════════
    """
    context_title: str              # "Alarma de temperatura en frigorífico"
    context_description: str        # Descripción del problema
    
    variables_desc: List[str]       # ["T > 5°C", "Puerta abierta", ...]
    output_desc: str                # "Activar alarma"
    logic_description: str          # Descripción de la lógica requerida
    
    # Variables limpias (sin descripción)
    vars_clean: List[str]           # ["T", "P", "A"]
    out_clean: str                  # "S"
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN
    ════════════════════════════════════════════════════════════
    """
    truth_table_outputs: List[int]  # Tabla de verdad correcta
    simplified_solution: str        # "S = T·P + A"


@dataclass
class MSIExerciseData(ExerciseData):
    """
    Ejercicio de Circuitos Integrados Medianos (Multiplexor, Comparador, Sumador).
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA
    ════════════════════════════════════════════════════════════
    """
    block_type: str                 # "MUX", "COMPARADOR", "SUMADOR"
    params: Dict[str, Any]          # Parámetros específicos del circuito
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN
    ════════════════════════════════════════════════════════════
    """
    expected_outputs: List[int]     # Salidas esperadas para las entradas
    truth_table: List[Dict[str, Any]]  # Tabla de verdad completa
