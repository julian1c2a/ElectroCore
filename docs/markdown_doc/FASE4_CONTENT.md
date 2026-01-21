# FASE 4: Content - Agregador de Contenido Numeral

## Resumen Ejecutivo

**Fase 4** toma la tabla estilizada de Fase 3 y la **llena con valores numéricos** del problema o solución. La responsabilidad principal es extraer datos del JSON (campos `problem` y `solution`) e insertarlos en las celdas correspondientes, manteniendo todos los estilos visuales de Fase 3.

| Aspecto | Descripción |
|---------|-------------|
| **Entrada** | JSON validado + TEX estilizado de Fase 3 |
| **Salida** | TEX con tabla llena + metadata de Fase 4 en JSON |
| **Archivo** | `renderers/latex/phase4_content.py` |
| **Clase** | `Phase4Content(ExerciseRendererPhase)` |
| **TEX Output** | `04_fase4_contenido.tex` |

---

## Responsabilidades

### 1. Extracción de Valores

**Objetivo**: Obtener valores del JSON según el tipo de ejercicio.

Para **ConversionRow**:

- Del `problem`: extrae `label` (etiqueta) y `val_decimal` (valor decimal)
- Del `solution`: extrae `sol_bin`, `sol_c2`, `sol_sm`, `sol_bcd` (conversiones)
- Modo **enunciado**: muestra label + decimal, resto vacío (para resolver)
- Modo **solución**: muestra todos los valores

Para **ArithmeticOp**:

- Del `problem`: extrae operandos y operador
- Del `solution`: extrae resultado
- Modo **enunciado**: muestra operandos, espacio para resultado
- Modo **solución**: muestra todo incluyendo resultado

### 2. Formateo de Valores

**Objetivo**: Preparar valores para LaTeX.

- Convierte a string con `str(value)`
- Preserva espacios en valores (ej: "0001 0101 0111" para BCD)
- Maneja valores vacíos ("") para espacios en blanco
- Usa "?" para valores faltantes

### 3. Generación de LaTeX

**Objetivo**: Producir tabla compilable con contenido.

- Mantiene estructura de Fase 3 (colores, padding, alineación)
- Inserta valores en celdas con `\texttt{valor}`
- Aplica `\cellcolor{color}` para cada celda
- Genera `\hline` correctamente
- Compilable y visualmente coherente

### 4. Metadata de Fase 4

**Objetivo**: Rastrear progreso a través del pipeline.

Agrega al JSON:

```python
'phase4_content': {
    'status': 'populated',
    'exercise_type': 'ConversionRow',
    'num_rows_filled': 1,
    'values_extracted': True,
    'content_added': True,
    'is_solution': False
}
```

---

## Arquitectura

### Clase Principal: `Phase4Content`

```python
class Phase4Content(ExerciseRendererPhase):
    """
    FASE 4: Agregador de contenido (valores numéricos).
    """
    
    # Colores (heredados de Fase 3)
    PROBLEMA_COLOR = "240,240,240"     # Gris
    SOLUCION_COLOR = "200,255,200"     # Verde
    ENCABEZADO_COLOR = "230,230,230"   # Gris medio
    
    # Espaciado
    CELL_PADDING = "0.3em"
    ROW_HEIGHT = "0.8em"
    FONT_FAMILY = "ttfamily"
```

### Métodos Principales

#### `render(exercise_json, is_solution)`

**Entrada**: JSON completo + flag de solución
**Salida**: `PhaseOutput` con TEX + JSON actualizado

Flujo:

1. Extrae metadata de Fase 2/3
2. Obtiene `num_rows`, `num_cols`, `columns`
3. Llama `_extract_values()` para obtener datos
4. Llama `_generate_content_latex()` para crear TEX
5. Acumula metadata en JSON
6. Retorna `PhaseOutput`

#### `_extract_values(exercise_json, exercise_type, is_solution)`

**Entrada**: JSON, tipo de ejercicio, flag solución
**Salida**: Lista de dicts `[{columna: valor}]`

Dispatch por exercise_type:

- `ConversionRow` → `_extract_conversion_values()`
- `ArithmeticOp` → `_extract_arithmetic_values()`
- Otros → retorna `[{}]` (fila vacía)

#### `_extract_conversion_values(exercise_json, is_solution)`

Para ConversionRow (numeración):

**Si `is_solution=False`** (enunciado):

```python
{
    'Etiqueta': problem['label'],           # 'a'
    'Decimal': problem['val_decimal'],      # 157
    'Binario': '',                          # Vacío
    'C2': '',
    'SM': '',
    'BCD': ''
}
```

**Si `is_solution=True`** (solución):

```python
{
    'Etiqueta': problem['label'],           # 'a'
    'Decimal': problem['val_decimal'],      # 157
    'Binario': solution['sol_bin'],         # '10011101'
    'C2': solution['sol_c2'],               # '10011101'
    'SM': solution['sol_sm'],               # '10011101'
    'BCD': solution['sol_bcd']              # '0001 0101 0111'
}
```

