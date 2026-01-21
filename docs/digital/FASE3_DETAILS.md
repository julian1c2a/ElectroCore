# FASE 3: Details (Detalles Visuales)

## Resumen Ejecutivo

**Fase 3** es el agregador de detalles visuales (estilos, colores, alineación) para las tablas. Toma un JSON + TEX de Fase 2 (estructura) y genera:

1. **TEX compilable**: Tabla estilizada con colores, padding, alineación
2. **JSON enriquecido**: Con metadata de detalles visuales para siguiente fase

## Responsabilidades

### Qué HACE

- ✅ Define colores (problema=gris, solución=verde)
- ✅ Agrega padding y espaciado en celdas
- ✅ Define altura mínima de filas
- ✅ Mejora encabezados (bold + fondo color)
- ✅ Usa fuente monoespaciada para alineación
- ✅ Produce TEX compilable con colores
- ✅ Propaga JSON con `phase3_details` metadata

### Qué NO HACE

- ❌ Agregar contenido/valores (eso es **Fase 4**)
- ❌ Validar JSON (eso fue **Fase 1**)
- ❌ Cambiar estructura (eso fue **Fase 2**)
- ❌ Generar enunciados (eso es **Fase 5**)

## Arquitectura

### Entrada

```json
{
  ...datos de Fase 1 y 2...
  "phase2_structure": {
    "num_rows": 1,
    "num_cols": 6,
    "columns": ["Etiqueta", "Decimal", "Binario", "C2", "SM", "BCD"],
    "structure_defined": true,
    "is_solution": false
  }
}
```

### Procesamiento

```python
Phase3Details.render(exercise_json, is_solution=False)
  |
  ├─ _extract_metadata(exercise_json)
  │  └─ Obtiene: exercise_type, etc
  │
  ├─ Extrae phase2_structure metadata
  │  └─ Obtiene: num_rows, num_cols, columns
  │
  ├─ _get_cell_color(is_solution)
  │  └─ Retorna: "240,240,240" (problema) o "200,255,200" (solución)
  │
  ├─ _generate_styled_latex(num_rows, num_cols, columns, is_solution, color)
  │  └─ Genera: LaTeX con colores, alineación, padding
  │
  └─ return PhaseOutput(
       latex_content = LaTeX estilizado,
       output_json = json + phase3_details metadata,
       phase_name = "detalles",
       tex_filename = "03_fase3_detalles.tex"
     )
```

### Salida

**TEX Output** (`03_fase3_detalles.tex`):

```latex
% ========================================
% FASE 3: DETALLES - Estilos visuales
% Tipo: ENUNCIADO
% ========================================

% Definición de colores (en RGB)
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

% Tabla de conversión con estilos
\newcommand{\cellpadding}[0]{\rule{0pt}{0.8em}}

\begin{tabular}{|c|c|c|c|c|c|}
\hline
\textbf{\cellcolor{encabezado} Etiqueta} & ... \\
\hline
\cellcolor{problema} \texttt{\cellpadding} & ... \\
\hline
\end{tabular}

% Notas de estilos aplicados:
% - Encabezados: fondo gris medio (230,230,230)
% - Celdas: fondo gris (240,240,240)
% - Padding: 0.3em
% - Altura mínima: 0.8em
% - Fuente: monoespaciada (\texttt) para alineación
```

**JSON Output** (añade metadata):

```json
{
  ...JSON anterior con phase1_validation y phase2_structure...
  "phase3_details": {
    "status": "styled",
    "problema_color": "240,240,240",
    "solucion_color": null,
    "encabezado_color": "230,230,230",
    "cell_padding": "0.3em",
    "row_height": "0.8em",
    "font": "ttfamily",
    "styles_applied": true,
    "is_solution": false
  }
}
```

## Paleta de Colores

```
Encabezado: RGB(230, 230, 230)  [Gris medio]
  - Fondo de encabezados
  - Siempre igual para enunciado y solución

Problema: RGB(240, 240, 240)    [Gris muy claro]
  - Celdas de datos cuando es_solution=False
  - Para celdas a rellenar en enunciado

Solución: RGB(200, 255, 200)    [Verde muy claro]
  - Celdas de datos cuando es_solution=True
  - Para mostrar respuestas en solución
```

## Parámetros de Estilo

```
Cell Padding:   0.3em   (espaciado horizontal/vertical en celda)
Row Height:     0.8em   (altura mínima de fila)
Font:          ttfamily (monoespaciada para alineación correcta)
Alignment:     centrado en todas columnas (|c|c|c|...)
```

## Comparación: Fase 2 vs Fase 3

| Aspecto | Fase 2 | Fase 3 |
|---------|--------|--------|
| **Tabla** | Estructura básica | Estilizada |
| **Colores** | Ninguno | Sí (gris/verde) |
| **Padding** | No | Sí (0.3em) |
| **Encabezados** | Normales | Bold + fondo |
| **Fuente** | Normal | Monoespaciada |
| **Contenido** | Vacío | Vacío |
| **Compilable** | Sí | Sí |

## Lógica de Color

```python
def _get_cell_color(is_solution: bool) -> str:
    if is_solution:
        return "solucion"      # Verde
    else:
        return "problema"      # Gris
```

**Resultado:**

- Enunciado: Tabla gris (para que el estudiante rellene)
- Solución: Tabla verde (para mostrar respuestas)

## Propiedades Clave

### Determinismo

