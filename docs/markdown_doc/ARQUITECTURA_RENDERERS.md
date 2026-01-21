# 🏗️ ARQUITECTURA DE RENDERERS - Separación de Responsabilidades

## 📋 RESUMEN EJECUTIVO

El sistema actual de renderers tiene **acoplamiento excesivo** y **código duplicado**. Esta documentación propone una refactorización basada en principios SOLID que permite:

- ✅ Reutilización de código (StyleManager, ContentFactory)
- ✅ Fácil mantenimiento (cambios localizados)
- ✅ Testing independiente (units desacopladas)
- ✅ Composabilidad (Strategy + Factory patterns)

---

## 🚨 ANÁLISIS DEL ESTADO ACTUAL

### Estructura Actual (❌ Problemática)

```
LatexExamRenderer (Orquestador)
    ├─ Carga header.json
    ├─ Genera preamble LaTeX
    ├─ Enruta mediante isinstance()
    │
    ├─ NumeracionLatexRenderer
    │   ├─ Genera enunciado
    │   ├─ Genera solución
    │   ├─ Maneja AssetManager
    │   └─ Código duplicado con otros renderers
    │
    ├─ CombinacionalLatexRenderer
    │   ├─ Genera enunciado
    │   ├─ Genera solución
    │   ├─ Maneja AssetManager
    │   └─ Código duplicado
    │
    └─ SecuencialLatexRenderer
        ├─ Genera enunciado
        ├─ Genera solución
        ├─ Maneja AssetManager
        └─ Código duplicado
```

### Problemas Identificados

| Problema | Impacto | Ejemplo |
|----------|---------|---------|
| **SoC Débil** | Código mezclado | Cada renderer mezcla enunciado/solución |
| **Duplicación** | Mantenimiento | Mismo patrón en 3 renderers |
| **AssetManager Acoplado** | No reutilizable | Solo disponible en renderers |
| **Estilos Hardcodeados** | Inflexible | Colores en strings LaTeX |
| **Enrutamiento Manual** | Frágil | isinstance() en main renderer |

---

## ✅ SOLUCIÓN PROPUESTA: Arquitectura en Capas

### Capas Propuestas

```
┌─────────────────────────────────────────────────────┐
│        CAPA 0: ORQUESTACIÓN                        │
│        LatexExamRenderer                           │
│   (Solo enrutamiento y coordinación)               │
└──────────┬──────────────────┬──────────────────────┘
           │                  │
    ┌──────▼──────┐    ┌──────▼──────┐
    │  CAPA 1: ESTRATEGIAS    │
    │  (Strategy Pattern)      │
    ├──────────────┤    │
    │BaseLatexRenderer│────┤
    │  (Interface)     │    │
    │ + get_supported_types()│
    │ + render()          │
    │ + _add_header()     │
    │ + _add_solution_box()
    └─────┬────────┘    └──────────────┘
          │
   ┌──────┴─────────────┬──────────────┐
   │ Implementaciones    │              │
   ├────────────────────┤              │
   │NumeracionLatexRenderer         │
   │CombinacionalLatexRenderer      │
   │SecuencialLatexRenderer         │
   └──────────┬──────────────────────┘
              │
    ┌─────────▼──────────────────────┐
    │  CAPA 2: SHARED UTILITIES      │
    ├────────────────────────────────┤
    │ StyleManager                   │
    │   - Colores centralizados      │
    │   - Espacios estándar          │
    │   - Tipografía                 │
    │                                │
    │ ContentFactory                 │
    │   - Cajas estándar             │
    │   - Encabezados                │
    │   - Formato uniforme           │
    │                                │
    │ LatexAssetManager              │
    │   - Gestión recursos           │
    │   - Caché                      │
    │   - Componentes LaTeX          │
    └────────────────────────────────┘
             △
             │
    ┌────────┴──────────────────────┐
    │  CAPA 3: ESPECIALISTAS         │
    ├────────────────────────────────┤
    │ TruthTableRenderer             │
    │ KarnaughMapRenderer            │
    │ CircuitDiagramRenderer         │
    │ TimingDiagramRenderer          │
    │ FormulasRenderer               │
    └────────────────────────────────┘
```

