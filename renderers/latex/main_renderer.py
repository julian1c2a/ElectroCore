import json
import os
from typing import List
from core.generator_base import ExerciseData
from modules.numeracion.models import ConversionExerciseData
from modules.combinacional.models import KarnaughExerciseData, LogicProblemExerciseData, MSIExerciseData
from modules.secuencial.models import SequentialExerciseData
from renderers.latex.numeracion_renderer import NumeracionLatexRenderer
from renderers.latex.combinacional_renderer import CombinacionalLatexRenderer
from renderers.latex.secuencial_renderer import SecuencialLatexRenderer

class LatexExamRenderer:
    def __init__(self, is_solution: bool = False):
        self.is_solution = is_solution
        self.numeracion_renderer = NumeracionLatexRenderer(is_solution)
        self.combinacional_renderer = CombinacionalLatexRenderer(is_solution)
        self.secuencial_renderer = SecuencialLatexRenderer(is_solution)
        
        self.header_config = self._load_json(os.path.join("config", "header.json"))
        self.scoring_config = self._load_json(os.path.join("config", "scoring.json"))

    def _load_json(self, filename: str) -> dict:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def render(self, exercises: List[ExerciseData]) -> str:
        latex = self._get_preamble()
        
        for i, ex_data in enumerate(exercises, 1):
            if isinstance(ex_data, ConversionExerciseData):
                latex += self.numeracion_renderer.render(ex_data, i)
            elif isinstance(ex_data, (KarnaughExerciseData, LogicProblemExerciseData, MSIExerciseData)):
                latex += self.combinacional_renderer.render(ex_data, i)
            elif isinstance(ex_data, SequentialExerciseData):
                latex += self.secuencial_renderer.render(ex_data, i)
            else:
                latex += f"\\section*{{Ejercicio {i}: Tipo desconocido}}\n"
                latex += f"No hay renderizador para {type(ex_data).__name__}\n"
        
        latex += self._get_footer()
        return latex

    def _get_preamble(self) -> str:
        h = self.header_config
        logo = h.get("logo_path", "")
        full_exam_title = h.get('exam_title', '')
        if h.get('exam_type'): full_exam_title += fr" - {h.get('exam_type')}"
        
        if self.is_solution:
            full_exam_title += r" \textcolor{red}{(SOLUCIÓN)}"
            
        right_header = fr"\textbf{{{h.get('subject', '')}}}"
        if h.get('semester'): right_header += fr" \\ {h.get('semester')}"
        if h.get('term'): right_header += fr" \\ {h.get('term')}"
        date_str = h.get('date', '')

        # Lógica para mostrar profesores
        show_prof = h.get("show_professors", False)
        # Aceptamos booleanos o strings "si"/"yes"
        if isinstance(show_prof, str) and show_prof.lower() in ["si", "yes", "true"]:
            show_prof = True
            
        cfoot_content = fr"{{\small {h.get('professors', '')}}}" if show_prof else ""

        return fr"""\documentclass[a4paper,11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[spanish]{{babel}}
\usepackage[top=2.5cm, bottom=2.5cm, left=2cm, right=2cm, headheight=2cm]{{geometry}}
\usepackage{{tikz}}
\usepackage{{circuitikz}}
\usepackage{{tikz-timing}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{array}}
\usepackage{{multirow}}
\usepackage{{colortbl}}
\usepackage{{enumitem}}
\usepackage{{float}}
\usepackage{{tcolorbox}}
\usepackage{{graphicx}}
\usepackage{{fancyhdr}}
\usepackage{{lastpage}}
\usepackage{{diagbox}}
\usepackage{{xcolor}}

\usetikzlibrary{{calc}}
\tcbset{{colback=gray!5!white, colframe=gray!75!black, title=\textbf{{ENUNCIADO}}, fonttitle=\bfseries, boxrule=0.5mm, arc=2mm}}

\newcolumntype{{C}}[1]{{>{{\centering\arraybackslash}}p{{#1}}}}
\newcolumntype{{B}}{{>{{\centering\arraybackslash}}p{{0.5cm}}}}

\pagestyle{{fancy}}
\fancyhf{{}}
\renewcommand{{\headrulewidth}}{{0.4pt}}
\renewcommand{{\footrulewidth}}{{0.4pt}}

\lhead{{\includegraphics[height=1.5cm]{{{logo}}}}}
\chead{{\textbf{{{h.get('university', '')}}} \\ {h.get('department', '')}}}
\rhead{{{right_header}}}

\lfoot{{\small {full_exam_title}}}
\cfoot{{{cfoot_content}}}
\rfoot{{\small Página \thepage\ de \pageref{{LastPage}}}}

\begin{{document}}

\begin{{center}}
    {{\LARGE \textbf{{{full_exam_title}}}}} \\ \vspace{{0.2cm}}
    {{\Large \textbf{{{date_str}}}}}
\end{{center}}

\vspace{{0.5cm}}
\noindent \textbf{{Apellido y Nombre:}} ............................................................................ \hfill \textbf{{Grupo:}} ....................
\vspace{{0.5cm}} \hrule \vspace{{0.5cm}}
"""

    def _get_footer(self) -> str:
        return r"\end{document}"
