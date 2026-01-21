# Conversión entre Bases Relacionadas

## Introducción

Cuando necesitas convertir un número de una base a otra, y ambas bases son **potencias de la misma base primitiva**, existe un algoritmo altamente optimizado que **no requiere pasar por decimal**.

### Ejemplo

```
11111111₂ → FF₁₆

En lugar de:
  11111111₂ → 255₁₀ → FF₁₆  (conversión tradicional, requiere decimal)

Podemos hacer:
  11111111₂ → FF₁₆  (conversión directa, sin decimal)
```

¿Por qué funciona? Porque **2 = 2^1** y **16 = 2^4**, ambas son potencias de 2.

---

## El Algoritmo

### Paso 0: Identificar Bases Relacionadas

Dado:
- Número n en base B^l
- Convertir a base B^k

Donde B es la **base primitiva** y l, k son los **exponentes**.

### Paso 1: Calcular Parámetros

```
m = gcd(l, k)
l' = l / m
k' = k / m
```

### Paso 2: Convertir de B^l a B

Cada dígito en base B^l = l' dígitos en base B

```
Dígito en B^l → l' dígitos en B (rellenar con ceros si es necesario)
```

### Paso 3: Agrupar Dígitos

Reagrupar los dígitos de B de **k' en k'** (desde la derecha)

```
...d₃d₂d₁d₀ (en base B)
↓ (agrupar de k' en k')
(...d₃d₂)(d₁d₀) o similar
```

### Paso 4: Convertir a B^k

Cada grupo de k' dígitos en B = 1 dígito en B^k

```
(k' dígitos en B) → 1 dígito en B^k
```

---

## Ejemplos Concretos

### Ejemplo 1: Binario → Hexadecimal

```
Número: 1010₂
Destino: Base 16

Paso 0:
  2 = 2^1 (binario)
  16 = 2^4 (hexadecimal)
  Base primitiva B = 2

Paso 1:
  l = 1, k = 4
  m = gcd(1, 4) = 1
  l' = 1/1 = 1
  k' = 4/1 = 4

Paso 2:
  1010₂ es ya 4 dígitos en base 2 ✓

Paso 3:
  Agrupar de 4 en 4 desde la derecha:
  (1010)₂

Paso 4:
  1010₂ = 10₁₀ = A₁₆

Resultado: A₁₆
```

### Ejemplo 2: Binario → Octal

```
Número: 101101010₂
Destino: Base 8

Paso 0:
  2 = 2^1 (binario)
  8 = 2^3 (octal)
  Base primitiva B = 2

Paso 1:
  l = 1, k = 3
  m = gcd(1, 3) = 1
  l' = 1/1 = 1
  k' = 3/1 = 3

Paso 2:
  101101010₂ es ya dígitos en base 2 ✓

Paso 3:
  Agrupar de 3 en 3 desde la derecha:
  (101)(101)(010)₂

Paso 4:
  101₂ = 5₈
  101₂ = 5₈
  010₂ = 2₈

Resultado: 552₈
```

### Ejemplo 3: Base 3 → Base 9

```
Número: 12101₃
Destino: Base 9

Paso 0:
  3 = 3^1 (ternario)
  9 = 3^2 (base 9)
  Base primitiva B = 3

Paso 1:
  l = 1, k = 2
  m = gcd(1, 2) = 1
  l' = 1/1 = 1
  k' = 2/1 = 2

Paso 2:
  12101₃ es ya dígitos en base 3 ✓

Paso 3:
  Agrupar de 2 en 2 desde la derecha:
  (1)(21)(01)₃

Paso 4:
  01₃ = 1₉ (sin el dígito importante)
  21₃ = 2×3 + 1 = 7₉
  1₃ = 1₉

Resultado: 171₉
```

---

## Casos de Uso

### Grupos de Bases Relacionadas

| Base Primitiva | Grupo | Ejemplo |
|---|---|---|
| 2 | 2, 4, 8, 16, 32 | Binario ↔ Hexadecimal |
| 3 | 3, 9, 27 | Ternario ↔ Base 9 ↔ Base 27 |
| 5 | 5, 25 | Base 5 ↔ Base 25 |
| 6 | 6, 36 | Base 6 ↔ Base 36 |
| 7 | 7, 49 | Base 7 ↔ Base 49 |
| etc. | ... | ... |

---

## Ventajas del Algoritmo

### ✅ Ventajas

1. **Sin conversión a decimal**: Evita números grandes intermedios
2. **Rápido**: Solo agrupación y conversión local
3. **Exacto**: Sin pérdida de precisión
4. **Escalable**: Funciona con números muy grandes
5. **Patrón visual**: Es fácil de ver en la práctica

### ⚠️ Limitaciones