- **Mismo JSON** → **Mismo TEX**
- Colores constantes
- Reproducible

### Agnósticismo

- Funciona tanto para **enunciado** como para **solución**
- Cambia solo el color de celdas
- Estructura idéntica

### Compilabilidad

- **TEX compilable** con colores
- Tabla vacía pero estilizada
- Útil para debugging visual

### Composabilidad

- **Input**: JSON + TEX de Fase 2
- **Output**: JSON + TEX compilable
- Encadena perfectamente con Fase 4

### Incrementalismo

- Mejora Fase 2 sin destruir estructura
- Cada fase agrega un nivel de complejidad

## Manejo de Errores

### Error 1: JSON sin `phase2_structure`

```python
# Indicador: JSON no procesado por Fase 2
# Solución: Pasar JSON a través de Fase 2 primero
```

### Error 2: `phase3_details` ya existe

```python
# Indicador: Fase 3 ejecutada dos veces
# Solución: Pipeline no debe ejecutar fase dos veces
```

### Error 3: Fase 1 o 2 fallaron

```python
# Solución: Pipeline detiene en Fase 1/2, no llega a Fase 3
```

## Caso de Uso Completo

### 1. Crear Pipeline con Fase 3

```python
from renderers.latex.phase1_validator import Phase1DataValidator
from renderers.latex.phase2_structure import Phase2StructureGenerator
from renderers.latex.phase3_details import Phase3Details
from renderers.latex.renderer_base import RendererPipeline

pipeline = RendererPipeline()
pipeline.add_phase(Phase1DataValidator())
pipeline.add_phase(Phase2StructureGenerator())
pipeline.add_phase(Phase3Details())  # NUEVO
```

### 2. Renderizar

```python
output = pipeline.render(ejercicio_json, is_solution=False)
```

### 3. Acceder a resultados

```python
fase3_output = output.phases[2]

# TEX con colores
print(fase3_output.latex_content)

# Metadata de estilos
print(fase3_output.output_json['phase3_details'])
```

### 4. Guardar archivos

```python
pipeline.save_main_file('build/latex/main.tex')
# Resultado:
# - build/latex/00_fase1_validacion.tex
# - build/latex/02_fase2_estructura.tex
# - build/latex/03_fase3_detalles.tex  ← CON COLORES
# - build/latex/main.tex (con \include de las tres)
```

## Relación con otras Fases

### Fase 2 → Fase 3

- **Entrada a Fase 3**: JSON + `phase2_structure` metadata
- **Salida de Fase 2**: Estructura de tabla definida
- **Dependencia**: Fase 3 usa `num_rows`, `num_cols` para estilos

### Fase 3 → Fase 4

- **Entrada a Fase 4**: JSON + `phase3_details` metadata
- **Salida de Fase 3**: Colores y estilos definidos
- **Dependencia**: Fase 4 sabe cómo colorear según metadata

## Pipeline Completo (hasta Fase 3)

```
ejercicio.json (raw)
    ↓
FASE 1: Validación [OK]
  - 00_fase1_validacion.tex
  - JSON + phase1_validation
    ↓
FASE 2: Estructura [OK]
  - 02_fase2_estructura.tex
  - JSON + phase2_structure
    ↓
FASE 3: Detalles [OK] ← ACTUAL
  - 03_fase3_detalles.tex (tabla con colores)
  - JSON + phase3_details
    ↓
FASE 4: Contenido [PRÓXIMO]
  - 04_fase4_contenido.tex (tabla con valores)
  - JSON + phase4_content
    ↓
FASE 5: Enunciados
  - 05_fase5_texto.tex (TEX FINAL)
  - JSON: None
    ↓
main.tex (composición con \include)
    ↓
[PDF OUTPUT]
```

## Características Futuras

- [ ] Colores personalizables por usuario
- [ ] Gradientes de color para resaltar filas
- [ ] Bordes más sofisticados
- [ ] Sombras en celdas
- [ ] Patrones de relleno (rayitas, punteado)
- [ ] Colores diferentes por tipo de ejercicio

## Integración con Pipeline

Fase 3 es el puente visual entre:

- **Fase 2**: Define QUÉ estructura
- **Fase 3**: Define CÓMO se ve (estilos)
- **Fase 4**: Define QSON los valores

## Archivos Implementados

- `renderers/latex/phase3_details.py`: Implementación de Phase3Details
- `FASE3_DEMO.py`: Demostración ejecutable del flujo Fase 1 → Fase 2 → Fase 3

## Status

✅ **COMPLETADO**: Phase3Details

- Definición de colores
- Cálculo de padding y altura
- Generación de LaTeX compilable
- Metadata para siguiente fase

⏳ **PRÓXIMO**: Phase4Content

- Agregar valores del problema
- Agregar valores de solución
- Mantener estilos de Fase 3

## Notas Técnicas

### Comando \cellpadding

```latex
\newcommand{\cellpadding}[0]{\rule{0pt}{0.8em}}
```

Define la altura mínima de celda sin agregar contenido visual.

### Colores con xcolor

```latex
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{nombre}{RGB}{R,G,B}
\cellcolor{nombre}
```

### Fuente Monoespaciada

```latex
\texttt{contenido}  % typewriter/monospace
```

Mantiene alineación correcta de números.

### Centrado en Tabular

```latex
\begin{tabular}{|c|c|c|}  % c = centrado
```

Todas las columnas centradas automáticamente.
