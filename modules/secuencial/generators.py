"""
Generadores de ejercicios para Sistemas Secuenciales.
Incluye generadores heredados del proyecto y los nuevos.
"""

import random
from typing import Dict, Any, List
from core.generator_base import ExerciseGenerator
from modules.secuencial.models import SequentialExerciseData


class SequentialGenerator(ExerciseGenerator):
    """GENERADOR HEREDADO: Mantiene compatibilidad hacia atrás."""
    
    def topic(self) -> str:
        return "Sistemas Secuenciales"

    def generate(self, difficulty: int = 1) -> SequentialExerciseData:
        # 1. Configuración del Circuito
        ff_type = random.choice(['JK', 'T']) # Simplificado a JK y T como en el renderer
        edge_type = random.choice(['Subida', 'Bajada'])
        logic_type = random.choice(['COUNTER', 'SHIFT'])
        
        has_async = random.choice([True, False])
        async_type = 'Set' if random.random() < 0.5 else 'Reset'
        
        # 2. Generación de Secuencias
        num_cycles = 12
        width_units = num_cycles * 2 # 24 unidades de tiempo
        
        # Generación de Entrada E (Estable por ciclo)
        # Para evitar condiciones de carrera, la entrada cambia solo entre ciclos completos.
        # Esto asegura setup/hold time suficiente para flancos de subida o bajada.
        input_seq_chars = []
        for _ in range(num_cycles):
            val = random.choice(['L', 'H'])
            input_seq_chars.append(val) # Primera mitad del ciclo
            input_seq_chars.append(val) # Segunda mitad del ciclo
            
        input_sequence = "".join(input_seq_chars)
        
        # Generación de Asíncrona (Set/Reset)
        async_sequence = ""
        if has_async:
            # Activo a nivel bajo (0) según enunciado del renderer
            # Generamos un pulso activo (L) en algún momento
            pulse_start = random.randint(2, 6) # Empezar un poco después del inicio
            pulse_len = 2 # Duración del pulso (1 ciclo completo)
            
            pre_h = pulse_start
            post_h = width_units - pre_h - pulse_len
            
            # Formato RLE para tikz-timing: "4H 2L 18H"
            async_sequence = f"{pre_h}H {pulse_len}L {post_h}H"

        return SequentialExerciseData(
            title="Sistemas Secuenciales",
            description=f"Síncrono ({logic_type}) por {edge_type}. FF {ff_type}. Async \\textbf{{{async_type}(asyn)}} a nivel 0.",
            ff_type=ff_type,
            edge_type=edge_type,
            logic_type=logic_type,
            async_set=has_async,
            async_type=async_type,
            input_sequence=input_sequence,
            async_sequence=async_sequence
        )


# ============================================================================
# NUEVOS GENERADORES: Secuencial Extendido
# ============================================================================


class FlipFlopExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Latches y Flip-Flops (elementos básicos de memoria).
    SR, JK, D, T con análisis de transiciones y restricciones temporales.
    """
    
    FLIPFLOPS = {
        'SR_Latch': {
            'description': 'SR Latch (Flip-Flop Set-Reset)',
            'inputs': ['S', 'R'],
            'truth_table': {
                (0, 0): 'Mantiene estado',
                (0, 1): 'Q=0 (Reset)',
                (1, 0): 'Q=1 (Set)',
                (1, 1): 'Indeterminado'
            }
        },
        'JK_FlipFlop': {
            'description': 'JK Flip-Flop (con sincronización de reloj)',
            'inputs': ['J', 'K', 'CLK'],
            'truth_table': {
                (0, 0): 'Mantiene Q',
                (0, 1): 'Q=0 (Clear)',
                (1, 0): 'Q=1 (Set)',
                (1, 1): 'Toggle (invierte Q)'
            }
        },
        'D_FlipFlop': {
            'description': 'D Flip-Flop (captura entrada en flancos)',
            'inputs': ['D', 'CLK'],
            'truth_table': {
                (0, '↑'): 'Q=0',
                (1, '↑'): 'Q=1'
            }
        },
        'T_FlipFlop': {
            'description': 'T Flip-Flop (Toggle)',
            'inputs': ['T', 'CLK'],
            'truth_table': {
                (0, '↑'): 'Mantiene Q',
                (1, '↑'): 'Q=NOT(Q)'
            }
        }
    }
    
    def topic(self) -> str:
        return "Elementos Básicos (Latches y Flip-Flops)"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre flip-flops."""
        flipflop_type = problem_dict.get('flipflop_type', random.choice(list(self.FLIPFLOPS.keys())))
        exercise_type = problem_dict.get('exercise_type', random.choice(['truth_table', 'transition', 'output']))
        
        ff_info = self.FLIPFLOPS[flipflop_type]
        
        if exercise_type == 'truth_table':
            problem_text = f"Construye la tabla de verdad del {ff_info['description']}"
            solution = "Ver tabla en hoja de soluciones"
        
        elif exercise_type == 'transition':
            # Análisis de transición de estado
            current_state = problem_dict.get('current_state', random.randint(0, 1))
            if flipflop_type == 'SR_Latch':
                S = problem_dict.get('S', random.randint(0, 1))
                R = problem_dict.get('R', random.randint(0, 1))
                if S == 1 and R == 0:
                    next_state = 1
                elif S == 0 and R == 1:
                    next_state = 0
                else:
                    next_state = current_state
                
                problem_text = f"{flipflop_type}: Estado actual Q={current_state}, S={S}, R={R}. ¿Próximo estado?"
            else:
                problem_text = f"{flipflop_type}: Analiza la transición de estado"
                next_state = 1 - current_state  # Toggle como ejemplo
            
            solution = str(next_state)
        
        else:  # output
            problem_text = f"¿Cuál es la salida del {flipflop_type} para las entradas dadas?"
            solution = "Consultar tabla de verdad del dispositivo"
        
        return {
            'title': 'Flip-Flops y Latches',
            'problem': problem_text,
            'solution': solution,
            'flipflop_type': flipflop_type,
            'exercise_type': exercise_type
        }


class SequentialSystemsExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Sistemas secuenciales principales.
    Contadores, registros de desplazamiento, memorias.
    """
    
    def topic(self) -> str:
        return "Sistemas Secuenciales Principales"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre sistemas secuenciales."""
        system_type = problem_dict.get('system_type', random.choice(['counter', 'shift_register', 'memory']))
        
        if system_type == 'counter':
            # Contador (binario ascendente)
            counter_size = problem_dict.get('counter_size', random.choice([4, 8]))
            max_count = 2**counter_size - 1
            
            current_count = problem_dict.get('current_count', random.randint(0, max_count-1))
            next_count = (current_count + 1) % (max_count + 1)
            
            problem_text = f"Contador de {counter_size} bits en estado {current_count}. ¿Próximo estado?"
            solution = f"{next_count} (en binario: {format(next_count, f'0{counter_size}b')})"
        
        elif system_type == 'shift_register':
            # Registro de desplazamiento
            register_size = problem_dict.get('register_size', random.choice([4, 8]))
            direction = problem_dict.get('direction', random.choice(['left', 'right']))
            
            state = problem_dict.get('state', format(random.randint(0, 2**register_size - 1), f'0{register_size}b'))
            new_bit = problem_dict.get('new_bit', random.randint(0, 1))
            
            if direction == 'left':
                new_state = state[1:] + str(new_bit)
                direction_name = "izquierda"
            else:
                new_state = str(new_bit) + state[:-1]
                direction_name = "derecha"
            
            problem_text = f"Registro de desplazamiento hacia la {direction_name}: {state} con entrada {new_bit}"
            solution = f"Nuevo estado: {new_state}"
        
        else:  # memory
            address = problem_dict.get('address', random.randint(0, 15))
            data = problem_dict.get('data', format(random.randint(0, 255), '08b'))
            
            problem_text = f"Escribe {data} en la dirección {address} de memoria. ¿Confirmación?"
            solution = f"Dato almacenado en posición {address}: {data}"
        
        return {
            'title': 'Sistemas Secuenciales Principales',
            'problem': problem_text,
            'solution': solution,
            'system_type': system_type
        }


class FSMExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Máquinas de Estados Finitos (FSM).
    Diagramas de estado, transiciones, detección de secuencias.
    """
    
    def topic(self) -> str:
        return "Máquinas de Estados Finitos"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre FSM."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['state_diagram', 'transitions', 'sequence_detection']))
        
        if exercise_type == 'state_diagram':
            n_states = problem_dict.get('n_states', random.choice([3, 4, 5]))
            problem_text = f"Dibuja el diagrama de estados para una máquina con {n_states} estados"
            solution = "Consultar diagrama en hoja de soluciones"
        
        elif exercise_type == 'transitions':
            current_state = problem_dict.get('current_state', 'S0')
            input_signal = problem_dict.get('input_signal', random.choice(['0', '1']))
            
            # Transición simple
            if input_signal == '0':
                next_state = 'S1'
            else:
                next_state = 'S0'
            
            problem_text = f"En estado {current_state} con entrada {input_signal}, ¿cuál es el siguiente estado?"
            solution = next_state
        
        else:  # sequence_detection
            sequence = problem_dict.get('sequence', '1011')
            test_input = problem_dict.get('test_input', '11011011')
            
            problem_text = f"Diseña un detector de secuencia para '{sequence}' que reconozca en entrada '{test_input}'"
            solution = f"Secuencia encontrada en posiciones: [consult solution sheet]"
        
        return {
            'title': 'Máquinas de Estados Finitos',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type
        }

