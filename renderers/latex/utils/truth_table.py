from typing import List, Optional

class TruthTableRenderer:
    def render(self, headers: List[str], output_label: str, output_values: Optional[List[int]]) -> str:
        n_vars = len(headers)
        n_rows = 2 ** n_vars
        cols_format = "|" + "c|" * (n_vars + 1)
        
        latex = fr"\begin{{table}}[H] \centering \renewcommand{{\arraystretch}}{{1.2}}" + "\n"
        latex += fr"\begin{{tabular}}{{{cols_format}}} \hline" + "\n"
        
        header_cells = [fr"\textbf{{{h}}}" for h in headers] + [fr"\textbf{{{output_label}}}"]
        latex += r"\rowcolor[gray]{0.9} " + " & ".join(header_cells) + r" \\ \hline" + "\n"
        
        for i in range(n_rows):
            bin_str = format(i, f'0{n_vars}b')
            input_cells = list(bin_str)
            
            if output_values and i < len(output_values):
                out_val = fr"\textbf{{{output_values[i]}}}"
            else:
                out_val = " "
            
            row_cells = input_cells + [out_val]
            latex += " & ".join(row_cells) + r" \\ \hline" + "\n"
            
        latex += r"\end{tabular} \end{table}" + "\n"
        return latex
