# 🚀 QUICK START: Usando Alphabet y FixedLengthLanguage

## Ejemplo 1: Crear un Lenguaje Binario Simple

```python
from core.sistemas_numeracion_basicos import Alphabet, FixedLengthLanguage

# Paso 1: Crear alfabeto
alfabeto = Alphabet(['0', '1'])

# Paso 2: Crear lenguaje (todas las palabras de 4 bits son válidas)
lenguaje = FixedLengthLanguage(
    alphabet=alfabeto,
    length=4,
    predicate=lambda p: True,  # Todas son válidas
    zero_element='0000',
    next_function=lambda p: format((int(p, 2) + 1) % 16, '04b'),
    name="Binario 4-bit"
)

# Paso 3: Usar el lenguaje
print(lenguaje.is_valid('1010'))              # True
print(lenguaje.hamming_distance('0000', '0011'))  # 2
```

---

## Ejemplo 2: Crear un Lenguaje Personalizado (Con Predicado)

```python
# Lenguaje con solo palabras pares (número de 1s es par)
lenguaje_pares = FixedLengthLanguage(
    alphabet=Alphabet(['0', '1']),
    length=4,
    predicate=lambda p: p.count('1') % 2 == 0,  # Paridad par
    zero_element='0000',
    next_function=lambda p: siguiente_paridad(p),
    name="Palabras con Paridad Par"
)

print(lenguaje_pares.is_valid('0011'))        # True (2 unos)
print(lenguaje_pares.is_valid('0111'))        # False (3 unos)
```

---

## Ejemplo 3: Usar Constructores Predefinidos

```python
from core.sistemas_numeracion_basicos import (
    crear_lenguaje_binario_saturado,
    crear_lenguaje_bcd,
    crear_lenguaje_johnson,
    crear_lenguaje_biquinario
)

# Crear lenguajes
binario = crear_lenguaje_binario_saturado(8)
bcd = crear_lenguaje_bcd()
johnson = crear_lenguaje_johnson()
biquinario = crear_lenguaje_biquinario()

# Todos usan la misma interfaz
print(f"BCD válido para '1001': {bcd.is_valid('1001')}")
print(f"Johnson válido para '11110': {johnson.is_valid('11110')}")
```

---

## Ejemplo 4: Analizar Propiedades del Lenguaje

```python
# Generar todas las palabras
todas_palabras = johnson.generate_all_words()
print(f"Palabras en Johnson: {todas_palabras}")
# ['00000', '00001', '00011', '00111', '01111', '11111', '11110', '11100', '11000', '10000']

# Analizar adyacencia
análisis = johnson.analyze_adjacency()
print(f"¿Es adyacente? {análisis['is_adjacent']}")      # True (cada sucesiva difiere en 1)
print(f"¿Es cíclico? {análisis['is_cyclic']}")          # True (último conecta con primero)
print(f"Total palabras: {análisis['total_words']}")     # 10

# Grafo de adyacencia
grafo = análisis['adjacency_graph']
print(f"Adyacentes a '00001': {grafo['00001']}")
```

---

## Ejemplo 5: Compatibilidad Hacia Atrás (Nombres Antiguos)

```python
# Puedes seguir usando nombres en español si lo prefieres
lenguaje = crear_lenguaje_bcd()

# Métodos antiguos siguen funcionando
print(lenguaje.es_valida('1001'))                  # is_valid() alias
print(lenguaje.distancia_hamming('0000', '0001'))  # hamming_distance() alias
print(lenguaje.son_adyacentes('0000', '0001'))     # are_adjacent() alias

# Propiedades antiguas siguen funcionando
print(lenguaje.alfabeto)                            # alphabet.symbols
print(lenguaje.longitud)                            # length
print(lenguaje.nombre)                              # name
```

---

## Ejemplo 6: Convención MSB/LSB (Importante para Hamming)

