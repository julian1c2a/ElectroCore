# Refactorización de Estructura de Directorios

## Resumen

Se ha refactorizado el proyecto para organizar los componentes generados por tópico (digital/análógica) y por módulo (numeración, combinacional, secuencial).

## Cambios Realizados

### 1. **main_v2.py** - Gestión de directorios

- Agregada función `setup_directories()` que crea la estructura:

     ```
     build/latex/
     ├── digital/
     │   ├── numeracion/componentes/
     │   ├── combinacional/componentes/
     │   └── secuencial/componentes/
     └── analogica/componentes/
     
     out/
     ├── digital/      (PDFs finales de exámenes digital)
     └── analogica/    (PDFs finales de exámenes análogica)
     ```

- Cambio en la limpieza: ahora destruye solo `build/latex/` pero crea la estructura completa
- Parámetro `work_type` y `output_dir` para separar por tipo

### 2. **main_renderer.py** - Pasar base_build_path

- Constructor ahora acepta parámetro `base_build_path` (default: `"build/latex"`)
- Cada renderer específico recibe su subdirectorio:
  - `NumeracionLatexRenderer`: `build/latex/digital/numeracion`
  - `CombinacionalLatexRenderer`: `build/latex/digital/combinacional`
  - `SecuencialLatexRenderer`: `build/latex/digital/secuencial`

### 3. **Renderers Específicos**

- **numeracion_renderer.py**: Acepta `base_build_path`
- **combinacional_renderer.py**: Acepta `base_build_path`, pasa a `LatexAssetManager`
- **secuencial_renderer.py**: Acepta `base_build_path`, pasa a `LatexAssetManager`

### 4. **asset_manager.py** - Gestión de componentes

- Cambiado `components/` por `componentes/` (Spanish)
- Ajuste de rutas relativas para `\input` en LaTeX:
  - Desde `build/latex/digital/{topic}/Examen.tex`
  - Componentes en: `build/latex/digital/{topic}/componentes/*.tex`
  - Ruta relativa en LaTeX: `\input{componentes/nombre.tex}`
  - Para recursos fijos: `\input{../../../../resources/latex/nombre.tex}`

### 5. **compiler.py** - Copia de PDFs

- Agregado parámetro `final_output_dir` (ej: `"out/digital"`)
- PDFs se generan en `build/latex/digital/` y se copian a `out/digital/`

### 6. **secuencial/generators.py** - Bug fix

- Agregado parámetro faltante `total_cycles` en `SequentialExerciseData`

## Ventajas de la Nueva Estructura

✅ **Escalabilidad**: Fácil agregar nuevos tópicos (análógica, digital-avanzado, etc.)  
✅ **Organización**: Componentes separados por módulo, no todos mezclados  
✅ **Claridad**: PDFs finales en `out/` separados por tipo  
✅ **Flexibilidad**: Cada renderer puede tener su propia estructura de componentes  
✅ **Mantenibilidad**: Fácil encontrar componentes de un tópico específico

## Estructura Final

```
GeneradorDeExamenesFE/
├── build/
│   └── latex/
│       ├── digital/
│       │   ├── numeracion/
│       │   │   ├── Examen_V2.tex
│       │   │   ├── Solucion_V2.tex
│       │   │   └── componentes/
│       │   │       ├── ej1_...tex
│       │   │       └── ...
│       │   ├── combinacional/
│       │   │   ├── Examen_V2.tex
│       │   │   ├── Solucion_V2.tex
│       │   │   └── componentes/
│       │   │       ├── ej2_kmap.tex
│       │   │       └── ...
│       │   └── secuencial/
│       │       ├── Examen_V2.tex
│       │       ├── Solucion_V2.tex
│       │       └── componentes/
│       │           ├── ej5_circuit.tex
│       │           └── ...
│       └── analogica/componentes/    (preparado para el futuro)
├── out/
│   ├── digital/
│   │   ├── Examen_V2.pdf
│   │   └── Solucion_V2.pdf
│   └── analogica/                     (preparado para el futuro)
└── resources/
    └── latex/                         (recursos fijos, sin cambios)
```

## Próximos Pasos Sugeridos

1. **Agregar soporte para análógica**: Crear `modules/analogica/generators.py` y `renderers/latex/analogica_renderer.py`
2. **Permitir múltiples tópicos en un examen**: Actualmente todo es digital, pero la estructura permite mezclar
3. **Actualizar configuración**: Agregar campo `work_type` en `config/test_exam.json` para especificar si es digital o análógica
