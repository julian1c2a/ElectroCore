import json
import os
import random
from typing import List, Dict, Any, Optional
from core.generator_base import ExerciseData, ExerciseGenerator, ExerciseRandomizer
from core.catalog import EXERCISE_CATALOG

# Fase C: Importar repository (opcional)
try:
    from database import ProblemRepository
    HAS_REPOSITORY = True
except ImportError:
    HAS_REPOSITORY = False
    ProblemRepository = None

# Fase C: Importar mappers
try:
    from models.mappers import MAPPER_REGISTRY
    HAS_MAPPERS = True
except ImportError:
    HAS_MAPPERS = False
    MAPPER_REGISTRY = {}

class ExamBuilder:
    def __init__(self, config_file: str, problem_repository: Optional['ProblemRepository'] = None):
        """
        Crea un ExamBuilder con soporte para persistencia (Fase C).
        
        Args:
            config_file: Ruta del archivo de configuración JSON
            problem_repository: (Opcional) Repositorio para guardar/cargar problemas.
                               Si None, no usa persistencia.
                               Puede ser FileProblemRepository o SQLiteProblemRepository.
        """
        self.config = self._load_config(config_file)
        self._configure_seed()
        self.exercises_data: List[ExerciseData] = []
        self.exercises_json: List[Dict[str, Any]] = []
        
        # Fase C: Repositorio
        self.problem_repository = problem_repository
        self.saved_problems: List[str] = []  # IDs de problemas guardados
        self.loaded_problems: List[str] = []  # IDs de problemas cargados del repo

    def _load_config(self, filename: str) -> Dict[str, Any]:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"El archivo de configuración '{filename}' no existe.")
        
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _configure_seed(self):
        """Configura la semilla aleatoria si está presente en la configuración."""
        seed = self.config.get("seed")
        if seed is not None:
            print(f"[SEED] Semilla fija detectada: {seed}. La generación será determinista.")
            random.seed(seed)
        else:
            print("[SEED] Semilla aleatoria (random).")

    def build(self, use_repository: bool = True, reuse_probability: float = 0.0) -> List[ExerciseData]:
        """
        Construye el examen generando los datos para cada ejercicio definido en la configuración.
        
        FASE C: Soporte para persistencia.
        
        ARQUITECTURA ORTOGONAL:
        1. Si el config especifica 'problem_json', usa generador directo (sin aleatorización)
        2. Si especifica 'randomizer_params', usa aleatorizador + generador con seed
        3. Si no especifica nada, usa generador legacy (backward compatibility)
        
        FASE C - PARÁMETROS:
        - use_repository: Si True y existe self.problem_repository, guarda cada problema generado
        - reuse_probability: (0.0-1.0) Probabilidad de reutilizar problema existente del repositorio
                             en lugar de generar uno nuevo
        
        IMPORTANTE: Genera dos salidas paralelas:
        1. self.exercises_data: List[ExerciseData] objetos Python (para renderers Python)
        2. self.exercises_json: List[Dict] JSON agnóstico (para cualquier renderer agnóstico)
        """
        self.exercises_data = []
        self.exercises_json = []
        self.saved_problems = []
        self.loaded_problems = []
        requested_exercises = self.config.get("exercises", [])

        print(f"[BUILD] Construyendo examen: {self.config.get('title', 'Sin título')}")
        
        # Fase C: Mostrar estado del repositorio
        if self.problem_repository:
            repo_info = self.problem_repository.info()
            print(f"   [REPO] Repositorio: {repo_info['backend']} ({repo_info['total']} problemas)")

        for req in requested_exercises:
            ex_id = req.get("id")
            qty = req.get("qty", 1)
            difficulty = req.get("difficulty", 1)

            if ex_id not in EXERCISE_CATALOG:
                print(f"[WARN]  Advertencia: El ejercicio '{ex_id}' no existe en el catálogo. Saltando.")
                continue

            # Buscar generador en el catálogo
            generator = EXERCISE_CATALOG[ex_id]
            print(f"   [*] Generando {qty}x '{ex_id}' ({generator.topic})...")

            for i in range(qty):
                data = None
                problem = None
                
                # Fase C: Opción 1 - Intentar reutilizar del repositorio
                if (use_repository and 
                    self.problem_repository and 
                    HAS_MAPPERS and 
                    reuse_probability > 0 and 
                    random.random() < reuse_probability):
                    
                    try:
                        # Obtener mapper para este tipo
                        problem_type = self._get_problem_type_for_generator(ex_id)
                        if problem_type and problem_type in MAPPER_REGISTRY:
                            mapper = MAPPER_REGISTRY[problem_type]
                            
                            # Cargar del repositorio
                            problems = self.problem_repository.get_by_type(problem_type.value)
                            if problems:
                                selected_problem = random.choice(problems)
                                data = mapper.problem_to_exercise(selected_problem)
                                self.loaded_problems.append(selected_problem.id)
                                print(f"      [REUSE]  Reutilizado del repositorio: {selected_problem.id[:8]}...")
                    except Exception as e:
                        print(f"      [WARN]  No se pudo reutilizar: {e}")
                        data = None
                
                # RUTA 1: JSON Manual (sin aleatorización) - DEBUG/TESTING
                if data is None and 'problem_json' in req:
                    problem_dict = req['problem_json']
                    print(f"      [JSON] Usando JSON manual (sin aleatorización)")
                    
                    if hasattr(generator, 'generate_from_problem'):
                        # Usar generador directo
                        data = generator.generate_from_problem(problem_dict)
                    else:
                        # Fallback: usar generate legacy
                        data = generator.generate(difficulty=difficulty)
                
                # RUTA 2: Con Aleatorizador + Seed Controlable - PRODUCCIÓN
                elif data is None and 'randomizer_params' in req:
                    randomizer_params = req['randomizer_params']
                    randomizer_seed = randomizer_params.get('seed')
                    
                    if randomizer_seed is not None:
                        print(f"      [RAND] Generando con seed={randomizer_seed} (reproducible)")
                    else:
                        print(f"      [RAND] Generando sin seed (aleatorio)")
                    
                    # Buscar aleatorizador (por convención: mismo nombre + 'Randomizer')
                    randomizer_class_name = generator.__class__.__name__.replace('Generator', 'Randomizer')
                    
                    # Crear aleatorizador (aquí simplificado, mejorar después)
                    # TODO: Implementar registro de aleatorizadores similar a generadores
                    if hasattr(generator, '__class__'):
                        # Obtener módulo del generador
                        module = __import__(generator.__class__.__module__, fromlist=[randomizer_class_name])
                        if hasattr(module, randomizer_class_name):
                            randomizer_class = getattr(module, randomizer_class_name)
                            randomizer = randomizer_class(**randomizer_params.get('args', {}))
                            
                            # Generar problema aleatorio
                            problem = randomizer.randomize(seed=randomizer_seed)
                            
                            # Pasar al generador
                            if hasattr(generator, 'generate_from_problem'):
                                data = generator.generate_from_problem(problem)
                            else:
                                data = generator.generate(difficulty=difficulty)
                        else:
                            # Fallback
                            data = generator.generate(difficulty=difficulty)
                    else:
                        data = generator.generate(difficulty=difficulty)
                
                # RUTA 3: Generación Legacy (backward compatibility)
                if data is None:
                    data = generator.generate(difficulty=difficulty)
                
                self.exercises_data.append(data)
                
                # Fase C: Guardar en repositorio si está disponible
                if use_repository and self.problem_repository and HAS_MAPPERS and data is not None:
                    try:
                        problem_type = self._get_problem_type_for_generator(ex_id)
                        if problem_type and problem_type in MAPPER_REGISTRY:
                            mapper = MAPPER_REGISTRY[problem_type]
                            problem = mapper.exercise_to_problem(data)
                            problem_id = self.problem_repository.save(problem)
                            self.saved_problems.append(problem_id)
                            print(f"      [SAVE] Guardado en repositorio: {problem_id[:8]}...")
                    except Exception as e:
                        print(f"      [WARN]  No se guardó en repositorio: {e}")
                
                # Serializar a JSON agnóstico
                if hasattr(data, 'asdict'):
                    self.exercises_json.append(data.asdict())
                else:
                    # Fallback para ejercicios sin asdict()
                    self.exercises_json.append({
                        "title": getattr(data, 'title', ''),
                        "description": getattr(data, 'description', ''),
                        "data": str(data)
                    })

        return self.exercises_data
    
    def _get_problem_type_for_generator(self, ex_id: str) -> Optional[Any]:
        """
        Obtiene el tipo de Problem (ProblemType enum) para un generador.
        
        Mapeo: ex_id → ProblemType
        """
        if not HAS_MAPPERS:
            return None
        
        from models.problem_type import ProblemType
        
        # Mapeo de ex_id a ProblemType
        mapping = {
            'numeracion': ProblemType.NUMERACION,
            'conversion': ProblemType.NUMERACION,
            'karnaugh': ProblemType.KARNAUGH,
            'karnaugh_simplification': ProblemType.KARNAUGH,
            'logic': ProblemType.LOGIC,
            'logic_problem': ProblemType.LOGIC,
            'msi': ProblemType.MSI,
            'medium_scale_integration': ProblemType.MSI,
            'secuencial': ProblemType.SECUENCIAL,
            'sequential': ProblemType.SECUENCIAL,
            'sequential_logic': ProblemType.SECUENCIAL,
        }
        
        ex_id_lower = str(ex_id).lower()
        return mapping.get(ex_id_lower)
    
    def get_exercises_json(self) -> List[Dict[str, Any]]:
        """Devuelve los ejercicios en formato JSON agnóstico (salida intermedia)."""
        return self.exercises_json
    
    def save_intermediate_json(self, output_file: str = None) -> str:
        """
        Guarda el JSON intermedio agnóstico en un archivo.
        
        Este es el PRODUCTO PRINCIPAL de la generación.
        Los renderers consumen este JSON, no los objetos Python.
        
        Args:
            output_file: Ruta del archivo. Si es None, usa {config_title}_ejercicios.json
        
        Returns:
            Ruta del archivo guardado
        """
        if not self.exercises_json:
            raise RuntimeError("No hay ejercicios generados. Llama a build() primero.")
        
        if output_file is None:
            config_title = self.config.get("title", "exam").replace(" ", "_").lower()
            output_file = os.path.join("build", "json", f"{config_title}_ejercicios.json")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Preparar salida con metadata
        output = {
            "exam_metadata": {
                "title": self.config.get("title", "Sin título"),
                "description": self.config.get("description", ""),
                "seed": self.config.get("seed"),
                "total_exercises": len(self.exercises_json)
            },
            "exercises": self.exercises_json
        }
        
        # Guardar con formato legible
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"[SAVE] JSON intermedio guardado: {os.path.abspath(output_file)}")
        return output_file
    # ============== FASE C: MÉTODOS DE PERSISTENCIA ==============
    
    def get_persistence_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de persistencia (Fase C).
        
        Returns:
            Dict con:
            - has_repository: bool
            - saved_count: int
            - loaded_count: int
            - reuse_ratio: float (loaded / total)
            - repository_info: Dict (si existe repo)
        """
        total = len(self.exercises_data)
        saved = len(self.saved_problems)
        loaded = len(self.loaded_problems)
        
        return {
            'has_repository': self.problem_repository is not None,
            'saved_count': saved,
            'loaded_count': loaded,
            'generated_count': total - loaded,
            'reuse_ratio': loaded / total if total > 0 else 0.0,
            'total': total,
            'repository_info': self.problem_repository.info() if self.problem_repository else None
        }
    
    def print_persistence_report(self):
        """Imprime un reporte de persistencia."""
        stats = self.get_persistence_stats()
        
        print("\n" + "="*70)
        print("REPORTE DE PERSISTENCIA (FASE C)")
        print("="*70)
        
        if not stats['has_repository']:
            print("[FAIL] No hay repositorio configurado (use_repository=False)")
            return
        
        print(f"[OK] Repositorio: {stats['repository_info']['backend']}")
        print(f"   Ubicación: {stats['repository_info']['location']}")
        print(f"   Total en BD: {stats['repository_info']['total']}")
        print()
        print(f"[STATS] Estadísticas de este examen:")
        print(f"   • Total ejercicios: {stats['total']}")
        print(f"   • Generados nuevos: {stats['generated_count']}")
        print(f"   • Reutilizados del repo: {stats['loaded_count']}")
        print(f"   • Guardados en repo: {stats['saved_count']}")
        print(f"   • Tasa de reutilización: {stats['reuse_ratio']:.1%}")
        print("="*70 + "\n")
    
    def save_persistence_report(self, output_file: str = None) -> str:
        """
        Guarda el reporte de persistencia en un archivo JSON.
        
        Args:
            output_file: Ruta del archivo. Si None, usa config_title_persistencia.json
        
        Returns:
            Ruta del archivo guardado
        """
        stats = self.get_persistence_stats()
        
        if output_file is None:
            config_title = self.config.get("title", "exam").replace(" ", "_").lower()
            output_file = os.path.join("build", "json", f"{config_title}_persistencia.json")
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        report = {
            "exam_title": self.config.get("title", "Sin título"),
            "persistence_stats": stats,
            "saved_problem_ids": self.saved_problems,
            "loaded_problem_ids": self.loaded_problems,
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[SAVE] Reporte de persistencia guardado: {os.path.abspath(output_file)}")
        return output_file