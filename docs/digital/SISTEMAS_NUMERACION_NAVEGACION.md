# Navegación: Sección 2.1.1 - Sistemas de Numeración

---

## 📍 Vista General

Esta sección cubre los **Sistemas de Numeración Posicionales y No Posicionales**, respondiendo a la pregunta: "¿Se te ocurre un sistema posicional que NO sea en potencias de una base?"

**Respuesta**: El sistema temporal babilónico (HH:MM:SS) - posicional con bases variables.

---

## 📚 Estructura Educativa

### Sección 2.1.1.1 - Sistemas Posicionales y No Posicionales

**Contenido**:

- Definiciones de sistemas posicionales vs no posicionales
- 3 ejemplos concretos:
  1. **Números Romanos** (no posicional)
  2. **Base 5** (posicional con potencias)
  3. **Sistema Temporal** (posicional con bases variables)

**Ubicación**: [CONTENIDOS_FE.md](CONTENIDOS_FE.md#2111-sistemas-posicionales-y-no-posicionales)

**Conceptos clave**:

- Valor de símbolo vs valor posicional
- Pesos en potencias vs pesos mixtos
- Origen histórico babilónico

---

### Sección 2.1.1.2 - Unicidad de la Representación

**Contenido**:

- Teorema: cada número natural tiene representación ÚNICA en una base dada
- Prueba mediante divisiones sucesivas
- Tabla de verificación con 4 números en múltiples bases
- Ejemplo: 1994 = MCMXCIV = 30434₅

**Ubicación**: [CONTENIDOS_FE.md](CONTENIDOS_FE.md#2112-unicidad-de-la-representacion)

**Aplicación**:

- Garantiza que no hay ambigüedad en sistemas posicionales
- Fundamental para computación (cada número tiene representación única en binario)

---

### Sección 2.1.1.3 - Conversión entre Sistemas

**Contenido**:

- Algoritmo de divisiones sucesivas (decimal → base B)
- Método del Polinomio (base B → decimal, explícito)
- Método de Horner (base B → decimal, optimizado)
- Conversiones entre bases relacionadas (B^m ↔ B^n)

**Ubicación**: [CONTENIDOS_FE.md](CONTENIDOS_FE.md#2113-conversion-entre-sistemas-de-numeracion)

**Ejemplos**:

- 1994₁₀ → 30434₅ (divisiones sucesivas)
- 30434₅ → 1994₁₀ (Horner: más eficiente)

---

### Sección 2.1.1.4 - Calculadora Interactiva

**Contenido**:

- Referencias a módulos Python
- Funciones disponibles
- Script demostrativo
- Tabla de ejemplos

**Ubicación**: [CONTENIDOS_FE.md](CONTENIDOS_FE.md#2114-calculadora-numeros-romanos--decimal)

---

### Sección 2.1.1.5 - Sistemas Binarios, Octales y Hexadecimales

**Subsecciones**:

- **2.1.1.5.1** - Sistemas de numeración binaria
  - Conversión entre binario ($B = 2$) y decimal ($B = 10$)

- **2.1.1.5.2** - Sistemas de numeración octal y hexadecimal
  - Conversión entre octal ($B = 8 = 2^3$), hexadecimal ($B = 16 = 2^4$) y decimal

- **2.1.1.5.3** - Conversión entre binario, octal y hexadecimal
  - Métodos de agrupación de dígitos

- **2.1.1.5.4** - Sistema de conversión entre bases relacionadas
  - Conversión entre base $B$ y base $B'$ donde $B = b^n$ y $b^m = B'$

---

### Sección 2.1.1.6 - Representación en Longitud Fija

**Subsecciones**:

- **2.1.1.6.1** - Representación de números naturales
  - Capacidad de representación para longitud fija n y base B (2.1.1.6.1.1)
  - Rango de valores representables (2.1.1.6.1.2)
  - Comparación entre números en sistemas nativos (2.1.1.6.1.3)
  - Sistemas BCD - Codificación Decimal Binaria (2.1.1.6.1.4)
  - Sistemas de representación binaria en base 2 (2.1.1.6.1.5)

- **2.1.1.6.2** - Relación base-dígitos-rango
  - Relación entre base, número de dígitos y rango de valores

---

### Sección 2.1.1.7 - Números Enteros con Signo

**Subsecciones**:

- **2.1.1.7.1** - Magnitud y signo
  - Representación en longitud fija

- **2.1.1.7.2** - Complemento a la base B
  - Complemento a 2 en base 2 (2.1.1.7.2.1)
  - Complemento a 10 en base 10 (2.1.1.7.2.2)
  - BCD exceso a 3 y BCD Aitken (2.1.1.7.2.3)

- **2.1.1.7.3** - Exceso a un sesgo k
  - Representación con sesgo

---

### Sección 2.1.1.8 - Operaciones Aritméticas

**Subsecciones**:

- **2.1.1.8.1** - Comparación de números
  - En magnitud y signo (2.1.1.8.1.1)
  - En complemento a 2 (2.1.1.8.1.2)
  - En exceso a un sesgo k (2.1.1.8.1.3)

- **2.1.1.8.2** - Suma y resta de números naturales
  - Suma y resta en base B

- **2.1.1.8.3** - Operaciones de complementación
  - Complementación a la base B y a la base B menos 1

- **2.1.1.8.4** - Inversión de signo
  - En magnitud y signo (2.1.1.8.4.1)
  - En complemento a la base B (2.1.1.8.4.2)
  - En exceso a un sesgo k (2.1.1.8.4.3)

- **2.1.1.8.5** - Suma y resta de números enteros
  - En magnitud y signo (2.1.1.8.5.1)
  - En complemento a la base B (2.1.1.8.5.2)
  - En exceso a un sesgo k (2.1.1.8.5.3)

- **2.1.1.8.6** - Multiplicación de números naturales
  - Multiplicación en base B

- **2.1.1.8.7** - División y resto
  - División y resto entre números naturales en base B=2

---

### Sección 2.1.1.9 - Representación de Números con Parte Fraccionaria

**Subsecciones**:

- **2.1.1.9.1** - Representación fija (fixed-point)
  - Concepto de punto fijo

- **2.1.1.9.2** - Conversiones entre formatos
  - Conversión E,L-E (parte entera, fraccionaria) (2.1.1.9.2.1)
  - Conversión entre bases B y B' en punto fijo (2.1.1.9.2.2)
  - Conversión entre bases 10 y 2 (2.1.1.9.2.3)
  - Conversión entre bases potencias de común (2.1.1.9.2.4)
  - Conversión entre bases 2, 4, 8 y 16 (2.1.1.9.2.5)
  - Conversión entre bases 3, 9 y 27 (2.1.1.9.2.6)

- **2.1.1.9.3** - Rango y precisión
  - Rangos representables para longitud fija L (2.1.1.9.3.1)
  - El épsilon de la representación (2.1.1.9.3.2)

- **2.1.1.9.4** - Representación en punto flotante
  - Concepto de punto flotante (2.1.1.9.4.1)
  - Norma IEEE 754 (2.1.1.9.4.2)
  - Épsilon de punto flotante (2.1.1.9.4.3)
  - Rangos IEEE 754 (2.1.1.9.4.4)
  - Formas normalizadas y denormalizadas (2.1.1.9.4.5)

- **2.1.1.9.5** - Operaciones en punto flotante
  - Redondeo y truncamiento (2.1.1.9.5.1)
  - Función 'normalizar' (2.1.1.9.5.2)
  - Conversión punto fijo ↔ punto flotante (2.1.1.9.5.3)
  - Operaciones aritméticas en punto flotante (2.1.1.9.5.4)

---

## 💻 Código Disponible

### Módulo Principal: `core/sistemas_numeracion_basicos.py`

**400+ líneas de código funcional**

#### Funciones de Números Romanos

```python
from core.sistemas_numeracion_basicos import (
    decimal_a_romano,
    romano_a_decimal,
    explicar_romano
)

# Conversión decimal → romano
resultado = decimal_a_romano(1994)  # "MCMXCIV"

# Conversión romano → decimal
numero = romano_a_decimal("MCMXCIV")  # 1994

# Explicación paso a paso
detalle = explicar_romano(1994)
# {
#   'numero_decimal': 1994,
#   'romano': 'MCMXCIV',
#   'desglose': [
#     {'valor': 1000, 'simbolo': 'M', 'cantidad': 1, 'representacion': 'M', 'resta': 1000},
#     {'valor': 900, 'simbolo': 'CM', ...},
#     ...
#   ]
# }
```

#### Funciones de Base 5

```python
from core.sistemas_numeracion_basicos import (
    decimal_a_base_5,
    base_5_a_decimal,
    explicar_base_5
)

# Conversión decimal → base 5
base5 = decimal_a_base_5(1994)  # "30434"

# Conversión base 5 → decimal
numero = base_5_a_decimal("30434")  # 1994

# Explicación paso a paso
detalle = explicar_base_5(1994)
# Incluye desglose por potencias:
# {
#   'potencias': [
#     {'posicion': 0, 'digito': '4', 'potencia': 1, 'calculo': '4*5^0', 'valor': 4},
#     {'posicion': 1, 'digito': '3', 'potencia': 5, 'calculo': '3*5^1', 'valor': 15},
#     ...
#   ]
# }
```

#### Funciones de Tiempo

```python
from core.sistemas_numeracion_basicos import (
    decimal_a_tiempo,
    tiempo_a_decimal,
    explicar_tiempo
)

# Conversión segundos → HH:MM:SS
tiempo = decimal_a_tiempo(3661)  # "01:01:01"

# Conversión HH:MM:SS → segundos
segundos = tiempo_a_decimal("01:01:01")  # 3661

# Explicación paso a paso
detalle = explicar_tiempo(3661)
# {
#   'segundos_totales': 3661,
#   'tiempo': '01:01:01',
#   'desglose': {'horas': 1, 'minutos': 1, 'segundos': 1},
#   'calculo': '1*3600 + 1*60 + 1 = 3661'
# }
```

#### Funciones Comparativas

```python
from core.sistemas_numeracion_basicos import (
    comparar_sistemas,
    demostrar_unicidad
)

# Ver número en múltiples sistemas
comparacion = comparar_sistemas(27)
# {
#   'numero_decimal': 27,
#   'sistemas': {
#     'romano': {'representacion': 'XXVII', 'tipo': 'No Posicional', ...},
#     'base_5': {'representacion': '102', 'tipo': 'Posicional (potencias de 5)', ...},
#     'base_10': {'representacion': '27', 'tipo': 'Posicional (potencias de 10)', ...}
#   }
# }

# Verificar unicidad de representación
unicidad = demostrar_unicidad()
# Tabla de 5 números con verificación de conversiones inversas
```

---

### Script Demostrativo: `demo_sistemas_numeracion_basicos.py`

**240+ líneas con 5 demostraciones completas**

**Ejecución**:

```bash
cd GeneratorFEExercises
python demo_sistemas_numeracion_basicos.py
```

**Salida completa**: ~350 líneas con 5 secciones

#### Demo 1: Números Romanos

```
Ejemplos: 4, 9, 27, 49, 99, 444, 1994
Formato:
  4 (base 10) = IV (inverso: 4)
  27 (base 10) = XXVII (inverso: 27)
  1994 (base 10) = MCMXCIV (inverso: 1994)

Desglose de 1994:
  M = 1× M = 1000
  CM = 1× CM = 900
  XC = 1× XC = 90
  IV = 1× IV = 4
  Total: MCMXCIV = 1994
```

#### Demo 2: Base 5

```
Ejemplos: 4, 9, 27, 49, 99, 125, 1994
Conversiones verificadas, desglose por potencias:
  Posicion | Digito | Potencia | Calculo  | Valor
  0        | 4      | 5^0      | 4*5^0    | 4
  1        | 3      | 5^1      | 3*5^1    | 15
  2        | 4      | 5^2      | 4*5^2    | 100
  3        | 0      | 5^3      | 0*5^3    | 0
  4        | 3      | 5^4      | 3*5^4    | 1875
  
  Suma: 4 + 15 + 100 + 0 + 1875 = 1994
```

#### Demo 3: Tiempo

```
Ejemplos: 4s, 49s, 99s, 3661s, 86400s, 90061s
Formato:
  4s = 00:00:04
  3661s = 01:01:01
  86400s = 24:00:00

Desglose de 3661:
  Horas: 3661 / 3600 = 1
  Minutos: (3661 % 3600) / 60 = 1
  Segundos: 3661 % 60 = 1
```

#### Demo 4: Comparación

```
El número 27 en diferentes sistemas:
  ROMANO: XXVII (no posicional)
  BASE 5: 102 (posicional con potencias)
  BASE 10: 27 (posicional con potencias)
```

#### Demo 5: Unicidad

```
Verificación de que cada número tiene representación ÚNICA:
  Numero | Decimal | Romano | Base 5 | Verificacion
  4      | 4       | IV     | 4      | ✓
  27     | 27      | XXVII  | 102    | ✓
  99     | 99      | XCIX   | 344    | ✓
  1994   | 1994    | MCMXCIV| 30434  | ✓
  
  Conclusion: Todas las conversiones son REVERSIBLES y UNICAS
```

---

## 📖 Documentación

### Archivo Principal: `CONTENIDOS_FE.md`

**Sección 2.1.1**: Sistemas de Numeración (850+ líneas nuevas)

- Definiciones matemáticas
- 3 ejemplos con detalles
- Tablas de pesos
- Algoritmos de conversión
- Fórmulas y ejemplos

**Acceso directo**:

- [2.1.1.1](CONTENIDOS_FE.md#2111-sistemas-posicionales-y-no-posicionales)
- [2.1.1.2](CONTENIDOS_FE.md#2112-unicidad-de-la-representacion)
- [2.1.1.3](CONTENIDOS_FE.md#2113-conversion-entre-sistemas-de-numeracion)
- [2.1.1.4](CONTENIDOS_FE.md#2114-calculadora-numeros-romanos--decimal)

### Resumen Ejecutivo: `SISTEMAS_NUMERACION_RESUMEN.md`

**300+ líneas con**:

- Respuesta a pregunta del usuario
- Características del sistema temporal
- Módulos y funciones disponibles
- Tabla de métodos de conversión
- Prueba de unicidad
- Referencias y archivos

---

## 🎯 Casos de Uso

### Usar para Enseñanza

```python
# Mostrar la diferencia entre posicional y no posicional
numero = 27

# No posicional
romano = decimal_a_romano(numero)  # XXVII

# Posicional (Base 5)
base5 = decimal_a_base_5(numero)   # 102

print(f"{numero} = {romano} (no posicional) = {base5}_5 (posicional)")
# 27 = XXVII (no posicional) = 102_5 (posicional)
```

### Verificar Conversiones

```python
# Garantizar reversibilidad
for numero in [4, 9, 27, 99, 1994]:
    romano = decimal_a_romano(numero)
    inverso = romano_a_decimal(romano)
    assert inverso == numero, f"Error en {numero}"
    
    base5 = decimal_a_base_5(numero)
    inverso = base_5_a_decimal(base5)
    assert inverso == numero, f"Error en {numero}"

print("Todas las conversiones verificadas: OK")
```

### Comparar Eficiencia (Horner vs Polinomio)

```python
# Ambos métodos dan el mismo resultado
# Pero Horner es más eficiente (n multiplicaciones vs 2n)

base5_str = "30434"

# Método Polinomio (explícito)
resultado_polinomio = (3*625 + 0*125 + 4*25 + 3*5 + 4*1)

# Método Horner (optimizado)
resultado_horner = (((3*5 + 0)*5 + 4)*5 + 3)*5 + 4

assert resultado_polinomio == resultado_horner == 1994
```

---

## 🔍 Archivos de Referencia

| Archivo | Tipo | Tamaño | Descripción |
|---------|------|--------|-------------|
| [core/sistemas_numeracion_basicos.py](core/sistemas_numeracion_basicos.py) | Módulo | 400+ líneas | Conversiones y funciones |
| [demo_sistemas_numeracion_basicos.py](demo_sistemas_numeracion_basicos.py) | Script | 240+ líneas | 5 demostraciones |
| [CONTENIDOS_FE.md](CONTENIDOS_FE.md) | Doc | 850+ líneas (secc 2.1.1) | Teoría y explicaciones |
| [SISTEMAS_NUMERACION_RESUMEN.md](SISTEMAS_NUMERACION_RESUMEN.md) | Doc | 300+ líneas | Resumen ejecutivo |
| [SISTEMAS_NUMERACION_NAVEGACION.md](SISTEMAS_NUMERACION_NAVEGACION.md) | Doc | Este archivo | Guía de navegación |

---

## ✅ Checklist de Contenido

- [x] Sección 2.1.1.1: Sistemas posicionales y no posicionales
- [x] Sección 2.1.1.2: Unicidad de representación
- [x] Sección 2.1.1.3: Conversión entre sistemas (Polinomio, Horner)
- [x] Sección 2.1.1.4: Calculadora de romanos y base 5
- [x] Módulo Python con conversiones
- [x] 5 demostraciones completas
- [x] Respuesta a pregunta del usuario (sistema temporal)
- [x] Documentación matemática
- [x] Tablas de ejemplos y verificación
- [x] Guía de navegación (este archivo)

---

## 🚀 Próximos Pasos

**Sugerencias para expansión**:

1. **Sección 2.1.2**: Sistemas Binarios, Octales y Hexadecimales
   - Usar módulos existentes: `core/numeracion_utils.py`
   - Crear `demo_bases_binario_octal_hexa.py`

2. **Sección 2.1.3**: Bases Relacionadas (B^m ↔ B^n)
   - Usar módulo existente: `core/conversiones_bases_relacionadas.py`
   - Crear demostraciones para 2↔4↔8↔16↔32, 3↔9↔27, etc.

3. **Representación en Longitud Fija**
   - Capacidad de representación
   - Rango de valores
   - Desbordamiento

4. **Números Enteros con Signo**
   - Magnitud y signo
   - Complemento a 2
   - Exceso a sesgo k

---

**Última actualización**: 2024-12-19
**Commits asociados**: `c2f0de1`, `464bf4e`
