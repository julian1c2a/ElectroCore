# Distancia de Hamming y Análisis de Lenguajes

**Ruta:** [📚 Fundamentos de Electrónica](../../../index.md) > [Módulo 6: Fundamentos de Electrónica Digital](../../index.md) > [Sistemas de Representación de la Información](../index.md) > [Alfabetos, Lenguajes y Semántica](index.md)
[⬅️ Anterior](propiedades_de_codigos_adyacente_ciclico_saturado.md)

---

**ID:** `1.6.1.1.3`

## 📝 Contenido Teórico

### 1. Introducción

La **distancia de Hamming** es una métrica fundamental en teoría de la información y códigos detectores/correctores de errores. Fue introducida por Richard Hamming en 1950 como parte de su trabajo sobre detección y corrección de errores en sistemas de comunicación digital.

#### Definición Formal

> **Definición**: Sea Σ un alfabeto finito. La distancia de Hamming entre dos palabras x, y ∈ Σⁿ de igual longitud n es:
>
> ```
> d_H(x, y) = |{i : 1 ≤ i ≤ n, x_i ≠ y_i}|
> ```
>
> Es decir, el número de posiciones en las que x e y difieren.

#### Ejemplo Introductorio

Para cadenas binarias:

```
    Posición (columnas):
    0  1  2  3  4  5  6
x = 1  0  1  1  0  1  0
y = 1  0  0  1  1  1  0
    ✓ ✓  ✗  ✓ ✗  ✓  ✓ d_H(x,y) = 2
    Posición (columnas):
    0  1  2  3  4  5  6
w = 1  0  2  9  8  7  0
z = 1  0  0  9  3  7  0
    ✓ ✓  ✗  ✓ ✗  ✓  ✓ d_H(w,z) = 2
```

d_H(x, y) = 2 (difieren en las posiciones 2 y 4)

### 2. Propiedades Matemáticas

#### 2.1 La Distancia de Hamming es una Distancia Métrica

**Lema 1**: Aditividad de la distancia de Hamming en subpalabras de ancho fijho de $n$ dígitos, con subdivisiones de longitud $n-1$ dígitos y $1$ dígitos.

```Lemma
Sea $\Sigma$ un alfabeto finito.
Sea $k \in \SetNat$
Sea ${\Sigma}^k$ el conjunto de todas las palabras de longitud $k$ sobre el alfabeto $\Sigma$.
$∀ x y ∈ {\Sigma}^k$, sean $x = x_{0} · x_{[1:k-1]}$ y $y = y_{0} · y_{[1:k-1]}$ se cumple que:
    $d_H(x, y) = d_H(x_{0}, y_{0}) + d_H(x_{[1:k-1]}, y_{[1:k-1]})$
```

**Demostración**:

```Proof
Sean $x ∈ {\Sigma}^k$ y $y ∈ {\Sigma}^k$ dos palabras de longitud $k$.
Caso base: $k = 0$
    Si $k = 0$, entonces $x = ε$ y $y = ε$ (palabra vacía).
    Luego:
       $d_H(x, y) = d_H(ε, ε) = 0$
       $d_H(x_{0}, y_{0}) + d_H(x_{[1:k-1]}, y_{[1:k-1]}) = d_H(ε, ε) + d_H(ε, ε) 
                                                          = 0 + 0 
                                                          = 0$ ✓
    
    Por tanto, el caso base $k=0$ se cumple.
Caso base: $k = 1$
    Si $k = 1$, entonces $x = x_{0}$ y $y = y_{0}$.
    Luego:
        $d_H(x, y) = d_H(x_{0}, y_{0}) + d_H(x_{[1:0]}, y_{[1:0]})$ 
                  $= d_H(x_{0}, y_{0}) + d_H(ε, ε)$ 
                  $= d_H(x_{0}, y_{0}) + 0$ 
                  $= d_H(x, y)$  ✓
    
    Por tanto, el caso base $k=1$ se cumple.
Hipótesis de inducción:
    Supongamos que para $k = t > 1$ se cumple que:
        $∀ x y ∈ {\Sigma}^t$, sean $x = x[0] · x[1:t-1]$ y $y = y[0] · y[1:t-1]$ se cumple que:
            $d_H(x, y) = d_H(x[0], y[0]) + d_H(x[1:t-1], y[1:t-1])$
Paso inductivo:
    Debemos demostrar que para $k = t + 1$ se cumple la propiedad.
    
    Sean $x ∈ {\Sigma}^{t+1}$ y $y ∈ {\Sigma}^{t+1}$ dos palabras de longitud $t + 1$.
    Entonces $x = x[0] · x[1:t]$ y $y = y[0] · y[1:t]$.
    
    Por definición de distancia de Hamming sobre palabras concatenadas:
    Las posiciones de x e y son:
      - Posición 0: $x[0]$ vs $y[0]$
      - Posiciones 1 a t: $x[1:t]$ vs $y[1:t]$
    
    Luego:
        $d_H(x, y) = d_H(x[0] · x[1:t], y[0] · y[1:t])$ # Definición de la concatenación
                  $= |{i : 0 ≤ i ≤ t, (x[0]·x[1:t])ᵢ ≠ (y[0]·y[1:t])ᵢ}|$ # Definición de d_H
    
    Particionamos el conjunto de índices {0, 1, ..., t} = {0} ∪ {1, 2, ..., t} (disjuntos).
    Por propiedades de indexación de concatenación:
      - (x[0]·x[1:t])₀ = x[0]  y  (y[0]·y[1:t])₀ = y[0]
      - Para i ≥ 1: (x[0]·x[1:t])ᵢ = x[1:t]ᵢ₋₁  y  (y[0]·y[1:t])ᵢ = y[1:t]ᵢ₋₁
    
    Por tanto:
                  $= |{0 : x[0] ≠ y[0]}| + |{i : 1 ≤ i ≤ t, x[1:t]ᵢ₋₁ ≠ y[1:t]ᵢ₋₁}|$ # Partición disjunta
    
    Aplicamos la propiedad fundamental: $|A ∪ B| = |A| + |B| + |A ∩ B|$ para conjuntos disjuntos.
    Observamos que:
      - $|{0 : x[0] ≠ y[0]}| = d_H(x[0], y[0])$  [$x[0]$, $y[0]$ son símbolos únicos]
      - $|{i : 1 ≤ i ≤ t, x[1:t]ᵢ₋₁ ≠ y[1:t]ᵢ₋₁}| = d_H(x[1:t], y[1:t])$  [por def. de d_H sobre palabras]
    
    Por tanto:
                  $= d_H(x[0], y[0]) + d_H(x[1:t], y[1:t])$  ✓
    
    **Observación**: Este resultado muestra que la concatenación de palabras es un homomorfismo 
    respecto a la descomposición aditiva de la distancia de Hamming:
        d_H(u·v, u'·v') = d_H(u, u') + d_H(v, v')  cuando |u| = |u'| y |v| = |v'|
    
    Por tanto, el paso inductivo se cumple.
```

