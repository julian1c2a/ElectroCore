from modules.secuencial.models import SequentialExerciseData

class TimingDiagramRenderer:
    def render(self, data: SequentialExerciseData) -> str:
        # Formateo basado en la plantilla definitiva de resources/latex/ej5_seq_timing.tex
        # Usamos espacios en lugar de \t para evitar problemas con LaTeX

        indent = "    " # 4 espacios

        # Construcción de filas
        rows = []
        rows.append(fr"{indent}{indent}CLK & {data.clk_sequence} \\")
        
        if data.has_async:
            rows.append(fr"{indent}{indent}{data.async_type}(asyn) & {data.async_sequence} \\")
            
        rows.append(fr"{indent}{indent}E & {data.input_sequence} \\")
        rows.append(fr"{indent}{indent}Q0 & [draw=none, fill=none] {data.output_placeholder} \\")
        rows.append(fr"{indent}{indent}Q1 & [draw=none, fill=none] {data.output_placeholder} \\")
        
        rows_str = "\n".join(rows)

        return fr"""\begin{{flushleft}}
{indent}% arraystretch=0 elimina el padding proporcional.
{indent}\renewcommand{{\arraystretch}}{{0}}
{indent}% extrarowheight negativo elimina altura fija extra.
{indent}\setlength{{\extrarowheight}}{{0pt}}
	
{indent}\begin{{tikztimingtable}}[
{indent}{indent}timing/slope=0,
{indent}{indent}timing/xunit=0.60cm,
{indent}{indent}timing/yunit=0.35cm,
{indent}{indent}timing/coldist=2pt
{indent}]
{rows_str}
{indent}{indent}\extracode \tablegrid
{indent}\end{{tikztimingtable}}
\end{{flushleft}}
"""
