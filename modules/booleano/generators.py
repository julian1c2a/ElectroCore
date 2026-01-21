"""
Generadores de ejercicios para Álgebra Booleana.
"""

import random
from typing import Dict, Any, List
from core.generator_base import ExerciseGenerator, ExerciseRandomizer
from modules.booleano.models import BooleanPropertiesExercise, LogicGate, TruthTable


class BooleanPropertiesExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Propiedades y teoremas del Álgebra de Boole.
    Simplificación mediante leyes específicas.
    """
    
    PROPERTIES = {
        'idempotencia': {
            'description': 'A + A = A y A·A = A',
            'expressions': ['A + A', 'A·A', 'A + 0', 'A·1'],
            'solutions': {'A + A': 'A', 'A·A': 'A', 'A + 0': 'A', 'A·1': 'A'}
        },
        'elemento_neutro': {
            'description': 'A + 0 = A y A·1 = A',
            'expressions': ['A + 0', 'A·1', 'B + 0', 'B·1'],
            'solutions': {'A + 0': 'A', 'A·1': 'A', 'B + 0': 'B', 'B·1': 'B'}
        },
        'elemento_absorbente': {
            'description': 'A + 1 = 1 y A·0 = 0',
            'expressions': ['A + 1', 'A·0', 'B + 1', 'B·0'],
            'solutions': {'A + 1': '1', 'A·0': '0', 'B + 1': '1', 'B·0': '0'}
        },
        'complemento': {
            'description': "A + A' = 1 y A·A' = 0",
            'expressions': ["A + A'", "A·A'", "B + B'", "B·B'"],
            'solutions': {"A + A'": '1', "A·A'": '0', "B + B'": '1', "B·B'": '0'}
        },
        'doble_negación': {
            'description': "A'' = A",
            'expressions': ["(A')'", "(B')'", "((A+B))'", "((A·B))'"],
            'solutions': {"(A')'": 'A', "(B')'": 'B', "((A+B))'": "A'·B'", "((A·B))'": "A'+B'"}
        },
        'absorción': {
            'description': "A + A·B = A y A·(A+B) = A",
            'expressions': ['A + A·B', 'A·(A+B)', 'B + A·B', 'B·(A+B)'],
            'solutions': {'A + A·B': 'A', 'A·(A+B)': 'A', 'B + A·B': 'B', 'B·(A+B)': 'B'}
        },
        'de_morgan': {
            'description': "(A+B)' = A'·B' y (A·B)' = A'+B'",
            'expressions': ["(A+B)'", "(A·B)'", "(A+B+C)'", "(A·B·C)'"],
            'solutions': {"(A+B)'": "A'·B'", "(A·B)'": "A'+B'", "(A+B+C)'": "A'·B'·C'", "(A·B·C)'": "A'+B'+C'"}
        }
    }
    
    def topic(self) -> str:
        return "Propiedades y Teoremas del Álgebra de Boole"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> BooleanPropertiesExercise:
        """Genera ejercicio de propiedades booleanas."""
        property_name = problem_dict.get('property_name', random.choice(list(self.PROPERTIES.keys())))
        prop = self.PROPERTIES[property_name]
        
        expression = problem_dict.get('expression', random.choice(prop['expressions']))
        solution = prop['solutions'].get(expression, expression)
        
        # Generar pasos de simplificación
        steps = self._generate_steps(property_name, expression, solution)
        
        return BooleanPropertiesExercise(
            title="Simplificación Booleana",
            description=f"Simplifica usando la ley de {property_name}",
            property_name=property_name,
            expression_problem=expression,
            law_to_apply=prop['description'],
            solution=solution,
            steps=steps
        )
    
    def _generate_steps(self, property_name: str, expression: str, solution: str) -> List[str]:
        """Genera los pasos de simplificación."""
        steps = [
            f"Expresión original: {expression}",
            f"Ley a aplicar: {self.PROPERTIES[property_name]['description']}",
            f"Resultado: {solution}"
        ]
        return steps


class ShannonAlgebraExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Álgebra de Conmutación de Shannon.
    Basada en el Álgebra de Boole pero aplicada a circuitos.
    """
    
    def topic(self) -> str:
        return "Álgebra de Conmutación de Shannon"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre Shannon."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['conversion', 'equivalence']))
        
        if exercise_type == 'conversion':
            # Convertir entre forma algebraica y tabla de verdad
            n_vars = problem_dict.get('n_vars', random.choice([2, 3]))
            expression = problem_dict.get('expression', self._generate_random_expression(n_vars))
            
            truth_table = self._expression_to_truth_table(expression, n_vars)
            
            problem_text = f"Construye la tabla de verdad para: {expression}"
            solution = self._format_truth_table(truth_table)
        
        else:  # equivalence
            # Verificar equivalencia entre dos expresiones
            expr1 = problem_dict.get('expr1', "A+B")
            expr2 = problem_dict.get('expr2', "B+A")
            
            are_equivalent = self._check_equivalence(expr1, expr2)
            
            problem_text = f"¿Son equivalentes las expresiones:\n  {expr1}\n  y\n  {expr2}?"
            solution = "Sí" if are_equivalent else "No"
        
        return {
            'title': 'Álgebra de Shannon',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type
        }
    
    def _generate_random_expression(self, n_vars: int) -> str:
        """Genera una expresión algebraica aleatoria."""
        variables = [chr(ord('A') + i) for i in range(n_vars)]
        # Expresión simple: una combinación aleatoria
        terms = []
        for _ in range(random.randint(1, 3)):
            term = random.choice(variables)
            if random.random() > 0.5:
                term += "'"
            terms.append(term)
        return '+'.join(terms) + " + ..." if len(terms) > 1 else terms[0]
    
    def _expression_to_truth_table(self, expression: str, n_vars: int) -> Dict[str, Any]:
        """Convierte una expresión a tabla de verdad."""
        return {'n_vars': n_vars, 'expression': expression}
    
    def _format_truth_table(self, truth_table: Dict[str, Any]) -> str:
        """Formatea la tabla de verdad."""
        return f"Tabla para {truth_table['n_vars']} variables"
    
    def _check_equivalence(self, expr1: str, expr2: str) -> bool:
        """Verifica si dos expresiones son equivalentes (simplificación)."""
        # Aquí iría la lógica real de equivalencia
        return expr1.replace('+', ' or ').lower() == expr2.replace('+', ' or ').lower()


class LogicGateExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre puertas lógicas básicas.
    Tablas de verdad, símbolos, comportamiento temporal.
    """
    
    GATES = {
        'AND': {
            'description': 'AND de 2 entradas',
            'symbol': '⋀',
            'truth_table_2': {
                (0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1
            },
            'boolean_equation': 'Y = A · B'
        },
        'OR': {
            'description': 'OR de 2 entradas',
            'symbol': '⋁',
            'truth_table_2': {
                (0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1
            },
            'boolean_equation': 'Y = A + B'
        },
        'NOT': {
            'description': 'NOT (inversor)',
            'symbol': '¬',
            'truth_table_1': {
                0: 1, 1: 0
            },
            'boolean_equation': "Y = A'"
        },
        'NAND': {
            'description': 'NAND de 2 entradas',
            'symbol': '⊼',
            'truth_table_2': {
                (0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0
            },
            'boolean_equation': "Y = (A · B)'"
        },
        'NOR': {
            'description': 'NOR de 2 entradas',
            'symbol': '⊽',
            'truth_table_2': {
                (0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0
            },
            'boolean_equation': "Y = (A + B)'"
        },
        'XOR': {
            'description': 'XOR de 2 entradas',
            'symbol': '⊕',
            'truth_table_2': {
                (0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0
            },
            'boolean_equation': "Y = A ⊕ B = A'B + AB'"
        }
    }
    
    def topic(self) -> str:
        return "Las Puertas Lógicas Básicas"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre puertas lógicas."""
        gate_type = problem_dict.get('gate_type', random.choice(list(self.GATES.keys())))
        exercise_type = problem_dict.get('exercise_type', random.choice(['truth_table', 'logic_value', 'identify']))
        
        gate_info = self.GATES[gate_type]
        
        if exercise_type == 'truth_table':
            problem_text = f"Construye la tabla de verdad para la puerta {gate_type} ({gate_info['description']})"
            solution = f"Ecuación: {gate_info['boolean_equation']}\nVer tabla adjunta"
        
        elif exercise_type == 'logic_value':
            if gate_type == 'NOT':
                input_val = problem_dict.get('input_val', random.randint(0, 1))
                output = gate_info['truth_table_1'][input_val]
                problem_text = f"¿Cuál es la salida de {gate_type} si A={input_val}?"
            else:
                input_a = problem_dict.get('input_a', random.randint(0, 1))
                input_b = problem_dict.get('input_b', random.randint(0, 1))
                output = gate_info['truth_table_2'][(input_a, input_b)]
                problem_text = f"¿Cuál es la salida de {gate_type} si A={input_a}, B={input_b}?"
            
            solution = str(output)
        
        else:  # identify
            problem_text = f"¿Cuál es la ecuación booleana para la puerta {gate_type}?"
            solution = gate_info['boolean_equation']
        
        return {
            'title': 'Puertas Lógicas Básicas',
            'problem': problem_text,
            'solution': solution,
            'gate_type': gate_type,
            'exercise_type': exercise_type
        }


class LogicFunctionExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Funciones lógicas, minterms, maxterms, mapas de Karnaugh.
    """
    
    def topic(self) -> str:
        return "Funciones Lógicas"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre funciones lógicas."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['minterms_maxterms', 'karnaugh', 'canonical_forms']))
        n_vars = problem_dict.get('n_vars', random.choice([2, 3]))
        
        if exercise_type == 'minterms_maxterms':
            # Generar tabla de verdad y pedir minterms/maxterms
            truth_table = self._generate_truth_table(n_vars)
            minterms = [i for i, val in enumerate(truth_table) if val == 1]
            maxterms = [i for i, val in enumerate(truth_table) if val == 0]
            
            problem_text = f"Para la función definida por la tabla de verdad, identifica los minterms"
            solution = f"Minterms: {minterms}\nMaxterms: {maxterms}"
        
        elif exercise_type == 'karnaugh':
            problem_text = f"Simplifica usando Mapa de Karnaugh para {n_vars} variables"
            solution = "Consultar mapa en hoja de soluciones"
        
        else:  # canonical_forms
            problem_text = f"Expresa la función en Forma Normal Disyuntiva (SOP)"
            solution = "f(A,B,...) = m1 + m3 + m5 + ..."
        
        return {
            'title': 'Funciones Lógicas',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type,
            'n_vars': n_vars,
            'truth_table': truth_table if exercise_type == 'minterms_maxterms' else None
        }
    
    def _generate_truth_table(self, n_vars: int) -> List[int]:
        """Genera una tabla de verdad aleatoria."""
        return [random.randint(0, 1) for _ in range(2**n_vars)]


class CombinationalCircuitExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Sistemas combinacionales básicos.
    Codificadores, decodificadores, multiplexores, sumadores.
    """
    
    def topic(self) -> str:
        return "Sistemas Combinacionales Básicos"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de circuitos combinacionales."""
        circuit_type = problem_dict.get('circuit_type', random.choice(['encoder', 'decoder', 'multiplexer', 'adder']))
        
        if circuit_type == 'encoder':
            # Codificador 8:3
            input_line = problem_dict.get('input_line', random.randint(0, 7))
            output = format(input_line, '03b')
            problem_text = f"¿Cuál es la salida de un codificador 8:3 si se activa la entrada {input_line}?"
            solution = output
        
        elif circuit_type == 'decoder':
            # Decodificador 3:8
            binary_input = problem_dict.get('binary_input', format(random.randint(0, 7), '03b'))
            output_line = int(binary_input, 2)
            problem_text = f"¿Cuál es la salida de un decodificador 3:8 para entrada {binary_input}?"
            solution = f"Línea {output_line} activada"
        
        elif circuit_type == 'multiplexer':
            # Multiplexor 4:1
            select = random.randint(0, 3)
            inputs = [random.randint(0, 1) for _ in range(4)]
            output = inputs[select]
            problem_text = f"Multiplexor 4:1 con entradas {inputs} y select={select}. ¿Salida?"
            solution = str(output)
        
        else:  # adder
            # Sumador completo
            a = problem_dict.get('a', random.randint(0, 1))
            b = problem_dict.get('b', random.randint(0, 1))
            cin = problem_dict.get('cin', random.randint(0, 1))
            
            sum_bit = (a + b + cin) % 2
            cout = 1 if (a + b + cin) >= 2 else 0
            
            problem_text = f"Sumador completo: A={a}, B={b}, Cin={cin}. ¿Sum y Cout?"
            solution = f"Sum={sum_bit}, Cout={cout}"
        
        return {
            'title': 'Sistemas Combinacionales',
            'problem': problem_text,
            'solution': solution,
            'circuit_type': circuit_type
        }


class AdvancedCombinationalExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Sistemas combinacionales avanzados.
    Análisis de retardo, hazards, ALU simplificada.
    """
    
    def topic(self) -> str:
        return "Sistemas Combinacionales Avanzados"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio de circuitos avanzados."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['propagation_delay', 'hazard_detection', 'bcd_operations']))
        
        if exercise_type == 'propagation_delay':
            # Calcular retardo de propagación
            num_gates = problem_dict.get('num_gates', random.randint(3, 6))
            gate_delay = problem_dict.get('gate_delay', 10)  # ns
            total_delay = num_gates * gate_delay
            
            problem_text = f"¿Cuál es el retardo total de una cadena de {num_gates} compuertas con retardo {gate_delay}ns cada una?"
            solution = f"{total_delay} ns"
        
        elif exercise_type == 'hazard_detection':
            problem_text = "Identifica los static hazards en el circuito dado"
            solution = "Requiere análisis detallado del circuito (ver hoja de soluciones)"
        
        else:  # bcd_operations
            bcd1 = problem_dict.get('bcd1', format(random.randint(0, 9), '04b'))
            bcd2 = problem_dict.get('bcd2', format(random.randint(0, 9), '04b'))
            
            dec1 = int(bcd1, 2)
            dec2 = int(bcd2, 2)
            result = dec1 + dec2
            
            problem_text = f"Suma en BCD: {bcd1} + {bcd2} = ?"
            solution = f"Decimal: {dec1} + {dec2} = {result}; BCD: {format(result, '08b')}"
        
        return {
            'title': 'Sistemas Combinacionales Avanzados',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type
        }

class HuntingtonPostulatesExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Los postulados de Huntington para el Álgebra de Boole.
    """
    
    def topic(self) -> str:
        return "Los Postulados de Huntington"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre postulados de Huntington."""
        postulate = problem_dict.get('postulate', random.choice([
            'cerradura', 'elemento_identidad', 'conmutatividad', 'asociatividad',
            'distributividad', 'complemento', 'unicidad'
        ]))
        
        postulate_descriptions = {
            'cerradura': ('El resultado de A+B y A·B está dentro del conjunto',
                         'Cerradura respecto a + y ·'),
            'elemento_identidad': ('Existe 0 y 1 tales que A+0=A y A·1=A',
                                  'Existencia de elementos identidad'),
            'conmutatividad': ('A+B = B+A y A·B = B·A',
                              'Propiedad conmutativa'),
            'asociatividad': ('(A+B)+C = A+(B+C) y (A·B)·C = A·(B·C)',
                             'Propiedad asociativa'),
            'distributividad': ('A·(B+C) = A·B + A·C y A+(B·C) = (A+B)·(A+C)',
                               'Propiedad distributiva'),
            'complemento': ("Existe A' tal que A+A'=1 y A·A'=0",
                           'Complemento'),
            'unicidad': ('Si A+B=1 y A·B=0, entonces B=A\' (unicidad del complemento)',
                        'Unicidad del complemento')
        }
        
        description, postulate_name = postulate_descriptions[postulate]
        
        problem_text = f"Enuncia el postulado de {postulate_name}"
        solution = description
        
        return {
            'title': 'Postulados de Huntington',
            'problem': problem_text,
            'solution': solution,
            'postulate': postulate
        }