**Teorema 1**: La distancia Hamming de las subpalabras de ancho fijo menor que $n$ es estrictamente aditiva.

```Theorem
${\Sigma}^k$ es el conjunto de todas las palabras de longitud $k ∈ \SetNat$ sobre el alfabeto $\Sigma$.
Sean $n, m ∈ \SetNat$ con $n+m=k$
Sean $x, y ∈ {\Sigma}^k$ dos palabras de longitud $k$.
Sean $x = x[0:n-1] · x[n:k-1]$ y $y = y[0:n-1] · y[n:k-1]$
Entonces: d_H(x, y) = d_H(x[0:n-1], y[0:n-1]) + d_H(x[n:k-1], y[n:k-1])
```

**Demostración**:

```Proof
Por el Lema 1, sabemos que para cualquier palabra w de longitud k:
    d_H(w[0]·w[1:k-1], z[0]·z[1:k-1]) = d_H(w[0], z[0]) + d_H(w[1:k-1], z[1:k-1])

Demostraremos el teorema por inducción sobre n (longitud del prefijo).

Caso base (n = 0):
    Si n = 0, entonces x[0:n-1] = ε (palabra vacía) y x[n:k-1] = x (palabra completa).
    Luego:
        d_H(x, y) = d_H(ε·x, ε·y) = d_H(ε, ε) + d_H(x, y) = 0 + d_H(x, y)  ✓

Caso base (n = 1):
    Si n = 1, entonces x = x[0]·x[1:k-1] y y = y[0]·y[1:k-1].
    Por Lema 1:
        d_H(x, y) = d_H(x[0], y[0]) + d_H(x[1:k-1], y[1:k-1])  ✓

Hipótesis de inducción:
    Supongamos que para n = t se cumple:
        d_H(x, y) = d_H(x[0:t-1], y[0:t-1]) + d_H(x[t:k-1], y[t:k-1])

Paso inductivo (n = t + 1):
    Sean x, y palabras de longitud k, con descomposición x[0:t]·x[t+1:k-1].
    
    Aplicamos Lema 1 con prefijo de longitud 1:
        d_H(x, y) = d_H(x[0]·x[1:k-1], y[0]·y[1:k-1])
                  = d_H(x[0], y[0]) + d_H(x[1:k-1], y[1:k-1])
    
    Ahora, sobre x[1:k-1] (que tiene longitud k-1), aplicamos la HI con n' = t:
        d_H(x[1:k-1], y[1:k-1]) = d_H(x[1:t], y[1:t]) + d_H(x[t+1:k-1], y[t+1:k-1])
    
    Sustituyendo:
        d_H(x, y) = d_H(x[0], y[0]) + d_H(x[1:t], y[1:t]) + d_H(x[t+1:k-1], y[t+1:k-1])
                  = d_H(x[0:t], y[0:t]) + d_H(x[t+1:k-1], y[t+1:k-1])  ✓
    
    Por tanto, el resultado se cumple para n = t + 1.

Por inducción matemática, el teorema se cumple para todo n ∈ ℕ con 0 ≤ n ≤ k.
```

**Observación**: Este teorema muestra que la distancia de Hamming se comporta aditivamente
sobre cualquier partición de las palabras en subpalabras contiguas. Es decir, para cualquier
descomposición x = x₁·x₂·...·xₘ con |xᵢ| = nᵢ y Σnᵢ = k:
    d_H(x, y) = Σᵢ d_H(xᵢ, yᵢ)

Esta propiedad es fundamental para el análisis de códigos de bloque.

#### 2.2 La Distancia de Hamming es una Métrica

**Teorema 2**: La distancia de Hamming d_H define una métrica sobre Σⁿ.

Para demostrar que d_H es una métrica, debemos probar que satisface las tres propiedades de una métrica:

##### Propiedad M1: No Negatividad e Identidad

