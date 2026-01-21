from modules.secuencial.models import SequentialExerciseData
from renderers.latex.utils.circuit import DigitalCircuitRenderer
from renderers.latex.utils.timing import TimingDiagramRenderer
from renderers.latex.utils.asset_manager import LatexAssetManager

class SecuencialLatexRenderer:
    def __init__(self, is_solution: bool = False):
        self.is_solution = is_solution
        self.circuit_renderer = DigitalCircuitRenderer()
        self.timing_renderer = TimingDiagramRenderer()
        self.asset_manager = LatexAssetManager()

    def render(self, data: SequentialExerciseData, index: int) -> str:
        # Marcador de inicio
        latex = "\n" + "%" * 60 + "\n"
        latex += f"% >>>>>> INICIO EJERCICIO {index}: {data.title} <<<<<<\n"
        latex += "%" * 60 + "\n"
        
        latex += fr"\newpage \section*{{Ejercicio {index}: {data.title}}}" + "\n"
        
        edge_txt = "Subida" if data.edge_type == "Subida" else "Bajada"
        async_txt = f"Async \\textbf{{{data.async_type}(asyn)}} a nivel {data.async_level}" if data.has_async else "Sin Async"

        latex += r"\begin{tcolorbox}[title=Enunciado]" + "\n"
        latex += fr"Síncrono ({data.logic_type}) por {edge_txt}. FF {data.ff_type}. {async_txt}." + "\n"

        # Circuito (Asset Manager)
        circuit_id = f"ej{index}_seq_circuit"
        circuit_gen = lambda: self.circuit_renderer.render_sequential_circuit(data)
        latex += self.asset_manager.get_component(circuit_id, circuit_gen)
        
        latex += r"\end{tcolorbox}" + "\n"

        # Cronograma (Asset Manager)
        timing_id = f"ej{index}_seq_timing"
        timing_gen = lambda: self.timing_renderer.render(data)
        latex += self.asset_manager.get_component(timing_id, timing_gen)
        
        latex += r"\vspace{0.5cm}" + "\n"
        latex += r"\noindent \textbf{Se pide:}" + "\n"
        latex += r"\begin{enumerate}[label=\alph*)]" + "\n"
        latex += r"\item Completar el cronograma (salidas Q0, Q1)." + "\n"
        latex += r"\item Determinar la secuencia de estados." + "\n"
        latex += r"\end{enumerate}" + "\n"
        
        return latex
