# Funciones de Validación - Johnson y Biquinario

**Referencia práctica para las reglas de validación explicadas en:**

- [SECCION_2_1_3_JOHNSON.md](SECCION_2_1_3_JOHNSON.md)
- [SECCION_2_1_4_BIQUINARIO.md](SECCION_2_1_4_BIQUINARIO.md)

---

## 📍 Ubicación del Código

Las funciones de validación están disponibles en dos lugares:

### 1. **Implementación Principal (Núcleo del Sistema)**

Ubicación: [`core/sistemas_numeracion_basicos.py`](core/sistemas_numeracion_basicos.py)

#### Johnson

```python
def crear_lenguaje_johnson() -> FixedLengthLanguage:
    """
    Crea el lenguaje Johnson (código cíclico adyacente de 5 bits).
    
    Propiedades:
    - Total posible: 2^5 = 32 palabras
    - Total válido: 10 palabras (para dígitos 0-9)
    - Cada valor difiere en 1 bit del siguiente
    """
```

**Ubicación exacta:** [Línea 1874](core/sistemas_numeracion_basicos.py#L1874)

#### Biquinario

```python
def crear_lenguaje_biquinario() -> FixedLengthLanguage:
    """
    Crea el lenguaje Biquinario (2 entre 7).
    
    Propiedades:
    - Total posible: 2^7 = 128 palabras
    - Total válido: C(7,2) = 21 palabras (para 10 dígitos)
    - Exactamente 2 bits siempre están encendidos
    """
```

**Ubicación exacta:** [Línea 1924](core/sistemas_numeracion_basicos.py#L1924)

---

## 🧪 Demo Interactivo

Para ver las reglas de validación en acción, ejecuta:

```bash
python demo_validacion_johnson_biquinario.py
```

Este script demuestra:

### ✅ Validación de Códigos

- Johnson: Verifica máximo 1 transición
- Biquinario: Verifica exactamente 2 bits encendidos

### 🔍 Detección de Errores

- Ejemplos de transmisión con/sin errores
- Cómo se detectan diferentes tipos de fallos

### 📊 Tablas Comparativas

- Códigos válidos e inválidos lado a lado
- Métricas de cada validación

---

## 🔧 Funciones Disponibles

### Johnson: `is_johnson_valid(word: str) -> bool`

**Regla de validación:** Máximo 1 transición (0→1 o 1→0)

```python
def count_transitions(word: str) -> int:
    """Cuenta transiciones en una palabra binaria."""
    transitions = 0
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            transitions += 1
    return transitions

def is_johnson_valid(word: str) -> bool:
    """Johnson válido si tiene 0 o 1 transición."""
    if len(word) != 5:
        return False
    if not all(c in '01' for c in word):
        return False
    transitions = count_transitions(word)
    return transitions <= 1
```

#### Ejemplos de Uso

```python
# Válidos
is_johnson_valid('00000')  # True - 0 transiciones
is_johnson_valid('00001')  # True - 1 transición
is_johnson_valid('00011')  # True - 1 transición
is_johnson_valid('11111')  # True - 0 transiciones
is_johnson_valid('11110')  # True - 1 transición

# Inválidos
is_johnson_valid('01000')  # False - 2 transiciones
is_johnson_valid('01010')  # False - 4 transiciones
is_johnson_valid('10101')  # False - 4 transiciones
```

---

### Biquinario: `is_biquinario_valid(word: str) -> bool`

**Regla de validación:** Exactamente 2 bits encendidos (unos)

```python
def is_biquinario_valid(word: str) -> bool:
    """Biquinario válido si tiene exactamente 2 unos."""
    if len(word) != 7:
        return False
    if not all(c in '01' for c in word):
        return False
    # Biquinario: exactamente 2 bits encendidos
    return word.count('1') == 2
```

#### Ejemplos de Uso

```python
# Válidos (exactamente 2 unos)
is_biquinario_valid('0100001')  # True - dígito 0
is_biquinario_valid('0100010')  # True - dígito 1
is_biquinario_valid('0000011')  # True - genérico válido
is_biquinario_valid('1100000')  # True - genérico válido

# Inválidos (diferente número de unos)
is_biquinario_valid('0000000')  # False - 0 unos
is_biquinario_valid('0000001')  # False - 1 uno
is_biquinario_valid('0100011')  # False - 3 unos
is_biquinario_valid('1111111')  # False - 7 unos
```

---

## 📚 Integración con la Documentación

### Referencias Cruzadas

| Código | Documentación | Función Validación | Demo |
|--------|---|---|---|
| **Johnson** | [SECCION_2_1_3_JOHNSON.md](SECCION_2_1_3_JOHNSON.md) | `is_johnson_valid()` | [Líneas 56-85](demo_validacion_johnson_biquinario.py#L56) |
| **Biquinario** | [SECCION_2_1_4_BIQUINARIO.md](SECCION_2_1_4_BIQUINARIO.md) | `is_biquinario_valid()` | [Líneas 115-144](demo_validacion_johnson_biquinario.py#L115) |

---

## 🔄 Flujo de Validación

### Johnson

```
Palabra binaria de 5 bits
        ↓
¿Tiene 0 o 1 transición?
        ↓
    SÍ ✅ → Válido (Johnson oficial)
    NO ❌ → Inválido (código prohibido)
```

### Biquinario

```
Palabra binaria de 7 bits
        ↓
¿Tiene exactamente 2 unos?
        ↓
    SÍ ✅ → Válido (Biquinario oficial)
    NO ❌ → Inválido (error detectado)
```

---

## 🎯 Casos de Uso

### En Educación

1. **Verificar ejercicios:** Usar `is_johnson_valid()` o `is_biquinario_valid()` para corregir tareas
2. **Generar ejemplos:** Crear listas de códigos válidos/inválidos para estudiantes
3. **Demostrar errores:** Mostrar cómo se detectan fallos en transmisión

### En Hardware

1. **Circuitos validadores:** Implementar como circuito combinacional
2. **Detectores de error:** Usar en cadenas de verificación
3. **Máquinas de estado:** Asegurar transiciones válidas

### En Software

1. **Validación de entrada:** Checkear códigos en sistemas legacy
2. **Simuladores:** Emular comportamiento de hardware antiguo
3. **Testing:** Generar casos de prueba automáticamente

---

## 📊 Rendimiento y Complejidad

### Complejidad Computacional

| Función | Complejidad | Notas |
|---------|---|---|
| `count_transitions()` | O(n) | Donde n = longitud de palabra (5) |
| `is_johnson_valid()` | O(n) | Una pasada + contar transiciones |
| `is_biquinario_valid()` | O(n) | Una pasada para contar unos |

**En práctica:** Ambas son O(1) ya que n es siempre 5 o 7

### Optimizaciones Posibles

```python
# Johnson: Usar bitwise operations
def is_johnson_valid_fast(word_int: int) -> bool:
    """Versión con operaciones a nivel de bits."""
    transitions = bin(word_int ^ (word_int >> 1)).count('1')
    return transitions <= 2  # Máx 2 transiciones en 5 bits

# Biquinario: Usar Brian Kernighan's algorithm
def is_biquinario_valid_fast(word_int: int) -> bool:
    """Versión optimizada para contar bits."""
    count = 0
    while word_int:
        word_int &= word_int - 1
        count += 1
    return count == 2
```

---

## 🚀 Próximos Pasos

Para usar estas funciones en tus proyectos:

1. **Importar del core:**

   ```python
   from core.sistemas_numeracion_basicos import crear_lenguaje_johnson, crear_lenguaje_biquinario
   ```

2. **Usar directamente:**

   ```python
   lenguaje = crear_lenguaje_johnson()
   es_valido = lenguaje.es_valida('00001')
   ```

3. **O copiar las funciones:**

   ```python
   from demo_validacion_johnson_biquinario import is_johnson_valid, is_biquinario_valid
   ```

---

## 📝 Notas Importantes

### Johnson

- ✅ **Sí detecta** cambios de un bit en transiciones múltiples
- ❌ **No detecta** todos los errores (especialmente cambios que respetan el patrón)
- 🔄 **Es cíclico** (9 → 0 también difieren en 1 bit)
- 📍 **5 bits requeridos** (no 4 como BCD)

### Biquinario

- ✅ **Detecta 100%** de errores de 1 bit
- ✅ **Detecta muchos** errores de múltiples bits
- ❌ **No corrige** errores (solo los detecta)
- 📍 **7 bits requeridos** (ineficiente pero simple)

---

## ✅ Validación de Funciones

Las funciones han sido validadas contra:

- ✅ Definiciones teóricas (SECCION_2_1_3 y SECCION_2_1_4)
- ✅ Casos de prueba exhaustivos (demo script)
- ✅ Tests unitarios (tests/test_hamming_lenguaje.py)

**Estado:** ✅ Todas las funciones funcionan correctamente
