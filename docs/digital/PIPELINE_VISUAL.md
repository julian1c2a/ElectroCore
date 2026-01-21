# PIPELINE VISUAL: Fase 1 + Fase 2

## Flujo de Datos Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ENTRADA: ejercicio.json (raw, no procesado)                    │
│  {                                                              │
│    "title": "Conversión Decimal a Bases",                      │
│    "metadata": { "exercise_type": "ConversionRow" },           │
│    "problem": { "val_decimal": 157, ... },                     │
│    "solution": { "sol_bin": "10011101", ... }                  │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FASE 1: Phase1DataValidator.render()                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Validar estructura JSON                                │ │
│  │    ✓ title, description, problem, solution, metadata      │ │
│  │                                                            │ │
│  │ 2. Validar campos requeridos por exercise_type            │ │
│  │    ✓ ConversionRow: label, val_decimal, representable... │ │
│  │                                                            │ │
│  │ 3. Validar tipos de datos                                 │ │
│  │    ✓ val_decimal es numérico                              │ │
│  │    ✓ representable es bool                                │ │
│  │                                                            │ │
│  │ 4. Extraer metadatos                                      │ │
│  │    ✓ exercise_type, campos presentes, etc                │ │
│  │                                                            │ │
│  │ 5. Generar TEX documentativo                              │ │
│  │    ✓ Archivo: 00_fase1_validacion.tex                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  SALIDA FASE 1:                                                 │
│  • TEX compilable: 00_fase1_validacion.tex                     │
│  • JSON con metadata:                                          │
│    {                                                            │
│      ...JSON anterior...                                        │
│      "phase1_validation": {                                     │
│        "status": "valid",                                       │
│        "exercise_type": "ConversionRow",                       │
│        "problem_fields": ["label", "val_decimal", ...],       │
│        "solution_fields": ["sol_bin", "sol_c2", ...],         │
│        "validated_at": "phase1"                                │
│      }                                                          │
│    }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  FASE 2: Phase2StructureGenerator.render()                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Extraer metadata del JSON                              │ │
│  │    ✓ exercise_type: "ConversionRow"                       │ │
│  │                                                            │ │
│  │ 2. Extraer problema del JSON                              │ │
│  │    ✓ label, val_decimal, target_col_idx, representable   │ │
│  │                                                            │ │
│  │ 3. Determinar num_rows basado en exercise_type            │ │
│  │    ConversionRow → 1 fila                                │ │
│  │    ArithmeticOp → 3 filas                                │ │
│  │    Default → 1 fila                                       │ │
│  │                                                            │ │
│  │ 4. Generar estructura LaTeX de tabla                      │ │
│  │    • \begin{tabular}{|c|c|c|c|c|c|}                      │ │
│  │    • Encabezados: Etiqueta|Decimal|Binario|C2|SM|BCD     │ │
│  │    • Filas vacías (1 fila para ConversionRow)            │ │
│  │                                                            │ │
│  │ 5. Compilar TEX de estructura                             │ │
│  │    ✓ Archivo: 02_fase2_estructura.tex                    │ │
│  │    ✓ Tabla compilable pero sin contenido                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  SALIDA FASE 2:                                                 │
│  • TEX compilable: 02_fase2_estructura.tex                     │
│  • JSON con metadata:                                          │
│    {                                                            │
│      ...JSON anterior (con phase1_validation)...               │
│      "phase2_structure": {                                      │
│        "status": "generated",                                   │
│        "table_type": "numeracion_conversion",                   │
│        "num_rows": 1,                                           │
│        "num_cols": 6,                                           │
│        "columns": ["Etiqueta", "Decimal", ...],                │
│        "structure_defined": true,                              │
│        "is_solution": false                                    │
│      }                                                          │
│    }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Archivos Generados en Fase 1 + Fase 2

```
build/latex/
├── 00_fase1_validacion.tex
│   └─ Comentarios con info de validación
│      Estado: VÁLIDO
│      Campos encontrados: label, val_decimal, ...
│      [Compilable pero solo comentarios]
│
└── 02_fase2_estructura.tex
    └─ Tabla LaTeX vacía pero estructurada
       \begin{tabular}{|c|c|c|c|c|c|}
       \hline
       Etiqueta & Decimal & Binario & C2 & SM & BCD \\
       \hline
        &  &  &  &  &  \\
       \hline
       \end{tabular}
       [Compilable: tabla estructura sin contenido]
```

## TEX Output de Cada Fase

### Fase 1: Validación (comentarios)

```latex
% ========================================
% FASE 1: VALIDACIÓN Y METADATOS
% ========================================

% Información del ejercicio
% Título: Conversión Decimal a Múltiples Bases
% Descripción: Convertir 157 a múltiples bases
% Tipo: ConversionRow

% Estado de validación: VÁLIDO

% Campos del problema detectados:
% label, val_decimal, target_col_idx, representable

% Campos de solución detectados:
% sol_bin, sol_c2, sol_sm, sol_bcd, target_val_str

% Solución disponible: SÍ
```

### Fase 2: Estructura (tabla vacía)

```latex
% ========================================
% FASE 2: ESTRUCTURA - marcos y dimensiones de tabla
% Tipo: ENUNCIADO
% ========================================

% Tabla de conversión de bases numéricas
% Estructura: 6 columnas x 1 filas

\begin{tabular}{|c|c|c|c|c|c|}
\hline
Etiqueta & Decimal & Binario & C2 & SM & BCD \\
\hline
 &  &  &  &  &  \\
\hline
\end{tabular}

% Estado de FASE 2
% - Estructura: DEFINIDA
% - Dimensiones: 1x6 (filas x columnas)
% - Bordes: SÍ (\hline)
% - Contenido: NO (se agrega en Fase 3+)
% - Estilos: NO (se agregan en Fase 3)
```

## Flujo de JSON a través del Pipeline

```
INICIAL:
{
  "title": "...",
  "description": "...",
  "metadata": { "exercise_type": "ConversionRow" },
  "problem": { "label": "a", "val_decimal": 157, ... },
  "solution": { "sol_bin": "10011101", ... }
}

DESPUÉS DE FASE 1:
{
  "title": "...",
  ...mismo JSON anterior...
  "phase1_validation": {
    "status": "valid",
    "exercise_type": "ConversionRow",
    "problem_fields": [...],
    "solution_fields": [...],
    "validated_at": "phase1"
  }
}

DESPUÉS DE FASE 2:
{
  "title": "...",
  ...JSON con phase1_validation...
  "phase2_structure": {
    "status": "generated",
    "table_type": "numeracion_conversion",
    "num_rows": 1,
    "num_cols": 6,
    "columns": ["Etiqueta", "Decimal", ...],
    "structure_defined": true,
    "is_solution": false
  }
}
```

## Compilación de TEX en cada Fase

```
FASE 1: TEX compilable
$ pdflatex 00_fase1_validacion.tex
→ PDF con comentarios de validación
→ Útil para debugging

FASE 2: TEX compilable
$ pdflatex 02_fase2_estructura.tex
→ PDF con tabla vacía
→ Útil para ver estructura sin contenido

FASES 1+2 JUNTAS:
$ cat > main.tex << EOF
\documentclass{article}
\begin{document}
\include{00_fase1_validacion}
\include{02_fase2_estructura}
\end{document}
EOF
$ pdflatex main.tex
→ PDF con validación + estructura
```

## Próximas Fases

```
FASE 3: Details (Detalles Visuales)
  Input: JSON + Fase2 TEX
  Output: TEX con estilos + colores
  Agrega: ✓ Colores, ✓ Alineación, ✓ Padding
  
FASE 4: Content (Contenido)
  Input: JSON + Fase3 TEX
  Output: TEX con valores del problema
  Agrega: ✓ Números, ✓ Valores de solución
  
FASE 5: Text (Enunciados)
  Input: JSON + Fase4 TEX
  Output: TEX FINAL con explicaciones
  Agrega: ✓ Texto, ✓ Enunciados, ✓ Pasos
  
COMPOSICIÓN FINAL:
  \include{00_fase1_validacion}
  \include{02_fase2_estructura}
  \include{03_fase3_detalles}
  \include{04_fase4_contenido}
  \include{05_fase5_texto}
  → main.tex → PDF final
```

## Separación de Responsabilidades

```
Fase 1: ¿Es correcto?   → Validar JSON
Fase 2: ¿Qué forma?     → Estructura de tabla
Fase 3: ¿Qué estilos?   → Colores, alineación
Fase 4: ¿Qué valores?   → Contenido numeral
Fase 5: ¿Qué texto?     → Enunciados
```

## Propiedades del Pipeline

✅ **Modular**: Cada fase independiente  
✅ **Composable**: Fases se encadenan  
✅ **Debuggable**: Compilable en cada fase  
✅ **Agnóstico**: Funciona para problema/solución  
✅ **Determinista**: Mismo input = mismo output  
✅ **Extensible**: Nuevas fases fácilmente  

## Status de Implementación

```
COMPLETADO:
✓ Fase 1: Phase1DataValidator [PRODUCTION-READY]
✓ Fase 2: Phase2StructureGenerator [PRODUCTION-READY]

PENDIENTE:
⏳ Fase 3: Phase3Details
⏳ Fase 4: Phase4Content
⏳ Fase 5: Phase5Text
⏳ Integration con main_v2.py
⏳ Unit tests para cada fase
```
