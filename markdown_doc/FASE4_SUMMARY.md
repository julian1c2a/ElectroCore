# FASE 4: Content - Resumen Ejecutivo

## Visión General

**Fase 4** es el agregador de **contenido numeral** en el pipeline de renderización. Toma la tabla estilizada pero vacía de Fase 3 y la llena con valores extraídos del JSON (campos `problem` y `solution`).

```
Fase 3: Tabla vacía + estilos
    ↓
Fase 4: Tabla llena + estilos ← AQUÍ
    ↓
Fase 5: Tabla llena + enunciados
```

---

## Implementación

### Archivo: `renderers/latex/phase4_content.py`

**Clase Principal**:

```python
class Phase4Content(ExerciseRendererPhase):
    """
    FASE 4: Agregador de contenido (valores numéricos).
    Extrae values de JSON e inserta en tabla LaTeX.
    """
```

**Líneas de Código**: ~250

### Métodos Clave

| Método | Responsabilidad |
|--------|-----------------|
| `render()` | Orquesta el flujo de Fase 4 |
| `_extract_values()` | Obtiene datos de JSON según exercise_type |
| `_extract_conversion_values()` | Extrae para ConversionRow |
| `_extract_arithmetic_values()` | Extrae para ArithmeticOp |
| `_generate_content_latex()` | Genera LaTeX compilable con valores |

---

## Entrada y Salida

### Entrada

- **JSON**: Validado de Fase 1-3, con campos `problem` y `solution`
- **TEX**: Tabla estilizada pero vacía de Fase 3
- **Metadata**: De fases anteriores (`phase1_validation`, `phase2_structure`, `phase3_details`)

### Salida

- **TEX**: `04_fase4_contenido.tex` (tabla con contenido, compilable)
- **JSON**: Actualizado con metadata de Fase 4
- **Formato**: LaTeX con colores, padding, alineación (heredado de Fase 3)

---

## Lógica de Extracción

### Para ConversionRow

#### Enunciado (`is_solution=False`)

```
Etiqueta → problem['label']         (ej: 'a')
Decimal  → problem['val_decimal']   (ej: 157)
Binario  → '' (vacío para resolver)
C2       → ''
SM       → ''
BCD      → ''
```

#### Solución (`is_solution=True`)

```
Etiqueta → problem['label']         (ej: 'a')
Decimal  → problem['val_decimal']   (ej: 157)
Binario  → solution['sol_bin']      (ej: '10011101')
C2       → solution['sol_c2']       (ej: '10011101')
SM       → solution['sol_sm']       (ej: '10011101')
BCD      → solution['sol_bcd']      (ej: '0001 0101 0111')
```

### Para ArithmeticOp (futuro)

3 filas: operando1, operador, operando2/resultado

---

## Comparación Visual

### Fase 3 vs Fase 4

```
FASE 3: Estilizada, vacía
┌───────────┬─────────┬─────────┬────┬────┬─────┐
│ Etiqueta  │ Decimal │ Binario │ C2 │ SM │ BCD │
├───────────┼─────────┼─────────┼────┼────┼─────┤
│           │         │         │    │    │     │  ← Vacío
└───────────┴─────────┴─────────┴────┴────┴─────┘

FASE 4: Estilizada, llena
┌───────────┬─────────┬──────────┬──────────┬──────────┬───────────────┐
│ Etiqueta  │ Decimal │ Binario  │ C2       │ SM       │ BCD           │
├───────────┼─────────┼──────────┼──────────┼──────────┼───────────────┤
│ a         │ 157     │ 10011101 │ 10011101 │ 10011101 │ 0001 0101 0111│
└───────────┴─────────┴──────────┴──────────┴──────────┴───────────────┘
```

**Diferencia**: Contenido (valores numéricos) insertados en celdas

---

## Características

### ✓ Determinismo

- Mismo JSON → Siempre mismo TEX
- Sin variables aleatorias
- Reproducible 100%

### ✓ Agnósticismo

- Funciona para **enunciado** (is_solution=False)
- Funciona para **solución** (is_solution=True)
- Un solo JSON, adaptable a ambos modos

### ✓ Compilabilidad

- TEX siempre válido
- Nunca genera errores LaTeX
- Compilable en cualquier compilador LaTeX

### ✓ Composabilidad

- Entrada: JSON + TEX de Fase 3
- Salida: JSON + TEX para Fase 5
- Encadenamiento limpio

### ✓ Incrementalismo

- Mejora Fase 3 sin destruir estructura
- Agrega contenido, mantiene estilos
- Construcción progresiva, sin regresiones

---

## Metadata en JSON

Fase 4 agrega a JSON:

```json
{
  "phase4_content": {
    "status": "populated",
    "exercise_type": "ConversionRow",
    "num_rows_filled": 1,
    "values_extracted": true,
    "content_added": true,
    "is_solution": false
  }
}
```

**Significado**:

- `status`: 'populated' = tabla llena
- `exercise_type`: Tipo que procesó (para auditoría)
- `num_rows_filled`: Cuántas filas se llenaron
- `values_extracted`: ✓ Valores extraídos exitosamente
- `content_added`: ✓ Contenido insertado en LaTeX
- `is_solution`: ✓ Modo usado (false=enunciado, true=solución)

---

## Colores Usados

Hereda colores de Fase 3:

| Color | RGB | Uso |
|-------|-----|-----|
| Problema | 240,240,240 (gris claro) | Fondo celdas cuando is_solution=False |
| Solución | 200,255,200 (verde claro) | Fondo celdas cuando is_solution=True |
| Encabezado | 230,230,230 (gris medio) | Fondo para nombres de columna |

