"""
FixedPointComparator: Genera tablas comparativas de representaciones de punto fijo.

Renderiza comparativas en múltiples formatos:
- LaTeX (tablas para documentos PDF)
- HTML (tablas para web)
- JSON (exportación de datos)
- Plain text (visualización rápida)

Ejemplo:
    >>> from core.punto_fijo_unified import FixedPointUnified
    >>> from core.punto_fijo_comparator import FixedPointComparator
    >>> 
    >>> fp_unsigned = FixedPointUnified(E=4, F=4, base=2, signed=False)
    >>> fp_ms = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='ms')
    >>> fp_complement = FixedPointUnified(E=4, F=4, base=2, signed=True, representation='complement')
    >>> 
    >>> comparator = FixedPointComparator()
    >>> print(comparator.render_text([fp_unsigned, fp_ms, fp_complement]))
    >>> latex = comparator.render_latex([fp_unsigned, fp_ms, fp_complement])
    >>> html = comparator.render_html([fp_unsigned, fp_ms, fp_complement])
    >>> json_data = comparator.export_json([fp_unsigned, fp_ms, fp_complement])
"""

import json
from typing import List, Dict, Tuple
from dataclasses import asdict
from core.punto_fijo_unified import FixedPointUnified


class FixedPointComparator:
    """Compara y renderiza representaciones de punto fijo."""
    
    def __init__(self):
        """Inicializar comparador."""
        self.fps: List[FixedPointUnified] = []
    
    def compare_range(self, fp1: FixedPointUnified, fp2: FixedPointUnified) -> Dict:
        """
        Compara el rango de dos representaciones.
        
        Returns:
            dict con min, max, epsilon, total_values representable
        """
        return {
            'fp1': {
                'min': fp1.min_value,
                'max': fp1.max_value,
                'epsilon': fp1.epsilon,
                'range_span': fp1.max_value - fp1.min_value,
            },
            'fp2': {
                'min': fp2.min_value,
                'max': fp2.max_value,
                'epsilon': fp2.epsilon,
                'range_span': fp2.max_value - fp2.min_value,
            },
            'difference': {
                'min_diff': fp2.min_value - fp1.min_value,
                'max_diff': fp2.max_value - fp1.max_value,
                'epsilon_ratio': fp2.epsilon / fp1.epsilon if fp1.epsilon != 0 else float('inf'),
            }
        }
    
    def get_characteristics(self, fp: FixedPointUnified) -> Dict:
        """Obtiene características principales de una representación."""
        return {
            'E': fp.E,
            'F': fp.F,
            'base': fp.base,
            'signed': fp.signed,
            'representation': fp.representation if fp.signed else 'N/A',
            'total_bits': fp.total_bits,
            'min_value': fp.min_value,
            'max_value': fp.max_value,
            'epsilon': fp.epsilon,
            'range_span': fp.max_value - fp.min_value,
        }
    
    def _format_number(self, value: float, precision: int = 6) -> str:
        """Formatea número para tablas."""
        if value == int(value):
            return str(int(value))
        return f"{value:.{precision}f}".rstrip('0').rstrip('.')
    
    def render_text(self, fps: List[FixedPointUnified]) -> str:
        """
        Renderiza comparativa en texto plano (ASCII).
        
        Args:
            fps: lista de FixedPointUnified
            
        Returns:
            tabla en formato texto
        """
        lines = []
        lines.append("\n" + "="*120)
        lines.append("COMPARATIVA DE REPRESENTACIONES DE PUNTO FIJO")
        lines.append("="*120 + "\n")
        
        # Encabezados
        header = f"{'ID':<4} {'E.F Base':<12} {'Tipo':<20} {'Rango Mín':<15} {'Rango Máx':<15} {'Epsilon':<15} {'Bits':<6}"
        lines.append(header)
        lines.append("-"*120)
        
        # Datos
        for i, fp in enumerate(fps, 1):
            tipo = "Sin signo" if not fp.signed else f"{fp.representation.upper()}"
            config = f"{fp.E}.{fp.F} B{fp.base}"
            min_str = self._format_number(fp.min_value)
            max_str = self._format_number(fp.max_value)
            eps_str = self._format_number(fp.epsilon)
            
            line = f"{i:<4} {config:<12} {tipo:<20} {min_str:<15} {max_str:<15} {eps_str:<15} {fp.total_bits:<6}"
            lines.append(line)
        
        lines.append("-"*120 + "\n")
        
        # Tabla de características adicionales
        if len(fps) <= 4:  # Solo si hay pocas para no saturar
            lines.append("\nDETALLES ADICIONALES:")
            lines.append("-"*120)
            for i, fp in enumerate(fps, 1):
                chars = self.get_characteristics(fp)
                lines.append(f"\nRepresentación {i}:")
                for key, value in chars.items():
                    lines.append(f"  {key:<20}: {self._format_number(value) if isinstance(value, float) else value}")
        
        return "\n".join(lines)
    
    def render_latex(self, fps: List[FixedPointUnified]) -> str:
        """
        Renderiza comparativa en formato LaTeX.
        
        Args:
            fps: lista de FixedPointUnified
            
        Returns:
            código LaTeX de tabla
        """
        lines = []
        
        # Encabezado
        lines.append("\\begin{table}[h]")
        lines.append("\\centering")
        lines.append("\\caption{Comparativa de Representaciones de Punto Fijo}")
        lines.append("\\label{tab:fixedpoint-comparison}")
        lines.append("\\begin{tabular}{|l|c|c|c|c|c|c|}")
        lines.append("\\hline")
        lines.append("\\textbf{ID} & \\textbf{Configuración} & \\textbf{Tipo} & \\textbf{Rango Mín} & "
                    "\\textbf{Rango Máx} & \\textbf{$\\epsilon$} & \\textbf{Bits} \\\\")
        lines.append("\\hline")
        
        # Datos
        for i, fp in enumerate(fps, 1):
            tipo = "Sin signo" if not fp.signed else f"{fp.representation.upper()}"
            config = f"Q({fp.E},{fp.F}) B{fp.base}"
            min_str = self._format_number(fp.min_value, 4)
            max_str = self._format_number(fp.max_value, 4)
            eps_str = self._format_number(fp.epsilon, 6)
            
            line = (f"{i} & ${config}$ & {tipo} & ${min_str}$ & ${max_str}$ & "
                   f"${eps_str}$ & {fp.total_bits} \\\\")
            lines.append(line)
        
        lines.append("\\hline")
        lines.append("\\end{tabular}")
        lines.append("\\end{table}")
        
        return "\n".join(lines)
    
    def render_html(self, fps: List[FixedPointUnified]) -> str:
        """
        Renderiza comparativa en formato HTML.
        
        Args:
            fps: lista de FixedPointUnified
            
        Returns:
            código HTML de tabla
        """
        lines = []
        
        lines.append("<table class='comparison-table' border='1' cellpadding='10'>")
        lines.append("  <caption>Comparativa de Representaciones de Punto Fijo</caption>")
        lines.append("  <thead>")
        lines.append("    <tr>")
        lines.append("      <th>ID</th>")
        lines.append("      <th>Configuración</th>")
        lines.append("      <th>Tipo</th>")
        lines.append("      <th>Rango Mín</th>")
        lines.append("      <th>Rango Máx</th>")
        lines.append("      <th>ε (Epsilon)</th>")
        lines.append("      <th>Total Bits</th>")
        lines.append("    </tr>")
        lines.append("  </thead>")
        lines.append("  <tbody>")
        
        # Datos
        for i, fp in enumerate(fps, 1):
            tipo = "Sin signo" if not fp.signed else f"{fp.representation.upper()}"
            config = f"Q({fp.E},{fp.F}) B{fp.base}"
            min_str = self._format_number(fp.min_value, 4)
            max_str = self._format_number(fp.max_value, 4)
            eps_str = self._format_number(fp.epsilon, 6)
            
            lines.append("    <tr>")
            lines.append(f"      <td>{i}</td>")
            lines.append(f"      <td><code>{config}</code></td>")
            lines.append(f"      <td>{tipo}</td>")
            lines.append(f"      <td>{min_str}</td>")
            lines.append(f"      <td>{max_str}</td>")
            lines.append(f"      <td>{eps_str}</td>")
            lines.append(f"      <td>{fp.total_bits}</td>")
            lines.append("    </tr>")
        
        lines.append("  </tbody>")
        lines.append("</table>")
        lines.append("\n<style>")
        lines.append(".comparison-table { border-collapse: collapse; margin: 20px 0; font-family: monospace; }")
        lines.append(".comparison-table th { background-color: #4CAF50; color: white; font-weight: bold; }")
        lines.append(".comparison-table tr:nth-child(even) { background-color: #f2f2f2; }")
        lines.append(".comparison-table tr:hover { background-color: #ddd; }")
        lines.append("</style>")
        
        return "\n".join(lines)
    
    def export_json(self, fps: List[FixedPointUnified]) -> str:
        """
        Exporta comparativa a JSON.
        
        Args:
            fps: lista de FixedPointUnified
            
        Returns:
            string JSON
        """
        data = {
            'comparison': [],
            'metadata': {
                'count': len(fps),
                'timestamp': None,
            }
        }
        
        for i, fp in enumerate(fps, 1):
            item = {
                'id': i,
                'configuration': {
                    'E': fp.E,
                    'F': fp.F,
                    'base': fp.base,
                },
                'type': 'unsigned' if not fp.signed else f'{fp.representation}',
                'range': {
                    'min': fp.min_value,
                    'max': fp.max_value,
                    'span': fp.max_value - fp.min_value,
                },
                'epsilon': fp.epsilon,
                'total_bits': fp.total_bits,
            }
            data['comparison'].append(item)
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_json_file(self, fps: List[FixedPointUnified], filename: str) -> None:
        """
        Exporta comparativa a archivo JSON.
        
        Args:
            fps: lista de FixedPointUnified
            filename: ruta del archivo
        """
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.export_json(fps))
        
        print(f"✅ Comparativa exportada a {filename}")
    
    def export_latex_file(self, fps: List[FixedPointUnified], filename: str) -> None:
        """
        Exporta comparativa a archivo LaTeX.
        
        Args:
            fps: lista de FixedPointUnified
            filename: ruta del archivo
        """
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.render_latex(fps))
        
        print(f"✅ Tabla LaTeX exportada a {filename}")
    
    def export_html_file(self, fps: List[FixedPointUnified], filename: str) -> None:
        """
        Exporta comparativa a archivo HTML.
        
        Args:
            fps: lista de FixedPointUnified
            filename: ruta del archivo
        """
        import os
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparativa Punto Fijo</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        h1 {{ color: #333; }}
        .container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Comparativa de Representaciones de Punto Fijo</h1>
        {self.render_html(fps)}
    </div>
</body>
</html>
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Tabla HTML exportada a {filename}")


def compare_all_variants(E: int, F: int, base: int = 2) -> Dict:
    """
    Compara todas las variantes (sin signo, M&S, complemento) para una configuración.
    
    Args:
        E: bits enteros
        F: bits fraccionarios
        base: base numérica
        
    Returns:
        dict con los 3 FixedPointUnified
    """
    return {
        'unsigned': FixedPointUnified(E=E, F=F, base=base, signed=False),
        'ms': FixedPointUnified(E=E, F=F, base=base, signed=True, representation='ms'),
        'complement': FixedPointUnified(E=E, F=F, base=base, signed=True, representation='complement'),
    }
