from dataclasses import dataclass
from typing import List
from core.generator_base import ExerciseData

@dataclass
class SequentialExerciseData(ExerciseData):
    """
    Ejercicio de Lógica Secuencial (Flip-Flops, Contadores, Registros).
    Separa explícitamente PARÁMETROS DEL PROBLEMA vs SOLUCIÓN.
    
    ════════════════════════════════════════════════════════════
    PARÁMETROS DEL PROBLEMA - Define lo que el alumno ve
    ════════════════════════════════════════════════════════════
    """
    # Descripción del circuito
    title: str                      # "Contador asincrónico JK"
    description: str                # Descripción del problema
    
    # Componentes del circuito
    ff_type: str                    # "JK", "D", "T", "RS"
    edge_type: str                  # "Subida" o "Bajada"
    logic_type: str                 # "SHIFT", "COUNTER", "FSM"
    
    # Entradas asincrónicas
    has_async: bool                 # ¿Tiene Clear/Preset?
    async_type: str                 # "Preset" o "Clear"
    async_level: str                # "0" o "1" (nivel activo)
    
    # Secuencias de entrada (lo que el alumno ve)
    total_cycles: int               # Número de ciclos a simular
    clk_sequence: str               # "0101010101..." (reloj)
    async_sequence: str             # "0000011000..." (entrada asincrónica)
    input_sequence: str             # "1010101010..." (J/K, D, T, R/S)
    
    """
    ════════════════════════════════════════════════════════════
    PARÁMETROS DE LA SOLUCIÓN - Necesarios para calificar
    ════════════════════════════════════════════════════════════
    """
    # Salidas calculadas por simulación
    output_sequence: str            # "1010101010..." (Q en cada ciclo)
    output_bar_sequence: str        # "0101010101..." (Q' en cada ciclo)
    
    # Tabla de transiciones de estado
    state_transitions: List[dict]   # [{"t": 0, "J": 1, "K": 0, "Q": 0, "Q_bar": 1}, ...]
    
    # Timing y validaciones
    setup_time_violations: List[str]  # [] o ["Setup violated at t=5"]
    hold_time_violations: List[str]   # [] o ["Hold violated at t=3"]
    
    # Placeholder para que los alumnos escriban
    output_placeholder: str         # Campo visualizado en enunciado (vacío)
