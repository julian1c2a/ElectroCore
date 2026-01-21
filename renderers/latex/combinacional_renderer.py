from modules.combinacional.models import KarnaughExerciseData, LogicProblemExerciseData, MSIExerciseData
from renderers.latex.utils.truth_table import TruthTableRenderer
from renderers.latex.utils.karnaugh import KarnaughMapRenderer
from renderers.latex.utils.circuit import DigitalCircuitRenderer
from renderers.latex.utils.asset_manager import LatexAssetManager

class CombinacionalLatexRenderer:
    def __init__(self, is_solution: bool = False):
        self.is_solution = is_solution
        self.tt_renderer = TruthTableRenderer()
        self.kmap_renderer = KarnaughMapRenderer()
        self.circuit_renderer = DigitalCircuitRenderer()
        self.asset_manager = LatexAssetManager()

    def render(self, data: object, index: int) -> str:
        # Marcador de inicio de ejercicio
        latex = "\n" + "%" * 60 + "\n"
        latex += f"% >>>>>> INICIO EJERCICIO {index}: {data.title} <<<<<<\n"
        latex += "%" * 60 + "\n"

        if isinstance(data, KarnaughExerciseData):
            return latex + self._render_karnaugh(data, index)
        elif isinstance(data, LogicProblemExerciseData):
            return latex + self._render_problem(data, index)
        elif isinstance(data, MSIExerciseData):
            return latex + self._render_msi(data, index)
        return ""

    def _render_karnaugh(self, data: KarnaughExerciseData, index: int) -> str:
        latex = fr"\newpage \section*{{Ejercicio {index}: {data.title}}}" + "\n"
        latex += r"\begin{tcolorbox}[title=Enunciado]" + "\n"
        latex += fr"\noindent {data.description}" + "\n"

        latex += self.tt_renderer.render(data.vars_name, data.out_name, data.truth_table_outputs)

        latex += r"\noindent Se pide:" + "\n"
        latex += r"\begin{enumerate}[label=\alph*)]" + "\n"
        latex += fr"\item Obtener la expresión canónica ({data.canon_type})." + "\n"
        latex += r"\item Simplificar por Karnaugh." + "\n"
        latex += fr"\item Implementar con puertas \textbf{{{data.gate_type}}}." + "\n"
        latex += r"\end{enumerate} \end{tcolorbox}" + "\n"

        latex += r"\textbf{Espacio de Resolución:}" + "\n"
        
        # Usar Asset Manager para el Mapa de Karnaugh
        vars_left = "".join(data.vars_name[:2])
        vars_top = "".join(data.vars_name[2:])
        
        generator_func = lambda: self.kmap_renderer.render_template(vars_left, vars_top, data.out_name)
        latex += self.asset_manager.get_component(f"ej{index}_kmap", generator_func)
        
        latex += r"\vspace{3cm}" + "\n"
        return latex

    def _render_problem(self, data: LogicProblemExerciseData, index: int) -> str:
        latex = fr"\newpage \section*{{Ejercicio {index}: {data.title}}}" + "\n"
        latex += r"\begin{tcolorbox}[title=Enunciado]" + "\n"
        latex += fr"\textbf{{Contexto: {data.context_title}}}" + "\n"
        latex += r"\begin{itemize}" + "\n"
        for v in data.variables_desc: latex += fr"\item {v}" + "\n"
        latex += fr"\item Salida: {data.output_desc}" + "\n"
        latex += r"\end{itemize}" + "\n"
        latex += fr"\textit{{Lógica: {data.logic_description}}}" + "\n"
        latex += r"\end{tcolorbox}" + "\n"

        latex += r"\textbf{1. Tabla de Verdad:}" + "\n"
        latex += self.tt_renderer.render(data.vars_clean, data.out_clean, None)
        
        latex += r"\newpage \textbf{2. Mapa de Karnaugh:}" + "\n"
        
        l_izq = "".join(data.vars_clean[:2])
        l_sup = "".join(data.vars_clean[2:])
        
        generator_func = lambda: self.kmap_renderer.render_template(l_izq, l_sup, data.out_clean)
        latex += self.asset_manager.get_component(f"ej{index}_problem_kmap", generator_func)
        
        latex += r"\vspace{1cm}" + "\n"
        latex += r"\noindent \textbf{3. Esquema Lógico:}" + "\n"
        latex += r"\vspace{4cm}" + "\n"
        return latex

    def _render_msi(self, data: MSIExerciseData, index: int) -> str:
        latex = fr"\newpage \section*{{Ejercicio {index}: {data.title}}}" + "\n"
        latex += r"\begin{tcolorbox}[title=Enunciado]" + "\n"
        latex += fr"{data.description}" + "\n"
        
        component_id = f"ej{index}_msi_{data.block_type.lower()}"
        
        if data.block_type == 'MUX':
            gen_func = lambda: self.circuit_renderer.render_mux()
        elif data.block_type == 'COMPARADOR':
            gen_func = lambda: self.circuit_renderer.render_comparator(data.params)
        elif data.block_type == 'SUMADOR':
            gen_func = lambda: self.circuit_renderer.render_adder(data.params)
        else:
            gen_func = lambda: "% Tipo desconocido"

        latex += self.asset_manager.get_component(component_id, gen_func)

        if data.block_type == 'MUX':
            latex += fr"Entradas I0-I15: {data.params['inputs']} \\ Determine Y para:" + "\n"
            latex += r"\begin{enumerate}" + "\n"
            for case in data.params['cases']:
                latex += fr"\item Enable={case['ena']}, Dir={case['addr']:04b}" + "\n"
            latex += r"\end{enumerate}" + "\n"
        elif data.block_type == 'COMPARADOR':
            latex += fr"\noindent Determine las salidas ($>, =, <$) para las entradas: \\" + "\n"
            latex += fr"\textbf{{A}} = {data.params['A']} ({data.params['A']:04b}), \textbf{{B}} = {data.params['B']} ({data.params['B']:04b})" + "\n"
        elif data.block_type == 'SUMADOR':
            latex += fr"\noindent Determine la salida S y el acarreo de salida Cout para: \\" + "\n"
            latex += fr"\textbf{{A}} = {data.params['A']} ({data.params['A']:04b}), \textbf{{B}} = {data.params['B']} ({data.params['B']:04b}) \\" + "\n"
            latex += r"(Analice para \textbf{Cin=0} y \textbf{Cin=1})" + "\n"

        latex += r"\end{tcolorbox} \vspace{5cm}" + "\n"
        return latex
