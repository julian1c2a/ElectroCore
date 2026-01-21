"""
Factory para instanciar dinámicamente generadores de ejercicios.
Permite crear generadores basados en topic_id del catálogo.
"""

import importlib
from typing import Optional, Type, Dict, Any
from core.generator_base import ExerciseGenerator
from core.exercise_mapper import ExerciseMapper, GeneratorConfig


class GeneratorFactory:
    """Factory para crear instancias de generadores."""
    
    # Cache de clases importadas
    _cache: Dict[str, Type[ExerciseGenerator]] = {}
    
    @classmethod
    def create_generator(cls, topic_id: str) -> Optional[ExerciseGenerator]:
        """
        Crea una instancia del generador para un topic_id específico.
        
        Args:
            topic_id: ID del tema del catálogo (ej: "2.1.1.1.3")
        
        Returns:
            Instancia del generador, o None si no está mapeado
        
        Raises:
            ImportError: Si el módulo no puede ser importado
            AttributeError: Si la clase no existe
        """
        config = ExerciseMapper.get_generator_config(topic_id)
        if not config:
            return None
        
        return cls._instantiate_generator(config)
    
    @classmethod
    def _instantiate_generator(cls, config: GeneratorConfig) -> ExerciseGenerator:
        """Instantía un generador desde su configuración."""
        # Obtener o cargar la clase del cache
        cache_key = f"{config.module_path}.{config.class_name}"
        
        if cache_key not in cls._cache:
            # Importar módulo y obtener clase
            module = importlib.import_module(config.module_path)
            generator_class = getattr(module, config.class_name)
            cls._cache[cache_key] = generator_class
        
        # Crear instancia
        generator_class = cls._cache[cache_key]
        return generator_class()
    
    @classmethod
    def create_generator_batch(cls, topic_ids: list) -> Dict[str, Optional[ExerciseGenerator]]:
        """
        Crea múltiples generadores.
        
        Args:
            topic_ids: Lista de topic IDs
        
        Returns:
            Diccionario topic_id -> generador (None si no existe)
        """
        return {topic_id: cls.create_generator(topic_id) for topic_id in topic_ids}
    
    @classmethod
    def get_available_generators(cls) -> Dict[str, GeneratorConfig]:
        """Obtiene todos los generadores mapeados."""
        return ExerciseMapper.get_all_generators()
    
    @classmethod
    def get_generators_by_module(cls, module_name: str) -> Dict[str, GeneratorConfig]:
        """Obtiene generadores de un módulo específico."""
        return ExerciseMapper.get_generators_by_module(module_name)
    
    @classmethod
    def test_generator_availability(cls) -> Dict[str, dict]:
        """
        Prueba qué generadores están disponibles (el módulo existe).
        
        Returns:
            Dict con status de cada generador
        """
        results = {}
        for topic_id, config in ExerciseMapper.get_all_generators().items():
            try:
                cls.create_generator(topic_id)
                results[topic_id] = {'status': 'available', 'class': config.class_name}
            except (ImportError, AttributeError) as e:
                results[topic_id] = {'status': 'missing', 'error': str(e)}
        
        return results


class ExerciseGeneratorBuilder:
    """
    Builder para construir ejercicios completos usando generadores.
    Encadena la creación de ejercicios con parámetros específicos.
    """
    
    def __init__(self, topic_id: str):
        """
        Inicializa el builder con un topic_id.
        
        Args:
            topic_id: ID del tema del catálogo
        """
        self.topic_id = topic_id
        self.generator = GeneratorFactory.create_generator(topic_id)
        self.problem_params: Dict[str, Any] = {}
        self.difficulty = 1
    
    def with_difficulty(self, difficulty: int) -> 'ExerciseGeneratorBuilder':
        """Establece el nivel de dificultad."""
        self.difficulty = difficulty
        return self
    
    def with_params(self, **kwargs) -> 'ExerciseGeneratorBuilder':
        """Establece parámetros del problema."""
        self.problem_params.update(kwargs)
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Construye el ejercicio completo.
        
        Returns:
            Ejercicio generado
        
        Raises:
            ValueError: Si el generador no está disponible
        """
        if self.generator is None:
            raise ValueError(f"No hay generador disponible para {self.topic_id}")
        
        # Intentar usar generate_from_problem si existe
        if hasattr(self.generator, 'generate_from_problem'):
            return self.generator.generate_from_problem(self.problem_params)
        
        # Si no, intentar usar generate
        elif hasattr(self.generator, 'generate'):
            return self.generator.generate(self.difficulty)
        
        else:
            raise ValueError(f"Generador {type(self.generator).__name__} no tiene método de generación")
    
    def get_config(self) -> Optional[GeneratorConfig]:
        """Obtiene la configuración del generador."""
        return ExerciseMapper.get_generator_config(self.topic_id)