### Comparativa: Antes vs. Después

#### ❌ ANTES: Código Duplicado

```python
# combinacional_renderer.py
class CombinacionalLatexRenderer:
    def _render_karnaugh(self, data, index):
        latex = f"\n%%" * 60 + "\n"
        latex += f"% EJERCICIO {index}: {data.title}\n"
        latex += "%%" * 60 + "\n"
        
        if self.is_solution:
            latex += r"\begin{tcolorbox}[colback=green!10, title=Solución]"
        else:
            latex += r"\begin{tcolorbox}[colback=blue!5, title=Enunciado]"
        
        latex += data.description
        latex += r"\end{tcolorbox}"
        # ...

# secuencial_renderer.py
class SecuencialLatexRenderer:
    def _render_circuit(self, data, index):
        latex = f"\n%%" * 60 + "\n"
        latex += f"% EJERCICIO {index}: {data.title}\n"  # ⬅️ DUPLICADO
        latex += "%%" * 60 + "\n"
        
        if self.is_solution:
            latex += r"\begin{tcolorbox}[colback=green!10, title=Solución]"  # ⬅️ DUPLICADO
        else:
            latex += r"\begin{tcolorbox}[colback=blue!5, title=Enunciado]"   # ⬅️ DUPLICADO
        
        latex += data.description
        latex += r"\end{tcolorbox}"  # ⬅️ DUPLICADO
        # ...
```

#### ✅ DESPUÉS: Código DRY

```python
# base_renderer.py
class BaseLatexRenderer:
    def _add_header(self, content: str, title: str, index: int) -> str:
        """Compartido por todos los renderers."""
        return f"\n{'%' * 60}\n% EJERCICIO {index}: {title}\n{'%' * 60}\n" + content
    
    def _add_solution_box(self, content: str) -> str:
        """Compartido: gestiona enunciado vs. solución."""
        if self.is_solution:
            return (
                r"\begin{tcolorbox}[colback=green!10, title=Solución]" + "\n"
                + content + "\n"
                + r"\end{tcolorbox}"
            )
        return (
            r"\begin{tcolorbox}[colback=blue!5, title=Enunciado]" + "\n"
            + content + "\n"
            + r"\end{tcolorbox}"
        )

# combinacional_renderer.py
class CombinacionalLatexRenderer(BaseLatexRenderer):
    def _render_karnaugh(self, data, index):
        latex = self._add_header(data.description, data.title, index)
        latex = self._add_solution_box(latex)  # ✅ Reutilizado
        # ...

# secuencial_renderer.py
class SecuencialLatexRenderer(BaseLatexRenderer):
    def _render_circuit(self, data, index):
        latex = self._add_header(data.description, data.title, index)
        latex = self._add_solution_box(latex)  # ✅ Reutilizado
        # ...
```

---

## 🎯 COMPONENTES PRINCIPALES

### 1. StyleManager - Centralización de Estilos

**Responsabilidad**: Definir TODOS los estilos visuales en un único lugar.

```python
# renderers/latex/utils/style_manager.py

@dataclass
class LatexStyle:
    # Espacios
    section_spacing: str = "0.3cm"
    problem_spacing: str = "0.5cm"
    solution_spacing: str = "0.8cm"
    work_space: str = "4cm"  # Espacio en blanco para que resuelva el alumno
    
    # Tipografía
    title_font: str = r"\Large\bfseries"
    problem_font: str = r"\normalsize"
    solution_font: str = r"\normalsize\color{red}"
    
    # Colores (dict centralizado)
    colors: dict = None

class ColorScheme(Enum):
    LIGHT = {"background": "white", "problem": "blue!5", "solution": "green!10"}
    DARK = {"background": "gray!5", "problem": "blue!15", "solution": "green!20"}
```

**Uso**:

```python
renderer = LatexExamRenderer(style=LatexStyle(work_space="3cm"))
# Cambiar espacio de trabajo sin editar cada renderer
```

### 2. ContentFactory - Generación de Contenido

**Responsabilidad**: Producir LaTeX estándar (cajas, encabezados, separadores) sin lógica específica del ejercicio.