```python
lenguaje = crear_lenguaje_binario_saturado(4)
palabra = '1010'

# Indices: 3 2 1 0
#          ↓ ↓ ↓ ↓
# Palabra: 1 0 1 0
#          ↑     ↑
#         MSB   LSB

# En la clase, los índices se usan así:
print(f"Bit en índice 3 (MSB): {palabra[3]}")   # '0'
print(f"Bit en índice 0 (LSB): {palabra[0]}")   # '0'

# Esto es importante para Hamming (7,4):
# - Posiciones 1, 2, 4 son de paridad (2^n)
# - Posiciones 3, 5, 6, 7 son de datos
# - Todos cuentan hacia atrás desde el MSB
```

---

## Ejemplo 7: Crear una Subclase Personalizada

```python
class HammingLanguage(FixedLengthLanguage):
    """Lenguaje Hamming (7,4) especializado"""
    
    def __init__(self):
        super().__init__(
            alphabet=Alphabet(['0', '1']),
            length=7,
            predicate=self.es_hamming_valido,
            zero_element='0000000',
            next_function=self.siguiente_hamming,
            name="Hamming (7,4)"
        )
    
    def es_hamming_valido(self, palabra):
        """Verificar que la palabra cumple con la matriz de paridad"""
        # Implementar validación específica de Hamming
        pass
    
    def siguiente_hamming(self, palabra):
        """Siguiente palabra Hamming válida"""
        # Implementar generación específica
        pass
    
    def calcular_sindrome(self, palabra):
        """Calcular síndrome (específico de Hamming)"""
        pass
```

---

## Resumen: API Principal

### Clase `Alphabet`

```python
alphabet = Alphabet(['0', '1', '2'])
alphabet.size              # 3
alphabet.base              # 3
'0' in alphabet            # True
alphabet.index_of('1')     # 1
list(alphabet)             # ['0', '1', '2']
```

### Clase `FixedLengthLanguage`

```python
# Constructor
lang = FixedLengthLanguage(alphabet, length, predicate, zero_element, next_function, name)

# Validación
lang.is_valid(palabra)                      # bool
lang.es_valida(palabra)                     # bool (alias)

# Navegación
lang.next_word(palabra)                     # str
lang.siguiente_palabra(palabra)              # str (alias)

# Análisis de distancia
lang.hamming_distance(p1, p2)               # int
lang.distancia_hamming(p1, p2)              # int (alias)

# Relaciones
lang.are_adjacent(p1, p2)                   # bool (d_H = 1)
lang.son_adyacentes(p1, p2)                 # bool (alias)

# Generación
lang.generate_all_words()                   # List[str]
lang.generar_todas_palabras()               # List[str] (alias)

# Análisis
lang.analyze_adjacency()                    # Dict con grafo
lang.analizar_adyacencia()                  # Dict (alias)

# Propiedades
lang.alphabet                               # Alphabet object
lang.length                                 # int
lang.name                                   # str
lang.zero_element                           # Any
lang.next_function                          # Callable
```

---

## Notas Importantes

1. **MSB/LSB Convention**:
   - MSB siempre en índice n-1
   - LSB siempre en índice 0
   - Crítico para Hamming (7,4)

2. **Caching**:
   - Lenguajes con ≤ 10,000 palabras se cachean automáticamente
   - `generate_all_words()` es rápido para lenguajes pequeños

3. **Backward Compatibility**:
   - 100% compatible con código antiguo
   - Puedes mezclar métodos antiguos y nuevos
   - `Lenguaje` sigue siendo válido como alias

4. **Performance**:
   - Operaciones O(1): `is_valid()`, `hamming_distance()`, `are_adjacent()`
   - Operaciones O(n): `generate_all_words()` (donde n = |Σ|^length)
   - `analyze_adjacency()` es O(n²) (cuidado con lenguajes grandes)

---

**Próximo**: Implementar FASE 5 (Hamming 7,4) usando esta arquitectura.