```

∀x, y ∈ Σⁿ: d_H(x, y) ≥ 0
∀x, y ∈ Σⁿ: d_H(x, y) = 0 ⟺ x = y

```

**Demostración**:

- **No negatividad**: d_H(x, y) cuenta elementos, por tanto d_H(x, y) ≥ 0
- **Identidad**:
  - (⟹) Si x = y, entonces ∀i: x_i = y_i, luego no hay posiciones diferentes, d_H(x, y) = 0
  - (⟸) Si d_H(x, y) = 0, no hay posiciones diferentes, luego ∀i: x_i = y_i, por tanto x = y
- **Positividad**: Por inducción, si $x, y ∈ Σ^1$, y $x \neq y$ entonces $x_0 ≠ y_0$. $d_H(x, y) = 1$
  - Hipótesis de inducción: Supongamos que para $n=k$ se cumple que si $x, y ∈ Σ^k$ y $x \neq y$ entonces $d_H(x, y) ≥ 1$
  - Paso inductivo: Para $n=k+1$, sean $x, y ∈ Σ^{k+1}$ y $x \neq y$. Entonces $d_H(x, y) = d_H(x[0:k-1], y[0:k-1]) + d_H(x[k],y[k])$. Hay 3 casos posibles:
    - $x[0:k-1] = y[0:k-1]$, entonces $x[k] \neq y[k]$ y por el caso base $d_H(x[0:k], y[0:k]) = d_H(x[0:k-1],y[0:k-1]) + d_H(x[k],y[k]) = 0 + 1 = 1 \le 1$, luego $d_H(x, y) = d_H(x[0:k], y[0:k]) ≥ 1$.
    - $x[0:k-1] \neq y[0:k-1]$, entonces por hipótesis de inducción $d_H(x[0:k-1], y[0:k-1]) ≥ 1$ y $d_H(x[k],y[k]) \le 0$, luego $d_H(x, y) = d_H(x[0:k], y[0:k]) = d_H(x[0:k-1], y[0:k-1]) + d_H(x[k],y[k]) ≥ 1 + 0 = 1$.
    -

□

##### Propiedad M2: Simetría

```

∀x, y ∈ Σⁿ: d_H(x, y) = d_H(y, x)

```

**Demostración**:

```

d_H(x, y) = |{i : x_i ≠ y_i}|
          = |{i : y_i ≠ x_i}|    (la desigualdad es simétrica)
          = d_H(y, x)

```

□

##### Propiedad M3: Desigualdad Triangular

```

∀x, y, z ∈ Σⁿ: d_H(x, z) ≤ d_H(x, y) + d_H(y, z)

```

**Demostración**:

Sea I_{xy} = {i : x_i ≠ y_i}, I_{yz} = {i : y_i ≠ z_i}, I_{xz} = {i : x_i ≠ z_i}

Para cada posición i hay tres casos:

1. **x_i = y_i = z_i**: i ∉ I_{xy} ∪ I_{yz} ∪ I_{xz}
2. **Dos son iguales, uno diferente**:
   - Si x_i = y_i ≠ z_i: entonces i ∈ I_{yz} ∩ I_{xz}, pero i ∉ I_{xy}
   - Si x_i = z_i ≠ y_i: entonces i ∈ I_{xy} ∩ I_{yz}, pero i ∉ I_{xz}
   - Si y_i = z_i ≠ x_i: entonces i ∈ I_{xy} ∩ I_{xz}, pero i ∉ I_{yz}
3. **Todos diferentes**: x_i ≠ y_i ≠ z_i ≠ x_i: entonces i ∈ I_{xy} ∩ I_{yz}

En todos los casos: Si i ∈ I_{xz}, entonces i ∈ I_{xy} ∪ I_{yz}

Por tanto: I_{xz} ⊆ I_{xy} ∪ I_{yz}

Luego: |I_{xz}| ≤ |I_{xy} ∪ I_{yz}| ≤ |I_{xy}| + |I_{yz}|

Es decir: d_H(x, z) ≤ d_H(x, y) + d_H(y, z)
□

**Conclusión**: Hemos demostrado que la distancia de Hamming es una métrica formal. Esta demostración está implementada como prueba formal en el sistema de lógica matemática del proyecto (ver sección de demostraciones formales).

#### 2.3 Peso de Hamming

**Definición**: El **peso de Hamming** de una palabra x ∈ Σⁿ, denotado w_H(x), es el número de posiciones no nulas (diferentes del símbolo cero del alfabeto):

```
w_H(x) = |{i : x_i ≠ 0}|
```

Para alfabetos binarios Σ = {0, 1}: w_H(x) = número de unos en x

**Ejemplos**:

- w_H(0000) = 0
- w_H(1010) = 2
- w_H(1111) = 4
- w_H(10110101) = 5

**Proposición 1**: El peso de Hamming es la distancia al origen

```
∀x ∈ Σⁿ: w_H(x) = d_H(x, 0ⁿ)
```

**Demostración**:

```Proof
Sea 0ⁿ = 00...0 (n ceros) la palabra nula.

Por definición de distancia de Hamming:
    d_H(x, 0ⁿ) = |{i : x_i ≠ 0}|

Por definición de peso de Hamming:
    w_H(x) = |{i : x_i ≠ 0}|

Por tanto: w_H(x) = d_H(x, 0ⁿ)  ✓
```

**Teorema 3** (Relación peso-distancia en alfabetos con estructura de grupo):