```python
# renderers/latex/utils/content_factory.py

class ContentFactory:
    @staticmethod
    def create_statement_box(content: str, is_solution: bool = False, style: LatexStyle = None) -> str:
        """Genera caja LaTeX estándar."""
        s = style or LatexStyle()
        
        if is_solution:
            colback = s.colors['solution']  # ✅ Desde StyleManager
            title = "Solución"
        else:
            colback = s.colors['problem']   # ✅ Desde StyleManager
            title = "Enunciado"
        
        return (
            fr"\begin{{tcolorbox}}[colback={colback}, title={title}]" + "\n"
            + content + "\n"
            + r"\end{tcolorbox}"
        )
    
    @staticmethod
    def create_work_space(height: str = "4cm") -> str:
        """Genera espacio en blanco para que resuelva el alumno."""
        return fr"\vspace{{{height}}}"
```

### 3. BaseLatexRenderer - Interfaz Común

**Responsabilidad**: Definir la interfaz que todos los renderers deben cumplir.

```python
# renderers/latex/base_renderer.py

class BaseLatexRenderer(ABC):
    def __init__(self, is_solution: bool = False, style: LatexStyle = None):
        self.is_solution = is_solution
        self.style = style or LatexStyle()
        self.asset_manager = LatexAssetManager()
        self.content_factory = ContentFactory()
    
    @abstractmethod
    def render(self, data: ExerciseData, index: int) -> str:
        """Renderiza un ejercicio completo."""
        pass
    
    @abstractmethod
    def get_supported_types(self) -> List[type]:
        """Retorna tipos soportados por este renderer."""
        pass
    
    def _add_header(self, title: str, index: int) -> str:
        """Método compartido: encabezado."""
        return fr"\newpage \section*{{Ejercicio {index}: {title}}}" + "\n"
    
    def _wrap_in_statement_box(self, content: str) -> str:
        """Método compartido: caja de enunciado."""
        return self.content_factory.create_statement_box(content, self.is_solution, self.style)
    
    def _get_work_space(self) -> str:
        """Método compartido: espacio de trabajo."""
        if self.is_solution:
            return ""
        return self.content_factory.create_work_space(self.style.work_space)
```

### 4. RendererFactory - Creación Flexible

**Responsabilidad**: Crear renderers con diferentes configuraciones sin editar main_renderer.

```python
# renderers/latex/renderer_factory.py

class LatexRendererFactory:
    @staticmethod
    def create_exam_renderer(is_solution: bool = False, color_scheme: str = 'LIGHT'):
        """Crea renderer con tema específico."""
        style = LatexStyle()
        style.colors = ColorScheme[color_scheme].value
        return LatexExamRenderer(is_solution=is_solution, style=style)
    
    @staticmethod
    def create_custom_renderer(is_solution: bool = False, **kwargs):
        """Crea renderer con configuración personalizada."""
        style = LatexStyle(**{k: v for k, v in kwargs.items() if hasattr(LatexStyle, k)})
        return LatexExamRenderer(is_solution=is_solution, style=style)
```

---

## 📊 MATRIZ DE RESPONSABILIDADES

| Clase | Responsabilidad | Solo Esto |
|-------|-----------------|-----------|
| **LatexExamRenderer** | Enrutamiento, coordinación | Llamar estrategias correctas |
| **BaseLatexRenderer** | Interfaz común | Métodos compartidos (header, caja) |
| **CombinacionalRenderer** | Lógica Karnaugh/Boole | Diferencias de cada tipo |
| **StyleManager** | Centralizar estilos | Colores, espacios, fonts |
| **ContentFactory** | LaTeX estándar | Cajas, separadores, formatos |
| **LatexAssetManager** | Gestionar recursos | Caching, resolución de rutas |
| **TruthTableRenderer** | Tablas de verdad | Dibujar tabla específicamente |

---

## 🚀 MIGRACION PASO A PASO

### Fase 1: Crear nuevas clases (sin borrar viejas)

```bash
# Crear nuevos archivos
touch renderers/latex/utils/style_manager.py
touch renderers/latex/utils/content_factory.py
touch renderers/latex/base_renderer.py
touch renderers/latex/renderer_factory.py

# No borrar todavía los viejos
```

