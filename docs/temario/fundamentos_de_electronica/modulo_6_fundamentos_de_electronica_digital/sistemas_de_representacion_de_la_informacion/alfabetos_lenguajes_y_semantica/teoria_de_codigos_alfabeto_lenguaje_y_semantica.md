# Teoría de Códigos: Alfabeto, Lenguaje y Semántica

**Ruta:** [📚 Fundamentos de Electrónica](../../../index.md) > [Módulo 6: Fundamentos de Electrónica Digital](../../index.md) > [Sistemas de Representación de la Información](../index.md) > [Alfabetos, Lenguajes y Semántica](index.md)
[Siguiente ➡️](propiedades_de_codigos_adyacente_ciclico_saturado.md)

---

**ID:** `1.6.1.1.1`

## 📝 Contenido Teórico

La pregunta es sencilla: en los sistemas analógicos tenemos una cantidad incontable de representaciones posibles de la información. De hecho esas representaciones solo podemos aproximarlas mediante mediciones con una precisión limitada. Las matemáticas que usamos en electrónica analógica se desarrollaron hace unos siglos y ustedes los conocéis como el cálculo infinitesimal. En los sistemas digitales, en cambio, la información se representa mediante un conjunto finito de símbolos discretos. El caso más sencillo es, además, el más práctico: el sistema binario. Con todo, veremos que existen otros sistemas de representación digital, y que todos ellos se basan en los mismos principios matemáticos. Será de utilidad verlos con generalidad, pues aunque la base nativa de nuestro sistema sea el binario, en capas de construcción superiores (construidas sobre el binario) usaremos conjuntos de símbolos discretos diferentes. Para  nosotros, a ese conjunto de símbolos discretos los llamaremos alfabeto.

### Alfabeto

Un alfabeto es un conjunto finito de símbolos o caracteres que se utilizan para construir cadenas o palabras en un lenguaje formal. En el contexto de la teoría de códigos y la informática, un alfabeto es la base para definir lenguajes formales y sistemas de representación de la información.

**Notación**: Se suele denotar como Σ (sigma mayúscula), y su cardinal como |Σ| = n.

### Lenguaje Formal

Dado un alfabeto Σ, un **lenguaje formal L** sobre Σ es un conjunto de palabras (cadenas finitas de símbolos) formadas con los símbolos de Σ.

#### Clasificación de lenguajes por longitud

1. **Lenguajes de longitud infinita**: Conjuntos infinitos de palabras de longitudes variables
   - Ejemplos: Todas las palabras binarias, números naturales en decimal, expresiones regulares
   - En práctica limitada: solo implementaremos casos específicos como ejemplos teóricos

2. **Lenguajes de longitud finita fija**: Todas las palabras tienen longitud l fija
   - **Lenguaje universo** Σ^l: Conjunto de todas las palabras de longitud l
   - Cardinal: |Σ^l| = n^l palabras posibles
   - Ejemplo: Alfabeto binario (n=2) de longitud l=3 → 2³ = 8 palabras: {000, 001, 010, 011, 100, 101, 110, 111}

3. **Sublenguajes**: Subconjuntos del lenguaje universo que cumplen ciertos criterios
   - Definidos mediante **funciones predicado**: L = {w ∈ Σ^l | P(w) = verdadero}
   - Ejemplo: Palabras binarias de longitud 4 con número par de unos

#### Criterios de pertenencia

Para determinar si una palabra w pertenece a un lenguaje L, podemos usar:

1. **Función predicado booleana**: P(w) → {True, False}
   - Retorna True si w ∈ L, False si w ∉ L
   - Ejemplo: `lambda w: w.count('1') % 2 == 0` (paridad de unos)

2. **Máquina de estados / Autómata**: M(w) → {Aceptar, Rechazar, Indeterminado}
   - **Aceptar**: La palabra pertenece al lenguaje
   - **Rechazar**: La palabra NO pertenece al lenguaje
   - **Indeterminado**: No se puede decidir (en lenguajes complejos o con límites de cómputo)

