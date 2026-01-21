# 🎯 RESUMEN: Arquitectura de Renderers - Separación de Responsabilidades

## ¿POR QUÉ ES IMPORTANTE?

**Problema Actual**: Los 3 renderers (Numeración, Combinacional, Secuencial) tienen **mucho código idéntico** (encabezados, cajas de enunciado/solución, estilos). Esto viola el principio **DRY** (Don't Repeat Yourself).

**Costo**: Cuando quieres cambiar algo (ej: color de soluciones), tienes que editar **3 archivos en 3 lugares diferentes**.

---

## ✅ SOLUCIÓN: Arquitectura en Capas

### Las 4 Capas Principales

```
┌────────────────────────────────────────┐
│ CAPA 1: ORQUESTACIÓN                   │
│ LatexExamRenderer                      │
│ (Enrutamiento: ¿Qué tipo es?)          │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ CAPA 2: ESTRATEGIAS (Strategy Pattern) │
│ • NumeracionLatexRenderer              │
│ • CombinacionalLatexRenderer           │
│ • SecuencialLatexRenderer              │
│ Todos heredan de BaseLatexRenderer     │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ CAPA 3: UTILIDADES COMPARTIDAS         │
│ • StyleManager (colores, espacios)     │
│ • ContentFactory (cajas LaTeX)         │
│ • LatexAssetManager (recursos)         │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ CAPA 4: ESPECIALISTAS                  │
│ • TruthTableRenderer                   │
│ • KarnaughMapRenderer                  │
│ • TimingDiagramRenderer                │
└────────────────────────────────────────┘
```

---

## 📝 Ejemplo: ¿Cómo Renderizar un Ejercicio?

### ANTES ❌ (Alto Acoplamiento)

```python
# Cada renderer hace TODO:

class CombinacionalLatexRenderer:
    def render(self, data, index):
        # 1. Crear encabezado (código copiado de otros)
        latex = f"\\newpage \\section*{{Ejercicio {index}: {data.title}}}"
        
        # 2. Crear caja (código copiado de otros)
        latex += r"\begin{tcolorbox}[colback=blue!5, title=Enunciado]"
        latex += data.description
        latex += r"\end{tcolorbox}"
        
        # 3. Dibujar tabla (especialidad de este renderer)
        latex += self.tt_renderer.render(...)
        
        # 4. Espacio o solución (código copiado de otros)
        if self.is_solution:
            latex += r"\begin{tcolorbox}[colback=green!10, title=Solución]"
            latex += data.solution_expr
            latex += r"\end{tcolorbox}"
        else:
            latex += r"\vspace{4cm}"
        
        return latex
```

### DESPUÉS ✅ (Bajo Acoplamiento)

```python
# Cada renderer solo hace su especialidad

class CombinacionalLatexRenderer(BaseLatexRenderer):
    def render(self, data, index):
        # 1. Encabezado (heredado de BaseLatexRenderer)
        latex = self._add_header(data.title, index)
        
        # 2. Caja de enunciado (heredado + StyleManager)
        latex += self._wrap_in_statement_box(data.description)
        
        # 3. Dibujar tabla (nuestra especialidad)
        latex += self.tt_renderer.render(...)
        
        # 4. Espacio o solución (heredado de BaseLatexRenderer)
        latex += self._get_work_space_or_solution(data)
        
        return latex
```

---

## 🔧 Nuevos Archivos a Crear

| Archivo | Responsabilidad | Líneas |
|---------|-----------------|--------|
| `style_manager.py` | Colores, espacios, fonts | ~50 |
| `content_factory.py` | Generar LaTeX estándar | ~60 |
| `base_renderer.py` | Interfaz común + métodos compartidos | ~70 |
| `renderer_factory.py` | Crear renderers con configs | ~30 |

**Total**: ~210 líneas de código NUEVO que elimina ~240 líneas DUPLICADAS

---

## 🎯 Cambio de Ejemplo: Modificar Color de Soluciones

### ANTES ❌: 3 ediciones en 3 archivos

```
numeracion_renderer.py:   LÍNEA 45  →  colback=green!10  →  colback=yellow!10
combinacional_renderer.py: LÍNEA 67  →  colback=green!10  →  colback=yellow!10
secuencial_renderer.py:    LÍNEA 89  →  colback=green!10  →  colback=yellow!10
```

### DESPUÉS ✅: 1 edición en 1 archivo

```
style_manager.py: LÍNEA 12  →  "solution": "green!10"  →  "solution": "yellow!10"
```

---

## 💡 Principios Aplicados

| Principio | Cómo se aplica |
|-----------|----------------|
| **S** (Single Resp.) | Cada clase tiene UNA responsabilidad |
| **O** (Open/Closed) | Abierto a extensión (nuevos renderers), cerrado a modificación |
| **L** (Liskov) | Todos los renderers cumplen contrato BaseLatexRenderer |
| **I** (Interface Seg.) | Renderers solo heredan lo que necesitan |
| **D** (Dependency Inv.) | Inyección de StyleManager en lugar de hardcoding |

---

## 📊 Impacto de la Refactorización

```
MÉTRICA                 ANTES    DESPUÉS    MEJORA
────────────────────────────────────────────────────
Código duplicado        ~30%     ~5%        -83%
Puntos de edición       3        1          -67%
Tiempo cambio estilo    15 min   1 min      -93%
Testing difficultad     Alto     Bajo       ✅
Extensibilidad          Baja     Alta       ✅
```

---

## 🚀 Plan de Implementación

**SEMANA 2**: Refactorización de Renderers

```
Lunes-Martes:    Crear nuevas clases base (style_manager, content_factory)
Miércoles:       Refactorizar combinacional_renderer
Jueves:          Refactorizar secuencial_renderer y numeracion_renderer
Viernes:         Tests y validación (asegurar mismo output)
```

**Garantías**:

- ✅ Output LaTeX idéntico (tests de regresión)
- ✅ Código más limpio y mantenible
- ✅ Más fácil agregar nuevos renderers

---

## 🔗 Documentación Completa

Para detalles técnicos, consulta: [ARQUITECTURA_RENDERERS.md](ARQUITECTURA_RENDERERS.md)

---

**Resumen ejecutivo para el equipo**: "Vamos a refactorizar renderers para eliminar duplicación de código. El output será exactamente igual, pero el código será mucho más fácil de mantener."