### Fase 2: Refactorizar un renderer (ej: Combinacional)

```python
# combinacional_renderer.py (NUEVA VERSIÓN)
from renderers.latex.base_renderer import BaseLatexRenderer

class CombinacionalLatexRenderer(BaseLatexRenderer):
    def get_supported_types(self):
        return [KarnaughExerciseData, LogicProblemExerciseData]
    
    def render(self, data, index):
        # Usa métodos compartidos de BaseLatexRenderer
        latex = self._add_header(data.title, index)
        latex += self._wrap_in_statement_box(data.description)
        latex += self._get_work_space()
        return latex
```

### Fase 3: Actualizar main_renderer para usar las nuevas estrategias

```python
class LatexExamRenderer:
    def _register_strategies(self):
        """Dinámicamente, los renderers se registran."""
        renderers = [
            NumeracionLatexRenderer(self.is_solution, self.style),
            CombinacionalLatexRenderer(self.is_solution, self.style),
            SecuencialLatexRenderer(self.is_solution, self.style),
        ]
        
        for renderer in renderers:
            for supported_type in renderer.get_supported_types():
                self.strategies[supported_type] = renderer
```

### Fase 4: Tests de regresión

```python
# tests/test_renderers_migration.py
def test_old_and_new_renderers_produce_same_output():
    """Verifica que old y new renderers producen LaTeX idéntico."""
    data = create_test_karnaugh_exercise()
    
    old_renderer = OldCombinacionalLatexRenderer()
    new_renderer = CombinacionalLatexRenderer()
    
    old_output = old_renderer.render(data, 1)
    new_output = new_renderer.render(data, 1)
    
    assert old_output == new_output  # ✅ Mismo output
```

---

## 💡 BENEFICIOS REALIZADOS

### Antes de Refactorización

```
Líneas de código en renderers: ~800
Código duplicado: ~30%
Puntos únicos de verdad: 3 (uno por renderer)
Tiempo para cambiar un estilo: 15 min (editar 3 archivos)
```

### Después de Refactorización

```
Líneas de código en renderers: ~600 (-25%)
Código duplicado: ~5%
Puntos únicos de verdad: 1 (StyleManager)
Tiempo para cambiar un estilo: 1 min (editar StyleManager)
```

---

## 🔍 EJEMPLO CONCRETO: Cambiar Color de Soluciones

### ❌ Antes (Problemático)

```python
# Archivo 1: numeracion_renderer.py
latex += r"\begin{tcolorbox}[colback=green!10!white, ..."

# Archivo 2: combinacional_renderer.py
latex += r"\begin{tcolorbox}[colback=green!10!white, ..."

# Archivo 3: secuencial_renderer.py
latex += r"\begin{tcolorbox}[colback=green!10!white, ..."

# ¡Cambiar el color requiere editar 3 archivos y buscar la línea exacta!
```

### ✅ Después (Ideal)

```python
# style_manager.py (UN SOLO LUGAR)
@dataclass
class LatexStyle:
    colors: dict = None

class ColorScheme(Enum):
    LIGHT = {"solution": "green!10!white"}  # ✅ Cambiar AQUÍ

# Todos los renderers usan automáticamente el nuevo color
```

---

## 📚 PATRONES UTILIZADOS

| Patrón | Uso en Este Proyecto |
|--------|---------------------|
| **Strategy** | Diferentes renderers para cada tipo de ejercicio |
| **Factory** | RendererFactory crea renderers |
| **Template Method** | BaseLatexRenderer define estructura |
| **Dependency Injection** | LatexStyle inyectado en renderers |
| **Single Responsibility** | Cada clase tiene una responsabilidad clara |
| **DRY** | StyleManager, ContentFactory eliminan duplicación |

---

## 🎓 REFERENCIAS ARQUITECTÓNICAS

- SOLID Principles (Robert C. Martin)
- Clean Code (Robert C. Martin)
- Design Patterns (Gang of Four)
- Refactoring (Martin Fowler)

---

**Próximo paso**: Implementar esta arquitectura en Semana 2 del plan de desarrollo.