#### `_extract_arithmetic_values(exercise_json, is_solution)`

Para ArithmeticOp (operaciones):

Retorna lista de 3 dicts (operando1, operador, operando2/resultado)

**Si `is_solution=False`**:

```python
[
    {'Etiqueta': 'A', 'Valor': '25', 'Base': '10'},
    {'Etiqueta': '+', 'Valor': '17', 'Base': '10'},
    {'Etiqueta': '=', 'Valor': '', 'Base': ''}  # Vacío
]
```

**Si `is_solution=True`**:

```python
[
    {'Etiqueta': 'A', 'Valor': '25', 'Base': '10'},
    {'Etiqueta': '+', 'Valor': '17', 'Base': '10'},
    {'Etiqueta': '=', 'Valor': '42', 'Base': '10'}  # Con resultado
]
```

#### `_generate_content_latex(...)`

**Objetivo**: Producir LaTeX compilable con valores.

Estructura:

1. Encabezado LaTeX (comentarios, definiciones de color)
2. Paquetes: `\usepackage[usenames,dvipsnames]{xcolor}`
3. Definiciones de color: `\definecolor{problema}{RGB}{240,240,240}`
4. Definición de comando: `\newcommand{\cellpadding}...`
5. Tabla `tabular` con encabezados y filas
6. Para cada fila: inserta valores con `\texttt{valor}`
7. Nota de estilos al final

Ejemplo de fila:

```latex
\cellcolor{problema} \texttt{\cellpadding a} & 
\cellcolor{problema} \texttt{\cellpadding 157} & 
\cellcolor{problema} \texttt{\cellpadding } & 
...
```

---

## Flujo de Datos

### Entrada de Fase 4

```
ejercicio.json (contiene problem y solution)
{
  'metadata': {...},
  'problem': {
    'label': 'a',
    'val_decimal': 157,
    ...
  },
  'solution': {
    'sol_bin': '10011101',
    'sol_c2': '10011101',
    ...
  },
  'phase1_validation': {...},
  'phase2_structure': {...},
  'phase3_details': {...}
}
```

### Procesamiento

```
1. Leer exercise_type = metadata['exercise_type']
   → 'ConversionRow'

2. Llamar _extract_values()
   → Obtiene valores de problem/solution
   → [{label: 'a', decimal: 157, ...}]

3. Llamar _generate_content_latex()
   → Inserta valores en tabla LaTeX
   → Mantiene colores de Fase 3

4. Acumular metadata
   → JSON['phase4_content'] = {...}
```

### Salida de Fase 4

```
04_fase4_contenido.tex:
  % Tabla con valores insertados
  \begin{tabular}{|c|c|c|c|c|c|}
    \hline
    \textbf{\cellcolor{encabezado} Etiqueta} & ...
    \hline
    \cellcolor{problema} \texttt{\cellpadding a} & ...
    \hline
  \end{tabular}

ejercicio_fase4.json:
  Contiene todo lo anterior más:
  {
    'phase4_content': {
      'status': 'populated',
      'num_rows_filled': 1,
      'content_added': True
    }
  }
```

---

## Modos de Operación

### Modo Enunciado (`is_solution=False`)

**Propósito**: Tabla lista para que alumno resuelva.

**Características**:

- Color de fondo: **gris** (problema)
- Contenido: Solo problema (label + valores iniciales)
- Celdas de respuesta: **Vacías** (para escribir)
- Uso: Imprimir para examen

**Ejemplo**:

```
| Etiqueta | Decimal | Binario | C2 | SM | BCD |
|----------|---------|---------|----|----|-----|
| a        | 157     | [  ]    | [ ]| [ ]| [ ] |
```

### Modo Solución (`is_solution=True`)

**Propósito**: Tabla con respuestas completas.

**Características**:

- Color de fondo: **verde** (solución)
- Contenido: Todos los valores (problema + respuestas)
- Celdas: **Todas llenas**
- Uso: Guía de corrección/soluciones

**Ejemplo**:

```
| Etiqueta | Decimal | Binario  | C2       | SM       | BCD           |
|----------|---------|----------|----------|----------|---------------|
| a        | 157     | 10011101 | 10011101 | 10011101 | 0001 0101 0111|
```

---

## Características Clave

### Determinismo

- Mismo JSON de entrada → **Siempre** mismo TEX
- Sin componentes aleatorios
- Reproducible

### Agnósticismo

- Funciona para **enunciado** (is_solution=False)
- Funciona para **solución** (is_solution=True)
- JSON único, adaptable a ambos modos

### Compilabilidad

- TEX siempre válido y compilable
- Sin errores LaTeX
- Tabla correctamente formada

### Composabilidad

- Entrada: JSON de Fase 3
- Salida: JSON + TEX para Fase 5
- Encadenamiento limpio

### Incrementalismo

- Mejora Fase 3 sin destruir su estructura
- Agrega contenido, mantiene estilos
- Construcción progresiva

---

## Casos de Uso

### Caso 1: ConversionRow Simple

