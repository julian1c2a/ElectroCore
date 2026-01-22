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

---

## 🔧 Alfabetos Jerárquicos

### Concepto de Alfabeto desde Lenguaje

Un alfabeto puede definirse no solo con símbolos básicos, sino usando **palabras de un lenguaje como símbolos**. Esto permite crear jerarquías multinivel:

- **Nivel 0**: Alfabeto básico Σ₀ = {0, 1}
- **Nivel 1**: Lenguaje L₁ sobre Σ₀ = {00, 01, 10, 11}
- **Nivel 2**: Alfabeto Σ₁ = L₁ (las palabras de L₁ son símbolos de Σ₁)
- **Nivel 3**: Lenguaje L₂ sobre Σ₁ (palabras formadas por símbolos del nivel anterior)

**Aplicaciones prácticas**:

- **BCD a bytes**: Usar dígitos BCD (4 bits) como símbolos → bytes (8 bits)
- **Códigos de error**: Usar palabras de código Hamming como símbolos
- **Protocolos de comunicación**: Tramas como símbolos de nivel superior
- **Lenguaje natural**: Palabras como símbolos → frases

### [[core.alfabetos.AlfabetoDesdeLenguaje]]

- **Descripción**: Alfabeto cuyos símbolos son las palabras de un lenguaje finito
- **Parámetros**: `(lenguaje: Lenguaje, separador: str = " ")`
- **Ejemplo**:

  ```python
  L1 = LenguajeUniverso(binario, longitud=2)  # {00, 01, 10, 11}
  alf_nivel2 = AlfabetoDesdeLenguaje(L1)      # Símbolos: '00', '01', '10', '11'
  ```

- **Atributos adicionales**:
  - `lenguaje_fuente`: Lenguaje del que provienen los símbolos
  - `separador`: String usado para separar símbolos al formar palabras
- **Estado**: ✅ Implementada

---

## 🔧 Lenguajes de Longitud Fija y Distancia de Hamming

### Teoría de Códigos: Distancia de Hamming

En teoría de códigos, la **distancia de Hamming** entre dos palabras de igual longitud es el número de posiciones en las que difieren sus símbolos.

**Definición**: d_H(w₁, w₂) = |{i | w₁[i] ≠ w₂[i]}|

**Propiedades importantes**:

- d_H(w, w) = 0 (distancia a sí misma)
- d_H(w₁, w₂) = d_H(w₂, w₁) (simétrica)
- d_H(w₁, w₃) ≤ d_H(w₁, w₂) + d_H(w₂, w₃) (desigualdad triangular)

**Peso de Hamming**: w_H(w) = número de símbolos no nulos (diferentes del primer símbolo del alfabeto)

- Ejemplo binario: w_H("0101") = 2 (dos unos)

**Distancia mínima de un código**: d_min = min{d_H(w₁, w₂) | w₁, w₂ ∈ L, w₁ ≠ w₂}

**Capacidad de detección y corrección**:

- d_min ≥ 2: puede **detectar** 1 error
- d_min ≥ 3: puede **detectar** 2 errores o **corregir** 1 error
- d_min ≥ 2t+1: puede **corregir** t errores

### [[core.lenguajes.LenguajeLongitudFija]]

- **Descripción**: Clase abstracta base para lenguajes donde todas las palabras tienen longitud fija
- **Hereda de**: `Lenguaje`
- **Capacidades adicionales**: Cálculo de distancia y peso de Hamming
- **Métodos**:
  - `distancia_hamming(palabra1, palabra2) -> int`: Calcula d_H
  - `distancia_minima() -> int`: Calcula d_min del código
  - `peso_hamming(palabra) -> int`: Calcula w_H
- **Estado**: ✅ Implementada

### [[core.lenguajes.LenguajeExplicitoLongitudFija]]

- **Descripción**: Lenguaje explícito con todas las palabras de la misma longitud
- **Hereda de**: `LenguajeLongitudFija`
- **Parámetros**: `(alfabeto: Alfabeto, palabras: Set[str], nombre: str = "")`
- **Validación**: Verifica que todas las palabras tengan la misma longitud
- **Ejemplo**:

  ```python
  # Código de repetición triple
  L = LenguajeExplicitoLongitudFija(binario, {"000", "111"}, "Rep-3")
  L.distancia_minima()  # → 3 (puede corregir 1 error)
  ```

- **Estado**: ✅ Implementada

**Nota**: `LenguajeExplicito` actúa como factory: si todas las palabras tienen la misma longitud, retorna automáticamente `LenguajeExplicitoLongitudFija`.

---

## 🔧 Semántica como Orden Parcial

### Concepto de Semántica

La **semántica** asocia significado a las palabras de un lenguaje mediante un **orden parcial** (L, ≤) donde:

- L es un lenguaje formal
- ≤ es una relación de orden parcial:
  - **Reflexiva**: w ≤ w
  - **Antisimétrica**: si w₁ ≤ w₂ y w₂ ≤ w₁ entonces w₁ = w₂
  - **Transitiva**: si w₁ ≤ w₂ y w₂ ≤ w₃ entonces w₁ ≤ w₃
- Tiene **elemento mínimo** ⊥ (bottom): ⊥ ≤ w para toda w ∈ L
- Tiene **elemento máximo** ⊤ (top): w ≤ ⊤ para toda w ∈ L
- Es **conexo**: no hay partes desconectadas (toda palabra es comparable con ⊥ y ⊤)

**Relaciones de orden**:

- w₁ < w₂: menor estrictamente
- w₁ = w₂: iguales según el orden
- w₁ > w₂: mayor estrictamente
- w₁ ⊥ w₂: incomparables (no relacionados)

### [[core.semantica.Semantica]]

- **Descripción**: Clase abstracta base para definir semántica como orden parcial
- **Parámetros**: `(lenguaje: Lenguaje)`
- **Métodos principales**:
  - `comparar(palabra1, palabra2) -> RelacionOrden`: Compara dos palabras
  - `es_menor()`, `es_igual()`, `es_mayor()`, `es_comparable()`
  - `minimo() -> str`: Retorna elemento ⊥
  - `maximo() -> str`: Retorna elemento ⊤
  - `supremo(conjunto) -> str`: Menor cota superior
  - `infimo(conjunto) -> str`: Mayor cota inferior
  - `ordenar(palabras) -> List[str]`: Ordena según el orden parcial
- **Estado**: ✅ Implementada

### [[core.semantica.SemanticaLexicografica]]

- **Descripción**: Orden lexicográfico según el alfabeto (como diccionario)
- **Parámetros**: `(lenguaje: Lenguaje, alfabeto: Alfabeto)`
- **Ejemplo**: En binario de longitud 3:
  - ⊥ = "000"
  - ⊤ = "111"
  - "001" < "010" < "011" < "100" < "101" < "110" < "111"
- **Estado**: ✅ Implementada

### [[core.semantica.SemanticaPesoHamming]]

- **Descripción**: Orden por peso de Hamming (número de símbolos no nulos)
- **Parámetros**: `(lenguaje: LenguajeLongitudFija)`
- **Características**:
  - Palabras con menor peso son menores
  - Palabras con mismo peso son incomparables
  - ⊥ = palabra de peso mínimo (todos ceros)
  - ⊤ = palabra de peso máximo (todos unos en binario)
- **Ejemplo**: "0000" < "0001" ⊥ "0010" < "0011" ⊥ "0101" < "1111"
- **Estado**: ✅ Implementada

### [[core.semantica.SemanticaLongitud]]

- **Descripción**: Orden por longitud de palabras
- **Parámetros**: `(lenguaje: Lenguaje)`
- **Características**:
  - Palabras más cortas son menores
  - Palabras de misma longitud son incomparables
- **Aplicación**: Lenguajes de longitud variable
- **Estado**: ✅ Implementada

### [[core.semantica.SemanticaPersonalizada]]

- **Descripción**: Orden definido por función de comparación personalizada
- **Parámetros**: `(lenguaje: Lenguaje, funcion_comparacion: Callable[[str, str], RelacionOrden])`
- **Uso**: Permite definir cualquier criterio de orden
- **Ejemplo**: Orden por suma de dígitos, número de transiciones, etc.
- **Estado**: ✅ Implementada

### Operaciones sobre órdenes parciales

**Supremo** (menor cota superior): Dado S ⊆ L, sup(S) es la menor palabra w tal que s ≤ w para todo s ∈ S

**Ínfimo** (mayor cota inferior): Dado S ⊆ L, inf(S) es la mayor palabra w tal que w ≤ s para todo s ∈ S

**Diagrama de Hasse**: Representación visual del orden parcial donde:

- Nodos = palabras del lenguaje
- Aristas = relaciones de orden inmediatas (sin transitividad)
- Niveles = palabras con misma "altura" en el orden

---

## 📚 Recursos Adicionales

- **Demos disponibles**:
  - `demos/demo_hamming.py` - Distancia de Hamming y códigos de error
  - `demos/demo_alfabeto_jerarquico.py` - Alfabetos multinivel
  - `demos/demo_semantica.py` - Órdenes parciales sobre lenguajes

## ✅ Estado de Desarrollo

- [x] Teoría documentada
- [x] Ejemplos añadidos
- [x] Funciones Python implementadas
  - [x] Alfabetos (básicos, estándar, binario, jerárquicos)
  - [x] Lenguajes (universo, predicado, autómata, explícito, vacío)
  - [x] Lenguajes de longitud fija con distancia de Hamming
  - [x] Operaciones sobre lenguajes (unión, intersección, complemento, etc.)
  - [x] Semántica como orden parcial (lexicográfico, peso Hamming, longitud, personalizado)
- [ ] Tests unitarios creados