#### Operaciones sobre lenguajes

- **Unión**: L₁ ∪ L₂ = {w | w ∈ L₁ o w ∈ L₂}
- **Intersección**: L₁ ∩ L₂ = {w | w ∈ L₁ y w ∈ L₂}
- **Complemento**: L̄ = Σ*\ L = {w ∈ Σ* | w ∉ L}
- **Concatenación**: L₁ · L₂ = {w₁w₂ | w₁ ∈ L₁, w₂ ∈ L₂}

### Ejemplo práctico: Códigos de longitud fija

En sistemas digitales, es común usar códigos de longitud fija:

- **BCD (4 bits)**: 10 palabras válidas de las 16 posibles (2⁴)
- **ASCII (7 bits)**: 128 caracteres posibles (2⁷)
- **UTF-8 básico**: Caracteres en rangos específicos

## 🔧 Funciones Python Asociadas

### [[core.alfabetos.Alfabeto]]

- **Descripción**: Clase abstracta base para representar alfabetos
- **Métodos principales**:
  - `contiene()`, `validar_palabra()`, `generar_palabras()`
  - `indice_de()`, `simbolo_en()`
  - `comparar_simbolos()`, `es_menor()`, `es_igual()`, `es_mayor()`
  - `comparar_palabras_lexicografico()`
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetoExplicito]]

- **Descripción**: Alfabeto definido mediante lista explícita de símbolos con índices
- **Ejemplo**: `AlfabetoExplicito('0', '1', '2', '3')` → {'0': 0, '1': 1, '2': 2, '3': 3}
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetoEstandar]]

- **Descripción**: Alfabeto estándar basado en base numérica (2-36)
- **Ejemplo**: `AlfabetoEstandar(16)` → ['0'-'9', 'A'-'F']
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetoBinario]]

- **Descripción**: Alfabeto binario especializado con '0' → 0 y '1' → 1
- **Ejemplo**: `AlfabetoBinario()` → {'0': 0, '1': 1}
- **Estado**: ✅ Implementada

### [[core.alfabetos.crear_alfabeto_explicito]]

- **Descripción**: Factory para crear alfabeto con símbolos explícitos
- **Parámetros**: `(*simbolos: str) -> AlfabetoExplicito`
- **Uso**: `crear_alfabeto_explicito('a', 'b', 'c')`
- **Estado**: ✅ Implementada

### [[core.alfabetos.crear_alfabeto_estandar_desde_cardinal]]

- **Descripción**: Factory para crear alfabeto estándar desde base numérica
- **Parámetros**: `(base: int, mayusculas: bool = True) -> AlfabetoEstandar`
- **Uso**: `crear_alfabeto_estandar_desde_cardinal(16)` para hexadecimal
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetosPredefinidos.binario]]

- **Descripción**: Alfabeto binario predefinido {0, 1}
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetosPredefinidos.octal]]

- **Descripción**: Alfabeto octal predefinido {0-7}
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetosPredefinidos.decimal]]

- **Descripción**: Alfabeto decimal predefinido {0-9}
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetosPredefinidos.hexadecimal]]

- **Descripción**: Alfabeto hexadecimal predefinido {0-9, A-F}
- **Parámetros**: `(mayusculas: bool = True)`
- **Estado**: ✅ Implementada

### [[core.alfabetos.AlfabetosPredefinidos.bcd]]

- **Descripción**: Alfabeto BCD (Binary Coded Decimal) con códigos de 4 bits
- **Estado**: ✅ Implementada

### [[core.alfabetos.unir_alfabetos]]

- **Descripción**: Crea nuevo alfabeto como unión de dos alfabetos (sin duplicados)
- **Parámetros**: `(alf1: Alfabeto, alf2: Alfabeto) -> AlfabetoExplicito`
- **Estado**: ✅ Implementada