**Lógica**:

- Si `is_solution=False` → Todas celdas con color "problema" (gris)
- Si `is_solution=True` → Todas celdas con color "solución" (verde)
- Encabezados siempre con color "encabezado" (gris medio)

---

## LaTeX Generated

### Estructura

```latex
% Definición de colores
\usepackage[usenames,dvipsnames]{xcolor}
\definecolor{problema}{RGB}{240,240,240}
\definecolor{solucion}{RGB}{200,255,200}
\definecolor{encabezado}{RGB}{230,230,230}

% Comando para padding
\newcommand{\cellpadding}[0]{\rule{0pt}{0.8em}}

% Tabla
\begin{tabular}{|c|c|c|c|c|c|}
  \hline
  \textbf{\cellcolor{encabezado} Etiqueta} & ...
  \hline
  \cellcolor{problema} \texttt{\cellpadding a} & 
  \cellcolor{problema} \texttt{\cellpadding 157} & ...
  \hline
\end{tabular}
```

### Características

- **Tabular**: 6 columnas para ConversionRow
- **Encabezados**: Bold + color encabezado
- **Celdas**: `\cellcolor{color} \texttt{valor}`
- **Padding**: 0.3em (heredado de Fase 3)
- **Alineación**: Centrada en todas columnas
- **Fuente**: Monoespaciada (texttt) para alineación

---

## Manejo de Errores

| Situación | Acción | Resultado |
|-----------|--------|-----------|
| exercise_type desconocido | Retorna fila vacía | Tabla sin datos pero compilable |
| Campo faltante en problem | Retorna "?" | Celda muestra "?" (indicador de falta) |
| is_solution=True, falta solution | Retorna valores disponibles | Tabla parcial con "?" en faltantes |
| JSON inválido | Excepción capturada | Error reportado, sin LaTeX generado |

**Principio**: NUNCA fallar silenciosamente. Siempre generar LaTeX compilable incluso con datos incompletos.

---

## Casos de Uso

### Uso 1: Generar Enunciado para Estudiante

```python
phase4 = Phase4Content()
output = phase4.render(exercise_json, is_solution=False)
# output.latex_content → tabla con problema, espacios vacíos para resolver
# Imprimir → estudiante ve lo que debe resolver
```

### Uso 2: Generar Solución para Corrección

```python
phase4 = Phase4Content()
output = phase4.render(exercise_json, is_solution=True)
# output.latex_content → tabla con todas las respuestas
# Imprimir → profesor ve la clave de respuestas
```

### Uso 3: Comparación lado a lado

```python
enunciado = phase4.render(exercise_json, is_solution=False)
solucion = phase4.render(exercise_json, is_solution=True)
# Ambas tablas tienen estilos idénticos, solo cambia contenido
# Útil para documentación de examen
```

---

## Validación Post-Fase 4

### Checklist

- ✓ Tabla compilable como LaTeX
- ✓ Contenido extraído del JSON correctamente
- ✓ Colores aplicados según is_solution
- ✓ Padding y alineación mantenida
- ✓ Encabezados presentes y resaltados
- ✓ Número de filas correcto
- ✓ Metadata agregada al JSON
- ✗ Enunciados (Fase 5)
- ✗ Explicaciones (Fase 5)

---

## Pipeline Completo

```
Input: ejercicio.json
    ↓
FASE 1: Validación
    |- Verificar estructura JSON
    |- Output: JSON + phase1_validation
    ↓
FASE 2: Estructura
    |- Determinar num_rows
    |- Crear tabla vacía (6 col × N filas)
    |- Output: JSON + phase2_structure + 02_fase2_estructura.tex
    ↓
FASE 3: Detalles
    |- Agregar colores
    |- Agregar padding, alineación
    |- Output: JSON + phase3_details + 03_fase3_detalles.tex
    ↓
FASE 4: Contenido ← AQUÍ
    |- Extraer values de problem/solution
    |- Llenar tabla CON VALORES
    |- Output: JSON + phase4_content + 04_fase4_contenido.tex
    ↓
FASE 5: Text
    |- Agregar enunciados
    |- Agregar explicaciones
    |- Output: JSON + phase5_text + 05_fase5_enunciados.tex
    ↓
main.tex (compilado) → PDF
```

---

## Estadísticas

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~250 |
| Métodos implementados | 4 |
| Exercise types soportados | 2 (ConversionRow, ArithmeticOp) |
| Colores definidos | 3 |
| Parámetros LaTeX | 3 (padding, height, font) |
| Campos en metadata | 7 |
| Compilabilidad | 100% |

---

## Próxima Fase

**Fase 5: Text (Enunciados)**

Toma tabla llena de Fase 4 y agrega:

1. **Enunciado** (problem statement)
2. **Explicación** (solution explanation)
3. **Instrucciones** (cómo resolver)
4. **Pasos** (paso a paso resolución)

Resultado: Documento completo y compilable → PDF

---

## Resumen

Fase 4 es el **extractor y pobladorde contenido** del pipeline:

✓ Extrae valores de JSON  
✓ Los inserta en tabla LaTeX  
✓ Mantiene estilos de Fase 3  
✓ Genera LaTeX compilable  
✓ Agnóstico (enunciado/solución)  
✓ Determinista (reproducible)  

**Próximo paso**: Fase 5 - agregar enunciados y documentación.
