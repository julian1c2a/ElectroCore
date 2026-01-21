# Referencia Rápida: Parámetros del Problema vs Solución

## 🎯 Regla de Oro

**NUNCA mostrar campos de SOLUCIÓN cuando `is_solution=False`**

```python
# ✅ CORRECTO
if is_solution:
    show(data.sol_bin)      # Solución en rojo
else:
    show(data.target_col_idx)  # Solo problema
    
# ❌ INCORRECTO
show(data.sol_bin)  # Se mostraría en ambos casos
```

---

## 📝 NUMERACIÓN

### ConversionRow - Tabla de Conversión

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `label` | str | **Problema** | Siempre |
| `val_decimal` | int | **Problema** | Siempre |
| `target_col_idx` | int | **Problema** | Siempre (define qué convertir) |
| `representable` | bool | **Problema** | En enunciado (si "NR") |
| `target_val_str` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `sol_bin` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `sol_c2` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `sol_sm` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `sol_bcd` | str | **Solución** | Solo en `is_solution=True` (rojo) |

### ArithmeticOp - Operaciones

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `op_type` | str | **Problema** | Siempre |
| `system` | str | **Problema** | Siempre |
| `operand1` | str | **Problema** | Siempre (referencia a fila) |
| `operand2` | str | **Problema** | Siempre (referencia a fila) |
| `operator_symbol` | str | **Problema** | Siempre (+ o -) |
| `val1_dec` | int | **Problema** | Mostrar los operandos originales |
| `val2_dec` | int | **Problema** | Mostrar los operandos originales |
| `result_dec` | int | **Solución** | Solo en `is_solution=True` (rojo) |
| `result_bin` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `overflow` | bool | **Solución** | Solo en `is_solution=True` |
| `underflow` | bool | **Solución** | Solo en `is_solution=True` |
| `carry_bits` | str | **Solución** | Solo en `is_solution=True` (azul) |

---

## 📊 COMBINACIONAL

### KarnaughExerciseData

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `title` | str | **Problema** | Siempre |
| `description` | str | **Problema** | Siempre |
| `vars_name` | List[str] | **Problema** | Siempre |
| `out_name` | str | **Problema** | Siempre |
| `truth_table_outputs` | List[int] | **Problema** | Siempre |
| `canon_type` | str | **Problema** | Siempre ("¿Simplifica a minitérminos?") |
| `gate_type` | str | **Problema** | Siempre ("Usa NAND") |
| `minterms` | List[int] | **Solución** | Solo en `is_solution=True` |
| `maxterms` | List[int] | **Solución** | Solo en `is_solution=True` |
| `simplified_sop` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `simplified_pos` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `simplified_nand` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `simplified_nor` | str | **Solución** | Solo en `is_solution=True` (rojo) |

### LogicProblemExerciseData

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `title` | str | **Problema** | Siempre |
| `context_title` | str | **Problema** | Siempre |
| `context_description` | str | **Problema** | Siempre |
| `variables_desc` | List[str] | **Problema** | Siempre |
| `output_desc` | str | **Problema** | Siempre |
| `logic_description` | str | **Problema** | Siempre |
| `vars_clean` | List[str] | **Problema** | Siempre |
| `out_clean` | str | **Problema** | Siempre |
| `truth_table_outputs` | List[int] | **Solución** | Solo en `is_solution=True` |
| `simplified_solution` | str | **Solución** | Solo en `is_solution=True` (rojo) |

### MSIExerciseData

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `title` | str | **Problema** | Siempre |
| `block_type` | str | **Problema** | Siempre |
| `params` | Dict | **Problema** | Siempre |
| `expected_outputs` | List[int] | **Solución** | Solo en `is_solution=True` |
| `truth_table` | List[dict] | **Solución** | Solo en `is_solution=True` |

---

## ⏱️ SECUENCIAL

### SequentialExerciseData

| Campo | Tipo | Categoría | Visibilidad |
|-------|------|-----------|-------------|
| `title` | str | **Problema** | Siempre |
| `description` | str | **Problema** | Siempre |
| `ff_type` | str | **Problema** | Siempre |
| `edge_type` | str | **Problema** | Siempre |
| `logic_type` | str | **Problema** | Siempre |
| `has_async` | bool | **Problema** | Siempre |
| `async_type` | str | **Problema** | Siempre (si `has_async=True`) |
| `async_level` | str | **Problema** | Siempre (si `has_async=True`) |
| `total_cycles` | int | **Problema** | Siempre |
| `clk_sequence` | str | **Problema** | Siempre (mostrar reloj) |
| `async_sequence` | str | **Problema** | Siempre (si `has_async=True`) |
| `input_sequence` | str | **Problema** | Siempre (J/K, D, T, etc.) |
| `output_placeholder` | str | **Problema** | En enunciado (campo vacío para alumno) |
| `output_sequence` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `output_bar_sequence` | str | **Solución** | Solo en `is_solution=True` (rojo) |
| `state_transitions` | List[dict] | **Solución** | Solo en `is_solution=True` |
| `setup_time_violations` | List[str] | **Solución** | Solo en `is_solution=True` |
| `hold_time_violations` | List[str] | **Solución** | Solo en `is_solution=True` |

