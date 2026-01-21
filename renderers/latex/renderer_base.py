"""
Base renderer architecture: Pipeline de fases sucesivas.

ARQUITECTURA:
- Cada fase es un renderer independiente
- Entrada: JSON (datos del ejercicio)
- Salida: TEX (compilable + parcial) + JSON (para siguiente fase)
- Última fase: SOLO TEX

PATRÓN: Pipe & Filter (Dean & Ghemawat)

FLUJO:
  ejercicio.json
    ↓
  Phase1Renderer (estructura) → phase1.tex + phase1_output.json
    ↓
  Phase2Renderer (detalles X) → phase2.tex + phase2_output.json
    ↓
  Phase3Renderer (detalles Y) → phase3.tex + phase3_output.json
    ↓
  PhaseNRenderer (texto) → phaseN.tex (FINAL)
    ↓
  RendererPipeline
    └─ Compone: main.tex con \include{phase1.tex}...\include{phaseN.tex}
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path


@dataclass
class PhaseOutput:
    """Salida de una fase del renderer."""
    latex_content: str  # Contenido LaTeX compilable
    output_json: Optional[Dict[str, Any]] = None  # Para siguiente fase (None si es última)
    phase_name: str = "unnamed"
    tex_filename: str = "phase.tex"


class ExerciseRendererPhase(ABC):
    """
    CLASE BASE: Define interfaz para cada fase del pipeline de renderers.
    
    Similiar a ExerciseGenerator:
    - Es determinista: mismo JSON → mismo TEX
    - Separa responsabilidades
    - Produce salida compilable + comunicación con siguiente fase
    """
    
    @abstractmethod
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """
        Renderiza esta fase específica.
        
        Args:
            exercise_json: Datos del ejercicio (problema + solución)
            is_solution: Si es para soluciones o enunciado
        
        Returns:
            PhaseOutput: LaTeX compilable + JSON para siguiente fase
        
        RESPONSABILIDAD: Solo renderizar lo que corresponde a esta fase.
        No tocar lo que hace la siguiente.
        """
        pass
    
    @property
    @abstractmethod
    def phase_name(self) -> str:
        """Nombre de la fase (ej: 'estructura', 'detalles_x')."""
        pass
    
    def _extract_problem(self, exercise_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae solo los datos del problema."""
        return exercise_json.get('problem', {})
    
    def _extract_solution(self, exercise_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae solo los datos de la solución."""
        return exercise_json.get('solution', {})
    
    def _extract_metadata(self, exercise_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae metadata del ejercicio."""
        return exercise_json.get('metadata', {})


class RendererPipeline:
    """
    ORQUESTADOR: Encadena fases sucesivas de rendering.
    
    RESPONSABILIDADES:
    - Ejecutar fases en orden
    - Pasar JSON intermedio entre fases
    - Recolectar TEX de cada fase
    - Componer TEX final con \include{}
    - Guardar archivos intermedios (opcional)
    """
    
    def __init__(self, exercise_type: str, output_dir: str = "build/latex"):
        self.exercise_type = exercise_type
        self.output_dir = Path(output_dir)
        self.phases: List[ExerciseRendererPhase] = []
        self.phase_outputs: List[PhaseOutput] = []
    
    def add_phase(self, phase: ExerciseRendererPhase) -> "RendererPipeline":
        """Agregar una fase al pipeline (orden importa)."""
        self.phases.append(phase)
        return self  # Fluent interface
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> Tuple[str, List[str]]:
        """
        Renderiza el ejercicio a través de todas las fases.
        
        Args:
            exercise_json: Datos del ejercicio (problema + solución)
            is_solution: Si es para soluciones o enunciado
        
        Returns:
            (main_latex_code, list_of_phase_tex_files)
        """
        self.phase_outputs = []
        current_json = exercise_json
        
        print(f"🎨 Renderizando {self.exercise_type} ({len(self.phases)} fases)...")
        
        # Ejecutar cada fase
        for i, phase in enumerate(self.phases, 1):
            print(f"   Phase {i}/{len(self.phases)}: {phase.phase_name}...", end=" ")
            
            # Renderizar esta fase
            output = phase.render(current_json, is_solution=is_solution)
            self.phase_outputs.append(output)
            
            # Pasar JSON intermedio a siguiente fase
            if output.output_json is not None:
                current_json = output.output_json
            
            print("✅")
        
        # Componer LaTeX final
        tex_files = self._save_phase_files()
        main_tex = self._compose_main_tex(tex_files)
        
        return main_tex, tex_files
    
    def _save_phase_files(self) -> List[str]:
        """Guarda archivos TEX para cada fase."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        tex_files = []
        
        for output in self.phase_outputs:
            tex_file = self.output_dir / output.tex_filename
            tex_file.write_text(output.latex_content, encoding='utf-8')
            tex_files.append(output.tex_filename)
            print(f"      💾 Guardado: {tex_file}")
        
        return tex_files
    
    def _compose_main_tex(self, tex_files: List[str]) -> str:
        """
        Compone el LaTeX principal usando \include{} para cada fase.
        
        Este es el patrón del preprocesador C/C++:
        - main.tex incluye los archivos de cada fase
        - Cada fase es compilable independientemente
        - La composición final es limpia y modular
        """
        includes = "\n".join([f"\\include{{{tex_file.replace('.tex', '')}}}" for tex_file in tex_files])
        
        main_tex = f"""% Renderizado modular por fases
% Cada \\include{{}} corresponde a una fase del renderer pipeline

{includes}

% Composición final: cada fase contribuye su responsabilidad
"""
        return main_tex
    
    def save_main_file(self, filename: str = "main.tex") -> Path:
        """Guarda el archivo TEX principal."""
        if not self.phase_outputs:
            raise RuntimeError("No hay fases renderizadas. Llama a render() primero.")
        
        main_path = self.output_dir / filename
        tex_files = [o.tex_filename for o in self.phase_outputs]
        main_tex = self._compose_main_tex(tex_files)
        
        main_path.write_text(main_tex, encoding='utf-8')
        print(f"📄 Archivo principal guardado: {main_path}")
        return main_path


class SimpleRendererPhase(ExerciseRendererPhase):
    """
    Fase simple de ejemplo: solo para demostración.
    
    Genera comentario LaTeX con el contenido JSON.
    """
    
    def __init__(self, phase_name_str: str):
        self._phase_name = phase_name_str
    
    def render(self, exercise_json: Dict[str, Any], is_solution: bool = False) -> PhaseOutput:
        """Renderiza phase simple."""
        content = f"% Phase: {self._phase_name}\n"
        content += f"% Ejercicio: {exercise_json.get('title', 'Sin título')}\n"
        
        return PhaseOutput(
            latex_content=content,
            output_json=exercise_json,  # Pasar igual al siguiente
            phase_name=self._phase_name,
            tex_filename=f"{self._phase_name}.tex"
        )
    
    @property
    def phase_name(self) -> str:
        return self._phase_name