Para alfabetos con operación de grupo (Σ, ⊕), en particular para F₂ = {0,1} con XOR:

```
∀x, y ∈ Σⁿ: d_H(x, y) = w_H(x ⊕ y)
```

donde (x ⊕ y)ᵢ = xᵢ ⊕ yᵢ (operación componente a componente)

**Demostración**:

```Proof
Sea z = x ⊕ y, donde zᵢ = xᵢ ⊕ yᵢ para cada posición i.

Por definición de distancia de Hamming:
    d_H(x, y) = |{i : x_i ≠ y_i}|

Por propiedades de la operación XOR en F₂:
    x_i ≠ y_i ⟺ x_i ⊕ y_i = 1
    x_i = y_i ⟺ x_i ⊕ y_i = 0

Por tanto:
    {i : x_i ≠ y_i} = {i : (x ⊕ y)ᵢ ≠ 0} = {i : z_i ≠ 0}

Luego:
    d_H(x, y) = |{i : x_i ≠ y_i}|
              = |{i : z_i ≠ 0}|
              = w_H(z)
              = w_H(x ⊕ y)  ✓
```

**Aplicación práctica**: En circuitos digitales, d_H(x, y) se puede calcular como:

1. Aplicar XOR bit a bit: z = x ⊕ y
2. Contar los unos en z (circuito contador de población/"popcount")

**Propiedades del peso de Hamming**:

1. **No negatividad**: w_H(x) ≥ 0 para todo x
2. **Nulidad**: w_H(x) = 0 ⟺ x = 0ⁿ
3. **Aditividad** (en F₂): w_H(x ⊕ y) ≤ w_H(x) + w_H(y) (desigualdad triangular trasladada)
4. **Invariancia por permutación**: w_H(π(x)) = w_H(x) para cualquier permutación π

#### 2.4 Esferas de Hamming y Volumen

**Definición**: La **esfera de Hamming** de radio r centrada en x es:

```
B(x, r) = {y ∈ Σⁿ : d_H(x, y) ≤ r}
```

Es el conjunto de todas las palabras a distancia ≤ r de x.

**Teorema 4** (Volumen de esferas de Hamming):

El número de palabras en una esfera de radio r es:

```
V(n, r) = |B(x, r)| = Σᵢ₌₀ʳ C(n, i) · (|Σ| - 1)ⁱ
```

donde C(n, i) = (n choose i) = n!/(i!(n-i)!)

**Demostración**:

```Proof
El volumen V(n, r) es independiente del centro x (por invariancia translacional de la métrica).
Tomemos x = 0ⁿ sin pérdida de generalidad.

Una palabra y está en B(0ⁿ, r) si y solo si w_H(y) ≤ r.

Para cada distancia exacta i (con 0 ≤ i ≤ r), contamos cuántas palabras tienen exactamente i símbolos no nulos:

1. **Elegir posiciones**: Hay C(n, i) formas de elegir i posiciones de n
2. **Elegir símbolos no nulos**: Para cada posición elegida, hay (|Σ| - 1) opciones 
   (cualquier símbolo excepto 0)
3. **Posiciones restantes**: Las n - i posiciones restantes deben ser 0

Por tanto, hay C(n, i) · (|Σ| - 1)ⁱ palabras a distancia exactamente i.

Sumando sobre todas las distancias de 0 a r:
    V(n, r) = Σᵢ₌₀ʳ C(n, i) · (|Σ| - 1)ⁱ  ✓
```

**Caso particular** (alfabeto binario Σ = {0, 1}):

```
V(n, r) = Σᵢ₌₀ʳ C(n, i)
```

**Ejemplos**:

Para n = 5, Σ = {0, 1}:

- V(5, 0) = C(5,0) = 1 (solo la palabra central)
- V(5, 1) = C(5,0) + C(5,1) = 1 + 5 = 6
- V(5, 2) = 1 + 5 + 10 = 16
- V(5, 5) = 2⁵ = 32 (todo el espacio)

**Teorema 5** (Hamming Bound o Sphere-Packing Bound):

Sea C ⊆ Σⁿ un código con distancia mínima $d_{min} = 2t + 1$ (corrige hasta t errores).
Entonces:

```
|C| ≤ |Σ|ⁿ / V(n, t)
```

**Demostración**:

```Proof
Si C corrige hasta t errores, entonces las esferas B(c, t) centradas en cada palabra-código c ∈ C 
deben ser disjuntas (no solapadas).

**Justificación**: Supongamos que B(c₁, t) ∩ B(c₂, t) ≠ ∅ para c₁ ≠ c₂.
Entonces existe y tal que d_H(y, c₁) ≤ t y d_H(y, c₂) ≤ t.
Por desigualdad triangular:
    d_H(c₁, c₂) ≤ d_H(c₁, y) + d_H(y, c₂) ≤ t + t = 2t

Pero $d_{min} = 2t + 1$, contradicción. Por tanto, las esferas son disjuntas.

Como hay |C| palabras-código y cada esfera tiene volumen V(n, t):
    |C| · V(n, t) ≤ |Σⁿ| = |Σ|ⁿ

Dividiendo por V(n, t):
    |C| ≤ |Σ|ⁿ / V(n, t)  ✓
```

**Interpretación**: Este teorema establece un **límite superior** para el número de palabras-código que puede tener un código con capacidad de corrección t. Es una restricción fundamental en teoría de códigos.