1. Solo funciona para bases **relacionadas** (potencias de la misma base)
2. Requiere identificar correctamente la base primitiva
3. Para bases no relacionadas, usar método tradicional

---

## Implementación

### Función Principal

```python
from core.conversiones_bases_relacionadas import convertir_bases_relacionadas

resultado = convertir_bases_relacionadas(
    numero_str="1010",      # Número como string
    base_origen=2,          # Base origen
    base_destino=16,        # Base destino
    verbose=False           # Mostrar pasos
)

print(resultado['resultado'])  # → "A"
```

### Con Pasos Detallados

```python
resultado = convertir_bases_relacionadas(
    "11111111",
    2, 16,
    verbose=True
)

for paso in resultado['pasos']:
    print(paso)
```

### Comparación de Métodos

```python
from core.conversiones_bases_relacionadas import comparar_conversiones_bases_relacionadas

comparacion = comparar_conversiones_bases_relacionadas("FF", 16, 2)

print(comparacion['resultado_optimizado'])    # Método optimizado
print(comparacion['resultado_tradicional'])   # Método tradicional
print(comparacion['coinciden'])               # Deben coincidir
```

---

## Ejemplos de Código

### Ejemplo 1: Conversión simple

```python
from core.conversiones_bases_relacionadas import convertir_bases_relacionadas

# Binario a Hexadecimal
resultado = convertir_bases_relacionadas("11001100", 2, 16)
print(f"Result: {resultado['resultado']}")  # → "CC"
```

### Ejemplo 2: Tabla de conversiones

```python
numero = "101010"
bases = [2, 4, 8, 16]

print(f"Número: {numero}₂\n")
for base_dest in bases[1:]:
    resultado = convertir_bases_relacionadas(numero, 2, base_dest)
    print(f"  En base {base_dest}: {resultado['resultado']}")
```

### Ejemplo 3: Conversion chains

```python
# 2 → 8 → 16
numero = "101010"

paso1 = convertir_bases_relacionadas(numero, 2, 8)
print(f"{numero}₂ → {paso1['resultado']}₈")

paso2 = convertir_bases_relacionadas(paso1['resultado'], 8, 16)
print(f"{paso1['resultado']}₈ → {paso2['resultado']}₁₆")
```

---

## Análisis Comparativo

### Método Optimizado vs Tradicional

Para convertir un número de base B^l a base B^k:

| Aspecto | Optimizado | Tradicional |
|---|---|---|
| Pasos intermedios | Agrupación de dígitos | Conversión a decimal |
| Velocidad | ⚡ Rápido | 🐌 Lento (especialmente números grandes) |
| Precisión | 100% | 100% |
| Aplicabilidad | Solo bases relacionadas | Cualquier base |
| Complejidad | O(n) donde n = # dígitos | O(n log base) |

### Ejemplo de Rendimiento

```
Número: 1111111111111111 (16 dígitos binarios)

Método Tradicional:
  1. Convertir a decimal: 65535₁₀
  2. Convertir a hex: FFFF₁₆
  Total: 2 conversiones

Método Optimizado:
  1. Agrupar 4 en 4: (1111)(1111)(1111)(1111)
  2. Convertir cada grupo: F, F, F, F
  Total: 1 agrupación + 4 conversiones locales

Con números más grandes, la diferencia es aún más notable.
```

---

## Concepto Educativo

Este algoritmo enseña:

1. **Relaciones entre bases**: Las bases pueden estar relacionadas matemáticamente
2. **Optimización algorítmica**: Usar propiedades matemáticas para mejorar
3. **Agrupación inteligente**: Reorganizar datos para facilitar conversión
4. **Eficiencia sin sacrificar exactitud**: El resultado es idéntico pero más rápido

---

## Validación

Todos los casos han sido testeados:

✅ Binario ↔ Octal ↔ Hexadecimal  
✅ Base 3 ↔ Base 9 ↔ Base 27  
✅ Base 5 ↔ Base 25  
✅ Base 6 ↔ Base 36  
✅ Manejo de errores (bases no relacionadas)  
✅ Validación de entrada (dígitos inválidos)  

---

## Scripts Demostrativos

Ver [demo_bases_relacionadas.py](demo_bases_relacionadas.py) para:

- 8 demostraciones prácticas
- Paso a paso detallado
- Comparación de métodos
- Tablas de conversión
- Manejo de errores

Ejecutar:

```bash
python demo_bases_relacionadas.py
```

---

## Referencias

- **Algoritmo**: Basado en propiedades de bases numéricas relacionadas
- **Aplicaciones prácticas**: Conversiones en informática (binario ↔ hexadecimal muy común)
- **Generalización**: Puede extenderse a más de 2 bases relacionadas en una cadena

---

**Status**: ✅ Completado y validado  
**Última actualización**: 16 de Enero, 2026