**Entrada**: Problema "Convierte 157 a binario/C2/SM/BCD"

**Enunciado**:

```
Etiqueta | Decimal | Binario | C2 | SM | BCD
---------|---------|---------|----|----|-----
a        | 157     |         |    |    |
```

**Solución**:

```
Etiqueta | Decimal | Binario  | C2       | SM       | BCD
---------|---------|----------|----------|----------|-----
a        | 157     | 10011101 | 10011101 | 10011101 | 0001 0101 0111
```

### Caso 2: ArithmeticOp (futuro)

**Entrada**: Problema "Suma 25 + 17 en binario"

**Enunciado**:

```
Operando | Valor | Base
---------|-------|-----
A        | 25    | 10
+        | 17    | 10
=        |       |
```

**Solución**:

```
Operando | Valor | Base
---------|-------|-----
A        | 25    | 10
+        | 17    | 10
=        | 42    | 10
```

---

## Manejo de Errores

### Error: `exercise_type` desconocido

- **Causa**: JSON contiene tipo no soportado
- **Acción**: Retorna `[{}]` en `_extract_values()`
- **Resultado**: Tabla vacía pero compilable
- **Severidad**: INFO

### Error: Campo faltante en `problem`

- **Causa**: JSON incompleto (ej: falta `val_decimal`)
- **Acción**: Retorna "?" como placeholder
- **Resultado**: Tabla muestra "?" para indicar dato faltante
- **Severidad**: WARNING

### Error: `is_solution=True` pero falta `solution`

- **Causa**: Intentar modo solución sin datos de solución
- **Acción**: Retorna valores parciales disponibles
- **Resultado**: Tabla muestra lo que hay, con "?" para faltantes
- **Severidad**: WARNING

**Principio General**: NUNCA fallar compilación. Siempre generar LaTeX válido incluso con datos incompletos.

---

## Validación de Salida

### Checklist de Fase 4

```
[OK] Tabla correctamente dimensionada
[OK] Encabezados presentes
[OK] Filas pobladas con valores
[OK] Bordes y líneas separadoras
[OK] Colores aplicados correctamente
[OK] Padding y alineación
[OK] Fuente monoespaciada
[OK] TEX compilable
[OK] Metadata en JSON
[NO] Sin enunciados (Fase 5)
```

---

## Integración con Pipeline

### Entrada desde Fase 3

```
Phase3Details.render() 
  ↓ retorna PhaseOutput
    - latex_content: tabla estilizada (vacía)
    - output_json: JSON + phase3_details
```

### Fase 4 consume

```
Phase4Content.render(output_json)
  - Lee phase2_structure (num_rows, columnas)
  - Lee phase3_details (colores, estilos)
  - Extrae values del problem/solution
  - Genera tabla con contenido
  ↓ retorna PhaseOutput
    - latex_content: tabla con valores
    - output_json: JSON + phase4_content
```

### Salida hacia Fase 5

```
Fase 5 (Phase5Text) espera:
  - JSON con phase4_content
  - Tabla ya llena
  - Solo falta agregar enunciados
```

---

## Resumen Técnico

| Aspecto | Detalle |
|---------|---------|
| **Líneas de Código** | ~250 |
| **Métodos Principales** | 4 (render, _extract_values, _extract_conversion_values,_generate_content_latex) |
| **Exercise Types Soportados** | ConversionRow, ArithmeticOp (+extendible) |
| **Colores Usados** | 3 (problema: gris, solución: verde, encabezado: gris medio) |
| **Parámetros de Estilo** | 3 (CELL_PADDING, ROW_HEIGHT, FONT_FAMILY) |
| **JSON Metadata** | 7 campos en phase4_content |
| **Compilabilidad** | 100% (nunca genera LaTeX inválido) |

---

## Notas Importantes

### Sobre Valores Vacíos

En modo **enunciado**, algunos campos están deliberadamente vacíos para que el alumno los complete. No es un error; es por diseño.

### Sobre Colores

- **Gris** (240,240,240): Problema a resolver
- **Verde** (200,255,200): Solución completada
- **Gris medio** (230,230,230): Encabezados

Esta codificación de color es automática según `is_solution`.

### Sobre Compilabilidad

Incluso si datos falta, Fase 4 genera LaTeX válido. Esto es intencional: facilita debugging y mantiene la cadena de compilación sin breaks.

---

## Próxima Fase: Fase 5 - Text

Fase 4 entrega tabla con valores. Fase 5 agregará:

- Enunciados (problem statement)
- Explicaciones (solution explanation)
- Instrucciones
- Pasos de resolución

Ejemplo final:

```
ENUNCIADO:
  "Convierte el número decimal 157 a sus representaciones 
   en binario, complemento a 2, signo-magnitud y BCD"

[Tabla de Fase 4]

SOLUCION:
  "Para convertir 157:
   1. Conversion a binario: divide por 2...
   2. C2: invierta bits...
   3. SM: use el bit más significativo...
   4. BCD: agrupe en nibbles..."

[Tabla de Fase 4 con respuestas]
```