**Definición**: Un código que alcanza la igualdad |C| = |Σ|ⁿ / V(n, t) se llama **código perfecto**, porque las esferas de radio t "empacan" completamente el espacio Σⁿ sin huecos ni solapamientos.

**Ejemplos de códigos perfectos**:

- Códigos de Hamming ($d_{min} = 3$, t = 1)
- Código de Golay binario [23, 12, 7]
- Código de repetición [n, 1, n] con n impar

#### 2.5 Distancia Promedio

**Definición**: La **distancia promedio** entre dos palabras aleatorias uniformemente distribuidas en Σⁿ es:

```
E[d_H(X, Y)] = Valor esperado de d_H cuando X, Y ~ Uniforme(Σⁿ)
```

**Teorema 6** (Distancia promedio):

Para X, Y palabras aleatorias independientes uniformemente distribuidas en Σⁿ:

```
E[d_H(X, Y)] = n · (|Σ| - 1) / |Σ| = n · (1 - 1/|Σ|)
```

**Demostración**:

```Proof
Por linealidad de la esperanza y la definición de d_H:
    E[d_H(X, Y)] = E[Σᵢ₌₀ⁿ⁻¹ 𝟙{Xᵢ ≠ Yᵢ}]
                  = Σᵢ₌₀ⁿ⁻¹ E[𝟙{Xᵢ ≠ Yᵢ}]
                  = Σᵢ₌₀ⁿ⁻¹ P(Xᵢ ≠ Yᵢ)

Para cada posición i:
    P(Xᵢ = Yᵢ) = Σₛ∈Σ P(Xᵢ = s) · P(Yᵢ = s)
                = Σₛ∈Σ (1/|Σ|) · (1/|Σ|)    [por independencia y uniformidad]
                = |Σ| · (1/|Σ|²)
                = 1/|Σ|

Por tanto:
    P(Xᵢ ≠ Yᵢ) = 1 - P(Xᵢ = Yᵢ) = 1 - 1/|Σ| = (|Σ| - 1)/|Σ|

Sustituyendo:
    E[d_H(X, Y)] = Σᵢ₌₀ⁿ⁻¹ (|Σ| - 1)/|Σ|
                  = n · (|Σ| - 1)/|Σ|  ✓
```

**Casos particulares**:

1. **Alfabeto binario** (Σ = {0, 1}, |Σ| = 2):

   ```
   E[d_H(X, Y)] = n · 1/2 = n/2
   ```

   Interpretación: En promedio, dos palabras binarias aleatorias difieren en la mitad de sus bits.

2. **Alfabeto cuaternario** (Σ = {0, 1, 2, 3}, |Σ| = 4):

   ```
   E[d_H(X, Y)] = n · 3/4 = 3n/4
   ```

3. **Alfabeto general de tamaño q**:

   ```
   E[d_H(X, Y)] = n(q-1)/q
   ```

**Varianza de la distancia de Hamming**:

```Proposition
Var[d_H(X, Y)] = n · P(Xᵢ ≠ Yᵢ) · P(Xᵢ = Yᵢ)
                = n · (|Σ| - 1)/|Σ| · 1/|Σ|
                = n(|Σ| - 1)/|Σ|²
```

Para alfabeto binario: Var[d_H(X, Y)] = n/4

**Aplicación práctica**:

La distancia promedio proporciona una **línea base** para evaluar códigos:

- Si $d_{min}$ de un código es mucho mayor que E[d_H], el código tiene buena separación
- Para códigos binarios de longitud n, queremos $d_{min} >> n/2$ para robustez

**Ejemplo**:

- Código con n = 16, $d_{min} = 8$: Está en E[d_H] = 8 (apenas adecuado)
- Código con n = 16, $d_{min} = 12$: Está bien por encima del promedio (excelente)

### 3. Distancia Mínima de un Lenguaje

#### Definición

Sea L ⊆ Σⁿ un lenguaje (conjunto de palabras de longitud n). La **distancia mínima** de L es:

```

$d_{min}(L) = min\{d_H(x, y) : x, y \in L, x \neq y\}$

```

#### Importancia

La distancia mínima determina la **capacidad de detección y corrección de errores**:

| $d_{min}$ | Capacidad |
|-------|-----------|
| $d_{min} = 1$ | No detecta errores (palabras adyacentes) |
| $d_{min} = 2$ | Detecta 1 error |
| $d_{min} = 3$ | Detecta 2 errores, corrige 1 error |
| $d_{min} = 4$ | Detecta 3 errores, corrige 1 error |
| $d_{min} = 2t+1$ | Corrige hasta t errores |
**Teorema 2**: Un código con distancia mínima d puede:

- **Detectar** hasta d-1 errores
- **Corregir** hasta ⌊(d-1)/2⌋ errores

#### Ejemplo: Código de Repetición Triple

```python
L = {000, 111}  # Alfabeto Σ = {0, 1}
$d_{min}(L) = d_H(000, 111) = 3$
```

Este código puede:

- Detectar hasta 2 errores
- Corregir 1 error (por votación mayoritaria)

Ejemplo de corrección:

```
Enviado:  111
Recibido: 101  (error en posición 2)
Decodificación: 
  d_H(101, 000) = 2
  d_H(101, 111) = 1  ← más cercano
Resultado: 111 (correcto)
```

### 4. Esferas de Hamming

#### Definición

La **esfera de Hamming** de radio r centrada en x es:

```
S_r(x) = {y ∈ Σⁿ : d_H(x, y) ≤ r}
```

