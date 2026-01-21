# 📋 PLAN DE ACCIÓN - Próximas 2 Semanas

## 🎯 OBJETIVO GENERAL

Convertir el generador de exámenes **de prototipo frágil a sistema robusto** con:

- ✅ Solvers que calculan automáticamente soluciones
- ✅ Compilador automático LaTeX → PDF
- ✅ Arquitectura de renderers sin duplicación
- ✅ Output: Examen_V2.pdf + Solucion_V2.pdf listos para usar

---

## 📅 SEMANA 1: SOLVERS + COMPILADOR (35 horas)

### Objetivo: Que los generadores calculen soluciones reales

#### MON-TUE: Solvers de Numeración (8h)

**Archivo**: `modules/numeracion/generators.py`

Tarea específica:

```python
# Implementar función _calculate_addition_with_carry()
# Input: a=5, b=3 (en decimal) → base=2 (binario)
# Output: (resultado='1000', carry_bits='0101', overflow=False)

# Lógica:
# 1. Convertir operandos a la base especificada
# 2. Sumar/restar bit a bit
# 3. Guardar acarreo de cada etapa
# 4. Detectar overflow (carry_out != carry_in en último bit)
```

Tests:

- [ ] Test simple: 1 + 1 = 10 (binario)
- [ ] Test con acarreo: 111 + 1 = 1000 (binario)
- [ ] Test overflow: 7 + 1 en 3 bits

**Entrega**: `solution_carry_bits` se rellena automáticamente ✅

---

#### WED: Solvers de Combinacional - Simplificación Booleana (10h)

**Archivo**: `modules/combinacional/generators.py`

Dependencia: `pip install sympy`

**🎯 ESTRATEGIA SELECCIONADA: Opción A (Hybrid)**

```
SEMANA 1-2: SymPy (MVP rápido, confiable)
SEMANA 3+:  Quine-McCluskey didáctico (opcional, valor pedagógico)
```

**¿POR QUÉ SYMPY AHORA?**

- ✅ Implementación rápida (10h vs. 30h con QM)
- ✅ Código confiable (probado por miles de usuarios)
- ✅ Mantiene focus en otros solvers importantes
- ✅ Prepara infraestructura para QM opcional después
- ✅ Soporta hasta 8+ variables sin problemas

Tarea específica (Semana 1):

```python
# Usar SymPy para simplificar funciones booleanas
from sympy.logic import SOPform, POSform
from sympy import symbols, latex

# Input: truth_table_outputs = [0,1,1,0,1,0,1,1] (para F(A,B,C))
# Output: solution_expr = "$A \\bar{C} + B$"

# Pasos:
# 1. Encontrar minterms (posiciones donde output=1)
# 2. Llamar SOPform(variables, minterms)  ← SymPy maneja todo
# 3. Convertir resultado a LaTeX
```

Tests:

- [ ] AND: F = AB
- [ ] OR: F = A + B
- [ ] Karnaugh 3 variables simplificado
- [ ] Karnaugh 4 variables con minimización
- [ ] Función 5 variables (complejidad media)
- [ ] Función 8 variables (máximo actual)

**NOTA**: Quine-McCluskey completo (con Petrick) → Semana 3 como módulo opcional. Ver [ROADMAP_QUINE_McCLUSKEY.md](ROADMAP_QUINE_McCLUSKEY.md).

**Entrega**: `solution_expr` se rellena con fórmula simplificada ✅

---

#### THU: Solvers de Secuencial - Simulador de FF (10h)

**Archivo**: `modules/secuencial/generators.py`

Tarea específica:

```python
# Simular flip-flops ciclo a ciclo
# Input: ff_type='D', input_sequence='HHLLHHLH' (2 chars/ciclo), initial_q=0
# Output: solution_q0='HHLLLLHH' (Q salida por ciclo)

# Lógica por tipo de FF:
# D-FF:  Q_next = D
# T-FF:  Q_next = Q XOR T
# JK-FF: Q_next según tabla (J,K) → (0,0=hold, 0,1=clear, 1,0=set, 1,1=toggle)

# Formato de entrada/salida es tikz-timing:
# 'H' = alto (1), 'L' = bajo (0)
# 2 caracteres por ciclo de reloj
```

Tests:

- [ ] D-FF con entrada 01010101
- [ ] T-FF con entrada 11111111 (toggles puros)
- [ ] JK-FF con secuencia compleja

**Entrega**: `solution_q0` (y opcional `solution_q1`) se rellenan ✅

---

