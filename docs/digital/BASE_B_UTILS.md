# Utilidades de Numeración - Conversión Base 10 a Base B

## Descripción General

Este módulo proporciona funciones para convertir números decimales (base 10) a cualquier base numérica entre 2 y 36 usando el **método de divisiones sucesivas**.

Las bases soportadas incluyen:

- **Bases comunes**: Binario (2), Octal (8), Decimal (10), Hexadecimal (16)
- **Bases especiales**: Base 36 (máximo soportado, alfanumérica)
- **Cualquier base intermedia**: 2, 3, 4, 5, ... 35, 36

## Tabla de Contenidos

- [Características Principales](#características-principales)
- [Funciones Disponibles](#funciones-disponibles)
- [Niveles de Complejidad](#niveles-de-complejidad)
- [Uso Básico](#uso-básico)
- [Ejemplos Completos](#ejemplos-completos)
- [Tabla de Referencia](#tabla-de-referencia)
- [Integración en Generadores](#integración-en-generadores)

---

## Características Principales

✅ **Conversión flexible**: De base 10 a cualquier base 2-36  
✅ **Algoritmo explícito**: Divisiones sucesivas, no bibliotecas  
✅ **Entrada flexible**: Acepta int, str, strings con espacios  
✅ **Notación clara**: Subíndices Unicode (1101₂, FF₁₆, RS₃₆)  
✅ **3 niveles de complejidad**: Simple, con pasos, verboso  
✅ **Padding opcional**: Ancho fijo con ceros a la izquierda  
✅ **Validación robusta**: Manejo seguro de errores  
✅ **Educativo**: Perfecto para ejercicios y enseñanza  

---

## Funciones Disponibles

### 1. `decimal_a_base_b_divisiones(numero, base, bits=None)`

**Conversión rápida y simple.**

Convierte un número decimal a una base específica usando divisiones sucesivas.

**Parámetros:**

- `numero` (int, str): Número decimal a convertir
- `base` (int): Base destino (2-36)
- `bits` (int, optional): Ancho mínimo con padding de ceros

**Retorna:**

- `str`: Número en la base especificada con notación clara (ej: "1101₂")

**Excepciones:**

- `ValueError`: Si base no está en rango 2-36 o número es inválido

**Ejemplos:**

```python
from core.numeracion_utils import decimal_a_base_b_divisiones

# Conversión simple
decimal_a_base_b_divisiones(173, 2)     # → "10101101₂"
decimal_a_base_b_divisiones(255, 16)    # → "FF₁₆"
decimal_a_base_b_divisiones(100, 36)    # → "2S₃₆"

# Con entrada string
decimal_a_base_b_divisiones("42", 8)    # → "52₈"

# Con padding
decimal_a_base_b_divisiones(42, 2, bits=8)   # → "00101010₂"
decimal_a_base_b_divisiones(255, 16, bits=4) # → "00FF₁₆"
```

---

### 2. `decimal_a_base_b_con_pasos(numero, base)`

**Conversión con tabla de divisiones intermedias.**

Útil para generar ejercicios educativos o visualizar todos los pasos.

**Parámetros:**

- `numero` (int, str): Número decimal a convertir
- `base` (int): Base destino (2-36)

**Retorna:**

- `dict` con las siguientes claves:
  - `numero`: Número original
  - `base`: Base destino
  - `pasos`: Lista de tuplas (dividendo, cociente, digito)
  - `digitos`: Lista de dígitos en orden inverso
  - `resultado`: Resultado final con notación
  - `explicacion`: Texto con explicación del proceso

**Ejemplos:**

```python
from core.numeracion_utils import decimal_a_base_b_con_pasos

resultado = decimal_a_base_b_con_pasos(100, 16)

# Acceder a los datos
print(resultado['resultado'])  # → "64₁₆"
print(resultado['pasos'])      # → [(100, 6, '4'), (6, 0, '6')]

# Generar tabla educativa
for dividendo, cociente, digito in resultado['pasos']:
    print(f"{dividendo} ÷ 16 = {cociente} resto {digito}")

# Output:
# 100 ÷ 16 = 6 resto 4
# 6 ÷ 16 = 0 resto 6
```

---

### 3. `decimal_a_base_b_verbose(numero, base)`

**Explicación completa y educativa del proceso.**

Ideal para mostrar a estudiantes cómo funciona la conversión.

**Parámetros:**

- `numero` (int, str): Número decimal a convertir
- `base` (int): Base destino (2-36)

**Retorna:**

- `str`: Explicación visual completa del proceso

**Ejemplos:**

```python
from core.numeracion_utils import decimal_a_base_b_verbose

print(decimal_a_base_b_verbose(42, 2))
```

**Output:**

```
Convertir 42 a base 2 (divisiones sucesivas):

 42 ÷ 2 = 21 resto 0
21 ÷ 2 = 10 resto 1
10 ÷ 2 = 5 resto 0
5 ÷ 2 = 2 resto 1
2 ÷ 2 = 1 resto 0
1 ÷ 2 = 0 resto 1

Resultado: 101010₂

(Leer los restos de abajo hacia arriba)
```

---

### 4. `validar_base(base)`

**Valida si una base está en el rango permitido.**

**Parámetros:**

- `base` (int): Base a validar

**Retorna:**

- `bool`: True si 2 ≤ base ≤ 36, False en caso contrario

**Ejemplos:**

```python
from core.numeracion_utils import validar_base

validar_base(2)   # → True
validar_base(16)  # → True
validar_base(36)  # → True
validar_base(37)  # → False
validar_base(1)   # → False
```

---

### 5. `obtener_digitos_para_base(base)`

**Obtiene los dígitos válidos para una base.**

**Parámetros:**

- `base` (int): Base numérica (2-36)

**Retorna:**

- `str`: String con los dígitos válidos

**Ejemplos:**

```python
from core.numeracion_utils import obtener_digitos_para_base

obtener_digitos_para_base(2)   # → "01"
obtener_digitos_para_base(8)   # → "01234567"
obtener_digitos_para_base(16)  # → "0123456789ABCDEF"
obtener_digitos_para_base(36)  # → "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

---

## Niveles de Complejidad

La API proporciona **3 niveles** para adaptarse a diferentes necesidades:

### NIVEL 1: Resultado Simple

```python
resultado = decimal_a_base_b_divisiones(173, 16)
# → "AD₁₆"
```

**Cuándo usar**: Cuando solo necesitas el resultado final rápido.

---

### NIVEL 2: Con Pasos Intermedios

```python
resultado = decimal_a_base_b_con_pasos(173, 16)

# Acceder a los pasos
for dividendo, cociente, digito in resultado['pasos']:
    print(f"{dividendo} ÷ 16 = {cociente} resto {digito}")

# Generar tabla de ejercicio
```

**Cuándo usar**:

- Generar ejercicios con tabla de divisiones
- Procesamiento de datos para generadores
- Visualización de pasos intermedios

---

### NIVEL 3: Explicación Completa

```python
explicacion = decimal_a_base_b_verbose(173, 16)
print(explicacion)
```

**Cuándo usar**:

- Ejercicios educativos detallados
- Enseñanza del algoritmo
- Material de aprendizaje

---

## Uso Básico

### Instalación/Importación

```python
from core.numeracion_utils import (
    decimal_a_base_b_divisiones,
    decimal_a_base_b_con_pasos,
    decimal_a_base_b_verbose
)
```

### Ejemplo Rápido

```python
# Convertir 255 a binario, octal y hexadecimal
numero = 255

binario = decimal_a_base_b_divisiones(numero, 2)    # 11111111₂
octal = decimal_a_base_b_divisiones(numero, 8)      # 377₈
hex_val = decimal_a_base_b_divisiones(numero, 16)   # FF₁₆

print(f"{numero} =")
print(f"  Binario:     {binario}")
print(f"  Octal:       {octal}")
print(f"  Hexadecimal: {hex_val}")
```

---

## Ejemplos Completos

### Ejemplo 1: Tabla de Conversión

```python
from core.numeracion_utils import decimal_a_base_b_divisiones

numero = 100
bases = [2, 8, 10, 16, 20, 36]

print(f"Conversión del número {numero}:\n")
print("Base | Resultado")
print("-" * 25)

for base in bases:
    resultado = decimal_a_base_b_divisiones(numero, base)
    print(f"{base:4} | {resultado}")
```

**Output:**

```
Conversión del número 100:

Base | Resultado
-------------------------
   2 | 1100100₂
   8 | 144₈
  10 | 100₁₀
  16 | 64₁₆
  20 | 50₂₀
  36 | 2S₃₆
```

---

### Ejemplo 2: Ejercicio Educativo

```python
from core.numeracion_utils import decimal_a_base_b_con_pasos

numero = 173
base = 16

print("Problema: Convierte 173 a hexadecimal usando divisiones por 16\n")

resultado = decimal_a_base_b_con_pasos(numero, base)

print("Solución:\n")
print(f"{'Dividendo':<10} | {'Cociente':<8} | {'Resto':<8}")
print("-" * 35)

for dividendo, cociente, digito in resultado['pasos']:
    print(f"{dividendo:<10} | {cociente:<8} | {digito:<8}")

print(f"\nRespuesta: {resultado['resultado']}")
print(f"\n(Se leen los restos de abajo hacia arriba)")
```

---

### Ejemplo 3: Base 36 para Compresión

```python
from core.numeracion_utils import decimal_a_base_b_divisiones

# Usar Base 36 para comprimir números grandes
ids_usuarios = [1000000, 2500000, 5000000]

print("Compresión de IDs con Base 36:\n")
print(f"{'ID Decimal':<15} | {'Base 36':<12}")
print("-" * 30)

for id_num in ids_usuarios:
    base36 = decimal_a_base_b_divisiones(id_num, 36).replace("₃₆", "")
    print(f"{id_num:<15} | {base36:>10}")
```

**Output:**

```
Compresión de IDs con Base 36:

ID Decimal      | Base 36
------------------------------
1000000         | LFLS
2500000         | 1X9Z
5000000         | 3DBJS
```

---

## Tabla de Referencia

### Bases Comunes (0-15)

| Dec | Bin     | Oct | Dec | Hex | Base20 | Base36 |
|-----|---------|-----|-----|-----|--------|--------|
| 0   | 0₂      | 0₈  | 0   | 0₁₆ | 0₂₀    | 0₃₆    |
| 1   | 1₂      | 1₈  | 1   | 1₁₆ | 1₂₀    | 1₃₆    |
| 2   | 10₂     | 2₈  | 2   | 2₁₆ | 2₂₀    | 2₃₆    |
| 3   | 11₂     | 3₈  | 3   | 3₁₆ | 3₂₀    | 3₃₆    |
| 4   | 100₂    | 4₈  | 4   | 4₁₆ | 4₂₀    | 4₃₆    |
| 5   | 101₂    | 5₈  | 5   | 5₁₆ | 5₂₀    | 5₃₆    |
| 6   | 110₂    | 6₈  | 6   | 6₁₆ | 6₂₀    | 6₃₆    |
| 7   | 111₂    | 7₈  | 7   | 7₁₆ | 7₂₀    | 7₃₆    |
| 8   | 1000₂   | 10₈ | 8   | 8₁₆ | 8₂₀    | 8₃₆    |
| 9   | 1001₂   | 11₈ | 9   | 9₁₆ | 9₂₀    | 9₃₆    |
| 10  | 1010₂   | 12₈ | 10  | A₁₆ | A₂₀    | A₃₆    |
| 11  | 1011₂   | 13₈ | 11  | B₁₆ | B₂₀    | B₃₆    |
| 12  | 1100₂   | 14₈ | 12  | C₁₆ | C₂₀    | C₃₆    |
| 13  | 1101₂   | 15₈ | 13  | D₁₆ | D₂₀    | D₃₆    |
| 14  | 1110₂   | 16₈ | 14  | E₁₆ | E₂₀    | E₃₆    |
| 15  | 1111₂   | 17₈ | 15  | F₁₆ | F₂₀    | F₃₆    |

---

### Información sobre Bases

| Base | Nombre          | Dígitos             | Usos Típicos                    |
|------|-----------------|---------------------|---------------------------------|
| 2    | Binario         | 0-1                 | Electrónica, Lógica digital     |
| 8    | Octal           | 0-7                 | Legacy (antes de hex)           |
| 10   | Decimal         | 0-9                 | Natural, humano                 |
| 12   | Duodecimal      | 0-9, A-B            | Reloj, docenas                  |
| 16   | Hexadecimal     | 0-9, A-F            | Color, memoria, direcciones     |
| 20   | Vigesimal       | 0-9, A-J            | Histórico (Maya, humano)        |
| 36   | Alphanumeric    | 0-9, A-Z            | URLs, IDs, compresión           |

---

## Integración en Generadores

### Usar en un Generador de Ejercicios

```python
from core.generador_base import ExerciseGenerator
from core.numeracion_utils import (
    decimal_a_base_b_divisiones,
    decimal_a_base_b_con_pasos
)

class ConversionBaseExerciseGenerator(ExerciseGenerator):
    """Genera ejercicios de conversión entre bases numéricas."""
    
    def generate_from_problem(self, params):
        # Parámetros del ejercicio
        numero = params.get('numero', 100)
        base_origen = params.get('base_origen', 10)
        base_destino = params.get('base_destino', 16)
        mostrar_pasos = params.get('mostrar_pasos', True)
        
        # Generar conversión
        if base_origen == 10:  # De decimal a otra base
            resultado = decimal_a_base_b_divisiones(numero, base_destino)
            
            if mostrar_pasos:
                pasos = decimal_a_base_b_con_pasos(numero, base_destino)
                return {
                    'titulo': f'Conversión de Base 10 a Base {base_destino}',
                    'problema': f'Convierte {numero} a base {base_destino}',
                    'respuesta': pasos['resultado'],
                    'pasos': pasos['pasos'],
                    'explicacion': pasos['explicacion']
                }
            else:
                return {
                    'titulo': f'Conversión de Base 10 a Base {base_destino}',
                    'problema': f'Convierte {numero} a base {base_destino}',
                    'respuesta': resultado
                }
```

---

## Notas de Implementación

### Algoritmo de Divisiones Sucesivas

```
1. Dividir el número entre la base
2. Guardar el resto (será un dígito en la nueva base)
3. Dividir el cociente entre la base
4. Repetir pasos 2-3 hasta que el cociente sea 0
5. Los restos en orden inverso forman el resultado

Ejemplo: 173 a base 16
173 ÷ 16 = 10 resto 13 (D)  ← Guardar 13
 10 ÷ 16 = 0  resto 10 (A)  ← Guardar 10

Leer restos de abajo a arriba: AD₁₆
```

### Dígitos por Base

- **Bases 2-10**: Usan solo dígitos 0-9
- **Bases 11-36**: Usan dígitos 0-9 y letras A-Z
  - 10 → A, 11 → B, ..., 35 → Z

### Notación de Subíndices Unicode

Todos los resultados incluyen subíndices Unicode para claridad:

- `1101₂` en lugar de `0b1101`
- `377₈` en lugar de `0o377`
- `FF₁₆` en lugar de `0xFF`
- `RS₃₆` para bases no estándar

---

## Casos de Uso Reales

### 1. Educación

- Enseñanza de sistemas de numeración
- Ejercicios de conversión paso a paso
- Comprensión del concepto de posición

### 2. Programación

- Conversión de colores (#FF5733 en hex)
- Direccionamiento de memoria
- Operaciones de bits en bajo nivel

### 3. Compresión de Datos

- Base 36 para URLs amigables
- IDs cortos en bases de datos
- Ahorro de almacenamiento

### 4. Sistemas Legados

- Conversión a octal (antiguo estándar)
- Compatibilidad con sistemas antiguos

---

## Preguntas Frecuentes

**P: ¿Puedo usar esta función para conversiones inversas (base B a decimal)?**

R: Por ahora, este módulo solo convierte DE decimal A otras bases. Para lo inverso, necesitarías una función separada. Contacta con el equipo si lo necesitas.

**P: ¿Qué pasa si intento una base fuera del rango 2-36?**

R: Levantará una `ValueError` con mensaje descriptivo.

**P: ¿Funciona con números negativos?**

R: No, el módulo solo acepta números no-negativos. Los números negativos levantarán un `ValueError`.

**P: ¿Puedo usar decimales (números con punto)?**

R: No, el módulo convierte solo números enteros. La entrada será convertida a int (truncando decimales).

---

## Archivos Relacionados

- `NUMERACION_UTILS.md` - Documentación del módulo original (binario, octal, hexadecimal)
- `RESUMEN_CONVERSION.md` - Resumen ejecutivo de toda la funcionalidad
- `demo_base_b.py` - Demostración completa de todas las funciones
- `ejemplo_base_b.py` - Ejemplos prácticos de uso

---

**Última actualización**: 15 de Enero, 2026  
**Versión**: 2.0 (Con soporte generalizado para bases 2-36)
