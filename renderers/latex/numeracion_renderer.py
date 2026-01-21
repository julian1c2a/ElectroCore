from typing import Optional
from modules.numeracion.models import ConversionExerciseData, ArithmeticOp, COLUMN_NAMES

class NumeracionLatexRenderer:
    def __init__(self, is_solution: bool = False):
        self.is_solution = is_solution

    def render(self, data: ConversionExerciseData, index: int) -> str:
        latex = fr"\section*{{Ejercicio {index}: {data.title} ({data.n_bits} bits)}}" + "\n"
        
        # Enunciado con indicación de la columna activa
        active_systems = ", ".join(sorted(set(COLUMN_NAMES[row.target_col_idx] for row in data.rows)))
        latex += r"\begin{tcolorbox}[title=Enunciado]" + "\n"
        latex += fr"\noindent \textbf{{a)}} {data.description}\\" + "\n"
        latex += fr"\noindent Convierte a: \textbf{{{active_systems}}}. Si no es representable, escribe 'NR'." + "\n"
        latex += r"\end{tcolorbox}" + "\n\n"

        # Tabla
        latex += r"\textbf{Respuesta:}" + "\n"
        latex += r"\begin{table}[H] \centering \renewcommand{\arraystretch}{1.5}" + "\n"
        latex += r"\begin{tabular}{|c|c|C{2.8cm}|C{2.8cm}|C{2.8cm}|C{2.8cm}|} \hline" + "\n"
        latex += r"\rowcolor[gray]{0.9} \textbf{Id} & \textbf{Decimal} & \textbf{Binario Nat.} & \textbf{Compl. 2} & \textbf{Signo-Mag.} & \textbf{BCD} \\ \hline" + "\n"

        for row in data.rows:
            cells = [""] * 6
            cells[0] = f"{row.label})"

            if self.is_solution:
                # Mostrar TODOS los valores en rojo (soluciones completas)
                cells[1] = fr"\textcolor{{red}}{{{row.val_decimal}}}"
                cells[2] = fr"\textcolor{{red}}{{{row.sol_bin}}}"
                cells[3] = fr"\textcolor{{red}}{{{row.sol_c2}}}"
                cells[4] = fr"\textcolor{{red}}{{{row.sol_sm}}}"
                cells[5] = fr"\textcolor{{red}}{{{row.sol_bcd}}}"
            else:
                # Mostrar SOLO la columna activa (target_col_idx)
                # El alumno debe completar solo esta columna
                cells[1] = ""  # Columna decimal vacía para que escriba el alumno
                cells[row.target_col_idx + 2] = f"\\textbf{{{row.target_val_str}}}"  # +2 porque col 0=label, col 1=decimal
                # Las otras columnas quedan vacías

            latex += " & ".join(cells) + r" \\ \hline" + "\n"
        latex += r"\end{tabular} \end{table}" + "\n"

        # Parte B
        if data.operations:
            latex += r"\begin{tcolorbox}[title=Enunciado (Parte b)]" + "\n"
            latex += r"\noindent \textbf{b)} Realice las siguientes operaciones aritméticas." + "\n"
            latex += r"\end{tcolorbox}" + "\n"
            
            for i, op in enumerate(data.operations, 1):
                # Usamos minipage para evitar que una operación se corte entre páginas
                latex += r"\noindent \begin{minipage}{\linewidth}" + "\n"
                latex += fr"\par \vspace{{0.5cm}} \noindent \textbf{{{i}) {op.op_type} en {op.system}:}} Fila {op.operand1} {op.operator_symbol} Fila {op.operand2}" + "\n"
                latex += self._render_grid(data.n_bits, op if self.is_solution else None)

                # Checkboxes
                chk_ov = r"$\boxtimes$" if (self.is_solution and op.overflow) else r"$\square$"
                chk_un = r"$\boxtimes$" if (self.is_solution and op.underflow) else r"$\square$"
                
                latex += r"\par \vspace{0.2cm}" + "\n"
                latex += fr"\noindent \textit{{¿Overflow? {chk_ov} \hspace{{1cm}} ¿Underflow? {chk_un} \hspace{{1cm}} ¿Correcto? $\square$}}" + "\n"

                latex += r"\par \vspace{0.3cm}" + "\n"
                latex += r"\noindent \hspace{0.5cm} \textbf{¿Por qué?}" + "\n" 
                latex += r"\par \vspace{0.8cm}" + "\n"
                latex += r"\end{minipage}" + "\n"

        return latex

    def _render_grid(self, n_bits: int, op: Optional[ArithmeticOp]) -> str:
        cols = "r|" + "B|" * n_bits
        latex = r"\begin{center} \renewcommand{\arraystretch}{1.5}" + "\n"
        latex += fr"\begin{{tabular}}{{{cols}}}" + "\n"

        # Helper para rellenar celdas
        def fill_cells(val_str, color="red"):
            if not val_str: return [""] * n_bits
            # Asumimos val_str es binario de n_bits
            bits = list(val_str)
            if len(bits) > n_bits: bits = bits[-n_bits:] # Truncar si excede
            return [fr"\textcolor{{{color}}}{{{b}}}" for b in bits]

        # Datos para rellenar
        c_carry = fill_cells(op.carry_bits, "blue") if op else [""] * n_bits
        c_op1 = fill_cells(format(op.val1_dec if op.val1_dec >=0 else (1<<n_bits)+op.val1_dec, f'0{n_bits}b') if op else "")
        c_op2 = fill_cells(format(op.val2_dec if op.val2_dec >=0 else (1<<n_bits)+op.val2_dec, f'0{n_bits}b') if op else "")
        c_res = fill_cells(op.result_bin) if op else [""] * n_bits

        latex += r"\tiny{Acarreo} & " + " & ".join(c_carry) + r" \\ \cline{2-" + str(n_bits+1) + "}" + "\n"
        latex += r"Op. 1 & " + " & ".join(c_op1) + r" \\ \cline{2-" + str(n_bits+1) + "}" + "\n"
        latex += r"Op. 2 & " + " & ".join(c_op2) + r" \\ \hline \hline" + "\n"
        latex += r"\textbf{Res.} & " + " & ".join(c_res) + r" \\ \cline{2-" + str(n_bits+1) + "}" + "\n"

        latex += r"\end{tabular} \end{center}" + "\n"
        return latex