#### FRI: Compilador LaTeX + Integration (7h)

**Archivo nuevo**: `renderers/latex/utils/compiler.py`

Tarea específica:

```python
# Crear función compile_tex_to_pdf(tex_file_path) -> bool
# Que:
# 1. Llame lualatex -interaction=nonstopmode
# 2. Ejecute 2 veces (para resolver referencias)
# 3. Limpie archivos auxiliares (.aux, .log, .out)
# 4. Verifique que .pdf se creó exitosamente

# Integración en main_v2.py:
# - Después de generar Examen_V2.tex → llamar compile_tex_to_pdf
# - Después de generar Solucion_V2.tex → llamar compile_tex_to_pdf
```

Tests:

- [ ] Compilar LaTeX simple sin errores
- [ ] Compilar con TikZ (circuitikz)
- [ ] Compilar con tikz-timing
- [ ] Limpiar archivos basura

**Entrega**: `Examen_V2.pdf` + `Solucion_V2.pdf` generados automáticamente ✅

---

### 📊 MÉTRICA SEMANA 1

```
ANTES                          DESPUÉS
─────────────────────────────────────────
Soluciones calculadas: NO      Soluciones calculadas: SÍ ✅
PDFs generados: Manual         PDFs generados: Automático ✅
Enunciados: Completos          Enunciados: Completos ✅
Soluciones en PDF: Vacías      Soluciones en PDF: LLENAS ✅

TESTS:
Solvers: 0%  →  80%
Compilador: 0%  →  100%
```

---

## 📅 SEMANA 2: REFACTORIZACIÓN RENDERERS + INTEGRACIÓN (40 horas)

### Objetivo: Eliminar duplicación, hacer código mantenible

#### MON-TUE: Crear Clases Base (10h)

**Archivos nuevos**:

1. `renderers/latex/utils/style_manager.py` (5h)
   - Definir `LatexStyle` (dataclass con todos los estilos)
   - Definir `ColorScheme` (enum: LIGHT, DARK)
   - NO debe contener lógica de negocio, solo configuración

2. `renderers/latex/utils/content_factory.py` (3h)
   - `ContentFactory.create_statement_box()` → caja LaTeX
   - `ContentFactory.create_work_space()` → espacio en blanco
   - `ContentFactory.create_header()` → encabezado

3. `renderers/latex/base_renderer.py` (2h)
   - Clase abstracta `BaseLatexRenderer`
   - Métodos compartidos: `_add_header()`, `_wrap_in_statement_box()`, etc.
   - Interfaz: `render()` y `get_supported_types()` abstractos

**Tests**: Unit tests para cada clase en aislamiento

---

#### WED: Refactorizar Renderers (12h)

**Archivos a refactorizar** (sin cambiar output):

1. `renderers/latex/combinacional_renderer.py` (4h)
   - Heredar de `BaseLatexRenderer`
   - Implementar `get_supported_types()`
   - Simplificar `_render_karnaugh()` usando métodos heredados

2. `renderers/latex/secuencial_renderer.py` (4h)
   - Lo mismo que combinacional

3. `renderers/latex/numeracion_renderer.py` (4h)
   - Lo mismo que combinacional

**Validación**: Tests de regresión (nuevo output == viejo output)

---

#### THU: Factory + Orquestación (8h)

**Archivos**:

1. `renderers/latex/renderer_factory.py` (3h)
   - `LatexRendererFactory.create_exam_renderer()`
   - `LatexRendererFactory.create_custom_renderer()`

2. Refactorizar `renderers/latex/main_renderer.py` (5h)
   - Cambiar de hardcoding a Strategy Pattern
   - Registrar dinámicamente renderers disponibles
   - Solo hacer enrutamiento (sin lógica específica)

**Tests**: Integration tests (ExamBuilder → Renderers → LaTeX)

---

#### FRI: Tests Completos (10h)

1. **Tests de Regresión** (5h)
   - Verificar que old y new renderers producen LaTeX idéntico
   - Compilar ambos y comparar PDFs

2. **Tests End-to-End** (3h)
   - ExamBuilder → Solvers → Renderers → Compilador → PDF
   - Verificar que Examen_V2.pdf + Solucion_V2.pdf son correctos

3. **Documentación** (2h)
   - Actualizar docstrings
   - Crear guía de "cómo agregar un nuevo renderer"

---

### 📊 MÉTRICA SEMANA 2

