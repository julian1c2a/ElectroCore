"""
Mapper que vincula temas del catálogo con generadores de ejercicios.
Permite consultar qué generador usar para cada tema específico.
"""

from typing import Dict, List, Optional, Type
from dataclasses import dataclass


@dataclass
class GeneratorConfig:
    """Configuración de un generador para un tema específico."""
    topic_id: str
    generator_class: str  # Nombre de la clase generadora
    module_path: str      # Ruta del módulo (ej: "modules.numeracion.generators")
    class_name: str       # Nombre de la clase
    description: str
    exercise_types: List[str]  # Tipos de ejercicios que genera


class ExerciseMapper:
    """Mapper central que vincula temas del catálogo con generadores."""
    
    # Mapeo: topic_id -> GeneratorConfig
    GENERATORS_MAP = {
        # ===== NUMERACIÓN =====
        "2.1.1.1.3": GeneratorConfig(
            topic_id="2.1.1.1.3",
            generator_class="ConversionExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="ConversionExerciseGenerator",
            description="Conversión entre sistemas de numeración",
            exercise_types=["conversion_bases", "decimal_to_binary", "binary_to_hex", "octal_to_decimal"]
        ),
        "2.1.1.2": GeneratorConfig(
            topic_id="2.1.1.2",
            generator_class="MultiBaseExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="MultiBaseExerciseGenerator",
            description="Sistemas Binarios, Octales y Hexadecimales",
            exercise_types=["binary_arithmetic", "octal_arithmetic", "hexadecimal_arithmetic"]
        ),
        "2.1.1.3": GeneratorConfig(
            topic_id="2.1.1.3",
            generator_class="FixedLengthExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="FixedLengthExerciseGenerator",
            description="Representación en Longitud Fija",
            exercise_types=["fixed_length_conversion", "range_calculation", "overflow_detection"]
        ),
        "2.1.1.4": GeneratorConfig(
            topic_id="2.1.1.4",
            generator_class="SignedIntegerExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="SignedIntegerExerciseGenerator",
            description="Números Enteros con Signo",
            exercise_types=["sign_magnitude", "twos_complement", "excess_notation", "conversion_between_representations"]
        ),
        "2.1.1.5.1": GeneratorConfig(
            topic_id="2.1.1.5.1",
            generator_class="ArithmeticOperationsExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="ArithmeticOperationsExerciseGenerator",
            description="Operaciones Aritméticas Básicas",
            exercise_types=["addition", "subtraction", "multiplication", "division", "modulo_operations"]
        ),
        "2.1.1.5.2": GeneratorConfig(
            topic_id="2.1.1.5.2",
            generator_class="FixedPointExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="FixedPointExerciseGenerator",
            description="Números con Parte Fraccionaria - Punto Fijo",
            exercise_types=["fixed_point_conversion", "fixed_point_arithmetic", "precision_calculation"]
        ),
        "2.1.1.5.3": GeneratorConfig(
            topic_id="2.1.1.5.3",
            generator_class="FloatingPointExerciseGenerator",
            module_path="modules.numeracion.generators",
            class_name="FloatingPointExerciseGenerator",
            description="Números en Punto Flotante - IEEE 754",
            exercise_types=["ieee754_representation", "normalization", "denormalization", "rounding_operations", "floating_point_arithmetic"]
        ),
        
        # ===== BOOLEANO =====
        "2.2.1": GeneratorConfig(
            topic_id="2.2.1",
            generator_class="HuntingtonPostulatesExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="HuntingtonPostulatesExerciseGenerator",
            description="Los Postulados de Huntington",
            exercise_types=["apply_postulates", "verify_postulates", "algebraic_proofs"]
        ),
        "2.2.2": GeneratorConfig(
            topic_id="2.2.2",
            generator_class="BooleanPropertiesExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="BooleanPropertiesExerciseGenerator",
            description="Propiedades y Teoremas del Álgebra de Boole",
            exercise_types=["simplification_by_laws", "verify_properties", "boolean_algebra_proofs"]
        ),
        "2.2.3": GeneratorConfig(
            topic_id="2.2.3",
            generator_class="ShannonAlgebraExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="ShannonAlgebraExerciseGenerator",
            description="El Álgebra de Conmutación de Shannon",
            exercise_types=["shannon_algebra_conversion", "truth_table_generation", "switching_algebra"]
        ),
        "2.2.4": GeneratorConfig(
            topic_id="2.2.4",
            generator_class="LogicGateExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="LogicGateExerciseGenerator",
            description="Las Puertas Lógicas Básicas",
            exercise_types=["truth_tables", "gate_circuits", "timing_diagrams", "gate_equivalence"]
        ),
        "2.2.5": GeneratorConfig(
            topic_id="2.2.5",
            generator_class="LogicFunctionExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="LogicFunctionExerciseGenerator",
            description="Funciones Lógicas",
            exercise_types=["minterms_maxterms", "karnaugh_maps", "sum_of_products", "product_of_sums", "quine_mccluskey"]
        ),
        "2.2.6": GeneratorConfig(
            topic_id="2.2.6",
            generator_class="CombinationalCircuitExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="CombinationalCircuitExerciseGenerator",
            description="Sistemas Combinacionales Básicos",
            exercise_types=["encoders", "decoders", "multiplexers", "demultiplexers", "comparators", "adders"]
        ),
        "2.2.7": GeneratorConfig(
            topic_id="2.2.7",
            generator_class="AdvancedCombinationalExerciseGenerator",
            module_path="modules.booleano.generators",
            class_name="AdvancedCombinationalExerciseGenerator",
            description="Sistemas Combinacionales Avanzados",
            exercise_types=["alu_design", "bcd_operations", "seven_segment_decoders", "propagation_delay", "hazard_analysis"]
        ),
        
        # ===== SECUENCIAL =====
        "2.3.2": GeneratorConfig(
            topic_id="2.3.2",
            generator_class="FlipFlopExerciseGenerator",
            module_path="modules.secuencial.generators",
            class_name="FlipFlopExerciseGenerator",
            description="Elementos Básicos (Latches y Flip-Flops)",
            exercise_types=["latch_analysis", "flipflop_transitions", "preset_clear_operations", "timing_constraints"]
        ),
        "2.3.3": GeneratorConfig(
            topic_id="2.3.3",
            generator_class="SequentialSystemsExerciseGenerator",
            module_path="modules.secuencial.generators",
            class_name="SequentialSystemsExerciseGenerator",
            description="Sistemas Secuenciales Principales",
            exercise_types=["counter_sequences", "register_operations", "memory_addressing", "shift_operations"]
        ),
        "2.3.4": GeneratorConfig(
            topic_id="2.3.4",
            generator_class="FSMExerciseGenerator",
            module_path="modules.secuencial.generators",
            class_name="FSMExerciseGenerator",
            description="Máquinas de Estados Finitos",
            exercise_types=["state_diagrams", "state_transitions", "state_minimization", "fsm_design", "sequence_detection"]
        ),
        
        # ===== ELECTRÓNICA BÁSICA =====
        "1.1.2": GeneratorConfig(
            topic_id="1.1.2",
            generator_class="OhmsLawExerciseGenerator",
            module_path="modules.basico.generators",
            class_name="OhmsLawExerciseGenerator",
            description="Ley de Ohm",
            exercise_types=["ohms_law_calculation", "resistance_calculation", "current_calculation", "voltage_calculation"]
        ),
        "1.1.3": GeneratorConfig(
            topic_id="1.1.3",
            generator_class="PowerExerciseGenerator",
            module_path="modules.basico.generators",
            class_name="PowerExerciseGenerator",
            description="Potencia eléctrica",
            exercise_types=["power_calculation", "energy_calculation", "resistance_heating", "efficiency_analysis"]
        ),
        "3.1.1": GeneratorConfig(
            topic_id="3.1.1",
            generator_class="KirchhoffLawsExerciseGenerator",
            module_path="modules.analogico.generators",
            class_name="KirchhoffLawsExerciseGenerator",
            description="Leyes Fundamentales de la Electricidad",
            exercise_types=["kirchhoff_voltage_law", "kirchhoff_current_law", "mesh_analysis", "nodal_analysis"]
        ),
    }
    
    @classmethod
    def get_generator_config(cls, topic_id: str) -> Optional[GeneratorConfig]:
        """Obtiene la configuración del generador para un tema específico."""
        return cls.GENERATORS_MAP.get(topic_id)
    
    @classmethod
    def get_all_generators(cls) -> Dict[str, GeneratorConfig]:
        """Obtiene todos los generadores mapeados."""
        return cls.GENERATORS_MAP
    
    @classmethod
    def get_generators_by_module(cls, module_name: str) -> Dict[str, GeneratorConfig]:
        """Obtiene todos los generadores de un módulo específico."""
        return {
            topic_id: config
            for topic_id, config in cls.GENERATORS_MAP.items()
            if config.module_path.startswith(f"modules.{module_name}")
        }
    
    @classmethod
    def get_unimplemented_generators(cls) -> List[str]:
        """Lista de temas sin generador implementado aún."""
        unimplemented = []
        for topic_id, config in cls.GENERATORS_MAP.items():
            try:
                # Intenta importar el módulo para verificar si existe
                module = __import__(config.module_path, fromlist=[config.class_name])
                getattr(module, config.class_name)
            except (ImportError, AttributeError):
                unimplemented.append(topic_id)
        return unimplemented
