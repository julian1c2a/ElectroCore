from typing import List, Optional

class KarnaughMapRenderer:
    def render_template(self, vars_left: str, vars_top: str, output_label: str, values: Optional[List[int]] = None) -> str:
        # Mapeo de índices para 4 variables (Gray Code)
        map_indices = [
            [0,  1,  3,  2],   # AB=00
            [4,  5,  7,  6],   # AB=01
            [12, 13, 15, 14],  # AB=11
            [8,  9,  11, 10]   # AB=10
        ]
        
        rows_content = []
        row_labels_natural = ["00", "01", "10", "11"]
        row_labels_gray    = ["00", "01", "11", "10"]
        
        for i in range(4):
            row_cells = []
            for j in range(4):
                idx = map_indices[i][j]
                val = ""
                if values and idx < len(values):
                    val = fr"\textbf{{{values[idx]}}}"
                row_cells.append(val)
            
            row_str = fr" & {row_labels_natural[i]} & {row_labels_gray[i]} & " + " & ".join(row_cells) + r" \\ \cline{2-7}"
            rows_content.append(row_str)

        latex = r"\begin{center}" + "\n"
        latex += r"\begin{table}[H] \centering \renewcommand{\arraystretch}{2}" + "\n"
        latex += r"\begin{tabular}{|c|c|c|c|c|c|c|} \hline" + "\n"
        
        latex += fr"\multicolumn{{3}}{{|c|}}{{\multirow{{3}}*{{\Huge \textbf{{{output_label}}}}}}} & \multicolumn{{4}}{{c|}}{{\textbf{{{vars_top} =}}}} \\ \cline{{4-7}}" + "\n"
        latex += r"\multicolumn{3}{|c|}{} & 00 & 01 & 10 & 11 \\ \cline{4-7}" + "\n"
        latex += r"\multicolumn{3}{|c|}{} & 00 & 01 & 11 & 10 \\ \hline" + "\n"
        
        first_row = rows_content[0]
        latex += fr"\multirow{{4}}*{{\rotatebox{{90}}{{\textbf{{{vars_left} =}}}}}}" + first_row + "\n"
        
        for row in rows_content[1:]:
            latex += row + "\n"
            
        latex += r"\hline" + "\n"
        latex += r"\end{tabular} \end{table}" + "\n"
        latex += r"\end{center}" + "\n"
        
        return latex