```
ANTES                          DESPUÉS
─────────────────────────────────────────
Código duplicado: 30%          Código duplicado: 5% ✅
Puntos de edición: 3           Puntos de edición: 1 ✅
Cobertura tests: 40%           Cobertura tests: 85% ✅
Tiempo mantener: Alto          Tiempo mantener: Bajo ✅

ARQUITECTURA:
├─ StyleManager: Centraliza todos los estilos ✅
├─ ContentFactory: Genera LaTeX estándar ✅
├─ BaseLatexRenderer: Métodos compartidos ✅
├─ RendererFactory: Crear renderers flexibles ✅
└─ main_renderer: Solo orquestación ✅
```

---

## 🎁 ENTREGABLES FINALES

### Por Semana 1

```
✅ modules/numeracion/generators.py          (solvers con carry)
✅ modules/combinacional/generators.py       (solvers con SymPy)
✅ modules/secuencial/generators.py          (solvers con simulación)
✅ renderers/latex/utils/compiler.py         (compilador automático)
✅ Examen_V2.pdf                             (enunciado completo)
✅ Solucion_V2.pdf                           (soluciones calculadas)
✅ Tests para solvers (~50 casos)            (cobertura 80%+)
```

### Por Semana 2

```
✅ renderers/latex/utils/style_manager.py    (estilos centralizados)
✅ renderers/latex/utils/content_factory.py  (LaTeX estándar)
✅ renderers/latex/base_renderer.py          (interfaz común)
✅ renderers/latex/renderer_factory.py       (factory pattern)
✅ renderers/latex/main_renderer.py          (REFACTORIZADO)
✅ renderers/latex/*_renderer.py             (REFACTORIZADOS x3)
✅ ARQUITECTURA_RENDERERS.md                 (documentación)
✅ Tests de regresión                        (0 diferencias)
✅ Tests end-to-end                          (pipeline completo)
```

### TOTAL

```
📊 Líneas nuevas: ~1500
📊 Líneas refactorizadas: ~600
📊 Código duplicado eliminado: ~240
📊 Tests totales: ~120
📊 Cobertura: 85%+
```

---

## ⚠️ RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|-----------|
| SymPy complejo | Media | Usar ejemplos, tests simples primero |
| LaTeX compilation fails | Baja | Probar en máquina + CI/CD early |
| Refactoring breaks output | Baja | Tests de regresión antes de cambios |
| Tiempo estimado insuficiente | Media | Priorizar solvers > compilador > refactoring |

**Fallback**: Si refactoring toma más tiempo, mantener old renderers como backup.

---

## 🏁 CHECKPOINT FINAL

**Fin de semana 19 de enero - Validar que TODO funciona**:

```bash
$ python main_v2.py

🚀 Generador de Exámenes V2.1 (con Solvers)

✅ Numeracion: 2 ejercicios con soluciones calculadas
✅ Combinacional: 3 ejercicios con Karnaugh simplificado
✅ Secuencial: 2 ejercicios con cronogramas simulados

✅ Compilando Examen_V2.pdf...
✅ Compilando Solucion_V2.pdf...

✨ ¡Listo! Archivos en build/latex/
```

```
$ ls -lh build/latex/*.pdf
Examen_V2.pdf        (250 KB)  ✅
Solucion_V2.pdf      (260 KB)  ✅
```

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Qué pasa si LaTeX no está instalado?**
R: Verificar en Semana 1. Instalar TeXLive (Ubuntu) o MiKTeX (Windows) antes de empezar.

**P: ¿Los PDFs viejos van a cambiar?**
R: No. El contenido será el mismo, solo que las soluciones estarán rellenadas (antes estaban vacías).

**P: ¿Puedo trabajar en Solvers mientras alguien refactoriza Renderers?**
R: Sí. Son independientes. Solvers en Semana 1, Renderers en Semana 2.

**P: ¿Qué si SymPy es lento?**
R: Usamos caché. Los solvers se corren una sola vez al generar el examen.

---

## 📚 RECURSOS NECESARIOS

```
SOFTWARE:
- Python 3.9+
- pip (gestor de paquetes)
- Git (control de versiones)
- TeXLive / MiKTeX (para compilar LaTeX)

LIBRERÍAS PYTHON:
pip install sympy pytest pytest-cov

DOCUMENTACIÓN CONSULTABLE:
- SymPy documentation: https://docs.sympy.org
- TikZ manual: https://tikz.dev
- SOLID principles: https://en.wikipedia.org/wiki/SOLID
```

---

**Versión**: 2.1 Plan
**Fecha**: 15 de enero de 2026
**Responsable**: Equipo de Desarrollo
**Estado**: 🟡 Planeado
