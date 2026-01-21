"""
Generadores de ejercicios para Electrónica Analógica.
Leyes de Kirchhoff, análisis de circuitos, transformadores.
"""

import random
from typing import Dict, Any, List, Tuple
from core.generator_base import ExerciseGenerator


class KirchhoffLawsExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre las Leyes de Kirchhoff.
    LVK (Ley de Voltajes), LCK (Ley de Corrientes).
    Análisis de mallas y nodos.
    """
    
    def topic(self) -> str:
        return "Leyes Fundamentales de la Electricidad"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre Leyes de Kirchhoff."""
        law_type = problem_dict.get('law_type', random.choice(['LVK', 'LCK', 'mesh_analysis', 'nodal_analysis']))
        
        if law_type == 'LVK':
            # Ley de Voltajes de Kirchhoff: ΣV = 0 en una malla
            V1 = problem_dict.get('V1', random.uniform(5, 50))
            V2 = problem_dict.get('V2', random.uniform(5, 50))
            V3 = problem_dict.get('V3', None)
            
            if V3 is None:
                V3 = V1 + V2  # Voltaje desconocido que debe encontrarse
                problem_text = f"En una malla de circuito: {V1:.1f}V + {V2:.1f}V + V3 = 0. ¿Cuál es V3?"
                solution = f"V3 = -{V3:.1f}V (por LVK: ΣV = 0)"
            else:
                problem_text = f"Verifica la LVK para una malla: {V1:.1f}V, {V2:.1f}V, {V3:.1f}V"
                total = V1 + V2 + V3
                solution = f"ΣV = {total:.2f}V" + (" ✓ (cumple LVK)" if abs(total) < 0.01 else " ✗ (no cumple)")
        
        elif law_type == 'LCK':
            # Ley de Corrientes de Kirchhoff: ΣI_entrada = ΣI_salida en un nodo
            I1 = problem_dict.get('I1', random.uniform(10, 500))
            I2 = problem_dict.get('I2', random.uniform(10, 500))
            I3 = problem_dict.get('I3', None)
            
            if I3 is None:
                I3 = I1 + I2  # Corriente desconocida
                problem_text = f"En un nodo: {I1:.1f}mA + {I2:.1f}mA = I3 + corriente_salida. Si corriente_salida=0, ¿I3?"
                solution = f"I3 = {I3:.1f}mA (por LCK: ΣI_entrada = ΣI_salida)"
            else:
                problem_text = f"Verifica LCK en un nodo: Entrada {I1:.1f}mA, Salida {I2:.1f}mA y {I3:.1f}mA"
                total_in = I1
                total_out = I2 + I3
                solution = f"ΣI_entrada = {total_in:.1f}mA, ΣI_salida = {total_out:.1f}mA" + (" ✓" if abs(total_in - total_out) < 0.01 else " ✗")
        
        elif law_type == 'mesh_analysis':
            # Análisis de mallas para circuito simple de 2 mallas
            V_source = problem_dict.get('V_source', random.uniform(10, 50))
            R1 = problem_dict.get('R1', random.uniform(100, 1000))
            R2 = problem_dict.get('R2', random.uniform(100, 1000))
            R3 = problem_dict.get('R3', random.uniform(100, 1000))
            
            # Simplificación: circuito básico 2 mallas
            # Ecuaciones:
            # V_source = I1·R1 + I_common·R3
            # 0 = I2·R2 + I_common·R3
            # donde I_common = I1 - I2
            
            problem_text = f"Analiza por mallas: V={V_source:.1f}V, R1={R1:.0f}Ω, R2={R2:.0f}Ω, R3={R3:.0f}Ω"
            solution = "Plantea ecuaciones: V = I1(R1+R3) - I2·R3; 0 = -I1·R3 + I2(R2+R3)"
        
        else:  # nodal_analysis
            # Análisis nodal
            V_source = problem_dict.get('V_source', random.uniform(10, 50))
            R1 = problem_dict.get('R1', random.uniform(100, 1000))
            R2 = problem_dict.get('R2', random.uniform(100, 1000))
            
            problem_text = f"Analiza por nodos: V={V_source:.1f}V, R1={R1:.0f}Ω, R2={R2:.0f}Ω"
            solution = "Plantea: (V_nodo - V_source)/R1 + V_nodo/R2 = 0"
        
        return {
            'title': 'Leyes de Kirchhoff',
            'problem': problem_text,
            'solution': solution,
            'law_type': law_type
        }