El conjunto de todas las palabras a distancia como máximo r de x.

#### Volumen de una Esfera

Para el alfabeto binario Σ = {0, 1}:

```
|S_r(x)| = Σ(i=0 to r) C(n, i)
```

donde C(n, i) es el coeficiente binomial.

**Justificación**: Hay C(n, i) formas de elegir i posiciones de n para cambiar.

Ejemplo para n=7, r=1:

```
|S_1(x)| = C(7,0) + C(7,1) = 1 + 7 = 8
```

(la palabra original + 7 palabras con 1 bit cambiado)

### 5. Cota de Hamming

**Teorema 3 (Cota de Hamming)**:

Para un código C ⊆ {0,1}ⁿ con distancia mínima d = 2t+1:

```
|C| · Σ(i=0 to t) C(n, i) ≤ 2ⁿ
```

**Interpretación**: Las esferas de radio t alrededor de cada palabra código no se solapan, y todas deben caber en el espacio {0,1}ⁿ.

**Código perfecto**: Cuando se alcanza la igualdad, el código se llama **perfecto**. Ejemplos:

- Código de Hamming (7,4): n=7, t=1, |C|=16
- Código de Golay (23,12): n=23, t=3, |C|=4096

### 6. Aplicaciones Prácticas

#### 6.1 Detección de Errores

La distancia de Hamming se usa en:

- **Códigos de paridad**: $d_{min} = 2$ (detecta 1 error)
- **CRC (Cyclic Redundancy Check)**: detecta ráfagas de errores
- **Checksums**: verificación de integridad

#### 6.2 Corrección de Errores

Códigos correctores:

- **Hamming (7,4)**: 4 bits de datos + 3 de paridad, corrige 1 error
- **Reed-Solomon**: usado en CD, DVD, QR codes
- **Turbo codes**: telecomunicaciones 4G/5G
- **LDPC**: WiFi, televisión digital

#### 6.3 Bioinformática

Comparación de secuencias de ADN:

```
Secuencia 1: ACGTACGT
Secuencia 2: ACGTAGGT
d_H = 2 (diferencias en posiciones 6 y 7)
```

#### 6.4 Procesamiento de Imágenes

Detección de similitud entre imágenes usando hashing perceptual.

### 7. Códigos Gray

Los **códigos Gray** son una aplicación especial donde palabras adyacentes tienen d_H = 1.

#### Código Gray de 3 bits

| Decimal | Binario | Gray |
|---------|---------|------|
| 0 | 000 | 000 |
| 1 | 001 | 001 |
| 2 | 010 | 011 |
| 3 | 011 | 010 |
| 4 | 100 | 110 |
| 5 | 101 | 111 |
| 6 | 110 | 101 |
| 7 | 111 | 100 |

**Propiedad**: Cada transición cambia exactamente 1 bit.

**Aplicaciones**:

- Encoders rotativos
- Conversión A/D
- Minimización de errores en transiciones

### 8. Relación con Códigos de Bloque

Un **código de bloque (n, k)** codifica k bits de información en n bits (n > k).

**Tasa de código**: R = k/n

**Redundancia**: n - k bits

**Objetivo**: Maximizar R manteniendo $d_{min}$ grande.

#### Ejemplo: Hamming (7,4)

```
n = 7 bits totales
k = 4 bits de datos
Redundancia = 3 bits de paridad
R = 4/7 ≈ 0.57
$d_{min} = 3$ (corrige 1 error)
```

### 9. Algoritmos de Cálculo

#### Algoritmo 1: Cálculo Directo

```python
def hamming_distance(x: str, y: str) -> int:
    """Calcula la distancia de Hamming entre dos cadenas."""
    if len(x) != len(y):
        raise ValueError("Las cadenas deben tener la misma longitud")
    
    return sum(c1 != c2 for c1, c2 in zip(x, y))
```

**Complejidad**: O(n)

#### Algoritmo 2: Usando XOR (para binarias)

```python
def hamming_distance_xor(x: int, y: int) -> int:
    """Distancia de Hamming usando XOR para números binarios."""
    xor = x ^ y
    count = 0
    while xor:
        count += xor & 1
        xor >>= 1
    return count
```

**Complejidad**: O(log n)

#### Algoritmo 3: Distancia Mínima de un Código

```python
def min_distance(code: list[str]) -> int:
    """Calcula la distancia mínima de un código."""
    n = len(code)
    if n < 2:
        return float('inf')
    
    min_dist = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            dist = hamming_distance(code[i], code[j])
            min_dist = min(min_dist, dist)
    
    return min_dist
```

**Complejidad**: O(n² · m) donde n = |código|, m = longitud de palabra

### 10. Teoremas Avanzados

#### Teorema 4 (Cota de Singleton)

```
|C| ≤ |Σ|^(n-d+1)
```

Para un código con distancia mínima d.

#### Teorema 5 (Cota de Plotkin)

Para códigos binarios con d > n/2:

```
|C| ≤ 2d / (2d - n)
```

#### Teorema 6 (Cota de Elias-Bassalygo)

Para un código binario C de longitud n con distancia mínima d:

```
|C| ≤ 2^n / (V(n, ⌊(d-1)/2⌋) · (1 - R(δ)))
```

donde:

- δ = d/n es la **distancia relativa**
- R(δ) es una función relacionada con la entropía binaria
- V(n, r) es el volumen de una esfera de Hamming de radio r

**Forma alternativa** usando la función de entropía binaria H(p) = -p log₂(p) - (1-p) log₂(1-p):

