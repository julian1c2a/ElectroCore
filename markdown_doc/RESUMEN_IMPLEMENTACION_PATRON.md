# Resumen: Patrón de Separación Problema ↔ Solución

## 🎯 Qué Se Implementó

Has identificado un problema arquitectónico crítico: **Los JSON de ejercicios mezclaban parámetros del problema con parámetros de la solución**, lo que hacía confuso:

- Qué mostrar en enunciado
- Qué mostrar en soluciones
- Cómo validar que no haya fuga de respuestas

### Solución Implementada

Aplicamos un **patrón de separación explícita** en todos los modelos de datos:

```python
@dataclass
class EjercicioData:
    # PARÁMETROS DEL PROBLEMA (visible en enunciado)
    label: str
    problem_var: int
    
    # PARÁMETROS DE LA SOLUCIÓN (solo en PDF con is_solution=True)
    solution_answer: str
    solution_details: dict
```

---

## 📚 Archivos Documentados

### 1. **PATRON_SEPARACION_PROBLEMA_SOLUCION.md** (20KB)

- Define el patrón arquitectónico general
- Explica beneficios
- Muestra 3 ejemplos (numeración, combinacional, secuencial)
- Lista cambios necesarios

### 2. **ESTRUCTURA_CONVERSION_ROW.md** (8KB)

- Ejemplo detallado para numeración
- Explicación de `target_col_idx`
- Validación de `representable`
- Casos de uso

### 3. **REFERENCIA_RAPIDA_PARAMETROS.md** (12KB)

- Tablas rápidas de qué mostrar cuándo
- Checklist para implementar
- Errores comunes
- Ejemplos de código

---

## 🔧 Cambios en Código

### Numeración (modules/numeracion/models.py)

```diff
@dataclass
class ConversionRow:
+   """
+   ════════════════════════════════════════════════════════════
+   PARÁMETROS DEL PROBLEMA
+   ════════════════════════════════════════════════════════════
+   """
    label: str
    val_decimal: int
    target_col_idx: int
    representable: bool
    
+   """
+   ════════════════════════════════════════════════════════════
+   PARÁMETROS DE LA SOLUCIÓN
+   ════════════════════════════════════════════════════════════
+   """
    target_val_str: str
    sol_bin: str
    sol_c2: str
    sol_sm: str
    sol_bcd: str
```

Similar para `ArithmeticOp`, `KarnaughExerciseData`, etc.

---

## ✅ Beneficios Inmediatos

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Claridad** | ¿Qué mostrar? Adivinar | Código dice qué mostrar |
| **Seguridad** | Posible filtración accidental | Imposible si sigues el patrón |
| **Testing** | Difícil validar separación | Fácil de verificar |
| **Mantenimiento** | Confuso para nuevo dev | Autodocumentado |
| **Extensibilidad** | Agregar solución = riesgo | Agregar solución = safe |

---

## 🎓 Cómo Usar en Desarrollo

### Para Desarrolladores de Generadores

Cuando crees un nuevo tipo de ejercicio:

1. Define `@dataclass XyzExerciseData`
2. Comenta claramente qué es problema vs solución
3. Asegúrate de que problema sea **invariante** (no cambia con la solución)
4. Solución debe ser **calculable** a partir del problema

### Para Desarrolladores de Renderers

Cuando implementes un renderer:

```python
def render(self, data: XyzExerciseData) -> str:
    # SIEMPRE mostrar:
    show(data.problem_param1)
    show(data.problem_param2)
    
    # SOLO si is_solution=True:
    if self.is_solution:
        show_in_red(data.solution_param1)
        show_in_red(data.solution_param2)
```

### Para Implementar en Renderers (Próximo Paso)

Actualizar estos archivos para respetar la separación:

- `renderers/latex/numeracion_renderer.py`
- `renderers/latex/combinacional_renderer.py`
- `renderers/latex/secuencial_renderer.py`

Cada uno debe:

1. Mostrar solo parámetros del problema en enunciado
2. Mostrar soluciones en rojo en PDF de soluciones
3. Documentar qué campos se muestran cuándo

---

## 📊 Matriz de Cambios

| Módulo | Archivo | Cambios |
|--------|---------|---------|
| **core** | `generator_base.py` | ✓ Sin cambios (base es agnóstica) |
| **numeracion** | `models.py` | ✓ Actualizado: ConversionRow + ArithmeticOp |
| **numeracion** | `generators.py` | ✓ Actualizado: pasa `representable` |
| **numeracion** | `numeracion_renderer.py` | ⏳ Pendiente: actualizar para respetar patrón |
| **combinacional** | `models.py` | ✓ Actualizado: Karnaugh + LogicProblem + MSI |
| **combinacional** | `generators.py` | ⏳ Pendiente: agregar campos de solución |
| **combinacional** | `combinacional_renderer.py` | ⏳ Pendiente: mostrar soluciones correctamente |
| **secuencial** | `models.py` | ✓ Actualizado: SequentialExerciseData |
| **secuencial** | `generators.py` | ⏳ Pendiente: agregar campos de solución |
| **secuencial** | `secuencial_renderer.py` | ⏳ Pendiente: mostrar salidas correctamente |

---

## 🔍 Validación

Para verificar que el patrón se sigue correctamente:

```bash
# Buscar separación clara en todos los modelos
grep -r "PARÁMETROS DEL PROBLEMA" modules/*/models.py
grep -r "PARÁMETROS DE LA SOLUCIÓN" modules/*/models.py

# Verificar que renderers no filtren por is_solution para problema
grep -r "if self.is_solution" renderers/latex/*renderer.py
```

---

## 💡 Impacto Futuro

Este patrón facilita:

1. **Múltiples soluciones** (ej: NAND + NOR para Karnaugh)

   ```python
   simplified_nand: str    # Solución con NAND
   simplified_nor: str     # Solución con NOR
   ```

2. **Distintos niveles de detalle**

   ```python
   solution_simple: str    # F = A·B
   solution_detailed: str  # F = (A AND B)
   ```

3. **Evaluación automática**

   ```python
   if student_answer == data.target_val_str:
       score = 1.0
   ```

4. **Estadísticas pedagógicas**

   ```python
   problem_difficulty = len(data.PROBLEM_PARAMS)
   solution_complexity = len(data.SOLUTION_PARAMS)
   ```

---

## 📌 Conclusión

El patrón está **documentado e implementado** en la capa de modelos. Ahora:

1. ✅ Estructura de datos lista
2. ✅ Validaciones automáticas
3. ⏳ Pendiente: actualizar renderers
4. ⏳ Pendiente: agregar campos de solución faltantes

Con esto, cualquier desarrollador puede:

- Saber exactamente qué mostrar en enunciado vs soluciones
- Agregar nuevas soluciones sin riesgo de fuga
- Entender la intención del código solo leyendo estructuras de datos
