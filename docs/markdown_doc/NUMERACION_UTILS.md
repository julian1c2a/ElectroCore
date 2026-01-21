# Utilidades de Conversión Numérica

## 📚 Descripción

Módulo `core/numeracion_utils.py` que implementa conversiones de números decimales a otras bases usando el **método de divisiones sucesivas** de forma explícita y educativa.

## 🎯 Funciones Principales

### 1. `decimal_a_binario_divisiones(numero, bits=None)`

Conversión simple de decimal a binario con notación clara.

**Parámetros:**

- `numero` (int o str): Número decimal a convertir
- `bits` (int, opcional): Ancho mínimo para padding

**Retorna:** String con formato `xxxxx₂`

**Ejemplos:**

```python
from core.numeracion_utils import decimal_a_binario_divisiones

# Conversión básica
print(decimal_a_binario_divisiones("13"))      # → 1101₂
print(decimal_a_binario_divisiones(42))        # → 101010₂

# Con padding
print(decimal_a_binario_divisiones(13, bits=8))   # → 00001101₂
print(decimal_a_binario_divisiones(255, bits=8))  # → 11111111₂
```

---

### 2. `decimal_a_binario_con_pasos(numero)`

Retorna un diccionario con todos los pasos intermedios (ideal para educación).

**Retorna:** Dict con:

- `'numero'`: Número original
- `'pasos'`: Lista de tuplas (dividendo, cociente, resto)
- `'restos'`: Lista de restos en orden
- `'binario'`: Resultado final
- `'explicacion'`: Texto con los pasos

**Ejemplo:**

```python
from core.numeracion_utils import decimal_a_binario_con_pasos

resultado = decimal_a_binario_con_pasos("13")

# Acceso a datos
print(f"Número: {resultado['numero']}")
print(f"Pasos: {resultado['pasos']}")
# [(13, 6, 1), (6, 3, 0), (3, 1, 1), (1, 0, 1)]

print(f"Binario: {resultado['binario']}")  # 1101₂

# Ver explicación
print(resultado['explicacion'])
# 13 ÷ 2 = 6 resto 1
# 6 ÷ 2 = 3 resto 0
# 3 ÷ 2 = 1 resto 1
# 1 ÷ 2 = 0 resto 1
#
# Leyendo los restos de abajo hacia arriba: 1101₂
```

---

### 3. `decimal_a_binario_verbose(numero)`

Retorna un string con explicación paso a paso en formato visual.

**Retorna:** String con desarrollo completo

**Ejemplo:**

```python
from core.numeracion_utils import decimal_a_binario_verbose

print(decimal_a_binario_verbose("42"))

# Salida:
# Convertir 42 a binario (sucesivas divisiones por 2):
# 
#  42 ÷ 2 = 21 resto 0
#  21 ÷ 2 = 10 resto 1
#  10 ÷ 2 = 5 resto 0
#  5 ÷ 2 = 2 resto 1
#  2 ÷ 2 = 1 resto 0
#  1 ÷ 2 = 0 resto 1
# 
# Resultado: 101010₂
# 
# (Leer los restos de abajo hacia arriba)
```

---

### 4. `validar_numero_decimal(numero)`

Valida si un input es un número decimal válido.

**Parámetros:**

- `numero`: Input a validar (int, str, float)

**Retorna:** Tupla (es_valido: bool, mensaje: str)

**Ejemplo:**

```python
from core.numeracion_utils import validar_numero_decimal

es_ok, msg = validar_numero_decimal("42")
# (True, "42 es un número decimal válido")

es_ok, msg = validar_numero_decimal("-5")
# (False, "El número debe ser no-negativo")

es_ok, msg = validar_numero_decimal("abc")
# (False, "'abc' no es un número decimal válido")
```

---

### 5. `decimal_a_octal_divisiones(numero, bits=None)`

Conversión de decimal a octal (base 8) usando divisiones sucesivas.

**Ejemplo:**

```python
from core.numeracion_utils import decimal_a_octal_divisiones

print(decimal_a_octal_divisiones(42))    # → 52₈
print(decimal_a_octal_divisiones(255))   # → 377₈
```

---

### 6. `decimal_a_hexadecimal_divisiones(numero, bits=None)`

Conversión de decimal a hexadecimal (base 16).

**Ejemplo:**

