from modules.secuencial.models import SequentialExerciseData

class DigitalCircuitRenderer:
    def render_mux(self) -> str:
        return r"""
\begin{center} \begin{tikzpicture}
    % Cuerpo del MUX (Trapecio)
    \draw[thick] (0,0) -- (0,8) -- (4,6) -- (4,2) -- (0,0) -- cycle;
    \node at (2,4) {\textbf{MUX 16:1}};
    
    % Entradas de datos (I0 - I15)
    \foreach \y in {0.5,1,...,7.5} \draw (-0.5,\y) -- (0,\y);
    \node[left] at (-0.5, 7.5) {I0};
    \node[left] at (-0.5, 0.5) {I15};
    
    % Salida Y
    \draw (4,4) -- (5,4) node[right]{Y};
    
    % Enable (E negado)
    \draw (3.5, -0.5) -- (3.5, 2.8); 
    \node[below] at (3.5,-0.5) {$\overline{E}$};
    
    % Entradas de Selección (S3..S0)
    \foreach \x/\lbl in {0.8/S3, 1.6/S2, 2.4/S1, 3.2/S0} {
        \draw (\x, -0.5) -- (\x, {0.5*\x}); 
        \node[below] at (\x, -0.5) {\lbl};
    }
\end{tikzpicture} \end{center}
"""

    def render_comparator(self, params: dict) -> str:
        vals = params['cascada']
        return fr"""
\begin{{center}} \begin{{tikzpicture}}
    \draw[thick] (0,0) rectangle (4,4);
    \node at (2,3.5) {{\textbf{{COMPARADOR}}}}; \node at (2,0.5) {{\textbf{{4 BITS}}}};
    
    % Entradas A y B (Buses)
    \draw[ultra thick] (-1.2, 3) -- (0,3); \node[left] at (-1.2, 3) {{A}}; 
    \node[above] at (-0.6, 3.1) {{\scriptsize 4}}; \draw[thick] (-0.7, 2.8) -- (-0.5, 3.2);
    
    \draw[ultra thick] (-1.2, 1) -- (0,1); \node[left] at (-1.2, 1) {{B}}; 
    \node[above] at (-0.6, 1.1) {{\scriptsize 4}}; \draw[thick] (-0.7, 0.8) -- (-0.5, 1.2);
    
    % Salidas
    \draw (4,3) -- (5,3) node[right]{{$>$}}; 
    \draw (4,2) -- (5,2) node[right]{{$=$}}; 
    \draw (4,1) -- (5,1) node[right]{{$<$}};
    
    % Entradas de cascada
    \draw (-1, 2.4) -- (0, 2.4); \node[left] at (-1, 2.4) {{\small $I_{{gr}}={vals[0]}$}};
    \draw (-1, 2.0) -- (0, 2.0); \node[left] at (-1, 2.0) {{\small $I_{{eq}}={vals[1]}$}};
    \draw (-1, 1.6) -- (0, 1.6); \node[left] at (-1, 1.6) {{\small $I_{{le}}={vals[2]}$}};
\end{{tikzpicture}} \end{{center}}
"""

    def render_adder(self, params: dict) -> str:
        return fr"""
\begin{{center}} \begin{{tikzpicture}}
    \draw[thick] (0,0) rectangle (4,4);
    
    % Sigma (Arriba)
    \node at (2,3.25) {{\Huge $\Sigma$}};
    % Texto descriptivo (Abajo)
    \node at (2,1.0) {{\textbf{{SUMADOR 4 BITS}}}};
    
    % Entradas A (Bus) en Y=3.0
    \draw[ultra thick] (-1.2, 3.0) -- (0,3.0); 
    \node[left] at (-1.2, 3.0) {{A}}; 
    \node[above] at (-0.6, 3.1) {{\scriptsize 4}}; 
    \draw[thick] (-0.7, 2.8) -- (-0.5, 3.2);
    
    % Entradas B (Bus) en Y=2.0
    \draw[ultra thick] (-1.2, 2.0) -- (0,2.0); 
    \node[left] at (-1.2, 2.0) {{B}}; 
    \node[above] at (-0.6, 2.1) {{\scriptsize 4}}; 
    \draw[thick] (-0.7, 1.8) -- (-0.5, 2.2);
    
    % Carry In (Parte izquierda abajo)
    \draw (-1, 0.5) -- (0, 0.5) node[midway, above]{{Cin}};
    
    % Salida S (Bus) en Y=2.5 (Punto medio)
    \draw[ultra thick] (4,2.5) -- (5.2,2.5); \node[right] at (5.2, 2.5) {{S}};
    \node[above] at (4.6, 2.6) {{\scriptsize 4}}; \draw[thick] (4.5, 2.3) -- (4.7, 2.7);
    
    % Carry Out (Cout) en Y=0.5 (Alineado con Cin)
    \draw (4,0.5) -- (5,0.5) node[right]{{Cout}};
\end{{tikzpicture}} \end{{center}}
"""

    def render_sequential_circuit(self, data: SequentialExerciseData) -> str:
        ff = data.ff_type
        ff_style = f"flipflop {ff}"
        
        # Determinar el pin de reloj según el tipo de FF
        # JK: pin 2 (centro)
        # T/D: pin 3 (abajo)
        clk_pin = "pin 2" if ff == 'JK' else "pin 3"
        
        code = r"\begin{center} " + "\n"
        code += r"	\begin{circuitikz}[scale=1.2, transform shape]" + "\n"
        code += r"        \draw" + "\n"
        
        # Flip Flops
        code += fr"            (0,0) node[{ff_style}, external pins width=0](FF1){{Q0}}" + "\n"
        code += fr"            (5,0) node[{ff_style}, external pins width=0](FF2){{Q1}};" + "\n"
        
        # Dibujar círculo de negación manualmente si es bajada
        if data.edge_type == "Bajada":
            code += fr"        \draw (FF1.{clk_pin}) ++(-0.1,0) circle(0.1);" + "\n"
            code += fr"        \draw (FF2.{clk_pin}) ++(-0.1,0) circle(0.1);" + "\n"
            clk_offset = "-0.2"
        else:
            clk_offset = "0"

        # Clock Bus (Estructura relativa mejorada)
        code += fr"        \draw (FF1.{clk_pin}) ++({clk_offset},0) -- ++(-0.5,0) -- ++(0,-2.0) coordinate(clk_bus);" + "\n"
        code += fr"        \draw (FF2.{clk_pin}) ++({clk_offset},0) -- ++(-0.5,0) -- ++(0,-2.0) -- (clk_bus);" + "\n"
        code += r"        \draw (clk_bus) -- ++(-0.5,0) node[left]{CLK};" + "\n"

        # Lógica específica (Shift vs Counter)
        if data.logic_type == 'SHIFT':
            code += r"        \draw (FF1.pin 1) -- ++(-1,0) node[left]{E};" + "\n"
            code += r"        \draw (FF1.pin 6) -- (FF2.pin 1);" + "\n"
        else: # COUNTER
            if ff == 'JK':
                code += r"        \draw (FF1.pin 1) -- ++(-0.5,0) coordinate(j1) -- ++(-0.5,0) node[left]{E};" + "\n"
                code += r"        \draw (FF1.pin 3) -- ++(-0.5,0) -- (j1);" + "\n"
                code += r"        \draw (FF1.pin 6) -- ++(0.5,0) coordinate(q0) -- (FF2.pin 1);" + "\n"
                code += r"        \draw (q0) -- ++(0,-0.5) -- ++(1.5,0) -- (FF2.pin 3);" + "\n"
            elif ff == 'T':
                code += r"        \draw (FF1.pin 1) -- ++(-1,0) node[left]{E};" + "\n"
                code += r"        \draw (FF1.pin 6) -- (FF2.pin 1);" + "\n"
        
        # Salidas Q (Desplazadas a la derecha antes de subir)
        code += r"        \draw (FF1.pin 6) -- ++(0.5, 0) -- ++(0, 1.5) node[above]{Q0};" + "\n"
        code += r"        \draw (FF2.pin 6) -- ++(0.5, 0) -- ++(0, 1.5) node[above]{Q1};" + "\n"

        # Asíncrono
        if data.has_async:
            pin = "up" if data.async_type in ['Set', 'Preset'] else "down"
            y_dir = "0.5" if pin == "up" else "-0.5"
            code += fr"        \draw (FF1.{pin}) -- ++(0,{y_dir}) coordinate(a);" + "\n"
            code += fr"        \draw (FF2.{pin}) -- ++(0,{y_dir}) -- (a);" + "\n"
            code += fr"        \draw (a) -- ++(0,{y_dir}) node[above]{{{data.async_type}}};" + "\n"

        code += r"    \end{circuitikz} " + "\n"
        code += r"\end{center}"
        return code