---

## 🎨 Ejemplo: Implementación en Renderer

```python
# modules/numeracion/numeracion_renderer.py

class NumeracionLatexRenderer:
    def render(self, data: ConversionExerciseData, index: int) -> str:
        latex = ""
        
        # 1. ENUNCIADO (siempre visible)
        latex += fr"\textbf{{a)}} {data.description}\n"
        latex += f"Convierte a: {data.rows[0].target_system}\n"
        
        # 2. TABLA
        for row in data.rows:
            if self.is_solution:
                # ✅ SOLUCIÓN: Mostrar todo en rojo
                cells.append(fr"\textcolor{{red}}{{{row.sol_bin}}}")
                cells.append(fr"\textcolor{{red}}{{{row.sol_c2}}}")
                # ... todas las soluciones
            else:
                # ✅ ENUNCIADO: Solo columna activa
                cells.append(row.target_val_str)
                # Otras columnas quedan vacías
        
        # 3. OPERACIONES
        if data.operations:
            for op in data.operations:
                # Mostrar PROBLEMA siempre
                latex += f"{op.operand1} {op.operator_symbol} {op.operand2}\n"
                
                if self.is_solution:
                    # ✅ SOLUCIÓN: Mostrar resultado
                    latex += fr"\textbf{{Resultado:}} {op.result_bin}\n"
                    latex += fr"Carry: \textcolor{{blue}}{{{op.carry_bits}}}\n"
                else:
                    # ✅ ENUNCIADO: Dejar espacio para alumno
                    latex += r"\underline{\hspace{5cm}} (escribe el resultado)\n"
        
        return latex
```

---

## ✅ Checklist para Cada Renderer

- [ ] Importar data classes correctos
- [ ] En `is_solution=False`: mostrar SOLO campos de **Problema**
- [ ] En `is_solution=True`: mostrar **Problema** + **Solución** en rojo
- [ ] Documentar en docstring cuáles campos se muestran cuándo
- [ ] Probar que `is_solution=False` no contiene respuestas
- [ ] Probar que `is_solution=True` contiene todas las respuestas

---

## 🔗 Relaciones entre Campos

### Numeración

```
Problema:      val_decimal + target_col_idx → Alumno debe escribir aquí
Solución:      target_val_str + sol_* → Profesor valida respuesta
Validación:    representable confirma que el problema tiene solución
```

### Combinacional

```
Problema:      truth_table_outputs + canon_type + gate_type → Tabla para llenar
Solución:      minterms + simplified_sop + simplified_nand → Ecuaciones correctas
Validación:    La tabla genera los minterms correctos
```

### Secuencial

```
Problema:      clk_sequence + input_sequence → Alumno simula
Solución:      output_sequence + state_transitions → Resultado correcto
Validación:    state_transitions validar tiempos de setup/hold
```

---

## 🚨 Errores Comunes

### ❌ Error 1: Mostrar solución en enunciado

```python
# MALO:
cells.append(row.sol_bin)  # ¡Se ve siempre!

# BUENO:
if self.is_solution:
    cells.append(fr"\textcolor{{red}}{{{row.sol_bin}}}")
else:
    cells.append("")  # Vacío en enunciado
```

### ❌ Error 2: Olvidar que algunos campos son "duplex"

```python
# MALO:
# val1_dec se muestra en PROBLEMA (operandos) pero en SOLUCIÓN se colorea en rojo

# BUENO:
cells.append(f"{op.val1_dec}")  # Siempre visible
if self.is_solution:
    cells.append(fr"\textcolor{{red}}{{{op.result_bin}}}")
```

### ❌ Error 3: No validar representabilidad

```python
# MALO:
target_val_str = "10011010"  # ¿Está correcto? ¿Debería ser "NR"?

# BUENO:
if row.representable:
    assert row.target_val_str != "NR"
else:
    assert row.target_val_str == "NR"
```

---

## 📚 Buscar Fácilmente

En cualquier archivo `.py`:

```bash
grep "PARÁMETROS DEL PROBLEMA" modules/*/models.py
grep "PARÁMETROS DE LA SOLUCIÓN" modules/*/models.py
```

Esto te mostrará rápidamente qué es qué en cada modelo.