```python
from core.numeracion_utils import decimal_a_hexadecimal_divisiones

print(decimal_a_hexadecimal_divisiones(42))    # → 2A₁₆
print(decimal_a_hexadecimal_divisiones(255))   # → FF₁₆
print(decimal_a_hexadecimal_divisiones(1000))  # → 3E8₁₆
```

---

## 📊 Método de Divisiones Sucesivas

El algoritmo funciona así:

```
Convertir 13 a binario:

13 ÷ 2 = 6  resto 1  ← último dígito
 6 ÷ 2 = 3  resto 0
 3 ÷ 2 = 1  resto 1
 1 ÷ 2 = 0  resto 1  ← primer dígito

Resultado: 1101₂ (leer de abajo hacia arriba)

Verificación: 1·2³ + 1·2² + 0·2¹ + 1·2⁰ = 8 + 4 + 0 + 1 = 13 ✓
```

---

## 🎓 Archivos de Demostración

### `demo_conversiones.py`

Ejecuta múltiples demostraciones:

```bash
python demo_conversiones.py
```

Muestra:

- Conversiones básicas
- Tabla de divisiones
- Formato verboso
- Validación
- Conversiones a múltiples bases
- Tabla de referencia 0-15

### `ejercicio_conversion.py`

Ejercicio educativo completo:

```bash
python ejercicio_conversion.py
```

Incluye:

- Enunciado del problema
- Explicación del método
- Desarrollo paso a paso
- Verificación inversa
- Práctica múltiple
- Tabla de referencia 0-31

---

## 💡 Casos de Uso

### En Generadores

```python
from core.numeracion_utils import decimal_a_binario_divisiones

class ConversionExerciseGenerator(ExerciseGenerator):
    def generate_from_problem(self, params):
        numero = params.get('numero', 42)
        # Genera ejercicio con binario claro
        binario = decimal_a_binario_divisiones(numero, bits=8)
        return {
            'problema': f'Convierte {numero} a binario',
            'respuesta': binario
        }
```

### En Ejercicios Educativos

```python
from core.numeracion_utils import decimal_a_binario_verbose

# Mostrar explicación completa al estudiante
print(decimal_a_binario_verbose(número))
```

### En Validación

```python
from core.numeracion_utils import validar_numero_decimal

entrada = input("Ingresa un número decimal: ")
es_valido, mensaje = validar_numero_decimal(entrada)

if es_valido:
    # Procesar número
else:
    print(f"Error: {mensaje}")
```

---

## 📈 Tabla de Conversión Rápida (0-15)

| Decimal | Binario | Octal | Hexadecimal |
|---------|---------|-------|-------------|
| 0 | 0000₂ | 0₈ | 0₁₆ |
| 1 | 0001₂ | 1₈ | 1₁₆ |
| 2 | 0010₂ | 2₈ | 2₁₆ |
| 3 | 0011₂ | 3₈ | 3₁₆ |
| 4 | 0100₂ | 4₈ | 4₁₆ |
| 5 | 0101₂ | 5₈ | 5₁₆ |
| 6 | 0110₂ | 6₈ | 6₁₆ |
| 7 | 0111₂ | 7₈ | 7₁₆ |
| 8 | 1000₂ | 10₈ | 8₁₆ |
| 9 | 1001₂ | 11₈ | 9₁₆ |
| 10 | 1010₂ | 12₈ | A₁₆ |
| 11 | 1011₂ | 13₈ | B₁₆ |
| 12 | 1100₂ | 14₈ | C₁₆ |
| 13 | 1101₂ | 15₈ | D₁₆ |
| 14 | 1110₂ | 16₈ | E₁₆ |
| 15 | 1111₂ | 17₈ | F₁₆ |

---

## 🎯 Notación

Las funciones retornan con notación clara que indica la base:

- **Binario**: `1101₂` (subíndice 2)
- **Octal**: `52₈` (subíndice 8)
- **Hexadecimal**: `FF₁₆` (subíndice 16)

---

## ⚠️ Limitaciones

- Solo acepta números **no-negativos**
- Para números decimales (con punto), convierte a int
- El padding con `bits` no expande si el número requiere más bits

---

## 🔧 Integración

Para usar en tus generadores:

```python
from core.numeracion_utils import decimal_a_binario_divisiones

# En tu generador
class TuGenerador(ExerciseGenerator):
    def generate_from_problem(self, params):
        numero = params.get('numero')
        binario = decimal_a_binario_divisiones(numero, bits=8)
        # Usar binario en el ejercicio
```

---

**Última actualización**: 2026-01-15
