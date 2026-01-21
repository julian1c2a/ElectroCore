"""
Generadores de ejercicios para Electrónica Básica.
Ley de Ohm, Potencia eléctrica, circuitos simples.
"""

import random
from typing import Dict, Any
from core.generator_base import ExerciseGenerator


class OhmsLawExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre la Ley de Ohm (V = I·R).
    Cálculo de voltaje, corriente y resistencia.
    """
    
    def topic(self) -> str:
        return "Ley de Ohm"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre Ley de Ohm."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['voltage', 'current', 'resistance']))
        
        if exercise_type == 'voltage':
            # Calcular V = I·R
            current_mA = problem_dict.get('current_mA', random.uniform(10, 500))
            resistance_ohm = problem_dict.get('resistance_ohm', random.uniform(100, 10000))
            
            # Convertir corriente a Amperios si está en mA
            current_A = current_mA / 1000 if current_mA > 100 else current_mA
            
            voltage = current_A * resistance_ohm
            
            problem_text = f"¿Cuál es el voltaje en una resistencia de {resistance_ohm:.0f}Ω cuando fluye una corriente de {current_mA:.1f}mA?"
            solution = f"{voltage:.2f}V"
        
        elif exercise_type == 'current':
            # Calcular I = V/R
            voltage_V = problem_dict.get('voltage_V', random.uniform(5, 100))
            resistance_ohm = problem_dict.get('resistance_ohm', random.uniform(100, 10000))
            
            current_A = voltage_V / resistance_ohm
            current_mA = current_A * 1000
            
            problem_text = f"¿Cuál es la corriente en una resistencia de {resistance_ohm:.0f}Ω con un voltaje de {voltage_V:.1f}V?"
            solution = f"{current_mA:.2f}mA ({current_A:.4f}A)"
        
        else:  # resistance
            # Calcular R = V/I
            voltage_V = problem_dict.get('voltage_V', random.uniform(5, 100))
            current_mA = problem_dict.get('current_mA', random.uniform(10, 500))
            
            current_A = current_mA / 1000
            resistance = voltage_V / current_A
            
            problem_text = f"¿Cuál es la resistencia si hay {voltage_V:.1f}V y {current_mA:.1f}mA?"
            solution = f"{resistance:.2f}Ω"
        
        return {
            'title': 'Ley de Ohm',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type,
            'formula': 'V = I·R'
        }


class PowerExerciseGenerator(ExerciseGenerator):
    """
    GENERADOR: Ejercicios sobre potencia eléctrica.
    P = V·I = I²·R = V²/R
    Cálculo de potencia disipada, energía, calor.
    """
    
    def topic(self) -> str:
        return "Potencia eléctrica"
    
    def generate_from_problem(self, problem_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Genera ejercicio sobre potencia eléctrica."""
        exercise_type = problem_dict.get('exercise_type', random.choice(['power_VI', 'power_IR', 'power_VR', 'energy', 'heating']))
        
        if exercise_type == 'power_VI':
            # P = V·I
            voltage_V = problem_dict.get('voltage_V', random.uniform(5, 100))
            current_mA = problem_dict.get('current_mA', random.uniform(10, 500))
            
            current_A = current_mA / 1000
            power_W = voltage_V * current_A
            power_mW = power_W * 1000
            
            problem_text = f"¿Cuál es la potencia en una carga con {voltage_V:.1f}V y {current_mA:.1f}mA?"
            solution = f"{power_mW:.2f}mW ({power_W:.4f}W)"
            formula = "P = V·I"
        
        elif exercise_type == 'power_IR':
            # P = I²·R
            current_mA = problem_dict.get('current_mA', random.uniform(10, 500))
            resistance_ohm = problem_dict.get('resistance_ohm', random.uniform(100, 10000))
            
            current_A = current_mA / 1000
            power_W = (current_A ** 2) * resistance_ohm
            power_mW = power_W * 1000
            
            problem_text = f"¿Cuál es la potencia disipada en {resistance_ohm:.0f}Ω cuando hay {current_mA:.1f}mA?"
            solution = f"{power_mW:.2f}mW ({power_W:.4f}W)"
            formula = "P = I²·R"
        
        elif exercise_type == 'power_VR':
            # P = V²/R
            voltage_V = problem_dict.get('voltage_V', random.uniform(5, 100))
            resistance_ohm = problem_dict.get('resistance_ohm', random.uniform(100, 10000))
            
            power_W = (voltage_V ** 2) / resistance_ohm
            power_mW = power_W * 1000
            
            problem_text = f"¿Cuál es la potencia en {resistance_ohm:.0f}Ω con {voltage_V:.1f}V aplicado?"
            solution = f"{power_mW:.2f}mW ({power_W:.4f}W)"
            formula = "P = V²/R"
        
        elif exercise_type == 'energy':
            # Energía = Potencia × Tiempo
            power_W = problem_dict.get('power_W', random.uniform(0.1, 10))
            time_hours = problem_dict.get('time_hours', random.uniform(1, 24))
            
            energy_Wh = power_W * time_hours
            energy_kWh = energy_Wh / 1000
            energy_J = energy_Wh * 3600
            
            problem_text = f"¿Cuánta energía consume un dispositivo de {power_W:.1f}W en {time_hours:.1f} horas?"
            solution = f"{energy_Wh:.2f}Wh ({energy_kWh:.4f}kWh, {energy_J:.0f}J)"
            formula = "E = P·t"
        
        else:  # heating (Efecto Joule)
            # Calor = I²·R·t = Energía
            current_mA = problem_dict.get('current_mA', random.uniform(10, 500))
            resistance_ohm = problem_dict.get('resistance_ohm', random.uniform(100, 10000))
            time_sec = problem_dict.get('time_sec', random.uniform(10, 300))
            
            current_A = current_mA / 1000
            energy_J = (current_A ** 2) * resistance_ohm * time_sec
            energy_cal = energy_J / 4.184  # Calorías
            
            problem_text = f"¿Cuál es el calor generado en {resistance_ohm:.0f}Ω con {current_mA:.1f}mA durante {time_sec:.0f}s?"
            solution = f"{energy_J:.2f}J ({energy_cal:.2f}cal)"
            formula = "Q = I²·R·t"
        
        return {
            'title': 'Potencia Eléctrica',
            'problem': problem_text,
            'solution': solution,
            'exercise_type': exercise_type,
            'formula': formula
        }