Para δ ≤ 1/2 y códigos suficientemente largos:

```
|C| ≤ 2^(n(1 - H(δ/2) + o(1)))
```

**Interpretación**: Esta cota mejora la cota de Hamming para códigos con distancia relativa moderada, proporcionando un límite más ajustado sobre el tamaño máximo del código.

**Aplicación**: Es especialmente útil para analizar códigos asintóticamente buenos y establecer límites en la teoría de códigos algebraicos.

### 11. Espacio Métrico de Hamming

El par (Σⁿ, d_H) forma un **espacio métrico**:

**Propiedades topológicas**:

- Espacio discreto (todas las distancias son enteras)
- **No es ultramétrica**: La distancia de Hamming no satisface la desigualdad triangular fuerte d(x,z) ≤ max(d(x,y), d(y,z)). Contraejemplo: x=000, y=111, z=100 da d(x,y)=3 > max(d(x,z), d(y,z))=max(1,2)=2
- Esferas son conjuntos finitos
- No es un espacio normado (no hay noción de "longitud")

**Embedding**: El espacio de Hamming puede embeberse en ℝⁿ con la métrica l₁.

### 12. Comparación con Otras Métricas

| Métrica | Definición | Uso |
|---------|------------|-----|
| **Hamming** | Número de posiciones diferentes | Cadenas de igual longitud |
| **Levenshtein** | Mín. operaciones (ins/del/sust) | Cadenas de distinta longitud |
| **Jaccard** | 1 - |A∩B|/|A∪B| | Conjuntos |
| **Coseno** | 1 - cos(θ) | Vectores (similitud) |
| **Euclidiana** | √Σ(xi-yi)² | Vectores en ℝⁿ |

**Nota**: Hamming es un caso especial de Levenshtein cuando solo se permiten sustituciones.

### 13. Demostración Formal Computacional

Este proyecto incluye una **demostración formal completa** de que la distancia de Hamming es una métrica, implementada en el sistema de lógica matemática:

```bash
cd demos
python demo_hamming_metrica.py
```

El demo demuestra formalmente:

1. ✓ No negatividad e identidad: d(x,y) ≥ 0 y d(x,y)=0 ⟺ x=y
2. ✓ Simetría: d(x,y) = d(y,x)
3. ✓ Desigualdad triangular: d(x,z) ≤ d(x,y) + d(y,z)

Además valida las propiedades con ejemplos computacionales sobre cadenas binarias.

**Ubicación del código**: `core/math_logic_system/` contiene el sistema completo de lógica formal que permite construir y verificar demostraciones matemáticas rigurosas.

### Resumen

La distancia de Hamming es fundamental para:

- ✅ Teoría de códigos correctores de errores
- ✅ Detección y corrección automática de errores
- ✅ Diseño de sistemas de comunicación robustos
- ✅ Bioinformática y comparación de secuencias
- ✅ Criptografía y hashing

Su caracterización como métrica formal garantiza propiedades matemáticas sólidas que sustentan su uso en aplicaciones críticas.

## 🔧 Funciones Python Asociadas

### Módulos Implementados

#### 1. `core/formal_languages.py`

Funciones básicas para trabajar con lenguajes formales y distancia de Hamming:

```python
from core.formal_languages import hamming_distance, min_distance_of_language

# Calcular distancia entre dos palabras
d = hamming_distance("10110", "10010")  # 1

# Distancia mínima de un código
code = ["000", "111", "101", "010"]
d_min = min_distance_of_language(code)  # 2
```

#### 2. `demos/demo_hamming_metrica.py`

Demostración formal completa que prueba que la distancia de Hamming es una métrica:

```python
from demos.demo_hamming_metrica import (
    create_metric_space_axioms,
    prove_hamming_is_metric,
    validate_with_examples
)

# Crear sistema de axiomas de espacio métrico
axioms = create_metric_space_axioms()

# Demostrar formalmente que Hamming es métrica
theorems = prove_hamming_is_metric(axioms)

# Validar con ejemplos
validate_with_examples()
```

**Salida**: Prueba formal paso a paso de cada propiedad métrica.

#### 3. `core/math_logic_system/`

Sistema completo de lógica matemática para demostraciones formales:

```python
from core.math_logic_system import (
    AxiomSystem, Proof, Theorem, 
    ProofVerifier, ModusPonens
)

# Crear sistema axiomático
system = AxiomSystem("Espacios Métricos", "...")

# Construir demostración
proof = Proof(goal, "Hamming es métrica")
# ... añadir pasos ...

# Verificar corrección
verifier = ProofVerifier(system)
if verifier.verify(proof):
    print("✓ Demostración válida")
```

### Ejemplos de Uso

#### Ejemplo 1: Cálculo Básico

```python
# Distancia entre cadenas binarias
x = "1011010"
y = "1001011"

d = hamming_distance(x, y)
print(f"Distancia: {d}")  # 3

# Posiciones diferentes
differences = [(i, x[i], y[i]) for i in range(len(x)) if x[i] != y[i]]
print(f"Difieren en: {differences}")
# [(2, '1', '0'), (4, '0', '1'), (6, '0', '1')]
```

#### Ejemplo 2: Código de Hamming (7,4)

