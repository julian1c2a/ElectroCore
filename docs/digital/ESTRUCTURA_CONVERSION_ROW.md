# Estructura Mejorada: ConversionRow

## 📋 Descripción General

La clase `ConversionRow` representa una fila en un ejercicio de conversión de numeración. **Contiene todas las soluciones posibles**, pero el enunciado solo muestra la **columna activa** definida por `target_col_idx`.

## 🏗️ Campos de la Clase

```python
@dataclass
class ConversionRow:
    label: str                  # 'a)', 'b)', 'c)' - Identificador de fila
    val_decimal: int            # 154 - Valor decimal original
    
    # COLUMNA ACTIVA (lo que el alumno debe resolver)
    target_col_idx: int         # 0-3 - Índice qué sistema convertir
    target_val_str: str         # '10011010' o 'NR' - Respuesta esperada
    representable: bool         # True si se puede representar en el sistema
    
    # SOLUCIONES PRECALCULADAS (todas disponibles)
    sol_bin: str                # '10011010' - Binario Natural
    sol_c2: str                 # '01100110' - Complemento a 2
    sol_sm: str                 # '10011010' - Signo-Magnitud
    sol_bcd: str                # '0001 0101 0100' - BCD
```

## 📊 Mapeo de Índices

```python
COLUMN_NAMES = {
    0: "Binario Natural",
    1: "Complemento a 2",
    2: "Signo-Magnitud",
    3: "BCD"
}
```

| `target_col_idx` | Sistema | Ejemplo |
|---|---|---|
| **0** | Binario Natural | `10011010` |
| **1** | Complemento a 2 | `01100110` |
| **2** | Signo-Magnitud | `10011010` |
| **3** | BCD | `0001 0101 0100` |

## 🎯 Ejemplo Concreto

### Objeto en Memoria

```python
ConversionRow(
    label='a)',
    val_decimal=154,
    target_col_idx=0,           # ← El alumno convierte a BINARIO
    target_val_str='10011010',
    representable=True,         # ← Sí es representable
    
    # Soluciones precalculadas
    sol_bin='10011010',
    sol_c2='01100110',
    sol_sm='10011010',
    sol_bcd='0001 0101 0100'
)
```

### Enunciado (is_solution=False)

```
Conversión de Numeración (8 bits)
──────────────────────────────────
Convierte a: Binario Natural. Si no es representable, escribe 'NR'.

Respuesta:
┌────┬─────────┬──────────────┬────────────┬────────────┬──────────────┐
│ Id │ Decimal │ Bin. Nat.    │ Compl. 2   │ Signo-Mag. │ BCD          │
├────┼─────────┼──────────────┼────────────┼────────────┼──────────────┤
│a)  │ 154     │ 10011010     │            │            │              │
│    │         │ (respuesta)  │   (vacío)  │   (vacío)  │  (vacío)     │
└────┴─────────┴──────────────┴────────────┴────────────┴──────────────┘
```

**Solo se muestra la columna activa** (Binario Natural)

### Solución (is_solution=True)

```
┌────┬─────────┬──────────────┬────────────┬────────────┬──────────────┐
│ Id │ Decimal │ Bin. Nat.    │ Compl. 2   │ Signo-Mag. │ BCD          │
├────┼─────────┼──────────────┼────────────┼────────────┼──────────────┤
│a)  │ 154(r)  │ 10011010(r)  │ 01100110(r)│ 10011010(r)│ 0001 0101...(r)
│    │ (rojo)  │ (rojo)       │   (rojo)   │  (rojo)    │  (rojo)      │
└────┴─────────┴──────────────┴────────────┴────────────┴──────────────┘
```

**Se muestran todas las soluciones en rojo**

## ✅ Validación de Consistencia

El método `__post_init__` valida:

```python
def __post_init__(self):
    # target_col_idx debe estar entre 0-3
    if not 0 <= self.target_col_idx < 4:
        raise ValueError(f"target_col_idx inválido: {self.target_col_idx}")
    
    # Consistencia: representable ↔ target_val_str
    if self.representable and self.target_val_str == 'NR':
        raise ValueError("Inconsistencia: representable=True pero target_val_str='NR'")
    
    if not self.representable and self.target_val_str != 'NR':
        raise ValueError("Inconsistencia: representable=False pero target_val_str != 'NR'")
```

## 🚫 Ejemplo de No Representable

```python
ConversionRow(
    label='b)',
    val_decimal=300,            # 300 > 255, no cabe en 8 bits
    target_col_idx=0,
    target_val_str='NR',        # ← No representable
    representable=False,        # ← Explícitamente marcado
    sol_bin='NR',
    sol_c2='NR',
    sol_sm='NR',
    sol_bcd='NR'
)
```

**Enunciado:**

```
│b)  │ 300     │ NR           │            │            │              │
│    │         │ (no represent)
```

## 🔧 Uso en Generador

```python
# En NumeracionGenerator.generate()
representable = text_val != "NR"

rows.append(ConversionRow(
    label=label,
    val_decimal=val,
    target_col_idx=col_idx,
    target_val_str=text_val,
    representable=representable,  # ← Auto-determinado
    sol_bin=sol_bin,
    sol_c2=sol_c2,
    sol_sm=sol_sm,
    sol_bcd=sol_bcd
))
```

## 📚 Propiedad Auxiliar

```python
@property
def target_system(self) -> str:
    """Devuelve el nombre del sistema target."""
    return COLUMN_NAMES.get(self.target_col_idx, "Desconocido")

# Uso:
row.target_system  # → "Binario Natural"
```

## 🎓 Beneficios de Esta Estructura

| Aspecto | Beneficio |
|---------|-----------|
| **Problema bien definido** | Solo una columna activa por fila |
| **Validación automática** | No hay inconsistencias posibles |
| **Flexibilidad pedagógica** | Cada alumno ve diferentes ejercicios |
| **Soluciones completas** | Disponibles para docentes |
| **Claridad de intención** | Campo `representable` es explícito |

## 🔄 Flujo Completo

```
1. Generator.generate()
   ├─ Elige val_decimal aleatoriamente
   ├─ Elige target_col_idx aleatoriamente
   ├─ Calcula target_val_str (o 'NR')
   ├─ Calcula todas las soluciones (sol_bin, sol_c2, etc.)
   └─ Crea ConversionRow con representable=True/False

2. Renderer.render(is_solution=False)
   ├─ Itera sobre rows
   ├─ SOLO muestra target_col_idx
   └─ Genera PDF de ENUNCIADO (columna activa vacía)

3. Renderer.render(is_solution=True)
   ├─ Itera sobre rows
   ├─ Muestra TODAS las columnas
   └─ Genera PDF de SOLUCIÓN (todo en rojo)

4. Alumno
   ├─ Recibe: enunciado con una columna
   └─ Debe escribir: el valor en esa columna

5. Profesor
   ├─ Recibe: soluciones con todas las columnas
   └─ Puede evaluar: si la respuesta del alumno es correcta
```

## 📝 Notas Importantes

- **`target_col_idx`** define qué columna el alumno debe completar
- **`target_val_str`** es la respuesta esperada o 'NR'
- **`representable`** valida que la respuesta sea posible en ese sistema
- **Todas las soluciones se precalculan** al generar el ejercicio
- **El enunciado solo muestra una columna** (la activa)
- **La solución muestra todas las columnas** para el docente