### [[core.alfabetos.Alfabeto.comparar_simbolos]]

- **Descripción**: Compara dos símbolos según su orden en el alfabeto
- **Parámetros**: `(simbolo1: str, simbolo2: str) -> Optional[int]`
- **Retorna**: `-1` (menor), `0` (igual), `1` (mayor), `None` (símbolo no válido)
- **Estado**: ✅ Implementada

### [[core.alfabetos.Alfabeto.es_menor]]

- **Descripción**: Verifica si simbolo1 < simbolo2 (operador <)
- **Parámetros**: `(simbolo1: str, simbolo2: str) -> bool`
- **Estado**: ✅ Implementada

### [[core.alfabetos.Alfabeto.es_igual]]

- **Descripción**: Verifica si simbolo1 = simbolo2 (operador =)
- **Parámetros**: `(simbolo1: str, simbolo2: str) -> bool`
- **Estado**: ✅ Implementada

### [[core.alfabetos.Alfabeto.es_mayor]]

- **Descripción**: Verifica si simbolo1 > simbolo2 (operador >)
- **Parámetros**: `(simbolo1: str, simbolo2: str) -> bool`
- **Estado**: ✅ Implementada

### [[core.alfabetos.Alfabeto.comparar_palabras_lexicografico]]

- **Descripción**: Compara dos palabras lexicográficamente según el alfabeto
- **Parámetros**: `(palabra1: str, palabra2: str) -> Optional[int]`
- **Ejemplo**: En binario, '101' < '110'
- **Estado**: ✅ Implementada

---

## 🔧 Funciones Python - Lenguajes Formales

### [[core.lenguajes.Lenguaje]]

- **Descripción**: Clase abstracta base para representar lenguajes formales
- **Atributos**: `alfabeto`, `longitud_fija`, `palabras`
- **Métodos**: `pertenece()`, `cardinal()`, `es_vacio()`, `enumerar()`, `es_sublenguaje_de()`, `es_igual_a()`
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeUniverso]]

- **Descripción**: Lenguaje universo Σ^l - todas las palabras de longitud l
- **Parámetros**: `(alfabeto: Alfabeto, longitud: int)`
- **Cardinal**: n^l donde n = |Σ|
- **Ejemplo**: `LenguajeUniverso(binario, 3)` → 8 palabras
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajePredicado]]

- **Descripción**: Sublenguaje definido por función predicado
- **Parámetros**: `(alfabeto: Alfabeto, longitud: int, predicado: Callable[[str], bool])`
- **Ejemplo**: `LenguajePredicado(binario, 4, lambda w: w.count('1') % 2 == 0)`
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeAutomata]]

- **Descripción**: Lenguaje definido por máquina de estados/autómata
- **Parámetros**: `(alfabeto: Alfabeto, automata: Callable[[str], EstadoDecision])`
- **Retorna**: `EstadoDecision.ACEPTAR | RECHAZAR | INDETERMINADO`
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeAutomata.combinar_con]]

- **Descripción**: Combina autómatas para reducir casos INDETERMINADO
- **Parámetros**: `(otro_automata: Callable[[str], EstadoDecision])`
- **Estrategia**: Si este da INDETERMINADO, consulta el otro autómata
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeExplicito]]

- **Descripción**: Lenguaje definido por lista explícita de palabras
- **Parámetros**: `(alfabeto: Alfabeto, palabras: Set[str])`
- **Ejemplo**: BCD = conjunto explícito de 10 códigos válidos
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeVacio]]

- **Descripción**: Lenguaje vacío ∅ - no contiene ninguna palabra
- **Propiedades**: |∅| = 0, ∅ ⊆ L para todo L, único (singleton)
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeInfinito]]

- **Descripción**: Lenguaje de longitud infinita (casos especiales)
- **Ejemplos**: `LenguajeNaturalesBinario()`
- **Métodos**: `pertenece()`, `generar_hasta(n)` (primeras n palabras)
- **Estado**: ✅ Implementada