```python
# Código de Hamming con 16 palabras
hamming_7_4 = [
    "0000000", "1101000", "0110100", "1011100",
    "0011010", "1110010", "0101110", "1000110",
    "0001101", "1100101", "0111001", "1010001",
    "0010111", "1111111", "0100011", "1001011"
]

# Calcular distancia mínima
d_min = min_distance_of_language(hamming_7_4)
print(f"Distancia mínima: {d_min}")  # 3

# Capacidad de corrección
t = (d_min - 1) // 2
print(f"Corrige hasta {t} errores")  # 1
```

#### Ejemplo 3: Esfera de Hamming

```python
from core.formal_languages import hamming_sphere

# Esfera de radio 1 alrededor de "101"
center = "101"
radius = 1
sphere = hamming_sphere(center, radius)

print(f"S_{radius}({center}) = {sphere}")
# {'101', '001', '111', '100'}

print(f"|S_{radius}({center})| = {len(sphere)}")  # 4
# Verificación: C(3,0) + C(3,1) = 1 + 3 = 4 ✓
```

#### Ejemplo 4: Corrección de Errores

```python
def decode_nearest_neighbor(received, code):
    """Decodifica usando el vecino más cercano."""
    min_dist = float('inf')
    closest = None
    
    for codeword in code:
        d = hamming_distance(received, codeword)
        if d < min_dist:
            min_dist = d
            closest = codeword
    
    return closest, min_dist

# Código de repetición triple
code = ["000", "111"]

# Palabra recibida con error
received = "101"

decoded, dist = decode_nearest_neighbor(received, code)
print(f"Recibido: {received}")
print(f"Decodificado: {decoded}")  # "111"
print(f"Distancia: {dist}")  # 1
```

#### Ejemplo 5: Verificación de Propiedades

```python
from demos.demo_hamming_metrica import validate_metric_properties

# Verificar propiedades métricas con ejemplos aleatorios
words = ["0000", "1111", "1010", "0101"]
validate_metric_properties(words)

# Salida:
# ✓ No negatividad: d(x,y) ≥ 0
# ✓ Identidad: d(x,x) = 0
# ✓ Simetría: d(x,y) = d(y,x)
# ✓ Desigualdad triangular: d(x,z) ≤ d(x,y) + d(y,z)
```

### Ejecución de Demos

```bash
# Demostración formal completa
cd demos
python demo_hamming_metrica.py

# Sistema de lógica matemática
python -c "from core.math_logic_system import PeanoArithmetic; p = PeanoArithmetic(); p.show_axioms()"
```

## 📚 Recursos Adicionales

### Referencias Académicas

1. **Hamming, R.W.** (1950). "Error detecting and error correcting codes". *Bell System Technical Journal*, 29(2):147-160.
   - Artículo original que introduce la distancia de Hamming

2. **MacWilliams, F.J. & Sloane, N.J.A.** (1977). *The Theory of Error-Correcting Codes*. North-Holland.
   - Tratado completo sobre códigos correctores

3. **Lin, S. & Costello, D.J.** (2004). *Error Control Coding* (2nd ed.). Prentice Hall.
   - Texto moderno sobre teoría de códigos

4. **Roth, R.M.** (2006). *Introduction to Coding Theory*. Cambridge University Press.
   - Introducción matemática rigurosa

### Recursos en Línea

- [Wikipedia: Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance)
- [Stanford CS259: Information Theory](https://web.stanford.edu/class/cs259/)
- [MIT 6.02: Introduction to EECS II (Coding Theory)](https://ocw.mit.edu/)

### Implementaciones de Referencia

- **SciPy**: `scipy.spatial.distance.hamming`
- **NumPy**: Cálculo vectorizado
- **Hamming**: Librería especializada en Python

### Material del Proyecto

- **Código fuente**: `core/formal_languages.py`, `core/math_logic_system/`
- **Demos**: `demos/demo_hamming_metrica.py`
- **Tests**: `tests/test_formal_languages.py`
- **Documentación API**: `core/math_logic_system/README.md`

## ✅ Estado de Desarrollo

- [x] Teoría documentada
  - [x] Definición formal
  - [x] Demostración de propiedades métricas
  - [x] Aplicaciones y ejemplos
  - [x] Teoremas avanzados
  - [x] Algoritmos de cálculo
  
- [x] Ejemplos añadidos
  - [x] Cálculo básico
  - [x] Códigos correctores (Hamming 7,4)
  - [x] Esferas de Hamming
  - [x] Corrección de errores
  - [x] Código Gray
  
- [x] Funciones Python implementadas
  - [x] `hamming_distance()` - Cálculo básico
  - [x] `min_distance_of_language()` - Distancia mínima
  - [x] `hamming_sphere()` - Esfera de radio r
  - [x] `decode_nearest_neighbor()` - Decodificación
  
- [x] Sistema de demostración formal
  - [x] Demostración de que Hamming es métrica
  - [x] Verificador automático de pruebas
  - [x] Biblioteca de teoremas reutilizables
  
- [x] Tests unitarios creados
  - [x] Tests para `hamming_distance()`
  - [x] Tests para propiedades métricas
  - [x] Tests para códigos correctores
  - [x] Tests de integración

### Próximas Mejoras

- [ ] Visualización de esferas de Hamming
- [ ] Implementación de códigos de Hamming (n,k) generales
- [ ] Algoritmos de decodificación eficientes
- [ ] Comparación de rendimiento con otras métricas
- [ ] Integración con módulos de códigos especializados (BCD, Gray, etc.)

---

**Última actualización**: Enero 2026  
**Estado**: ✅ Documentación completa con demostraciones formales