### [[core.lenguajes.Lenguaje.es_sublenguaje_de]]

- **Descripción**: Verifica si L1 ⊆ L2 (todas las palabras de L1 están en L2)
- **Parámetros**: `(otro: Lenguaje) -> bool`
- **Operador**: `L1 <= L2`
- **Estado**: ✅ Implementada

### [[core.lenguajes.Lenguaje.es_superlenguaje_de]]

- **Descripción**: Verifica si L1 ⊇ L2 (L1 contiene a L2)
- **Parámetros**: `(otro: Lenguaje) -> bool`
- **Operador**: `L1 >= L2`
- **Estado**: ✅ Implementada

### [[core.lenguajes.Lenguaje.es_igual_a]]

- **Descripción**: Verifica si L1 = L2 (mismo conjunto de palabras)
- **Parámetros**: `(otro: Lenguaje) -> bool`
- **Operador**: `L1 == L2`
- **Estado**: ✅ Implementada

### [[core.lenguajes.Lenguaje.es_vacio]]

- **Descripción**: Verifica si el lenguaje es vacío (L = ∅)
- **Retorna**: `bool` - True si |L| = 0
- **Estado**: ✅ Implementada

### [[core.lenguajes.union]]

- **Descripción**: Unión de dos lenguajes L₁ ∪ L₂ = {w | w ∈ L₁ o w ∈ L₂}
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado`
- **Estado**: ✅ Implementada

### [[core.lenguajes.interseccion]]

- **Descripción**: Intersección de dos lenguajes L₁ ∩ L₂ = {w | w ∈ L₁ y w ∈ L₂}
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado`
- **Estado**: ✅ Implementada

### [[core.lenguajes.complemento]]

- **Descripción**: Complemento de un lenguaje L̄ = Σ^l \ L
- **Parámetros**: `(L: Lenguaje) -> LenguajePredicado`
- **Nota**: Solo para lenguajes de longitud fija
- **Estado**: ✅ Implementada

### [[core.lenguajes.diferencia]]

- **Descripción**: Diferencia L₁ \ L₂ = {w | w ∈ L₁ y w ∉ L₂}
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado`
- **Estado**: ✅ Implementada

### [[core.lenguajes.diferencia_simetrica]]

- **Descripción**: Diferencia simétrica L₁ △ L₂ = (L₁ \ L₂) ∪ (L₂ \ L₁)
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje) -> LenguajePredicado`
- **Equivalente**: XOR entre lenguajes
- **Estado**: ✅ Implementada

### [[core.lenguajes.concatenacion]]

- **Descripción**: Concatenación L₁ · L₂ = {w₁w₂ | w₁ ∈ L₁, w₂ ∈ L₂}
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje) -> LenguajeExplicito`
- **Nota**: Solo para lenguajes finitos
- **Estado**: ✅ Implementada

### [[core.lenguajes.potencia]]

- **Descripción**: Potencia L^n = L · L · ... · L (n veces)
- **Parámetros**: `(L: Lenguaje, n: int) -> LenguajeExplicito`
- **Casos especiales**: L^0 = {ε}, L^1 = L
- **Estado**: ✅ Implementada

### [[core.lenguajes.producto_cartesiano]]

- **Descripción**: Producto cartesiano L₁ × L₂ = {(w₁, w₂) | w₁ ∈ L₁, w₂ ∈ L₂}
- **Parámetros**: `(L1: Lenguaje, L2: Lenguaje, separador: str) -> LenguajeExplicito`
- **Nota**: Representado como palabras con separador
- **Estado**: ✅ Implementada
  
## 📚 Recursos Adicionales

- Pendiente de añadir referencias

## ✅ Estado de Desarrollo

- [ ] Teoría documentada
- [ ] Ejemplos añadidos
- [ ] Funciones Python implementadas
- [ ] Tests unitarios creados
